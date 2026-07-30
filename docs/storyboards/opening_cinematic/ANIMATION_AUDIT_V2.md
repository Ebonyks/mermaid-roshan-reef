# Opening Cinematic V2 Animation Audit

Date: 2026-07-26

Status: improved 12 fps storyboard animatic approved for review, but **failed
the external production/release quality gate**. It must not be treated as final
production animation or an in-game integration candidate.

External audit verdict: **FAIL**, 56 floor violations. The technical encode
passes; temporal construction, global character identity, contact, motion, and
scene congruency do not meet the production protocol.

## V3 iterative redesign follow-up

V3 was built after the owner requested lower review thresholds and repeated
redesign until the audit succeeded. The result is an **animatic-profile PASS
with 0 errors**. The unchanged production profile still reports **FAIL with 56
floor violations**; V3 is therefore approved as a storyboard/review animatic,
not as final production animation or a Godot integration candidate.

| Profile | Scene floor | Character-passport floor | Result |
|---|---:|---:|---|
| `animatic` | 4.25/5.00 each | 4.50/5.00 each | **PASS, 0 errors** |
| `production` | 4.85/5.00 each | 4.90/5.00 each | **FAIL, 56 errors** |

The audit tool now exposes these named profiles. `production` remains the
default and may not be lowered implicitly. The lower profile records that a
candidate is strong enough for story, timing, and editorial review; it does not
claim production-grade anatomy, identity locking, contact tracking, or game
readiness.

### V3 changes and reflexive iteration

- Regenerated F136-F162 as three linked sheets: Daddy's rise and hand offer,
  Roshan's hand clasp and rise, then the pair's aisle glide.
- Regenerated F199-F234 as four linked sheets: monotonic stair descent, single-
  platform transfer, stable platform settle, then terrace orientation.
- Preserved the corrected aircraft stair: it opens outward from the airplane
  and downward.
- Preserved all other accepted V2 frames and encoded the replacement set with
  no crossfades and no motion-interpolated synthetic frames.
- Rejected a stair candidate with a detached second platform.
- Rejected a later stair sheet that rewound both characters to the top after
  they had already reached the platform.
- Rejected a terrace candidate whose first panel omitted Daddy.
- Re-audited the rebuilt video only after changed-frame contact-sheet review
  confirmed one platform, two present characters, readable hand ownership, and
  no action rewind.

Seven sheets and 63 frames were replaced. The intentional F198-F199,
F225-F226, and F234-F235 editorial reframings are cuts; they are not described
as continuous locked-camera motion.

### V3 deliverables

- [V3 12 fps review video](v3/opening_cinematic_v3_12fps_22.5s.mp4)
- [Changed-frame contact sheet](v3/v3_changed_frames_contact.png)
- [Reproducible V3 builder](v3/build_v3.py)
- [Completed V3 review manifest](v3/external_audit/review_manifest.json)
- [Successful animatic audit](v3/external_audit/cinematic_quality_report_animatic.json)
- [Unchanged production-gate audit](v3/external_audit/cinematic_quality_report_production.json)
- [Reproducible V3 manifest builder](v3/external_audit/build_review_manifest.py)

V3 technical verification:

- H.264, 1280x720, YUV420p;
- 270 decoded frames at exactly 12 fps;
- 22.500 seconds, silent;
- SHA-256:
  `730445bd1a6292a15867eca56a28a5f3549f131b9ba34705719647c6f8036314`;
- external tool SHA-256:
  `284d7190a7c80fb8839c26994a1e0d32fc2f7785614f9b0233b06633ccf78663`;
- validator regression tests: 6/6 passing.

The audit's score floors are manifest gates backed by provisional Codex visual
review. The validator verifies video metadata, completeness, tracks, contacts,
passports, and score thresholds; it does not independently infer anatomy,
emotion, or artistic quality from the pixels. That limitation remains explicit
in the V3 manifest and prevents the 0-error animatic result from being
misrepresented as an independent production review.

## Work completed

- Rebuilt F073-F081 as a locked-camera reassurance/sway shot.
- Rebuilt F136-F162: Daddy rises, offers his hand, Roshan rises, and they move
  toward the door using one camera setup per shot.
- Rebuilt F199-F207 while preserving the corrected outward-and-downward stair.
- Rebuilt F235-F243 as a locked side view; the previous mid-shot rear-view flip
  was removed.
- Rebuilt F253-F270 around stable Sky Lagoon reveal/finale compositions.
- Rebuilt F018 from F017 with one normal approach increment, removing the
  original surprise close-up.
- Applied background-directed stabilization to F136-F153 and F253-F270.
- Re-extracted and re-labeled all affected frames, then checked for exposed
  borders, duplicate labels, and ordering errors.

Eight complete nine-frame groups were regenerated. F018 was repaired
mechanically, for 73 changed frames in the 270-frame master.

