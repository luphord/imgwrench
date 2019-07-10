#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `filmstrip` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestFilmstrip(unittest.TestCase):
    '''Tests for `filmstrip` subcommand.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()

    def test_filmstrip_output(self):
        '''Test output of filmstrip command.'''
        execute_and_test_output_images(self, self.runner, 6, 1,
                                       'rc_', ['filmstrip', '-s', 10])
