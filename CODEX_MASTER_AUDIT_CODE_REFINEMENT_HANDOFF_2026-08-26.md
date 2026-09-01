# Codex handoff — master-audit code-refinement round (2026-08-26)

Audience: every agent working the round — the Luna implementation pool and
whichever agent (Codex or Claude) holds the integration and Stage R
re-audit lanes (agent assignment: design 08 §8). Authority: this document is
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
6. The wing inventory, `audit/MASTER_AUDIT_2026-08-09.md` section 3.4 —
   which design-consistency and performance wings apply to your package,
   and which are someone else's in-flight scope.
7. `CLAUDE.md` / `AGENTS.md` — the operating contract, including true-2D
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
- **Governance home** (owner instruction 2026-08-30): the current copies of
  this handoff, the master audit, the findings register, design 06 sections
  18–19, design 08, and the owner guide live on branch
  `claude/master-audit-game-analysis-qiko9l`; dev's copies are a stale
  earlier snapshot from its `a0571eea` merge. Read governance at that branch
  head, and land every governance edit there — the integration lane's
  ledger/`CHG` rows and Stage R's lifecycle transitions. Implementation
  branches still fork off fresh `origin/dev` and merge to dev per Branch
  law; only the governance documents live apart.
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
- **Reversibility is part of done** (design 08 §6): a package lands with a
  recorded way back — behavior-identical commits so `git revert` is always
  safe; replaced entry points become one-line delegating shims kept for one
  promotion cycle, never deletions (probes keep working; un-migrating stays
  local); the package report carries the exact inverse (revert command plus
  shim-restoration note) so the integration lane can append the package's
  `CHG-*` ledger entry.
- **Single-writer governance** (design 08 §8): implementation agents do NOT
  edit `audit/MASTER_AUDIT_2026-08-09.md`, the findings register, the
  `CHG-*` rollback ledger, `design/05_DOC_LEDGER.md`, or design 08. Deliver
  your package report; the integration lane applies ledger rows and `CHG`
  entries serially, and ONLY the Stage R re-audit lane applies lifecycle
  transitions. Proposing a transition in your report is your job; writing
  it is not.

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
- Any change inside another wing's in-flight scope — today that means the
  tablet performance wing's (capture tooling, tier thresholds,
  quality-tier semantics, device tuning) — or any child-visible work whose
  governing design-consistency wing does not exist yet (report the wing
  gap instead of improvising a style).

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

## Agent assignment (owner direction 2026-08-30; design 08 §8)

The owner drives this round through **single-prompt orchestrated runs**:
one kickoff prompt per stage, and the orchestrating agent divides the
packages across its own **Luna agents** — the owner has no per-agent
access, so every rule below is the orchestrator's to enforce internally.

- One package per internal agent, one branch per package, off fresh
  `origin/dev`. Stage A's six packages may run concurrently (WP-A3 lands
  as its own branch, never batched with another workflow-touching change).
  The Stage C spine is strictly serial — C0 through C6 in order, never
  concurrent; a C run's kickoff prompt names exactly which steps it may
  cover. Stage B parallelizes behind its stated dependencies.
- Governance edits (`CHG` entries, ledger rows) happen once per run,
  serially, in the run's closing integration phase — never inside an
  implementation agent's branch.
- The Stage R re-audit is performed by an internal agent that implemented
  NONE of the packages it reviews, or by a dedicated follow-up run.
- The run's final report to the owner states which internal agent carried
  each package and which carried the re-audit, so the separation is
  checkable.

The contract in this document is agent-neutral: whichever agent holds a
package obeys all of it.

## Wings and parallel workstreams (canonical section 3.4)

The master audit is a wing-extensible development bible: design-consistency
wings (image style/technique, character design, typography, palette,
animation, audio identity, chapter templates) are added regularly so new
chapters match established build and quality with minimal hand-tweaking.
Two obligations follow for every package in this round:

1. **Consult before you create.** Anything child-visible conforms to the
   applicable standing wings; a wing gap is reported to the owner as a wing
   request in your package report — never improvised around. Match the
   wing's named exemplars, not your own taste.

   The **Pacing and session flow wing is Standing** (2026-08-31;
   `DL-PACE-01`–`DL-PACE-06`, design 06 §21): any child-facing beat your
   package touches obeys the one-breath template (payoff → breath → one
   instruction; no same-frame caption bursts), announces macro transitions
   on the played path, and respects the idle assistance ladder and
   reaction-window floors. The Day One improvement guide
   (`DAY_ONE_PACING_REVIEW_2026-08-31.md` §4) is owner-prioritized work,
   not this round's scope — do not absorb it into round packages without
   an explicit owner ask.

   In particular, the **Animation improvement wing is Standing**
   (2026-08-31; `DL-ANIM-01`–`DL-ANIM-06`, design 06 §20): any feedback or
   decorative motion your package touches uses the `scripts/juice.gd`
   vocabulary or an eased in-place curve — never a new hand-rolled copy of
   a vocabulary pattern, never a per-call `Resource` allocation, always
   rest-state hygiene — and `tools/audit_animation_polish.py` (in
   `scripts/ci.sh`) must stay green. Migrate hand-rolled sites only in
   files you are already touching. Do not add the checker to
   `probes.yml` yourself: workflows are explicit-task-only, and those two
   lines are already proposed to the owner.
