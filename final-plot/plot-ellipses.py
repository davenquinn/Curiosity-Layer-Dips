from IPython import embed
from pandas import read_excel
from sys import path, argv
from pathlib import Path

# Add local modules to path
path.append(str(Path(__file__).absolute().parent.parent/'modules'))

data_file = str(Path(__file__).parent/"all_PCA_dips_montecarlo_BP_singlerun_three_std_final.xlsx")
outfile = argv[1]

df = read_excel(data_file)

embed(); raise

