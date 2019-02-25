'''Test `crop` command.'''

import unittest

from imgwrench.crop import crop

from .images import white100x100_img, white117x100_img, \
                    white100x123_img, white150x100_img


class TestResize(unittest.TestCase):
    '''Test for `crop` command.'''

    def test_original_sizes_to_be_sure(self):
        '''Checks the original image sizes.'''
        self.assertEqual(100, white100x100_img.size[0])
        self.assertEqual(100, white100x100_img.size[1])
        self.assertEqual(117, white117x100_img.size[0])
        self.assertEqual(100, white117x100_img.size[1])
        self.assertEqual(100, white100x123_img.size[0])
        self.assertEqual(123, white100x123_img.size[1])
        self.assertEqual(150, white150x100_img.size[0])
        self.assertEqual(100, white150x100_img.size[1])

    def test_crop_size(self):
        '''Test output sizes of crop.'''
        white100x67 = crop(white100x100_img, '3:2')
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(67, white100x67.size[1])
        # exactly the same as it is a square
        white100x67 = crop(white100x100_img, '2:3')
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(67, white100x67.size[1])
        # different ratio
        white100x67 = crop(white100x100_img, '2:1')
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(50, white100x67.size[1])
        # different images
        white117x78 = crop(white117x100_img, '3:2')
        self.assertEqual(117, white117x78.size[0])
        self.assertEqual(78, white117x78.size[1])
        white117x78 = crop(white117x100_img, '2:3')
        self.assertEqual(117, white117x78.size[0])
        self.assertEqual(78, white117x78.size[1])
