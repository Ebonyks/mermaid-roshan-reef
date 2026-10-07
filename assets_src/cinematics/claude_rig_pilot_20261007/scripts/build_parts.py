#!/usr/bin/env python3
"""Run 1 (rules off): cut the approved K0/K2 art into rig parts and build skinned meshes.

Writes run1_godot/parts/*.png (256 px cells, positions unchanged) and run1_godot/rig.json:
  body.png       K0 without the waving arm below the sleeve (one skinned mesh: torso/head/hair/tail)
  arm.png        K0 upper arm + forearm, plus a skin cap under the sleeve so rotation opens no gap
  hand_rest.png  K0 relaxed hand          hand_open.png  K2 open hand (scaled to the W3 hand length)
  sleeve.png     K0 left sleeve ruffle, drawn over the arm to hide the shoulder joint
This is the owner-permitted rules-off test (2026-10-07): it deliberately uses part layers.

    python -I scripts/build_parts.py
"""
import math, sys
import numpy as np, cv2
from PIL import Image
from scipy.spatial import Delaunay
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

OUT = PILOT / 'run1_godot'
# Waving-arm region in K0 (below the sleeve, left of the bodice/waistband/tail outlines), cell px.
ARM_POLY = [(104, 105), (115, 104), (117, 102), (121, 104), (124, 105), (124, 121), (123, 125), (121, 129),
            (119, 132), (117, 136), (116, 141), (113, 146), (114, 150), (116, 172), (86, 172), (86, 105)]
# Left sleeve ruffle overlay (covers the shoulder joint and the arm cap at every angle).
SLEEVE_POLY = [(115, 88), (127, 88), (128, 100), (126, 107), (121, 106), (117, 104), (112, 100), (113, 93)]
CAP = ((120.0, 101.5), 4.5)
# Body bones: name, parent, head, tail (cell px). The arm chain hangs off the torso at the K0 shoulder.
BONES = [('Root', None, (135.5, 143.0), (145.5, 143.0)),
         ('Torso', 'Root', (135.5, 143.0), (141.0, 93.0)),
         ('Head', 'Torso', (141.0, 93.0), (145.0, 25.0)),
         ('Hair', 'Head', (168.0, 40.0), (202.0, 100.0)),
         ('UpperArm', 'Torso', K0_ARM['shoulder'], K0_ARM['elbow']),
         ('Fore', 'UpperArm', K0_ARM['elbow'], K0_ARM['wrist']),
         ('Hand', 'Fore', K0_ARM['wrist'], K0_ARM['tip']),
         ('Tail1', 'Root', (135.5, 143.0), (128.0, 190.0)),
         ('Tail2', 'Tail1', (128.0, 190.0), (150.0, 228.0)),
         ('Fin', 'Tail2', (150.0, 228.0), (215.0, 200.0))]


def poly_mask(poly):
    m = np.zeros((256, 256), np.uint8)
    cv2.fillPoly(m, [np.round(np.array(poly) * 8).astype(np.int32)], 1, cv2.LINE_8, 3)
    return m.astype(bool)


def seg_dist(p, a, b):
    p, a, b = np.asarray(p, float), np.asarray(a, float), np.asarray(b, float)
    ab = b - a; t = np.clip(((p - a) @ ab) / (ab @ ab), 0, 1)
    return np.hypot(*(p - (a + t[:, None] * ab)).T)


def mesh(alpha, step=4):
    """Delaunay mesh over an alpha mask: interior grid + resampled contour; drops triangles over gaps."""
    m = (alpha > 0).astype(np.uint8)
    pts = []
    cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        c = c[:, 0, :].astype(float)
        if len(c) < 6: continue
        for k in range(0, len(c), 3): pts.append(c[k] + .5)
    er = cv2.erode(m, np.ones((3, 3), np.uint8))
    for y in range(2, 256, step):
        for x in range(2, 256, step):
            if er[y, x]: pts.append((x + .5, y + .5))
    pts = np.unique(np.round(np.array(pts), 2), axis=0)
    tri = Delaunay(pts).simplices
    dil = cv2.dilate(m, np.ones((3, 3), np.uint8))
    inside = lambda q: dil[int(np.clip(q[1], 0, 255)), int(np.clip(q[0], 0, 255))] > 0
    keep = []
    for t in tri:
        a, b, c = pts[t]
        if all(inside(q) for q in [(a + b + c) / 3, (a + b) / 2, (b + c) / 2, (a + c) / 2]):
            keep.append(t)
    return pts, np.array(keep)


def weights(pts, names):
    """Inverse-distance^4 weights to bone segments with region gates; normalised per vertex."""
    B = {b[0]: b for b in BONES}; W = {}
    for n in names:
        d = seg_dist(pts, B[n][2], B[n][3]); W[n] = 1.0 / (d + 1.5) ** 4
    x, y = pts[:, 0], pts[:, 1]
    if 'Head' in W:
        head_t = np.clip((98 - y) / 8, 0, 1)               # neck blend 90..98
        W['Head'] *= head_t; W['Hair'] *= head_t * np.clip((x - 158) / 14, 0, 1) * (y < 118)
        W['Torso'] *= np.clip((y - 88) / 8, 0, 1) * np.clip((150 - y) / 10, 0, 1)
        for n in ('Tail1', 'Tail2', 'Fin'): W[n] *= np.clip((y - 136) / 10, 0, 1)
        sl = poly_mask(SLEEVE_POLY); near = sl[np.clip(y.astype(int), 0, 255), np.clip(x.astype(int), 0, 255)]
        near |= (np.abs(x - 121) < 10) & (np.abs(y - 101) < 10)
        for n in W: W[n] = np.where(near, 1.0 if n == 'Torso' else 0.0, W[n])
    tot = sum(W.values()); tot[tot == 0] = 1
    W = {n: w / tot for n, w in W.items()}
    # Keep each vertex's three strongest bones (Godot packs four), drop <1%, renormalise.
    M = np.stack([W[n] for n in W], 1); order = np.argsort(-M, 1)
    for i in range(len(M)):
        M[i, order[i, 3:]] = 0
    M[M < 0.01] = 0; M /= np.maximum(M.sum(1, keepdims=True), 1e-9)
    return {n: M[:, k].astype(float) for k, n in enumerate(W)}


