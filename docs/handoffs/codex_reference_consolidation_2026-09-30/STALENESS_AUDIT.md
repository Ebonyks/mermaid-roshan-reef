# Staleness audit: the master audit and the repository's audits (2026-09-30)

**Status:** `SUPPORTING_CURRENT` audit evidence prepared by Claude (analysis
only; no game change). Static and Git-history evidence measured at `dev`
`6fc2f48e527dc20286d25455785abd9680d57368`; live counts re-run with the
repository's own tools. Tracking finding:
[`MA-DOC-007`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-007).
The execution plan is [README.md](README.md); the reference documents to build
are in [REFERENCE_PLAN.md](REFERENCE_PLAN.md).

**Owner request (2026-09-30):** *"Identifying stale elements of master audit
are the next steps, there are many outdated audits in this repo that should be
streamlined and truncated into reference documents."*

## 1. The answer

- **The master audit is mostly not current reference material.** Of its 65
  elements, 19 are current (about 27% of its bytes). The rest is sealed CI
  evidence (42%), stale fact (13%), superseded decision (9%), duplicate of the
  finding register (8%) and obsolete process (1%).
- **The finding register misleads.** 24 open findings plus the register
  preamble state something that is no longer true
  ([`data/stale_findings.json`](data/stale_findings.json)). One finding's own
  acceptance now fails: the `MA-CODE-004` command counts 456 distinct state
  keys against its 409 baseline.
- **Outdated audits outnumber current references.** Of 354 inventoried
  documents (2.26 MB of them audit-type), 119 can be archived now, 85 hold
  durable knowledge that should be absorbed into a reference and then archived,
  72 are evidence other files depend on, 76 stay as they are, and 2 are
  deletion candidates. The repository root holds 196 Markdown files; 6 need to
  stay there.
- **47 contradictions** between documents decide how a designer would
  build something, from whether the imp can win to which shot card is
  mandatory (section 5).
- **Some binding rules live only in documents that would be archived**
  (section 6). They must move into the rulebook first.

## 2. The master audit, element by element

Full register: [`data/master_audit_staleness_register.json`](data/master_audit_staleness_register.json)
(65 elements, each with a class, the current truth and a disposition).

| Class | Elements | Lines | KB | Disposition |
|---|---:|---:|---:|---|
| Current | 19 | 698 | 73.7 | Keep; this is the reference core |
| Stale fact | 21 | 322 | 36.9 | Rewrite from generated live status |
| Sealed evidence | 9 | 970 | 116.3 | Move verbatim to an archive file, keep headings |
| Superseded decision | 9 | 151 | 24.4 | Rewrite as a dated decision log entry |
| Duplicate | 6 | 164 | 21.0 | Delete with a pointer to the better home |
| Obsolete process | 1 | 45 | 2.7 | Move to the archive |

**Live facts used as the yardstick** (re-run at the measured head): the 2D
scanner reports 0 model files and 52 production 3D files; `scripts/main.gd` has
9,817 lines; there are 137 probe scripts and 82/81 trusted roster entries; the
Opera table has 15 careers, 61 phases and 36 modes with live mask `0x3BDEF`;
the music catalogue has 44 cues; the document gate reports 590 documents and
57 active findings; the Godot baseline is 4.7.2.

### The ten most misleading statements for a new developer

| # | Statement in the master audit | Truth |
|---|---|---|
| 1 | 13 careers, 53 phases, 27 modes; live mask `0xBDEF` | 15 careers, 61 phases, mask `0x3BDEF`; the next career takes star bit 18 and must raise four save clamps |
| 2 | 509 model files remain | 0 model files (retired 2026-08-26); 52 production 3D files |
| 3 | Castle-room distribution is the "correct navigation baseline" | The owner retired `DL-INT-12` on 2026-09-24 for a four-floor venue that is not yet built |
| 4 | The Reef is a live area; "Lagoon to Reef is verified" | Reef retired 2026-09-09; its 3D world removed 2026-09-23 |
| 5 | Racer finishes with a circle gesture and `op_racer_lap_two` | `kart_race` steering on its own surface since 2026-09-05 |
| 6 | Route cards obscure Roshan's lower body; repair item 5 asks for a fix | Fixed 2026-08-29 (`81a93f0c`) |
| 7 | 64/63 probe rosters, 106 probes, Day One ungated | 82/81 rosters, 137 probes, Day One gated |
| 8 | "Exact Godot 4.7.1 import" in gates and reproductions | The baseline is Godot 4.7.2 |
| 9 | "Still-spatial Castle rooms" | Canvas 2D since 2026-08-22; `castle_rooms_25d.gd` has no 3D nodes |
| 10 | The Detective crown is "still visibly painted" | Painted out 2026-08-29; owner review pending — acting on the old text redoes finished work |

## 3. The finding register

