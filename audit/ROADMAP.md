# Improvement roadmap — 2026-10-03b

Status: `SUPPORTING_CURRENT / GENERATED_ADVISORY`. Studied head: `e9915f44b8d7cf9085213a57c61ee6b1e7756a16`. Generated from canonical findings, the decision register, strengths and the study; never changes rules, findings, save state or images.

Order inside each lane: recorded owner priority first, then severity (P0 to P3), then child-impact wording, then directed dependencies, then age since the last dated history entry. This is a planning aid, not an owner verdict or a quality score. Every "Say" line is ready to give to Claude or Codex as written.

## Repair — 28

Child-facing defects that a change to the game can fix.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| MA-OPERA-001 (P1) | Fix MA-OPERA-001: Chef pours backwards and its steps stack flat code-drawn shapes over the painted kitchen | `REC-REPAIR`: `design/reference/recipes/repair.md` | owner report ODR-CHEF-VERDICT-20261003 (2026-10-03); P1 CONFIRMED_OPEN; access/comprehension wording; 0 days since last entry |
| MA-PLAY-005 (P0) | Fix MA-PLAY-005: Chapter 2's story careers cannot start or progress in normal play: setup rejects an empty… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P0 CONFIRMED_OPEN; play/agency wording; 0 days since last entry |
| MA-PLAY-003 (P1) | Fix MA-PLAY-003: Logical travel geometry and arrival gating are not independently proven across the live… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; progress/safety wording; 21 days since last entry |
| MA-PLAY-001 (P1) | Fix MA-PLAY-001: No fresh-save child-visible route has proved entry, exit, and re-entry for every visible… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; progress/safety wording; 10 days since last entry |
| MA-OPERA-002 (P1) | Fix MA-OPERA-002: Detective's supposedly missing crown is still visibly painted into the scene source | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; access/comprehension wording; 51 days since last entry |
| MA-OPERA-004 (P1) | Fix MA-OPERA-004: The Opera capture harness has not produced accepted evidence for every career, widget… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; access/comprehension wording; 51 days since last entry |
| MA-TYPE-003 (P1) | Fix MA-TYPE-003: Child-action and child-state copy has no enforced size/read-dependency role, with current… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; access/comprehension wording; 34 days since last entry |
| MA-TYPE-004 (P1) | Fix MA-TYPE-004: Critical navigation, category, habitat, care, career, lock, confirmation, progress, and… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; access/comprehension wording; 27 days since last entry |
| MA-OPERA-013 (P1) | Fix MA-OPERA-013: A second finger on the Astronaut pipe tray throws away the tile already being carried | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; access/comprehension wording; 0 days since last entry |
| MA-PLAY-004 (P1) | Finish MA-PLAY-004: Roshan must travel to and visibly perform every job instead of operating a detached tool… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 IN_PROGRESS; play/agency wording; 3 days since last entry |

Also open, in order (18 more): `MA-VIS-003`, `MA-TYPE-001`, `MA-2D-002`, `MA-TYPE-006`, `MA-VIS-006`, `MA-SAVE-001`, `MA-AUDIO-002`, `MA-TOUCH-002`, `MA-OPERA-003`, `MA-VIS-004`, `MA-PERF-003`, `MA-ASSET-001`, `MA-ASSET-004`, `MA-OPERA-006`, `MA-PERF-002`, `MA-TYPE-002`, `MA-TYPE-005`, `MA-ROSHAN-005`.

## Verify — 11

