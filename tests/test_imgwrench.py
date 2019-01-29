#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imgwrench` package."""


import unittest
from click.testing import CliRunner

from imgwrench import cli_imgwrench


class TestImgwrenchMainCli(unittest.TestCase):
    '''Tests for `imgwrench` main cli.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()

    def tearDown(self):
        '''Tear down test fixtures, if any.'''

    def test_command_line_interface(self):
        '''Test help invocation.'''
        help_msg = 'Show this message and exit'
        help_result = self.runner.invoke(cli_imgwrench, ['--help'])
        self.assertEqual(0, help_result.exit_code)
        self.assertIn(help_msg, help_result.output)
        # executing imgwrench without subcommands should have the same effect
        help_result = self.runner.invoke(cli_imgwrench)
        self.assertEqual(0, help_result.exit_code)
        self.assertIn(help_msg, help_result.output)

    def test_subcommand_availability(self):
        '''Test availability of subcommands'''
        self.assertGreaterEqual(len(cli_imgwrench.commands), 3)
        help_result = self.runner.invoke(cli_imgwrench, ['--help'])
        for subcommand in cli_imgwrench.commands:
            self.assertIn(subcommand, help_result.output)
