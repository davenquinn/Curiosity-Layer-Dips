#!/usr/bin/env python
from sys import argv
from json import dump
from pandas import read_parquet, concat
from stat_models import basic_model, weighted_model, monte_carlo_model

def get_parameters(val):
    return Series([
        val.n,
        *val.strike_dip_rake(),
        *val.angular_errors()
    ], index="n strike dip rake min_err max_err".split())

def create_mapping(ix, val):
    stacked = ix[1].startswith('stack')
    return val.to_mapping(
        centered_array=None,
        sol=ix[0],
        image=ix[1],
        roi=ix[2],
        stacked=stacked)

def dump_json(frame, filename):
    with open(filename, 'w') as f:
        dump([
            create_mapping(i,v)
            for i,v in frame.items()
        ], f)

df = read_parquet(argv[1])
outdir = argv[2]

# Merge stacks

stacked = (df.index
    .get_level_values('image')
    .str.startswith('stack'))

# Make sure we don't get SettingWithCopyWarning
df_stacked = df[stacked].copy()
df_normal = df[~stacked]

# Center stacks around mean on each axis
# Normally this would be done within the Attitude model,
# but doing it outside allows us to have simpler code.
g = df_stacked.groupby(level=['sol','image','roi'])
for ax in ['x','y','z']:
    # Center each axis around mean
    df_stacked.loc[:,ax] = g[ax].transform(lambda x: x-x.mean())

df_stacked.reset_index(level=2, inplace=True)
df_stacked.loc[:,'roi'] = 0
df_stacked.set_index('roi', drop=True, inplace=True, append=True)
df = concat([df_normal, df_stacked])

groups = df.groupby(level=['sol', 'image', 'roi'])

models = {
    "no-error": basic_model,
    "weighted": weighted_model,
    "monte-carlo": monte_carlo_model,
    "monte-carlo-3s": lambda x: monte_carlo_model(x, scale_errors=0.364),
    "monte-carlo-5s": lambda x: monte_carlo_model(x, scale_errors=0.210)
}

# Run the model in a bunch of different ways
for name, model in models.items():
    print(f"Running model {name}")
    res = groups.apply(model)
    dump_json(res, f"{outdir}/attitudes-{name}.json")
