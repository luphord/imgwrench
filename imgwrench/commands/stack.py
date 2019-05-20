'''Stack images vertically, empty space in the middle.'''

import click
from PIL import Image


def stack(img1, img2, width, height):
    '''Stack images vertically, empty space in the middle.'''
    ratio1 = min(float(height) / 2 / img1.size[1], float(width) / img1.size[0])
    resized_img1 = img1.resize((int(img1.size[0]*ratio1),
                                int(img1.size[1]*ratio1)),
                               Image.LANCZOS)
    ratio2 = min(float(height) / 2 / img2.size[1], float(width) / img2.size[0])
    resized_img2 = img2.resize((int(img2.size[0]*ratio2),
                                int(img2.size[1]*ratio2)),
                               Image.LANCZOS)
    stacked = Image.new(mode='RGB', size=(width, height),
                        color=(255, 255, 255))
    stacked.paste(resized_img1, (0, 0))
    stacked.paste(resized_img2, (0, height - resized_img2.size[1]))
    return stacked


@click.command(name='stack')
@click.option('-w', '--width', type=click.INT, default=2048,
              show_default=True,
              help='width of the stacked image')
@click.option('-s', '--height', type=click.INT, default=3072,
              show_default=True,
              help='height of the stacked image')
def cli_stack(width, height):
    '''Stacks pairs of images vertically, empty space in the middle.'''
    click.echo('Initializing stack with parameters {}'.format(locals()))

    def _stack(images):
        last_info = None
        last_image = None
        for info, image in images:
            if info.index % 2 == 0:
                last_info = info
                last_image = image
            else:
                yield last_info, stack(last_image, image, width, height)

    return _stack
