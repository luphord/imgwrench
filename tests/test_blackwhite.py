#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `blackwhite` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestBlackwhite(unittest.TestCase):
    '''Tests for `backwhite` subcommand.'''

    def test_blackwhite_output(self):
        '''Test output of blackwhite command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'bw_', ['blackwhite'])
