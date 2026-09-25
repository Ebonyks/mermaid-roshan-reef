"""Every-cell sweep of the sprite sheets the castle draws (scratch only).

Cell sizes come from the runtime inventory (the rect each sheet was sampled
with) plus the Rumi atlases' documented grids. For every non-empty cell it
measures edge contact (cut-off) and detached pieces touching the cell edge
(neighbouring-frame bleed), then renders a marked contact sheet per sheet.
"""
from __future__ import annotations

import glob
import json
import os
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
REPO = r"C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/claude-new-game-20260923"
SHEETS_OUT = os.path.join(OUT, "sheets")
os.makedirs(SHEETS_OUT, exist_ok=True)
VIS = 32

MANUAL = {
    "res://assets/characters/rumi/rumi_eight_pose_runtime.png": (256, 384),
    "res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png": (256, 256),
    "res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_angry.png": (512, 512),
    "res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_flinch.png": (512, 512),
    "res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_implode.png": (512, 512),
    "res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_jump.png": (512, 512),
    "res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_laugh_vulnerable.png": (512, 512),
}


def cell_sizes():
    sizes = defaultdict(set)
    for path in glob.glob(os.path.join(OUT, "inventory_*.json")):
        doc = json.load(open(path, encoding="utf-8"))
        for r in doc["records"]:
            tex = r["texture"]
            if not tex.startswith("res://"):
                continue
            w, h = r["sample_rect"][2], r["sample_rect"][3]
            sizes[tex].add((round(w, 2), round(h, 2)))
    out = {}
    for tex, s in sizes.items():
        full = os.path.join(REPO, tex.replace("res://", ""))
        if not os.path.exists(full) or full.lower().endswith((".jpg", ".webp")):
            continue
        W, H = Image.open(full).size
        cells = [c for c in s if c[0] < W - 0.5 or c[1] < H - 0.5]
        if len(cells) == 1:
            out[tex] = cells[0]
    out.update(MANUAL)
    return out


