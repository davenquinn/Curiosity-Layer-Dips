from pandas import read_csv
from numpy import split
from click import secho

def swap_columns(df, c1, c2):
    df.loc[:,"__"] = df.loc[:,c2]
    df.loc[:,c2] = df.loc[:,c1]
    df.loc[:,c1] = df.loc[:,"__"]
    return df.drop("__", axis=1)

def site_frame_to_global(df):
    """
    Convert Curiosity site frame coordinates to global frame
    coordinates suitable for use in GIS programs.

    Site frame: x North, y East, z Down
    Global frame: x East, y North, z Up
    """

    # Swap x and y axes, and invert z
    df = swap_columns(df,'x','y')
    df = swap_columns(df,'xe','ye')
    df.loc[:,"z"] *= -1
    return df

def read_roi(fn, names):
    df = read_csv(str(fn),
            delim_whitespace=True,
            comment=';',
            skip_blank_lines=False,
            names=names.split())
    frames = split(df, df[df.isnull().all(1)].index)
    for df in frames:
        df.drop(columns=["ID"], inplace=True)
        df.dropna(how='all', inplace=True)

        # Convert pixel coords to integer for simplicity
        df.loc[:,'X'] = df.loc[:,'X'].astype(int)
        df.loc[:,'Y'] = df.loc[:,'Y'].astype(int)
        df.set_index(["X","Y"], inplace=True)

    return frames

def __import_stereo_roi(xyz_path, xye_path=None, default_error=0.005):
    """
    Import a Curiosity MastCam stereo ROI from ENVI 5 ROIs
    """
    df_xyz = read_roi(xyz_path, "ID X Y x y z")
    # Get errors if they exist
    try:
        assert xye_path is not None
        df_xye = read_roi(xye_path, "ID X Y xe ye ze")
        # Join error to coordinates
        for coord, error in zip(df_xyz, df_xye):
            yield coord.join(error)
    except (FileNotFoundError, AssertionError) as err:
        secho(str(err), fg='red', err=True)
        secho(f"Setting error to {default_error} on all axes", dim=True, err=True)
        for df in df_xyz:
            # Set error to a low symmetrical value
            df['xe'] = df['ye'] = df['ze'] = default_error
            yield df

def import_stereo_roi(*args, **kwargs):
    for df in __import_stereo_roi(*args,**kwargs):
        yield site_frame_to_global(df)
