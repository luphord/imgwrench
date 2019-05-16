# -*- coding: utf-8 -*-

'''Command Line Interface for Image Wrench.'''

import os
from pathlib import Path

import click
from PIL import Image

from .info import ImageInfo
from .commands.blackwhite import cli_blackwhite
from .commands.colorfix import cli_colorfix
from .commands.crop import cli_crop
from .commands.frame import cli_frame
from .commands.framecrop import cli_framecrop
from .commands.resize import cli_resize
from .commands.save import cli_save
from .commands.stack import cli_stack


def _load_image(fname, preserve_exif):
    '''Load an image from file system and rotate according to exif'''
    img = Image.open(fname)
    # do not rotate image if exif is preserved
    # (otherwise it would be rotated twice)
    if not preserve_exif and hasattr(img, '_getexif'):
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
              show_default=True,
              help='prefix for all output filenames before numbering')
@click.option('-d', '--digits', type=click.INT, default=4,
              show_default=True,
              help='number of digits for file numbering')
@click.option('-c', '--increment', type=click.INT, default=1,
              show_default=True,
              help='increment for file numbering')
@click.option('-k', '--keep-names', is_flag=True, default=False,
              show_default=True,
              help='keep original file names instead of numbering')
@click.option('-f', '--force-overwrite', is_flag=True, default=False,
              show_default=True,
              help='force overwriting output image file if it exists')
@click.option('-o', '--outdir',
              type=click.Path(exists=False, file_okay=False, dir_okay=True,
                              writable=True, resolve_path=True),
              show_default=True,
              default='.', help='output directory')
@click.option('-q', '--quality', type=click.INT, default=88,
              show_default=True,
              help='quality of the output images, integer 0 - 100')
@click.option('-e', '--preserve-exif', is_flag=True, default=False,
              show_default=True,
              help='preserve image exif headers if available')
def cli_imgwrench(image_list, prefix, digits, increment, keep_names,
                  force_overwrite, outdir, quality, preserve_exif):
    '''The main command line interface function of imgwrench'''
    param = dict(**locals())
    del param['image_list']
    click.echo('Preparing imgwrench pipeline with parameters {}'.format(param))


@cli_imgwrench.resultcallback()
def pipeline(image_processors, image_list, prefix, increment, digits,
             keep_names, force_overwrite, outdir, quality, preserve_exif):

    def _load_images():
        with image_list:
            for i, line in enumerate(image_list):
                path = Path(line.strip()).resolve()
                img = _load_image(path, preserve_exif)
                info = ImageInfo(path, i, img.info.get('exif'))
                click.echo('<- Processing {}...'.format(info))
                yield info, img

    images = _load_images()
    # connecting pipeline image processors
    for image_processor in image_processors:
        images = image_processor(images)
    os.makedirs(outdir, exist_ok=True)
    click.echo('--- Executing pipeline ---')
    # executing pipeline
    fmt = '{}{:0' + str(digits) + 'd}.jpg'
    for i, (info, processed_image) in enumerate(images):
        newfname = info.fname \
                    if keep_names \
                    else fmt.format(prefix, i * increment)
        outpath = os.path.join(outdir, newfname)
        if not force_overwrite and os.path.exists(outpath):
            raise Exception(('{} already exists; use --force-overwrite ' +
                             'to overwrite').format(outpath))
        args = dict(quality=quality)
        if preserve_exif and info.exif:
            args['exif'] = info.exif
        processed_image.save(outpath, **args)
        click.echo('-> Saved {}'.format(outpath))
    click.echo('--- Pipeline execution completed ---')


cli_imgwrench.add_command(cli_blackwhite)
cli_imgwrench.add_command(cli_colorfix)
cli_imgwrench.add_command(cli_crop)
cli_imgwrench.add_command(cli_frame)
cli_imgwrench.add_command(cli_framecrop)
cli_imgwrench.add_command(cli_resize)
cli_imgwrench.add_command(cli_save)
cli_imgwrench.add_command(cli_stack)
