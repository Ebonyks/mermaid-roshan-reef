#!/usr/bin/env python3
"""Solve the tracked LTX motion onto the deterministic rig. Numbers only (no images).

Reads data/take1_tracks.json and writes:
  data/rig_pose.json  per-frame rig pose in the 256 px cell: body bone deltas, arm world angles,
                      shoulder offset, hand drawing, master phase; plus run-2 guide joints (canvas)
The arm is re-posed by two-bone IK at the W3 contract lengths onto the take's wrist and elbow side.
Cleanup is automatic and recorded: one rest -> open -> rest hand schedule chosen by total fit cost,
angle unwrapping, wrist limit +-75 deg, IoU-weighted Gaussian smoothing, exact K0 rest at frames 0 and 40.

    python -I scripts/solve.py
"""
import math, sys
import numpy as np
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

SIGMA = 1.0   # frames


def smooth(v, w=None, sigma=SIGMA):
    v = np.asarray(v, float); w = np.ones_like(v) if w is None else np.asarray(w, float)
    n = len(v); out = np.empty(n); k = np.arange(-3, 4); g = np.exp(-k ** 2 / (2 * sigma ** 2))
    for i in range(n):
        j = np.clip(i + k, 0, n - 1); ww = g * w[j]; out[i] = (ww * v[j]).sum() / ww.sum()
    return out


def ease_to(v, rest, n=3):
    """Blend the first and last n frames to the exact rest value (frames 0 and 40 equal K0)."""
    v = np.array(v, float)
    for i in range(n):
        t = i / n; t = t * t * (3 - 2 * t)
        v[i] = rest + (v[i] - rest) * t; v[-1 - i] = rest + (v[-1 - i] - rest) * t
    return v


