"""Test `quad` command."""

import unittest

from click.testing import CliRunner
from PIL import Image

from imgwrench.commands.quad import quad

from .images import pixel1x1_img
from .utils import execute_and_test_output_images


class TestQuad(unittest.TestCase):
    """Test for `quad` command."""

    def test_quad_size(self):
        """Test output sizes of quad."""
        out100x50 = quad([pixel1x1_img], 100, 50, 0, False, None)
        self.assertEqual(100, out100x50.size[0])
        self.assertEqual(50, out100x50.size[1])
        out50x100 = quad([pixel1x1_img], 50, 100, 0, False, None)
        self.assertEqual(50, out50x100.size[0])
        self.assertEqual(100, out50x100.size[1])

    def test_quad_pixels(self):
        """Test exact pixel colors of quad."""
        actual_white = Image.new("RGB", (10, 10), "white")
        images = [actual_white for i in range(4)]
        quad_img = quad(images, 100, 50, 0.1, False, "#00ff00")
        pixels = quad_img.load()
        for i in range(quad_img.size[0]):
            for j in range(quad_img.size[1]):
                r, g, b = pixels[i, j]
                inside_frame = (
                    i < 10
                    or 45 <= i < 55
                    or i >= 90
                    or j < 10
                    or 20 <= j < 30
                    or j >= 40
                )
                if inside_frame:
                    self.assertEqual(0, r)
                    self.assertEqual(255, g)
                    self.assertEqual(0, b)
                else:
                    self.assertEqual(255, r)
                    self.assertEqual(255, g)
                    self.assertEqual(255, b)
        # same thing with double frame
        quad_img = quad(images, 100, 50, 0.1, True, "#00ff00")
        pixels = quad_img.load()
        quad_img.save("test.png")
        for i in range(quad_img.size[0]):
            for j in range(quad_img.size[1]):
                r, g, b = pixels[i, j]
                inside_frame = (
                    i < 10 or 40 <= i < 60 or i >= 90 or j < 10 or 15 < j < 35 or j > 40
                )
                if inside_frame:
                    self.assertEqual(0, r, f"i={i}, j={j}")
                    self.assertEqual(255, g, f"i={i}, j={j}")
                    self.assertEqual(0, b, f"i={i}, j={j}")
                else:
                    self.assertEqual(255, r, f"i={i}, j={j}")
                    self.assertEqual(255, g, f"i={i}, j={j}")
                    self.assertEqual(255, b, f"i={i}, j={j}")

    def test_quad_output(self):
        """Test output of quad command."""
        execute_and_test_output_images(self, CliRunner(), 3, 1, "quad_", ["quad"])
        execute_and_test_output_images(self, CliRunner(), 4, 1, "quad_", ["quad"])
        execute_and_test_output_images(self, CliRunner(), 5, 2, "quad_", ["quad"])
        execute_and_test_output_images(self, CliRunner(), 8, 2, "quad_", ["quad"])
        execute_and_test_output_images(self, CliRunner(), 9, 3, "quad_", ["quad"])