[`data/stale_findings.json`](data/stale_findings.json) lists 24 findings and
the register preamble with the stale text, its line and the current truth. The
pattern: counts and line anchors copied into reproduction and evidence fields,
then never refreshed (`MA-2D-002`, `MA-CI-003`, `MA-CODE-001`, `MA-AUDIO-001`,
`MA-TYPE-006`); decisions that moved under a finding (`MA-OPERA-011`,
`MA-OPERA-012`); and repairs that never reached the register (`MA-OPERA-002`
crown, `MA-OPERA-012` cards). `MA-PERF-003`'s Galaxy claim was already wrong
when written. History is never rewritten: each correction is a dated history
entry.

## 4. The repository's audits

| Class | Documents | Size | Meaning |
|---|---:|---:|---|
| Keep as is | 76 | 3.66 MB | Binding or current, still the best home |
| Keep as evidence | 72 | 1.19 MB | Cited or hash-recorded by other files; move out of the active tree only where paths stay resolvable |
| Absorb, then archive | 85 | 1.20 MB | Durable content to extract into a reference first |
| Archive now | 119 | 1.95 MB | Superseded or historical with nothing durable left |
| Delete candidate | 2 | 3 KB | Tool output with no inbound links |

204 documents (about 3.1 MB) leave the active tree. By location: root 196
(16 keep, 3 evidence, 67 absorb, 110 archive), `audit/` 62, `design/` 47,
`docs/` 23, elsewhere 26. Domains with the most outdated material: art (33 to
archive), Opera careers (23), worlds (18 to archive, 13 to absorb), process
and governance, and castle (11 to absorb). The per-document classification is
in [REFERENCE_PLAN.md](REFERENCE_PLAN.md) section 3.

## 5. Contradictions between documents

Each needs either the newest owner decision applied (`DL-AUTH-01`), the code
treated as the truth for what ships, or an owner question.

| Domain | Contradiction | Suggested resolution |
|---|---|---|
| Opera | Can the imp win? Earlier documents say no; `DL-INT-14` (2026-09-30) says yes, with an instant rematch | Newest owner decision |
| Opera | Act length: 120–240 s (pacing doc), 70–150 s (balance probe), about 2:05 (two audits), no blanket duration (mechanics re-audit) | Owner question |
| Opera | Wrong-answer credit: a 0.05 crumb (input audit, code) versus zero for semantic choices (mechanics re-audit) | Owner question |
| Opera | Career counts: 13/53/27, 13/52, 14/57, 15/61/70 | Code; derive from the job catalogue |
| Opera | Costume atlas cells: 512 px (framing audit) versus 256 px (overhaul, code) | Code (256) |
| Opera | Spotlights stage-only versus drawn on tiled worlds | Code, or a bug for the owner |
| Opera and Day Two | Candy Maker's place: Kitchen and Chapter 2 step 3 versus reserved for a later section (2026-09-29) | Owner question (`OQ-ARBORIST-DAY2`) |
| Castle | Shell elevator exists (door language, Day One handoff) versus none | Code (none) |
| Castle | Door cue follows the painted arch (door language) versus drawn from the touch box | Code is the defect; the door handoff fixes it |
| Castle | Movie Lounge picture fades in versus hidden behind the screen | Repaired; update the castle audit |
| Castle | Sprite3D required (three documents) versus true 2D | `DL-MED-01` |
| Castle | 104 versus 96 interaction frames | Ledger JSON (96) |
| Castle and props | Colour meaning: red is plot for props, gold is plot and ruby is bonus for doors | Owner question (door handoff OD-1) |
| Castle | Back from Dream House rooms: to the gallery versus the Main Hall | Not verified; check code |
| Day One | Boss contract: three taps in 0.75 s versus dodge then tap the star | Newest (rebuild handoff) |
| Day One | Boss time ceilings: 90/120 s versus 150/240 s | Owner question |
| Day One | Seahorse "tap anywhere" a strength versus a defect | Newest (defect) |
| Day One | Attic arena 2048 native versus a 1254 px upscale | Provenance file (upscale) |
| Day One | Encounter true 2D: PASS versus still mixed 3D | Later audit (mixed) |
| Day Two | Party location: Main Hall versus Sky Lagoon lawn | Newest (lawn) |
| Day Two | Stuffie ballet payoff promised versus code goals that likely block it | Verify, then defect or owner question |
| Day One and castle | Idle re-prompts at 5/12(/25) s versus 8/20 s | Owner question (help ladder) |
| Art | New OmniLights allowed (style guide) versus forbidden (`CLAUDE.md`, `DL-PERF-03`) | Rule wins |
| Art | Sprite2D forbidden (living-card language) versus required (design 02) | `DL-MED-01` |
| Art | What 5/5 means: book source automatically 5 versus owner-only | Scoring governance (owner-only) |
| Art | Source-average palette gap an error versus diagnostic only | `DL-VIS-08` |
| Art | Never bake lighting versus flats that bake it | Owner question |
| Art | Parallax and colour grade: absent versus planned | Repair plan (newer) |
| Art | Claude may build reference packs versus Claude builds no images | `CLAUDE.md` (2026-09-30) |
| Engine | Godot 4.4 and 4.7.1 (both superseded) and 4.7.2 all named as baselines | 4.7.2 |
| Audio | Is `voice_yay` protected? | Path decides: it is outside `assets/audio/voices/` |
| Audio | Voice pipeline: Kokoro, Parler filler, consented talent later; enhancer advice versus `DL-SND-17` | Owner question (engine per job) |
| Audio | Music cues 42 versus 43 versus 44 | Catalogue (44) |
| Audio | Opera scope in the music audit (lobby, boss cues) versus deleted lobby and cut bosses | Owner decisions already made |
| Audio | Faron protected at runtime but absent from the protected list | Add to the list |
| Cinematic | Shot card V1 mandatory versus V2 required | Owner question |
| Cinematic | Grok output reference-only versus `DL-CIN-16` runtime story clips | Both: the exception is scoped to Day One |
| Cinematic | 24 fps versus 18 fps versus a 12 fps proposal | Owner question |
| Cinematic | The otter a failure versus kept | Newest (kept) |
| Cinematic | Circular shell arena versus stone attic | Newest (attic) |
| Cinematic | Baby Eagle basket versus two pins | Owner canon (two dust bunnies) |
| Performance | 3D debt 513/70, 509/65, 0/56, 0/52 | Live scanner |
| Performance | `main.gd` 8,465 / 8,734 / 10,907 / 9,817 lines | Live count |
| Performance | Device soak 20 versus 30 minutes | `DL-PERF-02` (30) |
| Performance | Texture compression saves 150–180 MB versus measured +24.9 MB | Measurement |
| Release | versionCode from run number versus commit count; publish on master only versus also dev | Workflow file |
| Process | "Defer new plot" versus the binding chapter guide | Chapter guide |

