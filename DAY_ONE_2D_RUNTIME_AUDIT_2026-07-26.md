# Day One 2D Runtime Audit — corrected 2026-07-27

## Result

The fixed-size 2048x1024 amendment is superseded. The two 2:1 SVG plates
introduced under that rule were removed. The corrected Stage 2 runtime now
preserves the approved panorama's exact native 3:1 composition and reconstructs
it from lossless tiles. Stage 3 and cleaning load no generated background plate
until a compliant approved-ratio source exists.

Static audit passes. Godot runtime validation remains a CI gate because no
Godot binary is installed in this workspace. `probe_l2.gd` and
`probe_story_day_one.gd` enforce the runtime structure, camera/touch mapping,
and tile adjacency.

## Ratio correction and rejection ledger

| Artifact | Dimensions | Ratio | Ratio delta vs approved | SHA-256 | Disposition |
|---|---:|---:|---:|---|---|
| Superseded reduced promenade reference | 1024x341 | 3.002932551 | +0.002932551 from native; 0.333px rounding | `2bd485457797d912ab6719efe88403d824acd9f3e79db9dd6cd6b3a7de677a4d` | Removed |
| Canonical native promenade master | 2172x724 | 3.000000000 | 0 | `7952b4579c922025a3030b3ddd976247fde138f697f00468b5a08fd5b88d66e3` | Accepted master; native long edge 2172 |
| Prior forced promenade SVG | 2048x1024 | 2.000000000 | -1.000000000 | `b1e3346d79671f2616b00b53e6bb1b26cd7470adb777bf0ac48039a5f9f71e77` | Removed |
| Prior forced castle SVG | 2048x1024 | 2.000000000 | +0.223166844 from approved castle source | `0e90e1e10fb9856a73f08fc9406556ad4a7a0597e049a635dd2520d1b11bf944` | Removed |
| Earlier generated panorama attempt | 1774x887 | 2.000000000 | -1.000000000 from promenade | `465a8d0c26e2bc0c2452fbde308090d6d54579c7e559a00a01bf1a820efba3d7` | Rejected; long edge below 2048 |
| Approved dirty-castle source | 1672x941 | 1.776833156 | -0.000944622 from 16:9; 0.5px rounding | `0d8256409ae75fa36a2fe1ca734e5a1132120482718bfe13b885aee4f307b3ca` | Preserved outside final tree; below 2048 |
| Constrained built-in castle edit attempt | 1672x941 | 1.776833156 | 0 from approved source | `ba1f7391fdd50b3e0e3ecf1d9ce94316f7fec2ae2b279beb047ab960ae0cd3e4` | Rejected; remained below 2048 |

No rejected output was upscaled, padded, copied into the repository, or sent
through a CLI/API fallback.

## Promenade master invariance

The canonical 2172x724 master is the original project-generated source of
`flat_sky_lagoon_main_panorama.png`. Reducing it to 1024x341 with the same
Lanczos operation reproduces the approved runtime reference exactly:

- maximum per-channel pixel delta: 0;
- mean absolute error: 0;
- RMS error: 0;
- ideal 3:1 short edge at width 1024: 341.333 pixels;
- approved 341-pixel short edge rounding delta: 0.333 pixels, within the
  one-pixel tolerance;
- corrected master ratio delta from exact 3:1: 0.

The master is preserved at
`assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_3x1.png`.
The `assets_src/.gdignore` keeps it out of runtime import.

## Lossless runtime tiles

The non-POT 2172px master exceeds the runtime texture limit, so all source
columns are partitioned without scaling into three adjacent 724x724 PNGs.

| Tile | Source rectangle (x,y,w,h) | SHA-256 |
|---|---|---|
| `flat_sky_lagoon_main_panorama_tile_0.png` | `0,0,724,724` | `78b1a33e5487d9dfbb75ab92fea5de84c20f4c1a7164eb5b1e8c8e9dba842703` |
| `flat_sky_lagoon_main_panorama_tile_1.png` | `724,0,724,724` | `b32ac8aebab3cbdf5d82a00f7004104981039a487ea0df829a44061b5e110a78` |
| `flat_sky_lagoon_main_panorama_tile_2.png` | `1448,0,724,724` | `ee3477137069b0fe3a5e007d84ca79fbdd52e82c2fa796c8ebbd988dcd159e3a` |

