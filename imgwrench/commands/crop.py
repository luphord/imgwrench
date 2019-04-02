'''Crop images to the given aspect ratio.'''

from math import floor, ceil

import click

from ..param import RATIO


def crop(image, aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    width, height = image.size[0], image.size[1]
    long_side = max(width, height)
    short_side = min(width, height)
    actual_ratio = long_side / short_side
    target_ratio = max(aspect_ratio, 1 / aspect_ratio)
    # we assume long_side == width and short_side == height
    # if not, we are going to switch later
    if target_ratio > actual_ratio:  # need to crop short side
        crop_pixels = round((1 - actual_ratio / target_ratio)
                            * short_side)
        left = 0
        right = long_side
        upper = floor(crop_pixels / 2)
        lower = short_side - ceil(crop_pixels / 2)
    else:  # need to crop long side
        crop_pixels = round((1 - target_ratio / actual_ratio)
                            * long_side)
        left = floor(crop_pixels / 2)
        right = long_side - ceil(crop_pixels / 2)
        upper = 0
        lower = short_side
    if height > width:
        upper, left = left, upper
        lower, right = right, lower
    return image.crop((left, upper, right, lower))


@click.command(name='crop')
@click.option('-a', '--aspect-ratio', type=RATIO, default='3:2',
              show_default=True,
              help='aspect ratio to crop to')
def cli_crop(aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    click.echo('Initializing crop with parameters {}'.format(locals()))

    def _crop(images):
        for info, image in images:
            yield info, crop(image, aspect_ratio)

    return _crop
