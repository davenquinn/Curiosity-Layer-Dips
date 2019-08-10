#!/usr/bin/env python

import rasterio
from fiona import collection
from shapely.geometry import shape
from shapely.ops import transform
import numpy as N
from affine import Affine

from attitude.helpers.dem import extract_shape

XYZFILE="from_nathan/2000/MLG_575047622XYZ_S0682626MCAM10489M1.img"
# Features were digitized off from_nathan/2000/MLF_575047622ILT_S0682626MCAM10489M1.img
LINES="traces/MLF_575047622-lines.geojson"
POLYS="traces/MLF_575047622-polygons.geojson"

features = []

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

    #xyz = xyz[xyz.sum(axis=1) != 0]
    return xyz


# QGIS gives us points with negative y axis pixels
with rasterio.open(XYZFILE,'r') as outcrop:
    with collection(LINES, 'r') as f:
        # Everything should be in pixel coordinates
        for feature in f:
            xyz = extract_feature(feature, outcrop)
            features.append(xyz)

    with collection(POLYS, 'r') as f:
        # Everything should be in pixel coordinates
        for feature in f:
            xyz = extract_feature(feature, outcrop)
            features.append(xyz)

    import IPython; IPython.embed(); raise
