#!/usr/bin/env python3
"""Run 5 pose: the hand goes up and comes back down at her side, and waves at the top.

Takes a2, c1 and d2 all smeared the hand at frames 24-30, where the revision-2 path brings the hand
down in front of the hair, face and shoulder at its fastest. LTX-2.5 encodes 8 frames per latent
frame, so a hand that crosses a busy background quickly inside one 8-frame group comes out as a
smudge; the rising half, which travels out to the side over the plain background, stayed readable.
So the arm path is rebuilt from the readable half:
  * rest 0-3;
  * rise 3-15: the revision-2 rise (frames 3-16), resampled;
  * wave 15-24: the top pose with two small side-to-side waves of the forearm and hand;
  * lower 24-35: the rise played backwards, so the hand returns outward at her side;
  * rest 35-40, so the 5-frame follow-through settles by frame 40; quick blink half 35, closed 36, half 37.
The acting (lift, lean, head tilt, counter-swings, hair wave, bob) uses the revision-2 formulas on
this path's own master phase. Same schema as data/rig_pose_rev2.json -> data/rig_pose_run5.json.
Numbers only.

    PILOT_CANVAS_SHIFT_X=40 python -I scripts/animate_run5.py
The figure sits 40 canvas px further right in run 5 (opening image and guides shifted), because the
rig arm at the W3 lengths reaches 7 px from the left canvas edge on the outward swing.
"""
import math, sys
import numpy as np
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

T = 40.0
D = math.radians


def resample(seq, a, b, n):
    """n samples of seq over the fractional index range [a, b] (linear, per angle channel, unwrapped)."""
    x = np.linspace(a, b, n); idx = np.arange(len(seq))
    return np.stack([np.interp(x, idx, np.unwrap(seq[:, k])) for k in range(seq.shape[1])], 1)


def main():
    src = load_json(PILOT / 'data/rig_pose_rev2.json')['frames']
    A = np.array([f['arm_world_angles_rad'] for f in src])          # world angles: upper arm, forearm, hand
    rest = A[0]
    rise = resample(A, 3, 16, 13)                                     # frames 3..15
    top = rise[-1]                                                    # the rise's last pose, so the joins are continuous
    arm = np.zeros((41, 3))
    arm[0:4] = rest
    arm[3:16] = rise
    for t in range(15, 25):                                           # two waves at the top, eased in and out
        u = (t - 15) / 9; env = math.sin(math.pi * u) ** 2
        arm[t] = top + env * np.array([0.0, D(9) * math.sin(4 * math.pi * u), D(14) * math.sin(4 * math.pi * u - 0.6)])
    arm[24:36] = resample(A, 3, 16, 12)[::-1]                         # back down the same outward path, frames 24..35
    arm[35:] = rest
    # Light smoothing at the joins (3-tap, keeps the end frames exact).
    sm = arm.copy()
    for t in range(1, 40):
        sm[t] = 0.25 * arm[t - 1] + 0.5 * arm[t] + 0.25 * arm[t + 1]
    sm[0] = sm[40] = rest; arm = sm
    # Keep the hand inside the 640 px canvas with a margin: where the outward swing would put the fingertip
    # left of canvas x 50 (cell x 83), turn the forearm and hand up by the smallest angle that clears it
    # (smoothed over time, never down). The revision-2 rise reached canvas x 7-11 at frames 4 and 34.
    sh = to_canvas(K0_ARM["shoulder"])
    def tip_x(a):
        r = (CONTRACT['upper_arm'] * math.cos(a[0]) + CONTRACT['forearm'] * math.cos(a[1]) + CONTRACT['hand'] * math.cos(a[2])) * CELL_SCALE
        return sh[0] + r
    def turn(t, dd):
        return arm[t] + np.array([0, dd, dd * 1.15])
    need = np.zeros(41)
    for t in range(41):           # smallest signed turn (toward vertical either way) that clears the margin
        if tip_x(arm[t]) >= 50:
            continue
        for mag in np.arange(D(0.5), D(90), D(0.5)):
            ok = [sg * mag for sg in (-1, 1) if tip_x(turn(t, sg * mag)) >= 50]
            if ok:
                need[t] = ok[0]; break
    for _ in range(20):           # spread each turn over its neighbours so the arm eases into and out of it
        sm_need = need.copy()
        for t in range(1, 40):
            sm_need[t] = 0.25 * need[t - 1] + 0.5 * need[t] + 0.25 * need[t + 1]
        for t in range(41):
            if tip_x(turn(t, sm_need[t])) < 50:
                sm_need[t] = need[t]
        need = sm_need
    need[0] = need[40] = 0
    arm = arm + np.stack([np.zeros(41), need, need * 1.15], 1)
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
    eyes = {35: 'half', 36: 'closed', 37: 'half'}
    frames = []
    for i in range(41):
        frames.append({'index': i, 'hand_drawing': 'open' if p[i] > 0.25 else 'rest', 'eyes': eyes.get(i, 'open'), 'phase': float(p[i]),
                       'arm_world_angles_rad': [float(v) for v in arm[i]],
                       'shoulder_offset_cell': [0.0, float(shrug[i])], 'root_offset_cell': [float(root_dx[i]), float(root_dy[i])],
                       'bone_delta_rad': {k: float(D(v[i])) for k, v in body.items()}})
    acc = {['upper', 'fore', 'hand'][k]: round(float(np.degrees(np.abs(np.diff(np.unwrap(arm[:, k]), 2)).max())), 1) for k in range(3)}
    spd = np.degrees(np.abs(np.diff(np.unwrap(arm[:, 0]))))
    save_json(PILOT / 'data/rig_pose_run5.json', {
        'revision': 5, 'source': 'data/rig_pose_rev2.json rise (frames 3-16) + authored top wave + the rise reversed',
        'units': 'cell px / radians, image y down', 'arm_max_acceleration_deg_per_frame2': acc,
        'upper_arm_max_speed_deg_per_frame': round(float(spd.max()), 1),
        'edge_turn_deg': [round(float(math.degrees(v)), 1) for v in need],
        'min_fingertip_canvas_x': round(float(min(tip_x(a) for a in arm)), 1),
        'timing': {'rest': [0, 3], 'rise': [3, 15], 'wave': [15, 24], 'lower': [24, 35], 'rest_end': [35, 40]},
        'blink': 'half 35, closed 36, half 37', 'frames': frames})
    print('arm max acceleration', acc, '| upper-arm max speed', round(float(spd.max()), 1), 'deg/frame | phase peak', int(np.argmax(p)))


if __name__ == '__main__':
    main()
