# Fable Handoff — Hybrid Touch Navigation and Interactable Language

**Project:** Mermaid Roshan: Reef of Light  
**Date:** 2026-07-25; redesign integration 2026-07-26; castle lighting amendment 2026-07-29  
**Audience:** Fable implementation agent  
**Status:** Interaction principles retained; presentation direction updated for 2.5D stages  
**Primary target:** Lenovo Tab M11 and older Android touch hardware, landscape, one non-reading four-year-old

## 0. Redesign integration — living 2.5D stages

The project is migrating authored areas from difficult-to-maintain 3D rooms to
sprite-led 2.5D storybook stages. The touch-ownership and explicit-activation
rules in this handoff remain binding. References below to keeping the 3D world
describe legacy behavior only. They do not authorize new 3D work.

### Main Hall strict-runtime supersession — 2026-08-04

This note supersedes the older eight-tile shaded-receiver and seam-bridge
exception below. The accepted two-screen Main Hall now uses two 3640×2048
screen masters joined losslessly into one 7280×2048 panorama, reconstructed by
sixteen exact, non-overlapping 910×1024 **unshaded Sprite3D** background cards
in a 2×8 grid. Runtime bleed is zero; camera-band culling controls overdraw.
Every door crest, retained throne, touch prop, character, foreground, and
background remains an unshaded depth-tested Sprite3D card. The current blocking
records are
`assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_strict_2k_build_manifest.json`,
`audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_audit.json`, and
`audit/castle_sprite3d/castle_main_hall_redraw_2026-08-03_node_inventory.json`.
Older values remain in this handoff only as dated implementation history.

### Binding 2D-source / Sprite3D-world rule

- All new and replacement artwork is 2D sprite art.
- Every in-world character, creature, prop, foreground, midground, and
  background is an unshaded `Sprite3D` card placed at real scene depth.
- `Sprite2D`, `AnimatedSprite2D`, `TextureRect`, `Polygon2D`, custom
  `CanvasItem` drawing, and screen-locked flat stages are forbidden for
  in-world art. They remain valid only for HUD, menus, touch controls, and
  full-screen interface/story overlays.
- `Node3D` depth containers and a perspective `Camera3D` are presentation
  infrastructure, not 3D art. Cards must keep billboard mode disabled unless
  an explicit world-facing behavior requires it.
- Do not add, generate, rig, render, repair, or extend a 3D model. Do not use
  Blender, Meshy, imported prop kits, GLBs, procedural meshes, mesh halos,
  decals, or other runtime 3D art.
- Never use an interaction task as a reason to preserve a touched legacy 3D
  prop: separate or generate its 2D sprite equivalent and mount that image on
  an unshaded `Sprite3D` card.

2026-07-29 Codex implementation amendment: the Pearl Castle Main Hall has one
narrow, audited exception to the unshaded-material rule. Its eight background
Sprite3D tiles are shaded receivers for the touch-controlled SpotLight3D
system. Characters, props, tapestries, foregrounds, and effects remain
unshaded Sprite3D cards; no mesh art is introduced. Speedy enables only the
visible half's two light clusters and at most one shadow map. Preserve this
implemented behavior and its on/off touch contract; do not generalize shaded
backgrounds to other rooms without a separate Mobile audit. Evidence and the
node inventory are in
`audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md`.

The final play-reviewed fixtures remain deliberately quiet, but the room
lighting is now dramatic. Accepted background masters retain their
architectural lamp housings, while six small unshaded pearl-core Sprite3D
cards provide the separable touch/animation surface. Their invisible hit areas
remain preschool-sized. Lit fixture cards use HDR modulation to feed a
castle-specific Environment glow buffer; the four equal-energy pooled
SpotLight3D clusters create warm pools against a lower cool lavender fill.
Turning off the visible half reduces the real lights, fill, glow, and bloom
together. A light tap still has no star burst and only a 3.5-percent pulse.
Do not replace these fixtures with button plaques, large icon cards, halo
sprites, particles, or persistent interaction badges.

The castle Environment is activated only while the Sprite3D room shell owns
the viewport and restores the prior environment on suspend/close. Full
quality uses glow `1.12`, bloom `0.24`, and threshold `0.74`; Speedy clamps
these to `0.75`, `0.11`, and one shadow map. When all fixtures in the visible
half are off, glow/bloom fall to `0.24`/`0.015`. This state-driven envelope is
the required feedback contract and does not add an art card or a light node.

At the raw two-screen join, the accepted masters retain a documented material
and floor-value discontinuity. Runtime repairs it with an alpha-masked,
approved open-corridor Sprite3D card at real depth. That bridge is also the
physical Playroom entrance and has an existing dust-bunny marker. Preserve the
bridge as an architectural layer, not a framed picture or screen overlay.

Every migrated room must now be built as a **living stage**, not a flat
background:

- Roshan moves on an authored floor lane with a real world-Z position and
  perspective/depth scaling.
- Back, touch-prop, mid, player, foreground, and effect bands are explicit
  `Node3D`/`Sprite3D` layers; hotspot and UI layers alone are `Control`.
- At least three visually obvious room props are independently touchable.
- Touchable props are separated into tight alpha sprites and removed from the
  runtime clean background plate. The immutable source composite may retain
  them only as an art source and is never rendered as the runtime backdrop.
- Item, midground, and foreground masks have exclusive pixel ownership: a
  recognizable object cannot be baked into the clean plate or duplicated
  across multiple `Sprite3D` cards.
- One direct tap owns the prop interaction and must not also move Roshan.
- The prop acknowledges within 100–150 ms with a short animation, a relevant
  sound, and restrained visual feedback.
- Decorative prop touches do not award progress, open activities, consume
  currency, or create fail states.
- The same prop cannot stack animations or sounds while its response is active.

The Pearl Castle reference implementation lives in
`scripts/arena/castle_rooms_25d.gd`. Its art/layer audit is
`FABLE_CASTLE_2P5D_LAYER_AUDIT_2026-07-26.md`. That audit includes the exact
runtime node counts and focused Godot evidence for Sprite3D-only world art,
real-Z occlusion/parallax, 51.2 reference PPM, 16:9 aspect preservation,
projected touch mapping, navigation, animation-frame preservation, audio/busy
guards, and the Speedy sparse-layer budget.
`FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json` is the machine-readable
source/clean-plate/card ownership record used by that probe.

The castle route is exclusive as of 2026-07-27. The modeled `CastleHall`
builder, its `hall:*` proximity registry, and the separate courtyard Opera
gate are retired. Entering the castle always opens the Main Hall Sprite3D
stage. Its physical door hotspots and omnipresent Storybook elevator are
parallel picture-first routes to the same rooms, including Opera Hall; neither
route may leave a destination inaccessible. Returning from a room activity
resumes the same stage, and either castle exit must free the stage before
restoring world controls. A future redesign must not reintroduce a model-based
fallback to preserve an old interaction.

### Native-2K environment amendment

The owner's corrected repository-wide source-resolution gate for generated
environment art is:

- Every generated environment master keeps the exact aspect ratio of its
  approved art and has a native long edge of at least 2048 pixels. It may be
  larger; one-pixel rounding tolerance is permitted.
- Never force a landscape, square, portrait, POT, 2:1, or 16:9 format unless
  that is already the approved source ratio. Never enlarge, interpolate,
  AI-upscale, pad, extend, letterbox, or crop a lower-resolution raster to
  comply.
- Preserve the low-resolution approved original as the visual reference.
- Regeneration is resolution/detail fidelity only. Composition, viewpoint,
  palette, lighting, identities, shapes, placement, silhouettes, negative
  space, navigation lanes, sockets, and depth boundaries remain invariant.
- Only an accepted native-2K source or layer may feed a final `Sprite3D`.
- Every accepted file records dimensions, SHA-256, generator path, exact final
  prompt, references/hashes, and visual/programmatic invariance comparisons.
- Preserve any accepted arbitrary-ratio master in full. If it violates the
  runtime texture-size/POT rule, slice it losslessly without scaling into
  non-overlapping tiles no longer than 1024 pixels on either axis, and rebuild
  it seam-free from adjacent `Sprite3D` cards at one coherent depth.
- Use visibility, sparse cards, lossless tiles, and POT import/compression
  controls where applicable for Speedy-tier cost. Never reduce master
  resolution as the fix.

The Pearl Castle's existing 1024×576 plates are therefore structural
references, not final compliant runtime art. Follow
`FABLE_CASTLE_2K_REGEN_HANDOFF_2026-07-26.md` before approving the castle art
handoff.

## 1. Outcome

For untouched legacy areas, interaction behavior may remain temporarily, but
must not be extended with new model art. When an area is migrated, use the
same ownership grammar with Sprite3D stage-floor movement and projected direct
prop hit regions:

1. A reserved lower-left analog zone for manual movement.
2. Tap-to-move and tap-to-interact everywhere else in the unobstructed world.

Add one shared visual and behavioral language for every interactable:

> **Glow → Acknowledge → Approach → Act → Rest**

Proximity advertises that something can be touched. Proximity must not launch an activity. One intentional tap is the activation decision.

The player must always be able to use one finger. Simultaneous stick plus action may remain available, but it must never be required.

## 2. Non-negotiable interaction rules

