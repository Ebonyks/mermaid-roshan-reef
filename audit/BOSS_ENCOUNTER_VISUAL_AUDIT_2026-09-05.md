# Boss encounter visual audit — 2026-09-05

## Record and authority

| Field | Value |
|---|---|
| Scope | Grand Puff introduction/tutorial, live battle hierarchy and cues, reusable encounter presentation, and a bounded static review of the legacy `CombatTutorial` presentation |
| Audit cycle | `VERIFYING` for Grand Puff and the bounded tutorial presentation repair |
| Document authority | `SUPPORTING_CURRENT`; this record cannot change canonical `MA-*` lifecycle states |
| Source base | Preceding intermediate baseline `1ecdf733`; the combined candidate is bound by the tracked source-hash manifest accompanying this record |
| Engine baseline | Exact Godot 4.7.2-stable local static/art/import gates and all 78 trusted probes pass with one isolated startup retry documented below. Remote exact-head CI and APK evidence remain pending. |
| Primary standards | `DL-AGE-01`–`DL-AGE-07`, `DL-MED-01`–`DL-MED-04`, `DL-READ-01`–`DL-READ-06`, `DL-UI-01`–`DL-UI-07`, `DL-MOT-03`–`DL-MOT-05`, `DL-SND-01`–`DL-SND-04`, and `DL-PERF-04` |
| Related canonical findings | `MA-2D-002`, `MA-VIS-006`, `MA-PLAY-001`, `MA-TOUCH-001`, `MA-CHILD-001` |
| Art action | Reuse only. No art generation, protected-asset modification, recompression, or cinematic work. |

This is a scoped evidence record under the master audit's section 2 lifecycle
and evidence taxonomy and section 3 authority order. It distinguishes source
facts from visual judgments and external acceptance. It does not claim the
game-wide audit is satisfied, that either encounter is fully converted to 2D,
or that implementation alone establishes visual acceptance.

## Inventory and evidence

### Current source and approved reuse

- `assets/flats/castle/boss/dusty_attic_arena_2048.png` is the restored August
  30 project-original 2048×2048 POT runtime background. Its SHA-256 is
  `A6F4BB59DF43E63CEDBF9A164526475B91985C85C73CAC7E061F830D60EF4122`.
  The preserved native and provenance are under
  `assets_src/imagegen/dust_bunny_boss_arena_2026-08-30/`.
- Grand Puff's accepted existing animation sheets remain under
  `assets/sprites/dust_bunnies/boss/`; the rebuild retains the flashing-head
  weakness and does not alter those images.
- The project-original downward tutorial hand is reused from
  `assets/castle/training/ghost_hand.png`, SHA-256
  `e484d14899d8137448128314536132dbd16f970cb1f0fabea006e9d51b5435b9`.
- Existing candidate captures under `tmp/bunny-rebuild/shots-attic/` informed
  the repair. They predate some current source changes, are ignored diagnostic
  artifacts, and are not V4 closure evidence for the repaired presentation.
- The tracked local packet `audit/boss_encounter_2026-09-05/manifest.json`
  binds LF-normalized SHA-256 hashes for 17 runtime/probe sources and SHA-256,
  dimensions and direct-copy provenance for 13 unmodified PNGs: four selected
  Dust states at each of 1280×720 and 1560×720 plus five 1280×720 tutorial
  states. Every declared source and capture hash was independently rechecked.
  Exact-4.7.2 Mobile logs `floor-final1280.log`, `floor-final1560.log` and
  `tutorial-root3.log` finish `DONE`/`ALL OK`; all three error logs are empty.
  The packet is source-bound local agent-review evidence. Its durable remote
  commit, physical device, child and owner acceptance remain pending.
- Historical CombatTutorial evidence is
  `audit/combat_tutorial_2026-08-01/combat_tutorial_art_review.png`, 2560×1369,
  SHA-256 `879b84f98119e1f933a8eddafa2bd5e454a87204419c7034be3de8accb2454403`.
  Its README classifies it as one historical phone-profile capture rather than
  current-head, Lenovo, child, owner, or reachability acceptance.
