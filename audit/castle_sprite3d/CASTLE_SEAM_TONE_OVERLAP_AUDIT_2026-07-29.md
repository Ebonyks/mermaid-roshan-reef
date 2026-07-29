# Pearl Castle seam, tone, placement, and resolution audit — 2026-07-29

## Verdict

Accepted Codex implementation.

- All eight rooms are Sprite3D-only world stages with multiple real depths.
- The seven destination rooms use preserved 1024 x 576 clean plates as
  references and exact 2 x 2 runtime grids cut from 2048 x 1152 derived
  masters.
- The Main Hall remains the approved two-screen stage. Its two immutable
  2048 x 1153 masters feed two same-size derived masters and eight exact
  runtime cards.
- All six interactive shell lights use one discreet accepted-pixel extraction
  and share logical center y=215.
- The A/B junction is an intentional architectural bay made from an accepted
  portal, pilaster, and tapered carpet inlay. The rejected opaque rectangle
  and blurred crossfade are not loaded.
- Every Main Hall prop clears every entrance approach and the fixed Storybook
  elevator.

Final verdicts from `tools/audit_castle_tile_tone.py`:

| Gate | Verdict |
| --- | --- |
| Internal tile splits | PASS |
| Derived A/B join | PASS — exact edge beneath architectural cards |
| Runtime A/B join | PASS — portal, pilaster, and floor inlay |
| Runtime castle-room tone | PASS |
| Fixed-elevator and door clearance | PASS |
| Speedy card/light budget | PASS |

## Resolution and reconstruction

`tools/build_castle_room_2k_tiles.py` produces the seven room masters with
Pillow Lanczos under the owner's explicit 2026-07-29 authorization to upscale
as needed. It preserves the original 16:9 ratio and originals, then cuts each
master without scaling into four 1024 x 576 runtime textures.

| Quantity | Result |
| --- | --- |
| Source room plates | 7 at 1024 x 576 |
| Preserved masters | 7 at 2048 x 1152 |
| Runtime room cards | 28 at 1024 x 576 |
| Ratio delta | 0.0 |
| Crop, padding, or canvas extension | none |
| Tile reconstruction | pixel-exact for all seven rooms |

Machine evidence:

- `castle_room_2k_upscale_manifest.json`
- `castle_room_2k_upscale_contact.png`
- `castle_main_hall_2x4_runtime_manifest.json`
- `castle_main_hall_2x4_runtime_proof.png`

The room contact sheet intentionally exposes the clean plates before their
separate foreground/midground/touch cards are recomposed. Final Mobile
captures such as `kitchen.png` and `playroom.png` verify that the independent
cards restore the complete room without a visible tile boundary.

## Main Hall seam evidence

The metric is mean absolute RGB change at the boundary divided by the average
one-pixel gradient immediately beside it.

| Boundary | Mean abs RGB | Relative to local gradient | Result |
| ---: | ---: | ---: | --- |
| x=836 | 6.5427 | 1.0246 | normal lossless split |
| x=1672 | 0.0000 | 0.0000 | exact derived edge; structurally occluded |
| x=2508 | 6.2735 | 0.9899 | normal lossless split |

At x=1672 the architecture, runner, and foreground-floor bands are all 0.0.
No runtime tile is stretched, padded, overlapped, or resampled after slicing.

Machine-readable evidence:
`castle_tile_tone_audit_2026-07-29.json`.

Annotated reconstruction:
`castle_tile_seam_audit_2026-07-29.png`, SHA-256
`dc6eded05cac3973cd0370661e13e40414d9d1c9cfd8a947009c040f5eeb291b`.

## Reused junction and fixture cards

| Asset | Dimensions | SHA-256 |
| --- | ---: | --- |
| `castle_playroom_portal_cutout_reuse.png` | 250 x 412 | `017e1425f9b4a801d650d6e0d3527e82ff345d453764ac3c421257e97f719db8` |
| `castle_join_column_cutout_reuse.png` | 190 x 941 | `fd5c050bf6115a46da89c4013fc3572592d2cdf5e32913cf7f2681d59d3756ab` |
| `castle_join_floor_inlay_reuse.png` | 48 x 321 | `237a7d55cd761725ba25a259d2dcd30f89f5d99da67ecfff7b443b4026ead88e` |
| `castle_shell_sconce_integrated_reuse.png` | 96 x 128 | `e1de2650ed6b329c678367fd80661d464e60dcf2db3d2bc75cbdad207f59d077` |

