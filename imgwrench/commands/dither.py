'''Apply black-white dithering to images.'''

import click
from PIL import ImageEnhance


def dither(image, brightness_factor):
    '''Apply black-white dithering to images.'''
    image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    return image.convert('1')


@click.command(name='dither')
@click.option('-b', '--brightness-factor', type=click.FLOAT, default=1.5,
              show_default=True,
              help='adjust brightness before dithering ' +
                   '(1.0 is neutral, larger is brighter, smaller is darker)')
def cli_dither(brightness_factor):
    '''Apply black-white dithering to images.'''
    click.echo('Initializing dither with parameters {}'.format(locals()))

    def _dither(images):
        for info, image in images:
            yield info, dither(image, brightness_factor)

    return _dither