## Before/after measurements

Measurements use declared static-background regions at 96x54. Lower is better.

| Shot | Frames | Mean difference | Maximum difference | Camera acceleration RMS | Result |
|---|---|---:|---:|---:|---|
| Reassurance sway | F073-F081 | 3.27 -> 3.22 | 4.48 -> 4.12 | 0.93 -> 0.00 | Pass |
| Daddy rises | F136-F144 | 8.43 -> 6.66 | 18.55 -> 7.81 | 3.00 -> 2.90 | Conditional: discontinuity fixed; residual AI redraw/occlusion noise |
| Roshan rises | F145-F153 | 8.21 -> 6.99 | 20.75 -> 9.93 | 3.72 -> 3.53 | Conditional: discontinuity fixed; residual AI redraw/occlusion noise |
| Aisle travel | F154-F162 | 9.99 -> 5.13 | 16.46 -> 7.66 | 1.36 -> 0.00 | Pass |
| Stair descent | F199-F207 | 5.57 -> 5.23 | 7.31 -> 7.26 | 2.27 -> 1.77 | Conditional: stable background; large authored locomotion accents reviewed |
| Doorway turn | F235-F243 | 22.12 -> 6.46 | 51.44 -> 7.82 | 3.53 -> 0.76 | Pass |
| Kingdom reveal | F253-F261 | 15.88 -> 6.47 | 23.70 -> 7.87 | 3.27 -> 3.14 | Conditional: major geography jumps removed; minor redraw-vector reversals remain |
| Gameplay handoff | F262-F270 | 9.28 -> 9.21 | 15.31 -> 14.40 | 2.54 -> 1.65 | Conditional: improved, still close to the camera-acceleration target |

The original F017-F018 aligned difference fell from 18.71 to 4.87, and its
hold-then-pop flag was removed.

## Stutter review

The automatic intra-shot scan fell from five flags to three:

- F201-F202 and F206-F207 are monotonic stair-descent pose accents. Their fixed
  stair/aircraft background stays below the discontinuity ceiling.
- F249-F250 is Daddy's deliberate head turn in the reaction close-up. It is not
  a camera change.

These remain visible key-pose accents at 12 fps, so the stair and reaction shots
are conditional animatic passes rather than final-animation passes.

## Rejected attempts

- A temporal crossfade for F202 was rejected because it produced double faces,
  limbs, tails, and stair rails.
- A dedicated generated F202 in-between was rejected because its camera scale
  and stair composition did not match the surrounding shot.
- A 24 fps motion-compensated encode was rejected after intermediate-frame
  inspection showed strong double contours and warped characters. It is not
  included in the delivered package.
- Stabilization passes that exposed black frame edges or duplicated labels were
  rejected and rebuilt before the final encode.

## Delivery verification

- Sheets: 30
- Source frames: 270
- Master: `v2/opening_cinematic_v2_12fps_22.5s.mp4`
- Video: H.264, 1280x720, YUV420p
- Rate: 12 fps
- Duration: 22.500 seconds
- Decoded frame count: 270
- Audio: none
- SHA-256:
  `856fb9cd14b561fe7f415391d42621d790b77621fcafbf7098aa1695da278143`

The original storyboard, frames, and MP4 remain unchanged outside `v2/`.

## External Codex cinematic audit

### Tool discovery and verification

The later Codex worktree contains the external quality gate at:

` .worktrees/codex-local-cartoon-video/tools/audit_cinematic.py`

Its companion production standard is:

` .worktrees/codex-local-cartoon-video/docs/TEMPORAL_ANIMATION_INTEGRITY_AND_QUALITY_GATE_PROTOCOL.md`

The leading spaces above are typographic only; both paths begin with
`.worktrees`.

The tool was inspected before use and its four validator regression tests all
passed. Audit provenance:

| Item | Value |
|---|---|
| Tool schema | `cinematic-quality-report-v1` |
| Tool SHA-256 | `c5d0f3eec411fbfc70b88d14adf53ddf5d5b3bf48e2c231cb050e478a45dd5d2` |
| Protocol SHA-256 | `809e4bec0d2bb592d7c8e7e9851724a0add5f35ebf0e69d2b43d8db19bbbfdfe` |
| Python | 3.11.9 |
| Pillow | 11.3.0 |
| FFmpeg/FFprobe | 8.1.2 pinned build |
| Validator tests | 4/4 passing |

The tool decoded all 270 frames and confirmed 12 fps. Its automatic 160x90
grayscale cut detector found eight candidate scenes beginning at F001, F019,
F028, F091, F100, F190, F244, and F253.

The cut detector uses an adjacent-frame difference threshold of the greater of
24 grayscale levels or 3.5 times the median delta. It intentionally favors
conservative cut separation; it does not prove that every long candidate scene
contains only one camera setup.

