# Fable Handoff — Hybrid Touch Navigation and Interactable Language

**Project:** Mermaid Roshan: Reef of Light  
**Date:** 2026-07-25  
**Audience:** Fable implementation agent  
**Status:** Approved design direction; implementation not started by this handoff  
**Primary target:** Lenovo Tab M11 and older Android touch hardware, landscape, one non-reading four-year-old

## 1. Outcome

Keep the existing 3D world. Replace the ambiguous global touch interpretation with two simultaneous, clearly separated movement systems:

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

- Rebuilding the world as a literal 2.5D side-scroller.
- Replacing the 3D renderer or existing environments.
- Converting all minigames to a new engine in the first change.
- The activity shelf/launcher.
- Re-recording objective voice lines.
- Changing save schema, currencies, medals, or progression.
- Replacing protected book art, family voices, or friend art.
- Making foliage, mass props, or interaction markers into physics bodies.
- Adding OmniLights.

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
- Prefer a shared unshaded halo mesh, billboard, material-emission lift, or instance shader parameter.
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

This works consistently for `Sprite3D`, imported GLBs, procedural meshes, and portals without mass collision objects.

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
- No tap on a menu leaks into the 3D world.
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
- Prefer shared unshaded meshes/billboards and instance shader parameters.
- Cull affordances for off-screen and occluded objects.
- Speedy tier gets the strictest simultaneous-highlight cap.
- Avoid general 3D path searches each frame.
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

The intended result is not “Roshan plays itself.” It is a 3D storybook world in which the child may either steer freely or touch what she means, and the game always responds in the same readable language.
