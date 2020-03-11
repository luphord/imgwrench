#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `colorfix` subcommand.'''


import unittest
from io import BytesIO
from base64 import encodebytes

from click.testing import CliRunner
from imgwrench.commands.colorfix import quantiles, colorfix_quantiles, \
    colorfix_fixed_cutoff, colorfix_quantiles_fixed_cutoff

from .utils import execute_and_test_output_images
from .images import colorcast_img, colorcast_fixed_001, colorcast_fixed_002, \
    colorcast_fixed_003, colorcast_fixed_005, colorcast_cutoff_boundaries, \
    colorcast_cutoff_red, colorcast_cutoff_middle, \
    colorcast_cutoff_combined_middle, colorcast_cutoff_combined_red


# targets for quantile regression test: (level, target)
QUANTILES_TARGETS = [
    (0.01, ((167, 252), (53, 218), (32, 207))),
    (0.02, ((169, 249), (56, 215), (35, 202))),
    (0.03, ((171, 247), (60, 213), (37, 200))),
    (0.05, ((174, 244), (69, 208), (44, 195)))
]


# targets for colorfix quantiles algorithm regression test:
# (level, target)
IMAGES_TARGETS = [
    (0.01, colorcast_fixed_001),
    (0.02, colorcast_fixed_002),
    (0.03, colorcast_fixed_003),
    (0.05, colorcast_fixed_005)
]

# targets for colorfix fixed-cutoff algorithm regression test:
# (lower_cutoff, upper_cutoff, target)
IMAGES_FIXED_CUTOFF_TARGETS = [
    ((0, 0, 0), (255, 255, 255), colorcast_cutoff_boundaries),
    ((150, 0, 0), (255, 255, 255), colorcast_cutoff_red),
    ((12, 34, 56), (111, 222, 233), colorcast_cutoff_middle)
]


# targets for colorfix quantiles-fixed-cutoff algorithm regression test:
# (level, lower_cutoff, upper_cutoff, target)
IMAGES_QUANTILES_FIXED_CUTOFF_TARGETS = [
    (0.01, (0, 0, 0), (255, 255, 255), colorcast_fixed_001),
    (0.05, (0, 0, 0), (255, 255, 255), colorcast_fixed_005),
    (0.02, (12, 34, 56), (111, 222, 233), colorcast_cutoff_combined_middle),
    (0.01, (127, 0, 0), (255, 255, 255), colorcast_cutoff_combined_red)
]


def _tobytes(img):
    b = BytesIO()
    img.save(b, format='JPEG')
    return b.getvalue()


def _b64encode(img):
    return encodebytes(_tobytes(img)).decode('ascii')


class TestBlackwhite(unittest.TestCase):
    '''Tests for `colorfix` subcommand.'''

    def test_colorfixed_output(self):
        '''Test output of colorfix command.'''
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'colorfix_', ['colorfix'])

    def test_colorfixed_output_quantiles(self):
        '''Test output of colorfix command with quantiles.'''
        args = ['colorfix', '-m', 'quantiles']
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'colorfix_', args)

    def test_colorfixed_output_fixed_cutoff(self):
        '''Test output of colorfix command with fixed-cutoff.'''
        args = ['colorfix', '-m', 'fixed-cutoff']
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'colorfix_', args)

    def test_colorfixed_output_quantiles_fixed_cutoff(self):
        '''Test output of colorfix command with quantiles-fixed-cutoff.'''
        args = ['colorfix', '-m', 'quantiles-fixed-cutoff']
        execute_and_test_output_images(self, CliRunner(), 3, 3,
                                       'colorfix_', args)

    def test_quantiles(self):
        '''Regression test for quantiles.'''
        for level, target in QUANTILES_TARGETS:
            self.assertEqual(target, quantiles(colorcast_img, level),
                             'level {} fail'.format(level))

    def test_colorfix_quantiles_regression(self):
        '''Regression test for colorfix quantiles algorithm.'''
        for level, target in IMAGES_TARGETS:
            cf = colorfix_quantiles(colorcast_img.copy(), level)
            self.assertEqual(target, _tobytes(cf),
                             'level {} fail'.format(level))

    def test_colorfix_fixed_cutoff_regression(self):
        '''Regression test for colorfix fixed-cutoff algorithm.'''
        for lower_cutoff, upper_cutoff, target in IMAGES_FIXED_CUTOFF_TARGETS:
            cf = colorfix_fixed_cutoff(colorcast_img.copy(),
                                       lower_cutoff, upper_cutoff)
            self.assertEqual(target, _tobytes(cf),
                             'cutoff {} - {} fail'.format(lower_cutoff,
                                                          upper_cutoff))

    def test_colorfix_quantiles_fixed_cutoff_regression(self):
        '''Regression test for colorfix fixed-cutoff algorithm.'''
        for alpha, lower_cutoff, upper_cutoff, target in \
                IMAGES_QUANTILES_FIXED_CUTOFF_TARGETS:
            cf = colorfix_quantiles_fixed_cutoff(colorcast_img.copy(),
                                                 alpha,
                                                 lower_cutoff,
                                                 upper_cutoff)
            if target != _tobytes(cf):
                print(_b64encode(cf))
            self.assertEqual(target, _tobytes(cf),
                             'cutoff {} / {} - {} fail'.format(alpha,
                                                               lower_cutoff,
                                                               upper_cutoff))
