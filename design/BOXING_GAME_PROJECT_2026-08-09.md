# Opera Boxer Rebuild — Project and Resource Manifest

Date: 2026-08-09
Status: implementation brief
Runtime: Godot 4.7.1-stable, Mobile renderer, fixed 1280×720 Opera stage space

## 1. Scope

Rebuild the existing **Boxer** Opera career as a dedicated touch game. This is
not a new overworld activity, portal, arena, or save track. `OperaAct` continues
to launch `OperaCareerWorld2D`; the boxer career swaps the generic gesture card
and generic `bop` combat for one specialist `Control` surface.

The specialist surface presents two floating padded gloves. Each glove can be
claimed by a separate screen-touch index and pushed forward toward the painted
target. Two-finger play is supported, but never required: one finger can claim,
punch, release, and then claim the other glove. Every phase must be completable
with that sequential one-finger path.

The career has no health, lives, fail screen, damage score, lost combo, lost
progress, or required reaction time. A friendly imp contact is a bubble-shield
pop and short visual recoil only.

## 2. Shipping phase contract

Use these five modes in `OperaCareerWorld2D.PHASES["boxer"]` and set
`FINALE_START["boxer"]` to `3` so **TITLE IMP** and **BELT** form the finale.
Every phase opts out of generic widget selection with `"widget": ""`.

| Index | Phase | Mode | Goal | Existing voice event | Play contract |
|---:|---|---|---:|---|---|
| 0 | GLOVE GUIDE | `boxing_guide` | 2.0 | `op_boxer_work` | A ghost finger demonstrates claiming and pushing each glove forward. One accepted punch from each glove, in either order. |
| 1 | JAB PRACTICE | `boxing_jab` | 4.0 | `op_boxer_jab` | One oversized focus mitt glows at a time. Either glove may hit it; the next mitt appears only after a real child punch. |
| 2 | SOFT GUARD | `boxing_guard` | 3.0 | `op_boxer_duck` | A slow padded counter is telegraphed. Move either glove into the large glowing guard bubble. An unguarded contact is harmless and simply repeats the cue. |
| 3 | TITLE IMP | `boxing_imp` | 6.0 | `op_boxer_bell_chase` | Fight one boxer imp. Punch forward during the bright open/recover cue. Guarded punches bounce softly and do not erase anything. |
| 4 | BELT | `boxing_belt` | 1.0 | `op_boxer_belt` | Push either glove into the glowing belt to finish, then hold the completed tableau for the curtain call. |

Equivalent phase data:

```gdscript
"boxer": [
	{"name": "GLOVE GUIDE", "mode": "boxing_guide", "widget": "", "goal": 2.0, "vo": "op_boxer_work", "voice": "Put a finger on a glove and push it toward the glowing mitt!"},
	{"name": "JAB PRACTICE", "mode": "boxing_jab", "widget": "", "goal": 4.0, "vo": "op_boxer_jab", "voice": "Jab practice! Punch each glowing training pad!"},
	{"name": "SOFT GUARD", "mode": "boxing_guard", "widget": "", "goal": 3.0, "vo": "op_boxer_duck", "voice": "Bring a glove down into the glowing guard bubble!"},
	{"name": "TITLE IMP", "mode": "boxing_imp", "widget": "", "goal": 6.0, "vo": "op_boxer_bell_chase", "voice": "The boxer imp rang the bell! Punch when the bright star opens!"},
	{"name": "BELT", "mode": "boxing_belt", "widget": "", "goal": 1.0, "vo": "op_boxer_belt", "voice": "Punch the glowing championship belt for the curtain call!"},
],
```

The `voice` strings are dialogue/debug companions. Spoken delivery uses only
the already recorded event IDs above. Each objective also has a visible pulse,
target halo, and ghost-finger demonstration; no objective depends on reading.

## 3. Specialist surface contract

Planned class: `OperaBoxingSurface extends OperaGestureSurface` in
`scripts/opera_boxing_surface.gd`.

The subclass preserves the integration methods already expected by the career
world: `configure()`, `set_fill()`, `restart_demo()`, `note_input()`,
`note_result()`, `accept_completion()`, and the inherited `gesture` signal.
`OperaCareerWorld2D` remains the authoritative owner of `phase_index`,
`phase_progress`, competition progress, completion timing, and the win
callback. The surface owns only transient glove, cue, opponent-pose, assist,
and cosmetic-FX state.

### Touch ownership

