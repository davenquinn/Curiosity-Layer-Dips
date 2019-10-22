# Extract ROIs to pandas data frame

from pandas import concat
from pathlib import Path

# Local ROI utilities
from roi_utils import import_stereo_roi

def find_xye(xyz):
    new_name = xyz.name.replace("xyz", "xye")
    pth = xyz.with_name(new_name)
    return pth

def get_params(xyz, stack=None):
    """
    Try to get sol and image id from filename
    """
    try:
        sol_id = int(xyz.parent.name)
    except ValueError:
        return 0, 0
    if stack is not None:
        image_id = "stack_"+str(stack)
    else:
        image_id = str(xyz.stem.split("_")[0])
    print(sol_id, image_id)
    return sol_id, image_id

def create_dataframe(xyz, stack=None, **kwargs):
    xye = find_xye(xyz)
    sol_id, image_id = get_params(xyz, stack=stack)

    res = enumerate(import_stereo_roi(xyz, xye, **kwargs))

    for i, df in res:
        # Iterate through ROIs in this dataframe
        df.reset_index(inplace=True)

        df['sol'] = sol_id
        df['image'] = image_id
        df['roi'] = i

        yield df

def merge_stacks(df, groupby=['sol','image','roi']):
    # Center stacks around mean on each axis
    # Normally this would be done within the Attitude model,
    # but doing it outside allows us to have simpler code.
    df_stacked = df.copy()
    g = df_stacked.groupby(level=groupby)
    for ax in ['x','y','z']:
        # Center each axis around mean
        df_stacked.loc[:,ax] = g[ax].transform(lambda x: x-x.mean())

    df_stacked.reset_index(level='roi', inplace=True)
    df_stacked.loc[:,'roi'] = 0
    df_stacked.set_index('roi', drop=True, inplace=True, append=True)
    return df_stacked


def merge_all_stacks(indf):
    # Merge stacked data along axis
    stacked = (indf.index
        .get_level_values('image')
        .str.startswith('stack'))
    # Make sure we don't get SettingWithCopyWarning
    df_stacked = merge_stacks(indf[stacked].copy())
    df_normal = indf[~stacked].copy()

    return concat([df_normal, df_stacked])

def roi_stream(file_stream):
    for xyz_file in file_stream:
        stack = 0 if xyz_file.stem.startswith("stacked") else None
        yield from create_dataframe(xyz_file, stack=stack)

def import_roi_files(xyz_files):
    df = concat([f for f in roi_stream(xyz_files)])
    df.set_index(['sol','image','roi'], inplace=True)
    # Merge stacked data
    return merge_all_stacks(df)
