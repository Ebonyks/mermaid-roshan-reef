# Codex handoff — master-audit code-refinement round (2026-08-26)

Audience: the implementing Codex agent. Authority: this document is
`SUPPORTING_CURRENT` and subordinate to `audit/MASTER_AUDIT_2026-08-09.md`
(canonical audit ledger, sections 9–13) and
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (the `DL-*` rules, including the
new section 18 `DL-CODE-*` family). The round analysis behind every package is
`audit/MASTER_AUDIT_2026-08-26.md`. If this document and those disagree,
those win.

## Mission

Execute the 2026-08-26 code-refinement round in three stages: first harden
the safety net (Stage A — gates, negative coverage, four bounded
child-facing repairs), then **remodel the architecture** (Stage C — the Mode
Platform of `design/08_TARGET_ARCHITECTURE.md`, which changes where growth
lands so new wings stop touching `main.gd` and arms a CI ratchet so the
shrink cannot regress again), with the remaining structural cleanups
(Stage B) running alongside. Everything is mechanical, probe-gated, and
invisible to the child.

## Read before any package

1. `audit/MASTER_AUDIT_2026-08-26.md` — the analysis, metrics, and goal set.
2. `design/08_TARGET_ARCHITECTURE.md` — the remodel: growth law, contracts,
   ratchet, and migration plan M0–M6. **Stage C implements this document;
   read it in full before any C package.**