def main():
    tr = load_json(PILOT / 'data/take1_tracks.json')['frames']
    n = len(tr)
    # 1. One rest -> open -> rest hand schedule with the lowest total fit cost.
    cr = np.array([f['rig_arm_fit']['per_hand']['rest']['cost'] for f in tr])
    co = np.array([f['rig_arm_fit']['per_hand']['open']['cost'] for f in tr])
    best = None
    for s1 in range(1, n - 1):
        for s2 in range(s1 + 1, n):
            c = cr[:s1].sum() + co[s1:s2].sum() + cr[s2:].sum()
            if best is None or c < best[0]:
                best = (c, s1, s2)
    _, s1, s2 = best
    hand = ['open' if s1 <= i < s2 else 'rest' for i in range(n)]
    sel = [f['rig_arm_fit']['per_hand'][h] for f, h in zip(tr, hand)]
    iou = np.array([s['iou'] for s in sel]); w = np.clip(iou, 0.05, 1) ** 2
    # 2. Re-pose the fixed-length rig arm onto the LTX joints by two-bone IK: the wrist goes to the
    #    take's wrist (clamped to the arm's reach), the elbow bends to the side the take's elbow is on,
    #    the hand keeps the take's direction. Lengths are the W3 contract, so foreshortened or stretched
    #    LTX segments become in-plane poses at one size.
    K = K0_ARM
    rest = [ang(K['shoulder'], K['elbow']), ang(K['elbow'], K['wrist']), ang(K['wrist'], K['tip'])]
    rest_rel = [rest[0], wrap(rest[1] - rest[0]), wrap(rest[2] - rest[1])]
    shrug = np.clip(ease_to(smooth([s['shoulder_offset_canvas'][1] / CELL_SCALE for s in sel], w), 0.0), -2.5, 0.5)
    off = [np.zeros(n), shrug]   # vertical shrug only; the horizontal offset is fit slop against the sleeve
    L1, L2 = CONTRACT['upper_arm'] * CELL_SCALE, CONTRACT['forearm'] * CELL_SCALE
    raw, miss = [], []
    for i, s in enumerate(sel):
        J = s['joints_canvas']; St = tr[i]['rig_arm_fit']['shoulder_torso_canvas']
        S = (St[0], St[1] + shrug[i] * CELL_SCALE); Wt, Ef = J['wrist'], J['elbow']
        d0 = dist(S, Wt); d = min(max(d0, abs(L1 - L2) + 1), L1 + L2 - 0.5)
        u = ang(S, Wt); al = math.acos((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))
        cr_ = (Wt[0] - S[0]) * (Ef[1] - S[1]) - (Wt[1] - S[1]) * (Ef[0] - S[0])
        t1 = u + (al if cr_ >= 0 else -al)
        E = (S[0] + L1 * math.cos(t1), S[1] + L1 * math.sin(t1)); Wr = (S[0] + d * math.cos(u), S[1] + d * math.sin(u))
        t2 = ang(E, Wr); t3 = s['angles_rad'][2]
        raw.append((t1, t2, t3)); miss.append(dist(Wr, Wt) / CELL_SCALE)
    raw = np.array(raw)
    rel = [np.unwrap(raw[:, 0]), np.array([wrap(v) for v in raw[:, 1] - raw[:, 0]]),
           np.clip([wrap(v) for v in raw[:, 2] - raw[:, 1]], -math.radians(75), math.radians(75))]
    rel[0] += 2 * math.pi * round((rest_rel[0] - rel[0][0]) / (2 * math.pi))
    R = [ease_to(smooth(rel[k], w), rest_rel[k]) for k in range(3)]
    A = [R[0], R[0] + R[1], R[0] + R[1] + R[2]]
    # 3. Body from the tracked landmarks (cell units, deltas from frame 0), smoothed, ends eased to rest.
    F = lambda i, k: np.array(to_cell(tr[i]['features_canvas'][k])) if k in tr[i]['features_canvas'] else None
    def series(fn):
        vals = []
        for i in range(n):
            try: vals.append(fn(i))
            except TypeError: vals.append(np.nan)
        v = np.array(vals, float); good = np.isfinite(v)
        v[~good] = np.interp(np.flatnonzero(~good), np.flatnonzero(good), v[good]) if (~good).any() else v[~good]
        return ease_to(smooth(v - v[0]), 0.0)
    da = lambda a, b: (lambda i: ang(F(i, a), F(i, b)))
    body = {
        'root_dx': series(lambda i: F(i, 'waist')[0]), 'root_dy': series(lambda i: F(i, 'waist')[1]),
        'torso': series(da('waist', 'neck')),
        'head': series(lambda i: ang(F(i, 'eyeL'), F(i, 'eyeR')) - ang(F(i, 'waist'), F(i, 'neck'))),
        'hair': series(lambda i: ang(F(i, 'crown'), F(i, 'hair')) - ang(F(i, 'eyeL'), F(i, 'eyeR'))),
        'tail1': series(da('waist', 'tailmid')),
        'tail2': series(lambda i: ang(F(i, 'tailmid'), F(i, 'tailbot')) - ang(F(i, 'waist'), F(i, 'tailmid'))),
        'fin': series(lambda i: ang(F(i, 'tailbot'), F(i, 'fin')) - ang(F(i, 'tailmid'), F(i, 'tailbot')))}
    # 4. Master phase = the solved arm's own elevation (one timing for every run-2 body response).
    Lc = (CONTRACT['upper_arm'] * CELL_SCALE, CONTRACT['forearm'] * CELL_SCALE)
    S0 = to_canvas(K['shoulder'])
    wy = [S0[1] + off[1][i] * CELL_SCALE + Lc[0] * math.sin(A[0][i]) + Lc[1] * math.sin(A[1][i]) for i in range(n)]
    phase = np.clip((wy[0] - np.array(wy)) / (wy[0] - min(wy)), 0, 1)
    frames = []
    for i in range(n):
        frames.append({
            'index': i, 'hand_drawing': hand[i], 'arm_fit_iou': float(iou[i]),
            'ltx_segment_scale_vs_contract': sel[i]['segment_scale_vs_contract'],
            'ik_wrist_miss_cell': float(miss[i]),
            'arm_world_angles_rad': [float(A[k][i]) for k in range(3)],
            'arm_local_angles_rad': [float(R[k][i]) for k in range(3)],
            'shoulder_offset_cell': [float(off[0][i]), float(off[1][i])],
            'body_delta': {k: float(v[i]) for k, v in body.items()}, 'phase': float(phase[i])})
    save_json(PILOT / 'data/rig_pose.json', {
        'source': 'data/take1_tracks.json', 'units': 'cell px / radians, image y down (Godot 2D convention)',
        'hand_schedule': {'open_from': s1, 'rest_from': s2, 'method': 'min total fit cost, one rest-open-rest schedule'},
        'cleanup': {'angle_smoothing_sigma_frames': SIGMA, 'weights': 'IoU^2', 'ends': 'frames 0-2 and 38-40 eased to exact K0 rest',
                    'ik': 'two-bone IK at W3 contract lengths to the take wrist; elbow side from the take; wrist limit +-75 deg',
                    'shoulder_offset': 'vertical shrug only, clamped to -2.5..0.5 cell px'},
        'rest_arm_angles_rad': rest, 'frames': frames})
    print('hand schedule: open %d..%d' % (s1, s2 - 1))
    for f in frames[::4]:
        print(f['index'], f['hand_drawing'], ' '.join('%+7.1f' % math.degrees(a) for a in f['arm_world_angles_rad']),
              'phase %.2f' % f['phase'], 'torso %+.2f' % math.degrees(f['body_delta']['torso']))


if __name__ == '__main__':
    main()
