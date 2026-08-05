# DRAFT - Codex Opera Animation Handoff (2026-08-03)

- **Status:** draft for owner review
- **Audience:** Codex runtime animation and visual-QA pass
- **Baseline:** `origin/dev` at
  `39997f72e4a23a6db889c870cd5c94320e130a75`
- **Target:** the thirteen Canvas-based Pearl Opera career worlds: twelve
  competitive careers plus Nursery Nurse

## 1. Outcome

Turn the accepted Pearl Opera paintings, actor poses, combat effects, and
diegetic widget layers into one responsive animation language that a
four-year-old can read on a phone.

This is primarily a **runtime integration and animation-quality pass**. It is
not a new art-generation campaign. The required static art is already present.
Reuse it, bind it to real game state, and make the motion feel intentional.

The pass is complete when:

- every imp-brain pose selects the correct authored sprite without costume
  swaps, first-use stalls, foot sliding, or transform overstatement;
- all sixty art-backed task widgets move because of the child's gesture or a
  clearly marked demonstration, never because of passive progress;
- Roshan, the career rival, Faron, props, and audience reactions have stable
  rest transforms and cannot drift after repeated or overlapping actions;
- the final-stage performance reads as a show, while remaining immediately
  responsive to one-finger input;
- the exact Godot 4.7.1 Mobile-renderer captures and the trusted probes pass.

## 2. Binding boundaries

These rules are not optional.

1. **Gameplay animation is not cinematic delivery.** Whole-sprite transforms,
   state swaps, runtime widget layers, particles, and tweens are allowed inside
   the live Opera game. If work touches an authored cinematic, the repository's
   full-frame image-regeneration rule applies instead; that work is outside this
   handoff.
2. Do not modify, recompress, replace, or derive new versions of anything in
   `assets/book/`, `assets/audio/voices/`, or
   `assets/characters/friends/`.
3. Do not regenerate Mermaid Roshan. Her accepted career cutouts are identity
   art. Animate them non-destructively as whole sprites.
4. Do not redesign the accepted career worlds, stages, actors, effects, task
   frame, station marker, magnifier, or widget art.
5. Do not generate new art unless a runtime capture proves that no accepted
   reusable asset can serve the beat. Record that precise gap before any
   generation and limit the request to it.
6. Preserve the no-fail contract. An animation may clarify, celebrate, or offer
   another try; it may not remove progress, create damage, lock the child out,
   or become a reading-dependent gate.
7. Preserve one-finger control. Animation never owns input authority and never
   requires a second finger, precision timing without mercy, or a drag that
   starts on a moving target.
8. Use the Mobile renderer everywhere. No new OmniLights, Forward+-only
   effects, runtime texture generation, or unbounded transparent layers.

## 3. Accepted baseline - do not request it again

The 2026-08-02 request documents describe how the art was made. Their pending
lists are no longer an accurate delivery census.

| Area | Current accepted/runtime baseline |
|---|---|
| Career environments | 27 native 2048x2048 world/stage masters and 104 runtime 1024x1024 tiles |
| Career widgets | 60/60 required backdrops; 154 runtime widget files; 45 transparent mover/shared layers |
| Interaction kit | Storybook task frame, station marker, and magnifier present and audited |
| Rival crews | 12 costume families, each with idle plus `windup`, `charge`, `slash`, `recover`, `guard`, `stagger`, `flee`, `taunt`, `hop_a`, `hop_b`, `bopped`, and `bow` |
| Base imps | `imp_mischief` and `imp_captain` each have idle plus dedicated combat, taunt, bopped, and bow art |
| Combat effects | Telegraph ring and bang, slash arc, dust puff, stolen sparkle, dizzy stars, and bop puff are present |
| Career performers | Thirteen Roshan career cutouts and `faron_nursery.png` are present |
| Existing audit | Automated Opera art QA passes; owner runtime visual review remains pending |

The original pose descriptions and silhouette intent in
`CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md` remain binding. That document is a
pose-direction reference now, not a request to regenerate the delivered files.

Source precedence for this pass is:

1. `AGENTS.md` and the protected-asset/security rules;
2. the current runtime and trusted probes on `origin/dev`;
3. this handoff;
4. older Opera request documents, only where they do not describe already
   completed work as pending.

## 4. Runtime touchpoints

Keep the change surface narrow.

