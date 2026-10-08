#!/usr/bin/env python3
"""Run 3 guides: the whole figure acts with the wave, so LTX draws whole frames that move as a whole.

Take a1 showed the LTX Union take follows the rig guides closely (W2 figure 0.13%, head 0.31%;
total arm length within -32/+11% of the contract against take 1's -52/+27%) but copies their
near-still body: the run-2 guides only lean 0.7 degrees. These guides keep run 2's contours and
the rig arm at the W3 lengths and add the revision-2 acting on the same LTX timing:
  * smoothed arm path (data/rig_pose_rev2.json; spline, max 13 deg/frame^2 instead of 76);
  * root lift, anticipation dip and buoyant bob; torso lean about the waist; head tilt toward the
    hand about the neck; waving-side shoulder lift; free-arm counter-swing; a travelling wave
    through the rainbow hair and the left strands; tail counter-swing and fin follow-through;
  * one blink while she settles (eye outlines half 33, closed 34-35, half 36).
The tail chain runs at 0.6 of revision 2 (fin sweep 37 instead of 62 canvas px).
Every motion is a rigid turn or shift of an outline region (no stretching), and frame 0 and frame
40 are exactly the K0 guide, so the opening image still locks both ends.
Writes run3/guide_{full,half,quarter}/0000-0040.png, run3/guide_plan.json, data/run3_joints.json.
Owner-requested image exception for this pilot (guides, 2026-10-07).

    python -I scripts/render_guides_acting.py [--occlude --out run4] [--still]

--occlude (run 4): the waving arm is drawn in front, so hair, face and body lines inside its filled
outline are removed. Takes a1 and a2 smeared the hand mostly where its outline crossed the hair and
face lines; the overlap left the model to guess which shape is in front.
--still: no body acting (run-2 body), for an occlusion-only comparison.
--blink quick: half 33, closed 34, half 35 (take c1 kept the eyes shut from 26 to 36 on the longer blink);
--blink rev2 takes the eyes from the pose file. --pose data/rig_pose_run5.json: the run-5 arm path.
With PILOT_CANVAS_SHIFT_X=40 every guide line moves 40 canvas px right (run 5).
"""
import argparse, math, sys
import cv2
import numpy as np
from PIL import Image
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *
import render_guides as rg

OUT = PILOT / 'run3'
OCCLUDE = False
WAIST, NECK, HEAD_C, RSHOULDER, RELBOW = (184.5, 453), (195, 301), (207, 195), (275, 326), (305, 452)
TAIL2_C, FIN_C = (262, 640), (318, 730)
TAIL_GAIN = 0.6     # the revision-2 tail chain at 0.6: its three turns add up to a 62 px fin sweep at full gain


def rot(p, c, a):
    co, si = math.cos(a), math.sin(a); dx, dy = p[0] - c[0], p[1] - c[1]
    return (c[0] + dx * co - dy * si, c[1] + dx * si + dy * co)


def smooth(t):
    t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)


def frame_deltas(frames):
    """Revision-2 deltas minus frame 0's, so frames 0 and 40 are the K0 pose exactly."""
    keys = list(frames[0]['bone_delta_rad'])
    b0 = frames[0]['bone_delta_rad']; r0 = frames[0]['root_offset_cell']
    out = []
    for f in frames:
        d = {k: (f['bone_delta_rad'][k] - b0[k]) * (TAIL_GAIN if k in ('Tail1', 'Tail2', 'Fin') else 1.0) for k in keys}
        d['root'] = ((f['root_offset_cell'][0] - r0[0]) * CELL_SCALE, (f['root_offset_cell'][1] - r0[1]) * CELL_SCALE)
        d['shrug'] = f['shoulder_offset_cell'][1] * CELL_SCALE
        out.append(d)
    return out


def make_tr(d):
    """Guide-space point + part -> canvas point (guide + 32), hierarchical rigid turns with soft weights."""
    def torso(p):
        return rot(p, WAIST, d['Torso'])

    def tr(x, y, part):
        p = (x, y)
        if part == 'tail':
            w1 = smooth((y - 440) / 120); p = rot(p, WAIST, d['Tail1'] * w1)
            c2 = rot(TAIL2_C, WAIST, d['Tail1'])
            w2 = smooth((y - 600) / 90) * smooth((x - 200) / 60 + 0.5); p = rot(p, c2, d['Tail2'] * w2)
            c3 = rot(rot(FIN_C, WAIST, d['Tail1']), c2, d['Tail2'])
            w3 = smooth((x - 300) / 50) * smooth((y - 560) / 80); p = rot(p, c3, d['Fin'] * w3)
        else:
            if part in ('head', 'hair', 'face', 'eye'):
                if part == 'hair':
                    r = math.hypot(x - HEAD_C[0], y - HEAD_C[1])
                    if x > 200:
                        a = (d['Hair1'] * smooth((r - 70) / 60) + (d['Hair2'] - d['Hair1']) * smooth((r - 130) / 60)
                             + (d['Hair3'] - d['Hair2']) * smooth((r - 180) / 60))
                    else:
                        a = d['HairL'] * smooth((r - 70) / 60) * smooth((HEAD_C[0] - x) / 40)
                    p = rot(p, HEAD_C, a)
                p = rot(p, NECK, d['Head'])
            if part == 'shoulder':
                lift = smooth(1 - abs(x - 140) / 120) * smooth((453 - y) / 140)
                p = (p[0], p[1] + d['shrug'] * lift)
            if part == 'free_arm':
                if y > 440:
                    p = rot(p, RELBOW, d['RFore'])
                p = rot(p, RSHOULDER, d['RUpper'])
            p = torso(p)
        return (p[0] + d['root'][0] + 32 + CANVAS_SHIFT_X, p[1] + d['root'][1] + 32)
    return tr


