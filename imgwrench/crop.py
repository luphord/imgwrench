'''Crop images to the given aspect ratio.'''

import click


def crop(image, aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    a, b = aspect_ratio.split(':')
    a, b = float(a), float(b)
    if image.size[0] >= image.size[1]:
        ratio = max(a, b) / min(a, b)
    else:
        ratio = min(a, b) / max(a, b)
    print(ratio)
    return image


@click.command(name='crop')
@click.option('-a', '--aspect-ratio', type=click.STRING, default='3:2',
              help='aspect ratio to crop to, defaults to "3:2"')
def cli_crop(aspect_ratio):
    '''Crop images to the given aspect ratio.'''
    click.echo('Initializing crop with parameters {}'.format(locals()))

    def _crop(images):
        for orgfname, image in images:
            yield orgfname, crop(image, aspect_ratio)

    return _crop
