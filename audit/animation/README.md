# Character animation — master audit branch

Owner commission: 2026-09-09 initial direction request, expanded and integrated
2026-09-11. Status: `SUPPORTING_CURRENT` production coverage register under
the [master audit](../MASTER_AUDIT_2026-08-09.md#development-task-index).
This branch organizes animation work by character, beginning with Roshan.
It does not create findings, close existing ones, or declare game-wide satisfaction.

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

- 2026-09-11: created the character animation branch, Roshan's expanded
  movement language, reusable character template and production protocol;
  integrated canonical motion rules and art/chapter/cinematic navigation.
  No motion study, runtime change, new art or acceptance is claimed.
