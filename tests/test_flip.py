"""Test `flip` command."""

import unittest
from pathlib import Path

from PIL import Image
from click.testing import CliRunner

from imgwrench.commands.flip import flip

from .utils import execute_and_test_output_images


class TestFlip(unittest.TestCase):
    """Test for `flip` command."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.runner = CliRunner()
        self.images_path = Path(__file__).resolve().parent / "images"
        self.red_blue_path = str(self.images_path / "red-blue.png")

    def test_original_sizes_to_be_sure(self):
        """Checks the original image sizes."""
        with Image.open(self.red_blue_path) as img:
            self.assertEqual(2, img.size[0])
            self.assertEqual(1, img.size[1])

    def test_flip(self):
        """Test flipping with a simple red-blue 2x1 pixel image"""
        red = (255, 0, 0)
        blue = (0, 0, 255)
        with Image.open(self.red_blue_path) as img:
            pixels = img.load()
            self.assertEqual(red, pixels[0, 0])
            self.assertEqual(blue, pixels[1, 0])
            img = flip(img)
            pixels = img.load()
            self.assertEqual(blue, pixels[0, 0])
            self.assertEqual(red, pixels[1, 0])

    def test_flipped_output(self):
        """Test output of flip command."""
        execute_and_test_output_images(self, CliRunner(), 3, 3, "flipped_", ["flip"])
