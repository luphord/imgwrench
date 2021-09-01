"""Collects images into a grid."""

from itertools import islice

import click
from PIL import Image

from ..param import COLOR
from .crop import crop


def grid(images, rows, columns, width, height, frame_width, double_inner_frame, color):
    assert images
    assert len(images) <= rows * columns
    is_landscape = width >= height
    width, height = max(width, height), min(width, height)
    rows, columns = (rows, columns) if is_landscape else (columns, rows)
    result = Image.new(mode="RGB", size=(width, height), color=color)
    frame_pixels = frame_width * width
    dbl = 2 if double_inner_frame else 1
    total_frame_pixels_width = ((columns - 1) * dbl + 2) * frame_pixels
    total_frame_pixels_height = ((rows - 1) * dbl + 2) * frame_pixels
    single_width = (width - total_frame_pixels_width) / columns
    single_height = (height - total_frame_pixels_height) / rows
    ratio = single_width / single_height
    for i, img in enumerate(images):
        if (ratio >= 1 and img.size[0] < img.size[1]) or (
            ratio < 1 and img.size[0] >= img.size[1]
        ):
            img = img.transpose(Image.ROTATE_90)
        img = crop(img, ratio)
        img = img.resize((int(single_width), int(single_height)))
        x = int(i // rows * (single_width + dbl * frame_pixels) + frame_pixels)
        y = int(i % rows * (single_height + dbl * frame_pixels) + frame_pixels)
        result.paste(img, (x, y))
    if not is_landscape:
        result = result.transpose(Image.ROTATE_270)
    return result


@click.command(name="grid")
@click.option(
    "-r",
    "--rows",
    type=click.INT,
    default=4,
    show_default=True,
    help="number of image rows in the grid",
)
@click.option(
    "-n",
    "--columns",
    type=click.INT,
    default=3,
    show_default=True,
    help="number of image columns in the grid",
)
@click.option(
    "-w",
    "--width",
    type=click.INT,
    default=3072,
    show_default=True,
    help="width of the grid image",
)
@click.option(
    "-s",
    "--height",
    type=click.INT,
    default=2048,
    show_default=True,
    help="height of the grid image",
)
@click.option(
    "-f",
    "--frame-width",
    type=click.FLOAT,
    default=0.01,
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
def cli_grid(rows, columns, width, height, frame_width, double_inner_frame, color):
    """Collects images into a grid."""
    click.echo("Initializing grid with parameters {}".format(locals()))

    def _grid(images):
        images = iter(images)
        while True:
            grid_images = list(islice(images, rows * columns))
            if grid_images:
                info = grid_images[0][0]
                yield info, grid(
                    [img for _, img in grid_images],
                    rows,
                    columns,
                    width,
                    height,
                    frame_width,
                    double_inner_frame,
                    color,
                )
            else:
                break

    return _grid
