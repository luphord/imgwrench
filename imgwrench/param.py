'''Custom parameter types for the click-based CLI'''

import click


class Ratio(click.ParamType):
    '''Parameter type representing a ratio or rational number'''
    name = 'ratio'

    def convert(self, value, param, ctx):
        try:
            a, b = value.split(':')
            a, b = float(a), float(b)
            ratio = a / b
        except ValueError:
            try:
                ratio = float(value)
            except ValueError:
                self.fail('{} is not a valid ratio'.format(value), param, ctx)
        if ratio <= 0:
            self.fail('parsed ratio {} is not strictly positive'.format(value),
                      param, ctx)
        return ratio


RATIO = Ratio()