2. **The tablet performance wing is IN FLIGHT and owned by Fable.** Its
   scope: target-device/tablet performance measurement, the capture
   protocol, quality-tier threshold values, and device-side tuning — the
   `MA-PERF-001` lineage. Round agents do NOT take that scope: no capture
   tooling, no tier-threshold or quality-tier-semantics changes, no
   device-performance claims. Where a package's change plausibly moves
   measured performance (allocation, draw calls, texture residency), state
   the expected delta in your report so the wing can account for it.
   Code-side work the round DOES own is unchanged: WP-C4's pooling and
   WP-B5's per-surface Speedy paths and budget notes. The engine-adoption
   evaluation (`ENGINE_ADOPTION_4_7_2026-08-30.md`) hands the wing its
   Tier-2 items by name: Perfetto/Tracy tracing as the capture-protocol
   backbone, Mobile-renderer debanding A/B, edge-to-edge display,
   16 KB-page verification on an Android 15+ device, F16 precision
   verification, shader-baker applicability on Android/Vulkan, and the
   one-time `msaa_2d` ruling.

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
  the thin GameMode surface over its existing lifecycle. The old entry
  functions become one-line delegating shims (design 08 §6.1), NOT
  deletions — probes keep calling them unchanged.
- **Gate:** `probe_dungeon` + suite green; probe transcripts byte-stable
  across the migration commit; `main.gd` net negative; the shim bodies'
  pre-migration originals recorded in the package report for the `CHG`
  inverse.
- **Non-goals:** dungeon gameplay or difficulty changes.

### WP-C2 — The standalone family (M2)

- **Scope:** kart, galaxy, combat, stuffie battle, ember, and opera entry —
  **one mode per commit**; each scaffold pair becomes a shim pair
  (design 08 §6.1); the ratchet arms as blocking in `scripts/ci.sh`.
- **Gate:** each mode's probes + suite green per commit; every scaffold
  body lives only in its shim (grep-verifiable); ratchet green in `ci.sh`;
  per-mode inverse recorded.
- **Non-goals:** touching the arena family yet.

### WP-C3 — The arena family (M3)

- **Scope:** `ArenaModeAdapter` wrapping the existing
  `_start_game → _tick_game → _end_game` satellites (fetch, dolls, seek,
  melody, slide, treasure, shop, fairy, brawl) and the K2 canvas kit; the
  `_enter_arena` switch and `_process` mode branches reduce to
  director-delegating shims (design 08 §6.1).
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
- **Coordination:** pooling is visual/behavior-identical; report the
  allocation delta to the tablet performance wing (Fable) and change no
  tier thresholds — those are the wing's.
- **Non-goals:** redesigning any service's behavior.

### WP-C5 — Typed mode state pilots (M5; executes G10/WP-B4)

- **Scope:** two high-traffic migrated modes swap `g["…"]` ephemeral keys
  for typed state per design 08 §4.5; the g-key budget ratchets down; the
  rule applies to every subsequently migrated mode. Typed state uses
  typed dictionaries (`Dictionary[K, V]`) and typed members — the
  engine-adoption evaluation measured 0 typed of 1,789 dictionary
  declarations; new and migrated state closes that gap as touched.
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
  one registry row with `main.gd` untouched (design 08 §9.1); shim windows
  and inverses recorded per glue family.
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
- **Coordination:** tier PATHS are this package's; tier THRESHOLD VALUES
  and all device verification belong to the in-flight tablet performance
  wing (Fable) — report each surface's expected device-side delta for the
  wing rather than measuring or tuning it here.
