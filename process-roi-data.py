#!/usr/bin/env python

from sys import argv
from click import secho
from pandas import read_parquet
from os import environ
import numpy as N

#from matplotlib import use
#environ['ITERMPLOT'] = ''
#use('module://itermplot')
#from matplotlib.pyplot import style
#style.use('dark_background')

from attitude.orientation import Orientation
from attitude.display import plot_aligned

df = read_parquet(argv[1])

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

for key, roi in df.groupby(level=0):
    secho(key, bold=True)
    for col in 'x y z'.split():
        print(col+" "+range_desc(roi[col]))
    for col in 'xe ye ze'.split():
        print(col+" "+err_desc(roi[col]))
    print("")

    xyz = roi.loc[:,["x","y","z"]].values

    # Basic
    val = Orientation(xyz)
    fig = plot_aligned(val)
    fig.savefig(f"plots/{key}_basic.pdf", bbox_inches='tight')


    xye = roi.loc[:,["xe","ye","ze"]]
    xym = xye.mean()
    norm_err = xym/xym.min()

    weights = 1/norm_err
    print(xye, weights)

    # Weighted
    val = Orientation(xyz, weights=weights.values)
    fig = plot_aligned(val)
    fig.savefig(f"plots/{key}_weighted.pdf", bbox_inches='tight')

    # Monte Carlo
    # Monte Carlo with 1000 replicates of each point
    xyzmc = N.repeat(xyz, 100, axis=0)
    xyemc = N.repeat(xye.values, 100, axis=0)

    fuzz = N.random.randn(*xyzmc.shape)

    xyzmc += xyemc*fuzz

    val = Orientation(xyzmc)
    fig = plot_aligned(val)
    fig.savefig(f"plots/{key}_monte_carlo.pdf", bbox_inches='tight')

