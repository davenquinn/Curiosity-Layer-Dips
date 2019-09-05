#!/usr/bin/env python

from sys import argv
from click import secho
from pandas import read_parquet, DataFrame, Series
from os import environ
import numpy as N
from json import dump
import re

from attitude.orientation import Orientation
from attitude.display import plot_aligned

df = read_parquet(argv[1])
outdir = argv[2]

def range_desc(series):
    mn = series.min()
    mx = series.max()
    rng = mx-mn
    return f"range {rng:8.3f} m"

def err_desc(series):
    mn = series.mean()
    mx = series.max()
    rng = mx-mn
    return f"mean {mn:5.3f}, max {mx:5.3f} m"

def get_values(roi):
    xyz = roi.loc[:,["x","y","z"]].values
    xye = roi.loc[:,["xe","ye","ze"]].values
    return xyz, xye

def basic_model(roi):
    """
    Orientation model that incorporates data without any accounting for errors.
    """
    xyz, xye = get_values(roi)
    return Orientation(xyz)

def weighted_model(roi):
    """
    Orientation model that applies a uniform error weighting to each axis.
    """
    xyz, xye = get_values(roi)
    xym = xye.mean()
    # Normalize error so the min error is weighted 1
    norm_err = xym/xym.min()
    return Orientation(xyz, weights=1/norm_err)

def monte_carlo_model(roi, n=1000):
    xyz,xye = get_values(roi)
    # Monte Carlo
    # Monte Carlo with 1000 replicates of each point
    xyzmc = N.repeat(xyz, n, axis=0)
    xyemc = N.repeat(xye, n, axis=0)
    # Random normal distribution
    fuzz = N.random.randn(*xyzmc.shape)
    # Apply the scaled error
    xyzmc += xyemc*fuzz
    return Orientation(xyzmc)

def get_parameters(val):
    return Series([
        val.n,
        *val.strike_dip_rake(),
        *val.angular_errors()
    ], index="n strike dip rake min_err max_err".split())

def create_mapping(ix, val):
    return val.to_mapping(
        centered_array=None,
        sol=ix[0],
        image=ix[1],
        roi=ix[2])

def dump_json(frame, filename):
    with open(filename, 'w') as f:
        dump([create_mapping(i,v) for i,v in frame.items()], f)

groups = df.groupby(level=['sol', 'image', 'roi'])
basic = groups.apply(basic_model)
#weighted = groups.apply(weighted_model)
monte_carlo = groups.apply(monte_carlo_model)
#params = monte_carlo.apply(get_parameters)

dump_json(basic, f"{outdir}/attitudes-no-errors.json")
#dump_json(weighted, f"{outdir}/attitudes-weighted.json")
dump_json(monte_carlo, f"{outdir}/attitudes-monte-carlo.json")