- Five current windowed Mobile tutorial captures under
  `tmp/bunny-rebuild/tutorial-root3-shots/`, with `tutorial-root3.log` reporting
  `ALL OK` and an empty error log, show the normal framed DustBunnySprite,
  Roshan and targets on the painted floor, the unrelated JUMP medallion hidden,
  and the shared TAP/HOLD guide adjacent to the live target, including the hand
  above the partner portrait. Their unmodified copies are bound in the packet.

### Evidence levels actually reached

| Evidence | Level | Result |
|---|---|---|
| Current script, asset, path, dimension, hash, and dependency inspection | `V1 STATIC` | Confirmed for the facts recorded here |
| Focused negative controls and gameplay probes | `V2 UNIT` | Shared contract, geometry, passive/spam/held controls, save/re-entry and reward idempotence pass |
| Exact Godot 4.7.2 trusted probes | `V3 RUNTIME`, complete local roster | All 78 have passing results; the aggregate roster had one pre-verdict castle-art startup exit, whose isolated retry exited 0 with `done failures=0`. See design validation record and `tmp/bunny-rebuild/final-probe-roster.log` / `pearl-final-retry.log`; remote exact-head CI remains pending |
| Fresh Mobile-renderer supported-aspect captures | `V4 CAPTURE`, source-bound local agent review | Tracked 13-PNG packet binds selected final Dust states at 1280×720/1560×720 and five tutorial root3 states; remote commit/device/child/owner acceptance pending |
| Lenovo Tab M11 / target phone | `V5 DEVICE` | Pending |
| Intended-child comprehension without adult verbal instruction | `V6 CHILD` | Pending externally |
| Owner visual acceptance | `V7 OWNER` | Pending |

## Grand Puff findings and repair state

### `BEV-001` — Required action was presented as a text control

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `FIXED_PENDING_VERIFICATION` |
| Evidence | `V1 STATIC`, focused `V2/V3`, source-bound local agent-review `V4` |
| Rules | `DL-AGE-01`, `DL-AGE-02`, `DL-READ-03`, `DL-READ-06`, `DL-UI-01`, `DL-UI-07` |
| Trigger | Live tell/opening displayed a large bottom-right `WAIT`/`BONK!` medallion while the actual fiction was move away, then tap Grand Puff's flashing head. |
| Expected | One visible world action: move to safety, then tap the live gold head marker. Text may only supplement it. |
| Actual before repair | The corner control competed with the world cue and could teach that a generic button, rather than Grand Puff's head, was the target. |
| Repair | Controller/touch integration hides both Hybrid and Classic boss action medallions and routes the intentional counter through the projected flashing head. The shared downward gesture guide replaces the retired emoji hand; old corner taps and held input cannot counter. |
| Closure | V3 verifies no corner-button counter and generous target routing; V4/V5 prove head readability and thumb reach; V6 proves comprehension. |

### `BEV-002` — Caption and HUD load competed with the battle

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `FIXED_PENDING_VERIFICATION` |
| Evidence | `V1 STATIC`, focused `V3`, source-bound local agent-review `V4` |
| Rules | `DL-READ-02`, `DL-READ-03`, `DL-UI-07`, `DL-SND-02` |
| Trigger | Long adult-readable caption slabs, mastery stars, round pips, pause and action chrome appeared simultaneously during the danger lesson. |
| Expected | One primary hazard/action, one supporting progress cue, and quiet periphery. Spoken instruction carries required semantics. |
| Actual before repair | The lower caption slab consumed a large play-space band and could remain semantically stale across state changes; mastery and round progress duplicated hierarchy. |
| Repair | Current integration removes WAIT/BONK, the duplicate mastery card, and the 3D square shadow; compacts captions; and keeps only the shared three-round progress cue during combat. |
| Closure | Fresh captures must show all live states without lower-arena obstruction or stale captions; exact cue timing and teardown remain V3/V5 checks. |

