# Codex handoff — retire stale audit content and consolidate outdated audits into reference documents (2026-09-30)

**Owner request (2026-09-30):** *"Identifying stale elements of master audit
are the next steps, there are many outdated audits in this repo that should be
streamlined and truncated into reference documents."*

**From:** Claude (analysis and recommendations only; no game change). **To:**
Codex (implementation). **Owner:** answers the questions in section 6 and
accepts the result.

**Status:** `PROPOSED / CANDIDATE`, revision 1. This packet recommends; it
grants no visual, device, child or owner acceptance and changes no finding
lifecycle. The one register change made with it is the new tracking finding
[`MA-DOC-007`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-007)
(P2, `CONFIRMED_OPEN`). Every wave still follows `CLAUDE.md`, `AGENTS.md` and
the master-audit development contract (`DL-AUTH-05`, `DL-AUTH-06`,
`DL-AUTH-07`): impact record, ledger rows, gates, CI, then integration into
`dev`.

**Evidence baseline:** measured at `dev`
`6fc2f48e527dc20286d25455785abd9680d57368`; this packet's branch starts at
`ce0331738970205a5aead4d3e0258eb7873a1642`, which changes no file the
measurements read. Line numbers are guides: re-locate by heading at your head.

Authority: subordinate to the [design language](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
the [master audit](../../../audit/MASTER_AUDIT_2026-08-09.md) (sections 9–13),
the [development contract](../../../design/AUDIT_DEVELOPMENT_CONTRACT.md) and
the [document ledger](../../../design/05_DOC_LEDGER.md). Where they disagree
with this packet, they win until the owner changes them.

## What is in this folder

| Path | What it is |
|---|---|
| `README.md` | This handoff: waves, acceptance, owner questions, gates |
| `STALENESS_AUDIT.md` | The findings: what is stale in the master audit, the finding register and the repository's audits, the contradictions, and the rules at risk |
| `REFERENCE_PLAN.md` | The fourteen reference documents to build, their outlines with source line ranges, the classification of every document, and the root cleanup |
| `data/master_audit_staleness_register.json` | All 65 elements of the master audit with class, current truth and disposition |
| `data/stale_findings.json` | 24 open findings and the register preamble: stale text, line and current truth |
| `MANIFEST.json` | SHA-256 of every file in this folder |

Nothing here is loaded by the game; `.gdignore` keeps Godot from importing it.

## 0. Summary

Three problems, three outcomes:

| Problem today | Outcome when this handoff is done |
|---|---|
| The master audit's current content is about 27% of its bytes; 21 elements state stale facts and 9 present superseded decisions as current | The master audit holds current content, generated status and pointers; sealed evidence sits verbatim in an archive file; superseded decisions are dated log entries |
| 24 open findings and the register preamble state things that are no longer true; one finding's acceptance now fails | Every open finding carries a dated history entry with the truth at your head; nothing in history is rewritten |
| About 204 outdated documents sit beside 76 current ones; the root holds 196 Markdown files | Fourteen reference documents hold the durable knowledge; outdated documents live in an archive with their file names; the root holds about six Markdown files |

The full evidence is in [STALENESS_AUDIT.md](STALENESS_AUDIT.md); the target
documents are in [REFERENCE_PLAN.md](REFERENCE_PLAN.md).

## 1. Coordination with the refinement handoff

The [master-audit refinement handoff](../codex_master_audit_refinement_2026-09-30/README.md)
(revision 4) already plans some of this work. Do each shared step once, in
whichever handoff runs first, and reuse the result in the other.

| This packet | Refinement handoff | Rule |
|---|---|---|
| W2 sealed evidence and obsolete process (10 elements) | WP-1 evidence archive | One pass; the register's element list is WP-1's input |
| W2 stale facts (21 elements) | WP-2 live status | Replace with the generated block or a link |
| W2 superseded decisions (9 elements) | WP-3 owner decision register | Each becomes a dated decision entry |
| W3 finding refresh (`data/stale_findings.json`) | WP-10 findings re-baseline | The file is WP-10's priority list |
| R08 `CANON.md` | WP-4 canon register | One document |
| `design/reference/` location for the references | Section 3 reference shelf | Same shelf |
| W5 reference checks | WP-11 checks | Extend WP-11 to the `REF_*` files |

Never run W2 and WP-1 at the same time on the master audit. Stage J of the
refinement handoff (the job-game playbook) is owner-critical and is not
blocked by anything here; R01 must not duplicate the playbook's recipe.

## 2. Invariants

- **Move, never edit, sealed evidence.** Byte-for-byte except line endings,
  under a heading naming its origin, with stub headings left so every anchor
  resolves.
- **Never rewrite a finding's history** (`DL-AUTH-02`). Append dated entries;
  move lifecycle only with evidence. Do not change a baseline or acceptance
  number to make a failing check pass.
- **Archived files keep their file names**, so a name cited in prose or a
  code comment can still be found.
- **Hash-recorded files do not move or change** (STALENESS_AUDIT section 7)
  unless their packet is republished as a full handoff cycle.
- **No game runtime file, protected path or high-risk file changes**, except
  where the owner names it (section 6). `assets/audio/voices/VOICE_MANIFEST.md`
  is inside a protected path.
- **Archived ledger rows** move to 🟡 or ⚪, and their notes must not contain
  `BINDING_`, `SUPPORTING_CURRENT` or `PROPOSED_CANONICAL`, or the document gate
  will keep treating them as current authority.
- **The change gate compares without rename detection**, so a move shows as
  a deletion plus an addition. Every impact record lists both paths.
- **References never restate rules.** They link to `DL-*` IDs, hold no commit
  hashes, CI run IDs, durations or hand-copied counts, and list contradictions
  as open questions instead of resolving them silently.

## 3. Waves

### W0 — Stage 0: re-measure and coordinate (read-only)

Re-run the live facts in STALENESS_AUDIT section 2 at your head (2D scanner,
`main.gd` lines, probe counts and rosters, Opera table, music catalogue,
document gate). Re-check each item marked "not verified" in the data files.
Check whether refinement WP-1, WP-2, WP-3 or WP-10 has already landed and
adjust W2 and W3 to verification only. Confirm the hash-recorded list against
the published manifests. **Gate:** a short note in the impact record listing
what changed since `6fc2f48e`.

### W1 — Save the rules that live only in documents marked for archive

STALENESS_AUDIT section 6 lists nine rules found nowhere in design 01, 02,
03, 06 or `AGENTS.md`. Promote seven into design 06 as new rule IDs in their
family, worded as in the source, with the source path and date: ingredient
direct manipulation, medal rules, the swipe exception, the single-leaf rule,
the art rubric and its hard caps (with the scoring-governance answer on who
may give 5/5), the 2026-06-25 licensing decision, and the overdraw budgets.
Two are contradicted elsewhere and go to the owner instead: act length (new
`OQ-ACT-LENGTH`) and the stuck-help ladder (existing `OQ-HELP`); their source
documents stay in place until answered. **Gate:** document gate ALL OK; each
new rule cites its source; no source document of a promoted rule moves
before its rule lands. **Non-goal:** no runtime change.

### W2 — Clean the master audit

Apply each element's disposition from
[`data/master_audit_staleness_register.json`](data/master_audit_staleness_register.json):

| Class | Do |
|---|---|
| Current (19) | Keep |
| Stale fact (21) | Replace with the generated live-status block or a link (refinement WP-2); never re-type a count |
| Sealed evidence (9) | Move verbatim to `audit/archive/MASTER_AUDIT_2026-08-09_SEALED_EVIDENCE.md` (the refinement handoff's file); leave stub headings |
| Superseded decision (9) | Write a dated decision entry, then remove the current-tense text, linking the entry |
| Duplicate of the finding register (6) | Delete, leaving one line pointing at the finding record |
| Obsolete process (1) | Move to the archive file |

Fix the ten most misleading statements (STALENESS_AUDIT section 2) first.
Keep the section 5 table rows and sections 9 and 12 in place: the document
gate parses them and checks the Godot baseline there. **Gate:** both
governance gates ALL OK; a script shows every removed sealed line exists
verbatim in the archive file; no link points at a heading that no longer
exists.

### W3 — Refresh the finding register

For each entry in [`data/stale_findings.json`](data/stale_findings.json):
re-run the finding's own reproduction at your head, append a dated history
entry with the current truth, and update reproduction commands that name
moved lines or files. Lifecycle moves only with evidence; the candidates are
`MA-OPERA-002` (crown painted out; owner review pending) and the parts of
`MA-OPERA-012` the 2026-08-29 route-card move and the 2026-09-24 owner
decision changed. `MA-CODE-004`: record that its own command now reports 456
keys against the 409 baseline; do not edit the baseline. Refresh the register
preamble's counts. If refinement WP-10 runs, do this inside it. **Gate:**
every listed finding has a dated entry or an explicit "not re-verified:
reason"; the diff touches only history, reproduction, evidence and
preamble text.

### W4 — Archive the 119 outdated documents

Move each "archive now" document (REFERENCE_PLAN section 3) to
`audit/archive/docs/<domain>/<same file name>`; add `!/audit/archive/` to
`.gitignore`. In the same commit: update the ledger row's path, state and
note; fix inbound links (`design/10_CHAPTER_REFERENCE_LIBRARY.md`,
`design/chapters/NORTHERN_ICE_WORLD.md`, the review-kit README, the master
task index); update tools that read a moved path. Move a review kit with its
handoff. Leave code comments that name a file: the name still finds it.
Record the move under the next unused change-group ID (`CHG-033` at the
measured head; rollback class `documentation_migration`), as the change
log's maintenance rule requires for a new behaviour. Work in
batches of about 20 files per commit, grouped by domain. **Gate:** document
gate ALL OK with no DOC072; `git grep` finds no path to a moved file outside
the archive, the ledger and history; tools that read moved paths still run.

### W5 — Build the fourteen references, then archive what they absorb

One reference per pull request, in this order: R01 Opera careers, R03 Day
One, R02 Castle, R06 Art, R12 Cinematics, R09 Audio, R13 Performance, then
R04, R05, R07, R08, R10, R11, R14. Follow REFERENCE_PLAN section 1 and the
outline; re-read each source range at your head; list every contradiction the
reference meets as an open question with its default. After the reference
lands, archive the documents it absorbed using the W4 procedure. Ledger state
🟣 until the owner accepts the reference, then 🔵. **Gate:** each reference
has a scope, sources (old and archive paths) and a last-verified date; a grep
finds no commit hash, run ID, duration or hand-copied count in it.

### W6 — Root cleanup and wrong operational documents

Make the coordinated moves in REFERENCE_PLAN section 4 with their referrers.
`MEDALS.md` and `STUFFIE_COMPANIONS.md` stay at the root while `CLAUDE.md`
names them (owner-gated). Correct the wrong operational documents in
STALENESS_AUDIT section 8 that are not owner-gated: `docs/ANDROID_RELEASE.md`
(dev publishing, version code from the commit count), `BACKUP.md` (the real
backup status), and design 00, 03 and 04 (through the live-status block).
Leave `CLAUDE.md`, `AGENTS.md` and `VOICE_MANIFEST.md` unless the owner names
them. Delete the two delete candidates only with owner approval; otherwise
archive them. **Gate:** at most six root Markdown files plus any the owner
kept; document gate ALL OK.

### W7 — Keep it fresh

- Each reference records the date it was last re-verified. The live-status
  tool lists every reference whose source code or documents changed after
  that date (refinement WP-2 "stale findings" metric, extended).
- A new audit names the reference it feeds. The task that lands the audit
  moves its durable conclusions into that reference or records why not, then
  marks the audit 🟡 or ⚪ (`DL-PLAN-06`: historical evidence stays separate
  from current requirements).
- Contradictions found later become `OQ-*` entries, never silent picks
  (`DL-AUTH-01`, `DL-AUTH-04`).

Write these as guidance in the
[development contract](../../../design/AUDIT_DEVELOPMENT_CONTRACT.md) only if
the owner accepts it (section 6, Q8); until then they are recommendations.

## 4. Contradictions: how each one is settled

STALENESS_AUDIT section 5 lists 47 contradictions with a suggested
resolution. Apply the ones settled by a newer owner decision, a rule, the
code that ships or a generated count, and record the reason in the
reference. Send the ten marked "Owner question" to the open-question
register (refinement WP-3) and block nothing else on them:

| Contradiction | Question ID |
|---|---|
| Opera act length | `OQ-ACT-LENGTH` (new) |
| Credit for a wrong answer | `OQ-WRONG-CREDIT` (new) |
| Candy Maker's place | `OQ-ARBORIST-DAY2` |
| Colour meanings for props and doors | `OQ-COLOUR`, `OQ-DOOR-SET` |
| Boss time ceilings | `OQ-BOSS-CEILING` |
| Idle re-prompt timings | `OQ-HELP` |
| Baked lighting in painted flats | `OQ-BAKED-LIGHT` (new) |
| Voice engine per job | `OQ-VOICE-ENGINE` (new) |
| Shot card V1 or V2 | `OQ-SHOT-CARD` (new) |
| Cinematic frame rate | `OQ-CINE-FPS` (new) |

Three more need a code check before they are settled: spotlights on tiled
worlds, the Back route from Dream House rooms, and whether the Chapter 2
stuffie ballet goals block its promised payoff. Each becomes a finding or an
owner question once checked.

## 5. Acceptance criteria

| ID | Criterion | How to show it |
|---|---|---|
| AC-1 | None of the ten misleading statements remains as a present-tense claim in the master audit | Grep for each listed phrase; each hit is in the archive or labelled historical |
| AC-2 | Every element in the register has its disposition applied, or a recorded reason | Register copy with an `applied_in` commit per element |
| AC-3 | Every entry in `data/stale_findings.json` has a dated history entry at your head; no history text was removed | Diff of the register shows additions only in history |
| AC-4 | `MA-CODE-004`'s baseline and acceptance are unchanged; the 456-key result is recorded | Diff and history entry |
| AC-5 | Each of the nine orphaned rules is in design 06 with its source, or has an `OQ-*` and a source document still in place | Rule list against design 06 |
| AC-6 | The 119 "archive now" documents are in `audit/archive/docs/` with their file names; zero broken links | Document gate ALL OK, no DOC072 |
| AC-7 | Each landed reference follows REFERENCE_PLAN section 1 and its absorbed documents are archived only after it | Grep for hashes, run IDs and durations; ledger history |
| AC-8 | The root holds at most six Markdown files plus those the owner kept | `ls *.md` |
| AC-9 | No hash-recorded file moved or changed | Compare against each published `MANIFEST.json` |
| AC-10 | No runtime, protected or high-risk file changed unless the owner named it | `git diff --name-only` against the protected and high-risk lists |
| AC-11 | Tools that read moved paths still run | Run each named tool or its test |
| AC-12 | Each of the 47 contradictions is applied with a reason or has an `OQ-*` | Contradiction list with outcome column |
| AC-13 | `MA-DOC-007` acceptance is met and recorded in its history | The finding record |

## 6. Owner questions (Codex proceeds on the default and reports it)

| # | Question | Default |
|---|---|---|
| Q1 | Who writes the reference text? | Claude drafts each reference from its outline as a documentation change (analysis is Claude's role); Codex does the moves, link and tool updates, ledger rows and gates. If the owner prefers one agent, Codex writes from the outlines |
| Q2 | Where does the archive live? | `audit/archive/docs/<domain>/` on `dev`, file names kept. Not a separate branch: agents must still find the history |
| Q3 | Promote the seven uncontested orphaned rules into design 06? | Yes, as new rule IDs citing their sources; act length and the help ladder wait for the owner |
| Q4 | Accept the suggested resolutions in STALENESS_AUDIT section 5? | Yes for those settled by a newer owner decision, a rule, the code or a generated count; the ten owner questions go to the register |
| Q5 | Delete the two tool-output files? | No; archive them unless the owner approves deletion |
| Q6 | Order relative to the refinement handoff | Refinement Stage 0 and Stage J first; then this packet's W0–W3 merged with WP-1, WP-2, WP-3 and WP-10 in one pass; then W4–W7 |
| Q7 | Correct `CLAUDE.md`, `AGENTS.md` and `VOICE_MANIFEST.md` (owner-gated files)? | No, unless the owner names them; the findings and this packet record the truth meanwhile |
| Q8 | Add the W7 freshness guidance to the development contract? | Recommendation only until the owner accepts it |

## 7. Gates and delivery

Before every push, from the repository root:

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
```

plus the tools that read a moved path, and the static section of
`scripts/ci.sh` when a tool changes (it runs several pinned-count gates). CI
on the branch must be green at its exact head before merging into `dev`.

## 8. Stop and escalate if

- A document marked for archive is read by a tool, probe, workflow or
  manifest not listed in STALENESS_AUDIT section 7.
- A move would change a hash-recorded file.
- A rule exists only in a document and conflicts with another rule: do not
  pick one; add an owner question.
- An archived document holds canon missing from the canon register.
- Passing the document gate would need a check weakened rather than a
  document fixed.
- Another branch has edited the master audit, design 06, the ledger or the
  finding register since you started: rebase and re-verify, never overwrite.
- Disk space is below what a checkout or import needs.

## 9. Report (per wave, in the pull request and the impact record)

- **Implemented:** files moved (old to new path), references written, rules
  promoted, findings refreshed, questions added.
- **Machine-verified:** exact commands and results at the named head.
- **Outstanding:** owner questions answered or pending (by number and
  `OQ-*`), findings not re-verified with the reason, and every visual,
  device, child and owner gate that remains open.
