'''Fix colors of images by stretching their channel histograms to full
range.'''

import click
from PIL import Image
import numpy as np

from ..param import COLOR


DEFAULT_LEVEL = 0.01


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


def quantiles(img, level=DEFAULT_LEVEL):
    '''Compute high and low quantiles to the given level'''
    r_low, r_high, g_low, g_high, b_low, b_high = \
        list(_quantiles_iter(img, level))
    return (r_low, r_high), (g_low, g_high), (b_low, b_high)


def colorfix_quantiles(img, level=DEFAULT_LEVEL):
    '''Fix colors by stretching channel histograms between given quantiles
       to full range.'''
    channel_quantiles = quantiles(img, level)
    return stretch_histogram(img, channel_quantiles)


def colorfix_fixed_cutoff(img, lower_cutoff, upper_cutoff):
    '''Fix colors by stretching channel histograms between given
       cutoff colors to full range.'''
    cutoffs = list(zip(lower_cutoff, upper_cutoff))
    return stretch_histogram(img, cutoffs)


def _inner_cutoffs(first_cutoffs, second_cutoffs):
    for first, second in zip(first_cutoffs, second_cutoffs):
        yield max(first[0], second[0]), min(first[1], second[1])


def colorfix_quantiles_fixed_cutoff(img, level, lower_cutoff, upper_cutoff):
    '''Fix colors by stretching channel histogram between inner values
       of given quantiles and cutoff colors to full range.'''
    channel_quantiles = quantiles(img, level)
    cutoffs = list(zip(lower_cutoff, upper_cutoff))
    combined = list(_inner_cutoffs(channel_quantiles, cutoffs))
    return stretch_histogram(img, combined)


def stretch_histogram(img, cutoffs):
    '''Stretch channel histograms between given cutoffs to full range.'''
    # convert PIL image to numpy array for processing
    arr = np.array(img).astype(np.int16)
    # type int16 is required to prevent stretched colors from overflowing
    # arr.shape = (height, width, channel)
    # iterate over all three color channels (red, green, blue)
    for idx_channel in range(3):
        low, high = cutoffs[idx_channel]
        assert low >= 0, ('low value for channel {} is {}, but must be 0 '
                          'or larger').format(idx_channel, low)
        assert high <= 255, ('high value for channel {} is {}, but must be 255'
                             ' or less').format(idx_channel, high)
        if low == 0 and high == 255:
            continue  # no stretching required, save some cpu cycles
        channel = arr[:, :, idx_channel]
        # stretch colors betweem low and high to full range
        stretched = (channel - low) / (high - low) * 256
        stretched = stretched.astype(np.int16)
        # cut off anything that has been scaled under or over full range
        channel[:, :] = np.maximum(np.minimum(stretched, 255), 0)
    # convert back to uint8 (lossless after range cutoff)
    # ... and to PIL image
    return Image.fromarray(arr.astype(np.uint8))


QUANTILES = 'quantiles'
FIXED_CUTOFF = 'fixed-cutoff'
QUANTILES_FIXED_CUTOFF = 'quantiles-fixed-cutoff'


@click.command(name='colorfix')
@click.option('-m', '--method',
              type=click.Choice([QUANTILES, FIXED_CUTOFF,
                                 QUANTILES_FIXED_CUTOFF],
                                case_sensitive=False),
              default='quantiles-fixed-cutoff',
              show_default=True,
              help='algorithm method to use; quantiles stretches all channel '
                   'histograms between the quantiles specified by --alpha; '
                   'fixed-cutoff stretches channels between the cutoffs '
                   'specified by --lower-cutoff and --upper-cutoff; '
                   'quantiles-fixed-cutoff combines the two methods and '
                   'applies the "stronger" of both cutoffs (i.e. the higher '
                   'value of lower cutoffs and lower value of upper cutoffs)')
@click.option('-a', '--alpha', type=click.FLOAT, default=DEFAULT_LEVEL,
              show_default=True,
              help='quantile (low and high) to be clipped to minimum '
                   'and maximum color; relevant for --method=quantiles '
                   'and --method=quantiles-fixed-cutoff')
@click.option('-l', '--lower-cutoff', type=COLOR, default='rgb(127,0,0)',
              show_default=True,
              help='lower cutoff as a color name, hex value '
                   'or in rgb(...) function form; '
                   'relevant for --method=fixed-cutoff '
                   'and --method=quantiles-fixed-cutoff')
@click.option('-u', '--upper-cutoff', type=COLOR, default='white',
              show_default=True,
              help='lower cutoff as a color name, hex value '
                   'or in rgb(...) function form; '
                   'relevant for --method=fixed-cutoff '
                   'and --method=quantiles-fixed-cutoff')
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
            elif method == QUANTILES_FIXED_CUTOFF:
                yield info, colorfix_quantiles_fixed_cutoff(image,
                                                            alpha,
                                                            lower_cutoff,
                                                            upper_cutoff)
            else:
                raise NotImplementedError('{} not implemented'.format(method))

    return _colorfix