### `BEV-003` — Danger, time, and safety needed one reusable visual grammar

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `FIXED_PENDING_VERIFICATION` |
| Evidence | `V1 STATIC`, focused `V2/V3`, source-bound local agent-review `V4` |
| Rules | `DL-AGE-01`, `DL-READ-02`, `DL-READ-03`, `DL-READ-06`, `DL-MOT-03`, `DL-MOT-04` |
| Trigger | A locked circle or lane begins its tell while Roshan is inside the threatened geometry. |
| Expected | Calm danger footprint, unambiguous time-to-impact motion, and a visible destination outside danger; impact feedback describes the same event. |
| Actual before repair | Small perimeter dots and a thin cyan endpoint were visually abstract and competed with the hazard outline. |
| Repair | `EncounterTelegraph2D` owns a calm peach footprint, one contracting countdown outline, coherent impact pulse, enlarged cyan destination, and the approved moving hand. `DustBossTelegraph2D` is a compatibility wrapper. The floor danger pass is separated from the overlay hand/pips so Dust can render danger behind actors and UI above them. Visibility changes and discrete pips invalidate redraw explicitly; geometry buffers remain cached; `configure_quality("speedy")` caps continuous redraw requests at 30 Hz. Optional `total` defaults to three and supports Pepper's seven rounds. |
| Closure | V3 geometry/lifecycle/performance probes; V4 circle/lane/tell/impact captures; V5 phone-size squint and 30 fps/overdraw checks; V6 unaided movement comprehension. |

The safe-point geometry is authoritative for correctness. Visual placement
outside both actor silhouettes is a presentation preference constrained by the
actual safe polygon. Current player `render_priority` 100 plus `no_depth_test`
preserves Roshan in the foreground at overlap. Earlier screenshots therefore
do **not** establish complete occlusion in current source. The remaining issue
is weaker figure separation and small scale when silhouettes overlap; this is
`REPORTED_UNCONFIRMED` until fresh captures reproduce it.

### `BEV-004` — Generic splash did not teach the live encounter

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `FIXED_PENDING_VERIFICATION` |
| Evidence | `V1 STATIC`, focused `V3`, source-bound local agent-review `V4` |
| Rules | `DL-AGE-01`, `DL-READ-01`, `DL-READ-03`, `DL-READ-04`, `DL-SND-02`, `DL-MOT-03` |
| Trigger | Entering the boss room. |
| Expected | The actual room, one readable boss entrance, and a short visual demonstration of the exact weak marker and tap action. |
| Actual before repair | A generic blue page, cloud decoration, three prose/name blocks, and a cryptic finger-star-finger legend displaced the room and action. |
| Repair | `BossSplash2D` uses the actual attic, one focal animated boss and the shared downward gesture guide aimed at the gold head marker. The generic legend and wrong-way emoji hand are retired. Its timeline is pausable and explicit cancel/re-entry removes stale callbacks. |
| Closure | V3 lifecycle/cancel/re-entry and animation-ID fallbacks; V4 captures with the actual attic; V5/V6/V7 readability and acceptance. |

### `BEV-005` — Final encounter remains mixed-medium transition debt

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `IN_PROGRESS`; canonical owner is `MA-2D-002` |
| Evidence | `V1 STATIC` |
| Rules | `DL-MED-01`–`DL-MED-04`, `DL-LAY-01` |
| Fact | The restored room and telegraph are Canvas assets, and the dust-boss stage can skip spatial floor/wall dressing. Remaining player, boss, camera, projection, and effects compatibility paths still include `Node3D`, `Sprite3D`, `Camera3D`, and `Vector3`. |
| Limit | This rebuild reduces presentation debt but is not a completed true-2D conversion. No separate local finding may close the canonical game-wide inventory. |
| Closure | Convert this bounded stage to Canvas/Node2D under the canonical migration inventory with exact no-regression and then strict-zero evidence. |

