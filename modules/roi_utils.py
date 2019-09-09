from pandas import read_csv
from numpy import split
from click import secho

def read_roi(fn, names):
    df = read_csv(str(fn),
            delim_whitespace=True,
            comment=';',
            skip_blank_lines=False,
            names=names.split())
    frames = split(df, df[df.isnull().all(1)].index)
    for df in frames:
        df.drop(columns=["ID"], inplace=True)
        df.set_index(["X","Y"], inplace=True)
        df.dropna(how='all', inplace=True)
    return frames

def import_stereo_roi(xyz_path, xye_path=None, default_error=0.005):
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
        secho(str(err), fg='red')
        secho(f"Setting error to {default_error} on all axes", dim=True)
        for df in df_xyz:
            # Set error to a low symmetrical value
            df['xe'] = df['ye'] = df['ze'] = default_error
            yield df
