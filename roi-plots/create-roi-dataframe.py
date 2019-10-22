#!/usr/bin/env python

# Extract ROIs to pandas data frame

import sys
from click import secho
from pandas import concat
from pathlib import Path

# Add local modules to path
sys.path.append(str(Path(__file__).absolute().parent.parent/'modules'))
# Local ROI utilities
from roi_dataframe import import_roi_files

data_dir = Path(__file__).parent/"data"

xyz_files = data_dir.glob("**/*_xyz.txt")
df = import_roi_files(xyz_files)

# Write this out to an intermediate machine-readable data file so we
# don't have to parse ROIs every time.
df.to_parquet(sys.argv[1])
