# Codex handoff — the self-improvement loop: study, keep, find, plan, prompt, build, check, learn (2026-10-03)

**Owner request (2026-10-03):** *"Analyze what is missing in this code and
construct, the whole idea is a self replicating loop, where it studies the
game, identifies the positive qualities of it to use as a reference for self
improvement, identifies ongoing new weakneses, provides a roadmap for
developing ongoing nuanced content with simple prompts. Analyze the feedback
loops currently in the master audit on these topics, and how they can be
further refined."* Then: *"Upload it to git as a codex handoff. Given URL for
easy handoff."*

**From:** Claude (analysis, written specification, templates, seeds and a
read-only measurement tool; no game change and no images). **To:** Codex
(implementation). **Owner:** answers the questions in section 6.

**Status:** `PROPOSED / CANDIDATE`, revision 1. This packet recommends; it
grants no visual, device, child or owner acceptance and changes no existing
finding lifecycle. It adds the tracking finding
[`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009)
and the sensor finding
[`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008)
(both P2, `CONFIRMED_OPEN`). Every package follows `CLAUDE.md`, `AGENTS.md` and
the master-audit development contract (`DL-AUTH-05`, `DL-AUTH-06`,
`DL-AUTH-07`).

**Evidence baseline:** `dev` `f2140465b0d97575cf1855b1d0422a2c4be6110f`. The
findings are in [LOOP_AUDIT.md](LOOP_AUDIT.md).

## What is in this folder

| Path | What it is |
|---|---|
| `README.md` | This handoff: the loop, work packages, build order, acceptance, owner questions |
| `LOOP_AUDIT.md` | The analysis: what is missing at each stage and every feedback loop in the master audit |
| `CYCLE_0_STUDY_REPORT.md` | The first turn of the loop, written now with existing tools, as the worked example |
| `templates/STUDY_REPORT_V1.md` | The per-cycle report |
| `templates/PROMPT_RECIPE_V1.md` | How a one-line prompt expands into a complete plan |
| `data/loop_health_2026-10-03.json` | Loop measurements at the baseline |
| `data/loop_inventory.json` | The twelve feedback loops with status, last activity and refinement |
| `data/strengths_seed.json` | First strengths register entries, each with evidence |
| `data/prompt_intents_seed.json` | First prompt intents and what each expands into |
| `tools/measure_loop_health.py` | Read-only loop measurement (standard library) |
| `MANIFEST.json` | SHA-256 of every file in this folder |

Nothing here is loaded by the game; `.gdignore` keeps Godot from importing it.

## 0. Summary

The parts of the loop exist; the loop does not turn. One loop is enforced by
a machine (the per-change impact record). The rest is write-only, frozen in
August, or specified and unbuilt: no exemplar has ever been promoted, 38 of 59
open findings have had no entry for 30 days, 12 fixes have never been
verified, the scorecards and repair order date from August, 4 of 77 change
records record a lesson, and none of the five handoffs written this week has
started. Where a loop did close, the lesson became a check, a reference or a
recipe step. This handoff builds the smallest loop that turns every cycle
with existing tools, then grows it.

## 1. The loop

| Stage | Output | Who | Cadence |
|---|---|---|---|
| 1 Study | `audit/cycles/<date>/STUDY_REPORT.md` and `study.json`: what changed, sensor results, loop health | Claude, from sensors Codex builds | Each cycle |
| 2 Keep | Strength candidates promoted into `design/reference/strengths.json`, patterns and exemplars | Claude proposes; owner accepts the top tier | Each cycle |
| 3 Find | New finding candidates, stale findings, regressions | Claude proposes; findings opened with reproductions | Each cycle |
| 4 Plan | `audit/ROADMAP.md`, regenerated: Repair, Grow and Strengthen lanes | Codex's generator; Claude writes the judgement | Each cycle |
| 5 Prompt | Up to five ready-to-say prompts, each mapped to a recipe | Claude | Each cycle |
| 6 Build | The chosen prompts, through their recipes | Codex | Between cycles |
| 7 Check | CI, tools, cards, before-and-after boards, owner and child notes | CI, Codex, owner | Per change, plus a monthly verification sweep |
| 8 Learn | Lessons written back to a named target (rule, decision, recipe, sensor, reference) | Whoever learned it, collected by the next study | Per change |

**The owner's interface stays tiny:** read one short report, answer up to
five numbered questions in one line (the format the owner already uses:
"1. yes, 2. keep, 3. no"), say one of the ready-made prompts.

## 2. Invariants

- No rule, finding history or protected art is changed by the loop itself;
  it proposes, and the existing contract decides.
