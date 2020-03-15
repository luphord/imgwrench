'''Tests for `collage` subcommand.'''

import unittest
from unittest.mock import Mock

from click.testing import CliRunner

from .utils import execute_and_test_output_images

from imgwrench.commands.collage import LayoutLeaf, Row, Column


class MockLeaf(LayoutLeaf):

    def __init__(self, width, height):
        image = Mock
        image.size = (width, height)
        super().__init__(image)
        self.width = width
        self.height = height


class TestCollage(unittest.TestCase):
    '''Tests for `collage` subcommand.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()
        self.tree = Row([
            (3, Column([
                (1, MockLeaf(300, 100)),
                (2, MockLeaf(50, 50))])),
            (2, MockLeaf(100, 150))])

    def test_cut_loss(self):
        '''Test cut loss functions.'''
        leaf = MockLeaf(150, 100)
        self.assertEqual(0, leaf.cut_loss(3/2))
        self.assertEqual(1/3, leaf.cut_loss(1/1))
        self.assertEqual(2/3, leaf.cut_loss(1/2))
        self.assertEqual(1/2, leaf.cut_loss(3/4))
        self.assertEqual(1/2, leaf.cut_loss(6/2))
        self.assertEqual(2/3, leaf.cut_loss(9/2))
        self.assertAlmostEqual(1/4, leaf.cut_loss(4/2))

    def test_collage_output(self):
        '''Test output of filmstrip command.'''
        execute_and_test_output_images(self, self.runner, 6, 1,
                                       'rc_', ['collage', '-w', 20, '-s', 10])
