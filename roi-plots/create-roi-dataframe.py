#!/usr/bin/env python

# Extract ROIs to pandas data frame

import numpy as N
from click import secho
from pandas import read_csv, concat
from sys import argv
from pathlib import Path

def read_roi(fn, names):
    df = read_csv(str(fn),
            delim_whitespace=True,
            comment=';',
            skip_blank_lines=False,
            names=names.split())
    frames = N.split(df, df[df.isnull().all(1)].index)
    for df in frames:
        df.drop(columns=["ID"], inplace=True)
        df.set_index(["X","Y"], inplace=True)
        df.dropna(how='all', inplace=True)
    return frames

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

def join_frames(coord_frames, error_frames):
    for coord, error in zip(coord_frames, error_frames):
        yield coord.join(error)

def create_dataframe(xyz, stack=None, default_error=0.005):
    xye = find_xye(xyz)
    sol_id, image_id = get_params(xyz, stack=stack)

    df0 = read_roi(xyz, "ID X Y x y z")
    df_c = None

    # Get errors if they exist
    try:
        df1 = read_roi(xye, "ID X Y xe ye ze")
        df_c = join_frames(df0,df1)
    except FileNotFoundError as err:
        secho(str(err), fg='red')
        df_c = df0
        for df in df_c:
            # Set error to a low symmetrical value
            df['xe'] = df['ye'] = df['ze'] = default_error

    for i, df in enumerate(df_c):
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
df.to_parquet(argv[1])
