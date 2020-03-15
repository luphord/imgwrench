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

    def aspect_ratios(self, container_aspect_ratio):
        '''Calculate aspect ratios of leaf nodes given aspect ratio
           of containing nodes.'''
        raise NotImplementedError('to_string is not implemented')

    def cut_loss(self, container_aspect_ratio):
        '''Sum of fractions of image area that are cut away.'''
        raise NotImplementedError('cut_loss is not implemented')

    def normalized_cut_loss(self, container_aspect_ratio):
        '''Sum of fractions of image area that are cut away
           normalized by number of images.'''
        leaf_count = self.leaf_count
        assert leaf_count > 0, 'Invalid node {}'.format(self)
        return self.cut_loss(container_aspect_ratio) / leaf_count

    def move_images_to_best_aspect_ratios(self, container_aspect_ratio):
        '''Exchange images between leaf nodes of the tree such that they
           are placed ranked according to their aspect ratios.'''
        target_ar = list(self.aspect_ratios(container_aspect_ratio))
        target_ar.sort(key=lambda tpl: tpl[0])
        image_ar = [(leaf.image_aspect_ratio, leaf.image)
                    for _, leaf in target_ar]
        image_ar.sort(key=lambda tpl: tpl[0])
        for (_, node), (_, image) in zip(target_ar, image_ar):
            node.image = image

    @property
    def leaf_count(self):
        return len(list(self.aspect_ratios(1.0)))


class LayoutBranch(LayoutNode):
    '''Non-leaf node in a layout tree structure;
       base class for specific types.'''

    def __init__(self, content):
        self.content = list(content)
        assert self.content, \
            'Cannot create {} without content'.format(self.__class__.__name__)

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

    def aspect_ratios(self, container_aspect_ratio):
        for weight, node in self.normalized_content:
            yield from node.aspect_ratios(container_aspect_ratio * weight)

    def cut_loss(self, container_aspect_ratio):
        '''Sum of fractions of image area that are cut away.'''
        return sum(node.cut_loss(container_aspect_ratio * w)
                   for w, node in self.content)


class Column(LayoutBranch):
    '''Column node in a layout tree structure.'''

    def positions(self, x, y, width, height):
        offset = 0.0
        for w, node in self.normalized_content:
            total_height = w * height
            yield from node.positions(x, y + offset, width, total_height)
            offset += total_height

    def aspect_ratios(self, container_aspect_ratio):
        for weight, node in self.normalized_content:
            yield from node.aspect_ratios(container_aspect_ratio / weight)

    def cut_loss(self, container_aspect_ratio):
        '''Sum of fractions of image area that are cut away.'''
        return sum(node.cut_loss(container_aspect_ratio / w)
                   for w, node in self.content)


class LayoutLeaf:
    '''Leaf node in a layout tree structure; contains a single image.'''

    def __init__(self, image):
        self.image = image

    def positions(self, x, y, width, height):
        yield (x, y, width, height, self.image)

    def to_string(self, indent=0, weight=None):
        w = '{:.2f}'.format(weight) if weight else ''
        yield '{}{} {}'.format(indent * '  ', w, self.__class__.__name__)

    def aspect_ratios(self, container_aspect_ratio):
        yield container_aspect_ratio, self

    @property
    def image_aspect_ratio(self):
        return self.image.size[0] / self.image.size[1]

    def cut_loss(self, container_aspect_ratio):
        '''Fraction of image area that is cut away.'''
        ai = self.image_aspect_ratio
        ac = container_aspect_ratio
        return (ai - ac) / ai if ai > ac else (1/ai - 1/ac) * ai


def random_weight(rnd):
    '''Random variable X in (0, 1].'''
    return 1.0 - rnd.random()


def random_partition(images, rnd):
    '''Partition list of images into a random number of subsets.'''
    n_parts = rnd.randint(1, len(images))
    parts = [list(images[start::n_parts]) for start in range(n_parts)]
    return parts


phi = (1 + 5**0.5) / 2


def _golden_section_tree_recursive(images, aspect_ratio, rnd):
    images = list(images)
    assert images, 'No golden sections layout without images'
    n = len(images)
    if n == 1:
        return LayoutLeaf(images[0])
    else:
        if aspect_ratio > 1:
            layout = Row
            ratios = [aspect_ratio / phi, aspect_ratio / (phi ** 2)]
        else:
            layout = Column
            ratios = [aspect_ratio * phi, aspect_ratio * (phi ** 2)]
        n_first = n // 2
        if n % 2 == 1:
            n_first += rnd.choice([0, 1])
        rnd.shuffle(ratios)
        weights = [ratio if aspect_ratio > 1 else 1 / ratio
                   for ratio in ratios]
        partition = [images[:n_first], images[n_first:]]
        cnt = [(weight, _golden_section_tree_recursive(part, ratio, rnd))
               for weight, ratio, part in zip(weights, ratios, partition)]
        return layout(content=cnt)


def golden_section_tree(images, aspect_ratio, rnd=None):
    '''Create a layout tree structure based on golden sections.'''
    rnd = rnd or random.Random(0)
    return _golden_section_tree_recursive(images, aspect_ratio, rnd)


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
    aspect_ratio = width / height
    tree = golden_section_tree(images, aspect_ratio, rnd)
    loss = tree.normalized_cut_loss(aspect_ratio)
    print('Loss before moving is {:.2f}'.format(loss))
    tree.move_images_to_best_aspect_ratios(aspect_ratio)
    loss = tree.normalized_cut_loss(aspect_ratio)
    print('Loss after moving is {:.2f}'.format(loss))
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
