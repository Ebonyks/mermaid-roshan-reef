# Master design documents — index

**Development routing:** use the [master task index](../audit/MASTER_AUDIT_2026-08-09.md#development-task-index) and [mandatory development contract](AUDIT_DEVELOPMENT_CONTRACT.md) for every change.

**Planning entry (2026-09-05):** start with the
[audit front page](../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry),
[chapter guide](09_CHAPTER_DEVELOPMENT_GUIDE.md),
[brief template](templates/CHAPTER_BRIEF_V1.md), and
[reference library](10_CHAPTER_REFERENCE_LIBRARY.md).
[Northern/Ice World](chapters/NORTHERN_ICE_WORLD.md) is the named future
planning branch, including the restaurant/customer-order mechanic remix.
The sealed evidence below retains its named commits and is not today's build.

**Stage pathfinding (2026-09-06):** use the
[approach, door and boundary protocol](../audit/stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md),
[coverage ledger](../audit/stage_pathfinding/README.md), and
[live-stage review atlas](../audit/stage_pathfinding/reproductions/index.html).
[MA-PLAY-003](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-003)
tracks the remaining per-stage geometry and external acceptance gaps.

_Initial consolidation: 2026-08-02. Authority reconciliation: 2026-08-09.
Runtime/audit merge synchronization: 2026-08-13._

The sealed document-authority sources are
`5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, exact parent `18b6150c`, and
contiguous hardening source `7eb945957776ab3458a9de71c8be9937e2354720`,
exact parent `5ed0c754`. CHG-023 maintenance parent
`e6edf559af219edd4e5ce38cab0c5094483be5c6` passes integrated dev Probe Suite
run `31722047536`: probes 34m25s/63-of-63, 36 document tests, six/six stress,
316/316 inventory/ledger, 34 active/36 retained records, and music 3m33s/
42-of-42. Earlier branch run `31719143975` is corroborating e6 history.
Current audit source `51d0abc0d32855a8ba32932599fedd8f59b398b7`, exact
parent `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`, is the 19-path
Sky true-Canvas repair (+3,318/-3,517). Exact source bytes pass official Godot
`4.7.1.stable.official.a13da4feb` full local CI in 1,404.5 seconds/all 64.
Run-14 is 20/20 local 1280×720 Mobile/Speedy with manifest hash
`AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34` and
visual-probe hash `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`;
those hashes bind the manifest/PNGs and probe script, while `source_revision`
remains unknown. Governance-only integrated evidence head
`441adf35f7dbdeb67d36fbf1a2217b87d3040d47` preserves unchanged product source
`51d0abc0` and passes exact local full CI in 1,391.5 seconds/all 64. Topic Probe
run `31760207048` and dev Probe run `31762132976` both succeed at exact
`441adf35`: their required loops are 63/63 unique with zero hard failures,
document authority is 36 tests/six stress/316/316 with 34 active/36 retained,
and music is 42/42. Each nonblocking Sky subprocess nevertheless requests
Mobile, misses `VK_KHR_surface`, falls back through llvmpipe to
`gl_compatibility`, emits 20 PASS rows plus `20/20/20/20` summary, and then
exits 1 on the renderer `GLOBAL`/`RESULT`; PNGs upload, but no remote JSON or
Mobile-renderer PASS exists. Android run `31763879294` checks out exact
`441adf35`, uses version code 1414 on `dev`/`android-dev`, and publishes the
596,033,220-byte APK with SHA-256
`f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`.
Historical source `7391c53c` and run `31728755204` retain the prior failed
remote Sky `gl_compatibility` subprocess. The current Opera product/runtime commit
remains `09e5e35665fd8d1bd782693e10fc0198f756d2c8`; its exact local suite is
green in 1463.4 seconds/all 64, while predecessor probe-readiness head
`ff068db002202839f920a6f9fb78c942788a3034` is green in 1379.3 seconds/all 64.
Historical integrated product/dev audit baseline
`18b6150c01e1587100dca97c85ebad03f369825a` passes exact-head Probe Suite run
`31693492735`: the probes job completes in 29m41s with exactly 63 remote trusted
headings, and the Windows music gate ends 42/42. Android run `31695675866`
checks out that exact SHA and publishes the matching dev APK (596,041,412 bytes;
SHA-256 `fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`).
Latest integrated predecessor `e6edf559` also supplies the raw checkout/package
source for successful workflow-run Android `31724927769`, which publishes a
596,041,412-byte APK at SHA-256
`66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`.
Historical predecessor run `31661887863` remains green at
`e0677ae4`; later pre-fix run `31678156887` at `3fc151c8` remains red because
Ubuntu sampled the 0.25-second Opera reveal after four frames. The APK gate is
now commit-bound; the exact `441adf35` package preserves unchanged `51d0abc0`
product bytes. Device, child, owner, exact-voice, listening, strict-2D, and
accepted-visual gates remain open.

## Why this folder exists

The project accumulated hundreds of design documents, audits, work orders and
handoffs. The original consolidation counted 149 Markdown documents; the
historical `f3b0de07` merge tree contains **315 tracked Markdown paths**.
Both are dated inventory facts, not stable design constants. The documents are
individually useful and collectively difficult to navigate:
the same rule is restated in six places with three different dates, several
documents supersede each other in a chain four deep, and two of the standing
authority files (`CLAUDE.md`, `AGENTS.md`) disagreed with each other about the
art direction before the 2026-08-09 reconciliation.

This folder is the streamlined result. The first five masters remain concise
domain summaries. The comprehensive design language and dated master audit now
carry the cross-domain rule and evidence layers. Contiguous sources `5ed0c754`
and `7eb94595` establish and harden the **316 tracked Markdown path** inventory,
give each
path exactly one row in `05_DOC_LEDGER.md`, and provides full records for all 36
material findings, including retained terminal history, in
`audit/findings/ACTIVE_FINDINGS_2026-08-13.md`. Exact parent `e6edf559`
preserves the verified document controls, so `MA-DOC-002` and `MA-DOC-005` are
`VERIFIED_FIXED`; the stable records remain present after terminal transition.
Manual/non-emitting CHG-031 owns the current 19-path source, including
`scripts/probe_northern.gd`; the catalog is 31 IDs/79 unique references/four
emitters/25 planner tests/27 manual groups.

| # | Document | Answers |
|---|---|---|
| 01 | [GAME_DESIGN.md](01_GAME_DESIGN.md) | What the game is, who it is for, what the player does, how progress and reward work, what every mode is |
| 02 | [ART_DIRECTION.md](02_ART_DIRECTION.md) | What it looks like, what medium world art ships in, what the quality bar is, what may never be touched |
| 03 | [TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) | How it is built, which engines exist, how it is tested, how it ships |
| 04 | [OPEN_WORK.md](04_OPEN_WORK.md) | Current `MA-*` work navigation plus an explicit lifecycle crosswalk for the historical `OW-*` list |
| 05 | [DOC_LEDGER.md](05_DOC_LEDGER.md) | Exhaustive verified authority/status index: one row for each of 316 Git-declared Markdown paths |
| 06 | [COMPREHENSIVE_DESIGN_LANGUAGE.md](06_COMPREHENSIVE_DESIGN_LANGUAGE.md) | Stable `DL-*` rules, including the owner's 2026-08-09 true-2D decision and the complete audit contract |
| 08 | [TARGET_ARCHITECTURE.md](08_TARGET_ARCHITECTURE.md) | The Mode Platform remodel (owner-requested 2026-08-26): the growth law, GameMode/registry/director/services contracts, the structure ratchet, and migration plan M0–M6 |
| 09 | [CHAPTER_DEVELOPMENT_GUIDE.md](09_CHAPTER_DEVELOPMENT_GUIDE.md) | Delegation, strategic unused-asset selection, mechanic remixing, production workflow, and evidence boundaries |
| 10 | [CHAPTER_REFERENCE_LIBRARY.md](10_CHAPTER_REFERENCE_LIBRARY.md) | Current continuity sources, seed patterns, asset discovery, and implementation availability |
| chapter template | [CHAPTER_BRIEF_V1.md](templates/CHAPTER_BRIEF_V1.md) | Commission, causal play, continuity, saves, asset shortlist, dependencies, acceptance, and learning |
| Northern planning | [NORTHERN_ICE_WORLD.md](chapters/NORTHERN_ICE_WORLD.md) | Future Ice World restaurant/customer-order opportunity and source/implementation dependencies |
| audit | [MASTER_AUDIT_2026-08-09.md](../audit/MASTER_AUDIT_2026-08-09.md) | Current audit-cycle state, synchronized evidence, lifecycle triage, and satisfaction gate |
| typography audit | [FONT_TYPOGRAPHY_AUDIT_2026-08-30.md](../audit/FONT_TYPOGRAPHY_AUDIT_2026-08-30.md) | V1 font, glyph, size, layout, and `Label3D` census; critique; and bounded TYPE-A–G implementation program |
| findings | [ACTIVE_FINDINGS_2026-08-13.md](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md) | Full canonical records for every material `MA-*` item, including retained terminal history |
| changes | [MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md](../audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md) | Stable `CHG-*` change groups, benefits/risks, dependencies, evidence, and guarded per-change rollback plans |

`06_COMPREHENSIVE_DESIGN_LANGUAGE.md` is tracked, verified, and
`CANONICAL_CURRENT` under the precedence below. Direct owner decisions and
binding operational/security rules remain higher authority.

## Precedence

When two documents disagree, resolve in this order:

1. **Binding `SECURITY.md`, protected-asset/save rules, credential and
   filesystem safeguards, and release requirements.** A content or design
   decision never weakens these boundaries.
2. **A direct, dated owner product decision within those boundaries.**
3. **Exact engine requirements and the remaining current operational rules in
   `AGENTS.md`.** `CLAUDE.md` mirrors the session contract.
4. **`06_COMPREHENSIVE_DESIGN_LANGUAGE.md`**, within its declared authority
   state, then the applicable 01–05 domain master.
5. **A domain document whose precise retained scope 05_DOC_LEDGER.md marks
   current** — living specs such as `MEDALS.md`, `STUFFIE_COMPANIONS.md`, and
   `ART_STYLE_GUIDE.md`, plus the retained portions of mixed documents. A
   mixed document cannot redefine a rule in its superseded scope.
6. Everything else is a **historical record**. Read it to learn why a
   decision was made; never take an instruction from it without checking the
   ledger first.

The latest scoped Opera and audio authorities are explicit examples of rule
5: `BALLERINA_PARTY_REBUILD_2026-08-09.md` controls Ballerina,
`design/BOXING_GAME_PROJECT_2026-08-09.md` controls Boxer mechanics, and
`MUSIC_AUDIT_2026-08-09.md` controls music. Their retained scopes and the
precise supersessions of the earlier Opera quality documents are recorded in
the ledger; provenance prompt/review files cannot overrule them.

`CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` is a mixed document, but three scopes
are direct owner authority rather than deferred chapter brainstorming. Section
10 / commit `7426c187` distributes the thirteen careers through Castle rooms
and makes Opera Hall one venue. Section 16 / commit `3d1236fe` cuts Curtain
Dragon, Shadow Phantom, and Midnight Maestro and retires save slots 4/9/14 in
place; section 17 / commit `ef2fd982` clarifies that any future boss fights
belong to Ember-aligned henchmen rather than restoring those Opera bosses. Later
sections supersede the earlier
section-10 mention of an Opera boss/finale card; they do not supersede room
distribution.

## What was NOT done, deliberately

- **No document was moved, renamed, or deleted during the original
  consolidation.** Its 2026-08-02 inventory found 149 files, 236 plain-text
  cross-references and 14 tools/probes reading document paths. Those are dated
  evidence, not current repository counts.
- **Historical source documents remain in place.** A `SUPERSEDED`,
  `DISMISSED_NOT_IN_PROJECT`, or `HISTORICAL_EVIDENCE` label preserves why a
  direction existed; it never authorizes executing that old direction.

## Current medium decision

**Owner decision 2026-08-09:** the final game is true Canvas/Node2D 2D
game-wide. `Node3D`, `Sprite3D`, `Camera3D`, models, spatial shaders, 3D
physics, Blender/Meshy work, and real-3D character or world directions are
only exact shrinking migration debt or explicitly labelled history. Mermaid
Roshan has no accepted GLB, rig, skeleton, or model fallback. Retired 3D
resources live only on the deprecated-resources archive branch; the active
project is not allowed to use that branch as a fallback or merge source.

At merge `f3b0de078898a8b4faddb2c738c4403180eff928` (parents `ea6185fd`
and `5f58ef0a`), GAME2D recorded the historical 68-production/77-probe
checkpoint. The current audit remains **`UNSATISFIED`** while Sky shrinks the
exact inventory to 509 model files, all 509 active/export, 157 tracked
sidecars, 352 active-untracked generated sidecars, 65 production 3D files, 70
probe 3D files, one scene, and one configuration. Regression mode is exact
`NO_REGRESSION` and all 14 falsification controls pass; neither result is strict
completion. The `f3b0de07` tree had 195 GDScript files under `scripts/`, 106
  `scripts/probe_*.gd` files, and an 8,519-line `scripts/main.gd`. Historical
  `09e5e356` retained 195/106 script/probe files and had an 8,647-line
  `scripts/main.gd`; current source `51d0abc0` has 8,734 lines.

Exact Godot 4.7.1-stable local `scripts/ci.sh` exits 0 at `f3b0de07` after
1437.1 seconds with all 64 then-current trusted probes. Predecessor product/audit
commit `e2c25878` exits 0 in 1428.6 seconds under official build `a13da4feb`.
Runtime commit `09e5e356` exits 0 in 1463.4 seconds, with all 64
trusted local probes, 74 GAME2D unit tests, all 14 falsification controls, 93
visual-contract unit tests, parser/lint/analyzer/import/static gates, and its
focused runtime matrix green. Castle frame-review candidate
`1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9`
passes its machine/review ledger for 13 assets/104 frames; it is not owner
acceptance. Probe-only `ff068db` preserves those runtime bytes and completes a
newer exact full-local run in 1379.3 seconds with all 64 probes green. These are
commit-pinned local results; exact-head remote is recorded separately below.
Visual advisory remains
`UNSATISFIED` and globally unchanged: 16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN,
86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE. Historical
remote run `31457593351` at `dacef140` remains evidence for that older SHA.
Run `31648427712` at `bbc817ef` proves the pinned Windows music job 42/42 but
fails only the Ubuntu static Opera-art gate on a CRLF-vs-LF raw hash for the
declared text input `GENERATION.json`; import, analyzer, and probes did not run.
Repair checkpoint `af4189a9` LF-canonicalizes only that declared text hash, keeps
binary hashes exact, and passes 10 focused tests plus Windows and LF-clean
Opera checks at 42/42. Replacement run `31649113587` succeeds at exact
`af4189a9`: the 35m27s Ubuntu job passes static/import/full analyzer/all 63
remote probes/boot/advisory balance/Opera manifest; all five capture/upload
pairs completed at the workflow level and uploaded diagnostic artifacts. The
3m55s Windows job passes
music 42/42. No full local suite at
`af4189a9`, and no APK, device, child, owner, listening, strict-2D, or
authoritative visual-evidence result, is claimed; the captures are diagnostic.

Historical exact-head run `31661887863` succeeds at predecessor SHA
`e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0`. The Ubuntu probes job succeeds in
33m8s after checkout/checksum, exact Godot, static gates, import, the full
analyzer, all 63 trusted probes, boot, Dust/Opera advisories, and the Opera
manifest. All five capture/upload pairs completed at the workflow level and
uploaded diagnostic artifacts. Remote GAME2D is exact
509/66/74 `NO_REGRESSION`/`UNSATISFIED`. The Windows music job succeeds in
6m52s and ends `MUSIC|check 42/42|picture_xmas`. Those uploaded artifacts remain
diagnostic and grant no authoritative visual, device, child, or owner
acceptance. Run `31678156887` at pre-fix head `3fc151c8` is retained as red: its
only probe failures are Detective/Nursery stable-Canvas checks sampled during
the 0.25-second reveal after four frames; all other executed gates/probes and
Windows pass. `ff068db` replaces that guess with bounded fail-closed semantic
readiness. Predecessor integrated dev/audit head `18b6150c` passes Probe Suite run
`31693492735`: the probes job completes in 29m41s with exactly 63 remote trusted
headings and the Windows music gate ends 42/42. Static/import/analyzer/probe/
boot/advisory/manifest gates are green. All five capture/upload pairs completed
at the workflow level and uploaded diagnostic artifacts; they are not capture
gates or visual passes. Raw Sky Lagoon `LAGOONSHOT` output itself has 21 `OK`,
44 `FAIL`, and `DONE` (66 diagnostic lines), with 20 PNGs, so the Sky Lagoon
diagnostic internally fails and cannot support visual acceptance. The run is
also not warning-clean. Android run `31695675866` succeeds from exact
`18b6150c` and publishes the matching dev APK (596,041,412 bytes; SHA-256
`fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`).
Later parent `e6edf559` passes integrated dev Probe Suite run `31722047536`
with probes 34m25s/63-of-63, document controls green, and music 3m33s/42-of-42;
earlier branch run `31719143975` is corroborating e6 history, and their inherited Sky
21-OK/44-FAIL/DONE result is predecessor history. Historical source `7391c53c`
and exact-source run `31728755204` preserve its failed remote
`gl_compatibility` subprocess. Current source `51d0abc0` passes exact official-
Godot full local CI in 1,404.5 seconds/all 64 and run-14 locally produces 20/20
ordered 1280×720 Mobile/Speedy captures, bound by manifest hash
`AEAC7C72…DE34` and visual-probe hash `B9EAF5E0…9C6C`.
Workflow-run Android `31724927769` uses raw checkout/package source exact e6
and publishes the integrated-predecessor APK (596,041,412 bytes;
SHA-256 `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`).
Source `51d0abc0` replaces the mural/spatial promenade with an owned
CanvasLayer/Node2D/Sprite2D/Camera2D stage and repairs the bounded readability,
focus, grounding, contact, touch, and route-lifecycle defects. `MA-VIS-002`
becomes `FIXED_PENDING_VERIFICATION`; `MA-VIS-006` remains open. No accepted-
visual result is claimed. Exact governance head `441adf35` has successful
topic/dev remote suites and a matching dev APK, but both Sky subprocesses still
fail renderer identity after 20 PASS rows and provide PNGs only, not remote
JSON/Mobile PASS. Authoritative visual, exact voice, human listening, device,
child, owner, and strict-zero 2D evidence remain open.

Current Opera content is 14 careers, 57 phases, and 28 modes with newer
diegetic rooms, the integrated Candymaker, current Ballerina/Boxer, and the
Canvas Racer plus cooperative Geologist. Commit `09e5e356` distributed the
original thirteen careers to exact thematic
Castle room, selects Movie Lounge as Racer's sole home, deletes the all-career
lobby, blocks hidden/off-room routes, and returns each activity to its launching
room. The 2026-08-30 owner-directed Geologist addition appends at bit 16 and
launches from the Library. Save identity preserves every historical lower-
sixteen-bit assignment inside the appended 17-slot namespace: slots 4/9/14 are
inert tombstones, raw legacy bits survive, the live completion mask is
`0x1BDEF`, and effective progress is 0–14. The exact
focused matrix plus full-local runtime `09e5e356` and probe-head `ff068db` gates
are green, so `MA-OPERA-010`, `MA-OPERA-011`, and `MA-OPERA-012` are
`FIXED_PENDING_VERIFICATION`, not closed.
The prior twenty-two 1280×720 Mobile captures (nine room routes plus thirteen careers)
were rendered and visually inspected as diagnostic/review evidence; they are
not target-device, child, owner, or authoritative visual acceptance. The route
cards obscure Roshan's lower body/tail in all nine room captures, a residual P2
composition defect. Painter purpose and Arborist remain
uncommitted candidates; Boxer V2 is docs-only on a separate branch and does not
supersede the integrated Boxer.

## Maintaining this

A new audit or work order is still written wherever it belongs. What changed
is the closing step: **when a document lands, add its ledger row, and if it
changes a standing rule, edit the master that owns that rule in the same
commit.** A master that lags its sources is worse than no master.
