# Job-game development and takeover readiness audit (2026-09-30)

**Status:** `SUPPORTING_CURRENT` audit. Static and Git-history evidence (V1)
at `dev` `5d9668a9a49f59f3224c2951bbbffb9e3b3a1145`; no runtime, device,
child or owner result is claimed. Prepared by Claude (analysis only; no game
change). Tracking finding:
[`MA-DOC-006`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-006).

**Owner request (2026-09-30):** *"Does the master audit serve as a script for
developing future job games for Roshan? The ultimate purpose of this is to take
over development of mermaid Roshan, and an audit to insure this is included is
critical."*

## 1. Verdict

| Question | Answer |
|---|---|
| Does the [master audit](MASTER_AUDIT_2026-08-09.md) serve as a script for developing a new job game? | **No.** Its task index routes chapters, repairs, code, art, touch, audio, animation, cinematics, save, performance and acceptance, but has no route for a job game. The closest line sends new content to the chapter guide, which has no job recipe. No document holds the end-to-end recipe; it lives in Git history, in about 25 code registries, and in probes that fail when a step is missed. |
| Could an agent take over development from the repository alone? | **Partly.** The rules, change-record contract, acceptance levels, branching and CI are documented and current. The job recipe, job registration, voice pipeline, job template, owner-decision register, roles, backup status, APK tooling notes and the priority queue are missing, stale or code-only (section 7). |
| Did the 2026-09-30 refinement handoff include it? | **No.** Its new-designer test covers design-reference questions only; it asks nothing about registering a career, voices, save bits, releases, backups or roles. Revision 3 of that handoff adds Stage J (section 11). |

A concrete trap shows the cost. The next career will take star bit 18, but
`opera_stars` is clamped to `262143` (bits 0–17) in four places in
[`scripts/save_state.gd`](../scripts/save_state.gd) (`:198`, `:294`, `:619`,
`:681`) and counted by a `range(18)` loop (`:86`). A save that holds bit 18 is
clamped to `262143`, which sets every bit from 0 to 17: every live career would
read as complete and the retired raw bits 4, 9 and 14 would be overwritten. The
only record of this step is commit `f4a5de33`, which raised the clamp when
Teacher and Geologist took bits 16 and 17. `DL-SAVE-06` still describes a
"16-slot" namespace and a `main.gd` comment says "17-slot".

## 2. Scope and method

A **job game** is any activity in which Roshan does a job. Four extension paths
exist in code (section 5): an Opera career row (all 15 shipped careers), a
standalone scene reached from the Opera House venue (the Tree Book practice), a
Chapter 2 party job, and a Day One room job.

Evidence: the commits that added or rebuilt jobs — `3d6b9ba6` (Geologist first
added at bit 16, 30 files), `f4a5de33` (Teacher, Geologist, Racer engine and
two-act shows, 155 files), `831f3eb4` (Tree Book practice, 64 files), the
Chapter 2 adapter history (`91b55ec4`, `3c3fa13f`, `c64919f1`), the specialist
rebuilds (`39746756` Candymaker, `8d67c2bd` Boxer, `dc48c91a` Ballerina) and
`09e5e356` (castle-room distribution); the code registries at the baseline; a
sweep of the master audit, design 00–10, templates, handoffs, `AGENTS.md`,
`CLAUDE.md` and the operations documents; and read-only GitHub queries of
workflow runs. Claims re-read directly by Claude are stated as facts; items
from the read-only sweeps are marked *(sweep)*.

## 3. What building a job game touches today

Adding one Opera career touches about 25 code and data files and at least six
trusted probes that pin counts by hand.

