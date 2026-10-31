# Job Platform — architecture for building job games from one catalogue (2026-09-30)

**Status:** `PROPOSED / CANDIDATE` architecture, prepared by Claude
(specification only; no game change). Codex implements it through the work
packages in [README.md](README.md). Owner questions are in README section 4.

**Baseline:** `dev` `7f068cb80766edd52a110cc1cb3958158f829822`. Facts were
re-read in code at that head or come from
[`tools/extract_job_catalog.py`](tools/extract_job_catalog.py), which is
read-only and re-runnable. Items marked *(sweep)* come from read-only
document and code sweeps and must be re-read at your head.

**Authority:** subordinate to [design 06](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
the [Mode Platform target architecture](../../../design/08_TARGET_ARCHITECTURE.md),
the save, protected-content and workflow rules, and dated owner decisions. It
specializes design 08 for the job family; it does not replace it.

---

## 0. The design in one page

**The problem.** Building a job game today means hand-editing about 25 code
and data files, six trusted probes with pinned counts, and several tools —
and missing any one of them fails silently or corrupts saves
([job-game audit](../../../audit/JOB_GAME_TAKEOVER_AUDIT_2026-09-30.md), finding
[`MA-DOC-006`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006)).
The same career list lives in at least a dozen places, at least 77 lines of
`scripts/opera_career_world_2d.gd` branch on a literal career ID, two hidden
bounds wait to break the next job (the 18-bit star clamp and the hard-coded
phase bound in both checkpoint validators), and drift has already set in
(Geologist's music cue is missing from the music build tool; the Geologist and
Teacher costume sheets are outside the atlas gate).

**The design.** Write every job fact once, in one record per job. Compile the
records into typed constants. Make runtime code, probes, build tools and
documents read the compiled catalogue instead of keeping their own copies.
Move the plumbing every job repeats into a small shared kit.

```text
 content/jobs/<id>.json  ┐
 content/jobs/_ledger.json├─ tools/content_build.py ─┬─ --write ─▶ scripts/generated/job_catalog_data.gd (const, typed)
 content/tokens.json     ┘                           │            scripts/generated/design_tokens.gd   (const, typed)
                                                     │            generated blocks in design and audit documents
                                                     └─ --check ─▶ called by the document gate both CI runners already run

 runtime   JobCatalog (static, stateless) ◀── generated constants
           ├─ OperaHouse · SaveState · CastleCareerRoutes · AudioDirector · venue · living world · Chapter 2 plan
           └─ JobHost (today: OperaCareerWorld2D) ─ capability lookups ─▶ JobKit: help · guide · exact voice ·
                                                                          reward · Roshan-at-work · imp contest ·
                                                                          phase checkpoint
                                     └─ surface: the generic gesture surface or one specialist JobSurface
 probes    expectations derived from JobCatalog; a conformance loop over every live job inside a trusted probe
 tools     music, atlas, audio ledger and stage-path inventory read content/jobs
```

**Proof that it fits today's code.** The extractor parses the current
registries into 15 job records and 3 tombstones and recomputes the values the
code hard-codes. All eleven match (`data/derivation_check.json`):

| Hard-coded today | Value | Derived from the records |
|---|---|---|
| `ACTIVE_STAR_MASK` (`scripts/opera_house.gd`), `OPERA_ACTIVE_STAR_MASK` (`scripts/save_state.gd`) | `0x3BDEF` | OR of live slots — match |
| `RETIRED_STAR_MASK` | `0x4210` | OR of tombstones — match |
| `ACTIVE_ACT_COUNT`, `OPERA_ACTIVE_ACT_COUNT` | 15 | count of live jobs — match |
| `LIVE_ACT_INDICES`, `RETIRED_ACT_INDICES` | 15 and 3 slots | from status — match |
| `range(18)` loop and four `262143` clamps (`scripts/save_state.gd`) | 18, `0x3FFFF` | slot count and `(1 << slots) - 1` — match |
| `ALL_PARTY_MASK` (`scripts/chapter_two_party_plan.gd`) | `0x2C4F` | OR of party jobs — match |
| Shipping phase pin (`scripts/probe_opera_2d.gd`) | 61 | sum of phases — match |

**The outcome.** Adding a permanent job becomes: one record, at most one
specialist surface, its assets, and `tools/content_build.py --write`. The
twenty-plus registries, the save bounds, the probe expectations, the tool
lists and the document tables follow automatically, and a CI check fails if
anything a job needs is missing.

---

## 1. Forces

| Force | Evidence at the baseline | Cost today |
|---|---|---|
| One fact, many copies | Career identity and slot appear in `opera_house.gd`, `save_state.gd`, `castle_career_routes.gd`, `opera_career_world_2d.gd`, `opera_competition.gd`, `opera_mastery.gd`, `opera_performance_plan.gd`, `opera_performance_overlay.gd`, `opera_hotspot_catalog.gd`, `opera_stage_paths.gd`, `opera_world_backdrop_2d.gd`, `living_world_catalog.gd`, `chapter_two_*`, `audio_director.gd`, four tools and eight probes *(sweep)*; `EXPECTED_ROOM_ACTS` in `scripts/probe_opera.gd` copies the room table | About 25 files per new job; copies drift |
| Hidden bounds | `opera_stars` clamped to `262143` at `scripts/save_state.gd:198`, `:294`, `:619`, `:681`; both checkpoint validators hard-code `phase_index <= 4.0` (`:731`, `:756`) | The next job at bit 18 marks every career complete; a job with more phases than the bound loses its mid-activity checkpoint |
| Behaviour keyed by literal ID | At least 77 lines of `scripts/opera_career_world_2d.gd` test `career_id ==` or `career_id in [`; the specialist surface is chosen by a five-way if-chain (Boxer, Ballerina, Teacher, Geologist, Racer) | A new specialist job edits the host's branches |
| Drift | `opera_geologist` absent from `EXPECTED_IDS` in `tools/build_area_music.py` and from the music manifest, although the OGG ships and `scripts/probe_audio.gd` requires it; Geologist and Teacher absent from `CAREERS` in `tools/audit_opera_roshan_animation.py`; 11 of 15 living-world names differ from the act titles *(sweep)* | Gates silently cover less than the game |
| Naming | Candy Maker appears as `candymaker`, `Candy Maker`, `candy` and `candy_maker` across scripts, crests, Chapter 2 and stage IDs; probes strip underscores to cope *(sweep)* | Lookups that fail on spelling |
| Dead data | `SLUGS`, `LEGACY_PHASES`, `LEGACY_FINALE_START`, Chapter 2 `CAREER_ORDER`, and most `ACTS` fields have no runtime reader *(sweep)* | Readers cannot tell live data from leftovers |
| Fragile tools | `tools/audit_stage_pathfinding.py` regex-parses `ACTS` and depends on its key order *(sweep)* | Any registry refactor breaks the tool |
| Checks outside CI | The stage-path check and the Day One voice-catalogue `--check` run in neither CI runner *(sweep)* | Coverage exists on paper only |
| Workflow cost | A new trusted probe means editing `.github/workflows/probes.yml`, a high-risk file | Teams avoid adding probes, or need owner sign-off each time |

## 2. Principles

| # | Principle | What it rules out |
|---|---|---|
| P1 | **One declaration per fact.** Every job fact is written once, in that job's record | The same career list hand-kept in a dozen files |
| P2 | **Author in data, compile to typed constants.** Records are JSON for review and tools; a generator compiles them to analyzer-checked `const` GDScript that runtime reads. Nothing parses JSON at runtime | Runtime parse failures, export include-filter surprises, typo-silent lookups (the reason design 08 §4.2 prefers `const` registries) |
| P3 | **Derive, never pin.** Masks, counts, clamps, loop bounds, room lists, phase totals and probe expectations are computed | The bit-18 trap and every pinned probe count |
| P4 | **Permanent IDs, append-only allocation.** Job IDs and star bits come from an append-only ledger; tombstones stay forever; aliases map old spellings | Reusing bits, renaming IDs that saves depend on, spelling drift |
| P5 | **Plumbing once, simulations per job.** Lifecycle, routing, save identity, voice and pointer, help, rewards, medals, contest and teardown live in a shared kit; each job keeps a surface only for what only it does | A universal job engine (rejected for the reason design 03 §2 rejected a universal game engine); per-job copies of plumbing |
| P6 | **Checks run where CI already runs.** New validation is called from the document gate and from probes already in both trusted rosters | Per-job workflow edits; checks that never run |
| P7 | **Documents are generated views.** Job tables and counts in design and audit documents are rendered from the catalogue and verified with `--check` | Hand-copied counts |
| P8 | **Strangle, don't rewrite.** Each registry moves behind the catalogue one at a time, after the generated value is proven equal to the literal it replaces | A big-bang rewrite of the 5,000-line Opera scripts; behaviour changes hidden in refactors (`DL-CODE-06`) |

## 3. Layers

| Layer | Lives in | Owns | Must not |
|---|---|---|---|
| Content | `content/` (with `.gdignore`, so Godot neither imports nor exports it) | Job records, the allocation ledger, design tokens | Hold code or generated output |
| Build | `tools/content_build.py` and its tests | Validation, compilation, document rendering | Change runtime behaviour by itself; it only writes generated files |
| Generated | `scripts/generated/` | Typed constants compiled from content | Be edited by hand (header says so; `--check` enforces it) |
| Runtime | `scripts/job_catalog.gd`, existing consumers, `scripts/jobkit/` | Queries over the catalogue; shared job plumbing | Keep its own copy of a job fact |
| Verification | Existing trusted probes and the document gate | Conformance over every live job; static validation | Pin a job count or mask |
| Documents | Generated blocks in design and audit Markdown | Human-readable views | Hold numbers that are not generated |

## 4. Content layer

### 4.1 Layout

```text
content/
  .gdignore
  jobs/
    _ledger.json          append-only allocation of job IDs and star bits, tombstones, aliases
    chef.json … teacher.json   one record per job (15 today)
  tokens.json             design tokens (touch size, help timings, latency, loudness …)
```

One file per job keeps concurrent branches from colliding: today every new
job edits the same dozen shared files, which is where parallel agents
conflict.

### 4.2 The job record

The full contract is [`schema/job_record.schema.json`](schema/job_record.schema.json);
[`examples/teacher.job.json`](examples/teacher.job.json) is a complete record
built from today's Teacher.

| Section | Fields | Replaces |
|---|---|---|
| Identity | `id`, `aliases`, `status` (`LIVE`, `PRACTICE`, `PROTOTYPE`, `PLANNED`, `RETIRED`), `family` (`opera_career`, `venue_scene`, `party_job`, `room_job`), `title`, `career_label`, `owner_decision` | `ACTS` identity fields, naming variants |
| Allocation | `star_bit` (from the ledger) or `progress_key` | `save_bit`, masks, counts, clamps |
| Home | `room`, `room_order`, `venue` (floor and door, for the four-floor venue), `crest` | `ROOM_ACT_INDICES`, `CAREER_CREST_FILES`, venue floor lists |
| Presentation | `colors` (floor, trim, curtain, accent, overlay), `backdrop`, `actors` (card, partner, partner visibility), `goal_prop` | `ACTS` colours, `CAREER_COLORS`, `PALETTES`, actor/partner branches, `GOAL_PROPS` |
| Phases | ordered list: `name`, `mode`, `goal`, `vo`, `station`, `hotspot`, `alias`, `final_act`; plus `finale_start`, `practice_count` | `PHASES`, `FINALE_START`, `PHASE_STATIONS`, `HOTSPOT_PHASE_ALIASES`, `EXPECTED_PHASES`, `SPECS`, `PRACTICE_COUNTS` |
| Surface and capabilities | `surface` (path or `gesture`), `capabilities` (named flags the host reads instead of testing the ID) | The specialist if-chain and ID branches |
| Voice | `engine`, `speaker`, `folder`, `prefix`, `required_keys`, `intro_line`, `win_line`, `win_suffix` | Hard-coded prefixes in `scripts/audio_director.gd`, audio-audit folder lists |
| Music | `cue` | `ACTS.music`, `EXPECTED_IDS`, `REQUIRED_AREA_MUSIC` |
| Art | `costume_sheet` with SHA-256, `provenance`, `props`, `tiles` | The atlas gate's career list, provenance lookups |
| Save | `checkpoint` (`key`, `schema_version`); the phase bound is derived from the phase count | Two copied validators, uneven key registration, slot-keyed clean-up |
| Competition and mastery | `competition` (`par_time`, `rival_cap`, `cooperative`, `timed_retry`), `mastery` (`min_actions`, medal thresholds), `two_act` | `CAREERS`, `RULES`, `ENABLED` |
| Contest | `contest` (`DL-INT-14` fields: archetype, skill, venue, player, imp, flub, voice, art) | The contest specification's per-career block |
| Chapter 2 | `chapter2` (`party_role`, `room`, `piece`, `guide_order`) or null | `LIVE_CAREERS`, `ALL_PARTY_MASK`, `GUIDE_ORDER`, `ACT_*` |
| Inventories | `living_world` row, `stage_inventory` row ID | Living-world Opera rows, stage-path IDs |
| Verification | `probes` (trusted probes that cover it), `docs` (design document) | Probe roster guesses |

### 4.3 The allocation ledger

`content/jobs/_ledger.json` is append-only. Each entry: `id`, `star_bit` or
`null`, `allocated` (date and commit), `status`, and for tombstones the
owner ruling that retired them. Bits 4, 9 and 14 stay tombstones forever
(`DL-SAVE-06`). Aliases live here (`candymaker` ↔ `candy_maker`, `candy`), so
Chapter 2 keys, crest file names and stage IDs resolve without renaming
anything saved or shipped. The checker refuses an edit that removes, reorders,
reuses or re-points an entry.

### 4.4 Tokens

`content/tokens.json` holds the design constants from the
[refinement handoff](../codex_master_audit_refinement_2026-09-30/seed/tokens_seed.json)
(touch minimum, response frames, text sizes, latency, loudness, help
timings). They compile to `scripts/generated/design_tokens.gd`;
`StorybookUI.MIN_TOUCH` and future help ladders read them. Values only change
with the rule or owner decision behind them.

## 5. Build layer: `tools/content_build.py`

| Command | Does |
|---|---|
| `--write` | Validates content, then writes `scripts/generated/job_catalog_data.gd`, `scripts/generated/design_tokens.gd`, and the generated blocks in design and audit documents |
| `--check` | Re-runs validation and fails if any generated output differs from what `--write` would produce |
| `--explain <id>` | Prints every place the job reaches: registries, files, probes, voice keys, assets, documents |

**Generated file rules.** A header line `# GENERATED by tools/content_build.py
— do not edit`; deterministic ordering; typed constants; for the migration
period, *compatibility shapes* identical to today's literals (`ACTS` with its
tombstone dictionaries, `ROOM_ACT_INDICES`, `PHASES`, `FINALE_START`, …) so a
consumer switches by replacing one literal with one reference.