def eye(cx, state):
    pts = [(cx - 13, 201), (cx - 10, 188), (cx, 182), (cx + 12, 189), (cx + 14, 207), (cx + 7, 220), (cx - 5, 221), (cx - 13, 211)]
    if state == 'open':
        return pts, True
    if state == 'half':        # upper lid lowered to the eye's middle
        return [(x, max(y, 201)) for x, y in pts], True
    return [(cx - 14, 206), (cx - 6, 211), (cx + 6, 211), (cx + 14, 206)], False     # closed: a soft lid line


def draw(f, d, scale):
    tr = make_tr(d); cv = rg.Canvas(scale)
    P = lambda pts, part, closed, smooth_: cv.path([tr(x, y, part) for x, y in pts], closed, smooth_)
    P([(113, 280), (96, 253), (104, 230), (95, 206), (104, 156), (124, 115), (161, 87), (202, 79), (254, 98), (304, 108), (332, 147), (384, 163), (414, 199), (410, 247), (385, 283), (381, 312), (339, 334), (308, 316), (276, 300), (276, 278)], 'hair', True, True)
    P([(142, 172), (163, 143), (192, 129), (220, 140), (250, 161), (273, 182), (276, 221), (262, 251), (232, 274), (201, 279), (172, 264), (147, 241), (138, 205)], 'head', True, True)
    P([(148, 166), (166, 153), (193, 149), (216, 170), (243, 179), (253, 172)], 'head', False, True)
    for x in (174, 242):
        pts, closed = eye(x, f['eyes']); P(pts, 'eye', closed, True)
    P([(185, 247), (202, 251), (219, 245)], 'head', False, True)
    P([(166, 100), (178, 83), (195, 91), (213, 54), (230, 92), (249, 83), (266, 107), (238, 105), (213, 87), (189, 105)], 'head', True, False)
    P([(160, 283), (164, 299), (190, 307), (217, 299), (230, 283)], 'shoulder', False, True)
    P([(144, 296), (126, 321), (137, 346), (149, 334), (154, 394), (150, 434), (184.5, 453), (247, 438), (263, 392), (265, 335), (282, 343), (296, 319), (279, 297), (241, 294), (217, 307), (190, 315), (162, 309)], 'shoulder', True, True)
    P([(150, 434), (137, 421), (133, 439), (152, 449), (184.5, 453), (220, 442), (247, 426), (262, 412), (274, 428), (247, 448)], 'shoulder', False, True)
    P([(150, 446), (126, 491), (124, 578), (132, 652), (149, 709), (190, 744), (237, 759), (284, 756), (312, 744), (336, 762), (379, 778), (423, 770), (467, 739), (523, 702), (493, 685), (448, 678), (416, 687), (385, 706), (423, 670), (428, 628), (460, 579), (486, 543), (450, 548), (416, 566), (381, 609), (345, 675), (330, 704), (303, 718), (271, 715), (254, 691), (248, 650), (263, 598), (277, 547), (279, 494), (266, 451)], 'tail', True, True)
    P([(312, 744), (350, 715), (400, 654), (450, 582)], 'tail', False, True)
    P([(336, 753), (391, 749), (450, 716), (496, 696)], 'tail', False, True)
    # Waving arm: the rig arm at the W3 lengths from the moved shoulder; it leans with the torso.
    s = to_canvas(K0_ARM['shoulder']); S = tr(s[0] - 32 - CANVAS_SHIFT_X, s[1] - 32, 'shoulder')
    A = [a + d['Torso'] for a in f['arm_world_angles_rad']]
    L = (CONTRACT['upper_arm'] * CELL_SCALE, CONTRACT['forearm'] * CELL_SCALE)
    E = (S[0] + L[0] * math.cos(A[0]), S[1] + L[0] * math.sin(A[0]))
    W = (E[0] + L[1] * math.cos(A[1]), E[1] + L[1] * math.sin(A[1]))
    T = (W[0] + CONTRACT['hand'] * CELL_SCALE * math.cos(A[2]), W[1] + CONTRACT['hand'] * CELL_SCALE * math.sin(A[2]))
    P([(275, 326), (285, 391), (321, 480), (341, 500), (346, 517), (342, 531), (336, 513), (335, 535), (329, 531), (327, 513), (321, 531), (317, 526), (318, 503), (311, 499), (282, 438), (262, 359)], 'free_arm', True, True)
    outline = rg.arm_outline(S, E, W, A)
    if OCCLUDE:      # the waving arm is in front: clear every line inside its filled outline (1 px margin)
        m = np.zeros_like(cv.im)
        cv2.fillPoly(m, [np.round(np.array(outline) / scale).astype(np.int32)], 255)
        cv.im[cv2.dilate(m, np.ones((3, 3), np.uint8)) > 0] = 0
    cv.path(outline, True, False)
    anchors = {}
    for name, (a, part) in {'crown': ((213, 54), 'head'), 'left_eye': ((174, 202), 'eye'), 'right_eye': ((242, 202), 'eye'),
                            'neck': ((195, 301), 'shoulder'), 'waist': ((184.5, 453), 'shoulder'), 'left_shoulder': ((140, 319), 'shoulder'),
                            'right_shoulder': ((275, 326), 'shoulder'), 'tail_junction': ((271, 715), 'tail'),
                            'hair_tip': ((414, 199), 'hair'), 'fin_tip': ((523, 702), 'tail')}.items():
        anchors[name] = tr(a[0], a[1], part)
    return cv.im, anchors, {'shoulder': S, 'elbow': E, 'wrist': W, 'tip': T}


