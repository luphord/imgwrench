'''Test `crop` command.'''

import unittest

from PIL import Image
from click.testing import CliRunner

from imgwrench.commands.crop import crop
from imgwrench.param import RATIO

from .images import white100x100_img, white117x100_img, \
                    white100x123_img, white150x100_img
from .utils import execute_and_test_output_images


def _ratio(value):
    return RATIO.convert(value, None, None)


class TestCrop(unittest.TestCase):
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
        white100x67 = crop(white100x100_img, _ratio('3:2'))
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(67, white100x67.size[1])
        # exactly the same
        white100x67 = crop(white100x100_img, _ratio('2:3'))
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(67, white100x67.size[1])
        # different ratio
        white100x67 = crop(white100x100_img, _ratio('2:1'))
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(50, white100x67.size[1])
        # different images
        # square
        white100x100 = crop(white100x100_img, _ratio('1:1'))
        self.assertEqual(100, white100x100.size[0])
        self.assertEqual(100, white100x100.size[1])
        # 117 x 100
        white117x78 = crop(white117x100_img, _ratio('3:2'))
        self.assertEqual(117, white117x78.size[0])
        self.assertEqual(78, white117x78.size[1])
        white117x78 = crop(white117x100_img, _ratio('2:3'))
        self.assertEqual(117, white117x78.size[0])
        self.assertEqual(78, white117x78.size[1])
        white100x100 = crop(white117x100_img, _ratio('1:1'))
        self.assertEqual(100, white100x100.size[0])
        self.assertEqual(100, white100x100.size[1])
        # 100 x 123
        white82x123 = crop(white100x123_img, _ratio('3:2'))
        self.assertEqual(82, white82x123.size[0])
        self.assertEqual(123, white82x123.size[1])
        white82x123 = crop(white100x123_img, _ratio('2:3'))
        self.assertEqual(82, white82x123.size[0])
        self.assertEqual(123, white82x123.size[1])
        white100x100 = crop(white100x123_img, _ratio('1:1'))
        self.assertEqual(100, white100x100.size[0])
        self.assertEqual(100, white100x100.size[1])
        # 150 x 100
        white150x100 = crop(white150x100_img, _ratio('3:2'))
        self.assertEqual(150, white150x100.size[0])
        self.assertEqual(100, white150x100.size[1])
        white150x100 = crop(white150x100_img, _ratio('2:3'))
        self.assertEqual(150, white150x100.size[0])
        self.assertEqual(100, white150x100.size[1])
        white100x100 = crop(white150x100_img, _ratio('1:1'))
        self.assertEqual(100, white100x100.size[0])
        self.assertEqual(100, white100x100.size[1])

    def test_rotation_changes_size(self):
        '''Test assumptions about the impact of rotation.'''
        self.assertEqual(117, white117x100_img.size[0])
        self.assertEqual(100, white117x100_img.size[1])
        white100x117 = white117x100_img.transpose(Image.ROTATE_90)
        self.assertEqual(100, white100x117.size[0])
        self.assertEqual(117, white100x117.size[1])
        # note that transpose seems to be required for this
        # rotate(90) does not impact the original site

    def test_crop_size_of_rotated_images(self):
        '''Test output sizes of crop for rotated images.'''
        white100x67 = crop(white100x100_img.transpose(Image.ROTATE_90),
                           _ratio('3:2'))
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(67, white100x67.size[1])
        # exactly the same
        white100x67 = crop(white100x100_img.transpose(Image.ROTATE_90),
                           _ratio('2:3'))
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(67, white100x67.size[1])
        # different ratio
        white100x67 = crop(white100x100_img.transpose(Image.ROTATE_90),
                           _ratio('2:1'))
        self.assertEqual(100, white100x67.size[0])
        self.assertEqual(50, white100x67.size[1])
        # different images
        # square
        white100x100 = crop(white100x100_img.transpose(Image.ROTATE_90),
                            _ratio('1:1'))
        self.assertEqual(100, white100x100.size[1])
        self.assertEqual(100, white100x100.size[0])
        # 117 x 100
        white117x78 = crop(white117x100_img.transpose(Image.ROTATE_90),
                           _ratio('3:2'))
        self.assertEqual(117, white117x78.size[1])
        self.assertEqual(78, white117x78.size[0])
        white117x78 = crop(white117x100_img.transpose(Image.ROTATE_90),
                           _ratio('2:3'))
        self.assertEqual(117, white117x78.size[1])
        self.assertEqual(78, white117x78.size[0])
        white100x100 = crop(white117x100_img.transpose(Image.ROTATE_90),
                            _ratio('1:1'))
        self.assertEqual(100, white100x100.size[1])
        self.assertEqual(100, white100x100.size[0])
        # 100 x 123
        white82x123 = crop(white100x123_img.transpose(Image.ROTATE_90),
                           _ratio('3:2'))
        self.assertEqual(82, white82x123.size[1])
        self.assertEqual(123, white82x123.size[0])
        white82x123 = crop(white100x123_img.transpose(Image.ROTATE_90),
                           _ratio('2:3'))
        self.assertEqual(82, white82x123.size[1])
        self.assertEqual(123, white82x123.size[0])
        white100x100 = crop(white100x123_img.transpose(Image.ROTATE_90),
                            _ratio('1:1'))
        self.assertEqual(100, white100x100.size[1])
        self.assertEqual(100, white100x100.size[0])
        # 150 x 100
        white150x100 = crop(white150x100_img.transpose(Image.ROTATE_90),
                            _ratio('3:2'))
        self.assertEqual(150, white150x100.size[1])
        self.assertEqual(100, white150x100.size[0])
        white150x100 = crop(white150x100_img.transpose(Image.ROTATE_90),
                            _ratio('2:3'))
        self.assertEqual(150, white150x100.size[1])
        self.assertEqual(100, white150x100.size[0])
        white100x100 = crop(white150x100_img.transpose(Image.ROTATE_90),
                            _ratio('1:1'))
        self.assertEqual(100, white100x100.size[1])
        self.assertEqual(100, white100x100.size[0])

    def test_cropped_output(self):
        '''Test output of crop command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'cropped_', ['crop'])
