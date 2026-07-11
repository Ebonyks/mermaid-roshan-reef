#!/usr/bin/env python3
"""GEN2 turnaround generation — multi-view sheets for Meshy multi-image input.

Takes a role's winning variant (round-2 verdict first, else the audit's best
flaw-free round-1 pick) and asks nano banana for the SAME creature from the
missing camera angles. Consistent front/side/back views are what turn Meshy's
single-image guesswork into faithful geometry, and a limbs-clear front view
is what gives its auto-rigger a fighting chance (every single-view rig
attempt so far was rejected at pose estimation).

Key from .secrets/gemini_key or $GEMINI_API_KEY — never committed.
Usage:
  python3 tools/gen2_turnaround.py aquatic_clownfish aquatic_penguin ...
Writes gen2/turnarounds/<role>/{source,front,side,back}.png
"""
import base64
import glob
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "models/gemini-3-pro-image"
OUT = os.path.join(ROOT, "gen2", "turnarounds")

VIEWS = {
    "front": "seen directly from the FRONT, facing the viewer straight on, "
             "body symmetrical, limbs and fins clearly separated from the body",
    "side":  "seen in a direct LEFT SIDE view, a full flat profile",
    "back":  "seen directly from BEHIND, swimming away from the viewer",
}
PROMPT = (
    "Redraw THE SAME EXACT creature shown in the reference image from a "
    "different camera angle: {view}. Identical species, identical colors, "
    "identical markings, identical proportions, identical friendly "
    "storybook style with crisp thin black outlines - ONLY the camera "
    "angle changes. Neutral relaxed pose. SINGLE SUBJECT, fully in frame, "
    "centered, PLAIN SOLID WHITE background, no ground shadow, no text, "
    "no sparkles, no bubbles."
)


def key() -> str:
    p = os.path.join(ROOT, ".secrets", "gemini_key")
    if os.path.exists(p):
        return open(p).read().strip()
    return os.environ["GEMINI_API_KEY"]


def pick_source(role: str) -> str:
    r2 = json.load(open(os.path.join(ROOT, "gen2", "audit", "round2.json")))
    if role in r2 and str(r2[role].get("verdict", "")).startswith("KEEP:"):
        v = r2[role]["verdict"].split(":", 1)[1]
        return os.path.join(ROOT, "gen2", "generated", role, v + ".webp")
    best, score = None, (-1, -1)
    for f in glob.glob(os.path.join(ROOT, "gen2", "audit", "claude_*.json")):
        d = json.load(open(f))
        if role in d:
            for v, info in d[role]["variants"].items():
                s = (1 if not info["flaws"] else 0, info["usable"])
                if s > score:
                    score, best = s, v
    if best is None:
        raise SystemExit(f"no audited variant for {role}")
    return os.path.join(ROOT, "gen2", "generated", role, best + ".webp")


def gen_view(k: str, src_png: bytes, view_desc: str) -> bytes:
    body = {
        "contents": [{"parts": [
            {"inline_data": {"mime_type": "image/webp",
                             "data": base64.b64encode(src_png).decode()}},
            {"text": PROMPT.format(view=view_desc)},
        ]}],
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


def main() -> None:
    roles = sys.argv[1:]
    if not roles:
        raise SystemExit(__doc__)
    k = key()
    for role in roles:
        src = pick_source(role)
        odir = os.path.join(OUT, role)
        os.makedirs(odir, exist_ok=True)
        raw = open(src, "rb").read()
        with open(os.path.join(odir, "source" + os.path.splitext(src)[1]), "wb") as f:
            f.write(raw)
        print(f"[{role}] source: {os.path.relpath(src, ROOT)}")
        for name, desc in VIEWS.items():
            dst = os.path.join(odir, name + ".png")
            if os.path.exists(dst):
                print(f"    {name}: exists, skip")
                continue
            img = gen_view(k, raw, desc)
            with open(dst, "wb") as f:
                f.write(img)
            print(f"    {name}: {len(img) // 1024} KB")


if __name__ == "__main__":
    main()
