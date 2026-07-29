# Pearl Castle room-led Codex implementation

Date: 2026-07-28  
Implementation: Codex  
Status: accepted after runtime and visual re-audit

## Outcome

The legacy modeled castle hall is no longer instantiated. Pearl Castle now
opens as a two-screen, walkable Sprite3D storybook hub:

- Screen A: courtyard exit, double-width Opera entrance, Library, Kitchen.
- Screen B: Playroom, Craft Room, Mermaid Pool, Bubble Bath, and Huluu's
  far-right throne.
- Eight physical touch doors/throne targets move Roshan to the target before
  entering it.
- The large Storybook elevator remains fixed at bottom-right and opens a
  balanced 3 x 3 picture-only room grid.
- Four reused dust-bunny cards occupy the lower walking lane. They animate and
  play sounds when touched.
- All seven destination rooms use their approved room paintings as the visual
  reference/base, with extracted prop, midground, foreground, character,
  contact-shadow, and effect cards at authored scene Z.

The Mobile-renderer contact sheet is:

`audit/castle_sprite3d/castle_rooms_runtime_contact_2026-07-28.png`

SHA-256:
`dc9b01ca7ad6f3242101adb86be6defe0d7ac97cca8df9a0d73cc3c2e82e385e`

## Runtime topology

The hall is one logical 3344 x 941 art space viewed through a 1672 x 941
camera window. Roshan's X position moves the perspective Camera3D from Screen
A to Screen B. The hall is not two disconnected menus.

Physical targets:

| Screen | Target | Art-space approach |
| --- | --- | --- |
| A | Opera Hall | `(630, 650)` |
| A | Royal Library | `(1135, 660)` |
| A | Royal Kitchen | `(1395, 660)` |
| B | Stuffie Playroom | `(1755, 670)` |
| B | Craft Room | `(2095, 670)` |
| B | Mermaid Pool | `(2500, 670)` |
| B | Bubble Bath | `(2805, 670)` |
| B | Huluu's throne | `(3090, 690)` |

Opera's portal rectangle is 420 art pixels wide; the ordinary doors are
190-280 pixels wide. Door art uses open, lit perspective corridors and large
room pictograms rather than framed room thumbnails.

## Node-type and depth inventory

World root: `Node3D`  
Camera: one perspective `Camera3D`  
World art: unshaded `Sprite3D` only  
Modeled runtime art: zero  
World `CanvasItem` art: zero

Main Hall steady maximum:

| Role | Count | Authored Z |
| --- | ---: | --- |
| Native hall background tiles | 8 | `0.0` |
| Touchable dust-bunny cards | 4 | `2.65-3.55` |
| Roshan cutout | 1 | `1.25-3.15`, derived from foot depth |
| Contact shadow | 1 | just behind Roshan |
| Total visible world cards | 14 | probe-enforced |

Destination-room steady state:

- one approved room-composite Sprite3D at `0.0`;
- three independent touch-prop Sprite3D cards at room-specific Z;
- optional midground Sprite3D at `2.0`;
- two foreground occluder Sprite3D cards at `4.0`;
- Roshan and a contact-shadow Sprite3D;
- transient touch sparkles at `4.35`.

`Control`, `Panel`, `Button`, and `Label` nodes are limited to the HUD,
elevator, invisible touch routing, pause/back controls, and pointers.

## Interaction inventory

Every accessible destination room has three independent touch props. The
Bubble Bath includes bathtub, sink, and toilet. Other rooms expose
room-relevant props such as curtains/chandelier/stage star, kitchen sink/soup
pot/teapot, magic book/pearl table/lamp, stuffie nook/toys, craft board/paint
table/palette, and pool waterfall/float/fountain.

The animation dispatcher supports pulse, hover, bounce, wiggle, spin, sway,
and splash. Each touch also creates Sprite3D sparkles and routes an existing
project sound through `CastleRoomPropSfx`. No new audio was introduced.

The strengthened probe activates one prop in every room and requires both a
live transform animation and a loaded audio stream.

## Resolution and tiling

Accepted Main Hall masters:

| Screen | Dimensions | SHA-256 |
| --- | --- | --- |
| A | 2048 x 1153 | `ae84f4f79a8183312b5ba26b6999f26b69c8a538424b5383a7d6623cc2f275e9` |
| B | 2048 x 1153 | `c333bdbd3243b2cfcd61e9475e7e5449d7165d03ff8413f860535d5ccb811454` |

Both retain the approved near-16:9 ratio within one-pixel rounding tolerance.
No generated pixel was enlarged. Native generator patches were placed
one-to-one into the 2048-pixel master canvases.

The accepted seam-free runtime rectangle is `(376, 212, 2048, 1153)` from
each master, or 1672 x 941. It is divided losslessly into:

- row 0: four 836 x 470 tiles;
- row 1: four 836 x 471 tiles.

All eight tiles are within the 1024-long-edge runtime rule and reconstruct the
two source views pixel-exactly. Rectangles and per-tile hashes are in
`audit/castle_sprite3d/castle_main_hall_2x4_runtime_manifest.json`.

## Generation audit

Twenty-four built-in ImageGen calls were used, below the owner's 25-call
ceiling:

1. Pass 1, two calls: full room-led compositions; retained as composition
   references only because decoded output was below the native-2K gate.
2. Pass 2, eight calls: independent quadrants; rejected for ghost seams.
3. Pass 3, eight calls: contextual quadrants; rejected for inconsistent
   boundary blending.
4. Pass 4, four calls: top/bottom central seam repairs; accepted as native
   one-to-one repair bands, but outer joins still needed correction.
5. Pass 5, two calls: lower-right contextual repairs; accepted. The visible
   runtime rectangle places the remaining join at its outer boundary.

No 25th generation was necessary: the accepted state passed the visual,
structural, interaction, and performance audits.

References, decoded dimensions, hashes, placement rectangles, preserved
rejected outputs, and final prompt text are under
`audit/castle_sprite3d/room_led_iterations/`.

## Visual intervention and rejection record

The first runtime re-audit exposed two unrelated defects:

- Roshan was too large for the hub and collided with the initial dust bunny.
- the old four-column elevator grid left an empty, unbalanced third row.

The accepted correction uses a 190-pixel hall character height, separated
spawn positions, and a centered 3 x 3 elevator grid.

The re-audit also found that the deterministically cleaned destination-room
plates leaked broad scanline-fill regions around low-depth alpha cards on the
Mobile renderer. Tightening the ownership masks reduced the source error to
near zero programmatically but did not clear the real renderer capture. That
state was rejected. Runtime therefore preserves the untouched, approved room
composites as the stable visual base while retaining the separately animated
and depth-positioned cards. This avoids the visible quality regression and
keeps the room paintings as the primary castle style reference.

## Validation

Static gates:

- `python -m gdtoolkit.parser scripts/arena/castle_rooms_25d.gd scripts/probe_castle_pearl_art.gd`
- `python tools/lint_inference.py scripts/arena/castle_rooms_25d.gd scripts/probe_castle_pearl_art.gd`
- Python compile for all touched castle build/slice tools

Godot 4.7.1 validation used the repository's Mobile rendering method because
the working project was already open in another Godot process. The same
scripts target Godot 4.4 APIs.

Final castle probe:

```text
room_stage_open OK
perspective_depth_camera OK
legacy_3d_hall_not_instantiated OK
storybook_elevator_inventory OK
all_eight_rooms_sprite3d_only OK
all_rooms_use_multiple_real_depths OK
approved_room_composites_preserved OK
all_rooms_touch_animation_live OK
all_rooms_touch_audio_live OK
speedy_visible_card_budget OK maximum visible cards=14
main_hall_native_2x4_sprite3d_grid OK
main_hall_physical_portal_inventory OK
main_hall_lower_lane_interactions OK
main_hall_two_screen_camera_travel OK camera_x=9.90
opera_opens_from_elevator OK
opera_returns_to_sprite_room OK
RESULT=OK checks_failed=0
```

## Final subjective re-audit

| Goal | Score | Verdict |
| --- | ---: | --- |
| Castle/room style continuity | 4.7 / 5 | Pass |
| Two-screen hub navigation | 4.6 / 5 | Pass |
| Preschool picture-first affordance | 4.7 / 5 | Pass |
| Depth/parallax/occlusion structure | 4.6 / 5 | Pass |
| Lower-third interaction density | 4.6 / 5 | Pass |
| Mobile readability and card budget | 4.8 / 5 | Pass |
| Overall | 4.67 / 5 | Accepted |

## 2026-07-29 lighting and fixture-continuity addendum

The Main Hall is no longer an unshaded static presentation. Its eight
Sprite3D background tiles are shaded light receivers, driven by a
Mobile-capped pool of four warm SpotLight3D clusters plus one lavender ambient
fill. Only the visible screen half enables its two clusters. Speedy uses one
shadow map; higher tiers may use two.

Six identical, small pearl-core glints now sit over the existing baked fixture
sockets without replacing their architectural housings or modifying either
accepted 2048 x 1153 master. The earlier navy mounted assembly was rejected
after play review because it read as a wall button. A tap now gives only a
3.5-percent pulse, plays the existing chime, and changes associated engine-light
energy; there is no star burst. One independent royal tapestry remains where it
has a clean socket.

The raw A/B master junction has a measured material and floor-value
discontinuity. A lossless alpha extraction of an approved open corridor now
bridges that junction as a shaded Sprite3D at real depth and supplies the
previously missing physical Playroom entrance. Its marker reuses the existing
dust-bunny family cutout. The lower-lane props were also moved clear of the
omnipresent elevator footprint.

The revised Mobile inventory is 23 visible Sprite3D cards, three visible
Light3D nodes, and one Speedy shadow map. The final probe additionally requires
fixture texture identity, tapestry provenance, the architectural bridge and
Playroom hotspot, fixed-UI clearance, a working single-light toggle, and a true
all-lights-off engine state.

Full prompt/provenance, hashes, node inventory, on/off captures, rejection
record, and the superseding 4.62 / 5 audit are in
`audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md`.
The lighting pass used the 25th and final call in the current 25-call castle
ImageGen ceiling.

The later seam/tone/overlap correction used no generation calls. Its
programmatic measurements, hashes, current runtime captures, and source-versus-
runtime junction verdict are in
`audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md`.
