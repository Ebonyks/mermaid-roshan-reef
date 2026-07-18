# Pearl Castle Art Audit and Rebuild

## Scope

This pass addresses the Grand Hall, ceremonial threshold, throne wall, upper
galleries, Cloud Lounge, Star Chamber, Royal Library, Toy Room, Dreaming Floor,
undercroft, basement rooms, music room, royal bedroom, back chamber, and Royal
Loo shape correction. It does not alter protected book art, Huluu, family
voices, friend cutouts, legacy character models, or child-supplied stuffed
animals.

The pass evaluates and applies the shared findings in:

- `ART_STYLE_GUIDE.md`
- `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`
- `ART_GAME_WIDE_PASS35_AUDIT_2026-07-16.md`
- `ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md`
- `assets/OBJECT_GENERATION_AUDIT_LOG.md`
- `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md`
- the owner's castle, cloud, motif, source-asset, and toilet feedback

## Baseline Findings

| Role | Prior score | Failure preventing 5/5 |
|---|---:|---|
| Hall columns | 1.5/5 | Generic cylinders with box capitals and bases |
| Balcony rails | 1/5 | Thin boxes and posts; no authored silhouette |
| Throne frame | 1.5/5 | Rectangular piers and tilted box canopy |
| Throne glass | 2.5/5 | Broad generic color panel without castle-specific construction |
| Throne model | 2/5 | Generic wooden scaffold crossed the protected character in gameplay views |
| Door frames | 1.5/5 | Three-box lintel language at focal transitions |
| Staircase dressing | 2/5 | Functional treads with no balustrade or ceremonial finish |
| Column lights | 1/5 | Exposed emissive spheres |
| Chandeliers | 1.5/5 | Bare torus meshes with no fixture construction |
| Tapestries | 2/5 | Flat quads with flat fill colors |
| Planters | 2/5 | Primitive cylinders plus unrelated generic foliage |
| Entrance exit | 2/5 | Raw rainbow torus; function visible, place identity absent |
| Cloud Lounge seats | 1/5 | Repeated colored boxes described as pillows |
| Royal toilet | 2.5/5 | Front read was acceptable, but side view omitted a convincing rear skirt and trap body |

The room also suffered a hierarchy problem. Shells appeared as isolated badges,
while rainbow treatment was either absent or used as a raw shader. Neither motif
was tied to architectural function.

## Motif Deployment

Shells are the castle's construction grammar. They appear at capitals,
balusters, keystones, fixture bowls, planter relief, banner crests, furniture
ends, and water features. They are not scattered as unrelated stickers.

Rainbows are a ceremonial and wayfinding grammar. They are limited to the
throne glass/canopy, entrance medallion, return gate, and selected upper-room
furnishings. Ordinary columns, arches, and every wall do not receive rainbow
bands. This prevents the recurring "generic cute pastel plus rainbow" failure.

Pearl, lavender shadow, deep ink, aqua, rose, coral, green, and restrained gold
create separate material reads. Matte surfaces and broad value groups preserve
the cel-shaded toy-diorama look under the Mobile renderer.

## Authored Kit

All assets are deterministic Blender 4.4.3 outputs from
`tools/build_pearl_castle_kit.py`. Each GLB is one runtime mesh, contains no
armature, animation, light, camera, or collision body, and remains under the
10,000-triangle per-prop ceiling.

