#!/usr/bin/env python3
"""Check that the game's outfits ride an animation clip consistently, and write the review copy.

Inputs: <clip>/atlas.png (base clip cells), <clip>/outfits/<name>_{ribbon,party,garden,disguise}.png
(baked by the production builder through scripts/bake_clip_outfits.sh), <clip>/pose_fit_clip.json.
Per outfit and frame it measures the clothing change (pixels that differ from the base cell): its
area, and its centroid relative to the bodice box. Across the clip the outfit should keep one size
(area spread) and stay on the bodice (centroid drift after removing the box motion).
Writes <clip>/cosmetics_report.json and <clip>/cosmetics_review.mp4
(base | ribbon | party | garden | disguise, 2x, 24 fps; H.264 viewing copy, PNG atlases authoritative).

    python -I scripts/cosmetics_review.py <clip dir> <source name>
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import save_json, load_json

KINDS = ('ribbon', 'party', 'garden', 'disguise')
COLS = 8


def cells(path, n):
    a = np.array(Image.open(path).convert('RGBA'))
    return [a[(i // COLS) * 256:(i // COLS + 1) * 256, (i % COLS) * 256:(i % COLS + 1) * 256] for i in range(n)]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('clip'); ap.add_argument('name'); v = ap.parse_args()
    clip = Path(v.clip); fit = load_json(clip / 'pose_fit_clip.json')['sources'][v.name]['cells']; n = len(fit)
    base = cells(clip / 'atlas.png', n)
    outs = {k: cells(clip / 'outfits' / f'{v.name}_{k}.png', n) for k in KINDS}
    rep = {'frames': n, 'outfits': {}}
    for k in KINDS:
        area, cen = [], []
        for i in range(n):
            d = np.abs(outs[k][i].astype(int) - base[i].astype(int)).max(2) > 8
            ys, xs = np.nonzero(d); x0, y0, x1, y1 = fit[i]
            area.append(int(d.sum()))
            cen.append([float(xs.mean() - (x0 + x1) / 2), float(ys.mean() - (y0 + y1) / 2)] if len(xs) else [np.nan, np.nan])
        area, cen = np.array(area, float), np.array(cen)
        rep['outfits'][k] = {'changed_px_per_frame': area.astype(int).tolist(),
                             'changed_px_spread_pct': round(float(100 * np.ptp(area) / area[0]), 1),
                             'centroid_vs_box_drift_px': round(float(np.nanmax(np.hypot(*(cen - cen[0]).T))), 2),
                             'frames_with_clothing': int((area > 0).sum())}
    save_json(clip / 'cosmetics_report.json', rep)
    for k, r in rep['outfits'].items():
        print(f"{k:9s} clothing on {r['frames_with_clothing']}/{n} frames, area spread {r['changed_px_spread_pct']}%, "
              f"drift on the bodice {r['centroid_vs_box_drift_px']} px")
    bg = np.array([200, 205, 214], np.float32)
    with tempfile.TemporaryDirectory() as t:
        for i in range(n):
            row = []
            for c in [base[i]] + [outs[k][i] for k in KINDS]:
                a = c[..., 3:4].astype(np.float32) / 255
                row.append((c[..., :3] * a + bg * (1 - a)).astype(np.uint8))
            im = cv2.resize(np.concatenate(row, 1), None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
            for j, s in enumerate(('base',) + KINDS):
                cv2.putText(im, f'{s} {i:02d}', (8 + 512 * j, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 40, 40), 1, cv2.LINE_AA)
            Image.fromarray(im).save(f'{t}/{i:04d}.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', f'{t}/%04d.png', '-c:v', 'libx264', '-crf', '14',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(clip / 'cosmetics_review.mp4')], check=True)


if __name__ == '__main__':
    main()
