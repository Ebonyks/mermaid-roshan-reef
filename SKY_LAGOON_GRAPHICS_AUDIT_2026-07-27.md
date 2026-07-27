# Sky Lagoon graphics audit — 2026-07-27

Owner report: *"textures not loading properly… there's a set of PNW assets
produced by codex that are not being utilized currently… playground equipment
looks very rough and minimalist."* Three phone captures of the Sky Lagoon
meadow accompanied it: black tree silhouettes with white edge fizz, pale
untextured trunks, and stick-frame playground toys.

## 1. The black trees are not a texture failure — they are inside-out meshes

Nothing in the Sky Lagoon is missing a texture. The PNW woody family is
deliberately texture-free (`audit_sky_lagoon_kit.py` gates it at zero images).
The trees rendered black because **their geometry ships with inward-facing
normals**.

`tools/build_sky_lagoon_pnw_woody_plants.py` composes every plant from
`mesh.from_pydata()` with hand-written face index lists. `from_pydata` takes
the winding exactly as written and never recomputes it, and the two workhorse
generators — `cloud()` (every crown mass, berry, bell, flower petal, samara
wing, acorn cap, plume pod, leaf segment, ground stone, moss tuft and bark
dash) and `skirt_tier()` (every conifer skirt) — listed their quads
higher-ring-first, which is the inside-out hand. Only `tube()` (trunks, stems,
canes, roots) happened to wind outward.

Measured on the shipped binaries: 24 of 32 closed shells inverted in
`lagoon_tree_douglas_fir`, 32 of 44 in `lagoon_tree_red_alder`, and **16 of 16
in `lagoon_shrub_salal_a`** — a completely inside-out asset.

This never showed up in review because **Blender flips the shading normal on a
backface and Godot does not**:

* `assets/shaders/cel.gdshader` computes
  `clamp(dot(normalize(NORMAL), normalize(LIGHT)), 0.0, 1.0)`. An inward normal
  clamps to zero, so `DIFFUSE_LIGHT` receives **nothing** — the surface keeps
  only ambient and reads black.
* The same shader's rim term is
  `pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 3.0)`. An inward normal makes
  that dot negative, `f` saturates to 1.0, and the Fresnel rim fires at full
  strength — the white speckle along every black crown in the captures.
* The inverted-hull outline `next_pass` then draws navy ink over the result.

The QA turntables in `assets_src/blender/qa_sky_lagoon_pnw_woody_plants/`
looked correct throughout, because EEVEE was silently flipping what Godot would
not. This is the same defect the 2026-07-19 runtime review already rejected
once — `ASSET_LICENSES.md` records that set as rejected for "inward face
winding" — but it was never fixed at the source, only re-shot.

### Fix

* `cloud()` and `skirt_tier()` now list quads and caps in the outward hand.
* `mesh_object()` runs `bmesh.ops.recalc_face_normals` as a standing safety
  net (`_make_normals_outward`), so no future volume in that module can ship
  inverted regardless of how its faces are listed. It is orientation-only and
  preserves face order and `material_index`, so it is safe after the material
  assignment.
* `panel_xz()` in `tools/build_sky_lagoon_quality_kit.py` gets the same pass,
  *before* its bevel modifier — an inverted panel bevels inward. This also
  repaired the two inverted shells in `lagoon_butterfly_world_gate`.
* All 24 woody GLBs and the butterfly gate were regenerated. Triangle counts,
  material counts and dimensions are **byte-identical to the previous build** —
  the change is purely orientation.

Verified with an engine-accurate preview (cel lighting, no backface flip):
crowns now band mint-highlight over jade-shadow instead of flat black.

## 2. The codex PNW packet was unmerged, not unwired

Two separate things were behind "PNW assets produced by codex that are not
being utilized".

The **modelled** 24-role woody roster was already wired: `sky_lagoon.gd` places
twelve hero trees, fourteen groves, twelve guaranteed shrub specimens and a
90-plant undergrowth pass under the ecological rules. Nothing needed rewiring
there — every one of those plants was rendering as a black blob, which is why
the set read as unused.

The **2D** packet was genuinely missing. `OPUS_ROSHAN_POOL_PNW_2D_HANDOFF_2026-07-26.md`
on `origin/codex/roshan-pool-pnw` hands over five painted atlases and their
runtime integration — 2,132 lines across 22 files — and none of it had reached
`dev` or `master`.

This pass integrates the Sky Lagoon part of that packet, by owner decision
(2026-07-27): the marsh only, with the castle pool, whale rescue, storyboard
and hutches left on the feature branch for their own pass.

- `assets/sky_lagoon/pnw_marsh_2d/pnw_marsh_atlas.png` — 16 rooted PNW wetland
  cards: cattails, slough sedge, tufted hairgrass, softstem bulrush, sword
  fern, deer fern, horsetail, skunk cabbage, water lilies, marsh marigold,
  mossy nurse log, cedar stump, river stones, reed seed heads, bog cranberry,
  western iris.
