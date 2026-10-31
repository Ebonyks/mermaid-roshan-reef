#!/usr/bin/env python3
"""Run 2 (rules back): proportion-locked structural guides for the next whole-frame LTX Union take.

A Python port of ltx25_union_trial_20261004/scripts/guide.lua (same contours, Catmull-Rom spans,
1 px white lines on black, full/half/quarter grids) with two changes:
  * the waving arm is the rig arm at the W3 contract lengths, posed by the LTX-solved angles
    (data/rig_pose.json): upper arm 25.5, forearm 24.5, open hand 20.5 cell px, always in-plane;
  * every body response (lean, shoulder lift, hair, tail) follows one master phase taken from the
    solved arm's own elevation, so the whole figure moves on one timing (W4).
Writes run2/guide_{full,half,quarter}/0000-0040.png, run2/guide_plan.json and data/run2_joints.json.
Owner-requested image exception for this pilot (2026-10-07).

    python -I scripts/render_guides.py
"""
import math, sys
import numpy as np
from PIL import Image
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

OUT = PILOT / 'run2'
HAND_K = CONTRACT['hand'] * CELL_SCALE / dist(GUIDE_HAND_WRIST, GUIDE_HAND_TIP)
W_UPPER, W_FORE = 22.0, 20.0     # outline widths in canvas px (the Union guide drew about 20)


