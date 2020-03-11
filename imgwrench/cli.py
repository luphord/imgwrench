# -*- coding: utf-8 -*-

'''Command Line Interface for Image Wrench.'''

import os
from pathlib import Path

import click
from PIL import Image

from .info import ImageInfo
from .commands.blackwhite import cli_blackwhite
from .commands.collage import cli_collage
from .commands.colorfix import cli_colorfix
from .commands.crop import cli_crop
from .commands.dither import cli_dither
from .commands.filmstrip import cli_filmstrip
from .commands.frame import cli_frame
from .commands.framecrop import cli_framecrop
from .commands.resize import cli_resize
from .commands.save import cli_save
from .commands.stack import cli_stack


def _xmp_from_image(img, xmp_marker=b'http://ns.adobe.com/xap/1.0/'):
    if hasattr(img, 'applist'):
        for key, val in img.applist:
            if key == 'APP1' and val.startswith(xmp_marker):
                return val


def _write_xmp_to_image(path, xmp):
    with open(path, 'rb') as f:
        raw_data = f.read()
    app1_start = raw_data.rfind(b'\xFF\xE1')
    if app1_start > 0:
        app1_raw_len = raw_data[app1_start+2:app1_start+4]
        app1_len = int.from_bytes(app1_raw_len, 'big')
        app1_end = app1_start + 2 + app1_len
        with open(path, 'wb') as f:
            f.write(raw_data[:app1_end])
            f.write(b'\xFF\xE1')
            f.write((len(xmp) + 2).to_bytes(2, 'big'))
            f.write(xmp)
            f.write(raw_data[app1_end:])


def _load_image(fname, i, preserve_exif):
    '''Load an image from file system and rotate according to exif'''
    img = Image.open(fname)
    info = ImageInfo(fname, i, img.info.get('exif'), _xmp_from_image(img))
    # do not rotate image if exif is preserved
    # (otherwise it would be rotated twice)
    if not preserve_exif and hasattr(img, '_getexif'):
        orientation = 0x0112
        exif = img._getexif()
        if exif is not None and orientation in exif:
            orientation = exif[orientation]
            rotations = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotations:
                img = img.transpose(rotations[orientation])
    if img.mode != 'RGB':
        return img.convert('RGB'), info
    return img, info


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
              help='preserve image exif and xmp metadata if available')
@click.option('-j', '--jpg/--png',
              default=True, show_default=True,
              help='save output images in JPEG format (otherwise PNG)')
def cli_imgwrench(image_list, prefix, digits, increment, keep_names,
                  force_overwrite, outdir, quality, preserve_exif, jpg):
    '''A highly opinionated image processor for the commandline.
       Multiple subcommands can be executed sequentially to form
       a processing pipeline.'''
    param = dict(**locals())
    del param['image_list']
    click.echo('Preparing imgwrench pipeline with parameters {}'.format(param))


@cli_imgwrench.resultcallback()
def pipeline(image_processors, image_list, prefix, increment, digits,
             keep_names, force_overwrite, outdir, quality, preserve_exif, jpg):

    def _load_images():
        with image_list:
            for i, line in enumerate(image_list):
                path = Path(line.strip()).resolve()
                img, info = _load_image(path, i, preserve_exif)
                click.echo('<- Processing {}...'.format(info))
                yield info, img

    images = _load_images()
    # connecting pipeline image processors
    for image_processor in image_processors:
        images = image_processor(images)
    os.makedirs(outdir, exist_ok=True)
    click.echo('--- Executing pipeline ---')
    # executing pipeline
    ext = 'jpg' if jpg else 'png'
    fmt = '{}{:0' + str(digits) + 'd}.' + ext
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
        if preserve_exif and jpg and info.xmp:
            _write_xmp_to_image(outpath, info.xmp)
        click.echo('-> Saved {}'.format(outpath))
    click.echo('--- Pipeline execution completed ---')


cli_imgwrench.add_command(cli_blackwhite)
cli_imgwrench.add_command(cli_collage)
cli_imgwrench.add_command(cli_colorfix)
cli_imgwrench.add_command(cli_crop)
cli_imgwrench.add_command(cli_filmstrip)
cli_imgwrench.add_command(cli_frame)
cli_imgwrench.add_command(cli_framecrop)
cli_imgwrench.add_command(cli_resize)
cli_imgwrench.add_command(cli_save)
cli_imgwrench.add_command(cli_stack)
cli_imgwrench.add_command(cli_dither)
