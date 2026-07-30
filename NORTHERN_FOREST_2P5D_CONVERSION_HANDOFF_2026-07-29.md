# Northern Forest 2D→2.5D Conversion — Codex Handoff (2026-07-29)

**Work order for codex.** Governing docs:
`SKY_LAGOON_LIVING_CARD_ANIMATION_V3_2026-07-28.md` (design language,
lighting, budgets, gates 1–20) and
`NORTHERN_FOREST_LIVING_CARD_FIRSTPASS_2026-07-29.md` (stage phases, autumn
motion identity). This handoff adds the owner decisions and the 2D→2.5D
conversion spec — the hard part of this stage — and the PR sequence.

## Owner decisions (locked)

1. **Progression approved:** autumn forest → winter castle across the three
   screens. Screen 1 deep autumn (the approved concept frame,
   `assets_src/concepts/northern_forest_concept_2026-07-29.png`), screen 2
   stream crossing with the transition beginning (first snow dusting on the
   teal pines, leaves thinning), screen 3 winter — snowline, kit cottages/
   mill or castle approach in the winter palette, aurora available in the
   night sky state. The kit art conditions all structures.
2. **The progression is painted, not graded.** The autumn→winter shift
   lives in the master's pixels as one continuous composition. Runtime
   grading handles time-of-day only, never season. (A graded season would
   fight the §4 neutral-plate rule and break the moment the camera pans.)
3. **The approved painting is preserved; independent items are regenerated.**
   Northern-specific owner direction in
   `NORTHERN_FOREST_LIVING_CARD_FIRSTPASS_2026-07-29.md` supersedes the v3
   extraction lane for any object that becomes an independent item card.
   Concept crops are references and mattes only. Final items are native
   high-resolution, volumetric-looking raster sprites on unshaded `Sprite3D`
   nodes at real depth. They are not shipped flat crops and are not runtime
   models or shaded meshes.

## The 2D→2.5D conversion spec

This is the core of the job: the concept is a flat painting; the stage is a
depth-planed world that must *still look exactly like the painting* from
the play camera. Every rule below exists to hold that equivalence.

### 1. The painting is the screen

Promenade precedent applies verbatim: the mural grid sits at
`BACKDROP_Z = -18`, the camera frustum is sized so the frame lands INSIDE
the mural with painted margin (lagoon: ~45 units tall at the mural, 1.6u
margin top/bottom, `CAM_DIST 47 / CAM_H 9.5 / FOV 38°`), pan clamped to
`screen_pan_limit`, no environment sky ever visible. Start from the lagoon
constants; re-derive only if the northern composition's horizon line
demands it, and record the derivation in the stage script comments.

### 2. Depth-plane assignment of the painted content

Everything in the concept gets classified before any pixel work — this
table IS the conversion plan. Assignment for the approved frame:

| Painted content | fate | plane |
|---|---|---|
| Purple atmospheric distance, far trees, sky glow | stays mural | −18 |
| Mid-ground canopies, trunks, boulders, path, stream *bed* | stays mural | −18 |
| One mid cloud/mist wisp (if the master gains one) | regenerate as volumetric sprite | CLOUD_Z −16 |
| Stream *surface* band (shimmer) | regenerate as exact-ratio living card | DRESS_Z −9 |
| Cyan crystals | regenerate as volumetric sprites | DRESS_Z / NEAR_Z |
| One near birch + red canopy (left third) | regenerate as volumetric sprite | DRESS_Z −9 |
| Kit structures on screens 2–3 (mill, cottages, castle) | born as cards, never painted in | LANDMARK_Z −11 / PLAY_Z −6 |
| Fern/mushroom clusters at the bottom edge | regenerate as volumetric sprites | NEAR_Z −1.5 |
| Red-cap mushroom cluster at the big trunk base | regenerate as volumetric sprite | NEAR_Z −1.5 |
| Overhanging foreground canopy (top of frame, optional) | regenerate as volumetric sprite | NEAR_Z, above the walk band |

Rules of the table:
- **In front of Roshan (NEAR_Z) is what buys 2.5D.** She is at z ≈ 0.2;
  the ferns, mushrooms, and the optional overhead canopy are the only
  things that occlude her — that occlusion, plus bounded parallax, IS the
  2D→2.5D transition as far as the player is concerned. Prioritize these.
- **New-for-screens-2/3 structures are cards from birth** (the lagoon's
  castle precedent): the master paints the terrain *behind* them, so no
  heal is ever needed and they sit at real depth on day one.
