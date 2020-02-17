#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `colorfix` subcommand.'''


import unittest

from click.testing import CliRunner
from imgwrench.commands.colorfix import quantiles

from .utils import execute_and_test_output_images
from .images import colorcast_img


# targets for quantile regression test: (level, target)
QUANTILES_TARGETS = [
    (0.01, ((167, 252), (53, 218), (32, 207))),
    (0.02, ((169, 249), (56, 215), (35, 202))),
    (0.03, ((171, 247), (60, 213), (37, 200))),
    (0.05, ((174, 244), (69, 208), (44, 195)))
]


class TestBlackwhite(unittest.TestCase):
    '''Tests for `colorfix` subcommand.'''

    def test_colorfixed_output(self):
        '''Test output of colorfix command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'colorfix_', ['colorfix'])

    def test_quantiles(self):
        '''Regression test for quantiles.'''
        for level, target in QUANTILES_TARGETS:
            self.assertEqual(target, quantiles(colorcast_img, level))
