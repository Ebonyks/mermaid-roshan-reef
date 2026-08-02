# Master design documents — index

_Consolidation date: 2026-08-02. Source: all 149 markdown documents in the
repository (134 at root, 11 under `docs/`, 4 under `audit/`)._

## Why this folder exists

The project accumulated 149 design documents, audits, work orders and
handoffs in ten weeks. They are individually good and collectively unusable:
the same rule is restated in six places with three different dates, several
documents supersede each other in a chain four deep, and two of the standing
authority files (`CLAUDE.md`, `AGENTS.md`) disagree with each other about the
current art direction.

This folder is the streamlined result. **Five master documents carry the
current design; everything else is history.**

| # | Document | Answers |
|---|---|---|
| 01 | [GAME_DESIGN.md](01_GAME_DESIGN.md) | What the game is, who it is for, what the player does, how progress and reward work, what every mode is |
| 02 | [ART_DIRECTION.md](02_ART_DIRECTION.md) | What it looks like, what medium world art ships in, what the quality bar is, what may never be touched |
| 03 | [TECHNICAL_ARCHITECTURE.md](03_TECHNICAL_ARCHITECTURE.md) | How it is built, which engines exist, how it is tested, how it ships |
| 04 | [OPEN_WORK.md](04_OPEN_WORK.md) | Every unresolved finding from every audit, deduped and re-verified against today's code |
| 05 | [DOC_LEDGER.md](05_DOC_LEDGER.md) | Status of all 149 historical documents: authoritative, supporting, superseded, or historical record |

## Precedence

When two documents disagree, resolve in this order:

1. **A direct owner decision**, wherever it is recorded (they are all
   collected in 01–03 with their dates).
2. **`CLAUDE.md` / `AGENTS.md` hard rules** — the per-session contract every
   agent reads first. These stay the operational entry point; the masters
   never contradict them.
3. **These five master documents.**
4. **A historical document that 05_DOC_LEDGER.md marks AUTHORITATIVE** —
   living specs (`MEDALS.md`, `STUFFIE_COMPANIONS.md`,
   `MINIGAME_ENGINES.md`, `SECURITY.md`, `BACKUP.md`,
   `ASSET_LICENSES.md`, `ART_STYLE_GUIDE.md`) that are too detailed to fold
   in and are still true.
5. Everything else is a **historical record**. Read it to learn why a
   decision was made; never take an instruction from it without checking the
   ledger first.

## What was NOT done, deliberately

- **No document was moved, renamed, or deleted.** The 149 files cross-
  reference each other 236 times in plain backtick text (there is not a
  single markdown link among them), and 14 tools and probes read doc paths
  directly. Moving files would have broken references in exchange for
  nothing the ledger does not already give.
- **`CLAUDE.md` and `AGENTS.md` were not edited.** They are flagged
  explicit-task-only under the security rules. The contradiction between
  them is recorded as [OW-1](04_OPEN_WORK.md#ow-1) with the exact fix.

## Maintaining this

A new audit or work order is still written wherever it belongs. What changed
is the closing step: **when a document lands, add its ledger row, and if it
changes a standing rule, edit the master that owns that rule in the same
commit.** A master that lags its sources is worse than no master.
