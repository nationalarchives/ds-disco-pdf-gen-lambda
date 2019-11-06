import unittest
import json
from PIL import Image
from PIL import ImageFont
import PrepareFiles

data = '{ "Iaid": "C7351413", "ReplicaId": "769c283b-1676-4eb6-a85b-63c7e6eb5272", "Reference": "WO 95/1105/1", "FileExtension": "pdf", "MaxDeliverySize": 46925 }'


class TestMethods(unittest.TestCase):

    def test_calculate_im_size_portrait(self):
        replica = PrepareFiles.Replica(data)
        # Test image size 2475x3504
        size = (replica._calculate_im_size((2475, 3504)))
        self.assertEqual(size, (781.207191780822, 1106))

    def test_calculate_im_size_landscape(self):
        replica = PrepareFiles.Replica(data)
        # Test image size 3504x2475
        size = (replica._calculate_im_size((3504, 2475)))
        self.assertEqual(size, (1106, 781.207191780822))

    def test_calculate_im_size_square(self):
        replica = PrepareFiles.Replica(data)
        # Test image size 2475x2475
        size = (replica._calculate_im_size((2475, 2475)))
        self.assertEqual(size, (782, 782))

    def test_calculate_im_size_high(self):
        replica = PrepareFiles.Replica(data)
        # Test image size 1000x2475
        size = (replica._calculate_im_size((1000, 2475)))
        self.assertEqual(size, (446.86868686868684, 1106))

    def test_calculate_im_size_wide(self):
        replica = PrepareFiles.Replica(data)
        # Test image size 3500x1475
        size = (replica._calculate_im_size((3500, 1475)))
        self.assertEqual(size, (1106, 466.1))

    def test_create_file_name_prefix(self):
        replica = PrepareFiles.Replica(data)
        output = replica._create_file_name_prefix('WO 95/1105/1')
        self.assertEqual(output, 'WO-95-1105-1_')

    def test_create_image_list_3_files(self):
        replica = PrepareFiles.Replica(data)
        with open('test-3-files.json') as content_file:
            json_content = content_file.read()
        content = json.loads(json_content)
        files = content['files']
        output = replica._create_image_list(46925, files)
        self.assertEqual(output, [['66/DEFE/24/23D96610-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/242C63EC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2476ADD0-4D5A-11E8-BACD-B7E50F03B1FA.jpg']])

    def test_create_image_list_20_files(self):
        replica = PrepareFiles.Replica(data)
        with open('test-20-files.json') as content_file:
            json_content = content_file.read()
        content = json.loads(json_content)
        files = content['files']
        output = replica._create_image_list(46925, files)
        self.assertEqual(output, [['66/DEFE/24/23D96610-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/242C63EC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2476ADD0-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/266B578A-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/26BE6452-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2701FA5A-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2754C7BC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/279FACA0-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/27E9F8DC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/282D1D24-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2886ED7C-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/28D99856-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/29245CD8-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/29672306-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/29B15200-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2A04B54E-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2A4FA9FA-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2A9B2164-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2ADDFE44-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2B2861A0-4D5A-11E8-BACD-B7E50F03B1FA.jpg']])

    def test_create_image_list_20_lg_files(self):
        replica = PrepareFiles.Replica(data)
        with open('test-20-lg-files.json') as content_file:
            json_content = content_file.read()
        content = json.loads(json_content)
        files = content['files']
        output = replica._create_image_list(46925, files)
        self.assertEqual(output, [['66/DEFE/24/23D96610-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/242C63EC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2476ADD0-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/266B578A-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/26BE6452-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2701FA5A-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2754C7BC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/279FACA0-4D5A-11E8-BACD-B7E50F03B1FA.jpg'],
                                  ['66/DEFE/24/27E9F8DC-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/282D1D24-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2886ED7C-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/28D99856-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/29245CD8-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/29672306-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/29B15200-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2A04B54E-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2A4FA9FA-4D5A-11E8-BACD-B7E50F03B1FA.jpg'],
                                  ['66/DEFE/24/2A9B2164-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2ADDFE44-4D5A-11E8-BACD-B7E50F03B1FA.jpg',
                                   '66/DEFE/24/2B2861A0-4D5A-11E8-BACD-B7E50F03B1FA.jpg']])

    def test_compose_canvas_landscape(self):
        replica = PrepareFiles.Replica(data)
        image_object = Image.open('tree-landscape.jpg')
        target_size = (replica._calculate_im_size(image_object.size))
        image_object.thumbnail(target_size, Image.ANTIALIAS)
        output = replica._compose_canvas(image_object)
        output.save('output-landscape.jpg')
        self.assertEqual(output.size, (1191, 842))

    def test_compose_canvas_portrait(self):
        replica = PrepareFiles.Replica(data)
        image_object = Image.open('tree-portrait.jpg')
        target_size = (replica._calculate_im_size(image_object.size))
        image_object.thumbnail(target_size, Image.ANTIALIAS)
        output = replica._compose_canvas(image_object)
        output.save('output-portrait.jpg')
        self.assertEqual(output.size, (842, 1191))

    def test_write_text_to_image_landscape(self):
        replica = PrepareFiles.Replica(data)
        image_object = Image.open('output-landscape.jpg')
        font = ImageFont.truetype('./font/Arial.ttf', 16)
        output = replica._write_text_to_image(image_object, 'WO 95/1105/1', font)
        output.save('output-landscape-text.jpg')
        self.assertEqual(output.size, (1191, 842))

    def test_write_text_to_image_portrait(self):
        replica = PrepareFiles.Replica(data)
        image_object = Image.open('output-portrait.jpg')
        font = ImageFont.truetype('./font/Arial.ttf', 16)
        output = replica._write_text_to_image(image_object, 'WO 95/1105/1', font)
        output.save('output-portrait-text.jpg')
        self.assertEqual(output.size, (842, 1191))
