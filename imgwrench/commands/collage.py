'''Create a collage from multiple images.'''

import random

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

    def to_json(self):
        content_json = [(w, node.to_json())
                        for w, node in self.normalized_content]
        return dict(node_type=self.__class__.__name__,
                    content=content_json)


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

    def to_json(self):
        return self.__class__.__name__


def random_weight(rnd):
    return 1.0 - rnd.random()


def random_partition(images, rnd):
    n_parts = rnd.randint(1, len(images))
    parts = [list(images[start::n_parts]) for start in range(n_parts)]
    return parts


def random_tree_recursive(images, contained_in, rnd):
    images = list(images)
    rnd.shuffle(images)
    if not images:
        raise Exception('No random layout without images')
    if len(images) <= 2:
        for img in images:
            yield random_weight(rnd), Leaf(img)
    else:
        layout = Column if contained_in == Row else Row
        for part in random_partition(images, rnd):
            rnd_cnt = list(random_tree_recursive(part, layout, rnd))
            yield random_weight(rnd), layout(content=rnd_cnt)


def random_tree(images):
    rnd = random.Random(123)
    root_layout = rnd.choice([Row, Column])
    rnd_cnt = list(random_tree_recursive(images, root_layout, rnd))
    return root_layout(content=rnd_cnt)


def crop(img, width, height):
    '''Center crop image and resize to width * height'''
    return img.resize((width, height), Image.LANCZOS)


def render(tree, width, height, frame_width, color):
    collg = Image.new('RGB', (width, height), color)
    frame_half_pixels = round(frame_width * max(width, height) / 2)
    frame_pixels = frame_half_pixels * 2
    inner_width = width - frame_pixels
    inner_height = height - frame_pixels
    for (x, y, w, h, img) in tree.positions(frame_half_pixels,
                                            frame_half_pixels,
                                            inner_width, inner_height):
        inner_w = int(w) - frame_pixels
        inner_h = int(h) - frame_pixels
        inner_x = int(x) + frame_half_pixels
        inner_y = int(y) + frame_half_pixels
        resized_img = crop(img, inner_w, inner_h)
        collg.paste(resized_img, (inner_x, inner_y))
    return collg


def collage(images, width, height, frame_width, color):
    '''Create a collage from multiple images.'''
    return render(random_tree(images), width, height, frame_width, color)


@click.command(name='collage')
@click.option('-w', '--width', type=click.INT, default=3072,
              show_default=True,
              help='width of the collage')
@click.option('-s', '--height', type=click.INT, default=2048,
              show_default=True,
              help='height of the collage')
@click.option('-f', '--frame-width', type=click.FLOAT, default=0.01,
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
