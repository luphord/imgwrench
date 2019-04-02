'''Fix colors of images by stretching their channel histograms to full
range.'''

import click


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
    pixels = img.load()
    # for every pixel
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            r_new = max(min(int((r - qr[0]) / (qr[1] - qr[0]) * 256), 255), 0)
            g_new = max(min(int((g - qg[0]) / (qg[1] - qg[0]) * 256), 255), 0)
            b_new = max(min(int((b - qb[0]) / (qb[1] - qb[0]) * 256), 255), 0)
            pixels[i, j] = (r_new, g_new, b_new)
    return img


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