- Override `_gui_input()`. The generic surface has one shared pointer and does
  not preserve screen-touch indices, so it cannot drive two gloves safely.
- Maintain a `finger_to_glove` dictionary and one claimed finger ID per glove.
- A press claims the nearest unclaimed glove within a generous home/hit region.
  A second finger may claim the other glove.
- Route `InputEventScreenDrag` and release strictly by `event.index`. Releasing
  one finger must never release, snap back, or punch the other glove.
- Mouse input uses one sentinel finger for editor and probe coverage.
- Clear all claims on `configure()`, completion, close, visibility loss, and
  tree exit so re-entry cannot create a phantom punch.
- Ownership is sticky until release. Crossing two fingers must not swap their
  gloves. An unknown or duplicate release is a no-op.
- Ignore emulated mouse events paired with real screen-touch input so one
  physical action cannot fire twice.
- Application focus loss calls `cancel_all_touches()` before any further input
  is accepted.

### Forward punch

- The painted glove home, target, demonstration, and hit-test geometry all come
  from the same local 1280×720-space calculations.
- A glove follows its finger from a lower home zone toward the active target.
  Forward reach is the projection of that drag along the home-to-target ray.
- Emit one accepted punch only when reach crosses the target plane while the
  target is hittable. Latch that extension until the glove retracts or releases;
  extra drag samples cannot pay duplicate progress.
- On release, return the glove with a short spring tween. No punch depends on
  drag speed or a narrow timing window.
- Interactive diameters are at least 110 px. At five seconds, replay the ghost
  gesture; at ten seconds, widen the target/corridor. Assistance never creates
  progress on its own.

### Signal meanings

- `boxing_guide`, `boxing_jab`, `boxing_guard`, `boxing_imp`, and `boxing_belt`
  with `amount > 0` are accepted work and may bank phase progress.
- The same kinds with `amount == 0` are friendly near-miss/blocked cues. The
  world replays the instruction and must not call `competition.note_miss()`.
- `boxing_pose` changes the visible imp pose but never changes progress.
- `boxing_contact` triggers bubble/recoil feedback only.
- `boxing_ready` requests the phase's existing recorded instruction after a
  wordless demonstration.

### Deterministic probe seam

Expose a small read-only/control seam on the specialist so trusted probes do
not infer state from pixels:

- `glove_rest_position(side: int) -> Vector2`
- `active_target_position() -> Vector2`
- `touch_owner_snapshot() -> Dictionary`
- `landed_count() -> int`
- `round_index() -> int`
- `is_demo_active() -> bool`
- `has_friendly_hit_feedback() -> bool`
- `cancel_all_touches() -> void`
- `receive_friendly_hit() -> void`

These methods expose deterministic geometry/counters or invoke the same
cosmetic contact path used in play. They must not bypass punch validation,
advance a phase, award a star, or write a save.

## 4. Phase behavior

### GLOVE GUIDE

Both gloves float in large lower-screen bays. The demonstration touches one,
pushes it toward a central mitt, releases, then repeats on the other side. The
child may use the same finger for both gloves and may complete them in either
order. Accepted glove state is banked; replay never erases the first glove.

### JAB PRACTICE

Use slow, deterministic left/right focus-mitt placements. A large gold halo
marks the current mitt. Any glove may score so a crossed hand or one-finger
player is never rejected. A miss produces bubbles and immediately re-highlights
the same mitt. Four accepted forward punches complete the phase.

### SOFT GUARD

The padded counter travels only after a long windup and visible guard bubble.
Holding or moving either glove into that bubble banks one guard. If the child
does nothing, the counter touches the shield, makes a soft puff, and resets the
same cue. It does not bank progress passively and does not remove progress.

### TITLE IMP

Use one deterministic opponent state machine, not the generic roaming-crew
combat layer:

`idle/taunt → windup → charge/contact → guard or recover/open → idle`

Only the bright `recover/open` window accepts a forward punch. A guarded punch
plays the guard pose and soft bounce, then reopens the same opportunity. A
successful punch plays `stagger` and banks exactly one unit. After six accepted
punches, play `bopped`, then `bow`; there is no opponent health UI or player
damage state.

### BELT

Stop opponent attacks and release any stale touch claims. Present the existing
belt with a large pulse. One real glove-to-belt extension completes the career;
a passive timer cannot claim it.

## 5. Career-world integration

- Preload and instantiate the boxer specialist where
  `OperaCareerWorld2D._build_world()` selects its gesture surface. Keep the
  shared field typed as `OperaGestureSurface`.
