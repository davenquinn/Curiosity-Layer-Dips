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

index = {
    11: '#ff0608',
    2: '#fe999a',
    10: '#ecad15',
    1: '#c0ddc6',
    9: '#49bdee',
    12: '#6279a3',
    7: '#2b3e62'
}

order = [11,2,10,1,9,12,7]

arr = []
orientations = df.groupby(level='roi').apply(mc)
for ix,val in orientations.items():
    key = ix+1
    if key not in index.keys():
        continue
    arr.append(val.to_mapping(
        centered_array=None,
        roi=key,
        index=order.index(key),
        color=index[key],
        stacked=False))

arr.sort(key=lambda x: x['index'])

stacked = df_stack.groupby(level='roi').apply(mc)
for ix,val in stacked.items():
    arr.append(val.to_mapping(
        centered_array=None,
        color='#888888',
        stacked=True))

dump(arr, stdout)
