# Codex handoff — master-audit refinement: one design reference for the next generation (2026-09-30)

**Owner request (2026-09-30):** *"What are the recommended refinements for the
master audit to help design the next generation of the game, and use it as a
easy reference for the game to draw from to maintain consistency between
designs? Design as codex handoff."*

**From:** Claude (analysis, measurements and recommendations only; no game
change). **To:** Codex (implementation). **Owner:** answers the questions in
section 8 and accepts the result.

**Status:** `PROPOSED / CANDIDATE`, revision 3 (2026-09-30): adds Stage J —
a job-game playbook, job catalogue checker, takeover kit and cold-start dry
run — after the owner called takeover readiness critical. Revision 2 corrected
wording in revision 1 (`0bbf8b7c`). This packet recommends; it grants no
visual, device, child or owner acceptance and changes no finding lifecycle.
Every package still follows `CLAUDE.md`, `AGENTS.md` and the master-audit
development contract (`DL-AUTH-05`, `DL-AUTH-06`, `DL-AUTH-07`): impact
record, ledger rows, gates, CI, then integration into `dev`.

**Evidence baseline:** `dev` at `55032e88936b22723fd9af5282c61ba6696b3d43`
(2026-09-29). Every number below was measured there by
[`tools/measure_reference_health.py`](tools/measure_reference_health.py),
which is read-only and re-runnable, or by a named grep. Facts marked
*(sweep)* come from read-only document sweeps and must be re-read at your head.

