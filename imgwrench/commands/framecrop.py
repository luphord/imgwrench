'''Crop and frame an image to a target aspect ratio.'''
from math import floor

import click

from ..param import COLOR, RATIO
from .crop import crop
from .frame import frame


def _floor(x, digits):
    return floor(x*10**digits) / 10**digits


def _unachievable_ratio_msg(target_ratio, frame_width):
    max_frame = _floor(1 / (2*(target_ratio-1)), 2)
    max_ratio = _floor(1 + 1/(2*frame_width), 2)
    return 'Unachievable target ratio; ' + \
           'reduce frame width to < {}'.format(max_frame) + \
           ' or aspect ratio to < {}'.format(max_ratio)


def crop_ratio(target_ratio, frame_width):
    '''Computes the crop ratio for a framecrop operation
       such that the resulting image matches `target_ratio`
       and has a frame of width `frame_width`
    '''
    target_ratio = max(target_ratio, 1 / target_ratio)
    assert target_ratio < 1 + 1 / (2 * frame_width), \
        _unachievable_ratio_msg(target_ratio, frame_width)
    return target_ratio / (1 + 2*frame_width*(1-target_ratio))


def framecrop(image, aspect_ratio, width, color):
    '''Crop and frame an image to a target aspect ratio.'''
    cropped_image = crop(image, crop_ratio(aspect_ratio, width))
    return frame(cropped_image, width, color)


@click.command(name='framecrop')
@click.option('-a', '--aspect-ratio', type=RATIO, default='3:2',
              show_default=True,
              help='aspect ratio of final image including frame')
@click.option('-w', '--frame-width', type=click.FLOAT, default=0.025,
              show_default=True,
              help='width of the frame as a fraction of the longer ' +
                   ' side of the cropped image')
@click.option('-c', '--color', type=COLOR, default='white',
              show_default=True,
              help='color of the frame as a color name, hex value ' +
                   'or in rgb(...) function form')
def cli_framecrop(aspect_ratio, frame_width, color):
    '''Crop and frame an image to a target aspect ratio.'''
    click.echo('Initializing framecrop with parameters {}'.format(locals()))
    # for side effect of checking valid aspect_ratio and frame_width:
    crop_ratio(aspect_ratio, frame_width)

    def _framecrop(images):
        for info, image in images:
            yield info, framecrop(image, aspect_ratio, frame_width, color)

    return _framecrop
