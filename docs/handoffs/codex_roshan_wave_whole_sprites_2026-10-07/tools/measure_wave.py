#!/usr/bin/env python3
"""Numbers-only check for a Roshan sprite clip: does she keep one size, and is each frame one whole sprite?

Reads exported frames (never writes an image). Reports per frame:
  * figure scale: one similarity fit to fixed features (crown gem, eyes, mouth, neckline, waist,
    tail) tracked from the clip's own frame 0;
  * head scale: whole-patch (ECC affine) alignment of the face and fringe against frame 0;
  * waving-arm lengths (upper arm, forearm, hand) from annotated joints, against the proportion
    contract below (needs --joints);
  * the Aseprite master's layer count (needs --master): a whole sprite is one layer.

    python -I tools/measure_wave.py --frames 'frames/native/%04d.png' --count 41 \\
        [--cell-scale 1 --offset 0 0] [--joints joints.json] [--master wave.aseprite] [--out report.json]

Feature positions are given in the approved 256 px cell (roshan_gesture_a.png row 0, K0) and mapped
to the clip canvas by --cell-scale and --offset (canvas = scale * cell + offset).
joints.json: {"frames": [{"index": 0, "shoulder": [x, y], "elbow": [x, y], "wrist": [x, y],
"tip": [x, y], "hand_open": true}, ...]} in canvas pixels; tip is the longest fingertip. Set
"hand_open": false on frames that show the relaxed rest hand (K0's curled hand is shorter by design);
the hand length is then not checked on that frame.
"""
import argparse, json, struct, sys
import numpy as np, cv2
from PIL import Image

# Fixed features on the approved K0 cell (256 px). Same points as the wave studies' anchors.
FEATURES = {'crown': (145, 25), 'eyeL': (130, 63.6), 'eyeR': (153, 63.6), 'mouth': (142, 75.7),
            'neck': (141, 93), 'waist': (135.5, 143), 'tailmid': (128, 190), 'tailbot': (150, 228)}
FACE_BOX = (118, 38, 172, 92)   # x0, y0, x1, y1 in the cell: fringe, eyes, cheeks, mouth
# Proportion contract for the waving arm in the 256 px cell (front view, arm kept in the picture
# plane). Measured on the approved full-length drawings K0 and K2: upper arm 24.5/26.7, forearm
# 25.5/24.6, open hand 21.0 (K2), 20.2 (K1). K1's 15.3 px and K3's 22.0 px upper arms are the
# drawings that break it.
CONTRACT = {'upper_arm': 25.5, 'forearm': 24.5, 'hand': 20.5}
LIMITS = {'figure_scale_pp_pct': 1.0, 'head_scale_pp_pct': 2.0, 'arm_length_pct': 5.0, 'master_layers': 1}


def gray(path):
    a = np.array(Image.open(path).convert('RGBA')).astype(np.float32) / 255
    rgb = a[:, :, :3] * a[:, :, 3:4] + 0.5 * (1 - a[:, :, 3:4])
    return cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)


def subpixel(r, ml):
    j, i = ml; dx = dy = 0.0
    if 0 < j < r.shape[1] - 1:
        a, b, c = r[i, j - 1], r[i, j], r[i, j + 1]; d = a - 2 * b + c; dx = 0.5 * (a - c) / d if d else 0.0
    if 0 < i < r.shape[0] - 1:
        a, b, c = r[i - 1, j], r[i, j], r[i + 1, j]; d = a - 2 * b + c; dy = 0.5 * (a - c) / d if d else 0.0
    return j + dx, i + dy


def track(pattern, count, scale, off):
    half, search = max(4, round(8 * scale)), max(6, round(14 * scale)); pad = half + search + 2
    g0 = np.pad(gray(pattern % 0), pad, constant_values=128)
    pts0 = {k: (v[0] * scale + off[0], v[1] * scale + off[1]) for k, v in FEATURES.items()}
    rows = []
    for f in range(count):
        g = np.pad(gray(pattern % f), pad, constant_values=128); found = {}
        for k, (x, y) in pts0.items():
            cx, cy = int(round(x)) + pad, int(round(y)) + pad
            T = g0[cy - half:cy + half + 1, cx - half:cx + half + 1]
            R = g[cy - half - search:cy + half + search + 1, cx - half - search:cx + half + search + 1]
            r = cv2.matchTemplate(R, T, cv2.TM_CCOEFF_NORMED); _, mx, _, ml = cv2.minMaxLoc(r)
            if mx >= 0.55:
                sx, sy = subpixel(r, ml); found[k] = (cx - search + sx - pad, cy - search + sy - pad)
        rows.append(found)
    return pts0, rows


