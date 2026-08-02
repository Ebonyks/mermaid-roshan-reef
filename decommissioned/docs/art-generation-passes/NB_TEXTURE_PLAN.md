# Nano Banana Texture Plan — Mermaid Roshan Reef of Light

Goal: every texture in the game comes from Nano Banana (Gemini image generation),
matching the storybook's soft painterly pastel style, replacing the CC0 photo
textures (`up_*`, `Ground054_2K_*`, `Rock061_2K_*`) currently in
`assets/terrain/`.

## Status

- **No Nano Banana texture tiles exist yet** (checked Downloads' 512 Gemini
  images, gemini_originals_backup, and all project folders on 2026-07-11 —
  they are all book illustrations / character stickers).
- The game code is already funneled through a small number of texture slots
  (see table), so once tiles land in Downloads the swap is mechanical.

## How to generate

Paste each prompt below into Nano Banana. Every prompt already carries the
shared style block. Save/download each result — Claude will pick them up from
`/Downloads`, verify seamlessness, auto-derive normal + roughness maps, install
them as `assets/terrain/nb_<slot>_col.png`, rewire `main.gd`, and screenshot-
verify in-engine.

**Shared style block (already in each prompt):**
> seamless repeating texture tile, perfectly tileable on all four edges, flat
> even lighting, no shadows, no vignette, no border, top-down orthographic
> view, square 1:1, children's storybook watercolor style, soft pastel colors,
> gentle painterly grain

## The 10 texture slots

| # | Slot (file) | Used for | Nano Banana prompt |
|---|-------------|----------|--------------------|
| 1 | `nb_sand` | reef ocean floor | Fine smooth ocean-floor sand with faint ripple marks, pale aqua-beige, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 2 | `nb_rock` | reef rocks, wreck rocks, lagoon boulders, cavern floor | Weathered sea rock with soft layered strata, cool grey with warm sandy veins, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 3 | `nb_stone` | castle keep, battlements, turrets, hall walls + columns | Large dressed castle stone blocks in neat courses with thin mortar lines, pale cream-pink, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, straight-on orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 4 | `nb_marble` | grand hall + back-room floors, checker tiles | Polished marble floor tiles with soft veining, pearly white with lavender hints, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 5 | `nb_wood` | castle side-room floors, pier, dock, wreck planks, keep door | Smooth wooden planks with gentle grain and soft knots, warm honey brown, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 6 | `nb_grass` | lagoon hills, meadow arena floor, mossy boulders | Soft meadow grass, fresh spring green with tiny painted blades, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 7 | `nb_dirt` | race arena floor, lagoon terrain blend | Soft packed earth with tiny pebbles, warm light brown, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 8 | `nb_cobble` | path to the castle | Rounded cobblestone path stones with sandy joints, warm cream and grey, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 9 | `nb_snow` | snowy fetch minigame floor | Fresh untouched snow with soft drifts and tiny sparkles, bright white with pale blue shadows, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, top-down orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |
| 10 | `nb_roof` | turret + tower roofs | Overlapping clay roof shingles in neat rows, soft coral pink-red, seamless repeating texture tile, perfectly tileable on all four edges, flat even lighting, no shadows, no vignette, no border, straight-on orthographic view, square 1:1, children's storybook watercolor style, soft pastel colors, gentle painterly grain |

Optional extras (only if wanted): `nb_flagstone` (currently unused after the
marble checker swap), `nb_cliff` (Level-2 cliff face — currently up_cliff).

## Wiring notes (for the session that installs them)

- Color map only is enough: normal + roughness will be derived
  programmatically (height-from-luminance) and saved as `nb_<slot>_nrm.png`
  / `nb_<slot>_rgh.png`.
- After copying into `assets/terrain/`, run
  `Godot_console.exe --headless --path . --import` once or the `-s` probe
  cannot load the new files.
- Code slots to update in `scripts/main.gd` (search for these anchors):
  `_up_mat(` key names, `Ground054_2K_` (seabed), `Rock061_2K_` (all rocks +
  cavern arena floor), `up_snowsoft_col.jpg` (snow arena), `up_wood/grass/dirt`
  in `_arena_floor` calls, `up_grass/up_dirt` in the lagoon splat shader
  (`grass_t`/`dirt_t` shader params), `up_water_nrm` (river ripple normal).
- Verify with `scripts/probe_castle_shots.gd` (screenshots every retextured
  area) before declaring done.
