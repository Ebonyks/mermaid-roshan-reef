# Combat tutorial — Codex asset generation handoff (2026-08-01)

The INTRODUCTION TO COMBAT is live on `codex/tap-combat-feel`
(`scripts/combat_tutorial.gd`): touching the Royal throne in the castle
Main Hall opens a sparring class — one friendly imp, lessons TAP → 1-2-3
COMBO → three-stage CHARGE → partner bubble → graduation wave, each taught
by a pause-and-demonstrate golden pointer + looping ghost-finger animation.
It ships fully playable on placeholder presentation (flat dojo colors, a
code-drawn ghost dot). This handoff lists the art that would dress it.

## Binding rules (do not deviate)

- **Art direction**: pastel toy playset, rounded geometry, toon shading,
  navy/purple outlines, oversized child-readable props (`AGENTS.md`
  §Art direction, `ART_STYLE_GUIDE.md`). NO text baked into art — the
  player cannot read.
- **Licensing**: owner-generated or CC0 only; every new file gets an
  `ASSET_LICENSES.md` row in the same commit.
- **Art-finalization mode**: reuse before generating. Each request below
  names the reuse that was considered and why a gap remains. Do not
  regenerate any existing approved asset.
- **Format**: PNG, RGBA only where alpha is used, **power-of-two
  dimensions** (the headless importer deadlocks on NPOT + compress
  mode 2 — `AGENTS.md` known issue). Mobile renderer, Lenovo Tab M11
  budget: keep each sheet ≤ 2048×2048, prefer 1024.
- **Placement**: new files under `assets/castle/training/`. Derived
  variants of existing art go to NEW paths with attribution preserved.
- **Acceptance**: `GODOT=... scripts/ci.sh` stays green (probe_combat_tutorial,
  probe_crown, probe_castle_pearl_art are the closest gates); the tutorial
  must still run when any of these files is absent — every integration
  point keeps its current code fallback.

## Requests

| # | id / path | Size | What to generate | Reuse considered | Integration point + fallback |
|---|---|---|---|---|---|
| 1 | `assets/castle/training/training_grotto_backdrop.png` | 2048×1024, opaque | The sparring grotto: a cozy underwater training nook in lavender/periwinkle pastels — rounded coral pillars, a rack of toy bubble-wands, soft kelp pennants, gentle god-rays. Empty center stage (the 3D octagon sits in front). Storybook depth, no characters, no text. | Arena backdrops are flat env colors today; no existing backdrop fits the lavender dojo palette. | `combat_tutorial.gd` `_build_stage()` — add a backdrop quad at z ≈ −30 behind the octagon (SideScrollStage "backdrop" idiom). Fallback: current flat `Color(0.13, 0.10, 0.22)` environment stays. |
| 2 | `assets/castle/training/ghost_hand.png` | 512×512, alpha | A chubby, friendly child's hand with a pointing finger, storybook-outlined, slight glow — neutral skin-tone-free (mermaid-pearl cream), reads at 64 px. This becomes the demo "finger" that acts out taps/holds. | The opera ghost-finger is a code-drawn dot (deliberate); a real little hand reads better for brand-new players. | `combat_tutorial.gd` `DemoFinger._draw()` — draw_texture centered at `anchor` under the halo. Fallback: the current drawn dot + halo stays (identical choreography). |
| 3 | `assets/castle/training/verb_chip_tap.png` | 256×256, alpha | Decorative chip: hot-pink round bubble with a soft ⭐ impression (the TAP identity from COMBO_SYSTEM). Icon-only, no text. | Emoji glyphs render in UI already; a painted chip matches the storybook UI cards better. | Optional garnish beside `show_msg` lesson lines. Fallback: none needed — decoration only. |
| 4 | `assets/castle/training/verb_chip_hold.png` | 256×256, alpha | Decorative chip: lavender calm bubble wrapped by a gold→pink gradient ring arc (the three-stage CHARGE identity). Icon-only, no text. | Same as #3. | Same as #3. |
| 5 | `assets/castle/training/sparring_imp_band.png` | 512×512, alpha | OPTIONAL, derived-variant only: the existing mischief-imp face sheet with a tiny white training headband, so the classroom imp reads "practice buddy". Only worth doing as a cheap derivative of the existing imp art with attribution preserved; skip if it would mean repainting the imp. | The tutorial reuses the standard `DungeonArt` imp today — perfectly acceptable. | `combat_tutorial.gd` `_spawn_imp()` — texture swap on the imp head part if present. Fallback: standard imp (current behavior). |

**Explicitly NOT requested**: a throne tap-prompt overlay (the hall's ✦
symbol + hotspot system already advertises the throne), any verb
demonstration ANIMATION frames (owner 2026-07-25: prompts are looping
demonstration animations performed in code — fingertip press, drumming,
sustained hold — static glyphs are decoration only), and any voice audio
(family-recorded lines only, never generated).

## Prompt seeds (Gemini/Codex image generation)

- #1: "storybook children's game backdrop, underwater training grotto,
  pastel lavender and periwinkle, rounded coral pillars, toy bubble wand
  rack, soft kelp banners, gentle light rays, toon shading, thick navy
  outlines, empty center floor, no characters, no text, 2048x1024"
- #2: "cute chubby cartoon child hand pointing with one finger, pearl
  cream color, thick navy outline, soft glow, storybook toy style, plain
  transparent background, no text, 512x512"
- #3/#4: "round glossy bubble button, [hot pink with soft star | lavender
  with gold-to-pink ring arc], toon shading, navy outline, transparent
  background, no text, 256x256"

## After generation

1. Drop files at the exact paths above; power-of-two check; add
   `ASSET_LICENSES.md` rows.
2. Wire the two real integration points (#1 backdrop quad, #2 demo hand)
   behind `ResourceLoader.exists()` so the fallbacks survive.
3. Run `GODOT=<godot> scripts/ci.sh` — all probes green before merge, per
   `AGENTS.md`. Screenshot the tutorial (probe screenshot pattern) for the
   owner's visual pass.