class Canvas:
    def __init__(self, scale):
        self.s = scale; self.im = np.zeros((896 // scale, 640 // scale), np.uint8)

    def line(self, a, b):
        n = max(1, math.ceil(max(abs(b[0] - a[0]), abs(b[1] - a[1]))))
        for j in range(n + 1):
            x = math.floor(a[0] + (b[0] - a[0]) * j / n + .5); y = math.floor(a[1] + (b[1] - a[1]) * j / n + .5)
            if 0 <= x < self.im.shape[1] and 0 <= y < self.im.shape[0]:
                self.im[y, x] = 255

    def path(self, pts, closed, smooth):
        pts = [(x / self.s, y / self.s) for x, y in pts]; count = len(pts)
        if smooth:
            total = count if closed else count - 1
            at = (lambda k: pts[(k - 1) % count]) if closed else (lambda k: pts[max(1, min(count, k)) - 1])
            for j in range(1, total + 1):
                a, b, c1, d = at(j - 1), at(j), at(j + 1), at(j + 2); last = b
                for q in range(1, 13):
                    t = q / 12; t2, t3 = t * t, t * t * t
                    now = tuple(.5 * ((2 * b[k]) + (-a[k] + c1[k]) * t + (2 * a[k] - 5 * b[k] + 4 * c1[k] - d[k]) * t2
                                      + (-a[k] + 3 * b[k] - 3 * c1[k] + d[k]) * t3) for k in range(2))
                    self.line(last, now); last = now
        else:
            for j in range(count - 1): self.line(pts[j], pts[j + 1])
            if closed: self.line(pts[-1], pts[0])


def body_transform(phase):
    a = .012 * phase; c, s = math.cos(a), math.sin(a)
    def tr(x, y, part):
        if part == 'shoulder':
            y = y - 6 * phase * (1 - min(1, abs(x - 140) / 120)) * max(0, min(1, (453 - y) / 140))
        if part == 'hair':
            x = x + 4 * phase * max(0, (x - 260) / 155)          # was 4*sin(i*pi/20): now on the one master timing
        if part == 'tail':
            x = x + 4 * phase * max(0, (y - 453) / 330)
        dx, dy = x - 184.5, y - 453
        return (184.5 + dx * c - dy * s + 32, 453 + dx * s + dy * c + 32)
    return tr


def arm_joints(f):
    """Rig arm joints in canvas px at the contract lengths, from the solved world angles."""
    tr = body_transform(f['phase'])
    s = to_canvas(K0_ARM['shoulder']); S = tr(s[0] - 32, s[1] - 32, 'shoulder')
    S = (S[0], S[1] + f['shoulder_offset_cell'][1] * CELL_SCALE)
    A = f['arm_world_angles_rad']; L = (CONTRACT['upper_arm'] * CELL_SCALE, CONTRACT['forearm'] * CELL_SCALE)
    E = (S[0] + L[0] * math.cos(A[0]), S[1] + L[0] * math.sin(A[0]))
    W = (E[0] + L[1] * math.cos(A[1]), E[1] + L[1] * math.sin(A[1]))
    hl = CONTRACT['hand'] * CELL_SCALE
    T = (W[0] + hl * math.cos(A[2]), W[1] + hl * math.sin(A[2]))
    return S, E, W, T, A


def arm_outline(S, E, W, A):
    """One closed contour: shoulder (under the sleeve) -> elbow -> wrist -> hand -> back."""
    n = lambda a: (-math.sin(a), math.cos(a))
    off = lambda p, a, w: (p[0] + n(a)[0] * w, p[1] + n(a)[1] * w)
    top = (S[0] + 8 * math.cos(A[0]), S[1] + 8 * math.sin(A[0]))      # start inside the sleeve
    we = (W_UPPER + W_FORE) / 4
    turn = math.sin(A[1] - A[0])

    def elbow(sign):
        """Outer side of the bend: a rounded arc around the elbow. Inner side: the crease point."""
        p0, p1 = off(E, A[0], sign * we), off(E, A[1], sign * we)
        outer = (sign < 0) == (turn > 0)
        if not outer or abs(turn) < 1e-3:
            return [((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)]
        a0, a1 = math.atan2(p0[1] - E[1], p0[0] - E[0]), math.atan2(p1[1] - E[1], p1[0] - E[0])
        d = wrap(a1 - a0)
        return [(E[0] + we * math.cos(a0 + d * k / 6), E[1] + we * math.sin(a0 + d * k / 6)) for k in range(7)]
    rot = A[2] - math.atan2(GUIDE_HAND_TIP[1] - GUIDE_HAND_WRIST[1], GUIDE_HAND_TIP[0] - GUIDE_HAND_WRIST[0])
    c, s = math.cos(rot), math.sin(rot)
    hand = [(W[0] + HAND_K * ((x - GUIDE_HAND_WRIST[0]) * c - (y - GUIDE_HAND_WRIST[1]) * s),
             W[1] + HAND_K * ((x - GUIDE_HAND_WRIST[0]) * s + (y - GUIDE_HAND_WRIST[1]) * c)) for x, y in GUIDE_HAND]
    # GUIDE_HAND runs from the wrist's -x side to its +x side; the arm's +normal side meets the hand's +x side.
    side = 1 if ((hand[-1][0] - hand[0][0]) * n(A[1])[0] + (hand[-1][1] - hand[0][1]) * n(A[1])[1]) > 0 else -1
    if side < 0: hand = hand[::-1]
    return ([off(top, A[0], -W_UPPER / 2)] + elbow(-1) + [off(W, A[1], -W_FORE / 2)] + hand
            + [off(W, A[1], W_FORE / 2)] + elbow(1)[::-1] + [off(top, A[0], W_UPPER / 2)])


def draw(f, scale):
    phase = f['phase']; tr = body_transform(phase); cv = Canvas(scale)
    P = lambda pts, part, closed, smooth: cv.path([tr(x, y, part) for x, y in pts], closed, smooth)
    i = f['index']
    # Hair, face, crown and facial landmarks; bodice, sleeves, waist and tail (guide.lua, unchanged shapes).
    P([(113, 280), (96, 253), (104, 230), (95, 206), (104, 156), (124, 115), (161, 87), (202, 79), (254, 98), (304, 108), (332, 147), (384, 163), (414, 199), (410, 247), (385, 283), (381, 312), (339, 334), (308, 316), (276, 300), (276, 278)], 'hair', True, True)
    P([(142, 172), (163, 143), (192, 129), (220, 140), (250, 161), (273, 182), (276, 221), (262, 251), (232, 274), (201, 279), (172, 264), (147, 241), (138, 205)], 'head', True, True)
    P([(148, 166), (166, 153), (193, 149), (216, 170), (243, 179), (253, 172)], 'head', False, True)
    for x in (174, 242):
        P([(x - 13, 201), (x - 10, 188), (x, 182), (x + 12, 189), (x + 14, 207), (x + 7, 220), (x - 5, 221), (x - 13, 211)], 'head', True, True)
    P([(185, 247), (202, 251), (219, 245)], 'head', False, True)
    P([(166, 100), (178, 83), (195, 91), (213, 54), (230, 92), (249, 83), (266, 107), (238, 105), (213, 87), (189, 105)], 'head', True, False)
    P([(160, 283), (164, 299), (190, 307), (217, 299), (230, 283)], 'shoulder', False, True)
    P([(144, 296), (126, 321), (137, 346), (149, 334), (154, 394), (150, 434), (184.5, 453), (247, 438), (263, 392), (265, 335), (282, 343), (296, 319), (279, 297), (241, 294), (217, 307), (190, 315), (162, 309)], 'shoulder', True, True)
    P([(150, 434), (137, 421), (133, 439), (152, 449), (184.5, 453), (220, 442), (247, 426), (262, 412), (274, 428), (247, 448)], 'shoulder', False, True)
    P([(150, 446), (126, 491), (124, 578), (132, 652), (149, 709), (190, 744), (237, 759), (284, 756), (312, 744), (336, 762), (379, 778), (423, 770), (467, 739), (523, 702), (493, 685), (448, 678), (416, 687), (385, 706), (423, 670), (428, 628), (460, 579), (486, 543), (450, 548), (416, 566), (381, 609), (345, 675), (330, 704), (303, 718), (271, 715), (254, 691), (248, 650), (263, 598), (277, 547), (279, 494), (266, 451)], 'tail', True, True)
    P([(312, 744), (350, 715), (400, 654), (450, 582)], 'tail', False, True)
    P([(336, 753), (391, 749), (450, 716), (496, 696)], 'tail', False, True)
    # Waving arm: the rig arm (canvas coordinates already include the lean).
    S, E, W, T, A = arm_joints(f)
    cv.path(arm_outline(S, E, W, A), True, False)
    P([(275, 326), (285, 391), (321, 480), (341, 500), (346, 517), (342, 531), (336, 513), (335, 535), (329, 531), (327, 513), (321, 531), (317, 526), (318, 503), (311, 499), (282, 438), (262, 359)], 'shoulder', True, True)
    anchors = {}
    for name, a in {'crown': (213, 54), 'left_eye': (174, 202), 'right_eye': (242, 202), 'neck': (195, 301), 'waist': (184.5, 453),
                    'left_shoulder': (140, 319), 'right_shoulder': (275, 326), 'tail_junction': (271, 715)}.items():
        part = 'tail' if name == 'tail_junction' else ('shoulder' if name in ('neck', 'left_shoulder', 'right_shoulder') else 'head')
        anchors[name] = tr(a[0], a[1], part)
    return cv.im, anchors, {'shoulder': S, 'elbow': E, 'wrist': W, 'tip': T}


def main():
    pose = load_json(PILOT / 'data/rig_pose.json')['frames']
    for lane in ('full', 'half', 'quarter'): (OUT / f'guide_{lane}').mkdir(parents=True, exist_ok=True)
    plan, joints = [], []
    for f in pose:
        for lane, sc in (('full', 1), ('half', 2), ('quarter', 4)):
            im, anchors, J = draw(f, sc)
            Image.fromarray(np.stack([im] * 3, 2)).save(OUT / f'guide_{lane}' / ('%04d.png' % f['index']))
            if sc == 1: full_anchors, fj = anchors, J
        plan.append({'index': f['index'], 'anchors': {k: [round(v[0], 3), round(v[1], 3)] for k, v in full_anchors.items()},
                     'arm_joints': {k: [round(v[0], 3), round(v[1], 3)] for k, v in fj.items()},
                     'phase': f['phase'], 'uniform_body_lean_radians': .012 * f['phase'], 'world_scale': 1,
                     'role': 'structural_motion_control_only', 'used_as_delivery_pixels': False})
        joints.append({'index': f['index'], **{k: [float(v[0]), float(v[1])] for k, v in fj.items()}, 'hand_open': True})
    save_json(OUT / 'guide_plan.json', {
        'status': 'AUTHORING_PLAN_NOT_PIXEL_ACCEPTANCE', 'frames': plan, 'delivery_pixels': False,
        'source': 'Union guide.lua contours (body) + rig arm at the W3 contract lengths posed by the LTX take-1 solve',
        'method': 'scripts/render_guides.py; one master phase from the solved arm elevation drives lean, shoulder, hair and tail',
        'appearance_authority': 'Approved source atlas through the registered opening; outlines carry no appearance authority'})
    save_json(PILOT / 'data/run2_joints.json', {'note': 'run 2 guide arm joints, 640x896 canvas px', 'frames': joints})
    print('wrote', len(pose), 'frames x 3 lanes')


if __name__ == '__main__':
    main()