| Asset | Triangles | Runtime role |
|---|---:|---|
| `pearl_column.glb` | 5,652 | Fluted pearl shaft, modeled base, shell capital |
| `pearl_balustrade.glb` | 5,224 | Hall arcade and throne-gallery rails |
| `pearl_shell_arch.glb` | 2,556 | Door and window transition frame |
| `pearl_rainbow_window.glb` | 5,328 | Throne-wall stained glass |
| `pearl_shell_sconce.glb` | 952 | Wall-mounted shell-and-pearl fixture; reuses existing OmniLight |
| `pearl_shell_chandelier.glb` | 5,092 | Main and gallery hanging fixture; reuses existing lights |
| `pearl_floor_medallion.glb` | 2,124 | Entrance ceremonial focal point |
| `pearl_throne_canopy.glb` | 2,924 | Pearl-and-shell frame around the rainbow glass |
| `pearl_shell_throne.glb` | 3,012 | Open-sightline shell throne replacing the generic scaffold |
| `pearl_shell_planter.glb` | 3,488 | Integrated planter and modeled leaf family |
| `pearl_shell_bench.glb` | 3,432 | Entrance seating |
| `pearl_cloud_settee.glb` | 4,284 | Cloud Lounge seating with explicit cushion, back, and arms |
| `pearl_cloud_pouf.glb` | 1,704 | Low Cloud Lounge footstool/seating pair with exposed cushion |
| `pearl_shell_fountain.glb` | 2,064 | New side-bay water landmark |
| `pearl_rainbow_gate.glb` | 4,372 | Return threshold replacing the torus marker |
| `pearl_shell_banner_a.glb` | 1,608 | Plum shell-and-wave wall hanging |
| `pearl_shell_banner_b.glb` | 1,608 | Aqua shell-and-wave wall hanging |
| `pearl_stair_rail.glb` | 4,824 | Sloped ceremonial rail for the throne staircase |

The evidence expansion added thirty-six more single-mesh assets after the
eleven-view Mobile pass exposed out-of-frame blockouts:

| Family | Assets | Triangle range | Runtime role |
|---|---:|---:|---|
| Threshold and windows | 2 | 1,844-2,456 | Graphic ocean return curtain and nineteen shell-framed windows |
| Library and Toy Room | 8 | 1,264-5,768 | Story seat/table, visible-color blocks and chest, physical hopscotch, sailboat, drum, rainbow stacker |
| Secret chamber | 1 | 1,608 | Sliding shell treasure chest with existing tween contract |
| Royal bedroom | 3 | 1,608-4,244 | Open canopy bed, bedside fixture, dress-up wardrobe |
| Playable music set | 9 | 560-1,768 | One rail, seven separately triggered rainbow keys, and a shell mallet stand |
| Undercroft and pantry | 4 | 904-5,144 | Barrel, crate, shell lantern, stocked pantry shelf |
| Craft and bath | 5 | 540-2,512 | Easel, paint rack, paper table, anatomical bath duck, towel stack |
| Dreaming keepsakes | 4 | 1,540-2,240 | Tiara, cradle, empty pet basket, physical music box |

No generated stuffed animal was introduced. The pet basket surrounds the
existing protected Wacky and Chuck cutout; child-specific toys remain a manual
future source-art workflow.

The editable source is `assets_src/blender/pearl_castle_kit.blend`; isolated
renders live in `assets_src/blender/qa_pearl_castle_kit/`.

## First Runtime Review And Correction

The first six Mobile captures were not promoted. They proved four failures that
isolated renders and structural probes had missed:

- the retained generic throne crossed Huluu's face and torso with wooden bars;
- outdoor landmark clouds became oversized blank masses when misused as seats;
- sconces attached to column faces and read as floating lightbulbs;
- the entrance and upper-gallery cameras clipped geometry or missed the work
  they were supposed to validate.

The second pass replaces the throne with a shell-backed seat whose character
sightline stays open, uses purpose-built cloud settees and poufs, mounts smaller
pearl lights on the walls, moves entrance planters off the runner, and expands
the fixed runtime review from six views to eleven. This is a direct application
of R-GEO5, R-QA2, and R-QA4: a technically valid asset or nonblank screenshot is
not evidence when it hides the functional assembly or target composition.

## Second Runtime Review And Evidence Expansion

The green eleven-view pass was still rejected as an art-completeness claim.
Human inspection found a blank return-gate void; raw Toy Room boxes; clumped
Cloud Lounge poufs; clipped Star Chamber, bedroom, music, loo, and back-room
cameras; slab bedroom furniture; primitive xylophone rails and keys; a generic
secret chest; and uncaptured blockout storage, pantry, craft, bath, and Dreaming
Floor props. This was not an exporter failure. It was an evidence-radius and
art-direction failure.

The expanded pass therefore:

- turns the return gate into an ocean-facing threshold rather than decoration;
- replaces labels and emoji glyphs with physical arches, fixtures, and keepsakes;
- preserves seven independent music triggers under one coordinated instrument;
- rebuilds the bedroom around one bed/bedside/wardrobe furniture family;
- replaces undercroft, pantry, craft, bath, and Dreaming Floor primitives;
- retains every protected family cutout and authored legacy bed unchanged;
- expands fixed Mobile review from eleven to seventeen contiguous-area views.

