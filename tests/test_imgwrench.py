#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imgwrench` package."""


import unittest
from click.testing import CliRunner

from imgwrench import cli_imgwrench

from .images import pixel1x1


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

    def test_pipeline(self):
        '''Test pipeline functionality'''
        self.assertTrue(cli_imgwrench.chain)
        pipelinetest = 'pipelinetest'

        n_invocations = [0]
        n_image_invocations = [0]

        @cli_imgwrench.command(pipelinetest)
        def _pipelintest():
            n_invocations[0] += 1

            def _process(images):
                for orgfname, image in images:
                    n_image_invocations[0] += 1
                    yield orgfname, image

            return _process

        with self.runner.isolated_filesystem():
            with open('pixel1x1.jpg', 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                for i in range(10):
                    f.write('pixel1x1.jpg\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-i', 'images.txt', pipelinetest,
                                         pipelinetest, pipelinetest])
            self.assertEqual(0, result.exit_code)
            self.assertEqual(3, n_invocations[0], 'expecting 3 processors')
            self.assertEqual(30, n_image_invocations[0], 'expecting 30 calls')
        del cli_imgwrench.commands[pipelinetest]
