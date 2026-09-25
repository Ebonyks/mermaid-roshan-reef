"""Transparency / cut-off analyzer for the castle inventory (scratch only).

Reads out/inventory_*.json and out/regions/*.png written by inventory.gd,
measures every sampled region, and writes out/findings.json plus evidence
images. Heuristics are deliberately conservative; every flag is reviewed by
eye before it reaches the report.
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
EVID = os.path.join(OUT, "evidence")
os.makedirs(EVID, exist_ok=True)

VISIBLE = 32
OPAQUE = 200


def load_records():
    recs = []
    for path in sorted(glob.glob(os.path.join(OUT, "inventory_*.json"))):
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        recs.extend(doc["records"])
    return recs


def is_background(rec, w, h):
    role = rec.get("meta_role", "")
    tex = rec.get("texture", "")
    if "background" in role or "background" in tex.lower() or "main_hall_room_led" in tex:
        return True
    wr = rec.get("window_rect", [0, 0, 0, 0])
    return wr[2] * wr[3] > 0.30 * 2560 * 1369


def analyze_region(img: Image.Image):
    rgba = np.asarray(img.convert("RGBA")).astype(np.int32)
    a = rgba[..., 3]
    h, w = a.shape
    vis = a >= VISIBLE
    res = {"w": w, "h": h, "visible_frac": float(vis.mean()),
           "min_alpha": int(a.min()), "has_alpha": bool(a.min() < 250)}
    if vis.sum() == 0:
        res["empty"] = True
        return res, {}
    masks = {}
    # 1. border touch (cut-off): longest run of visible pixels along each edge
    border = {}
    for side, line in (("top", vis[0, :]), ("bottom", vis[-1, :]),
                       ("left", vis[:, 0]), ("right", vis[:, -1])):
        run = best = 0
        for v in line:
            run = run + 1 if v else 0
            best = max(best, run)
        border[side] = {"run": int(best), "frac": float(line.mean()),
                        "len": int(line.size)}
    res["border"] = border
    edge = np.zeros_like(vis)
    edge[0, :] = vis[0, :]
    edge[-1, :] = vis[-1, :]
    edge[:, 0] |= vis[:, 0]
    edge[:, -1] |= vis[:, -1]
    masks["border"] = ndimage.binary_dilation(edge, iterations=2) & vis
    # 2. components: main silhouette vs stray fragments
    lab, n = ndimage.label(vis, structure=np.ones((3, 3)))
    sizes = ndimage.sum(vis, lab, range(1, n + 1)) if n else []
    comps = sorted([(int(s), i + 1) for i, s in enumerate(sizes)], reverse=True)
    res["components"] = len(comps)
    strays = []
    if comps:
        main_area, main_id = comps[0]
        main_mask = lab == main_id
        dist_to_main = ndimage.distance_transform_edt(~main_mask)
        stray_mask = np.zeros_like(vis)
        for area, cid in comps[1:]:
            if area < 20:
                continue
            m = lab == cid
            ys, xs = np.nonzero(m)
            near_border = (ys.min() <= 6 or xs.min() <= 6 or ys.max() >= h - 7
                           or xs.max() >= w - 7)
            gap = float(dist_to_main[m].min())
            strays.append({"area": area, "gap_px": round(gap, 1),
                           "near_border": bool(near_border),
                           "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                           "rel_area": round(area / max(main_area, 1), 4)})
            if gap >= 3:
                stray_mask |= m
        masks["stray"] = stray_mask
        res["main_area"] = main_area
    res["strays"] = strays
    # 3. interior translucency (see-through holes inside the silhouette)
    filled = ndimage.binary_fill_holes(vis)
    interior = ndimage.binary_erosion(filled, iterations=3)
    holes = interior & (a < OPAQUE)
    hl, hn = ndimage.label(holes, structure=np.ones((3, 3)))
    if hn:
        hs = ndimage.sum(holes, hl, range(1, hn + 1))
        res["hole_components"] = int(hn)
        res["hole_speckles"] = int((np.asarray(hs) <= 4).sum())
        res["hole_largest"] = int(np.max(hs))
        res["hole_mean_alpha"] = float(a[holes].mean())
    res["interior_px"] = int(interior.sum())
    res["interior_translucent_px"] = int(holes.sum())
    res["interior_translucent_frac"] = float(holes.sum() / max(interior.sum(), 1))
    enclosed = filled & ~vis
    res["enclosed_transparent_px"] = int(enclosed.sum())
    masks["holes"] = holes | enclosed
    # 4. halo: partial-alpha rim colour vs the opaque colour just inside it
    rgb = rgba[..., :3].astype(np.float32) / 255.0
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    rim = vis & (a < 230) & ndimage.binary_dilation(~vis, iterations=1)
    inner = (a >= 250) & ndimage.binary_dilation(rim, iterations=3) & ~rim
    if rim.sum() >= 30 and inner.sum() >= 30:
        res["rim_lum"] = float(lum[rim].mean())
        res["inner_lum"] = float(lum[inner].mean())
        res["halo_delta"] = res["rim_lum"] - res["inner_lum"]
    masks["rim"] = rim
    # 5. baked checkerboard / matte box on the outer ring
    ring = np.zeros_like(vis)
    k = max(2, min(8, h // 10, w // 10))
    ring[:k, :] = ring[-k:, :] = True
    ring[:, :k] = ring[:, -k:] = True
    ring_op = ring & (a >= 250)
    res["ring_opaque_frac"] = float(ring_op.sum() / max(ring.sum(), 1))
    if ring_op.sum() > 50:
        c = rgba[..., :3][ring_op]
        neutral_light = (c.min(axis=1) >= 185) & ((c.max(axis=1) - c.min(axis=1)) <= 14)
        res["ring_neutral_light_frac"] = float(neutral_light.mean())
        res["ring_color_std"] = float(c.std(axis=0).mean())
    # 6. faint alpha dust in the transparent area
    faint = (a > 0) & (a < 16) & ~ndimage.binary_dilation(vis, iterations=4)
    res["faint_dust_px"] = int(faint.sum())
    return res, masks


def classify(rec, m):
    flags = []
    if m.get("empty"):
        return flags
    bg = rec["_bg"]
    wr = rec["window_rect"]
    st = rec.get("_stage", [0, 0, 2560, 1369])
    at_left = wr[0] <= st[0] + 4
    at_right = wr[0] + wr[2] >= st[0] + st[2] - 4
    at_top = wr[1] <= st[1] + 4
    at_bottom = wr[1] + wr[3] >= st[1] + st[3] - 4
    strip_sides = rec.get("_strip_sides", set())
    if not bg:
        if not m["has_alpha"]:
            flags.append(("opaque_box", "No transparency at all: draws as a rectangle"))
        for side, info in m["border"].items():
            screen_edge = {"left": at_left, "right": at_right, "top": at_top, "bottom": at_bottom}[side]
            if screen_edge or side in strip_sides:
                continue
            if info["run"] >= max(6, int(0.03 * info["len"])):
                flags.append(("cut_off_" + side,
                              f"Art runs into the {side} edge of its card ({info['run']} px of {info['len']})"))
        bled = [s for s in m["strays"] if s["gap_px"] >= 3 and s["near_border"] and s["area"] >= 20]
        if bled:
            biggest = max(bled, key=lambda s: s["area"])
            flags.append(("stray_fragment",
                          f"{len(bled)} detached fragment(s) at the card edge (largest {biggest['area']} px) - likely a neighbouring frame bleeding in"))
        loose = [s for s in m["strays"] if s["gap_px"] >= 6 and not s["near_border"] and s["area"] >= 150]
        if loose:
            flags.append(("loose_piece", f"{len(loose)} large detached piece(s) inside the card"))
        if m["interior_translucent_frac"] > 0.03 and m["interior_translucent_px"] > 250:
            speck = m.get("hole_speckles", 0)
            comps = max(m.get("hole_components", 1), 1)
            kind = "speckled (compression-style alpha noise)" if speck / comps > 0.6 and m.get("hole_largest", 0) < 400 else "solid translucent areas"
            flags.append(("see_through", f"{m['interior_translucent_frac']:.1%} of the silhouette is partly transparent ({m['interior_translucent_px']} px; {kind}; mean alpha {m.get('hole_mean_alpha', 0):.0f})"))
        hd = m.get("halo_delta")
        if hd is not None and hd > 0.20:
            flags.append(("light_halo", f"Edge rim is much lighter than the art inside it (+{hd:.2f} luminance)"))
        if hd is not None and hd < -0.30 and m.get("rim_lum", 1.0) < 0.06:
            flags.append(("black_matte_fringe", f"Near-black rim around the art ({m.get('rim_lum', 0):.2f} luminance): matte left from a dark background"))
        if m.get("ring_neutral_light_frac", 0) > 0.5 and m["ring_opaque_frac"] > 0.5:
            flags.append(("baked_background", "Opaque light-grey/white border ring: likely a baked checkerboard or matte"))
    return flags


def checker(w, h, s=8):
    yy, xx = np.mgrid[0:h, 0:w]
    c = (((xx // s) + (yy // s)) % 2).astype(np.uint8)
    base = np.where(c[..., None] == 1, np.array([205, 205, 214], np.uint8), np.array([238, 238, 244], np.uint8))
    return Image.fromarray(base, "RGB")


def evidence(rec, region_img, masks, name):
    w, h = region_img.size
    scale = max(1, min(4, int(420 / max(w, h)) or 1))
    bg = checker(w, h).convert("RGBA")
    bg.alpha_composite(region_img.convert("RGBA"))
    over = np.zeros((h, w, 4), np.uint8)
    for key, color in (("border", (255, 40, 40, 190)), ("stray", (255, 0, 220, 220)),
                       ("holes", (255, 210, 0, 170))):
        mk = masks.get(key)
        if mk is not None and mk.any():
            over[mk] = color
    ov = Image.fromarray(over, "RGBA")
    marked = bg.copy()
    marked.alpha_composite(ov)
    left = bg.resize((w * scale, h * scale), Image.NEAREST)
    right = marked.resize((w * scale, h * scale), Image.NEAREST)
    pair = Image.new("RGBA", (w * scale * 2 + 12, h * scale), (40, 38, 70, 255))
    pair.paste(left, (0, 0))
    pair.paste(right, (w * scale + 12, 0))
    pair.convert("RGB").save(os.path.join(EVID, name + "_asset.png"))
    shot_path = os.path.join(OUT, "shots", rec["scene"] + ".png")
    if os.path.exists(shot_path):
        shot = Image.open(shot_path).convert("RGB")
        x, y, ww, hh = rec["window_rect"]
        pad = max(24, int(0.25 * max(ww, hh)))
        box = (max(0, int(x - pad)), max(0, int(y - pad)),
               min(shot.width, int(x + ww + pad)), min(shot.height, int(y + hh + pad)))
        if box[2] > box[0] and box[3] > box[1]:
            crop = shot.crop(box)
            d = ImageDraw.Draw(crop)
            d.rectangle([int(x) - box[0], int(y) - box[1], int(x + ww) - box[0], int(y + hh) - box[1]], outline=(255, 60, 60), width=2)
            if crop.width < 380:
                f = 380 / crop.width
                crop = crop.resize((int(crop.width * f), int(crop.height * f)), Image.LANCZOS)
            crop.save(os.path.join(EVID, name + "_ingame.jpg"), quality=88)


def main():
    recs = load_records()
    by_region = defaultdict(list)
    for r in recs:
        if r.get("region_file"):
            by_region[r["region_file"]].append(r)
    stage = {}
    for r in recs:
        if "background" in r.get("texture", "") or "main_hall_room_led" in r.get("texture", ""):
            x, y, w, h = r["window_rect"]
            s0 = stage.get(r["scene"])
            box = [x, y, x + w, y + h]
            stage[r["scene"]] = box if s0 is None else [min(s0[0], box[0]), min(s0[1], box[1]), max(s0[2], box[2]), max(s0[3], box[3])]
    for r in recs:
        b = stage.get(r["scene"])
        if b:
            r["_stage"] = [b[0], b[1], b[2] - b[0], b[3] - b[1]]
    by_tex = defaultdict(list)
    for r in recs:
        by_tex[(r["scene"], r["texture"])].append(r)
    for group in by_tex.values():
        if len(group) < 2:
            continue
        for r in group:
            sides = set()
            x, y, w, h = r["sample_rect"]
            for o in group:
                if o is r:
                    continue
                ox, oy, ow, oh = o["sample_rect"]
                if abs((x + w) - ox) < 1.5 and abs(y - oy) < 1.5:
                    sides.add("right")
                if abs((ox + ow) - x) < 1.5 and abs(y - oy) < 1.5:
                    sides.add("left")
                if abs((y + h) - oy) < 1.5 and abs(x - ox) < 1.5:
                    sides.add("bottom")
                if abs((oy + oh) - y) < 1.5 and abs(x - ox) < 1.5:
                    sides.add("top")
            r["_strip_sides"] = sides
    findings = []
    stats = {"records": len(recs), "unique_regions": len(by_region)}
    for region_file, group in by_region.items():
        rep = max(group, key=lambda r: r["window_rect"][2] * r["window_rect"][3])
        path = os.path.join(OUT, "regions", region_file)
        img = Image.open(path)
        w, h = img.size
        rep["_bg"] = is_background(rep, w, h)
        metrics, masks = analyze_region(img)
        flags = classify(rep, metrics)
        if not flags:
            continue
        name = region_file[:-4]
        evidence(rep, img, masks, name)
        findings.append({
            "region_file": region_file,
            "texture": rep["texture"],
            "sample_rect": rep["sample_rect"],
            "class": rep["class"],
            "node": rep["node"],
            "scenes": sorted({g["scene"] for g in group}),
            "window_rect": rep["window_rect"],
            "flags": [{"code": c, "text": t} for c, t in flags],
            "metrics": metrics,
            "evidence": {"asset": name + "_asset.png", "ingame": name + "_ingame.jpg"},
        })
    findings.sort(key=lambda f: (f["texture"], str(f["sample_rect"])))
    with open(os.path.join(OUT, "findings.json"), "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "findings": findings}, f, indent=1)
    print("records", stats["records"], "unique", stats["unique_regions"], "flagged", len(findings))
    counts = defaultdict(int)
    for fd in findings:
        for fl in fd["flags"]:
            counts[fl["code"]] += 1
    print(dict(counts))


if __name__ == "__main__":
    main()
