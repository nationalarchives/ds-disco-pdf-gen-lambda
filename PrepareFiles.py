from PIL import Image
import json
import boto3
client = boto3.client('s3')

def sqs_json(data):
    list = json.loads(data)
    return list


def get_replica(rid):
    with open('response.json') as content_file:
        json_content = content_file.read()
    content = json.loads(json_content)
    replica = Replica(content)
    return replica


class Replica:
    def __init__( self, content ):
        self.replica_data = content


    def process_files(self, delivery_type, cal_avg_size):
        if delivery_type == "PDF":
            self._create_pdf(cal_avg_size)
        # else:
        #     create_zip(cal_avg_size)


    def _create_image_list( self, cal_avg_size ):
        output_file_list = []
        size = 0
        this_pdf = []
        for file in self.replica_data['files']:
            this_pdf.append(file['name'])
            size = file['size'] + size
            if size > cal_avg_size:
                output_file_list.append(this_pdf)
                size = 0
                this_pdf = []
        return output_file_list


    def _create_pdf(self, cal_avg_size):
        batch_list = self._create_image_list(cal_avg_size)
        images = []
        for batch in batch_list:
            for image in batch:
                im = Image.open(image)
                if im.mode == "RGBA":
                    im = im.convert("RGB")
                images.append(im)



#
#     def create_pdf(images):
#         images[0].save(out_fname, save_all=True, quality=100, append_images=images[1:])
#
#     def get_file(item):
#         return file
#
#
#
#
#
#
#
#
#
#
#