def analyze_cell(a):
    vis = a >= VIS
    if vis.sum() < 50:
        return None
    h, w = vis.shape
    runs = {}
    for side, line in (("top", vis[0, :]), ("bottom", vis[-1, :]), ("left", vis[:, 0]), ("right", vis[:, -1])):
        best = run = 0
        for v in line:
            run = run + 1 if v else 0
            best = max(best, run)
        runs[side] = best
    lab, n = ndimage.label(vis, structure=np.ones((3, 3)))
    if n == 0:
        return None
    sizes = ndimage.sum(vis, lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    main_mask = lab == main
    dist = ndimage.distance_transform_edt(~main_mask)
    bleed_mask = np.zeros_like(vis)
    bleed_px = 0
    for cid in range(1, n + 1):
        if cid == main or sizes[cid - 1] < 20:
            continue
        m = lab == cid
        ys, xs = np.nonzero(m)
        near_edge = ys.min() <= 10 or xs.min() <= 10 or ys.max() >= h - 11 or xs.max() >= w - 11
        gap = dist[m].min()
        if (near_edge and gap >= 3) or (sizes[cid - 1] >= 150 and gap >= 6):
            bleed_mask |= m
            bleed_px += int(sizes[cid - 1])
    main_runs = {}
    for side, sl in (("top", (0, slice(None))), ("bottom", (-1, slice(None))),
                     ("left", (slice(None), 0)), ("right", (slice(None), -1))):
        line = main_mask[sl]
        best = run = 0
        for v in line:
            run = run + 1 if v else 0
            best = max(best, run)
        main_runs[side] = best
    return {"runs": runs, "main_runs": main_runs, "bleed_px": bleed_px,
            "bleed_mask": bleed_mask, "main_mask": main_mask}


def main():
    grids = cell_sizes()
    report = []
    for tex, (cw, ch) in sorted(grids.items()):
        full = os.path.join(REPO, tex.replace("res://", ""))
        img = Image.open(full).convert("RGBA")
        W, H = img.size
        cols, rows = int(round(W / cw)), int(round(H / ch))
        if cols * rows <= 1 or cols > 16 or rows > 16:
            continue
        arr = np.asarray(img)
        cells = []
        for r in range(rows):
            for c in range(cols):
                x0, y0 = int(round(c * cw)), int(round(r * ch))
                x1, y1 = int(round((c + 1) * cw)), int(round((r + 1) * ch))
                res = analyze_cell(arr[y0:y1, x0:x1, 3])
                if res is None:
                    continue
                limit = max(6, int(0.03 * min(x1 - x0, y1 - y0)))
                cut = [s for s, v in res["main_runs"].items() if v >= limit]
                cells.append({"cell": [c, r], "box": [x0, y0, x1, y1], "bleed_px": res["bleed_px"],
                              "cut_sides": cut, "_res": res})
        flagged = [c for c in cells if c["bleed_px"] >= 20 or c["cut_sides"]]
        entry = {"texture": tex, "size": [W, H], "cell": [cw, ch], "grid": [cols, rows],
                 "cells_used": len(cells),
                 "cells_with_bleed": sum(1 for c in cells if c["bleed_px"] >= 20),
                 "cells_cut": sum(1 for c in cells if c["cut_sides"]),
                 "flagged": [{k: v for k, v in c.items() if k != "_res"} for c in flagged]}
        report.append(entry)
        if flagged:
            sheet = Image.new("RGBA", img.size, (0, 0, 0, 0))
            yy, xx = np.mgrid[0:H, 0:W]
            chk = (((xx // 12) + (yy // 12)) % 2).astype(np.uint8)
            bg = np.where(chk[..., None] == 1, np.array([205, 205, 214, 255], np.uint8), np.array([240, 240, 246, 255], np.uint8))
            sheet = Image.fromarray(bg, "RGBA")
            sheet.alpha_composite(img)
            over = np.zeros((H, W, 4), np.uint8)
            for c in cells:
                x0, y0, x1, y1 = c["box"]
                res = c["_res"]
                sub = over[y0:y1, x0:x1]
                sub[res["bleed_mask"]] = (255, 0, 220, 230)
                for side in c["cut_sides"]:
                    if side == "top":
                        sub[0:3, :][res["main_mask"][0:3, :]] = (255, 40, 40, 230)
                    if side == "bottom":
                        sub[-3:, :][res["main_mask"][-3:, :]] = (255, 40, 40, 230)
                    if side == "left":
                        sub[:, 0:3][res["main_mask"][:, 0:3]] = (255, 40, 40, 230)
                    if side == "right":
                        sub[:, -3:][res["main_mask"][:, -3:]] = (255, 40, 40, 230)
            sheet.alpha_composite(Image.fromarray(over, "RGBA"))
            d = ImageDraw.Draw(sheet)
            for r in range(rows + 1):
                d.line([(0, int(r * ch)), (W, int(r * ch))], fill=(40, 90, 200, 255), width=2)
            for c in range(cols + 1):
                d.line([(int(c * cw), 0), (int(c * cw), H)], fill=(40, 90, 200, 255), width=2)
            name = os.path.basename(full).rsplit(".", 1)[0]
            sheet.convert("RGB").save(os.path.join(SHEETS_OUT, name + "_marked.jpg"), quality=86)
            entry["marked"] = name + "_marked.jpg"
    report.sort(key=lambda e: (-(e["cells_with_bleed"] + e["cells_cut"]), e["texture"]))
    with open(os.path.join(OUT, "sheet_sweep.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)
    for e in report:
        if e["cells_with_bleed"] or e["cells_cut"]:
            print(f"{e['texture'].replace('res://','')} grid {e['grid']} cell {e['cell']} used {e['cells_used']} bleed {e['cells_with_bleed']} cut {e['cells_cut']}")
    print("sheets swept", len(report))


if __name__ == "__main__":
    main()
