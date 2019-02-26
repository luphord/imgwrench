=====
Usage
=====


colorfix
========

The `colorfix` subcommand repairs aged images with a color shift (usually towards
red) by shifting the channel histograms back to the full range.

Assuming image `old.jpg` in the current directory, `colorfix` can be applied to
repair its colors and output as `img_0000.jpg` as follows:

.. code-block:: console

    ls old.jpg | imgwrench colorfix

.. image:: _static/colorfix.jpg

`colorfix` supports the float parameter -a/--alpha representing the quantile
within each color channel that is clipped to the minimum and maximum value.
It defaults to `0.01`. Increasing `alpha` will stretch the histogram further
and will intensify the contrast of the resulting image.

.. code-block:: console

    Usage: imgwrench colorfix [OPTIONS]

    Fix colors by stretching channel histograms to full range.

    Options:
    -a, --alpha FLOAT  quantile (low and high) to be clipped to minimum and
                        maximum color, defaults to 0.01
    --help             Show this message and exit.


crop
====

The `crop` subcommand crops images to a specified aspect ratio.

Assuming image `rainbow.jpg` in the current directory, `crop` can be applied
with aspect ratio 2:1 and output to `img_0000.jpg` as follows:

.. code-block:: console

    ls rainbow.jpg | imgwrench crop -a 2:1

.. image:: _static/crop.jpg

`crop` supports the parameter -a/--aspect-ratio which has to be an aspect ratio
specified as two numbers separated by a colon, e.g. "2:1", "3:4", "117:123".

.. code-block:: console

    Usage: imgwrench crop [OPTIONS]

    Crop images to the given aspect ratio.

    Options:
    -a, --aspect-ratio TEXT  aspect ratio to crop to, defaults to "3:2"
    --help                   Show this message and exit.