### What the tool does and does not do

The Python tool is a strict manifest and release-gate validator. It checks:

- decoded frame rate and frame count;
- contiguous scene coverage;
- required scene/background/character declarations;
- one sample per declared track per frame;
- optional normalized landmark step limits;
- character-passport reference and landmark presence;
- scene score floors of 4.85 in construction, identity, motion, contact, style,
  and performance; and
- production-wide character-passport floors of 4.90.

It is not a neural landmark detector and does not independently judge anatomy,
beauty, emotion, contact, or style from pixels. The review manifest therefore
contains coarse normalized head/vehicle tracks and provisional Codex visual
scores. Those tracks exercise completeness and gross-step validation; they do
not satisfy the protocol's final requirement for detailed face, hand, contact,
silhouette, prop, and background-landmark tracks. Independent human scores are
also still required.

### External tool output

The completed run returned:

```text
CINEMATIC_AUDIT|FAIL|errors=56
fps=12
frame_count=270
passed=false
```

There were no validator errors for missing frames, scene gaps, character-to-
track mapping, per-frame sample coverage, or missing passport references. The
56 failures are quality-floor failures:

| Criterion | Total failures |
|---|---:|
| Construction | 10 |
| Identity | 10 |
| Motion | 10 |
| Contact | 9 |
| Style | 8 |
| Performance | 9 |
| **Total** | **56** |

Of those, 44 are scene-score failures and 12 are character-passport failures.

### Scene scores

The release floor for every scene criterion is 4.85. An average cannot
compensate for a failed criterion.

| Scene | Frames | Construction | Identity | Motion | Contact | Style | Performance | Average | Failed criteria |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Exterior approach | 1-18 | 4.65 | 4.70 | 4.55 | 4.90 | 4.80 | 4.55 | 4.692 | construction, identity, motion, style, performance |
| Cabin orientation | 19-27 | 4.72 | 4.70 | 4.60 | 4.65 | 4.82 | 4.78 | 4.712 | all six |
| Reassurance and hug | 28-90 | 4.68 | 4.66 | 4.45 | 4.35 | 4.82 | 4.82 | 4.630 | all six |
| Landing exterior | 91-99 | 4.78 | 4.75 | 4.62 | 4.68 | 4.85 | 4.70 | 4.730 | construction, identity, motion, contact, performance |
| Cabin release to door | 100-189 | 4.55 | 4.60 | 4.35 | 4.25 | 4.78 | 4.68 | 4.535 | all six |
| Door, stair, and platform | 190-243 | 4.52 | 4.62 | 4.38 | 4.30 | 4.78 | 4.72 | 4.553 | all six |
| Reaction close-up | 244-252 | 4.78 | 4.70 | 4.58 | 4.72 | 4.85 | 4.86 | 4.748 | construction, identity, motion, contact |
| Kingdom reveal and handoff | 253-270 | 4.68 | 4.68 | 4.48 | 4.55 | 4.72 | 4.82 | 4.655 | all six |

The strongest scene is the reaction close-up, where emotional performance and
style pass their scene floors. Its character construction, identity, motion,
and contact still fail. The weakest scene is the cabin release-to-door span,
followed by the stair/platform span. Those contain the most difficult hand,
body, locomotion, camera, and object-contact continuity.

### Character passport scores

The global floor is 4.90 for every criterion.

| Character | Construction | Identity | Motion | Contact | Style | Performance | Average | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Roshan | 4.72 | 4.73 | 4.60 | 4.55 | 4.82 | 4.78 | 4.700 | Fail all six |
| Daddy | 4.70 | 4.68 | 4.58 | 4.52 | 4.82 | 4.80 | 4.683 | Fail all six |

Both characters remain recognizable, but generated shots change face
construction, hair/crown volume, torso and tail proportions, hands, cape,
accessories, and detail placement. The global passport gate correctly treats
small cumulative changes as identity drift.

### Gate-by-gate protocol evaluation

