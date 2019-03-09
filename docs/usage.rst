=====
Usage
=====



blackwhite
==========

The `blackwhite` subcommand converts color images to black and white.

Assuming image `rainbow.jpg` in the current directory, `blackwhite` can
be applied to output to `img_0000.jpg` as follows:

.. code-block:: console

    ls rainbow.jpg | imgwrench blackwhite

.. image:: _static/blackwhite.jpg

At the moment, `blackwhite` supports no further parameters. Conversion
is delegated to the PIL `convert('L')` method call.

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

frame
=====

The `frame` subcommand puts a monocolor frame around the image. The frame is
added to the image size.

Assuming image `saarschleife.jpg` in the current directory, `frame` can
be applied with a frame width equal to 3% of the original image width (which
is in landscape format, i.e. width > height) and a light grey color
to output to `img_0000.jpg` as follows:

.. code-block:: console

    ls saarschleife.jpg | imgwrench frame -w 0.03 -c '#ddd'

.. image:: _static/frame.jpg

`frame` supports the parameter -w/--frame-width which specifies the frame width
as fraction of the longer image side, e.g. 0.1 for a frame width that is equal
to 10% of the longer image side. Also -c/--color is supported which accepts
the frame color as either a name (e.g. 'white', 'green'), a hex value (e.g.
'#ab1fde') or an rgb function value (e.g. 'rgb(120,23,217)').

.. code-block:: console
    Usage: imgwrench frame [OPTIONS]

    Put a monocolor frame around images.

    Options:
    -w, --frame-width FLOAT  width of the frame as a fraction of the longer
                            image side (default: 0.025)
    -c, --color TEXT         color of the frame as a color name, hex value or in
                            rgb(...) function form (default: white)
    --help                   Show this message and exit.