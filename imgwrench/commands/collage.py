'''Create a collage from multiple images.'''

import click

from ..param import COLOR


def collage(images, width, height, frame_width, color):
    '''Create a collage from multiple images.'''
    raise NotImplementedError()


@click.command(name='collage')
@click.option('-w', '--width', type=click.INT, default=3072,
              show_default=True,
              help='width of the collage')
@click.option('-s', '--height', type=click.INT, default=2048,
              show_default=True,
              help='height of the collage')
@click.option('-f', '--frame-width', type=click.FLOAT, default=0.025,
              show_default=True,
              help='width of the frame as a fraction of the longer ' +
                   'image side')
@click.option('-c', '--color', type=COLOR, default='white',
              show_default=True,
              help='color of the frame as a color name, hex value ' +
                   'or in rgb(...) function form')
def cli_collage(width, height, frame_width, color):
    '''Create a collage from multiple images.'''
    click.echo('Initializing collage with parameters {}'.format(locals()))

    def _collage(images):
        images = list(images)
        yield images[0][0], collage(images, width, height, frame_width, color)

    return _collage
