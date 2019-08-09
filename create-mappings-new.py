#!/usr/bin/env python

from pandas import read_excel
from json import dump
from attitude.orientation.reconstructed import ReconstructedPlane

fn = "from_nathan/results_new_method/all_PCA_dips_montecarlo_BP_singlerun.xlsx"
df = read_excel(fn)

def make_mapping(row):
    strike = row['Dip Direction']-90
    o = ReconstructedPlane(
            strike,
            row['Dip'],
            row['Rake'],
            row['Min_e'],
            row['Max_e'])
    return o.to_mapping()

collection = [make_mapping(row) for i, row in df.iterrows()]

with open("webapp/attitudes-new.json", 'w') as f:
    dump(collection, f)
