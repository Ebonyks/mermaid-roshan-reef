# Game study — 2026-10-03b

`SUPPORTING_CURRENT`. Numbers come from [study.json](study.json); the judgement in sections 2, 3, 6 and 7 is written by Claude in [judgement.json](judgement.json). Machine evidence is not owner, device or child acceptance.

All 81 trusted probes ran clean at this head, and the advisory checks are read correctly for the first time. The problem you can see right now is Chef: it pours backwards and piles flat shapes over the painted kitchen. Your report reopened it after this study ran, and it now tops the roadmap. The loop finishes its first turn when you answer the five questions below.

## 0. Cycle header

- Studied head `e9915f44` (clean), as of 2026-10-03. Previous cycle: 2026-10-03; 4 commits since.
- CI: run [37170079511](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/37170079511) — completed, success. Advisory checks: 11 measured, 3 failed, 1 capped, 1 retired.
- Trusted probes at this head: 81 ran; 0 reported failures; 0 hung after their verdict and were accepted.

## 1. What changed since the last cycle

- `self-improvement-loop-implementation-20261003` — Implement LP0-LP10 of the commissioned feedback-loop handoff: measured study cycles, evidence-backed candidate strengths, owner-decision intake, validated lessons, prompt recipes…
- `self-improvement-loop-review-20261003` — Owner request 2026-10-03: "audit, evaluate, and improve" commit 4cb14feb (Codex's implementation of the self-improvement loop handoff), then "Refine and fix it." Review and…

## 2. Strengths

- **S-01** — Nothing is lost and nothing is won by doing nothing: probe_passive and the other 80 trusted probes ran clean at this head.
- **S-02** — Touching the world changes it where the child touches: the Day One bathroom dirt now clears along the scrub path (2 October).
- **S-07** — The family's own voices stay untouched; new lines must use the separate synthetic Parler voices.
- **S-10** — This cycle turned five lessons into checks the next change cannot skip, including the one behind the false CI failures.

## 3. Weaknesses

- **Chef pours backwards and looks cluttered** — The jug picture faces left but the code tips it to the right, so it pours from the handle; every step also piles a dark oval and flat shapes on top of the painted bowl, oven and cake. Reopened as MA-OPERA-001; Codex package CR0 has the exact fix.
- **Chef's pour may also never finish** — Codex checks it with the same fix (CR1); the phone session asks you to look too.
- **Review screenshots fail on the CI computer** — The Sky Lagoon, castle and dust-boss arena captures fail because that computer cannot draw with the phone's renderer (CR2); fixing it changes the CI workflow, so it needs your yes.
- **Opera pacing is measured for 4 of 15 jobs** — Codex adds simulated play for the other ten kinds of activity (CR3).
- **Fixes still wait for a phone check** — DEVICE_SESSION.md batches them into one 30-minute session; Chef left that list when your report reopened it.
- Advisory check Opera balance playtest (advisory): capped — opera-balance: at least one simulated run reached its cap.
- Advisory check Capture Sky Lagoon visual review: fail — sky-lagoon-review: process exit 1 or explicit failure.
- Advisory check Capture dust-boss arena review: fail — dust-boss-review: process exit 1 or explicit failure.
- Advisory check Capture pearl-castle visual review: fail — castle-review: process exit 1 or explicit failure.
- 9 findings need a recheck because files they name changed since their last entry: MA-VIS-002, MA-ACCESS-003, MA-CI-004, MA-CODE-003, MA-PERF-002, MA-PERF-003, MA-SAVE-001, MA-AUDIO-002, MA-TYPE-004.
- 37 of 61 (61%) open findings have had no history entry for 30 days.
- 12 fixes wait for a phone, owner or child check (6 for more than 30 days); see [DEVICE_SESSION.md](DEVICE_SESSION.md).
- 8 motion studies are recorded; owner verdicts exist for 1 of them.
- Day Two library: 12 watched sources changed since their review.

## 4. Loop health

| Measure | Now | Target | Status |
|---|---|---|---|
| Open findings without an entry for 30 days | 37 of 61 (61%) | <=0.10 | needs attention |
| Fixes unverified for more than 30 days | 6 | 0 | needs attention |
| Change records with a lesson (since lesson fields began) | 2 of 2 (100%) | >=0.50 | on target |
| Owner corrections repeated | not measured | 0 | not measured |
| Roadmap regenerated this cycle | yes | regenerated this cycle | on target |
| Handoffs waiting more than two cycles | not measured | all listed | not measured |

Change records: 80. Validation entries still PENDING: 40, of which 25 have a finished CI run at their record's head (25 success) and are proposed for a record update in a later change; 4 only cancelled, 2 no run, 0 not looked up, 1 not resolved, 8 not CI checks. FAIL entries kept: 36.

## 5. Roadmap

Findings by lane: Repair 26 · Verify 11 · Decide 2 · Waiting 7 · Parked 1 · Strengthen 14. Full plan: [ROADMAP.md](ROADMAP.md).
- Strengthen: "Fix MA-DOC-006: No current step-by-step script exists for building a new job game" (owner priority)
- Strengthen: "Fix MA-CI-004: Day One and start-menu probes are now gated"
- Repair: "Fix MA-OPERA-001: Chef pours backwards and its steps stack flat code-drawn shapes over the painted kitchen"
- Repair: "Fix MA-PLAY-003: Logical travel geometry and arrival gating are not independently proven across the live…"

## 6. Next prompts

1. "Fix MA-OPERA-001: Chef pours backwards and its steps stack flat code-drawn shapes over the painted kitchen" — `INT-REPAIR`; your report today; top of the Repair lane; Codex package CR0; medium.
2. "Fix MA-DOC-006: No current step-by-step script exists for building a new job game" — `INT-REPAIR`; your recorded priority: job-game takeover comes first; large.
3. "Fix the CI review screenshots" — `INT-REPAIR`; three captures fail on every run (CR2); needs your yes for the workflow change; small.
4. "a rainy-day activity in the castle" — `INT-ROOM-ACTIVITY`; new content through the generic planner; you approve the premise first; medium.
5. "Study the game" — `INT-STUDY`; the next cycle, after these fixes reach dev; small.

## 7. Questions for the owner

1. When could you do the 30-minute phone check in DEVICE_SESSION.md? Default: ask again next cycle; nothing is booked.
2. May Codex add a software graphics driver to the CI computer (a CI workflow change) so its screenshots use the phone's renderer? Default: yes.
3. The dark spotlight oval behind Chef's steps also sits behind other jobs' activity cards. Remove it everywhere, not just in Chef? Default: remove it in Chef first and show you before changing other jobs.
4. Which new content should grow first: a job, a castle room activity, a new stuffie friend or a seasonal event? Default: a castle room activity.
5. Farmer and Doctor take place above water while the other jobs are underwater (MA-OPERA-007). Keep that difference? Default: yes, keep it; no art changes.

Answer in one line, for example "1. yes, 2. Saturday morning". Answers enter through `tools/record_owner_decision.py`; defaults are never recorded as answers.

## 8. Lessons

- A mandatory test that pins hashes of live documents turns routine edits into red builds; gate structure and report drift for re-review. → written back to `tools/build_study_roadmap.py` (self-improvement-loop-review-20261003).
- A cold-start test passes by construction when the tool stores the answer to its own test prompt; test on prompts the tool has never seen. → written back to `tools/tests/test_plan_prompt.py` (self-improvement-loop-review-20261003).
- CI logs echo each step's script; classify the step's own verdict line, never keywords anywhere in the log. → written back to `tools/study_game.py` (self-improvement-loop-review-20261003).
- Moving a dated owner priority into history without a register entry silently drops it from planning. → written back to `design/reference/owner_decisions.json` (self-improvement-loop-review-20261003).
- A generated machine draft is not the owner report; the judgement layer (strengths, prompts, questions) must be written for a parent. → written back to `audit/cycles/README.md` (self-improvement-loop-review-20261003).
- CI checks each push against the previous pushed SHA, so a follow-up commit must change the impact record inside that range; run audit_development.py --base <previous pushed SHA> before pushing, not only --base auto. → written back to `design/AUDIT_DEVELOPMENT_CONTRACT.md` (self-improvement-loop-review-20261003).
- Owner decisions recorded: 9; operating defaults: 8.

Details behind every number: [study.json](study.json).
