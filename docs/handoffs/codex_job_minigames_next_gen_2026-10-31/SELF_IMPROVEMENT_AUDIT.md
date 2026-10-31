# Job minigame self-improvement audit

- **Status:** the cycle (sections 2 to 5) is a `PROPOSED / CANDIDATE`
  procedure; the JC0 baseline (section 6) is `SUPPORTING_CURRENT` static
  analysis. It extends the 2026-10-03 improvement loop and the gold star; it
  replaces neither, grants no acceptance and adds no approval checkpoint.
- **Baseline:** dev `a0bb2cf4691631a534e210a5fb60fd227213322f` (2026-10-31).
- **Builds on:** the
  [loop audit](../codex_self_improvement_loop_2026-10-03/LOOP_AUDIT.md) and
  [cycle home](../../../audit/cycles/README.md) (study, keep, find, plan,
  prompt, build, check, learn); the
  [gold-star scorecard](../../../design/reference/GOLD_STAR.md) and
  `tools/gold_star.py`; the master audit's repair procedure (section 9, step 12:
  "At every study cycle, repeat inventory, audit, confirmation, triage and
  repair verification").

## 1. Why the job minigames need their own cycle

1. **The loop has stopped.** The last study cycle is 2026-10-03b; its five
   owner questions were never answered; `audit/ROADMAP.md` dates from the same
   day and lacks `MA-OPERA-014`, `MA-VIS-010`, `MA-VIS-011` and `MA-SAVE-002`
   ([`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009),
   `IN_PROGRESS`).
2. **Every career's score is stale.** `python -B tools/gold_star.py --check`
   reports 33 stale games, all 15 careers among them; each career is rated 1/5
   because C1 was 0 before the 2026-10-14 Chapter 2 repair, and C7 predates the
   painted art.
3. **The gold star does not predict the owner.** He rejected Pop Star (13 of
   24), Ballerina (14) and Racer (15) as the weakest careers while it ranks
   Detective (9), Astronaut (10) and Candy Maker (10) lower. It scores generic
   quality; he judged whether the job is there at all.
4. **No route exists.** `python -B tools/plan_prompt.py "self-improvement audit
   of the job minigames"` returns `NEEDS_INTENT`; no recipe covers re-auditing
   or rebuilding an existing job.
5. **The sensors see little.** The pacing sensor measures 4 of 15 careers
   ([`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008));
   `tools/study_game.py` folds 13 careers into one "Opera careers" surface;
   `tools/measure_loop_health.py` reports the October job handoffs as
   `UNTRACKED`; no gate checks that a spoken line matches its recording.
6. **No device, child or owner evidence exists for any career.** The
   7 November demo is the first device session.
7. **Records drift.** `DL-INT-07` and `DL-INT-12` count 13 careers against the
   code's 15; two owner directions on racing exist only on branches
   ([RACER_VERSIONS.md §2](RACER_VERSIONS.md#2-the-owners-words-on-racing)).

## 2. The job lens

Six judgements per career, scored 0, 1 or 2. They measure what the gold star
does not: whether the job's fantasy is present. Each is scored from cited
evidence (a file and line, a recording's text, a dated record), at the route the
child meets first (the Part 2 story for the eight party jobs).

| ID | Judgement | 2 | 1 | 0 | Anchors |
|---|---|---|---|---|---|
| JL1 | The job's own skill and feel | The core loop is a skill that belongs to the job and carries its defining feel: a beat for a performer, speed and passing for a racer, searching for a detective, care for a nurse, making for a chef or painter | The job's objects are there, but most steps are shared chores (hold, circle, swipe, any tap), or the real skill lacks its feel | No job skill: a demonstration or a held finger does the work | `DL-INT-07`, `DL-INT-02`; owner 2026-10-17 ("supposed to be a rhythm game") |
| JL2 | Roshan does the job | She goes to the place and performs each action with authored whole frames that change as she works | She goes to or stands by the place but holds still pose keys while the object moves | Hidden, cropped or absent while the child plays | `DL-INT-02` (owner 2026-09-06), `DL-MOT-07`; [`MA-PLAY-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004) |
| JL3 | The world is the control | Every touch lands on the job's own object in the scene, and that object changes | A mix of world objects and widgets (bars, rings, panels, lane strips) | Widgets only, or an invisible touch target | `DL-INT-01`, `DL-INT-02` |
| JL4 | Growth, not repetition | Each step adds something new, and repeat visits grow (tiers, new combinations) | Steps differ within a visit, but nothing grows across visits | The same chore repeats unchanged within a visit | Owner 2026-10-17 ("not just a repeating game"); `DL-AGE-05` |
| JL5 | A job payoff | The finish shows and says the job's own result (the served cake, the podium, the band's big finish), and it stays in the world or the save | The finish shows the job's object, but the spoken win is generic | A generic cheer and a code-drawn medal or digits | `DL-AGE-07`, `DL-MOT-03`, `DL-SND-04` |
| JL6 | Story truth | The job does what the record says, and every spoken line is true of the scene | One line or role detail is untrue | Several lines are untrue, or the job contradicts a recorded owner decision | `DL-AUTH-05` to `DL-AUTH-07`, `DL-INT-12`, `DL-SND-01`; the decision register |

**Calibration against the owner (the self-correcting part).** Each recorded
owner verdict is mapped to the lens or rubric criterion its words name, and that
criterion must score below 2 for that game:

- 2026-10-17, Pop Star, Ballerina, Racer ("weakest", "very weak", "supposed to
  be a rhythm game"): JL1. At JC0 they score 1, 0 and 0, and they are the three
  lowest lens totals.
- 2026-10-17, the Pop Star echo ("a usable mechanic"): that phase must keep
  JL1 at least 1. It does.
- 2026-10-03, Chef ("pours backwards", "lots of overdraw"): gold-star C6 or C7.
  C7 is 1.

When a new owner verdict disagrees with the lens (he rejects a career the lens
scores well, or praises one it scores badly), the disagreement is recorded as a
lens lesson in the cycle's impact record with `write_back` to this section, and
the lens is revised before the next cycle. JC0's agreement is a fit to the
verdict the lens was built from; the first real test is the next verdict (the
owner's look at the painted Chef, and the demo).

The lens is advisory beside the gold star. Folding it into the rubric would
change every career's score, so that is an owner decision (README Q7).

## 3. One cycle (JC*n*)

Run by hand after the demo build is promoted. Claude writes; Codex builds code,
images, boards and captures. A command marked "existing" is in the repository
today; one marked "NG11" is proposed in [WORK_PACKAGES.md](WORK_PACKAGES.md).

| Step | Who | What | Commands and output |
|---|---|---|---|
| 0. Precheck | Claude | Is the freeze lifted? Is the head's Probe Suite green? | Freeze: the demo handoff and `ODR-DEMO-FREEZE-20261031`; CI: the exact head's run |
| 1. Inventory | Claude | Every career branch not on dev, with a land, park or close note; every owner direction on a job, branch-only ones included | Existing: `git branch -r --no-merged origin/dev`, `git cherry origin/dev BRANCH`; search unmerged branches for `owner_verbatim`, `owner_request_quote` and `OWNER_DECISIONS.md` rows |
| 2. Sensors | Claude | Machine facts, numbers only | Existing: `python -B tools/gold_star.py --check` and `--rank`; `python -B tools/record_owner_decision.py --check`; `python -B tools/measure_loop_health.py --today DATE`; the job-art census `python -B docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py --summary`; the Probe Suite's `opera-balance` advisory. NG11: per-career pacing for all 15; the voice-truth check; the phase census |
| 3. Re-assess | Claude | Every stale career first: the gold-star criteria whose code changed, then JL1 to JL6, each with evidence | `design/reference/games.json`; `python -B tools/gold_star.py --rebind GAME`; the cycle's lens file |
| 4. Calibrate | Claude | Check every recorded owner verdict against section 2's rule | A lens lesson for every mismatch |
| 5. Register | Claude | New, changed and closed weaknesses, with stable IDs; closed ones keep their history | The cycle's register (the JC0 one is [WEAKNESS_REGISTER.md](WEAKNESS_REGISTER.md)) |
| 6. Choose | Claude, then the owner | At most three careers for the next build round, in this order: an owner verdict; a P0; the route she reaches first (the Part 2 order, then free play); the lowest lens; the lowest gold star | Up to five numbered owner questions, each with a default; defaults never become recorded answers |
| 7. Specify | Claude | One bounded change per weak criterion: the pattern to copy (`GS-*` or a stronger career), what the child sees change, and the probe assertion that proves it | A spec in the cycle folder or a handoff |
| 8. Build | Codex | One branch per package (`ODR-JOBART-PROCESS-20261018`), with its impact record and a green Probe Suite | Existing gates: `audit_document_authority.py`, `audit_development.py --base auto`, `scripts/ci.sh` |
| 9. Check | Claude | Re-score only the criteria whose code changed; record before and after | `--rebind GAME`, `--render` |
| 10. Learn | Claude | Lessons with `write_back`; the owner's verdicts through `tools/record_owner_decision.py`; revise the lens on a calibration miss | Impact-record `lessons` and `owner_corrections` |
| 11. Publish | Claude | The cycle folder `audit/cycles/job-DATE/` (cycle notes plus a lens JSON in the shape of [data/job_lens_jc0.json](data/job_lens_jc0.json)), its impact record and ledger rows; push and verify anonymously | The handoff delivery rule in `CLAUDE.md` |

**Cadence.** By hand for the first two cycles after promotion, then ask the
owner (`ODR-LOOP-Q3`, an operating default: "Run two manual cycles, then ask
the owner before creating scheduled automation"). Run a cycle
also after any owner verdict on a career, any landed career package, any device
or child session, and when 14 days pass without one.

**First two cycles.**

- **JC1 (the week after the demo):** inputs are the demo-day notes
  ([runbook R7](../codex_demo_readiness_2026-10-31/DEMO_RUNBOOK.md)), the
  owner's look at the painted Chef, the gold-star re-assessment of all 15
  careers (NG10) and a lens re-score. Output: at most three careers chosen and
  specified.
- **JC2 (after the first landed packages):** re-score the changed careers,
  calibrate against any new verdict, and ask the owner about cadence.

## 4. Lessons that change how handoffs are made

From the Day Two correction (2026-09-30), the October work and this audit:

| ID | Lesson | Evidence | Write-back target |
|---|---|---|---|
| JCL-1 | Before specifying, search every branch for the owner's words on the topic | Generation 1 missed the 2026-10-03 racing priority; the Day Two draft missed the job canon until the owner pointed to it | `design/reference/recipes/publish_handoff.md` and a job-audit recipe (NG11) |
| JCL-2 | An owner question lists every recorded option, built branches included | The 2026-10-18 Racer question offered two designs and not the existing engine | The same recipes |
| JCL-3 | Record an owner direction in the shared register when it is given | The 2026-10-03 and 2026-10-22 racing directions exist only on branches; the 2026-10-22 row would vanish on regeneration | `tools/record_owner_decision.py` usage in the cycle home |
| JCL-4 | Check a spoken line against its recording's text, not the phase's own text | Boxer and Geologist phases carry a correct caption and a wrong recording ([`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004)) | The voice-truth check (NG11) |
| JCL-5 | Judge the job's fantasy apart from generic quality | The gold star ranked the owner-rejected careers mid-table | Section 2 of this document; README Q7 |
| JCL-6 | Count from the code, not from a rule's text | `DL-INT-07` says 13 careers, 53 phases and 27 modes; the code has 15, 61 and 36 | NG10 |

## 5. Tooling the cycle needs (Codex, after the freeze)

Specified as package NG11 in [WORK_PACKAGES.md](WORK_PACKAGES.md):

1. A job-audit intent and recipe in `design/reference/prompt_intents.json`,
   rendered with `python -B tools/plan_prompt.py --render-recipes`, so a short
   prompt such as "audit the job games" routes to this cycle.
2. Per-career surfaces in `tools/study_game.py`, one for each live career.
3. Pacing personas for every career in the balance sensor (the loop review's
   CR3), with unsupported modes reported, not faked.
4. A voice-truth check: for every phase in `PHASES` and the Chapter 2 adapter,
   look up the recording's text in the voice manifests and flag a mismatch with
   the phase's objective, as section 2 of the register does by hand.
5. The job-art census gate already specified (job-art P10).
6. The lens as data: a `job_lens` block per career in
   `design/reference/games.json`, read and hash-bound by `tools/gold_star.py`,
   if the owner agrees (README Q7).
7. Targets for these packages in `tools/measure_loop_health.py`, so they stop
   reading `UNTRACKED`.
8. `gold_star.py --check` in remote CI. Local `scripts/ci.sh` runs it; the
   Probe Suite does not. It is a `.github/workflows/` change, a high-risk path
   that needs the owner's explicit yes (README Q8).

## 6. Baseline JC0 (2026-10-31)

Static judgement by Claude at the baseline; not acceptance. Evidence for every
score is in the [register](WEAKNESS_REGISTER.md) and
[data/job_lens_jc0.json](data/job_lens_jc0.json). Gold-star points are the
stale 2026-10-03 values.

| Career | JL1 | JL2 | JL3 | JL4 | JL5 | JL6 | Lens | Gold star | First change (package) |
|---|---|---|---|---|---|---|---|---|---|
| Racecar Driver | 0 | 0 | 0 | 0 | 1 | 1 | 2 | 15 | R1 after Q2 (NG3) |
| Pop Star | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 13 | BeatKit, then MR2 (NG4) |
| Ballerina | 0 | 1 | 1 | 0 | 0 | 1 | 3 | 14 | DR5 picker; then MR3 (NG5) |
| Candy Maker | 1 | 1 | 0 | 1 | 1 | 0 | 4 | 10 | Visible story input (NG7b) |
| Painter | 0 | 1 | 1 | 1 | 1 | 1 | 5 | 11 | Keep her marks (NG7c) |
| Detective | 1 | 1 | 1 | 1 | 1 | 1 | 6 | 9 | No reset; candle target (NG7e) |
| Farmer | 1 | 1 | 1 | 1 | 1 | 1 | 6 | 11 | DR5 door; crop seam (NG7a) |
| Astronaut Engineer | 1 | 1 | 1 | 1 | 1 | 1 | 6 | 10 | Two-finger proof; countdown (NG7d) |
| Magician | 1 | 1 | 1 | 0 | 1 | 2 | 6 | 15 | Glide taps (NG8b) |
| Pastry Chef | 1 | 1 | 1 | 1 | 1 | 2 | 7 | 10 | The owner's look (NG6) |
| Stuffie Doctor | 1 | 1 | 1 | 1 | 1 | 2 | 7 | 11 | Care pays (NG8c) |
| Boxer | 2 | 0 | 2 | 1 | 1 | 1 | 7 | 16 | True first line (NG8a) |
| Geologist | 2 | 1 | 2 | 1 | 1 | 0 | 7 | 11 | True lines; win caption (NG8e) |
| Arborist Tree Book | 1 | 1 | 1 | 1 | 1 | 2 | 7 | – | Spray fix; alpha (NG2, NG8g) |
| Teacher | 1 | 1 | 2 | 2 | 1 | 1 | 8 | 15 | Pearl targets (NG8f) |
| Nursery Nurse | 2 | 1 | 2 | 1 | 1 | 2 | 9 | 14 | Faron reactions (NG8d) |

Read across the columns: JL2 (Roshan does the job) and JL5 (a job payoff) are
weak almost everywhere, which is why the shared packages NG9b (curtain call)
and the art packages matter more than any one career's polish. JL1 is strong
only where one skill truly belongs to the job (Boxer, Geologist, Nursery).

## 7. Cycle notes template

Copy into `audit/cycles/job-DATE/JOB_CYCLE.md`:

```text
# Job cycle JCn (DATE)
Head: <40-character SHA>   Probe Suite: <run id and result>   Freeze: <lifted | active>
Inventory: <branches with job work not on dev, each with land | park | close and why>
Owner words found: <new or branch-only directions, with file and line>
Sensors: gold_star --check <stale count>; pacing <careers measured of 15>;
  voice truth <mismatches>; job-art census <primitive draws, texture draws>
Re-assessed: <careers and criteria re-scored, with rebind hashes>
Calibration: <each owner verdict, the criterion its words name, the score; misses>
Register changes: <new, changed and closed weakness IDs>
Chosen for the next round (at most three): <career: weakness: package>
Owner questions (at most five, each with a default): <...>
Lessons (with write_back): <...>
Three claims: implemented <...>; machine-verified at <SHA> <...>; outstanding <...>
```
