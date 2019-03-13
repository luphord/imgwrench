'''Test `framecrop` command.'''

import unittest

from PIL import Image
from click.testing import CliRunner

from imgwrench.commands.framecrop import framecrop
from imgwrench.param import RATIO

from .images import white150x100_img, white100x123_img
from .utils import execute_and_test_output_images


def _ratio(value):
    return RATIO.convert(value, None, None)


def _aratio(img):
    return img.size[0] / img.size[1]


class TestFramecrop(unittest.TestCase):
    '''Test for `framecrop` command.'''

    def test_framecrop_aspect_ratio(self):
        '''Test output size ratios of framecrop.'''
        framed_img = framecrop(white150x100_img, _ratio('3:2'), 0.1, 'green')
        self.assertEqual(3/2, _aratio(framed_img))
        framed_img = framecrop(white150x100_img, _ratio('2:3'), 0.1, 'green')
        self.assertEqual(3/2, _aratio(framed_img))
        framed_img = framecrop(white150x100_img, _ratio('4:3'), 0.1, 'green')
        self.assertEqual(round(4/3, 1), round(_aratio(framed_img), 1))
        framed_img = framecrop(white150x100_img, _ratio('1:1'), 0.1, 'green')
        self.assertEqual(1, _aratio(framed_img))
        framed_img = framecrop(white150x100_img, _ratio('1:2'), 0.1, 'green')
        self.assertEqual(2/1, _aratio(framed_img))
        framed_img = framecrop(white100x123_img, _ratio('3:2'), 0.2, 'green')
        self.assertEqual(round(2/3, 2), round(_aratio(framed_img), 2))
        framed_img = framecrop(white100x123_img, _ratio('2:3'), 0.2, 'green')
        self.assertEqual(round(2/3, 2), round(_aratio(framed_img), 2))
        framed_img = framecrop(white100x123_img, _ratio('2:1'), 0.2, 'green')
        self.assertEqual(round(1/2, 2), round(_aratio(framed_img), 2))
        framed_img = framecrop(white100x123_img, _ratio('3:1'), 0.2, 'green')
        self.assertEqual(round(1/3, 1), round(_aratio(framed_img), 1))
        with self.assertRaises(AssertionError):
            framecrop(white100x123_img, _ratio('4:1'), 0.2, 'green')
        with self.assertRaises(AssertionError):
            framecrop(white100x123_img, _ratio('6:1'), 0.1, 'green')
        with self.assertRaises(AssertionError):
            framecrop(white100x123_img, _ratio('1:3'), 0.3, 'green')

    def test_framecrop_pixelcolor(self):
        '''Test all pixels of a framecrop operation'''
        actual_white150x100 = Image.new('RGB', (150, 100), 'white')
        framed_img = framecrop(actual_white150x100, _ratio('3:2'),
                               0.1, '#00ff00')
        self.assertEqual(180, framed_img.size[0])
        self.assertEqual(120, framed_img.size[1])
        pixels = framed_img.load()
        for i in range(framed_img.size[0]):
            for j in range(framed_img.size[1]):
                r, g, b = pixels[i, j]
                inside_frame = i < 15 or i >= 165 \
                    or j < 15 or j >= 105
                if inside_frame:
                    self.assertEqual(0, r)
                    self.assertEqual(255, g)
                    self.assertEqual(0, b)
                else:
                    self.assertEqual(255, r)
                    self.assertEqual(255, g)
                    self.assertEqual(255, b)

    def test_framecropped_output(self):
        '''Test output of framecrop command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'framecroppedd_', ['framecrop'])
