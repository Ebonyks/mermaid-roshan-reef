# Ballerina Party Rebuild — Design and Implementation Record

Date: 2026-08-09  
Status: implementation complete on the task branch; targeted local gates green;
full CI and target-device play-test still pending.

## Decision

Rebuild Ballerina as a three-act, full-stage mermaid ballet party rather than
reskinning the shared Opera widgets. Do not generate or modify art for this
rebuild. The repository already contains a more open underwater finale stage,
an accepted Roshan atlas, a shell music-box prop, and exact recorded prompts.
Those assets are sufficient when the interaction is designed around them.

The intended acts are:

1. **Pearl Mirror** — watch Roshan hold a clear port-de-bras pose, then tap the
   matching large pearl portrait. The first round has two choices; later rounds
   have three. Three accepted poses complete the act.
2. **Ribbon Trail** — guide a pearl along one luminous S-shaped current. The
   same curve function must paint the ribbon, animate the demonstration, and
   perform hit testing.
3. **Grand Twirl** — drag a pearl once around the shell music box. Either initial
   direction is valid; after the child chooses a direction, progress continues
   consistently in that direction and ends in a deliberate curtain-call pose.

This is a recital, not a race or combat encounter. All three acts stay on the
same stage. Ballerina does not need station wandering, a rival score meter, an
imp fight, or an opaque task card between Roshan and the dance floor.

## Audited root causes

- The shared interaction was presented inside a generic **392×232** card. On a
  1280×720 playfield it was too small for a non-reader using one finger and
  visually disconnected from Roshan and the stage.
- The Ballerina lane painting contained **three** authored shell pads, while the
  gesture code created **four** hit targets and used a four-step sequence. A
  child could not reliably infer which painted object corresponded to the
  invisible fourth rule.
- The ribbon widget painted a dark **zigzag**, but collision accepted a
  mathematical **sine curve**. Following the visible ribbon could therefore be
  judged wrong. This was a presentation/geometry defect, not player failure.
- The pose phase was a generic hold: touching and holding almost anywhere could
  satisfy it. It did not ask the child to recognize or reproduce a ballet idea.
- The twirl was the generic crank/circle interaction with themed decoration. It
  did not connect the finger, Roshan's pose, the ribbon, or the music box into a
  single readable action.
- Roshan's 4×4 atlas contains four useful pose keys per row, not four temporal
  in-betweens. Looping each row at 4–8 fps produced audited adjacent-pose
  silhouette jumps of **41.6–47.3%**, abrupt arm reversals, scale/position
  popping, and a cheer loop that snapped from raised arms back into a bow.
  The atlas must be used as held poses, with only an intentional non-looping
  curtain call.

## Asset reuse and no-new-art boundary

The rebuild reuses these already licensed runtime assets without editing their
pixels or protected sources:

- Underwater finale stage: `assets/opera/worlds/stage/finale_stage_c0r0.png`,
  `finale_stage_c1r0.png`, `finale_stage_c0r1.png`, and
  `finale_stage_c1r1.png`. Ballerina `kind == "stage"` routing selects this set;
  other careers and world backdrops retain their existing paths.
- Roshan pose atlas:
  `assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png`.
- Shell music box: `assets/opera/worlds/props/goal_ballerina.png`.
- Existing protected voice lines, used in place:
  `roshan_op_ballerina_watch.ogg`, `roshan_op_ballerina_steps.ogg`,
  `roshan_op_ballerina_ribbon.ogg`, and `roshan_op_ballerina_twirl.ogg`.
- Existing Opera music and project chime/tap feedback remain available; this
  rebuild does not commission, synthesize, or re-encode a new music track.

No asset-generation run, derivative image, import change, or license-ledger
change is part of this implementation.

## Help, replay, and progress rules

- Each act begins with a short visual demonstration and its exact spoken cue.
  Pearl Mirror changes from the `watch` cue to the `steps` cue when control is
  handed to the child.
- After **5 seconds** without meaningful progress, replay only the unresolved
  pose, remaining ribbon segment, or remaining orbit. After **10 seconds**,
  replay again and enlarge the relevant target/corridor. This satisfies the
  requested 5–10 second recovery window without creating a timeout.
- Correct work is monotonic and banked. Replays, pauses, release/re-grab,
  incorrect touches, or a stronger assist may never reduce pose round,
  ribbon progress, twirl progress, career progress, or saved completion.
- A wrong touch produces brief gentle feedback and another demonstration. It
  does not reset the act, remove a correct answer, play a punitive sound, or
  create a fail screen.
- Zero input must never complete an act. Demonstrations and assists teach; only
  accepted child input advances progress.

## Acceptance criteria

### Child clarity and accessibility

- The game is completable with one finger and no reading. No multi-touch,
  precision timing, drag-and-hold duration, or knowledge of ballet terms is
  required.
- The Ballerina surface occupies the open right side of the stage, approximately
  **854×660**, while Roshan remains visible on the left. No opaque generic card
  covers the performance.
- Pose options are **180–220 px square**. The ribbon resume pearl is at least
  **128 px** across, the base ribbon corridor is **116 px** wide, the twirl
  handle is **112 px** across, and the twirl ring corridor is **116 px** wide.
  Strong assist increases rather than decreases these tolerances.
