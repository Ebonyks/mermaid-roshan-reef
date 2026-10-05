# Character animation production protocol

Status: current production protocol under `DL-MOT-10` through `DL-MOT-16`.
Owner revision 2026-10-03 permits final animation workflows with identity,
motion, provenance and device checks and prefers Aseprite as the bridge.
Compulsory independent still generation is superseded; historical rejects remain.
Commission: 2026-09-11, richer Roshan movement direction and project integration.
This defines how to brief, build and review animation. It accepts no new clip,
asset, runtime behavior, cinematic delivery, device result or release.

Read the [master planning entry](../../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry),
[task index](../../audit/MASTER_AUDIT_2026-08-09.md#development-task-index),
[design rules](../06_COMPREHENSIVE_DESIGN_LANGUAGE.md#9-motion-acting-feedback-and-rewards),
[ledger](../05_DOC_LEDGER.md) and [development contract](../AUDIT_DEVELOPMENT_CONTRACT.md).
The [animation branch](../../audit/animation/README.md) records coverage and
acceptance; the [Roshan profile](ROSHAN_MOVEMENT_LANGUAGE.md) supplies acting direction.
Existing operational, protected-content, save and cinematic rules take precedence.
Routine authorized production continues without another planning approval checkpoint.

## Begin with an intention

Write one visible sentence: **who wants what, what they do, and what changes**.
For example: “Roshan notices the leaf, glides to the pool edge, scoops it with
the skimmer, and looks at the now-clear water.” Specify the character's emotional
register and the child's actionable cue separately. A cheerful performance does
not make an unavailable object actionable; an idle glance does not request a tap.

Use the character's profile to choose gaze, silhouette, rhythm and effort.
Roshan's working direction is Ribbon Glide for ordinary travel and attentive
work, with Playful Dolphin as an excitement register. These are proposed acting
references, not accepted clips, new anatomy or two interchangeable personalities.
Use [the profile template](../templates/CHARACTER_MOVEMENT_PROFILE_V1.md) for each
additional character; unknown canon stays unknown until sourced or explicitly decided.

## Select the production lane before making pixels

Default to local character design/animation and object workflows; APIs serve
cinematic scenes, preserving approved storybook 2D identity. Use Aseprite as the
editable sprite bridge where practical. The [dated workstation comparison](WORKFLOW_OPTIONS_2026-10-03.md#local-models-and-runners-for-this-pc)
selects bounded pilots; it does not accept their output or commission an install.
Record reasons for exceptions and respect the funded task budget.

| Lane | Construction and evidence |
|---|---|
| Interactive gameplay | Authored approved 2D frames/states on Canvas with explicit anchors and draw order. Navigation moves the actor through the stage; accepted authored states explain propulsion and acting. Observe the production input, contact and save owners. |
| Authored cinematic delivery | Suitable declared 2D/video workflow under revised `DL-CIN-01` through `DL-CIN-12` and the [AGENTS contract](../../AGENTS.md#animation-production-owner-decision-2026-10-03). Flattened footage requires exact provenance, production-profile scene/temporal/human gates and device/child/owner acceptance. |
| Motion or editorial study | Label reference-only; record method and source. A useful study never becomes runtime art or accepted cinematic pixels by relabeling or encoding it. |

Gameplay translation, gentle idle motion and effects remain subject to the
living-card rules. Wobbling or moving one static sticker does not establish
character animation; blending frames cannot repair missing contact or identity.
Use `Node2D`, `Sprite2D`, `Control` and related Canvas nodes. Existing spatial
staging is measured migration debt; no model, rig or 3D fallback is introduced.

Choose a method using the [dated workflow comparison](WORKFLOW_OPTIONS_2026-10-03.md)
and complete the [job card](../templates/ANIMATION_JOB_CARD_V1.md). ImageGen fills
specific art gaps, not an automatic animation-frame batch. Declared 2D
articulation/compositing/interpolation is eligible when it preserves identity
and performs the actual action. Declare authored key/frame durations and
cadence; animation on twos may preserve a painted performance without adding
synthetic in-betweens. Review the complete action and preserve frame mapping.
Holds/duplicates/static-sticker motion cannot
hide missing acting or contact. Historical owner rejections remain in force.

Prefer an editable RGBA Aseprite master for sprite isolation, matte/detail
cleanup, stable pivots/sockets, transitions, timing/tags and lossless atlas/JSON
export. Keep sources and cleaned layers separate; preserve painted appearance,
custom metadata and all master/export hashes. A video editor handles long
footage/audio; Aseprite may bridge bounded repair windows. Review every affected
transition, source-to-output mapping and actual engine sampling. Native outputs
and all edit/retiming/interpolation declarations remain in the derivation log.

Pilot one action before a batch. Set attempt, wall/cleanup-time and monetary/task
caps; default two generated takes per brief/backend. Stop after two nonviable
takes or the task cap, diagnose and change method/input. Rejects/cleanup count
in total cost/minutes per accepted second. Use only an already-authorized funded
budget for paid jobs; no routine new planning approval is introduced.
Position-only guides retain their neutral-field and excluded-pixel contract.

## Preserve crisp contours and figure-wide continuity

Owner corrections 2026-10-04: character performances must move as a coherent
figure. Shoulder, torso, dress/bodice, hair and tail respond to the acting when
appropriate. Root/pelvis, sockets and scene landmarks provide registration and
contact references; they do not authorize freezing the rest of the body while
only a limb animates. Preserve the source figure's changing silhouette,
attachments, cloth/hair response and counterbalance throughout the action.
Object motion likewise includes its relevant support and moving parts.

Owner correction 2026-10-05 (`ODR-ROSHAN-WHOLE-FRAME-20261005`): "No arm moves
as a single figure, the whole body moves at once, drawn as a whole frame." A
limb never moves as a separate cut-out over a body from another drawing, and
parts do not run on their own delays. Each frame is one whole drawing of the
figure; arm, shoulders, head, hair, torso and tail move together. The
[rejected cut-out wave](../../assets_src/cinematics/claude_2d_deform_wave_20261005/README.md)
and the [whole-frame revision](../../assets_src/cinematics/claude_whole_frame_wave_20261005/README.md)
record the difference; neither is accepted output.

Inspect decoded native frames before encoding to distinguish generated smear
from matte spill and export artifacts. Small character/object footage must
retain clear painted hands, fingers and prop edges. Review moving edges at the
intended scale through the complete action. Deliberate motion blur must be
specified in the direction brief and preserve readable acting/contact.

For a video pilot, request sharply defined painted poses, short-exposure motion
and continuous whole-figure anatomy. Bind globally registered original figure
poses rather than compositing unrelated limbs onto a frozen plate. Stronger
pose guidance is a timing experiment, not a guaranteed blur repair. The
[registered wave study](../../assets_src/cinematics/ltx_registered_wave_20261004/README.md)
retains both smeared native takes and the owner-rejected limb-only correction.
That correction sharpened arm pixels but did not meet figure-wide continuity.
A prompt revision generates a new candidate; it does not certify sharpness.

After bounded retries, diagnose and change inputs/method without hiding prior
costs. Authored 2D may be suitable when it performs the complete coordinated
figure action; isolated limb replacement alone is insufficient for this wave.
Local repaint/cleanup can repair a named region while its neighboring body,
cloth, hair and transitions remain temporally coherent. Global sharpening
cannot recover missing anatomy/contact. Do not start a still-generation campaign
or repeated upscaling in place of this diagnosis.

Keep full native outputs and editable masters. Declare spatial resampling,
pose-source switches, replacements, cadence and holds. Review the complete
figure before and after matte/detail repairs, including shoulder/wrist seams
and neighboring transitions. Export lossless frames and reopen the master.
Neither a crisp key nor a pixel-check PASS proves acting, a loop or device
performance.

## Verify the model recipe before judging a take

The [2026-10-04 two-pass wave trial](../../assets_src/cinematics/ltx_two_pass_wave_20261004/README.md)
checks the omitted refinement in the installed LTX-Video 2B 0.9.8 recipe.
Before submitting a multiscale job, record the actual first-pass dimensions,
learned latent upscaler, latent-statistics normalization, second-pass sigmas
and step count, guide bindings in both passes, and native decoded dimensions.
A first-pass-only result cannot be reported as the two-pass recipe. Preserve
both native outputs; whole-canvas output normalization is a declared production
transform and does not replace native-resolution QA. A Comfy reproduction
must state its differences from the publisher's executable pipeline.

At CFG 1, ordinary negative conditioning is omitted by the sampler. An
anti-blur phrase in the positive prompt can influence the request but cannot
guarantee short exposure, sharp fingers or complete anatomy. To claim effective
negative guidance, bind actual negative conditioning to a compatible dedicated
implementation and retain evidence that its attention code executed. A generic
NAG node whose hooks the model never calls supplies no such evidence.

Timed image guides influence motion; they do not lock poses to exact frames.
Inspect anticipation, the largest travel interval, every contact and the actual
settle time. Refine may improve contours while retaining a first-pass timing
failure. Place missing complete-figure keys before another bounded take;
register the body without freezing shoulder, torso, cloth, hair or tail pixels.

Sampling on twos is an authored cadence choice, not anatomy repair. Record
selected source indices, timing and any changed holds. Select a crisper frame
within a pair only if the full figure and neighboring action remain coherent.
If both frames fail, retain the defect as a failed span for repaint or temporal
retake; do not hold an unrelated clean pose over it. Review Aseprite exports
at their native resolution, reopen the editable master and verify pixel/timing
round trips before any production claim.

## Inventory and bind sources

1. Find the current profile, exact scene, costume, prop and accepted source family.
   Start Roshan with the [approved atlas contract](../../assets/characters/roshan_25d/README.md),
   then verify actual call sites and current specialist rules at the task baseline.
2. Record each usable source's path, SHA-256, dimensions, role, license/provenance
   and acceptance scope. Distinguish identity reference, pose key, temporal clip,
   contact pose, background and diagnostic capture; a pose sheet is not a loop.
3. Test existing authored states against the required action and runtime scale.
   Reuse intact approved art whenever it satisfies identity and purpose. Record
   the exact missing view, contact, transition or expression before generating.
4. Preserve protected originals and existing source masters. Put authorized
   derivatives at new paths; add each new asset to `ASSET_LICENSES.md` in its change.
   Keep rejected candidates and review material outside runtime `assets/`.

Do not repack Roshan for convenience: `MA-ROSHAN-003` remains a deferred
optimization. Do not loop Ballerina pose keys; `DL-MOT-09` retains its held-pose
and one-shot curtain-call contract. This protocol does not replace a specialist's
accepted behavior with a generic travel or celebration loop.

## Complete one brief per clip or shot

All fields below are required when applicable; write a reason for non-applicability.
Names such as `contact_begin` are proposed contract labels, not existing Godot APIs.

| Field | What the operator records |
|---|---|
| Identity | Stable character/clip ID, revision, task baseline, profile revision, author, purpose and lane. |
| Intent | Observable want/action/consequence; register; intended audience attention; one dominant verb. |
| Scene | Runtime route or movie/shot ID; place, costume, prop state, lighting reference, cast and fixed fixtures. |
| Sources | Exact approved bindings, hashes and roles; reuse decision; named gaps; rejected-source exclusions. |
| Entry and exit | Facing, pose, anchor, eye line, prop ownership, world state and safe resting state at both boundaries. |
| Geometry | Actor reference height, pivot, bounds, local hand/tool sockets, target contact region and layer/occlusion ownership. |
| Timeline | Seconds and authored-state indices for anticipation, action, contact, payoff and settle; loop seam or held span. |
| Translation | Who owns stage movement, reachable approach point, arrival radius, permitted travel path and camera responsibility. |
| Events | Which semantic markers may request sound, effects or a gameplay commit; preconditions; at-most-once owner. |
| Interruptions | Valid retarget, pause, focus loss, back, door, teardown and reload behavior at every phase; safe pose and prop resolution. |
| Readability | Intended display scale, supported aspect ratios, cue visibility, silhouette clearances and quiet background/effect budget. |
| Verification | Exact machine checks, in-context transitions, measurements, human review questions and remaining device/child/owner evidence. |

Bind pivots and contact geometry to one coordinate transform. Normalize cinematic
positions to the full frame and gameplay pose offsets to a stated actor reference
height. Include units and sign conventions; “slightly left” cannot be a socket
contract. Measure authored landmarks across frames instead of assuming equal cell
sizes guarantee stability. Declare tolerances before judging the candidate.

## Program intention, contact and cancellation together

Use a conceptual sequence of request → approach → anticipation → action →
contact/consequence → settle → available. This is a behavior contract to map onto
the existing architecture; it is not a commission to add an animation framework.
Gameplay state remains with its current state owner. Presentation reports events;
it does not independently grant rewards, save progress or select another room.

| Boundary | Required behavior |
|---|---|
| Valid touch | A visible response begins within two rendered frames at 30 fps (`DL-AGE-07`), even if travel or anticipation continues. Repeated taps cannot stack the action. |
| Approach | Use the [stage pathfinding protocol](../../audit/stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md). Travel to the reachable approach point; verify arrival, stop navigation and clear velocity before work. |
| Contact | The hand/tool meets the actual object at its declared socket and Roshan visibly performs the verb. Arrival, remote effects or a moving tool while she stays elsewhere do not count. |
| Consequence | The real gameplay owner validates current request, target, scene and eligibility, then commits the intentional action at most once after its required visible work. Sound/effects describe that same event. |
| Retarget or exit before commit | Cancel the prior request and all owned delayed work. No later frame event, timer, voice callback or tween can award its progress or act in the next scene. |
| Interrupt after commit | Preserve committed progress. Resolve the prop into its declared stable ownership, cancel remaining presentation safely, and do not replay the reward on re-entry. |
| Pause or focus loss | Clear touch ownership and apply the clip's declared freeze/cancel behavior; persist already committed progress through existing save rules. Resume cannot replay a commit. |
| Reload or return | Restore authoritative world progress and the exact source room/variant/camera contract; enter a safe pose. Do not infer completed work from a remembered animation timestamp. |

Separate a semantic contact interval from its optional sound/effect markers.
A scrub can contain several strokes while the job commits once after the required
work; a multi-step activity gives each step its own identity. Never attach reward
to “last frame reached” without validating the live request and actual action.
Demonstration clips share readable acting but cannot cross the completion threshold.

If a fixture prevents contact, fix route/socket/action selection. Stretching an
arm or sliding the whole actor through furniture cannot conceal a geometry error.
A still-active unresolved interaction offers a kind, voiced/picture-first route
to retry; it never costs progress or becomes a failure state. Voluntary retarget
or exit cancels quietly and clears owned cues; it cannot queue retry speech in
the next scene.

## Compare Roshan's two registers with one controlled pilot

Use the same approved identity, costume, camera, stage, route length, prop,
starting pose and action outcome for both studies. Compare at gameplay size with
HUD and also in a closer diagnostic view. Keep the screen layout fixed so acting,
not staging or camera polish, explains the difference.

Use the ten-second study in the Roshan profile: notice, travel, arrive, offer one
readable greeting, react and settle. Follow it with the separate real work/contact
study and carried-object turn before claiming contact quality. Run Ribbon Glide with a long easy glide and
quiet recovery; run Playful Dolphin with compact paired propulsion beats and a
brief buoyant reaction. Do not insert dolphin anatomy, acrobatics or extra action.
Timing ranges in the profile are starting hypotheses; record actual measurements
and revisions. Neither style may delay valid-touch feedback or compromise contact.

First use existing approved state coverage. If either study requires missing
acting, record that narrow gap and the applicable production lane before making
new pixels. Keep failed candidates with reasons. Select the most legible ordinary
performance and reserve the livelier register for narrative excitement; one good
study does not accept every clip in that family.

## Review hard failures before expressive quality

A missing required measurement is an evidence gap. The following failures cannot
be averaged away by beauty, smoothness, a high style score or machine success:

- Changed identity/costume, extra or detached anatomy, duplicated tail, cropped hair,
  unexplained silhouette substitution, sampling bleed or unstable pivot.
- Missing required authored action, pose snap, bad loop seam, false/remote contact,
  object penetration or ownership changing without a readable transfer.
- Delayed touch response, unreachable approach, duplicate/passive reward, stale
  callback, lost progress, broken pause/re-entry or a trapped navigation state.
- Undeclared derivation, missing native/provenance/transition evidence, guide-
  pixel reuse or unreviewed identity/topology/style/motion. The independent-still
  lane also retains its strict per-index/accepted-neighbor records.
- Runtime occlusion hiding the action/target, unsupported aspect behavior, or a
  measured device frame-time/performance failure against applicable project gates.

For every review, bind build/source revision, clip/asset hashes, scene, input
sequence, viewport, renderer, device, capture path and reviewer/date. Report:

| Measure | Evidence |
|---|---|
| Response and rhythm | Touch-to-first-visible-response in rendered frames; measured phase durations; where a glide, hold or recovery reads. |
| Anchors and contact | Per-frame pivot/socket positions in declared units; contact interval; maximum separation/penetration; checked tolerances and visible result. |
| Identity and flow | Start, apex, contact, turn, exit and loop-boundary frames; full-speed and slow review of every transition; explicit anatomical/style findings. |
| Truth and lifecycle | Far/near input, repeated tap, zero input, retarget, cancel before/after contact, pause/focus loss, exit, reload and exact return observations. |
| Presentation cost | Phone-size readability, two supported aspects, Mobile/Speedy frame pacing, transparent overlap and memory/load impact for the changed assets. |

After hard failures are resolved, compare intention clarity, character specificity,
weight/buoyancy, rhythm, warmth and quietness. Use descriptive evidence first;
optional 1–5 scores mean 1 unclear, 3 readable but generic, 5 specific and effortless.
Record each dimension and concrete revision; there is no composite passing score.
A missing child/device/owner session stays pending, whatever the desktop judgment.
Authoritative visual PASS still requires `DL-QA-11`; ordinary captures are diagnostic.

## Keep a repeatable iteration and evidence record

For each attempt retain brief revision, source/asset hashes, method, changed
parameters, exact output, review findings and disposition. Record “kept because…”
or “rejected because…” against exact frames/events, not merely “looks better.”
Fix the smallest cause, rerun its neighboring transitions and affected lifecycle
checks, then rerun required surrounding gates. Never weaken a tolerance to promote
a failed candidate; a justified contract revision retains the earlier failure.

For final footage retain the `DL-CIN-11` job-card derivation sidecar and run:

```text
python -B tools/audit_cinematic.py VIDEO --manifest QUALITY.json --profile production --report REPORT.json
```

Its existing scene/character/contact/track validator does not enforce every
workflow hash, edit declaration or external acceptance: review these separately
and retain exact receipts. No machine PASS alone is `DELIVERY_ACCEPTED`. A
chosen independent-still method also retains per-index records and runs
`--frame-regeneration-manifest`; keep that strict validator without mislabeling
video/2D output or weakening its method requirements.
An external job also needs the complete GitHub-hosted archive packet. A Grok job
uses the [required V1 shot card](../templates/IMAGINE_SHOT_CARD_V1.md); another
backend receives only supported bound inputs and the animation job sidecar.
Consult the
[current handoff formula](../GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md) only within
that higher-precedence contract. Keep `ARCHIVE_COMPLETE`, `GENERATION_READY` and
`DELIVERY_ACCEPTED` independent. This document alone grants none of those claims.

For gameplay, run applicable parser/inference, source/atlas, exact-engine import/
analyzer, focused positive/negative/save/teardown and full trusted gates. Recheck
authority and impact coverage before commit/push. Report implemented behavior,
machine evidence and visual/device/child/owner acceptance separately in the
[animation branch](../../audit/animation/README.md) and task impact record.

### Iterative repair with Aseprite and temporal retakes

Owner direction 2026-10-04: prioritize locally viable retake workflows and use
Aseprite drawings to identify and correct frame defects. A completed hardware
trial is required before describing a newer model as usable on the 8 GB card.
A configured graph, successful download or vendor recommendation is not evidence
of rendering speed, memory fit or acceptable animation.

- Mark defects on native frames and group them into continuous temporal spans.
  Distinguish torn/disconnected anatomy, ghost/smeared contours, matte/export
  problems, identity drift and timing/contact errors. Include clean context on
  both sides; expand the span when shoulder, clothing, hair or tail response
  extends past the initially damaged hand/limb frames.
- Prefer a few corrected complete-figure poses to an independent still job for
  every frame. The default first repair experiment uses clean entry/exit poses,
  one corrected intermediate pose and at most two generated candidates. Existing
  task caps and prior rejected costs remain visible; changing a backend or
  calling a render a retake does not reset them.
- Store originals, corrected poses, timing/tags, defects and registration/contact
  landmarks in an editable Aseprite master. Preserve painted contours and
  antialiasing. Distinguish ImageGen/redraw pixels from Aseprite registration,
  inspection and export; an import/roundtrip is not an automatic anatomy repair.
  Landmarks constrain placement/contact while permitting figure-wide acting.
- Feed corrected poses as declared keyframe guides, or use a temporal retake
  mask that regenerates complete frames in the selected span. Spatial attention
  masks and image-guide strength are influence controls, not promises that the
  model will reproduce a pose or freeze outside pixels. Strongly conditioning
  on bad source footage can retain its defects.
- Preserve native retake outputs and exact source/global frame mapping. If a
  model decodes the whole input again, verify reconstruction changes separately;
  for a review splice, retain original complete frames outside the replacement
  span and explicitly record the contiguous replacement. Never repair only a
  limb against a frozen body or conceal a bad boundary with a dissolve.
- Choose the retake window against the model's temporal VAE blocks and clean context, not only the visible defect indices. Retained source latents can contain failed neighboring motion. Prove mask behavior separately from decoded continuity; expand/replace contaminated context within the bounded brief when necessary.
- For isolated character/object work, a measured whole-figure crop may reduce empty-canvas cost. Preserve all moving parts with a motion margin, apply one source crop to every frame/guide, retain full originals and record the transformed registration coordinates. Audit the complete figure; this is not permission for frozen-body limb repair. New dimensions require a hardware/quality check.
- Cache unchanged conditioning/context only under exact model, VAE, source, prompt and dimension hashes. Preserve cold and warm timing separately. A completed low-resolution retake establishes hardware execution, not final-resolution quality or practical iteration speed.
- Review both boundaries and the complete figure at full speed and frame-step.
  Check velocity, identity/topology, contour clarity, body/clothing/hair response,
  root/contact and settle timing. A clean guide, low pixel difference or successful
  Aseprite export cannot accept the motion. Reject regressions and stop at the
  cap; use the result to change inputs/method rather than starting a still-frame
  generation campaign.

The [bounded repair/8 GB retake study](../../assets_src/cinematics/ltx_retake_repair_20261004/README.md)
records hardware execution and visual outcomes separately. It grants no runtime,
owner, device, child or final cinematic acceptance.

