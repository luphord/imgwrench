'''Fix colors of images by stretching their channel histograms to full
   range.'''

import click


@click.command()
@click.option('-a', '--alpha', type=click.FLOAT, default=0.01,
              help='quantile (low and high) to be clipped to minimum ' +
                    'and maximum color, defaults to 0.01')
@click.pass_context
def colorfix(ctx, alpha):
    '''Fix colors by stretching channel histograms to full range.'''
    click.echo('Starting colorfix')
    click.echo(locals())
    click.echo(ctx.obj['images'])
    click.echo('colorfix completed')
