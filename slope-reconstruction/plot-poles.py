import sys
from matplotlib import pyplot as plt
from attitude.display.polar import pole, uncertain_pole
from attitude import Orientation
from pathlib import Path

# Add local modules to path
sys.path.append(str(Path(__file__).parent.parent/'modules'))
# Local ROI utilities
from roi_utils import import_stereo_roi

def swap_columns(df, c1, c2):
    df.loc[:,"__"] = df.loc[:,c2]
    df.loc[:,c2] = df.loc[:,c1]
    df.loc[:,c1] = df.loc[:,"__"]
    return df.drop("__", axis=1)

def orientation_model(label):
    fn = Path(__file__).parent/'data'/(label+'.txt')
    df = next(import_stereo_roi(fn))

    # x cross y = z
    # y cross x = -z
    # To invert z and maintain right-hand-rule, we swap x and y

    # Swap x and y axes, and invert z
    df = swap_columns(df,'x','y')
    df = swap_columns(df,'xe','ye')
    df.loc[:,"z"] *= -1

    xyz = df.loc[:,["x","y","z"]].values
    return Orientation(xyz)

def strike_dip(dip, azimuth):
    return azimuth-90, dip

def plot_pole(ax, o, *args, **kwargs):
    uncertain_pole(ax,
        *o.strike_dip_rake(),
        *o.angular_errors(),
        *args, **kwargs)

fig = plt.figure()

ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim([0,25])
ax.set_rticks([5,10,15,20])
ax.grid()

# East-facing hillslope
dip, azimuth = 16, 80
sd = strike_dip(dip, azimuth)
pole(ax, *sd, marker="o", markersize=3, color='C1')

o = orientation_model('e-hillslope')
plot_pole(ax, o, color='C1', alpha=0.5)

# Northwest-facing hillslope
dip, azimuth = 18, 345
sd = strike_dip(dip, azimuth)
pole(ax, *sd, 'ro', markersize=3, color='C2')

o = orientation_model('nw-hillslope')
plot_pole(ax, o, color='C2', alpha=0.5)

ax.grid()

fig.savefig(sys.argv[1], bbox_inches='tight')
