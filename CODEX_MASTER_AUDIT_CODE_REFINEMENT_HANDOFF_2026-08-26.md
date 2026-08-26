# Codex handoff — master-audit code-refinement round (2026-08-26)

Audience: the implementing Codex agent. Authority: this document is
`SUPPORTING_CURRENT` and subordinate to `audit/MASTER_AUDIT_2026-08-09.md`
(canonical audit ledger, sections 9–13) and
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (the `DL-*` rules, including the
new section 18 `DL-CODE-*` family). The round analysis behind every package is
`audit/MASTER_AUDIT_2026-08-26.md`. If this document and those disagree,
those win.

## Mission

Execute the 2026-08-26 code-refinement goal set G1–G12: first harden the
safety net (gates, negative coverage, four bounded child-facing repairs),
then reverse the structural regression (coordinator size, god-object mass,
clone families, string state, allocation churn) — mechanically,
probe-gated, and without changing what the child experiences.

## Read before any package

1. `audit/MASTER_AUDIT_2026-08-26.md` — the analysis, metrics, and goal set.
2. `audit/MASTER_AUDIT_2026-08-09.md` sections 9 (repair protocol),
   10 (finding fields), 12 (satisfaction gate incl. the code-refinement
   conditions), 13 item 11 (this round's mandate).
3. `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` section 18
   (`DL-CODE-01`–`DL-CODE-10`).
4. The canonical finding record for the package at hand, in
   `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`.
5. `CLAUDE.md` / `AGENTS.md` — the operating contract, including true-2D
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

- Any change to `.github/workflows/` beyond WP-A3's named scope (workflows
  are explicit-task-only; WP-A3 is that explicit task, exactly as bounded).
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

## Stage B packages — structural refinement (start after A1–A3 merge)

### WP-B1 — Extract the Day One / venue / start-menu glue from main (G7, `MA-CODE-001`, binding constraint)

- **Scope:** `scripts/main.gd` `day_one_*` function family, start-menu
  routing, venue delegation; their owning satellites
  (`day_one_director.gd`, `opera_house_venue_2d.gd`, or a new thin
  controller following the satellite mold).
- **Do:** mechanical moves, one bounded owner per commit, state on main per
  the mold, `game_nodes` registration preserved, delegators ≤5 lines.
- **Gate:** `main.gd` at or below 9,000 lines at package end; suite green
  after EVERY commit; zero behavior delta reported by the Day One,
  start-menu (once WP-A1 gates them), opera, and castle probes.
- **Non-goals:** the 2,500-line target (later rounds); any rewrite.

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

- **Scope:** the eight named families (action-press read, `▼` pointer
  widget, cached material factory, AABB kit, avatar spawn, stage input map,
  mode start/end scaffold, act teardown list) and their call sites.
- **Do:** one family per commit: extract one shared helper, migrate every
  copy mechanically. Start with action-press and pointer (smallest).
- **Gate:** owning probes green per family; suite green; the finding's
  history records each family's before/after copy count.
- **Non-goals:** new abstractions beyond the named families.

### WP-B4 — Freeze and shrink string state (G10, `MA-CODE-004`)

- **Scope:** `g`-key usage; typed accessor helpers or per-mode typed state
  objects for the top-traffic families; a recorded distinct-key count.
- **Do:** freeze the surface at 409 (reviewed against the baseline); migrate
  two high-traffic modes to typed accessors mechanically.
- **Gate:** distinct-key count at or below 409 recorded in the package
  report; migrated modes' probes green; suite green.
- **Non-goals:** repo-wide migration in one pass.

### WP-B5 — Pool bursts, tier the newest surfaces (G11, `MA-PERF-002`/`MA-PERF-003`)

- **Scope:** `scripts/main.gd` `_sparkle_burst`; the tier-blind files named
  in `MA-PERF-003` (`games/melody.gd`, `day_one_director.gd`,
  `games/side_scroll.gd`, `opera_gesture_surface.gd` redraw cadence,
  remaining spatial `galaxy.gd`/`companion.gd` costs).
- **Do:** cache mesh/materials, pool a bounded node ring, add the Speedy
  reduction; per tier-blind surface, implement a Speedy path or record the
  measured budget note (`DL-CODE-08`).
- **Gate:** no per-call mesh/material allocation remains in the helper;
  visual spot-check at both tiers for one touched surface; suite green.
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

`A1 ∥ A2 ∥ A3 ∥ A4 ∥ A5 ∥ A6` → merge as each goes green →
`B1 → B2` (B2 may start once B1's main-side opera delegation is stable) →
`B3 ∥ B4 ∥ B5 ∥ B6` behind them. If capacity is constrained, strict order:
A1, A2, A3, A6, A4, A5, B1, B2, B3, B5, B4, B6.

---

This handoff changes no rule and grants no authority: it sequences work the
canonical audit already mandates in its section 13 item 11. When all twelve
packages are merged or reported "no change needed", the next master-audit
round re-measures the section-4 metrics table and re-scores the moved
dimensions.