| Role | Files and symbols (at the baseline) |
|---|---|
| Registries | `scripts/opera_house.gd` (`ACTS`, `LIVE_ACT_INDICES`, `ACTIVE_STAR_MASK`, `ACTIVE_ACT_COUNT`); `scripts/save_state.gd` (`OPERA_ACTIVE_STAR_MASK`, `OPERA_ACTIVE_ACT_COUNT`, the bit loop and four clamps); `scripts/opera_competition.gd` (`CAREERS`); `scripts/opera_hotspot_catalog.gd`; `scripts/opera_stage_paths.gd`; `scripts/castle_career_routes.gd` (`ROOM_ACT_INDICES`); `scripts/living_world_catalog.gd`; `scripts/opera_mastery.gd`; `scripts/opera_performance_overlay.gd`; `scripts/chapter_two_career_scene_adapter.gd` (`VALID_MODES`) |
| Job engine | `scripts/opera_career_world_2d.gd` (`PHASES`, `FINALE_START`, `PHASE_STATIONS`, `GOAL_PROPS`, actor and specialist-surface branches); a new `scripts/opera_<job>_surface.gd` when the job needs its own surface; `scripts/opera_world_backdrop_2d.gd` (`PALETTES` or tile files) |
| Audio | Voice clips in `assets/audio/<job>/`; the folder prefix in `scripts/audio_director.gd` (`:202-213`, `:262`); `category()` and hard-coded folders in `tools/audit_audio_quality.py`; a music score in `assets_src/audio/music/area_music_scores.json` with the ordered `EXPECTED_IDS` in `tools/build_area_music.py`; `REQUIRED_AREA_MUSIC` in `scripts/probe_audio.gd` |
| Art | Roshan costume sheet `assets/opera/worlds/actors/animation/roshan_<job>_sheet_a.png` (1024×1024, 4×4: idle, travel, work, cheer; 256-px cells), crest, hotspot art with a transparent border, backdrop; provenance under `assets_src/`; `ASSET_LICENSES.md` rows |
| Probes | `scripts/probe_opera.gd` (`:91-93` pins the live list, `ACTIVE_ACT_COUNT == 15` and mask `0x3BDEF`; `EXPECTED_ROOM_ACTS`), `scripts/probe_opera_2d.gd` (`:159` 61 phases, `:1343` 15 careers, `:1345` 70 phase units), `scripts/probe_opera_nursery.gd:31`, `scripts/probe_living_world.gd:137`, `scripts/probe_audio.gd:59` |
| Governance | Impact record, design document, ledger row, typography manifest entries for new characters, `audit/stage_pathfinding/stage_inventory.json` row |

`f4a5de33` shows the scale: 31 scripts, 17 voice clips, a music cue, the save
mask, room routes, seven probes, three tools and four design documents in one
commit.

## 4. Interim job-game recipe

This is the script the repository does not yet have. It is reconstructed from
the commits above, so verify every line at your head. It is **interim**: Stage J of the
[refinement handoff](../docs/handoffs/codex_master_audit_refinement_2026-09-30/README.md)
turns it into a maintained playbook with a checker. Roles follow `CLAUDE.md`:
the owner decides, Claude writes specifications and audits, Codex builds code,
images and generated audio.

### 4.1 Decide (owner and designer)