### `BEV-010` — Splash can advance while the game is paused

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `FIXED_PENDING_VERIFICATION` |
| Evidence | `V1 STATIC`, focused exact-4.7.2 `V3` |
| Rules | `DL-AGE-06`, `DL-UI-05` |
| Concrete source | The splash keeps Pause input ownership but stops its timeline while the tree is paused or app focus is quarantined. Explicit cancel remains idempotent. |
| Impact | The teaching beat no longer expires behind Pause, and resume continues from the retained splash time. |
| Required repair | Implemented; retain the pause/focus/cancel negative probe in the trusted encounter gate. |
| Closure | Focused exact-4.7.2 probe confirms Pause freezes splash progression. Local trusted roster also passes; remote exact-head CI and device Pause/resume remain pending. |

## Legacy CombatTutorial presentation audit

The legacy tutorial remains useful: it is patient, never attacks the child,
demonstrates each gesture, repeats after inactivity, and requires intentional
input. This review does not authorize a broad Combat Wing rewrite.

### `BEV-006` — CombatTutorial is predominantly 3D runtime debt

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `IN_PROGRESS`; canonical owner is `MA-2D-002` |
| Evidence | `V1 STATIC`, focused exact-4.7.2 `V3`, source-bound local agent-review root3 `V4` |
| Rules | `DL-MED-01`–`DL-MED-04`, `DL-LAY-01` |
| Concrete source | The approved grotto is now a full-rect `TextureRect` at Canvas layer -10, bound through `Environment.BG_CANVAS`; the tutorial-created arena, `DirectionalLight3D`, backdrop quad/mesh, materials and `Label3D` pointer are removed. Current root3 frames show the normal framed DustBunnySprite rather than its whole pose atlas. The class and retained Roshan/imp/Camera/HitEngine staging still use `Node3D`, `Sprite3D`, `Camera3D` and `Vector3`. |
| Impact | Bounded scenery and cue debt shrank without adding 3D nodes, but the retained actors prevent strict-2D closure. |
| Bounded plan | Convert the retained actors/camera/effects in a dedicated mechanical slice; preserve lesson sequencing, input grammar and save behavior. |
| Closure | Canonical inventory reaches strict zero for this activity, exact gates pass, and current Mobile/device captures show every lesson state. |

### `BEV-007` — Tutorial instruction depends on long written imperatives

| Field | Value |
|---|---|
| Severity | `P1 / HIGH` |
| Lifecycle | `CONFIRMED_OPEN` |
| Evidence | `V1 STATIC`, focused exact-4.7.2 `V3`; root3 `V4` does not capture live caption persistence |
| Rules | `DL-AGE-01`, `DL-AGE-02`, `DL-UI-07`, `DL-SND-01`, `DL-SND-02`, `DL-SND-13` |
| Concrete source | Required captions are shortened to “Tap the imp!”, “Tap, tap, tap!”, “Press and hold!”, “Tap your partner!” and “Your turn!” in a scoped 640×82 strip with the compact style applied and the global layout restored on exit. They still route through `show_msg`, not an exact contextual voice ledger. |
| Existing strength | `EncounterGestureGuide2D` demonstrates press, drum and hold at the live target, repeats after inactivity and uses the approved picture chips. This reduces reading dependence but does not prove an exact spoken semantic cue. |
| Bounded plan | Bind each lesson to an exact recorded semantic cue synchronized with its live target. Preserve the open ledger gap until the recording exists and is tested. |
| Closure | Exact cue/ledger checks at V3, target-device intelligibility at V5, and unaided intended-child comprehension at V6. |

### `BEV-008` — Tutorial graphics do not yet use their approved picture chips

| Field | Value |
|---|---|
| Severity | `P2 / MEDIUM` |
| Lifecycle | `FIXED_PENDING_VERIFICATION` |
| Evidence | `V1 STATIC`, focused exact-4.7.2 `V3`, source-bound local agent-review root3 `V4` |
| Rules | `DL-READ-02`, `DL-READ-03`, `DL-UI-06`, `DL-MOT-04` |
| Concrete source | `EncounterGestureGuide2D` loads the approved TAP/HOLD chips beside one downward ghost hand at the live target. It is input-transparent, shared with Grand Puff, quality-capped at 30 Hz on Speedy, and replaces the large 3D pointer. |
| Impact | The learned gesture and live target now share one Canvas focal cue without a competing touch target. The wave deliberately removes the demo after teaching the verbs. |
| Bounded plan | Implemented; visually verify fingertip alignment, chip separation and hierarchy in every lesson state. |
| Closure | Durable source-bound captures plus V5/V6 squint/comprehension review. |

