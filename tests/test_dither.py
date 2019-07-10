#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `dither` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestDither(unittest.TestCase):
    '''Tests for `dither` subcommand.'''

    def test_dither_output(self):
        '''Test output of dither command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'dither_', ['dither', '-b', '1.6'])
