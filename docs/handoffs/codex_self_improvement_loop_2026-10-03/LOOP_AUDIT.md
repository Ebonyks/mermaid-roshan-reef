# Self-improvement loop audit (2026-10-03)

**Status:** `SUPPORTING_CURRENT` audit evidence prepared by Claude (analysis
only; no game change). Measured at `dev`
`f2140465b0d97575cf1855b1d0422a2c4be6110f`. Tracking finding:
[`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009).
The plan is [README.md](README.md).

**Owner request (2026-10-03):** *"Analyze what is missing in this code and
construct, the whole idea is a self replicating loop, where it studies the
game, identifies the positive qualities of it to use as a reference for self
improvement, identifies ongoing new weakneses, provides a roadmap for
developing ongoing nuanced content with simple prompts. Analyze the feedback
loops currently in the master audit on these topics, and how they can be
further refined."*

## 1. The answer

**The parts of the loop exist; the loop does not turn.** Only one feedback
loop is enforced by a machine: every change must carry an impact record, and
CI checks it on every push. Everything that would let the game learn from
itself is write-only, frozen in August, or specified and not built.

| Measure (at the head above) | Value |
|---|---|
| Open findings | 59 |
| Open findings with no history entry for 30 days | 38 |
| Findings fixed but never verified (`FIXED_PENDING_VERIFICATION`) | 12, six of them for 51 days |
| Exemplars ever promoted to the reference library | 0 |
| Satisfaction-gate boxes ticked | 1 of 23 |
| Change records (impact records) | 77, of which 4 record a lesson and 27 link no finding |
| Validation entries left `PENDING` or `FAIL` in change records, never collected | 36 and 36, in 35 and 22 records; many `PENDING` entries (Claude's included) are "CI must pass before merge" lines that nothing updates once CI passes |
| Scorecards | Last edited 12–13 August; still rate the retired Reef; no row for Day One, Grand Puff, Day Two, Teacher or Geologist |
| Repair order (master audit section 13) | 52 of 83 lines last edited 13 August |
| Master-audit change history | 56 rows in August, 11 in September, none in October; 21 dated update paragraphs in the planning entry carry the rest |
| Codex handoffs specified this week and built | 0 of 5 |
| Workflows that run on a schedule | 1 (the weekly backup, which has never succeeded) |

Numbers come from [`tools/measure_loop_health.py`](tools/measure_loop_health.py)
([`data/loop_health_2026-10-03.json`](data/loop_health_2026-10-03.json)) and a
read-only sweep of the governance documents.

**Where a loop did close, it closed the same way twice.** The Grok handoff
retrospective turned its best exemplar into a rule, the rule into a tool
(`tools/audit_imagine_handoff.py`) and the tool into the V2 shot card. The
2026-09-16 handoff-publication correction went into both entry points and was
locked by a contract test. **A lesson closes only when it becomes a check, a
reference or a recipe step that the next task cannot skip.** Everything else
is read once, if at all.

## 2. The loop the owner described, stage by stage

| Stage | What should happen | What exists | What is missing |
|---|---|---|---|
| 1 Study | Measure and observe the whole game on a cadence | CI probes on every push (regressions of known defect classes); one-off studies (persona playthroughs, art library, playtest launcher) | No cadence, no cycle report, no "what changed since last time"; fun, comprehension and charm are not sensed (section 4) |
| 2 Keep | Turn positive qualities into references that new work must use | "What works" columns in August scorecards; seed patterns; Day Two library scores; a Grand Puff identity lock | No strengths register; 0 promoted exemplars; promotion blocked behind device, child and owner review that never happens |
| 3 Find | Discover new weaknesses continuously | Findings register with a rich lifecycle; owner-requested audit rounds | Discovery only when someone audits; no trigger when code under a finding changes; 12 fixes never verified |
| 4 Plan | Keep one living roadmap of repairs, new content and system upkeep | Repair order (defects only, August); three-row planning table (5 September); five handoffs | No roadmap that combines findings, strengths and owner goals; nothing regenerates it |
| 5 Prompt | Turn a short owner prompt into a complete plan | Chapter guide and brief; an interim job recipe; shot cards; movement profiles | No intake for a one-line prompt; no recipe for a room activity, companion, event, polish or retirement; no canon, pattern, token or decision registers |
| 6 Build | Codex implements | Works well: 76 change records in September | Built work does not record which references it used |
| 7 Check | CI, tools, owner, device and child acceptance | CI and tools on every push | Owner, device and child acceptance has no scheduled moment, so closure stalls |
| 8 Learn | Write lessons back into rules, references, recipes and sensors | A learning log in the chapter brief, a "what worked" list here and there, the rule-earning clause in sections 12 and 18 | No lesson field in change records; the rule-earning clause has never fired although 15 recurring defect classes are counted; owner corrections scatter over 49 files |

## 3. The feedback loops in the master audit today

| Loop | Closes? | Last activity | What breaks it | Refinement |
|---|---|---|---|---|
| L1 Findings lifecycle (sections 2, 9, 10; register) | Broken at closure and re-audit | 2026-09-30 (new records) | Closure needs device, child and owner evidence that is blocked; re-audit runs only "when no active item remains", which never happens | A monthly verification sweep that batches what each stuck finding needs into one owner page and one device session; re-audit on a cadence, not on empty |
| L2 Change record (impact record, `DL-AUTH-05` to `DL-AUTH-07`) | Closed as a gate, open as learning | Every change | No field for lessons, strengths or corrections; `PENDING` and `FAIL` entries are never collected; rule citations have become boilerplate | Add `lessons`, `strengths_observed`, `references_used` and `owner_corrections` fields; a collector reads them into each cycle report |
| L3 Chapter brief to guide improvement (`DL-PLAN-06`) | Open; never completed a cycle | One partial use (faerie prototype) | The review step that writes back into the guide has never run | Make the retro a required step of every recipe, read back by the next cycle |
| L4 Reference-library promotion | Never fired | 0 promoted | Promotion waits for device, child and owner review | Two tiers: owner-accepted exemplars, and candidate exemplars with evidence; recipes may bind candidates |
| L5 Satisfaction gate and rule earning (sections 12, 18) | Terminal; rule earning never fired | 1 of 23 boxes | Nothing counts recurring defect classes | The cycle report counts recurrences; three in a cycle proposes a rule or a check |
| L6 Repair order (section 13) | Broken | Mostly 2026-08-13 | Hand-maintained; not derived from findings | Generate it from findings by child impact, owner priority and dependency |
| L7 Change log and rollback (`CHG-*`) | Dormant | One entry since August | Impact records replaced it in practice | Keep for behaviour-changing groups only; say so in its maintenance rule |
| L8 Scorecards (section 1) | Broken | 2026-08-12/13 | Nothing refreshes or reads them | Regenerate per cycle from studies, covering surfaces that ship now |
| L9 Owner-decision capture | Closed once, broken elsewhere | 2026-09-16 (closed case) | No register; decisions live in handoffs and paragraphs | One decision register; every cycle's answers land there the same day |
| L10 Animation study and profile (`DL-MOT-10` to `DL-MOT-13`) | Closed for Roshan; no home for object motion | 2026-09-13 (last Roshan entry) | The index covers characters only; the Sky Lagoon object-motion studies of 2026-09-30 and 10-01, and the owner's rejection of them, live only in their own packets and impact records | The cycle report lists motion studies and owner verdicts; each verdict becomes a review criterion (for example: animate the object, do not transform the existing picture) |
| L11 Document authority gate | Closed for structure only | Every push | Semantic staleness (wrong counts and decisions) passes | Live status block and stale-fact checks (refinement handoff WP-2) |
| L12 Owner question to audit and handoff | Produces proposals only | Six rounds on 2026-09-30 | Handoffs queue up unbuilt | A build order across handoffs, and the cycle report shows what is waiting |

## 4. Studying the game: what is sensed and what is not

Nothing in the repository creates or updates a finding, exemplar or roadmap
item by itself; every one is written by an agent or the owner. What runs:

| Sensor | Senses | Runs | Result kept? |
|---|---|---|---|
| Trusted probe roster (81 in CI, 82 locally) | Games can be won; doing nothing wins nothing; rewards; saves; Back; touch adversaries; target sizes; asset hashes | Every push | CI log only |
| Static gates (2D debt, document authority, art and hash contracts, headroom, Sky Lagoon congruency) | Structure and regressions of known defect classes | Every push | Log; a few JSON files |
| Advisory balance runs (dust boss, Opera) | Simulated-child timings | Every push, never failing the build | Log lines only |
| Six review captures | Screenshots for a person to look at | Every push, never failing the build | Artifacts, deleted by quota cleanup |
| Day Two art library, minigame art registry | Agent-scored image reviews | By hand | Committed reports |
| Day One persona playthroughs (16 simulated children) | Attention, confusion, pacing, hazards | Once (2026-09-02); not repeatable | Committed; none of its findings DO-01 to DO-23 reached the register |
| Opera elevator launcher | Lets the owner play any of the 15 jobs fresh | By hand | Records nothing about the playtest |

**Two sensors fail silently today** (probe run `37100729058` at this head,
green; recorded as
[`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008)):

