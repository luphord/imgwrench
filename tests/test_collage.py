'''Tests for `collage` subcommand.'''

import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images

from imgwrench.commands.collage import LayoutLeaf, Row, Column


class TestCollage(unittest.TestCase):
    '''Tests for `collage` subcommand.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()
        self.tree = Row([
            (3, Column([
                (1, LayoutLeaf(None)),
                (2, LayoutLeaf(None))])),
            (2, LayoutLeaf(None))])

    def test_collage_output(self):
        '''Test output of filmstrip command.'''
        execute_and_test_output_images(self, self.runner, 6, 1,
                                       'rc_', ['collage', '-w', 20, '-s', 10])
