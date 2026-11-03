"""Numbers-only caption contrast gate for the chapter-one picture book.

For every text line the renderer recorded in a page_provenance.json, this
samples the caption-free source art under the line's box and reports the WCAG
relative-luminance contrast between the caption fill colour and that art.

  typical = contrast against the median background pixel
  worst   = contrast against the lightest 10% (white text) or the darkest
            10% (navy text) of background pixels

Verdicts (V34 handoff, work item W6):
  PASS              worst >= 3.0 and typical >= 4.5
  OUTLINE_REQUIRED  worst >= 3.0 but typical < 4.5: keep only with the heavier
                    navy outline, or move the line
  FAIL              worst < 3.0: move the line or change its colour

The thin navy outline on white captions is not counted, so white lines read
slightly better than their figures. The script writes no images.

Usage:
  python -B caption_contrast.py <landscape_dir> <page_provenance.json> [--out results.tsv]
"""
import argparse
import json
from pathlib import Path

from PIL import Image

WHITE_FILL = (255, 255, 249.9)
NAVY_FILL = (0.06 * 255, 0.16 * 255, 0.29 * 255)


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb[:3]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a, b):
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def measure(landscape, provenance):
    prov = json.loads(Path(provenance).read_text(encoding="utf-8"))
    images = {}
    rows = []
    for line in prov["text_lines"]:
        page = str(line["page"])
        x, y, w, h = line["box"]
        cx, cy = x + w / 2, y + h / 2
        chosen = None
        for layer in prov["layers"]:
            if str(layer["page"]) != page or layer.get("alpha") or "polygon" in layer["operation"]:
                continue
            tx, ty, tw, th = layer["target_box_points"]
            if tx - 0.5 <= cx <= tx + tw + 0.5 and ty - 0.5 <= cy <= ty + th + 0.5:
                chosen = layer  # later layers draw on top
        if chosen is None:
            rows.append(dict(page=page, text=line["text"], color=line["color"], size=line["font_size"],
                             layer="", typical=None, worst=None, verdict="NO_LAYER"))
            continue
        rel = chosen["file"]
        if rel not in images:
            images[rel] = Image.open(Path(landscape) / rel).convert("RGBA")
        img = images[rel]
        sx0, sy0, sx1, sy1 = chosen["source_box_pixels"]
        tx, ty, tw, th = chosen["target_box_points"]
        kx, ky = (sx1 - sx0) / tw, (sy1 - sy0) / th
        box = (max(int(round(sx0 + (x - tx) * kx)), 0),
               max(int(round(sy0 + ((ty + th) - (y + h)) * ky)), 0),
               min(int(round(sx0 + (x + w - tx) * kx)), img.width),
               min(int(round(sy0 + ((ty + th) - y) * ky)), img.height))
        crop = img.crop(box)
        pixels = crop.get_flattened_data() if hasattr(crop, "get_flattened_data") else crop.getdata()
        lums = sorted(luminance(p) for p in pixels if p[3] > 200)
        if not lums:
            rows.append(dict(page=page, text=line["text"], color=line["color"], size=line["font_size"],
                             layer=chosen["source_key"], typical=None, worst=None, verdict="NO_PIXELS"))
            continue
        n = len(lums)
        median, dark10, light10 = lums[n // 2], lums[n // 10], lums[(9 * n) // 10]
        if line["color"] == "white":
            fill = luminance(WHITE_FILL)
            typical, worst = ratio(fill, median), ratio(fill, light10)
        else:
            fill = luminance(NAVY_FILL)
            typical, worst = ratio(fill, median), ratio(fill, dark10)
        if worst < 3.0:
            verdict = "FAIL"
        elif typical < 4.5:
            verdict = "OUTLINE_REQUIRED"
        else:
            verdict = "PASS"
        rows.append(dict(page=page, text=line["text"], color=line["color"], size=line["font_size"],
                         layer=chosen["source_key"], typical=round(typical, 2), worst=round(worst, 2),
                         verdict=verdict))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("landscape")
    parser.add_argument("provenance")
    parser.add_argument("--out")
    args = parser.parse_args()
    rows = measure(args.landscape, args.provenance)
    header = "page\tcolor\tsize_pt\ttypical\tworst\tverdict\tlayer\ttext"
    lines = [header] + [
        f"{r['page']}\t{r['color']}\t{r['size']}\t{r['typical']}\t{r['worst']}\t{r['verdict']}\t{r['layer']}\t{r['text']}"
        for r in rows
    ]
    text = "\n".join(lines) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("SUMMARY\t" + "\t".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
