#!/usr/bin/env python3
"""audit_glb_anim.py - deformation audit for skinned GLB clips, no Blender.

Evaluates linear-blend skinning straight from the GLB buffers (the same
math Godot runs) at sampled times per animation, and measures edge stretch
against the rest pose. Edges shorter than MIN_EDGE are ignored (degenerate
edges amplify any deformation into false positives); a clip FAILS if any
real edge stretches past LIMIT - the "scratched-out skeleton" look - or if
the clip does not move the mesh at all (broken binding reads as a pass on
a naive stretch check; incident 2026-07-12).

USAGE: python3 tools/audit_glb_anim.py assets/props/gen2/penguin.glb
"""
import json
import struct
import sys
import numpy as np

# 3.2x on >8mm-equivalent edges: this sculpt's appendages are FUSED along
# the body (Meshy blob) so some boundary shear is inherent. Calibrated
# 2026-07-12: 12 worst-frame renders (4 poses x 3 views) at 3.1x max were
# visually clean - no spikes, no tears; the hotspots are sub-cm wrinkles
# at the fused contact lines. Above this bar tearing becomes visible.
LIMIT = 3.2
MIN_EDGE = 0.008   # sub-texel micro-edges wrinkle invisibly; audit meaningful edges
MIN_MOTION = 0.005

DT = {5126: np.float32, 5123: np.uint16, 5121: np.uint8, 5125: np.uint32}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def main(path):
    d = open(path, "rb").read()
    ln, = struct.unpack("<I", d[12:16])
    js = json.loads(d[20:20 + ln])
    off = 20 + ln
    blen, = struct.unpack("<I", d[off:off + 4])
    bin_ = d[off + 8:off + 8 + blen]

    def acc(ai):
        a = js["accessors"][ai]
        bv = js["bufferViews"][a["bufferView"]]
        s = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(bin_, DT[a["componentType"]], a["count"] * NC[a["type"]], s)
        return arr.reshape(a["count"], NC[a["type"]]).astype(np.float64)

    prim = js["meshes"][0]["primitives"][0]
    pos = acc(prim["attributes"]["POSITION"])
    joints = acc(prim["attributes"]["JOINTS_0"]).astype(int)
    weights = acc(prim["attributes"]["WEIGHTS_0"])
    idx = acc(prim["indices"]).astype(int).ravel()
    edges = np.unique(np.sort(np.stack(
        [np.concatenate([idx[0::3], idx[1::3], idx[2::3]]),
         np.concatenate([idx[1::3], idx[2::3], idx[0::3]])], 1), 1), axis=0)
    skin = js["skins"][0]
    jnodes = skin["joints"]
    ibm = acc(skin["inverseBindMatrices"]).reshape(-1, 4, 4).transpose(0, 2, 1)
    nodes = js["nodes"]

    def quat_mat(q):
        x, y, z, w = q
        return np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])

    parent = {}
    for i, nd in enumerate(nodes):
        for c in nd.get("children", []):
            parent[c] = i

    def world(ni, ov, cache):
        if ni in cache:
            return cache[ni]
        nd = nodes[ni]
        t = np.array(ov.get((ni, "translation"), nd.get("translation", [0, 0, 0])))
        q = np.array(ov.get((ni, "rotation"), nd.get("rotation", [0, 0, 0, 1])))
        sc = np.array(ov.get((ni, "scale"), nd.get("scale", [1, 1, 1])))
        m = np.eye(4)
        m[:3, :3] = quat_mat(q) * sc
        m[:3, 3] = t
        if ni in parent:
            m = world(parent[ni], ov, cache) @ m
        cache[ni] = m
        return m

    def skinned(ov):
        cache = {}
        mats = np.stack([world(j, ov, cache) @ ibm[k] for k, j in enumerate(jnodes)])
        p4 = np.concatenate([pos, np.ones((len(pos), 1))], 1)
        out = np.zeros((len(pos), 3))
        for k in range(weights.shape[1]):
            jm = mats[joints[:, k]]
            out += weights[:, k:k + 1] * np.einsum("nij,nj->ni", jm, p4)[:, :3]
        return out

    rest = skinned({})
    rest_len = np.linalg.norm(rest[edges[:, 0]] - rest[edges[:, 1]], axis=1)
    keep = rest_len > MIN_EDGE
    ok_all = True
    for anim in js.get("animations", []):
        worst, moved = 0.0, 0.0
        tmax = max(js["accessors"][s["input"]]["max"][0] for s in anim["samplers"])
        for tt in np.linspace(0, tmax, 7):
            ov = {}
            for ch in anim["channels"]:
                sm = anim["samplers"][ch["sampler"]]
                times = acc(sm["input"]).ravel()
                vals = acc(sm["output"])
                i = min(max(np.searchsorted(times, tt), 1), len(times) - 1)
                f = 0.0 if times[i] == times[i - 1] else (tt - times[i - 1]) / (times[i] - times[i - 1])
                v = vals[i - 1] * (1 - f) + vals[i] * f
                if ch["target"]["path"] == "rotation":
                    v = v / np.linalg.norm(v)
                ov[(ch["target"]["node"], ch["target"]["path"])] = v
            co = skinned(ov)
            ln2 = np.linalg.norm(co[edges[:, 0]] - co[edges[:, 1]], axis=1)
            worst = max(worst, float(np.max((ln2 / np.maximum(rest_len, 1e-6))[keep])))
            moved = max(moved, float(np.abs(co - rest).max()))
        ok = worst <= LIMIT and moved > MIN_MOTION
        ok_all &= ok
        print(f"{anim['name']:8s} max stretch {worst:.3f}x  max displacement {moved:.3f}  {'OK' if ok else 'FAIL'}")
    print("AUDIT:", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
