from IPython import embed
import numpy as N
import spectra
from pandas import read_excel
from sys import path, argv
from pathlib import Path
from attitude.orientation.reconstructed import ReconstructedPlane
from attitude.display.polar import pole_error
from matplotlib import pyplot as plt
from matplotlib import patches
from itertools import chain

# Add local modules to path
path.append(str(Path(__file__).absolute().parent.parent/'modules'))

data_file = str(Path(__file__).parent/"all_PCA_dips_montecarlo_BP_singlerun_three_std_final.xlsx")
outfile = argv[1]
outfile2 = argv[2]

df = read_excel(data_file)

# Create figure
fig, axes = plt.subplots(
    nrows=1,
    ncols=2,
    figsize=(12, 6),
    subplot_kw=dict(projection='polar'))

fig2, axes2 = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(6, 6),
    subplot_kw=dict(projection='polar'))
axes2 = axes2.reshape(4)

for ax in chain(axes,axes2):
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim([0,25])
    ax.grid(dashes=(2,2))

for ax in axes2:
    ax.set_xticklabels([])
    ax.set_yticklabels([])


black = (0,0,0)

def create_plane(row):
    """Function to create reconstructed planes"""
    return ReconstructedPlane(
        row["Dip Direction"]-90, # Strike
        row["Dip"],
        row["Rake"],
        row["Max_e"]/2,
        row["Min_e"]/2)

df['plane'] = df.apply(create_plane, axis=1)

def opacity(orientation):
    """Opacity that is roughly inversely proportional to
    the ellipse's area in steradians
    """
    errors = N.radians(orientation.angular_errors())
    area = N.pi*N.prod(errors/2)
    return N.interp(area, (0.001, 0.01), (0.05, 0.005))

for i, row in df.iterrows():
    orientation = row['plane']
    o = opacity(orientation)
    e = o+0.05
    pole_error(
        axes[0],
        orientation,
        color='black',
        fc=(*black, o),
        ec=(*black, e),
        linewidth=0.5)

grouped = df.groupby("Geological Classification")
color_ix = dict(IO="black",IOC="red",B="green",OL="blue")
group_ix = dict(IO=0,IOC=1,B=2,OL=3)

for name, group in grouped:
    color = spectra.html(color_ix[name])
    for i, row in group.iterrows():
        orientation = row['plane']
        o = opacity(orientation)
        e = o+0.05
        pole_error(
            axes[1],
            orientation,
            fc=(*color.rgb, o),
            ec=(*color.rgb, e),
            linewidth=0.5)
        # Plot to four-up figure
        groupix = group_ix[name]
        pole_error(
            axes2[groupix],
            orientation,
            fc=(*color.rgb, o*2),
            ec=(*color.rgb, o*2+0.1),
            linewidth=0.5)

plt.tight_layout()

# fig.legend(handles=[
    # patches.Patch(color='black', label='Bedding'),
    # patches.Patch(color='blue', label='Cross-bedding')
# ], frameon=False)

#ax.set_rticks([15,30,45,60])
#ax.grid(zorder=12)
#ax.set_axisbelow(False)

fig.savefig(outfile, bbox_inches='tight')
fig2.savefig(outfile2, bbox_inches='tight')
