============
Image Wrench
============


.. image:: https://img.shields.io/pypi/v/imgwrench.svg
        :target: https://pypi.python.org/pypi/imgwrench

.. image:: https://img.shields.io/travis/luphord/imgwrench.svg
        :target: https://travis-ci.org/luphord/imgwrench

.. image:: https://readthedocs.org/projects/imgwrench/badge/?version=latest
        :target: https://imgwrench.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A highly opinionated image processor for the commandline. Multiple subcommands can
be executed sequentially to form a processing pipeline.


* Free software: MIT license
* Documentation: https://imgwrench.readthedocs.io.

Usage
-----

.. code-block:: console

        Usage: imgwrench [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

        A highly opinionated image processor for the commandline. Multiple
        subcommands can be executed sequentially to form a processing pipeline.

        Options:
        -i, --image-list FILENAME  File containing paths to images for processing,
                                defaults to stdin
        -p, --prefix TEXT          prefix for all output filenames before numbering
                                [default: img_]
        -d, --digits INTEGER       number of digits for file numbering  [default: 4]
        -c, --increment INTEGER    increment for file numbering  [default: 1]
        -k, --keep-names           keep original file names instead of numbering
                                [default: False]
        -f, --force-overwrite      force overwriting output image file if it exists
                                [default: False]
        -o, --outdir DIRECTORY     output directory  [default: .]
        -q, --quality INTEGER      quality of the output images, integer 0 - 100
                                [default: 88]
        -e, --preserve-exif        preserve image exif headers if available
                                [default: False]
        -j, --jpg / --png          save output images in JPEG format (otherwise PNG)
                                [default: True]
        --help                     Show this message and exit.

        Commands:
        blackwhite  Convert color images to black and white.
        colorfix    Fix colors by stretching channel histograms to full range.
        crop        Crop images to the given aspect ratio.
        dither      Apply black-white dithering to images.
        filmstrip   Stack all images horizontally, creating a filmstrip.
        frame       Put a monocolor frame around images.
        framecrop   Crop and frame an image to a target aspect ratio.
        resize      Resize images to a maximum side length preserving aspect...
        save        No-op to enable saving of images without any processing.
        stack       Stacks pairs of images vertically, empty space in the middle.

Features
--------

* Subcommands can be executed sequentially to form a pipeline
* Command *blackwhite* for converting images to black and white
* Command *colorfix* for fixing the colors of aged photographs
* Command *crop* for cropping images to give aspect ratio
* Command *dither* for converting images to black and white and dithering
* Command *filmstrip* to stack images horizontally forming a filmstrip
* Command *frame* to put a monocolor frame around images
* Command *framecrop* top frame and crop an image to a target aspect ratio
* Command *resize* for resizing images
* Command *save* for no processing, but saving images with the given parameters
* Command *stack* for vertically stacking images

Pipelines
---------

imgwrench subcommands can be combined into pipelines. This saves you from generating intermediate
files cluttering your filesystem and reducing the quality of the final results. For example, if you
would like to convert all images in the current directory to black and white, put a white frame
around them and have them cut to an aspect ratio of 3:2 (for standard format printing), you would
execute the following command:

.. code-block:: console

        ls *.JPG | \
        imgwrench -o out -q 95 -p oldschool_img_ \
                blackwhite \
                framecrop -a 3:2 -w 0.03 -c white

Please refer to the `detailed subcommand documentation`_ for the individual parameters.

.. _`detailed subcommand documentation`: https://imgwrench.readthedocs.io/en/latest/usage.html

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
