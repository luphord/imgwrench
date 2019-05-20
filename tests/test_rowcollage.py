#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `rowcollage` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestRowCollage(unittest.TestCase):
    '''Tests for `rowcollage` subcommand.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()

    def test_rowcollage_output(self):
        '''Test output of rowcollage command.'''
        execute_and_test_output_images(self, self.runner, 6, 1,
                                       'rc_', ['rowcollage', '-s', 10])
