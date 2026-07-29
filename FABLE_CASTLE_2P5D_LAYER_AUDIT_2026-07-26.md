# Fable Audit — Pearl Castle 2.5D Layering and Navigation

**Date:** 2026-07-26  
**Scope:** Pearl Castle room stages only  
**Target:** one-finger preschool play on Lenovo Tab M11 / Speedy tier  
**Status:** Sprite3D structure is implemented at the preserved legacy
1024×576 source resolution. It is **resolution-nonconforming** under the
owner's corrected native-2K amendment; accepted exact-16:9 source regeneration,
lossless runtime tiling, and the device composition/frame-rate pass are still
required.

## Direction update

This audit supersedes the castle-specific assumptions in
`FABLE_INTERACTION_HANDOFF_2026-07-25.md`. The shared deterministic touch
principles remain valid, but Pearl Castle rooms are now authored as 2.5D
storybook Sprite3D-card stages rather than model-built 3D rooms.

Owner amendment for the redesign: source artwork remains 2D, but every
in-world character, prop, foreground, midground, and background must be an
unshaded `Sprite3D` card at real scene depth. A screen-locked `TextureRect` or
`Sprite2D` stage is nonconforming. Only HUD, menus, touch targets, and
full-screen interface/story overlays may remain `Control`/`CanvasItem`.

The first castle prototype used a single flattened backdrop and moved Roshan
only horizontally. It did **not** meet the 2.5D navigation standard: every
object lived behind Roshan, there was no depth sorting, and several source
views were corridor or close-up compositions rather than playable stages.

## Exclusive runtime route correction — 2026-07-27

The initial integration left the sprite-stage castle behind a feature branch
and retained the modeled `CastleHall` fallback. That made the shipped doorway
capable of entering the old free-roaming 3D game even though the layered room
implementation existed. This is now structurally corrected:

- `scripts/arena/castle_hall.gd` is removed.
- `_enter_castle_interior_now()` has one path: clear the courtyard world,
  establish the `hall` return phase, hide the free-roaming player, and open
  `CastleRooms25D` in `main_hall`.
- The `hall` tick never creates meshes, environments, lights, colliders,
  modeled props, or the old proximity interaction registry.
- No `hall:*` touch targets or retired hall state (`bed_pos`, bells, modeled
  toilet, secret stand, wardrobe, dungeon gate) are populated.
- The modeled courtyard Opera marquee and `court:opera` route are removed.
  Opera Hall is reached only through the Storybook elevator; closing the Opera
  activity resumes `opera_hall`.
- The companion system no longer ticks its modeled throne-gift or physical
  Stuffie Den builders in the hall phase. The Playroom action opens the
  existing storybook stuffie picker.
- Both the courtyard exit and direct Level 2 exit close the castle UI and
  free `CastleRoomsSprite3DWorld`, then restore the appropriate free-roaming
  camera and controls.

The 3D coordinate system remains presentation infrastructure only. It gives
the 2D-source cards perspective, depth-buffer occlusion, and parallax; it is
not a modeled 3D castle.

## Native-2K owner amendment

The corrected owner amendment supersedes both the 1024×576 texture assumption
and the briefly recorded fixed-2048×1024/POT-master rule:

- Every generated background/environment master, far layer, scenic-mid layer,
  floor/skirt plate, room plate, and large environmental occluder must retain
  the exact aspect ratio of its approved art and have a native long edge of at
  least 2048 pixels. It may be larger.
- The eight approved castle references are 1024×576, exactly 16:9. Their
  smallest conforming target is therefore 2048×1152, not 2048×1024. One-pixel
  rounding tolerance is permitted when a generator chooses a larger canvas.
- Enlarging, interpolating, AI-upscaling, padding, letterboxing, or cropping a
  lower-resolution raster does not satisfy the gate.
- The preserved 1024×576 composites remain immutable references. They cannot
  feed the final runtime `Sprite3D` cards after the native-2K migration.
- Each accepted source must record exact dimensions, SHA-256, generator path,
  exact final prompt, reference paths/hashes, and visual plus programmatic
  invariance evidence.
- Resolution/detail fidelity is the only permitted change. Composition,
  viewpoint, palette, lighting, object identities/counts/shapes/placement,
  silhouettes, negative space, navigation lane, interaction sockets, and
  depth boundaries must remain invariant.
- An accepted non-POT or over-1024 master remains preserved in full. Runtime
  copies are losslessly sliced without scaling into non-overlapping tiles
  whose longest edge is at most 1024 pixels, then reconstructed seam-free with
  adjacent unshaded `Sprite3D` cards at one coherent authored depth.
- Performance is solved with active-room visibility, sparse cards, lossless
  runtime tiles, and POT import controls where applicable—not by lowering
  master resolution.

The current 1024×576 clean plates remain in the worktree only as the last
structurally validated reference implementation. They are not approved by the
native-2K gate. `FABLE_CASTLE_2K_REGEN_HANDOFF_2026-07-26.md` records the
rejected wrong-ratio generator attempts and the corrected acceptance workflow.
Neither rejected 1774×887 output was copied into the repository or connected
to runtime art, so there was no stretched/cropped/padded runtime change to
revert.

### Texture-quality precedence

The 2026-07-27 texture review establishes a strict source hierarchy for the
Main Hall redesign and every later castle master:

1. The immutable approved room composites are the sharpest authoritative
   references for painted detail, palette, edge character, and material
   identity.
2. Accepted high-resolution material studies may guide surface fidelity, but
   may not replace the storybook painting or alter its composition.
3. The interpolated clean plates are structural prototypes only. Their
   inpainted regions are visibly softer and may not be used as visual
   references for a production master.

A consistent edge/detail comparison found the original Main Hall composite at
16.19 versus 11.61 for its clean plate, the Kitchen at 21.07 versus 12.66, and
the Library at 18.42 versus 14.50. This confirms that copying or enlarging a
clean plate would preserve the blurred patches rather than recover approved
detail. The production path must begin from the sharp composite and regenerate
connective architecture natively at exact-ratio long-edge ≥2048. It must never
resize, interpolate, sharpen, AI-upscale, or paint over the low-resolution
clean plate.

The following accepted 1254×1254 material sources are secondary fidelity
references only:

| Source | SHA-256 |
|---|---|
| `R032_CASTLE_KITCHEN_COUNTER_TEXTURE__counter_stone_source.png` | `2c7ce73e8e3d03ac69cc716152dbf81a9910d3336ddafb95f767b901e4d9795c` |
| `R033_CASTLE_KITCHEN_FLOOR_TEXTURE__floor_tiles_source.png` | `6cea643df5ee5757bff513193932ec4945b40363a9b9746a96103588bcb9f7b4` |
| `R034_CASTLE_KITCHEN_WOOD_TEXTURE__painted_wood_source.png` | `07bb1d12d11048c1cc114240e7f094f56d6746096838fc7e1030b0b958145cc2` |

They live under
`assets/full_texture_regen_2026-07-18/source_generations/accepted/`.
Production masters remain high-quality lossless PNGs. Only their lossless
≤1024 runtime tiles may feed the unshaded Sprite3D cards.

## Required room-stage contract

Every Pearl Castle room now uses five semantic bands:

1. **Clean background plate, Z=0.00** — one opaque 1024×576 unshaded
   `Sprite3D` card containing architecture and distant dressing. Pixels owned
   by a nearer card are removed from this runtime plate.
2. **Touchable props, authored Z=0.55–4.00** — three tightly cropped unshaded
   `Sprite3D` cards. Their resting projection reconstructs the source
   composition and their transforms animate independently when touched.
3. **Midground, Z=2.00** — sparse route cards such as a reading table. Roshan draws
   behind these when her feet are farther back and in front when she approaches.
4. **Player plane, Z=1.25–3.15** — an explicit room-specific walk rectangle.
   A tap selects horizontal position and real world depth. Roshan crosses the
   midground Z at the room's authored foot threshold and scales from 72% at
   the back to 105% at the front.
5. **Foreground, Z=4.00** — large side-framing `Sprite3D` cards that always occlude Roshan.
   These establish depth without blocking the central one-finger route.

Layer images must be tight alpha crops, not full-screen transparent canvases.
This controls transparent overdraw and uncompressed texture memory on Mali-G52.
The clean background plate remains opaque RGB. The immutable full-room
composite is an art source only and is never rendered at runtime.

Transient feedback uses at most six tightly cropped unshaded `Sprite3D`
sparkle cards per prop touch at Z=4.35, or nine for a room-action celebration.
There are no mesh particles, model props, decals, or runtime-drawn CanvasItem
effects.

## Runtime node-type inventory

| Node / band | Type | Steady count | Compliance role |
|---|---:|---:|---|
| `CastleRoomsSprite3DWorld` | `Node3D` | 1 | sole castle-interior world root; the legacy hall builder is removed |
| `CastleRoomsCamera` | perspective `Camera3D` | 1 | real perspective projection and parallax |
| `RoomBackdrop` | unshaded `Sprite3D` | 1 | current single-room opaque architecture plate |
| `MainHallBackdropGrid` | `Node3D` | 1 in redesigned Main Hall | container only; no visible art |
| `MainHallBackdrop_r*_c*` | unshaded `Sprite3D` | 8 in redesigned Main Hall | exact 2×4 lossless background grid at one Z |
| `TouchableRoomProps` | `Node3D` | 1 | container for three prop cards |
| `Animated_*` | unshaded `Sprite3D` | 3 | separated, independently animated touch props |
| `RoomMidground` | `Node3D` | 1 | container for zero or one sparse regional mid card |
| mid cards | unshaded `Sprite3D` | 0–1 | real-Z regional occluder |
| `RoshanCutout` | unshaded `Sprite3D` | 1 | navigable character card |
| `RoshanContactShadow` | unshaded `Sprite3D` | 1 | generated alpha contact-shadow card |
| `RoomForeground` | `Node3D` | 1 | container for two front cards |
| front cards | unshaded `Sprite3D` | 2 | real-Z foreground occluders |
| `TouchablePropEffects` | `Node3D` | 1 | transient effect-card container |
| `Touch_*` | transparent `Button` | 3 | projected touch routing only; no visible world art |
| elevator, room buttons, exit, action | `Control` subclasses | UI only | permitted Storybook interface |

Structural rule: no `CanvasItem`, `MeshInstance3D`, `MultiMeshInstance3D`,
`CSGShape3D`, `Decal`, model, or procedural mesh node may appear below
`CastleRoomsSprite3DWorld`.

## Room audit

| Room | Previous result | Action | Runtime depth |
|---|---|---|---|
| Main Hall | Good source composition; objects baked into image | Reused art; two native screen masters split into an exact 2×4 backdrop grid; throne, fountains, doors, dressing, and foregrounds remain separate | 8 background tiles + independent depth cards |
| Opera Hall | Wide source stage; objects baked into image | Reused source; cleaned plate and separated stage props/seating | clean plate + 3 props + 2 foreground |
| Royal Kitchen | Strong open floor; objects baked into image | Reused source; cleaned plate and separated fixtures/tables | clean plate + 3 props + 2 foreground |
| Royal Library | Wide source chamber; objects baked into image | Reused source; pearl table is the unique Z=2 prop card | clean plate + 3 props + 2 foreground |
| Stuffie Playroom | Wide source stage; objects baked into image | Reused source; stacking toy and blocks are unique Z=2 prop cards | clean plate + 3 props + 2 foreground |
| Craft Room | Wide source studio; objects baked into image | Reused source; paint table is the unique Z=2 prop card | clean plate + 3 props + 2 foreground |
| Mermaid Pool | Pool needed depth behavior | Reused source; cleaned plate plus one pool band and corner coral | clean plate + 3 props + 1 mid + 2 foreground |
| Bubble Bath | Wide fixture-room source; objects baked into image | Reused source; cleaned plate and separated bathtub, sink, toilet | clean plate + 3 props + 2 foreground |

## Living-room touch items

Each accessible room now exposes three separated touch-prop sprites:

| Room | Touchable props |
|---|---|
| Main Hall | throne, left fountain, right fountain |
| Opera Hall | curtains, chandelier, stage star |
| Royal Kitchen | sink, soup pot/stove, teapot |
| Royal Library | magic book, pearl reading table, pearl lamp |
| Stuffie Playroom | stuffie nook, stacking toy, blocks |
| Craft Room | idea board, paint table, rainbow palette |
| Mermaid Pool | rainbow waterfall, flower float, bubble fountain |
| Bubble Bath | bathtub, sink, toilet |