| File | Responsibility in this pass |
|---|---|
| `scripts/opera_career_world_2d.gd` | Career performers, imp state selection, combat pose envelopes, effects, stage transitions, audience reactions |
| `scripts/opera_gesture_surface.gd` | Widget-layer motion driven by gesture state and demonstrations |
| `scripts/opera_nursery_catch.gd` | Nursery catch motion and safe pillow landing |
| `scripts/opera_imp_clips.gd` | Shared naming and bopped clip; its older transform-only comments are not the current art contract |
| `scripts/imp_ai.gd` | Authoritative combat state and timing; do not rewrite the brain for visual convenience |
| `scripts/opera_world_backdrop_2d.gd` | Existing bounded spotlight/footlight ambience only; accepted paintings remain static plates |
| `scripts/probe_imp_animation_art.gd` | Authored-state and combat-FX capture gate |
| `scripts/probe_opera_2d.gd` | Thirteen-world runtime, identity, widget, and finale contract |
| `scripts/probe_opera_nursery.gd` | Nursery-specific interaction contract |

Do not move this work into `scripts/main.gd`. Opera state stays with the
existing Opera owners. If a helper is extracted, it receives the owning Opera
node by reference and must not introduce a second source of truth.

## 5. Work package A - authored imp and rival motion

### A1. Make sprite resolution explicit

`OperaCareerWorld2D._imp_texture()` already resolves the correct family and
fallback order. Preserve that identity lock, but make the animation path know
whether it received:

- the exact requested authored state;
- an authored cousin such as `hop_a`, `hop_b`, or `bow`; or
- the family idle fallback.

Return or retain enough resolution metadata to choose the correct transform
envelope. Do not infer identity by crossing to another family. A missing chef
state may fall back only within `rival_chef`; it must never show a base imp or a
different career costume.

Warm the active family's state textures at career-world setup. The first
wind-up or slash must not be the moment a phone performs a disk load. Keep the
existing cache bounded to the active family plus the two base families and
shared effects.

### A2. Stop double-posing delivered art

The present procedural squash, tilt, lift, and tint were designed to keep a
single idle cutout readable before authored state art landed. The authored
poses now carry most of that silhouette change themselves.

- If the exact authored pose resolves, apply only the motion needed to sell the
  beat: a small anticipation pulse, follow-through, recoil, or breathing loop.
- If a cousin or idle fallback resolves, retain the stronger procedural
  envelope so the missing pose remains readable.
- Keep the authored sprite's bottom-center registration fixed while scale and
  rotation change. Measure the visible sole position, not only the Control
  rectangle.
- Do not opacity-crossfade two actor sprites. It muddies the silhouette, doubles
  transparent overdraw, and can read as two characters. Swap at the state
  boundary and let the transform envelope bridge the beat.
- Do not globally tint accepted costume art except for a short, bounded hit or
  telegraph pulse. Restore `Color.WHITE` deterministically on exit.

The dedicated pose remains the acting. Runtime motion supports it; runtime
motion must not redraw it.

### A3. Preserve the combat timeline

The imp brain is authoritative. The animation layer must expose, not alter,
these beats:

| Pose | Current readable interval | Required animation read |
|---|---:|---|
| `windup` | 0.55-1.35 s | Long, interruptible anticipation; telegraph ring and bang remain visible |
| `charge` | about 0.40 s | Committed travel toward the stored aim point; no re-homing |
| `slash` | about 0.28 s | One clear swing and follow-through |
| `recover` | 1.15-1.60 s | Harmless, inviting counter window |
| `guard` | about 0.80 s | Captain block with a short recoil, never a punishment state |
| `stagger` | about 0.50 s | Playful surprise; no dizzy eyes unless bopped |
| `flee` | about 1.10 s | Cheeky retreat with the carried sparkle readable |
| `taunt` / `rally` | 0.85-1.00 s | Pantomime challenge; never menacing |
| `bopped` | about 0.62 s | One shoo-off squash, spin, dizzy-star beat, and fade |

No charge may begin without the wind-up visual. No recover may be visually
shortened because the child needs that generous response window. No animation
event may award phase progress; only the existing input/gameplay path does.

### A4. Effects

Use the shipped raster effect first and retain the procedural draw only as its
fallback. Anchor effects to the character's stage-space feet or center, not a
hard-coded screen location.

- Telegraph ring stays beneath the actor; bang stays above the head.
- Slash arc faces the committed travel direction.
- Dust begins at the feet and does not obscure the tappable body.
- Dizzy stars follow the bopped actor until the fade ends.
- Stolen sparkle remains visible during flee and is restored by the existing
  bop reward path.

Effects never intercept touch and never become collision or scoring objects.

