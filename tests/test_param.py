'''Test custom parameter types.'''

import unittest

from click.exceptions import BadParameter

from imgwrench.param import RATIO


def _ratio(value):
    return RATIO.convert(value, None, None)


class TestRatio(unittest.TestCase):
    '''Test for `crop` command.'''

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