- A touch receives one owner when it begins and keeps that owner until release.
- Never reinterpret a touch using duration, late movement, or finger number.
- A touch beginning in the lower-left movement zone is movement only.
- A touch beginning on the action control is action only.
- A touch beginning on a visible UI control is UI only.
- A touch beginning on an interactable selects that interactable.
- A touch beginning on open playable space establishes a movement destination.
- Manual analog input immediately cancels auto-movement.
- Auto-movement never resumes after manual cancellation.
- Tap-to-move must never produce jump/action.
- A slow stationary press must not disappear or be reclassified.
- Do not require double-tap, long-press, pinch, rotation, or two-finger camera control.
- Proximity may highlight an activity, but may not start it.
- Give visual feedback within 100–150 ms of an accepted touch.
- If a destination is invalid, choose the nearest safe destination rather than silently rejecting the touch.
- Direct touch on an object takes priority over open-space movement.

## 3. Scope

### In scope

- Deterministic touch routing in `scripts/touch_ui.gd`.
- A real, touch-consuming action button.
- Analog/manual movement and tap-to-move coexisting.
- Tap selection of registered characters, portals, activities, and props.
- Auto-approach to a selected interactable.
- A shared proximity/focus/activation affordance state machine.
- Removal of proximity-only activity launches from the reef friend loop.
- Mobile-safe glows, target rings, acknowledgment animations, and restrained particles.
- Headless probes for touch ownership, passive safety, selection, cancellation, and activation.
- Documentation of the shared input grammar in `MINIGAME_ENGINES.md`.

### Out of scope for this handoff

- Bulk-converting areas that have not received an explicit 2.5D migration task.
- Replacing the 3D renderer or existing environments.
- Converting all minigames to a new engine in the first change.
- The activity shelf/launcher.
- Re-recording objective voice lines.
- Changing save schema, currencies, medals, or progression.
- Replacing protected book art, family voices, or friend art.
- Making foliage, mass props, or interaction markers into physics bodies.
- Adding OmniLights.

### 2.5D touch-prop production contract

Each room's art pass must identify:

```text
immutable source composite (authoring input only)
accepted native >=2K exact-source-ratio master
opaque clean background reconstructed from lossless <=1024 runtime tiles
midground occluders
foreground occluders
touchable prop Sprite3D cards
walkable floor rectangle
projected prop hit rectangles
```

Do not make an entire room-sized transparent layer. Runtime clean background
plates remain opaque RGB. Midground, foreground, and touch props use tightly
cropped alpha textures mounted on unshaded `Sprite3D` cards to control memory
and transparent overdraw. Build the clean plate only from the existing source
composite for reuse-only passes; do not introduce new illustration. Remove
every card-owned object from that plate and make all card masks mutually
exclusive.

Required node inventory for each migrated living stage:

| Runtime role | Allowed type |
|---|---|
| world root and semantic depth bands | `Node3D` |
| perspective projection | `Camera3D` |
| background, characters, props, occluders, shadows, effects | unshaded `Sprite3D` |
| projected hit targets, elevator/menu, touch controls | `Button`/`Control` outside the world root |

The handoff for a migrated area must list actual counts for those roles and
attach probe evidence for node-type compliance, Z ordering/parallax,
pixels-per-meter/aspect, touch projection, navigation, texture-frame
preservation, and transparent-overdraw limits.

Recommended runtime item record:

```gdscript
{
	"id": "toilet",
	"name": "Royal toilet",
	"sprite": sprite,
	"hotspot": hotspot_button,
	"art_rect": Rect2(...),
	"animation": "wiggle",
	"sound": "res://assets/audio/fart.ogg",
	"pitch": 1.15,
	"effect_texture": preload("res://assets/mg/star.png"),
	"effect_color": Color(...),
	"busy": false,
}
```

Animation vocabulary should stay small and reusable:

| Response | Suitable props |
|---|---|
| Pulse | throne, pearl lamp, glowing sign, inspiration board |
| Wiggle/sway | teapot, curtains, stacking toy, toilet |
| Bounce/hover | stuffies, blocks, magic book, paint jars |
| Splash/squash | sink, bathtub, fountain, waterfall, soup pot |
| Spin | floating flowers, wheels, safe turnable ornaments |

Responses should generally last 0.35–0.8 seconds and restore the exact authored
position, rotation, scale, and source texture. Bind tweens to the Sprite3D card so closing or
switching rooms stops them automatically.

Sound design rules:

- Reuse an existing suitable SFX before adding audio.
- Pitch variants may give related props distinct voices without extra files.
- Route prop sounds through the SFX bus and keep them below family voices.
- Water fixtures need a soft water/pop response; toys need a gentle boing or
  giggle; magical props use restrained chimes; comedic bathroom sounds may be
  playful but never shaming.
- One shared room player is sufficient because repeated prop taps are
  intentionally rate-limited.
- Do not use spoken instructions for optional decorative touches.

