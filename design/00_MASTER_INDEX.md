# Master design documents — index

_Initial consolidation: 2026-08-02. Authority reconciliation: 2026-08-09._

## Why this folder exists

The project accumulated hundreds of design documents, audits, work orders and
handoffs. The original consolidation counted 149 Markdown documents, but that
count is historical and the repository has grown since then. They are
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

At the synchronized committed snapshot recorded by the 2026-08-09 master
audit, the game remains **`UNSATISFIED`** at 513 model files and 70 production
3D files. A no-regression result is not 2D completion.

## Maintaining this

A new audit or work order is still written wherever it belongs. What changed
is the closing step: **when a document lands, add its ledger row, and if it
changes a standing rule, edit the master that owns that rule in the same
commit.** A master that lags its sources is worse than no master.
