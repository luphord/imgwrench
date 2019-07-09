'''Apply black-white dithering to images.'''

import click


def dither(image):
    '''Apply black-white dithering to images.'''
    return image.convert('1')


@click.command(name='dither')
def cli_dither():
    '''Apply black-white dithering to images.'''
    click.echo('Initializing dither with parameters {}'.format(locals()))

    def _dither(images):
        for info, image in images:
            yield info, dither(image)

    return _dither