- Claude writes; Codex builds every image (`CLAUDE.md`, 2026-09-30). Sensors
  never write images unless Codex runs them.
- New permanent content still needs the owner's premise approval
  (`DL-PLAN-01`); variation inside an approved scope is delegated
  (`DL-PLAN-04`).
- Child-facing rules do not bend for throughput: no fail states, a voice line
  and a visual pointer for every objective, additive saves.
- No telemetry from the child's device without an explicit owner decision.

## 3. Work packages

### LP0 — Stage 0 (read-only)

Run `tools/measure_loop_health.py` from this folder at your head. Note which
earlier handoff packages have landed. **Gate:** a note in the impact record.

### LP1 — Cycle home

Create `audit/cycles/` with a README index, the two templates in
`design/templates/`, and a "Study the game" route in the master-audit task
index. Move the 21 dated update paragraphs out of the planning entry into
the first cycle report, leaving current answers only. **Gate:** both
governance gates ALL OK.

### LP2 — Study runner

`tools/study_game.py`: runs the sensors and writes `study.json` plus a draft
report with every number filled in. Includes the loop-health measures, the
live-status counts (refinement handoff WP-2), the latest CI result for the
studied head, the 2D, typography and visual-profile measures, the Day Two
library refresh delta, findings whose referenced files changed since their
last history entry, motion studies and owner verdicts by kind, impact-record
lessons and `PENDING`/`FAIL` entries, handoff build status, unmerged branches,
and every advisory step's result line, so a capped, failed or empty advisory
run is reported (`MA-CI-008`). Advisory; never writes images. **Gate:**
unit tests with fixtures; a stress case that fails.

### LP3 — Strengths register

`design/reference/strengths.json` (`S-*`) rendered to `STRENGTHS.md`, seeded
from `data/strengths_seed.json`. Two tiers: *candidate* (evidence: file,
capture, probe or owner note) and *accepted* (owner or child evidence). Each
strength links to the patterns, exemplars and identity sheets it justifies.
Recipes may bind candidates, labelled as such. **Gate:** every entry has
evidence that exists.

### LP4 — Lessons in every change

Add optional impact-record fields: `lessons` (each with `write_back` target),
`strengths_observed`, `references_used`, `owner_corrections`.
`tools/audit_development.py` validates their shape when present. The study
runner collects them and lists lessons without a write-back target, and
`PENDING` validation entries whose result now exists (for example a CI run
that has finished). **Gate:** existing records stay valid.

### LP5 — Decision register intake

Build the owner decision register (refinement handoff WP-3) and make every
cycle's answers land in it the same day. An owner correction that can be
checked also becomes a check, so it never has to be said twice. **Gate:** the
2026-09-30 answers (Roshan identity, Q12–Q16) are entries.

### LP6 — Living roadmap

`audit/ROADMAP.md`, generated each cycle. **Repair** lane: findings by child
impact, owner priority, dependency and age. **Grow** lane: new content from
strengths and owner goals. **Strengthen** lane: unbuilt handoffs, stale
references, missing sensors and recipes. Every item carries a one-line prompt
and a recipe ID. Master-audit section 13 becomes a pointer plus the ordering
rule. **Gate:** generator tests; no item without a recipe or a reason.

### LP7 — Prompt catalogue and recipes

`design/reference/prompt_intents.json` and `design/reference/recipes/*.md`,
from `data/prompt_intents_seed.json` and `templates/PROMPT_RECIPE_V1.md`.
First recipes: add a job, add a room activity, repair, polish an area, retire
something, study an area, publish a handoff; then a new chapter (wrapping the
chapter guide), a character animation (movement profile) and a story clip
(shot card). Each recipe names its references, variety rules, owner
touchpoints, gates and write-backs. **Gate:** a cold-start test: a fresh agent
given only "add a bakery job" and the repository produces a complete plan
without asking anything outside the recipe's owner touchpoints.

### LP8 — Monthly verification sweep

For every `FIXED_PENDING_VERIFICATION` finding, collect what evidence is
missing, then batch it into one owner page and one device session per month.
Move lifecycles only with evidence. **Gate:** the twelve current items each
show their missing evidence.

### LP9 — Master-audit refinements

Generate the change history (section 14) from impact records in one order;
regenerate the scorecards (section 1) from the cycle report for the surfaces
that ship now; change the re-audit trigger from "no active item remains" to
"each cycle"; make the rule-earning clause (sections 12 and 18) count
recurrences, three in a cycle proposing a rule or check. **Gate:** governance
gates ALL OK; no history text rewritten.

### LP10 — Loop health checks

