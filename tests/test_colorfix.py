#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `colorfix` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestBlackwhite(unittest.TestCase):
    '''Tests for `colorfix` subcommand.'''

    def test_colorfixed_output(self):
        '''Test output of colorfix command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'colorfix_', ['colorfix'])