Authority: subordinate to the [design language](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
the [master audit](../../../audit/MASTER_AUDIT_2026-08-09.md) (sections 9–13),
the [development contract](../../../design/AUDIT_DEVELOPMENT_CONTRACT.md) and
the [document ledger](../../../design/05_DOC_LEDGER.md). Where they disagree
with this packet, they win until the owner changes them.

## What is in this folder

| Path | What it is |
|---|---|
| `README.md` | This handoff: diagnosis, target design, work packages, acceptance, owner questions |
| `data/composition.json` | Size and evidence density of every section of the master audit, design 06 and design 00 |
| `data/duplicated_evidence_tokens.json` | Commit and CI-run identifiers copied across Markdown files |
| `data/live_vs_documented_counts.json` | Live measurements next to the 35 present-tense counts that disagree with them |
| `data/finding_staleness.json` | Every open finding with its last history date and the code churn since then |
| `data/owner_decisions.json` | Every dated owner-decision mention in tracked Markdown (98 mentions, 49 files, 30 dates) |
| `data/rule_inventory.json` | All 183 `DL-*` rules: family, size, volatile facts, citation counts |
| `seed/canon_seed.json` | Starting canon entries (characters, places, story) with sources and 15 conflicts |
| `seed/patterns_seed.json` | Nineteen starting design patterns with maturity, rules, reference code and anti-patterns |
| `seed/tokens_seed.json` | Twenty-seven design constants with their rules, code anchors and drifting variants |
| `seed/open_questions_seed.json` | Nineteen pending owner questions consolidated from current handoffs, design documents and findings |
| `tools/measure_reference_health.py` | The measurement script (standard library only) |
| `MANIFEST.json` | SHA-256 of every file in this folder |

Nothing here is loaded by the game; `.gdignore` keeps Godot from importing it.

**Companion audit (revision 3):** [`audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md`](../../../audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md)
answers whether the master audit can drive job-game development (it cannot
yet), holds the interim job-game recipe, and defines the closure of
[`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006),
the finding that tracks this work in the master audit.

---

## 0. Summary

**The short answer.** The master audit is an excellent *ledger* and a poor
*reference*. The design rules that keep designs consistent are good but small
(183 rules, about 8,600 words) and they are buried under evidence, copied
counts that have gone stale, and owner decisions scattered across 49 files.
The recommended refinement is to separate three things that are currently
mixed together, and to make the numbers generated instead of hand-copied:

```text
        READ FIRST                      FOLLOW                        PROVE
 ┌────────────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
 │ 1. DESIGN REFERENCE    │   │ 2. RULES               │   │ 3. AUDIT LEDGER        │
 │ design/11 + reference/ │◄──│ design/06 (DL-*)       │◄──│ master audit, findings │
 │ canon, patterns,       │   │ unchanged IDs, no      │   │ status, evidence,      │
 │ tokens, engines, owner │   │ evidence preamble,     │   │ closure; generated     │
 │ decisions, design card │   │ tagged core/domain/    │   │ live status; sealed    │
 │ no commits, no counts  │   │ process                │   │ evidence archived      │
 └────────────────────────┘   └────────────────────────┘   └────────────────────────┘
   references point left only: the ledger cites rules, rules cite the reference;
   the reference never cites a commit, a CI run or a hand-copied count
```

**The seven refinements.**

1. **Give designers a front door.** A new `design/11_DESIGN_REFERENCE.md` —
   pillars, the game map, the Day/Chapter vocabulary, canon at a glance,
   patterns, tokens, engines, open owner questions and a ten-step "how to
   design something new" — each answer at most two links from the task index.
2. **Write the canon down once.** A canon register (characters, places,
   objects, story facts, cut content) with approved art paths and hashes,
   voice facts, sources and an explicit conflict list. Today there is none;
   15 live contradictions were found.
3. **Name the patterns.** A pattern library (`PAT-*`) for the solutions the
   game should reuse: one guided target, highlight-from-art, one pointer,
   colour meanings, help ladder, Roshan-does-the-job, exit/return, reward
   ceremony, friendly boss, and so on. Fifteen recurring defect classes were
   each fixed one area at a time; only one was fixed game-wide.
4. **Turn design numbers into tokens.** One machine-readable file for touch
   size, text size, latency, loudness, outline width, background resolution,
   help timings and colour meanings, with a checker that reports where code or
   documents drift (touch minimums currently read 110, 112, 128 and 160).
5. **Record owner decisions in one register.** Dated `ODR-*` records plus one
   open-question list (`OQ-*`), so a designer can see what the owner has
   decided and what is still pending. The 2026-09-24 decision to retire
   `DL-INT-12` is recorded only in a handoff and a repair plan today.
6. **Move evidence out of the way and generate status.** Move the sealed
   evidence verbatim into an archive with stub headings (the evidence-dense
   sections hold 88% of the master audit's bytes), generate a live-status block from tools, and stop
   hand-copying counts: 35 present-tense counts in the authority documents,
   including `CLAUDE.md`'s "513 model files", disagree with the tree (live: 0).
7. **Re-baseline the findings for the next generation.** 46 of 56 open
   findings have no history since 2026-09-01; re-verify each at the current
   head, refresh the scorecards to the game that ships now (Day One, Grand Puff,
   Day Two, Chapter 3 route, the Opera House), and route new work through a
   one-page **design card** that cites canon, pattern and token IDs.
8. **Make it a script for job games and a takeover kit (owner-critical,
   2026-09-30).** A maintained job-game playbook routed from the task index, a
   machine-checked catalogue of every job, a start-here takeover kit (roles,
   operations loop, real backup status, environment), and a cold-start dry run
   by a fresh agent. Today no route or recipe exists, and a naive next career
   would corrupt star progress (the bit-18 clamp trap in the companion audit).

**What Codex builds, in order.** Stage 0 re-measure and coordinate → Stage J
job-game playbook and takeover kit (owner-critical) → Stage 1
make room (archive, live status) → Stage 2 build the reference (register,
canon, patterns, tokens, engines, card) → Stage 3 rules and findings hygiene →
Stage 4 guardrails in the existing gates → Stage 5 owner-gated extras. See
section 6.

**What does not change.** Authority precedence, every `DL-*` and `MA-*` ID,
finding history, the sealed evidence text (it moves, it is not edited), the
mandatory contract text in `CLAUDE.md`/`AGENTS.md`/`tools/audit_development.py`,
protected content, and every acceptance gate. No game runtime file changes.

---

## 1. What is wrong today (verified at `dev` `55032e88`)

| # | Problem | Evidence | Why it hurts design consistency |
|---|---|---|---|
| R1 | The master audit is a ledger, not a reference | 2,335 lines, about 269 KB, 944 commit/run/duration tokens. 88% of its bytes sit in sections with at least 10 such tokens per 100 lines (`data/composition.json`). Only the planning entry, taxonomy, protocol, field list and satisfaction gate are low-density — about 12% | A designer who opens the "start here" document reads CI run numbers before any design guidance |
| R2 | The rules start at line 249 | Design 06 opens with a 248-line preamble holding 104 commit IDs, 29 CI run IDs and 17 durations before `DL-AUTH-01`; design 00 repeats the same evidence in its preamble and "Current medium decision" | The good part (the rules) is the hardest part to find |
| R3 | Evidence is copied, not linked | `51d0abc0` appears 125 times in 11 files; `441adf35` 108 times in 11; run `31763879294` 46 times in 10 (`data/duplicated_evidence_tokens.json`). The ledger itself keeps a table of rules "stated more than once … so a future edit updates every copy" | Every copy must be updated by hand, so copies drift |
| R4 | Hand-copied counts have gone stale | 35 present-tense counts disagree with the tree (`data/live_vs_documented_counts.json`): `CLAUDE.md:110` and `AGENTS.md:114-115` say 513 model files and 70 production 3D files — the scanner reports 0 and 52; `CLAUDE.md:162` says `main.gd` has 8,465 lines — it has 9,826; the audit and design 03/04 say 106 probe scripts — there are 137. Rules drift too: `DL-INT-07` and `DL-SAVE-06` say 13 careers while `scripts/opera_house.gd:13-15` ships 15 (`ACTIVE_STAR_MASK := 0x3BDEF`); `DL-SND-06` says 42 new cues while the music manifest lists 44 files and 60 OGG files ship | A designer planning against the documents plans against a game that no longer exists |
| R5 | The findings register lags the game | 46 of 56 open findings have no history entry since 2026-09-01; 16 cite code that has changed since their last entry (`data/finding_staleness.json`). Scorecards still rate the Reef, retired on 2026-09-09. *(sweep)* At least 10 of 53 impact records repaired defects that never reached the register, and `MA-OPERA-012` was not updated after the 2026-08-29 route-card fix | The "what is broken" list cannot guide the next generation's priorities |
| R6 | Owner decisions are scattered and some are unapplied | 98 dated owner-decision mentions in 49 files across 30 dates; 18 of those dates never appear in design 06 (`data/owner_decisions.json`). The 2026-09-24 direction to build the four-floor Opera House and retire `DL-INT-12` lives only in [the visual-polish handoff](../codex_visual_polish_2026-09-25/README.md) and the repair plan. Handoff-local question IDs collide (Day One OD-1..OD-9, door OD-1..OD-6) | Nobody can answer "what has the owner decided about X?" from one place |
| R7 | There is no canon bible | *(sweep, key items verified)* Canon lives in about 30 sources in four tiers. The only cast list in a design master (`design/01_GAME_DESIGN.md:471-481`) has about ten lines and omits Rumi, Grand Puff, the rainbow friend and the Ember King and Prince. The fullest store, the Grok builder `DATABASE.json` (49 entities, 36 events), is cinematic-only, frozen on 2026-09-14 and unclassified. Fifteen contradictions are listed in `seed/canon_seed.json`, for example Roshan's colours (01:480 versus the approved atlas prompt), a blanket instead of two dust bunnies in a Day One storyboard prompt, and Grand Puff "deflates into a small cuddly puff" in a ledger-binding document | New chapters re-derive characters from whichever file the designer happens to open |
| R8 | Patterns are re-solved per area | *(sweep)* Fifteen recurring defect classes; only one (a card duplicated in its background, `MA-VIS-007`) was fixed game-wide with a register and a detector. At least nine pointer styles appear in one Day One arc and `ghost_hand` is referenced by 14 scripts; colour cues carry at least four conflicting meanings; five help ladders; Back/exit changed in at least six incidents in four weeks; at least four celebration implementations; the boss cue style was revised four times in eight days | Every new room invents its own pointer, colours, timings and exit |
| R9 | Pattern documents exist but are not routed | *(sweep)* `design/07_CASTLE_DOOR_LANGUAGE.md`, `design/BOSS_SPLASH_DESIGN_LANGUAGE.md` and `design/BUNNY_BOSS_REBUILD_2026-09-05.md` are binding, yet none is linked from design 06 or the task index. The index has no route for UI/navigation, doors/pointers, bosses or rewards. No spec exists for pointers, reward ceremonies, Back/exit, draw-order roles, help ladders, colour meanings or highlight geometry | A binding rule nobody is routed to behaves like no rule |
| R10 | Next-generation planning has to dig | *(sweep)* No filled chapter brief exists; the reference library was last reviewed at `775ceee1` (2026-09-05) and misses the lawn finale, boss engine, Teacher, Racer, Painter, Tree Book, Comfy Games and story clips. `DL-CODE-11`/`DL-CODE-12` describe a Mode Platform that has not started (`scripts/platform/` and `tools/audit_structure.py` are absent). The chapter probes run in neither trusted roster (0 matches in `scripts/ci.sh` and `.github/workflows/probes.yml`). The room list, the portrait-to-friend map and voice-key prefixes live only in code. Battle of the Bands (commissioned 2026-09-20) is not on `dev` | Each new chapter starts with a research project instead of a design |
| R11 | Paperwork concentrates on narrative, not status | Since 2026-09-01: 153 non-merge commits on `dev`, 33 edited the master audit, 53 edited the ledger, 52 touched documentation only — yet 46 findings got no lifecycle entry. `DL-AUTH-05`..`07` are cited by 51 of 53 impact records as boilerplate, while 19 rules were never cited by any record or finding | Effort goes into re-telling evidence instead of keeping the reference true |
| R12 | The gates hard-code the current layout | See Appendix E: four fixed paths, two anchors, eleven required task routes, the `## 5.`–`## 6.` window, sections 9 and 12, and a byte-identical contract mirrored in three files. Ordinary links are checked for file existence only, not anchors | A careless restructure breaks CI, or silently breaks inbound anchors across the repo |
| R13 | Nothing lets an agent build a job game or take over | See the [companion audit](../../../audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md): no task-index route or recipe for a job game; adding a career touches about 25 files and six probes with hand-pinned counts; `opera_stars` is clamped to 18 bits in four places in `scripts/save_state.gd`, so a career at bit 18 would mark every career complete; two voice engines with no rule; the atlas gate covers 13 of 15 careers; every weekly backup run has failed; the images rule is missing from `AGENTS.md` | The owner's goal — an agent taking over development — cannot be met or tested |

---

## 2. Invariants that do not change

- **Precedence** stays: security and protected-asset/save/release rules →
  dated owner decisions → engine/operational rules → design 06 → current
  domain documents → historical evidence (`DL-AUTH-01`).
- **IDs are permanent.** No `DL-*`, `MA-*` or `CHG-*` ID is renumbered,
  reused or deleted. New reference IDs (`PAT-*`, `TOK-*`, `ODR-*`, `OQ-*`,
  canon IDs) follow the same rule.
- **History is never rewritten** (`DL-AUTH-02`). Sealed evidence is *moved
  verbatim* with its original wording and SHAs; it is not summarised,
  corrected or re-dated. Finding history gains dated entries only.
- **File paths and anchors stay**: `audit/MASTER_AUDIT_2026-08-09.md`,
  `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`,
  `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`, `design/05_DOC_LEDGER.md`,
  `#0-planning-entry` and `#development-task-index`. Numbered section headings
  in the master audit and design 06 keep their numbers and titles, because
  other documents link to their anchors and the gate does not check those.
- **The mandatory contract text** in `CLAUDE.md`, `AGENTS.md` and
  `tools/audit_development.py` is untouched unless the owner names WP-12.
- **No game change.** Nothing under `scripts/`, `scenes/`, `assets/`,
  `project.godot` or export presets changes in Stages 0–4. Protected paths
  (`assets/book/`, `assets/audio/voices/`, `assets/characters/friends/`,
  `attic/gabby/`) are never touched.
- **Acceptance stays honest.** The audit remains `IN_PROGRESS` /
  `UNSATISFIED`; no reference entry, pattern maturity or green checker grants
  visual, device, child or owner acceptance (`DL-QA-07`, `DL-PLAN-05`).
- **Canon is recorded, not invented.** Where sources conflict, the register
  records the conflict and the default; major character or plot choices stay
  with the owner (`DL-PLAN-01`).

---

## 3. Target shape: three shelves

### 3.1 What may live on each shelf

| Shelf | Holds | Must not hold | Changes when |
|---|---|---|---|
| **1. Design reference** — `design/11_DESIGN_REFERENCE.md` and `design/reference/` | Pillars, game map and vocabulary, canon, patterns, tokens, engines, owner decisions and open questions, how-to-design recipe, consistency checklist | Commit IDs, CI run IDs, durations, hand-copied measurements, acceptance claims | Canon, a pattern, a token or an owner decision changes |
| **2. Rules** — design 06 | Normative `DL-*` text, section intros, "see" links to patterns and tokens | Evidence preambles, run IDs, commit history, snapshot counts (outside owner-pinned identity hashes such as `DL-MOT-09`) | The owner decides, or a recurring defect class earns a rule |
| **3. Audit ledger** — master audit, findings, change log, archive | Status, triage, evidence, closure, change history, generated live status | Design guidance that is not already a rule or pattern | Evidence or lifecycle changes |

### 3.2 File plan

| Path | New or changed | Purpose |
|---|---|---|
| `design/11_DESIGN_REFERENCE.md` | New | The front door (section 4.1) |
| `design/reference/canon.json` and `CANON.md` | New | Canon register; the Markdown is generated from the JSON |
| `design/reference/PATTERNS.md` and `patterns.json` | New | Pattern library; the JSON is the checked index |
| `design/reference/tokens.json` | New | Design constants; rendered as a table in design 11 |
| `design/reference/engines.json` | New | Reusable mechanic families and the game map |
| `design/reference/owner_decisions.json` and `OWNER_DECISIONS.md` | New | Owner decision register and open questions |
| `design/templates/DESIGN_CARD_V1.md`, `design/templates/CHAPTER_BRIEF_V2.md` | New | One-page card; brief V2 cites reference IDs (V1 stays) |
| `design/12_JOB_GAME_PLAYBOOK.md`, `design/templates/JOB_CARD_V1.md` | New (Stage J) | The maintained job-game script and its one-page job card |
| `design/reference/jobs.json` | New (Stage J) | Catalogue of every job game, checked against the code registries |
| `tools/design_reference.py` and its tests | New | Render generated blocks, `--check` them, validate IDs, paths, hashes and token drift |
| `tools/audit_live_status.py` and its tests | New | Generate `audit/status/LIVE_STATUS.json` and the live-status block |
| `audit/archive/MASTER_AUDIT_2026-08-09_SEALED_EVIDENCE.md` | New | Verbatim home for moved evidence |
| `audit/MASTER_AUDIT_2026-08-09.md`, design 06, 00, 01, 03, 04, 09, 10, ledger | Changed | Section 5 dispositions |
| `tools/audit_document_authority.py`, `tools/audit_development.py` | Changed | Guardrails, called from the existing CI invocations (section 6, WP-11) |

The names are defaults; owner question Q1 may rename them. Keep the number of
new files small: one front door, one folder.

### 3.3 How the game draws from it

"The game draws from the reference" is meant literally, in three steps:

1. **Documents draw from it now.** Design 06, chapter briefs and handoffs cite
   `PAT-*`, `TOK-*`, canon and `ODR-*` IDs instead of restating facts;
   `tools/design_reference.py --check` fails on an undefined ID.
2. **Checks draw from it now.** The checker compares token values with the
   code constants listed as anchors (for example `MIN_TOUCH` in
   `scripts/storybook_ui.gd:23`) and canon art paths with their hashes, and
   reports drift. It is read-only; drift is reported, not auto-fixed.
3. **Runtime may draw from it later.** Reading `tokens.json` or a generated
   GDScript constants file from runtime code is a behaviour-identical refactor
   that belongs in a separate, owner-approved package (WP-13), gated by the
   probe suite.

---

## 4. The design reference — specification

### 4.1 Front door: `design/11_DESIGN_REFERENCE.md`

A short book (target 10–14 printed pages) with generated tables between
`<!-- GENERATED:<name> -->` markers. Outline:

| § | Title | Content | Source |
|---|---|---|---|
| 1 | Who we design for | The child, one finger, non-reader, no fail, short sessions, family voices and book art are irreplaceable, true 2D, Mobile renderer — each line cites its rule (`DL-AGE-01`..`08`, `DL-MED-01`, `DL-PERF-01`, `DL-ASSET-03`) | Prose |
| 2 | The game at a glance | Day One → Grand Puff → Day Two birthday → Chapter 3 route → planned Northern; rooms and what lives in each; retired places; Day/Chapter vocabulary table | Generated from `canon.json` and `engines.json` |
| 3 | Canon at a glance | Cast, places, story facts, never-list; link to `CANON.md` | Generated |
| 4 | Patterns | `PAT-*` index with maturity and one-line promise; link to `PATTERNS.md` | Generated from `patterns.json` |
| 5 | Design tokens | The numbers, their rules and their status | Generated from `tokens.json` |
| 6 | Engines to reuse | Mechanic families, where they live, which probe drives them, maturity | Generated from `engines.json` |
| 7 | How to design something new | The ten steps below | Prose |
| 8 | Consistency checklist | The fifteen questions a reviewer asks of any design card | Prose |
| 9 | Owner decisions and open questions | Latest decisions and every pending question with its default | Generated from `owner_decisions.json` |
| 10 | Where evidence lives | One paragraph pointing to the ledger, findings, impact records and archive | Prose |

**How to design something new (section 7 of the front door):**

1. Read the pillars and the owner-decision list; check `OQ-*` items that block you.
2. Fill a design card (`DESIGN_CARD_V1.md`); one per activity, beat or room.
3. Cast from canon only; list any minor addition as a proposal (`DL-PLAN-01`).
4. Choose patterns by ID; write down every deliberate deviation and why.
5. Use tokens; a different number is a deviation, not a local choice.
6. Reuse an engine before inventing one (`DL-PLAN-04`); name its probe.
7. List every spoken line with speaker, key and "exists / missing" (`DL-SND-13`).
8. Plan art reuse first (`DL-ASSET-01`, `DL-PLAN-03`); new art goes to Codex
   image generation with the style-matching protocol and owner sign-off.
9. Name save milestones as additive keys with defaults (`DL-SAVE-01`).
10. Write the acceptance plan in V0–V7 terms and the owner questions it needs.

### 4.2 Owner decision register and open questions

`design/reference/owner_decisions.json` holds two lists.

**Decisions** (`ODR-YYYYMMDD-NN`, dated so they never collide): `id`, `date`,
`decision` (one sentence), `quote` (short, when a verbatim source exists),
`scope`, `supersedes`, `rules` (`DL-*` affected), `canon` (IDs affected),
`status` (`RECORDED` → `RULES_UPDATED` → `IMPLEMENTED` → `ACCEPTED`, or
`SUPERSEDED`), `source` (path:line or commit).

**Open questions** (`OQ-<TOPIC>`): `question`, `source_ids` (the original
handoff-local IDs, kept for traceability), `default` (what work proceeds on),
`blocks` (the only work it may hold up), `asked_in`, `answered_by` (an `ODR-*`
once answered).

Seeds: `data/owner_decisions.json` lists every dated mention to deduplicate;
`seed/open_questions_seed.json` consolidates 19 pending questions. Minimum
backfill: every decision dated 2026-08-09 or later, including 2026-09-05
(chapter delegation, Northern planning), 2026-09-06 (Roshan travels to each
job, `DL-INT-02`), 2026-09-11 (animation language), 2026-09-16 (GitHub
delivery), 2026-09-19/20 (picture-book art, `DL-ASSET-08`), 2026-09-23 (Day One
story clips and Grand Puff canon, `DL-CIN-16`), 2026-09-24 (four-floor Opera
House and retiring `DL-INT-12`; Baby Eagle backpack-free; Claude recommends and
Codex implements), 2026-09-29 (Tree Book corrections; Candy Maker reserved for
a later section) and 2026-09-30 (door guidance rewrite requested).

### 4.3 Canon register

`design/reference/canon.json` is the source; `CANON.md` is generated from it.
Entity IDs: `CHR-*` characters, `PLC-*` places, `OBJ-*` recurring objects and
companions, `STY-*` story facts and beats, `CUT-*` removed or cut content.

| Field | Content |
|---|---|
| `id`, `names` | Stable ID; display name; aliases including code keys (for example the speaker key used for Baby Eagle) |
| `status` | `ACTIVE`, `PLANNED`, `RETIRED`, `REMOVED_IP_HOLD`, `CUT` |
| `role` | One or two sentences; relationships to other IDs |
| `identity` | Approved art paths with SHA-256; `must` traits (for example one tail); `never` traits (for example a backpack on Baby Eagle) |
| `voice` | Speaker; recording type (family, synthetic, stock); protected flag; key prefixes; "no invented voice" where the owner said so |
| `movement` | Movement-profile path or `GAP` (`DL-MOT-10`) |
| `appears_in` | Days/chapters, rooms, activities |
| `decisions`, `sources` | `ODR-*` IDs; path:line with ledger authority |
| `conflicts` | `CANON-C*` records with both sources, the default and the status |

Seed: `seed/canon_seed.json` — 21 entities and 15 conflicts. Coverage target:
every character and place named in design 01, 06, 07, 09 and 10, the chapter
documents and the Day One clip manifest. The Grok builder `DATABASE.json`
stays the cinematic database; the canon register links to its entity IDs
rather than copying shot data.

### 4.4 Pattern library

`design/reference/PATTERNS.md` holds one entry per pattern; `patterns.json`
indexes them for the checker.

| Field | Content |
|---|---|
| `id`, `name`, `maturity` | `STANDARD` (one shared implementation, driven by a trusted probe), `CANDIDATE` (a written spec or one implementation), `GAP` (needed, not written), `RETIRED` |
| Promise | What the child experiences, in one sentence |
| Use when / not when | Boundaries |
| Recipe | Steps, with token IDs for every number |
| Required cues | Voice line, pointer, sound, timing |
| Reference implementation | Paths and functions; the probe that drives them |
| Anti-patterns | The defects that taught the pattern, with finding or handoff IDs |
| Rules, open question | `DL-*` IDs; `OQ-*` if the owner must choose |

Seed (`seed/patterns_seed.json`): nineteen patterns — `PAT-GUIDE-01` one
guided target, `PAT-GUIDE-02` highlight follows the painted object,
`PAT-GUIDE-03` one pointer vocabulary (GAP), `PAT-GUIDE-04` colour meanings
(GAP), `PAT-HELP-01` help ladder (GAP), `PAT-JOB-01` Roshan does the job,
`PAT-OBJ-01` truthful object change, `PAT-OBJ-02` a card owns its pixels once,
`PAT-LAYER-01` draw-order roles (GAP), `PAT-VOICE-01` the exact line for every
objective, `PAT-EXIT-01` one way back (GAP), `PAT-REWARD-01` one celebration
ceremony (GAP), `PAT-BOSS-01` friendly boss with a guaranteed finish,
`PAT-STORY-01` story clip between scenes, `PAT-BUILD-01` persistent
construction, `PAT-JOURNEY-01` landmark journey with exact return,
`PAT-UI-01` picture-first interface, `PAT-FOLLOW-01` companion follower,
`PAT-ACT-01` character acting profile.

Route the existing pattern documents through the library rather than
rewriting them: `design/07_CASTLE_DOOR_LANGUAGE.md` under `PAT-GUIDE-01`/`02`,
`design/BOSS_SPLASH_DESIGN_LANGUAGE.md` and `design/BUNNY_BOSS_REBUILD_2026-09-05.md`
under `PAT-BOSS-01`, `audit/stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md`
under `PAT-JOB-01`, the movement language under `PAT-ACT-01`, and the
interactive/background ownership protocol under `PAT-OBJ-02`.

For each `GAP`, write the best current option as the entry's proposal, cite
the competing proposals, and link the `OQ-*`. Do **not** unify runtime code in
this handoff; the pattern entry becomes the target for later implementation
work (for example the clone families in `MA-CODE-003`).

### 4.5 Tokens

`design/reference/tokens.json`: `id`, `value`, `unit`, `strength`
(`MUST`/`SHOULD`/`MAY`/`GAP`), `rules`, `code_anchors` (path:line or symbol),
`variants` (other values found), `decision` (`ODR-*` when the owner settles a
variant). Seed: `seed/tokens_seed.json`, 27 tokens. Rule text keeps its
numbers for now; section 5.2 explains how rules and tokens stay in step.

### 4.6 Engines and the game map

`design/reference/engines.json`: family, main files, registry-like entry
(Opera `ACTS`/`PHASES`, `ChapterTwoPartyPlan`, none), probe and whether it is
in a trusted roster, consumers (rooms, days), maturity (`SHIPPED`,
`PROTOTYPE`, `DORMANT`, `RETIRED`), known limits. Appendix D is the seed. The
game map (days, chapters, rooms, activities) is generated from `canon.json`
places plus `engines.json` consumers and shows status honestly: for example
the friend games (seek, dolls, melody, fetch) as `DORMANT` since the Reef was
retired *(sweep)*.

### 4.7 Design card and chapter brief V2

`design/templates/DESIGN_CARD_V1.md` is one page per activity, beat or room:
premise and child desire; canon used (IDs) and proposed minor additions;
place; patterns used and deviations; token deviations; engine reused; lines
needed (speaker, key, exists/missing); art reuse and gaps (Codex image
generation with style matching); save keys; acceptance plan (V0–V7); open
questions (`OQ-*`). `design/templates/CHAPTER_BRIEF_V2.md` is V1 plus a table
of design cards and the canon/pattern/token sections; V1 stays for history.

Worked examples, both labelled as examples and neither commissioning work:
backfill one card for an integrated beat (the Chapter 2 Farmer berries, whose
facts already exist in design 10) and one planning card for the Northern
restaurant customer-order activity (planning is owner-authorized; runtime is
not). Unknowns stay written as unknowns.

---

## 5. Refinements to the existing documents

### 5.1 Master audit — section by section

| Section | Today | Disposition |
|---|---|---|
| 0 Planning entry | 99 lines; 15 "Scoped … supplement" paragraphs accumulating | Rewrite to at most 60 lines: purpose; "start with design 11"; the generated live-status block; current priorities (link §13); open owner questions (link); where evidence lives. Replace the supplement paragraphs with a generated "recent changes" table built from impact records (id, date, one-line scope, findings touched, link) |
| Task index | 11 required routes | Keep all required routes and section links; add routes for design reference, canon, patterns, tokens, UI/navigation, doors and pointers, bosses and encounters, rewards, owner decisions, and the evidence archive. Put design 11 in the "Every task" and "New chapter" rows first |
| Sealed snapshot metadata | 137 lines, 74 evidence tokens | Move verbatim to the archive; leave a three-line pointer |
| 1 Executive verdict and scorecards | 472 lines; scorecards pinned to 2026-08-13 | Keep headings 1.1–1.7 as stubs; move the text verbatim; add a short current verdict and scorecards generated from `audit/status/scorecard.json` produced by the re-baseline (WP-10), covering the surfaces that ship now, with retired surfaces in their own table |
| 2 Taxonomy | Clean | Keep |
| 3 Authority | Map missing the reference shelf; `VISUAL_AUDIT_TOOL.md` listed as `BINDING_DOMAIN` while the ledger says 🟠 `SUPPORTING_CURRENT` | Add the reference shelf and the register; reconcile the mismatch; move evidence sentences out of 3.3 |
| 4 Evidence | 537 lines | Stub; move verbatim |
| 5 Triage index | Rows carry commit and run evidence | Keep the section (the gate parses it); shorten each row to issue plus closure requirement and let the finding record hold evidence; refresh during WP-10 |
| 6 Supporting evidence | 92 lines, the densest section | Stub; move verbatim |
| 7 Superseded ideas | Useful never-list | Keep; mirror the design-relevant rows into the reference never-list by link |
| 8 Expanded acceptance notes | 228 lines | Stub; move verbatim; link each note from its finding's `evidence` field |
| 9, 10, 12 | Protocol, fields, gate | Keep (the gate checks the Godot baseline in 9 and 12); update 12's stale wording during WP-10 |
| 11 Tools and documentation control | Mixed | Keep the requirements; move the evidence paragraphs |
| 13 Repair order | Evidence-laden | Rewrite as a short prioritised list of findings and patterns; move the evidence verbatim |
| 14 Change history | 68 rows, the most evidence-dense | Keep rows dated 2026-09-01 or later; move older rows verbatim |
| Stage pathfinding inventory | Appended after §14 | Move into §11 or §3 as a pointer |

Every moved block goes to `audit/archive/MASTER_AUDIT_2026-08-09_SEALED_EVIDENCE.md`
under a heading that names its original section and line range at the moving
commit, so every old citation can still be followed.

### 5.2 Design 06

- Replace the 248-line preamble with a header of at most 20 lines: document
  ID, status, precedence pointer, audience, "start with design 11". Move the
  preamble verbatim to the archive.
- Add `design/reference/rules_index.json`: each rule's class — `CORE` (design
  grammar: AGE, READ, UI, VIS, LAY, most INT, MOT, SND, TYPE), `DOMAIN`
  (activity or system contracts: `DL-INT-07`..`13`, `DL-MOT-08`/`09`,
  `DL-SND-06`, `DL-SAVE-06`, `DL-QA-12`/`13`, the cinematic family) or
  `PROCESS` (AUTH, QA, PLAN, CODE) — plus pattern and token links. Render it in
  design 11; do not edit rule text to add tags.
- Add one "See also" line under each numbered section pointing to its
  patterns and tokens.
- Rule text changes only through the owner: record the `DL-INT-12` retirement
  as `ODR-20260924-*` now, and let the four-floor Opera port amend the rule
  (see the visual-polish handoff, item 3). Record `DL-INT-07`/`DL-SAVE-06`
  (13 careers versus 15 in code) and `DL-SND-06` (42 cues versus 44) as drift;
  open a finding if re-verification confirms it (section 8, Q5).
- Rules that name a platform that does not exist (`DL-CODE-11`, `DL-CODE-12`)
  get a dated note in the rules index: "target; not implemented at
  `<head>`". The text stays.

### 5.3 Design 00–04, 09, 10 and the ledger

- **00, 01, 03, 04:** move evidence paragraphs to the archive and replace
  copied counts with a pointer to the live status. Design 01 §6 (cast) points
  to the canon register.
- **09 chapter guide:** point planning at design 11, the design card and brief
  V2; keep the delegation charter unchanged.
- **10 reference library:** becomes the *examples and evidence* shelf behind
  the pattern library. Refresh its missing entries (lawn finale, boss engine,
  Teacher, Racer, Painter, Tree Book, Comfy Games, story clips) and its
  "available implementation" section (the Mode Platform has not started).
- **Ledger:** fix the stale notes the sweep found (the pool beat order row, the
  companion row, the `DUST_BUNNY_BOSS_2026-08-02.md` Grand Puff row, the
  voice-manifest row, the repeated-rules row saying thirteen careers belong in
  Castle rooms (stale since the 2026-09-24 decision), and "design 07" where the
  Mode Platform is design 08); add rows for every new Markdown file; classify
  design 11 and the register as `CANONICAL_CURRENT` only after the owner
  accepts them (until then 🟣 `PROPOSED / CANDIDATE`).

### 5.4 Paperwork diet

The refinement must lower the cost of every future change, not raise it.

| Stop doing | Start doing |
|---|---|
| Copying evidence into the master audit, design 06 and 00–04 | Evidence lives in exactly three places: the impact record (per change), the finding history (per defect), the archive (sealed) |
| Hand-updating counts | `tools/audit_live_status.py --write` regenerates the block; `--check` runs in CI only when the master audit changed in the diff, so code-only changes carry no documentation work |
| Writing "Scoped … supplement" paragraphs | The recent-changes table is generated from impact records |
| Listing `DL-AUTH-05`..`07` in every impact record | The record gate treats them as implied; a record still needs at least one other applicable rule |
| Re-deriving canon, colours, sizes and timings per handoff | Cite `CHR-*`, `PAT-*` and `TOK-*` IDs; add optional impact-record fields `patterns`, `canon`, `owner_decisions` and `sibling_sweep` (the sites of the same pattern that were checked) |

---

## 6. Work packages

One branch per stage, `codex/<topic>` off fresh `origin/dev`; merge to `dev`
only with CI green at the branch's exact head. Each package: impact record,
ledger rows, gates, then the report in section 11.

### Stage 0 — re-measure and coordinate (read-only)

**WP-0.** Run `python -B docs/handoffs/codex_master_audit_refinement_2026-09-30/tools/measure_reference_health.py --out <scratch>`
at your head and diff it against `data/`. Check free disk space first — on
2026-09-30 drive C: of this machine reached 0 bytes free with 316 registered
worktrees; reuse an existing worktree rather than creating a full new checkout.
List open branches that edit the master audit, ledger or design 06 (at
`55032e88`: `origin/rescue/windows-2026-09-30-day2-audit`,
`origin/ccr-ba906acd-1aepcb` (Day Two jobs), `origin/codex/mermaid-roshan-picture-book`,
`origin/rescue/opera-four-floors-20260906-worktree`, plus the Battle of the
Bands work) and plan WP-1 for a quiet window. **Gate:** a short note in the
first PR with the re-measured numbers and the branch list.

### Stage J — job-game playbook and takeover kit (owner-critical; runs right after Stage 0)

Owner direction 2026-09-30: the purpose of this work is for an agent to take
over development of Mermaid Roshan, starting with future job games, and an
audit ensuring that is included is critical. The audit is
[`audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md`](../../../audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md);
the tracking finding is
[`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006).
Stage J closes that finding. It does not wait for Stages 1–5: the playbook
cites today's documents and code first, then switches its citations to canon,
pattern and token IDs as WP-4 to WP-6 land (WP-J5).

**WP-J1 Job catalogue and checker.** Create `design/reference/jobs.json`: one
entry per job game that exists in code or is planned. Fields: `id`, name,
extension path (Opera career row, venue scene, Day Two job, room job),
owning room or venue, act index and star bit (or its own save key), surface
script, phases and their verbs, imp-contest status (`DL-INT-14`), voice
prefix and required voice keys, music cue, Roshan career atlas path and
SHA-256, prop/backdrop art, driving probes and whether each is in both trusted
rosters, design document, status (`LIVE`, `PRACTICE`, `PROTOTYPE`,
`PLANNED`, `RETIRED`, `CUT`). Add a checker (inside the existing document
gate, see WP-11) that compares the catalogue with the code registries the
audit lists in its section 3 and fails when a live act, mask bit, room route,
voice prefix, music cue or trusted probe is missing or disagrees. **Gate:**
the checker passes at your head and fails on three injected faults (an
unregistered act, a wrong star bit, a job with no trusted probe).

**WP-J2 Job-game playbook.** Write `design/12_JOB_GAME_PLAYBOOK.md` from the
interim recipe in the audit's section 4. Every step names its inputs, the
exact files and symbols it changes, the gate that proves it, who does it
(owner, Claude, Codex), and its stop points (owner approval of a new job's
premise and room; image generation by Codex only; protected voices never
altered). Include the job formula (acts, phases, one-finger verbs, help,
rewards, imp contest), the four extension paths with when to use each, and a
job design card template (`design/templates/JOB_CARD_V1.md`). Route it from
the master-audit task index row "New job game" and from the planning entry.
**Gate:** every file, symbol, command and tool named in the playbook exists at
your head (checked by script); the task-index route resolves.

**WP-J3 Takeover kit.** Add a "New developer: start here" section to the
front door (design 11) or to the playbook if design 11 does not exist yet:
reading order, glossary (Day One, Day Two, Chapter, career, job, act, phase,
star bit), roles (owner, Claude, Codex, Grok; who may change the game, build
images, release), the operations loop (branch, impact record, gates, CI,
merge to `dev`, dev APK, promotion only on the owner's word), backups and
their real status, security boundaries, environment setup and known machine
hazards (disk space, shared checkout). Correct any operational claim the audit
found stale. **Gate:** each linked command or file exists; each stale claim in
the audit's sections 8 and 9 is corrected or listed as an open question.

**WP-J4 Cold-start dry run.** Give a fresh agent session only the repository
and a one-line job commission chosen by the owner (default: a practice-only
job that changes no shipped behaviour, for example a second patient in the
Tree Book or a Northern restaurant planning card). The agent produces a job
card and a complete build plan using only the playbook and catalogue. A
reviewer scores it against the audit's checklist (section 10). Record the
result, every question the agent had to ask, and every step it could not find
in the audit's history table, then fix the playbook. **Gate:** no
undocumented step remains; the owner accepts the dry-run output.

**WP-J5 Upgrade to reference IDs.** After WP-4 to WP-6 land, replace prose
facts in the playbook and catalogue with canon, pattern and token IDs, and
re-run the WP-J1 checker.

**Closing `MA-DOC-006`:** move it to `FIXED_PENDING_VERIFICATION` when WP-J1
to WP-J3 are merged green; to `VERIFIED_FIXED` only after the WP-J4 dry run
passes and the owner accepts it. Record both transitions in the finding
history and the master-audit index.

### Stage 1 — make room (documentation only, mechanical)

**WP-1 Evidence archive.** Scope: the master audit sections in 5.1 marked
"move", the design 06 preamble, the design 00 preamble and "Current medium
decision" evidence, and evidence paragraphs in 01/03/04. Do: create the
archive; move each block byte-for-byte (except line endings) under a heading
naming its origin; leave stub headings with the same text so every anchor
resolves; keep section 5 table rows and sections 9 and 12 in place. **Gate:**
`audit_document_authority.py` and `audit_development.py --base auto` ALL OK;
a script shows every removed line exists verbatim in the archive; `git grep`
finds no link to a heading that no longer exists. **Non-goals:** no rewording
and no lifecycle changes.

**WP-2 Live status.** Scope: `tools/audit_live_status.py` plus tests,
`audit/status/LIVE_STATUS.json`, the generated block in the planning entry,
and the recent-changes table. Measure: GAME2D categories and status;
`main.gd` lines and scripts over 3,000 lines; probe scripts and both trusted
rosters; findings by severity and lifecycle; stale findings (no history for
21 days and referenced code changed); Markdown inventory and ledger rows;
register and open-question counts. Replace the copied counts in the master
audit and design 00–04 with the block or a link (`CLAUDE.md` and `AGENTS.md`
wait for WP-12). **Gate:** `--check` green; `measure_reference_health.py`
reports zero stale present-tense counts outside `CLAUDE.md`/`AGENTS.md`.

### Stage 2 — build the reference

**WP-3 Owner decision register.** Backfill from `data/owner_decisions.json`
(read each source; deduplicate), seed the open questions from
`seed/open_questions_seed.json`, and map every handoff-local OD number to an
`OQ-*` without renaming it in its source. **Gate:** every dated owner-decision
mention in the current-authority documents resolves to an `ODR-*` (the
checker reports the rest).

**WP-4 Canon register.** Start from `seed/canon_seed.json`; re-read every
source; add art paths with hashes and voice facts; record every conflict with
its default. **Gate:** coverage target in 4.3 met; every art path exists and
its hash matches; no conflict silently resolved.

**WP-5 Pattern library.** Start from `seed/patterns_seed.json`; write each
entry; route the existing pattern documents; add task-index routes. **Gate:**
each of the fifteen recurring classes in Appendix B maps to a pattern entry
with rules, reference or `GAP`, and anti-pattern evidence.

**WP-6 Tokens.** Start from `seed/tokens_seed.json`; add exact code anchors
(for example typography role sizes and ducking constants); render the table.
**Gate:** the drift report lists every variant; nothing in code changes.

**WP-7 Engines, game map and front door.** Write `engines.json` from
Appendix D, generate the game map and vocabulary table, and write design 11.
**Gate:** the new-designer test (Appendix F) — each of the twelve questions
answered from design 11 within two links; record the answers and links in the
PR.

**WP-8 Design card and brief V2.** Templates plus the two worked examples;
point design 09 and 10 at them. **Gate:** both examples cite only defined IDs
and list their unknowns.

### Stage 3 — rules and findings hygiene

**WP-9 Rules index.** Classify all 183 rules, add "See also" lines, record the
volatile-fact rules, and add dated notes to `DL-CODE-11`/`DL-CODE-12` in the
index. **Gate:** every rule classified; the checker validates every pattern
and token link.

**WP-10 Findings re-baseline ("next-generation baseline" round).** For each of
the 56 open findings: re-verify with its own reproduction at your head (the
Stage 0 rule of the [2026-08-26 handoff](../../../CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md));
append a dated history entry with the result; move lifecycle only with
evidence. Priority order: the 16 whose referenced code changed
(`MA-CI-004`, `MA-PERF-003`, `MA-CODE-005`, `MA-PERF-002`, `MA-SAVE-001`,
`MA-AUDIO-001` first); the 2D cluster (`MA-2D-002` counts are 509/65 in the
record, 0/52 live); the Opera cluster against the 2026-09-24 decision and the
15-career code (`MA-OPERA-012` after the 08-29 route-card fix); `MA-CI-003`
(137 probe scripts, not 106); `MA-CODE-001` (9,826 lines). Open new findings
only for confirmed defects with child impact or rule drift — candidates are
listed in section 8, Q5. Produce `audit/status/scorecard.json` for the
surfaces that ship now and regenerate the §1 scorecards from it; rewrite §13.
**Gate:** every open finding has a dated re-verification entry or an explicit
"not re-verified: reason"; `audit_document_authority.py` ALL OK.

### Stage 4 — guardrails inside the existing gates

**WP-11 Checks.** Implement `tools/design_reference.py` (render, `--check`,
ID/path/hash validation, token drift report) and extend
`tools/audit_document_authority.py` so that:

- `ODR-*`, `PAT-*`, `TOK-*`, `OQ-*` and canon IDs cited by current-authority
  documents must be defined (like the existing undefined-rule check);
- the reference shelf and design 06 rule sections contain no CI run IDs,
  durations or backticked commit SHAs (evidence and archive files are exempt;
  owner-pinned identity hashes are allowed by an explicit list);
- generated blocks match their sources;
- the impact-record gate accepts the optional fields in 5.4 and treats
  `DL-AUTH-05`..`07` as implied.

Call the new checks from the functions that `scripts/ci.sh` and
`.github/workflows/probes.yml` already run, so no workflow file changes. Add
unit tests and a stress control for each new check. **Gate:** tests green;
each check proven to fail on a deliberately broken fixture.

### Stage 5 — owner-gated

**WP-12 Entry points** (only if the owner names it when assigning this
handoff; high-risk files, called out in the commit message). Replace the stale
counts in `CLAUDE.md` and `AGENTS.md` ("513 model files and 70 production 3D
files"; "8,465 lines") with a pointer to the live status; optionally add
design 11 to the mandatory contract, changing all three synchronized copies
together.

**WP-13 Runtime tokens** (separate owner approval). Have runtime code read
token values from one generated source with identical values; probe-gated,
behaviour-identical.

---

## 7. Acceptance criteria

| ID | Criterion | How to show it |
|---|---|---|
| AC-1 | The master audit is at most about 70 KB and its planning entry at most 60 lines; design 06 rules begin before line 60 | `data/composition.json` regenerated |
| AC-2 | Zero CI run IDs, durations or backticked commit SHAs in design 06 rule sections, design 00–04 current sections and the reference shelf | WP-11 check |
| AC-3 | Zero stale present-tense counts outside `CLAUDE.md`/`AGENTS.md` (zero everywhere if WP-12 runs) | `measure_reference_health.py` |
| AC-4 | The live-status block is generated and `--check` passes | CI log |
| AC-5 | Every dated owner decision since 2026-08-09 has an `ODR-*`; every open question has an `OQ-*`, a default and a blocking scope; no ID collisions | WP-11 check plus register review |
| AC-6 | Canon covers every character and place in the target sources; every conflict is listed with a default; art paths and hashes verify | WP-11 check |
| AC-7 | Every recurring class in Appendix B maps to a pattern entry; the task index routes UI/navigation, doors and pointers, bosses, rewards and the reference | Review plus navigation gate |
| AC-8 | The new-designer test passes: all twelve questions answered from design 11 within two links | PR table |
| AC-9 | Every open finding has a dated re-verification entry or a stated reason | Findings diff |
| AC-10 | No moved evidence was edited; every old anchor still resolves | WP-1 verification script |
| AC-11 | `audit_document_authority.py` and `audit_development.py --base auto` ALL OK; unit tests green; CI green at the merged head | Logs |
| AC-12 | No game runtime file changed in Stages 0–4; protected paths untouched | `git diff --stat` |
| AC-13 | `design/12_JOB_GAME_PLAYBOOK.md` is routed from the task index and every file, symbol, command and gate it names exists at the merged head | WP-J2 existence check |
| AC-14 | `design/reference/jobs.json` covers every job in code; its checker runs in the existing document gate and fails on the three injected faults | WP-J1 test log |
| AC-15 | The takeover kit exists and every stale claim in sections 8 and 9 of the companion audit is corrected or listed as an open owner question | Review against the audit |
| AC-16 | A cold-start dry run passes the companion audit's section 10 checklist, the owner accepts it, and `MA-DOC-006` moves to `VERIFIED_FIXED` | Dry-run record and finding history |

The reference becomes `CANONICAL_CURRENT` only after the owner accepts it
(`DL-QA-06`); until then it is 🟣 `PROPOSED / CANDIDATE`.

---

## 8. Owner questions (Codex proceeds on the default and reports it)

| # | Question | Default |
|---|---|---|
| Q1 | Name and location of the reference | `design/11_DESIGN_REFERENCE.md` plus `design/reference/` |
| Q2 | Day/Chapter vocabulary: is Day One Chapter 1 and Day Two Chapter 2, and is Chapter 3 the Fairy Conservatory? (`CANON-C12`, `CANON-C15`) | Record the mapping the code uses and the route that ships; flag the question in the register |
| Q3 | Canon conflicts in `seed/canon_seed.json` | Record each with its default: approved art wins over prose, the newest owner decision wins over older text, and anything major waits for the owner |
| Q4 | One pointer, colour meanings, help ladder, Back/exit, touch minimum, encounter ceiling (`OQ-POINTER`, `OQ-COLOUR`, `OQ-HELP`, `OQ-BACK`, `OQ-TOUCH-MIN`, `OQ-BOSS-CEILING`) | Write the best current option into each pattern as a proposal; no runtime change; the owner picks |
| Q5 | New findings from the re-baseline | Open only confirmed ones. Likely candidates: documentation drift from live measurements (an `MA-DOC-*` item), `DL-INT-07`/`DL-SAVE-06` versus the 15 shipping careers, and the Day One pointer and colour inconsistency if a child-facing conflict is reproduced |
| Q6 | Should "design reference checks green" join the satisfaction gate? | Advisory only for now |
| Q7 | Run WP-12 (entry points)? | No, unless the owner names it |
| Q8 | Runtime tokens (WP-13)? | Not in this handoff |
| Q9 | Where the job-game playbook lives | `design/12_JOB_GAME_PLAYBOOK.md`, plus `design/templates/JOB_CARD_V1.md` and `design/reference/jobs.json` |
| Q10 | Who approves a new job | The owner approves each new permanent job's premise and room; practice or prototype jobs inside an approved scope are delegated (`DL-PLAN-01`) |
| Q11 | Which synthetic voice speaks Roshan's new job lines | The engine of the Roshan layer the game prefers at runtime (Parler, per the audit sweep), recorded in the catalogue; protected family recordings are never altered |
| Q12 | May Codex add the 2026-09-30 images rule and the real backup status to `AGENTS.md` (a high-risk file) | No, unless the owner names that change; the takeover kit states both meanwhile |

---

## 9. Gates and delivery

Before every push, from the repository root:

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
python -B docs/handoffs/codex_master_audit_refinement_2026-09-30/tools/measure_reference_health.py --out <scratch>
```

plus the new tools' tests, and the static section of `scripts/ci.sh` when a
tool changes (see the pinned-count gates it runs). CI on the branch must be
green at its exact head before merging into `dev`. Report implementation,
machine verification and outstanding acceptance separately.

## 10. Stop and escalate if

- A step would edit sealed evidence text rather than move it, or rewrite a
  finding's history.
- A step needs `CLAUDE.md`, `AGENTS.md`, `SECURITY.md`, `.claude/`, `.codex/` or
  `.github/workflows/` and the owner has not named that package.
- Recording canon would require choosing between conflicting sources on a
  major character or plot point.
- A change would touch a protected path or any game runtime file.
- Another branch has edited the master audit, design 06 or the ledger since
  you started WP-1: rebase and re-verify rather than overwrite.
- Disk space is below what a checkout or import needs.

## 11. Report (per package, in the PR and the impact record)

- **Implemented:** files, IDs created, sections moved (origin → archive heading).
- **Machine-verified:** exact commands and results at the named head;
  `measure_reference_health.py` before/after for the metrics it moves.
- **Outstanding:** owner questions answered or still pending (by `OQ-*`),
  findings re-verified or not, and every visual, device, child and owner gate
  that remains open.

---

## Appendix A — measurements at `dev` `55032e88`

**Master audit composition** (`data/composition.json`; lines, bytes, and
commit/run/duration tokens per 100 lines):

| Section | Lines | Bytes | Tokens per 100 lines |
|---|---:|---:|---:|
| 0 Planning entry | 99 | 15,895 | 1.0 |
| Sealed audit snapshot metadata | 137 | 8,398 | 54.0 |
| 1 Executive verdict and scorecards | 472 | 48,572 | 29.4 |
| 2 Taxonomy | 82 | 4,855 | 0.0 |
| 3 Authority | 81 | 9,446 | 19.8 |
| 4 Evidence | 537 | 31,531 | 36.1 |
| 5 Triage index | 153 | 33,825 | 44.4 |
| 6 Supporting evidence | 92 | 29,623 | 171.7 |
| 7 Superseded ideas | 47 | 8,173 | 27.7 |
| 8 Expanded acceptance notes | 228 | 22,330 | 29.4 |
| 9 Repair protocol | 29 | 1,547 | 0.0 |
| 10 Finding fields | 32 | 1,650 | 0.0 |
| 11 Tools and documentation control | 86 | 4,669 | 25.6 |
| 12 Satisfaction gate | 103 | 6,175 | 1.0 |
| 13 Repair order | 82 | 5,548 | 50.0 |
| 14 Change history | 68 | 35,660 | 220.6 |

**Live measurements versus documents** (`data/live_vs_documented_counts.json`):

| Fact | Documents say | Live at `55032e88` |
|---|---|---|
| GAME2D model files | 513 (`CLAUDE.md:110`, `AGENTS.md:114`); 509 (audit, findings, design 00/01/03/04) | 0 |
| GAME2D production 3D files | 70 (`CLAUDE.md`, `AGENTS.md`); 65 or 68 (audit, findings, design 00/01/04) | 52 (status `UNSATISFIED`; probe 3D files 61) |
| `scripts/main.gd` lines | 8,465 (`CLAUDE.md:162`, `AGENTS.md:304`); 8,734 (audit, design 00/03/04); 10,499 (`MA-CODE-001` title) | 9,826 |
| Probe scripts | 106 (audit §5.2 and §11.2, `MA-CI-003`, design 03/04) | 137 |
| Opera careers | 13 (`DL-INT-07`, `DL-SAVE-06`, audit scorecard) | 15 (`scripts/opera_house.gd:15` `ACTIVE_ACT_COUNT := 15`; `scripts/save_state.gd:11` `0x3BDEF`) |
| New area music cues | 42 (`DL-SND-06`, `MA-AUDIO-001`) | 44 manifest files; 60 OGG files in `assets/audio/music/` |

**Findings** (`data/finding_staleness.json`): 58 records, 56 open (P1: 30,
P2: 25, P3: 1). By last history entry: 48 in August, 10 in September. Open
findings whose cited code changed since their last entry, with commit counts:
`MA-CI-004` 98, `MA-PERF-003` 69, `MA-CODE-005` 66, `MA-PERF-002` 66,
`MA-SAVE-001` 30, `MA-AUDIO-001` 16, `MA-TYPE-004` 8, `MA-CODE-003` 6,
`MA-VIS-002` 4, `MA-AUDIO-002` 3, and one commit each for `MA-ACCESS-003`,
`MA-TYPE-003`, `MA-TYPE-005`, `MA-TYPE-006`, `MA-CI-005`, `MA-CODE-001`.
Commit counts over heavily shared files such as `main.gd` are a triage signal,
not proof that the finding changed.

**Rules** (`data/rule_inventory.json`): 183 rules, about 8,600 words; the
largest families are `DL-CIN-*` (964 words), `DL-QA-*` (941), `DL-SND-*`
(802) and `DL-INT-*` (800); the child-constraint family `DL-AGE-*` is 246.
Nineteen rules have never been cited by an impact record or finding:
`DL-MED-06`, `DL-MED-07`, `DL-VIS-10`, `DL-READ-04`, `DL-LAY-06`,
`DL-LAY-09`, `DL-INT-05`, `DL-INT-11`, `DL-SND-07` to `DL-SND-12`,
`DL-SND-16`, `DL-ASSET-07`, `DL-QA-08`, `DL-CODE-11`, `DL-CODE-12`.

**Owner decisions** (`data/owner_decisions.json`): 98 mentions, 49 files, 30
distinct dates; 18 dates never appear in design 06.

**Churn since 2026-09-01:** 153 non-merge commits on `dev`; 33 edited the
master audit, 53 the ledger, 15 the findings; 52 were documentation-only.

## Appendix B — recurring design-drift classes and their patterns

*(sweep; re-verify at your head)*

| # | Class | Seen | Rule today | Fixed how | Pattern |
|---|---|---|---|---|---|
| 1 | Highlight drawn from the touch box | Hall doors and the Moonflower gate; art-room pointer offset | `DL-INT-01`, `DL-INT-04`, `DL-READ-06`; no rule separates visual and touch geometry | Per area | `PAT-GUIDE-02` |
| 2 | Pointer vocabulary | At least nine styles in one Day One arc | `DL-READ-06`, `DL-CODE-05` | Two proposals disagree | `PAT-GUIDE-03` |
| 3 | Colour meaning | Props, doors, back arrow, boss counter | None | Not reconciled | `PAT-GUIDE-04` |
| 4 | Missing exact voice, generic fallback | 46% exact coverage of Day One action beats; generic `talk` for Family Evening | `DL-SND-01`, `DL-SND-13` | Per-area opt-in lists | `PAT-VOICE-01` |
| 5 | Tool does Roshan's job remotely | Pool, sink, toilet, seahorse; open cases remain | `DL-INT-02` | Per job | `PAT-JOB-01` |
| 6 | Card duplicated in its background | Bath, Castle plates, Detective crown | `DL-LAY-03`, `DL-LAY-05` | Game-wide, with a detector | `PAT-OBJ-02` |
| 7 | Occlusion and draw order | Route cards, door cue, rescue star, panels, follower | `DL-READ-05`, `DL-LAY-01` | Per instance | `PAT-LAYER-01` |
| 8 | Sprite cut-off and frame bleed | Three waves (08-02, 08-29, 09-25) | `DL-MOT-01`, `DL-MOT-02` | Per asset; checks cover Roshan and room cards only | Add to `PAT-ACT-01` recipe plus a sheet gate |
| 9 | Idle, pose and facing | About six surfaces | `DL-MOT-01`, `DL-MOT-07`, `DL-MOT-10` | Per surface | `PAT-ACT-01` |
| 10 | Back and exit | At least six incidents in four weeks | `DL-UI-05`, `DL-UI-06`, `DL-AGE-06` | Per incident | `PAT-EXIT-01` |
| 11 | Help ladders and target sizes | Five ladders; 110/112/128/160 px | `DL-UI-03` for size only | Diverging | `PAT-HELP-01`, `TOK-TOUCH-MIN-PX` |
| 12 | Progress backstop and difficulty | Grand Puff, seahorse, Opera partial credit | `DL-AGE-03`..`05`; no ceiling rule | Per encounter | `PAT-BOSS-01` |
| 13 | Reward ceremonies | At least four implementations | `DL-MOT-04`, `DL-MOT-05`, `DL-CODE-05` | None | `PAT-REWARD-01` |
| 14 | Typography role bypass | 43 local overrides in 13 files | `DL-TYPE-03`, `DL-TYPE-04` | Partly | `PAT-UI-01` |
| 15 | Music ownership | Boss music re-seeks on warnings | `DL-SND-08` | Per owner | Note under `PAT-BOSS-01` |

Only class 6 was generalized. Its fix is the model to copy: a written
protocol, a register, a detector tool and a test (`PAT-OBJ-02`).

## Appendix C — canon inventory

See `seed/canon_seed.json` for sources. Headlines:

- **No canon bible exists.** Candidates: design 01 §6 (short cast list,
  `BINDING_DOMAIN`), design 10 (navigation only), the Grok builder
  `DATABASE.json` (49 entities, cinematic, unclassified), the Grand Puff
  character sheet in `DUST_BUNNY_BOSS_2026-08-02.md` (stale), and the
  Roshan movement language (Roshan only).
- **Owner corrections from 2026-09-12 to 2026-09-26 are hard to find:** they
  sit in `CLAUDE.md`/`AGENTS.md`, in two rules titled for cinematics
  (`DL-CIN-16`) and the picture book (`DL-ASSET-08`), and in handoffs.
- **Code-only canon:** the full room list (`scripts/arena/castle_rooms_25d.gd`),
  the portrait-to-friend map (`scripts/main.gd` `FRIEND_DEFS`), speaker keys,
  and Ember Fortress lore.
- **Top conflicts to record:** Roshan's colours (`CANON-C01`), Rumi's voice
  (`C02`), what traps Baby Eagle in an older storyboard prompt (`C03`),
  Grand Puff's fate in a ledger-binding document (`C04`), the Ember King's
  motive and the Prince's role (`C05`), the Magician's "bunny-fish" text in
  `scripts/opera_house.gd:87` (`C06`), career count and the Opera House layout
  (`C11`), and what Chapter 3 is (`C12`).

## Appendix D — next-generation inventory, engines and friction

*(sweep; re-verify at your head)*

| Content | Status on `dev` `55032e88` |
|---|---|
| Day One and Grand Puff | Integrated; rebuild handoff is a draft with owner decisions OD-1..OD-9 open |
| Day Two birthday (Chapter 2): eight careers, cake, candle; lawn finale | Integrated candidate; lawn finale integrated alpha |
| Day Two Comfy Games | Integrated; no design document or ledger row found |
| Battle of the Bands | Prototype and Grok packet, not on `dev` |
| Chapter 3 Fairy Conservatory route | Runtime implemented; Butterfly World and Fairy Pond remain 3D debt |
| Northern restaurant | Planning only |
| Arborist Tree Book | Art handoff plus a one-patient practice level |
| Painter flood-fill | Standalone prototype |
| Teacher, Geologist, Racer engine, two-act shows | Integrated on 2026-09-05 |
| Mode Platform (design 08) | Not started; no registry exists |

| Engine family | Main files | Consumers |
|---|---|---|
| Cleaning and scrubbing | `scripts/games/day_one_bathroom_*.gd`, `day_one_pool_cleanup.gd`, `pool_*_activity.gd` | Day One rooms |
| Gestures, including cooking | `scripts/opera_gesture_surface.gd`, `chapter_two_career_scene_adapter.gd` | Kitchen careers, Day Two jobs, proposed Northern restaurant |
| Teacher learning | `scripts/teacher_lesson_plan.gd`, `opera_teacher_surface.gd` | Library |
| Tree doctor | `scripts/opera_tree_book_test.gd` | Opera House foyer |
| Racer | `scripts/kart_driving.gd`, `opera_racer_surface.gd` | Movie Lounge |
| Boss encounter | `scripts/boss_encounter_2d.gd`, `encounter_*_2d.gd`, `games/dust_boss.gd` | Grand Puff, Chapter 2 Ember encounter |
| Persistent construction | `scripts/chapter_two_giant_cake_2d.gd` and siblings | Day Two |
| Journeys and story clips | `scripts/arena/fairy_conservatory_handoff_2d.gd`, `day_two_transition_2d.gd`, `day_one_story_clips.gd` | Chapter 3 entry, Day Two card, Day One |
| Friend games (seek, dolls, melody, fetch) | `scripts/games/*.gd` | Dormant since the Reef was retired |
| Comfy games | `scripts/comfy_games.gd` | Day Two castle rooms |
| Follower | `scripts/rainbow_friend_follower.gd` | Castle, after Grand Puff |

**Where a designer has to dig today:** the career mask is stored twice in
code (`save_state.gd`, `opera_house.gd`) and three ways in documents; save
conventions follow four persistence patterns; voice-key prefixes are
hard-coded per activity in `scripts/audio_director.gd`; the room and route
lists live only in code; idle-help timings and touch minimums differ by
document; chapter probes are not in either trusted roster; and "Day One/Day
Two" and "Chapter 2/3" are never mapped.

**What the next designs need first from the reference:** Battle of the Bands
needs `OQ-BANDS-VS-LAWN` answered and the Ember King and Prince canon; the
Northern restaurant needs its place entry, the cooking engine entry and a
customer-order pattern candidate; the Chapter 3 continuation needs the
journey pattern and the 2D conversion status of Butterfly World and Fairy
Pond; any new Day Two job needs `OQ-ARBORIST-DAY2`, the construction pattern
and the save conventions.

## Appendix E — governance-tool constraints (exact lines at `55032e88`)

| Constraint | Where |
|---|---|
| Fixed paths for the ledger, master audit, design 06 and findings | `tools/audit_document_authority.py:17-20` |
| Index rows: any table row whose first cell holds an `MA-*` ID is parsed for severity and lifecycle | `tools/audit_document_authority.py:276-319` |
| Every active item must be linked from the text between `## 5.` and `## 6.` | `tools/audit_document_authority.py:460-480` |
| Rules are found only as lines starting with a backticked `DL-*` ID followed by an em dash, in design 06 only | `tools/audit_document_authority.py:322-336` |
| Sections 9 and 12 must exist and name the baseline Godot version | `tools/audit_document_authority.py:696-723` |
| Ordinary links are checked for file existence only (anchors are not) | `tools/audit_document_authority.py:607-628` |
| The mandatory contract is byte-identical in `CLAUDE.md`, `AGENTS.md` and the tool, within the first 2,000 characters | `tools/audit_development.py:24-35`, `:134-138` |
| Task index markers, position before the sealed snapshot, eleven required routes, and a link to every `## N.` section of the master audit and design 06 | `tools/audit_development.py:148-171` |
| Impact records: fields, full baseline SHA, defined rules and findings, exact file coverage | `tools/audit_development.py:184-219`, `:248-278` |

Consequences for this handoff: keep the four paths and both anchors; keep
section numbers and titles; if rules ever move out of design 06, teach the
tool to read every rule source first; add new checks inside these functions.

## Appendix F — the new-designer test

Each question must be answerable from `design/11_DESIGN_REFERENCE.md` within
two links, with the answer's source cited:

1. Who is Rumi, what does she look like, may she speak, and where does she appear?
2. Which colour means "the story wants you here", and what does a bonus look like?
3. How big must a touch target be, and where is that enforced?
4. How long before help appears, what does each step do, and what must it never do?
5. What line plays when a room is finished, and what happens if the clip is missing?
6. How does the child leave an activity, and where do they return?
7. Which engine should a restaurant customer-order activity reuse, and which probe drives it?
8. How does a new chapter milestone name, default and write its save key?
9. Which owner decisions govern the Opera House right now?
10. What is the canonical order of the Day One pool beats?
11. Which art may a new Northern room reuse, and what happens when art is missing?
12. What evidence makes a new activity "done", and who grants each level?
