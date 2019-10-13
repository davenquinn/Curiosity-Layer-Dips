#!/usr/bin/env python

# Extract ROIs to pandas data frame

from sys import path, stdout
from pathlib import Path
from pandas import concat
from json import dump

# Add local modules to path
path.append(str(Path(__file__).absolute().parent.parent/'modules'))
# Local ROI utilities
from roi_dataframe import merge_stacks, create_dataframe
from stat_models import monte_carlo_model
from json_output import dump_json

data_dir = Path(__file__).parent/"data"

xyz_files = data_dir.glob("*_xyz.txt")
df = concat([f for f in create_dataframe(next(xyz_files), stack=0)])
df.set_index('roi', inplace=True)
df_stack = merge_stacks(df, groupby='roi')

# 3s monte carlo model
mc = lambda x: monte_carlo_model(x, scale_errors=0.364)

arr = []
orientations = df.groupby(level='roi').apply(mc)
for ix,val in orientations.items():
    arr.append(val.to_mapping(
        centered_array=None,
        roi=ix,
        stacked=False))

stacked = df_stack.groupby(level='roi').apply(mc)
for ix,val in stacked.items():
    arr.append(val.to_mapping(
        centered_array=None,
        roi=ix,
        stacked=True))

dump(arr, stdout)
