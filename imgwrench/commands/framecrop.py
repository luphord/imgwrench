'''Crop and frame an image to a target aspect ratio.'''

import click

from ..param import COLOR, RATIO
from .crop import crop
from .frame import frame


def crop_ratio(target_ratio, frame_width):
    '''Computes the crop ratio for a framecrop operation
       such that the resulting image matches `target_ratio`
       and has a frame of width `frame_width`
    '''
    target_ratio = max(target_ratio, 1 / target_ratio)
    return target_ratio / (1 + 2*frame_width*(1-target_ratio))


def framecrop(image, aspect_ratio, width, color):
    '''Crop and frame an image to a target aspect ratio.'''
    cropped_image = crop(image, crop_ratio(aspect_ratio, width))
    return frame(cropped_image, width, color)


@click.command(name='framecrop')
@click.option('-a', '--aspect-ratio', type=RATIO, default='3:2',
              help='aspect ratio of final image including frame, ' +
                   'defaults to "3:2"')
@click.option('-w', '--frame-width', type=click.FLOAT, default=0.025,
              help='width of the frame as a fraction of the longer ' +
                   ' side of the cropped image (default: 0.025)')
@click.option('-c', '--color', type=COLOR, default='white',
              help='color of the frame as a color name, hex value ' +
                   'or in rgb(...) function form (default: white)')
def cli_framecrop(aspect_ratio, frame_width, color):
    '''Crop and frame an image to a target aspect ratio.'''
    click.echo('Initializing framecrop with parameters {}'.format(locals()))

    def _framecrop(images):
        for orgfname, image in images:
            yield orgfname, framecrop(image, aspect_ratio, frame_width, color)

    return _framecrop