## 6. Work package B - Roshan, partner, rival, and finale acting

### B1. Stable rest transforms

The current helpers create local tweens for glides, bounces, prop movement,
audience hops, and the rival bow. Repeated gestures can start new tweens before
old ones finish. Introduce explicit per-actor animation ownership:

- store the true rest position, scale, rotation, flip, texture, and modulate;
- cancel or replace the actor's previous motion before starting a new one;
- animate from the sampled current transform toward the stored rest transform;
- restore the complete rest transform on phase change, retry, teardown, and
  early exit;
- never treat the already-offset value from an interrupted tween as the next
  rest position.

Twenty rapid taps must end at exactly the same rest transform as one tap.

### B2. Mermaid Roshan

Animate Roshan only with her accepted career cutout:

- a shallow vertical arc and slight directional lean during stage-route glide;
- a small success bounce tied to accepted progress;
- a softer "try again" acknowledgment that does not look like damage;
- a larger, bounded curtain-call lift after the result is decided.

No skeletal deformation, cutout limb separation, image regeneration, costume
redesign, or texture substitution is authorized.

### B3. Career rival and Nursery partner

The competitive rival is the same costume family already used by the scuffle
crew. Reuse its delivered state art on the final stage:

- `taunt` for a rival step or playful lead change;
- `bow` for the curtain call;
- idle for neutral waiting;
- a subtle whole-sprite hop only when no more specific state is appropriate.

Restore the rival's idle texture and registered feet after every temporary
state. Do not use combat `bopped`, `slash`, or `flee` art in the job contest.

Faron has no rival pose family. Keep `faron_nursery.png` and use only gentle
whole-sprite bounces, nod-like rotation, and bedside glides. A missed nursery
catch remains a safe pillow landing and a kind prompt, never a failure act.

### B4. Props, audience, and transition skips

- Goal-prop theft, recovery, and celebration must preserve the prop's aspect
  ratio and return it to one canonical home transform.
- Audience reaction stays bounded to the existing small portrait set. Do not
  duplicate protected friend portraits or create new variants.
- Confetti and sparkle counts remain bounded and self-freeing.
- Any touch may continue to skip the between-phase sparkle sting. Skipping an
  animation must produce the same gameplay state as letting it finish.

## 7. Work package C - sixty diegetic widget animations

All required art exists in `assets/opera/worlds/widgets/`. Bind and polish it;
do not reopen the art request by default.

| Template | Count | Motion authority |
|---|---:|---|
| T1 `gauge` | 3 | `timing_position` rotates the shared needle; accepted tap flashes success |
| T2 `track` | 8 | `timing_position` translates the career mover through the baked green zone |
| T3 `pour` | 4 | `held` shows vessel/stream; `widget_fill` reveals the registered fill state |
| T4 `basin` | 2 | `held` and fill reveal bubbles; completion shows the shared shine |
| T5 `charge` | 5 | hold progress scales the glow and reveals the full-charge overlay |
| T6 `crank` | 9 | actual finger angle rotates the centered mover; fill reveals progress |
| T7 `trace` | 6 | accepted swipe distance reveals the registered lit path monotonically |
| T8 `push` | 4 | `swipe_dir` and accepted fill move the subject along the intended axis |
| T9 `target` | 8 | `tap_point` owns the mover; accepted taps leave registered marks |
| T10 `lanes` | 10 | demo/choice flash reveals only the target cell; picks show shared feedback |
| T11 `catch` | 1 | live baby fall, cradle x, catch, and safe pillow landing own all movement |

### C1. Causality

- Motion follows input continuously where the mode is continuous. Releasing a
  hold stops the pour/charge motion immediately.
- Demonstration motion is visually distinct and stops as soon as the child
  touches the surface.
- A demonstration never changes `phase_progress`, score, choice history, catch
  count, or save data.
- Wrong input may re-show the affordance, but it never removes progress.
- Completion overlays begin only after the gameplay owner accepts completion.
- Decorative looping motion remains subtle enough that the interactive mover
  is always the strongest local motion cue.

### C2. Registration and color locks

- Backdrops remain 1024x608 and registered overlays remain pixel-aligned.
- POT mover pivots stay at their declared center or bottom-center registration.
- Do not stretch a mover to repair bad registration. Fix runtime placement or
  record an art gap.
- The success green is reserved for the baked go-zones in T1 and T2. Animation
  must not pulse that green elsewhere.
- Keep widget centers uncluttered enough for the existing white demonstration
  finger and child-readable target cue.

### C3. Motion limits