Every prop has an oversized invisible hit control, an independently animated
alpha `Sprite3D` card, one short sound response, a tap-only Sprite3D effect
burst, and a busy guard that prevents stacked animations. These touches are
decorative and never alter progression.

Animations are transform-based, not atlas animations: each separated prop has
one preserved source frame and uses a short pulse, wiggle, sway, bounce, hover,
spin, or splash tween. The probe retains the `Texture2D` identity across the
animation to ensure the frame is neither replaced nor lost.

### 4.5/5 item-style consistency gate — 2026-07-28

All 24 touch props were rescored against five equal visual criteria: Pearl
Castle palette, navy/gold edge language, rounded shell/pearl shapes, soft
hand-painted texture, and room perspective/scale/function fit. Twenty-two
legacy props passed unchanged. The legacy Main Hall left and right pedestal
fountains scored 3.3/5 and were the only outliers.

The two failing fountain textures remain preserved. Runtime now selects
`room_main_hall_item_fountain_left_v2.png` and
`room_main_hall_item_fountain_right_v2.png`: a tight-alpha extraction and
mirrored instance of the richer shell fountain already painted in the approved
dressed Main Hall concept. The extraction is downsampled once to 214×182 for
the established 1024-wide runtime scale; no low-resolution image is enlarged
and no new object design is introduced. Item IDs, splash animation, sound,
and progression behavior are unchanged. Both remain in the foreground band
at Z=4.15, just ahead of the Z=4.0 side dressing to prevent coplanar sorting.
Their
explicit 220×180 minimum Storybook hit regions expand with camera projection
to cover the complete larger silhouettes.

The tighter silhouette exposed the old clean plate's broad pedestal-fill
regions. Runtime therefore uses `room_main_hall_background_v2.png`, which
refills only the padded legacy-fountain alpha silhouettes from surrounding
pixels in the immutable room composite. The original clean plate remains
preserved. This is still a 1024×576 structural prototype plate and does not
change or claim to pass the blocked native-2K environment-master gate.

After replacement, every effective touch prop scores at least 4.5/5. All 16
foreground card files were also inventoried; their eight composited room pairs
all score at least 4.5/5. The pair score is intentional because mutually
exclusive source-pixel ownership can leave one card visually incomplete when
viewed outside its matching cards.

Evidence:

- `FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md`;
- `audit/castle_sprite3d/castle_item_style_audit.json`;
- `audit/castle_sprite3d/castle_item_style_accepted_contact.png`;
- `tools/audit_castle_item_style.py`;
- `tools/build_castle_item_style_replacements.py`.

## Projection, pixels-per-meter, and touch mapping

- The currently implemented reference art space is 1024×576; Storybook UI
  space is 1280×720. This is retained for structural comparison only.
- The current reference backdrop is 20.0×11.25 world units, giving 51.2
  pixels per meter and preserving 16:9. The accepted native-2K migration must
  preserve that 20.0×11.25 plane. A 2048×1152 accepted master gives 102.4
  pixels per meter on both axes and fills the 1280×720 Storybook stage without
  stretch, crop, padding, canvas extension, or letterboxing.
- The perspective camera sits at local Z=18 with a 58.109° horizontal field
  of view and keep-width behavior. The authored 20-unit width therefore maps
  to the 1280-wide stage even in the probe's square headless viewport; the
  16:9 world image letterboxes with the Storybook UI instead of stretching.
- A crop card at depth `z` uses
  `pixel_size = (20 / 1024) × ((18 - z) / 18)`. This compensates its resting
  projection to the source crop while still producing real perspective
  parallax and depth-buffer occlusion when the camera moves.
- Runtime camera tracking is intentionally tiny (at most 0.04 world units from
  center) to reveal depth without exposing backdrop edges. When an object
  moves, only the same-source clean fill is revealed beneath it; no duplicate
  resting object remains on the background plate.
- Invisible `Button` hit rectangles are UI only. Every frame, the camera
  projects each prop card's center and transformed X/Y extents back into the
  Storybook stage, adds preschool-sized padding, and enforces a 112×112 minimum
  touch target. A moving, scaling, or rotating prop therefore keeps the correct
  hit mapping.

## Navigation and sorting rules

- Room taps map into an authored `Rect2` walk lane; invalid edge taps clamp to
  the nearest safe floor location.
- Roshan's authored foot point, not her Sprite3D origin, determines world Z.
- Scale changes continuously with foot depth to reinforce perspective.
- A room-specific foot threshold maps Roshan below or above Z=2.00 so the depth
  buffer places her behind or in front of midground props without `z_index`.
- Foreground pieces remain nearer to the camera than Roshan at all depths.
- Buttons and the elevator menu remain above every scene layer.
- Existing action entry remains one intentional picture tap; background
  movement never activates an activity.
- The Mermaid Pool permits a farther-back water position. Its water/rim layer
  occludes Roshan's lower body before she returns to the front deck.

## Asset generation and reproducibility

Runtime images live in `assets/flats/castle/rooms/`.

`tools/build_castle_room_layers.py`:

- treats each existing `room_<id>.png` as an immutable source composite;
- builds `room_<id>_background.png` as an opaque clean architecture plate;
- builds authored item, midground, and foreground cards using mutually
  exclusive pixel masks, with touch items taking ownership first;
- replaces card-owned background pixels using horizontal/vertical interpolation
  and nearest-pixel fallback from unowned pixels in the same room source;
- crops transparent margins tightly;
- applies a sub-pixel feather to avoid hard alpha stair-stepping;
- creates the small transparent `room_actor_shadow.png` Sprite3D contact card;
- writes `FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json` with source/background
  hashes, crop bounds, alpha-pixel counts, overlap counts, and clean-plate
  replacement/reconstruction measurements;
- can be rerun deterministically after a source composite is revised.

This depth pass created no new illustration and used no ImageGen, Blender,
model, external texture, or protected asset. It only reorganized pixels already
present in the eight room composites. The manifest records five or six
non-empty art cards per room, zero pixels owned by two cards, and greater than
99.9% replacement of card-owned pixels on every clean background plate.