These four assets contain only pixels from accepted Main Hall masters plus
deterministic alpha masks. The portal, pilaster, and inlay are shaded
Sprite3D cards. The six shell lights are unshaded Sprite3D cards. There is no
black mount, plaque, star burst, wall-sized alpha patch, model, or mesh.

The hopping dust bunny is at logical (1845, 805), below both neighboring
entrance approaches. The probe compares every touch-card rectangle against
every door approach and the fixed elevator footprint.

## Lighting and tone

All six fixture centers are exactly y=215. Touch still toggles the associated
real SpotLight3D cluster and plays the existing chime; the visible card uses a
restrained pulse.

| Capture | Mean Lab | Delta-E76 to seven-room mean |
| --- | --- | ---: |
| Main Hall Screen A | 57.346, 17.698, -9.838 | 11.562 |
| Main Hall Screen B | 56.604, 14.412, -10.451 | 11.305 |
| Seven-room reference mean | 63.829, 12.027, -1.881 | — |

Both halves pass the established Delta-E76 <= 12 threshold.

## Node and performance inventory

| Runtime world type | Maximum visible | Notes |
| --- | ---: | --- |
| Shaded background Sprite3D | 8 | exact 2 x 4 Main Hall grid |
| Shaded structural Sprite3D | 3 | portal, pilaster, floor inlay |
| Unshaded structural marker Sprite3D | 1 | existing dust-bunny family |
| Unshaded touch-item Sprite3D | 11 | six fixtures, tapestry, four bunnies |
| Player/contact-shadow Sprite3D | 2 | depth-sorted stage actors |
| Visible Light3D | 3 | fill plus visible-half clusters |
| Speedy shadow maps | 1 | pooled cap |
| Modeled or CanvasItem world art | 0 | HUD remains Control-only |

Maximum visible Sprite3D cards: 25, below the probe cap of 26.

## Validation

Focused Mobile-renderer result:

```text
all_eight_rooms_sprite3d_only OK
all_rooms_use_multiple_real_depths OK
all_destination_rooms_use_2k_exact_tile_grids OK
all_destination_room_objects_within_authored_canvas OK
speedy_visible_card_budget OK maximum visible cards=25
main_hall_native_2x4_sprite3d_grid OK
main_hall_screen_join_architectural_bridge OK
main_hall_mobile_light_pool OK visible=3 shadowed=1
main_hall_fixture_height_alignment OK shared_y=215.0
main_hall_objects_clear_all_door_approaches OK
main_hall_touch_lighting_engine OK
main_hall_all_lights_off_affects_engine OK
RESULT=OK checks_failed=0
```

Fresh Mobile captures:

- `main_hall.png`:
  `a89667ea7eb876facde386233b77af27698927f0b6b60abb5e551058618143c2`
- `main_hall_seam_bridge.png`:
  `c1ccfbc0f18994990305ce130b5c0f3bf554d3ace627f0b99dc4e8de1937a8c0`
- `main_hall_screen_b.png`:
  `ab0f77ad46c28c91ad131d5d2c948ff53129ecd92a4b5df268bf918b170bfefa`
- `main_hall_lights_off.png`:
  `8ad58e55bb5f18365b879bfa5559ab96a609244c8c22ca1a1c28d65d02a7f191`

## Generation and provenance note

Two precise-object cleanup candidates were generated after the owner reopened
this correction pass. Each was ratio-preserving registered to its immutable
2048 x 1153 master and accepted only inside the three compact fixture masks
for that screen; every pixel outside those masks is exact. Generator paths,
prompts, dimensions, hashes, mask coverage, and invariance are recorded in
`castle_hall_alignment_manifest.json`.

The runtime fixture, portal, pilaster, inlay, 2K room masters, and all runtime
tiles are deterministic same-source derivatives and required no additional
generation.

## Subjective re-audit

| Goal | Score | Result |
| --- | ---: | --- |
| Fixture integration/discretion | 4.7 / 5 | pass |
| Room resolution and tile reconstruction | 4.9 / 5 | pass |
| Runtime junction continuity | 4.6 / 5 | pass |
| Castle-room lighting tone | 4.5 / 5 | pass |
| Child interaction clearance | 4.8 / 5 | pass |
| Overall | 4.70 / 5 | accepted |
