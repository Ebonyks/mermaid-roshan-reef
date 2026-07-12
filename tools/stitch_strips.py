#!/usr/bin/env python3
"""Stitch audit frame renders into per-clip film-strip contact sheets.
Usage: python tools/stitch_strips.py <audit_out_dir>"""
import os, sys, glob
from PIL import Image

out = sys.argv[1]
fr = os.path.join(out, "frames")
clips = {}
for p in sorted(glob.glob(os.path.join(fr, "*_side.png"))) + sorted(glob.glob(os.path.join(fr, "*_front.png"))):
    base = os.path.basename(p)
    clip = base.rsplit("_f", 1)[0] + ("_front" if base.endswith("_front.png") else "")
    clips.setdefault(clip, []).append(p)
for clip, paths in clips.items():
    ims = [Image.open(p) for p in paths]
    w, h = ims[0].size
    cols = 8
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), (28, 28, 32))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    dst = os.path.join(out, f"strip_{clip}.png")
    sheet.save(dst)
    print("wrote", dst, f"({len(ims)} frames)")
