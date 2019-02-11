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




A command line tool for my image processing needs. Multiple subcommands can
be executed sequentially to form a processing pipeline.


* Free software: MIT license
* Documentation: https://imgwrench.readthedocs.io.

Usage
-----

.. code-block:: console

        Usage: imgwrench [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

        The main command line interface function of imgwrench

        Options:
        -i, --image-list FILENAME  File containing paths to images for processing,
                                defaults to stdin
        -p, --prefix TEXT          prefix for all output filenames before numbering
        -d, --digits INTEGER       number of digits for file numbering (default 4)
        -c, --increment INTEGER    increment for file numbering (default 1)
        -k, --keep-names           keep original file names instead of numbering
        -f, --force-overwrite      force overwriting output image file if it exists
        -o, --outdir DIRECTORY     output directory
        -q, --quality INTEGER      quality of the output images, integer 0 - 100
        --help                     Show this message and exit.

        Commands:
        colorfix  Fix colors by stretching channel histograms to full range.
        resize    Resize images to a maximum side length preserving aspect ratio.
        save      No-op to enable saving of images without any processing.
        stack     Stack images vertically, empty space in the middle.

Features
--------

* Subcommands can be executed sequentially to form a pipeline
* Command *colorfix* for fixing the colors of aged photographs
* Command *resize* for resizing images
* Command *stack* for vertically stacking images
* Command *save* for no processing, but saving images with the given parameters

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
