#!/usr/bin/env python

import rasterio
from fiona import collection
from shapely.geometry import shape
from shapely.ops import transform
import numpy as N
from json import dump
from sys import argv

from attitude import Orientation, plot_aligned
from attitude.helpers.dem import extract_shape

file_key = '575047622'
XYZFILE=f"traces/sol_2000_images/MLG_{file_key}XYZ_S0682626MCAM10489M1.img"
# Features were digitized off from_nathan/2000/MLF_575047622ILT_S0682626MCAM10489M1.img
LINES=f"traces/digitized-traces/MLF_{file_key}-lines.geojson"
POLYS=f"traces/digitized-traces/MLF_{file_key}-polygons.geojson"

features = []
mappings = []

def reject_outliers(data, n=4):
    m = data.mean(axis=0)
    s = data.std(axis=0)
    ix = N.all(N.abs(data-m) < n*s, axis=1)
    return data[ix]

def extract_feature(feature, dem, embed=False):
    geom = shape(feature['geometry'])
    # QGIS uses a negative Y axis for pixel coordinates
    tfunc = lambda x,y: (x,-y)
    geom = transform(tfunc, geom)

    # We don't support multiband extraction yet
    x = extract_shape(geom, dem, band=1)
    y = extract_shape(geom, dem, band=2)
    z = extract_shape(geom, dem, band=3)

    # Z in Curiosity site frame is apparently down, whose idea was that?
    z *= -1

    ix = N.index_exp[:,-1]
    xyz = N.column_stack((x[ix], y[ix], z[ix]))

    xyz = xyz[xyz.sum(axis=1) != 0]
    # We don't deal well with doubles right now
    return xyz.astype(N.float32)


# QGIS gives us points with negative y axis pixels
with rasterio.open(XYZFILE,'r') as outcrop:
    with collection(LINES, 'r') as f:
        # Everything should be in pixel coordinates
        for feature in f:
            xyz = extract_feature(feature, outcrop)
            if len(xyz) == 0:
                continue
            features.append(xyz)

    with collection(POLYS, 'r') as f:
        # Everything should be in pixel coordinates
        for feature in f:
            xyz = extract_feature(feature, outcrop)
            if len(xyz) == 0:
                continue
            features.append(xyz)

# Compute orientations for features
for i, xyz in enumerate(features):
    xyz_ = reject_outliers(xyz)
    val = Orientation(xyz_)
    fig = plot_aligned(val)
    fig.savefig(f"output/{file_key}_{i}.pdf", bbox_inches='tight')
    mappings.append(val.to_mapping())

folder = argv[1]
with open(f"{folder}/{file_key}-attitudes.json", 'w') as f:
    dump(mappings, f)
