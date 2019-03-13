'''Test `resize` command.'''

import unittest

from click.testing import CliRunner

from imgwrench.commands.resize import resize

from .images import pixel1x1_img
from .utils import execute_and_test_output_images


class TestResize(unittest.TestCase):
    '''Test for `resize` command.'''

    def test_resize_size(self):
        '''Test output sizes of resize.'''
        pixel100 = resize(pixel1x1_img, 100)
        self.assertEqual(100, pixel100.size[0])
        self.assertEqual(100, pixel100.size[1])
        pixel67 = resize(pixel100, 67)
        self.assertEqual(67, pixel67.size[0])
        self.assertEqual(67, pixel67.size[1])

    def test_resized_output(self):
        '''Test output of resize command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'resized_', ['resize'])
