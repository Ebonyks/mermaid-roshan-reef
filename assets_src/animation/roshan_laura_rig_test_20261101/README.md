# Laura-led Roshan current-rig movement test

Owner commission and requested redo: 2026-11-01.
Status: SOURCE-ONLY REVIEW CANDIDATE; no production or owner acceptance.

[Watch the livelier redo](review/roshan_laura_vibrant_take04.mp4).
[Chronological sheet](review/contact_sheet.jpg).
[Editable whole-figure Aseprite master](masters/whole_sprite.aseprite).

## Owner rejection and correction

The owner rejected take02: "It's very stiff at this point, doesn't look like
laura at all. Redo, with more vibrant energy". Its source, movie and master
remain in rejected_take02/. Earlier numerical passes accept no acting.

The inspection found two concrete causes. The Root pitch leaned against the
travel direction. Also, LeftHand has no nonzero mesh weights, so its wrist
track changed telemetry without moving the painted hand. The previous
"wrist greeting" description was incorrect. The right-arm control names also
have no painted articulation in this seed. The painted forearm and hand are
bound to LeftFore; the upper arm is bound to LeftUpper.

The redo pitches into travel, distinguishes two efforts from their glides,
adds stronger fin follow-through, and performs the greeting through the
visible forearm and shoulder. Torso and tail answer the same action.
Take03 also tried independent Head motion, but that overstretched the current
neck/shoulder mesh. Numerical ablation isolated that cause. Take04 retains the
livelier acting and keeps only the unsupported independent head rotation at
rest; the head/hair unit follows the torso and whole-body bank.

The native 14-bone rig, rest, vertices, weights and painted source textures
remain unchanged from b700b846d1d2f4b1843279f268e2bb12e4b1f4ec. No new art,
new topology, image generation, paid service or game/save change is used.
The [Laura-led profile](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md#laura-led-visual-movement-specification-v2-2026-11-01)
provides authored Roshan direction, not quantitative measurements of Laura.

## Actual sequence

| Time | Visible action | Remaining limitation |
|---|---|---|
| 0-0.25s | Brief supported gather and blink | No targeted eye-direction artwork |
| 0.25-3.55s | Forward pitch into rightward travel; two tail efforts, recovery and glide | Frontal banked art, not a finished side-view swimmer |
| 3.55-5.50s | Counterbalance, opposite bank and leftward return | Route reversal only: actual facing-turn surfaces are absent |
| 5.30-9.95s | Shoulder/forearm greeting with coordinated torso/tail response; deliberate lowering | Existing fingers; no independently articulated palm |
| 9.95-11s | Fin resolves once and she returns to quiet availability | Independent hair and head/neck acting remain pose/binding gaps |

There are 331 actual samples, t=0 through 11s inclusive. Playback at 30fps is
11.033s. The 1280x720 square-pixel MP4 is a silent, lossy review derivative.
The original native figure PNGs are preserved literally in indexed ZIPs.
No mirror, horizontal squeeze, cross-fade, optical interpolation or invented
profile surface disguises the missing turn. The movie labels that limitation.

## Poses and bindings still needed

1. Registered left/right side-swim load, push, extension, recovery and brake
   poses. Frontal tail flex plus banking cannot reveal those surfaces.
2. Quarter-right, front crossover and quarter-left turn breakdowns, with
   changing face/hair, near/far shoulders and hands, and an attached fin swish.
3. A dedicated open-palm wave, finger silhouettes and useful hand articulation.
   Named unweighted controls are not evidence that the painted hand moves.
4. Neck/shoulder coverage that permits independent head acting without visible
   strain, plus view-correct gaze and eyelids.
5. Independent tied-ponytail/curl follow-through and tail/fin changing surfaces.
   Current hair moves with the head unit; it does not flow independently.
6. Exact review of strict interior-hole failures, rather than accepting a
   smooth trace as clean contour evidence.

## Evidence and scope

inspection.json records the current actual samples. The seed geometry/alpha
helper is copied unchanged; visible strain 0.80-1.20, zero triangle folds,
140 degrees/s and 650 degrees/s2 remain the same numerical floors. Motion,
geometry, alpha, natural acting and human/device/child/owner review are
separate claims. No failing floor is lowered and no human verdict is invented.

Rejected take02 and diagnostic take03 retain their own source/inspection
records. Take03's independent Head test fails geometry despite passing motion;
that is the reason for the bounded correction, not evidence of new accepted
anatomy. The initial scale-check report is also retained: it compared a
float32 .62 with a Python literal. Its corrected check compares observed scale
across all frames and checks the intended .62 to 1e-7; no animation or geometry
floor was changed for that diagnostic correction.

The first two local renders remain counted. The owner's explicit redo extends
the same task to at most four local renders, not a fresh campaign or a reset
of the 45-minute aggregate art-work window. Generated calls and paid cost are
zero. No artwork cleanup was performed. See job_cards.json for actual limits,
attempts, authoring changes and reported usage.

Agent review covers chronological sheets and selected full-size poses.
Human normal-speed/frame-step, actual phone performance, child and owner
acceptance remain open. MA-ROSHAN-005 and MA-ROSHAN-006 do not close, and the
master audit remains UNSATISFIED. This is not a production cinematic or game
integration, and grants no GENERATION_READY or DELIVERY_ACCEPTED claim.

## Reproduce and edit

Open godot/project.godot in exactly Godot 4.7.2-stable with Mobile rendering.
Press Space to play/pause the sequence.
motion.gd authors the current curves and writes godot/sequence.tres. Run
capture.gd with an absolute output directory after -- for actual scene and
transparent figure captures plus bone telemetry. The source project never
loads the main game or its saves. A rendering window is required; the headless
dummy renderer is not valid pixel evidence.

tools/inspect_capture.py <capture-folder> reproduces the source diagnostics.
tools/aseprite_bridge.lua is the project's unchanged whole-frame bridge:
331 native figure images, one layer, phase tags and 33/34ms duration rounding.
The native Godot curves are the editable rig source; Aseprite preserves and
reopens the complete rendered figure sequence. tools/package.py verifies
literal native PNG archives and exact RGBA equality after reopening the master.

See [source inventory](source_inventory.json), [job cards](job_cards.json),
[provenance](provenance.json), [manifest](manifest.json),
[export receipt](export_receipt.json) and
[impact](../../../design/audit_impacts/roshan-laura-rig-test-20261101.json).