Fixed, waiting for a phone, owner or child check. Batched into the cycle folder's `OWNER_REVIEW.md` and `DEVICE_SESSION.md`.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| MA-TOUCH-001 (P1) | Check the fix for MA-TOUCH-001: Held travel and medallion input lacks recorded real-phone hold, drag, multitouch, and… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; progress/safety wording; 21 days since last entry |
| MA-OPERA-010 (P1) | Check the fix for MA-OPERA-010: Opera's unified Canvas lifecycle lacks authoritative Mobile, device, child, and owner… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; access/comprehension wording; 51 days since last entry |
| MA-RELEASE-001 (P1) | Check the fix for MA-RELEASE-001: The current integrated head is machine-green with a matching APK but lacks remote… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; access/comprehension wording; 51 days since last entry |
| MA-VIS-007 (P1) | Check the fix for MA-VIS-007: Interactive foreground sprites can duplicate baked background objects or expose blurred… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; access/comprehension wording; 35 days since last entry |
| MA-OPERA-009 (P1) | Check the fix for MA-OPERA-009: Boxer's five-phase Canvas implementation lacks two-aspect, target-device, child, and… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; access/comprehension wording; 3 days since last entry |
| MA-OPERA-011 (P1) | Check the fix for MA-OPERA-011: The retired Opera bosses and stable save tombstones lack authoritative visual, device… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; presentation/support wording; 51 days since last entry |
| MA-VIS-002 (P1) | Check the fix for MA-VIS-002: Sky Lagoon's true-Canvas repair has exact machine integration but still lacks… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; presentation/support wording; 51 days since last entry |
| MA-OPERA-012 (P1) | Check the fix for MA-OPERA-012: The thirteen Castle-room career routes pass current machine/build gates but still lack… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 FIXED_PENDING_VERIFICATION; presentation/support wording; 3 days since last entry |
| MA-COMBAT-001 (P2) | Check the fix for MA-COMBAT-001: Combat's repaired wave count, slash-band scale, and tutorial discoverability lack phone… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P2 FIXED_PENDING_VERIFICATION; access/comprehension wording; 51 days since last entry |
| MA-OPERA-005 (P2) | Check the fix for MA-OPERA-005: The current three-act mermaid Ballerina lacks accepted two-aspect, M11, child, and owner… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P2 FIXED_PENDING_VERIFICATION; access/comprehension wording; 3 days since last entry |
| MA-AUDIO-001 (P2) | Check the fix for MA-AUDIO-001: Complete runtime audio has measured delivery and bounded repairs but lacks required… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P2 FIXED_PENDING_VERIFICATION; play/agency wording; 3 days since last entry |

## Decide — 2

Waiting for an owner decision; each one is asked as a numbered question with a default.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| MA-PLAY-002 (P2) | Decide MA-PLAY-002: The standalone fire arena has no owner-approved truthful home or retirement for its… | Owner decision required (DL-PLAN-01); asked in the cycle report, never assumed | no recorded owner priority; P2 OWNER_DECISION_REQUIRED; play/agency wording; 51 days since last entry |
| MA-OPERA-007 (P2) | Decide MA-OPERA-007: Farmer and Doctor use above-water settings while other Opera careers use a different… | Owner decision required (DL-PLAN-01); asked in the cycle report, never assumed | no recorded owner priority; P2 OWNER_DECISION_REQUIRED; presentation/support wording; 51 days since last entry |

## Waiting — 7

Blocked by evidence or people outside the project.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| MA-ACCESS-002 (P1) | Unblock MA-ACCESS-002: Lamba's current semantic role still plays protected recordings that call the character a… | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; access/comprehension wording; 51 days since last entry |
| MA-CHILD-001 (P1) | Unblock MA-CHILD-001: No current observed five-minute child golden-path session proves comprehension and… | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; access/comprehension wording; 51 days since last entry |
| MA-PERF-001 (P1) | Unblock MA-PERF-001: No exact-release target-device matrix establishes frame time, hitches, memory, thermal… | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; access/comprehension wording; 51 days since last entry |
| MA-TYPE-007 (P1) | Unblock MA-TYPE-007: No current exact-APK M11/older-phone, accompanying-adult, child, or owner typography… | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; access/comprehension wording; 34 days since last entry |
| MA-ACCESS-003 (P1) | Unblock MA-ACCESS-003: Seek lacks an exact protected Evie recording that tells the child to tap the wiggly tree | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; presentation/support wording; 51 days since last entry |
| MA-DOC-003 (P1) | Unblock MA-DOC-003: The reported off-repository journal of 36 findings cannot be verified or reconciled from… | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; presentation/support wording; 51 days since last entry |
| MA-ACCESS-001 (P1) | Unblock MA-ACCESS-001: Some required objectives still lack an authorized exact spoken cue or an independently… | Waiting on evidence or people outside the project; a source change cannot close it | no recorded owner priority; P1 BLOCKED_EXTERNAL; presentation/support wording; 3 days since last entry |

## Parked — 1

Deferred with a recorded reason.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| MA-ROSHAN-003 (P2) | Leave MA-ROSHAN-003 parked: Roshan atlas repacking is optional optimization because current owned-pixel windows and… | Deferred with a recorded reason; reopen only when that reason changes | no recorded owner priority; P2 DEFERRED_WITH_REASON; play/agency wording; 51 days since last entry |

## Strengthen — 26

