# Study cycles

Use this entry when the owner says "study the game". The loop runs after each development batch integrates into dev, at least monthly, and on request. Two manual owner-answer/build/check/learn cycles precede any proposal for scheduled automation. No schedule or child-device telemetry is created by these tools.

## Run a cycle

Study a **committed** head. The runner refuses uncommitted changes outside the cycle folder, so every number can be reproduced from git; `--allow-dirty` exists only for scratch studies written outside `audit/cycles/`, and their report says "NOT REPRODUCIBLE". Wait until the exact-head Probe Suite run has finished, or the advisory checks are reported as not measured. A cycle ID is the date, with a letter suffix for a second cycle on the same day (for example `2026-10-03b`).

```text
python -B tools/study_game.py --cycle CYCLE --as-of YYYY-MM-DD --previous audit/cycles/PREVIOUS/study.json --timeout 300
python -B tools/build_study_roadmap.py --study audit/cycles/CYCLE/study.json --output audit/ROADMAP.md --cycle-dir audit/cycles/CYCLE
python -B tools/study_game.py --render audit/cycles/CYCLE/study.json --refresh-roadmap
```

Then **Claude writes the judgement**: `audit/cycles/CYCLE/judgement.json` (schema `cycle_judgement/1`) holds a short summary, the strengths and weaknesses that matter this cycle, up to five ready-to-say prompts (each must route to its recipe through `tools/plan_prompt.py`) and up to five numbered owner questions with defaults. Render once more so the report picks it up:

```text
python -B tools/study_game.py --render audit/cycles/CYCLE/study.json
```

The report keeps numbers from `study.json` and judgement from `judgement.json`; without a judgement it shows generated candidates, labelled as such. `study.json` keeps verdicts, summaries, hashes and short output tails; the full sensor output is reproducible from the recorded commands at the studied head. Commit the cycle with an impact record and ledger rows, publish it to the established GitHub repository, verify the exact remote revision and report one cycle entry link. Update the index below when a cycle is added.

What the runner reads: four read-only sensors, the exact-head CI run (each advisory step's own `ADVISORY|…|RESULT|…` verdict; echoed script lines are ignored), trusted-probe results, the workflow as committed at the studied head, finding records, change records, the strengths register, the decision register, the Day Two library hashes (text compared as committed) and the shipping surfaces. It never writes images and never changes a finding, rule or record.

## Plan a prompt

```text
python -B tools/plan_prompt.py "add a vet job"
python -B tools/plan_prompt.py --check
```

Recipes in `design/reference/recipes/` are rendered from `design/reference/prompt_intents.json`; edit the catalogue, then run `python -B tools/plan_prompt.py --render-recipes`. A prompt that matches no single recipe returns the closest recipes and their example phrasings; that gap is a lesson for the next study.

## Decisions and verification

For decision intake, save a JSON array of actual answers containing `id`, `date`, `subject`, `decision`, `source`, `authority: recorded_owner`, `question` and `checks` (file paths). Then run:

```text
python -B tools/record_owner_decision.py --answers PATH --cycle CYCLE --answered-on YYYY-MM-DD
python -B tools/record_owner_decision.py --check --base origin/dev
```

The supplied date is the actual owner session date. The register is append-only: `--check --base` and the register test reject any changed, removed or reordered decision, so corrections append a new ID. Operating defaults cannot enter as owner answers. Each checkable correction must name an implemented executable check in `checks` and set `checkable: true`; artistic judgements retain exact human-review requirements. A decision may carry `applies_to` finding IDs with `priority: first`; the roadmap then puts those findings first in their lane. Intake appends to the decision register and that cycle's owner_answers.json in the same invocation. Do not collect identifying child media.

The verification sweep groups missing evidence into one owner page and one device session. Their plain-language steps come from `design/reference/verification_checks.json`, which Claude writes from each finding's acceptance criterion; the technical sweep keeps the canonical wording. A proposed time is an advisory target, not a booked session; record a confirmed time before claiming that a session is scheduled, and move finding lifecycles only with the required evidence.

## Cycle index

| Cycle | State | Evidence |
|---|---|---|
| [2026-10-03b](2026-10-03b/STUDY_REPORT.md) | First reproducible cycle, at the repair head; Claude's judgement written; awaiting the owner's answers | [Roadmap](2026-10-03b/ROADMAP.md), [owner page](2026-10-03b/OWNER_REVIEW.md), [phone session](2026-10-03b/DEVICE_SESSION.md), [surfaces](2026-10-03b/CURRENT_SURFACES.md) |
| [2026-10-03](2026-10-03/STUDY_REPORT.md) | Infrastructure study at `30d82725` plus uncommitted implementation changes, with CI from before the sensor repair; reviewed in the [loop review](../../docs/handoffs/codex_loop_review_2026-10-03/REVIEW.md) | [Roadmap](2026-10-03/ROADMAP.md), [verification sweep](2026-10-03/VERIFICATION_SWEEP.md), [implementation evidence](2026-10-03/IMPLEMENTATION.md) |
| 2026-10-03 baseline | Intake measurement; historical handoff cycle zero; one historic owner priority entered on 2026-10-03 | [Loop health](2026-10-03-baseline/loop_health.json), [preserved planning updates](2026-10-03-baseline/PLANNING_HISTORY.md), [historical repair order](2026-10-03-baseline/REPAIR_ORDER_HISTORY.md), [owner answers](2026-10-03-baseline/owner_answers.json) |

Each operational cycle also records actual owner answers (at most five per session), built impact IDs, exact check evidence and lessons with write-back targets. Rerunning a measurement does not complete a development cycle. Keep AC-1, AC-7, AC-9 and AC-10 of the [handoff](../../docs/handoffs/codex_self_improvement_loop_2026-10-03/README.md#5-acceptance-criteria) open until their real evidence exists.
