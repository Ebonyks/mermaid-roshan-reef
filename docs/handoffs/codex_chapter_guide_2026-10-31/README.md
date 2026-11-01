# Codex handoff — what a future chapter needs from the master audit (2026-10-31)

**Status:** `PROPOSED / CANDIDATE` written handoff prepared by Claude: analysis,
specification and a read-only measurement tool. No game change and no images.
**Owner request, 2026-10-31:** "Analyze the master audit in this project from
the perspective of being a development guide for future chapters of the mermaid
roshan game. What is missing at this point that would strengthen the
document?", followed by "Yes, write handoff".
**Measured at:** dev `218ae766f8e60afb3f6338b8fafce28ec9fab7f2`.
**Finding:** [`MA-DOC-010`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-010)
(P2, `CONFIRMED_OPEN`).
**Recipient:** Codex. **Delivery:** this folder in the public GitHub
repository `Ebonyks/mermaid-roshan-reef`; anonymous read access.

## What is in this folder

| Path | What it is |
|---|---|
| `README.md` | This work order: the gaps, work packages CG0–CG8, acceptance criteria and owner questions |
| `data/measurements_218ae766.json` | Every number in this README, as produced by the tool below |
| `data/chapter_map_seed.json` | A starting chapter map: five chapters, carried state, seven open threads, blocked sources and name aliases, each with sources and a default owner mark |
| `tools/measure_chapter_guide.py` | Read-only measurement. Run `python -B docs/handoffs/codex_chapter_guide_2026-10-31/tools/measure_chapter_guide.py --rev HEAD` at the implementation head |
| `MANIFEST.json` | SHA-256 of every other file in this folder |

---

## 0. Summary

The chapter path already says *how* to plan a chapter, and that part is sound:
creative delegation (`DL-PLAN-01`), the one-sentence cause-and-effect test for
each activity, the three linked plans for story, navigation and save, the rules
for choosing unused assets, and separate lanes for permission, build progress
and acceptance. Keep all of it.

What it does not give the next chapter's developer:

1. **Chapter 2's lessons.** The guide and brief were last edited on 2026-09-11.
   Chapter 2's first party job then shipped as a dead end while its probes
   passed (`MA-PLAY-005`, P0), and a story clip covered Rumi's wave
   (`MA-PLAY-006`). Neither lesson is in the guide, brief or recipe.
2. **The story so far.** No canon register exists. The one the 2026-09-30
   refinement handoff planned (`MA-DOC-006`) has not been built.
3. **Where a chapter fits.** No chapter map, no list of open story threads and
   no list of the state every chapter inherits (followers, outfits, masks).
4. **How a chapter plugs into the code.** The two chapter directors share an
   informal interface that no document describes; Chapter 3 has no director.
5. **When a chapter is done.** No per-chapter status ladder and no chapter rows
   in the master audit.
6. **A clean way in.** 16 of the task index's 37 rows are art-candidate
   receipts, and 31 status notes sit in the planning entry.
7. **The founding story decisions.** The decision register starts on
   2026-09-30, after every founding story decision.