**Validation rules (each a numbered error the checker can report):**

1. The record matches the schema; IDs and aliases are unique across the ledger.
2. The ledger is append-only; tombstones keep their bits; no bit is reused.
3. `room` exists in the castle room list; `room_order` is unique within the room.
4. Phases are non-empty; `finale_start` is inside the phase list; every
   `station` exists in the stage paths.
5. Every `required_keys` voice file exists in the job's folder, or the job is
   `PROTOTYPE`/`PRACTICE` with the gap listed.
6. The music cue OGG exists and the cue is known to the music build.
7. The costume sheet exists, matches its SHA-256 and is in the atlas gate's list.
8. The crest, goal prop, partner and tiles exist.
9. The checkpoint key is registered in every save key list it needs.
10. The star ceiling covers the highest allocated bit.
11. A `party_job` role uses a bit the Chapter 2 plan can hold (today below 16).
12. A competitive career has a `contest` block once `DL-INT-14` lands.
13. Each `probes` entry is in both trusted rosters.
14. The `docs` entry exists and has a document-ledger row.
15. Generated outputs are current.

**Where it runs.** `tools/audit_document_authority.py` imports the checker
the way it already imports `navigation_issues` from
`tools/audit_development.py`, so both CI runners execute it without a
workflow change. A dedicated CI step is optional and owner-gated.

