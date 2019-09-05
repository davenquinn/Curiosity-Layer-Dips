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
    #print(pth)
    #assert pth.exists()
    return pth

def get_params(xyz):
    sol_id = int(xyz.parent.name)
    image_id = int(xyz.stem.split("_")[0])
    print(sol_id, image_id)
    return sol_id, image_id

def create_dataframe(xyz):
    xye = find_xye(xyz)
    sol_id, image_id = get_params(xyz)

    df0 = read_roi(xyz, "ID X Y x y z")
    df1 = read_roi(xye, "ID X Y xe ye ze")

    for i, (coord, error) in enumerate(zip(df0, df1)):
        # Iterate through ROIs in this dataframe
        df = coord.join(error)
        df.reset_index(inplace=True)

        df['sol'] = sol_id
        df['image'] = image_id
        df['roi'] = i

        yield df

data_dir = Path(__file__).parent/"data"

xyz_files = data_dir.glob("**/*_xyz.txt")
roi_list = []
for xyz in xyz_files:
    # Skip stacked data for now
    if xyz.stem.startswith("stacked"):
        continue
    try:
        roi_list += list(create_dataframe(xyz))
    except FileNotFoundError as err:
        secho(str(err), fg='red')

df = concat(roi_list)
df.set_index(['sol','image','roi'], inplace=True)

# Convert pixel coords to integer for simplicity
df.loc[:,'X'] = df.loc[:,'X'].astype(int)
df.loc[:,'Y'] = df.loc[:,'X'].astype(int)

# Write this out to an intermediate machine-readable data file so we
# don't have to parse ROIs every time.
df.to_parquet(argv[1])