The hit target may exceed the visible card, but overlapping hit regions must
be resolved during the art audit. Project each card's transformed bounds with
`Camera3D.unproject_position()` and update its transparent `Button`; never
substitute a physics body or a visible `TextureRect`. UI and room-action
controls retain priority over props. Prop controls retain priority over
open-floor movement.

Minimum automated checks for every migrated room:

1. At least three prop records and three touch-consuming hit controls exist.
2. A prop tap does not establish a movement destination.
3. A tap starts one animation and one SFX response.
4. Repeated taps during the response do not stack tweens.
5. Switching rooms frees the previous sprites, effects, and hit controls.
6. Decorative touches do not change save/progression state.
7. Closing the room leaves no looping tween or sound owner.
8. A recursive node inventory finds only `Node3D`, `Camera3D`, and unshaded
   `Sprite3D` below the world root—no `CanvasItem`, mesh, decal, GLB, or
   procedural geometry.
9. A perspective-camera offset produces a larger screen shift for a foreground
   card than the backdrop, proving real depth/parallax.
10. The projected card center remains inside its touch button after camera,
    scale, and animation updates.
11. The runtime background uses the clean-plate asset, not the immutable
    full-room source composite, and contains no recognizable card-owned object.
12. A machine-readable layer manifest reports non-empty card masks and zero
    overlapping owned pixels for every migrated room.
13. Every generated environment master has a native long edge of at least
    2048 pixels, preserves its approved aspect ratio within one-pixel rounding
    tolerance, and records its hash, generator path, final prompt, references,
    and invariance comparison.
14. No lower-resolution source is enlarged, interpolated, AI-upscaled,
    padded, canvas-extended, letterboxed, or cropped to pass the 2K gate;
    runtime size compliance uses lossless non-overlapping ≤1024 tiles whose
    seam reconstruction is verified.

## 4. Existing implementation to preserve or migrate

### Touch input

`scripts/touch_ui.gd` currently interprets:

- First-finger drag as a floating stick.
- First-finger quick release as action.
- Second-finger tap/hold as action.
- Second-finger drag as camera look.

The current classification depends on `TAP_SLOP`, `TAP_MS`, `JUMP_HOLD_MS`, and finger order. This ambiguity is the primary system being replaced.

The visible action bubble is currently a `Panel` with `MOUSE_FILTER_IGNORE`; it looks tappable but is not an isolated button. Convert it to a real touch-consuming control while keeping `action_down`, `action_just`, `set_action_label()`, and `consume_action_just()` compatible with existing callers.

### Player movement

`scripts/player.gd` consumes:

- `touch_ui.stick_vec` for movement.
- `touch_ui.action_down` for jump/swim-up.
- `touch_ui.consume_look()` for camera look.

Do not rewrite the swim controller. Add an auto-movement contribution that uses the same movement path and immediately yields to non-zero manual input.

### Current guidance and activity entry

`scripts/main.gd` already has useful pieces:

- Friend beacons and pillars.
- Gold objective sparkles and a helping current.
- Per-friend discovery, linger, and start radii.
- Existing reaction animations, voice events, and particle helpers.

The current friend loop discovers a friend by proximity and starts the game after lingering inside the start radius. Migrate this to:

- Proximity: discovery and affordance only.
- Tap: focus and approach.
- Arrival: explicit activation.

Do not remove existing save keys such as `found` or `won`.

### Architectural constraint

`ReefMain` remains the state owner. New extracted logic should follow the Phase 7 pattern:

- `RefCounted` helper.
- Typed `var m: ReefMain`.
- Logic only.
- Shared runtime state remains on `main`.

Do not use this feature as an excuse for a broad `main.gd` rewrite.

## 5. Touch ownership model

Use a touch-owner enum or equivalent fixed values:

```gdscript
enum TouchOwner {
	NONE,
	UI,
	STICK,
	ACTION,
	WORLD_INTERACT,
	WORLD_MOVE,
}
```

Track ownership by touch index:

```gdscript
var touch_owners: Dictionary = {} # index -> TouchOwner
```

Assignment priority at touch-down:

1. An active full-screen overlay or GUI control.
2. The real action button.
3. The reserved lower-left movement zone.
4. A registered interactable under the touch.
5. Open-world tap-to-move.

The assigned owner does not change before release.

### Movement zone

- Reserve approximately the lower-left 28–32% of screen width and lower 40–45% of screen height.
- Keep the current floating-stick behavior inside this region.
- Show a faint persistent movement affordance; strengthen it when touched.
- A stationary touch in this zone does nothing beyond showing the stick.
- It must not fire action or world movement when released.
- Important characters and prompts should not be staged behind this screen region.

Use viewport-relative coordinates so the region remains stable under `1280×720` expand scaling and different Android aspect ratios.

### Action button

