> **Current-runtime correction (2026-07-29):** Later addenda in this handoff mention the v4 master and older card inventories. The active background is `sky_lagoon_panorama_master_v5_hd_3x1.png`, 6144×2048 at exact 3:1, reconstructed from twelve unscaled 1024×1024 Sprite3D cards. `probe_l2.gd` currently expects 34 Sprite3D world cards and no more than 29 visible at the audited Day One frame. See `SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27.md` for the blocking per-screen resolution evidence.
# Sky Lagoon first-stage rebuild — audit handoff

## Outcome

The Sky Lagoon promenade is one continuous 3×1 stage from the water and
airplane at the west end, through the playground, to the castle drawbridge
and upper mountain path at the east end. The implementation uses unshaded
Sprite3D cards at real scene depth for all in-world art. It introduces no
MeshInstance3D, runtime mesh, GLB, Blender asset, Sprite2D, TextureRect,
Polygon2D, or custom CanvasItem world drawing.

The deterministic scene-congruency gate reports `SCENE_CONGRUENCY 10/10`.
Its machine-readable evidence is `audit/congruency_sky_lagoon.json`, and the
exact-coordinate three-screen preview is
`audit/sky_lagoon_congruency_preview_3x1.jpg`.

## Composition and behavior

- West screen: the approved pearl-green airplane, lagoon water, dock/runway,
  land-rooted PNW firs and currants, flowers, and the intentionally blocked
  water edge.
- Middle screen: child-scaled two-seat swing, rung-ladder slide, symmetric
  seesaw, dense PNW planting, and a clearly enclosed play lawn rather than an
  unexplained exit.
- The final 2026-07-28 silhouette correction measures opaque pixels rather
  than nominal texture rectangles. It places the slide, swing, and seesaw at
  12.0, 11.0, and 4.2 world units with at least 0.5 world units of visible
  grass between neighboring opaque bounds. Roshan's equipment-relative
  animation paths scale with those cards. The west fir remains rooted on the
  planted shoreline at x = -41.5.
- East screen: readable castle façade, Mermaid Roshan stained glass,
  drawbridge entrance, foreground flora, and a separate upper path framed by
  mountains.
- Activity frames retain two-press activation: first press highlights the
  frame, second press opens its picture activity.
- Roshan retains dedicated Sprite3D-card swing, slide, and seesaw sequences.
  Her swing pose tracks the ropes, the slide sequence uses the rung ladder and
  seated descent, and the seesaw sequence rocks through repeated alternating
  bounces.
- Fir and currant cards sway; flower cards bob; cloud families drift using
  transforms on existing Sprite3D cards, without particle systems or new
  per-frame textures.

## Structural inventory

Final `probe_l2.gd` scene inventory:

| Type / property | Count |
| --- | ---: |
| Sprite3D world cards | 52 |
| Visible Sprite3D cards at probe frame | 42 |
| Background panorama cards | 12 |
| Contact-shadow Sprite3D cards | 14 |
| Distinct real-depth layers | 5 |
| MeshInstance3D / runtime meshes | 0 |
| Sprite2D / AnimatedSprite2D / Polygon2D / world CanvasItem art | 0 |
| Shaded world sprites | 0 |

The twelve background tiles occupy one coherent depth plane. Foreground,
activity props, vegetation, Roshan, and contact shadows occupy separate
z-depths, preserving parallax and occlusion ordering. Touch targets remain
world-to-screen projected areas around the corresponding Sprite3D card.

## Master, aspect ratio, and lossless tiling

The approved HD master is 6144×2048 pixels, exactly 3.000000:1. Twelve
independent high-detail repaints were made from a strict 6-column by 2-row
crop grid of the approved 2172×724 composition. A 96px seam-safe transition
retains generated detail in each tile interior and returns to the preserved
source geometry at every boundary. The result is reconstructed at runtime
from twelve non-overlapping, unscaled 1024×1024 Sprite3D cards.

