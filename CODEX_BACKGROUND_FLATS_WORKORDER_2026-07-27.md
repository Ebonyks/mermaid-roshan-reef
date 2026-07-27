# Codex work order — promenade background flat sets (2026-07-27)

Companion to GAME_REDESIGN_2P5D_2026-07-27.md. The game is being redesigned
as 2.5D promenade stages, and **background sprites are now the game's
primary art** (owner decision 2026-07-27 — Codex 2D output is higher
quality than our Blender/Meshy 3D and takes the lead role). This order
defines the layer format once, then the per-zone shot lists.

The whole redesign's look lives or dies on these sets. Nothing here blocks
on code: the engine's layer stack is already merged, and every set can be
dropped in behind a config table.

## House rules (binding, unchanged)

- Original art (Codex-generated) or CC0-derived, restyled to ART_STYLE_GUIDE:
  pastel toy playset, rounded shapes, navy/purple outlines, aqua/lavender
  shadows, oversized child-readable props. Wind Waker is a rendering
  reference only.
- **No words, letters, or digits anywhere in a flat.** The player cannot
  read; text in a background teaches her that ignorable squiggles exist.
- One ASSET_LICENSES.md line per file, in the commit that adds it.
- Never touch assets/book/, assets/audio/voices/, assets/characters/friends/.

## The look (owner decision 2026-07-27, binding on every painting)

**A modernized, happy, 4-year-old Curse of Monkey Island.** Reference
only — no Monkey Island/LucasArts assets, characters, designs or music.
Four rendering rules implement it:

1. **Light is paint.** Bake light pools, god rays, window glow and
   lantern warmth into the murals. Nothing in a flat assumes a runtime
   light; the renderer will never add one.
2. **Atmospheric recession.** Per layer going back: roughly −15–20%
   saturation, lifted value toward the sky haze color, softer edges.
   Saturation and contrast peak at the walk band (L3 + standees). If a
   squinted composite doesn't separate into depth bands, it fails.
3. **Color script.** Each stage declares one dominant hue + one accent in
   its batch notes (reef: aqua-lavender + coral gold). Every layer of
   that stage obeys it.
4. **Happy inversion.** CMI's composition and light, never its grime or
   menace: pastel candy surfaces, cozy interiors, night as
   bioluminescent magic. Nothing scary at child eye level (unchanged).

## Animation deliverables (what to paint for motion)

Frames are paintings — the scarce resource. The engine animates
transforms on a stepped ~10 fps cel clock, so most motion needs NO extra
art:

- **Standees: one sprite each** (default). The engine bobs/sways them.
  Foliage-class standees should be painted with a clear base/root so
  ground-pivot sway looks right.
- **New named characters & hero props: paper-doll part sets** — 4–6
  pieces (body, head, arm(s), tail/prop) as separate PNGs on one POT
  sheet or as files, plus a one-line sidecar note giving pivot points.
  One painted pose; the engine does the acting.
- **Flipbooks only as a last resort**: ≤4 frames, ≤512 px, only the
  changing region (blink card, mouth card, splash). Never a full-body
  frame cycle — one 8-frame 1024² cycle costs more VRAM than an entire
  zone's murals.
- Opera "states, not poses" rule continues to apply to interactive props.

## Layer format (every zone uses this)

Back-to-front, per stage. PNG. **Power-of-two sizes only** so VRAM
compression is legal (CLAUDE.md texture rule):

| Layer | Name | Size (px) | Alpha? | `lock` | Content |
|---|---|---|---|---|---|
| L0 | `sky` | 1024×512 | **opaque** | 0.9–1.0 | Sky/water gradient, sun/moon, far haze. Rides the camera. |
| L1 | `far` | 2048×1024 | opaque* | 0.6 | Distant silhouettes: hills, reef wall, castle skyline. *Painted onto the L0 palette so it can stay opaque. |
| L2 | `mid` | 2048×1024 | alpha, ≤40% transparent px | 0.3 | The zone's identity dressing: coral heads, columns, market stalls, trees. |
| L3 | `skirt` | 2048×512 | **opaque** | 0.0 | The floor strip under the play plane: sand, tiles, boardwalk. Pinned to the stage. |
| L4 | `fore` | 2048×512 | alpha, **sparse** (≤15% painted px) | 0.0 | Optional foreground vignette: a frond, a rope, a shelf edge, framing top/bottom corners. Never mid-screen — it must not occlude Roshan or targets. |

### Standee sprites (the second half of every set — same priority as murals)

Owner note 2026-07-27: the redesign's look is **intentional layering of 2D
designs in 3D space** — a set is never one painting. Murals (the table
above) sit strictly behind the walk band and may never overlap Roshan.
Everything she can pass in front of, pass behind, stand at, or tap ships
as its own **standee**: an individual cutout sprite the engine stands at a
real depth in the stage (`SideScrollStage.flat()`), so the depth buffer
sorts her against it correctly as she moves.

