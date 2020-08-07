'''Collects four images to a quad.'''

from itertools import islice

import click
from PIL import Image

from .crop import crop
from .resize import resize


def quad(quad_images, width, height):
    assert quad_images
    assert len(quad_images) <= 4
    width, height = max(width, height), min(width, height)
    result = Image.new(mode='RGB', size=(width, height),
                       color=(0, 0, 0))
    for i, (info, img) in enumerate(quad_images):
        if img.size[0] < img.size[1]:
            img = img.transpose(Image.ROTATE_90)
        img = crop(img, width / height)
        img = resize(img, width / 2)
        result.paste(img, (int(i % 2 * width/2), int(int(i/2) * height/2)))
    return quad_images[0][0], result


@click.command(name='quad')
@click.option('-w', '--width', type=click.INT, default=3072,
              show_default=True,
              help='width of the quad image')
@click.option('-s', '--height', type=click.INT, default=2048,
              show_default=True,
              help='height of the quad image')
def cli_quad(width, height):
    '''Collects four images to a quad.'''
    click.echo('Initializing quad with parameters {}'.format(locals()))

    def _quad(images):
        images = iter(images)
        while True:
            quad_images = list(islice(images, 4))
            if quad_images:
                yield quad(quad_images, width, height)
            else:
                break

    return _quad
