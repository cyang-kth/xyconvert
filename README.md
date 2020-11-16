### xyconvert

This is a python package for converting xy coordinates (in lng,lat order) in numpy array between WGS-84, GCJ-02 and BD-09 system.

The conversion in numpy is much more efficient (50-70 times speedup) compared with previous Python implementations such as [eviltransform](https://github.com/googollee/eviltransform) and [coordTransform_py](https://github.com/wandergis/coordTransform_py) that convert only a single point at each call.

### Install the package

```bash
pip install xyconvert
```

### Usage

```python
from xyconvert import gcj2wgs
import numpy as np
gcj_xy = np.asarray([[104.07008157,  30.73199687],
       [104.07008159,  30.73177709],
       [104.06999188,  30.73147758]])
wgs_xy = gcj2wgs(gcj_xy)
print wgs_xy
'''
[[104.06756309  30.73437796]
 [104.06756312  30.73415829]
 [104.06747357  30.73385904]]
'''
```

### Reference

The code is partly copied/modified from https://github.com/Argons/nextlocation and https://github.com/wandergis/coordTransform_py.