- **Non-goals:** device measurement or threshold tuning (the tablet
  performance wing's scope, `MA-PERF-001`).

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

## Stage R — implementation re-audit (design 08 §9; runs at each stage boundary)

No package's finding advances on its author's word. WP-R1 runs after
Stage A merges, WP-R2 after C2, WP-R3 after C6 plus the remaining B
packages. The re-auditing agent must not have implemented the package under
review. Per package it: re-executes the gate (re-runs the named probes and
checks at the merged head, re-measures the gate's metric, re-runs the
deliberate-break demonstration where the gate names one); diff-verifies the
non-goals; verifies reversibility (the `CHG` entry exists, its inverse is
coherent, shims match their recorded originals); and only then applies the
lifecycle transition in both the section-5 index and the canonical record,
running `python3 tools/audit_document_authority.py` to `ALL OK`. A failed
re-audit gets a dated failure note in the finding history and returns to
the implementation lane with its lifecycle unmoved. WP-R3 additionally runs
the growth-law acceptance test (design 08 §9.1) and re-measures the round's
standing metrics table.

## Stage E packages — engine adoption, Tier 1 (any time after Stage A; see `ENGINE_ADOPTION_4_7_2026-08-30.md`)

### WP-E1 — Revalidate the 4.4-era engine-bug protocols (`MA-ENGINE-002`, P2)

- **Scope:** the exit-124 amnesty in `scripts/ci.sh:179-186` and
  `.github/workflows/probes.yml:196-205` (the probes.yml half is workflow
  scope — same explicit-task boundary discipline as WP-A3, own branch,
  called out in the commit message); the NPOT + `compress/mode=2`
  importer-deadlock protocol; no probe assertions change.
- **Do:** per `DL-ENGINE-03`, empirically: run the full suite N
  consecutive times (N ≥ 5) with the amnesty in report-only and record
  every exit-124; on a throwaway branch import a deliberately NPOT +
  `compress/mode=2` texture under the 20-minute guard. Zero reproductions
  → retire the amnesty copies / propose the importer-rule rewording to
  the owner (CLAUDE/AGENTS edits are explicit-task-only — report, do not
  self-apply). Reproduced → re-attribute the comments to 4.7.2 with dated
  observations and a next-bump re-test trigger.
- **Gate:** the demonstration evidence (run logs, import log) in the
  package report; suite green; neither protocol still attributes its
  reason to an engine version the project does not run.
- **Non-goals:** loosening any failure regex; texture-budget rule changes.

### WP-E2 — Unify exact-version assertions onto the baseline record (`MA-ENGINE-001`, P2)

- **Scope:** `tools/audit_opera_capture.py` version check + its test
  fixtures; `tools/audit_godot_baseline.py` required-pins list; the seven
  live rollback narratives in `tools/plan_audit_rollback.py` (one-line
  then-current-baseline qualifiers, applied by the integration lane).
- **Do:** the capture tool derives its required version from
  `tools/godot_baseline.json`; fixtures follow with a drift-negative
  test; the tool joins the baseline audit's required pins so the class is
  structurally closed.
- **Gate:** baseline contract tests + capture-tool tests green; one fresh
  4.7.2-produced capture manifest demonstrated accepted; suite green.
- **Non-goals:** touching historical evidence documents' version mentions
  (they are correct history).

## Reporting format (per package, into the PR/branch description)

1. Finding re-verification result (Stage 0), with any history correction
   made.
2. Commit list with one-line scopes.
3. Probe evidence: local suite result and the CI run link for the branch
   head.
4. Metric before/after where the gate names one (line counts, key counts,
   copy counts, roster counts).
5. Reversibility evidence: the exact inverse (revert command; for shim
   steps, the recorded pre-migration bodies) for the integration lane's
   `CHG` entry.
6. Proposed lifecycle transition with the evidence that supports it — or
   "no change needed" with evidence. Stage R applies transitions; you do
   not.

## Sequencing summary

`A1 ∥ A2 ∥ A3 ∥ A4 ∥ A5 ∥ A6` (six Luna agents in parallel; A3 merges
alone) → **WP-R1** → the platform spine, strictly in order and single-agent:
`C0 → C1 → C2` → **WP-R2** → `C3 → C4 → C5 → C6`. Independent cleanups
interleave behind it: `B2` any time; `B3` after C2 (so the
platform-dissolved families are already gone); `B5` after C4 (FxService
exists); `B6` any time; `E1`/`E2` any time after Stage A (E1's workflow
half merges alone) → **WP-R3** (final re-audit + growth-law test +
metrics re-measure). If capacity is constrained, strict order:
A1, A2, A3, A6, A4, A5, R1, C0, C1, C2, R2, B2, C3, C4, B5, C5, B3, C6,
B6, R3.

WP-B1 and WP-B4 are not in the order because Stage C executes them (C6 and
C5); running them standalone is an error.

---

This handoff changes no rule and grants no authority: it sequences work the
canonical audit already mandates in its section 13 item 11, through the
remodel the owner requested in `design/08_TARGET_ARCHITECTURE.md`. When all
packages are merged or reported "no change needed", the next master-audit
round re-measures the section-4 metrics table, runs the growth-law test,
and re-scores the moved dimensions.