def ecc_scale(pattern, count, scale, off):
    x0, y0, x1, y1 = [round(v * scale + (off[i % 2])) for i, v in enumerate(FACE_BOX)]
    T = gray(pattern % 0)[y0:y1, x0:x1].astype(np.float32)
    out = []
    for f in range(count):
        I = gray(pattern % f).astype(np.float32)
        W = np.array([[1, 0, x0], [0, 1, y0]], np.float32)
        try:
            _, W = cv2.findTransformECC(T, I, W, cv2.MOTION_AFFINE,
                                        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 3)
            out.append(float(np.sqrt(abs(np.linalg.det(W[:, :2])))))
        except cv2.error:
            out.append(float('nan'))
    return out


def fit_scale(src, dst):
    if len(src) < 3: return float('nan')
    M, _ = cv2.estimateAffinePartial2D(np.float32(src), np.float32(dst), method=cv2.LMEDS)
    return float(np.hypot(M[0, 0], M[1, 0])) if M is not None else float('nan')


def aseprite_layers(path):
    b = open(path, 'rb').read(); assert struct.unpack_from('<H', b, 4)[0] == 0xA5E0, 'not an Aseprite file'
    p = 128; fsize, magic, old, _, _, new = struct.unpack_from('<IHHH2sI', b, p); q = p + 16; n = new or old; layers = 0
    for _ in range(n):
        csz, ct = struct.unpack_from('<IH', b, q); layers += ct == 0x2004; q += csz
    return layers


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--frames', required=True); ap.add_argument('--count', type=int, required=True)
    ap.add_argument('--cell-scale', type=float, default=1.0); ap.add_argument('--offset', type=float, nargs=2, default=(0.0, 0.0))
    ap.add_argument('--joints'); ap.add_argument('--master'); ap.add_argument('--label', default=''); ap.add_argument('--out')
    a = ap.parse_args()
    pts0, rows = track(a.frames, a.count, a.cell_scale, a.offset)
    fig = []
    for found in rows:   # compare with frame 0's own tracked positions, so frame 0 measures exactly 1
        ks = [k for k in found if k in rows[0]]; fig.append(fit_scale([rows[0][k] for k in ks], [found[k] for k in ks]))
    head = ecc_scale(a.frames, a.count, a.cell_scale, a.offset)
    rep = {'label': a.label, 'frames': a.count, 'limits': LIMITS, 'contract_cell_px': CONTRACT, 'checks': {}}
    def pp(v): v = np.array(v, float); v = v[np.isfinite(v)]; return float(100 * (v.max() - v.min())) if len(v) else float('nan')
    rep['figure_scale_pct'] = [round(100 * (s - 1), 2) for s in fig]
    rep['head_scale_pct'] = [round(100 * (s - 1), 2) for s in head]
    rep['checks']['figure_scale_pp_pct'] = {'value': round(pp(fig), 2), 'pass': pp(fig) <= LIMITS['figure_scale_pp_pct']}
    rep['checks']['head_scale_pp_pct'] = {'value': round(pp(head), 2), 'pass': pp(head) <= LIMITS['head_scale_pp_pct']}
    if a.joints:
        J = {j['index']: j for j in json.load(open(a.joints))['frames']}; worst = {}; per = []
        for f in range(a.count):
            if f not in J: continue
            j = J[f]; L = {'upper_arm': (j['shoulder'], j['elbow']), 'forearm': (j['elbow'], j['wrist']), 'hand': (j['wrist'], j['tip'])}
            if not j.get('hand_open', True): del L['hand']
            dev = {k: 100 * (float(np.hypot(p[0] - q[0], p[1] - q[1])) / (CONTRACT[k] * a.cell_scale) - 1) for k, (p, q) in L.items()}
            per.append({'frame': f, **{k: round(v, 1) for k, v in dev.items()}})
            for k, v in dev.items():
                if abs(v) > abs(worst.get(k, (0, 0))[1]): worst[k] = (f, v)
        rep['arm_length_vs_contract_pct'] = per
        rep['checks']['arm_length_pct'] = {'value': {k: {'frame': f, 'pct': round(v, 1)} for k, (f, v) in worst.items()},
                                           'pass': all(abs(v) <= LIMITS['arm_length_pct'] for _, v in worst.values())}
    if a.master:
        n = aseprite_layers(a.master); rep['checks']['master_layers'] = {'value': n, 'pass': n == LIMITS['master_layers']}
    rep['all_pass'] = all(c['pass'] for c in rep['checks'].values())
    for k, c in rep['checks'].items(): print('%-22s %s  %s' % (k, 'PASS' if c['pass'] else 'FAIL', json.dumps(c['value'])))
    print('RESULT', 'PASS' if rep['all_pass'] else 'FAIL')
    if a.out: json.dump(rep, open(a.out, 'w'), indent=1)
    return 0 if rep['all_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
