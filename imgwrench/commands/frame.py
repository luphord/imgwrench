'''Put a monocolor frame around images.'''

import click
from PIL import Image

from ..param import COLOR


def frame(image, width, color):
    '''Put a monocolor frame around images.'''
    frame_pixels = round(width * max(image.size))
    new_size = (image.size[0] + 2*frame_pixels, image.size[1] + 2*frame_pixels)
    framed_image = Image.new('RGB', new_size, color)
    framed_image.paste(image, (frame_pixels, frame_pixels))
    return framed_image


@click.command(name='frame')
@click.option('-w', '--frame-width', type=click.FLOAT, default=0.025,
              show_default=True,
              help='width of the frame as a fraction of the longer ' +
                   'image side')
@click.option('-c', '--color', type=COLOR, default='white',
              show_default=True,
              help='color of the frame as a color name, hex value ' +
                   'or in rgb(...) function form')
def cli_frame(frame_width, color):
    '''Put a monocolor frame around images.'''
    click.echo('Initializing frame with parameters {}'.format(locals()))

    def _frame(images):
        for info, image in images:
            yield info, frame(image, frame_width, color)

    return _frame