## 6. Runtime layer

### 6.1 `JobCatalog`

`scripts/job_catalog.gd` (`class_name JobCatalog`) is a stateless static API
over `JobCatalogData`: `job(id)`, `live_jobs()`, `jobs_in_room(room)`,
`star_bit(id)`, `active_star_mask()`, `star_ceiling()`, `phases(id)`,
`voice_route_for(event)`, `music_cue(id)`, `checkpoint(id)`, `contest(id)`,
`capability(id, name)`, `resolve_alias(name)`. It has no state, so it is not an
autoload and does not reopen design 08's owner point 2 (services as owned
objects); probes that build `main.tscn` fresh see identical data.

### 6.2 Consumers, one at a time

| Consumer | Change | Behaviour |
|---|---|---|
| `scripts/opera_house.gd` | `ACTS`, `LIVE_ACT_INDICES`, `RETIRED_ACT_INDICES`, both masks and the count become references to generated constants; completion clean-up loops over `JobCatalog.checkpoint(id)` instead of `finished == 17` and the `"geologist"` test | Identical |
| `scripts/save_state.gd` | Masks, count, loop bound and the four clamps read `JobCatalogData`; one generic checkpoint validator replaces the two copies; each job's key is registered from the catalogue | Identical for every existing save; bit 18 becomes safe |
| `scripts/castle_career_routes.gd`, `scripts/opera_house_venue_2d.gd` | Room table, crest map and venue placement come from `home` | Identical; the four-floor venue reads `home.venue` when it lands |
| `scripts/opera_career_world_2d.gd` | `PHASES`, `FINALE_START`, `PHASE_STATIONS`, `GOAL_PROPS` and aliases come from the catalogue; the specialist if-chain becomes `JobCatalog.job(id).surface`; ID branches become capability lookups, one family per commit | Identical |
| `scripts/opera_competition.gd`, `scripts/opera_mastery.gd`, `scripts/opera_performance_plan.gd`, `scripts/opera_performance_overlay.gd` | Tables generated from `competition`, `mastery`, `two_act`, `colors` | Identical |
| `scripts/audio_director.gd` | Voice folders and prefixes come from `voice`; the exact-clip rule reads the same table | Identical |
| `scripts/living_world_catalog.gd`, `scripts/chapter_two_party_plan.gd`, `scripts/chapter_two_career_scene_adapter.gd` | Opera rows, party masks, guide order and valid modes generated | Identical (living-world names change only by owner choice) |

