#!/usr/bin/env python3
"""Run 6 pose: a side wave whose hand never crosses her hair, face or body.

Takes c1, d1 and e1 smeared the hand wherever it moved across the hair or face. LTX-2.5 packs
8 frames into each latent frame, and a hand moving over busy detail inside one group decodes as
a smudge. Over the plain background the hand stayed readable (e1 frame 20, the hand held at the
top). Run 5 still put the top pose against the hair edge (the revision-2 top), so its rise and
lowering crossed the hair. Run 6 follows the approved keys instead:
  * the hand rises in front-left of her body with the elbow out (K1/K3's idea, but in the picture
    plane at the W3 lengths), reaches a top pose beside her head with the open hand left of the
    hair (K2/K3's idea), waves twice there, and comes back down the same way;
  * every frame keeps the forearm and hand at least CLEAR cell px outside the head, hair and body
    silhouette of K0 (without its arm), and the fingertip inside the 40 px right-shifted canvas;
  * eyes open in every frame. c1, d1 and e1 asked for a blink and LTX shut her eyes for 9 to 27
    frames instead; a2, which did not ask, kept them open.
Timing: rest 0-2, rise 3-13, two waves 13-25, lower 25-35 (the rise reversed), rest 35-40; the rise and
lowering are eased along the fingertip's path length.
The acting (lift, lean, head tilt, counter-swings, hair wave, bob) uses the revision-2 formulas on
this path's own master phase. Same schema as data/rig_pose_rev2.json -> data/rig_pose_run6.json.
Numbers only.

    PILOT_CANVAS_SHIFT_X=40 python -I scripts/animate_run6.py
    PILOT_CANVAS_SHIFT_X=40 python -I scripts/animate_run6.py --run7

--run7 (take g1): take f1 kept the hand outside the hair and the eyes open, but the fastest rise and
lowering frames (f1 frames 9-11 and 28-30, about 20 cell px of fingertip travel per frame) still
smeared the hand. Run 7 keeps the same path and lowers the peak fingertip speed by a third: rise
3-15 and lowering 23-35 (12 frames instead of 10), a cosine-ramped constant-speed profile (3-frame
ramps; peak 1.33x the mean instead of smoothstep's 1.5x), and one gentle wave at the top (15-23)
instead of two. Writes data/rig_pose_run7.json.
"""
import math, sys
import numpy as np, cv2
from PIL import Image
from scipy.interpolate import PchipInterpolator
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

T = 40.0
D = math.radians
CLEAR = 5.0          # cell px between the forearm/hand outline and the body silhouette
HAND_HALF = 6.0      # half width of the open hand, cell px
FORE_HALF = 4.0      # half width of the forearm, cell px
MARGIN_X = 40.0      # minimum fingertip canvas x
# World angles (image y down; 90 = pointing down, 180 = left, 270 = up) of upper arm, forearm and hand.
REST = [math.degrees(ang(K0_ARM['shoulder'], K0_ARM['elbow'])), math.degrees(ang(K0_ARM['elbow'], K0_ARM['wrist'])),
        math.degrees(ang(K0_ARM['wrist'], K0_ARM['tip']))]
KNOTS_U = [0.0, 0.125, 0.25, 0.5, 0.75, 1.0]
# The hand leads upward at the wrist early in the rise so the fingertip stays inside the canvas.
KNOTS = [REST, [108, 170, 200], [118, 210, 232], [150, 240, 248], [185, 252, 254], [210, 255, 256]]
WAVE_FORE, WAVE_HAND = 8.0, 11.0      # degrees either side of the top pose, two cycles


def body_mask():
    """K0 silhouette without the waving arm (cell px), for the clearance check."""
    a = np.array(Image.open(ATLAS).convert('RGBA'))[0:256, 0:256, 3] > 127
    arm = np.zeros((256, 256), np.uint8)
    pts = [K0_ARM[k] for k in ('shoulder', 'elbow', 'wrist', 'tip')]
    for p, q in zip(pts, pts[1:]):
        cv2.line(arm, tuple(int(round(v)) for v in p), tuple(int(round(v)) for v in q), 255, 15)
    m = a & (arm == 0)
    ys = np.arange(256)[:, None]
    m &= ~((ys > 100) & (np.arange(256)[None, :] < 112))       # the rest hand and wrist below the sleeve
    return m


