from matplotlib import pyplot as plt
from attitude.display.polar import pole, uncertain_pole

def strike_dip(dip, azimuth):
    return azimuth-90, dip

def plot_pole(ax, o, *args, **kwargs):
    uncertain_pole(ax, *o.strike_dip_rake(), *o.angular_errors(), *args, **kwargs)

fig = plt.figure()

ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim([0,20])
ax.set_rticks([4,8,12,16,20])
ax.grid()

# East-facing hillslope
dip, azimuth = 16, 80
sd = strike_dip(dip, azimuth)
pole(ax, *sd, 'ro', markersize=3)

o = orientation_model('e-hillslope')
plot_pole(ax, o)

# Northwest-facing hillslope
dip, azimuth = 18, 345
sd = strike_dip(dip, azimuth)
pole(ax, *sd, 'ro', markersize=3)

o = orientation_model('nw-hillslope')
plot_pole(ax, o)
