# Agent workflow rules — Mermaid Roshan Reef of Light

Multiple agents (Claude sessions, Codex, humans) work on this repo
concurrently, on several machines. These rules exist because divergent local
masters and stale side-copies have repeatedly forced manual merge rescues.

## Branching
- **Local `master` is pull-only.** Never commit to it. Update it only with
  `git pull --ff-only`. If that fails, STOP — do not merge or rebase master;
  rescue your work (below) and re-clone mentally from `origin/master`.
- Start every task from a fresh fetch: branch `codex/<topic>` or
  `claude/<topic>` off `origin/master`.
- If the working tree is dirty when your session starts, first push it to
  `rescue/<machine>-<date>` untouched, then start clean.
- Push your own branch and stop. Do not push to `master` or to another
  agent's branch. Central merging favors the most recent development time.
- Never work in other local copies of this project (`reef2`,
  `roshan-graphics-fork`, `roshan-new`, backups) — only a clone of this repo.

## Gates (run before every push)
- `python -m gdtoolkit.parser <changed .gd files>`
- `python tools/lint_inference.py <changed .gd files>`
- CI also runs Godot's full analyzer (`--check-only`) on every script:
  `var x := <expr>` fails when the receiver is untyped — declare explicit
  types (`var x: Node3D = ...`), and keep `var m: ReefMain` back-references
  typed in extracted classes.

## Structure (post-refactor map)
- `scripts/main.gd` — world + orchestration (`class_name ReefMain`)
- `scripts/games/*.gd` — one class per minigame (build/tick/end via `m.*`)
- `scripts/arena/*.gd` — Sky Lagoon, Castle Hall builders
- `scripts/physics.gd` — ReefPhysics (analytic). Jolt is ONLY for the
  dev-mode Physics Lab; mass gameplay/foliage must never become bodies.
- Target device: Lenovo Tab M11 (Helio G88 / Mali-G52) — Speedy tier is the
  mobile default; treat 30 fps and transparent-overdraw budget as hard limits.
