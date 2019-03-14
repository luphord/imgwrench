#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `save` subcommand.'''


import unittest

from click.testing import CliRunner

from .utils import execute_and_test_output_images


class TestBlackwhite(unittest.TestCase):
    '''Tests for `save` subcommand.'''

    def test_saved_output(self):
        '''Test output of saved command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'save_', ['save'])
