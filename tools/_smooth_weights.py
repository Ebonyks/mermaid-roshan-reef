"""Post-bind weight repair for proxy-bound rigs (the penguin lessons applied
to build_chuck_rig output).

The 3-NN proxy transfer leaves two defects that read as nightmare-fuel
deformation: HARD WEIGHT CLIFFS between adjacent verts (tail vs hind leg:
42x edge stretch) and THIN/DISCONNECTED features sampled to the wrong bone
(whiskers picking up leg weights, then flying when the head turns).

Pass 1: Laplacian-smooth all weights on the welded edge graph (N iters).
Pass 2: every small disconnected shell (<min_verts) copies the weights of
        the nearest big-shell vertex — whiskers ride the face rigidly.

USAGE:
  blender -b --python tools/_smooth_weights.py -- <rig.blend> [iters=20] [min_verts=250]
"""
import bpy
import sys
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
blend = argv[0]
iters = 20
min_verts = 250
for a in argv[1:]:
    if a.startswith("iters="):
        iters = int(a.split("=")[1])
    if a.startswith("min_verts="):
        min_verts = int(a.split("=")[1])

bpy.ops.wm.open_mainfile(filepath=blend)
mesh = next(o for o in bpy.data.objects if o.type == "MESH")
me = mesh.data
n = len(me.vertices)
co = np.empty(n * 3)
me.vertices.foreach_get("co", co)
co = co.reshape(n, 3)

groups = [g.name for g in mesh.vertex_groups]
gi = {g.name: g.index for g in mesh.vertex_groups}
W = np.zeros((n, len(groups)))
for v in me.vertices:
    for g in v.groups:
        W[v.index, g.group] = g.weight

# weld map: coincident UV twins share weights
keys = {}
weld = np.empty(n, dtype=np.int64)
for vi in range(n):
    kk = (round(co[vi, 0] * 500), round(co[vi, 1] * 500), round(co[vi, 2] * 500))
    weld[vi] = keys.setdefault(kk, len(keys))
nw = len(keys)

ne = len(me.edges)
ev = np.empty(ne * 2, dtype=np.int64)
me.edges.foreach_get("vertices", ev)
gev = weld[ev.reshape(-1, 2)]
deg = np.zeros(nw)
np.add.at(deg, gev[:, 0], 1.0)
np.add.at(deg, gev[:, 1], 1.0)

# ---- pass 1: Laplacian smoothing on the welded graph ----
GW = np.zeros((nw, W.shape[1]))
GC = np.zeros(nw)
np.add.at(GW, weld, W)
np.add.at(GC, weld, 1.0)
GW /= np.maximum(GC[:, None], 1.0)
for _ in range(iters):
    acc = np.zeros_like(GW)
    np.add.at(acc, gev[:, 0], GW[gev[:, 1]])
    np.add.at(acc, gev[:, 1], GW[gev[:, 0]])
    GW = 0.5 * GW + 0.5 * acc / np.maximum(deg[:, None], 1.0)
    GW /= np.maximum(GW.sum(axis=1, keepdims=True), 1e-6)

# ---- pass 2: rigid-attach small disconnected shells ----
parent = np.arange(nw)
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a
for e0, e1 in gev:
    r0, r1 = find(e0), find(e1)
    if r0 != r1:
        parent[r0] = r1
roots = np.array([find(i) for i in range(nw)])
sizes = np.bincount(roots, minlength=nw)
big = sizes[roots] >= min_verts
gco = np.zeros((nw, 3))
np.add.at(gco, weld, co)
gco /= np.maximum(GC[:, None], 1.0)
big_idx = np.nonzero(big)[0]
small_idx = np.nonzero(~big)[0]
reattached = 0
if len(small_idx) and len(big_idx):
    bigpts = gco[big_idx]
    # per small shell, one donor point (its centroid's nearest big vert) so
    # the whole filament rides one region rigidly instead of striping
    for r in np.unique(roots[small_idx]):
        members = np.nonzero(roots == r)[0]
        cen = gco[members].mean(axis=0)
        bi = int(np.argmin(((bigpts - cen) ** 2).sum(axis=1)))
        GW[members] = GW[big_idx[bi]]
        reattached += len(members)
W2 = GW[weld]
print("smoothed %d iters; reattached %d weld-verts across %d small shells"
      % (iters, reattached, len(np.unique(roots[small_idx])) if len(small_idx) else 0))

for g in mesh.vertex_groups:
    for vi in range(n):
        g.remove([vi])
for gname in groups:
    g = mesh.vertex_groups[gname]
    col = gi[gname]
    for vi in range(n):
        if W2[vi, col] > 0.004:
            g.add([vi], float(W2[vi, col]), "REPLACE")

bpy.ops.wm.save_as_mainfile(filepath=blend)
print("SAVED", blend)
