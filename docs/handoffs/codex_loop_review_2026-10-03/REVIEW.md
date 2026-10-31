# Review of the self-improvement loop implementation (`4cb14feb`)

**Status:** `SUPPORTING_CURRENT` audit and repair record by Claude. Reviewed
commit: [`4cb14feb`](https://github.com/Ebonyks/mermaid-roshan-reef/commit/4cb14febc2c5f0074d5ad8386ce66f19f940c84d),
Codex's implementation of the
[self-improvement loop handoff](../codex_self_improvement_loop_2026-10-03/README.md)
(revision 1). Tracking findings:
[`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009),
[`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008),
[`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006).
The work left for Codex is in [README.md](README.md).

**Owner requests (2026-10-03):** *"audit, evaluate, and improve"* the commit,
then *"Refine and fix it."* The owner's explicit request in this task covers
fixing the loop's tooling and records; game code, probe captures and images
stay with Codex.

## 1. Verdict

**Before:** a strong, honest foundation that did not yet do what the owner
asked. The plumbing was real (study runner, strengths and decision registers,
lesson fields, fifteen recipes, roadmap, verification sweep, Godot resolver,
164 passing tests, green CI) and nothing claimed acceptance it did not have.
But the cycle report was a 2,100-word machine dump that never asked the owner
anything, nothing looked at the game itself, the roadmap was every open finding
with one template prompt, the job planner had the bakery answer built in, and
a mandatory test would have turned CI red on the next routine edit to
`AGENTS.md` or design 06.

**After this change:** the loop's outputs are usable. The report is a short
page with Claude's judgement, five ready-to-say prompts and numbered
questions; the roadmap separates what to fix, check, decide, wait on and park,
ranked by severity and recorded owner priority; the planner works for any job;
the study reads the game's shipping surfaces from CI; and the build no longer
breaks when a strength's source file changes. The loop has still not turned
with the owner (no answers yet), and several CI captures still fail for a
reason only Codex can repair.

## 2. Scorecard

### 2.1 Work packages

| Package | At `4cb14feb` | After this change |
|---|---|---|
| LP0 baseline | Done | Unchanged |
| LP1 cycle home | Done; history moved verbatim (all 25 dated paragraphs, links re-pointed) | Runbook rewritten; cycle files unignored instead of force-added |
| LP2 study runner | Built and tested, but false FAILs from echoed CI script text, a dirty-tree study, CI from before the fix, 2.6 MB per cycle, absolute local paths | Wrapper verdicts authoritative; committed heads only; workflow read from the studied commit; per-surface evidence; compact output; relative commands |
| LP3 strengths | 15 entries, hash-bound; a changed source failed the build | Drift reported for re-review; structure still gated |
| LP4 lessons | Fields validated; lessons target never measured | Measured from the LP4 boundary by default |
| LP5 decisions | Register and intake; not enforced append-only; the owner's job-takeover priority missing | Append-only check in a CI-run test; priority entered from its two sources |
| LP6 roadmap | All 61 findings, one prompt, severity ignored | Lanes by lifecycle, severity and owner priority; prompts route to recipes |
| LP7 prompts | 15 recipes; bakery answer stored; reserved decisions proceeded; image rule softened | Generic planner, recipes rendered from the catalogue, reserved decisions wait, image rule restated |
| LP8 sweep | Lists all 12; owner and device pages copied stale developer steps | Plain owner checklist and a 30-minute phone script |
| LP9 master audit | Generated history, re-audit each cycle, counted rule earning, surfaces listed | Surfaces carry probes, captures and findings |
| LP10 health | Targets reported; some failed open | Fail closed; human-readable values |
| LP11 cadence | Manual; no schedule | Unchanged (owner-gated) |

### 2.2 Acceptance criteria of the handoff

| AC | At `4cb14feb` | Now | Still needed |
|---|---|---|---|
| AC-1 two complete cycles | Not met | Not met; cycle `2026-10-03b` asks the first questions | Owner answers, a built prompt, its check and lesson, then a second cycle |
| AC-2 numbers from `study.json` | Met for numbers; prompts and questions were fixed text | Met; judgement comes from Claude's validated `judgement.json` | — |
| AC-3 strengths with evidence, bound by recipes | Met | Met | Owner or child evidence to promote candidates |
| AC-4 lessons in half the records | Not measurable | Measured from the LP4 boundary | More change records |
| AC-5 roadmap with prompts and recipes | Formally met; prompts wrong for 17 findings | Met; each item routes to its recipe or names its reason | — |
| AC-6 cold-start bakery test | Passed by construction | Planner generic; unseen-job tests | A fresh-agent cold start on an unseen job, transcript kept |
| AC-7 sweep lists missing evidence; first session scheduled | Half | Half; plain pages ready | The owner's time slot |
| AC-8 generated history, current scorecards, per-cycle re-audit | Partly | Surfaces now carry machine evidence | Human scores stay unassessed |
| AC-9 three measures improve between cycles | Not yet | Not yet | Two real cycles |
| AC-10 `MA-DOC-009` acceptance | Not yet | Not yet | All of the above and owner review |

## 3. What was done well (keep)

- Honesty: no owner answer, session, cycle or acceptance is claimed without
  evidence; defaults are labelled; `MA-DOC-009` and `MA-CI-008` moved only to
  `IN_PROGRESS`.
- History: every moved planning and repair-order paragraph is preserved
  verbatim with links re-pointed; finding histories are appended, not rewritten.
- The advisory wrapper makes failures visible that `grep … || true` hid, and
  rejects old screenshots as evidence for a new run.
- Save allocation reads live code (mask `0x3BDEF`, 15 live jobs, retired bits
  4, 9 and 14, four clamps of 262143).
- The engine baseline is right: Godot 4.7.2-stable, released 18 August 2026,
  is the latest stable on the official download page (checked 2026-10-03).
- 164 tests, green CI on branch and `dev`, no new Actions, no secrets, no
  schedule.

## 4. Findings and what this change did

| ID | Severity | Finding | Evidence | Status |
|---|---|---|---|---|
| LR-01 | High | A mandatory CI test failed whenever any of 22 live evidence files changed (`AGENTS.md`, design 06, `storybook_ui.gd`, …), blocking `dev` merges and APKs | `tools/tests/test_build_study_roadmap.py`, `validate_strengths` | Fixed: structure gated, drift reported as a re-review item |
| LR-02 | High | Four advisory steps whose wrapper said MEASURED were reported FAIL, because echoed script lines contain "timeout" and a benign audio warning contains "failed" | Run `37161828730` log; `study_game.py` `BAD_RE` | Fixed: the wrapper's verdict is authoritative; echoes and the warning are ignored |
| LR-03 | High | The cycle report was 168 lines and 2,102 words with raw log lines, JSON, 16-digit fractions, no strengths, two fixed prompts and no questions | `audit/cycles/2026-10-03/STUDY_REPORT.md` | Fixed: owner page with Claude's judgement file and generated candidates; tests cap length and forbid raw machine text |
| LR-04 | High | The planner stored the bakery answer; "add a pizza job" returned bakery steps and no job card | `plan_prompt.py` (old line 170); `prompt_intents.json` step 1 | Fixed: generic job card, derived numbers, no-leak tests on unseen jobs |
| LR-05 | High | The roadmap listed all 61 findings with one prompt and ignored severity; 17 cannot be fixed by a source change | `audit/ROADMAP.md`; `build_study_roadmap.py` sort key | Fixed: lifecycle lanes, severity, owner priority, specific prompts |
| LR-06 | Medium | The owner's 2026-09-30 priority (job takeover first) was moved to history without a register entry; the roadmap ranked it 24th | `REPAIR_ORDER_HISTORY.md` line 7 | Fixed: `ODR-PRIORITY-JOB-TAKEOVER`; it now heads the Strengthen lane |
| LR-07 | Medium | The committed cycle studied `30d82725` plus uncommitted changes with CI from before the sensor repair, and read workflow step names from the working tree | Report header; `advisory_step_names` | Fixed: committed heads only; workflow read at the studied commit |
| LR-08 | Medium | Pending CI entries were matched only against the 50 newest runs: 2 of 38 resolved though about 26 had a finished run at their head | `gh api …/runs?head_sha=` per record | Fixed: per-head lookup with states |
| LR-09 | Medium | `study.json` was 2.6 MB per cycle: impact records stored twice (1.6 MB) and raw sensor output (0.6 MB) | `study.json` sections | Fixed: compact records, output tails, branch list capped |
| LR-10 | Medium | Day Two library hashes depended on line endings: 52 "changed" sources on Windows, 12 by content | `library_delta` | Fixed: text hashed as committed |
| LR-11 | Medium | Owner and device pages told a parent to install an older APK, run probes under Godot 4.7.1 and check "Gaussian blur"; the device page duplicated the sweep | `OWNER_REVIEW.md`, `DEVICE_SESSION.md` | Fixed: plain checks in `design/reference/verification_checks.json` |
| LR-12 | Medium | All 15 recipes said "existing session authorization takes precedence over generic role defaults", softening the no-images rule; boards were not assigned to Codex | Recipes | Fixed: the CLAUDE.md wording, Codex builds boards and captures |
| LR-13 | Medium | Reserved owner decisions defaulted to proceeding (DL-PLAN-01 says silence grants nothing); three touchpoints were not questions | Recipes | Fixed: defaults wait; the catalogue rejects non-questions |
| LR-14 | Medium | The job recipe treated the contest-only restart as settled and left out the 2-second win beat, no idle win and the slowdown | `DL-INT-14` | Fixed |
| LR-15 | Medium | The voice recipe did not name Parler or rule out Kokoro for new lines | `VOICE_MANIFEST.md` | Fixed |
| LR-16 | Medium | The decision register's "immutable" rule was not enforced: rewriting or deleting a decision still validated | `record_owner_decision.py` | Fixed: append-only check against the comparison base, run by a CI test |
| LR-17 | Low | Health targets reported on-target when no findings parsed; the lessons target could never be measured | `health_targets` | Fixed |
| LR-18 | Low | A retired advisory step raised a red error on every green run; a verdict printed before an engine hang counted as capped | `run_advisory_sensor.py` | Fixed |
| LR-19 | Low | `run_godot.ps1` dropped `-d` and `-v` and crashed on `-e`; `ci.sh` did not export `GODOT`; the build line in `CLAUDE.md` and `AGENTS.md` still said "or godot on PATH" | Stub test in PowerShell 5.1 | Fixed |
| LR-20 | Low | The motion-study list included Chapter 2 and hall-art records | `motion_studies` | Fixed: records citing `DL-MOT-13`, or a `DL-MOT-*` rule with motion wording |
| LR-21 | Low | Cycle files were tracked only by force-add; `.gitignore` excludes `audit/*` | `.gitignore` line 27 | Fixed: `audit/cycles/` and `audit/ROADMAP.md` unignored |
| LR-22 | Low | Mojibake "Q12â€“Q16"; `study.json` carried absolute local paths in a public repository; git output capped at 200 KB | `IMPLEMENTATION.md`; sensor commands | Fixed; one older mojibake remains in a cinematics README (README.md, CR5) |
| LR-23 | High if confirmed | Chef's first step may never finish: the poured amount sums to 4.999… against a goal of 5.0 once the bowl is full | Python model of `opera_gesture_surface.gd`; all three Chef personas stop at `progress=5.000000` | For Codex (README.md, CR1); the phone session checks it too |
| LR-24 | Medium | Sky Lagoon and Castle captures fail on every CI run because the runner falls back to OpenGL while the probes require Mobile; the dust-boss arena capture is incomplete | Run `37161828730` | For Codex (CR2) |
| LR-25 | Medium | Opera pacing measures 12 of 45 runs (4 of 15 careers); 10 modes unsupported; a cancelled act counts as finished | `BALANCE\|RESULT\|CAPPED\|measured=12` | For Codex (CR3) |
| LR-26 | Low | The dust-boss fun band is described as dropped, not checked; the controls run repeats work; captures hard-code engine patch 2; the legacy diagnostic still saves Reef shots | `probes.yml`, probes | For Codex (CR4) |
| LR-27 | Low | Roshan decisions list a dummy test as their check; Q12 drops "no rule is enforced" | `owner_decisions.json` | Append correction entries (CR5); records are immutable |
| LR-28 | High | The owner reported on 2026-10-03: "Chef pours backwards still" and "Chef still looks bad, lots of overdraw". The jug art faces left while the code tilts it clockwise and pours from its right side; every Chef step stacks a dark bloom and flat code-drawn duplicates of the painted bowl, oven and cake | `widget_pour_chef_mover.png` (spout at x=22 of 256); `_pour_spout_point`, `_draw_activity_focus`, `_draw_chef_crank`, `_draw_oven`, `_draw_trace_chef_subject` | `MA-OPERA-001` reopened; `ODR-CHEF-VERDICT-20261003`; Codex package CR0 |

The committed `2026-10-03` report and roadmap stay as the historical record of
the infrastructure study; the first reproducible cycle is `2026-10-03b`.

## 5. The owner's four asks

| The owner asked for a loop that… | At `4cb14feb` | Now |
|---|---|---|
| studies the game | Measured documents and CI receipts; surfaces listed as "source present" | Each shipping surface shows its trusted probes at the head, review captures, open findings and recent change; playing quality still needs people |
| keeps the game's positive qualities as references | A register, but the report showed none | Accepted strengths and re-review items appear in every report; Claude names the ones that matter |
| finds new weaknesses | Real, but buried and partly false | Advisory gaps, stale findings, findings whose files changed and unverified fixes, plainly listed |
| gives a roadmap for nuanced content from simple prompts | Bakery-only planner; one template prompt per finding | A planner for any job, recipes that cannot drift from the catalogue, a roadmap whose every line can be said as written |

## 6. Method and limits

Read-only reviews of the tools, the CI and probes, and the generated content;
the full gates and 164 tests at `4cb14feb`; a read-only rerun of the study at
`4cb14feb` (numbers in [data/study_rerun_4cb14feb_summary.json](data/study_rerun_4cb14feb_summary.json));
the logs and artifact lists of Probe Suite runs `37161828730`, `37159346388` and
`37100729058`; and the official Godot download page. No Godot run, capture or
image was made. The Chef stall (LR-23) rests on a Python model of the pour code
and on the balance probe's log; it is unverified in Godot. No device, child or
owner evidence is claimed.
