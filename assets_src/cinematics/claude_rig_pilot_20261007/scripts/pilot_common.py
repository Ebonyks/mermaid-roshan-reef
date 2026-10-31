"""Shared constants and the Union guide math for the rig pilot (2026-10-07).

Coordinates:
  cell   - the approved 256 px roshan_gesture_a.png cell (K0 = row 0, column 0)
  canvas - the 640x896 LTX Union take canvas; canvas = CELL_SCALE * cell + OFFSET
  guide  - the Union guide.lua drawing space; canvas = guide + 32
"""
import json, math
from pathlib import Path

PILOT = Path(__file__).resolve().parents[1]
ROOT = PILOT.parents[2]
UNION = ROOT / 'assets_src/cinematics/ltx25_union_trial_20261004'
TAKE1 = UNION / 'take_1/refined_frames/%04d.png'
ATLAS = ROOT / 'assets/characters/roshan_25d/roshan_gesture_a.png'
MEASURE = ROOT / 'docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py'
FRAMES, FPS = 41, 24

# Mapping measured on take 1 in the 2026-10-07 wave handoff (measure_wave.py --cell-scale/--offset).
CELL_SCALE, OFFSET = 3.2025, (-216.95, 33.85)
# W3 proportion contract, 256 px cell (docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07).
CONTRACT = {'upper_arm': 25.5, 'forearm': 24.5, 'hand': 20.5}
# Approved K0 waving-arm joints, 256 px cell (same annotation as the handoff data).
K0_ARM = {'shoulder': (120.0, 103.0), 'elbow': (115.0, 127.0), 'wrist': (104.0, 150.0), 'tip': (98.0, 165.0)}
# K2 open hand, 256 px cell (K2 = row 0, column 2): wrist crease, longest (middle) fingertip and the
# forearm direction point used to cut the hand at the wrist.
K2_HAND = {'wrist': (74.0, 41.0), 'tip': (71.0, 19.5), 'elbow': (87.0, 70.0)}


def hand_cells():
    """Approved hand pixels from the atlas: K0 relaxed rest hand and K2 open hand.

    Returns {name: (rgba_cell, mask, wrist, tip)} in each key's own 256 px cell. The hand is cut at
    the wrist line perpendicular to that key's forearm."""
    import numpy as np
    from PIL import Image
    a = np.array(Image.open(ATLAS).convert('RGBA'))
    out = {}
    for name, col, (wr, tp, el), box in [
            ('rest', 0, (K0_ARM['wrist'], K0_ARM['tip'], K0_ARM['elbow']), (88, 146, 116, 170)),
            ('open', 2, (K2_HAND['wrist'], K2_HAND['tip'], K2_HAND['elbow']), (58, 15, 86, 46))]:
        cell = a[0:256, col * 256:col * 256 + 256].copy()
        d = np.array(wr) - np.array(el); d = d / np.hypot(*d)
        ys, xs = np.mgrid[0:256, 0:256]
        x0, y0, x1, y1 = box
        m = (cell[:, :, 3] > 0) & (xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1)
        m &= ((xs + .5 - wr[0]) * d[0] + (ys + .5 - wr[1]) * d[1]) >= -1.5
        import cv2
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
        m = lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))       # the hand only
        out[name] = (cell, m, wr, tp)
    return out


def to_canvas(p):
    return (p[0] * CELL_SCALE + OFFSET[0], p[1] * CELL_SCALE + OFFSET[1])


def to_cell(p):
    return ((p[0] - OFFSET[0]) / CELL_SCALE, (p[1] - OFFSET[1]) / CELL_SCALE)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def ang(a, b):
    return math.atan2(b[1] - a[1], b[0] - a[0])


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def load_json(p):
    return json.loads(Path(p).read_text())


def save_json(p, data):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(data, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else float(o)) + '\n')


# ---- Port of ltx25_union_trial_20261004/scripts/guide.lua (pose keys and transforms) ----
GUIDE_KEYS = [(0, 80, 500, 116, 408, 0), (3, 82, 500, 118, 407, 0), (7, 100, 236, 92, 321, .65),
              (17, 80, 104, 117, 226, 1), (22, 96, 180, 65, 289, .85), (27, 82, 339, 99, 382, .45),
              (36, 80, 500, 116, 408, 0), (40, 80, 500, 116, 408, 0)]
GUIDE_HAND = [(-9, 18), (-18, 5), (-21, -9), (-18, -17), (-12, -4), (-13, -26), (-9, -32), (-5, -8), (-4, -33),
              (1, -35), (4, -8), (7, -30), (12, -32), (10, -5), (18, -21), (22, -20), (16, 2), (21, -6), (27, -6),
              (27, 0), (13, 15), (9, 18)]
GUIDE_HAND_WRIST, GUIDE_HAND_TIP = (0, 18), (1, -35)


def guide_pose(i):
    """hx, hy, ex, ey, phase exactly as guide.lua's pose(i)."""
    for j in range(len(GUIDE_KEYS) - 1):
        a, b = GUIDE_KEYS[j], GUIDE_KEYS[j + 1]
        if a[0] <= i <= b[0]:
            t = (i - a[0]) / (b[0] - a[0]); t = t * t * (3 - 2 * t)
            return [a[k] + (b[k] - a[k]) * t for k in range(1, 6)]
    raise ValueError(i)


def guide_arm_joints(i):
    """Union guide arm joints for frame i in canvas pixels (shoulder base, elbow, wrist, longest tip)."""
    hx, hy, ex, ey, phase = guide_pose(i)
    a = .012 * phase; c, s = math.cos(a), math.sin(a)
    def tr(x, y):
        dx, dy = x - 184.5, y - 453
        return (184.5 + dx * c - dy * s + 32, 453 + dx * s + dy * c + 32)
    ha = math.pi * (1 - phase); hc, hs = math.cos(ha), math.sin(ha)
    hand = lambda x, y: (hx + x * hc - y * hs, hy + x * hs + y * hc)
    return {'shoulder': tr(140, 319), 'elbow': tr(ex, ey), 'wrist': tr(*hand(*GUIDE_HAND_WRIST)),
            'tip': tr(*hand(*GUIDE_HAND_TIP)), 'phase': phase}
