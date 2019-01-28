'''Fix colors of images by stretching their channel histograms to full
range.'''

import click


@click.command(name='colorfix')
@click.option('-a', '--alpha', type=click.FLOAT, default=0.01,
              help='quantile (low and high) to be clipped to minimum ' +
                    'and maximum color, defaults to 0.01')
def cli_colorfix(alpha):
    '''Fix colors by stretching channel histograms to full range.'''
    click.echo('Initializing colorfix with parameters {}'.format(locals()))

    def _colorfix(images):
        for image in images:
            yield image  # todo apply colorfix

    return _colorfix