- No animation may move the real hit target after pointer-down.
- No essential cue may flash for less than 250 ms.
- No completion hold may block the next touch for more than 350 ms.
- Avoid continuous full-surface alpha pulses. Animate the smallest meaningful
  layer.
- Reuse loaded textures; no `load()` calls, image decoding, or large temporary
  allocations inside `_process()` or `_draw()`.

## 8. Work package D - world and stage ambience

The accepted world and stage paintings are static plates. Do not pan, warp,
parallax, cross-dissolve, or independently animate painted subjects inside
them.

The current bounded spotlight and footlight overlays may continue to breathe.
Keep their redraw cadence at or below the existing 12.5 Hz unless a measured
Mobile capture proves a higher rate is needed and affordable. Do not add new
full-screen transparent washes.

Career-specific activity belongs in the widget, actor, prop, or a separately
accepted foreground card. It must not be faked by moving the entire background.

## 9. Implementation order

Deliver in this order so each checkpoint is reviewable and reversible.

1. Capture the current baseline for the fourteen imp/rival families and shared
   effects through `probe_imp_animation_art.gd`.
2. Add authored-versus-fallback resolution metadata and bounded texture
   prewarming without changing timing or scoring.
3. Calibrate authored-pose envelopes and foot locking, one base family first,
   then one costume family, then the remaining families.
4. Add stable actor tween ownership and bind rival `taunt`/`bow` finale states.
5. Audit all eleven widget templates, then all sixty career-template pairs,
   fixing runtime bindings rather than repainting accepted art.
6. Polish prop, audience, and bounded ambience only after interaction motion is
   approved.
7. Run the complete gates, capture every family and career at gameplay scale,
   and prepare the owner review contact sheets.

Do not mix art regeneration, a combat-brain rewrite, or unrelated Opera story
changes into these commits.

## 10. Acceptance gates

### Functional

- All thirteen career worlds enter, play, reach their finale, finish, and tear
  down through the shipping 2D path.
- Every authored imp state resolves through the live loader.
- No competitive crew frame displays `imp_mischief` or `imp_captain` art.
- A charge cannot visually skip wind-up; a bopped actor cannot keep an active
  hit target; a skipped transition cannot double-award progress.
- Widget demonstrations produce zero passive progress.
- Nursery misses remain safe and do not reduce progress.
- Save keys and completion semantics are unchanged.

### Visual

- Feet remain locked within 3 runtime pixels during grounded state swaps at
  gameplay scale.
- No actor, prop, audience member, or widget mover accumulates transform drift
  after twenty repeated triggers.
- No state change creates a one-frame scale pop, costume pop, wrong-facing prop,
  or un-restored tint.
- Each combat state reads in silhouette at the shipped phone scale.
- All sixty widget movers align with the painted receiver/path/zone in Mobile
  captures.
- The child-controlled mover is more visually prominent than ambient motion.

### Performance

- Speedy tier sustains the project's 30 fps target on the Lenovo Tab M11 class
  device.
- No new lights, physics bodies, per-frame texture loads, or unbounded nodes.
- Animated transparency remains bounded; effects free themselves after their
  declared lifetime.
- Repeated entry/exit leaves no Opera nodes, tweens, or cached world textures
  alive outside their owner.

### Child-readability

- The next useful touch is shown by motion plus the existing voice/visual cue,
  not text alone.
- Telegraph, target, and success cues remain large and visible under a finger.
- Rapid tapping cannot corrupt state, push an actor off register, or lose
  progress.
- Waiting for the green timing zone remains more rewarding than mashing, while
  mercy behavior still lets the child continue.

## 11. Verification

Use exactly Godot 4.7.1-stable and the Mobile renderer.

For every changed GDScript file:

```sh
python -m gdtoolkit.parser <changed .gd files>
python tools/lint_inference.py <changed .gd files>
```

Minimum focused probes:

```sh
$GODOT --headless -s scripts/probe_imp_animation_art.gd
$GODOT --headless -s scripts/probe_imp_ai.gd
$GODOT --headless -s scripts/probe_opera_2d.gd
$GODOT --headless -s scripts/probe_opera_nursery.gd
$GODOT --headless -s scripts/probe_passive.gd
```

Full blocking gate before integration:

```sh
GODOT=$GODOT scripts/ci.sh
```

For owner review, capture:

- all fourteen families across every delivered state using
  `IMP_ANIM_CAPTURE_FAMILY`, `IMP_ANIM_CAPTURE_STATES`, and an ignored
  `IMP_ANIM_SHOT_OUT` directory;
