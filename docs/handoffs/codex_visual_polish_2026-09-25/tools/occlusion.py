"""Occlusion pass: is every drawn castle object actually visible on screen?

For each inventory record, the object's own opaque pixels (its sampled region,
scaled to its window rect, tried as drawn and mirrored) are compared with the
full-window screenshot taken in the same frame. A visible object matches the
screen; an object hidden behind an opaque card does not. Low-visibility
objects are written to a review sheet so each one can be judged by eye.
"""
from __future__ import annotations

import glob
import json
import os

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
REG = os.path.join(OUT, "regions")
SHOTS = os.path.join(OUT, "shots")
REVIEW = os.path.join(OUT, "occlusion")
os.makedirs(REVIEW, exist_ok=True)

MATCH_DIFF = 40.0      # mean |RGB| difference under which a pixel "shows"
MIN_OPAQUE_PX = 400    # ignore tiny cards
FLAG_BELOW = 0.60      # visible fraction under which a record is reviewed


def visible_fraction(obj: np.ndarray, shot: np.ndarray, mask: np.ndarray) -> float:
    diff = np.abs(obj[..., :3].astype(np.int16) - shot[..., :3].astype(np.int16)).mean(axis=2)
    return float((diff[mask] < MATCH_DIFF).mean())


def main() -> None:
    shots: dict[str, np.ndarray] = {}
    rows = []
    for inv in sorted(glob.glob(os.path.join(OUT, "inventory_*.json"))):
        for rec in json.load(open(inv, encoding="utf-8"))["records"]:
            if not rec.get("region_file") or rec["class"] == "NinePatchRect":
                continue
            if rec["modulate_a"] < 0.9 or rec["texture"].startswith("generated:"):
                continue
            x, y, w, h = rec["window_rect"]
            if w < 8 or h < 8:
                continue
            scene = rec["scene"]
            if scene not in shots:
                p = os.path.join(SHOTS, scene + ".png")
                if not os.path.exists(p):
                    continue
                shots[scene] = np.asarray(Image.open(p).convert("RGB"))
            shot = shots[scene]
            H, W = shot.shape[:2]
            x0, y0 = int(round(x)), int(round(y))
            x1, y1 = int(round(x + w)), int(round(y + h))
            cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
            if cx1 - cx0 < 8 or cy1 - cy0 < 8:
                continue
            img = Image.open(os.path.join(REG, rec["region_file"])).convert("RGBA")
            ex = rec.get("extra", {})
            if ex.get("flip_v"):
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img = img.resize((x1 - x0, y1 - y0), Image.BILINEAR)
            best, best_img = -1.0, None
            for mirrored in (False, True):
                cand = img.transpose(Image.FLIP_LEFT_RIGHT) if mirrored else img
                if ex.get("flip_h"):
                    cand = cand.transpose(Image.FLIP_LEFT_RIGHT)
                arr = np.asarray(cand)[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
                mask = arr[..., 3] >= 250
                if mask.sum() < MIN_OPAQUE_PX:
                    break
                frac = visible_fraction(arr, shot[cy0:cy1, cx0:cx1], mask)
                if frac > best:
                    best, best_img = frac, arr
            if best < 0:
                continue
            rows.append({"scene": scene, "node": rec["node"].split("/")[-1], "class": rec["class"],
                         "texture": rec["texture"].replace("res://", ""), "z": rec["z"],
                         "window_rect": [cx0, cy0, cx1 - cx0, cy1 - cy0],
                         "material": rec["material"], "visible_frac": round(best, 3),
                         "_obj": best_img})
    rows.sort(key=lambda r: r["visible_frac"])
    flagged = [r for r in rows if r["visible_frac"] < FLAG_BELOW]
    print(f"records compared {len(rows)}; flagged under {FLAG_BELOW:.0%}: {len(flagged)}")
    for i, r in enumerate(flagged):
        print(f"{i:3d} {r['visible_frac']:.0%}  {r['scene']:28s} {r['node'][:34]:34s} z{r['z']:<4} "
              f"{r['texture'][-58:]}{'  [' + os.path.basename(r['material']) + ']' if r['material'] else ''}")
    # review sheets: object as drawn (on checker) | what the screen shows there
    tiles = []
    for i, r in enumerate(flagged):
        obj = Image.fromarray(r["_obj"], "RGBA")
        x, y, w, h = r["window_rect"]
        scr = Image.fromarray(shots[r["scene"]][y:y + h, x:x + w], "RGB")
        s = 200 / max(w, h)
        size = (max(1, int(w * s)), max(1, int(h * s)))
        chk = Image.new("RGBA", obj.size, (225, 225, 232, 255))
        chk.alpha_composite(obj)
        tile = Image.new("RGB", (430, 236), (40, 38, 70))
        tile.paste(chk.convert("RGB").resize(size), (10, 30))
        tile.paste(scr.resize(size), (220, 30))
        d = ImageDraw.Draw(tile)
        d.text((10, 6), f"#{i} {r['visible_frac']:.0%} {r['node'][:40]}", fill=(255, 255, 255))
        d.text((10, 18), r["scene"][:60], fill=(190, 186, 230))
        tiles.append(tile)
    per = 12
    for k in range(0, len(tiles), per):
        chunk = tiles[k:k + per]
        sheet = Image.new("RGB", (430 * 3, 236 * ((len(chunk) + 2) // 3)), (20, 18, 40))
        for j, t in enumerate(chunk):
            sheet.paste(t, ((j % 3) * 430, (j // 3) * 236))
        sheet.save(os.path.join(REVIEW, f"review_{k // per}.jpg"), quality=86)
    with open(os.path.join(OUT, "occlusion.json"), "w", encoding="utf-8") as f:
        json.dump([{k: v for k, v in r.items() if k != "_obj"} for r in rows], f, indent=1)


if __name__ == "__main__":
    main()
