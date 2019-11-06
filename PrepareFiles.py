import math
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json
import boto3
from io import BytesIO
import PreparedFiles_config

session = boto3.session.Session(profile_name='intersiteadmin')
s3_client = session.client('s3')


def get_input_variables(data):
    # TODO Interface with SQS here to get the real input data
    list = json.loads(data)
    return list


def get_replica(rid):
    # TODO Interface with the DigitalMetadataAPI to fetch a real replica here
    with open('tests/response.json') as content_file:
        json_content = content_file.read()
    content = json.loads(json_content)
    replica = Replica(content)
    return replica


class Replica:
    def __init__( self, content ):
        self.replica_data = content

    def process_files(self, delivery_type, max_deliveryfile_size, reference):
        # TODO Code the ZIP case. Can any of the PDF case be generalised?
        if delivery_type == "pdf":
            self._create_pdf(max_deliveryfile_size, reference)
        # else:
        #     create_zip(cal_avg_size)

    def _create_image_list(self, max_deliveryfile_size, data):
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

    def _create_pdf(self, max_deliveryfile_size, reference):
        # TODO update digitalfile mata data with progress
        # TODO keep track of list of PDFs
        # TODO write list of PDFs back to digitalfile meta data
        # TODO push pdfs to S3
        batch_list = self._create_image_list(max_deliveryfile_size, self.replica_data['files'])
        output_name_prefix = self._create_file_name_prefix(reference)
        font = ImageFont.truetype('./font/Arial.ttf', 16)
        images = []
        n = 1
        for batch in batch_list:
            for image_key in batch:
                print(image_key)
                s3_obj = s3_client.get_object(Bucket='tna-digital-files', Key=image_key)
                image_bytes = s3_obj['Body'].read()
                image_object = Image.open(BytesIO(image_bytes))
                target_size = (self._calculate_im_size(image_object.size))
                image_object.thumbnail(target_size, Image.ANTIALIAS)
                if image_object.mode == "RGBA":
                    image_object = image_object.convert("RGB")
                canvas = self._compose_canvas(image_object)
                canvas_with_text = self._write_text_to_image(canvas, reference, font)
                images.append(canvas_with_text)
            output_name = output_name_prefix + '{:02d}'.format(n) + '.pdf'
            print(output_name)
            n += 1
            images[0].save(output_name, save_all=True, quality=100, append_images=images[1:])
            # TODO check file has successfully uploaded to s3 and then delete local file
            r = s3_client.put_object(
                ACL='public-read',
                Body=open(output_name, 'rb'),
                ContentType='application/pdf',
                Bucket=PreparedFiles_config.S3_BUCKET_NAME,
                Key="test-"+output_name
            )

    def _create_file_name_prefix(self, reference):
        name = reference.replace(" ", "-")
        name = name.replace("/", "-")
        return name + '_'

    def _calculate_im_size(self, size):
        width, height = size
        max_long_edge = 1106
        max_short_edge = 782
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

    def _compose_canvas(self,image_object):
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