def main():
    global OUT, OCCLUDE
    ap = argparse.ArgumentParser(); ap.add_argument('--occlude', action='store_true'); ap.add_argument('--still', action='store_true')
    ap.add_argument('--blink', choices=['rev2', 'quick'], default='rev2')
    ap.add_argument('--pose', default='data/rig_pose_rev2.json')
    ap.add_argument('--out', default='run3'); a = ap.parse_args(); OUT = PILOT / a.out; OCCLUDE = a.occlude
    frames = load_json(PILOT / a.pose)['frames']; deltas = frame_deltas(frames)
    if a.blink == 'quick':      # c1 held the eyes shut for frames 26-36; one closed frame, half lids either side
        quick = {33: 'half', 34: 'closed', 35: 'half'}
        frames = [dict(f, eyes=quick.get(f['index'], 'open')) for f in frames]
    if a.still:
        deltas = [{k: (v if k == 'shrug' else ((0.0, 0.0) if k == 'root' else 0.0)) for k, v in d.items()} for d in deltas]
        frames = [dict(f, eyes='open') for f in frames]
    for lane in ('full', 'half', 'quarter'):
        (OUT / f'guide_{lane}').mkdir(parents=True, exist_ok=True)
    plan, joints = [], []
    for f, d in zip(frames, deltas):
        for lane, sc in (('full', 1), ('half', 2), ('quarter', 4)):
            im, anchors, J = draw(f, d, sc)
            Image.fromarray(np.stack([im] * 3, 2)).save(OUT / f'guide_{lane}' / ('%04d.png' % f['index']))
            if sc == 1:
                full_anchors, fj = anchors, J
        plan.append({'index': f['index'], 'anchors': {k: [round(v[0], 3), round(v[1], 3)] for k, v in full_anchors.items()},
                     'arm_joints': {k: [round(v[0], 3), round(v[1], 3)] for k, v in fj.items()}, 'eyes': f['eyes'],
                     'deltas_deg': {k: round(math.degrees(v), 3) for k, v in d.items() if k not in ('root', 'shrug')},
                     'root_canvas_px': [round(v, 3) for v in d['root']], 'world_scale': 1,
                     'role': 'structural_motion_control_only', 'used_as_delivery_pixels': False})
        joints.append({'index': f['index'], **{k: [float(v[0]), float(v[1])] for k, v in fj.items()}, 'hand_open': f['hand_drawing'] == 'open'})
    a0 = plan[0]['anchors']
    travel = {k: round(max(math.hypot(p['anchors'][k][0] - a0[k][0], p['anchors'][k][1] - a0[k][1]) for p in plan), 2) for k in a0}
    end = max(math.hypot(plan[40]['anchors'][k][0] - a0[k][0], plan[40]['anchors'][k][1] - a0[k][1]) for k in a0)
    save_json(OUT / 'guide_plan.json', {
        'status': 'AUTHORING_PLAN_NOT_PIXEL_ACCEPTANCE', 'frames': plan, 'delivery_pixels': False,
        'max_anchor_travel_canvas_px': travel, 'frame40_vs_frame0_max_anchor_px': round(end, 4),
        'source': 'run-2 contours + rig arm at the W3 lengths on the smoothed revision-2 path + revision-2 acting (deltas from frame 0)',
        'method': 'scripts/render_guides_acting.py; rigid region turns about waist, neck, head, shoulders, tail and fin pivots',
        'options': {'occlude': a.occlude, 'still': a.still, 'blink': a.blink, 'pose': a.pose},
        'appearance_authority': 'Approved source atlas through the registered opening; outlines carry no appearance authority'})
    save_json(PILOT / f'data/{a.out}_joints.json', {'note': f'{a.out} guide arm joints, 640x896 canvas px', 'frames': joints})
    print('anchor travel (canvas px):', travel, '| frame 40 vs 0:', round(end, 4))


if __name__ == '__main__':
    main()