## Acceptance standard

A castle room is not approved merely because it looks dimensional. It must
pass all of these:

- Roshan can move horizontally and in depth with one tap.
- All world-visible nodes are unshaded `Sprite3D` cards below a `Node3D` world
  root; no in-world `CanvasItem` or mesh art is present.
- At least one authored object can visibly pass in front of Roshan.
- A midground prop, when present, sorts correctly on both sides of its foot
  threshold.
- The central route remains visually open at Roshan's largest scale.
- Roshan never disappears behind an unpainted rectangular mask.
- A prop/occluder recognizable on a `Sprite3D` card is absent from the runtime
  clean background plate beneath it.
- No source pixel is owned by more than one item/midground/foreground card.
- Room UI never falls behind scene art.
- No interaction launches from proximity or movement alone.
- Final background/environment masters are natively generated with a long
  edge of at least 2048 pixels and preserve the exact approved aspect ratio
  within the one-pixel rounding tolerance.
- No lower-resolution raster is enlarged, interpolated, AI-upscaled, padded,
  letterboxed, or cropped to satisfy the final resolution gate.
- Every over-1024 or runtime-nonconforming master/layer is preserved in full
  and losslessly sliced without scaling into non-overlapping runtime tiles
  with a longest edge no greater than 1024 pixels.
- Steady state uses the minimum seam-free background tiles needed for the
  accepted ratio plus no more than one mid, two foreground, three touch-prop,
  one Roshan, and one shadow alpha card before any required large-card tiling.
- Speedy tier holds 30 fps during repeated room changes.
- The target-device pass checks edge taps, all four walk-lane corners, elevator
  opening, room switching, and return from Opera/Craft/Stuffies.

## Validation evidence

Focused structural validation on 2026-07-26, with the exclusive-route
regression pass updated on 2026-07-27:

| Check | Evidence |
|---|---|
| Source syntax and inference | `gdtoolkit.parser`, `tools/lint_inference.py`, and `git diff --check` completed with no errors for every changed GDScript, including the room runtime and updated trusted probes. |
| Asset import | The focused Godot 4.4 runtime probe loaded all eight rooms, eight clean plates, and 41 unique room cards successfully. A fresh full-repository import was stopped after three minutes because unrelated legacy `assets/art35` GLBs repeatedly reference missing embedded texture paths; no castle import error appeared. |
| Exclusive asset ownership | `clean_background_unique_pixel_manifest: OK`: eight clean plates, all cards non-empty, `card_overlap_pixels == 0`, and every room's `changed_owned_ratio > 0.99`. |
| Resting reconstruction | The manifest rebuilds each source composition from its clean plate and unique cards; worst-room mean absolute RGB error is 0.7872/255, and the probe requires every room to remain below 1.0/255. |
| Exact-ratio native-2K gate | `native_2k_environment_gate: FAIL`: expected and blocking. The preserved 1024×576 references remain active because no native long-edge ≥2048, exact-16:9 generator output has been accepted. The rejected 1774×887 attempts were both below 2K and changed the source ratio. |
| Corrected generator retry | Built-in Main Hall attempt C decoded to 1672×941 RGB, SHA-256 `711fe5811ffce1b595400b995aa040a90af9998b3225d788a352d26313cd8ae4`. Its ratio is within 0.5-pixel rounding tolerance, but its long edge is below 2048, so it was rejected and never copied into the repository. |
| Node-type inventory | `probe_crown.gd`: `manifest_sprite3d_node_contract`, `sprite3d_world_root`, `world_has_no_canvas_or_mesh_art`, `backdrop_is_unshaded_sprite3d`, `library_node_inventory`, and `all_room_art_uses_unshaded_sprite3d` all `OK`; Library steady inventory is eight Sprite3D cards. |
| Depth and occlusion | `library_depth_bands`, `sorts_behind_midground`, and `sorts_in_front_of_midground` all `OK`. |
| Perspective/parallax | `real_depth_parallax: OK`; a 0.12-unit camera offset moved the Z=0 backdrop 7.68 screen pixels and the Z=4 foreground 9.87 pixels. |
| PPM and aspect | `reference_pixels_per_meter: OK ppm=51.200`; `backdrop_aspect_preserved: OK`. |
| Touch mapping and navigation | `projected_touch_hit_mapping` and `touch_navigation_maps_to_walk_lane` both `OK`, including the square headless viewport/letterbox case. |
| Animation and audio | Toilet transform animation, single-frame texture preservation, Sprite3D effects, SFX, busy guard, and no-progression mutation all `OK`. |
| Authored object depth | `objects_have_authored_real_depth: OK`: every room has at least two item Z values, and every item card declares unique-object ownership. |
| Speedy structural budget | `speedy_sparse_layer_budget: OK` for all eight rooms: one opaque clean plate, three touch cards, at most one mid card, and two foreground cards. |
| Crown and exit behavior | Crown award, in-castle persistence, no retrigger teleport, and child-selected front-door exit all `OK`. |
| Exclusive runtime route | `probe_crown.gd`: `legacy_3d_castle_hall_not_built`, `sprite_castle_is_only_interior_route`, and `opera_lives_in_elevator_not_3d_courtyard` all `OK`. The deleted `CastleHall` class has no remaining runtime reference. |
| Eight-room runtime inventory | `probe_castle_pearl_art.gd`: all eight rooms are Sprite3D-only, use multiple real depths, remain within nine steady world cards, and Opera opens from and returns to the elevator stage; `RESULT=OK checks_failed=0`. |
| Bathroom and kitchen assets | The updated source probes load the reused background, two foreground, and three item PNGs for each room within the ≤1024 runtime texture budget. Bubble Bath integration reports the tub, sink, and toilet as separate unshaded Sprite3D cards with real depth, touch animation, sound, and foreground occlusion; all `OK`. |
| Touch and teardown | `probe_interaction.gd` reports `ALL OK`; `probe_touch_adversary.gd` reports all 25 fresh-instance scenarios clear. Direct Level 2 exit frees the room UI/world roots and restores controls. |
| Cross-system return behavior | `probe_train.gd` confirms the courtyard train disappears on Sprite3D castle entry and rebuilds after the child-selected exit. `probe_stuffie.gd` confirms the Playroom action opens the existing picker and the full companion suite remains `ALL OK`. |
| Broader Level 2 integration | `probe_l2.gd` reports the retired courtyard Opera marquee `OK`, enters the castle, and completes Level 2 in 61.6 simulated seconds. `probe_audit.gd` reports the Sprite3D stage, retired 3D castle absence, eight-room elevator, Level 2 finish, save, and finale all `OK`. |

