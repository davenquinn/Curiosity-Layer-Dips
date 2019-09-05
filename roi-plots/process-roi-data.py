#!/usr/bin/env python
from sys import argv
from json import dump
from pandas import read_parquet
from stat_models import basic_model, weighted_model, monte_carlo_model

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

df = read_parquet(argv[1])
outdir = argv[2]

groups = df.groupby(level=['sol', 'image', 'roi'])

# Run the model in a bunch of different ways
basic = groups.apply(basic_model)
weighted = groups.apply(weighted_model)
monte_carlo = groups.apply(monte_carlo_model)
monte_carlo_rescaled = groups.apply(monte_carlo_model, scale_errors=0.1)
#params = monte_carlo.apply(get_parameters)

dump_json(basic, f"{outdir}/attitudes-no-errors.json")
dump_json(weighted, f"{outdir}/attitudes-weighted.json")
dump_json(monte_carlo, f"{outdir}/attitudes-monte-carlo.json")
dump_json(monte_carlo_rescaled, f"{outdir}/attitudes-monte-carlo-rescaled.json")
