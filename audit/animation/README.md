# Character animation — master audit branch

Owner commission: 2026-09-09 initial direction request, expanded and integrated
2026-09-11. Status: `SUPPORTING_CURRENT` production coverage register under
the [master audit](../MASTER_AUDIT_2026-08-09.md#development-task-index).
This branch organizes animation work by character, beginning with Roshan.
It does not create findings, close existing ones, or declare game-wide satisfaction.

<!-- ROSHAN_LEFT_RIGHT_20260916_START -->
## Current Roshan directional scope

Owner decision 2026-09-16: **left/right gameplay animation only**. Author one
right-facing family and mirror the complete sprite for left; do not commission
four-way/eight-way or front/rear animation sets. The
[movement profile](../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md#gameplay-facing--leftright-only)
defines screen-side asymmetry permission, stable pivots, reflected contact
anchors and two-facing review. Existing art stays preserved. This is a direction
change, not a new visual pass or a runtime flip implementation.
[Impact](../../design/audit_impacts/2026-09-16-roshan-left-right.json).

<!-- ROSHAN_LEFT_RIGHT_20260916_END -->

<!-- ROSHAN_TWO_SPEED_20260916_START -->
## Current Roshan swimming source commission

The owner now requests separate **slow relaxed swim** and **dash** performances.
Use [movement profile v1.3](../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md#two-swim-speeds-and-performance-led-openings)
and the [current Grok handoff](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/START_HERE.txt).
Suitable actual Grok frames seed new takes; the old opening/rest pose is not a
lock. The two modes are separately performed, not playback-speed variants.
Rest-to-motion bridges are deferred separate work if needed. Source, loop,
mode-distinction and human review remain open; no new animation is accepted.
[Impact](../../design/audit_impacts/2026-09-16-roshan-two-speed-handoff.json).
<!-- ROSHAN_TWO_SPEED_20260916_END -->

The owner approves A001's motion direction but rejects ten-second gameplay
pacing. The [short-action direction](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/EXCHANGE_07.txt)
and [A001 review / A002 handoff](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/reshoots/reviews/PAIR-A001-20260916/START_HERE.txt)
require quick starts, repeatable cruise and short stops demonstrated on 1s/2s
travel, including interruption. Source crop, actual loop and phase-exit tests
remain open; source-film length must not lock movement duration.
[Impact](../../design/audit_impacts/2026-09-16-roshan-pair-a001-source-review.json).

Compact originals now exist: slow A002 take-02 and dash A003 take-03 (dash A002
preserved as cropped history). The [Codex review handoff](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/reshoots/reviews/PAIR-COMPACT-20260917/START_HERE.txt)
and [EXCHANGE_08](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/EXCHANGE_08.txt)
ask independent source review. Producer notes are not scores; no clip, runtime
or delivery is accepted.
[Impact](../../design/audit_impacts/2026-09-17-roshan-compact-codex-handoff.json).

Owner then asked for more horizontal in-plane fin motion for 2D sprite
conversion (no extra effects). Current pair: slow A003 take-03 and dash A004
take-04. Direction: [EXCHANGE_09](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/EXCHANGE_09.txt).
Prior compact takes remain history. Conversion is still later; these are source
candidates only.
[Impact](../../design/audit_impacts/2026-09-17-roshan-inplane-fin-return.json).

The [independent A003/A004 review and next requests](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/reshoots/reviews/PAIR-INPLANE-20260917/START_HERE.txt)
reject the dash opening's ghosted second tail (also present in its input seed).
Ordered-frame evidence does not establish the two compact cadences or a clean
whole-body loop; no full temporal score is claimed. The next bounded method
isolates core-loop production: slow A004 and dash A005 use screened native
inputs, with separate entry/phase-aware exit work still required afterward.
Owner renewed Codex Git checks every 15 minutes; no Grok timer is changed.
[Impact](../../design/audit_impacts/2026-09-17-roshan-inplane-source-review.json).

Grok returned the two core-loop originals: slow A004 take-04 and dash A005
take-05, using the Codex-screened IMAGE_1 files. Ghosted dash seed was not
reused. Producer cadence measurements are inspection notes, not a 4.8 score
or loop acceptance. Independent Codex review is next.
[Impact](../../design/audit_impacts/2026-09-17-roshan-core-loop-return.json).

The [independent first core-loop review and second trial](../../assets_src/cinematics/roshan_swim_flow_revision_2026-09-15/reshoots/reviews/PAIR-CORE-01-20260917/START_HERE.txt)
preserve improved single-tail anatomy and acting. Short coordinated whole-body
cycles and seams remain unproven; dash adds forbidden hand-water ribbons and
droplets. Slow A005 and dash A006 reuse the same clean native seeds with
phase-defined short strokes and no visible water. This is trial 2 of the same
core-only method: another failure requires reassessment before further renders.
No full temporal score, source pass or Aseprite conversion is claimed.
[Impact](../../design/audit_impacts/2026-09-17-roshan-core-first-review.json).

Grok returned the second-trial originals: slow A005 take-05 and dash A006
take-06, reusing the same clean IMAGE_1 files. Producer cadence still misses
the ~1s/~0.5s pilots; sampled dash frames did not show the prior hand-water
ribbons. No third take is authorized. Independent Codex review / method
reassessment is next.
[Impact](../../design/audit_impacts/2026-09-19-roshan-core-second-return.json).

## Start an animation task here

1. Read the [canonical motion rules](../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md#9-motion-acting-feedback-and-rewards)
   and the character's individual movement profile.
2. Use the [production protocol](../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md)
   to bind intention, approved sources, timing, contact, event ownership and
   evidence. Use the [profile template](../../design/templates/CHARACTER_MOVEMENT_PROFILE_V1.md)
   for a character not yet covered; verify its canon and roster authority first.
3. Inspect existing art and callers before commissioning missing poses or
   changing playback. Register the exact scoped action and acceptance gaps.
4. Implement and review only the commissioned work. Update this coverage row
   and its evidence when their facts change, with an audit-impact record.

## Character coverage

| Character | Direction document | Working direction | Authored candidates for this profile | Runtime/machine evidence for this profile | Visual/device/child/owner acceptance |
|---|---|---|---|---|---|
| Mermaid Roshan | [Movement language v1](../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md) | Ribbon Glide everyday; Playful Dolphin for delight. Pilot selection remains open. | Not produced by this documentation task; existing atlas inventory is linked in the profile | Not implemented or tested as a new movement suite; existing scoped game evidence is not transferred | All remain open for the proposed suite |

This table is a **profile commission inventory**, not a claim that only one
character exists or that the game has no prior animation. Add each next
commissioned character as an individual row, with verified source/canon links.
Do not infer personalities from filenames or copy Roshan's rhythm to fill a
blank. Career costumes remain Roshan and inherit her profile; record their
specific actions and special pose constraints as extensions. Distinct actors
receive distinct identity/profile IDs even when they share a species or room.

## Roshan work queue

| Order | Bounded deliverable | Question it resolves | Required next evidence |
|---|---|---|---|
| 1 | Asset-to-action coverage review | Which existing chronological frames support the new phrasing? | Exact paths/cells, source hashes, directions, anchors, keep/gap rationale; no speculative regeneration |
| 2 | Matched ten-second A/B studies | Does the gentle glide or eager pulse best express her? | Same scene/scale/route/camera; exact candidates, normal-speed review, recorded selection and remaining owner review |
| 3 | One real work/contact study and carry turn | Is she still recognizable while actually helping? | Before/contact/after, prop ownership, support and interruption evidence |
| 4 | Bounded gameplay integration | Does the chosen performance preserve agency and saved truth? | Valid input, arrival/contact, cancellation, passive negative, pause/re-entry and required local/CI gates |
| 5 | In-context acceptance | Does it read on the child's device? | Exact build, Mobile/Speedy captures, target-device frame timing, child comprehension and owner review |

This is a proposed production sequence, not a new runtime commission. The
current task delivers documentation and routing. Missing dependent evidence
blocks the dependent claim, not independent drafting or source inspection.

## Evidence record for each character/action

Record character/profile version, action ID, source revision, artifact paths
and hashes, register, environment/support, directional coverage, contact and
effect markers, validation command/log, reviewer/date, decision and remaining
gaps. Keep rejected candidates and specific correction reasons. Profile or
source changes require reviewing affected descendants; unrelated acceptance
does not transfer or reset automatically.

Report these claims separately:

| Claim | Evidence that supports it | What it does not prove |
|---|---|---|
| Direction documented | Profile plus source/authority review | Approved visual performance |
| Candidate selected | Exact comparison clips and recorded selection | Final acceptance or implemented behavior |
| Authored art reviewed | Identity/anatomy/contact/temporal review of exact sources | Correct engine sampling or device behavior |
| Runtime machine verified | Exact code/assets, relevant probes and required gates | Child comprehension or owner preference |
| In-context visual reviewed | Exact build/settings and normal-speed/captured review | Actual target-device performance |
| Device/child/owner accepted | Each named reviewer/session/build and outcome | Whole-game master-audit satisfaction |

External cinematic `ARCHIVE_COMPLETE`, `GENERATION_READY`, and
`DELIVERY_ACCEPTED` are additional independent claims governed by the existing
cinematic contract. An animation profile or motion-reference movie supplies
none of them by itself. No new lifecycle taxonomy replaces the master findings.

## Existing findings and authority

- [MA-PLAY-004](../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004): Roshan
  travels and visibly works at each real target. This profile supports future
  repairs but does not close the remaining job cases.
- [MA-VIS-006](../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-006): current
  runtime visual acceptance remains scoped to its actual evidence.
- [MA-PERF-001](../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-001): device
  measurements remain necessary; fluid-looking desktop playback is insufficient.

Rule coverage: `DL-MOT-01` through `DL-MOT-13`, with applicable touch, child,
contact, medium, cinematic, save and performance rules. Canonical finding
lifecycles/history remain unchanged because this commission defines direction
and production protocol rather than repairing or verifying runtime defects.

Change/evidence: [2026-09-11 audit impact](../../design/audit_impacts/2026-09-11-roshan-animation-language.json).

## Branch history

- 2026-09-13: [video-first handoff revision](../../assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/README.md#video-first-revision--2026-09-13) requires actual image-to-video capability and attached source inputs, one returned/reviewed RSW-01 video before the larger batch, and no still-board substitute. Publication now has a committed hash-bound envelope, separate from opening approval and video acceptance. [Impact](../../design/audit_impacts/2026-09-13-roshan-grok-video-first.json). No art pixels changed, no videos generated, no finding closed.
- 2026-09-12: owner requests [eight Grok swimming-performance auditions](../../assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/README.md), allowing selection or compatible beat combinations. The local swim-scull-v6 prototype is rated 3.5/5 by the owner, superseding earlier agent 4.5 motion scores; static source-art approval does not accept that performance. Two new opening compositions remain pending exact human approval. [Scope and evidence](../../design/audit_impacts/2026-09-12-roshan-grok-auditions.json); no live findings closed or runtime changed.
- 2026-09-11: created the character animation branch, Roshan's expanded
  movement language, reusable character template and production protocol;
  integrated canonical motion rules and art/chapter/cinematic navigation.
  No motion study, runtime change, new art or acceptance is claimed.
