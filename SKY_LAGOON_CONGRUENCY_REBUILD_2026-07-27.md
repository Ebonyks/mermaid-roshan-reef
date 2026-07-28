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
- The 2026-07-28 fit correction reduced the slide to 13.8 world units, swing
  to 13.3, and seesaw to 6.8, preserving each ground contact and rescaling
  Roshan's equipment-relative animation paths. The west fir moved from the
  lagoon edge to the planted shoreline at x = -41.5.
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
| Sprite3D world cards | 44 |
| Visible Sprite3D cards at probe frame | 34 |
| Background panorama cards | 4 |
| Contact-shadow Sprite3D cards | 14 |
| Distinct real-depth layers | 5 |
| MeshInstance3D / runtime meshes | 0 |
| Sprite2D / AnimatedSprite2D / Polygon2D / world CanvasItem art | 0 |
| Shaded world sprites | 0 |

The four background tiles occupy one coherent depth plane. Foreground,
activity props, vegetation, Roshan, and contact shadows occupy separate
z-depths, preserving parallax and occlusion ordering. Touch targets remain
world-to-screen projected areas around the corresponding Sprite3D card.

## Master, aspect ratio, and lossless tiling

The approved master is 2172×724 pixels, exactly 3.000000:1, with a native
long edge above 2048. The previous approved 3×1 layout was also 2172×724, so
the aspect-ratio delta is 0.000000. No stretch, crop, padding, letterbox, or
canvas extension is used. Because the master exceeds the runtime texture
budget, it is reconstructed from four non-overlapping, unscaled 543×724
tiles:

| Tile | Source rectangle `(x, y, width, height)` | SHA-256 |
| --- | --- | --- |
| 0 | `(0, 0, 543, 724)` | `b056cc6e1b5530115f66e5a327af683f208a5100363958abfb9009fe56ee975d` |
| 1 | `(543, 0, 543, 724)` | `587a32bf2e03b3839f72322f0b4cb4a5576eaa7a1c01275cd3e56a7c3c3cc7ae` |
| 2 | `(1086, 0, 543, 724)` | `f168302a9debcf404bf6b2cd0a104c9ca76e2c43d131e4320ff2a9f9bcdaab13` |
| 3 | `(1629, 0, 543, 724)` | `2b7c843c0d21d06fdf412d8e6b74729043232e6c67e1a84856160c9f4bd4c53b` |

Master SHA-256:
`7b9e09243311d0bcb9960f3898d13fc5873537f92568397e1b951676f223c0af`.

The Level 2 probe traverses all four joins and reports four seam checks with
maximum camera drift of 0.3%, confirming seam-free reconstruction and
continuous navigation. The preview is also 2172×724 and has SHA-256
`41c96ae03c0d40242600dec3aa6d0e168c981d61a1fe1dc0dd735ecee6761025`.

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
