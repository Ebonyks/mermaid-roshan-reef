# Combat feel & indicators — Codex asset generation handoff (2026-08-04)

Companion to `COMBAT_TUTORIAL_CODEX_ASSETS_2026-08-01.md` (the sparring class)
and `COMBAT_DIFFICULTY_AUDIT_2026-08-04.md` (why these exist).

The 2026-08-04 difficulty pass added four things the child must be able to
*see*, and shipped all four on **code-drawn placeholder presentation**:

| System | What ships today | What art would replace |
|---|---|---|
| SLICE band | `Line2D`, flat cream, round caps | a painted blade ribbon |
| Charge stages | three untextured spheres above the target | three painted lamps |
| Enemy health | small green spheres, snuffing to grey | painted hp lamps |
| Bop reach | a `TorusMesh` ring, tinted gold when lit | a painted reach decal |

Everything below is **presentation only**. Every integration point already
works without art and must keep working — the fallbacks are the current code
drawings, not error paths.

## Binding rules (do not deviate)

- **Art direction**: pastel toy playset, rounded geometry, toon shading,
  navy/purple outlines, oversized child-readable shapes (`CLAUDE.md`
  §Art direction, `ART_STYLE_GUIDE.md`). **No text baked into any art** — the
  player cannot read. No numerals either, including on the hp lamps.
- **Licensing**: owner-generated or CC0 only; every new file gets an
  `ASSET_LICENSES.md` row in the same commit that adds it.
- **Reuse before generating.** Each request names the reuse considered. Do not
  regenerate an existing approved asset.
- **Format**: PNG, RGBA where alpha is used, **power-of-two dimensions**
  (the headless importer deadlocks on NPOT + compress mode 2 — `CLAUDE.md`
  known issue). Mobile renderer on every platform; Lenovo Tab M11 budget.
- **These are HUD-frequency assets.** The ribbon and the lamps can be on
  screen many times a second during a fight. Keep them small (≤512), keep
  alpha simple, and prefer one sheet over many files where noted.
- **Honesty rule, specific to this handoff**: the ribbon art must not read as
  wider than the band it represents. The band is the hitbox
  (`HitEngine.SLASH_BAND = 54 px` either side); soft edges are welcome, but a
  glow that suggests reach the blade does not have is a lie the child will
  learn the hard way. Same for the reach ring: paint the ring, not a wide
  halo outside it.
- **Acceptance**: `GODOT=<godot> scripts/ci.sh` green. Closest gates:
  `probe_hit`, `probe_combat`, `probe_combat_tutorial`, `probe_partner`.

## Requests

