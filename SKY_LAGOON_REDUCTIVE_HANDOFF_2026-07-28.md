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

The 2026-07-29 playground-fit revision removes all three mismatched lawn
picture easels. The center screen now uses an enlarged slide, a new
single-seat/two-rope mermaid swing, and a low right-side seesaw. Their opaque
silhouettes have measured world gaps of 2.54 and 2.89 units. Roshan's swing
pose is centered on the one chair and horizontally grip-fitted to the two
ropes; slide rung-bounce and seesaw-rock animations remain purpose-built.
The redundant near tree at the screen-one/screen-two boundary was retired,
and a baked oversized conifer was removed through the overscan tile source.

## Node-type inventory asserted by `probe_l2.gd`

| Scope | Day One before departure | Revisit / after departure |
|---|---:|---:|
| Sprite3D world-art nodes | 33 | 30 |
| Visible Sprite3D cards | ≤27 | ≤25 |
| Backdrop Sprite3D cards | 12 | 12 |
| Ambient Sprite3D cards | 2 (1 tree, 1 cloud) | 2 |
| MeshInstance3D world-art nodes | 0 | 0 |
| CanvasItem world-art nodes | 0 | 0 |
| Shaded Sprite3D cards | 0 | 0 |
| Contact-shadow cards | 6 | 5 |
| Interactive targets | 5 | 4 |

HUD, messages, and touch UI remain outside the stage root and are not part of
this world-art inventory.

Depth layers are real scene depths: mural `z=-18.0`, cloud `-16.0`,
castle/Day One plane `-11.0`, rear PNW foliage `-9.0`, playground `-6.0`,
and Roshan `0.20`. The
approved screen composition is retained with perspective-compensated card
heights and vertical positions. The probe verifies visible, bounded parallax,
near-foliage/player occlusion, non-billboarded backdrop cards, a route spanning
all three screens and ending at the castle door, and Sprite3D-only interactive
world art.

## Resolution and seam evidence

- Approved composition reference: 2172×724, ratio 3.0.
- Native master: 6144×2048, ratio 3.0, ratio delta 0.
- Master SHA-256:
  `017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41`.
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
  lawn-picture removal, two-press prop targets, non-overlapping equipment,
  Roshan/swing grip fit, three unique playground animations, and persistent
  plane departure.
- Local Godot 4.4 `probe_l2.gd`: `LAGOON25D|ALL: OK`.
