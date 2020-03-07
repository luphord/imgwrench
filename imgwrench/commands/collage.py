'''Create a collage from multiple images.'''

import random
from math import floor, ceil

import click
from PIL import Image

from ..param import COLOR


class LayoutNode:
    '''Node in a layout tree structure; base class for specific types.'''

    def to_string(self, indent=0, weight=None):
        raise NotImplementedError('to_string is not implemented')

    def __str__(self):
        return '\n'.join(self.to_string())


class LayoutBranch(LayoutNode):
    '''Non-leaf node in a layout tree structure;
       base class for specific types.'''

    def __init__(self, content):
        self.content = list(content)

    @property
    def normalized_content(self):
        total = sum(w for w, _ in self.content)
        return [(w / total, node) for w, node in self.content]

    def to_string(self, indent=0, weight=None):
        yield '{}{} {}:'.format(indent * '  ',
                                '{:.2f}'.format(weight) if weight else '',
                                self.__class__.__name__)
        for weight, node in self.normalized_content:
            yield from node.to_string(indent + 1, weight)


class Row(LayoutBranch):
    '''Row node in a layout tree structure.'''

    def positions(self, x, y, width, height):
        offset = 0.0
        for w, node in self.normalized_content:
            total_width = w * width
            yield from node.positions(x + offset, y, total_width, height)
            offset += total_width


class Column(LayoutBranch):
    '''Column node in a layout tree structure.'''

    def positions(self, x, y, width, height):
        offset = 0.0
        for w, node in self.normalized_content:
            total_height = w * height
            yield from node.positions(x, y + offset, width, total_height)
            offset += total_height


class LayoutLeaf:
    '''Leaf node in a layout tree structure; contains a single image.'''

    def __init__(self, image):
        self.image = image

    def positions(self, x, y, width, height):
        yield (x, y, width, height, self.image)

    def to_string(self, indent=0, weight=None):
        w = '{:.2f}'.format(weight) if weight else ''
        yield '{}{} {}'.format(indent * '  ', w, self.__class__.__name__)


def random_weight(rnd):
    '''Random variable X in (0, 1].'''
    return 1.0 - rnd.random()


def random_partition(images, rnd):
    '''Partition list of images into a random number of subsets.'''
    n_parts = rnd.randint(1, len(images))
    parts = [list(images[start::n_parts]) for start in range(n_parts)]
    return parts


def _random_tree_recursive(images, contained_in, rnd):
    images = list(images)
    if not images:
        raise Exception('No random layout without images')
    if len(images) <= 2:
        for img in images:
            yield random_weight(rnd), LayoutLeaf(img)
    else:
        layout = Column if contained_in == Row else Row
        for part in random_partition(images, rnd):
            rnd_cnt = list(_random_tree_recursive(part, layout, rnd))
            yield random_weight(rnd), layout(content=rnd_cnt)


def random_tree(images, rnd=None):
    '''Create a random layout tree structure.'''
    rnd = rnd or random.Random(0)
    rnd.shuffle(images)
    root_layout = rnd.choice([Row, Column])
    rnd_cnt = list(_random_tree_recursive(images, root_layout, rnd))
    return root_layout(content=rnd_cnt)


def crop(image, width, height):
    '''Center crop image and resize to width * height.'''
    actual_ratio = image.size[0] / image.size[1]
    target_ratio = width / height
    if target_ratio > actual_ratio:  # need to crop height
        crop_pixels = round((1 - actual_ratio / target_ratio)
                            * image.size[1])
        left = 0
        right = image.size[0]
        upper = floor(crop_pixels / 2)
        lower = image.size[1] - ceil(crop_pixels / 2)
    else:  # need to crop width
        crop_pixels = round((1 - target_ratio / actual_ratio)
                            * image.size[0])
        left = floor(crop_pixels / 2)
        right = image.size[0] - ceil(crop_pixels / 2)
        upper = 0
        lower = image.size[1]
    image = image.crop((left, upper, right, lower))
    return image.resize((width, height), Image.LANCZOS)


def render(tree, width, height, frame_width, color):
    '''Render layout tree structure to given width and height
       with specified frame; returns a PIL.Image.'''
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


def collage(images, width, height, frame_width, color, rnd=None):
    '''Create a collage from multiple images.'''
    tree = random_tree(images, rnd)
    return render(tree, width, height, frame_width, color)


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
        rnd = random.Random(123)
        yield image_infos[0][0], \
            collage(images, width, height, frame_width, color, rnd)

    return _collage
