import sys
from matplotlib import pyplot as plt
from attitude.display.polar import pole, pole_error, uncertain_pole
from attitude import Orientation
from pathlib import Path

# Add local modules to path
sys.path.append(str(Path(__file__).parent.parent/'modules'))
# Local ROI utilities
from roi_utils import import_stereo_roi

def orientation_models():
    for fn in (Path(__file__).parent/'xyz').glob("*_xyz.txt"):
        df = next(import_stereo_roi(fn))
        xyz = df.loc[:,["x","y","z"]].values
        yield fn.stem, Orientation(xyz)

def plot_pole(ax, o, *args, **kwargs):
    sdr = o.strike_dip_rake()
    uncertain_pole(ax,
        *sdr,
        *o.angular_errors(),
        *args, **kwargs)

fig = plt.figure()

ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim([0,60])
ax.set_rticks([15,30,45,60])

ax.grid()

for name, o in orientation_models():
    print(name)
    print(o)
    if o.angular_errors()[0] == 0:
        pole(ax, *o.strike_dip(), marker='o', markersize=5, label=name)
    else:
        plot_pole(ax, o, alpha=0.5, label=name)

ax.grid()
fig.legend()

fig.savefig(sys.argv[1], bbox_inches='tight')

