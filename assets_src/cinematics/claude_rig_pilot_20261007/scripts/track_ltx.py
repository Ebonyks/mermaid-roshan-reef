#!/usr/bin/env python3
"""Track LTX Union take 1 (native 640x896 frames) into numbers: body landmarks and the waving arm.

Writes data/take1_tracks.json only (no images). Body landmarks use the same template tracker as
measure_wave.py (plus a hair and a fin point). The waving arm is solved per frame onto the
rig arm (approved hand drawings, segment lengths free around the W3 contract) by matching the take's
arm skin mask; the result is joints, angles, segment scales and the hand drawing to show. The solve
step then re-poses the fixed-length rig onto these joints by two-bone IK.
Elbow and wrist joint limits keep the solve anatomically plausible on smeared frames.

    python -I scripts/track_ltx.py [--frames <pattern %04d>] [--seed-guide union|run2|run3|run4|run4s] [--out data/<name>.json]
Defaults reproduce the Union take-1 track; run-2 takes seed the arm search from the rig guide joints.
"""
import importlib.util, math, sys
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from pilot_common import *

spec = importlib.util.spec_from_file_location('measure_wave', MEASURE)
mw = importlib.util.module_from_spec(spec); spec.loader.exec_module(mw)

EXTRA = {'hair': (190.0, 75.0), 'fin': (205.0, 200.0)}   # K0 cell points inside the rainbow hair and fin


SRC = str(TAKE1)        # frames pattern; set from --frames


def rgb(i):
    return np.array(Image.open(SRC % i).convert('RGB'))


def skin_mask(a):
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    m = ((hsv[:, :, 0] >= 3) & (hsv[:, :, 0] <= 22) & (hsv[:, :, 1] >= 35) & (hsv[:, :, 1] <= 150)
         & (hsv[:, :, 2] >= 170)).astype(np.uint8)
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def arm_component(m, neck_x):
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, connectivity=8)
    best, area = 0, 0
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] > 300 and cen[k][0] < neck_x - 30 and st[k, cv2.CC_STAT_AREA] > area:
            best, area = k, st[k, cv2.CC_STAT_AREA]
    return (lab == best).astype(np.uint8) if best else None


def track_extra(count):
    s, off = CELL_SCALE, OFFSET
    half, search = 26, 60; pad = half + search + 2
    g0 = np.pad(mw.gray(SRC % 0), pad, constant_values=128); rows = []
    pts0 = {k: to_canvas(v) for k, v in EXTRA.items()}
    for f in range(count):
        g = np.pad(mw.gray(SRC % f), pad, constant_values=128); found = {}
        for k, (x, y) in pts0.items():
            cx, cy = int(round(x)) + pad, int(round(y)) + pad
            T = g0[cy - half:cy + half + 1, cx - half:cx + half + 1]
            R = g[cy - half - search:cy + half + search + 1, cx - half - search:cx + half + search + 1]
            r = cv2.matchTemplate(R, T, cv2.TM_CCOEFF_NORMED); _, mx, _, ml = cv2.minMaxLoc(r)
            if mx >= 0.5:
                sx, sy = mw.subpixel(r, ml); found[k] = (cx - search + sx - pad, cy - search + sy - pad)
        rows.append(found)
    return rows


