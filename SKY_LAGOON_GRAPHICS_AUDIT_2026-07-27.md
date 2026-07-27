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

## 2. The codex PNW set *is* wired up — it was invisible, not unused

`scripts/arena/sky_lagoon.gd` already places the full accepted 24-role roster
as the meadow's primary flora: twelve hero trees, fourteen groves, twelve
guaranteed shrub specimens and a 90-plant undergrowth pass, all under the
ecological placement rules (snow admits conifers only, alder/cottonwood/
salmonberry hold wet banks, madrone/Garry oak/oceanspray keep 20 units from
water). Nothing needed rewiring. Every one of those plants was simply
rendering as a black blob, which is why the set read as "not being utilized".

With the normals corrected the PNW family now reads as the dominant flora it
was authored to be.

## 3. Playground rebuilt

The six `lagoon_play_*` toys were bare primitive frames — the swing was **580
triangles**: four leg rods, one beam and two flat slabs. They read as diagrams
rather than equipment. Rebuilt in `tools/build_sky_lagoon_quality_kit.py`:

| toy | before | after | added |
|---|---|---|---|
| slide | 3448 | 7880 | top deck + side walls, scalloped canopy, climbing handrails, chute channel walls, run-out lip, landing cushions, post feet and caps, bunting |
| swing | 580 | 6636 | A-frame cross-bracing, ground feet, beam trim and end caps, chains with visible links, contoured seats with backrests, bunting, crest |
| seesaw | 1644 | 4360 | fulcrum cheek plates and pivot bolt, painted plank stripes, twin handle grips, seats with backrests, end bumper cushions |
| merry-go-round | 2032 | 6516 | pinwheel deck wedges, hub, rim valance, four riding seats, curved grab handles, bunting |
| sandbox | 2092 | 6192 | wall coping, sandcastle with four towers, sand mounds, bucket and spade, toadstool shade parasol |
| spring horse | 1852 | 3976 | chest/rump volumes, neck, muzzle, eyes and cheeks, mane and forelock, hooves, saddle skirt, stirrups, grab handle, spring mount plate |

Total 11,648 → 35,560 triangles for the whole playground corner. No new
textures, no new materials beyond the existing kit palette, no new draw-call
families.

**Every gameplay landmark is unchanged.** `scripts/arena/sky_lagoon.gd` derives
its play-moment anchors and collision cylinders from post spacing, ladder-foot
offset, chute run, beam height, seat x-positions, pivot centre, deck radius,
sandbox rim and saddle height — all of those coordinates are byte-for-position
identical, so the climb, swing, ride, seat, bounce and dig moments and
`player.gd`'s calibrated poses still land exactly where they did. The sandbox
stays non-solid on purpose. The added dressing is outside the solids.

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
