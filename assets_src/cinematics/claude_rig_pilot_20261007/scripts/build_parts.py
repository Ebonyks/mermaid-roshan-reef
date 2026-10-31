#!/usr/bin/env python3
"""Run 1 (rules off): cut the approved K0/K2 art into rig parts and build skinned meshes.

Writes run1_godot/parts/*.png (256 px cells, positions unchanged) and run1_godot/rig.json:
  body.png       K0 without the waving arm below the sleeve (one skinned mesh: torso/head/hair/tail)
  arm.png        K0 upper arm + forearm, plus a skin cap under the sleeve so rotation opens no gap
  hand_rest.png  K0 relaxed hand          hand_open.png  K2 open hand (scaled to the W3 hand length)
  sleeve.png     K0 left sleeve ruffle, drawn over the arm to hide the shoulder joint
  eyes_half.png, eyes_closed.png
                 revision 2 blink overlays painted on K0's own eyes (inpainted lids plus a lash line in
                 K0's lash colour); no approved front-facing closed-eye drawing exists to reuse
Revision 2 adds a three-bone rainbow-hair chain, a left hair bone and a free-arm chain to the body mesh.
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
CAP = ((120.5, 99.5), 4.5)
# Shoulder pivot sits inside the sleeve, so the arm's top never swings out from under it.
PIVOT = (120.5, 99.5)
EYES = [(130.5, 63.0), (153.5, 63.0)]          # K0 eye centres (cell px)
# Rainbow hair (hangs free over the right shoulder; the sleeve ruffle below it stays on the torso).
RAINBOW_POLY = [(164, 28), (186, 26), (206, 42), (213, 68), (209, 96), (202, 114), (186, 114), (181, 99),
                (178, 88), (171, 70), (166, 52)]
LASH = (84, 38, 26)                            # K0 upper-lash brown
# Body bones: name, parent, head, tail (cell px). The arm chain hangs off the torso at the K0 shoulder.
BONES = [('Root', None, (135.5, 143.0), (145.5, 143.0)),
         ('Torso', 'Root', (135.5, 143.0), (141.0, 93.0)),
         ('Head', 'Torso', (141.0, 93.0), (145.0, 25.0)),
         ('Hair1', 'Head', (168.0, 36.0), (190.0, 55.0)),
         ('Hair2', 'Hair1', (190.0, 55.0), (201.0, 78.0)),
         ('Hair3', 'Hair2', (201.0, 78.0), (197.0, 102.0)),
         ('HairL', 'Head', (114.0, 42.0), (104.0, 92.0)),
         ('RUpper', 'Torso', (160.0, 103.0), (165.0, 127.0)),
         ('RFore', 'RUpper', (165.0, 127.0), (177.0, 150.0)),
         ('UpperArm', 'Torso', PIVOT, K0_ARM['elbow']),
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
        ramp = lambda v, a, b: np.clip((v - a) / (b - a), 0, 1)
        head_t = ramp(-y, -98, -90)                                     # neck blend 90..98
        face = (x > 117) & (x < 168) & (y > 38) & (y < 92)              # the face never bends
        rb = poly_mask(RAINBOW_POLY).astype(np.uint8)
        inside = cv2.distanceTransform(rb, cv2.DIST_L2, 3)
        hair = np.clip(inside[np.clip(y.astype(int), 0, 255), np.clip(x.astype(int), 0, 255)] / 3.0, 0, 1) * ~face
        for n in ('Hair1', 'Hair2', 'Hair3'): W[n] *= hair
        for n in ('Head', 'Torso'): W[n] *= (1 - hair)
        W['HairL'] *= ramp(-x, -119, -113) * ramp(y, 36, 42) * ramp(-y, -95, -89) * ~face
        W['Head'] *= head_t
        rarm = ramp(x, 156.5, 159.5) * ramp(y, 104, 110) * (y < 174) * (x < 196)
        rarm = rarm * np.where(y > 134, ramp(x, 159, 162), 1)
        for n in ('RUpper', 'RFore'): W[n] *= rarm
        W['Torso'] *= ramp(y, 88, 96) * ramp(-y, -150, -140) * (1 - rarm)
        for n in ('Tail1', 'Tail2', 'Fin'): W[n] *= ramp(y, 136, 146) * (1 - rarm)
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


def paint_blink(k0):
    """Half-lid and closed-eye overlays on K0's own eyes. The covered eye is refilled with K0's own skin:
    per row, the median of skin-coloured pixels beside the eye (hair and lashes excluded), smoothed
    vertically. The lid line is drawn 8x supersampled and area-downsampled in K0's lash colour."""
    rgb = k0[:, :, :3].astype(float); yy, xx = np.mgrid[0:256, 0:256] + .5
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    skinlike = (R > 225) & (G > 175) & (B > 145) & (R - B < 95) & (k0[:, :, 3] == 255)
    out = {}
    for name in ('half', 'closed'):
        cover = np.zeros((256, 256), bool); lines = []; fill = rgb.copy()
        for cx, cy in EYES:
            u = (xx - cx) / 6.4; ell = u ** 2 + ((yy - 63.0) / 6.2) ** 2 <= 1
            band = skinlike & ~ell & (np.abs(xx - cx) < 11)
            rows = {}
            for y in range(52, 75):
                m = band & (np.abs(yy - (y + .5)) <= 1.5)
                if m.sum() >= 4: rows[y] = np.median(rgb[m], axis=0)
            ys = np.array(sorted(rows)); cols = np.array([rows[y] for y in ys])
            prof = np.stack([np.convolve(np.interp(np.arange(256), ys, cols[:, c]), np.ones(3) / 3, 'same') for c in range(3)], 1)
            # Lash and lower-lid fragments just outside the ellipse join the cover (hair stays: x limit).
            lum = rgb @ np.array([.299, .587, .114])
            frag = (lum < 170) & (np.abs(xx - cx) <= 6.8) & (((xx - cx) / 7.6) ** 2 + ((yy - 63.0) / 7.6) ** 2 <= 1)
            if name == 'closed':
                c_ = ell | frag
                lines.append([(cx + 5.9 * t, 64.4 + 1.4 * (1 - t * t)) for t in np.linspace(-1, 1, 25)])
            else:
                lid = 61.8 + 0.8 * (1 - u ** 2); c_ = (ell | frag) & (yy <= lid + .3)
                lines.append([(cx + 6.2 * t, 61.8 + 0.8 * (1 - t * t)) for t in np.linspace(-1, 1, 25)])
            fill[c_] = prof[(yy[c_] - .5).astype(int)]
            cover |= c_
            outer = -1 if cx < 140 else 1                                     # lash flick at the outer corner
            ex, ey = lines[-1][0 if outer < 0 else -1]
            lines.append([(ex, ey), (ex + 1.7 * outer, ey - 1.5)])
        big = np.zeros((2048, 2048), np.uint8)
        for ln in lines:
            pts = np.round(np.array(ln) * 8 * 16).astype(np.int32)
            cv2.polylines(big, [pts], False, 255, 11 if name == 'closed' else 12, cv2.LINE_AA, 4)
        a = cv2.resize(big, (256, 256), interpolation=cv2.INTER_AREA).astype(float)[..., None] / 255
        col = fill * (1 - a) + np.array(LASH) * a
        reach = cover | (a[..., 0] > 0.02)
        ov = np.zeros((256, 256, 4), np.uint8); ov[reach, :3] = np.round(col[reach]).astype(np.uint8); ov[reach, 3] = 255
        out[name] = ov
    return out


