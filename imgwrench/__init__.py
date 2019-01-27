# -*- coding: utf-8 -*-

"""Top-level package for Image Wrench."""

__author__ = """luphord"""
__email__ = 'luphord@protonmail.com'
__version__ = '0.1.0'

import click

from .colorfix import colorfix


@click.group(name='imgwrench', chain=True, invoke_without_command=True)
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
    click.echo('Starting imgwrench')
    click.echo(locals())
    click.echo('imgwrench completed')


@imgwrench.resultcallback()
def pipeline(image_processors, image_list, prefix,
             keep_names, outdir, quality):
    click.echo('Initializing pipeline')

    def _load_images():
        with image_list:
            for line in image_list:
                click.echo('loading {}...'.format(line.strip()))
                yield 'loaded {}'.format(line)

    images = _load_images()
    click.echo(locals())
    # connecting pipeline image processors
    for image_processor in image_processors:
        images = image_processor(images)
    # exectung pipeline
    for processed_image in images:
        click.echo('saved {}'.format(processed_image))
    click.echo('pipeline completed completed')


imgwrench.add_command(colorfix)
