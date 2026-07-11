#!/usr/bin/env python3
"""GEN2 rainbow road tile — nano banana (gemini-3-pro-image).

Generates the painted, seamlessly-tiling rainbow tile the kart engine's
rainbow road wears (scripts/kart.gd ROAD_TEX). The road mesh maps the tile
once across the width (UV.x) and ~40 times along the loop (UV.y), so the
stripes must run HORIZONTALLY and the top edge must continue the bottom.

Makes 3 variants for the eyeball pick, enforces vertical seamlessness with
a 64px cross-fade, then installs the chosen one (default v1) as a 1024 POT
JPEG q88 per the terrain-tile conventions:
    assets/terrain/up_rainbowroad_col.jpg

Key from .secrets/gemini_key or $GEMINI_API_KEY — never committed.
Usage:
    python3 tools/gen2_rainbow_road.py            # generate 3 variants
    python3 tools/gen2_rainbow_road.py --pick v2  # install a variant

REMEMBER: add this line to ASSET_LICENSES.md in the same commit as the tile:
| assets/terrain/up_rainbowroad_col.jpg | GEN2 pipeline: painted rainbow road tile (Gemini/nano banana, kart_rainbow_road) | (c) Mermaid Roshan LLC - generated for this project | gen2/generated/kart_rainbow_road/ | seamless-blended, 1024 POT, JPEG q88 |
"""
import base64
import io
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "models/gemini-3-pro-image"
OUT = os.path.join(ROOT, "gen2", "generated", "kart_rainbow_road")
DEST = os.path.join(ROOT, "assets", "terrain", "up_rainbowroad_col.jpg")

PROMPT = (
    "A square seamless repeating texture tile of a magical rainbow race "
    "track surface, painted storybook style for a children's picture book. "
    "Soft flat horizontal bands of rose red, peach orange, buttery yellow, "
    "mint green, sky blue and lavender purple running edge to edge, with "
    "gentle painterly brush texture, tiny sparkling star flecks and a faint "
    "pearly shimmer. Rich saturated pastel colors on a MEDIUM brightness - "
    "never washed out or white. The pattern at the very top edge must "
    "continue perfectly from the very bottom edge so the tile repeats "
    "vertically without a visible seam. Flat orthographic view straight "
    "down, even lighting, no vignette, no border, no text, no objects."
)


def key() -> str:
    p = os.path.join(ROOT, ".secrets", "gemini_key")
    if os.path.exists(p):
        return open(p).read().strip()
    return os.environ["GEMINI_API_KEY"]


def gen(k: str) -> bytes:
    body = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        f"{API}/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": k})
    for attempt in range(4):
        try:
            resp = json.load(urllib.request.urlopen(req, timeout=180))
            for part in resp["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    return base64.b64decode(part["inlineData"]["data"])
            raise RuntimeError("no image part in response")
        except Exception as e:  # noqa: BLE001 — retry transient API failures
            if attempt == 3:
                raise
            print(f"    retry {attempt + 1}: {e}")
            time.sleep(8 * (attempt + 1))
    return b""


def seamless_vertical(im, blend: int = 64):
    # cross-fade the top rows into the bottom rows so UV.y tiling never seams
    from PIL import Image
    im = im.convert("RGB")
    w, h = im.size
    top = im.crop((0, 0, w, blend))
    bot = im.crop((0, h - blend, w, h))
    for y in range(blend):
        a = y / float(blend)          # 0 at the seam edge -> 1 inside
        row_t = bot.crop((0, y, w, y + 1))
        blended = Image.blend(row_t, top.crop((0, y, w, y + 1)), a)
        im.paste(blended, (0, y))
    return im


def install(variant: str) -> None:
    from PIL import Image
    src = os.path.join(OUT, variant + ".png")
    if not os.path.exists(src):
        raise SystemExit(f"{src} not found — run the generator first")
    im = Image.open(src)
    im = seamless_vertical(im)
    im = im.resize((1024, 1024), Image.LANCZOS)
    im.save(DEST, "JPEG", quality=88)
    print(f"installed {DEST} ({os.path.getsize(DEST) // 1024} KiB)")
    print("kart.gd picks it up automatically (ROAD_TEX). Re-import before running:")
    print("  $GODOT --headless --import .")
    print("Don't forget the ASSET_LICENSES.md line (see this file's docstring).")


def main() -> None:
    if "--pick" in sys.argv:
        install(sys.argv[sys.argv.index("--pick") + 1])
        return
    k = key()
    os.makedirs(OUT, exist_ok=True)
    for i in range(1, 4):
        print(f"  generating v{i}...")
        raw = gen(k)
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.save(os.path.join(OUT, f"v{i}.png"))
    print(f"3 variants in {OUT} — eyeball them, then:")
    print("  python3 tools/gen2_rainbow_road.py --pick v1")
    install("v1")


if __name__ == "__main__":
    main()