- The Opera pacing probe reports `verdict=capped` at its 300-second cap for
  all 15 careers (`scripts/probe_opera_2d_balance.gd`, `TIME_CAP`), in every
  sampled `dev` run since 2026-09-02. It also still says it drives "thirteen"
  acts. Pacing is not being measured at all.
- The Sky Lagoon review capture ends `LAGOONSHOT|RESULT|FAIL` and the pearl
  castle capture uploads nothing; both steps are marked continue-on-error, so
  the run stays green and keeps four of its six expected artifacts (one of
  them a capture of the retired Reef).

The workflow also says the dust-boss balance run checks a 45–120 second fun
band; the probe checks only win or no win. And machine checks passed the
2026-09-30 Sky Lagoon motion studies that the owner then rejected ("transform
the existing items than truly animating them"), so the sensors are blind to
the owner's taste unless the owner's verdicts are written back as rules.

**Not sensed at all:** fun (only time bands, one of them dead), comprehension
(no child evidence; `MA-CHILD-001` blocked since 2026-08-13), charm and beauty
(agent opinion only), variety (one static voice-repetition audit), pacing (the
dead sensor above), emotional payoff (only that a celebration fires). There is
no play log: the save keeps a launch counter, and the phone save that
`backup.sh` already copies is never read.

## 5. Positive qualities: why none is kept

Positive qualities appear in five places: the August scorecards' "what works"
and "best qualities" columns, the seed patterns of the chapter reference
library, the Day Two art library's 4.6–4.9 reviews (205 of 637 images), the
minigame audit's "keep" column, and the "what already works" list of the
visual language audit. None is promoted, and no rule or tool reads them. The
reference library's promotion step needs device, child and owner review,
which is blocked, so it has promoted nothing.

Refinement: a **strengths register** (`S-*`) with two tiers. A *candidate*
needs evidence (a file, a capture, a probe or an owner note) and may already
be bound by recipes as "follow this". An *accepted* strength has owner or
child evidence. Strengths link to the pattern (`PAT-*`), exemplar (`EX-*`) and
identity sheets they justify. The seed in
[`data/strengths_seed.json`](data/strengths_seed.json) starts from what the
repository already proves.

## 6. New weaknesses: discovery and the stuck verification loop

Weaknesses are found when the owner asks for an audit or a review touches an
area. CI catches regressions of defect classes that are already encoded. Two
things never happen on their own: a finding is not re-checked when the code it
names changes, and a fixed finding is not verified. Six of the twelve
fixed-but-unverified findings have waited 51 days.

Refinement: the cycle report lists (a) findings whose referenced files changed
since their last history entry, (b) fixed findings waiting for a named kind of
evidence, grouped into one owner page and one device session per month, and
(c) new weakness candidates from the sensors, each either opened with a
reproduction or recorded as "watching".

## 7. Roadmap and simple prompts

**Owner prompts are already simple; the expansion is invented each time.**
Recent one-sentence prompts produced four different document shapes: a
research-and-self-score report (Teacher, Geologist), a handoff (Tree Book,
Day One), a filled chapter brief (faerie restoration) and a Codex packet (imp
contests). The one that followed a recipe, the faerie prototype with the
chapter brief, went from prompt to combined green CI the same day.

**Owner corrections are mostly about canon and fit**, not mechanics: wrong
room, wrong job role, a missing visible change, the wrong tool for the job.
That is what a canon register, a decision register and recipes with "read
first" lists prevent.

| Content type | Recipe today |
|---|---|
| New chapter | Chapter guide and brief (binding; used once) |
| New job | Interim recipe in the job-game takeover audit; Job Platform proposed |
| Character animation | Movement profile and production protocol (Roshan only) |
| Story clip | Shot card (V1 or V2 still unsettled) |
| Still art | Art style card (draft in the visual language handoff) |
| Castle room activity, companion, seasonal or weather event, non-job minigame, voice-line set | None |
| Repair, polish, retire, study, publish a handoff | Repair protocol (section 9) only; the rest live in conversations |

**The game already has a variety grammar, unlisted.** Fifteen careers, 61
phases and 36 gesture modes; the Teach / Play / Twist / Bow act shape; the
rule that beats are different verbs (`OPERA_ACT_PACING_2026-07-25.md`);
truthful transformations (dirty to clean, sick to healthy, bud to bloom); the
owner's "visceral" ingredient rule; rewards that only upgrade; the imp
contest in three forms (`DL-INT-14`); thirteen castle rooms as thematic homes.
The richest variety mechanism, a seeded "challenge deck" of Mischief, Helper,
Coach and Hint cards so replays differ, sits on the unmerged branch
`ccr-ba906acd-1aepcb`. Writing this grammar down is what lets a simple prompt
produce *nuanced* content instead of a copy of the last job.

**There is no roadmap that joins the three lanes.** The repair order covers
defects (August), the planning table has three rows (2026-09-05), and new
content arrives by owner request. Meanwhile 19 remote branches with commits
since 2026-09-25 are not merged into `dev`: seven feature branches (the imp
contests being built, a Day Two story revision with the challenge deck, a
job-art rebuild of 55 commits and 41,425 changed files, Day Two art
replacements, the picture book, the battle of the bands and a fairy
storybook) and twelve one- or two-commit rescue snapshots. The audit cannot
see work in flight.

**What the child enjoys is unknown to the repository.** The owner has relayed
tastes (silly humour, stuffed animals, followers, the family band); no session
has been observed (`MA-CHILD-001`). The best observation script that exists is
the imp contest's acceptance questions (for example, whether the child laughs).

## 8. Learning: why lessons stay write-only

Lessons are written in many places (the chapter brief's learning log, design
02's rejected approaches, the never-list in section 7, the animation
protocol's "kept/rejected because" records, the Grok retrospective) and read
back only where they became a tool or a contract. Change records have no
lesson field, so the most frequent record type teaches nothing.

Refinement: each lesson names its **write-back target** (rule, decision,
recipe step, sensor, reference) and the cycle report shows lessons without
one. An owner correction is the strongest lesson: it lands in the decision
register the same day and, where it can be checked, becomes a check, so the
owner never has to say it twice.

## 9. Method and limits

Three read-only sweeps (governance loops; game-study mechanisms; content
pipelines), the loop-health measurement and direct reads of the master audit.
No runtime, device, child or owner evidence is claimed. Counts are measured at
the head above and will move.
