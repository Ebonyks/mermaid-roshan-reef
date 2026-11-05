# Roshan native Godot rig stress study — 2026-10-31

Owner-commissioned source-only experiment: shoulder/arm bend, natural blink and
tail bend using native Godot 4.7.2 Canvas animation. The current chat explicitly
authorizes rigged parts and ImageGen repairs for this test. This is a bounded
exception to earlier whole-drawing/no-rig study restrictions; it does not change
the accepted production character, integrate art, close findings or release a game.

Baseline: `218ae766f8e60afb3f6338b8fafce28ec9fab7f2` from freshly fetched `origin/dev`.
Approved identity source: `assets/characters/roshan_25d/roshan_base.png`.
Direction: `design/animation/ROSHAN_MOVEMENT_LANGUAGE.md`.
Rules and change coverage: [impact](../../../design/audit_impacts/native-rig-stress-20261031.json).
Related `MA-ROSHAN-005` and `MA-ROSHAN-006` remain open; this study is not their repair.

## Construction and reproduction

Retained ImageGen source art supplies the painted pixels. Registration, alpha
cleanup, small eyelid extraction and resampling are deterministic derivations.
The final actor uses three textured `Polygon2D` meshes, fourteen `Bone2D` controls,
`Skeleton2D` and complete authored `AnimationPlayer` tracks. Painted upper-arm
and forearm pieces are rigid, with a rounded elbow overlap and a hidden painted
shoulder cap. Head/hair follow the torso as a rigid unit. The right arm stays
with the torso; five tail controls provide a bounded soft flex. Eyelids use small
local replacement patches on the rigid head. No 3D resources, AI inference in
the game, generated motion frames or game/save edits are introduced.

From this folder, run `python scripts/build_study.py`. The builder resolves its
inputs from the script location. Open
`godot/project.godot` in the exact approved Godot build. Keys 1/2/3 choose the
studies and Space pauses. Rendering: `godot --path godot --rendering-method mobile
--script res://render_stress.gd -- <absolute-output-folder>`. Audit:
`python scripts/audit_study.py <absolute-output-folder>`.

Each job has its own `job_*.json` card, fixed limits and acceptance gaps.
`provenance.json` retains exact ImageGen prompts, calls and hidden-model limits.
Raw source art is never overwritten. The `.gdignore` keeps the study out of the game.

## Iterations and review

1. Revision 1 rejected: arm weights pulled the upper tail; rectangular blink
   boundary; numerical local stretch/compression failures. Actual render, rig,
   telemetry and geometry audit are retained under `evidence/render_v1/`.
2. Revision 2 rejected: tail pulling improved, but elbow contour pinched and
   feathering used premultiplied colors as straight alpha, producing dark lids.
   Numerical arm/tail strain still failed unchanged thresholds. Exact evidence
   remains under `evidence/render_v2/`.
3. Revision 3, rejected: measured shoulder/elbow/wrist corrections, region boundaries in
   transparent arm/body gaps, finer mesh, wider tail-weight transitions and
   correct straight-alpha eyelid masks. Arm/body weight contamination remained.
4. Revision 4 improved the visible arm but still failed geometry near the narrow
   underarm gap. Revision 5's contour mesh clipped 523 opaque source pixels at
   rest and still failed strain, so it was rejected.
5. Revision 6 separated the soft arm but exposed lower-hair/torso and stationary
   arm/tail weight leaks. Revision 7 was a captured intermediate, not separately
   fully audited or accepted. Revision 8's broad soft elbow still compressed
   painted proportions, and a head/hair boundary crossed the stationary arm.
6. Revision 9 kept head/hair rigid but retained the unaccepted soft arm. It was
   captured without a separate full geometry acceptance claim. Revision 10 uses
   rigid painted arm segments and rounded overlap; all named final gates pass.

Machine checks cover actual Mobile renders, fixed-length bone transforms,
rigid face dimensions, visible triangle folding/stretch, alpha connectivity,
padding, identical loop endpoint pixels and repeated/randomized state seeks at
15/24/30/60/120 fps. Deliberate slit, detached-piece and head-scale faults must
be detected. These checks do not establish natural acting, unseen surfaces,
true swimming, device performance, human/child/owner or production acceptance.

## Evidence and acceptance

Implementation: three source-study animations and a reusable local render/audit loop.
Machine geometry, motion/contact, archive and Aseprite round-trip checks: **PASS**
at revision 10. Broader repository gates are tracked separately in the impact.
Codex inspected all 291 final frames on chronological detail sheets and selected
full-resolution poses. No visible shoulder/elbow gap, mask rectangle/halo or
unexplained source/contour pop remains in that inspection. A human normal-speed
naturalness judgement remains pending; numerical smoothness is not such a score.
Target-device, child and owner review: **PENDING**. Runtime integration: **NONE**.
`DELIVERY_ACCEPTED`: **false**. Source archive completeness is tracked separately.

Review videos are conveniences; exact RGBA pixels and hashes are authoritative.
Original PNG bytes remain locally preserved in ignored capture folders. All 30
Matroska archives contain lossless H264 RGB stream 0 plus FFV1 grayscale alpha
stream 1. Decode with `ffmpeg -i <archive.mkv> -filter_complex
'[0:v:0][0:v:1]alphamerge[out]' -map '[out]' <output>`; every decoded frame was
compared with its original pixels. Intermediate source-code edits were not each
separately snapshotted; historical renders and rig data are retained without
claiming complete historical code reproducibility. Final authoring sources are preserved.

## Watch and edit

