# Master design documents — index

_Initial consolidation: 2026-08-02. Authority reconciliation: 2026-08-09.
Runtime/audit merge synchronization: 2026-08-12._

The latest CI-repair checkpoint is
`af4189a99cfd5a32d0df0f75185f6912d3889399`; the last committed complete
local-suite checkpoint remains merge `f3b0de07`. The current Opera retirement/lifecycle
repair is based on audit checkpoint `41087f66`. Its exact local working-slice
`scripts/ci.sh` is green under Godot
`4.7.1.stable.official.a13da4feb`; exact-head remote, APK, device, child, and
owner gates are not yet complete.

## Why this folder exists

The project accumulated hundreds of design documents, audits, work orders and
handoffs. The original consolidation counted 149 Markdown documents; the
current `f3b0de07` merge tree contains **315 tracked Markdown paths**.
Both are dated inventory facts, not stable design constants. The documents are
individually useful and collectively difficult to navigate:
the same rule is restated in six places with three different dates, several
documents supersede each other in a chain four deep, and two of the standing
authority files (`CLAUDE.md`, `AGENTS.md`) disagreed with each other about the
art direction before the 2026-08-09 reconciliation.

This folder is the streamlined result. The first five masters remain concise
domain summaries. The comprehensive design language and dated master audit now
carry the cross-domain rule and evidence layers; the ledger is still a partial
index, not proof that every tracked Markdown file has been classified.

| # | Document | Answers |
|---|---|---|
| 01 | [GAME_DESIGN.md](01_GAME_DESIGN.md) | What the game is, who it is for, what the player does, how progress and reward work, what every mode is |
| 02 | [ART_DIRECTION.md](02_ART_DIRECTION.md) | What it looks like, what medium world art ships in, what the quality bar is, what may never be touched |
| 03 | [TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) | How it is built, which engines exist, how it is tested, how it ships |
| 04 | [OPEN_WORK.md](04_OPEN_WORK.md) | Current `MA-*` work navigation plus an explicit lifecycle crosswalk for the historical `OW-*` list |
| 05 | [DOC_LEDGER.md](05_DOC_LEDGER.md) | Partial authority/status index for the original document set plus targeted later additions; not yet exhaustive |
| 06 | [COMPREHENSIVE_DESIGN_LANGUAGE.md](06_COMPREHENSIVE_DESIGN_LANGUAGE.md) | Stable `DL-*` rules, including the owner's 2026-08-09 true-2D decision and the complete audit contract |
| audit | [MASTER_AUDIT_2026-08-09.md](../audit/MASTER_AUDIT_2026-08-09.md) | Current audit-cycle state, synchronized evidence, lifecycle triage, and satisfaction gate |
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
`scripts/probe_*.gd` files, and an 8,519-line `scripts/main.gd`.

Exact Godot 4.7.1-stable local `scripts/ci.sh` exits 0 at `f3b0de07` after
1437.1 seconds with all 64 then-current trusted probes. The current Opera slice
also exits 0 in 1428.6 seconds under official build `a13da4feb`, with all 64
trusted local probes, 74 GAME2D unit tests, all 14 falsification controls, 93
visual-contract unit tests, parser/lint/analyzer/import/static gates, and its
focused runtime matrix green. Castle frame-review candidate
`1754c880e4ef3df87daed47e1a8ec1ed36e114956ae86dbc50a74e40bba392d9`
passes its machine/review ledger for 13 assets/104 frames; it is not owner
acceptance. This is a local working-slice result; exact-head remote is pending.
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
remote probes/boot/advisory balance/Opera manifest and five diagnostic capture
pairs; the 3m55s Windows job passes music 42/42. No full local suite at
`af4189a9`, and no APK, device, child, owner, listening, strict-2D, or
authoritative visual-evidence result, is claimed; the captures are diagnostic.

Current Opera content is 13 careers, 53 phases, and 27 modes with newer
diegetic rooms, the integrated Candymaker, current Ballerina/Boxer, and the
Canvas Racer. The current repair removes the ordinary-headless legacy lobby,
external-kart, and Opera-boss runtime paths. Save identity remains a stable
16-slot namespace: slots 4/9/14 are inert tombstones, raw legacy bits survive,
the live completion mask is `0xBDEF`, and effective progress is 0–13. The exact
focused matrix and full local working-slice gate are green, so `MA-OPERA-010`
and `MA-OPERA-011` are
`FIXED_PENDING_VERIFICATION`, not closed. Seventeen 1280×720 Mobile captures
were rendered and visually inspected as diagnostic/review evidence; they are
not target-device, child, owner, or authoritative visual acceptance. Navigation
is still not final authority: the three-page picker remains transitional and
P1 `CONFIRMED_OPEN` under `MA-OPERA-012`. Painter purpose and Arborist remain
uncommitted candidates; Boxer V2 is docs-only on a separate branch and does not
supersede the integrated Boxer.

## Maintaining this

A new audit or work order is still written wherever it belongs. What changed
is the closing step: **when a document lands, add its ledger row, and if it
changes a standing rule, edit the master that owns that rule in the same
commit.** A master that lags its sources is worse than no master.