How the project is built, checked and studied: process findings, sensors, handoffs and references.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| MA-DOC-006 (P2) | Fix MA-DOC-006: No current step-by-step script exists for building a new job game | `REC-REPAIR`: `design/reference/recipes/repair.md` | owner priority ODR-PRIORITY-JOB-TAKEOVER (2026-09-30); P2 CONFIRMED_OPEN; access/comprehension wording; 0 days since last entry |
| ADVISORY-Opera balance playtest (advisory): Opera balance playtest (advisory): CAPPED — opera-balance: at least one simulated run reached its cap. | Fix the advisory check Opera balance playtest (advisory) | `REC-REPAIR`: `design/reference/recipes/repair.md` | Exact-head CI advisory result; CI success alone is insufficient. |
| ADVISORY-Capture Sky Lagoon visual review: Capture Sky Lagoon visual review: FAIL — sky-lagoon-review: process exit 1 or explicit failure. | Fix the advisory check Capture Sky Lagoon visual review | `REC-REPAIR`: `design/reference/recipes/repair.md` | Exact-head CI advisory result; CI success alone is insufficient. |
| ADVISORY-Capture dust-boss arena review: Capture dust-boss arena review: FAIL — dust-boss-review: process exit 1 or explicit failure. | Fix the advisory check Capture dust-boss arena review | `REC-REPAIR`: `design/reference/recipes/repair.md` | Exact-head CI advisory result; CI success alone is insufficient. |
| ADVISORY-Capture pearl-castle visual review: Capture pearl-castle visual review: FAIL — castle-review: process exit 1 or explicit failure. | Fix the advisory check Capture pearl-castle visual review | `REC-REPAIR`: `design/reference/recipes/repair.md` | Exact-head CI advisory result; CI success alone is insufficient. |
| SENSOR-game_2d: Sensor game_2d: MEASURED; measured summary UNSATISFIED. | Study the game_2d sensor gap | `REC-STUDY`: `design/reference/recipes/study.md` | Measured summary reports open work; no passing evidence claimed. |
| MA-CI-004 (P1) | Fix MA-CI-004: Day One and start-menu probes are now gated | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; play/agency wording; 3 days since last entry |
| MA-CI-005 (P1) | Fix MA-CI-005: Central passive snapshots cover Day One and Chapter Two | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P1 CONFIRMED_OPEN; presentation/support wording; 3 days since last entry |
| MA-CODE-001 (P2) | Fix MA-CODE-001: scripts/main.gd remains 9,153 lines at the 2026-09-30 dead-code cleanup candidate, far… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P2 CONFIRMED_OPEN; access/comprehension wording; 3 days since last entry |
| MA-CODE-002 (P2) | Fix MA-CODE-002: String-owned state, duplicated input, save frequency, material churn, and remaining 3D… | `REC-REPAIR`: `design/reference/recipes/repair.md` | no recorded owner priority; P2 CONFIRMED_OPEN; access/comprehension wording; 3 days since last entry |

Also open, in order (16 more): `MA-DOC-007`, `MA-DOC-009`, `MA-CI-003`, `MA-CI-006`, `MA-CI-007`, `MA-CODE-003`, `MA-CODE-004`, `MA-DOC-008`, `MA-CI-008`, `codex_job_platform_architecture_2026-09-30`, `codex_master_audit_refinement_2026-09-30`, `codex_reference_consolidation_2026-09-30`, `codex_roshan_art_repairs_2026-09-30`, `codex_visual_design_language_2026-09-30`, `LIBRARY-REFRESH`, `STRENGTH-REVIEW`.

## Grow — 4

New content. Choosing one still needs the owner's premise for anything permanent.

| Item | Say | Recipe or reason | Why here |
|---|---|---|---|
| GROW-ADD-JOB: A new job the owner names: the recipe plans the room, distinct verbs, voice, save and checks. | add a bakery job | `REC-ADD-JOB`: `design/reference/recipes/add_job.md` | ODR-LOOP-Q8 operating default: jobs and room activities first; strengths S-01, S-02, S-03, S-12, S-13; new permanent content still needs the owner's premise (DL-PLAN-01). |
| GROW-ROOM-ACTIVITY: Something to do inside an approved castle room, with a visible change that stays. | a rainy-day activity in the castle | `REC-ROOM-ACTIVITY`: `design/reference/recipes/room_activity.md` | ODR-LOOP-Q8 operating default: jobs and room activities first; strengths S-01, S-02, S-03, S-08; new permanent content still needs the owner's premise (DL-PLAN-01). |
| GROW-COMPANION: A friend who follows Roshan, built from an identity sheet and a movement profile. | add a new stuffie friend | `REC-COMPANION`: `design/reference/recipes/companion.md` | prompt catalogue; strengths S-06, S-14; new permanent content still needs the owner's premise (DL-PLAN-01). |
| GROW-EVENT: A time-limited event that reuses rooms and art and adds its own save key. | a birthday surprise | `REC-EVENT`: `design/reference/recipes/event.md` | prompt catalogue; strengths S-08, S-14; new permanent content still needs the owner's premise (DL-PLAN-01). |
