# Cycle 0 study report (2026-10-03)

**Status:** `SUPPORTING_CURRENT` worked example of
[`templates/STUDY_REPORT_V1.md`](templates/STUDY_REPORT_V1.md), written by
Claude by hand with the tools that exist today. From cycle 1 the numbers come
from `study.json` written by the study runner (work package LP2), never typed.
No runtime, device, child or owner evidence is claimed. Tracking finding:
[`MA-DOC-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-009).

## 0. Cycle header

```text
cycle:            2026-10-03   previous: none (cycle 0)
head:             f2140465b0d97575cf1855b1d0422a2c4be6110f (dev)
changes studied:  1e62991e..f2140465, 15 commits, 6 impact records
                  (everything since the last Claude handoff merged on 2026-09-30)
sensors run:      tools/measure_loop_health.py (this packet);
                  Probe Suite run 37100729058 at this head (success), log read;
                  document authority and development gates; remote branch survey
skipped:          device, child and owner sensors (none exist yet);
                  image-writing gates (Codex and CI run them)
```

## 1. What changed since the last cycle

- **Day One bathroom:** sink and bathtub dirt now clears where the child
  scrubs, by revealing the existing clean artwork under the existing dirty
  artwork; no new art (`day-one-bathroom-touch-dirt-20261002`, owner request
  of 2026-10-02).
- **Opera House:** a temporary developer menu in the left elevator starts any
  job fresh for playtesting and leaves child saves untouched
  (`opera-job-playtest-20260930`).
- **Sky Lagoon motion:** ten object-motion reference studies, then the
  owner's verdict that they transform the existing pictures instead of
  animating them and that the swing moves on the wrong axis; fresh swing poses
  were trialled and review v3 corrected the samples. References only
  (`sky-lagoon-local-animation-20260930`, `sky-lagoon-motion-owner-qc-20260930`,
  `sky-lagoon-moderate-animation-20260930`, `sky-lagoon-review-v3-20261001`).

## 2. Strengths observed

The full seed (15 entries) is [`data/strengths_seed.json`](data/strengths_seed.json).
The ones this cycle's changes show again:

| ID | Strength | Evidence | Proposed action |
|---|---|---|---|
| `S-02` | Touching the world changes it truthfully, where the child touches | `f2140465`; pattern `PAT-OBJ-01` | Keep as candidate; bind it in the room-activity recipe |
| `S-08` | Reuse first: the bathroom change used existing dirty and clean art | `day-one-bathroom-touch-dirt-20261002` | Keep; every recipe starts from an asset shortlist |
| `S-01` | The child cannot lose, and doing nothing wins nothing | `scripts/probe_passive.gd`, every push | Accepted (binding rule) |
| `S-09` | Numbered owner questions with defaults get one-line answers | The owner's 2026-09-30 answers | Accepted; section 7 uses it |
| `S-10` | A lesson that becomes a check stays learned | Grok retrospective, `tools/audit_imagine_handoff.py`, shot card V2 | Accepted; work package LP4 builds on it |
| `S-12` | Acts shaped Teach, Play, Twist, Bow, with a different verb per beat | `OPERA_ACT_PACING_2026-07-25.md` | Candidate; the job recipe's variety rule |
| `S-15` | A seeded challenge deck makes replays differ | Branch `ccr-ba906acd-1aepcb` (not merged) | Candidate; needs a merge decision |

## 3. Weaknesses observed

| Kind | Item | Evidence | Proposed action |
|---|---|---|---|
| New finding | Advisory sensors fail silently: Opera pacing hits its 300-second cap for all 15 careers; the Sky Lagoon capture ends in `FAIL`; the pearl-castle capture uploads nothing; the dust-boss "fun band" is not checked | Run 37100729058; `scripts/probe_opera_2d_balance.gd` lines 11 and 58; `.github/workflows/probes.yml` lines 269–418 | Opened as [`MA-CI-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-008) (P2) |
| New finding | The improvement loop does not turn | [LOOP_AUDIT.md](LOOP_AUDIT.md) | Opened as `MA-DOC-009` (P2) |
| Stale findings | 38 of 59 open findings without a history entry for 30 days; the oldest (51 days) include `MA-DOC-003`, `MA-VIS-003`, `MA-ACCESS-002`, `MA-ACCESS-003`, `MA-OPERA-002` and `MA-OPERA-004` | [`data/loop_health_2026-10-03.json`](data/loop_health_2026-10-03.json) | Re-verify in cycle 1, starting with findings whose files changed (LP2) |
| Unverified fixes | 12 fixed but unverified; six since 2026-08-13: `MA-VIS-002`, `MA-OPERA-001`, `MA-OPERA-010`, `MA-OPERA-011`, `MA-RELEASE-001`, `MA-COMBAT-001` | Same file | First monthly verification sweep (LP8) |
| Drift | The Opera pacing probe still says it drives "thirteen" acts; there are 15 careers | `scripts/probe_opera_2d_balance.gd` line 4 | Part of `MA-CI-008` |
| Drift | Scorecards still rate the retired Reef and have no row for Day One, Grand Puff, Day Two, the Teacher or the Geologist | Master audit section 1 | LP9 |
| Variety | The Geologist plays the Detective's music under its own ID; it has no score of its own | `ASSET_LICENSES.md` line 2828; not in `assets_src/audio/music/area_music_scores.json` | Grow lane: a Geologist score |
| Conflict | The voice manifest requires the Parler pipeline for new provisional lines; the Teacher, the Chapter 2 lawn and the fairy prototype used the legacy Kokoro path | `assets/audio/voices/VOICE_MANIFEST.md` lines 57–62; `design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md` line 48 | The voice recipe follows the manifest; Codex reconciles the three sets |
| Gap | Object-motion studies and the owner's verdict on them have no register | `sky-lagoon-motion-owner-qc-20260930` | LP2 lists them; LP5 turns the verdict into a review criterion |
| Coordination | The job-art rebuild branch (55 commits, 41,425 changed files) records a shared Roshan final-action format; the Roshan art repairs (`MA-ROSHAN-005`) have not started | `origin/codex/job-art-review-v2-20261001` at `cfcadc96` | Reconcile the two before either merges |
| Work in flight | 19 remote branches with commits since 2026-09-25 are not merged into `dev`: 7 feature branches, 12 rescue snapshots | Branch survey, 2026-10-03 | A keep, merge or close list for the owner (question 5) |

