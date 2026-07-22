#!/usr/bin/env python3
"""Prep NPC sprite art into Meshy-ready source images.

The friend cutouts are RGBA with transparent backgrounds; meshy_pipeline.py
flattens to RGB at submit time, which would turn transparency into black and
poison the generation. This tool composites each single-character sprite onto
a white card, trims the transparent border (with padding), and caps at 1024px
-> gen2/npc_src/<role>.png, the paths staged in gen2/meshy/tasks.json.

Pair sheets (pearl_friend, two_friends, wacky_chuck, mama_baby) are NOT
handled here: each figure must be cropped/generated as its own source first
(see NPC_3D_WORKORDER_2026-07-19.md), then added to SOURCES below.

Usage: python3 tools/prep_npc_sources.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "gen2", "npc_src")

# role -> single-character source art
SOURCES = {
    "daddy": "assets/characters/friends/daddy.webp",
    "huluu": "assets/characters/friends/huluu.png",
    "kareem": "assets/characters/friends/kareem.png",
    "flower_friend": "assets/characters/friends/flower_friend.png",
}

PAD = 48  # white breathing room around the trimmed figure


def prep(role, rel):
    im = Image.open(os.path.join(ROOT, rel)).convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop(bbox)
    card = Image.new("RGBA", (im.width + PAD * 2, im.height + PAD * 2),
                     (255, 255, 255, 255))
    card.alpha_composite(im, (PAD, PAD))
    card = card.convert("RGB")
    card.thumbnail((1024, 1024))
    out_path = os.path.join(OUT, role + ".png")
    card.save(out_path, "PNG")
    print(f"{role}: {rel} -> {os.path.relpath(out_path, ROOT)} {card.size}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for role, rel in SOURCES.items():
        prep(role, rel)
