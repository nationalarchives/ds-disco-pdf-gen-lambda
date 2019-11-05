from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json
import boto3
from io import BytesIO

session = boto3.session.Session(profile_name='intersiteadmin')
s3_client = session.client('s3')


def get_input_variables(data):
    # TODO Interface with SQS here to get the real input data
    list = json.loads(data)
    return list


def get_replica(rid):
    # TODO Interface with the DigitalMetadataAPI to fetch a real replica here
    with open('response.json') as content_file:
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


    def _create_image_list(self, max_deliveryfile_size):
        output_file_list = []
        size = 0
        this_pdf = []
        for file in self.replica_data['files']:
            this_pdf.append(file['name'])
            size = file['size'] + size
            if size > max_deliveryfile_size:
                output_file_list.append(this_pdf)
                size = 0
                this_pdf = []
        return output_file_list

    def _create_pdf(self, max_deliveryfile_size, reference):
        # TODO add reference and page number to PDF
        # TODO update digitalfile mata data with progress
        # TODO keep track of list of PDFs
        # TODO write list of PDFs back to digitalfile meta data
        batch_list = self._create_image_list(max_deliveryfile_size)
        output_name_prefix = self._create_file_name_prefix(reference)
        font = ImageFont.truetype('./font/Arial.ttf', 16)
        images = []
        n = 1
        for batch in batch_list:
            for image_key in batch:
                obj = s3_client.get_object(Bucket='tna-digital-files', Key=image_key)
                print(image_key)
                image = obj['Body'].read()
                im = Image.open(BytesIO(image))
                size = (self._calculate_im_size(im.size))
                im.thumbnail(size, Image.ANTIALIAS)
                if im.mode == "RGBA":
                    im = im.convert("RGB")
                draw = ImageDraw.Draw(im)
                draw.text((4, 2), 'The National Archives reference ' + reference, (0, 0, 0), font)
                images.append(im)
            output_name = output_name_prefix + '{:02d}'.format(n) + '.pdf'
            print(output_name)
            n += 1
            images[0].save(output_name, save_all=True, quality=100, append_images=images[1:])

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