Recommended order: CG1 (cheap, and it stops a repeat of the P0), then CG2, CG3
and CG7 (they need the owner's answers to Q1–Q3), then CG4, CG5 and CG6, and
CG8 last as the test of the whole.

---

## 1. What is missing, with evidence (dev `218ae766`)

All numbers come from `data/measurements_218ae766.json` unless a file and line
are named.

| # | Gap | Evidence | Effect on the next chapter |
|---|---|---|---|
| G1 | Chapter 2's lessons are not written back | `design/09_CHAPTER_DEVELOPMENT_GUIDE.md` and `design/templates/CHAPTER_BRIEF_V1.md` last changed at `3f02d625` (2026-09-11); the master audit has had 158 commits since. `MA-PLAY-005` (P0, `IN_PROGRESS`) records that Chapter 2's story careers could not start in normal play, with 19 of 29 story steps bound to no room object (historical measurement at `87f99268`), while "the trusted probes bypass both paths": `probe_chapter2.gd` called director callbacks directly and `probe_chapter2_farmer_resume.gd` armed phases itself. The repaired lane plays all 29 phases through viewport input but still starts from an injected post-boss fixture; fresh-save door traversal remains open. `MA-PLAY-006` records a clip that started over Rumi's wave. The guide states the goals (section 4: "Fresh, partial, complete, replay, Back, and legacy access have coherent routes"; section 5 step 4: "Use the actual production implementation") but names no check that would have caught either defect. `DL-QA-02` already says a probe that writes state around the interaction it claims to test is diagnostic, not closure evidence; the chapter documents never cite it | The next chapter can pass every probe and still strand the child |
| G2 | No story bible | No `design/reference/canon.json` or `CANON.md` exists (none of the six reference files planned in `MA-DOC-006` exists). `design/01_GAME_DESIGN.md` §6 "Cast and story" is 16 lines (lines 485–500), and line 494 still describes Roshan with "lavender clothing", which `ODR-ROSHAN-IDENTITY` and `ODR-ROSHAN-IRIDESCENT` superseded (tracked by `MA-DOC-008`). Design 06 mentions Grand Puff, the Ember King and Rumi 0 times each and has no story or canon rule family among its 18. Grand Puff's canon lives in the AGENTS.md and CLAUDE.md story-clip section, Baby Eagle under two dust bunnies only in the picture-book rule (`DL-ASSET-08`), the Ember King's motive in the Chapter 2 spine. Design 10 asks for a character card before a returning character is used; none has been filled | Without the canon, the delegation rule cannot be applied: an agent cannot tell a minor addition from a major change |
| G3 | No chapter map, open threads or carried state | The planning answer "Which chapter sources control?" links only the two Chapter 2 documents and the early Chapter 3 route. The names drift: across 74 design, audit and AGENTS documents, "Day One" occurs 117 times, "Day Two" 19, "Chapter 2" 66, "Chapter Two" 19, "Chapter 3" 15 and "Chapter 1" 0. Open threads have no owner mark: the Ember King took the candle; Chapter 3's second world and ending are outside its prototype's commission; Fashion's later disguise mission (`ODR-FASHION-PERSISTENCE-20261006`) has no home; the Rumi book proposes a book-led chapter (its Q6, not commissioned). Followers, outfits and masks carry across chapters, and no document lists them | A new chapter can contradict or quietly close a thread the owner meant to keep, or forget the Rainbow Friend |
| G4 | No chapter integration contract | `DayOneDirector` (836 lines) and `ChapterTwoDirector` (1,098 lines) both extend `RefCounted` and share an informal interface: the `hook_event` signal, `serialize_state()` and `restore_state()`, each returning 26 namespaced keys merged into the one save document. They differ on who holds state: Day One's director holds its own; Chapter 2's header says "The director owns policy only" yet it holds most fields, with 5 of its 26 keys read from `ReefMain`. Chapter 3 has no director: `scripts/save_state.gd` reads and writes its 3 keys as `ReefMain` fields. `design/03_TECHNICAL_ARCHITECTURE.md` names neither chapter director. The Chapter 3 route, handoff and prototype probes are in neither trusted roster, while `DL-CODE-10` asks a new mode for a driving trusted probe in both. The Mode Platform in design 08 is not built | Chapter 4 would invent a fourth save and handoff pattern |
| G5 | No per-chapter status or "done" | Master audit sections 1, 9, 12 and 13 contain the word "chapter" 0 times. The area scorecard (§1.4, last changed 2026-08-13/14) has 12 rows and none for Day One, the birthday chapter or Chapter 3. The satisfaction gate (§12) is game-wide only | Nobody can say which chapter is ready for the phone or accepted |
| G6 | The way in is cluttered | The task index has 36 table rows plus 1 row above the table header that renders as raw text; 16 of those 37 rows are single art-candidate receipts (Geologist R100–R115, Dolls R118, insect tab R91). 31 status notes sit in the planning entry (11 above the index, 20 inside its markers). The entry was last updated "2026-10-03 against integration source `30d82725`" | The New chapter route is one row among receipts |
| G7 | Founding story decisions are not in the register | `design/reference/owner_decisions.json` holds 60 decisions; the earliest is dated 2026-09-30. Absent: the Chapter 2 spine (2026-08-30), creative delegation and the Northern direction (2026-09-05), the picture-book canon (2026-09-19/20), Day One story clips and Grand Puff canon (2026-09-23). `MA-DOC-006` §4.2 already lists this as its minimum backfill. Three learning-session answers exist only on the unmerged branch `claude/angry-roentgen-6a8f7b` (`7b851b3d`) | An agent checking the register for story authority finds none |

Smaller gaps:

| # | Gap | Evidence |
|---|---|---|
| G8 | Game-wide systems a chapter touches | The brief has no section for what a chapter adds to or expects from followers, outfits (`ODR-FASHION-PERSISTENCE-20261006`: unlockable outfits "throughout play"), stuffies, medals, the guide voice or free-play career cards |
| G9 | Books and chapters | The guide mentions books once, the library and brief never. The Rumi book handoff recommends a book-led chapter and the owner wants that book to "integrate smoothly into the game environment" (`ODR-RUMI-REVISION-HANDOFF-20261017`), but nothing says how a book may seed a chapter or which wins when they disagree |
| G10 | Chapter-sized pacing | Design 01 §4 covers one career act (about 2 minutes) and how fast an objective must be voiced. Nothing covers a whole chapter: sessions to finish it, time between saved milestones, longest clip before the child acts. The Luna study's `audit/cycles/luna-playtest-20261012/PLAYTEST_GUIDE.md` already defines per-run measurement fields that could be reused |
| G11 | Blocked or stranded sources | Iko Iko for the Day Two story waits on game-use rights (`ODR-POPSTAR-SONG-20261018`). The owner-confirmed July 29 Northern concept exists only on the rescue commit `f07027af` (SHA-256 `db0cc66cc90551774ffe28809c095658324634ccf8f27c5742b7735da489208d`) |
| G12 | The guide has never been trialled on a whole chapter | Guide §8 makes the first commissioned chapter "a bounded autonomy trial". The only filled brief is `design/FAIRY_RESTORATION_PROTOTYPE_2026-09-30.md`, and its §8 log records integration fixes, not the trial's measures (where the agent guessed, needed clarification, contradicted canon or duplicated a system) |

---

## 2. What already exists: build on it, do not duplicate it

| Source | What it already plans or holds | How this handoff uses it |
|---|---|---|
| [Refinement handoff](../codex_master_audit_refinement_2026-09-30/README.md) (`MA-DOC-006`) | Canon register `design/reference/canon.json` and `CANON.md` with schema (§4.3) and seed (`seed/canon_seed.json`: 21 entities, 15 conflicts); design 11 front door with the Day/Chapter vocabulary; `engines.json`; `DESIGN_CARD_V1` and `CHAPTER_BRIEF_V2` (§4.7); decision backfill list (§4.2) | CG2 and CG7 build the chapter slice of those plans with their schemas. Do not create a competing file |
| [Consolidation handoff](../codex_reference_consolidation_2026-09-30/README.md) (`MA-DOC-007`) | Reference R04 (design 10 extended with Chapter 2 history) and R08 (`CANON.md`); waves W0–W7 for stale text | CG6 moves status notes with the same verbatim-move rule; no wave is redone |
| [Visual language handoff](../codex_visual_design_language_2026-09-30/README.md) (`MA-DOC-008`) | Fixes the Roshan anchors in design 01 §6 | CG2 points design 01 §6 at the canon register; the anchor repair stays in `MA-DOC-008` |
| [Loop handoff](../codex_self_improvement_loop_2026-10-03/README.md) (`MA-DOC-009`) | Recipes rendered from `design/reference/prompt_intents.json`; generated surfaces and roadmap | CG1 edits the catalogue, not the rendered recipe. The roadmap (last generated 2026-10-03b) still lists `MA-PLAY-005` as `CONFIRMED_OPEN`, so regenerate it in the next study cycle rather than by hand |
| `MA-PLAY-005` | Its remaining acceptance is a fresh-save Chapter 2 traversal through normal doors | Build that probe under `MA-PLAY-005`. CG1 makes the same kind of probe a standing requirement for every chapter |
| [Rumi book handoff](../codex_rumi_book_revision_2026-10-17/README.md) | Book-led chapter proposal (Q6), world bible (Q1–Q4), draft brief values | CG3 lists it as a proposed chapter; CG2 lists its characters as `PLANNED` only |
| Rules | `DL-QA-02` (diagnostic probes), `DL-SAVE-04` (the acceptance path), `DL-CODE-10` (trusted probes for a new mode), `DL-CIN-16` (clips never replace a child action), gold-star pattern `GS-21` (the reward beat plays out before the next scene) | CG1 cites these instead of restating them |

---

## 3. Invariants

- **Claude recommends, Codex implements.** This packet contains no image and
  asks for none. Nothing here needs a picture.
- **No game behaviour change** except the optional static checks in CG1 and CG4
  and the probe work owned by `MA-PLAY-005`. No save key is removed or
  renamed. Chapter names are documentation aliases: code identifiers and save
  keys keep their names.
- **History is never rewritten** (`DL-AUTH-02`). Status notes move verbatim to
  history; finding histories gain dated entries only.
- **Canon is recorded, not invented.** Unknowns stay written as unknowns. The
  owner marks in `data/chapter_map_seed.json` are defaults until the owner
  answers Q2.
- **High-risk files need an explicit owner task.** `.github/workflows/`,
  `AGENTS.md`, `CLAUDE.md`, `SECURITY.md`, `.claude/` and `.codex/` are out of
  scope here (see section 7).
- **Every change carries an impact record**, and the usual gates run before
  each push (section 8).

---

## 4. Work packages

### CG0 — Baseline

Run the measurement tool at the implementation head and record any difference
from `data/measurements_218ae766.json` in the impact record. Read
`MA-DOC-006` §3–§4 and the consolidation plan's R04 and R08 first, and say in
the impact record which of their parts this work builds.

**Done when:** the impact record holds the head's measurements and the overlap
statement.

### CG1 — Write Chapter 2's lessons back (do first)

Edit `design/09_CHAPTER_DEVELOPMENT_GUIDE.md` (§4, §5 step 4, §8),
`design/templates/CHAPTER_BRIEF_V1.md` (§3, §4, §7) and the `INT-NEW-CHAPTER`
entry of `design/reference/prompt_intents.json` (then run
`python -B tools/plan_prompt.py --render-recipes`). Add three named
requirements, each with its check:

1. **Fresh-save chapter traversal.** Closure evidence for a chapter is a trusted
   probe that reaches the chapter from a fresh save, or from the previous
   chapter's real end state reached by the same probe, through visible doors
   and real touches on the production input path. That probe may not call
   director callbacks, pass phase overrides, mount fixtures or use a
   probe-only gesture. Fixture probes stay useful and are labelled diagnostic
   (`DL-QA-02`). Cite `DL-SAVE-04` for the path it must cover.
2. **Every story step has a reachable room object.** Each authored story step
   (phase or beat) maps to a child-visible room object, hotspot or stage action
   that the step's own room can reach. A static check over the chapter's step
   registry fails on any unmapped step. Specify it for Chapter 2 first (the
   party plan and the story bindings `MA-PLAY-005` added; verify the exact
   symbols at the head) and write it so a later chapter registers its steps
   the same way. Prove it with injected faults: an unbound step, and a step
   bound to an object in another room.
3. **A story clip waits for the reward beat.** A clip that follows an in-room
   reward starts only after that beat's authored sequence and spoken line have
   finished, with a minimum and a hard maximum, polled in the owner's process
   (`GS-21`; the `MA-PLAY-006` repair is the worked example). A clip never
   covers a character's acting or a child action (`DL-CIN-16`).

Requirement 1 restates `DL-QA-02` and `DL-SAVE-04` at chapter level, so it needs
no new rule. Requirement 2 is a recurring defect class (`MA-PLAY-005`: 19 of 29
steps at `87f99268`, 18 of 29 in the later explicit-phase measurement).
Propose it as the next planning rule after `DL-PLAN-06` in design 06 §20, and
refresh any rule-count pin the document gates keep. Requirement 3 stays a guide requirement that cites
`DL-CIN-16`; do not edit the owner-decision text of `DL-CIN-16`.

**Done when:** the three requirements are in the guide, brief and recipe; the
step-binding check runs in the existing static gates and fails on both injected
faults; `MA-PLAY-005` and `MA-PLAY-006` are cited as the source lessons.

### CG2 — Canon register, chapter slice

Build `design/reference/canon.json` and the generated `CANON.md` exactly as
`MA-DOC-006` §4.3 specifies, starting from its seed. Do the chapter slice first:
every character, place and story fact named in the five chapter entries of
`data/chapter_map_seed.json`, in the Day One clip manifest, in
`scripts/chapter_two_voice_catalog.gd` and in the lawn-finale draft. Add two
fields per character, because a chapter author needs them:

- `chapter_latitude`: what a chapter may change (`NONE`, `MINOR` such as
  outfits, staging or new lines in an existing voice, or `RESERVED`), with
  its source.
- `voice_availability`: family recording, synthetic narrator, or no voice
  (Rumi uses approved animation and notes, with no invented voice).

Resolve each of the 15 seed conflicts to a default with both sources cited, or
leave it open with a question ID. List the Rumi book's characters as `PLANNED`
until its Q3 is answered. Point `design/01_GAME_DESIGN.md` §6 and design 10 §1
at the register. Replace design 10's "fill a character card" instruction with
"cite the canon entry; add a card only for a new minor character".

**Done when:** every recurring character in the chapter slice has an entry with
sources, latitude and voice; conflicts are resolved or carry a question; the
register's check runs in the document gate.

### CG3 — Chapter map, carried state and open threads

Create `design/chapters/CHAPTER_MAP.md`, or make it section 2 of design 11 if
`MA-DOC-006` has landed design 11 by then. Keep one home. Start from
`data/chapter_map_seed.json` and re-verify every entry. For each chapter give:
name and number (Q1), aliases, premise, status, entry condition in save terms,
end state, what the ending obliges the next chapter to honour, code entry
points, trusted probes and sources.

Add three lists. **Carried state:** what every chapter inherits and must decide
on, namely companions, the Rainbow Friend, outfits, medals, the global and
story career masks, and free-play cards. **Open threads**, each marked
`OWNER_RESERVED` or `DELEGATED` (Q2). **Blocked sources.**

Link the map from the master-audit planning answer "Which chapter sources
control?", the "New chapter" task row, guide §1 and design 10 §1.

**Done when:** every chapter, thread and carried item cites a source; the
planning answer and task row link the map; aliases are listed once.

### CG4 — Chapter integration contract

Add a "Chapter directors" section to `design/03_TECHNICAL_ARCHITECTURE.md`. It
has two parts.

**As built.** The shared informal interface (`hook_event`, `serialize_state()`,
`restore_state()`, a normalise step, namespaced keys merged into the one save
document); the state-ownership difference between Day One and Chapter 2; how
Chapter 3 differs; how the Day Two transition bridges chapters; how a director
hands control to an activity and gets it back (`OperaHouse.start` with
`ChapterTwoDirector.opera_config_overrides`); how story clips are triggered;
the voice catalogs.

**For a new chapter.** A director exposing that interface; a save prefix
`chapterN_` with defaults and normalisation; story progress kept separate from
free play and from the global mask; a voice catalog; music cues; the CG1 probes
plus the passive and resume probes; registration in both trusted rosters. Mark
each item `BUILT` or `TARGET (design 08 Mode Platform, not built)`.

Optional: `tools/audit_chapter_contract.py`, which reads the chapter map and
fails when a listed chapter lacks its director file, save defaults or trusted
probes. Do not refactor the existing directors onto a shared base class in this
work; extract-don't-rewrite applies when a third director is commissioned.

**Done when:** a reader can name every file and symbol a new chapter must touch
without opening the code, and every named file and symbol exists at the head.

### CG5 — Chapter status ladder and chapter board

Define the ladder in guide §8:

| Rung | Means | Needs |
|---|---|---|
| `PLANNED` | A brief or seed exists | The brief or map entry |
| `COMMISSIONED` | The owner approved premise and boundaries | The dated decision in the register (`DL-PLAN-01`) |
| `PLAYABLE_REVIEW` | The whole chapter plays from a fresh save | CG1 probes green at the exact head; captures (V4) |
| `ON_PHONE` | It runs on the target phone | One recorded device session (V5) |
| `ACCEPTED` | The owner accepts it | Owner review (V7); child observation recorded when available and never invented (Q4) |

Add a chapter board to the master audit: one row per chapter with its rung,
evidence links and blocking findings. Generate it from the chapter map through
the study tools if practical (the `MA-DOC-009` approach); otherwise keep a
hand-written table whose rows link their evidence. If the board becomes a new
numbered top-level section, link it from the task index in the same change: the
development gate requires every numbered section to be indexed.

**Done when:** each chapter in the map has a board row whose rung matches its
recorded evidence.

### CG6 — A clean way in

Keep only stable task types in the task index. Move the 16 candidate-receipt
rows and the 31 status notes verbatim into the change history or the matching
cycle folder; their impact records already hold the evidence. Keep one
"Job-game art" route. Fix or remove the row outside the table.

Add a check to `tools/audit_development.py` (which already validates the index)
that fails on a row outside the index table, a row whose "Start with" cell links
a per-candidate folder (`/r<number>_…/`), or a dated status paragraph between
the index markers. Prove it with three injected faults.

Coordinate with `MA-DOC-007`: if its wave W1 or W2 has started, fold this into
that wave instead of moving the same text twice.

**Done when:** the index holds only stable task types; the check fails on each
injected fault; no moved text is edited.

### CG7 — Story decisions in the register

Backfill the founding story decisions with
`tools/record_owner_decision.py --answers PATH --cycle story-backfill-20261031 --answered-on DATE`,
once per original date. Each `answered-on` is the owner's original session
date, which the tool requires. Each `source` is the document that records the
owner's words:

- 2026-08-30: the owner direction incorporated in the Chapter 2 spine (separate
  the owner's choices from the agent's design there).
- 2026-09-05: creative delegation (the two policies quoted in guide §2; design
  06 §20) and the Northern direction (Northern branch §1).
- 2026-09-19 and 2026-09-20: picture-book art and canon (`DL-ASSET-08`).
- 2026-09-23: Day One story clips and Grand Puff canon (`DL-CIN-16`).

A statement that is only an agent's summary is not entered as an owner
answer; leave it as a source note. Then run
`python -B tools/record_owner_decision.py --check --base origin/dev`. Leave the
learning-session decisions to the merge of their own branch.

**Done when:** the register holds those decisions with sources, the append-only
check passes, and the canon register cites their IDs.

### CG8 — Cold-start trial

After CG1–CG5 land, give a fresh agent with no conversation history only the
repository and the prompt "Plan the Northern restaurant chapter" (the default
of Q5). It fills `CHAPTER_BRIEF_V1` (or V2 if landed) as a proposal and runs
nothing at runtime. Log every guess, every missing fact, every canon conflict
and every duplicated system: these are guide §8's measures. Write each gap
back into the guide, map or register, and record the trial as the guide's
first autonomy-trial entry.

**Done when:** the log exists, every gap has a write-back or an owner
question, and the owner has reviewed the brief (V7).

---

## 5. Acceptance criteria

| ID | Criterion | Package |
|---|---|---|
| AC-1 | The guide, brief and recipe carry the three CG1 requirements, citing `DL-QA-02`, `DL-SAVE-04`, `DL-CIN-16` and `GS-21`; the step-binding check fails on both injected faults | CG1 |
| AC-2 | Every recurring character in the chapter slice has a canon entry with sources, `chapter_latitude` and `voice_availability`; design 01 §6 and design 10 point to it | CG2 |
| AC-3 | The chapter map lists every chapter in the seed, the carried state and every open thread with an owner mark, and the planning answer and New chapter row link it | CG3 |
| AC-4 | Design 03 documents the chapter contract as built and as targeted, and every file and symbol it names exists at the head | CG4 |
| AC-5 | The ladder is in guide §8 and every chapter has a board row consistent with its evidence | CG5 |
| AC-6 | The task index holds only stable task types and the new index check fails on its three injected faults | CG6 |
| AC-7 | The founding story decisions are in the register and the append-only check passes | CG7 |
| AC-8 | The cold-start log exists and every gap it found has a write-back or a question | CG8 |
| AC-9 | The owner reviews the result (V7). Machine passes do not replace that review | All |

---

## 6. Owner questions

| Q | Question | Default (work proceeds on this) | Blocks |
|---|---|---|---|
| Q1 | What are the chapters called? | Documents use numbers with the story name: "Chapter 1: Day One", "Chapter 2: Day Two, Roshan's birthday party", "Chapter 3: The Fairy Conservatory". "Day One" and "Day Two" stay as the story's own words. Code and save keys are not renamed | CG3 names |
| Q2 | Which loose threads may an agent continue without asking? | Reserved for you: the candle and the Ember family, Chapter 3's ending and second world, the disguise mission, the Northern story and the Lantern Night chapter. Delegated: where the Rainbow Friend and companions stand, and minor characters or side activities inside an approved premise | CG3 marks |
| Q3 | When a book and the game disagree, which wins? | The game's canon register. A book seeds a chapter only through a commissioned brief; the picture book keeps `DL-ASSET-08`; the Rumi book's Q1–Q6 stay open | CG2, CG3 |
| Q4 | What does "accepted" mean for a chapter? | Your review after a phone session. A child observation is recorded when there is one and never invented, but it is not required | CG5 top rung |
| Q5 | Which chapter should the cold-start trial plan? | The Northern restaurant, whose planning you authorized on 2026-09-05; no runtime work | CG8 |

---

## 7. Out of scope or needing separate owner authority

- **Adding the Chapter 3 probes to the trusted rosters.** This touches
  `.github/workflows/probes.yml`, a high-risk file, so it needs an explicit
  owner task. Until then, record the gap on the chapter board.
- **Editing AGENTS.md or CLAUDE.md.** The chapter route lives in the master
  audit, design 06 and the guide.
- **Refactoring the directors onto a shared base class** (see CG4).
- **Commissioning any chapter** (`DL-PLAN-01`), and **merging the
  learning-sessions branch**.
- **Building `MA-PLAY-005`'s fresh-save probe** belongs to that finding, not to
  this package.

---

## 8. Gates and reporting

Run before each push, and see the result line of each before committing:

```text
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development
python -B tools/plan_prompt.py --check
python -B tools/record_owner_decision.py --check --base origin/dev
python -B tools/audit_game_2d.py --regression-gate
```

Any new JSON under `design/` is scanned by the 2D gate: write "3D nodes" in
plain words, never an engine class name. A follow-up push must change its
impact record in the pushed range. Report three things separately: what was
implemented, what was machine-verified, and which owner, device and child
reviews remain open.

---

## 9. Revision history

- **Revision 1 (2026-10-31).** Written by Claude at dev `218ae766` from the
  owner's request; opens `MA-DOC-010`.