def joints(a):
    S = K0_ARM['shoulder']
    E = (S[0] + CONTRACT['upper_arm'] * math.cos(a[0]), S[1] + CONTRACT['upper_arm'] * math.sin(a[0]))
    W = (E[0] + CONTRACT['forearm'] * math.cos(a[1]), E[1] + CONTRACT['forearm'] * math.sin(a[1]))
    Tp = (W[0] + CONTRACT['hand'] * math.cos(a[2]), W[1] + CONTRACT['hand'] * math.sin(a[2]))
    return S, E, W, Tp


def clearance(a, dist_out):
    """Smallest distance (cell px) from the forearm's outer half and the hand to the body silhouette."""
    S, E, W, Tp = joints(a)
    best = 1e9
    for (p, q, half) in (((E[0] * .5 + W[0] * .5, E[1] * .5 + W[1] * .5), W, FORE_HALF), (W, Tp, HAND_HALF)):
        for t in np.linspace(0, 1, 12):
            x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            xi, yi = int(round(x)), int(round(y))
            d = float(dist_out[yi, xi]) if 0 <= xi < 256 and 0 <= yi < 256 else 99.0
            best = min(best, d - half)
    return best


def tip_canvas_x(a):
    return to_canvas(joints(a)[3])[0]


def trapezoid(ramp, n):
    """Distance share covered after s of n frames: cosine ramps of `ramp` frames, constant speed between."""
    t = np.linspace(0, n, 4001)
    v = np.ones_like(t)
    up = t < ramp; dn = t > n - ramp
    v[up] = 0.5 - 0.5 * np.cos(math.pi * t[up] / ramp)
    v[dn] = 0.5 - 0.5 * np.cos(math.pi * (n - t[dn]) / ramp)
    d = np.r_[0, np.cumsum((v[1:] + v[:-1]) / 2 * np.diff(t))]
    d /= d[-1]
    return lambda s: float(np.interp(s * n, t, d))


