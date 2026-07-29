# Sky Lagoon reductive rebuild handoff — 2026-07-28

## Result

The three-screen promenade is one continuous 6144×2048 clean plate,
reconstructed at runtime by a 6×2 grid of unshaded Sprite3D cards. Each
playable screen receives four native 1024×1024 cards (2048×2048 total native
coverage). The approved low-resolution panorama remains composition reference
only.

The background keeps the connected shore path, open playground clearing,
snow-covered mountain, cabins placed beside rather than on the mountain road,
and the castle approach. Selected baked-in foreground trees and the castle
were removed before the native repaint. Existing approved PNW tree cards and
one full stained-glass castle/drawbridge card restore those elements at scene
depth without duplicate painted silhouettes.

The plane is a Day One arrival card. After seven seconds of the first visit it
is removed with its highlight/touch target and
`save_data["lagoon_plane_departed"]` is written. Revisits do not construct it.

## Node-type inventory asserted by `probe_l2.gd`

| Scope | Day One before departure | Revisit / after departure |
|---|---:|---:|
| Sprite3D world-art nodes | 43 | 40 |
| Visible Sprite3D cards | ≤35 | ≤33 |
| Backdrop Sprite3D cards | 12 | 12 |
| Ambient Sprite3D cards | 3 (2 trees, 1 cloud) | 3 |
| MeshInstance3D world-art nodes | 0 | 0 |
| CanvasItem world-art nodes | 0 | 0 |
| Shaded Sprite3D cards | 0 | 0 |
| Contact-shadow cards | 8 | 7 |
| Interactive targets | 8 | 7 |

HUD, messages, and touch UI remain outside the stage root and are not part of
this world-art inventory.

Depth layers are real scene depths: mural `z=-18.0`, cloud `-16.0`,
castle/Day One plane `-11.0`, rear PNW foliage `-9.0`, playground `-6.0`,
activity frames `-5.0`, near PNW foliage `-1.5`, and Roshan `0.20`. The
approved screen composition is retained with perspective-compensated card
heights and vertical positions. The probe verifies visible, bounded parallax,
near-foliage/player occlusion, non-billboarded backdrop cards, a route spanning
all three screens and ending at the castle door, and Sprite3D-only interactive
world art.

## Resolution and seam evidence

- Approved composition reference: 2172×724, ratio 3.0.
- Native master: 6144×2048, ratio 3.0, ratio delta 0.
- Master SHA-256:
  `2de9b63d8d2e8c531e8d3213b4d92fff8fb65587053252676d94f75ea813d4c5`.
- Runtime grid: 6×2, twelve non-overlapping 1024×1024 PNGs.
- Generated overscan per tile: 115 native pixels.
- All five vertical joins and the horizontal join pass the seam ratio gate;
  worst measured ratio is 1.028 against the 2.0 limit.
- The owner-supplied stained glass changes only pixel bounds
  `[429,213,625,509]`, inside allowed window bounds `[427,210,626,510]`;
  changed pixels outside the window: 0.

Tracked evidence:

- `audit/sky_lagoon_hd_grid.json`
- `audit/sky_lagoon_hd_seam_capture.jpg`
- `audit/sky_lagoon_congruency_preview_3x1.jpg`

## Validation

- GDScript parser: pass.
- Variant-inference linter: pass.
- Python tool compilation: pass.
- Sky Lagoon scene congruency: 9/9 pass.
- HD grid seam audit: pass.
- `probe_l2.gd`: asserts native dimensions, Sprite3D-only structure,
  overdraw budget, tree placement, cloud corridor, continuous route,
  two-press targets, three unique playground animations, and persistent plane
  departure.
- The installed local Godot 4.7 helper did not execute project scripts (it
  emitted only its engine header), so Godot 4.4 runtime evidence is delegated
  to the repository probe workflow before integration to `dev`.