### 6.3 Capabilities instead of ID branches

The host asks what a job *does*, not who it is. Examples, each replacing a
family of `career_id ==` branches: `hide_partner`, `partner_actor`,
`roshan_actor_atlas`, `uses_room_tiles`, `two_act_show`,
`cooperative_win_suffix`, `nursery_catch_overlay`. Capabilities are declared
in the record and listed in the schema, so a new capability is a reviewed
addition, not a silent string.

### 6.4 Save

- **Now (behaviour-identical):** every bound derives from the ledger, so the
  next job's bit is safe. One generic validator, keyed by job, accepts
  `phase_index` up to that job's phase count.
- **Later (owner-gated):** completion keyed by job ID in an additive
  dictionary, mirroring the bits for existing jobs. Precedents already exist:
  `opera_mastery.best_tiers`, `medals` and `opera_performance_checkpoints` are
  keyed by career ID. Keys are only added, with defaults (`DL-SAVE-01`).

## 7. JobKit — the plumbing every job shares

`scripts/jobkit/` holds small components a job host or surface composes.

| Component | Pattern it implements | Replaces |
|---|---|---|
| `JobSurface` contract and `JobContext` | One doorway for specialist surfaces: `start`, `probe_surface`, `cancel`, signals for phase done and help needed | Per-surface wiring in the host |
| `HelpLadder` | One help ladder (timings from tokens) | Five different ladders |
| `GuidedTarget` | One highlighted target; highlight drawn from the painted object, not the touch box | Per-area highlight code |
| `ExactVoice` | Every required line resolved from `voice.required_keys`; a missing line is a visible probe gap, never a generic cheer | Prefix lists and caption fallbacks |
| `RewardCeremony` | One celebration, pooled and tier-aware | Several celebration implementations |
| `RoshanAtWork` | Travel, contact, work, then completion, using the existing stage navigation | Per-job arrival code (`MA-PLAY-004`) |
| `ImpContest` | The `DL-INT-14` contest, parameterized by the record's `contest` block | Twelve hand-built contests |
| `PhaseCheckpoint` | Generic mid-activity save and restore by job | Copied validators and slot-keyed clean-up |

