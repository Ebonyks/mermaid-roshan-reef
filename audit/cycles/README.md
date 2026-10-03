# Study cycles

Use this entry when the owner says "study the game". The commissioned loop runs after each development batch integrates into dev, at least monthly, and on request. Two manual owner-answer/build/check/learn cycles precede any proposal for a scheduled automation. No schedule or child-device telemetry is created by these tools.

Run from the repository root:

```text
python -B tools/study_game.py --cycle YYYY-MM-DD --as-of YYYY-MM-DD --output audit/cycles/YYYY-MM-DD --timeout 180
python -B tools/build_study_roadmap.py --study audit/cycles/YYYY-MM-DD/study.json --output audit/ROADMAP.md --cycle-dir audit/cycles/YYYY-MM-DD
python -B tools/study_game.py --render audit/cycles/YYYY-MM-DD/study.json --refresh-roadmap
python -B tools/plan_prompt.py "add a bakery job"
python -B tools/record_owner_decision.py --check
```

The runner writes study.json and STUDY_REPORT.md from the same measurements, records every sensor failure, cap, empty run or skip, and never writes images. Use its `--previous` option with the preceding study.json to measure changes. An offline study retains CI as unavailable unless an exact-head CI fixture is supplied. A green machine result supplies no visual, device, child or owner acceptance.

Generate the roadmap, strengths view, verification sweep, history and shipping-surface scorecard using the roadmap tool's documented CLI. Then refresh the saved roadmap observation; this measures the generated plan while preserving every raw sensor and CI receipt. Ordinary --render reproduces the saved report without a live observation. Commit the study and generated outputs with an updated impact record and ledger rows. Publish to the established GitHub repository; verify the exact remote revision and report one cycle entry link. Update this index when a cycle is added.

| Cycle | State | Evidence |
|---|---|---|
| [2026-10-03](2026-10-03/STUDY_REPORT.md) | Infrastructure study; owner-answer/build cycles and sessions pending | [Roadmap](2026-10-03/ROADMAP.md), [verification sweep](2026-10-03/VERIFICATION_SWEEP.md), [implementation evidence](2026-10-03/IMPLEMENTATION.md) |
| 2026-10-03 baseline | Intake measurement; historical handoff cycle zero; no new owner answers | [Loop health](2026-10-03-baseline/loop_health.json), [preserved planning updates](2026-10-03-baseline/PLANNING_HISTORY.md), [historical repair order](2026-10-03-baseline/REPAIR_ORDER_HISTORY.md) |

Each operational cycle also records actual owner answers (at most five per session), built impact IDs, exact check evidence and lessons with write-back targets. Rerunning a measurement does not complete a development cycle. Keep AC-1, AC-7, AC-9 and AC-10 of the [handoff](../../docs/handoffs/codex_self_improvement_loop_2026-10-03/README.md#5-acceptance-criteria) open until their real evidence exists.

For decision intake, save a JSON array of actual answers containing `id`, `date`, `subject`, `decision`, `source`, `authority: recorded_owner`, `question` and `checks` (file paths). Then run:

```text
python -B tools/record_owner_decision.py --answers PATH --cycle YYYY-MM-DD --answered-on YYYY-MM-DD
```

The supplied date is the actual owner session date. Existing records are immutable; later corrections append a new ID. Operating defaults cannot enter as owner answers. Each checkable correction must name an implemented executable check in `checks` and set `checkable: true`; artistic judgements retain exact human-review requirements. Intake appends to the decision register and that cycle's owner_answers.json on the same invocation. Historic answers keep their original decision dates and separate import date. Do not collect identifying child media.

The verification sweep groups missing evidence into one owner page and one device session. Its proposed date is an advisory target, not a booked session. Record a confirmed time before claiming that the session is scheduled; move finding lifecycles only with the required evidence.
