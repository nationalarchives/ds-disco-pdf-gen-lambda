import math
import os
import urllib
import json
import boto3
import zipfile
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
from botocore.exceptions import ClientError

if "DIGITAL_METADATA_API" in os.environ:
    s3_bucket_get = os.environ['S3_BUCKET_NAME_GET']
    s3_bucket_put = os.environ['S3_BUCKET_NAME_PUT']
    metadata_api = os.environ['DIGITAL_METADATA_API']
    role_arn = os.environ['S3_CROSS_ACCOUNT_ROLE_ARN']
    client = boto3.client('sts')
    sts_response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='cross_acct_lambda',
        DurationSeconds=900
    )
    ACCESS_KEY = sts_response['Credentials']['AccessKeyId']
    SECRET_KEY = sts_response['Credentials']['SecretAccessKey']
    SESSION_TOKEN = sts_response['Credentials']['SessionToken']
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
else:
    s3_bucket_get = 0
    s3_bucket_put = 0
    metadata_api = 0
    role_arn = 0


def get_replica(rid):
    with urllib.request.urlopen(metadata_api + 'replicas/' + rid) as content_file:
        json_content = content_file.read()
    content = json.loads(json_content)
    replica = Replica(content)
    return replica


class Replica:
    def __init__(self, content):
        self.replica_data = content

    def process_files(self, delivery_type, max_deliveryfile_size, reference, iaid):
        # TODO Code the ZIP case. Can any of the PDF case be generalised?
        status = False
        if delivery_type == "pdf":
            status = self._create_pdf(max_deliveryfile_size, reference, iaid)
        else:
            status = self._create_zip(max_deliveryfile_size, reference, iaid)
        return status

    def _create_file_list(self, max_deliveryfile_size, data):
        output_file_list = []
        size = 0
        this_pdf = []
        length = len(data)
        count = 1
        for file in data:
            this_pdf.append(file['name'])
            size = file['size'] + size
            if size > max_deliveryfile_size:
                output_file_list.append(this_pdf)
                size = 0
                this_pdf = []
            elif length == count:
                output_file_list.append(this_pdf)
            count += 1
        return output_file_list

    def _create_zip(self, max_deliveryfile_size, reference, iaid):
        print(self.replica_data['files'])
        batch_list = self._create_file_list(max_deliveryfile_size, self.replica_data['files'])
        zipfile_name_prefix = self._create_file_name_prefix(reference)
        n = 1
        for batch in batch_list:
            output_name = zipfile_name_prefix + '{:02d}'.format(n) + '.zip'
            zip_file = zipfile.ZipFile('/tmp/' + output_name, 'w')
            with zip_file:
                for file_key in batch:
                    try:
                        s3_obj = s3_client.get_object(Bucket=s3_bucket_get, Key=file_key)
                        file_data = s3_obj['Body'].read()
                        zip_file.write(file_data)
                    except ClientError as e:
                        print(e)
                        print('[ERROR 404 NoSuchKey] - Failed to retrieve file from s3: ' + file_key)
                        break
            zip_file.close()
            success = self._s3_put_object(s3_bucket_put, '/tmp/' + output_name, 'test/' + output_name)
        return {"code": 200}

    def _create_pdf(self, max_deliveryfile_size, reference, iaid):
        batch_list = self._create_file_list(max_deliveryfile_size, self.replica_data['files'])
        output_name_prefix = self._create_file_name_prefix(reference)
        font = ImageFont.truetype('./font/Arial.ttf', 16)
        images = []
        n = 1
        parts = []
        count_images = 0
        start = self._post_progress(iaid, 1)
        if start:
            print('Progress reporting started')
        else:
            print('Progress reporting failed')
        for batch in batch_list:
            for image_key in batch:
                image_object = self._get_s3_image(s3_bucket_get, image_key)
                if image_object:
                    target_size = (self._calculate_im_size(image_object.size))
                    image_object.thumbnail(target_size, Image.ANTIALIAS)
                    canvas = self._compose_canvas(image_object)
                    canvas_with_text = self._write_text_to_image(canvas, reference, font)
                    images.append(canvas_with_text)
                else:
                    print('[ERROR 404 NoSuchKey] - Failed to retrieve image from s3: ' + image_key)
                    break
            tmp_path = '/tmp/'
            output_name = output_name_prefix + '{:02d}'.format(n) + '.pdf'
            n += 1
            images[0].save(tmp_path + output_name, save_all=True, quality=100, append_images=images[1:])
            success = self._s3_put_object(s3_bucket_put, tmp_path + output_name, 'test/' + output_name)
            if success:
                print('Successfully uploaded to s3: ' + output_name)
                total_parts = len(batch_list)
                total_batch_images = len(batch)
                from_image = count_images + 1
                to_image = count_images + total_batch_images
                count_images = to_image
                part = {"FileName": output_name, "FromImage": from_image, "ToImage": to_image, "ContentType": "application/pdf"}
                parts.append(part)
                percentage = round((100 / total_parts) * len(parts))
                send = self._post_progress(iaid, percentage, parts)
                if send:
                    progress = str(percentage) + '% progress'
                    print(progress)
                else:
                    print('Progress reporting failed')
                os.remove(tmp_path + output_name)
                images = []
            else:
                print('Failed to upload to s3: ' + output_name)
                pass
        return {"code": 200}

    def _create_file_name_prefix(self, reference):
        name = reference.replace(" ", "-")
        name = name.replace("/", "-")
        return name + '_'

    def _calculate_im_size(self, size):
        width, height = size
        max_long_edge = 1141
        max_short_edge = 807
        if width < height:
            # Portrait
            ratio = width / height
            if ratio > 0.707:
                new_width = max_short_edge
                new_height = new_width / width * height
            else:
                new_height = max_long_edge
                new_width = new_height / height * width
        else:
            # Landscape
            ratio = width / height
            if ratio > 1.4144:
                new_width = max_long_edge
                new_height = new_width / width * height
            else:
                new_height = max_short_edge
                new_width = new_height / height * width
        return new_width, new_height

    def _compose_canvas(self, image_object):
        image_width, image_height = image_object.size
        canvas_width = 0
        canvas_height = 0
        if image_width < image_height:
            # Portrait
            canvas_width = 842
            canvas_height = 1191
        else:
            canvas_width = 1191
            canvas_height = 842
        canvas = Image.new(image_object.mode, (canvas_width, canvas_height), (255, 255, 255))
        x1 = int(math.floor((canvas_width - image_width) / 2))
        y1 = int(math.floor((canvas_height - image_height) / 2))
        canvas.paste(image_object, (x1, y1, x1 + image_width, y1 + image_height))
        return canvas

    def _write_text_to_image(self, image_object, reference, font):
        draw = ImageDraw.Draw(image_object)
        text = 'The National Archives reference ' + reference + '  -  © Crown Copyright'
        draw.text((4, 2), text, (0, 0, 0), font)
        return image_object

    def _get_s3_image(self, s3_bucket_get, image_key):
        try:
            s3_obj = s3_client.get_object(Bucket=s3_bucket_get, Key=image_key)
            image_bytes = s3_obj['Body'].read()
            image_object = Image.open(BytesIO(image_bytes))
            if image_object.mode == "RGBA":
                image_object = image_object.convert("RGB")
        except ClientError as e:
            print(e)
            return False
        return image_object

    def _s3_put_object(self, bucket_name, src_data, object_key):
        try:
            s3_client.put_object(
                ACL='public-read',
                Bucket=bucket_name,
                Body=open(src_data, 'rb'),
                Key=object_key
            )
        except ClientError as e:
            print(e)
            return False
        return True

    def _check_s3(self, bucket_name, object_key):
        try:
            s3_client.head_object(Bucket=bucket_name, Key=object_key)
        except ClientError as e:
            print(e)
            return False
        return True

    def _post_progress(self, iaid, percentage, parts=None):
        if parts is None:
            data = {"Iaid": iaid, "PercentCompleted": percentage}
        else:
            data = {"Iaid": iaid, "PercentCompleted": percentage, "Parts": parts}
        api = metadata_api + 'preparedfile'
        try:
            params = json.dumps(data).encode('utf8')
            req = urllib.request.Request(api, data=params, headers={'Content-Type': 'application/json'}, method='POST')
            response = urllib.request.urlopen(req)
        except Exception as ex:
            print(ex)
            return False
        return True