- Replace the non-interactive action `Panel` with a genuine `Button` or touch-consuming `Control`.
- Preserve the large circular visible treatment.
- Give it a larger invisible hit target than its visible circle.
- Press sets `action_down` and `action_just`.
- Release clears held state after the existing pulse/hold semantics.
- Keep action available as a second touch while the stick is held.
- Use a picture/icon as the primary cue; the existing text label may remain secondary.
- Hidden action controls must not intercept world taps.

### World taps

- World interaction occurs on touch-down after UI/stick/action exclusion.
- No hold-duration gate is required.
- If an interactable is hit, acknowledge and select it immediately.
- Otherwise attempt open-space tap-to-move.
- While the analog stick is actively held:
  - Permit the action button.
  - Permit direct activation of an already-near interactable.
  - Do not establish a distant open-space auto-move destination.
- UI overlays must consume their touches before world routing.

### Camera

- Remove touch-based camera look from the preschool default grammar.
- Preserve gamepad/mouse camera support where it already exists.
- Let existing camera follow, watchdog, and authored minigame cameras continue to operate.
- If a temporary developer setting is needed during migration, keep touch camera behind a disabled-by-default constant. Do not require it for play.

## 6. Interactable design language

### State machine

Use these states:

```text
AMBIENT
DISCOVERABLE
FOCUSED
APPROACHING
READY
ACTIVATING
COOLDOWN
DISABLED
```

#### AMBIENT

- Normal character/prop idle animation.
- No instructional glow.
- The object may still be tappable when clearly visible.

#### DISCOVERABLE

- Entered when Roshan is within the object's discovery radius and it is visible.
- Gentle aqua/lavender breathing halo.
- Optional quiet idle acknowledgment: look toward Roshan, small bob, ear twitch, or prop wiggle.
- No activity starts and no progress is awarded.

#### FOCUSED

- Entered immediately after a valid tap.
- Visible response begins within 100–150 ms.
- Increase halo strength briefly.
- Show a lavender target ring.
- Play one small, rate-limited acknowledgment sound or voice event.
- Start auto-approach when outside activation range.

#### APPROACHING

- Roshan moves toward the object's authored approach point.
- Display a restrained bubble trail or moving target ring.
- Object keeps a mild focus animation.
- Manual stick input cancels this state immediately.
- Losing visibility alone should not cancel a valid approach; invalid/free targets should.

#### READY

- Roshan is inside activation range and in a safe position.
- Character turns toward Roshan or prop performs a readable anticipatory animation.
- Most social/prop interactions should activate automatically at this point because the child already made the intentional tap.
- Activities requiring a deliberate confirmation may reveal the contextual action button.

#### ACTIVATING

- Run the bespoke interaction or existing `_start_game()` entry.
- Ignore repeated activation taps during the transition.
- Play the appropriate animation, voice, sound, and success feedback.

#### COOLDOWN

- Return the object gradually to ambient presentation.
- Prevent chatter and duplicate starts for a short object-specific period.
- Repeatable objects become discoverable again after cooldown.

#### DISABLED

- No glow, hit eligibility, or activation.
- Use while overlays, cutscenes, incompatible minigames, or teardown are active.

### Visual vocabulary

Use a small, consistent semantic palette:

| Meaning | Treatment |
|---|---|
| Touchable nearby object | Aqua/lavender breathing halo |
| Selected destination | Lavender target ring |
| Current objective | Gold sparkle and visual pointer |
| Successful social interaction | Pink heart/star burst |
| Roshan approaching | Short bubble trail |

Do not use red warnings, failure crosses, padlocks, or flashing urgency.

### Glow behavior

- Pulse slowly, approximately 0.8–1.2 Hz.
- Keep size/energy variation subtle, approximately 8–12%.
- Prefer a pooled, tightly cropped unshaded `Sprite3D` halo card or a
  temporary modulation of the target card.
- Do not add an OmniLight for the interaction effect.
- Do not create a new material or particle node every frame.
- Pool target rings and short feedback effects.
- Limit highlighted objects:
  - Current objective always wins.
  - Otherwise, one nearest visible interactable receives the full discoverable treatment.
  - At most two additional nearby objects receive a weaker treatment.
  - On Speedy tier, prefer one discoverable plus one focused object.
- Occluded or off-screen non-objective items do not glow.

### Immediate acknowledgment

Every accepted object tap must visibly respond before travel:

- Character: turn, bob, wave, blink, chirp, or speak.
- Animal: look, hop, tail motion, or heart pop.
- Prop: squash, wobble, rotate slightly, or emit a few bubbles.
- Portal: brighten its rim and send a short directional sparkle.

Do not require a literal double tap. The initial tap is the child's decision.

## 7. Interactable data contract

Keep runtime records on `ReefMain`, for example:

```gdscript
var interactables: Array[Dictionary] = []
var focused_interactable_id: String = ""
var interaction_state: int = 0
var auto_move_active := false
var auto_move_target := Vector3.ZERO
var auto_move_interactable_id: String = ""
```

