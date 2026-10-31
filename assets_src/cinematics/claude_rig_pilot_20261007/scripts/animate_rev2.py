#!/usr/bin/env python3
"""Run 1 revision 2 pose (owner review 2026-10-07: "frozen otherwise", "frame-by-frame artifacts").

Revision 1 copied LTX's own body motion, which is noise-level (torso <= 0.5 deg), and its per-frame arm
solve kept the jumps of the smeared LTX frames. Revision 2 keeps LTX for what it measures well (the arm
path and the timing) and authors everything else on that timing:
  * arm: the revision-1 IK angles through an IoU^4-weighted smoothing spline (lam 5), ends eased to K0
  * one master phase from the arm's elevation drives the acting: anticipation dip, body lift, lean away
    from the raised arm, head tilt toward the hand, shoulder lift, free-arm counter-swing, tail counter-
    swing and follow-through, each with a short overlapping-action lag
  * underwater idle: buoyant bob, tail undulation and a travelling wave through the rainbow hair and the
    left strands (one 40-frame cycle, so the wave flows rather than jitters)
  * one blink while she settles: half lid 33, closed 34-35, half lid 36
Writes data/rig_pose_rev2.json. Numbers only.

    python -I scripts/animate_rev2.py
"""
import math, sys
import numpy as np
from scipy.interpolate import make_smoothing_spline
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

T = 40.0                       # idle cycle (frames)
D = math.radians


def main():
    src = load_json(PILOT / 'data/rig_pose.json'); F = src['frames']; n = len(F); x = np.arange(n, dtype=float)
    w = np.array([f['arm_fit_iou'] for f in F]) ** 4
    R = np.array([f['arm_local_angles_rad'] for f in F])
    K = K0_ARM
    rest = [ang(K['shoulder'], K['elbow']), wrap(ang(K['elbow'], K['wrist']) - ang(K['shoulder'], K['elbow'])),
            wrap(ang(K['wrist'], K['tip']) - ang(K['elbow'], K['wrist']))]
    arm = []
    for k in range(3):
        v = make_smoothing_spline(x, R[:, k], w=w / w.mean(), lam=5.0)(x)
        e = np.ones(n)                                   # ease the first/last 3 frames onto K0 rest
        for i in range(3):
            t = i / 3; t = t * t * (3 - 2 * t); e[i] = t; e[-1 - i] = t
        arm.append(rest[k] + (v - rest[k]) * e)
    A = [arm[0], arm[0] + arm[1], arm[0] + arm[1] + arm[2]]
    # Master phase: wrist elevation of the K0-length arm, 0 at rest, 1 at the top of the wave.
    L1, L2 = dist(K['shoulder'], K['elbow']), dist(K['elbow'], K['wrist'])
    wy = K['shoulder'][1] + L1 * np.sin(A[0]) + L2 * np.sin(A[1])
    p = np.clip((wy[0] - wy) / (wy[0] - wy.min()), 0, 1)
    lag = lambda k: np.interp(x - k, x, p, left=0.0, right=float(p[-1]))
    wave = lambda amp, ph: amp * np.sin(2 * math.pi * x / T - ph)
    bump = lambda c, s: np.exp(-(x - c) ** 2 / (2 * s * s))
    body = {   # degrees, relative to each bone's parent; + is clockwise on screen (y down)
        'Torso': 2.2 * lag(1) - 0.9 * bump(4, 1.5) + wave(0.5, -0.8),        # lean away from the raised arm
        'Head': -4.5 * lag(2) + 1.0 * bump(4, 1.5) + wave(0.6, -1.6),        # tilt toward the waving hand
        'Hair1': 1.5 * lag(3) + wave(2.0, 0.6),
        'Hair2': 2.0 * lag(4) + wave(3.0, 1.3),
        'Hair3': 2.5 * lag(5) + wave(4.0, 2.0),
        'HairL': -2.0 * lag(3) + wave(2.5, 1.0),
        'RUpper': -4.0 * lag(2) + wave(1.0, 0.5),                           # free arm swings out to balance
        'RFore': -3.0 * lag(3) + wave(1.5, 1.2),
        'Tail1': 1.6 * lag(2) + wave(1.2, 0.4),                             # tail counter-swing ...
        'Tail2': 1.2 * lag(3) + wave(2.4, 1.1),
        'Fin': -2.5 * lag(5) + wave(4.5, 1.9)}                              # ... and fin follow-through
    root_dx = wave(0.4, 0.0)
    root_dy = wave(0.9, 0.0) - 1.4 * lag(1) + 0.7 * bump(4, 1.5)          # buoyant bob, lift, anticipation dip
    shrug = -1.5 * p                                                       # waving shoulder lifts with the arm
    eyes = {33: 'half', 34: 'closed', 35: 'closed', 36: 'half'}
    hand = [f['hand_drawing'] for f in F]
    frames = []
    for i in range(n):
        frames.append({'index': i, 'hand_drawing': hand[i], 'eyes': eyes.get(i, 'open'), 'phase': float(p[i]),
                       'arm_world_angles_rad': [float(A[k][i]) for k in range(3)],
                       'arm_local_angles_rad': [float(arm[k][i]) for k in range(3)],
                       'shoulder_offset_cell': [0.0, float(shrug[i])],
                       'root_offset_cell': [float(root_dx[i]), float(root_dy[i])],
                       'bone_delta_rad': {k: float(D(v[i])) for k, v in body.items()}})
    acc = {['upper', 'elbow', 'wrist'][k]: round(float(np.degrees(np.abs(np.diff(arm[k], 2)).max())), 1) for k in range(3)}
    save_json(PILOT / 'data/rig_pose_rev2.json', {
        'revision': 2, 'source': 'data/rig_pose.json (revision-1 IK solve of LTX Union take 1)',
        'units': 'cell px / radians, image y down (Godot 2D convention)',
        'arm': 'IoU^4-weighted smoothing spline (scipy make_smoothing_spline, lam 5) on the IK angles; frames 0-2 and 38-40 eased to K0',
        'arm_max_acceleration_deg_per_frame2': acc,
        'acting': 'authored on one master phase (wrist elevation) with 1-5 frame overlapping-action lags; idle cycle 40 frames',
        'blink': 'half 33, closed 34-35, half 36 (painted overlays on K0 eyes)', 'frames': frames})
    print('arm max acceleration deg/frame^2', acc, '| phase peak frame', int(np.argmax(p)))


if __name__ == '__main__':
    main()
