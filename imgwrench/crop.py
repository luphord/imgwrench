'''Crop images to the given aspect ratio.'''

from math import floor, ceil

import click


def crop(image, aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    a, b = aspect_ratio.split(':')
    a, b = float(a), float(b)
    width, height = image.size[0], image.size[1]
    long_side = max(width, height)
    short_side = min(width, height)
    actual_ratio = long_side / short_side
    target_ratio = max(a, b) / min(a, b)
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
@click.option('-a', '--aspect-ratio', type=click.STRING, default='3:2',
              help='aspect ratio to crop to, defaults to "3:2"')
def cli_crop(aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    click.echo('Initializing crop with parameters {}'.format(locals()))

    def _crop(images):
        for orgfname, image in images:
            yield orgfname, crop(image, aspect_ratio)

    return _crop
