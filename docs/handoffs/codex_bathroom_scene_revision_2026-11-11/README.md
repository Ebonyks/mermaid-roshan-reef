# Bathroom scene revision work order (for Codex)

Status: `PROPOSED`, revision 1 (2026-11-11). Prepared by Claude for Codex. This is analysis, work packages and acceptance criteria only; it makes no game, art or audio change. Evidence baseline: branch `codex/claude-bathroom-action-audit-20261110` at `07e88a8beb26f8c0c0be0c63daa3c2128f78ffaf` (dev `c6e5d120` plus the packet), with the packet digest `ec6638ec434be53799249c3a6da7ba14527c12fe4e10c8b66a7b6d44e59cdf7d`.

Read first:
1. The [independent secondary review](../claude_bathroom_action_review_2026-11-11/README.md). Issue IDs `C-01` to `C-12` below refer to it.
2. The [audited packet](../../../assets_src/cinematics/claude_bathroom_action_audit_20261110/README.md) and its [scene code](../../../assets_src/cinematics/claude_bathroom_action_audit_20261110/raw/scene/scene.mjs).
3. The [master-audit scene acting rig pattern](../../../audit/MASTER_AUDIT_2026-08-09.md#scene-acting-rig-pattern-bathroom-study), which defines how this scene's style generalizes.
4. `design/animation/ROSHAN_MOVEMENT_LANGUAGE.md` (Turns T0–T4, timing table) and design-language `DL-AGE-01…07`, `DL-INT-01…04` and `DL-MOT-14…16`.

## 0. The request

Owner, 2026-11-11: "improve the bathroom scene by studying the animations, sequencing and current formula, and provide recommendations for improvement", followed by "create both handoff to codex for scene revision, as well as information into the master audit involving rigging process, so we can expand the style of this scene with relatively low effort to the rest of the game".

How this work order reads it:
- **Phase A** revises the **browser study** using the existing harness. It is fast to iterate, and every change is measurable with the probes shipped in the review. It is authorized as source-only prototype work, in the same scope as the packet.
- **Phase B** covers the rig contract reconciliation and the Godot reconstruction. It is **gated on the owner decisions in §4** and on whatever demo or integration rules are current when it starts.

## 1. Ground rules

- **Do not modify the audited packet.** It is hash-bound. Copy it to a new revision folder, `assets_src/cinematics/bathroom_scene_revision_20261111/`, with its own `manifest.json`, `.gdignore` and `iteration_summary.json`, and keep the rebound02 packet as the baseline.
- **Protected material:** do not touch `assets/book/`, `assets/audio/voices/` or `assets/characters/friends/`. Family voice cues stay silent placeholders in the browser study.
- **Medium:** true 2D only. No 3D resources, lights or models. Any new texture is ≤ 1024 px on its longest side or power-of-two; new audio is OGG. Every new asset gets an `ASSET_LICENSES.md` row in the same commit. Reuse approved art first.
- **Generated art:** only the named gaps in WO-A6. Fill out one `design/templates/ANIMATION_JOB_CARD_V1.md` card per brief. `DL-MOT-16` caps apply: at most two takes per brief, then stop and diagnose.
- **Report honestly:** keep machine evidence separate from visual, device, child and owner acceptance. Keep failed variants with the reason they failed.
- **Unchanged gates:** visible-triangle strain 0.8–1.2 with zero flips in all three looks, palm and bristle socket error < 1 px, passive and stationary input earn 0, release and resume keep progress, and a live wardrobe swap keeps the clock, actor and contact.

## 2. Phase A: browser-study revision, in order

Run the packet harness (`node test_playtest.mjs all|reversal|swapview|video`) and the review probes (`child.cjs`, `child2.cjs`, `trace.cjs` in the [review evidence](../claude_bathroom_action_review_2026-11-11/evidence/probes/)) **before and after each work order**. Record the deltas in a table that mirrors [`trace_summary.json`](../claude_bathroom_action_review_2026-11-11/evidence/trace_summary.json).

### WO-A1 Contact math: no soft-locks, visible targets (C-03, C-04)

Code changes in `scene.mjs`:
1. **Hit-test the visible fixture.** Replace the ellipse in `hit()` with the fixture outline (`assetData.outlines[f.id]`, already loaded as `cleanShapes`) dilated by a pad. Use pad 24 to start work and 48 to keep crediting once work has started (hysteresis):
   ```js
   function hit(point,f,pad=24){
     room.save(); room.lineWidth=pad*2;
     const p=cleanShapes[f.id];
     const inside=room.isPointInPath(p,point[0],point[1])||room.isPointInStroke(p,point[0],point[1]);
     room.restore(); return inside;
   }
   // update(): const moving=phase==='work'&&mouseTarget&&hit(mouseTarget,f,48);
   ```
   Keep `projectTouch()` unchanged: it decides where the bristles go, not whether the touch counts.
2. **Shape-agnostic completion with a mercy ramp** in `earn()`. The correct shape finishes at the time floor; any other intentional rub finishes shortly after:
   ```js
   const base=Math.min(g.distance/f.need,g.seconds/2.55);
   const shape=f.id==='tub'
     ? Math.min((g.span[1]-g.span[0])/85,g.reversals/2)
     : Math.min(g.arc/(TAU*1.06),sectors/7);
   const mercy=smooth((g.seconds-2.5)/3);   // credited seconds only; passive time never counts
   progress=Math.min(base,mix(shape,1,mercy));
   ```
3. Make the reversal pivot tolerate vertical drift. Keep `g.span` on x, but stop requiring the 85 px span once `mercy` reaches 1.

Accept when, on the 20 gesture cases, every case completes in ≤ 6 s of active scrubbing, the 10×6 px wiggle completes in ≤ 12 s, and correct shapes still complete fastest (`DL-AGE-05`). Stationary hold, off-target drag, touch cancel and passive watch must still earn 0 (harness `all`). Add a 20-point sampled start test per fixture: touches inside the visible outline start work, and touches 40 px outside do not.

### WO-A2 Feedback: response in every phase and a real completion beat (C-07 response, C-08)

1. In the `pointerdown` handler, when `startTouch()` returns false, call `acknowledge(point)`. It pushes a bubble puff at the finger (reuse `session.bubbles` with an `ack` flag) and sets a 0.4 s glance target that biases `session.attention`. This must render on the next frame.
2. Restructure `settle`:
   - 0–0.35 s: lift (the existing `smooth(age/.56)` becomes `smooth(age/.35)`).
   - 0.35–1.25 s: **admire hold**. Gaze on the fixture, a one-shot sparkle burst at the fixture centre, and one completion cue (`say(f.doneVoice)`, using a silent placeholder or an existing approved chime from the repo).
   - The clean reveal finishes by 0.75 s (`session.clean[...] = smooth(age/.6)`), and departure happens at `age >= 1.25`.
3. Final `done`: a 1.0–1.4 s celebration (the existing `pride` bones plus a sparkle ring), a voice placeholder, and the text panel kept only as an adult aid.

Accept when a probe tap in every phase changes the frame within 2 rendered frames, the reveal is complete at least 0.5 s before the first carry frame, and each fixture logs exactly one completion cue.

### WO-A3 Animation curves: leading brush carry and distance-scaled travel (C-06, C-07)

1. **Facing-relative brush angle.** In the `carry` branch of `update()`, the left-leg path (`route.left && acting.gripBridge`) currently blends towards `raised = .39 - travelling*.27`, which points backward. Express the carry angle relative to facing, so the left legs mirror the right: `leadAngle = facing<0 ? Math.PI - rightAngle : rightAngle`. Try two candidates and keep the better by metric: (a) **torch carry**, forward and up, about 2.5–2.9 rad on left legs; (b) **upright tuck**, about −1.2 rad near the chest at mid-glide. Flip the handle's transverse offset (`handleY` term in `handleOffset`) with facing so the palm stays on the painted handle.
2. **Distance-scaled travel.** Replace the fixed `FIXTURES[].carry` and the approach 2.15 s with `seconds = clamp(routeLength/200, 1.6, 2.6)`. Generalize `GLIDE_BEATS` to `n = clamp(ceil(routeLength/180), 1, 3)` pulses, with the last pulse ending by 0.62 of the leg so arrival keeps a glide. Keep `thrustPlan()` causal: the tail-disabled ablation must still give zero travel.

Accept when, in both directions, bristles lead the palm in ≥ 90% of carry samples, bristle-to-fluke distance is ≥ 80 px, and left/right parity is within 10%. Watch-mode non-interactive time must be ≤ 12 s (currently 18.3 s). Socket error stays < 1 px and strain stays 0.8–1.2 in all looks.

### WO-A4 Layering: draw the tool where the hand is (C-06)

When the brush leads, draw it inside the actor pass rather than in the room layer. The renderer already supports interleaving through the `between` hook used by `drawLeftHead()`. Emit the brush quad between the far-arm slot and the near-hand slot with `renderer.emit` (the same pattern as `drawLeftHead()`). Keep the room-layer draw during `work`, where the bristles must stay visible on the fixture.

Accept on frame-step at the midpoint of each left leg: no tool hidden by the tail or torso, and the fingers over the handle.

### WO-A5 Feedback and art: the tub payoff and diegetic grime (C-02, C-09)

1. **Tub refill (`DL-INT-02`, "water pours").** On tub completion, pour from the faucet with 2D particles from the spout (measure it on the dirty plate), while a clean-water layer rises from the bottom of the bowl over about 1.2 s with a wobbling edge, then bubbles and the duck pop up, then gleams. The water layer must sit inside the **dirty plate's** bowl (see WO-A6 for the registered water art). Keep `tubLip` occlusion over the water.
2. **Brush-path grime mask.** Give each fixture an offscreen mask canvas. On credited travel, erase along the bristle path (`destination-out`, line width about the bristle footprint, roughly 16–20 px). Show grime at alpha ≥ 0.7 where it remains. At completion, sweep the remainder clean under the sparkle.

Accept when at least 25% of the bowl interior changes state at completion, the cleared-mask area increases monotonically with credited travel, and passive time clears nothing.

### WO-A6 Art: named local repairs (C-01, C-05 part, C-09)

Reuse first. These are the named gaps, each limited to two takes per brief:

| Gap | Output (new path, RGBA, registered to dirty-plate coordinates) | Gate |
|---|---|---|
| Clean sink, registered | Clean-state sink cutout painted over the dirty plate's exact sink geometry (faucet, basin, cabinet, plinth) | Alpha-edge IoU ≥ 0.95 against the dirty sink and centroid offset ≤ 2 px; style match to the approved room |
| Clean toilet, registered | Same for the toilet, including the tank | Same |
| Clean tub water, registered | Water, bubbles and duck layer fitted to the drained dirty bowl's interior | Stays inside the bowl interior; the near lip occludes it correctly |
| Grime overlays (if reuse fails) | Child-readable smudge and "stink bubble" grime at fixture scale | Grime-to-clean ΔE ≥ 15 inside each fixture |
| Left-view head registration | The left head at the right-view head scale (first try data only: `leftHeadScale` 1.0, `leftHeadDrop` 0, then measure) | Head width matches between views within 1% |

Use the production feather pattern for the cutout edges (`_add_fixture_cutout()` in `scripts/games/day_one_bathroom_cleanup.gd`: an inner ring scaled 0.94/0.91 from alpha 0 to 1), not a hard clip. Record the source plate, the hash of each take, the job card and the `ASSET_LICENSES.md` row.

### WO-A7 Rig and art: the turn crossover (C-05). Phase A may prototype; production waits for OD-2

Implement the movement-language turn rather than the binary facing switch at `update()` line 789:

| Beat | Pose and view | Rule |
|---|---|---|
| T0 Notice | Gaze toward the new target (the existing `attention`) | Starts immediately |
| T1 Gather | Quarter-right; arms compact, tail curls under the body | No hand through hair or torso |
| T2 Cross | **Front seed view** from `roshan.canvas.shared` v1 (`views[front] = SEED_AVAILABLE`) | Both shoulders accounted for; the brush stays supported |
| T3 Commit | Quarter-left (the authored left head plus body) | The same attached tail and fin follow through |
| T4 Resolve | Left cruise; tail and ponytail resolve once | Stable size |

Make each view change at the frame where the outgoing and incoming silhouettes overlap most (tail tucked). Target a visible turn of 0.25–0.40 s, with the full reversal allowed to run longer if its surfaces need it. **A squash, cross-fade or instant mirror swap is not allowed as a substitute** (movement language, Turns).

Accept when head, palm and fluke displacement per frame is ≤ 20 px at every view change (currently fluke 120–126 px), no frame contains two views, and a frame-step of T1–T3 is reviewed in both directions and all three looks.

### WO-A8 Interaction (owner preference, OD-3): free fixture order (C-12)

Let a tap on any dirty fixture during `ready` or `carry` choose the next target; Roshan carries there with the same route and acting. Keep one arrival voice per fixture. Accept when all six orders complete; any save keys are added with defaults only.

## 3. Phase B: reconcile the rig and rebuild in Godot (gated on §4)

- **WO-B1 Contract v2 (shared-skeleton owner only).** Propose `roshan.canvas.shared` **v2.0.0** = v1 + `chest` split from `torso` + `ponytail_base` / `ponytail_tip`, with the adapter table from the master-audit section. This is a **major** contract change (topology): it needs an explicit adapter, remapped weights and all regression evidence for the existing native-rig outfit studies. Outfit workers do not fork the skeleton. The bathroom's quarter-right and authored-left views become contract views, filling the v1 `SOURCE_GAP` entries.
- **WO-B2 Rigby → Godot converter.** A tool (for example `tools/rigby_to_godot.py`) that turns `project.json` and images into one `Skeleton2D`, `Bone2D` nodes and skinned `Polygon2D` slots (`Polygon2D.bones` weights), with skins as data-only attachments per `design/animation/COSTUME_SKIN_CONVERSION_GUIDE.md`. Accept when rest transforms match within 1e-4, the visible-triangle strain over the demonstration animation equals the browser result within 0.005, and two skins swap mid-action on one live actor.
- **WO-B3 Godot scene.** Follow the [review's reconstruction checklist](../claude_bathroom_action_review_2026-11-11/README.md#7-deliverable-3-cold-start-reconstruction-checklist-raw-art--replayable-godot), steps 1–13, as a satellite that receives `main` by reference and keeps state on `main`. Integrate with the existing `day_one_bathroom_cleanup.gd` flow (supply hunt, drain beat, fixture cutouts) rather than replacing it. Port the harness modes and the gesture matrix as headless probes, and add them to the trusted roster only through an explicit workflow task. Run `scripts/ci.sh` green before any `dev` merge.

## 4. Owner decisions this work needs

| ID | Question | Default if the owner says "use the defaults" |
|---|---|---|
| OD-1 | Is a skinned 2D deformation rig over approved RGBA cutouts an accepted **runtime** representation for Roshan in gameplay? CLAUDE.md and AGENTS.md currently say she has no accepted skeleton, rig or skin-weight representation; rig work runs under scoped prototype exceptions. | Yes, for Canvas gameplay acting only, with the approved RGBA art as the only texture source. No GLB, 3D or model work. The CLAUDE.md and AGENTS.md wording changes only in an explicit high-risk task. |
| OD-2 | Adopt `roshan.canvas.shared` v2.0.0 (17 bones) as the single character authority? | Yes, through the shared-skeleton owner with an adapter; no second skeleton. |
| OD-3 | Free fixture order or fixed order? | Free order. |
| OD-4 | Tub payoff: refill with clean bubbly water, or a dry clean tub? | Refill (it matches the clean-room endpoint and `DL-INT-02`). |

## 5. Return package

- The revision folder with manifest, rebuild script, silent HTML, harness receipts (`all`, `reversal`, `swapview`, `video`), gesture-matrix output and a trace summary.
- A before/after metric table against the [review baseline](../claude_bathroom_action_review_2026-11-11/evidence/trace_summary.json): view-swap displacement, brush lead percentage, bristle-to-fluke minimum, non-interactive seconds, gesture-matrix completion times, strain range per look, and socket errors.
- Frame-step sheets for both turns in both directions, every reveal, and the tub refill.
- Job cards, take hashes, rejects and `ASSET_LICENSES.md` rows for any WO-A6 art.
- A short status listing which issue IDs are resolved by machine evidence, which await visual review, and which remain open. Device, child and owner acceptance stay separate.