This evidence validates structure and behavior, not tablet frame time. The
native-2K asset gate and 30-fps/overdraw result remain acceptance items.

## Remaining device checks

Headless probes can verify state and progression, but visual sorting needs one
short tablet pass. Watch specifically for Roshan's feet crossing the Library
table, Craft worktable, Playroom toys, and Mermaid Pool rim. If a silhouette
clips, adjust only the corresponding polygon in
`tools/build_castle_room_layers.py`; do not destructively edit the immutable
source composite.

## Superseded Main Hall radial-hub concept — 2026-07-27

The existing Main Hall remains the active low-resolution runtime asset, but it
is no longer the approved structural design. The owner rejected two hub
directions during concept review:

1. Destination-room composites placed inside decorative arches read as flat
   pictures in frames, not connected rooms.
2. Doorways placed on an upper balcony were not physically reachable from the
   shared navigation floor.

The replacement Main Hall must be a practical, single-story circulation hub:

- exactly seven destination thresholds, with three to the left of the throne
  socket and four to the right;
- every destination threshold begins on the same continuous walkable floor;
- no destination doorway is on a balcony, mezzanine, stair landing, or raised
  platform;
- a visible, unobstructed floor path connects the central medallion to every
  threshold;
- the center remains reserved for the current
  `room_main_hall_item_throne.png` Sprite3D card, including its red stair;
- each destination is identified by one integrated keystone motif and subtle
  corridor light, never by a pasted room composite;
- each arch is a thick wall opening with a short corridor: separate floor,
  jamb/side-wall, ceiling, and far-turn/far-door depth cues must visibly recede
  behind the Main Hall wall;
- the destination room itself is not visible from the hub.

The runtime implementation must preserve that spatial reading with separate
unshaded Sprite3D depth cards. A compliant corridor is not one transparent
room screenshot placed behind an arch. At minimum, its far cap must sit behind
the hall shell, its floor must meet the Main Hall floor without a screen-space
gap, and its near jamb/arch card must occlude Roshan as she crosses the
threshold. Transition input may fire only after the character reaches the
corresponding threshold; the elevator remains a redundant touch-first route,
not a substitute for inaccessible architecture.

The latest built-in preview demonstrates the approved single-floor topology:

- generator: `builtin:image_gen.imagegen`;
- generator file:
  `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_EZCNDS27NAx75gdNH8Os2UmU.png`;
- decoded dimensions: 1672×941 RGB;
- aspect ratio: 1.776833156;
- SHA-256:
  `b0ee2acfccdf3dc319f23c53655ef6e8c33078a699b8684cc07bcdb77c8f9e09`;
- concept decision: accepted for topology and accessibility only;
- runtime decision: rejected because its long edge is below 2048 pixels.

Do not copy, resize, upscale, pad, or otherwise feed this preview into the
game. A fresh native long-edge ≥2048 exact-ratio master is still required,
followed by lossless ≤1024 runtime tiling, corridor-card extraction, seam
capture, projected touch/navigation tests, node inventory, and Speedy-tier
overdraw validation.

This entire single-screen radial topology was subsequently rejected as
unwieldy and too sterile. It remains here only as decision history and must not
be implemented.

## Approved Main Hall interface direction — horizontal 2×1 strip

The Main Hall is one continuous level exactly two gameplay viewports wide and
one viewport tall. The camera shows one normal 16:9 view at a time and follows
Roshan horizontally. It is not a panorama squeezed into one screen, a radial
room-selector lobby, or a wall that displays all destinations at once.

### Screen A — entry gallery

Screen A preserves the established character of the existing Main Hall and
reuses as much current artwork as possible:

- the red carpet, lavender block architecture, cream-and-gold columns, upper
  railing, chandeliers, shell banners, wall lamps, fountain, small reading/tea
  furnishings, potted coral, and sparkle accents;
- the current character scale, contact shadow, navigation depth, and
  foreground-column occlusion behavior;
- the courtyard exit at the far-left end.

Three real ground-floor corridors are encountered while walking through this
section: Opera Hall, Royal Library, and Royal Kitchen. Their large masks,
storybook, and shell-pot signs sit immediately above the arches. The corridors
are separated by columns, lamps, fountains, and lived-in furnishings rather
than grouped as a destination grid. The red carpet continues horizontally
toward Screen B; there is no throne or physical elevator in Screen A.

The Opera Hall entrance is the deliberate exception to the standard doorway
module. Its clear opening and visual presence are approximately twice the
width of a Library, Kitchen, Playroom, Craft, Pool, or Bath entrance. It keeps
the same floor baseline and remains fully reachable from the carpet. Large
comedy/tragedy masks and tied-back purple curtains announce the grand public
venue; they do not reduce the walkable opening. The Library and Kitchen
entrances retain the standard module so the Opera scale reads immediately.

### Screen B — throne gallery

Screen B continues the same floor, red carpet, wall scale, lighting, columns,
banners, and chandeliers without a scene change or visible seam. Four more
ground-floor corridors are spaced through this section: Stuffie Playroom,
Craft Room, Mermaid Pool, and Bubble Bath. Existing room motifs are reused only
as large, child-readable teddy, palette, droplet, and bubble signs above their
arches; no destination-room props are placed in the hub. Each sign is
approximately one-quarter to
one-third of its doorway width. Destination-room composites must never be
pasted into the doorway.

The existing `room_main_hall_item_throne.png` throne and red stair terminate
the far-right end of Screen B. They remain unchanged Sprite3D art and form the
hall's destination landmark. The staircase meets the shared carpet/walk lane.

### Frame-density amendment

The 2026-07-27 tightened framing supersedes the first wide establishing
previews. In both gameplay views:

- reduce the visible ceiling band by approximately 20% relative to the prior
  approved concept;
- reduce the visible foreground floor band by approximately 20%;
- redistribute that vertical area to the wall, doorway signs, arches,
  thresholds, and visible corridor mouths;
- keep enough foreground floor for Roshan's full authored depth lane and
  foreground occlusion;
- preserve every destination's horizontal order, the double-width Opera
  hierarchy, the far-left courtyard exit, and the unchanged far-right throne;
- make door signs, jambs, curtain edges, gold thresholds, and corridor
  perspective boundaries the cleanest architectural edges in the frame.

This is a camera/framing and focal-hierarchy change, not permission to crop a
door or character, enlarge a low-resolution raster, remove lived-in
furnishings, flatten the depth lane, or redesign the castle. Screen A and
Screen B must use the same wall scale, carpet height, foreground-floor depth,
cornice height, and pixels-per-meter across their shared seam.

### Prop-family and doorway-clearance amendment

The 2026-07-28 compatibility audit **rejects and supersedes** the prior
destination-vignette dressing pass. Exporting Library furniture, Kitchen tea
service, Playroom toys, Craft storage, Pool coral, or Bath baskets into the
Main Hall made the hub read as several asset sets mixed together. It also put
near-depth cards across doorway landings even where the corridor opening
itself remained technically visible.

The Main Hall now follows one strict ownership rule:

- loose floor and foreground dressing must belong to the Main Hall family;
- destination identity is carried by the large wall-mounted symbol above the
  corresponding arch, not by objects borrowed from the destination;
- the entire corridor mouth, gold threshold, and direct landing from the
  threshold to the carpet are protected clear space;
- the projected silhouette of a nearer foreground card counts as an
  obstruction even if its world Z differs from the door;
- destination-room props remain available unchanged inside their source rooms;
  none were deleted or redesigned.

| Screen | Removed from the hub | Resolution |
|---|---|---|
| A | Library console/stool/books/plants; loose Pool coral; cropped Library/Kitchen chair, rug, tea table, cups, and display | Returned to their source-room vocabulary; existing wall/baseboard/floor restored |
| B | Craft/Kitchen wall shelf; Pool shell planter; Library lamp table; Library/Bath chair | Returned to their source-room vocabulary; existing wall/baseboard/floor restored |
| B foreground | Main Hall shell fountain projected below the Stuffie landing | Screen B instance removed; the matching Screen A fountain remains, so no new asset was needed |
| All seven doors | Entire former destination-vignette pass | Rejected wholesale; large above-door pictograms remain the only destination accent in the hub |

The retained loose dressing is deliberately small: Screen A keeps the
far-left coral vase, one between-bay shell fountain, and one far-foreground
shell fountain; Screen B keeps only the far-left coral vase/pearl-table group.
The unchanged far-right throne and stair remain architectural landmarks.
These retained groups are all classified as Main Hall family and their
authored bounds do not intersect any protected door rectangle.

The cleanup reused the tightened screens and performed object removal only.
It generated no replacement furniture or new architectural design. To
minimize raster regeneration, each cleanup candidate is composited over the
original only inside explicit feathered removal regions. Screen A changes
10.81% of the canvas mask and Screen B 24.39%; every pixel outside those masks
has maximum channel delta 0 and is byte-identical to the tightened reference.
The visual/programmatic proof is
`audit/castle_sprite3d/main_hall_dressing_invariance_audit.png`. The rejected
dressed previews remain preserved as negative comparison evidence; they must
not be tiled, displayed as the approved composition, or used as runtime input.

The machine-readable audit is
`audit/castle_sprite3d/main_hall_prop_compatibility_audit.json`. It records
source families, removal decisions, final hashes, exact 1672×941 dimensions,
protected rectangles, retained-prop rectangles, generator paths, and the
all-clear intersection result. The visual proof is
`audit/castle_sprite3d/main_hall_door_clearance_audit.png`.

Production implementation remains stricter than the flattened concept proof:
architecture, door states, props, foregrounds, throne, and characters are
separate unshaded Sprite3D cards at real depth. The protected rectangles map
to navigation and touch coordinates; moving a card in Z never exempts it from
the projected-clearance check.

The existing large turquoise elevator control remains a fixed Storybook HUD
button in both camera views. Pressing it opens the quick-travel menu from
anywhere in the hall; the physical doors remain direct walk-to destinations.
No elevator door, elevator alcove, lift prop, or elevator symbol is baked into
either environment panel. The elevator is an omnipresent, child-friendly UI
route, not a discreet object at one end of the hall and not a replacement for
walkable doors.

### Castle-wide open/closed door language

Every destination uses one consistent architectural module in two readable
states. The state is built from separate unshaded Sprite3D cards, not painted
into the hall background:

| State | Required visual language | Depth and behavior |
|---|---|---|
| Open — inviting and walkable | Cream-and-gold shell arch; twin pearl leaves retracted into side pockets; destination sign at full color with a gentle glow; visible corridor; warm lavender/aqua spill on the threshold; sparse sparkles | Far corridor cap and floor sit behind the hall shell; retracted leaves and near jambs sit in front and can occlude Roshan. Walking across the gold threshold triggers the same transition as the elevator. |
| Closed — gently dreaming | Identical arch, scale, and destination sign; opaque twin pearl-shell leaves meet at a clear center seam; muted destination-color insets; non-glowing sign; pearl clasp with a crescent moon; cool resting shadow; no corridor light or sparkles | Closed leaves form one near-depth occluder across the threshold and block navigation. Touch gives a soft wiggle, visual pulse, and friendly voice response such as “That room is dreaming”; it never creates a fail state or reading requirement. |

The seven initially accessible rooms use the open state. Later bedrooms and
any temporarily unavailable destination use the closed/dreaming state. Door
state changes swap or animate the door-leaf, corridor, glow, and sparkle cards;
they must not replace the whole screen or reveal a flat room screenshot. The
double-width Opera entrance follows the same state language with proportionally
wider leaves and corridor, while all other destinations use the standard
module.

### Runtime and depth contract

- World art remains exclusively unshaded Sprite3D cards at real depth.
- The 2×1 strip is approximately 40 world units wide while each camera view
  retains the established 20-unit width and perspective.