`audit/sky_lagoon_hd_grid.json` records old/new dimensions, ratio delta,
master hashes, all twelve tile rectangles and hashes, downsampled content
delta, and numerical join checks. `audit/sky_lagoon_hd_seam_capture.jpg`
visually captures all five vertical joins and the horizontal join. Every seam
check passes. The exact 3:1 composition is preserved without stretch, crop,
padding, letterbox, or aspect-ratio change.

## Congruency audit

The audit evaluates the guide's seven criteria for every registered scene
element: palette centroid, luminance anchors, key direction, specular budget,
local contrast, authored/displayed density, and contact-shadow treatment.
All ten registered element families pass all seven criteria:

`cloud`, `activity frame`, `plane`, `swing`, `slide`, `castle gate`,
`Roshan`, `seesaw`, `PNW currant`, and `PNW fir`.

The gate runs in `scripts/ci.sh` and `.github/workflows/probes.yml`. Rejected
generation iterations are retained beside accepted source masters as audit
evidence; runtime directories contain only accepted assets.

## Validation evidence

- Godot headless asset import: passed.
- `python -m gdtoolkit.parser` for changed GDScript: passed.
- `python tools/lint_inference.py` for changed GDScript: passed.
- Python bytecode compilation for the three new tooling scripts: passed.
- `probe_l2.gd`: all navigation, door, activity, animation, seam, node-type,
  overdraw, and shadow checks passed (`LAGOON25D|ALL: OK`).
- Level re-entry probe: stable node counts and 8/8 targets, no duplicate
  level nodes.
- Congruency gate: `SCENE_CONGRUENCY 10/10`.

The complete local suite also exposes unrelated pre-existing failures in
ocean-kingdom return gates, audit/rank save setup, galaxy partial rescue, and
the verb probe under the local Godot 4.7 Windows runner. The Sky Lagoon
probes within that run remain green; the repository's pinned Godot 4.7.1 Linux
CI is the authoritative full-suite result.

## Tree-card and cloud-clearance correction (2026-07-28)

The shoreline tree that read as growing from lagoon water and the two
duplicate fir cards stacked over painted groves have been removed. Three
mural columns were selectively repainted at native tile resolution to restore
sky, mountains, low shrubs, dry ground, and the castle approach. Columns 2,
3, and 5 remain byte-for-byte unchanged from v3.

Two approved PNW evergreen designs are now visible, unshaded Sprite3D cards
at real depth. Each includes a planted shrub-and-stone footing. Their opaque
rectangles are disjoint, remain right of the lagoon-water exclusion, and sit
on dry vegetation. A third size variant remains runtime-ready but is not
instantiated, avoiding unnecessary transparent overdraw.

The former three-cloud family card is now one small cloud Sprite3D. Its
transform wraps only inside the empty upper-center corridor `x=-10..10`,
`y>=28.5`, so it cannot sweep across painted cloud clusters. Tree sway and
cloud drift remain transform-only animations.

Updated `probe_l2.gd` inventory:

| Type / property | Count |
| --- | ---: |
| Sprite3D world cards | 50 |
| Visible Sprite3D cards at probe frame | <=40 |
| Background panorama cards | 12 |
| Planted tree Sprite3D cards | 2 |
| Contact-shadow Sprite3D cards | 12 |
| MeshInstance3D / runtime meshes | 0 |
| Sprite2D / AnimatedSprite2D / Polygon2D / world CanvasItem art | 0 |
| Shaded world sprites | 0 |

The current master is
`assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v4_hd_3x1.png`
(6144x2048, exact 3:1). Runtime reconstruction uses twelve unscaled
1024x1024 `flat_sky_lagoon_main_panorama_v4_tile_*` Sprite3D cards.
`audit/sky_lagoon_hd_grid.json` records dimensions, ratio delta, hashes,
tile rectangles, and numerical seam checks. The exact-coordinate visual is
`audit/sky_lagoon_congruency_preview_3x1.jpg`.
