'''Test `frame` command.'''

import unittest

from PIL import Image
from click.testing import CliRunner

from imgwrench.commands.frame import frame

from .images import white150x100_img, white100x123_img
from .utils import execute_and_test_output_images


class TestFrame(unittest.TestCase):
    '''Test for `frame` command.'''

    def test_frame_size(self):
        '''Test output sizes of frame.'''
        framed_img = frame(white150x100_img, 0.1, 'green')
        self.assertEqual(180, framed_img.size[0])
        self.assertEqual(130, framed_img.size[1])
        framed_img = frame(white100x123_img, 0.2, 'green')
        self.assertEqual(150, framed_img.size[0])
        self.assertEqual(173, framed_img.size[1])

    def test_frame_color(self):
        actual_white150x100 = Image.new('RGB', (150, 100), 'white')
        framed_img = frame(actual_white150x100, 0.1, '#00ff00')
        pixels = framed_img.load()
        for i in range(framed_img.size[0]):
            for j in range(framed_img.size[1]):
                r, g, b = pixels[i, j]
                inside_frame = i < 15 or i >= 165 \
                    or j < 15 or j >= 115
                if inside_frame:
                    self.assertEqual(0, r)
                    self.assertEqual(255, g)
                    self.assertEqual(0, b)
                else:
                    self.assertEqual(255, r)
                    self.assertEqual(255, g)
                    self.assertEqual(255, b)

    def test_framed_output(self):
        '''Test output of frame command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'framed_', ['frame'])