- The camera follows only the horizontal player coordinate and clamps to the
  left and right screen extents. It must not zoom out to show both screens.
- Screen A and Screen B remain separate exact-16:9 source masters, but their
  runtime background is one logical two-row by four-column grid of eight
  adjacent cards. This subdivision changes no art or world dimensions.
- Each production master preserves the approved 1672:941 aspect ratio and has
  a native long edge of at least 2048. With one-pixel rounding, the minimum
  target is 2048×1153. It crops losslessly into a 2×2 group with 1024-pixel
  columns and 576/577-pixel rows. Screen A owns global columns 0–1 and Screen
  B owns global columns 2–3. No scaling, interpolation, overlap, padding, or
  discarded pixel is permitted.
- At a 40×11.255980861-world-unit logical hall size, every tile is exactly
  10 world units wide. The two row heights follow their actual pixel counts
  rather than being forced equal; the manifest derives their centers from the
  576/577 split. Card centers remain X = -15, -5, 5, 15 at one coherent
  background Z. All eight cards use one pixels-per-meter value and unshaded
  material settings.
- A normal camera view needs only its four local background cards. At the
  inter-screen camera seam, at most the adjoining column pair from the other
  screen is additionally visible. Off-view cards are hidden; tiles never
  overlap to conceal a seam.
- Each corridor uses a far cap behind the wall, floor/side-wall depth cues, and
  a near arch/jamb card that can occlude Roshan. A flat doorway screenshot is
  nonconforming.
- Existing throne, Main Hall fountains, columns, banners, lamps, and
  wall-mounted room-symbol cards are preferred over regenerated equivalents.
  Destination-room furnishings stay inside their source rooms. New art is
  limited to connective architecture and corridor surfaces that do not
  already exist.
- The camera seam must preserve carpet, floor perspective, wall courses,
  cornice height, lighting, and pixels-per-meter.
- Walking into a door and pressing an elevator destination must call the same
  room-transition path and preserve save/progression behavior.

The background grid does not absorb doors, props, characters, foregrounds, or
touchables. Those remain independent Sprite3D cards at their existing authored
depth. Touch and navigation coordinates remain in the same
40×11.255980861 logical
hall space; tile ownership must not change a hotspot or walk target.

### Current concept evidence

The built-in concept previews establish composition only and are not runtime
assets:

| Preview | Dimensions | SHA-256 | Decision |
|---|---:|---|---|
| Screen A — clear dressing | 1672×941 RGB | `69aa7e6d3c1566f493683cc6f3df092da7869bf1872bf14e39b5062b5a45444e` | approved composition reference; mixed destination furnishings removed; runtime rejected below 2K |
| Screen B — clear dressing | 1672×941 RGB | `1f5467fc24c9ceea0a2803a6aa5b1417c0d667fc10e3c252767246f5a31c34e2` | approved composition reference; all four entrances and throne approach clear; runtime rejected below 2K |
| Screen A — former dressed pass | 1672×941 RGB | `605cc7838b5b6279424a574ab295eb2368dcdac30a26b2a55f0a4a9867420123` | rejected: mixed Library/Kitchen/Opera props around doors |
| Screen B — former dressed pass | 1672×941 RGB | `bc15736768ae8b2ed9ad18fadca83eed21155cd2d09c4810b37189f3a90710af` | rejected: mixed Playroom/Craft/Pool/Bath props and blocked approaches |
| Open/closed door language | 1672×941 RGB | `d3a29733ab6e097662472c10f37a484932776483172a9d6adedddc6399e23ca8` | state design accepted; implementation must remain separate Sprite3D cards; runtime rejected below 2K |

Accepted cleanup generator paths:

- `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_BvhJfMe0EMr7JlioBl7prWWe.png`
- `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_7DY51my4MF6NriHBHxdDN0KL.png`
- `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_Sdq1b0fsrJVWlJrZ2dIM6hu7.png`

The current review montage is
`audit/castle_sprite3d/main_hall_2x1_interface_concept_clear.png`
(`dd6d0e04b2ec3758d61a9ca40bc060804a48fbd15d6b7b7c0f0a0126a18f334d`).
Its project-local component previews are
`main_hall_screen_a_clear_preview.png` and
`main_hall_screen_b_clear_preview.png` in the same directory. The montage
includes the existing large elevator control only to communicate fixed
interface placement. The prior base and tightened montages remain preserved
as superseded comparison evidence; the two dressed previews are specifically
rejected. The audited source contact sheets are
`castle_existing_prop_candidates.png`
(`2e9f208feb3dd86c1a37be18922dde2b6cf1a71843d16f30fa1fa1dd957fe2e8`)
and `castle_existing_foreground_candidates.png`
(`0350ec3739d5db75f1e5ee582fa561bdf6e6d369eed952d6689269fa894ac315`).
The door-state review board is
`audit/castle_sprite3d/castle_door_open_closed_language.png`
(`dc2bb2ffb670621ffa86d273e96ea6306c3134cbdb5a13229654962cfcf2f622`).

The 2×4 subdivision was demonstrated without changing the approved art:

- proof:
  `audit/castle_sprite3d/main_hall_2x4_tile_layout.png`
  (`7a597ea77c28e6e4c77e0ab6b9537810528da6cbc58a18bac2be460cb9b09571`);
- manifest:
  `audit/castle_sprite3d/main_hall_2x4_tile_manifest.json`;
- preview tiles:
  `audit/castle_sprite3d/main_hall_2x4_tiles_preview/`;
- reproducible slicer:
  `tools/slice_castle_hall_2x4.py`;
- preview tile dimensions: top row 836×470, bottom row 836×471;
- result: both source screens reconstruct pixel-for-pixel with
  `all_sources_reconstruct_exactly: true`.
- primary alignment proofs:
  `main_hall_2x4_exact_reconstruction_screen_a.png` and
  `main_hall_2x4_exact_reconstruction_screen_b.png`; each is reconstructed
  solely from its four lossless cards and is pixel-identical to its source
  screen.

