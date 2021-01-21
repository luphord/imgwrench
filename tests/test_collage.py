"""Tests for `collage` subcommand."""

import unittest
from unittest.mock import Mock
from random import Random

from click.testing import CliRunner
import numpy as np

from .utils import execute_and_test_output_images

from imgwrench.commands.collage import (
    LayoutLeaf,
    Row,
    Column,
    _binary_tree_recursive,
    bric_tree,
)


class MockLeaf(LayoutLeaf):
    def __init__(self, width, height):
        image = Mock()
        image.size = (width, height)
        super().__init__(image)
        self.width = width
        self.height = height


class TestCollage(unittest.TestCase):
    """Tests for `collage` subcommand."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.runner = CliRunner()
        self.tree = Row(
            [
                (3, Column([(1, MockLeaf(300, 100)), (2, MockLeaf(50, 50))])),
                (2, MockLeaf(100, 150)),
            ]
        )

    def test_cut_loss(self):
        """Test cut loss functions."""
        leaf = MockLeaf(150, 100)
        self.assertEqual(0, leaf.cut_loss(3 / 2))
        self.assertEqual(1 / 3, leaf.cut_loss(1 / 1))
        self.assertEqual(2 / 3, leaf.cut_loss(1 / 2))
        self.assertEqual(1 / 2, leaf.cut_loss(3 / 4))
        self.assertEqual(1 / 2, leaf.cut_loss(6 / 2))
        self.assertEqual(2 / 3, leaf.cut_loss(9 / 2))
        self.assertAlmostEqual(1 / 4, leaf.cut_loss(4 / 2))
        leaf = MockLeaf(100, 100)
        self.assertAlmostEqual(1 / 3, leaf.cut_loss(3 / 2))
        self.assertEqual(0, leaf.cut_loss(1 / 1))
        self.assertEqual(1 / 2, leaf.cut_loss(1 / 2))
        self.assertEqual(1 / 4, leaf.cut_loss(3 / 4))
        self.assertAlmostEqual(2 / 3, leaf.cut_loss(6 / 2))
        self.assertEqual(7 / 9, leaf.cut_loss(9 / 2))
        self.assertEqual(1 / 2, leaf.cut_loss(4 / 2))
        leaf = MockLeaf(100, 200)
        self.assertAlmostEqual(2 / 3, leaf.cut_loss(3 / 2))
        self.assertEqual(1 / 2, leaf.cut_loss(1 / 1))
        self.assertEqual(0, leaf.cut_loss(1 / 2))
        self.assertAlmostEqual(1 / 3, leaf.cut_loss(3 / 4))
        self.assertEqual(10 / 12, leaf.cut_loss(6 / 2))
        self.assertEqual(16 / 18, leaf.cut_loss(9 / 2))
        self.assertEqual(3 / 4, leaf.cut_loss(4 / 2))

    def test_width_height_coeff(self):
        for i in range(1, 50):
            images = []
            for i in range(i):
                img = Mock()
                img.size = (150, 100) if i % 2 == 0 else (100, 150)
                images.append(img)
            aspect_ratio = 1.0
            rnd = Random(i)
            tree = bric_tree(images, aspect_ratio, rnd)
            width, height, coeff = tree.width_height_coeff()
            self.assertEqual(len(images) - 1, len(coeff))
            leafs_set = set(tree.leafs)
            self.assertEqual(len(images), len(leafs_set))
            for c in coeff + [{**width, **height}]:
                for node in c:
                    leafs_set.discard(node)
            self.assertFalse(leafs_set)

    def test_binary_tree_recursive(self):
        for i in range(1, 50):
            images = []
            for i in range(i):
                img = Mock()
                img.size = (150, 100) if i % 2 == 0 else (100, 150)
                images.append(img)
            tree = _binary_tree_recursive(images, Random(i), True)
            self.assertEqual(len(images), tree.leaf_count)

    def test_bric_tree(self):
        images = []
        for i in range(12):
            img = Mock()
            img.size = (150, 100) if i % 3 == 2 else (100, 150)
            images.append(img)
        bric_tree(images, 1, Random(1))

    def test_bric_paper_tree(self):
        """Test tree example from seminal BRIC paper"""
        leafs = [MockLeaf(150, 100) for i in range(5)]
        p1, p2, p3, p4, p5 = leafs
        tree = Row(
            [
                (1, Column([(1, Row([(1, p1), (1, p5)])), (1, p3)])),
                (1, Column([(1, p2), (1, p4)])),
            ]
        )
        idx = [leafs.index(leaf) for leaf in tree.leafs]
        for i1, i2 in enumerate(idx):
            self.assertEqual(leafs[i2], list(tree.leafs)[i1])
        for node, i in tree.leafs_index.items():
            self.assertEqual(leafs[idx[i]], node)
        a1, a2, a3, a4, a5 = [1 / p.image_aspect_ratio for p in leafs]
        a_expected = np.array(
            [
                [a1, 0, 0, 0, -a5],
                [a1, 0, -a3, 0, a5],
                [0, 1, 0, -1, 0],
                [a1, -a2, a3, -a4, 0],
                [1, 1, 0, 0, 1],
            ]
        )
        b_expected = np.array([0, 0, 0, 0, 1])
        sol_expected = np.linalg.solve(a_expected, b_expected)
        a, b = tree.linear_equations
        sol = np.linalg.solve(a, b)
        self.assertTrue(np.allclose(sol_expected[idx], sol))

    def test_collage_output(self):
        """Test output of filmstrip command."""
        execute_and_test_output_images(
            self, self.runner, 6, 1, "rc_", ["collage", "-w", 20, "-s", 10]
        )