def main():
    a = np.array(Image.open(ATLAS).convert('RGBA'))
    k0 = a[0:256, 0:256].copy()
    hands = hand_cells()
    arm_region = poly_mask(ARM_POLY) & (k0[:, :, 3] > 0)
    n, lab, st, _ = cv2.connectedComponentsWithStats(arm_region.astype(np.uint8), connectivity=8)
    arm_region = lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))     # the arm only, no stray hair bits
    hand_rest = hands['rest'][1] & arm_region
    arm = arm_region & ~hand_rest
    sl = poly_mask(SLEEVE_POLY) & (k0[:, :, 3] > 0) & ~arm_region
    body = k0.copy(); body[arm_region | sl] = 0        # sleeve pixels live only in the overlay
    (OUT / 'parts').mkdir(parents=True, exist_ok=True)
    def save(name, rgba): Image.fromarray(rgba).save(OUT / 'parts' / name)
    arm_px = np.zeros_like(k0); arm_px[arm] = k0[arm]
    # Skin cap under the sleeve: fill empty pixels of a disc at the shoulder with the upper arm's skin.
    skin = k0[(arm) & (np.arange(256)[:, None] > 106) & (np.arange(256)[:, None] < 118)]
    skin = skin[skin[:, 3] == 255]; col = np.median(skin[skin[:, :3].sum(1) > 600], axis=0).astype(np.uint8)
    yy, xx = np.mgrid[0:256, 0:256]; (cx, cy), r = CAP
    cap = ((xx + .5 - cx) ** 2 + (yy + .5 - cy) ** 2 <= r * r) & (arm_px[:, :, 3] == 0) & sl & (k0[:, :, 3] == 255)
    arm_px[cap] = col
    save('body.png', body); save('arm.png', arm_px)
    hr = np.zeros_like(k0); hr[hand_rest] = k0[hand_rest]; save('hand_rest.png', hr)
    ho_cell, ho_m = hands['open'][0], hands['open'][1]
    ho = np.zeros_like(ho_cell); ho[ho_m] = ho_cell[ho_m]; save('hand_open.png', ho)
    sp = np.zeros_like(k0); sp[sl] = k0[sl]
    save('sleeve.png', sp)
    # Meshes and weights.
    bpts, btri = mesh(body[:, :, 3]); bw = weights(bpts, ['Torso', 'Head', 'Hair', 'Tail1', 'Tail2', 'Fin'])
    apts, atri = mesh(arm_px[:, :, 3], step=3)
    proj = (apts - np.array(K0_ARM['shoulder'])) @ (np.array(K0_ARM['elbow']) - K0_ARM['shoulder'])
    proj /= dist(K0_ARM['shoulder'], K0_ARM['elbow'])
    t = np.clip((proj - (dist(K0_ARM['shoulder'], K0_ARM['elbow']) - 3)) / 6, 0, 1); t = t * t * (3 - 2 * t)
    aw = {'UpperArm': 1 - t, 'Fore': t}
    w2, t2 = K2_HAND['wrist'], K2_HAND['tip']
    rig = {'cell': 256, 'bones': [{'name': n, 'parent': p, 'head': h, 'tail': tl} for n, p, h, tl in BONES],
           'meshes': [{'name': 'Body', 'texture': 'parts/body.png', 'z': 0, 'vertices': bpts.tolist(),
                       'triangles': btri.tolist(), 'weights': {k: v.tolist() for k, v in bw.items()}},
                      {'name': 'Arm', 'texture': 'parts/arm.png', 'z': 1, 'vertices': apts.tolist(),
                       'triangles': atri.tolist(), 'weights': {k: v.tolist() for k, v in aw.items()}}],
           'sprites': [{'name': 'HandRest', 'texture': 'parts/hand_rest.png', 'bone': 'Hand', 'z': 2,
                        'cell_wrist': K0_ARM['wrist'], 'cell_tip': K0_ARM['tip'], 'scale': 1.0},
                       {'name': 'HandOpen', 'texture': 'parts/hand_open.png', 'bone': 'Hand', 'z': 2,
                        'cell_wrist': w2, 'cell_tip': t2, 'scale': CONTRACT['hand'] / dist(w2, t2)},
                       {'name': 'Sleeve', 'texture': 'parts/sleeve.png', 'bone': 'Torso', 'z': 3,
                        'cell_wrist': None, 'cell_tip': None, 'scale': 1.0}]}
    save_json(OUT / 'rig.json', rig)
    print('body mesh %d verts %d tris; arm mesh %d verts %d tris; cap %d px' % (
        len(bpts), len(btri), len(apts), len(atri), int(cap.sum())))


if __name__ == '__main__':
    main()