- Boxer has no wander stations. Its five phases open directly on the existing
  boxer world/stage painting.
- Give the boxer surface a full-stage transparent host and suppress the generic
  task-card frame. Keep touch geometry inside the fixed `StagePaths.SCREEN`
  transform so Godot inverse-transforms phone and tablet input correctly.
- Intercept boxer signals in `_on_gesture()` before the generic scorer, parallel
  to the specialist ballet route. Only accepted work changes career-owned
  progress.
- Do not call `_start_stage_combat()` for `boxing_imp`. Keep `combat_layer` on
  `MOUSE_FILTER_IGNORE` so it cannot intercept either glove finger.
- On phase change and `close()`, clear glove claims, stop surface timelines, and
  restore normal Opera actors for the curtain call.

## 6. Friendly-hit and no-loss rules

These are hard invariants, including during TITLE IMP:

- No health, lives, damage counter, loss screen, knockout, restart, timeout, or
  negative score.
- Never decrement `phase_progress`, accepted guide state, guard count, title
  hits, `opera_stars`, pearls, or competition points.
- Never reset an accepted combo/checkpoint because of a miss, blocked punch, or
  imp contact.
- Imp contact draws the existing bubble/fizzle effect, moves the gloves or
  tableau by at most a short cosmetic recoil, and returns control immediately.
- A miss may replay/widen guidance. It cannot auto-complete the objective.
- There is no simultaneous-touch gate. Holding both gloves may look lively but
  is never a completion requirement.

## 7. Existing approved runtime resources

All resources below already exist in the repository and are covered by the
project asset ledger. The rebuild does not require image generation, downloaded
content, or new audio.

### Backdrops

- `assets/opera/worlds/backdrops/world_boxer.png` (preview/reference only;
  never use this 1024x576 image as the playable full-screen background)
- `assets/opera/worlds/backdrops/world_boxer_c0r0.png`
- `assets/opera/worlds/backdrops/world_boxer_c0r1.png`
- `assets/opera/worlds/backdrops/world_boxer_c1r0.png`
- `assets/opera/worlds/backdrops/world_boxer_c1r1.png`
- `assets/opera/worlds/backdrops/stage_boxer_c0r0.png`
- `assets/opera/worlds/backdrops/stage_boxer_c0r1.png`
- `assets/opera/worlds/backdrops/stage_boxer_c1r0.png`
- `assets/opera/worlds/backdrops/stage_boxer_c1r1.png`

### Roshan and opponent art

- `assets/opera/worlds/actors/roshan_boxer.png`
- `assets/opera/worlds/actors/animation/roshan_boxer_sheet_a.png`
- `assets/opera/worlds/actors/rival_boxer.png`
- `assets/opera/worlds/actors/rival_boxer_windup.png`
- `assets/opera/worlds/actors/rival_boxer_charge.png`
- `assets/opera/worlds/actors/rival_boxer_slash.png`
- `assets/opera/worlds/actors/rival_boxer_recover.png`
- `assets/opera/worlds/actors/rival_boxer_guard.png`
- `assets/opera/worlds/actors/rival_boxer_stagger.png`
- `assets/opera/worlds/actors/rival_boxer_flee.png`
- `assets/opera/worlds/actors/rival_boxer_taunt.png`
- `assets/opera/worlds/actors/rival_boxer_hop_a.png`
- `assets/opera/worlds/actors/rival_boxer_hop_b.png`
- `assets/opera/worlds/actors/rival_boxer_bopped.png`
- `assets/opera/worlds/actors/rival_boxer_bow.png`

### Gloves, targets, props, and effects

- `assets/opera/worlds/widgets/widget_lanes_boxer.png`
- `assets/opera/worlds/widgets/widget_lanes_boxer_lit.png`
- `assets/opera/worlds/widgets/widget_push_boxer.png`
- `assets/opera/worlds/widgets/widget_push_boxer_mover.png`
- `assets/opera/worlds/widgets/widget_target_boxer.png`
- `assets/opera/worlds/widgets/widget_target_boxer_mark.png`
- `assets/opera/worlds/widgets/widget_target_boxer_mover.png`
- `assets/opera/worlds/widgets/widget_target_boxer_success.png`
- `assets/opera/worlds/widgets/widget_track_boxer.png`
- `assets/opera/worlds/widgets/widget_track_boxer_mover.png`
- `assets/opera/worlds/props/goal_boxer.png`
- `assets/opera/worlds/props/fx_bop_puff.png`
- `assets/opera/worlds/ui/crests/opera_crest_boxer.png`

