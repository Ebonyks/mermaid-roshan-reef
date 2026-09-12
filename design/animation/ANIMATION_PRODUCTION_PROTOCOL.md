# Character animation production protocol

Status: current production protocol under `DL-MOT-10` through `DL-MOT-13`.
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

| Lane | Construction and evidence |
|---|---|
| Interactive gameplay | Authored approved 2D frames/states on Canvas with explicit anchors and draw order. Navigation moves the actor through the stage; accepted authored states explain propulsion and acting. Observe the production input, contact and save owners. |
| Authored cinematic delivery | Complete flattened generated frames under `DL-CIN-01` through `DL-CIN-12` and the full [AGENTS cinematic contract](../../AGENTS.md). Every changed action frame independently passes the required full-frame evidence. |
| Motion or editorial study | Label reference-only; record method and source. A useful study never becomes runtime art or accepted cinematic pixels by relabeling or encoding it. |

Gameplay translation, gentle idle motion and effects remain subject to the
living-card rules. Wobbling or moving one static sticker does not establish
character animation; blending frames cannot repair missing contact or identity.
Use `Node2D`, `Sprite2D`, `Control` and related Canvas nodes. Existing spatial
staging is measured migration debt; no model, rig or 3D fallback is introduced.

Cinematic action/review delivery forbids tweening, morphing, optical flow,
interpolation, cross-dissolve, sprite/cutout animation, rig animation, procedural
warping, static-layer/camera translation and duplicates concealing missing action.
Intentional holds need a declared span and narrative purpose. Production-only
whole-canvas normalization follows acceptance and preserves native generation hashes.
Position guides remain neutral-field, `POSITION_GUIDE_ONLY`, non-delivery evidence
under the complete binding exception; no guide pixels enter a delivered frame.

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
- Forbidden cinematic method, missing native/provenance/frame-neighbor evidence,
  guide-pixel reuse or unreviewed identity/topology/style.
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

For cinematic regeneration, add every field required by `DL-CIN-11` and run
`tools/audit_cinematic.py`; this protocol's clip summary cannot replace frame records.
An external job also needs the complete GitHub-hosted archive packet and the
[AGENTS-required V1 shot card](../templates/IMAGINE_SHOT_CARD_V1.md). Consult the
[current handoff formula](../GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md) only within
that higher-precedence contract. Keep `ARCHIVE_COMPLETE`, `GENERATION_READY` and
`DELIVERY_ACCEPTED` independent. This document alone grants none of those claims.

For gameplay, run applicable parser/inference, source/atlas, exact-engine import/
analyzer, focused positive/negative/save/teardown and full trusted gates. Recheck
authority and impact coverage before commit/push. Report implemented behavior,
machine evidence and visual/device/child/owner acceptance separately in the
[animation branch](../../audit/animation/README.md) and task impact record.
