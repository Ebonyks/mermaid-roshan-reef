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

from PIL import Image, ImageDraw

from prepare_opera_2d_worlds import _fit_actor, _remove_edge_field

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "assets_src/concepts/opera_jobs_flat_2026-07-21/cards"
PROPS_OUT = ROOT / "assets/opera/worlds/props"
ACTORS_OUT = ROOT / "assets/opera/worlds/actors"

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
    for career, card in sorted(PROP_CARDS.items()):
        source = CARDS / card
        if not source.is_file():
            raise SystemExit(f"card not found: {source}")
        prop = _fit_actor(_remove_edge_field(source), 512)
        out = PROPS_OUT / f"goal_{career}.png"
        prop.save(out)
        print(f"prop  {out.relative_to(ROOT)}")
    for name, captain in (("imp_mischief", False), ("imp_captain", True)):
        out = ACTORS_OUT / f"{name}.png"
        _draw_placeholder_imp(512, captain).save(out)
        print(f"imp   {out.relative_to(ROOT)} (basic place-in)")


if __name__ == "__main__":
    main()
