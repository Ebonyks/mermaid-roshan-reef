"""Resolve tail-vs-hind-leg weight blends on the kitty rig.

The kitty's tail rests against her hind legs, so the proxy bind blended
tail and leg weights through the contact patch. A smooth blend between two
bones that move APART (tail wraps left, legs fold under) stretches ~8x and
reads as nightmare fuel. Fix: every vert in the conflict gets ALL its weight
on the side whose bone segment it is geometrically closest to.

USAGE: blender -b --python tools/_split_tail_legs.py -- <rig.blend>
"""
import bpy
import sys
import numpy as np

blend = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.open_mainfile(filepath=blend)
mesh = next(o for o in bpy.data.objects if o.type == "MESH")
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
me = mesh.data
n = len(me.vertices)
co = np.empty(n * 3)
me.vertices.foreach_get("co", co)
co = co.reshape(n, 3)

TAIL = ["tail1", "tail2"]
LEGS = ["legU_BL", "legL_BL", "foot_BL", "legU_BR", "legL_BR", "foot_BR"]

segs = {}
for b in arm.data.bones:
    segs[b.name] = (np.array(b.head_local), np.array(b.tail_local))

def seg_dist(p, names):
    best = 1e9
    for nm in names:
        a, bb = segs[nm]
        ab = bb - a
        t = np.clip(np.dot(p - a, ab) / max(np.dot(ab, ab), 1e-9), 0.0, 1.0)
        d = np.linalg.norm(p - (a + t * ab))
        best = min(best, d)
    return best

gi = {g.name: g.index for g in mesh.vertex_groups}
tail_cols = [gi[nm] for nm in TAIL if nm in gi]
leg_cols = [gi[nm] for nm in LEGS if nm in gi]
W = np.zeros((n, len(mesh.vertex_groups)))
for v in me.vertices:
    for g in v.groups:
        W[v.index, g.group] = g.weight

moved = 0
for vi in range(n):
    wt = W[vi, tail_cols].sum()
    wl = W[vi, leg_cols].sum()
    if wt < 0.05 or wl < 0.05:
        continue
    p = co[vi]
    if seg_dist(p, TAIL) < seg_dist(p, LEGS):
        # tail wins: fold the leg share into the tail bones proportionally
        scale = (wt + wl) / max(wt, 1e-9)
        W[vi, tail_cols] *= scale
        W[vi, leg_cols] = 0.0
    else:
        scale = (wt + wl) / max(wl, 1e-9)
        W[vi, leg_cols] *= scale
        W[vi, tail_cols] = 0.0
    moved += 1
W /= np.maximum(W.sum(axis=1, keepdims=True), 1e-6)
print("resolved %d tail/leg conflict verts" % moved)

for g in mesh.vertex_groups:
    for vi in range(n):
        g.remove([vi])
names = [g.name for g in mesh.vertex_groups]
for gname in names:
    g = mesh.vertex_groups[gname]
    col = gi[gname]
    for vi in range(n):
        if W[vi, col] > 0.004:
            g.add([vi], float(W[vi, col]), "REPLACE")
bpy.ops.wm.save_as_mainfile(filepath=blend)
print("SAVED", blend)
