#!/usr/bin/env python3
"""GEN2 polish lane - the scripted 'photo editing suite' pass.

sprite mode: white background -> clean alpha cutout (border flood-fill so
white INSIDE the subject survives), autocontrast against washed pastels,
tight crop with small margin. tile mode: forces seamless tiling via the
classic offset-and-blend, then equalizes luma so clumps repeat less.

Usage:
  python3 tools/polish_sprite.py sprite <in> <out.png>
  python3 tools/polish_sprite.py tile   <in> <out.png>
"""
import sys
from PIL import Image, ImageFilter, ImageOps


def sprite(src, dst):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # flood-fill white from every border pixel -> background mask
    from collections import deque
    px = im.load()
    bg = bytearray(w * h)
    q = deque()
    def near_white(p):
        return p[0] > 235 and p[1] > 235 and p[2] > 235
    for x in range(w):
        for y in (0, h - 1):
            if near_white(px[x, y]) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if near_white(px[x, y]) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and near_white(px[nx, ny]):
                bg[ny * w + nx] = 1; q.append((nx, ny))
    mask = Image.frombytes("L", (w, h), bytes(bytearray(0 if b else 255 for b in bg)))
    mask = mask.filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert("RGBA")
    out.putalpha(mask)
    bbox = mask.getbbox()
    if bbox:
        m = max(8, (bbox[2] - bbox[0]) // 40)
        out = out.crop((max(0, bbox[0]-m), max(0, bbox[1]-m),
                        min(w, bbox[2]+m), min(h, bbox[3]+m)))
    # gentle contrast lift against pastel wash (RGB only)
    r, g, b, a = out.split()
    rgb = ImageOps.autocontrast(Image.merge("RGB", (r, g, b)), cutoff=1)
    out = Image.merge("RGBA", (*rgb.split(), a))
    out.save(dst)
    print("sprite ->", dst, out.size)


def tile(src, dst):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # offset by half and blend the seams away
    off = Image.new("RGB", (w, h))
    off.paste(im.crop((w//2, h//2, w, h)), (0, 0))
    off.paste(im.crop((0, h//2, w//2, h)), (w//2, 0))
    off.paste(im.crop((w//2, 0, w, h//2)), (0, h//2))
    off.paste(im.crop((0, 0, w//2, h//2)), (w//2, h//2))
    # feathered cross mask over the (now centered) old seams
    mask = Image.new("L", (w, h), 0)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(mask)
    band = max(16, w // 12)
    dr.rectangle((w//2 - band, 0, w//2 + band, h), fill=255)
    dr.rectangle((0, h//2 - band, w, h//2 + band), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(band // 2))
    healed = Image.composite(im, off, mask)
    healed.save(dst)
    print("tile ->", dst, healed.size)


if __name__ == "__main__":
    {"sprite": sprite, "tile": tile}[sys.argv[1]](sys.argv[2], sys.argv[3])
