'''Create a collage from multiple images.'''

import click
from PIL import Image

from ..param import COLOR


class Branch:
    def __init__(self, content):
        self.content = list(content)

    @property
    def normalized_content(self):
        total = sum(w for w, _ in self.content)
        return [(w / total, node) for w, node in self.content]


class Row(Branch):
    def positions(self, x, y, width, height):
        offset = 0.0
        for w, node in self.normalized_content:
            total_width = w * width
            yield from node.positions(x + offset, y, total_width, height)
            offset += total_width


class Column(Branch):
    def positions(self, x, y, width, height):
        offset = 0.0
        for w, node in self.normalized_content:
            total_height = w * height
            yield from node.positions(x, y + offset, width, total_height)
            offset += total_height


class Leaf:
    def __init__(self, image):
        self.image = image

    def positions(self, x, y, width, height):
        yield (x, y, width, height, self.image)


def render(tree, width, height, frame_width, color):
    collg = Image.new('RGB', (width, height), color)
    for (x, y, w, h, img) in tree.positions(0, 0, width, height):
        resized_img = img.resize((int(w), int(h)), Image.LANCZOS)
        collg.paste(resized_img, (int(x), int(y)))
    return collg


def collage(images, width, height, frame_width, color):
    '''Create a collage from multiple images.'''
    row = Row((1.0, Leaf(img)) for img in images[1:])
    col = Column([(1.0, Leaf(images[0])), (1.0, row)])
    return render(col, width, height, frame_width, color)


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

    def _collage(image_infos):
        image_infos = list(image_infos)
        images = [img for _, img in image_infos]
        yield image_infos[0][0], \
            collage(images, width, height, frame_width, color)

    return _collage
