# Pearl Castle Art Audit and Rebuild

## Scope

This pass addresses the Grand Hall, its ceremonial threshold and throne wall,
the upper gallery visible from the hall, the Cloud Lounge, and the Royal Loo
shape correction. It does not alter protected book art, Huluu, family voices,
friend cutouts, legacy character models, or child-supplied stuffed animals.

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
| `pearl_shell_sconce.glb` | 1,012 | Column light fixture; reuses existing OmniLight |
| `pearl_shell_chandelier.glb` | 5,092 | Main and gallery hanging fixture; reuses existing lights |
| `pearl_floor_medallion.glb` | 2,124 | Entrance ceremonial focal point |
| `pearl_throne_canopy.glb` | 4,444 | Pearl, shell, and restrained rainbow throne frame |
| `pearl_shell_planter.glb` | 3,488 | Integrated planter and modeled leaf family |
| `pearl_shell_bench.glb` | 3,432 | Entrance and Cloud Lounge seating |
| `pearl_shell_fountain.glb` | 2,064 | New side-bay water landmark |
| `pearl_rainbow_gate.glb` | 4,372 | Return threshold replacing the torus marker |
| `pearl_shell_banner_a.glb` | 1,608 | Plum shell-and-wave wall hanging |
| `pearl_shell_banner_b.glb` | 1,608 | Aqua shell-and-wave wall hanging |
| `pearl_stair_rail.glb` | 4,824 | Sloped ceremonial rail for the throne staircase |

The editable source is `assets_src/blender/pearl_castle_kit.blend`; isolated
renders live in `assets_src/blender/qa_pearl_castle_kit/`.

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
- Protected Huluu and the existing throne remain unchanged inside the new canopy.
- The exit gameplay marker remains a plain `Node3D`; the authored gate is visual only.
- Existing authored storybook clouds replace the Cloud Lounge box cushions.
- `scripts/probe_castle_pearl_art.gd` enforces import budgets, one-mesh exports,
  static-only assets, minimum live placement counts, exit/toilet contracts, and
  six fixed Mobile-render review captures.

## Current Rating

The generated models and isolated renders meet the project's structural 4/5
candidate gate. They are designed as 5/5 replacements, but final 5/5 status is
not self-awarded: it requires the fixed in-game Mobile captures, gameplay-scale
inspection, and owner acceptance. Particular review attention should go to
column-capital readability at distance, throne-wall motif balance, staircase
rail alignment, fountain route clearance, and repeated arch density upstairs.

The prior files are preserved in
`backups/art_pre_castle_pearl_2026-07-18/castle_pre_pearl_assets.zip` for
file-by-file reversal.
