'''Resize images to a maximum side length preserving aspect ratio.'''

import click
from PIL import Image


def resize(image, maxsize):
    '''Resize image to maxsize (longer) side length preserving aspect ratio.'''
    ratio = float(maxsize) / max(image.size)
    return image.resize((int(image.size[0]*ratio), int(image.size[1]*ratio)),
                        Image.LANCZOS)


@click.command(name='resize')
@click.option('-m', '--maxsize', type=click.INT, default=1024,
              help='size of the longer side (width or height) in pixels')
def cli_resize(maxsize):
    '''Resize images to a maximum side length preserving aspect ratio.'''
    click.echo('Initializing colorfix with parameters {}'.format(locals()))

    def _resize(images):
        for orgfname, image in images:
            yield orgfname, resize(image, maxsize)

    return _resize