The rejected six-view and eleven-view runtime evidence is retained under the
Blender QA source tree. A green structural probe is not promoted without human
inspection of every frame.

## Third Runtime Review And Material Visibility Correction

CI run `29663467793` was fully green and produced all seventeen requested
Mobile frames, but human inspection rejected the art-completeness claim again.
The Toy Room blocks, undercroft barrels/crates, wardrobe sides, and chest lids
rendered as dark slabs even though their isolated source scenes contained color.
The generator had placed an opaque navy object completely around a smaller
colored object to imitate an outline. In an opaque 3D export, that construction
hides the inner form instead of outlining it. The same capture also exposed a
thin Toy Room composition, a repetitive straight storage row, an under-staged
music focal point, and the incomplete half-fish bitmap on the craft easel.

The corrected fifty-four-asset kit now:

- gives the intended color/material ownership of each block, barrel, crate,
  chest lid, and wardrobe body, with dark geometry limited to visible plinths,
  rails, caps, or braces;
- adds a non-plush rainbow stacker, shell drum, sailboat, library reading table,
  and music mallet stand rather than filling rooms with unrelated decoration;
- varies undercroft storage depth and angle so mass placement is not a repeated
  row;
- frames the playable song star with a scaled rainbow gate while preserving all
  seven independent key triggers;
- replaces the incomplete craft bitmap with a complete modeled fish outline;
- retains the already corrected 8,412-triangle Royal Loo mesh and lowers the
  review camera to show its cistern, bowl, pedestal, and continuous rear skirt.

All fifty-four exported GLBs remain one mesh, at 560-6,104 triangles and no
more than twelve material surfaces. The rejected seventeen-view evidence is
retained under `runtime_rejected_50b1907/`; fifteen superseded GLBs are retained
under `backups/art_pre_castle_visibility_2026-07-18/`.

## Toilet Correction

The toilet now has a continuous rear ceramic skirt between cistern and bowl, a
modeled pedestal transition, and a broad two-tone molded S-trap relief visible
from either side. The seat, lid, open bowl, water, terrazzo, shell badge, and
approved palette remain intact. Bounds are unchanged at 4.2 x 3.1267 x 5.0,
the runtime mesh remains at 11 consolidated material-role nodes, and the new
count is 8,412 triangles with zero exported degenerate triangles.

## Integration Contract

- Existing walls, doorway gaps, stair floor zones, and navigation solids stay in place.
- Column and fountain collision uses the existing analytic solid system.
- No new OmniLights were added; authored fixtures wrap the existing lights.
- Protected Huluu remains unchanged; the audited 2/5 generic throne is retained
  in the rollback archive but replaced at runtime by `pearl_shell_throne.glb`.
- The exit gameplay marker remains a plain `Node3D`; the authored gate is visual only.
- Purpose-built settees and poufs replace both the old box cushions and the
  rejected first-pass use of outdoor landmark clouds as furniture.
- `scripts/probe_castle_pearl_art.gd` enforces import budgets, one-mesh exports,
  static-only assets, minimum live placement counts, exit/toilet/music/bed/
  wardrobe/craft/secret-stand contracts, and seventeen fixed Mobile-render
  review captures spanning every contiguous castle wing touched by this pass.

## Current Rating

The fifty-four generated models and isolated renders meet the project's
structural and isolated-visual candidate gate. They are designed as 5/5
replacements, but final 5/5 status is not self-awarded: the material-visibility
correction still requires replacement in-game Mobile captures, gameplay-scale
inspection, and owner acceptance. Particular review attention should go to
Toy Room spacing, storage color read, the song-star canopy, wardrobe front/side
read, the complete craft fish, toilet side anatomy, fountain route clearance,
and repeated arch density.

The prior files are preserved in
`backups/art_pre_castle_pearl_2026-07-18/castle_pre_pearl_assets.zip` for
full pre-pass reversal. The fifteen GLBs superseded by the third review are also
preserved under `backups/art_pre_castle_visibility_2026-07-18/` for direct
file-by-file reversal.
