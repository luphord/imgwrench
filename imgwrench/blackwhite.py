'''Convert color images to black and white.'''

import click


def blackwhite(image):
    '''Convert color images to black and white.'''
    return image.convert('L')


@click.command(name='blackwhite')
def cli_blackwhite():
    '''Convert color images to black and white.'''
    click.echo('Initializing blackwhite with parameters {}'.format(locals()))

    def _blackwhite(images):
        for orgfname, image in images:
            yield orgfname, blackwhite(image)

    return _blackwhite
