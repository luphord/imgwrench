'''Test `quad` command.'''

import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestQuad(unittest.TestCase):
    '''Test for `quad` command.'''

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
