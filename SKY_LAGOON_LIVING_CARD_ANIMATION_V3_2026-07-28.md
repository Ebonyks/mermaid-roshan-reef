# Sky Lagoon Living-Card Animation — v3 Production Document (2026-07-28)

**For:** codex production. **Target stage:** `SkyLagoonPromenade`
(`scripts/arena/sky_lagoon_promenade.gd`, 6×2 Sprite3D promenade,
`codex/sky-lagoon-reductive-extraction` lineage, commit `08c9adaa`).
**Supersedes:** v2 (`SKY_LAGOON_LIVING_CARD_ANIMATION_V2_2026-07-28.md`).
v3 = v2's design language **plus** the concrete extraction inventory for
panorama v5, the isolation/heal/regeneration workflow, hard performance
budgets for the 3-year-old-Android-tablet floor, and the lighting
architecture (neutral-plate relight + light layers + time-of-day staging).
Where v2 and v3 differ, v3 wins.

**Mural facts (fixed):** native master `sky_lagoon_panorama_master_v5_hd_3x1.png`,
6144×2048, ratio 3.0. **Master hash of record:** the SHA-256 in the current
approved audit evidence (`audit/sky_lagoon_hd_grid.json`) — as of the
2026-07-29 implementation audit that is `017532ae…be41`, NOT the
`2de9b63d…` this document originally quoted from the stale `08c9adaa`
handoff. Never hardcode the hash from a document; read it from the evidence
JSON at work time and record which hash the work was performed against.
Runtime: 6×2 grid of non-overlapping 1024×1024 tiles
(`flat_sky_lagoon_main_panorama_v5_tile_rR_cC.png`), columns c0–c5 left→right
(x = c×1024), rows r0 (sky, y 0–1024) / r1 (ground, y 1024–2048).
**The native resolution is preserved through every step of this document —
no master downscale, no tile rescale, ever.**

---

## 0. Corrections from the 2026-07-29 implementation audit

The first implementation slice (wind envelope, night tint, cabin smoke,
contact shadow, teardown, living-card probe contract — see
`SKY_LAGOON_LIVING_CARD_V3_IMPLEMENTATION_AUDIT_2026-07-29.md` and
`LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` in the codex worktree) landed
with all applicable gates green. It surfaced these corrections, which
supersede the corresponding text below:

1. **Master hash mismatch (blocking for §2).** The E1–E6 boxes were derived
   against the `08c9adaa`-era master; the approved v5 master of record is
   `017532ae…be41`. **The §2a table is not to be executed until its boxes
   are re-derived/verified against the master of record** and re-approved.
   The E3-pilot-then-owner-review sequencing stands.
2. **Baseline counts.** "Current 43 nodes" was the stale handoff table. The
   measured live baseline before the slice was 31 revisit / 34 Day One
   (plane contributes 3 transient cards); §2's projected totals shift
   accordingly. The probe's measured inventory is always the authority over
   any count printed in a document — including this one.
3. **Determinism gate (gate 2) amended:** cold-build comparison is by
   complete placement/phase/motion **signature**, plus recorded day/night
   captures — not pixel-identical screenshots, which produce false
   negatives from renderer/driver timing.
4. **Smoke style (owner direction):** thin wisps, not discrete rounded
   puffs — a narrow S-ribbon card (~46×256) with a clear lavender
   edge/midtone, 3 staggered cards per column. Implemented and accepted
   (attempt 4). §2b's "puffs" wording is superseded; the northern stage
   inherits the wisp direction.
5. **Sway/brush-past are conditional features:** they activate only when a
   conforming extracted NEAR_Z card exists. Applying them before the
   extraction batch is impossible (painted foliage) or a violation
   (duplicate cards over the painting) — the design language now states
   this conditionality explicitly.

## 1. Architecture (carried from v2, binding)

- Sprite3D-only world art; no MeshInstance3D, no particles, no shaded cards.
- One bounded stage tick (`_tick_ambient_life`) over tagged ambient cards;
  no per-frame allocation; reactive motion is a comparison inside that tick.
- Every added card updates `probe_l2.gd`'s node-type inventory in the same PR.
- **Living card contract:** unshaded Sprite3D at a named depth plane
  (`CLOUD_Z −16` … `NEAR_Z −1.5`), baked ink outline + cel color, bottom-flush
  root anchor, measured aspect/content fraction, target world height, touch
  footprint if interactive, contact-shadow card when grounded, one motion
  class + one intensity class, deterministic phase
  (`wrapf(pos.x*0.73 + pos.z*1.31, 0, TAU)` — never `randf()`).
- **Motion layers:** ambient (weather/depth) → reactive (brush-past) →
  authored (playground, plane, castle door — already shipped, never diluted).
- **Wind state:** stage-owned direction sign + deterministic gust schedule;
  all ambient amplitudes multiply by it; reset on teardown.
