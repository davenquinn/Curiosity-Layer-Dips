#!/usr/bin/env python

from pandas import read_excel
from json import dump
from attitude.orientation.reconstructed import ReconstructedPlane

df = read_excel("from_nathan/all_PCA_dips_noxye.xlsx")

def make_mapping(row):
    strike = row['Dip Direction']-90
    o = ReconstructedPlane(
            strike,
            row['Dip'],
            row['Rake'],
            row['min'],
            row['max'])
    return o.to_mapping()

collection = [make_mapping(row) for i, row in df.iterrows()]

with open("webapp/attitudes.json", 'w') as f:
    dump(collection, f)


