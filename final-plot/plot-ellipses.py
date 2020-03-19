from IPython import embed
import numpy as N
from pandas import read_excel
from sys import path, argv
from pathlib import Path
from attitude.orientation.reconstructed import ReconstructedPlane
from attitude.display.polar import pole_error
from matplotlib import pyplot as plt
from matplotlib import patches
from spectra import scale

# Add local modules to path
path.append(str(Path(__file__).absolute().parent.parent/'modules'))

data_file = str(Path(__file__).parent/"all_PCA_dips_montecarlo_BP_singlerun_three_std_final.xlsx")
outfile = argv[1]

df = read_excel(data_file)

# Create figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim([0,25])
ax.grid()

black = (0,0,0)

for i, row in df.iterrows():
    o = ReconstructedPlane(
        row["Dip Direction"]-90, # Strike
        row["Dip"],
        row["Rake"],
        row["Max_e"]/2,
        row["Min_e"]/2)

    mx = N.radians(o.angular_errors()[1])
    opacity = 0.2-mx**0.5
    if opacity < 0.01:
        opacity = 0.01

    area=N.pi*N.prod(N.radians(o.angular_errors())/2)
    opacity = N.interp(area, (0.001, 0.01), (0.05, 0.005))
    print(area, opacity)
    ec = opacity + 0.05


    pole_error(ax, o, color='black', fc=(*black, opacity), ec=(*black,ec), linewidth=0.5)

fig.legend(handles=[
    patches.Patch(color='black', label='Bedding'),
    patches.Patch(color='blue', label='Cross-bedding')
], frameon=False)

ax.grid()

#ax.set_rticks([15,30,45,60])
#ax.grid(zorder=12)
#ax.set_axisbelow(False)

fig.savefig(outfile, bbox_inches='tight')
