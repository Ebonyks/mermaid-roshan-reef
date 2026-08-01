"""Prepare the 2D career-world goal props and placeholder scuffle imps.

Non-destructive, deterministic derivation (same contract as
prepare_opera_2d_worlds.py):

1. Twelve goal-prop sprites — one accepted flat-package gameplay card per
   career, navy presentation field removed, fitted into a 512x512 transparent
   canvas — written to assets/opera/worlds/props/goal_<career>.png. These are
   the "made thing" each act builds, which the imp captain steals in beat
   four and the stage finale wins back (OPERA_2D_REBUILD_2026-08-01.md).
2. Two BASIC PLACE-IN imp sprites (imp_mischief.png / imp_captain.png in
   assets/opera/worlds/actors/) drawn from simple shapes. They are throwaway
   placeholders: the codex regeneration list requests proper mischief-imp
   sprites at these exact paths, and the gesture surface falls back to its
   own vector imps if the files are absent.

Sources under assets_src/ are never modified. Re-running reproduces
byte-equivalent output.
"""

from __future__ import annotations

from pathlib import Path

from collections import deque

from PIL import Image, ImageDraw, ImageFilter

from prepare_opera_2d_worlds import _fit_actor

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "assets_src/concepts/opera_jobs_flat_2026-07-21/cards"
KEYS = ROOT / "assets_src/concepts/opera_jobs_2p5d_2026-07-24"
PROPS_OUT = ROOT / "assets/opera/worlds/props"
ACTORS_OUT = ROOT / "assets/opera/worlds/actors"
BACKDROPS_OUT = ROOT / "assets/opera/worlds/backdrops"

# career id -> accepted 2p5d scene key (owner decision 2026-08-01: these
# paintings ARE the runtime career backdrops; 1024x576 matches the 1280x720
# viewport aspect exactly and the 1024px-longest-side texture rule)
BACKDROP_KEYS = {
    "chef": "pastry_chef_2p5d_scene_key_2026-07-24.png",
    "detective": "detective_2p5d_scene_key_2026-07-24.png",
    "ballerina": "ballerina_2p5d_scene_key_2026-07-24.png",
    "candymaker": "candy_maker_2p5d_scene_key_2026-07-24.png",
    "doctor": "doctor_2p5d_scene_key_2026-07-24.png",
    "farmer": "farmer_2p5d_scene_key_2026-07-24.png",
    "boxer": "boxer_2p5d_scene_key_2026-07-24.png",
    "magician": "magician_2p5d_scene_key_2026-07-24.png",
    "painter": "painter_2p5d_scene_key_2026-07-24.png",
    "astronaut": "astronaut_engineer_2p5d_scene_key_2026-07-24.png",
    "racer": "racecar_driver_2p5d_scene_key_2026-07-24.png",
    "popstar": "pop_star_2p5d_scene_key_2026-07-24.png",
}

# shared bop-hit effect: the accepted boxer bubble-puff impact card
FX_PUFF_CARD = "opera_job_boxer_gameplay_bubble_puff_impact.png"


