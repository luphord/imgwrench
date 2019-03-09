'''Custom parameter types for the click-based CLI'''

import click


class Ratio(click.ParamType):
    '''Parameter type representing a ratio or rational number'''
    name = 'ratio'

    def convert(self, value, param, ctx):
        try:
            a, b = value.split(':')
            a, b = float(a), float(b)
            return a / b
        except ValueError:
            self.fail('{} is not a valid ratio'.format(value), param, ctx)


RATIO = Ratio()
