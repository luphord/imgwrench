=======
History
=======

0.10.0 (2020-03-04)
-------------------

* -m/--method option to colorfix (default: quantiles)
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
* images can be saved in PNG format using --png CLI flag

0.7.1 (2019-05-16)
------------------

* fix development status

0.7.0 (2019-05-16)
------------------

* option for preserving exif image metadata
* fix error when running with -k/--keep-names
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

* -d/--digits option to specify number of digits in file names
* -c/--increment option to define increment for file numbering
* create non-existing output folder instead of complaining

0.2.0 (2019-01-30)
------------------

* no-op save command for only saving images
* raise exception if output image already exists
* -f / --force-overwrite flag to enable overwriting output
* tests for cli, pipeline and resize

0.1.1 (2019-01-29)
------------------

* Fix __main__ module

0.1.0 (2019-01-29)
------------------

* First release on PyPI.