| # | id / path | Size | What to generate | Reuse considered | Integration point + fallback |
|---|---|---|---|---|---|
| 1 | `assets/ui/combat/slash_ribbon.png` | 512×128, alpha | The blade's trail as a **horizontal** strip meant to stretch along a swipe: bright pearl-cream core, warm gold edge, tapering to nothing at BOTH short ends. Vertically it must fade out by the top and bottom edge — that fade IS the band boundary. Sparkle flecks welcome inside the core, none outside. | `_sparkle_burst` colours reused for the flecks; no existing streak/trail art in the repo. | `hit_engine.gd` `_draw_ribbon()` — set `ribbon.texture` + `texture_mode = LINE_TEXTURE_STRETCH`. Fallback: flat `Color(1.0, 0.93, 0.66, 0.55)` (current). |
| 2 | `assets/ui/combat/slash_ribbon_spent.png` | 512×128, alpha | Same silhouette as #1, drained: cool grey-lilac, no sparkle, visibly "out of puff". This is what a swipe inside the 0.9 s cooldown draws. It must read as *resting*, never as *wrong* — no red, no cross, no buzzer iconography. | Derived from #1; generate as a desaturated sibling in the same pass so the silhouettes match exactly. | Same call site, `spent` branch. Fallback: flat `Color(0.72, 0.74, 0.80, 0.30)` (current). |
| 3 | `assets/ui/combat/charge_lamp_sheet.png` | 512×128, alpha — 4 frames of 128×128 | The charge stage lamp in four states, left to right: **dim** (unlit pearl bead), **stage 1** lavender lit, **stage 2** gold lit, **stage 3** hot-pink lit and blazing. Round, glossy, thick navy outline, each a clear step brighter/bigger-feeling than the last. | `verb_chip_hold.png` (2026-08-01) is the lavender/gold/pink CHARGE identity — match its palette exactly so the chip and the lamps are obviously the same system. | `hit_engine.gd` `_build_charge_pips()` / `_light_charge_pip()` — swap the sphere meshes for billboarded `Sprite3D`s with `region_rect` per frame. Fallback: current spheres tinted by `CHARGE_COLORS`. |
| 4 | `assets/ui/combat/hp_lamp_sheet.png` | 256×128, alpha — 2 frames of 128×128 | The enemy hit-point lamp, two states: **full** (bright mint-green bead, glossy, navy outline) and **spent** (the same bead gone dark and matte, slightly deflated). Must read at ~16 px, since a row of three sits above an imp's head. | The chain-pip HUD uses the ⭐ glyph; a painted bead distinguishes "this enemy's health" from "your combo" — they must never be confused. | `hit_engine.gd` `show_hp_pips()` — billboarded `Sprite3D` per lamp. Fallback: current green/grey spheres. |
| 5 | `assets/ui/combat/reach_ring.png` | 512×512, alpha | A top-down soft ring decal for the courtyard floor: a clean ring band, pastel, with the inside almost entirely transparent (she must see the floor and the imps' feet through it). **Two tints are not needed** — supply one neutral pearl ring; the code tints it gold when lit and pale blue when resting. Nothing outside the ring's outer edge. | The castle sconce/affordance glows are square-ish hotspot art, wrong shape. No existing floor decal. | `brawl.gd` `_update_reach_ring()` — swap the `TorusMesh` for a textured quad lying flat. Fallback: current torus mesh. |
| 6 | `assets/castle/training/verb_chip_slice.png` | 256×256, alpha | Completes the verb-chip set (`verb_chip_tap`, `verb_chip_hold` exist): a mint/aqua round bubble crossed by a single confident gold swipe arc. Icon only, no text. | Matches #3/#4 of the 2026-08-01 handoff exactly in size, framing and gloss — this is a third sibling, not a new style. | Garnish beside the SLICE lesson's `show_msg` line when that lesson is written (see below). Fallback: none needed — decoration. |
| 7 | `assets/castle/training/ghost_hand_swipe.png` | 512×512, alpha | OPTIONAL. The existing `ghost_hand.png` posed for a swipe — same hand, same pearl-cream, angled as if mid-sweep with a faint motion smear behind the knuckles. Only worth generating as a cheap sibling of the approved hand; skip if it would mean redrawing the hand. | `ghost_hand.png` (approved 2026-08-01) is the demo finger; the tutorial's swipe demo can simply translate that same hand. | `combat_tutorial.gd` `DemoFinger` — texture swap during a SLICE demo. Fallback: the approved pointing hand, translated (perfectly acceptable). |

**Explicitly NOT requested**: damage numbers or any numeral art (non-reader);
any "miss"/"fail" iconography — a spent blade rests, it never scolds; a
distinct art set per enemy type for the hp lamps (one shared lamp keeps the
grammar legible); and any voice audio (family-recorded lines only, never
generated).

## Prompt seeds (Codex/Gemini image generation)

- **#1**: "horizontal glowing sword-swipe trail, pearl cream core with warm
  gold edges, tapering to points at both ends, soft fade at top and bottom,
  tiny sparkle flecks inside the core only, toon shading, storybook children's
  game, transparent background, no text, 512x128"
- **#2**: same prompt, "drained cool grey-lilac, no sparkle, soft and tired,
  still gentle and friendly"
- **#3**: "four round glossy bead lamps in a row, left to right: unlit pearl,
  glowing lavender, glowing gold, blazing hot pink, thick navy outline, toon
  shading, storybook toy style, transparent background, no text, 512x128"
- **#4**: "two round glossy bead lamps side by side, left bright mint green and
  glowing, right dark matte and deflated, thick navy outline, toon shading,
  transparent background, no text, 256x128"
- **#5**: "top-down soft glowing ring decal for a game floor, pale pearl,
  clean thin band, fully transparent inside and outside the ring, toon
  shading, storybook style, transparent background, no text, 512x512"
- **#6**: "round glossy bubble button, mint aqua, crossed by one confident
  gold swipe arc, toon shading, navy outline, transparent background, no text,
  256x256"

## After generation

1. Drop files at the exact paths above; power-of-two check; add
   `ASSET_LICENSES.md` rows in the same commit.
2. Wire each integration point behind `ResourceLoader.exists()` so every
   fallback above survives a missing file.
3. Run `GODOT=<godot> scripts/ci.sh` — all probes green before merge.
4. Capture the four indicators for the owner's visual pass: a swipe mid-ribbon,
   a hold at stage 2, an imp at 1 of 3 hp lamps, and the reach ring both lit
   and resting.

## Known code work this art does NOT cover

The SLICE currently has **no tutorial lesson**. The throne sparring class
teaches TAP → COMBO → CHARGE and graduates. Chip #6 and hand #7 are for a
fourth lesson that still has to be written in `combat_tutorial.gd`; until it
exists the slice is an undiscovered bonus verb rather than a taught one.
Tracked in `COMBAT_DIFFICULTY_AUDIT_2026-08-04.md` §6.4.
