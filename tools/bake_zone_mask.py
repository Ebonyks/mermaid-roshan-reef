"""Bake craft-creature paint-zone masks (R=body, G=accent, B=third zone).

The craft repaint was a 2-colour luma split — monochrome, nothing like the
book art. The references are ZONED (kitty: pastel body, WHITE muzzle+chest,
pink ears; birdie: aqua body, PINK wings, YELLOW belly, silver feet). This
bakes a mask texture from mesh GEOMETRY: rasterize every triangle in UV
space, interpolate its 3D position per texel, classify into zones. Black
(no zone) = keep the baked texture (silver horn/feet, dark beak, eyes).

USAGE: python tools/bake_zone_mask.py <rigged.glb> <kitty|birdie> <out_mask.png>
"""
import json
import struct
import sys

import numpy as np
from PIL import Image

glb_path, kind, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
SIZE = 1024

data = open(glb_path, "rb").read()
jlen = struct.unpack("<I", data[12:16])[0]
gltf = json.loads(data[20:20 + jlen])
binoff = 20 + jlen + 8
buf = data[binoff:]

def accessor(idx):
    a = gltf["accessors"][idx]
    bv = gltf["bufferViews"][a["bufferView"]]
    off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    comp = {5126: np.float32, 5123: np.uint16, 5125: np.uint32}[a["componentType"]]
    ncomp = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]
    arr = np.frombuffer(buf, dtype=comp, count=a["count"] * ncomp, offset=off)
    return arr.reshape(a["count"], ncomp) if ncomp > 1 else arr

prim = gltf["meshes"][0]["primitives"][0]
pos = accessor(prim["attributes"]["POSITION"]).astype(np.float64)
uv = accessor(prim["attributes"]["TEXCOORD_0"]).astype(np.float64)
idxs = accessor(prim["indices"]).astype(np.int64).reshape(-1, 3)
print("verts %d tris %d  bbox x[%.2f %.2f] y[%.2f %.2f] z[%.2f %.2f]" % (
    len(pos), len(idxs), pos[:, 0].min(), pos[:, 0].max(),
    pos[:, 1].min(), pos[:, 1].max(), pos[:, 2].min(), pos[:, 2].max()))

# normalize axes: GLB frame is y-up, face +z. Scale-normalize by height.
ymin, ymax = pos[:, 1].min(), pos[:, 1].max()
H = ymax - ymin
P = pos.copy()
P[:, 1] = (pos[:, 1] - ymin) / H            # 0 ground .. 1 top
P[:, 0] = pos[:, 0] / H                     # width, height units
P[:, 2] = pos[:, 2] / H                     # +front/-back, height units

def classify(p):
    """p: (n,3) normalized -> (n,3) mask RGB in 0..1 (body, accent, third)."""
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    w = np.zeros((len(p), 3))
    if kind == "kitty":
        # zone3 (B): muzzle + chest bib — the white patch of the reference
        muzzle = (z > 0.17) & (y > 0.30) & (y < 0.62) & (np.abs(x) < 0.14)
        chest = (z > 0.05) & (y <= 0.36) & (y > -0.02) & (np.abs(x) < 0.19)
        # zone2 (G): ears (top, off-centre) + tail (rear)
        ears = (y > 0.72) & (np.abs(x) > 0.10) & (z < 0.30)
        tail = z < -0.42
        w[:, 2] = (muzzle | chest).astype(float)
        w[:, 1] = ((ears | tail) & ~(muzzle | chest)).astype(float)
        w[:, 0] = 1.0 - w[:, 1] - w[:, 2]
        # horn stays FIXED silver: carve it out of every zone
        horn = (y > 0.74) & (np.abs(x) < 0.14) & (z > 0.0) & (z < 0.55)
        w[horn] = 0.0
    else:  # birdie
        # zone2 (G): wings (outer x, mid-height) + crest (very top)
        wings = (np.abs(x) > 0.155) & (y > 0.28) & (y < 0.62)
        crest = y > 0.93
        # zone3 (B): belly — front centre of the torso
        belly = (z > 0.10) & (y > 0.22) & (y < 0.55) & (np.abs(x) < 0.16) & ~wings
        w[:, 1] = (wings | crest).astype(float)
        w[:, 2] = belly.astype(float)
        w[:, 0] = np.clip(1.0 - w[:, 1] - w[:, 2], 0.0, 1.0)
        # fixed: feet/legs stay silver, beak stays its baked colour
        feet = y < 0.24
        beak = (z > 0.30) & (y > 0.60)
        w[feet | beak] = 0.0
    return w

mask = np.zeros((SIZE, SIZE, 3))
count = np.zeros((SIZE, SIZE, 1))
uvp = uv.copy()
uvp[:, 0] = np.clip(uvp[:, 0] % 1.0, 0, 1) * (SIZE - 1)
uvp[:, 1] = np.clip(uvp[:, 1] % 1.0, 0, 1) * (SIZE - 1)

zw = classify(P)
for t in idxs:
    a, b, c = uvp[t[0]], uvp[t[1]], uvp[t[2]]
    za, zb, zc = zw[t[0]], zw[t[1]], zw[t[2]]
    x0 = int(max(0, np.floor(min(a[0], b[0], c[0]))))
    x1 = int(min(SIZE - 1, np.ceil(max(a[0], b[0], c[0]))))
    y0 = int(max(0, np.floor(min(a[1], b[1], c[1]))))
    y1 = int(min(SIZE - 1, np.ceil(max(a[1], b[1], c[1]))))
    if x1 <= x0 or y1 <= y0 or (x1 - x0) * (y1 - y0) > 40000:
        continue
    xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    if abs(det) < 1e-9:
        continue
    l0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / det
    l1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / det
    l2 = 1.0 - l0 - l1
    inside = (l0 >= -0.02) & (l1 >= -0.02) & (l2 >= -0.02)
    if not inside.any():
        continue
    val = (l0[..., None] * za + l1[..., None] * zb + l2[..., None] * zc)
    yy, xx = np.nonzero(inside)
    mask[ys[yy, xx], xs[yy, xx]] += val[yy, xx]
    count[ys[yy, xx], xs[yy, xx]] += 1.0

filled = count[..., 0] > 0
mask[filled] /= count[filled]
# dilate into unfilled gutters so bilinear sampling never bleeds black
m8 = (np.clip(mask, 0, 1) * 255).astype(np.uint8)
img = Image.fromarray(m8, "RGB")
from PIL import ImageFilter
grown = img.filter(ImageFilter.MaxFilter(5))
m8 = np.where(filled[..., None], m8, np.array(grown))
Image.fromarray(m8.astype(np.uint8), "RGB").save(out_path)
cov = float(filled.mean()) * 100
print("MASK %s: %.0f%% texels filled -> %s" % (kind, cov, out_path))
zsum = m8.astype(float).sum(axis=(0, 1))
print("zone px weights R(body)=%.0f G(accent)=%.0f B(third)=%.0f" % tuple(zsum / 255))
