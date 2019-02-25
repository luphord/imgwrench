'''Test `resize` command.'''

import unittest

from imgwrench.resize import resize

from .images import pixel1x1_img


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