- One PNG per object, alpha, POT (512×512, 512×1024 or 1024×1024), the
  **bottom edge of the painted art = the ground line** (the engine plants
  it there).
- Crisp 2–3 px navy/purple outline per the style guide — standees render
  alpha-scissor (hard edge), murals may keep soft edges.
- Per zone, deliver the standee inventory as separate files beside the
  mural layers: `assets/flats/<zone>/<stage>/standee_<zone>_<thing>.png`.
- **Nothing at band depth may be baked into a mural.** If a concept paints
  a counter, rock, or doorway where Roshan walks, that object must be cut
  out into a standee and the mural healed behind it. A mural "prop" at
  band depth is a layering bug and fails acceptance.
- Reef batch-1 standee inventory: market counter, 3 coral heads (small/
  med/large), kelp column, wreck bow, den mouth, 2 anemone clumps, plus
  the shared door cards below.

- **Overdraw budget (Mali GPU, hard):** at most TWO alpha layers per stage
  (L2 + L4). L0/L1/L3 must ship opaque. If a zone concept needs a third
  transparent layer, it needs a redesign, not an exception.
- Horizontal tiling: L0–L3 must tile seamlessly left-right (stages are
  2–4 screens wide; the engine repeats layers).
- Palette: day + optional night variant per zone (night = repaint, not a
  runtime tint — the day/night system swaps textures).
- Contrast rule: the play plane (L3 + lower third of L2) stays LOW detail
  and LOW saturation relative to characters and tap targets. Backgrounds
  frame; they never compete with the things a finger should find.

### Naming & landing zone

```
assets/flats/<zone>/<stage>/flat_<zone>_<stage>_L0_sky.png
assets/flats/<zone>/<stage>/flat_<zone>_<stage>_L1_far.png   … etc.
```

### Door cards & pointers (shared, batch 1)

Cross-cutting sprites every promenade needs — same priority as the first
zone set:

1. **Door cards** — oversized wordless archway/gate sprites, one per
   destination *type*: castle gate, minigame tent, shop awning, cave mouth,
   portal ring, stair arch, train platform. 512×1024 each, alpha. A door
   card + the destination's icon medallion is the entire wayfinding system.
2. **Icon medallions** — round pictogram badges (friend faces, kart,
   pearls, bed, opera mask…), 256×256, matching the medal/HUD icon style.
3. **Screen-edge arrow** — one soft golden chevron, 256×256, used by the
   off-screen objective pointer on the line.

## Batch 1 — Reef Promenade (the pilot; blocks P3)

The reef is one wide stage, morning-lit, reading left→right as: home
nook → friends' garden → market rock (Manta Pearl Shop) → wreck point →
race & brawl doors → rainbow portal.

- L0 sunbeam water gradient (aqua→lavender), soft god-ray bands, bubble
  drift band near the top.
- L1 far reef wall silhouette with the castle skyline glowing at the far
  right (the "that way to the castle" landmark — composition should pull
  the eye rightward).
- L2 identity dressing (background depth ONLY): distant coral banks,
  anemone drifts, the manta's market rock silhouette, the wreck seen
  behind the band. Leave clear "sockets" (unpainted low-detail zones)
  where live targets and standees stand: five friends, market counter,
  den mouth, portal — those are standees/cutouts/3D, never mural paint
  (see the standee rule above).
- L3 pale sand skirt with shell/starfish sprinkles at toy scale.
- L4 one kelp frond top-left, one coral shelf bottom-right.
- Night variant of L0/L1 only (bioluminescent accents).

## Batch 2 — Pearl Castle hall (two stages: hall, upper floor)

Interior warmth; blush/cream/gold. L2 sockets for: bed, wardrobe, craft
easel, music bells, golden stand, Daddy's chest, dungeon door, opera door,
balcony arch. Chandeliers live in L2 (painted, never lit — no OmniLights).

## Batch 3 — Courtyard (train visible in L1 loop) · Batch 4 — Sky Lagoon
(3 stages: lagoon shore, alpine route, gate terrace) · Batch 5 — Northern
kingdom · Batch 6 — Ember Fortress / Butterfly World

Shot lists for 3–6 will be issued per zone as its migration branch opens;
do not start them speculatively — the reef pilot's device test may revise
the layer spec.

## Acceptance (per set)

1. Files POT-sized, named, licensed as above; alpha budgets respected.
2. A composite mock (all layers stacked at rest) attached to the PR — the
   diorama must read at M11 size: squint test = you can still find every
   socket.
3. No text, no fail-state imagery, nothing scary at child eye level.
4. The style audit pass (ART_SCORING_GOVERNANCE) scores the set as one
   unit, not per-file.
