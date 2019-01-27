'''Fix colors of images by stretching their channel histograms to full
range.'''

import click


@click.command()
@click.option('-a', '--alpha', type=click.FLOAT, default=0.01,
              help='quantile (low and high) to be clipped to minimum ' +
                    'and maximum color, defaults to 0.01')
def colorfix(alpha):
    '''Fix colors by stretching channel histograms to full range.'''
    click.echo('Starting colorfix')
    click.echo(locals())
    click.echo('colorfix completed')

    def _colorfix(images):
        for image in images:
            yield 'colorfixed {}'.format(image)

    return _colorfix