- Runtime and provenance SHA-256 both verified against the packet manifest
  before integration.
- `sky_lagoon.gd` gains `_build_lagoon_marsh_2d()` from the handoff branch
  unchanged: unshaded double-sided alpha-scissor cards, water lilies laid flat
  inside the pond rim, the rest ringed around the pond with the last four
  spread along separate river banks. No collision, lights or particles; a
  150-unit Speedy visibility range bounds the transparent overdraw.
- `probe_l2.gd` gains the handoff's assertions: atlas present at 1024x1024 and
  exactly 16 cards placed.

## 3. Playground rebuilt to the concept sheet

The six `lagoon_play_*` toys were bare primitive frames — the swing was **580
triangles**: four leg rods, one beam and two flat slabs.

A first rebuild attempt invented equipment: canopies, bunting, cross-bracing, a
toadstool parasol and a sandcastle. The owner rejected it as "strange
playground equipment", and correctly — the designs were already drawn, in the
playground row of `assets_src/concepts/sky_lagoon_quality_2026-07-20.png`,
which had been in the repository since the 2026-07-20 quality pass and was
never opened. The sheet is the contract.

Built to the sheet:

| toy | before | after | design |
|---|---|---|---|
| swing | 580 | 3964 | teal A-frames with gold collar bands and lavender foot pads, lavender top bar with gold end caps, one wooden plank seat on two twisted gold ropes |
| slide | 3448 | 5488 | gold ladder with rungs to the chute head, pearl-and-gold post finials, one continuous lavender ramp with teal edge rails and a run-out lip |
| seesaw | 1644 | 1488 | wooden plank on a lavender wedge over a teal base plate, lavender whale head one end, little pink treat the other, teal seat pads |
| merry-go-round | 2032 | 4264 | lavender deck with a gold rim and painted gold star, four gold grab arches, gold-banded post under a pearl finial |
| ball pit | 2092 | 5564 | masonry rim banded stone / butter / rose, packed with pastel balls |
| spring horse | 1852 | 2764 | no card on the sheet — shipped anatomy kept, finished only to the level the sheet's own whale head sets (rounded volumes, visible eye, contrast muzzle). No invented gear. |

Two deviations, both deliberate:

* The sheet draws a **ball pit**, but `sky_lagoon.gd` runs a dig play-moment
  with `_sand_puff` over this toy. The rim is built to the sheet and the cream
  fill stays under the balls, so the pit reads correctly and keeps its
  animation.
* The spring horse has no concept card. It needs one before it can be judged
  against the sheet like the others.

Total 11,648 → 23,532 triangles. No new textures, no new materials.

**Every gameplay landmark is unchanged.** `sky_lagoon.gd` derives its
play-moment anchors and collision cylinders from post spacing, ladder-foot
offset, chute run, beam height, pivot centre, deck radius, rim radius and
saddle height — those coordinates are byte-for-position identical, so the
climb, swing, ride, seat, bounce and dig moments and `player.gd`'s calibrated
poses still land where they did. Moving the single swing seat to the centre of
the bar actually matches the existing anchor better than the two offset seats
did. The ball pit stays non-solid on purpose.

## 4. New gate: inside-out meshes now fail CI

`tools/audit_glb_shell_orientation.py` welds every primitive of a GLB by
position, splits it into connected components, and requires each closed
component's signed volume to be positive. Open components (banners, cards,
decals) have no meaningful sign and are reported, never failed.

It is invoked from `tools/audit_sky_lagoon_kit.py`, which
`.github/workflows/probes.yml` already runs in its static-gate step — no
workflow change was needed. `scripts/ci.sh` was missing that audit entirely
and now runs it too.

Verified both ways: the current kit reports `oriented=61`, and re-introducing
any pre-fix asset fails the gate.

## 5. Outstanding — inverted shells outside this stage

The same sweep found inside-out shells in other kits. They are partial (a few
shells per asset, not whole assets), so they show as isolated black parts
rather than black props, and they are outside the Sky Lagoon stage this pass
covers. Recorded here rather than fixed, since each needs its own builder fix,
regeneration and probe cycle:

* `assets/northern/*` — 11 inverted shells in `northern_center_castle`, 3–5
  each in the six houses, mill house, forge, bedroom set, dock, spirit stone
  and wisp.
* `assets/art35/landmarks/butterfly_gate.glb` — 4.
* `assets/props/gen2/` — 1 each in `clownfish`, `shrimp` and `play_seesaw`.

Also noted: `assets/props/gen2/play_*.glb` (six textured Meshy playground
sculpts) are now dead assets. `main.gd`'s `KIT_GEN2` maps `play/slide_A` and
friends to them, but nothing calls `_kit("play/…")` any more — the Sky Lagoon
playground moved to the authored `lagoon_play_*` family in the 2026-07-20
quality pass. Either the mapping or the files should go; left alone here
because deleting art is an owner call.
