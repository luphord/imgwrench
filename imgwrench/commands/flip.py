"""Flip/mirror images left-right."""

import click

from PIL import Image


def flip(image):
    """Flip/mirror images left-right."""
    return image.transpose(Image.FLIP_LEFT_RIGHT)


@click.command(name="flip")
def cli_flip():
    """Flip/mirror images left-right."""
    click.echo("Initializing flip with parameters {}".format(locals()))

    def _flip(images):
        for info, image in images:
            yield info, flip(image)

    return _flip
