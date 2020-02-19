'''Fix colors of images by stretching their channel histograms to full
range.'''

import click
from PIL import Image
import numpy as np


nmax = np.maximum
nmin = np.minimum


def aint(arr):
    return arr.astype(int)


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


def colorfix(img, level=0.01):
    '''Fix colors by stretching channels histograms to full range.'''
    qr, qg, qb = quantiles(img, level)
    arr = np.array(img).astype(np.int16)
    # arr.shape = (height, width, channel)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    r[:, :] = nmax(nmin(aint((r - qr[0]) / (qr[1] - qr[0]) * 256), 255), 0)
    g[:, :] = nmax(nmin(aint((g - qg[0]) / (qg[1] - qg[0]) * 256), 255), 0)
    b[:, :] = nmax(nmin(aint((b - qb[0]) / (qb[1] - qb[0]) * 256), 255), 0)
    return Image.fromarray(arr.astype(np.uint8))


@click.command(name='colorfix')
@click.option('-a', '--alpha', type=click.FLOAT, default=0.01,
              show_default=True,
              help='quantile (low and high) to be clipped to minimum ' +
                    'and maximum color')
def cli_colorfix(alpha):
    '''Fix colors by stretching channel histograms to full range.'''
    click.echo('Initializing colorfix with parameters {}'.format(locals()))

    def _colorfix(images):
        for info, image in images:
            yield info, colorfix(image, alpha)

    return _colorfix