JobKit calls design 08's Services (objective, fx, reward, input) once they
exist. Until then each component delegates to today's main methods from one
place, so the private calls into `main.gd` live in JobKit only and move to
Services in one sweep at M4. The 6,232-line generic gesture surface stays as
it is; its decomposition remains WP-B2 of the
[2026-08-26 handoff](../../../CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md).

## 8. Verification layer

- **Static.** `tools/content_build.py --check`, called from the document gate,
  with unit tests that inject faults: an unregistered act, a reused tombstone
  bit, a star ceiling below the highest bit, a missing voice key, a missing
  costume sheet, a job without a trusted probe, a stale generated file.
- **Runtime.** Probes read expectations from `JobCatalog` instead of
  literals: `ACTS.size()`, the counts, masks, the 61-phase and 70-unit totals,
  the room table copy and the per-career lists in `scripts/probe_opera.gd`,
  `scripts/probe_opera_2d.gd`, `scripts/probe_living_world.gd`,
  `scripts/probe_opera_nursery.gd`, `scripts/probe_opera_mastery.gd` and
  `scripts/probe_chapter2.gd`.
- **Conformance loop.** A routine inside `scripts/probe_opera.gd` (already in
  both trusted rosters) walks every live job: launch from its room, drive its
  phases through `probe_surface`, record which voice keys it requests, run an
  idle leg that must not award anything, complete it, check the star or
  progress write, check the exact-room return, tear down, re-enter, reload the
  save. A new job is covered the moment its record exists.
