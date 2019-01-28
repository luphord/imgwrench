# -*- coding: utf-8 -*-

"""Top-level package for Image Wrench."""

__author__ = """luphord"""
__email__ = 'luphord@protonmail.com'
__version__ = '0.1.0'

import click
from PIL import Image

from .colorfix import colorfix


def _load_image(fname):
    '''Load an image from file system and rotate according to exif'''
    img = Image.open(fname)
    if hasattr(img, '_getexif'):
        orientation = 0x0112
        exif = img._getexif()
        if exif is not None:
            orientation = exif[orientation]
            rotations = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotations:
                img = img.transpose(rotations[orientation])
    return img


@click.group(name='imgwrench', chain=True)
@click.option('-i', '--image-list', type=click.File(mode='r'), default='-',
              help='File containing paths to images for processing, ' +
                    'defaults to stdin')
@click.option('-p', '--prefix', type=click.STRING, default='img_',
              help='prefix for all output filenames before numbering')
@click.option('-k', '--keep-names', is_flag=True, default=False,
              help='keep original file names instead of numbering')
@click.option('-o', '--outdir',
              type=click.Path(exists=False, file_okay=False, dir_okay=True,
                              writable=True, resolve_path=True),
              default='.', help='output directory')
@click.option('-q', '--quality', type=click.INT, default=88,
              help='quality of the output images, integer 0 - 100')
def imgwrench(image_list, prefix, keep_names, outdir, quality):
    '''The main command line interface function of imgwrench'''
    param = dict(**locals())
    del param['image_list']
    click.echo('Preparing imgwrench pipeline with parameters {}'.format(param))


@imgwrench.resultcallback()
def pipeline(image_processors, image_list, prefix,
             keep_names, outdir, quality):

    def _load_images():
        with image_list:
            for line in image_list:
                fname = line.strip()
                click.echo('Processing {}...'.format(fname))
                yield _load_image(fname)

    images = _load_images()
    # connecting pipeline image processors
    for image_processor in image_processors:
        images = image_processor(images)
    click.echo('--- Executing pipeline ---')
    # exectung pipeline
    for processed_image in images:
        click.echo('saved {}'.format(processed_image))
    click.echo('Pipeline execution completed')


imgwrench.add_command(colorfix)
