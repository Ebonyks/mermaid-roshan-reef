#!/usr/bin/env python3
"""Eye openness per cell: dark iris pixels in the two K0 eye boxes, as a share of frame 0.

K0's irises sit at cell (132, 61) and (152, 61), about 9x9 px each. Each box adds a few pixels of
margin for head motion. A share under 0.7 marks a frame where the lids cover most of the iris.
Numbers only.

    python -I scripts/eye_openness.py <cells dir> [...]
"""
import json, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image

BOXES = ((123, 53, 141, 70), (144, 53, 162, 70))     # x0, y0, x1, y1, 256 px cell


def dark(p):
    a = np.array(Image.open(p).convert('RGBA'))
    v = cv2.cvtColor(np.ascontiguousarray(a[..., :3]), cv2.COLOR_RGB2HSV)[..., 2]
    d = (v < 150) & (a[..., 3] > 200)
    return sum(int(d[y0:y1, x0:x1].sum()) for x0, y0, x1, y1 in BOXES)


def report(cells):
    files = sorted(Path(cells).glob('*.png'))
    s = [dark(f) for f in files]
    share = [round(x / s[0], 2) for x in s]
    return {'iris_px_frame0': s[0], 'share_of_frame0': share, 'mostly_closed_frames': [i for i, x in enumerate(share) if x < 0.7]}


if __name__ == '__main__':
    for c in sys.argv[1:]:
        r = report(c); print(c, json.dumps({k: r[k] for k in ('iris_px_frame0', 'mostly_closed_frames')}))