- **Growth-law test for jobs.** On a throwaway branch, add a hidden practice
  job (record plus a trivial surface), run `--write`, and show that the diff
  touches no registry, probe or tool by hand and that the suite passes. Repeat
  it at every audit round, like design 08 §8.

## 9. Documents

- Job tables, counts and the game map in the planned design reference and
  job playbook are generated blocks.
- The master audit's live status reads counts from the catalogue.
- Rules that pin counts (`DL-INT-07`, `DL-SAVE-06`, `DL-QA-12`) are amended,
  with the owner's approval, to cite the shipping table in `content/jobs`
  instead of numbers.

## 10. How it fits the existing plans

| Plan | Relationship |
|---|---|
| [Design 08 Mode Platform](../../../design/08_TARGET_ARCHITECTURE.md) | Complementary. The Opera entry becomes one `ModeRegistry` row at M2; the Job Platform is that mode's internal registry. Compiling to `const` keeps the analyzer-checked property of §9 point 4 while letting tools read the data. `JobCatalog` is stateless, consistent with point 2. Jobs already touch `main.gd` zero times; this makes them touch the other twenty-plus files zero times too |
| [Refinement handoff Stage J](../codex_master_audit_refinement_2026-09-30/README.md) | The WP-J1 catalogue *is* this content layer (`content/jobs/`, compiled), not a documentation-only mirror. The WP-J2 playbook becomes short: write a record, a surface if needed, assets, then `--write` |
| [Imp contest handoff](../codex_opera_imp_contest_2026-09-30/README.md) (`DL-INT-14`) | Contest data lives in each record's `contest` block; `ImpContest` runs it; the generic checkpoint validator removes the hard-coded phase bound before contests add phases |
| Four-floor Opera House (owner direction 2026-09-24) | Door placement comes from `home.venue` |
| Findings | Closes the job half of `MA-DOC-006`; gives `MA-CODE-003` and `MA-CODE-004` a target (one implementation per pattern, typed lookups); makes passive coverage per job automatic (`MA-CI-005`); exposes exact-voice gaps per job (`MA-ACCESS-001`); hosts `RoshanAtWork` for `MA-PLAY-004` |

## 11. Migration in safe steps