- Every actionable object pulses or demonstrates before input is expected. The
  visible object, demonstrated object, and accepted hit geometry are identical.
- All prompts have an exact Ballerina VO. Text may support an adult but cannot
  be required to discover the goal.

### Ballet and animation readability

- Pearl Mirror reads as watch-and-match; Ribbon Trail reads as guiding a pearl;
  Grand Twirl reads as circling the shell music box. None may display generic
  arrows, meters, crank art, or unrelated four-lane controls.
- Roshan uses recognizable low/heart, open/second, and crown/fifth arm shapes.
  A pose stays still until a demonstration cue or accepted progress band asks
  for another pose. Idle, travel, and work do not loop all four atlas cells.
- The curtain call runs once from bow to celebration and holds its final frame;
  it must not wrap back to the first frame.
- Roshan remains a mermaid throughout: one continuous tail, no implied human
  feet or leg-dependent instruction. Ribbon current, pearl mirrors, shells, and
  the underwater proscenium carry the Mermaid Roshan identity.

### Functional and regression behavior

- The three acts run in order and each completes exactly once. Completing the
  third act returns through the existing career win callback and save flow.
- Wrong or interrupted gestures preserve accepted progress. Starting away from
  the resume pearl/ring cannot advance progress. Large teleports, reversals, or
  motion outside the corridor cannot award hidden progress.
- Clockwise and counter-clockwise starts are both accepted for Grand Twirl;
  jitter or direction reversal does not subtract progress.
- No-input automation remains negative, and all non-Ballerina careers retain
  their existing phase definitions, widget routing, backdrop paths, and actor
  playback.

### Mobile performance

- Validate with exactly Godot 4.7.1-stable, the Mobile renderer, the 1280×720
  expanded canvas, and the Speedy profile. The Lenovo Tab M11 target must hold
  **30 fps** through all three acts.
- Reuse the four existing 1024×1024 stage tiles. Add no OmniLight, physics body,
  particle fleet, full-screen shader, or new high-overdraw transparent layer.
- Gesture rendering should remain code-native and redraw at no more than the
  existing 0.05-second cadence when active. Input sampling must be bounded and
  must not allocate an unbounded point history during a drag.

## Technical routing and test gates

- `scripts/opera_career_world_2d.gd` owns the three phase definitions, stage
  layout, VO handoff, assist replay, monotonic career progress, and win callback.
- `scripts/opera_ballet_surface.gd` owns Pearl Mirror, Ribbon Trail, and Grand
  Twirl presentation plus their authoritative gesture geometry. It does not own
  save or career state.
- `scripts/opera_roshan_actor.gd` selects held Ballerina atlas cells and the
  one-shot curtain call; other careers keep their existing animation behavior.
- `scripts/opera_world_backdrop_2d.gd` routes only the Ballerina stage tile set
  to the reusable underwater finale-stage tiles.

Before calling the rebuild complete:

1. Run `python -m gdtoolkit.parser` and `python tools/lint_inference.py` on every
   changed GDScript file.
2. Update the Ballerina expectations in `scripts/probe_opera_2d.gd`; its older
   assertions refer to the retired `dance_sequence`/PHRASE/POSE flow and must
   not be treated as evidence for the new design.
3. Extend `scripts/probe_opera_gesture_quality.gd` or add an equally focused
   trusted probe for exact paint/hit geometry, 5/10-second assistance,
   monotonic replay, both twirl directions, held actor poses, and one-shot cheer.
4. Run Godot import, `scripts/probe_passive.gd`, `scripts/probe_audit.gd`, the
   updated Opera probes, and finally `scripts/ci.sh`. Any `FAIL` line blocks
   integration.
5. Play-test on the target Android device for one-finger reach, VO clarity,
   visual contrast, stable 30 fps, and comprehension without adult explanation.

### Local validation snapshot

Using exactly Godot `4.7.1.stable.official.a13da4feb` on 2026-08-09:

- `gdtoolkit.parser` and the project inference lint pass for every changed
  GDScript file.
- `probe_opera_gesture_quality.gd` reports `ALL OK (235 checks)`, including
  zero passive payout, 5/10-second assists, wrong-pose replay, monotonic coarse
  ribbon tracing with lift/resume, straight-chord rejection, centre-scrub
  rejection, and both twirl directions.
- `probe_opera_2d.gd` reports `ALL OK`, including the exact three-phase route,
  underwater stage from phase one, large specialist surface, hidden race UI,
  stable atlas poses, one-shot cheer, full act completion, and reward flow.

The full trusted suite, CI result, and Lenovo Tab M11 play-test are recorded
separately when they complete; this document does not pre-certify them.

## Optional future art gap — not part of this rebuild

Only revisit background generation if a target-device play-test shows that the
reused underwater finale stage materially obstructs the large touch paths or
cannot provide sufficient contrast after code/UI adjustment. The narrowly
scoped fallback would be one complete, character-free, open underwater ballet
stage master with at least 2048×2048 native coverage, then four non-overlapping
1024×1024 runtime tiles. It must be generated as one continuous full frame,
preserve the current stage and source masters, and receive prompt/hash/review
provenance plus `ASSET_LICENSES.md` entries. It is not authorized or required by
the present implementation plan.