The preview grid proves crop ownership only; it does not make a low-resolution
image more detailed. Production requires two separate native masters with the
approved 1672:941 aspect ratio and a long edge of at least 2048, one per
gameplay viewport. At the minimum long edge, the one-pixel-rounded size is
2048×1153 and its lossless rows are 576/577 pixels. Do not create a single
ultrawide source master. Preserve both full masters and use the slicer to
produce the exact eight runtime cards. Do not resize or otherwise feed the
1672×941 concept previews into the game.

A 2026-07-28 maximum-native retry generated all eight cells independently.
Every output again decoded to 1672×941, so all fail the native ≥2048-long-edge
gate. Only 2 of 10 source-relative seam comparisons pass, and all cells show
composition drift; r1c1 also changes Roshan's identity, pose, outfit, and
scale. No candidate feeds runtime. Exact hashes, dimensions, prompts,
normalized invariance metrics, and seam evidence are in
`audit/castle_sprite3d/main_hall_2x4_max_native_audit.json`,
`audit/castle_sprite3d/main_hall_2x4_max_native_prompts.md`, and the three
`main_hall_2x4_REJECTED_*.png` proof sheets. These rejected sheets are failure
evidence only and must never be presented as the intended stage layout.

### Main Hall polish and foreground-play amendment — 2026-07-28

The currently accepted composition references are now
`main_hall_screen_a_fullres_play_preview.png` and
`main_hall_screen_b_fullres_play_preview.png`, both 1672×941. They correct the
banner and destination-sign language and demonstrate an occupied,
touch-friendly bottom third without importing destination-room furniture into
the hub.

The previews flatten layers only for review. Production must use:

- one native ≥2048-long-edge polished background master per screen, losslessly
  reconstructed by the existing 2×4 card grid;
- four independent unshaded Sprite3D touch-prop cards per screen;
- one independent unshaded Sprite3D contact-shadow card beneath every touch
  prop;
- the elevator as a fixed `Control` HUD, never a world card;
- no `Sprite2D`, `AnimatedSprite2D`, `TextureRect`, `Polygon2D`, custom
  CanvasItem world drawing, model, GLB, or procedural mesh.

The eight touch props reuse only the Main Hall fountain and established
storybook star/shell motifs. Their projected bounds begin below the carpet,
clear every protected door landing, and clear the elevator. Each has a
forgiving non-reading hit target plus an animation and existing sound hook.
The complete node-type inventory, Z order, rectangles, source hashes,
contact-shadow records, and validation results are in
`audit/castle_sprite3d/main_hall_polish_interaction_manifest.json`.

The masked image cleanup is similarly constrained: Screen A's total allowed
sign/fountain mask covers 19.9446%, Screen B's sign mask covers 16.0820%, and
both report exact pixels with maximum channel delta 0 everywhere outside the
allowed regions. The reproducible builder is
`tools/build_castle_hall_polish_interactions.py`.

### Room-led visual-polish supersession — 2026-07-28

The current two-screen topology remains approved. The visual finish of
`main_hall_screen_a_fullres_play_preview.png` and
`main_hall_screen_b_fullres_play_preview.png` does not.

The finished Castle rooms are now the primary art-direction source for the
hub. Kitchen, Library, Playroom, Craft, Pool, Bath, and Opera establish the
required shell architecture, material variety, palette, value range, prop
scale, and clustered activity rhythm. Sky Lagoon and Northern are secondary
references for depth staging and landmark rhythm only.

The former eight-object foreground row remains useful as a hit-size,
Sprite3D-node, and entrance-clearance proof. It is rejected as a composition:
equally spaced stars, fountains, and chimes read as pickups on an empty floor.
Production instead uses two or three asymmetric activity islands per screen,
assembled from coherent Castle-native cards and recent dust-bunny/response
effects. Door landings and the center of the carpet remain clear.

This amendment changes no door order, doorway rectangle, Opera scale,
courtyard exit, camera span, elevator behavior, or far-right throne placement.
It changes the wall/material hierarchy and foreground grouping. New generation
remains limited to connective architecture after reuse is exhausted.

The complete comparison, reuse inventory, screen-by-screen intervention,
depth bands, and acceptance gates are in
`FABLE_CASTLE_VISUAL_POLISH_INTERVENTION_2026-07-28.md`. Review evidence is
`audit/castle_sprite3d/castle_room_led_reference_board.png`, with exact source
metrics and hashes in
`audit/castle_sprite3d/castle_room_led_visual_audit.json`.

### Codex resolution, placement, and junction closure — 2026-07-29

This implementation amendment supersedes the older native-master placeholder
status for the seven destination rooms.

- Opera, Kitchen, Library, Playroom, Craft, Pool, and Bath each preserve their
  approved 1024 x 576 clean plate and own a 2048 x 1152 derived master.
- Each master is cut without scaling into four exact 1024 x 576 runtime
  textures. The runtime displays those four textures as adjacent Sprite3D
  cards at one coherent background depth. Foregrounds, midgrounds, touch
  props, Roshan, and contact shadows remain separate real-depth cards.
- The Main Hall still owns two native 2048 x 1153 masters and eight exact
  runtime cards. A four-pixel edge ramp eliminates sampling cracks; the
  visible screen transition is an accepted-pixel portal, pilaster, and carpet
  inlay at real depth.
- Six shell-light cards use one 96 x 128 accepted-pixel extraction and share
  logical center y=215. Their large invisible touch zones do not alter their
  discreet visual presentation.
- Every destination-room prop rectangle remains inside its authored canvas.
  Every Main Hall prop clears every door approach and the fixed elevator.
- Maximum visible Sprite3D inventory is 25, with three visible lights and one
  Speedy shadow map. World `CanvasItem` and modeled-art counts remain zero.

The owner explicitly authorized the deterministic room upscaling for this
pass. Originals are preserved, aspect ratio delta is 0.0, and every 2 x 2
reconstruction is pixel-exact. Reproduce with
`tools/build_castle_room_2k_tiles.py` and
`tools/build_castle_hall_alignment.py`.

Final evidence is in:

- `audit/castle_sprite3d/castle_room_2k_upscale_manifest.json`;
- `audit/castle_sprite3d/castle_hall_alignment_manifest.json`;
- `audit/castle_sprite3d/castle_tile_tone_audit_2026-07-29.json`;
- `audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md`;
- fresh Mobile captures for all eight rooms in
  `audit/castle_sprite3d/`.
