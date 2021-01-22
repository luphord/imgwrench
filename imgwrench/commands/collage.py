"""Create a collage from multiple images."""

import random
from math import floor, ceil
from abc import ABC, abstractmethod

import click
from PIL import Image
import numpy as np

from ..param import COLOR


class LayoutNode(ABC):
    """Node in a layout tree structure; base class for specific types."""

    @abstractmethod
    def to_string(self, indent=0, weight=None):
        raise NotImplementedError("to_string is not implemented")

    def __str__(self):
        return "\n".join(self.to_string())

    @abstractmethod
    def positions(self, x, y, width, height):
        """Positions of individual images"""
        pass

    @abstractmethod
    def aspect_ratios(self, container_aspect_ratio):
        """Calculate aspect ratios of leaf nodes given aspect ratio
        of containing nodes."""
        raise NotImplementedError("to_string is not implemented")

    @abstractmethod
    def cut_loss(self, container_aspect_ratio):
        """Sum of fractions of image area that are cut away."""
        raise NotImplementedError("cut_loss is not implemented")

    def normalized_cut_loss(self, container_aspect_ratio):
        """Sum of fractions of image area that are cut away
        normalized by number of images."""
        leaf_count = self.leaf_count
        assert leaf_count > 0, "Invalid node {}".format(self)
        return self.cut_loss(container_aspect_ratio) / leaf_count

    def relative_areas(self, width, height):
        """Relative area of leaf nodes"""
        area = width * height
        for (x, y, w, h, img) in self.positions(0, 0, width, height):
            yield w * h / area

    def balance_score(self, width, height):
        """Score function penalizing different image sizes.
        Between 0 and 1. Equal to 1 if every image has the same area."""
        target_area = 1 / self.leaf_count
        areas = np.array(list(self.relative_areas(width, height)))
        return np.prod(np.minimum(areas / target_area, 1)) ** target_area

    def score(self, width, height):
        """Score function to compare layouts, between 0 (worst) and 1 (best)."""
        return (1 - self.normalized_cut_loss(width / height)) * self.balance_score(
            width, height
        )

    @property
    def leaf_count(self):
        return len(list(self.aspect_ratios(1.0)))

    @property
    def leafs(self):
        for _, node in self.aspect_ratios(1.0):
            yield node

    @property
    def leafs_index(self):
        return {node: i for i, node in enumerate(self.leafs)}

    @abstractmethod
    def width_height_coeff(self):
        """width, height and coefficients for system of linear equation
        as required by BRIC algorithm"""
        pass

    @abstractmethod
    def set_weights_from_widths(tree, widths):
        pass

    @property
    def linear_equations(self):
        width, height, coeff = self.width_height_coeff()
        leafs = self.leafs_index
        a = np.zeros(shape=(len(leafs), len(leafs)))
        for row, c in enumerate(coeff + [width]):
            for node, w in c.items():
                a[row, leafs[node]] = w
        b = np.zeros(shape=len(leafs))
        b[-1] = 1
        return a, b


class LayoutBranch(LayoutNode):
    """Non-leaf node in a layout tree structure;
    base class for specific types."""

    def __init__(self, content):
        self.content = list(content)
        assert self.content, "Cannot create {} without content".format(
            self.__class__.__name__
        )

    @property
    def normalized_content(self):
        total = sum(w for w, _ in self.content)
        return [(w / total, node) for w, node in self.content]

    def to_string(self, indent=0, weight=None):
        yield "{}{} {}:".format(
            indent * "  ",
            "{:.2f}".format(weight) if weight else "",
            self.__class__.__name__,
        )
        for weight, node in self.normalized_content:
            yield from node.to_string(indent + 1, weight)