- [All three studies](review/three_studies.mp4), left to right: arm, blink, tail.
- Arm: [normal](review/arm_bend.mp4), [half speed](review/arm_bend_slow.mp4), [master](masters/arm_bend.aseprite).
- Blink: [normal](review/blink.mp4), [half speed](review/blink_slow.mp4), [master](masters/blink.aseprite).
- Tail: [normal](review/tail_bend.mp4), [half speed](review/tail_bend_slow.mp4), [master](masters/tail_bend.aseprite).
- Exact final [geometry](evidence/render_v10/geometry_audit.json),
  [motion/contact](evidence/render_v10/motion_audit.json),
  [engine](evidence/render_v10/engine_receipt.json),
  [Aseprite proof](evidence/aseprite_roundtrip.json) and [manifest](manifest.json).

Review MP4s are flattened 1280×720, silent and square-pixel. Slowed copies
deliberately duplicate presentation frames; they are not animation masters.
Aseprite 1.3.18.4 retains whole RGBA cels without pixel-art conversion. Its
33/33/34 ms integer-ms review cadence does not retime native Godot playback.
The editable bone authoring source remains `godot/project.godot`.

## Exact stress results and limits

Ten actual Godot 4.7.2-stable Mobile/Vulkan/RTX3060Ti passes produced **2,910
frames**, **1,200 loop cycles** and **577,440 state seeks** at 15/24/30/60/120 fps.
Each seek is interrupted by an unrelated clip and random position before
returning; every pass has zero repeat matrix error. Final coverage is 97 arm,
73 blink and 121 tail frames, including the matching terminal sample.

| Final check | Actual result |
|---|---|
| Folded visible triangles | 0 in all three meshes and all checked poses. |
| Detached alpha pieces | One connected figure throughout; 12-pixel component floor. |
| Frame-edge clipping | 0 alpha pixels at any border. |
| Loop endpoints | 0 changed RGBA pixels in each clip; identical endpoint transforms. |
| Rigid painted arm pieces | Local length factors approximately 1.000000; no soft-skin width compression. |
| Rigid head distance error | Below 0.00002 px. |
| Body during arm gesture | Local length factors 0.9675–1.0601. |
| Tail during flex | **0.8174–1.1269**, within the fixed 0.8–1.2 prototype gate. This is real soft deformation, not a zero-distortion claim. |
| Sampled shoulder/elbow/wrist coverage | Minimum alpha 252/255; no uncovered sampled joint center. |
| Arm timing | Peak 115.41°/s and 394.23°/s², below fixed 140°/s and 650°/s² limits. |
| Blink | Two fully closed 30-fps frames; no simultaneous half/closed overlays or leaked state. |
| Archive pixel round trips | All 30 sequences, all 2,910 frames match exactly. |
| Aseprite reopen/export | All 291 final RGBA frames match exactly. |
| Falsification | Deliberate interior slit, detached piece, head scaling and 90° pose pop detected. |

A final audit-code review strengthened the seam gate: it now rejects an added
enclosed gap, more than eight pixels of growth in either total or largest hole
area over the rest reference, or a failed fault-injection control. The rest
figure has six intentional enclosed gaps (708 pixels total, largest 258 pixels).
All final frames retain six such gaps with total area at most 708 pixels; the
largest is 262 pixels. The [earlier geometry report](evidence/render_v10/geometry_audit_before_seam_gate.json) is retained separately.

Triangle strain uses source centroids with alpha above 192; it does not sample
every partially transparent contour texel. The pixel checks and full-sequence
frame sheets provide separate contour evidence.

Zero component breaks and covered joint centers are useful tearing checks,
not proof against every possible subpixel seam. Frame sheets cover the whole
sequence; normal/slowed videos are supplied for human motion judgement.
Independent head turns, dynamic clothes, prop contact, large bends,
out-of-plane action, true swim propulsion and target-device performance are
**NOT TESTED**. `MA-ROSHAN-005` and `MA-ROSHAN-006` remain open.

Four built-in ImageGen calls supplied the neutral, two eyelid sources and the
hidden shoulder cap. The model revision, request IDs and billing were not exposed.
Exact fourth-call provenance is in `provenance_shoulder.json`; only its shoulder
region is used, with the new neutral's original arm retained below native y460.
Art preparation and static segment/patch edits are in `evidence/art_preparation.json`.

## Project-gate continuation

The full local script passed its static, audio, visual and import prefix, then
stopped at the unchanged game-wide scanner: revision 6's 5.4 MB indented native
2D rig JSON exceeded the scanner's 4 MiB complete-inspection cap. Its compact
1.56 MB representation retains identical data and reconstructs the original
bytes exactly; see [format receipt](evidence/rig_json_format_receipt.json).
The original failed transcript remains preserved. Document authority/coverage
and the exact import/regression/probe suffix are re-run after this change.
This uses the permitted probe-by-probe verification lane; no check, threshold,
model-debt manifest or production game file is changed.

The complete continuation exited 0: all **82 ordered trusted probes exited 0**
with no reported probe failures. The earlier 4 MiB guard failure remains visible.

Current authority is reconciled at `a0bb2cf4691631a534e210a5fb60fd227213322f`; runtime and gate source
trees are identical to the tested baseline, as recorded in
[reconciliation proof](evidence/authority_reconciliation.json). The current
`ODR-DEMO-FREEZE-20261031` limits dev to demo-readiness work. This commissioned
experiment targets `codex/native-rig-stress-20261031`, outside dev.

Authoring currently uses editable `study.gd` tracks and `rig.json`; a saved
scene-editor rig/timeline is not packaged. The desktop preview reads sibling
art files; APK export and target-device performance are not packaged or tested.
