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

df = read_excel(data_file)

def setup_axis(ax):
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rlim([0,25])
    ax.grid(dashes=(2,2))

# Create figure
fig, axes = plt.subplots(
    nrows=1,
    ncols=2,
    figsize=(12, 6),
    subplot_kw=dict(projection='polar'))

for ax in axes:
    setup_axis(ax)

black = (0,0,0)

def plot_ellipses(ax, row, color, opacity_scale=1):
    orientation = row['plane']
    o = opacity(orientation)
    e = o+0.05
    pole_error(
        ax,
        orientation,
        fc=(*color, o*opacity_scale),
        ec=(*color, e*opacity_scale),
        linewidth=0.5)

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
    plot_ellipses(axes[0], row, black)

grouped = df.groupby("Geological Classification")
color_ix = dict(IO="black",IOC="red",B="green",OL="blue")
group_ix = dict(IO=0,IOC=1,B=2,OL=3)

for name, group in grouped:
    color = spectra.html(color_ix[name])
    for i, row in group.iterrows():
        plot_ellipses(axes[1], row, color.rgb)

plt.tight_layout()
fig.savefig(argv[1], bbox_inches='tight')

fig, axes = plt.subplots(
    nrows=2,
    ncols=2,
    figsize=(6, 6),
    subplot_kw=dict(projection='polar'))
axes = axes.reshape(4)

# Axis setup
for ax in axes:
    setup_axis(ax)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

for name, group in grouped:
    color = spectra.html(color_ix[name])
    groupix = group_ix[name]
    for i, row in group.iterrows():
        plot_ellipses(axes[groupix], row, color.rgb, opacity_scale=2)

plt.tight_layout()
fig.savefig(argv[2], bbox_inches='tight')

