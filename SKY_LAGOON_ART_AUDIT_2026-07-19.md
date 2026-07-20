# Sky Lagoon Art Audit - 2026-07-19

Scope: the full Sky Lagoon runtime world, including the courtyard, meadow,
rivers, Fairy Pond, rainbow route, castle approach, train stop, and Alpine
corner. Protected book paintings are identity references and were not modified.

## Binding botanical rule

A single detached leaf must never represent a complete plant emerging from
terrain. Single leaves are permitted only as litter, a collectible, or part of
a larger branch or canopy assembly. Ground vegetation must show one believable
attachment point and a complete growth habit: baby rosette, multi-leaf clump,
reed bed, shrub, flowering plant, or mature tree.

This rejects both the former `grass_leafsLarge` spear-leaf scatter and the
`plant_bush`/`plant_bushLargeTriangle` crossed cards when they resolve to one
enlarged leaf. The rule is enforced in `SkyLagoon._lagoon_plant_allowed()` and
covered by `probe_l2.gd`.

## Human-review baseline and action

Scores below describe the pre-pass runtime presentation. New candidates remain
unscored until Mobile-render near, mid, and gameplay-distance captures survive
human review. Provenance or successful import does not award 5/5.

| Area or asset family | Baseline | Main failure | Action in this pass |
|---|---:|---|---|
| Meadow undergrowth | 1/5 | One enlarged leaf used as a whole bush or grass plant; obvious crossed-card repetition | Replaced by five complete modeled growth habits |
| Pond edge | 1/5 | Fourteen single spear leaves mislabeled as cattails | Replaced by ten rooted multi-stem reed beds |
| Fairy Pond | 1/5 | Glowing spheres stood in for flowers, and the entire pond was buried under the rolling terrain | Replaced by rooted flower clusters, seated pond and trigger on terrain height, and reduced the reading-dependent label to a fairy pictogram |
| Riverbanks | 2/5 | Bare shader boundary with little physical transition | Added restrained modeled bank-stone groups |
| Grand-path lighting | 2/5 | Box/cylinder lamp construction | Replaced visible side with shell-crested story lanterns; collider and light contract preserved |
| Protected memory displays | 3/5 | Book art floated in generic generated slabs | Added shell-and-gold architectural surrounds; source art unchanged |
| Rainbow race route | 2/5 | One giant decorative torus disagreed with two remote gameplay triggers | Replaced by one authored arch at each functional race trigger |
| Train station | 1/5 | Primitive slab, posts, and roof | Replaced station shell; train cars and track remain a separate P0 rebuild |
| Clouds | 1/5 | Small lumpy/faceted silhouettes and muddy value grouping | Rebuilt as three smooth broad cloud families; runtime review required |
| Butterfly World gate | 1/5 | Giant opaque wing panels obscured the route and failed as a swim-through frame | Replaced in iteration two by four open wing rims, a complete body, and two antennae at the existing trigger |
| Alpine snow edge | 3/5 | Abrupt shader boundary | Added low snowbank families without changing clearances |
| Castle exterior | 3/5 | Stronger than the old gate, but much of the shell still reads as assembled primitives | Not closed by this kit; retain as P0 for an authored exterior-shell pass |
| Alpine chalets and crag | 2-3/5 | Primitive breakup and weak material hierarchy | Not closed; retain as P0 after runtime review of this pass |
| Courtyard train cars and track | 1/5 | Functional primitives dominate a high-frequency ride | Not closed; station is only the first replacement |
| Playground | 3/5 | Imported toy set is coherent but not fully integrated with Lagoon motifs | Review in the dedicated capture set before deciding whether to rebuild |
| Dream Stars | 4/5 candidate | Prior authored rebuild is functionally readable; acceptance still requires current runtime views | Re-capture alongside new work; do not auto-promote |

## New authored kit

Runtime models live in `assets/sky_lagoon/lagoon_kit/`. The deterministic source
is `tools/build_sky_lagoon_kit.py`; isolated QA images live in
`assets_src/sky_lagoon/qa_kit/`. Replaced cloud binaries and the pre-pass scripts
are preserved under `backups/art_pre_sky_lagoon_5of5_2026-07-19/`.

The kit adds no textures and does not replace book art, family voices, friend
cutouts, or stuffed animals. Navigation solids, minigame triggers, race trigger
coordinates, pond trigger, and save keys are unchanged.

Iteration one (`1e2412a`) was rejected after Mobile review: ellipsoid faces were
wound inward, allowing the inverted-hull pass to cover plant crowns, shell
crests, and clouds in navy. The same review also rejected the previously shipped
opaque Butterfly World gate. Iteration two reverses those faces, uses smooth
normals on rounded masses, and adds an open four-wing gate. Green probes alone
did not promote the rejected candidate.

Iteration two (`9da8457`) passed every technical and gameplay gate but was also
rejected by Mobile review: the Fairy Pond was buried under its hill, the high-key
lighting bleached new materials, one low cloud obscured the castle, and the
Alpine camera entered a wall. Iteration three seats the pond and trigger on the
terrain surface, reserves its footprint, deepens source palette bands for the
actual Lagoon lighting, composes smaller clouds around the island rim, and fixes
the invalid review camera.

Iteration three (`584d3a0`) passed every technical gate but Mobile review still
rejected its presentation. The persistent reef sun and the Lagoon sun were both
lighting the world, so pearl terrain, flowers, water, and new landmarks clipped
toward white even after source colors were deepened. Iteration four gives Sky
Lagoon a dedicated contrast grade, uses only its authored courtyard sun while
the world is active, restores the reef sun on ocean return, and makes Speedy the
binding full capture tier with Sparkly comparison views.

## Acceptance gates

1. `probe_l2.gd` must report the botanical rule, all kit resources, and all fixed
   placements as OK.
2. The Mobile-render Sky Lagoon capture artifact must include arrival/path,
   complete ground plants, pond reeds, Fairy Pond, riverbanks, both race gates,
   Butterfly gate, castle facade, clouds, Alpine edge, and train station.
   The complete set is captured in Speedy, with arrival, pond, and castle also
   captured in Sparkly to expose quality-toggle drift.
3. Reject any candidate that reads as an isolated leaf, repeated mesh island,
   stone-like cloud, decorative gate that disagrees with its trigger, floating
   prop, or protected art alteration.
4. Only owner-accepted runtime views may receive 5/5.
