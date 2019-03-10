'''Test custom parameter types.'''

import unittest

from click.exceptions import BadParameter

from imgwrench.param import RATIO, COLOR


def _color(value):
    return COLOR.convert(value, None, None)


class TestColor(unittest.TestCase):
    '''Test for `COLOR` custom parameter type'''

    def test_color_names(self):
        '''Test colors specified as name.'''
        self.assertEqual((0, 0, 0), _color('black'))
        self.assertEqual((255, 255, 255), _color('white'))
        self.assertEqual((255, 0, 0), _color('red'))
        self.assertEqual((0, 255, 0), _color('lime'))
        self.assertEqual((0, 0, 255), _color('blue'))
        self.assertEqual((0, 128, 0), _color('green'))
        self.assertEqual((255, 255, 0), _color('yellow'))

    def test_hex_colors(self):
        '''Test colors specified as hex values.'''
        self.assertEqual((0, 0, 0), _color('#000'))
        self.assertEqual((0, 0, 0), _color('#000000'))
        self.assertEqual((255, 255, 255), _color('#fff'))
        self.assertEqual((240, 230, 140), _color('#F0E68C'))

    def test_rgb_colors(self):
        '''Test colors specified as rgb function values.'''
        self.assertEqual((0, 0, 0), _color('rgb(0,0,0)'))
        self.assertEqual((255, 255, 255), _color('rgb(255, 255, 255)'))
        self.assertEqual((240, 230, 140), _color('rgb(240, 230, 140)'))

    def test_bad_colors(self):
        '''Test several bad color specifications which must raise errors.'''
        bad_colors = ['asd', '0', '0.0', 'greenish', '#1', 'rgb()', 'rgb(0)']
        for bad_color in bad_colors:
            with self.assertRaises(BadParameter):
                _color(bad_color)


def _ratio(value):
    return RATIO.convert(value, None, None)


class TestRatio(unittest.TestCase):
    '''Test for `RATIO` custom parameter type.'''

    def test_float_ratios(self):
        '''Test several good ratio specifications as floating points.'''
        self.assertEqual(1.0, _ratio('1'))
        self.assertEqual(2.0, _ratio('2'))
        self.assertEqual(1.23, _ratio('1.23'))
        self.assertEqual(0.333, _ratio('0.333'))

    def test_colon_ratios(self):
        '''Test several good ratio specifications using colons.'''
        self.assertEqual(1.0, _ratio('1:1'))
        self.assertEqual(2.0, _ratio('2:1'))
        self.assertEqual(1.5, _ratio('3:2'))
        self.assertEqual(2/3, _ratio('2:3'))
        self.assertEqual(1.23, _ratio('123:100'))
        self.assertEqual(1/3, _ratio('1:3'))
        self.assertEqual(1/3, _ratio('-1:-3'))

    def test_bad_ratios(self):
        '''Test several bad ratio specifications which must raise errors.'''
        bad_ratios = ['asd', '0', '0.0', '0:1', '-1', '-1.2', '-1:3',
                      'one half', '']
        for bad_ratio in bad_ratios:
            with self.assertRaises(BadParameter):
                _ratio(bad_ratio)