## 6. Rules that live only in documents marked for archive

These must be promoted into the rulebook (design 06), or explicitly retired by
the owner, before their source documents move. Confirmed absent from design
01, 02, 03, 06 and `AGENTS.md`:

| Rule | Source |
|---|---|
| 120–240 s act length with 3–4 distinct verbs | `OPERA_ACT_PACING_2026-07-25.md` (binding) |
| Direct manipulation of ingredients (the causal principle) | `OPERA_INGREDIENT_INTERACTION_DIRECTION_2026-08-03.md` |
| Medal rules (practice never earns a medal; quarter-milestone actions; bronze always) | `MEDALS.md`, `design/OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md` |
| The swipe exception | `COMBO_SYSTEM.md` |
| "A single detached leaf must not represent a whole plant" | Three Sky Lagoon audits |
| The 0–4 art rubric and its seven hard caps (design 02 restates two) | `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`, `ART_SCORING_GOVERNANCE_2026-07-18.md` |
| The 2026-06-25 freeware licensing decision | `ASSET_AUDIT.md` |
| Overdraw budgets (8 cards over 10% of the screen, 150% cumulative) | `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` |
| Stuck-help escalation (voice at 10 s; pointer at 20 s or after two wrong taps; never auto-solve) and 8–12 minute sittings | `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` |

## 7. Files that cannot be edited or moved freely

- **Hash-recorded by published packets:** `docs/handoffs/*/*.md`;
  `audit/minigame_art_quality_2026-09-05/*.md`;
  `audit/stage_pathfinding/*.md`; `design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md`;
  `audit/OVERNIGHT_RECUT_FRAME_AUDIT_2026-09-12.md`. Republishing a packet is a
  full handoff cycle.
- **Read by tools or entry points:** `AGENTS.md`, `CLAUDE.md`,
  `ASSET_LICENSES.md` (22 code files), `SECURITY.md`, `BACKUP.md`
  (`backup.yml`, `backup.sh`), the change-log rollback catalogue
  (`tools/plan_audit_rollback.py`), the Chapter 2 spine (document gate), and
  `FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json` (10 tools and probes).
- **Moved together with their links:** `design/10_CHAPTER_REFERENCE_LIBRARY.md`,
  `design/chapters/NORTHERN_ICE_WORLD.md`, the review-kit README and the
  master-audit task index link to documents marked for archive.

## 8. Operational documents that are wrong today

- `CLAUDE.md` and `AGENTS.md`: 513 model files, 70 production 3D files and an
  8,465-line `main.gd` (owner-gated edit).
- `CLAUDE.md` and `BACKUP.md`: verified weekly backups — every run since
  2026-07-27 has failed and no backup release exists.
- `docs/ANDROID_RELEASE.md`: says builds publish only from `master` and the
  version code is the run number; the workflow also publishes `android-dev`
  and uses the commit count.
- `assets/audio/voices/VOICE_MANIFEST.md`: Faron is protected at runtime but
  missing from the protected list; its speech-enhancer advice conflicts with
  `DL-SND-17`.
- `design/00_MASTER_INDEX.md`, `design/03_TECHNICAL_ARCHITECTURE.md`,
  `design/04_OPEN_WORK.md`: Godot 4.7.1, 509/65 debt counts, 8,734 lines,
  `0x1BDEF`/14 careers.

## 9. Method and limits

Four read-only sweeps (master audit element by element; repository inventory
and consolidation map; durable-knowledge extraction for Opera, castle and Day
One/Day Two; and for art, audio, cinematics, performance and process), with
the headline facts re-run by Claude. Items the sweeps could not check are
marked "not verified" in the data files. No runtime, device, child or owner
evidence is claimed.
