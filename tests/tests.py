import unittest
import json
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

