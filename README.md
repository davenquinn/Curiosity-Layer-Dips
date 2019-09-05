# Curiosity layer dips

This repository contains codes to analyze layer dips
extracted from Curiosity rover Mastcam images.

## Running the code

The code in this repository is split into several parts, each in a
specific subdirectory. Python 3.7 is required for most operations.

Several dependencies are locally linked so they can be developed in
tandem with this module. These can be installed and periodically synced using
`git submodule update --init`.

Data files are tracked in this module using `git annex`. This means that the
actual contents of the data files are not stored in the repository, but the
file reference and checksum is. This should make it possible to understand what
data was used, but it is *experimental* – I have not yet validated how easy it is to
manage data files in this way, beyond the basics.

The code can be run using `make`. `make -B` will run everything, while
`make traces`, `make roi_plots`, and `make graphics` will run individual parts.