class Row(LayoutBranch):
    """Row node in a layout tree structure."""

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
        """Sum of fractions of image area that are cut away."""
        return sum(
            node.cut_loss(container_aspect_ratio * w) for w, node in self.content
        )

    def width_height_coeff(self):
        width = {}
        height = {}
        coeff = []
        h0 = None
        for _, node in self.content:
            wi, hi, ci = node.width_height_coeff()
            width.update(wi)
            coeff.extend(ci)
            if h0:
                same_height_rule = {**h0, **{k: -v for k, v in hi.items()}}
                coeff.append(same_height_rule)
            else:
                h0 = hi
                height.update(hi)
        return width, height, coeff

    def set_weights_from_widths(self, widths_index):
        nodes = [node for _, node in self.content]
        widths_heights = [node.set_weights_from_widths(widths_index) for node in nodes]
        widths = [w for w, _ in widths_heights]
        sum_widths = sum(widths)
        rel_widths = [w / sum_widths for w in widths]
        self.content = list(zip(rel_widths, nodes))
        return sum_widths, widths_heights[0][1]


class Column(LayoutBranch):
    """Column node in a layout tree structure."""

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
        """Sum of fractions of image area that are cut away."""
        return sum(
            node.cut_loss(container_aspect_ratio / w) for w, node in self.content
        )

    def width_height_coeff(self):
        width = {}
        height = {}
        coeff = []
        w0 = None
        for _, node in self.content:
            wi, hi, ci = node.width_height_coeff()
            height.update(hi)
            coeff.extend(ci)
            if w0:
                same_width_rule = {**w0, **{k: -v for k, v in wi.items()}}
                coeff.append(same_width_rule)
            else:
                w0 = wi
                width.update(wi)
        return width, height, coeff

    def set_weights_from_widths(self, widths_index):
        nodes = [node for _, node in self.content]
        widths_heights = [node.set_weights_from_widths(widths_index) for node in nodes]
        heights = [h for _, h in widths_heights]
        sum_heights = sum(heights)
        rel_heights = [h / sum_heights for h in heights]
        self.content = list(zip(rel_heights, nodes))
        return widths_heights[0][0], sum_heights


class LayoutLeaf(LayoutNode):
    """Leaf node in a layout tree structure; contains a single image."""

    def __init__(self, image):
        self.image = image

    def positions(self, x, y, width, height):
        yield (x, y, width, height, self.image)

    def to_string(self, indent=0, weight=None):
        w = "{:.2f}".format(weight) if weight else ""
        yield "{}{} {}".format(indent * "  ", w, self.__class__.__name__)

    def aspect_ratios(self, container_aspect_ratio):
        yield container_aspect_ratio, self

    @property
    def image_aspect_ratio(self):
        return self.image.size[0] / self.image.size[1]

    def cut_loss(self, container_aspect_ratio):
        """Fraction of image area that is cut away."""
        ai = self.image_aspect_ratio
        ac = container_aspect_ratio
        return (ai - ac) / ai if ai > ac else (1 / ai - 1 / ac) * ai

    def width_height_coeff(self):
        return {self: 1}, {self: 1 / self.image_aspect_ratio}, []

    def set_weights_from_widths(self, widths_index):
        return widths_index[self], widths_index[self] / self.image_aspect_ratio


def _binary_tree_recursive(images, rnd, is_row):
    images = list(images)
    assert images, "No binary tree layout without images"
    layout = Row if is_row else Column
    if len(images) == 1:
        return LayoutLeaf(images[0])
    elif len(images) == 2:
        return layout([(1, LayoutLeaf(images[0])), (1, LayoutLeaf(images[1]))])
    else:
        n = rnd.randint(1, len(images) - 1)
        left = _binary_tree_recursive(images[:n], rnd, not is_row)
        right = _binary_tree_recursive(images[n:], rnd, not is_row)
        return layout([(1, left), (1, right)])


def bric_tree(images, aspect_ratio, rnd=None):
    """Create a layout tree structure using a variant of the
    Blocked Recursive Image Composition (BRIC) algorithm
    by C. Brian Atkins."""
    rnd = rnd or random.Random(0)
    tree = _binary_tree_recursive(images, rnd, aspect_ratio >= 1)
    a, b = tree.linear_equations
    solution = np.linalg.solve(a, b)
    widths = {leaf: solution[i] for leaf, i in tree.leafs_index.items()}
    tree.set_weights_from_widths(widths)
    return tree


