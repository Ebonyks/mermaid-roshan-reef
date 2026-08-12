# Master design documents — index

_Initial consolidation: 2026-08-02. Authority reconciliation: 2026-08-09.
Runtime/audit merge synchronization: 2026-08-12._

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
and `5f58ef0a`), the game remains **`UNSATISFIED`**. GAME2D reports 509 model
files, all 509 active/export, 157 tracked sidecars, 352 active-untracked
generated sidecars, 68 production 3D files, 77 probe 3D files, one scene, and
one configuration: exact `NO_REGRESSION`, not strict completion. The tree has
195 GDScript files under `scripts/`, 106 `scripts/probe_*.gd` files, and an
8,519-line `scripts/main.gd`.

Exact Godot 4.7.1-stable local `scripts/ci.sh` exits 0 at `f3b0de07` after
1437.1 seconds with all 64 trusted probes, 74 GAME2D unit tests plus 14
falsification controls, and current static/provenance gates green. Visual
advisory remains `UNSATISFIED`: 16 FAIL, 17 REVIEW_OPEN, two
MANUAL_OPEN, 86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE. Historical
remote run `31457593351` at `dacef140` remains evidence for that older SHA; no
exact-`f3b0de07` remote, APK, device, child, owner, listening, strict-2D, or
authoritative visual-evidence result is claimed.

Current Opera is 13 careers, 53 phases, and 27 modes with newer diegetic rooms,
the integrated Candymaker, current Ballerina/Boxer, and the Canvas Racer on the
display/forced-2D path. Ordinary headless source still retains a legacy lobby
and external-kart route, open as `MA-OPERA-010`/`MA-2D-002`. Painter purpose
and Arborist remain uncommitted candidates; Boxer V2 is docs-only on a separate
branch and does not supersede the integrated Boxer.

## Maintaining this

A new audit or work order is still written wherever it belongs. What changed
is the closing step: **when a document lands, add its ledger row, and if it
changes a standing rule, edit the master that owns that rule in the same
commit.** A master that lags its sources is worse than no master.