Advisory targets reported every cycle: open findings without an entry for 30
days at most 10%; fixed-but-unverified items older than 30 days zero; lessons
in at least half of change records; repeated owner corrections zero; roadmap
regenerated each cycle; handoffs waiting more than two cycles listed.

### LP11 — Cadence and automation (owner-gated)

Run the study after each batch merges into `dev` and at least monthly. After
two cycles by hand, automate it if the owner agrees (a scheduled Claude
routine, or a CI schedule, which changes `.github/workflows/`, a high-risk
file). Publish each cycle report to GitHub with one link.

## 4. Build order across all outstanding handoffs

The loop's critical path first, then the larger handoffs as roadmap items.

1. LP0, LP1 and a minimal LP2 (existing tools only), and the `MA-CI-008`
   sensor repair so the first study reads working sensors. Claude runs
   cycle 1.
2. LP4 and LP5 (lessons and decisions).
3. LP3 with refinement WP-5 (patterns) and WP-4 (canon).
4. LP7, starting with "add a job" (the interim job recipe), "repair" and
   "add a room activity".
5. LP6 and LP9.
6. LP8: the first verification sweep in the first month.
7. Then, as roadmap items: the [Roshan art repairs](../codex_roshan_art_repairs_2026-09-30/README.md)
   (owner-commissioned and ready), refinement WP-2 (live status, feeds the
   study), [Job Platform](../codex_job_platform_architecture_2026-09-30/README.md)
   JP0–JP2 (feeds the job recipe), [visual language](../codex_visual_design_language_2026-09-30/README.md)
   VL1–VL3 (feeds art recipes), [reference consolidation](../codex_reference_consolidation_2026-09-30/README.md)
   W2–W4 (cleans what the loop reads).
8. LP10 and LP11 once two cycles have run.

## 5. Acceptance criteria

| ID | Criterion | How to show it |
|---|---|---|
| AC-1 | Two complete cycles have run: study, owner answers, build, check, learn | Two cycle folders and their impact records |
| AC-2 | Each cycle report's numbers come from `study.json`, none typed | Study runner test |
| AC-3 | The strengths register exists with evidence for every entry, and at least one recipe binds strengths | Register check |
| AC-4 | Lessons in at least half of the change records since LP4; none without a write-back target | Study report section 8 |
| AC-5 | The roadmap is generated and every item has a prompt and a recipe | Generator test |
| AC-6 | The cold-start "add a bakery job" test passes | Test record |
| AC-7 | The twelve fixed-but-unverified findings each list their missing evidence; the first owner page and device session are scheduled | Sweep record |
| AC-8 | Master-audit history is generated; scorecards cover the surfaces that ship now; re-audit runs each cycle | Master audit |
| AC-9 | Loop health improves between cycle 1 and cycle 2 on at least three LP10 measures | Two `study.json` files |
| AC-10 | `MA-DOC-009` acceptance met and recorded | Finding record |

## 6. Owner questions (Codex proceeds on the default and reports it)

| # | Question | Default |
|---|---|---|
| Q1 | How often should the loop turn? | After each batch merges into `dev`, at least monthly, and whenever the owner says "study the game" |
| Q2 | Who does what? | Claude studies, plans and writes recipes; Codex builds; the owner answers up to five numbered questions per cycle |
| Q3 | Automate the study on a schedule? | By hand for two cycles, then ask again |
| Q4 | Publish every cycle report to GitHub with one link? | Yes |
| Q5 | Change the master audit's process: generated history and repair order, re-audit each cycle, counted rule earning? | Yes |
| Q6 | May recipes follow candidate strengths before owner or child acceptance? | Yes, labelled candidate; accepted ones first |
| Q7 | After play sessions, would a one-line parent note (what the child loved, where the child got stuck) be possible? | Optional; it goes into the next cycle report; no telemetry |
| Q8 | Which content should grow first? | Jobs and room activities, the most frequent requests |

## 7. Gates and delivery

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
```

plus the new tools' tests and `scripts/ci.sh` when a tool changes. CI on the
branch must be green at its exact head before merging into `dev`.

## 8. Stop and escalate if

- A step would change a rule, rewrite finding history or touch protected art.
- Automation would need `.github/workflows/`, `CLAUDE.md`, `AGENTS.md` or
  `.claude/` changes the owner has not named.
- A sensor would need data from the child's device.
- Another branch has edited the master audit, design 06, the ledger or the
  finding register since you started: rebase and re-verify.

## 9. Report (per package)

- **Implemented:** files, IDs, sensors and recipes added.
- **Machine-verified:** commands and results at the exact head.
- **Outstanding:** owner answers pending, and every visual, device, child and
  owner gate still open.
