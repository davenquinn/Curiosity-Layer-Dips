import sys, json
from attitude import Orientation
from pathlib import Path

# Add local modules to path
sys.path.append(str(Path(__file__).parent.parent/'modules'))
# Local ROI utilities
from roi_utils import import_stereo_roi

def create_mapping(o, name):
    return o.to_mapping(
        centered_array=None,
        name=name)

def orientation_models():
    for fn in (Path(__file__).parent/'xyz').glob("*_xyz.txt"):
        df = next(import_stereo_roi(fn))
        xyz = df.loc[:,["x","y","z"]].values
        o = Orientation(xyz)
        if o.angular_errors()[0] == 0:
            continue
        yield fn.stem, o

map = [create_mapping(o, name)
        for name, o in orientation_models()]

with open(sys.argv[1],'w') as f:
    json.dump(map, f)