| Step | Work | Proof |
|---|---|---|
| JP0 | Content model, ledger, schema, the real extractor (from this prototype), generator emitting compatibility shapes, and an equality probe asserting generated equals literal for every registry | All registries equal; suite green; nothing reads the generated file yet |
| JP1 | Save bounds and the generic checkpoint validator read the catalogue | Save probes byte-stable; a test with a synthetic bit-18 ledger entry shows no corruption |
| JP2 | Consumers switch one per commit (house, routes, venue, world tables, competition, mastery, performance, overlay, audio, living world, Chapter 2) | Probe transcripts byte-stable per commit; the replaced literal is deleted |
| JP3 | Probes derive expectations; the conformance loop lands in `probe_opera` | A throwaway extra record changes no probe line and passes |
| JP4 | Tools read the catalogue: music build, atlas gate, audio ledger, stage-path inventory; the stage-path check runs from the document gate | Geologist cue and both costume sheets covered; injected tool faults fail |
| JP5 | JobKit wraps today's behaviour (help, guide, voice, reward, checkpoint), then the ID branches move to capabilities one family per commit | Byte-stable probes; ID-branch count falls to the specialist surfaces only |
| JP6 | Generated document blocks; rule-text amendments with owner approval; the playbook rewritten around the record | Document gate green; no pinned counts in rules |
| JP7 | Owner-gated: job-ID-keyed completion | Save migration tests both ways |
| JP8 | With design 08 M2: Opera entry becomes a `ModeRegistry` row | Design 08 gates |

## 12. Worked example: promoting the Tree Book to a permanent career

Hypothetical and not commissioned: promoting the Arborist practice scene to a
career needs the owner's approval (`OQ-ARBORIST-DAY2` in the refinement
handoff; `DL-PLAN-01`).

| Work | Today (reconstructed) | With the Job Platform |
|---|---|---|
| Identity, slot, masks, count, clamps | `opera_house.gd` (4 constants plus an `ACTS` row), `save_state.gd` (2 constants, loop, 4 clamps) | `content/jobs/arborist.json` plus one ledger line |
| Phases, finale, stations, goal prop, aliases | `opera_career_world_2d.gd` (5 tables) | The record's `phases` |
| Specialist surface | New surface plus an if-chain branch and ID branches | New `scripts/opera_arborist_surface.gd` implementing `JobSurface`; capabilities in the record |
| Room card, crest | `castle_career_routes.gd`, probe copy | `home` |
| Competition, mastery, overlay, performance | Four scripts | The record |
| Voice | Clips plus a hard-coded prefix in `audio_director.gd` and the audio audit | Clips (Codex generates new lines with the declared engine) plus `voice` in the record |
| Music | Score, ordered `EXPECTED_IDS`, `REQUIRED_AREA_MUSIC` | Score plus `music.cue` |
| Costume sheet | Built by Codex; atlas gate list edited by hand | Built by Codex; hash in the record |
| Living world, stage inventory, hotspot specs | Three files | The record (stage geometry still measured from the painting) |
| Probes | Six pinned counts plus the room copy | None; the conformance loop covers it |
| Documents | Hand-edited counts | Regenerated |
| Hand-edited files | About 25 | About 4 (record, ledger line, surface, music score) plus assets |

## 13. Risks and how the design handles them

| Risk | Handling |
|---|---|
| Generated files drift from content | `--check` in the document gate; header forbids edits |
| A refactor changes behaviour | JP0 equality probe; byte-stable probe transcripts per commit; revert on any difference (`DL-CODE-06`) |
| Save corruption | Values identical by construction in JP1; legacy fixtures (`0xFFFF`, `0x3FFFF`) and a synthetic bit-18 test |
| Merge conflicts with in-flight branches (Day Two alpha, imp contest, four-floor venue) | JP2 consumers switch after those land, or are rebased on them; per-job files avoid conflicts afterwards |
| Colour and float literals change in round trip | The generator emits the literal text the extractor read; equality is checked on parsed values |
| Over-abstraction | Capabilities are added only when a second job needs the same branch; one-off behaviour stays in that job's surface |
| Hidden export problems | No runtime JSON; generated scripts export like any script |
| Tools that regex-parse source | They read `content/jobs` instead (JP4) |

