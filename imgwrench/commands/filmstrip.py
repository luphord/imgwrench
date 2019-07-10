'''Stack images horizontally, creating a filmstrip.'''

import click
from PIL import Image

from ..param import COLOR


def filmstrip(height, frame_width, color, images):
    '''Stack all images horizontally, creating a filmstrip.'''
    images = list(images)
    frame_pixels = round(frame_width * height)
    n = len(images)
    ratios = sum(img.size[0] / img.size[1] for img in images)
    new_width = int(ratios * (height - 2 * frame_pixels)
                    + (n + 1) * frame_pixels)
    new_size = (new_width, height)
    framed_image = Image.new('RGB', new_size, color)
    offset = frame_pixels
    for i, img in enumerate(images):
        w = int(img.size[0] / img.size[1] * (height - 2 * frame_pixels))
        h = height - 2 * frame_pixels
        resized_img = img.resize((w, h), Image.LANCZOS)
        framed_image.paste(resized_img, (offset, frame_pixels))
        offset += w + frame_pixels
    return framed_image


@click.command(name='filmstrip')
@click.option('-s', '--height', type=click.INT, default=2048,
              show_default=True,
              help='height of the filmstrip')
@click.option('-w', '--frame-width', type=click.FLOAT, default=0.025,
              show_default=True,
              help='width of the frame as a fraction of the height ' +
                   ' of the filmstrip')
@click.option('-c', '--color', type=COLOR, default='white',
              show_default=True,
              help='color of the frame as a color name, hex value ' +
                   'or in rgb(...) function form')
def cli_filmstrip(height, frame_width, color):
    '''Stack all images horizontally, creating a filmstrip.'''
    click.echo('Initializing filmstrip with parameters {}'.format(locals()))

    def _filmstrip(images):
        images = list(images)
        yield images[0][0], filmstrip(height, frame_width, color,
                                      [img for info, img in images])

    return _filmstrip