- **Per-screen budget (hard):** 1 dominant moving landmark, ≤3 quiet loops,
  calm walk band and touch-target surroundings. Runway: water + Day One
  plane dominant. Playground: authored equipment dominant. Castle: door
  invitation dominant.

## 2. Extraction inventory — panorama v5, complete and closed

This is the full conversion list for this background. Nothing else gets
extracted without a new owner-approved revision of this table.

### 2a. Extractions (mural pixels → card, background healed behind)

Boxes are approximate master-space (x0,y0)–(x1,y1) for scoping; codex
measures exact bounds at isolation time (pad the matte generously, the heal
region is what's exact). Priority 1 = do; 2 = do if budget allows.

| # | Object | approx master box | tiles touched | depth | motion class | pri |
|---|---|---|---|---|---|---|
| E1 | Flora bank, far-left corner (lupine/fern cluster) | (0,1700)–(580,2048) | r1_c0 | NEAR_Z | foliage_near + reactive | 1 |
| E2 | Flora bank left of path, below easel 1 (foxglove/berry) | (1640,1610)–(2260,1985) | r1_c1+r1_c2 (boundary object) | NEAR_Z | foliage_near + reactive | 1 |
| E3 | Flora bank center (lily/berry cluster) | (3300,1655)–(3885,2015) | r1_c3 | NEAR_Z | foliage_near + reactive | 1 |
| E4 | Flora bank center-right (fern/foxglove) | (4080,1565)–(4640,2015) | r1_c3+r1_c4 (boundary object) | NEAR_Z | foliage_near + reactive | 2 |
| E5 | Lupine cluster by bridge posts | (5650,1305)–(6110,1675) | r1_c5 | NEAR_Z | foliage_near + reactive | 2 |
| E6 | One mid-size cloud, screen-2 sky | (3730,430)–(4000,540) | r0_c3 | CLOUD_Z | cloud drift | 2 |

Notes: E2 and E4 straddle tile joins — exactly the objects the AGENTS.md
boundary rule says to extract. E1–E5 sit in front of the walk band, so each
buys player occlusion + sway + brush-past: the highest depth-per-card value
in the painting. Each grounded extraction (E1–E5) also adds a
contact-shadow card — count 2 inventory nodes per flora bank.

### 2b. New ornament cards (no mural edit, no healing)

| # | Object | anchor | depth | motion class | pri |
|---|---|---|---|---|---|
| N1–N3 | 3 thin smoke wisps, one column (§0.4 — DONE 2026-07-29) | actual upper-cabin chimney, LANDMARK_Z-corrected y | LANDMARK_Z | smoke tween loop | 1 |
| N4–N5 | 2 emissive glints (castle window, one flower center) | castle facade / E3 bank | LANDMARK_Z / NEAR_Z | slow pulse | 2 |
| N6 | Sun-glow card (only if sunset feature ships) | horizon, mural plane | BACKDROP_Z+ε | authored (time-of-day) | opt |

**Explicitly NOT converted:** bridge, path, pond, stepping stones,
mountains, cabins themselves, all mid-ground bushes, the ~20 painted clouds
beyond E6. Static + non-interactive = stays painted, permanently.

**Resulting totals** (corrected per §0.2, measured baseline 31 revisit /
34 Day One): the full batch adds ~13 nodes (5 flora cards + 5 contact
shadows + 1 cloud + 2 glints; smoke already landed) → ~44 revisit / ~47
Day One. The probe's measured inventory is the authority. Inside every
budget in §5.

## 3. Isolation → heal → regenerate workflow (per extraction)

The card keeps the **approved pixels**; only the **healed background** is
regenerated. Never the reverse. Sequence per object, all at native master
resolution:

1. **Matte.** On a working copy of the v5 master, isolate the object at
   native resolution: alpha matte hugging the painted silhouette
   (`tools/polish_sprite.py` techniques apply; hand-refine the matte — these
   silhouettes sit on busy painted ground, flood-fill alone won't cut them).
   Export the card as RGBA PNG of the object's exact pixels. **The card is
   the original artwork — zero regeneration, zero repaint.**
2. **Card finishing** (art-pipeline lane): fringe-decontaminate over a dark
   swatch, crop bottom-flush to the root line, center stem, measure content
   fraction/aspect, pad to POT ≤1024 longest side, Fix Alpha Border ON,
   record manifest entry (depth, motion class, touch footprint n/a,
   contact-shadow dims).
3. **Heal.** Regenerate ONLY the pixels inside the extraction matte (+ a
   small feather margin) so the background continues seamlessly behind where
   the object stood — matching grass/path/sky context on all sides. This is
   the codex generative step. Gate, same as the stained-glass precedent:
   **changed pixels outside the declared heal bounds = 0**, verified by
   pixel diff against v5 and recorded in the evidence JSON.
4. **Master versioning.** All heals land on one new master:
   `sky_lagoon_panorama_master_v6_hd_3x1.png`, still exactly 6144×2048,
   ratio 3.0, new SHA-256 recorded. v5 stays in the repo untouched
   (never-overwrite rule). One master rev for the whole batch — do not
   version per object.
5. **Re-slice affected tiles only.** E1–E6 touch r1_c0, r1_c1, r1_c2,
   r1_c3, r1_c4, r1_c5, r0_c3 — regenerate those 1024² tiles from v6 with
   the same 115px overscan procedure; untouched tiles keep their v5 files.
   Tile filenames bump to `_v6_`; the builder's tile path constant updates
   once.
6. **Seam re-audit.** All five vertical joins + the horizontal join re-pass
   the seam ratio gate (≤2.0) — healing near a join can break a seam that
   passed in v5. Update `audit/sky_lagoon_hd_grid.json` + capture evidence.
7. **Reinsert at depth.** Place the card at its §2a depth plane with
   perspective-compensated height so the on-screen composition matches the
   approved v5 framing **pixel-for-pixel at the reference camera** (the
   congruency probe is the check: a before/after capture from the same
   camera must show the object in the same screen position, now parallaxing).
   Add contact shadow, motion class, phase token; update probe inventory.
8. **Batch order:** one priority-1 object end-to-end first (E3 is the
   cleanest — single tile, no join), through owner review, THEN the rest.
   Same pilot-first discipline as the card pipeline.

New-ornament cards (N1–N6) skip steps 1, 3–6 entirely: generate art per the
pipeline's stage-0 spec, finish per step 2, place per step 7.

## 4. Lighting architecture — neutral plate, light layers, time-of-day

There is no real lighting path on world art (unshaded Sprite3D by rule), so
runtime "lighting" = multiplicative grading (modulate), overlay cards, and
additive glows. Those grade cleanly only over a **neutral-lit plate** — the
v5 mural's baked daylight fights them (golden plate × dusk orange = mud).
The fix is decomposition, NOT de-lighting: a fully light-stripped painting
would look dead and nothing in the engine could relight it.

### 4a. The distinction that governs everything

- **Form shading** — volume modeling inside objects: foliage-clump
  undersides, cel planes on towers, occlusion in bushes. This IS the painted
  look. **Always kept.**
- **Scene lighting** — the directional/time-of-day layer: cast shadows on
  the lawn, sun-side highlights, warm daylight color cast, sky-blue bounce.
  **This is what gets removed** and re-applied at runtime.

### 4b. The layer stack (what codex produces)

1. **Neutral ground plate** — relight-only regeneration of the master
   (workflow in 4c): soft overcast ambient, no sun direction, no cast
   shadows, local color at true value, all form shading retained.
2. **Sky variants, never a de-lit sky** — a sky IS light; it is swapped,
   not neutralized. Day / golden-hour / night states of the same cloud
   composition for the sky regions of row r0, tile-crossfaded at
   transitions. (Both sets resident only during the ~3 s crossfade —
   VRAM ledger applies.)
3. **Cast-shadow layer** — all object shadows (playground, easels, trees,
   castle-on-lawn) on their own multiply-blend card(s) over the plate. The
   highest-leverage trick available: shadows that fade, stretch away from
   the sun side (~2.2× at golden hour), and cool/warm with time of day read
   as dynamic lighting with zero lights. Produce as a shadow-only pass on
   transparency (or the with/without difference image).
4. **Emissive layer** — window/lantern glints as small additive cards
   (already N4–N5) fading in at dusk.
5. **Runtime grading** — per-depth-plane modulate curves over `time_phase`
   (0 day → 0.5 golden hour → 1 night): far planes warm first and most,
   NEAR_Z drives toward dark navy-purple backlit silhouettes, Roshan's card
   takes the mid-plane grade, contact shadows stretch/cool with the
   cast-shadow layer. Curves are Gradient resources sampled from
   `time_phase`; a sunset that *happens* on screen (~20–30 s tween
   timeline) is layer-3 authored motion. Same determinism + lifecycle rules
   as wind: stage-owned, seeded, reset on teardown.

Extracted cards (E1–E5, castle) receive the same neutral relight in card
finishing so they stay congruent with the plate under every grade.

### 4c. Relight generation workflow (master-level, never per-tile)

Image-to-image on the full 6144×2048 master — lighting must be globally
consistent; re-slice afterward per §3 steps 4–6 (new master rev, e.g.
v6→v7; prior rev untouched; same resolution/ratio/SHA/seam gates). Prompt
skeleton for codex:

> Relight this exact painting to soft overcast ambient light. Change
> NOTHING except lighting: identical composition, object positions,
> silhouettes, line work, and palette identity. Remove: all cast shadows on
> ground and objects, all sun-direction highlights, the warm daylight color
> cast, sky-colored bounce light. Keep: all form shading and volume
> modeling inside objects, ambient occlusion in foliage, the cel-shaded
> paint style, saturation at local color value. Even, directionless,
> slightly cool-neutral white balance throughout.

Generators drift — gates in §7 (17–20) are mandatory, and the plate is
never judged raw: it ships only under a grade.

### 4d. Ruled out

- **Normal-map relighting with real lights:** violates the
  shaded-Sprite3D = 0 probe assertion, fights the mobile renderer, and
  painterly art under normal maps reads plasticky — the exact look the
  reductive rebuild removed.
- **Full mural repaints per time-of-day** as the primary mechanism: N× art
  scope and VRAM, and every future mural edit multiplies by N. Permitted
  for the sky rows only (small, and genuinely un-gradable).

Runtime cost: one mostly-transparent multiply layer + small additive cards
— inside the §5 overdraw budget; count it in the coverage measurement.

## 5. Performance budgets — 3-year-old Android tablet floor

(Adreno 610 / Mali-G52 class, ~1200p.) Three ceilings, in the order they
actually arrive; the probe asserts the first two:

1. **Texture VRAM (arrives first).** Lossless 1024² ≈ 4–5 MB with mips;
   the 12 backdrop tiles are ~60 MB alone. Budget: **stage total ≤150 MB.**
   Rules: only E1–E5 flora cards justify 1024px; cloud ≤512; puffs/glints
   ≤256; POT everything so VRAM compression is available; never add a
   lossless texture without checking this ledger. (Boot-time audit: lossless
   textures are the #1 boot lever — same budget.)
2. **Transparent overdraw (frame-rate wall).** Budget per camera framing:
   **≤6–8 large cards (>10% screen coverage each), cumulative card coverage
   ≤150% of the screen** on top of the backdrop. Full-screen transparent
   layers are the killer: acceptable transiently (sunset sky crossfade,
   ~3 s), never steady-state.
3. **Draw calls (distant third).** ~1 per Sprite3D; comfortable to ~150
   visible. At v3's ~45 visible, not a factor — do not spend effort here.

If a framing fails budget 2, remove quiet-loop cards; never shrink the
dominant landmark's motion.

## 6. Art pipeline (two lanes, shared finishing)

- **Extraction lane** (E-items): §3 — original pixels, matte + heal.
- **Generation lane** (N-items + future flora): near-white background, root
  line visible, no border shadow, baked ink outline + warm-light/cool-shadow
  cel (shadow tones toward navy-purple), neutral top-down light →
  `polish_sprite.py` cutout → fringe check → finishing per §3 step 2.
- Both lanes end in the same manifest, import settings, and probe gate.
- E-lane cards additionally pass through the §4 neutral relight before
  finishing, so cards and plate grade identically.

## 7. Acceptance gates

All v2 gates carry (inventory, determinism, pinned bases, touch clearance,
per-screen budget count, night congruence, grounding, greyscale layer
separation, bloom, teardown lifecycle, <1 ms/frame). v3 adds:

12. **Master integrity:** v6 is 6144×2048 ratio 3.0; SHA recorded; pixel
    diff v5→v6 shows changes only inside declared heal bounds (count of
    out-of-bounds changed pixels: 0); v5 files untouched in the repo.
13. **Seam gate re-pass** on all joins after re-slice, evidence updated.
14. **Congruency:** reference-camera before/after captures per extraction —
    object occupies the same screen position as the painted v5 original.
15. **VRAM ledger:** stage texture total ≤150 MB, recorded in the PR.
16. **Coverage measurement:** probe computes per-framing cumulative card
    coverage; asserts ≤150% + ≤8 large cards (includes the cast-shadow
    multiply layer and any active sky crossfade).
17. **Relight congruency:** edge-map/structural diff of the neutral plate
    vs. the prior master — silhouettes, positions, and line work unchanged
    (structural gate, not exact-pixel: every pixel value legitimately
    shifts).
18. **No-shadow review:** human pass over lawn, path, and building bases on
    the neutral plate — generators reinvent cast shadows; none may survive
    outside the dedicated shadow layer.
19. **White balance:** sampled reference patches (path stones, castle wall,
    lawn) read neutral — no residual warm cast on the plate.
20. **Grade sweep (owner gate):** the runtime day / golden-hour / night
    grade curves applied to the candidate plate, all states reviewed
    together. The plate is accepted only if every graded state looks
    natural; the raw plate is never the judged artifact.

## 8. Portability

The contract, motion layers, budgets, deterministic tokens, the two-lane
pipeline, and the §3 extraction workflow are the required design language
for all future stages. The §2 inventory table is the per-stage part: every
stage gets its own closed, owner-approved extraction table before any
isolation work begins.
