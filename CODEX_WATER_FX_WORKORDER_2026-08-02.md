# Codex work order — shared water-FX animation vocabulary (2026-08-02)

Companion to `WATER_PHYSICS_EVALUATION_2026-08-02.md` (why) and
`CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md` (house style precedent).

The game is getting **one shared set of traditional, frame-by-frame water
effect animations** — splashes, ripples, bubbles — proc'd by every water
system (reef surface breach, the Jolt prop fleet + swell on underwater
promenades, lagoon rivers/moat, the fetch lake, and future bathtub-scale
interactions). Your bubble-bath atlas set is the quality and style
reference: this order scales that idiom from one room to the whole game.
Nothing here blocks on code — the engine's playback primitive lands
separately; every atlas drops in behind a spec table.

## House rules (binding, unchanged)

- Original Codex art restyled to ART_STYLE_GUIDE: pastel toy playset,
  navy/purple outlines, aqua/lavender shadows. Wind Waker is a rendering
  reference only.
- **No words, letters, or digits anywhere in a frame.**
- One ASSET_LICENSES.md line per file, in the commit that adds it.
- Never touch assets/book/, assets/audio/voices/,
  assets/characters/friends/.
- Power-of-two atlas sheets only (VRAM compression must stay legal).

## Atlas format (matches the proven bubble-bath convention)

- **Fixed pivot, deterministic playback**: every frame is drawn against
  the same anchor (the waterline contact point, marked below per item) so
  the engine can flipbook the grid with zero per-frame offsets — exactly
  like `bubble_bath_bathtub_atlas.png`.
- Grid packed left→right, top→bottom; unused trailing cells fully
  transparent.
- Alpha, hard-edged enough to survive alpha-scissor (2–3 px navy/purple
  outline; interior soft gradients are fine).
- Sheet sizes 1024×1024 (3×3, 4×2) or 1024×512 (4×2 small) — POT always.
- Timing is data, not art: the engine plays castle-style fixed
  `frame_duration`; suggested durations below are starting points.

### Palette (the continuity contract)

Draw all water from the family already shipping in the toon water and the
castle atlases — deep `#3389CC`-ish aqua, light `#80D1E6`, foam near-white
`#F2FBFF`, sparkle white, outline navy/purple. No new hues. This single
palette is what makes a splash in the reef, a ripple in the moat, and the
bathtub bubbles read as one game.

## The vocabulary — batch 1 (everything below, in this order)

| # | File (under `assets/sprites/fx_water/`) | Grid / frames | Pivot | Content |
|---|---|---|---|---|
| 1 | `fx_water_splash_small_atlas.png` | 1024×512, 4×2, 8 | bottom-center at waterline | A plink: small crown of water + 2–3 droplets + collapsing ring. For toy props, the fetch ball, river entry. ~0.08 s/frame. |
| 2 | `fx_water_splash_medium_atlas.png` | 1024×1024, 3×3, 8 | bottom-center | A real splash: crown, thrown droplets, foam burst, settle. For Chuck's lake landing, heavier props. ~0.10 s/frame. |
| 3 | `fx_water_splash_breach_atlas.png` | 1024×1024, 3×3, 8 | bottom-center | The hero moment: Roshan-scale water burst with arcing spray and sparkle dots, readable at full screen. Fires on reef surface breach (both directions). ~0.11 s/frame. |
| 4 | `fx_water_ripple_ring_atlas.png` | 1024×512, 4×2, 8 | center | A flat expanding ring + foam flecks, drawn face-on so it can lie on a water surface (the engine tilts the quad). For settle-on-water, wet footfalls, taps on water. ~0.12 s/frame. |
| 5 | `fx_water_bubble_burst_atlas.png` | 1024×512, 4×2, 8 | center | 4–6 pastel bubbles rising then popping to sparkles. Underwater counterpart of a splash: procs when something plunges *below* the surface. ~0.10 s/frame. |
| 6 | `fx_water_foamline_strip.png` | 1024×256, static (1 frame) | top edge = waterline | A tileable horizontal foam/meniscus band, sparse alpha. Dressing for waterlines on promenade murals and floating standees; the engine drifts it with the swell — do not paint motion into it. |

Small/medium/breach must read as **three sizes of the same splash** — same
crown silhouette, same droplet language, same foam — because the engine
picks the tier from impulse energy and the same event must always look
like the same thing.

## Acceptance

- Grid dimensions and POT sizes exactly as the table (a probe in the
  `probe_bathroom_props.gd` style will assert sheet size and grid).
- Fixed pivot verified: onion-skinning any two frames must keep the
  contact point stationary.
- Reads at gameplay scale on a 1280×720 phone screen: the small splash
  will render ~90 px tall, the breach ~300 px. Check silhouettes at those
  sizes, not at 1024.
- Saturation ≤ the standee foreground band (the audit tool's contrast rule
  §3.3): effects may sparkle, but they punctuate — they never out-shout a
  tap target for more than their ~0.8 s life.
- Day-neutral: one set only. Effects sit in every zone and both day/night
  palettes, so keep shading self-contained (no baked directional light).

## Explicitly out of scope

- No character art, no reworking the bubble-bath / mermaid-pool room
  atlases (they are the reference, they stay).
- No shader or particle work — this order is drawn frames only.
- No per-zone splash variants; one vocabulary serves the whole game. If a
  zone seems to need its own, that is a design conversation, not a batch-2
  item.