| Step | What | Rules and sources |
|---|---|---|
| D1 | Get the owner's approval of the job's premise and home. A new permanent career is a major addition; a practice or prototype job inside an approved chapter scope is delegated | `DL-PLAN-01`, `DL-PLAN-05` |
| D2 | Choose the extension path (section 5): an Opera career row for a permanent job, a venue scene for a prototype; a Chapter 2 or Day One job only with owner approval | Section 5 |
| D3 | Check the live constraints: the owner retired `DL-INT-12` on 2026-09-24 for a four-floor venue that is not built (the current venue's three portals are fixed to acts 2, 8 and 13 in `scripts/opera_house_venue_2d.gd:24-34`); `DL-INT-14` makes the final act of a competitive career an imp contest (target contract); the Chapter 2 roster is locked below bit 16 (`scripts/chapter_two_party_plan.gd:35`); Candy Maker is reserved for a later section *(sweep)*; a new career card is hidden while Chapter 2 is active (`scripts/castle_career_routes.gd:330-341`) | `DL-INT-12`, `DL-INT-14`, [imp contest design](../docs/handoffs/codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md) |
| D4 | Write the job card: the job's signature object and verb per phase, one finger, kind feedback, help that never pays, passive play never wins, Roshan travels and makes contact, rewards and medals, the imp contest if competitive, exact voice lines, art reuse and gaps (in words; Codex builds images), music cue, save design, acceptance plan | `DL-INT-07`, `DL-AGE-01`–`DL-AGE-05`, `DL-INT-02`, `DL-INT-06`, `DL-SND-13`, `DL-ASSET-01`, [two-act shows](../design/OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md) |

### 4.2 Build (Codex) — Opera career path

| Step | Add or change (file: symbol) | What fails if skipped | Documented today? |
|---|---|---|---|
| B0 | Impact record, design document and ledger row | `tools/audit_development.py --base auto`, `tools/audit_document_authority.py` | Yes (`design/AUDIT_DEVELOPMENT_CONTRACT.md`) |
| B1 | `scripts/opera_house.gd`: append `ACTS[18]` (list index equals `save_bit`; keys start `save_bit, name, career`); add 18 to `LIVE_ACT_INDICES`; `ACTIVE_STAR_MASK` becomes `0x7BDEF`; `ACTIVE_ACT_COUNT` becomes 16 | `scripts/probe_opera.gd:91-93`, `scripts/probe_opera_nursery.gd:31`, `scripts/probe_living_world.gd:137`, `scripts/probe_audio.gd:59` | No |
| B2 | `scripts/save_state.gd`: `OPERA_ACTIVE_STAR_MASK`, `OPERA_ACTIVE_ACT_COUNT`, `range(18)` at `:86` to `range(19)`, clamp `262143` to `524287` at `:198`, `:294`, `:619`, `:681`; any per-job checkpoint key with its normaliser; the checkpoint clean-up in `scripts/opera_house.gd:283-286` | Nothing unless `probe_opera.gd` `_audit_save_matrix` gains a bit-18 case; otherwise progress is silently corrupted (section 1) | No |
| B3 | `scripts/opera_competition.gd` `CAREERS[<id>]` | `OperaAct.supports_config` refuses the career; `probe_opera`, `probe_opera_2d` fail | Contract only, in `OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md` |
| B4 | `scripts/opera_career_world_2d.gd` `PHASES`, `FINALE_START`, `PHASE_STATIONS`, `GOAL_PROPS`, actor or partner branch, specialist surface branch; `scripts/opera_mastery.gd` `CAREERS`/`RULES`; `scripts/opera_performance_overlay.gd` `CAREER_COLORS` | `probe_opera_2d.gd:159`, `:1343`, `:1345`; `probe_opera_gesture_quality` | Per-career documents only |
| B5 | `scripts/opera_hotspot_catalog.gd` `EXPECTED_PHASES`, `SPECS`, `ASSET_META` | `validate_specs()` inside `probe_opera_2d` | Code comments only |
| B6 | `scripts/opera_stage_paths.gd` `PATHS`, `STATION_NAV`; `audit/stage_pathfinding/stage_inventory.json` row `opera.act.18.<slug>` | `probe_opera_2d` route checks; `tools/audit_stage_pathfinding.py --check` would fail but runs in neither `scripts/ci.sh` nor `.github/workflows/probes.yml` | Partly ([protocol](stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md)) |
| B7 | Backdrop: `scripts/opera_world_backdrop_2d.gd` `PALETTES` plus a draw function, or 2×2 tiles | Barely checked | Only the 2048-px rule (`DL-LAY-07`) |
| B8 | Roshan costume sheet (spec in section 6), crest, rival or partner art; add the job to `CAREERS` in `tools/audit_opera_roshan_animation.py` | `probe_opera_2d.gd:260-274` and missing-resource errors; the atlas gate itself lists only 13 careers, so it will not check a new sheet unless extended | Per-career `PROVENANCE.md` only |
| B9 | `scripts/castle_career_routes.gd` `ROOM_ACT_INDICES` (not `opera_hall`); `EXPECTED_ROOM_ACTS` in `scripts/probe_opera.gd` | `probe_opera.gd:98-110`, `probe_opera_2d.gd:295` | Stale room table in `design/01_GAME_DESIGN.md` |
| B10 | Music cue: score plus ordered `EXPECTED_IDS`, then `python tools/build_area_music.py --cue opera_<id>`; or a byte-identical reuse (the Geologist precedent); `REQUIRED_AREA_MUSIC` in `probe_audio.gd` | `tools/build_area_music.py --check`; `probe_audio` | Partly (`DL-SND-06`, `DL-SND-07`) |
| B11 | Voice clips (section 6), prefix route in `scripts/audio_director.gd`, `category()` in `tools/audit_audio_quality.py`, regenerate the audio ledger | `tools/audit_audio_quality.py --check` (only in `scripts/ci.sh`); no gate notices a phase without a recording, which falls back to a caption silently | No |
| B12 | `scripts/living_world_catalog.gd` row and `EXPECTED_STAGE_COUNT`; `scripts/probe_living_world.gd` | `probe_living_world` | No |
| B13 | Typography manifest entries for new characters; `ASSET_LICENSES.md` rows; 2D nodes only | `tools/audit_typography.py --check` (only in `scripts/ci.sh`); `tools/audit_game_2d.py --regression-gate`; licence rows are not gated | Rules only |
| B14 | Extend existing trusted probes; a new trusted probe must be added to both `scripts/ci.sh` and `.github/workflows/probes.yml` (a high-risk file) | `tools/audit_probe_parity.py` | High-risk rule only |

### 4.3 Verify, integrate and accept

| Step | What |
|---|---|
| V1 | Static gates, focused probes, the full `scripts/ci.sh`, then CI green at the branch head. Run the checks CI does not run: `tools/audit_stage_pathfinding.py --check`, the extended atlas audit, a voice-per-phase review and licence rows |
| V2 | Mobile captures of every phase at 1280×720 and a wide phone; human review |
| V3 | Merge into `dev`; play the `android-dev` build on the phone and M11; observed child session; owner review (`DL-QA-04`–`DL-QA-06`) |
| V4 | With owner approval, update rule text that pins counts (`DL-INT-07`, `DL-SAVE-06`, `DL-QA-12`), record the lessons (`DL-PLAN-06`) and correct this recipe |
| V5 | Promotion to `master` only when the owner says so (`CLAUDE.md` release shorthand) |

## 5. Choosing an extension path

| Path | Built as | Save | Reached by | Protected by | Use for |
|---|---|---|---|---|---|
| (a) Opera career row (Teacher, Geologist) | `OperaHouse` → `OperaAct` → `OperaCareerWorld2D` | A bit in `opera_stars`, plus medals | A picture card in a castle room; hidden during Day One and while Chapter 2 is active | Six trusted probes | Every permanent job |
| (b) Venue scene (Tree Book) | `scripts/opera_house_venue_2d.gd` `_build_practice_book` → `m._navigation_push(...)` (`:479`) | Its own key, outside the career namespace | The Opera House foyer | Checks inside `probe_opera_2d` | Prototypes and practice; about 10 files, no mask or count changes |
| (c) Chapter 2 party job | `reward_policy: "chapter2_story"`, adapter `PHASE_SETS`, `ChapterTwoPartyPlan` | Chapter 2 masks; bits below 16 only | In story order (`GUIDE_ORDER`) | `probe_chapter2*` are in neither trusted roster *(sweep)* | Only with owner approval (story canon) |
| (d) Day One room job | `scripts/games/*.gd` plus `DayOneDirector` | `day_one_*` keys | The fixed Day One sequence | `probe_day_one_*` | Only with owner approval |

## 6. Pipelines

- **Roshan costume sheets:** image generation from a Roshan identity reference
  plus another career's sheet as a layout reference; a per-career builder
  (`tools/build_teacher_actor.py` is the worked example) removes the background;
  `tools/prepare_opera_roshan_animation.py` packs the 1024×1024 4×4 sheet; each
  career keeps a `PROVENANCE.md` with hashes, prompts and rejected attempts.
  Under `CLAUDE.md` (2026-09-30) Claude describes the art in words and Codex
  produces it. The blocking atlas gate does not check the Geologist and Teacher
  sheets today.
- **Voice:** two synthetic engines are in use and no binding document says which
  one new jobs use: Kokoro in `tools/make_voices.py` (Teacher, Chapter 2 lawn;
  48 kHz, −16 LUFS; the script writes no manifest, so Teacher's manifest was
  built separately) and Parler in `tools/make_parler_voice_trials.py` (Tree
  Book), which matches the Roshan filler layer the game prefers at runtime
  *(sweep)*. Protected family recordings are never altered (`DL-SND-05`,
  `DL-SND-11`).
- **Music:** add a score and its ordered ID, run
  `tools/build_area_music.py --cue`, and check with `--check` (in `scripts/ci.sh`
  and the Windows CI job).
- **Save bits:** 18 bits today; 16 and 17 are Geologist and Teacher; 4, 9 and
  14 are permanent tombstones (`0x4210`); the next free bit is 18 (section 1).

## 7. Can a new agent do it from the documents?

Status per capability *(sweep, with the key rows re-read)*:
`CURRENT` documented and current, `STALE` documented but wrong,
`PARTIAL`, `CODE_ONLY`, `MISSING`.

| Capability | Status | Gap |
|---|---|---|
| Deciding the job and its home | PARTIAL | Delegation covers chapters only; `DL-INT-12`'s room list is stale (the Library hosts acts 1, 16 and 17) and its retirement is recorded only in a handoff |
| Job formula and structure | PARTIAL | Analysis exists in the imp-contest handoff; no recipe; no standard help ladder |
| Registering the job | CODE_ONLY | No checklist; masks duplicated in two files; clamp trap (section 1) |
| Roshan costume sheet | PARTIAL | Layout written down only in one provenance file; gate misses two sheets |
| Props and backdrop art | PARTIAL | Rules exist; the "Codex builds images" rule is not in `AGENTS.md`, which Codex reads |
| Voice lines | PARTIAL | Two engines, two folder conventions, hard-coded prefixes |
| Music cue | STALE | Documents say 42 cues; the catalogue has 44 |
| Save, progress, rewards | STALE | "16-slot" and 13-career statements; masks `0xBDEF` and `0x1BDEF` in documents |
| Probes and CI | PARTIAL | Pinned counts undocumented; stage-path check not in CI; several job probes outside the trusted rosters |
| Acceptance | CURRENT | `DL-QA-12` binds a stale 13-career table |
| Governance paperwork | CURRENT | Heavy but correct |
| Day Two and imp contests | PARTIAL | Roster locked; imp contest is a target contract |
| Worked example or template | MISSING | No job template or card |
| Cold-start onboarding | PARTIAL | No glossary (Day One/Day Two versus Chapter), no game map |
| Owner decisions | PARTIAL | Spread over 49 files; no register |
| Roles | PARTIAL | The role rule is in `CLAUDE.md` only |
| Branching, CI, promotion | CURRENT | — |
| APK install and device testing | STALE | `docs/ANDROID_RELEASE.md` and `pull-apk.sh` describe old channels *(sweep)* |
| Backups | STALE | `CLAUDE.md` and `BACKUP.md` describe verified weekly backups; section 9 |
| Security boundaries | CURRENT | — |
| Environment | PARTIAL | Local Godot on PATH is 4.7.1 against the 4.7.2 baseline; disk space |
| Current priorities | STALE | Section 13 of the master audit cites sealed evidence; live queues sit in five handoffs |

## 8. Facts a new agent would get wrong by trusting the documents

| Fact | Documents | Code at the baseline |
|---|---|---|
| Live careers | 13 (`DL-INT-07`, `DL-SAVE-06`, master audit scorecard); 14 elsewhere *(sweep)* | 15 (`scripts/opera_house.gd:15`) |
| Star namespace | "16-slot" (`DL-SAVE-06`); "17-slot" (`scripts/main.gd:487`) | 18 bits, clamped at `262143` |
| Room owning Teacher and Geologist | Not in `DL-INT-12` | Library, with Detective (`scripts/castle_career_routes.gd`) |
| Probes that pin counts | Not documented | Section 3, probes row |
| Growth path | `DL-CODE-11`, `DL-CODE-12` (Mode Platform) | `scripts/platform/` and `tools/audit_structure.py` do not exist |
| Music cues | 42 | 44 in the catalogue |
| Backups | Verified weekly bundle | Every run failed (section 9) |

## 9. Takeover hazards found on the way

- **No backup has ever succeeded.** GitHub shows all 10 weekly
  `backup.yml` runs from 2026-07-27 to 2026-09-28 failed, and no
  `project-backup` release exists, while `CLAUDE.md` and `BACKUP.md` describe a
  verified, restore-drilled weekly bundle. Repairing the workflow is a
  high-risk workflow change for the owner to authorize; the takeover kit must
  state the real status.
- **The images rule is missing where Codex reads.** The 2026-09-30 rule
  ("Claude writes, Codex builds images") is in `CLAUDE.md` only.
- **Two shipped costume sheets are ungated**, and the stage-path coverage check
  is not in CI.
- **Local tooling is not baseline-exact.** Godot on PATH is 4.7.1; the release
  baseline is 4.7.2, so local runs are advisory and CI is authoritative.
- **Disk space.** Drive C: reached 0 bytes free on 2026-09-30 with 316
  registered worktrees; reuse a worktree rather than adding one.

## 10. What closes `MA-DOC-006`

1. A maintained job-game playbook, routed from the master-audit task index,
   whose every named file, symbol, command and gate exists at its head.
2. A machine-readable job catalogue with a checker in the existing document
   gate that fails when code registries and the catalogue disagree, proven by
   injected faults (an unregistered act, a wrong star bit, a job with no
   trusted probe).
3. A takeover kit: start-here reading order, glossary, roles, the operations
   loop, the real backup status, environment notes and the current priority
   queue, with every stale claim in sections 8 and 9 corrected or listed as an
   open owner question.
4. A cold-start dry run: a fresh agent with only the repository and a one-line
   job commission produces a job card and a complete build plan. It passes when
   the reviewer ticks every item below and the owner accepts the output.

**Dry-run checklist:** found the playbook from the entry points; chose and
justified the extension path; listed the owner decisions needed with defaults;
allocated the save bit and listed every mask, clamp and count site; listed
every registry row; listed the probes to extend and the pinned counts to
change; planned exact voice lines per objective with speaker, engine, folder,
prefix route and ledger; planned the music cue; planned art reuse, Codex
generation, the costume-sheet spec, provenance and the atlas-gate entry;
planned the room route and reachability during Day One and Chapter 2; decided
the imp-contest role; covered help, no-fail, passive and Roshan-does-the-job
checks; wrote the acceptance plan by evidence level and who grants each; listed
the impact record, ledger and licence rows; described integration and release;
needed no fact from chat history or private memory.

## 11. How this audit keeps it included

- `MA-DOC-006` sits in the master-audit index and the finding register; like
  every open P2 it blocks game-wide satisfaction until it is verified fixed.
- The master-audit task index has a **New job game** route and the planning
  entry answers "How should an agent build a new job game?", both pointing to
  section 4 until the playbook exists.
- The [refinement handoff](../docs/handoffs/codex_master_audit_refinement_2026-09-30/README.md),
  revision 3, adds Stage J (playbook, job catalogue and checker, takeover kit,
  dry run), ordered straight after its read-only Stage 0.
- Once the WP-J1 checker is in the document gate, a job that lands without its
  catalogue entry fails CI.
- After every new job lands, the finding history records whether the recipe
  held; a material change to the playbook repeats the dry run.