3. `audit/MASTER_AUDIT_2026-08-09.md` sections 9 (repair protocol),
   10 (finding fields), 12 (satisfaction gate incl. the code-refinement
   conditions), 13 item 11 (this round's mandate).
4. `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` section 18
   (`DL-CODE-01`–`DL-CODE-12`).
5. The canonical finding record for the package at hand, in
   `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`.
6. `CLAUDE.md` / `AGENTS.md` — the operating contract, including true-2D
   medium rules and protected-content law.

## Stage 0 — review first (mandatory, per package)

The audit is evidence, not gospel; the code is the truth. Before changing
behavior for a package:

- Re-verify its finding at your current head with the record's own
  reproduction steps. The round pinned its measurements to `9a1754c1`; dev
  may have moved.
- If the code has moved materially, append a dated correction to the
  finding's `history` cell (never rewrite existing history) and adjust the
  package scope to what is actually true before implementing.
- If the finding no longer reproduces at all, stop: record that in the
  history, mark your package report "no change needed", and do not
  manufacture a change.

## Ground rules (binding on every package)

- **Branch law:** one package per branch, `codex/<topic>` off fresh
  `origin/dev`; merge to dev only with the full probe suite green on CI for
  the branch's exact head; never touch `master`
  (`WORKFLOW_BRANCHING_2026-07-18.md`).
- **Behavior contract:** Stage B packages are behavior-preserving. Exact
  behavior, state ownership, and save compatibility are unchanged; if a
  trusted probe fails after a refactor step, revert the step — never patch
  the probe (`DL-CODE-06`, `DL-QA-02`).
- **Smallest truthful change** (canonical section 9.5): no bundled redesign,
  no opportunistic cleanup outside the package boundary.
- **Invariants outrank goals:** nothing in this round may weaken no-fail,
  non-reader, one-finger, save-compatibility, protected-content, or
  security/workflow rules to hit a number.
- **Save schema:** additive keys with defaults only; never remove or rename
  a key (`DL-SAVE-01`).
- **Probes are the gate:** run the relevant focused probes plus the full
  local suite (`scripts/ci.sh`) before pushing; CI must be green at the head
  you merge.
- **Lifecycle bookkeeping:** when a package completes its acceptance gate,
  move its finding to `FIXED_PENDING_VERIFICATION` (not `VERIFIED_FIXED`)
  in both the section-5 index row and the canonical record, with the closure
  evidence you actually produced. Terminal claims wait for the canonical
  verification levels.

## Escalation triggers — stop and surface to the owner

- Any change to `.github/workflows/` beyond the named scopes of WP-A3 and
  WP-C6 (workflows are explicit-task-only; those two packages are the
  explicit tasks, exactly as bounded).
- Any save-schema question beyond additive keys with defaults.
- Anything touching `assets/book/`, `assets/audio/voices/`,
  `assets/characters/friends/`, or `attic/gabby/`.
- Any package that seems to require a behavior change a probe would have to
  be rewritten for.
- Any conflict with an owner decision, including the 2026-08-25 venue
  commits (`0277071f`/`9a1754c1`) — the newest owner direction wins
  (`DL-AUTH-01`).

## Stage A packages — harden the net (run first, any order, parallel-safe)

### WP-A1 — Gate the Day One wing (G1, `MA-CI-004`, P1)

- **Scope:** `scripts/ci.sh`, `.github/workflows/probes.yml` trusted-roster
  lines; the eight `scripts/probe_day_one_*.gd` /
  `scripts/probe_start_menu_routing.gd` files (classification only —
  repairs to a probe's own determinism are in scope; gameplay changes are
  not).
- **Do:** classify the eight per canonical section 11.2; promote the
  deterministic non-capture ones (at minimum `probe_day_one_director`,
  `probe_day_one_integration`, `probe_day_one_pool_cleanup`,
  `probe_start_menu_routing`) into BOTH rosters; capture-style ones become
  advisory. Run each candidate three consecutive green local runs before
  promotion.
- **Gate:** on a throwaway branch, deliberately break the New Game routing
  and show the suite go red; revert; suite green; wall time within the
  workflow ceiling.
- **Non-goals:** no Day One gameplay changes; no roster removals.

### WP-A2 — Extend the passive negative test (G2, `MA-CI-005`, P1)

- **Scope:** `scripts/probe_passive.gd`; read-only over save/reward fields.
- **Do:** extend `_progress_snapshot()` to every save-backed reward surface
  (opera stars/progress/pantry, combat + tutorial completion, dungeon
  checkpoints, `stuffie_wins`/care points, Day One serialized state, castle
  milestone fields); add cheap passive legs where entry is trivial; document
  the extend-or-own-idle-leg rule in the probe header.
- **Gate:** mutation test per snapshot section (hand-award one field under
  idle input → probe fails); full suite green.
- **Non-goals:** no gameplay changes; no weakening of existing legs.

### WP-A3 — Pin the promotion gate (G3, `MA-CI-006`, P2)

- **Scope:** `.github/workflows/promote.yml` run-selection logic ONLY, plus
  a committed expected-roster count and the probe-heading count emission in
  `probes.yml`'s existing summary output if needed. This is the explicit
  workflow task; call it out in the commit message per the security rules.
- **Do:** select the newest completed run for the SHA (prefer `push`
  events); fail on red; compare executed trusted-heading count to the
  committed expected count.
- **Gate:** dry-run promotion path demonstrated on a test ref (do not
  promote); a shortened-roster branch shows the guard trip.
- **Non-goals:** no channel, signing, tag, or android.yml changes.

### WP-A4 — Declare the Mic bus (G4, `MA-AUDIO-002`, P2)

- **Scope:** `default_bus_layout.tres`, `scripts/mic_input.gd` (assertion
  only), `scripts/probe_audio.gd`.
- **Do:** declare a seventh, muted `Mic` bus; keep the runtime rename as a
  defensive assertion path; extend `probe_audio` to assert Mic exists and is
  muted.
- **Gate:** `probe_audio` and `probe_mic` green; suite green.
- **Non-goals:** no mix, volume, or ducking changes.

### WP-A5 — Guard the swim pointer path (G5, `MA-TOUCH-002`, P2)

- **Scope:** `scripts/games/side_scroll.gd` swim branch;
  `scripts/probe_touch_stress.gd` (new leg).
- **Do:** route the swim-branch press through `reserved_zone_hit()` exactly
  as the walk path does; then audit the remaining direct
  `Input.is_mouse_button_pressed` reads in gesture code and confirm each is
  inside a router-owned drag context, recording the audit result in the
  finding history.
- **Gate:** new touch-stress leg proves a held medallion no longer steers in
  a swim stage; suite green.
- **Non-goals:** no control-feel tuning.

### WP-A6 — Persist castle interaction progress (G6, `MA-SAVE-001`, P2)

- **Scope:** `scripts/arena/castle_rooms_25d.gd` state writes,
  `scripts/save_state.gd` additive keys, save probes.
- **Do:** promote durable child-visible castle interaction progress (the
  per-pin dust-bunny clearing map and equivalents) into append-only save
  fields with defaults, written through the existing `_queue_save` cadence;
  leave true per-session scratch in `g`.
- **Gate:** kill-and-relaunch restore demonstrated by an extended save
  probe; passive probe unchanged; suite green.
- **Non-goals:** no interaction redesign; no non-castle scratch migration.

## Stage C packages — the Mode Platform (the remodel; start after A1–A2 merge)

Stage C is `design/08_TARGET_ARCHITECTURE.md` §7 turned into packages —
WP-C0 through WP-C6 are migration steps M0 through M6, and that document's
step table carries the full detail; the entries below add only the
handoff-level boundaries. Each package is one branch, behavior-identical,
suite-green at every commit. Do not reorder: the pattern is proven on the
cheapest real mode before anything load-bearing moves.

### WP-C0 — Platform skeleton (M0)

- **Scope:** new `scripts/platform/` (GameMode, ModeContext, ModeRegistry,
  ModeDirector, Services façade delegating to today's main methods); new
  `tools/audit_structure.py` + `tools/structure_budget.json` in report-only
  mode; new trusted `probe_mode_platform`. **Pure addition — zero existing
  lines change.**
- **Gate:** suite green; the new probe green three consecutive local runs
  and added to BOTH rosters; the structure gate prints its baselines.
- **Non-goals:** migrating any real mode; arming the ratchet.

### WP-C1 — Pilot: dungeon through the director (M1)

- **Scope:** the dungeon glue (`_start_dungeon_now`/`_end_dungeon`, its
  pause-Leave branch) and one `ModeRegistry` row; `dungeon_level.gd` gains
  the thin GameMode surface over its existing lifecycle.
- **Gate:** `probe_dungeon` + suite green; `main.gd` net negative; the
  director reproduces the music-save/HUD/player sequence exactly (compare
  probe transcripts before/after).
- **Non-goals:** dungeon gameplay or difficulty changes.

### WP-C2 — The standalone family (M2)

- **Scope:** kart, galaxy, combat, stuffie battle, ember, and opera entry —
  **one mode per commit**; the `_start_X_now`/`_end_X` scaffold family
  dissolves; the ratchet arms as blocking in `scripts/ci.sh`.
- **Gate:** each mode's probes + suite green per commit; the scaffold grep
  count reaches zero; ratchet green in `ci.sh`.
- **Non-goals:** touching the arena family yet.

### WP-C3 — The arena family (M3)

- **Scope:** `ArenaModeAdapter` wrapping the existing
  `_start_game → _tick_game → _end_game` satellites (fetch, dolls, seek,
  melody, slide, treasure, shop, fairy, brawl) and the K2 canvas kit; the
  `_enter_arena` switch and `_process` mode branches dissolve.
- **Gate:** `probe_audit`, the per-game probes, and `probe_passive` + suite
  green; `_process` under 100 lines.
- **Non-goals:** changing any game's simulation or feel.

### WP-C4 — Services extraction (M4)

- **Scope:** `services.stage` (StageKit — the six builder helpers and their
  ~280 cross-module call sites), `services.objective` (voice + pointer +
  card in one call), `services.fx` (pooled, tier-aware — this executes the
  pooling half of G11/`MA-PERF-002`), `services.input` (GameInput — closes
  the composite-read duplication), `services.reward` formalized.
  Delegate-first, call sites next, delegate deleted last.
- **Gate:** suite green per commit; the `m._`-private-call budget ratchets
  down; no per-call mesh/material allocation remains in the FX path
  (allocation grep + visual spot-check at both tiers).
- **Non-goals:** redesigning any service's behavior.

### WP-C5 — Typed mode state pilots (M5; executes G10/WP-B4)

- **Scope:** two high-traffic migrated modes swap `g["…"]` ephemeral keys
  for typed state per design 08 §4.5; the g-key budget ratchets down; the
  rule applies to every subsequently migrated mode.
- **Gate:** pilot-mode probes + suite green; distinct-key count at or below
  409 and recorded.
- **Non-goals:** repo-wide migration in one pass.

### WP-C6 — Finale: Day One, venue, start-menu; ratchet everywhere (M6; executes G7/WP-B1)

- **Scope:** the `day_one_*` glue (~30 functions), venue delegation, and
  start-menu routing become modes/registry rows; the ratchet arms as
  blocking in `.github/workflows/probes.yml` (workflow edit — the same
  explicit-task boundary discipline as WP-A3, called out in the commit
  message); budgets set at the measured post-migration floor.
- **Gate:** Day One/start-menu probes (gated by WP-A1) + suite green;
  `main.gd` at or below 9,000 lines at package end with the steady-state
  target below 2,500 tracked by the ratchet from there; **the growth-law
  test passes** — a throwaway branch adds a trivial test mode as one file +
  one registry row with `main.gd` untouched (design 08 §8.1).
- **Non-goals:** Day One gameplay changes; reaching 2,500 in this round.

## Stage B packages — remaining structural cleanups (interleave behind C)

Three original Stage B packages are executed by Stage C and MUST NOT be run
standalone (moving the same code twice is churn): **WP-B1 → WP-C6**,
**WP-B4 → WP-C5**, and the pooling half of **WP-B5 → WP-C4**. The packages
below remain independent.

### WP-B2 — Decompose the opera gesture surface (G8, `MA-CODE-001`/`MA-CODE-002`)

- **Scope:** `scripts/opera_gesture_surface.gd` (6,185 lines) split along
  its per-career/per-widget seams behind an unchanged dispatcher API;
  `opera_career_world_2d.gd` call sites only as needed.
- **Do:** first commit a decomposition plan into the finding history naming
  the intended modules (`DL-CODE-02`), then extract one module per commit.
- **Gate:** every resulting module at or below 3,000 lines; opera probes
  (`probe_opera`, `probe_opera_2d`, `probe_opera_pipe`,
  `probe_opera_nursery`) byte-identical in verdicts; suite green each step.
- **Non-goals:** widget behavior, art, timing, or difficulty changes.

### WP-B3 — Consolidate the clone families (G9, `MA-CODE-003`)

- **Scope:** the six families the platform does not already dissolve —
  action-press read, `▼` pointer widget, cached material factory, AABB kit,
  avatar spawn, act teardown list — and their call sites. (The mode
  start/end scaffold dissolves in WP-C1–C2 and the stage input map becomes
  `services.input` in WP-C4; do not consolidate those separately.)
- **Do:** one family per commit: extract one shared helper, migrate every
  copy mechanically. Start with action-press and pointer (smallest). Where
  a family's natural home is a Stage C service that already exists by then,
  put the helper there rather than inventing a second home.
- **Gate:** owning probes green per family; suite green; the finding's
  history records each family's before/after copy count.
- **Non-goals:** new abstractions beyond the named families.

### WP-B5 — Tier the newest surfaces (G11, `MA-PERF-003`; pooling half runs in WP-C4)

- **Scope:** the tier-blind files named in `MA-PERF-003`
  (`games/melody.gd`, `day_one_director.gd`, `games/side_scroll.gd`,
  `opera_gesture_surface.gd` redraw cadence, remaining spatial
  `galaxy.gd`/`companion.gd` costs). The `_sparkle_burst` pooling itself is
  WP-C4's FxService — do not fix it twice.
- **Do:** per tier-blind surface, implement a Speedy path or record the
  measured budget note (`DL-CODE-08`); registry rows gain their `tier`
  field as modes migrate.
- **Gate:** every named surface has a tier path or budget note; visual
  spot-check at both tiers for one touched surface; suite green.
- **Non-goals:** device measurement (that is `MA-PERF-001`'s protocol, not
  this container's).

### WP-B6 — Dead code out, shared probe harness in (G12, `MA-CODE-005`/`MA-CI-007`)

- **Scope:** `scripts/main.gd` `_fail_line` + dead lose branch; a new shared
  probe harness; the top twenty trusted probes by roster order.
- **Do:** delete the dead loss path in one commit. Then introduce one shared
  harness (boot, intro skip, sim-time waits, isolated user dirs, snapshot
  helpers) and migrate probes a few per commit, preferring bounded semantic
  waits over wall-clock windows (the `ff068db` pattern).
- **Gate:** symbols gone; harness adopted by twenty trusted probes with no
  assertion weakened; no fixed-frame timing sample remains in trusted
  probes; suite green throughout.
- **Non-goals:** untrusted-probe cleanup (that is `MA-CI-003`
  classification work).

## Reporting format (per package, into the PR/branch description and the finding history)

1. Finding re-verification result (Stage 0), with any history correction
   made.
2. Commit list with one-line scopes.
3. Probe evidence: local suite result and the CI run link for the branch
   head.
4. Metric before/after where the gate names one (line counts, key counts,
   copy counts, roster counts).
5. Lifecycle transition applied (`CONFIRMED_OPEN` →
   `FIXED_PENDING_VERIFICATION`) in index + record, or "no change needed"
   with evidence.

## Sequencing summary

`A1 ∥ A2 ∥ A3 ∥ A4 ∥ A5 ∥ A6` → merge as each goes green. Then the platform
spine, strictly in order: `C0 → C1 → C2 → C3 → C4 → C5 → C6`. Independent
cleanups interleave behind it: `B2` any time; `B3` after C2 (so the
platform-dissolved families are already gone); `B5` after C4 (FxService
exists); `B6` any time. If capacity is constrained, strict order:
A1, A2, A3, A6, A4, A5, C0, C1, C2, B2, C3, C4, B5, C5, B3, C6, B6.

WP-B1 and WP-B4 are not in the order because Stage C executes them (C6 and
C5); running them standalone is an error.

---

This handoff changes no rule and grants no authority: it sequences work the
canonical audit already mandates in its section 13 item 11, through the
remodel the owner requested in `design/08_TARGET_ARCHITECTURE.md`. When all
packages are merged or reported "no change needed", the next master-audit
round re-measures the section-4 metrics table, runs the growth-law test,
and re-scores the moved dimensions.
