# Day One 2D Runtime Audit — 2026-07-26

## Result

Static audit passes the owner constraints. Godot runtime validation remains a
CI gate because no Godot binary is installed in this workspace. The trusted
`probe_l2.gd` and new `probe_story_day_one.gd` now enforce the runtime parts of
this contract.

The image-generation attempt for a replacement panorama returned 1774x887. It
was rejected and never copied into the repository. The runtime uses two
project-authored vector masters declared natively at exactly 2048x1024.

## Native plate invariance

| Runtime master | Native size | SHA-256 |
|---|---:|---|
| `assets/flats/sky_lagoon/main/day_one_promenade_2048x1024.svg` | 2048x1024 | `b1e3346d79671f2616b00b53e6bb1b26cd7470adb777bf0ac48039a5f9f71e77` |
| `assets/flats/dirty_castle/day_one_dirty_castle_2048x1024.svg` | 2048x1024 | `0e90e1e10fb9856a73f08fc9406556ad4a7a0597e049a635dd2520d1b11bf944` |

Evidence:

- Each SVG declares `width="2048" height="1024"` and a matching
  `viewBox="0 0 2048 1024"`.
- The authored master is the runtime `res://` file. There is no smaller source,
  resized export, padded copy, crop, or upscaled derivative.
- Stage 1 fallback and Stage 2 load the same promenade master. Stage 3 fallback
  and the cleaning minigame load the same castle master.
- Display-time Sprite3D pixel sizing and Control layout do not rewrite either
  asset. The probes assert both imported texture dimensions and source-file
  SHA-256 through `FileAccess.get_sha256()`.
- All 36 branch-imported 1024x576 castle frames, their raw sources, and the
  historical 3D-derived room-skin/tooling path were removed from the final
  tree after the owner audit.

## Stage 2 node inventory

The first arrival has 22 Sprite3D art cards; after the one-time imp exits it
has 21. Every card is `shaded = false`, casts no shadow, and carries
`source_path` and `depth_role` metadata.

| Node family | Count | Type | Local depth | Touch/navigation behavior |
|---|---:|---|---:|---|
| `PromenadeBackgroundCard` | 1 | Sprite3D | -18.0 | Noninteractive background |
| Plane, slide, swing, seesaw, castle gate | 5 | Sprite3D | -5.8 to -5.4 | Camera ray intersects each card depth plane |
| Their highlight duplicates | 5 | Sprite3D | about -5.85 to -5.45 | Noninteractive visual focus |
| Three page/frame/highlight sets | 9 | Sprite3D | -4.84 to -4.8 | Camera ray intersects holder depth plane |
| `ArrivalImpCard` | 1 first arrival | Sprite3D | -0.2 | Noninteractive foreground story beat |
| `PromenadeRoshanCard` | 1 | Sprite3D | +0.2 | Follows the hidden navigation proxy |

The background-to-foreground order is therefore real depth, not canvas draw
order. `_target_at()` casts from the active Camera3D to each candidate card's
actual Z plane and selects the nearest positive intersection inside its world
radius. `_set_walk_goal()` independently casts to the promenade walking plane.
`probe_l2.gd` verifies ray hit mapping, walk mapping, depth layers, exact card
count, zero MeshInstance3D, zero CanvasItem world art, and zero shaded cards.

The SideScrollStage root and hidden player are navigation/camera state, not art.
No mesh, model, procedural mesh, Sprite2D, AnimatedSprite2D, TextureRect,
Polygon2D, physics body, or new light depicts the Stage 2 world.

## Cleaning overlay exception inventory

`DirtyCastle2DLayer` is deliberately the allowed exception: a full-screen,
non-navigable UI/minigame implemented as a CanvasLayer containing a Control
root. It sets:

- `presentation_kind = "full_screen_control_minigame"`
- `navigable_world = false`
- `runtime_plate = res://assets/flats/dirty_castle/day_one_dirty_castle_2048x1024.svg`

Its visual nodes are TextureRect/ColorRect and its interactions are Button
Controls. The hidden player does not navigate inside it, world controls are
blocked, and there are no Node3D children. One target Button is enabled at a
time; exactly three explicit presses complete that target and immediately save
it. Timers, physics, idle processing, wrong-tool choices, and passive helpers
cannot complete progress.

## Raster cutout dimensions and hashes

- `assets/sprites/story/arrival_imp.png`: 683x1024 RGBA,
  SHA-256 `ab1026350656ac43f6c4576d4fec6658b61b702fc0cd7801a9e5ea2cc14174d5`.
- The retained cleanup pack contains 54 transparent 512x512 PNG cutouts:
  6 dust-bunny poses, 12 effects, 6 progress icons, 18 generic cleaning
  targets, and 12 tools.
- Existing Stage 2 cards and the three protected activity-page images are
  included read-only in the machine manifest.

The complete 67-file dimension/SHA-256 ledger and machine-readable node
inventory are in
`audit/day_one_2d_runtime_manifest_2026-07-26.json`. The cleanup pack's focused
runtime inventory is in
`assets/castle/dirty_cleanup_2d/manifest.json`.

## Probe coverage

`probe_story_day_one.gd` asserts:

- opening fallback control and stable OGV path;
- native 2K promenade texture and exact source hash;
- unshaded foreground imp and real depth relative to the background;
- exact Stage 2 Sprite3D-only inventory and camera-ray target hit;
- one-time imp persistence;
- Stage 3 reveal and full-screen Control handoff;
- native 2K castle texture and exact source hash;
- no Node3D in the cleaning overlay;
- zero-input non-completion, three-tap completion, and disk persistence;
- no physics bodies or lights in the cleaning overlay.

`scripts/ci.sh` includes this probe in the trusted suite.