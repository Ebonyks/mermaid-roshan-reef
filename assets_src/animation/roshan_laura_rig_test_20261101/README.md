# Roshan locomotion restart and rejected Laura rig studies

Owner correction: 2026-11-01. Status: **NO VIABLE ANIMATION CANDIDATE**.
Take02 and take04 are OWNER_REJECTED. New locomotion-only trial is diagnostic,
not a successful redo, production asset or accepted Laura performance.

## Why the previous movement failed

The owner rejected shoulder-led motion and tweened sprite relocation, and
said to start over. The earlier upright front pose, Root banking and independent
position path could not establish tail propulsion. More arm/fin amplitude did
not repair that structural error. Geometry passes never accepted the acting.
The old source, original native frames, MP4s and Aseprite masters stay preserved.

## The separate restart

[Watch the failed stroke/glide diagnostic](restart_tail_propulsion/roshan_tail_stroke_glide.mp4).
It uses existing approved swim atlas cell10, a diagonal three-quarter swim pose,
rather than tilting the upright portrait. The shared front source is unchanged.
A provisional per-view binding keeps the same semantic14-bone parent graph,
with new registered rest/weights; this is not an accepted shared rig extension.

A traveling flexion begins at the tail base and reaches the fluke. The fin
feathers against its sweep. Shoulders, torso and whole-actor rotation do not
drive the action. Horizontal travel is integrated from a qualitative planar
tail/water drag approximation at240Hz, not an independent position curve.
Disabling tail motion gives exactly zero displacement and zero speed. That
ablation proves only this causal relationship; it does not validate swimming
biomechanics or establish a convincing character performance.

Two local renders were made, retaining the four earlier attempts in the count.
The first tore visibly at hard fin-weight boundaries and was rejected by the
agent. The second uses continuous weights and has no strict alpha predicate
failures, but remains **NOT VIABLE**:

| Evidence lane | Result at new binding take02 |
|---|---|
| Actual native render | Godot4.7.2-stable Mobile;181 samples,1280x720,30fps |
| Root/shoulder propulsion | No actor rotation; upper figure held; tail-disabled travel0 |
| Contour predicate | PASS across181 actual transparent captures; no threshold change |
| Visible mesh strain | FAIL102/181frames;0.30205–2.63007 against unchanged0.80–1.20 |
| Visible triangle folds |0 |
| Bone motion | FAIL Fin179.25deg/s/2410.83deg/s2; TailC721.39deg/s2; TailD865.52deg/s2; original limits140/650 |
| Natural acting/full-speed human review | Not established; selected full-size frame inspection only |
| Actual phone, child and owner acceptance | Not performed |

The two-render restart cap is reached. No third deformation revision is made.
New authored keys and a reviewed binding are required before another full-sequence
trial. The head/hair/arms remain largely rigid in this mechanics diagnostic;
no facing turn, wave, active brake or quiet supported settle is falsely supplied.

## Required poses before the next full sequence

The detailed [pose specification](restart_tail_propulsion/pose_requirements.json)
names load, power stroke, extension, glide, recovery/fluke reversal and brake.
Each needs a complete whole-figure silhouette, continuous waist/tail volume,
actual fluke edge/underside/face coverage and reviewed intermediate surfaces.
The wave additionally needs an open palm and useful gaze; a facing turn needs
actual quarter/front/quarter occlusion, near/far arms, face, hair and fin views.
Independent tied-ponytail response and neck/shoulder coverage remain open.
A flat front pose cannot acquire hidden surfaces from bone names or scaling.

Laura remains the owner's acting reference. No anime pixels, traced poses or
quantitative Laura swimming measurements were used. The selected reference
was sampled in the browser at0,10,34and48seconds: dialogue/face views and a
held tail close-up do not provide a measured full swimming cycle. Further
swimming reference must be directly observed before claiming a shot match.

## Source, evidence and reproduction

Use exactly Godot4.7.2-stable, Mobile rendering. The new native editable source
is restart_tail_propulsion/project.godot, study.gd, view_binding.json and
build_plan.py/plan.json. Run build_plan.py, then the native Godot project with
-- --capture. A real rendering window is required; the headless dummy renderer
is not pixel evidence. Run restart_tail_propulsion/inspect.py for actual-sample
geometry/motion/alpha diagnostics with the unchanged seed helper.

181 literal new RGBA frames and181 literal failed-first-binding scene frames
are preserved in indexed native ZIPs with SHA256 receipts. The silent MP4 is a
6.033s H264 review derivative, frame i at i/30seconds, square pixels, whole
1280x720 canvas, no interpolation or new pixels. The old source/master records
retain their exact scope. No new Aseprite master is claimed for this failed
new binding; the editable native solver, binding, scene and plan are retained.
No image generation, paid service, pixel repaint or protected-art change occurs.

See [intake](restart_tail_propulsion/intake.json),
[inspection](restart_tail_propulsion/inspection.json),
[solver ablation](restart_tail_propulsion/solver_evidence.json),
[job cards](job_cards.json), [provenance](provenance.json),
[manifest](manifest.json), [source inventory](source_inventory.json) and
[impact](../../../design/audit_impacts/roshan-laura-rig-test-20261101.json).
No gameplay/save changes, integration, finding closure, GENERATION_READY or
DELIVERY_ACCEPTED claim. MA-ROSHAN-005/006 and the master audit remain open.