The specialist may crop/draw regions from the approved widget textures at
runtime and may use Godot drawing primitives for halos, bubbles, glove paths,
and pointers. It must not create or commit extracted/repainted image variants
for this implementation.

### Existing boxer voices

- `assets/audio/voices/roshan_op_boxer_work.ogg`
- `assets/audio/voices/roshan_op_boxer_spar.ogg`
- `assets/audio/voices/roshan_op_boxer_jab.ogg`
- `assets/audio/voices/roshan_op_boxer_duck.ogg`
- `assets/audio/voices/roshan_op_boxer_bell_chase.ogg`
- `assets/audio/voices/roshan_op_boxer_round.ogg`
- `assets/audio/voices/roshan_op_boxer_belt.ogg`
- `assets/audio/voices/imp_op_boxer_arrive.ogg`
- `assets/audio/voices/imp_op_boxer_bop.ogg`
- `assets/audio/voices/imp_op_boxer_copy.ogg`
- `assets/audio/voices/imp_op_boxer_steal.ogg`

### Existing impact sounds

- `assets/audio/sfx/combat_bonk.wav`
- `assets/audio/sfx/combat_charge_ring.wav`
- `assets/audio/sfx/combat_fizzle.wav`
- `assets/audio/sfx/combat_freeze.wav`
- `assets/audio/sfx/combat_poof.wav`
- `assets/audio/sfx/combat_pop.wav`

These shipped WAV files may be reused as-is. This manifest does not authorize
editing, recompressing, or adding voice/audio files.

### Existing 3D boxer resources retained but not required by the 2D surface

- `assets/opera/jobs/boxer/opera_boxer_outfit.glb`
- `assets/opera/jobs/boxer/opera_boxer_dressing.glb`
- `assets/opera/rivals/opera_rival_boxer.glb`
- `assets/opera/rivals/opera_rival_boxer_match.png`

## 8. Save and reward integration

No new save key is allowed or needed.

1. Completing BELT advances the final career-world phase and invokes the
   existing world win callback exactly once.
2. `OperaAct` completes the existing performance/curtain-call flow.
3. `OperaHouse._act_won()` marks the existing Boxer act bit in
   `m.opera_stars` (`Boxer` is the existing zero-based act index 7, mask 128), awards the
   existing first-time/replay pearl amount, recomputes `m.opera_progress`, and
   calls the existing save writer.
4. Existing all-star handling may set `opera_done`; the boxing surface never
   writes it directly.

The persistent contract remains `opera_stars`, `opera_progress`, `opera_done`,
and the existing Opera reward fields. Glove positions, per-phase progress,
opponent pose, assists, contacts, and touch IDs are transient session state and
must not be added to `reef_save.json`.

## 9. Required regression coverage

- Both touch indices can hold and drag separate gloves concurrently.
- Releasing finger 0 does not move or release finger 1's glove.
- Crossing the two fingers preserves the original glove-owner mapping.
- Unknown and duplicate releases are no-ops; emulated mouse events after a
  touch do not duplicate the punch.
- One finger can complete all five phases sequentially.
- Mouse fallback can complete all phases in headless/editor probes.
- No input for an extended interval produces zero progress and no reward.
- A wrong target, guarded punch, and imp contact preserve all banked progress.
- `receive_friendly_hit()` preserves landed/round/phase counters, competition
  `player_progress`, score and mistakes, and all persistent save fields.
- A held extended glove emits at most one accepted punch.
- Touch claims are empty after phase change, close, and career re-entry.
- Focus loss clears all touch claims through `cancel_all_touches()`.
- Each objective starts/repeats an existing boxer voice event and visibly
  points at the actionable geometry.
- TITLE IMP uses one opponent and never enables the generic combat layer.
- BELT calls the win callback once; existing `opera_stars` behavior remains
  unchanged and no save key is added.
- Draw and hit-test geometry agree at 1280×720 and through the existing root
  scaling on tablet and tall-phone aspect ratios.

## 10. Explicit non-goals

- No overworld portal or separate main-game mode.
- No changes to `main.gd` ownership or the Opera lobby/door index.
- No generic roaming-crew `bop` phase, `HitEngine`, physics bodies, or health
  system.
- No new or regenerated art, voices, music, sound effects, or save schema.
- No requirement to use two fingers simultaneously and no reading-dependent
  instruction.
