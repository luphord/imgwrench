'''Crop images to the given aspect ratio.'''

from math import floor, ceil

import click


def crop(image, aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    a, b = aspect_ratio.split(':')
    a, b = float(a), float(b)
    actual_ratio = image.size[0] / image.size[1]
    if actual_ratio >= 1:  # landscape
        target_ratio = max(a, b) / min(a, b)
    else:  # portrait
        target_ratio = min(a, b) / max(a, b)
    if target_ratio > actual_ratio:  # need to crop height
        crop_pixels = int((1 - actual_ratio / target_ratio)
                          * image.size[1])
        left = 0
        right = image.size[0]
        upper = floor(crop_pixels / 2)
        lower = image.size[1] - ceil(crop_pixels / 2)
    else:  # need to crop width
        crop_pixels = int((1 - actual_ratio / target_ratio)
                          * image.size[0])
        left = floor(crop_pixels / 2)
        right = image.size[0] - ceil(crop_pixels / 2)
        upper = 0
        lower = image.size[1]
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
