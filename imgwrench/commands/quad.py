"""Collects four images to a quad."""

from itertools import islice

import click
from PIL import Image

from ..param import COLOR
from .crop import crop
from .resize import resize


def quad(quad_images, width, height, frame_width, double_inner_frame, color):
    assert quad_images
    assert len(quad_images) <= 4
    is_landscape = width >= height
    width, height = max(width, height), min(width, height)
    result = Image.new(mode="RGB", size=(width, height), color=color)
    frame_pixels = frame_width * width
    dbl = 1 if double_inner_frame else 0
    total_frame_pixels = (3 + dbl) * frame_pixels
    ratio = (width - total_frame_pixels) / (height - total_frame_pixels)
    single_width = (width - total_frame_pixels) / 2
    single_height = (height - total_frame_pixels) / 2
    for i, img in enumerate(quad_images):
        if img.size[0] < img.size[1]:
            img = img.transpose(Image.ROTATE_90)
        img = crop(img, ratio)
        img = resize(img, single_width)
        x = int(i % 2 * (single_width + (1 + dbl) * frame_pixels) + frame_pixels)
        y = int(int(i / 2) * (single_height + (1 + dbl) * frame_pixels) + frame_pixels)
        result.paste(img, (x, y))
    if not is_landscape:
        result = result.transpose(Image.ROTATE_270)
    return result


@click.command(name="quad")
@click.option(
    "-w",
    "--width",
    type=click.INT,
    default=3072,
    show_default=True,
    help="width of the quad image",
)
@click.option(
    "-s",
    "--height",
    type=click.INT,
    default=2048,
    show_default=True,
    help="height of the quad image",
)
@click.option(
    "-f",
    "--frame-width",
    type=click.FLOAT,
    default=0.0,
    show_default=True,
    help="width of the frame as a fraction of the longer "
    + " side of the output image",
)
@click.option(
    "-d",
    "--double-inner-frame",
    is_flag=True,
    default=False,
    show_default=False,
    help="double inner frame width for even cuts",
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
def cli_quad(width, height, frame_width, double_inner_frame, color):
    """Collects four images to a quad."""
    click.echo("Initializing quad with parameters {}".format(locals()))

    def _quad(images):
        images = iter(images)
        while True:
            quad_images = list(islice(images, 4))
            if quad_images:
                info = quad_images[0][0]
                yield info, quad(
                    [img for _, img in quad_images],
                    width,
                    height,
                    frame_width,
                    double_inner_frame,
                    color,
                )
            else:
                break

    return _quad