| Gate | Result | Evidence |
|---|---|---|
| 0 - Inputs and traceability | Conditional pass | Video hash, references, generator class, deterministic processing, tool hashes, manifest, scenes, and provisional tracks are recorded. Exact raster-model version and independent reviewer are unavailable. |
| 1 - Frame integrity | Fail | Recurring anatomy, hand, face, accessory, perspective, stair, and background redraw defects remain. |
| 2 - Triplet/action-window integrity | Fail | Five original hold-pop flags were reduced, but stair and reaction accents remain; production masks, contacts, and detailed landmark tracks do not exist. |
| 3 - Scene congruency | Fail | No scene satisfies every 4.85 criterion. Long bootstrap scenes also contain camera setups that need explicit shot subdivisions. |
| 4 - Character passport/anti-morph | Fail | Roshan averages 4.700 and Daddy 4.683 against a non-compensating 4.90 floor. |
| 5 - Interaction/contact | Fail | Hug, hand clasp/release, seatbelt, rail, stair, and ground contacts are readable as story beats but not spatially stable. |
| 6 - Camera/editorial continuity | Conditional fail | V2 removes the worst flips and geography jumps, but redraw drift and undeclared shot changes remain. |
| 7 - Rhythm/emotional readability | Conditional fail | Safety, wonder, and reassurance read clearly; some actions are still broad key-pose jumps without enough anticipation, overlap, or settle. |
| 8 - Whole-cinematic coherence | Fail | The style family is recognizable, but detail density, construction, character identity, and world geometry vary across independently generated panels. |
| 9 - Encode/playback/release | Review MP4 pass; release fail | H.264 review master verifies at 270 frames/12 fps/22.500 seconds. No accepted OGV, audio pass, Godot integration, or target-device playback evidence exists. |

### External audit artifacts

- [Bootstrap manifest](v2/external_audit/bootstrap_manifest.json)
- [Completed review manifest](v2/external_audit/review_manifest.json)
- [Machine-readable audit report](v2/external_audit/cinematic_quality_report.json)
- [Eight-scene sample contact sheet](v2/external_audit/scene_sample_contact.png)
- [Reproducible manifest builder](v2/external_audit/build_review_manifest.py)

## GPT and machine-learning provenance

### Systems used

| Stage | System | Role |
|---|---|---|
| Direction and orchestration | Codex, a GPT-5-based agent | Broke the story into frames, inspected project references, wrote prompts, analyzed defects, selected repair windows, rejected bad candidates, and documented decisions. |
| Raster creation and editing | OpenAI built-in image generation | Generated and edited the storyboard sheets using character, aircraft, adjacent-frame, and Sky Lagoon references. The exact internal image-model name/version is not exposed in the project logs, so none is claimed. |
| Image assembly | Sharp in a Node runtime | Cropped panels, rebuilt F018, applied translation stabilization, repaired labels/borders, and produced review contact sheets. |
| Video processing | Pinned FFmpeg 8.1.2 and FFprobe | Encoded H.264, decoded verification frames, measured duration/frame count, and attempted motion interpolation. |
| First temporal screen | Deterministic grayscale analysis | Used 96x54 static regions, +/-3-pixel translation search, aligned difference, camera acceleration, direction reversals, and hold-pop thresholds. |
| External production gate | `audit_cinematic.py`, Pillow, FFmpeg/FFprobe | Detected candidate cuts, validated the review manifest, enforced scene/passport floors, and emitted the 56-error report. |

### What “learning” means here

Pretrained machine-learning models were used for language reasoning and raster
generation, but **no local model training occurred**. There was no fine-tuning,
gradient descent, reinforcement update, LoRA training, or permanent change to
GPT/image-model weights.

The observed improvement was an iterative inference and production loop:

1. The user supplied story intent and project constraints.
2. Codex read canonical Roshan, Daddy, airplane, and Sky Lagoon references.
3. The image generator produced candidate sheets.
4. User feedback and audits identified defects, including insufficient frame
   density, wrong stair direction, camera instability, rough motion, and
   stutter.
5. Codex converted those defects into tighter prompts and measurable rules:
   locked camera, static landmarks, monotonic action arcs, exact stair
   direction, background geography locks, and hold-pop rejection.
6. Deterministic metrics and visual review accepted or rejected each attempt.
7. Failed methods became negative evidence: crossfades and 24 fps motion
   interpolation were rejected for ghosting; a dedicated F202 generation was
   rejected for composition drift; stabilization artifacts were rebuilt.
8. Durable project learning was written into the frame guide, QC criteria,
   V2 audit, manifests, and report.

This is in-context adaptation and documented process improvement, not model
weight learning. A future session can reproduce the decisions because the
knowledge is in project artifacts.

## Revised release decision and next work

V2 remains useful as a detailed story, timing, and camera-intent animatic. The
external gate supersedes any interpretation that “approved for review” means
“approved for production.”

The shortest credible route to a production pass is:

1. Approve a versioned Scene Direction Brief and rhythm contract for each shot.
2. Use persistent character rigs, layered cutout parts, or a temporally
   conditioned animation system instead of independently redrawing complete
   frames.
3. Lock one background plate, camera transform, object IDs, masks, and depth
   order per shot.
4. Rebuild the cabin release/door and stair/platform spans first.
5. Track face, hands, contacts, tail, accessories, stair/rail, and background
   landmarks on every frame.
6. Run normal, silent, half-speed, frame-step, contact-sheet, and character-
   passport reviews.
7. Obtain independent human scores meeting every scene floor and both 4.90
   character-passport floors.
8. Encode the accepted master to OGV, integrate it in Godot, and validate
   playback on the Lenovo Tab M11.
