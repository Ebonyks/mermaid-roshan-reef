# Sky Lagoon background-resolution audit — corrected 2026-07-29

This file supersedes its earlier long-edge-only audit. The 2172×724 panorama is a preserved low-resolution composition reference, not a runtime-ready three-screen background. Resolution is measured per playable screen.

## Blocking contract

Sky Lagoon is a horizontal 3×1 stage. Each playable screen requires at least 2048×2048 native background coverage, so the continuous stage master must provide at least 6144×2048 pixels while preserving the approved 3.000000:1 aspect ratio and composition. Runtime textures may be at most 1024 pixels on the long edge; an oversized master is retained and sliced losslessly without scaling.

The active assets meet that contract:

| Role | Path | Dimensions | Ratio | SHA-256 |
| --- | --- | ---: | ---: | --- |
| Preserved composition reference only | `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v2_3x1.png` | 2172×724 | 3.000000000 | `7b9e09243311d0bcb9960f3898d13fc5873537f92568397e1b951676f223c0af` |
| Active native master | `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png` | 6144×2048 | 3.000000000 | `017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41` |

Ratio delta is `0.0`. The active master has no stretch, crop, padding, canvas extension, or letterbox. Downsampling the active master to the preserved reference dimensions yields mean absolute RGB delta `0.1127113810`; this is recorded in `audit/sky_lagoon_hd_grid.json`. The 2172×724 comparison overlay remains at `audit/sky_lagoon_panorama_content_invariance_overlay.png` (SHA-256 `b300df1ddb616e873d4c8d3a8d0e0d51eb98d0849a30c9b21266ba48e59f6650`).

## Lossless runtime grid

The master is divided into a 6-column × 2-row grid of twelve non-overlapping 1024×1024 tiles. Three adjacent 2×2 tile groups supply 2048×2048 native coverage to the three playable screens.

| Tile | Master rectangle `(x,y,w,h)` | SHA-256 |
| --- | --- | --- |
| `r0_c0` | `(0,0,1024,1024)` | `5addf12c775f697d89b5f7227485155616558c5c2c3c4b29accc89fd9a93fcdb` |
| `r0_c1` | `(1024,0,1024,1024)` | `ae962d17088df75e6f3db9fd632a1c2f105d91a902996cd5ac5aba184f82fc1d` |
| `r0_c2` | `(2048,0,1024,1024)` | `a5e0dc1e71031ade14059722885bf7905d88f3ea45e9b04e5994cb09ece88850` |
| `r0_c3` | `(3072,0,1024,1024)` | `b423c7c320377e15a38d684d4cec4499c81fa9a31e20bdf4d7dbf051d63c1959` |
| `r0_c4` | `(4096,0,1024,1024)` | `bb674934980b1b3e70dfe4e2fcb0f866e61f0ac6eefc3414b398a6da654f86ac` |
| `r0_c5` | `(5120,0,1024,1024)` | `563cdab3a65bd22518350c441cffd6f0f1173ab51df7d70cf09c11b4c151035c` |
| `r1_c0` | `(0,1024,1024,1024)` | `60b2ca6fb0ed517929a7dcdaa19cc9cf13a61cb27d7a7700c396383c85418a3a` |
| `r1_c1` | `(1024,1024,1024,1024)` | `2fb96fa18f1e9ccec77ba4f1fd162223385fdfaa230f57647f0240de27ca1400` |
| `r1_c2` | `(2048,1024,1024,1024)` | `2c095349af8d05bb11e43f2115406ce55f583eb885f2abf5b7b4faf7cb8b1e28` |
| `r1_c3` | `(3072,1024,1024,1024)` | `1f84c75cdfc85923b2a18011e50ac60e78145ed6a9703f7c99ae26592bb6edb7` |
| `r1_c4` | `(4096,1024,1024,1024)` | `72e54d1d6a1fbfbeba326670c0d0c640d582b0a60f89d95db77ebcec1257e9c4` |
| `r1_c5` | `(5120,1024,1024,1024)` | `6ef1dd25a1ea4ee998886d6e0c5a824ef915dddb2cff786ffad5520ba0aa2e21` |

Runtime paths follow `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{column}.png`. The cards are unscaled, non-billboarded Sprite3D nodes at coherent depth `z=-18.0`; columns use `x=-60,-36,-12,12,36,60` and rows use `y=21.5,-2.5`.

## Seam and runtime evidence

All six grid-boundary measurements pass. The worst seam/near-seam jump ratio is `1.0279491576`, at vertical pixel 4096. The visual seam capture is `audit/sky_lagoon_hd_seam_capture.jpg`, 720×448, SHA-256 `554bdfc08f39ae50df223666c492300a3ad16e9ff0048645e49a72d9200e2935`.

`tools/audit_sky_lagoon_hd_grid.py` regenerates the dimension, hash, rectangle, downsample-invariance, and seam evidence. `scripts/probe_l2.gd` independently blocks on the 6144×2048 master, twelve 1024×1024 textures, the exact twelve card positions, a single coherent mural depth, disabled billboarding, world-camera ownership, world touch projection, zero mesh/world CanvasItem art, 34 Sprite3D cards total, and at most 29 visible cards in the audited Day One frame.

## Rejected interpretation

A 2172×724 or 1774×887 panorama is below the per-screen native coverage requirement. A three-screen stage does not become compliant merely because its panorama long edge exceeds 2048. Upscaling, padding, changing aspect ratio, or re-labeling logical stage coordinates as pixels does not cure the deficiency.
