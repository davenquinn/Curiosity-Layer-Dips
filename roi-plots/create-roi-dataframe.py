#!/usr/bin/env python

# Extract ROIs to pandas data frame

import numpy as N
from pandas import read_csv, concat
from sys import argv

def read_roi(fn, names):
    df = read_csv(fn,
            delim_whitespace=True,
            comment=';',
            skip_blank_lines=False,
            names=names)
    frames = N.split(df, df[df.isnull().all(1)].index)
    for df in frames:
        df.drop(columns=["ID"], inplace=True)
        df.set_index(["X","Y"], inplace=True)
        df.dropna(how='all', inplace=True)
    return frames

def get_data(ix):
    key = str(ix)+"_MR"
    prefix = "roi-plots/data/"+key
    xyz = read_roi(prefix+"_xyz.txt",
            "ID X Y x y z".split())
    xye = read_roi(prefix+"_xye.txt",
            "ID X Y xe ye ze".split())

    for i, (coord, error) in enumerate(zip(xyz, xye)):
        df = coord.join(error)
        yield concat([df], keys=[key+f"_{i:.0f}"], names=['key'])

point_clouds = []
for ix in [2980, 6826]:
    point_clouds += list(get_data(ix))

# Create a single data frame for all point clouds
df = concat(point_clouds)

# Write this out to an intermediate machine-readable data file so we
# don't have to recalculate the Monte Carlo model every time.
df.to_parquet(argv[1])
