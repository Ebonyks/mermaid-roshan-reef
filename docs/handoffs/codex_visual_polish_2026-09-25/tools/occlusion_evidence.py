"""Evidence images for the hidden-object findings (scratch only).

Each image pairs what the screen shows (a crop of the same-frame capture, with
the hidden object's drawn rectangle outlined in red) with the object's own
pixels as drawn at that spot, on a light checkerboard.
"""
from __future__ import annotations

import json
import os

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
EVID = os.path.join(OUT, "evidence")
BG = (40, 38, 70)


def record(inv: str, suffix: str) -> dict:
    for r in json.load(open(os.path.join(OUT, inv), encoding="utf-8"))["records"]:
        if r["node"].endswith(suffix):
            return r
    raise KeyError(suffix)


def checker(w: int, h: int, s: int = 10) -> Image.Image:
    yy, xx = np.mgrid[0:h, 0:w]
    c = (((xx // s) + (yy // s)) % 2).astype(np.uint8)
    base = np.where(c[..., None] == 1, np.array([205, 205, 214], np.uint8),
                    np.array([238, 238, 244], np.uint8))
    return Image.fromarray(base, "RGB").convert("RGBA")


def hidden_pair(inv: str, suffix: str, pad: float, tint=(1.0, 1.0, 1.0), height: int = 520) -> Image.Image:
    rec = record(inv, suffix)
    shot = Image.open(os.path.join(OUT, "shots", rec["scene"] + ".png")).convert("RGB")
    x, y, w, h = rec["window_rect"]
    p = pad * max(w, h)
    box = (int(max(0, x - p)), int(max(0, y - p)), int(min(shot.width, x + w + p)),
           int(min(shot.height, y + h + p)))
    crop = shot.crop(box)
    d = ImageDraw.Draw(crop)
    d.rectangle([x - box[0], y - box[1], x + w - box[0], y + h - box[1]], outline=(255, 40, 40), width=5)
    obj = Image.open(os.path.join(OUT, "regions", rec["region_file"])).convert("RGBA")
    if tint != (1.0, 1.0, 1.0):
        a = np.asarray(obj).astype(np.float32)
        a[..., 0] *= tint[0]
        a[..., 1] *= tint[1]
        a[..., 2] *= tint[2]
        obj = Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")
    obj = obj.resize((int(round(w)), int(round(h))), Image.LANCZOS)
    drawn = checker(crop.width, crop.height)
    drawn.alpha_composite(obj, (int(round(x - box[0])), int(round(y - box[1]))))
    dd = ImageDraw.Draw(drawn)
    dd.rectangle([x - box[0], y - box[1], x + w - box[0], y + h - box[1]], outline=(255, 40, 40), width=5)
    s = height / crop.height
    size = (int(crop.width * s), height)
    pair = Image.new("RGB", (size[0] * 2 + 14, height), BG)
    pair.paste(crop.resize(size, Image.LANCZOS), (0, 0))
    pair.paste(drawn.convert("RGB").resize(size, Image.LANCZOS), (size[0] + 14, 0))
    return pair


def panel_cover(inv: str, suffixes: list[str], box_px: tuple[int, int, int, int], width: int = 1000) -> Image.Image:
    shot = None
    crop = None
    for suffix in suffixes:
        rec = record(inv, suffix)
        if shot is None:
            shot = Image.open(os.path.join(OUT, "shots", rec["scene"] + ".png")).convert("RGB")
            crop = shot.crop(box_px)
        x, y, w, h = rec["window_rect"]
        ImageDraw.Draw(crop).rectangle([x - box_px[0], y - box_px[1], x + w - box_px[0], y + h - box_px[1]],
                                       outline=(255, 40, 40), width=5)
    s = width / crop.width
    return crop.resize((width, int(crop.height * s)), Image.LANCZOS)


def main() -> None:
    hidden_pair("inventory_free.json", "Animated_movie_picture", 0.9).save(
        os.path.join(EVID, "movie_picture_hidden.jpg"), quality=88)
    hidden_pair("inventory_d1_playroom.json", "BabyEagleRescuePointer", 2.2, tint=(1.0, 0.86, 0.32)).save(
        os.path.join(EVID, "rescue_pointer_hidden.jpg"), quality=88)
    panel_cover("inventory_free.json", ["Animated_sleepy_bunny", "Animated_shell_bunny"],
                (700, 760, 2200, 1369)).save(os.path.join(EVID, "panel_covers_hall_bunnies.jpg"), quality=88)
    panel_cover("inventory_d1_pool.json", ["DustBunny_mermaid_pool"],
                (100, 700, 1400, 1369)).save(os.path.join(EVID, "panel_covers_pool_bunny.jpg"), quality=88)
    for n in ("movie_picture_hidden", "rescue_pointer_hidden", "panel_covers_hall_bunnies", "panel_covers_pool_bunny"):
        im = Image.open(os.path.join(EVID, n + ".jpg"))
        print(n, im.size)


if __name__ == "__main__":
    main()
