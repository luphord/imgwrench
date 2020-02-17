#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `colorfix` subcommand.'''


import unittest
from io import BytesIO
from base64 import encodebytes

from click.testing import CliRunner
from imgwrench.commands.colorfix import quantiles, colorfix

from .utils import execute_and_test_output_images
from .images import colorcast_img, colorcast_fixed_001, colorcast_fixed_002, \
    colorcast_fixed_003, colorcast_fixed_005


# targets for quantile regression test: (level, target)
QUANTILES_TARGETS = [
    (0.01, ((167, 252), (53, 218), (32, 207))),
    (0.02, ((169, 249), (56, 215), (35, 202))),
    (0.03, ((171, 247), (60, 213), (37, 200))),
    (0.05, ((174, 244), (69, 208), (44, 195)))
]


# targets for colorfix algorithm regression test: (level, target)
IMAGES_TARGETS = [
    (0.01, colorcast_fixed_001),
    (0.02, colorcast_fixed_002),
    (0.03, colorcast_fixed_003),
    (0.05, colorcast_fixed_005)
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

    def test_quantiles(self):
        '''Regression test for quantiles.'''
        for level, target in QUANTILES_TARGETS:
            self.assertEqual(target, quantiles(colorcast_img, level),
                             'level {} fail'.format(level))

    def test_colorfix_regression(self):
        '''Regression test for colorfix algorithm.'''
        for level, target in IMAGES_TARGETS:
            cf = colorfix(colorcast_img.copy(), level)
            self.assertEqual(target, _tobytes(cf),
                             'level {} fail'.format(level))
