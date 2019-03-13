#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `stack` subcommand.'''


import os
import unittest
from click.testing import CliRunner

from imgwrench import cli_imgwrench

from .images import pixel1x1


class TestStack(unittest.TestCase):
    '''Tests for `stack` subcommand.'''

    def setUp(self):
        '''Set up test fixtures, if any.'''
        self.runner = CliRunner()

    def test_stacked_output(self):
        '''Test output of stack command'''
        prefix = 'stacked_'
        n_output = 3
        with self.runner.isolated_filesystem():
            with open('pixel1x1.jpg', 'wb') as f:
                f.write(pixel1x1)
            with open('images.txt', 'w') as f:
                for i in range(n_output * 2):
                    f.write('pixel1x1.jpg\n')
            result = self.runner.invoke(cli_imgwrench,
                                        ['-p', prefix,
                                         '-d', 4,
                                         '-i', 'images.txt', 'stack'])
            self.assertEqual(0, result.exit_code)
            for i in range(n_output):
                fname = '{}{:04d}.jpg'.format(prefix, i)
                self.assertTrue(os.path.exists(fname), fname + ' missing')