### `BEV-009` — Historical visual evidence cannot validate current tutorial ownership

| Field | Value |
|---|---|
| Severity | `P2 / MEDIUM` |
| Lifecycle | `FIXED_PENDING_VERIFICATION`; remote/device/child/owner evidence gaps remain |
| Evidence | Historical capture, current focused `V3`, and tracked source-bound local agent-review root3 `V4` |
| Rules | `DL-VIS-07`, `DL-VIS-08`, `MA-VIS-006` visual-evidence contract |
| Fact | The tracked packet binds root3 tap, combo, hold, partner and wave frames to exact source hashes. They show the corrected bunny frame, suppressed JUMP medallion, floor placement and shared guide; the partner frame keeps the hand above the portrait. The log verifies compact caption geometry/restoration and that the prior combo cannot hide the new hold guide. |
| Closure | Push the packet at an immutable remote commit, add success/cancel/re-entry capture coverage if required, and complete device, child and owner review. |

## Reusable presentation contract

The reusable part of this work is deliberately narrow:

1. Encounter logic exposes projected polygon points, progress, active state,
   player point and optional safe point.
2. `EncounterTelegraph2D` renders a consistent avoid/safe/impact language and
   never decides collision, damage, reward, or completion.
3. `BossSplash2D` accepts existing `SpriteFrames`, one supplemental name,
   weak-marker texture, optional approved scene backdrop and optional animation
   role identifiers. It contains no Grand Puff asset import.
4. Activity-specific compatibility wrappers may preserve public types while
   the shared renderer remains reusable.
5. `EncounterGestureGuide2D` owns the input-transparent downward hand, optional
   TAP/HOLD picture chip, cue colour and Speedy redraw cap; the host supplies
   only a projected live target and gesture mode.
6. Reuse does not imply every encounter needs a danger polygon, boss splash,
   or identical pacing. The child-visible grammar must match the actual verb.

This contract creates no new art and no new 3D nodes. Runtime owners must avoid
per-frame resource creation and keep the renderer below HUD/pause ownership.

## Verification and closure plan

1. Run exact Godot 4.7.2-stable import, analyzer, focused boss and touch probes,
   surrounding save/passive/re-entry probes, and the trusted full suite.
2. Record negative controls: zero input cannot win; stationary tapping cannot
   finish; the retired corner action cannot counter; tap outside the projected
   head cannot counter; focus loss cannot release a stale action.
3. Capture splash, circle tell, clean escape, impact, bump recovery, vulnerable
   head, phase-two lane, round completion and friendship at 1280×720 Mobile and
   a supported narrow-phone aspect. Bind captures to exact source and renderer.
4. Review hierarchy, caption lifetime, player/boss separation, safe-cue
   contrast, touch target size, cropping, and 30 fps/overdraw on Lenovo Tab M11.
5. Observe the intended child without added verbal instruction. Record whether
   she moves to cyan, waits for gold, taps the head, understands repeated
   patterns, pauses, resumes and completes.
6. Obtain owner visual acceptance. Only the canonical master audit may then
   move related `MA-*` states.

## Canonical cross-reference

The canonical master audit indexes this report as `SUPPORTING_CURRENT` scoped
evidence. `BEV-001`–`BEV-005` and `BEV-010` map to `MA-VIS-006`,
`MA-PLAY-001`, `MA-TOUCH-001` and `MA-2D-002`; `BEV-006`–`BEV-009` map to
`MA-2D-002`, `MA-VIS-006` and the exact-voice evidence gap. The cross-reference
does not alter aggregate lifecycle, inventory counts or satisfaction state.