Recommended record fields:

```gdscript
{
	"id": "friend_huluu",
	"node": node,
	"kind": "friend",
	"enabled": true,
	"objective": false,
	"discovery_radius": 14.0,
	"activation_radius": 6.0,
	"screen_hit_radius_px": 88.0,
	"approach_position": Vector3.ZERO,
	"priority": 20,
	"repeatable": true,
	"cooldown": 0.0,
	"halo": halo_node,
	"target_ring": ring_node,
	"on_activate": callable,
}
```

Values are per-object and must be tuned to current world scale. Preserve existing friend radii initially unless an on-device pass demonstrates a need to change them.

### Registration

Create a typed helper such as:

```text
scripts/interaction_director.gd
class_name InteractionDirector
extends RefCounted
var m: ReefMain
```

Suggested public surface:

```gdscript
func register_interactable(data: Dictionary) -> void
func unregister_interactable(id: String) -> void
func clear_scope(scope: String) -> void
func tick(delta: float) -> void
func handle_world_touch(screen_position: Vector2) -> bool
func cancel_focus(reason: String = "") -> void
func cancel_auto_move(reason: String = "") -> void
func set_enabled(enabled: bool) -> void
```

Do not let this helper own authoritative progress or save state.

## 8. Touch hit testing

Avoid giving every decorative object a physics body.

For the first implementation, use registered screen-space targets:

1. Reject disabled, freed, off-screen, or behind-camera nodes.
2. Project each eligible node or its authored focus anchor with `Camera3D.unproject_position()`.
3. Compare the projected position to the touch.
4. Use a generous per-object screen radius.
5. Score matches by:
   - Objective priority.
   - Explicit interaction priority.
   - Screen-space distance.
   - World distance.
6. Select one best match.

This works consistently for characters, props, portals, and effects that all
use the binding `Sprite3D` card structure, without mass collision objects.

If the project already has a safe collision query for a particular authored object, it may supply a higher-confidence hit, but the shared interaction system must still work without one.

## 9. Tap-to-move

### Two destination types

#### Interactable destination

Use the interactable's authored `approach_position`. This is the reliable default and should ship first.

- Face Roshan toward the target while approaching.
- Stop within `activation_radius`.
- Clamp the destination to existing arena/world bounds.
- Preserve seabed/surface constraints already enforced by the player controller.
- If the direct route is invalid, choose the nearest valid approach anchor.

#### Open-space destination

Ship after interactable approach is stable.

Because the reef is volumetric, an arbitrary screen pixel does not imply an unambiguous underwater depth. Use one of these authored solutions per area:

- An invisible movement sheet/plane.
- A bounded set of navigation anchors.
- A zone-provided projection callback.

For the main reef, the first safe version may move on the current swim-depth plane and clamp vertical position to existing water/seabed clearance. Tapping a character or portal may still move to its full 3D approach point.

Do not introduce a large general-purpose navigation stack before the target-approach behavior is proven. Do not allow pathfinding work to block frames on the target phone.

### Player integration

Prefer a small extracted helper:

```text
scripts/tap_move_director.gd
class_name TapMoveDirector
extends RefCounted
var m: ReefMain
```

Keep destination and active-state fields on `ReefMain`.

The helper should produce a desired movement direction that enters the existing player movement calculation. Do not directly teleport Roshan except for existing recovery logic.

Priority:

```text
manual stick/keyboard/gamepad > cutscene/minigame owner > auto-move > idle
```

Any meaningful manual movement input cancels auto-move before applying velocity.

Auto-move must also cancel when:

- A full-screen overlay opens.
- Pause opens.
- The game/arena mode changes.
- The target is freed or disabled.
- An approach times out.
- The player is placed by a cutscene or recovery system.
- Application focus is lost.

## 10. Friend activity migration

Migrate the five main reef friends first because their existing auto-start behavior demonstrates the complete problem.

Current flow:

```text
Enter discovery radius → show message → linger → activity starts
```

Required flow:

```text
Enter discovery radius → subtle discoverable affordance
Tap friend → immediate acknowledgment → approach
Arrive in activation radius → start existing activity
```

Requirements:

- Preserve `found`, `won`, cooldowns, messages, voices, beacons, medals, and `_start_game()` behavior.
- Discovery may continue setting `found` and saving it.
- Remove the countdown text and proximity-only `_start_game()` call.
- Do not start an activity if the child merely swims past or rests near a friend.
- A tap while already inside activation range may activate immediately.
- A tap from farther away selects and approaches.
- A manual stick movement cancels the approach without penalty.
- After cancellation, the friend remains softly discoverable and may be tapped again.

Once this path is trusted, migrate:

1. Reef activity portals.
2. Shop and treasure entrances.
3. Castle/lagoon interactables.
4. Social animals and repeatable props.
5. Other world entrances.