Reassembling the three decoded tiles produces a 2172x724 image with maximum
pixel delta 0 and zero nonmatching pixels against the master. The canonical 50% master/reconstruction overlay is
`audit/sky_lagoon_panorama_content_invariance_overlay.png`, SHA-256
`b300df1ddb616e873d4c8d3a8d0e0d51eb98d0849a30c9b21266ba48e59f6650`.
The canonical seam capture is
`audit/sky_lagoon_panorama_seam_capture.png`, SHA-256
`1fa87682faed7114de38ee23648e409cea1cdf038faa19343d5ed724688d0890`.
Its source windows are `(700,0,48,724)` around x=724 and
`(1424,0,48,724)` around x=1448.

## Stage 2 node inventory and depth

First arrival has 24 Sprite3D art cards; after the one-time imp exits it has
23. Every card is `shaded = false`, casts no shadow, and carries
`source_path` and `depth_role` metadata.

| Node family | Count | Type | Local depth | Geometry/touch behavior |
|---|---:|---|---:|---|
| `PromenadeBackgroundCard_00..02` | 3 | Sprite3D | -18.0 | 48x48 world units each; centers -48, 0, +48; exactly adjacent |
| Plane, slide, swing, seesaw, castle gate | 5 | Sprite3D | -5.8 to -5.4 | Camera ray intersects each card depth plane |
| Their highlight duplicates | 5 | Sprite3D | about -5.85 to -5.45 | Noninteractive visual focus |
| Three page/frame/highlight sets | 9 | Sprite3D | -4.84 to -4.8 | Camera ray intersects holder depth plane |
| `ArrivalImpCard` | 1 first arrival | Sprite3D | -0.2 | Noninteractive foreground story beat |
| `PromenadeRoshanCard` | 1 | Sprite3D | +0.2 | Follows the hidden navigation proxy |

All three background cards use identical pixel size, z=-18, and y=24. Their
computed world edges meet with absolute gap <=0.0001. `_target_at()` casts
from Camera3D to each candidate card's actual Z plane and selects the nearest
positive intersection. `_set_walk_goal()` casts independently to the
promenade navigation plane. No MeshInstance3D, procedural mesh, CanvasItem
world art, Sprite2D, AnimatedSprite2D, TextureRect, Polygon2D, physics body, or
new light depicts the Stage 2 world.

## Stage 3 and cleaning fallback correction

The approved 1672x941 dirty-castle source cannot satisfy the >=2048 long-edge
rule without forbidden upscaling. The built-in constrained edit retained its
1672x941 dimensions, so it was also rejected. Consequently:

- the missing Stage 3 movie uses neutral black;
- `DirtyCastle2DLayer` remains a full-screen, non-navigable Control minigame;
- its background is a code-native ColorRect palette, not an image plate;
- transparent target/tool/effect cutouts remain Control children;
- no Node3D, physics, light, timer, or passive helper completes progress.

Layer metadata records
`presentation_kind=full_screen_control_minigame`,
`navigable_world=false`,
`runtime_background_kind=code_native_control_color`, and an empty
`runtime_plate`.

## Probe and audit evidence

`probe_story_day_one.gd` asserts native master dimensions/hash, all three
tile dimensions/hashes/source rectangles, coherent depth, zero world-space
seam gap, 24-card first-arrival inventory, camera-ray touch mapping, one-time
imp persistence, empty cinematic fallback-art paths, the Control-only cleaning
exception, zero-input non-completion, three-tap completion, and disk save.

`probe_l2.gd` independently asserts the 2172x724 source, lossless tile
resources, adjacent card geometry, Sprite3D-only inventory, depth layers,
camera-ray card selection, camera-ray navigation, and Stage 3 handoff.

The canonical panorama audit is `SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27.md`; the day-one machine-readable ledger is
`audit/day_one_background_ratio_2026-07-27/manifest.json`. Runtime seam
rendering remains pending Godot CI; the static source reconstruction and card
edge equations are already exact.