def main():
    a = np.array(Image.open(ATLAS).convert('RGBA'))
    k0 = a[0:256, 0:256].copy()
    hands = hand_cells()
    arm_region = poly_mask(ARM_POLY) & (k0[:, :, 3] > 0)
    n, lab, st, _ = cv2.connectedComponentsWithStats(arm_region.astype(np.uint8), connectivity=8)
    arm_region = lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))     # the arm only, no stray hair bits
    hand_rest = hands['rest'][1] & arm_region
    arm = arm_region & ~hand_rest
    hsv = cv2.cvtColor(np.ascontiguousarray(k0[:, :, :3]), cv2.COLOR_RGB2HSV)
    hairlike = (hsv[:, :, 0] >= 5) & (hsv[:, :, 0] <= 28) & (hsv[:, :, 1] >= 90)     # brown/golden hair (OpenCV hue)
    sl = poly_mask(SLEEVE_POLY) & (k0[:, :, 3] > 0) & ~arm_region & ~hairlike          # hair stays in the skinned body
    body = k0.copy(); body[arm_region | sl] = 0        # sleeve pixels live only in the overlay
    # Revision 2: the arm used to hide the bodice's left contour and the sleeve hem. Close both with
    # K0's own outline colour where they border the removed arm, and drop stray specks from the body.
    lum = k0[:, :, :3] @ np.array([.299, .587, .114])
    edge_px = k0[118:122, 123:126].reshape(-1, 4); outline = np.median(edge_px[np.argsort(edge_px[:, :3].sum(1))[:4]], axis=0).astype(np.uint8)
    ring = cv2.dilate(arm_region.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~arm_region
    body_edge = ring & (body[:, :, 3] >= 200) & ~hairlike & (np.arange(256)[:, None] <= 135)   # bodice + waistband only
    body[body_edge] = outline
    n_, lab_, st_, _ = cv2.connectedComponentsWithStats((body[:, :, 3] > 0).astype(np.uint8), connectivity=8)
    for c in range(1, n_):
        if st_[c, cv2.CC_STAT_AREA] < 8: body[lab_ == c] = 0
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
    hem = ring & sl; sp[hem] = outline                 # sleeve hem outline where it meets the arm
    save('sleeve.png', sp)
    for name, ov in paint_blink(k0).items():
        save(f'eyes_{name}.png', ov)
    # Meshes and weights.
    bpts, btri = mesh(body[:, :, 3], step=3)
    bw = weights(bpts, ['Torso', 'Head', 'Hair1', 'Hair2', 'Hair3', 'HairL', 'RUpper', 'RFore', 'Tail1', 'Tail2', 'Fin'])
    apts, atri = mesh(arm_px[:, :, 3], step=3)
    proj = (apts - np.array(K0_ARM['shoulder'])) @ (np.array(K0_ARM['elbow']) - K0_ARM['shoulder'])
    proj /= dist(K0_ARM['shoulder'], K0_ARM['elbow'])
    t = np.clip((proj - (dist(K0_ARM['shoulder'], K0_ARM['elbow']) - 3)) / 6, 0, 1); t = t * t * (3 - 2 * t)
    aw = {'UpperArm': 1 - t, 'Fore': t}
    w2, t2 = K2_HAND['wrist'], K2_HAND['tip']
    rig = {'cell': 256, 'bones': [{'name': n, 'parent': p, 'head': h, 'tail': tl} for n, p, h, tl in BONES],
           'meshes': [{'name': 'Body', 'texture': 'parts/body.png', 'z': 0, 'vertices': bpts.tolist(),
                       'triangles': btri.tolist(), 'weights': {k: v.tolist() for k, v in bw.items()}},
                      {'name': 'Arm', 'texture': 'parts/arm.png', 'z': 2, 'vertices': apts.tolist(),
                       'triangles': atri.tolist(), 'weights': {k: v.tolist() for k, v in aw.items()}}],
           'sprites': [{'name': 'EyesHalf', 'texture': 'parts/eyes_half.png', 'bone': 'Head', 'z': 1,
                        'cell_wrist': None, 'cell_tip': None, 'scale': 1.0},
                       {'name': 'EyesClosed', 'texture': 'parts/eyes_closed.png', 'bone': 'Head', 'z': 1,
                        'cell_wrist': None, 'cell_tip': None, 'scale': 1.0},
                       {'name': 'HandRest', 'texture': 'parts/hand_rest.png', 'bone': 'Hand', 'z': 3,
                        'cell_wrist': K0_ARM['wrist'], 'cell_tip': K0_ARM['tip'], 'scale': 1.0},
                       {'name': 'HandOpen', 'texture': 'parts/hand_open.png', 'bone': 'Hand', 'z': 3,
                        'cell_wrist': w2, 'cell_tip': t2, 'scale': CONTRACT['hand'] / dist(w2, t2)},
                       {'name': 'Sleeve', 'texture': 'parts/sleeve.png', 'bone': 'Torso', 'z': 4,
                        'cell_wrist': None, 'cell_tip': None, 'scale': 1.0}]}
    save_json(OUT / 'rig.json', rig)
    print('body mesh %d verts %d tris; arm mesh %d verts %d tris; cap %d px; contour px body %d hem %d' % (
        len(bpts), len(btri), len(apts), len(atri), int(cap.sum()), int(body_edge.sum()), int(hem.sum())))


if __name__ == '__main__':
    main()
