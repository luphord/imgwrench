# -*- coding: utf-8 -*-

"""Top-level package for Image Wrench."""

__author__ = """luphord"""
__email__ = 'luphord@protonmail.com'
__version__ = '0.4.0'

import os
import click
from PIL import Image

from .colorfix import cli_colorfix
from .resize import cli_resize
from .crop import cli_crop
from .stack import cli_stack
from .save import cli_save


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
    if img.mode != 'RGB':
        return img.convert('RGB')
    return img


@click.group(name='imgwrench', chain=True)
@click.option('-i', '--image-list', type=click.File(mode='r'), default='-',
              help='File containing paths to images for processing, ' +
                    'defaults to stdin')
@click.option('-p', '--prefix', type=click.STRING, default='img_',
              help='prefix for all output filenames before numbering')
@click.option('-d', '--digits', type=click.INT, default=4,
              help='number of digits for file numbering (default 4)')
@click.option('-c', '--increment', type=click.INT, default=1,
              help='increment for file numbering (default 1)')
@click.option('-k', '--keep-names', is_flag=True, default=False,
              help='keep original file names instead of numbering')
@click.option('-f', '--force-overwrite', is_flag=True, default=False,
              help='force overwriting output image file if it exists')
@click.option('-o', '--outdir',
              type=click.Path(exists=False, file_okay=False, dir_okay=True,
                              writable=True, resolve_path=True),
              default='.', help='output directory')
@click.option('-q', '--quality', type=click.INT, default=88,
              help='quality of the output images, integer 0 - 100')
def cli_imgwrench(image_list, prefix, digits, increment, keep_names,
                  force_overwrite, outdir, quality):
    '''The main command line interface function of imgwrench'''
    param = dict(**locals())
    del param['image_list']
    click.echo('Preparing imgwrench pipeline with parameters {}'.format(param))


@cli_imgwrench.resultcallback()
def pipeline(image_processors, image_list, prefix, increment, digits,
             keep_names, force_overwrite, outdir, quality):

    def _load_images():
        with image_list:
            for line in image_list:
                fname = line.strip()
                click.echo('<- Processing {}...'.format(fname))
                yield os.path.basename(fname), _load_image(fname)

    images = _load_images()
    # connecting pipeline image processors
    for image_processor in image_processors:
        images = image_processor(images)
    os.makedirs(outdir, exist_ok=True)
    click.echo('--- Executing pipeline ---')
    # executing pipeline
    fmt = '{}{:0' + str(digits) + 'd}.jpg'
    for i, (orgfname, processed_image) in enumerate(images):
        newfname = orgfname if keep_names else fmt.format(prefix, i*increment)
        outpath = os.path.join(outdir, newfname)
        if not force_overwrite and os.path.exists(outpath):
            raise Exception(('{} already exists; use --force-overwrite ' +
                             'to overwrite').format(outpath))
        processed_image.save(outpath, quality=quality)
        click.echo('-> Saved {}'.format(outpath))
    click.echo('--- Pipeline execution completed ---')


cli_imgwrench.add_command(cli_colorfix)
cli_imgwrench.add_command(cli_resize)
cli_imgwrench.add_command(cli_crop)
cli_imgwrench.add_command(cli_stack)
cli_imgwrench.add_command(cli_save)
