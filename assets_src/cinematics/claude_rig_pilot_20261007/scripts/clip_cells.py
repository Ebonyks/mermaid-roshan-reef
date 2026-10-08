#!/usr/bin/env python3
"""Generated take -> 256 px RGBA game cells (whole frames only; no part edits).

For each 640x896 frame on the flat light-grey stage:
  * background colour = median of a 12 px border ring;
  * matte: background = the near-background region connected to the border plus enclosed
    near-background holes of >= 150 px (gaps between limbs); a 3 px soft band at the boundary
    takes alpha from the colour distance, and edge colours are un-blended from the background;
    one uniform 2.5 px erosion of the whole silhouette removes the opening image's upscale spread;
  * the whole frame is mapped back to the approved 256 px cell (cell = (canvas - OFFSET) / CELL_SCALE)
    with a premultiplied Gaussian pre-filter (sigma 0.45 x scale) and bilinear resampling.
  * --grade-to-k0: one per-channel gain and offset for the whole clip, fitted so the opaque interior of
    frames 0 and 40 matches the approved K0 cell, then applied identically to every cell (LTX renders
    the figure about 6 levels darker than K0, which pops when the game swaps the still sprite for the clip).
Every operation applies to the whole frame; nothing is cut, pasted or redrawn.
Writes <out>/cells/NNNN.png, <out>/atlas.png (8 columns of 256 px cells) and <out>/cells_report.json
with the frame-0 silhouette IoU against the approved K0 cell.

    python -I scripts/clip_cells.py <frames pattern %04d> <out dir> [--count 41] [--grade-to-k0]
"""
import argparse, json, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_common import CELL_SCALE, OFFSET, ATLAS, save_json

COLS = 8
ERODE = 2.5     # canvas px


def matte(rgb):
    h, w, _ = rgb.shape
    ring = np.concatenate([rgb[:12].reshape(-1, 3), rgb[-12:].reshape(-1, 3), rgb[:, :12].reshape(-1, 3), rgb[:, -12:].reshape(-1, 3)])
    bg = np.median(ring, 0)
    d = np.abs(rgb - bg).max(2)
    near = (d < 14).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(near, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    keep = np.zeros(n, bool)
    for k in range(1, n):
        keep[k] = k in border or (st[k, cv2.CC_STAT_AREA] >= 150 and np.median(d[lab == k]) < 8)
    bgm = keep[lab]
    soft = np.clip((d - 6.0) / 30.0, 0, 1)
    din = cv2.distanceTransform((~bgm).astype(np.uint8), cv2.DIST_L2, 3)     # inside the figure
    dout = cv2.distanceTransform(bgm.astype(np.uint8), cv2.DIST_L2, 3)       # inside the background
    a = np.where(~bgm, np.where(din > 3, 1.0, np.maximum(soft, 0.0)), np.where(dout <= 1.5, soft, 0.0))
    fg = np.where(a[..., None] > 0.04, (rgb - (1 - a[..., None]) * bg) / np.maximum(a[..., None], 1e-3), 0)
    # The opening image (K0 upscaled 3.2x) carries a ~0.6 cell-px outer spread; one uniform 2.5 canvas-px
    # alpha erosion over the whole silhouette brings frame 0 back to the K0 edge (IoU 0.94 -> 0.98).
    dt = cv2.distanceTransform((a > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    a = a * np.clip(dt - ERODE + 0.5, 0, 1)
    return np.clip(fg, 0, 255), a, bg


def to_cell(fg, a):
    s = CELL_SCALE
    pre = np.dstack([fg * a[..., None], a * 255]).astype(np.float32)
    pre = cv2.GaussianBlur(pre, (0, 0), 0.45 * s)
    M = np.float32([[s, 0, OFFSET[0]], [0, s, OFFSET[1]]])          # cell -> canvas (inverse map)
    c = cv2.warpAffine(pre, M, (256, 256), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    al = c[..., 3] / 255
    rgb = np.where(al[..., None] > 1e-3, c[..., :3] / np.maximum(al[..., None], 1e-3), 0)
    al = np.where(al < 2 / 255, 0, al)
    return np.dstack([np.clip(rgb, 0, 255), al * 255]).round().astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('frames'); ap.add_argument('out'); ap.add_argument('--count', type=int, default=41)
    ap.add_argument('--grade-to-k0', action='store_true')
    v = ap.parse_args(); out = Path(v.out); (out / 'cells').mkdir(parents=True, exist_ok=True)
    rows = (v.count + COLS - 1) // COLS
    atlas = np.zeros((rows * 256, COLS * 256, 4), np.uint8); bgs = []
    cells = []
    for i in range(v.count):
        rgb = np.array(Image.open(v.frames % i).convert('RGB'), np.float32)
        fg, a, bg = matte(rgb); bgs.append([round(float(x), 2) for x in bg])
        cells.append(to_cell(fg, a))
    k0rgba = np.array(Image.open(ATLAS).convert('RGBA'))[0:256, 0:256].astype(np.float32)
    grade = None
    if v.grade_to_k0:
        A, B = [], []
        for c in (cells[0], cells[-1]):
            m = (k0rgba[..., 3] > 250) & (c[..., 3] > 250)
            A.append(c[m, :3].astype(np.float32)); B.append(k0rgba[m, :3])
        A, B = np.concatenate(A), np.concatenate(B)
        grade = [np.polyfit(A[:, k], B[:, k], 1) for k in range(3)]
        for c in cells:
            g = np.stack([np.polyval(grade[k], c[..., k].astype(np.float32)) for k in range(3)], -1)
            c[..., :3] = np.where(c[..., 3:] > 0, np.clip(g, 0, 255).round(), 0).astype(np.uint8)
    for i, cell in enumerate(cells):
        Image.fromarray(cell).save(out / 'cells' / f'{i:04d}.png')
        atlas[(i // COLS) * 256:(i // COLS + 1) * 256, (i % COLS) * 256:(i % COLS + 1) * 256] = cell
    Image.fromarray(atlas).save(out / 'atlas.png')
    k0 = np.array(Image.open(ATLAS).convert('RGBA'))[0:256, 0:256, 3] > 127
    f0 = np.array(Image.open(out / 'cells/0000.png'))[:, :, 3] > 127
    iou = float((k0 & f0).sum() / (k0 | f0).sum())
    save_json(out / 'cells_report.json', {'frames': v.count, 'source': v.frames, 'cell_scale': CELL_SCALE, 'offset': OFFSET,
                                          'atlas_columns': COLS, 'frame0_vs_K0_silhouette_iou': round(iou, 4),
                                          'grade_to_k0_gain_offset_rgb': [[round(float(x), 4) for x in g] for g in grade] if grade else None,
                                          'background_rgb_per_frame': bgs, 'used_as_delivery_pixels': False})
    print('cells', v.count, 'frame-0 silhouette IoU vs K0', round(iou, 4))


if __name__ == '__main__':
    main()
