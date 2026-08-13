# Master design documents — index

_Initial consolidation: 2026-08-02. Authority reconciliation: 2026-08-09.
Runtime/audit merge synchronization: 2026-08-13._

The current sealed document-authority source and latest completed full-local
checkpoint is `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, with exact parent
`18b6150c01e1587100dca97c85ebad03f369825a`. Exact official Godot
`4.7.1.stable.official.a13da4feb` `scripts/ci.sh` is green at the sealed source
in 1,359.8 seconds with all 64 trusted probes. No exact-source-head remote or
APK result is claimed for `5ed0c754`. The current Opera product/runtime commit
remains `09e5e35665fd8d1bd782693e10fc0198f756d2c8`; its exact local suite is
green in 1463.4 seconds/all 64, while predecessor probe-readiness head
`ff068db002202839f920a6f9fb78c942788a3034` is green in 1379.3 seconds/all 64.
Predecessor integrated dev/audit authority head
`18b6150c01e1587100dca97c85ebad03f369825a` passes exact-head Probe Suite run
`31693492735`: the probes job completes in 29m41s with exactly 63 remote trusted
headings, and the Windows music gate ends 42/42. Android run `31695675866`
checks out that exact SHA and publishes the matching dev APK (596,041,412 bytes;
SHA-256 `fb4979473441d416f7b07914b1396f5f883935d4c08bf077baed3dfb91b78941`).
Historical predecessor run `31661887863` remains green at
`e0677ae4`; later pre-fix run `31678156887` at `3fc151c8` remains red because
Ubuntu sampled the 0.25-second Opera reveal after four frames. The APK gate is
now commit-bound; device, child, owner, exact-voice, listening, strict-2D, and
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
carry the cross-domain rule and evidence layers. Sealed source `5ed0c754`
inventories **316 tracked Markdown paths**, gives each
path exactly one row in `05_DOC_LEDGER.md`, and provides full records for all 36
material active findings in
`audit/findings/ACTIVE_FINDINGS_2026-08-13.md`. Its fail-closed validator and CI
wiring are committed and locally green. `MA-DOC-002` and `MA-DOC-005` remain
`FIXED_PENDING_VERIFICATION` until exact-source-head remote gates pass.

| # | Document | Answers |
|---|---|---|
| 01 | [GAME_DESIGN.md](01_GAME_DESIGN.md) | What the game is, who it is for, what the player does, how progress and reward work, what every mode is |
| 02 | [ART_DIRECTION.md](02_ART_DIRECTION.md) | What it looks like, what medium world art ships in, what the quality bar is, what may never be touched |
| 03 | [TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) | How it is built, which engines exist, how it is tested, how it ships |
| 04 | [OPEN_WORK.md](04_OPEN_WORK.md) | Current `MA-*` work navigation plus an explicit lifecycle crosswalk for the historical `OW-*` list |
| 05 | [DOC_LEDGER.md](05_DOC_LEDGER.md) | Exhaustive sealed-source authority/status index: one row for each of 316 tracked Markdown paths; exact-source-head remote verification remains pending |
| 06 | [COMPREHENSIVE_DESIGN_LANGUAGE.md](06_COMPREHENSIVE_DESIGN_LANGUAGE.md) | Stable `DL-*` rules, including the owner's 2026-08-09 true-2D decision and the complete audit contract |
| audit | [MASTER_AUDIT_2026-08-09.md](../audit/MASTER_AUDIT_2026-08-09.md) | Current audit-cycle state, synchronized evidence, lifecycle triage, and satisfaction gate |
| findings | [ACTIVE_FINDINGS_2026-08-13.md](../audit/findings/ACTIVE_FINDINGS_2026-08-13.md) | Full canonical records for all 36 material active `MA-*` items; pending exact-source-head remote verification |
| changes | [MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md](../audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md) | Stable `CHG-*` change groups, benefits/risks, dependencies, evidence, and guarded per-change rollback plans |

`06_COMPREHENSIVE_DESIGN_LANGUAGE.md` is tracked and recognized here, but its
own status remains `PROPOSED_CANONICAL` until the documentation gate described
by the master audit is complete.

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
checkpoint. The current Opera repair remains **`UNSATISFIED`** but shrinks the
exact inventory to 509 model files, all 509 active/export, 157 tracked
sidecars, 352 active-untracked generated sidecars, 66 production 3D files, 74
probe 3D files, one scene, and one configuration. Regression mode is exact
`NO_REGRESSION` and all 14 falsification controls pass; neither result is strict
completion. The `f3b0de07` tree had 195 GDScript files under `scripts/`, 106
  `scripts/probe_*.gd` files, and an 8,519-line `scripts/main.gd`. Current
  `09e5e356` retains 195/106 script/probe files and has an 8,647-line
  `scripts/main.gd`.

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
readiness. Current integrated dev/audit head `18b6150c` passes Probe Suite run
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
Authoritative visual, exact voice, human listening, device, child, owner, and
strict-zero 2D evidence remain open.

Current Opera content is 13 careers, 53 phases, and 27 modes with newer
diegetic rooms, the integrated Candymaker, current Ballerina/Boxer, and the
Canvas Racer. Commit `09e5e356` distributes every career to one exact thematic
Castle room, selects Movie Lounge as Racer's sole home, deletes the all-career
lobby, blocks hidden/off-room routes, and returns each activity to its launching
room. Save identity remains a stable
16-slot namespace: slots 4/9/14 are inert tombstones, raw legacy bits survive,
the live completion mask is `0xBDEF`, and effective progress is 0–13. The exact
focused matrix plus full-local runtime `09e5e356` and probe-head `ff068db` gates
are green, so `MA-OPERA-010`, `MA-OPERA-011`, and `MA-OPERA-012` are
`FIXED_PENDING_VERIFICATION`, not closed.
Twenty-two 1280×720 Mobile captures (nine room routes plus thirteen careers)
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
