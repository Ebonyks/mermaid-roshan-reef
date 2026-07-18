# Branching Workflow Change — Staged Integration (2026-07-18)

Briefing for every agent working on this repo (Codex, Claude sessions,
humans). This supersedes the 2026-07-13 "merge finished work into master"
rule in earlier revisions of AGENTS.md / CLAUDE.md. If your instructions
conflict with this document, this document wins.

## What changed, in one line

Finished work now merges into **`dev`**, not `master`; `master` only moves
by a gated fast-forward promotion from `dev`.

## Why

Until now every probed-green work branch merged straight into `master`,
and `master` is also the live release channel — the branch whose APK the
owner's phone bookmark installs. That meant zero buffer between "an agent
finished a task" and "the 4-year-old is playing it." A staged integration
branch keeps master clean: work accumulates and soaks on `dev` (playable
on its own APK channel), and promotion to master is a deliberate, gated
step.

## The three tiers

| Branch | Role | Who writes to it |
|---|---|---|
| `codex/<topic>`, `claude/<topic>` | per-task work branches | you, freely |
| `dev` | integration; where finished work lands | agents, ONLY by merging a probes-green work branch |
| `master` | release; phone's stable APK channel | NOBODY directly — only the "Promote dev to master" workflow |

## Rules for a Codex session

1. Branch `codex/<topic>` off **`origin/dev`** (not master — master may
   lag dev until the next promotion).
2. Work as usual. Run the local gates before every push
   (`python -m gdtoolkit.parser`, `python tools/lint_inference.py`, or
   full `scripts/ci.sh` when a Godot binary is available).
3. Push the work branch; `.github/workflows/probes.yml` runs the full
   gate (import, per-file `--check-only` compile, all trusted probes) on
   every push.
4. When the task is COMPLETE and probes are green on CI for your branch:
   fetch and reconcile `origin/dev` (merge, resolve, re-run gates if the
   merge wasn't clean), then merge your branch into `dev` and push dev.
5. **Never** commit to, merge into, rebase, or push `master`. There are
   no exceptions for "finished", "trivial", "docs-only", or "the owner
   asked for it fast" — promotion handles all of that.
6. Local `master` and `dev` are pull-only (`git pull --ff-only`); if
   fast-forward fails, stop and rescue your work to `rescue/<machine>-<date>`
   per AGENTS.md — do not force anything.

## How master moves: the Promote workflow

`.github/workflows/promote.yml` ("Promote dev to master", manual
`workflow_dispatch` from the Actions tab):

1. Checks out `dev` HEAD.
2. Queries the probe-suite run for that **exact commit**; refuses to
   promote unless its conclusion is `success`.
3. Verifies `master` is an ancestor of `dev` (if not: merge master into
   dev first, let probes go green, re-run).
4. Fast-forward pushes `master` to dev's HEAD.

Fast-forward-only means master's history is always byte-identical to
history that already passed the gate — no promotion-time merge commits,
nothing on master that CI never saw. Promotion is normally triggered by
the owner; an agent may trigger it only when the owner explicitly asks.

## APK channels

`.github/workflows/android.yml` builds after each green probes run:

- `master` → release tag `android-test` — the phone's stable bookmark
  (URL unchanged from before this change).
- `dev` → release tag `android-dev` — pre-promotion play-testing:
  https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/android-dev/roshan-reef.apk

The old `claude/graphics-upgrade-fork` → `android-graphics` channel is
retired; that branch's work was absorbed into this line long ago.

Version codes derive from the commit count, so they are monotonic and
identical for the same commit on both channels. One practical caveat:
`dev` is always ahead of (or equal to) `master`, so after installing a
dev build on the phone, installing from the stable bookmark again will be
refused as a downgrade until dev has been promoted. Keep the family
phone on the stable bookmark day-to-day.

## Things that did NOT change

- The probe gate itself: red CI = do not merge, revert-don't-patch-probes,
  all AGENTS.md refactor and asset rules.
- Work-branch naming, rescue-branch discipline, pull-only local masters.
- The stable phone bookmark URL.
- `probes.yml` still runs on every push of every branch.

## Bootstrap state (for the curious)

The architecture landed via one final direct merge to master (a
`workflow_dispatch` workflow must exist on the default branch before it
can be run), after which `dev` was created from master. From that point
the direct-merge path is closed.