class RigArmFit:
    """Solve the waving arm onto a fixed-length rig by analysis-by-synthesis.

    The model is the rig's arm: upper-arm and forearm capsules plus the approved hand silhouette (K0 rest
    hand or K2 open hand, cut from the atlas, at the W3 hand length). Free parameters are the three world
    angles, a small shoulder offset and the two segment lengths as scales of the W3 contract (0.45-1.45),
    so foreshortened or stretched LTX arms are measured rather than forced. The hand drawing is chosen
    per frame. The cost is 1 - IoU against the take's arm skin mask, plus weak priors."""
    def __init__(self, width):
        self.w = width
        self.L = (CONTRACT['upper_arm'] * CELL_SCALE, CONTRACT['forearm'] * CELL_SCALE)
        self.hands = {}
        for name, (cell, m, wr, tp) in hand_cells().items():
            m = m & (skin_mask(np.ascontiguousarray(cell[:, :, :3])) > 0) & (cell[:, :, 3] > 200)
            ys, xs = np.nonzero(m); sub = (np.arange(4) + .5) / 4
            px = (xs[:, None, None] + sub[None, :, None]).repeat(4, 2).ravel()
            py = (ys[:, None, None] + sub[None, None, :]).repeat(4, 1).ravel()
            ax = np.array(tp) - np.array(wr); length = np.hypot(*ax); ux = ax / length; uy = np.array([-ux[1], ux[0]])
            rel = np.stack([px - wr[0], py - wr[1]], 1)
            k = (CONTRACT['hand'] / length) if name == 'open' else 1.0       # open hand at contract length
            self.hands[name] = np.stack([rel @ ux, rel @ uy], 1) * k * CELL_SCALE

    def joints(self, S, x):
        t1, t2, t3, dx, dy, k1, k2 = x; S2 = (S[0] + dx, S[1] + dy)
        E = (S2[0] + k1 * self.L[0] * math.cos(t1), S2[1] + k1 * self.L[0] * math.sin(t1))
        W = (E[0] + k2 * self.L[1] * math.cos(t2), E[1] + k2 * self.L[1] * math.sin(t2))
        return S2, E, W, t3

    def render(self, shape, S, x, hand):
        S2, E, W, t3 = self.joints(S, x)
        im = np.zeros(shape, np.uint8)
        a = (S2[0] + .3 * (E[0] - S2[0]), S2[1] + .3 * (E[1] - S2[1]))   # top of the upper arm is under the sleeve
        P = lambda p: (int(round(p[0] * 4)), int(round(p[1] * 4)))
        cv2.line(im, P(a), P(E), 1, int(round(self.w)), cv2.LINE_8, 2)
        cv2.line(im, P(E), P(W), 1, int(round(self.w)), cv2.LINE_8, 2)
        u = np.array([math.cos(t3), math.sin(t3)]); v = np.array([-u[1], u[0]])
        pts = self.hands[hand][:, :1] * u + self.hands[hand][:, 1:] * v + np.array(W)
        xi, yi = np.round(pts[:, 0]).astype(int), np.round(pts[:, 1]).astype(int)
        ok = (xi >= 0) & (yi >= 0) & (xi < shape[1]) & (yi < shape[0]); h = np.zeros(shape, np.uint8)
        h[yi[ok], xi[ok]] = 1
        return im | cv2.morphologyEx(h, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    def cost(self, mask, S, x, hand, prev):
        m = self.render(mask.shape, S, x, hand)
        inter = np.count_nonzero(m & mask); union = np.count_nonzero(m | mask)
        iou = inter / union if union else 0.0
        reg = (x[3] ** 2 + x[4] ** 2) / 400.0 * 0.02 + 0.02 * ((x[5] - 1) ** 2 + (x[6] - 1) ** 2)
        reg += 10 * sum(max(0, .45 - x[k]) + max(0, x[k] - 1.45) for k in (5, 6))
        # Joint limits: the elbow flexes one way (-25..165 deg); the wrist stays within +-60 deg.
        el, wr = math.degrees(wrap(x[1] - x[0])), math.degrees(wrap(x[2] - x[1]))
        reg += 0.002 * (max(0, -25 - el) + max(0, el - 165)) ** 2 / 10 + 0.002 * max(0, abs(wr) - 60) ** 2 / 10
        if prev is not None:
            reg += 0.01 * sum(wrap(x[k] - prev[k]) ** 2 for k in range(3))
        return 1 - iou + reg, iou

    def fit(self, mask, S, seeds, prev, rng):
        ys, xs = np.nonzero(mask); pad = 160
        x0, y0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
        x1, y1 = min(mask.shape[1], xs.max() + pad), min(mask.shape[0], ys.max() + pad)
        x0, y0 = int(min(x0, S[0] - 40)), int(min(y0, S[1] - 40))
        sub = mask[y0:y1, x0:x1]; So = (S[0] - x0, S[1] - y0)
        best = {}
        for hand in self.hands:
            for seed in seeds:
                mu = np.array(seed, float); sig = np.array([.5, .5, .5, 6, 6, .15, .15])
                for it in range(32):
                    pop = mu + rng.standard_normal((56, 7)) * sig; pop[0] = mu
                    sc = np.array([self.cost(sub, So, p, hand, prev)[0] for p in pop])
                    el = pop[np.argsort(sc)[:7]]; mu = el.mean(0); sig = np.maximum(el.std(0), [.004, .004, .004, .1, .1, .005, .005])
                c, iou = self.cost(sub, So, mu, hand, prev)
                if hand not in best or c < best[hand][0]:
                    best[hand] = (c, iou, mu)
        return best


def main():
    global SRC
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--frames', default=str(TAKE1)); ap.add_argument('--out', default='data/take1_tracks.json')
    ap.add_argument('--seed-guide', choices=['union', 'run2', 'run3', 'run4', 'run4s', 'run5', 'run6', 'run7'], default='union'); a = ap.parse_args(); SRC = a.frames
    rig_guide = load_json(PILOT / f'data/{a.seed_guide}_joints.json')['frames'] if a.seed_guide != 'union' else None
    pts0, rows = mw.track(SRC, FRAMES, CELL_SCALE, OFFSET)
    extra = track_extra(FRAMES)
    for f in range(FRAMES):
        rows[f].update(extra[f])
    base = rows[0]
    out = {'source': str(Path(SRC).parent.resolve().relative_to(ROOT)).replace('\\', '/'), 'seed_guide': a.seed_guide,
           'canvas': [640, 896], 'cell_scale': CELL_SCALE, 'offset': OFFSET, 'frames': []}
    K = {k: to_canvas(v) for k, v in K0_ARM.items()}
    m0 = arm_component(skin_mask(rgb(0)), base['neck'][0])
    sk = cv2.distanceTransform(m0, cv2.DIST_L2, 5)
    fitter = RigArmFit(float(2 * np.median(sk[sk >= np.percentile(sk[sk > 0], 75)])))
    rng = np.random.default_rng(20261007); prev = None
    for f in range(FRAMES):
        r = rows[f]
        # Torso rigid motion (rotation about the waist + translation) from neck and waist; scale ignored.
        th = ang(r['waist'], r['neck']) - ang(base['waist'], base['neck'])
        c, s = math.cos(th), math.sin(th)
        def torso(p):
            dx, dy = p[0] - base['waist'][0], p[1] - base['waist'][1]
            return (r['waist'][0] + dx * c - dy * s, r['waist'][1] + dx * s + dy * c)
        S = torso(K['shoulder'])
        mask = arm_component(skin_mask(rgb(f)), r['neck'][0])
        g = rig_guide[f] if rig_guide else guide_arm_joints(f)
        gseed = [ang(g['shoulder'], g['elbow']), ang(g['elbow'], g['wrist']), ang(g['wrist'], g['tip']), 0, 0,
                 dist(S, g['elbow']) / fitter.L[0], dist(g['elbow'], g['wrist']) / fitter.L[1]]
        kseed = [ang(K['shoulder'], K['elbow']), ang(K['elbow'], K['wrist']), ang(K['wrist'], K['tip']), 0, 0, 1, 1]
        seeds = [kseed] if f == 0 else [list(prev), gseed]
        fits = fitter.fit(mask, S, seeds, prev, rng)
        hand = min(fits, key=lambda h: fits[h][0]); cost, iou, x = fits[hand]; prev = x
        S2, E, W, t3 = fitter.joints(S, x)
        hl = (CONTRACT['hand'] if hand == 'open' else dist(K0_ARM['wrist'], K0_ARM['tip'])) * CELL_SCALE
        J = {'shoulder': S2, 'elbow': E, 'wrist': W, 'tip': (W[0] + hl * math.cos(t3), W[1] + hl * math.sin(t3))}
        def js(m_):
            a_, b_, c_, _ = fitter.joints(S, m_); return {'shoulder': list(a_), 'elbow': list(b_), 'wrist': list(c_)}
        diag = {'iou_vs_take_arm_mask': round(float(iou), 4), 'hand_drawing': hand,
                'angles_rad': [float(v) for v in x[:3]], 'shoulder_offset_canvas': [float(x[3]), float(x[4])],
                'segment_scale_vs_contract': [float(x[5]), float(x[6])],
                'per_hand': {h: {'cost': float(c_), 'iou': float(i_), 'angles_rad': [float(v) for v in m_[:3]],
                                 'shoulder_offset_canvas': [float(m_[3]), float(m_[4])],
                                 'segment_scale_vs_contract': [float(m_[5]), float(m_[6])], 'joints_canvas': js(m_)}
                             for h, (c_, i_, m_) in fits.items()},
                'shoulder_torso_canvas': [float(S[0]), float(S[1])]}
        ks = [k for k in r if k in base and k in mw.FEATURES]
        fig = mw.fit_scale([base[k] for k in ks], [r[k] for k in ks])
        out['frames'].append({
            'index': f, 'features_canvas': {k: [round(float(v[0]), 3), round(float(v[1]), 3)] for k, v in r.items()},
            'torso_rotation_rad': float(th), 'figure_scale': float(fig),
            'arm_canvas': {k: [round(float(v[0]), 3), round(float(v[1]), 3)] for k, v in J.items()},
            'arm_cell': {k: [round(float(c_), 3) for c_ in to_cell(v)] for k, v in J.items()},
            'rig_arm_fit': diag, 'arm_mask_px': int(mask.sum())})
        print('frame %2d iou %.3f hand %-4s angles %s  seg %.2f %.2f' % (
            f, iou, hand, ' '.join('%+7.1f' % math.degrees(v) for v in x[:3]), x[5], x[6]), flush=True)
    out['arm_width_canvas'] = fitter.w
    save_json(PILOT / a.out, out)


if __name__ == '__main__':
    main()