- **Regenerated means a native ≥2048px authoring master.** Preserve that
  master under `assets_src/`; wire a separate POT runtime derivative,
  normally 1024px on the long edge, only after alpha/fringe, pixel-density,
  aspect, depth, touch, VRAM, and overdraw gates pass. Never upscale a crop.
- Anything not in the table stays painted. When in doubt: painted.

### 3. Perspective compensation (the "still looks like the painting" math)

Each regenerated card moves forward from the mural plane, so it must scale
DOWN and shift vertically to subtend the same screen rect from the
reference camera: for a card moved from mural depth `d_m` to plane depth
`d_c`, scale by `(CAM_DIST + d_c) / (CAM_DIST + d_m)` (using
camera-relative distances) and re-solve its y so the base stays on its
painted footprint. The lagoon did exactly this ("heights and y positions
are perspective-compensated... preserving the approved 720p composition").
**Gate 14 (congruency) is the check:** reference-camera capture before and
after regeneration must show the object in the same screen position —
parallax appears only when the camera pans.

### 4. Walk band and touch mapping

The concept's sandy path is the walk band — read its screen-height window
off the painting and map it per the lagoon (`BAND_Y/BAND_H`, hold-to-travel
`0.20 s`). Constraints carried from the promenade: Roshan's card ≈24% of
frame height with feet on the painted path; NEAR_Z extractions must never
overlap her touch silhouette or any registered target's bounds
(gate 4); the stepping-stone stream crossing on screen 2 stays *painted
ground* — it is route, not a card, and must remain stable (v2 rule:
ground that moves reads as broken).

### 5. Parallax bounds

Bounded, restrained parallax (probe-asserted, lagoon precedent): the depth
illusion comes from small relative slips between planes during pan, not
from dramatic layer sliding. If a card's parallax exposes healed
background that looks wrong at max pan, the heal is insufficient — fix the
heal, don't shrink the parallax.

### 6. Season-progression seams

The autumn→winter gradient must survive the tile grid: place the visible
snowline transition INSIDE screen 2's tiles, not on a column join, and run
the seam gate (≤2.0 ratio) with special attention to the c2/c3 and c3/c4
joins where the palette is shifting. The §4 sky variants must carry the
same progression (autumn-gold dusk over screen 1 blending to winter-blue
over screen 3 within each single sky state).

### 7. Screen-blended time-of-day grading

Because the palette shifts along x, the runtime grade curves (§4b.5) get a
per-screen key each: sample the curve set by `time_phase`, then blend
between adjacent screens' keys by camera x during pans. Cheap (a second
lerp) and prevents the autumn grade from tinting the winter screen amber.

## PR sequence (each PR is gated before the next starts)

1. **PR-A — Composition reference.** Three-screen ~2172×724 layout per the
   firstpass Phase 0 + the locked progression; snowline placement marked.
   → owner approval.
2. **PR-B — Native master + layers.** 6144×2048 neutral plate (gates
   12/13/17–20), cast-shadow pass, emissive pass (crystals, windows), sky
   variant set with painted progression. Master + evidence only, no code.
3. **PR-C — Stage skeleton.** `NorthernForestPromenade` cloned from the
   lagoon promenade: backdrop grid, camera/lens derivation, walk band,
   probe with node-type inventory table (starts at 12 backdrop cards + 0),
   route across all three screens. Playable on the flat mural alone —
   **ship this state**: it is the 2D baseline every later congruency
   capture compares against.
4. **PR-D — Volumetric-card pilot.** Regenerate ONE forest-trail red
   mushroom cluster end-to-end through the northern Phase 3 contract:
   reference crop → native ≥2048 master → alpha/finish → clean-plate heal →
   runtime derivative → reinsert → congruency at NEAR_Z, with a separate
   contact shadow and brush-past wobble. → owner approval of the pilot's
   probe sheet.
5. **PR-E — Volumetric-card batch.** Remainder of the closed structural
   table plus all 24 enumerated touch items and the structures on screens
   2–3 as born-cards. Preserve the placeholder crops; replace their runtime
   paths only after each new card passes inventory, touch, coverage, and
   4.5/5 visual gates.
6. **PR-F — Motion + grading.** Firstpass Phase 4 motion identity, wind
   state, time-of-day curves with screen-blended keys, acceptance gates
   1–11 full pass.

## Budgets (unchanged, restated)

v3 §5 verbatim: VRAM ≤150 MB stage total; ≤6–8 large cards and ≤150%
cumulative card coverage per framing; ~40–55 total nodes target; per-screen
motion budget 1 dominant + ≤3 quiet loops. The conversion is done when the
painting breathes — not when the card count is exhausted.
