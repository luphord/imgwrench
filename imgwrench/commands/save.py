'''No-op to enable saving of images using imgwrench without processing.'''

import click


@click.command(name='save')
def cli_save():
    '''No-op to enable saving of images without any processing.'''
    click.echo('Initializing save (no-op) without parameters')

    def _save(images):
        for info, image in images:
            yield info, image

    return _save
