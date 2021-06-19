"""Custom parameter types for the click-based CLI"""

import click
from PIL import ImageColor


class Color(click.ParamType):
    """Parameter type representing a color as name, hex or rgb value"""

    name = "color"

    def convert(self, value, param, ctx):
        if isinstance(value, tuple):
            # click 8.0 may pass already parsed parameter values to convert, see
            # https://github.com/pallets/click/issues/1898
            return value
        try:
            return ImageColor.getrgb(value)
        except ValueError:
            self.fail("{} is not a valid color".format(value), param, ctx)


class Ratio(click.ParamType):
    """Parameter type representing a ratio or rational number"""

    name = "ratio"

    def convert(self, value, param, ctx):
        if isinstance(value, float):
            # click 8.0 may pass already parsed parameter values to convert, see
            # https://github.com/pallets/click/issues/1898
            return value
        try:
            a, b = value.split(":")
            a, b = float(a), float(b)
            ratio = a / b
        except ValueError:
            try:
                ratio = float(value)
            except ValueError:
                self.fail("{} is not a valid ratio".format(value), param, ctx)
        if ratio <= 0:
            self.fail(
                "parsed ratio {} is not strictly positive".format(value), param, ctx
            )
        return ratio


COLOR = Color()
RATIO = Ratio()