Keep automatic pearl collection unless play-testing indicates otherwise; collectibles are a different interaction category.

## 11. Suggested file changes

### `scripts/touch_ui.gd`

- Introduce fixed touch ownership.
- Restrict floating stick creation to the movement zone.
- Remove first-finger tap-to-action.
- Remove preschool-default second-finger camera classification.
- Convert the action bubble into a real touch-consuming control.
- Emit or queue world-touch positions for the director.
- Preserve compatibility fields and methods used by existing minigames.
- Clear all ownership and movement state on pause, focus loss, and close.

Suggested signals:

```gdscript
signal world_touched(screen_position: Vector2)
signal manual_move_started
signal manual_move_ended
```

### `scripts/interaction_director.gd` — new

- Registration and cleanup.
- Screen-space selection.
- Proximity ranking.
- Affordance state transitions.
- Focus, approach, activation, and cooldown.
- Pooled/shared visual treatment control.

### `scripts/tap_move_director.gd` — new

- Destination validation.
- Auto-movement desired direction.
- Arrival detection.
- Cancellation and timeout.
- No save or progression ownership.

### `scripts/main.gd`

- Add authoritative interaction and tap-move state.
- Instantiate the two helpers.
- Register friends and the first portal set.
- Replace friend proximity auto-start with explicit activation callbacks.
- Forward world touches.
- Cancel on mode/overlay transitions.
- Tick helpers in the existing world-update path.
- Preserve behavior outside the migrated scope.

### `scripts/player.gd`

- Consume auto-move direction only when manual input is absent.
- Cancel auto-move on manual input.
- Preserve current swim physics and arena early returns.
- Do not absorb interaction selection or progression logic.

### `MINIGAME_ENGINES.md`

Document the canonical grammar:

```text
lower-left drag = manual movement
open-world tap = move
object tap = select/use
visible action control = contextual action
```

State that two-finger input is supported where useful but never required.

### Probes

Prefer focused new probes such as:

```text
scripts/probe_touch_router.gd
scripts/probe_interaction.gd
```

Also extend `probe_passive.gd` so standing near an activity cannot start or win it.

## 12. Implementation sequence

Land this in small, independently gated commits. Follow the repository's extract-don't-rewrite rule.

### Phase 0 — Characterize

- Record current trusted probe results.
- Add deterministic tests for current action, stick, pause, and overlay behavior where missing.
- Add a passive assertion that no activity begins from proximity alone once the migration phase starts.

### Phase 1 — Deterministic touch zones

- Add touch ownership.
- Create a real action button.
- Keep existing analog movement working.
- Do not add tap-to-move yet.
- Gate all trusted probes and manually verify touch overlays.

### Phase 2 — Interactable registry and affordances

- Add `InteractionDirector`.
- Register main reef friends.
- Add discoverable/focused visual states.
- Do not change activity entry until selection and cleanup are proven.
- Enforce Speedy-tier highlight limits.

### Phase 3 — Explicit friend activation

- Remove friend proximity auto-start.
- Tap a near friend to start.
- Preserve discovery and progress behavior.
- Extend passive and interaction probes.

### Phase 4 — Auto-approach

- Add `TapMoveDirector`.
- Tap a distant friend to acknowledge, approach, and activate.
- Manual input cancels.
- Validate mode transitions, pause, focus loss, and target deletion.

### Phase 5 — Open-space tap-to-move

- Add area-authored movement projection.
- Start with the main reef.
- Keep analog available at all times.
- Do not enable open-space tapping in an arena until its movement surface is explicitly defined and tested.

### Phase 6 — Broader migration

- Portals, shop, castle/lagoon, social animals, and safe props.
- Consolidate duplicate affordance code only after behavior matches.
- Do not migrate specialized minigame controls mechanically without a dedicated behavior review.

## 13. Probe requirements

At minimum, automate these cases:

1. Touch beginning in the movement zone owns the stick until release.
2. A stationary movement-zone touch does not jump, activate, or move to a destination.
3. Movement-zone drag produces stick movement.
4. Touch on the action button produces action and no world tap.
5. Touch on an overlay produces no world tap.
6. World touch never produces jump.
7. A near interactable becomes discoverable but does not activate passively.
8. Tapping a near interactable activates exactly once.
9. Tapping a distant interactable establishes focus and auto-approach.
10. Manual input cancels auto-approach immediately.
11. A freed/disabled target cancels safely.
12. Pause and focus loss clear every touch owner and auto-move state.
13. Mode change clears focus and auto-move.
14. Passive probe can stand inside former friend linger radius without starting a game.
15. Save/load remains compatible and no key is removed.
16. Existing keyboard and gamepad controls still function.

Before every push:

```text
python -m gdtoolkit.parser <changed .gd files>
python tools/lint_inference.py <changed .gd files>
```