## 4. Loop health

Baseline; there is no previous cycle to compare with. Targets are the advisory
LP10 targets.

| Measure | Now | Target |
|---|---|---|
| Open findings without a history entry for 30 days | 38 of 59 (64%) | At most 10% |
| Fixed-but-unverified findings older than 30 days | 7 of 12 | 0 |
| Change records that record a lesson | 4 of 77 (5%) | At least half |
| Validation entries left `PENDING` / `FAIL` | 36 / 36 | Collected each cycle |
| Change-history rows: August / September / October | 56 / 11 / 0, plus 21 dated update paragraphs | Generated from change records |
| Tracked handoffs not started | 5 of 5 | None waiting more than two cycles |
| Workflows on a schedule | 1 (the weekly backup; every run has failed, latest 2026-09-28) | Owner decision (LP11) |
| Repeated owner corrections; prompts that needed clarification | Not measured (no register yet) | 0; measured from LP5 |

## 5. Roadmap delta

The first roadmap, so every item is new.

- **Repair:** fix the silent sensors (`MA-CI-008`); the first verification
  sweep for the 12 unverified fixes; the Roshan art repairs (`MA-ROSHAN-005`,
  owner-commissioned and ready); re-verify the oldest stale findings.
- **Grow:** jobs and room activities through recipes once LP7 exists (default
  of owner question 4); a Geologist score; the imp contests already in flight;
  the Day Two story revision and its challenge deck, after a merge decision.
- **Strengthen:** this handoff's LP0–LP2, then LP4 and LP5; then the earlier
  handoffs in the order of the [README](README.md#4-build-order-across-all-outstanding-handoffs).

## 6. Next prompts for the owner

1. "Fix the silent sensors" — recipe `INT-REPAIR` (`MA-CI-008`); pacing and
   two review captures are blind on every push; small.
2. "Build the loop, stage one" — this handoff, LP0–LP2; nothing else turns
   without it; medium.
3. "Do the Roshan art repairs" — recipe `INT-REPAIR` (`MA-ROSHAN-005`); ready
   and owner-commissioned; reconcile with the job-art branch first; medium.
4. "Sort the open branches" — recipe `INT-STUDY` for the 19 branches, each
   with a keep, merge or close default; small.
5. "Study the game" — recipe `INT-STUDY`; cycle 1, after the next batch
   merges into `dev`; small.

## 7. Questions for the owner

1. Turn the loop after each batch merges into `dev`, and at least monthly?
   Default: yes.
2. May recipes follow candidate strengths, labelled, before owner or child
   acceptance? Default: yes.
3. After play sessions, a one-line parent note (what the child loved, where
   the child got stuck)? Default: optional; no telemetry.
4. What should grow first? Default: jobs and room activities.
5. May Claude list the 19 open branches with a keep, merge or close default
   each, for a one-line answer? Default: yes.

These are README questions Q1, Q6, Q7 and Q8 plus one for this cycle; the
other README questions keep their defaults.

## 8. Lessons recorded this cycle

| Lesson | Written back to |
|---|---|
| A full commit SHA typed from memory was invented; caught before commit | Recipe `INT-PUBLISH-HANDOFF`: full SHAs come from `git rev-parse`; LP2: every 40-character SHA in a changed document must resolve |
| Counts from a read-only sweep disagreed with the tool (26 dated paragraphs against 21; 68 September change records against 76, because records that arrived through merges were missed) | AC-2: report numbers come only from `study.json`; the tool now dates merged files by their first commit |
| Claude's own change records leave "CI must pass" entries `PENDING` after CI passes | LP4: the collector resolves each from the CI run for the commit that last changed the record |
| Advisory steps marked continue-on-error hide their own `FAIL` lines | `MA-CI-008`; LP2 reads every advisory step's result line |
| Machine checks passed object motion the owner rejected as transformed rather than animated | LP5: the verdict becomes an animation review criterion |
| The Sky Lagoon studies were first counted as unregistered character studies; they are object studies, which no register covers | [LOOP_AUDIT.md](LOOP_AUDIT.md) loop L10 corrected; LP2 lists motion studies by kind |
