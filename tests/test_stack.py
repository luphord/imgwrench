#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `stack` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestStack(unittest.TestCase):
    '''Tests for `stack` subcommand.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()

    def test_stacked_output(self):
        '''Test output of stack command.'''
        execute_and_test_output_images(self, self.runner, 6, 3,
                                       'stacked_', ['stack'])
