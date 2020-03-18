from sys import path, argv
from pathlib import Path
from json import dump
from pandas import read_parquet

# Add local modules to path
path.append(str(Path(__file__).absolute().parent.parent/'modules'))
from json_output import dump_json
from stat_models import basic_model, weighted_model, monte_carlo_model

df = read_parquet(argv[1])
outfile = argv[2]

groups = df.groupby(level=['sol', 'image', 'roi'])
res = groups.apply(basic_model)