def main():
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--run7', action='store_true'); a = ap.parse_args()
    if a.run7:
        rise, top, low, cycles, prof, out, rev = (3, 15), (15, 23), (23, 35), 1, trapezoid(3, 12), 'data/rig_pose_run7.json', 7
    else:
        rise, top, low, cycles, prof, out, rev = (3, 13), (13, 25), (25, 35), 2, (lambda s: s * s * (3 - 2 * s)), 'data/rig_pose_run6.json', 6
    m = body_mask()
    dist_out = cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5)
    path = PchipInterpolator(KNOTS_U, np.radians(np.array(KNOTS)), axis=0)
    # Ease along the fingertip's path length, not the knot parameter, so the hand never flicks: the
    # same 10 frames give a peak fingertip speed of 1.5x the mean instead of a burst at the wrist turn.
    us = np.linspace(0, 1, 2001)
    tips = np.array([joints(path(u))[3] for u in us])
    arc = np.r_[0, np.cumsum(np.hypot(*np.diff(tips, axis=0).T))]
    ease = lambda s: float(np.interp(prof(s) * arc[-1], arc, us))
    arm = np.zeros((41, 3))
    for t in range(41):
        if t <= rise[0]:
            u = 0.0
        elif t <= rise[1]:
            u = ease((t - rise[0]) / (rise[1] - rise[0]))
        elif t <= top[1]:
            u = 1.0
        elif t <= low[1]:
            u = ease((low[1] - t) / (low[1] - low[0]))
        else:
            u = 0.0
        arm[t] = path(u)
        if top[0] < t < top[1]:                          # waves of the forearm and hand, eased in and out
            w = (t - top[0]) / (top[1] - top[0]); env = math.sin(math.pi * w) ** 2; c = 2 * cycles * math.pi * w
            arm[t] += env * np.array([0.0, D(WAVE_FORE) * math.sin(c), D(WAVE_HAND) * math.sin(c - 0.6)])
    arm[0] = arm[40] = np.radians(REST)
    clear = [clearance(a, dist_out) for a in arm]
    tipx = [tip_canvas_x(a) for a in arm]
    moving = [t for t in range(41) if 4 <= t <= 34]
    worst_clear = min(clear[t] for t in moving)
    assert worst_clear >= CLEAR, f'hand within {worst_clear:.1f} px of the body (frame {moving[int(np.argmin([clear[t] for t in moving]))]})'
    assert min(tipx) >= MARGIN_X, f'fingertip at canvas x {min(tipx):.1f}'
    x = np.arange(41, dtype=float)
    K = K0_ARM
    L1, L2 = dist(K['shoulder'], K['elbow']), dist(K['elbow'], K['wrist'])
    wy = K['shoulder'][1] + L1 * np.sin(arm[:, 0]) + L2 * np.sin(arm[:, 1])
    p = np.clip((wy[0] - wy) / (wy[0] - wy.min()), 0, 1)
    lag = lambda k: np.interp(x - k, x, p, left=0.0, right=float(p[-1]))
    wave = lambda amp, ph: amp * np.sin(2 * math.pi * x / T - ph)
    bump = lambda c, s: np.exp(-(x - c) ** 2 / (2 * s * s))
    body = {
        'Torso': 2.2 * lag(1) - 0.9 * bump(4, 1.5) + wave(0.5, -0.8),
        'Head': -4.5 * lag(2) + 1.0 * bump(4, 1.5) + wave(0.6, -1.6),
        'Hair1': 1.5 * lag(3) + wave(2.0, 0.6),
        'Hair2': 2.0 * lag(4) + wave(3.0, 1.3),
        'Hair3': 2.5 * lag(5) + wave(4.0, 2.0),
        'HairL': -2.0 * lag(3) + wave(2.5, 1.0),
        'RUpper': -4.0 * lag(2) + wave(1.0, 0.5),
        'RFore': -3.0 * lag(3) + wave(1.5, 1.2),
        'Tail1': 1.6 * lag(2) + wave(1.2, 0.4),
        'Tail2': 1.2 * lag(3) + wave(2.4, 1.1),
        'Fin': -2.5 * lag(5) + wave(4.5, 1.9)}
    root_dx = wave(0.4, 0.0)
    root_dy = wave(0.9, 0.0) - 1.4 * lag(1) + 0.7 * bump(4, 1.5)
    shrug = -1.5 * p
    frames = []
    for i in range(41):
        frames.append({'index': i, 'hand_drawing': 'open' if p[i] > 0.25 else 'rest', 'eyes': 'open', 'phase': float(p[i]),
                       'arm_world_angles_rad': [float(v) for v in arm[i]],
                       'shoulder_offset_cell': [0.0, float(shrug[i])], 'root_offset_cell': [float(root_dx[i]), float(root_dy[i])],
                       'bone_delta_rad': {k: float(D(v[i])) for k, v in body.items()}})
    un = np.unwrap(arm, axis=0)
    acc = {['upper', 'fore', 'hand'][k]: round(float(np.degrees(np.abs(np.diff(un[:, k], 2)).max())), 1) for k in range(3)}
    spd = {['upper', 'fore', 'hand'][k]: round(float(np.degrees(np.abs(np.diff(un[:, k])).max())), 1) for k in range(3)}
    tip_speed = max(dist(joints(arm[t])[3], joints(arm[t + 1])[3]) for t in range(40))
    save_json(PILOT / out, {
        'revision': rev, 'source': 'authored side-wave path (knots below) + revision-2 acting formulas',
        'units': 'cell px / radians, image y down', 'knots_deg': {'u': KNOTS_U, 'angles': KNOTS},
        'wave_deg': {'forearm': WAVE_FORE, 'hand': WAVE_HAND}, **({'wave_cycles': 1, 'speed_profile': 'cosine-ramped constant speed, 3-frame ramps'} if a.run7 else {}),
        'arm_max_acceleration_deg_per_frame2': acc, 'arm_max_speed_deg_per_frame': spd,
        'fingertip_max_speed_cell_px_per_frame': round(tip_speed, 1),
        'min_clearance_cell_px_frames_4_34': round(worst_clear, 1), 'clearance_cell_px': [round(c, 1) for c in clear],
        'min_fingertip_canvas_x': round(min(tipx), 1),
        'timing': {'rest': [0, rise[0]], 'rise': list(rise), 'wave': list(top), 'lower': list(low), 'rest_end': [low[1], 40]},
        'blink': 'none; eyes open in every frame', 'frames': frames})
    print('clearance min', round(worst_clear, 1), 'cell px | fingertip min canvas x', round(min(tipx), 1),
          '| max accel', acc, '| max speed', spd, '| tip speed', round(tip_speed, 1), 'cell px/frame')


if __name__ == '__main__':
    main()
