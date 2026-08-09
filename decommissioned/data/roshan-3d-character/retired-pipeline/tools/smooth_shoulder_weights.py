#!/usr/bin/env python3
"""Smooth the torso<->upper-arm skin-weight transition on roshan_v4.glb.

Root cause of the visible shoulder stretching (human review 2026-07-18):
shoulder-crease vertices carry jagged chest/armU weight splits, so adjacent
vertices move very differently when the arm raises -> sheet stretching at the
crease on every arm verb (wave 0.073, cheer 0.060 edge opening).

Fix: harmonic (Laplace) re-solve of the arm-fraction field over the crease
band, per side. Only vertices that are >=92% owned by {root,spine1,chest} +
{armU} and not forearm/hand-influenced are touched. Hair, tail, head, elbow,
forearm, hand weights and all geometry/joints are untouched. Rest pose is
invariant to weight changes, so the still look is identical.

Usage: fix_shoulder_weights.py in.glb out.glb [--iters 120]
"""
import json, struct, sys, shutil
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
ITERS = int(sys.argv[sys.argv.index("--iters")+1]) if "--iters" in sys.argv else 120

data = bytearray(open(src, "rb").read())
clen, _ = struct.unpack_from("<II", data, 12)
gltf = json.loads(bytes(data[20:20+clen]))
off = 20 + clen
blen, _ = struct.unpack_from("<II", data, off)
bin_off = off + 8

def acc_info(idx):
    acc = gltf["accessors"][idx]
    bv = gltf["bufferViews"][acc["bufferView"]]
    start = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
    dt = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}[acc["componentType"]]
    n = {"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4}[acc["type"]]
    return start, dt, n, acc["count"], acc.get("normalized", False)

def acc_np(idx):
    start, dt, n, cnt, norm = acc_info(idx)
    a = np.frombuffer(bytes(data[bin_off+start:bin_off+start+cnt*n*np.dtype(dt).itemsize]), dtype=dt).reshape(cnt, n)
    return a

prims = gltf["meshes"][0]["primitives"]
skin = gltf["skins"][0]
joints = skin["joints"]
nodes = gltf["nodes"]
jname = {k: nodes[j].get("name") for k, j in enumerate(joints)}
name2k = {v: k for k, v in jname.items()}

counts = [gltf["accessors"][p["attributes"]["POSITION"]]["count"] for p in prims]
offs = np.cumsum([0] + counts[:-1])
P = np.concatenate([acc_np(p["attributes"]["POSITION"]).astype(np.float64) for p in prims])
J = np.concatenate([acc_np(p["attributes"]["JOINTS_0"]).astype(int) for p in prims])
W_raw = [acc_np(p["attributes"]["WEIGHTS_0"]) for p in prims]
W = np.concatenate([w.astype(np.float64) for w in W_raw])
Wn = W / np.maximum(W.sum(1, keepdims=True), 1e-9)
IDX = np.concatenate([acc_np(p["indices"]).astype(np.int64).reshape(-1,3) + offs[i] for i,p in enumerate(prims)])

def slot_w(names):
    ks = [name2k[n] for n in names if n in name2k]
    w = np.zeros(len(P))
    for c in range(4):
        w += np.where(np.isin(J[:,c], ks), Wn[:,c], 0)
    return w

TORSO = ["root", "spine1", "chest"]
torso = slot_w(TORSO)

edges = np.unique(np.sort(np.concatenate([IDX[:,[0,1]],IDX[:,[1,2]],IDX[:,[0,2]]]),1), axis=0)
nbr = {}
for a,b in edges:
    nbr.setdefault(a,[]).append(b); nbr.setdefault(b,[]).append(a)

report = {}
for side, (uarm, farm, hand) in {"L": ("armU","armF","hand"), "R": ("armU2","armF2","hand2")}.items():
    a = slot_w([uarm])
    fh = slot_w([farm, hand])
    tot = a + torso
    band = (tot >= 0.92) & (a > 0.02) & (a < 0.98) & (fh < 0.10)
    fixed = (tot >= 0.92) & ~band                     # pure-torso / pure-arm anchors
    s = np.where(tot > 1e-9, a/np.maximum(tot,1e-9), 0.0)
    region = band.copy()
    for v in np.flatnonzero(band):                    # include 1-ring anchors
        for u in nbr.get(v, []):
            if fixed[u]: region[u] = True
    s2 = s.copy()
    interior = np.flatnonzero(band)
    nb_list = [np.array([u for u in nbr.get(v,[]) if region[u]], dtype=int) for v in interior]
    for _ in range(ITERS):
        new = s2.copy()
        for i, v in enumerate(interior):
            ns_ = nb_list[i]
            if len(ns_): new[v] = s2[ns_].mean()
        s2 = new
    # rebuild weights: same bone sets, arm share = s2*tot, torso share = (1-s2)*tot
    changed = interior
    for v in changed:
        av, tv = a[v], torso[v]
        av2, tv2 = s2[v]*tot[v], (1-s2[v])*tot[v]
        for c in range(4):
            bone = jname.get(int(J[v,c]))
            if bone == uarm and av > 1e-9:
                Wn[v,c] *= av2/av
            elif bone in TORSO and tv > 1e-9:
                Wn[v,c] *= tv2/tv
    report[side] = (len(interior), float(np.abs(s2[interior]-s[interior]).max()))

# renormalize touched rows exactly
Wn = Wn / np.maximum(Wn.sum(1, keepdims=True), 1e-9)

# write back per primitive, preserving dtype/normalization
pos = 0
for i, p in enumerate(prims):
    idx = p["attributes"]["WEIGHTS_0"]
    start, dt, n, cnt, norm = acc_info(idx)
    seg = Wn[pos:pos+cnt]
    if dt == np.float32:
        out = seg.astype(np.float32)
    else:
        mx = np.iinfo(dt).max
        out = np.round(seg*mx).astype(dt)
    data[bin_off+start:bin_off+start+cnt*n*np.dtype(dt).itemsize] = out.tobytes()
    pos += cnt

open(dst, "wb").write(bytes(data))
for side,(nv,ds) in report.items():
    print(f"side {side}: smoothed {nv} crease verts, max s-shift {ds:.3f}")
print(f"wrote {dst}")
