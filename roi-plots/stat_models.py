import numpy as N
from attitude.orientation import Orientation

def get_values(roi):
    xyz = roi.loc[:,["x","y","z"]].values
    xye = roi.loc[:,["xe","ye","ze"]].values
    return xyz, xye

def basic_model(roi):
    """
    Orientation model that incorporates data without any accounting for errors.
    """
    xyz, xye = get_values(roi)
    return Orientation(xyz)

def weighted_model(roi):
    """
    Orientation model that applies a uniform error weighting to each axis.
    """
    xyz, xye = get_values(roi)
    xym = xye.mean(axis=0)
    # Normalize error so the min error is weighted 1
    norm_err = xym/xym.min()
    return Orientation(xyz, weights=1/norm_err)

def monte_carlo_model(roi, n=1000, scale_errors=1):
    xyz,xye = get_values(roi)
    # Monte Carlo
    # Monte Carlo with 1000 replicates of each point
    xyzmc = N.repeat(xyz, n, axis=0)
    xyemc = N.repeat(xye*scale_errors, n, axis=0)
    # Random normal distribution
    fuzz = N.random.randn(*xyzmc.shape)
    # Apply the scaled error
    xyzmc += xyemc*fuzz
    return Orientation(xyzmc)
