#!/usr/bin/env python

# Extract ROIs to pandas data frame

import sys
from pathlib import Path
from pandas import concat

# Add local modules to path
sys.path.append(str(Path(__file__).absolute().parent.parent/'modules'))
# Local ROI utilities
from roi_dataframe import merge_stacks, create_dataframe

data_dir = Path(__file__).parent/"data"

xyz_files = data_dir.glob("*_xyz.txt")
df = concat([f for f in create_dataframe(next(xyz_files), stack=0)])
df.set_index('roi', inplace=True)
df_stack = merge_stacks(df, groupby='roi')

import IPython; IPython.embed(); raise
