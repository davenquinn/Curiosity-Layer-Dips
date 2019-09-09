#!/usr/bin/env python

# Extract ROIs to pandas data frame

import sys
from click import secho
from pandas import read_csv, concat
from pathlib import Path

# Add local modules to path
sys.path.append(str(Path(__file__).parent.parent/'modules'))
# Local ROI utilities
from roi_utils import import_stereo_roi

def find_xye(xyz):
    new_name = xyz.name.replace("xyz", "xye")
    pth = xyz.with_name(new_name)
    return pth

def get_params(xyz, stack=None):
    sol_id = int(xyz.parent.name)
    if stack is not None:
        image_id = "stack_"+str(stack)
    else:
        image_id = str(xyz.stem.split("_")[0])
    print(sol_id, image_id)
    return sol_id, image_id

def create_dataframe(xyz, stack=None, **kwargs):
    xye = find_xye(xyz)
    sol_id, image_id = get_params(xyz, stack=stack)

    res = enumerate(import_stereo_roi(xyz, xye, **kwargs))

    for i, df in res:
        # Iterate through ROIs in this dataframe
        df.reset_index(inplace=True)

        df['sol'] = sol_id
        df['image'] = image_id
        df['roi'] = i

        yield df

def merge_stacks(indf):
    # Merge stacked data along axis

    stacked = (indf.index
        .get_level_values('image')
        .str.startswith('stack'))

    # Make sure we don't get SettingWithCopyWarning
    df_stacked = indf[stacked].copy()
    df_normal = indf[~stacked].copy()

    # Center stacks around mean on each axis
    # Normally this would be done within the Attitude model,
    # but doing it outside allows us to have simpler code.
    g = df_stacked.groupby(level=['sol','image','roi'])
    for ax in ['x','y','z']:
        # Center each axis around mean
        df_stacked.loc[:,ax] = g[ax].transform(lambda x: x-x.mean())

    df_stacked.reset_index(level=2, inplace=True)
    df_stacked.loc[:,'roi'] = 0
    df_stacked.set_index('roi', drop=True, inplace=True, append=True)
    return concat([df_normal, df_stacked])

def roi_stream(file_stream):
    for xyz_file in file_stream:
        stack = 0 if xyz_file.stem.startswith("stacked") else None
        yield from create_dataframe(xyz_file, stack=stack)

data_dir = Path(__file__).parent/"data"

xyz_files = data_dir.glob("**/*_xyz.txt")
df = concat([f for f in roi_stream(xyz_files)])
df.set_index(['sol','image','roi'], inplace=True)

# z is parameterized as DOWN in in the MSL site frame, weirdly
df.loc[:,"z"] *= -1

# Convert pixel coords to integer for simplicity
df.loc[:,'X'] = df.loc[:,'X'].astype(int)
df.loc[:,'Y'] = df.loc[:,'Y'].astype(int)

# Merge stacked data
df = merge_stacks(df)

# Write this out to an intermediate machine-readable data file so we
# don't have to parse ROIs every time.
df.to_parquet(sys.argv[1])