- one complete scuffle and one captain scuffle from at least chef, detective,
  ballerina, candymaker, and nursery;
- the final-stage rival reaction and curtain call for all twelve competitive
  careers;
- every one of the sixty widget phases at idle/demo, active input, near
  completion, and accepted completion;
- a rapid-input stress pass and repeated early-exit/re-entry pass;
- a real Android Speedy-tier frame-time capture.

Contact sheets are review evidence, not replacement runtime assets.

## 12. Delivery record

The implementation handoff must report:

```text
baseline commit:
implementation commit(s):
changed runtime files:
new assets: none / listed gap authorization
families captured:
career widgets captured:
focused probe results:
full scripts/ci.sh result:
Android device and Speedy-tier frame result:
owner identity/topology/style review:
known fallbacks still exercised:
```

Do not describe the pass as complete while owner runtime review is pending.

## 13. Explicitly out of scope

- New Roshan poses or regenerated Roshan career art.
- Editing family voice recordings or adding substitute voice lines.
- Lamba's legacy 3D actor or new Lamba voice recording.
- New 3D rigs, skeletal clips, or converting Opera back to a 3D world.
- Cinematic production or frame interpolation of any kind.
- Repainting accepted career backgrounds, stages, widget backdrops, or props.
- Combat balance, damage, fail states, score economy, or save-schema redesign.
- Changes to `main.gd`, protected project instructions, CI workflows, or the
  release process unless separately requested.

## 14. Codex implementation record - 2026-08-03

This implementation may be integrated to `dev` for owner runtime review but
is **not marked complete for art acceptance**. The exact-engine Opera gates,
review captures, and final repository-wide gate are green. The owner authorized
`dev` integration on 2026-08-03; identity/topology/style review and a real
Android Speedy-tier capture remain pending.

```text
baseline commit: 39997f72e4a23a6db889c870cd5c94320e130a75
implementation commit(s): d0a35d3e0085a1bb1ccd3319196ff6788818e076
repository integration: owner-authorized; final dev commit is reported in the task delivery
changed runtime files:
  scripts/opera_career_world_2d.gd
  scripts/opera_gesture_surface.gd
  scripts/opera_imp_clips.gd
changed probes:
  scripts/probe_imp_animation_art.gd
  scripts/probe_opera_2d.gd
  scripts/probe_opera_nursery.gd
new assets: none
families captured: 14/14; 56 live full-viewport frames; 14 family sheets plus one master
career widgets captured: 60/60 at four states; 240 cropped live frames; 60 sheets plus one master
finale rivals captured: 12/12 at taunt and bow; 24 live frames; 12 sheets plus one master
selected scuffles captured: opening and captain sequences for chef, detective,
  ballerina, candymaker, and nursery; 77 live frames; 10 sheets plus one master
rapid-input/lifecycle captured: one twenty-tap rest frame plus five early
  exit/re-entry frames; every cycle freed the Opera world and restored touch
focused probe results:
  probe_imp_animation_art.gd: ALL OK
  probe_imp_ai.gd: ALL OK
  probe_opera.gd: ALL OK
  probe_opera_2d.gd: ALL OK
  probe_opera_nursery.gd: ALL OK
  probe_passive.gd: ALL OK
full scripts/ci.sh result:
  final UTF-8-mode run on the complete diff exited 0 after import and every
  trusted probe. probe_throne walked three taps to x=233.62 and printed ALL OK.
  Two earlier runs had exposed its intermittent two-tap left-edge interception;
  those historical logs are retained with the green final log.
Android device and Speedy-tier frame result:
  pending - `adb devices -l` reported no attached device
owner identity/topology/style review:
  pending - portable review masters, hashes, and usage instructions are under
  FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/; the raw capture tree remains
  build-only under .godot/opera_animation_review_20260803/
known fallbacks still exercised:
  neutral prowl uses same-family idle; rally uses same-family taunt;
  base families have no delivered hop_a/hop_b and do not cross families
```

Portable review kit:

- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/README.md`

Tracked review masters:

- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_imp_family_master_contact.png`
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_60_widget_master_contact.png`
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_12_rival_master_contact.png`
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_selected_scuffles_master_contact.png`
- `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/review_masters/opera_stress_master_contact.png`

Build-only full-gate logs:

- `.godot/opera_animation_review_20260803/ci_utf8.log`
- `.godot/opera_animation_review_20260803/ci_retry2.log`
- `.godot/opera_animation_review_20260803/ci_final.log`
