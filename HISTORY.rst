=======
History
=======

0.16.0 (2021-01-23)
-------------------
* :code:`quad` subcommand supports doubling inner frame using the :code:`-d/--double-inner-frame` flag

0.15.0 (2021-01-22)
-------------------
* :code:`collage` subcommand selects best layout based on score function
* :code:`collage` subcommand supports :code:`-n/--number-tries` parameter to specify number of layout tries

0.14.0 (2021-01-21)
-------------------
* BREAKING CHANGE: replace golden collage approach with BRIC algorithm in :code:`collage` subcommand
* BREAKING CHANGE: drop support for Python 3.5
* format code with :code:`black`

0.13.0 (2020-10-26)
-------------------
* :code:`quad` subcommand to to collect four images into a quad
* improve documentation


0.12.0 (2020-07-24)
-------------------

* :code:`flip` subcommand to flip/mirror images left-right
* Monkey patch :code:`IFDRational.__eq__` method of Pillow in tests to avoid regression with Pillow 7.2.0

0.11.1 (2020-04-05)
-------------------

* :code:`-x/--seed` option for collage to control initialization of random number generator

0.11.0 (2020-03-21)
-------------------

* collage subcommand for creating a framed collage from images
* BREAKING CHANGE: default method for colorfix is now quantiles-fixed-cutoff
* preserve xmp metadata when :code:`-e/--preserve-exif` is used (in addition to exif metadata)

0.10.0 (2020-03-04)
-------------------

* :code:`-m/--method` option to colorfix (default: quantiles)
* add fixed-cutoff as new method to colorfix accepting fixed colors as color cutoff boundaries
* add quantiles-fixed-cutoff as new method to colorfix combining quantiles and fixed-cutoff
* deprecate running colorfix without specifying method (as default will change in next version)

0.9.0 (2020-02-19)
------------------

* add numpy as dependency
* change colorfix algorithm to vectorized numpy code for performance
* support Python 3.8

0.8.1 (2020-01-12)
------------------

* fix crash when orientation is missing in exif headers

0.8.0 (2019-07-10)
------------------

* dither subcommand for dithering
* filmstrip subcommand to stack images horizontally
* images can be saved in PNG format using :code:`--png` CLI flag

0.7.1 (2019-05-16)
------------------

* fix development status

0.7.0 (2019-05-16)
------------------

* option for preserving exif image metadata
* fix error when running with :code:`-k/--keep-names`
* status progress to Alpha

0.6.0 (2019-03-14)
------------------

* framecrop subcommand to crop and frame an image to a target aspect ratio incl. tests and docs
* breaking change: moved command modules to `commands` package
* introduced ImageInfo as a container for additional meta information in the pipeline
* increased test coverage
* more documentation

0.5.2 (2019-03-10)
------------------

* use a custom parameter type for colors

0.5.1 (2019-03-09)
------------------

* changed default frame width to 0.025
* usage doc for frame subcommand
* consistent alphabetic sorting of subcommands
* use a custom parameter type for ratios

0.5.0 (2019-03-07)
------------------

* blackwhite subcommand to convert color images to black and white; incl. doc
* frame subcommand to put a monocolor frame around images; incl. tests

0.4.0 (2019-02-26)
------------------

* convert RGBA mode PNG images to RGB (to enable saving as JPG)
* crop subcommand to crop images to a specified aspect ratio
* documentation for colorfix and crop

0.3.0 (2019-02-17)
------------------

* :code:`-d/--digits` option to specify number of digits in file names
* :code:`-c/--increment` option to define increment for file numbering
* create non-existing output folder instead of complaining

0.2.0 (2019-01-30)
------------------

* no-op save command for only saving images
* raise exception if output image already exists
* :code:`-f/--force-overwrite` flag to enable overwriting output
* tests for cli, pipeline and resize

0.1.1 (2019-01-29)
------------------

* Fix __main__ module

0.1.0 (2019-01-29)
------------------

* First release on PyPI.