---

## Appendix A — registry inventory *(sweep, key rows verified)*

| Registry | Where | Per-job data | Derivable from the record? |
|---|---|---|---|
| `ACTS`, `LIVE_ACT_INDICES`, `RETIRED_ACT_INDICES`, masks, count | `scripts/opera_house.gd:9-152` | identity, colours, music, win line | Yes |
| Masks, count, loop, clamps, checkpoint validators and key lists | `scripts/save_state.gd:11-12`, `:34-76`, `:86`, `:198`, `:294`, `:567`, `:582`, `:619`, `:681`, `:715-764` | bounds and keys | Yes |
| `PHASES`, `FINALE_START`, `PHASE_STATIONS`, `HOTSPOT_PHASE_ALIASES`, `GOAL_PROPS` | `scripts/opera_career_world_2d.gd:262-463` | phases | Yes |
| Specialist surface choice, actor and partner branches | `scripts/opera_career_world_2d.gd:1203-1294` | surface, actors | Yes (capabilities) |
| `CAREERS` | `scripts/opera_competition.gd:12-141` | competition | Yes |
| `RULES` | `scripts/opera_mastery.gd:35-51` | mastery | Yes |
| `ENABLED`, `PRACTICE_COUNTS` | `scripts/opera_performance_plan.gd:8-14` | two-act, practice | Yes |
| `CAREER_COLORS` | `scripts/opera_performance_overlay.gd:12-21` | overlay colour | Yes |
| `EXPECTED_PHASES`, `SPECS`, `ASSET_META` | `scripts/opera_hotspot_catalog.gd:24-197` | hotspots | Mostly (dimensions measured) |
| `PATHS`, `STATION_NAV`, `ROAM`, `BLEED` | `scripts/opera_stage_paths.gd` | stage geometry | Partly (geometry measured from art) |
| `PALETTES`, tile naming | `scripts/opera_world_backdrop_2d.gd` | backdrop | Yes (draw functions stay code) |
| `ROOM_ACT_INDICES`, `CAREER_CREST_FILES` | `scripts/castle_career_routes.gd:20-50` | home, crest | Yes |
| Venue floor list and portals | `scripts/opera_house_venue_2d.gd:24-47` | venue | Yes |
| Opera rows, `EXPECTED_STAGE_COUNT` | `scripts/living_world_catalog.gd` | living world | Yes |
| Voice routing | `scripts/audio_director.gd:194-235`, `:269` | voice | Yes |
| `LIVE_CAREERS`, `ALL_PARTY_MASK`, `GUIDE_ORDER`, adapter `VALID_MODES`, `PHASE_SETS` | `scripts/chapter_two_party_plan.gd`, `scripts/chapter_two_career_scene_adapter.gd`, `scripts/chapter_two_director.gd` | Chapter 2 role | Mostly (story glue stays code) |
| Tool lists | `tools/audit_opera_roshan_animation.py`, `tools/build_area_music.py`, `tools/audit_audio_quality.py`, `tools/audit_stage_pathfinding.py` | — | Yes (tools read content) |
| Probe pins | `scripts/probe_opera.gd`, `probe_opera_2d.gd`, `probe_living_world.gd`, `probe_opera_nursery.gd`, `probe_opera_mastery.gd`, `probe_chapter2.gd`, `probe_opera_diegetic_paths.gd` | — | Yes (derived expectations) |

**Stays hand-written per job:** specialist surface scripts and the per-career
behaviour inside the generic gesture surface; vector backdrop draw functions;
measured stage geometry; mid-phase checkpoint contents; Chapter 2 story glue;
contest mechanics beyond the shared runner; prose; assets and recordings;
behavioural probe assertions specific to a job.

## Appendix B — files in this packet that support the design

- `tools/extract_job_catalog.py` and its outputs `data/extracted_catalog.json`
  (15 records and 3 tombstones from today's code) and
  `data/derivation_check.json` (the eleven equalities and the drift list).
- `schema/job_record.schema.json` — the record contract.
- `examples/teacher.job.json` and `examples/ledger.example.json` — a complete
  record and a ledger built from today's values.