def crop(image, width, height):
    """Center crop image and resize to width * height."""
    actual_ratio = image.size[0] / image.size[1]
    target_ratio = width / height
    if target_ratio > actual_ratio:  # need to crop height
        crop_pixels = round((1 - actual_ratio / target_ratio) * image.size[1])
        left = 0
        right = image.size[0]
        upper = floor(crop_pixels / 2)
        lower = image.size[1] - ceil(crop_pixels / 2)
    else:  # need to crop width
        crop_pixels = round((1 - target_ratio / actual_ratio) * image.size[0])
        left = floor(crop_pixels / 2)
        right = image.size[0] - ceil(crop_pixels / 2)
        upper = 0
        lower = image.size[1]
    image = image.crop((left, upper, right, lower))
    return image.resize((width, height), Image.LANCZOS)


def render(tree, width, height, frame_width, color):
    """Render layout tree structure to given width and height
    with specified frame; returns a PIL.Image."""
    collg = Image.new("RGB", (width, height), color)
    frame_half_pixels = round(frame_width * max(width, height) / 2)
    frame_pixels = frame_half_pixels * 2
    inner_width = width - frame_pixels
    inner_height = height - frame_pixels
    for (x, y, w, h, img) in tree.positions(
        frame_half_pixels, frame_half_pixels, inner_width, inner_height
    ):
        inner_w = int(w) - frame_pixels
        inner_h = int(h) - frame_pixels
        inner_x = int(x) + frame_half_pixels
        inner_y = int(y) + frame_half_pixels
        resized_img = crop(img, inner_w, inner_h)
        collg.paste(resized_img, (inner_x, inner_y))
    return collg


def collage(images, width, height, frame_width, color, seed, n_tries=1):
    """Create a collage from multiple images."""
    aspect_ratio = width / height
    best_tree = None
    best_score = None
    for i in range(seed, seed + n_tries):
        tree = bric_tree(images, aspect_ratio, random.Random(i))
        best_tree = best_tree or tree
        best_score = tree.score(width, height) if best_score is None else best_score
        score = tree.score(width, height)
        if score > best_score:
            best_tree = tree
            best_score = score
    print("Cut loss is {:.2f}".format(best_tree.normalized_cut_loss(aspect_ratio)))
    print("Balance score is {:.2f}".format(best_tree.balance_score(width, height)))
    print("Overall score is {:.2f}".format(best_tree.score(width, height)))
    return render(best_tree, width, height, frame_width, color)


@click.command(name="collage")
@click.option(
    "-w",
    "--width",
    type=click.INT,
    default=3072,
    show_default=True,
    help="width of the collage",
)
@click.option(
    "-s",
    "--height",
    type=click.INT,
    default=2048,
    show_default=True,
    help="height of the collage",
)
@click.option(
    "-f",
    "--frame-width",
    type=click.FLOAT,
    default=0.01,
    show_default=True,
    help="width of the frame as a fraction of the longer " + "image side",
)
@click.option(
    "-c",
    "--color",
    type=COLOR,
    default="white",
    show_default=True,
    help="color of the frame as a color name, hex value "
    + "or in rgb(...) function form",
)
@click.option(
    "-x",
    "--seed",
    type=int,
    default=123,
    show_default=True,
    help="seed for random number generator",
)
@click.option(
    "-n",
    "--number-tries",
    type=int,
    default=100,
    show_default=True,
    help="number of tries for layout generation",
)
def cli_collage(width, height, frame_width, color, seed, number_tries):
    """Create a collage from multiple images."""
    click.echo("Initializing collage with parameters {}".format(locals()))

    def _collage(image_infos):
        image_infos = list(image_infos)
        images = [img for _, img in image_infos]
        yield image_infos[0][0], collage(
            images, width, height, frame_width, color, seed, number_tries
        )

    return _collage
