#!/usr/bin/env python

from sys import argv
from os import path
from pandas import read_excel
from json import dump
from attitude.orientation.reconstructed import ReconstructedPlane

outdir = argv[1]

def make_mapping(row):
    strike = row['Dip Direction']-90
    o = ReconstructedPlane(
            strike,
            row['Dip'],
            row['Rake'],
            row['Min_e'],
            row['Max_e'])
    return o.to_mapping(
            sol=row['Sol'],
            id=row['ID'],
            n=row['n'],
            L=row['L'],
            ratio_1=row['First PC Ratio'],
            ratio_2=row['Second PC Ratio'])

data = {
    '1s': 'all_PCA_dips_montecarlo_BP_singlerun_one_std_w_errors',
    '1s-stacked': 'all_PCA_dips_montecarlo_BP_singlerun_one_std_w_errors_stacked_results',
    '2s': 'all_PCA_dips_montecarlo_BP_singlerun_one_std_w_errors',
    '2s-stacked': 'all_PCA_dips_montecarlo_BP_singlerun_two_std_w_errors_stacked_results'
}

for k,v in data.items():
    fn = f"data/{v}.xlsx"
    df = read_excel(fn)

    collection = [make_mapping(row) for i, row in df.iterrows()]

    fp = path.join(outdir, f"attitudes-{k}.json")
    with open(fp, 'w') as f:
        dump(collection, f)
