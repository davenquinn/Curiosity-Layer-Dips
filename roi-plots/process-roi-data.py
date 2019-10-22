#!/usr/bin/env python
from sys import path, argv
from pathlib import Path
from json import dump
from pandas import read_parquet

# Add local modules to path
path.append(str(Path(__file__).absolute().parent.parent/'modules'))
from json_output import dump_json
from stat_models import basic_model, weighted_model, monte_carlo_model

df = read_parquet(argv[1])
outdir = argv[2]

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
