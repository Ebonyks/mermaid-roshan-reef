# Codex handoff — Job Platform architecture (2026-09-30)

**Owner request (2026-09-30):** *"Design an architecture that will support
these changes more effectively, and upload to git as handoff."*

**From:** Claude (specification only; no game change). **To:** Codex
(implementation, including any generated art or audio). **Owner:** answers the
questions in section 4.

**Status:** `PROPOSED / CANDIDATE`. Publication is not acceptance. Every
package follows `CLAUDE.md`, `AGENTS.md` and the master-audit development
contract (`DL-AUTH-05`, `DL-AUTH-06`, `DL-AUTH-07`): impact record, ledger rows,
gates, CI, then integration into `dev`.

**Evidence baseline:** `dev` `7f068cb80766edd52a110cc1cb3958158f829822`.
Re-measure at your head first (package JP0).

**"These changes"** are the ones the owner set in motion on 2026-09-30: a design
reference and a maintained job-game playbook
([refinement handoff](../codex_master_audit_refinement_2026-09-30/README.md),
Stage J), finding
[`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006)
from the [job-game audit](../../../audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md),
imp contests in every competitive career
([`DL-INT-14`](../codex_opera_imp_contest_2026-09-30/README.md)), the four-floor
Opera House, and future job games built by an agent that takes over
development. The architecture makes each of them cheaper and safer.

## What is in this folder

| Path | What it is |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | The design: forces, principles, layers, the job record, build and runtime layers, the shared JobKit, verification, documents, fit with existing plans, migration, a worked example, risks, registry inventory |
| `schema/job_record.schema.json` | Proposed contract for one job record |
| `examples/teacher.job.json` | A complete record built from today's Teacher |
| `examples/ledger.example.json` | The append-only star-bit ledger built from today's slots, including the three tombstones |
| `tools/extract_job_catalog.py` | Read-only prototype that rebuilds per-job records from today's registries and re-derives every hard-coded mask, count and bound |
| `data/extracted_catalog.json` | Its output: 15 job records and 3 tombstones |
| `data/derivation_check.json` | Its proof: 11 of 11 hard-coded values reproduced from the records; drift found; the next-job trap quantified |
| `MANIFEST.json` | SHA-256 of every file in this folder |

Nothing here is loaded by the game; `.gdignore` keeps Godot from importing it.

---

## 0. Summary

1. **One record per job** in `content/jobs/<id>.json`, plus an append-only
   ledger of star bits and tombstones (ARCHITECTURE §4).
2. **Compiled, not parsed.** `tools/content_build.py --write` compiles the
   records into typed `const` GDScript under `scripts/generated/`; `--check` runs
   inside the document gate both CI runners already execute (§5).
3. **Derived, not pinned.** Masks, counts, the star clamp, loop bounds,
   checkpoint bounds, room tables and probe expectations come from the
   catalogue, which removes the bit-18 trap and the six pinned probes (§6, §8).
4. **Plumbing once.** A small JobKit (help ladder, guided target, exact voice,
   reward ceremony, Roshan-at-work, imp contest, phase checkpoint) and a
   `JobSurface` contract replace per-job wiring and at least 77 lines that
   branch on a literal career ID (§7).
5. **Strangle, don't rewrite.** Each registry moves behind the catalogue only
   after the generated value is proven equal to the literal it replaces (§11).

The prototype extractor already reproduces all eleven hard-coded values from
per-job records (`data/derivation_check.json`). Adding a permanent job falls
from about 25 hand-edited files to about four plus assets (ARCHITECTURE §12).

**Read in this order:** ARCHITECTURE §0, §4–§8 and §11, then sections 1–3
below.

## 1. Invariants

- **No big rewrite.** Packages are mechanical and behaviour-preserving unless
  their text says otherwise (only JP7 does, and it is owner-gated): exact
  behaviour, state ownership and save compatibility stay identical; the trusted
  suite is green before and after; a probe failure after a step reverts the
  step (`DL-CODE-06`).
- **Saves.** Keys are only added, with defaults (`DL-SAVE-01`). Star bits 0–17
  keep their meaning; tombstones 4, 9 and 14 stay forever (`DL-SAVE-06`); every
  save written before JP0 loads unchanged after JP8.
- **Medium and platform.** True 2D only (`DL-MED-01`), Mobile renderer, Godot
  4.7.2-stable. No runtime JSON parsing is introduced.
- **Protected content.** Nothing under `assets/book/`, `assets/audio/voices/` or
  `assets/characters/friends/` changes; generated voices never overwrite
  protected recordings (`DL-SND-05`, `DL-SND-11`).
- **Growth law.** No package adds lines to `scripts/main.gd` beyond a delegation
  it nets out in the same branch (`DL-CODE-01`, `DL-CODE-11`).
- **Workflows.** No package edits `.github/workflows/` unless the owner names it;
  new checks run from invocations CI already makes.
- **Roles.** Claude wrote this; Codex implements it and produces any image or
  generated audio; the owner decides section 4.

## 2. Work packages

One branch per package, `codex/<topic>` off fresh `origin/dev`; merge to `dev`
only with CI green at the branch's exact head. Each package: impact record
(rules `DL-CODE-05`, `DL-CODE-06`, `DL-SAVE-01`, `DL-SAVE-06` and whichever
apply), ledger rows for new Markdown, gates, report.

**JP0 — Content model and proof (pure addition).**
- Create `content/` with `.gdignore`, `content/jobs/<id>.json` for all 15 live
  jobs and `content/jobs/_ledger.json` (start from `data/extracted_catalog.json`
  and the examples; re-read every value at your head).
- Write `tools/content_build.py` (`--write`, `--check`, `--explain`) and its
  tests; generate `scripts/generated/job_catalog_data.gd` with compatibility
  shapes identical to today's literals; add `scripts/job_catalog.gd`.
- Add an equality check inside `scripts/probe_opera.gd` that compares each
  generated shape with the literal it will replace.
- Hook `--check` into `tools/audit_document_authority.py` (as it imports
  `navigation_issues`).
- **Gate:** every registry in ARCHITECTURE Appendix A marked derivable compares
  equal; the checker fails on the seven injected faults in ARCHITECTURE §8;
  suite green; no runtime file reads the generated script yet.
- **Non-goals:** no consumer switches; no behaviour change.

**JP1 — Save bounds first (owner-critical trap).**
- `scripts/save_state.gd`: the masks, count, `range(18)` loop and the four
  `262143` clamps read `JobCatalogData`; one generic checkpoint validator keyed
  by job replaces the two copies, with the phase bound derived from each job's
  phase count; keys are registered from the catalogue.
- `scripts/opera_house.gd`: completion clean-up iterates the catalogue's
  checkpoint keys instead of `finished == 17` and the `"geologist"` test.
- **Gate:** save probes byte-stable; legacy fixtures (`0xFFFF`, `0x3FFFF`) load
  identically; a test with a synthetic ledger entry at bit 18 proves no
  corruption; the frozen `opera_progress` migration path (`clampi(…, 0, 16)` and
  `(1 << opera_prog) - 1`) is untouched.

**JP2 — Consumers switch, one per commit.** `opera_house.gd` constants;
`castle_career_routes.gd` room table and crests; `opera_house_venue_2d.gd`
floor list; `opera_career_world_2d.gd` phase, finale, station, alias and goal
tables and the specialist-surface choice; `opera_competition.gd`;
`opera_mastery.gd`; `opera_performance_plan.gd`; `opera_performance_overlay.gd`;
`audio_director.gd` voice routing; `living_world_catalog.gd` Opera rows;
Chapter 2 masks, guide order and valid modes.
- **Gate:** probe transcripts byte-stable per commit; the replaced literal is
  deleted in the same commit.
- **Non-goals:** no renamed IDs, no visible text change (living-world names stay
  as recorded in each record unless the owner chooses otherwise).

**JP3 — Probes derive their expectations.** Replace the pinned values in
`scripts/probe_opera.gd`, `probe_opera_2d.gd`, `probe_living_world.gd`,
`probe_opera_nursery.gd`, `probe_opera_mastery.gd`, `probe_chapter2.gd` and
`probe_opera_diegetic_paths.gd` with catalogue queries; add the conformance
loop inside `probe_opera` (ARCHITECTURE §8).
- **Gate:** on a throwaway branch, an extra hidden practice record changes no
  probe line and passes; deleting a live job's voice key or room makes a probe
  fail.

**JP4 — Tools read the catalogue.** `tools/build_area_music.py` expected IDs,
`tools/audit_opera_roshan_animation.py` career list,
`tools/audit_audio_quality.py` folders and categories,
`tools/audit_stage_pathfinding.py` IDs (no more regex over `ACTS`); run the
stage-path `--check` from the document gate.
- **Gate:** the Geologist cue and the Geologist and Teacher costume sheets are
  covered; each tool fails on an injected missing entry.

**JP5 — JobKit, then capabilities.** Add `scripts/jobkit/` components that wrap
today's behaviour exactly (help, guided target, exact voice, reward ceremony,
phase checkpoint, Roshan-at-work); then move the `career_id` branches of
`opera_career_world_2d.gd` to capability lookups, one family per commit.
`ImpContest` lands with the imp-contest implementation, not before.
- **Gate:** byte-stable probes per commit; the count of literal career-ID
  branches in the host falls to zero (specialist surfaces may keep their own).
- **Non-goals:** no change to help timings, voices, rewards or feel; the
  gesture-surface decomposition stays WP-B2 of the 2026-08-26 handoff.

**JP6 — Documents.** Generated job tables and counts in the job playbook and
design reference (refinement handoff Stage J and WP-7); rewrite the playbook
around the record; with owner approval, amend `DL-INT-07`, `DL-SAVE-06` and
`DL-QA-12` to cite the catalogue instead of numbers; record progress in
`MA-DOC-006`'s history.
- **Gate:** document gate green; no pinned job count left in rule text.

**JP7 — Job-ID completion (owner-gated).** Additive completion keyed by job ID,
mirroring existing bits. Only if the owner answers Q3 yes.

**JP8 — Mode Platform alignment.** When design 08 reaches M2, the Opera entry
becomes one `ModeRegistry` row and the Job Platform is its internal registry.

## 3. Acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| AC-1 | `tools/content_build.py --check` runs in the document gate on both CI runners and fails on each injected fault | Test log; CI log |
| AC-2 | JP0 equality holds for every derivable registry in ARCHITECTURE Appendix A | Probe output |
| AC-3 | No literal job count, mask, star clamp or room-table copy remains in runtime scripts or probes outside `scripts/generated/` | Grep report in the PR |
| AC-4 | A synthetic bit-18 entry round-trips through save, load and normalise without setting any other bit; checkpoint bounds come from phase counts | Save test |
| AC-5 | Probe transcripts are byte-stable across every JP1–JP5 commit | Transcript diffs |
| AC-6 | The conformance loop covers every live job and fails when a job loses a voice key, room or star write | Probe output with injected faults |
| AC-7 | Growth-law test for jobs: on a throwaway branch a new hidden practice job needs only its record, a trivial surface and `--write`; the suite passes | Throwaway branch diff |
| AC-8 | The Geologist music cue and the Geologist and Teacher costume sheets are inside their gates; the stage-path check runs in CI | Tool logs |
| AC-9 | The host has no literal career-ID branches | Grep count |
| AC-10 | `scripts/main.gd` is not larger; no workflow file changed unless the owner named it | `git diff --stat` |
| AC-11 | Legacy saves load identically after every package | Save fixtures |
| AC-12 | Stage J WP-J1 of the refinement handoff is satisfied by JP0, and `MA-DOC-006` history records it | Finding history |

## 4. Owner questions (Codex proceeds on the default and reports it)

| # | Question | Default |
|---|---|---|
| Q1 | Author job data as JSON compiled to `const` GDScript? (design 08 §9 point 4 prefers a `const` script; this keeps that property and lets tools read the data) | Yes |
| Q2 | Put the source data in a top-level `content/` folder hidden from Godot? | Yes |
| Q3 | Add job-ID-keyed completion now (JP7)? | No; derived bounds remove the trap without a schema change |
| Q4 | Start before the Mode Platform's M0? | Yes; the two fit together (ARCHITECTURE §10) |
| Q5 | Run the content check from the document gate rather than a new CI step? | Yes (no workflow edit) |
| Q6 | Put the conformance loop inside `probe_opera` rather than a new trusted probe? | Yes (no roster or workflow edit) |
| Q7 | Unify living-world names with job titles? | No; keep today's names in each record |
| Q8 | Which synthetic voice engine do new job lines use? | Record each existing job's engine; new jobs use the Roshan voice layer the game prefers at runtime |

## 5. Sequencing with other work

- **JP0 and JP1 can start now.** JP0 adds files only; JP1 removes the bit-18
  trap before anyone adds a sixteenth career.
- **JP2 waits for, or rebases onto,** the in-flight Opera work: imp contests
  (`DL-INT-14`), the four-floor venue port, and the Day One and Day Two alpha
  repairs. Per-job files avoid conflicts once JP2 lands.
- **Refinement handoff.** Stage J WP-J1's catalogue is JP0's content layer
  (`content/jobs/`, compiled), not a documentation-only `design/reference/jobs.json`;
  WP-J2's playbook is written after JP3; WP-J4's dry run uses the record.
- **Imp contests.** Implement them on top of JP1 (derived checkpoint bounds) and
  JP5 (`ImpContest`), so twelve contests share one runner.
- **Design 08.** M0–M6 proceed unchanged; JP8 joins M2.

## 6. Gates and delivery

Before every push, from the repository root:

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
python -B tools/content_build.py --check            (from JP0 on)
```

plus the focused probes named in each package, the full `scripts/ci.sh`, and
CI green at the branch's exact head. Re-run
`docs/handoffs/codex_job_platform_architecture_2026-09-30/tools/extract_job_catalog.py`
before JP0 to confirm the baseline still derives cleanly.

## 7. Stop and escalate if

- A step would change behaviour, a save value, a visible name or a voice.
- Any generated value differs from the literal it replaces and the difference
  is not a known drift listed in `data/derivation_check.json`.
- A package needs `.github/workflows/`, `CLAUDE.md`, `AGENTS.md`, `SECURITY.md`,
  `.claude/` or `.codex/`, and the owner has not named it.
- A star bit, tombstone or job ID would be reused, removed or renamed.
- An in-flight branch has changed the same registry since you started: rebase
  and re-prove equality rather than overwrite.
- Disk space is below what a checkout or import needs (drive C: reached 0 bytes
  free on 2026-09-30).

## 8. Report (per package, in the PR and the impact record)

- **Implemented:** files, records, generated outputs, literals deleted.
- **Machine-verified:** exact commands and results at the named head; the
  equality and byte-stability evidence.
- **Outstanding:** owner questions by number, packages not started, and every
  visual, device, child and owner gate that remains open.
