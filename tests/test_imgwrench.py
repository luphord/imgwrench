#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imgwrench` package."""


import unittest
from click.testing import CliRunner

from imgwrench import cli_imgwrench


class TestImgwrench(unittest.TestCase):
    """Tests for `imgwrench` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli_imgwrench)
        assert result.exit_code == 0
        help_result = runner.invoke(cli_imgwrench, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit' in help_result.output
