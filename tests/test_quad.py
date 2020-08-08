'''Test `quad` command.'''

import unittest

from click.testing import CliRunner

from imgwrench.commands.quad import quad

from .images import pixel1x1_img
from .utils import execute_and_test_output_images


class TestQuad(unittest.TestCase):
    '''Test for `quad` command.'''

    def test_quad_size(self):
        '''Test output sizes of quad.'''
        _, out100x50 = quad([(None, pixel1x1_img)], 100, 50, 0, None)
        self.assertEqual(100, out100x50.size[0])
        self.assertEqual(50, out100x50.size[1])
        _, out50x100 = quad([(None, pixel1x1_img)], 50, 100, 0, None)
        self.assertEqual(50, out50x100.size[0])
        self.assertEqual(100, out50x100.size[1])

    def test_quad_output(self):
        '''Test output of quad command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 1,
                                       'quad_', ['quad'])
        execute_and_test_output_images(self, CliRunner(), 4, 1,
                                       'quad_', ['quad'])
        execute_and_test_output_images(self, CliRunner(), 5, 2,
                                       'quad_', ['quad'])
        execute_and_test_output_images(self, CliRunner(), 8, 2,
                                       'quad_', ['quad'])
        execute_and_test_output_images(self, CliRunner(), 9, 3,
                                       'quad_', ['quad'])