def _matte_card(source: Path) -> Image.Image:
    """Prop-card matting, stricter than the actor pipeline.

    1. Crop uniform caption/border bands from the top and bottom (they
       corrupt the corner field sample — the racer trophy failure).
    2. Flood the edge-connected navy field with a TIGHT color window so the
       fill cannot creep through dark costume shadows (the magician
       chew-hole failure).
    3. Remove enclosed field-colored pockets that have a solid core, so
       navy showing through gaps in the artwork goes too (the detective
       tiara failure) while thin navy outlines survive.
    """
    img = Image.open(source).convert("RGBA")
    px = img.load()
    w, h = img.size

    def row_uniform(y: int) -> bool:
        base = px[w // 2, y]
        hits = sum(
            1 for x in range(0, w, 8)
            if sum(abs(px[x, y][c] - base[c]) for c in range(3)) < 42
        )
        return hits >= (w // 8) * 0.92

    top = 0
    while top < h // 4 and row_uniform(top):
        top += 1
    bottom = h
    while bottom > h * 3 // 4 and row_uniform(bottom - 1):
        bottom -= 1
    img = img.crop((0, top, w, bottom))
    px = img.load()
    w, h = img.size

    corners = [px[6, 6], px[w - 7, 6], px[6, h - 7], px[w - 7, h - 7]]
    field = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    def is_field(p: tuple, window: int) -> bool:
        if max(p[0], p[1], p[2]) >= 94:
            return False
        return sum((p[i] - field[i]) ** 2 for i in range(3)) <= window * window

    mask = bytearray(w * h)
    queue: deque = deque()
    for x in range(w):
        for y in (0, h - 1):
            queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or mask[y * w + x]:
            continue
        near_edge = x < 26 or y < 26 or x >= w - 26 or y >= h - 26
        if not (is_field(px[x, y], 58) or (near_edge and is_field(px[x, y], 96))):
            continue
        mask[y * w + x] = 1
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                queue.append((x + dx, y + dy))

    # enclosed pockets: field-colored, unremoved, with a 9x9 solid core
    pocket = [
        1 if not mask[i] and is_field(px[i % w, i // w], 52) else 0
        for i in range(w * h)
    ]
    for y in range(4, h - 4):
        for x in range(4, w - 4):
            if not pocket[y * w + x]:
                continue
            core = all(
                pocket[(y + dy) * w + (x + dx)]
                for dx in range(-4, 5)
                for dy in range(-4, 5)
            )
            if not core:
                continue
            queue.append((x, y))
            while queue:
                qx, qy = queue.popleft()
                if qx < 0 or qy < 0 or qx >= w or qy >= h or mask[qy * w + qx]:
                    continue
                if not pocket[qy * w + qx]:
                    continue
                mask[qy * w + qx] = 1
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        queue.append((qx + dx, qy + dy))

    alpha = Image.new("L", (w, h), 255)
    alpha.putdata([0 if m else 255 for m in mask])
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.1))
    img.putalpha(alpha)
    bbox = img.getbbox()
    if bbox is None:
        raise SystemExit(f"matting removed everything: {source}")
    return img.crop(bbox)

# career id -> accepted gameplay card (the act's goal prop)
PROP_CARDS = {
    "chef": "opera_job_pastry_chef_gameplay_finished_cake.png",
    "detective": "opera_job_detective_gameplay_pearl_tiara.png",
    "ballerina": "opera_job_ballerina_gameplay_music_box.png",
    "candymaker": "opera_job_candy_maker_gameplay_wrapped_candy_reward.png",
    "doctor": "opera_job_doctor_gameplay_recovered_starfish.png",
    "farmer": "opera_job_farmer_gameplay_piggy_fed.png",
    "boxer": "opera_job_boxer_gameplay_championship_belt.png",
    "magician": "opera_job_magician_gameplay_bunny_fish_reveal.png",
    "painter": "opera_job_painter_gameplay_framed_sunrise.png",
    "astronaut": "opera_job_astronaut_engineer_gameplay_rocket_front.png",
    "racer": "opera_job_racecar_driver_gameplay_shell_trophy.png",
    "popstar": "opera_job_pop_star_gameplay_microphone_finale.png",
}

BODY = (122, 79, 154, 255)
BODY_DARK = (95, 58, 133, 255)
BELLY = (178, 140, 205, 255)
HORN = (232, 214, 168, 255)
HORN_STRIPE = (168, 121, 79, 255)
AMBER = (244, 182, 66, 255)
DARK = (51, 32, 63, 255)
GOLD = (224, 179, 76, 255)


def _draw_placeholder_imp(size: int, captain: bool) -> Image.Image:
    """A deliberately simple stand-in matching the runtime vector fallback."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = size // 2
    r = int(size * 0.30)
    body = BODY_DARK if captain else BODY
    # curled tail
    d.arc([c + int(r * 0.4), c + int(r * 0.1), c + int(r * 1.8), c + int(r * 1.4)],
          start=200, end=80, fill=body, width=size // 24)
    # striped horns
    for sign in (-1, 1):
        hx = c + sign * int(r * 0.62)
        hy = c - int(r * 1.05)
        hr = int(r * 0.38)
        d.arc([hx - hr, hy - hr, hx + hr, hy + hr], start=180, end=40,
              fill=HORN, width=size // 20)
        d.arc([hx - hr, hy - hr, hx + hr, hy + hr], start=250, end=330,
              fill=HORN_STRIPE, width=size // 20)
    # body and belly
    d.ellipse([c - r, c - r, c + r, c + r], fill=body)
    br = int(r * 0.55)
    d.ellipse([c - br, c - int(r * 0.1), c + br, c + int(r * 0.95)], fill=BELLY)
    # amber eyes
    for sign in (-1, 1):
        ex = c + sign * int(r * 0.34)
        ey = c - int(r * 0.22)
        er = int(r * 0.17)
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=AMBER)
        pr = int(r * 0.08)
        d.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=DARK)
    # friendly fanged grin
    mr = int(r * 0.34)
    d.arc([c - mr, c - int(r * 0.1), c + mr, c + int(r * 0.55)],
          start=20, end=160, fill=DARK, width=size // 40)
    fw = size // 40
    for sign in (-1, 1):
        fx = c + sign * int(r * 0.18)
        fy = c + int(r * 0.36)
        d.polygon([(fx - fw, fy), (fx + fw, fy), (fx, fy + fw * 2)],
                  fill=(255, 255, 255, 255))
    if captain:
        # plain gold waistband — no shell, pearl or crest motifs, ever
        d.rectangle([c - int(r * 0.80), c + int(r * 0.78),
                     c + int(r * 0.80), c + int(r * 0.94)], fill=GOLD)
    return img


def main() -> None:
    PROPS_OUT.mkdir(parents=True, exist_ok=True)
    ACTORS_OUT.mkdir(parents=True, exist_ok=True)
    BACKDROPS_OUT.mkdir(parents=True, exist_ok=True)
    for career, card in sorted(PROP_CARDS.items()):
        source = CARDS / card
        if not source.is_file():
            raise SystemExit(f"card not found: {source}")
        prop = _fit_actor(_matte_card(source), 512)
        out = PROPS_OUT / f"goal_{career}.png"
        prop.save(out)
        print(f"prop      {out.relative_to(ROOT)}")
    for career, key in sorted(BACKDROP_KEYS.items()):
        source = KEYS / key
        if not source.is_file():
            raise SystemExit(f"scene key not found: {source}")
        out = BACKDROPS_OUT / f"world_{career}.png"
        with Image.open(source) as img:
            img.save(out)  # verbatim pixels, new runtime path
        print(f"backdrop  {out.relative_to(ROOT)}")
    puff_source = CARDS / FX_PUFF_CARD
    if not puff_source.is_file():
        raise SystemExit(f"card not found: {puff_source}")
    puff = _fit_actor(_matte_card(puff_source), 512)
    puff_out = PROPS_OUT / "fx_bop_puff.png"
    puff.save(puff_out)
    print(f"fx        {puff_out.relative_to(ROOT)}")
    for name, captain in (("imp_mischief", False), ("imp_captain", True)):
        out = ACTORS_OUT / f"{name}.png"
        _draw_placeholder_imp(512, captain).save(out)
        print(f"imp       {out.relative_to(ROOT)} (basic place-in fallback)")


if __name__ == "__main__":
    main()
