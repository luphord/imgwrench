'''Fix colors of images by stretching their channel histograms to full
range.'''

import click
from PIL import Image
import numpy as np

from ..param import COLOR


def _quantiles_iter(img, level):
    assert img.mode == 'RGB'
    assert level > 0 and level < 1
    h = img.histogram()
    for i in range(3):
        channel_h = h[i*256:(i+1)*256]
        n_pixels = sum(channel_h)
        low = int(level * n_pixels)
        high = int((1-level) * n_pixels) + 1
        s = 0
        searching_low = True
        for i, p in enumerate(channel_h):
            s += p
            if searching_low:
                if s >= low:
                    yield i
                    searching_low = False
                    continue
            else:
                if s >= high:
                    yield i
                    break


def quantiles(img, level=0.01):
    '''Compute high and low quantiles to the given level'''
    r_low, r_high, g_low, g_high, b_low, b_high = \
        list(_quantiles_iter(img, level))
    return (r_low, r_high), (g_low, g_high), (b_low, b_high)


def colorfix_quantiles(img, level=0.01):
    '''Fix colors by stretching channel histograms between given quantiles
       to full range.'''
    channel_quantiles = quantiles(img, level)
    arr = np.array(img).astype(np.int16)
    # arr.shape = (height, width, channel)
    for channel in range(3):
        q = channel_quantiles[channel]
        c = arr[:, :, channel]
        stretched = (c - q[0]) / (q[1] - q[0]) * 256
        c[:, :] = np.maximum(np.minimum(stretched.astype(np.int16), 255), 0)
    return Image.fromarray(arr.astype(np.uint8))


def colorfix_fixed_cutoff(img, lower_cutoff, upper_cutoff):
    '''Fix colors by stretching channel histograms between given
       cutoff colors to full range.'''
    raise NotImplementedError('colorfix_fixed_cutoff not implemented yet')


QUANTILES = 'quantiles'
FIXED_CUTOFF = 'fixed-cutoff'


@click.command(name='colorfix')
@click.option('-m', '--method',
              type=click.Choice([QUANTILES, FIXED_CUTOFF],
                                case_sensitive=False),
              default=QUANTILES,
              show_default=True,
              help='algorithm method to use; quantiles stretches all channel'
                   'histograms between the quantile specified by --alpha; '
                   'fixed-cutoff stretches channels between the cutoffs'
                   'specified by --lower-cutoff and --upper-cutoff')
@click.option('-a', '--alpha', type=click.FLOAT, default=0.01,
              show_default=True,
              help='quantile (low and high) to be clipped to minimum '
                   'and maximum color; only relevant for --method=quantiles')
@click.option('-l', '--lower-cutoff', type=COLOR, default='black',
              show_default=True,
              help='lower cutoff as a color name, hex value '
                   'or in rgb(...) function form; '
                   'only relevant for --method=fixed-cutoff')
@click.option('-u', '--upper-cutoff', type=COLOR, default='white',
              show_default=True,
              help='lower cutoff as a color name, hex value '
                   'or in rgb(...) function form; '
                   'only relevant for --method=fixed-cutoff')
def cli_colorfix(method, alpha, lower_cutoff, upper_cutoff):
    '''Fix colors by stretching channel histograms to full range.'''
    click.echo('Initializing colorfix with parameters {}'.format(locals()))

    def _colorfix(images):
        for info, image in images:
            if method == QUANTILES:
                yield info, colorfix_quantiles(image, alpha)
            elif method == FIXED_CUTOFF:
                yield info, colorfix_fixed_cutoff(image,
                                                  lower_cutoff,
                                                  upper_cutoff)
            else:
                raise NotImplementedError('{} not implemented'.format(method))

    return _colorfix
