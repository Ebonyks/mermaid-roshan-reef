#!/usr/bin/env python3
"""Per-frame clothing fit for an animation clip, in the game outfit builder's pose_fit.json schema.

The game bakes outfits (ribbon, party, garden, disguise) per 256 px cell with
tools/build_fashion_outfits.gd from one bodice box per cell. For an animation clip the box must not
change size from frame to frame, or the dress would breathe. So:
  * box size = the approved K0 bodice box (party_garment_v1/pose_fit.json, roshan_gesture_a cell 0);
  * box position follows the bodice: the neck and waist features (measure_wave.py points) are tracked
    from the clip's own frame 0 by normalised cross-correlation with sub-pixel peaks; the mean
    displacement, lightly smoothed (Savitzky-Golay, 5 frames), is rounded to whole pixels
    (the builder places garments on the pixel grid). The residual is reported as clothing slip.
Writes <clip>/pose_fit_clip.json (builder schema) and <clip>/pose_fit_report.json. Numbers only.

    python -I scripts/clip_pose_fit.py <clip dir with cells/ and atlas.png> <source name>
"""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image
from scipy.signal import savgol_filter
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import ROOT, save_json, load_json

K0_BODICE = load_json(ROOT / 'assets_src/fashion_designer/party_garment_v1/pose_fit.json')['sources']['roshan_gesture_a']['cells'][0]
POINTS = {'neck': (141, 93), 'waist': (135.5, 143)}      # measure_wave.py FEATURES, 256 px cell
HALF, SEARCH = 8, 14


def gray(p):
    a = np.array(Image.open(p).convert('RGBA')).astype(np.float32) / 255
    rgb = a[:, :, :3] * a[:, :, 3:4] + 0.5 * (1 - a[:, :, 3:4])
    return cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)


def peak(r, ml):
    j, i = ml; dx = dy = 0.0
    if 0 < j < r.shape[1] - 1:
        a, b, c = r[i, j - 1], r[i, j], r[i, j + 1]; d = a - 2 * b + c; dx = 0.5 * (a - c) / d if d else 0.0
    if 0 < i < r.shape[0] - 1:
        a, b, c = r[i - 1, j], r[i, j], r[i + 1, j]; d = a - 2 * b + c; dy = 0.5 * (a - c) / d if d else 0.0
    return j + dx, i + dy


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('clip'); ap.add_argument('name'); v = ap.parse_args()
    clip = Path(v.clip).resolve(); cells = sorted((clip / 'cells').glob('*.png')); n = len(cells)
    pad = HALF + SEARCH + 2
    g0 = np.pad(gray(cells[0]), pad, constant_values=128)
    disp, conf = np.zeros((n, 2, 2)), np.zeros((n, 2))
    for f, p in enumerate(cells):
        g = np.pad(gray(p), pad, constant_values=128)
        for k, (x, y) in enumerate(POINTS.values()):
            cx, cy = int(round(x)) + pad, int(round(y)) + pad
            T = g0[cy - HALF:cy + HALF + 1, cx - HALF:cx + HALF + 1]
            R = g[cy - HALF - SEARCH:cy + HALF + SEARCH + 1, cx - HALF - SEARCH:cx + HALF + SEARCH + 1]
            r = cv2.matchTemplate(R, T, cv2.TM_CCOEFF_NORMED); _, mx, _, ml = cv2.minMaxLoc(r)
            sx, sy = peak(r, ml); disp[f, k] = (sx - SEARCH, sy - SEARCH); conf[f, k] = mx
    raw = disp.mean(1)
    vec = np.array(POINTS['waist']) - np.array(POINTS['neck'])
    rot = [float(np.degrees(np.arctan2(*(vec + disp[f, 1] - disp[f, 0])[::-1]) - np.arctan2(*vec[::-1]))) for f in range(n)]
    smooth = savgol_filter(raw, 5, 2, axis=0) if n >= 5 else raw
    smooth[0] = 0.0
    step = np.round(smooth).astype(int)
    x0, y0, x1, y1 = K0_BODICE
    boxes = [[x0 + int(dx), y0 + int(dy), x1 + int(dx), y1 + int(dy)] for dx, dy in step]
    atlas = clip / 'atlas.png'
    rel = str(atlas.relative_to(ROOT)).replace('\\', '/')
    save_json(clip / 'pose_fit_clip.json', {
        'schema': 1, 'status': 'PILOT_CLIP_POSE_FIT_NOT_RUNTIME',
        'method': 'Constant K0 bodice box (party_garment_v1 pose_fit roshan_gesture_a cell 0) moved by the tracked neck/waist '
                  'displacement of each frame (scripts/clip_pose_fit.py); same schema as party_garment_v1/pose_fit.json.',
        'sources': {v.name: {'source': rel, 'sha256': hashlib.sha256(atlas.read_bytes()).hexdigest(), 'cells': boxes}}})
    slip = np.hypot(*(raw - step).T)
    save_json(clip / 'pose_fit_report.json', {
        'frames': n, 'k0_bodice_box': K0_BODICE, 'tracked_points_cell': POINTS,
        'min_match_score': round(float(conf.min()), 3), 'low_score_frames': [int(f) for f in np.nonzero(conf.min(1) < 0.6)[0]],
        'bodice_offset_px': [[round(float(a), 2) for a in r] for r in raw],
        'bodice_rotation_deg': [round(r, 2) for r in rot],
        'box_offset_px': step.tolist(),
        'clothing_slip_px': {'max': round(float(slip.max()), 2), 'mean': round(float(slip.mean()), 2),
                             'note': 'distance between the tracked bodice and the whole-pixel garment position'},
        'bodice_travel_px': {'x': round(float(np.ptp(raw[:, 0])), 2), 'y': round(float(np.ptp(raw[:, 1])), 2)},
        'rotation_range_deg': round(float(np.ptp(rot)), 2)})
    print(v.name, 'bodice travel', np.ptp(raw, 0).round(2), 'rotation range', round(float(np.ptp(rot)), 2),
          'slip max', round(float(slip.max()), 2), 'min score', round(float(conf.min()), 3))


if __name__ == '__main__':
    main()