Then run the full trusted gate:

```text
GODOT=<godot binary> scripts/ci.sh
```

If no local Godot binary is available, push only to the task branch and require the probe workflow to be green before integration.

## 14. On-device acceptance criteria

The feature is not complete based only on headless probes. On the target Android device verify:

- Roshan can choose analog or tapping without a settings screen.
- A child can tap a visible friend and understand the response immediately.
- Swimming near a friend never unexpectedly starts a game.
- Manual movement always overrides auto-movement.
- No accepted tap appears dead.
- No tap on a menu leaks into the Sprite3D world stage.
- The action control remains easy to press while the stick is held.
- Open-space tapping does not send Roshan to surprising depths.
- Roshan does not become stuck behind scenery while auto-approaching.
- At most the allowed number of objects glow.
- Speedy tier sustains the 30 fps target without new light or transparency spikes.
- Five-minute repeated interaction produces no particle/node growth.
- Pausing, backgrounding, and resuming clears stuck movement/action state.

Child-facing success targets:

- The desired friend can be selected on the first or second touch.
- The next interaction is understandable without reading.
- The child can cancel an approach simply by moving manually.
- The child does not need two simultaneous fingers to complete any migrated flow.

## 15. Performance constraints

- Mobile renderer on every platform.
- No new OmniLights.
- No per-frame node/material allocation for glows.
- Reuse or pool rings, halos, and acknowledgment particles.
- Prefer pooled, tightly cropped unshaded `Sprite3D` effect cards.
- Cull affordances for off-screen and occluded objects.
- Speedy tier gets the strictest simultaneous-highlight cap.
- Avoid general world/path searches each frame.
- Never convert mass props, foliage, or decorative life into collision bodies for tapping.
- Profile transparent overdraw around halos and particles on the target device.

## 16. Completion definition

This handoff is complete when:

- Analog and tap-to-move are both available without ambiguity.
- Touch ownership is fixed at touch-down.
- The action bubble is a real input control.
- Touch camera is not part of the preschool-default grammar.
- Main reef friends use the shared interactable state machine.
- Proximity advertises but does not launch.
- A tap acknowledges immediately, approaches when necessary, and activates on arrival.
- Manual movement cancels auto-movement.
- Existing save/progression and minigame behavior remain intact.
- Trusted probes and the new touch/interaction probes are green.
- Target-device validation meets the acceptance criteria above.

## 17. Stop conditions

Stop and report instead of broadening scope if:

- Implementing tap-to-move would require rewriting the swim controller.
- A proposed solution requires making the world or foliage into physics bodies.
- Activity entry cannot be separated from progression without changing save semantics.
- The current dirty worktree overlaps the required files and cannot be reconciled safely.
- Any trusted probe changes behavior outside the explicitly migrated interaction path.
- Target-device performance falls below the existing Speedy-tier budget.
- Protected family assets would need modification.

The intended result is not “Roshan plays itself.” It is a depth-layered
Sprite3D storybook world in which the child may either steer freely or touch
what she means, and the game always responds in the same readable language.

## 18. Castle room-card interaction amendment — 2026-07-29

The Codex Castle implementation establishes the concrete world-card pattern
for the broader interaction redesign:

- A room background may be reconstructed from several adjacent Sprite3D cards,
  but the background cards never absorb touch props.
- Every animated/touchable room object remains its own Sprite3D with a
  forgiving Control hotspot projected from its authored world rectangle.
- The visual card may animate discreetly while the hotspot remains large.
  Shell lights use this separation: the 96 x 128 fixture card pulses subtly,
  while a 112 x 128 minimum touch target toggles a real light cluster and
  plays the existing chime.
- Door and elevator actions share the same room-transition path. The elevator
  remains fixed Storybook HUD; door art and corridor art remain world-depth
  Sprite3D cards.
- A placement audit must reject a prop when its authored rectangle intersects
  a door approach, even if its hotspot would still technically work.
- Multi-card backgrounds require exact reconstruction checks and a fresh
  Mobile capture. A numerical edge pass alone is insufficient; any visible
  pasted rectangle or blurred transition is rejected.
- Source tile rectangles remain lossless and non-overlapping. When the Mobile
  rasterizer exposes a clear row between exactly adjacent Sprite3D cards, a
  render-only one-pixel edge bleed is permitted only if it duplicates the
  corresponding approved neighboring source row byte-for-byte, changes no
  pixels-per-meter value, and is backed by both a hash manifest and a dark
  Forward Mobile capture.

The focused acceptance probe now covers exact 2K-derived tile grids, object
bounds, depth diversity, animation/audio hooks, fixture alignment, entrance
clearance, junction architecture, light toggling, camera travel, and the
Speedy overdraw cap. Use
`audit/castle_sprite3d/CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md`
as the implementation evidence for this pattern.
