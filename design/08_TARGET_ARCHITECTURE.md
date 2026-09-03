# Master design — target architecture: the Mode Platform

- **Document ID:** `TA-2026-08-26` · **Revision 2, 2026-08-30** (owner
  direction: add explicit reversibility machinery, an independent
  implementation re-audit stage, and the agent-assignment model; complete
  the contracts to implementation grade — revision 1's interface sketches
  and its replace-by-deletion migration were not executable as written).
- **Status:** `BINDING_DOMAIN` for game-code structure, produced on direct
  owner request 2026-08-26. Section 11 lists the decisions reserved for
  explicit owner confirmation; everything else binds as each migration step
  lands suite-green.
- **Subordinate to:** `SECURITY.md`, the save/protected-content/workflow
  rules, direct owner decisions, and
  `06_COMPREHENSIVE_DESIGN_LANGUAGE.md`. `03_TECHNICAL_ARCHITECTURE.md`
  describes what the code **is**; this document specifies what it
  **becomes** and the law that keeps it there.
- **Companions:** analysis and evidence in
  `../audit/MASTER_AUDIT_2026-08-26.md`; execution packages in
  `../CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md`
  (Stages A / C / B / R); rules `DL-CODE-01`–`DL-CODE-12`; rollback ledger
  `../audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`.
- **What this is not:** not a rewrite authorization. Every step is a
  mechanical, behavior-preserving move under `DL-CODE-06`, gated by the
  trusted suite, reversible one step at a time. It is also not a universal
  game engine — that was evaluated and **rejected** (03 §2), and this
  document keeps that ruling: simulations stay per-mode; only the
  *plumbing* is unified.

---

## 0. The disease, precisely

`main.gd` does not grow because people are careless. It grows because the
codebase has exactly one place where five different seams live, so **every
new wing must edit main to exist**:

| Seam | Where it lives today | Cost of mode N+1 |
|---|---|---|
| Mode start/stop | a hand-copied `_start_X_now` / `_end_X` pair per mode — the same music-save / `game = id` / HUD-off / hide-player / instantiate / `finish_cb` sequence seven-plus times | ~30 lines on main |
| Tick dispatch | the ~390-line `_process` and the `_enter_arena` switch route by string id | edits to both |
| Interaction/touch registration | `_populate_touch_interactables` and friends on main | edits on main |
| Cross-cutting services | `_say`, `_set_objective`, `_sparkle_burst`, `_reward`, `_write_save`, and six builder helpers are **private methods of main**, called 846 times from satellites as `m._…()` (about 6,100 `m.` member accesses of every kind; both measured 2026-09-01) — `m._…` | main can never shrink below the sum of its services |
| Ephemeral state | the `g` scratch dictionary (409 distinct string keys at `9a1754c1`; 413 at the 2026-09-01 re-audit) plus main-side fields | new keys, new fields |

Six weeks of a standing shrink target still lost ground
(8,239 → 10,499 lines) because every shrink was a one-off extraction while
every new feature paid the five seams again (`MA-CODE-001`,
`MA-CODE-002`). Shrinking harder is not the fix. **Changing where growth
lands is.**

## 1. The growth law

> **Adding an activity, wing, or zone touches `main.gd` zero times.**
> A new mode is: one mode script (plus its art and its probe) and one
> registry row. Dispatch, teardown, music hand-off, HUD hand-off, pause
> Leave, save wiring, touch registration, and the probe surface are
> platform plumbing that exists exactly once.

This is rule `DL-CODE-11`, it is testable (§9.1), and it is enforced by the
structure ratchet (§7, `DL-CODE-12`) so it cannot silently regress the way
the line-count target did.

## 2. What stays true

- **One contract, few engines.** The MiniGame contract (03 §2) already
  names the six planks every game shares — lifecycle, GameInput, reward
  funnel, mercy hooks, voice+pointer, probe surface. Today those planks are
  prose plus copy-paste; the platform turns them into runtime objects. The
  K2 Canvas kit, HitEngine, StorybookUI, camera composition, and every
  per-mode simulation remain exactly what they are.
- **The Phase-7 satellite mold is unchanged** for RefCounted satellites:
  logic only, durable state on main, teardown-owned nodes, a probe.
- **Standalone mode nodes already own their ephemeral state** (03 §1:
  `kart`, `galaxy`, `combat_arena`, `dungeon_level`, `stuffie_battle`,
  `ember_fortress`, `opera_*`). The platform generalizes that existing
  reality. The dividing line is sharpened in §5.6: *durable* progress lives
  on main/`save_state` through the reward funnel; *ephemeral* mode state
  lives on the mode instance and dies with it.
- **The save contract, no-fail rules, non-reader rules, true-2D migration,
  and owner decisions are untouched.** The platform is medium-neutral
  plumbing: a spatial legacy mode and a Canvas mode ride the same director
  while `MA-2D-002` converts their interiors on its own schedule.
- **Extract, don't rewrite.** Every migration step moves existing bodies
  behind a uniform doorway. A mode that fits badly keeps a thin adapter
  instead of being rewritten to fit.
- **The rollback culture is reused, not duplicated.** Reversibility rides
  the existing `CHG-*` ledger and its guarded-inverse discipline (§8);
  this document adds the platform-specific mechanisms, not a second
  ledger.

## 3. Target shape

```text
scenes/main.tscn
└── ReefMain — coordinator (steady-state target < 2,500 lines)
    ├── owns: save-backed fields · world root · shrinking legacy g/mg scratch
    ├── mode_director: ModeDirector ──reads──> ModeRegistry.MODES (const data)
    │     └── current: GameMode instance
    │           ├── standalone node modes (dungeon, kart, galaxy, opera, …)
    │           ├── ArenaModeAdapter → games/* satellites (fetch, dolls, …)
    │           └── CanvasModeAdapter → K2 kit (picture games, dance)
    ├── services: Services — owned object created in _ready(), passed by ref
    │     ├── objective : ObjectiveService   say + pointer + picture card, one call
    │     ├── fx        : FxService          pooled bursts/celebrations, tier-aware
    │     ├── reward    : RewardService      the _reward funnel + medals + save writes
    │     ├── input     : GameInput          the one composite one-finger read
    │     ├── stage     : StageKit           the builder helpers main lends out today
    │     └── refs to existing satellites: audio_director, medal_system,
    │         interaction_director, camera_kit, storybook_ui, save_state
    └── world builders — per-zone, extracted on the true-2D schedule
```

File layout (all new files; nothing existing moves in M0):

```text
scripts/platform/game_mode.gd            class_name GameMode
scripts/platform/mode_context.gd         class_name ModeContext
scripts/platform/mode_registry.gd        class_name ModeRegistry
scripts/platform/mode_director.gd        class_name ModeDirector
scripts/platform/services.gd             class_name Services
scripts/platform/arena_mode_adapter.gd   class_name ArenaModeAdapter   (M3)
scripts/platform/canvas_mode_adapter.gd  class_name CanvasModeAdapter  (M3)
scripts/probe_mode_platform.gd           trusted probe (M0)
tools/audit_structure.py                 the ratchet (M0, report-only)
tools/structure_budget.json              budgets + append-only history
```

Main keeps three jobs for good: **owning durable state**, **composing the
world root**, and **hosting the director and services**. It stops being the
place where mode plumbing accumulates.

## 4. The contracts — implementation grade

Signatures below are normative. A deviation an implementer believes
necessary is an escalation, not a silent choice. All files use the repo's
tab/typed-GDScript style; every declaration is typed.

### 4.1 `GameMode`

```gdscript
## scripts/platform/game_mode.gd
## The plumbing every activity presents to the ModeDirector. The simulation
## inside stays the mode's own business. Default implementations are no-ops
## so a thin mode overrides only what it uses.
class_name GameMode
extends Node

var ctx: ModeContext

func mode_id() -> String:
	return ""                     # MUST equal its ModeRegistry key

func enter(context: ModeContext) -> void:
	ctx = context                 # override MUST call super() first

func tick(delta: float) -> void:
	pass                          # driven by the director; never self-driven
	                              # from _process while directed

func leave_neutral() -> void:
	pass                          # pause-menu Leave: never a loss, never a
	                              # free win; mode cancels its own tweens,
	                              # timers, audio queue, touch ownership
	                              # (DL-SAVE-03) then calls ctx.finish

func end(win: bool) -> void:
	pass                          # normal completion; rewards ONLY via
	                              # ctx.services.reward; then ctx.finish

func probe_surface() -> Dictionary:
	return {}                     # analytic objective state for bots
	                              # (DL-CODE-10); stable keys, no Nodes

func serialize() -> Dictionary:
	return {}                     # durable fields only; additive keys
	                              # (DL-SAVE-01); {} = nothing durable

func restore(data: Dictionary) -> void:
	pass                          # tolerate missing keys with defaults
```

### 4.2 `ModeContext`

```gdscript
## scripts/platform/mode_context.gd
## The typed handle a mode receives. Modes reach shared behavior through
## `services` and never call m._private_method() — that habit welded ~850 private-call sites (and ~6,100 member accesses)
## call sites to main's internals.
class_name ModeContext
extends RefCounted

var main: ReefMain                # state owner; read save-backed fields here
var services: Services
var cfg: Dictionary = {}          # the mode's ModeRegistry row (read-only)
var finish: Callable              # ModeDirector._on_mode_finished(win: bool)
```

### 4.3 `ModeRegistry`

```gdscript
## scripts/platform/mode_registry.gd — const data. Adding a mode = one row.
## A const script (not JSON) is deliberate: a typo fails the analyzer
## instead of failing silently at runtime.
class_name ModeRegistry

const MODES := {
	"dungeon": {
		"script": "res://scripts/dungeon_level.gd",
		"family": "standalone",        # standalone | arena | canvas
		"music": "dungeon_ice",        # "" = keep current track
		"hide_player": true,
		"hide_hud": true,
		"medal_id": "dungeon",         # "" = no medal surface
		"tier": "room-local; ambient under cap",   # DL-CODE-08 budget note
		"probe": "probe_dungeon",      # ratchet check 5 verifies roster membership
	},
}
```

Row keys are fixed to the set above; the ratchet rejects unknown keys so
the registry cannot become a second scratch dictionary.
`castle_career_routes.gd` is the in-repo precedent — an immutable route
registry that already centralizes thirteen careers' identity without owning
their state.

### 4.4 `ModeDirector` — the seven copies become one body

```gdscript
## scripts/platform/mode_director.gd (~150 lines total, written once)
class_name ModeDirector
extends RefCounted

var m: ReefMain
var services: Services
var current: GameMode = null
var current_id: String = ""
var _prev_track: String = ""
var _prev_hud_visible: bool = true
var _prev_player_visible: bool = true

func start(id: String) -> bool:
	# 1. Guards — the child must never crash or double-enter:
	if current != null:            # re-entry: ignore, warn in log
		return false
	if not ModeRegistry.MODES.has(id):
		push_warning("mode_director: unknown mode '%s'" % id)
		return false               # no-op beats a crash (DL-AGE-03 spirit)
	var row: Dictionary = ModeRegistry.MODES[id]
	# 2. The exact sequence every _start_X_now copy performs today:
	_prev_track = m.cur_track
	if String(row.get("music", "")) != "":
		m._play_music(String(row["music"]))
	m.game = id
	_prev_hud_visible = m.hud_layer.visible if m.hud_layer != null else true
	if bool(row.get("hide_hud", false)) and m.hud_layer != null:
		m.hud_layer.visible = false
	_prev_player_visible = m.player.visible
	if bool(row.get("hide_player", false)):
		m.player.visible = false
	# 3. Instantiate and hand over:
	var mode_script := load(String(row["script"]))
	current = mode_script.new()
	current_id = id
	m.add_child(current)
	var ctx := ModeContext.new()
	ctx.main = m
	ctx.services = services
	ctx.cfg = row
	ctx.finish = Callable(self, "_on_mode_finished")
	current.enter(ctx)
	return true

func tick(delta: float) -> void:
	if current != null:
		current.tick(delta)

func leave_neutral() -> void:      # the pause menu's ONE call
	if current == null:
		return
	current.leave_neutral()        # mode cancels its own state (DL-SAVE-03)
	_teardown()

func _on_mode_finished(_win: bool) -> void:
	_teardown()

func _teardown() -> void:
	# The one teardown every _end_X copy performs today:
	if current != null:
		current.queue_free()
	current = null
	current_id = ""
	m.game = ""
	if m.hud_layer != null:
		m.hud_layer.visible = _prev_hud_visible
	m.player.visible = _prev_player_visible
	if _prev_track != "" and _prev_track != m.cur_track:
		m._play_music(_prev_track)  # restore exactly like dungeon_prev_track does
	_prev_track = ""
```

Edge cases, decided here so no implementer guesses:

| Case | Behavior |
|---|---|
| `start()` while a mode runs | ignored with a warning; never stacks |
| Unknown id / missing script | warning + no-op; the world stays playable |
| Focus loss / app pause mid-mode | unchanged: `touch_ui` clears held input (`DL-UI-05`) and the save flush path runs as today; the director adds nothing and removes nothing |
| Pause-menu Leave | `leave_neutral()` — one branch replaces the per-mode list in `pause_menu.gd`; an already-won state still pays out (the `combat_arena.cancel(notify_finish)` pattern generalized: a mode's `leave_neutral` MAY call `end(true)` if its win already happened) |
| Save during a mode | unchanged: durable writes go through `services.reward`/`save_state` when they happen; the director never writes saves |
| Music row `""` | current track kept; restore logic skips |
| Nested activities (a mode launching a sub-activity) | out of scope for M0–M6: modes that do this today (castle rooms → careers) keep their existing internal routing; the director owns only top-level modes |

### 4.5 Services

```gdscript
## scripts/platform/services.gd — owned by main, created in _ready(),
## passed by reference. NOT autoloads (see §11.2).
class_name Services
extends RefCounted

var m: ReefMain
var objective: ObjectiveService    # M4; delegates to m until then
var fx: FxService                  # M4
var reward: RewardService          # M4
var input: GameInput               # M4
var stage: StageKit                # M4
```

In **M0 the members are façade objects whose every method is a one-line
delegate to the existing main method** (`fx.sparkle(pos, col)` →
`m._sparkle_burst(pos, col)`). Call sites migrate mechanically over M1–M3;
the real implementations replace the delegate bodies in M4; main's
originals become shims (§6) and are deleted after their window. At no point
does behavior change.

| Service | Absorbs (from main, M4) | Retires |
|---|---|---|
| `objective` | `_set_objective`, `_say` routing, the golden pointer, the picture card | text-only objectives become impossible — voice + pointer + card are one call, so the non-reader rule holds by construction |
| `fx` | `_sparkle_burst`, celebration bursts, contact shadows | per-call node/mesh/material allocation (`MA-PERF-002`): cached mesh + per-color materials, bounded pooled node ring, Speedy-tier count reduction |
| `reward` | `_reward`, medal awards, save-write triggers | scattered reward writes; the funnel becomes an object with one door |
| `input` | the composite touch/stick/pad/key read | the re-implemented input reads (`MA-CODE-002`) |
| `stage` | `_l2_box`, `_castle_mat`, `_up_mat`, `_soft_mat`, `_wall_solid`, `_cyl_solid` | the inverted dependency: 289 cross-module calls into the six main-side private builders (the six `m._…(` builder calls counted over `scripts/**/*.gd` minus `main.gd`, re-measured 2026-09-03; the 2026-09-01 figure of 422 also counted the frozen `backups/` copies) |

### 4.6 The adapters (M3)

`ArenaModeAdapter extends GameMode`: wraps one `games/*` satellite behind
the doorway without touching the satellite. `enter` performs what the
game's `_enter_arena` branch does today (arena build + satellite
`build(cfg)`); `tick` calls the body that lives in main's `_tick_game`
branch for that game (moved verbatim into the adapter); `end` routes
through the existing `_end_game` semantics via `ctx`. The satellite's
`m.g` scratch usage is **left exactly as-is** until M5 — adapters bridge,
they do not modernize. `CanvasModeAdapter` does the same for the K2 kit
(`picture_games`, `dance_engine`) around its `_mg2d_*` lifecycle.

### 4.7 Probe compatibility — a binding transition contract

Probes drive modes through today's entry points (`_start_dungeon_now`,
`_start_game(...)`, `_skip_intro`, direct `g` reads). Therefore:

1. **No entry point is deleted during migration.** Each migrated mode's
   old `_start_X_now`/`_end_X` become one-line shims delegating to the
   director (§6). Probe transcripts must be byte-stable across the
   migration commit.
2. `probe_surface()` is **additive**: probes MAY adopt it; existing `g` and
   field reads keep working until the mode's M5 state migration, which
   updates the mode's probes in the same commit.
3. `probe_mode_platform` (new, trusted, M0) owns the platform's own
   contract: registers a synthetic throwaway mode at runtime (the registry
   gains no row for it — the probe injects a test row through a
   probe-only, headless-guarded path, the same pattern as
   `living_probe_stage_override`), drives enter → tick → leave_neutral and
   enter → end(false)/end(true), asserts zero reward on the negative legs,
   clean teardown (node count returns to baseline), and music/HUD/player
   restoration.

## 5. Where everything goes — the mapping

| Today | Target home | Step | What dissolves |
|---|---|---|---|
| `_start_X_now` / `_end_X` × 7+ | ModeDirector + registry rows; originals become shims | M1–M2 | the scaffold clone family (after shim windows close) |
| `_enter_arena` switch, `_tick_game` dispatch, `_process` mode branches | `director.tick()` → adapters | M3 | ~530 lines of dispatch on main (`_process` 386, `_enter_arena` 117, `_tick_game` 30 at the 2026-09-01 re-audit) |
| pause-menu per-mode Leave branches | `director.leave_neutral()` | M1–M3 | one branch list |
| six builder helpers + 289 `m._` builder calls | `services.stage` (StageKit) | M4 | the inverted dependency |
| `_sparkle_burst` + celebration copies | `services.fx`, pooled + tiered | M4 | `MA-PERF-002` |
| `_set_objective` / HUD strings / pointer | `services.objective` | M4 | text-without-voice gaps |
| `day_one_*` glue (~30 funcs), venue + start-menu routing | Day One modes + registry rows | M6 | the newest accretion |
| `g["…"]` ephemeral keys | typed state per migrated mode | M5 | silent-typo state |
| `opera_gesture_surface.gd` decomposition | per-career modules behind its dispatcher (WP-B2) | parallel | orthogonal to the platform |
| reef/world builders on main | per-zone builders on the true-2D schedule | `MA-2D-002` | unchanged plan |

### 5.6 Typed mode state — the end of the scratch dictionary

- **Durable** (anything the child would miss after an app kill): main's
  save-backed fields, written through `services.reward`/`save_state`,
  append-only keys. Unchanged.
- **Ephemeral** (timers, positions, phase counters): typed `var`s on the
  mode instance — created at `enter`, dead at teardown. Already how every
  standalone node behaves; becomes the rule for migrated modes at M5.
- The `g` dictionary is **frozen at its M0-measured count** (`MA-CODE-004`: 409 at `9a1754c1`, 413 at the 2026-09-01 re-audit) from M0 and
  shrinks per migrated mode; the ratchet watches the count. `mg` follows
  when the K2 kit migrates.

## 6. Reversibility — every step has a cheap way back

Reversibility is a design input here, not an afterthought, and it reuses
the program's existing machinery:

1. **Shim windows instead of deletions.** A migrated mode's old entry
   functions are replaced by one-line delegating shims
   (`func _start_dungeon_now() -> void: mode_director.start("dungeon")`),
   kept for **one full dev→master promotion cycle** after the mode
   migrates. Un-migrating a mode is therefore local: restore the shim's
   recorded body and delete its registry row — no cross-file surgery, no
   probe edits. Shim deletion is its own later cleanup commit (with
   probe-callsite updates) and its own revert unit. This mirrors the
   repo's standing "attic'd, not deleted, one promotion cycle later" rule.
2. **One behavior-identical branch per step** (§10): because every M-step
   preserves behavior exactly, `git revert` of the step's merge commit is
   always safe and always sufficient; no step may mix platform migration
   with a behavior change that would make its revert ambiguous.
3. **A `CHG-*` ledger entry per landed step.** Each M-step that merges to
   dev appends the next unused `CHG` ID to
   `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` with the exact
   commit, path delta, risk notes, and the guarded inverse (the revert
   command plus the shim-restoration note), per that ledger's own
   maintenance rule. Stage A packages do the same. Rollback never bypasses
   protected-asset, save, security, or medium rules.
4. **Registry rows are independently removable.** Because a row is data,
   disabling one mode's platform routing (while its shim window is open)
   is a two-line change: delete the row, restore the shim body.
5. **The ratchet is history-preserving.** `tools/structure_budget.json`
   carries an append-only history of every budget change with commit and
   reason, so the structural trajectory is auditable and any budget change
   is attributable and individually revertible.
6. **The platform itself is removable until M3.** M0 is pure addition;
   through M2 the old dispatch still exists behind shims, so reverting the
   entire platform is: revert the step merges in reverse order. After M3
   (dispatch dissolved) reversal is per-step rather than wholesale — the
   ledger entries carry that boundary explicitly.

## 7. Enforcement — the structure ratchet

**`tools/audit_structure.py`** (stdlib Python, seconds, fail-closed once
armed) reading **`tools/structure_budget.json`**:

```json
{
	"budgets": {
		"main_gd_lines": 10499,
		"file_line_ceiling": 3000,
		"distinct_g_keys": 409,
		"main_private_cross_calls": 0
	},
	"ceiling_exempt": [
		{"path": "scripts/opera_gesture_surface.gd", "plan": "WP-B2", "until": "2026-10-01"}
	],
	"waivers": [],
	"history": [
		{"date": "2026-08-30", "commit": "<M0 commit>", "field": "main_gd_lines", "from": null, "to": 10499, "reason": "baseline"}
	]
}
```

Budgets are MEASURED at the M0 commit — the values above are `9a1754c1`-era illustrations, not the seed. At the 2026-09-01 re-audit the seed would be `main_gd_lines` 10,927, `distinct_g_keys` 413, and check 4's report-only baseline 846; and `ceiling_exempt` must be seeded from measurement too, because four non-probe files already exceed 3,000 lines — `opera_gesture_surface.gd` 6,185 (WP-B2), `arena/castle_rooms_25d.gd` 4,881, `opera_career_world_2d.gd` 3,433, `kart.gd` 3,324 — each entering with a plan reference and expiry or a `# DECOMPOSITION_PLAN:` header, or check 2 fails the moment it arms.

Checks (each printed as a `STRUCTURE|` line; exit 1 on any FAIL once armed):

1. `scripts/main.gd` line count ≤ `main_gd_lines`.
2. Every non-probe `scripts/**.gd` ≤ `file_line_ceiling` (probes are `MA-CI-007`'s domain) unless listed in
   `ceiling_exempt` with a plan reference and an expiry, or carrying a
   `# DECOMPOSITION_PLAN:` header naming its intended modules
   (`DL-CODE-02`).
3. Distinct `g["…"]` key count (the audited grep, exact) ≤
   `distinct_g_keys`.
4. Cross-module calls matching `m._[a-z_]+(` from non-main scripts ≤
   `main_private_cross_calls` **once M4 completes**; before M4 the check
   is report-only with the measured baseline.
5. Every `ModeRegistry.MODES` row: only the fixed key set, `script` path
   exists, `probe` value appears in BOTH trusted rosters.
6. **Budgets only decrease** (`main_private_cross_calls` may be set once
   at its M4 baseline): the history array must show monotone non-increase
   per field; an increase is legal only through a `waivers` entry naming
   the finding, reason, owner acknowledgement, and expiry (`DL-QA-08`
   shape). An expired waiver is a FAIL.

Arming schedule: report-only at M0 → blocking in `scripts/ci.sh` at M2 →
blocking in `.github/workflows/probes.yml` at M6 (a workflow edit under the
explicit-task boundary discipline). `DL-CODE-12` makes weakening or
removing the armed gate an audit finding, not a cleanup.

## 8. Agent assignment — Luna does the work, review is independent

Owner direction 2026-08-30: most of the actual implementation work is
carried by **Luna agents** — and the owner reaches them only through
single-prompt orchestrated runs: **one kickoff prompt per stage; the
orchestrator (Codex) divides the packages across its own Luna agents and
holds the lane rules internally.** The owner has no per-agent access, so a
"lane" below names a role inside a run, not a separately addressed agent,
and every guardrail in this section must therefore be carried by the
kickoff prompt itself. The platform contract was already written
agent-neutral; this section makes the division of labor and its guardrails
explicit, because the failure mode of parallel agents is already in this
repo's history — concurrent edits to the shared governance files produced
exactly the merge reconciliation the 2026-08-30 integration had to
perform.

**Roles:**

| Lane (a role inside a run) | Who | Owns |
|---|---|---|
| Implementation | **Luna agents** the orchestrator spawns, one package per agent, one `codex/`- or `luna/`-prefixed branch per package off fresh `origin/dev` | The package's code and probes, its package report, its `CHG` inverse notes — nothing else |
| Integration | the orchestrator's single closing phase (serial, after its implementation agents finish) or the owner's next run | Merging green packages, resolving cross-package drift, appending `CHG` entries and ledger rows — governance files edited once per run, serially |
| Re-audit (Stage R) | a distinct agent inside the run that implemented **none** of the packages it reviews, or a dedicated follow-up run | Spec-conformance verification (§9) and all lifecycle transitions, applied on the governance branch `claude/master-audit-game-analysis-qiko9l` (master audit §3.2, owner instruction 2026-08-30) |
| Owner | the human | One kickoff prompt per stage; the §11 review points, waivers, promotions; judging what a run hands back |

**The single-writer rule (binding):** implementation agents do **not**
edit the governance files — `audit/MASTER_AUDIT_2026-08-09.md`,
`audit/findings/ACTIVE_FINDINGS_2026-08-13.md`,
`audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`,
`design/05_DOC_LEDGER.md`, and this document. They deliver a package
report (handoff reporting format) in their branch/PR description; the
run's closing integration phase applies the ledger rows and `CHG` entries
once, serially, and only the re-audit role applies lifecycle transitions.
This removes the governance-file merge-conflict class entirely and keeps
the doc-authority gate's history linear.

**Parallelism map — and the run boundaries the owner's prompts draw:** one
stage per kickoff prompt, never the whole round in one run. Stage A is six
independent packages — the orchestrator may run them on six agents
concurrently (A3 touches a workflow and lands as its own branch, never
batched). Stage C is a strict spine — C0 through C6 in order, one agent at
a time, never concurrent with each other; a C run's prompt names exactly
which steps it may cover. Stage B packages parallelize behind their stated
dependencies. Stage R runs at each stage boundary, inside the run (distinct
agent) or as its own follow-up run when the owner wants stronger
independence.

**What any agent must satisfy** is unchanged and non-negotiable: the
handoff's Stage 0 review-first pass, the section-9 repair protocol, suite
green at every head, the escalation triggers, and the reversibility
requirements of §6. An agent that cannot run the full local suite does not
merge; it hands its branch to the integration lane.

## 9. Stage R — the implementation re-audit

No implementation is complete on its author's word. After each stage
boundary, an independent re-audit confirms every merged package against
its spec before any finding advances:

**Protocol, per package:**

1. Re-read the package's Do / Gate / Non-goals in the handoff and the
   relevant sections of this document; re-read the finding's canonical
   record acceptance field.
2. Verify the gate **by re-execution**, not by reading the report: re-run
   the named probes and checks at the merged head; re-measure the metric
   the gate names; for A1, re-run the deliberate-break demonstration on a
   throwaway branch; for ratchet-touching steps, run
   `tools/audit_structure.py` and diff its `STRUCTURE|` output against the
   package report.
3. Verify the non-goals: diff review confirming nothing outside the scope
   boundary moved.
4. Verify reversibility: the `CHG` entry exists, its inverse is coherent
   (for a shim-window step, the shim exists and the recorded body matches
   the pre-migration original), and the budget history rows are present.
5. **Then and only then** apply the lifecycle transition
   (`CONFIRMED_OPEN` → `FIXED_PENDING_VERIFICATION`, or
   `FIXED_PENDING_VERIFICATION` → `VERIFIED_FIXED` where every required
   verification level in the record is now present) in both the section-5
   index and the canonical record, and run the doc-authority tool to
   `ALL OK`.
6. A package that fails re-audit gets a dated failure note in the finding
   history and goes back to the implementation lane; its lifecycle does
   not move.

**Checkpoints:** WP-R1 after Stage A merges; WP-R2 after C2 (the platform
pattern proven); WP-R3 after C6 + remaining B packages, which also runs
§9.1 and re-measures the round's standing metrics table.

### 9.1 The growth-law acceptance test

On a throwaway branch at the current head: add a trivial hidden test mode
as exactly one new mode script plus one registry row. The diff must show
`main.gd` untouched, and `probe_mode_platform` must drive the mode through
enter/tick/leave with zero reward. Repeated at every future master-audit
round. If it fails, `DL-CODE-11` is regressed and the round reopens
`MA-CODE-001`.

## 10. Migration plan — M0 through M6

One step per branch, full suite green at every head, behavior identical.
Each step lands with its `CHG` entry and inverse (§6.3). Order proves the
pattern on the cheapest real mode before anything load-bearing moves.

| Step | Work | Proof gate | Reverse path |
|---|---|---|---|
| **M0 — skeleton** | `scripts/platform/` files per §4 with delegate-only Services; ratchet + budget file, report-only; trusted `probe_mode_platform` in BOTH rosters. Pure addition. | Suite green; new probe green three consecutive local runs; `STRUCTURE\|` baselines printed | revert the branch merge |
| **M1 — pilot: dungeon** | Route dungeon through the director; `_start_dungeon_now`/`_end_dungeon` become shims; its pause-Leave branch collapses. | `probe_dungeon` + suite green; transcripts byte-stable; `main.gd` net negative | restore shim bodies (recorded in the CHG entry) + delete the row |
| **M2 — standalone family** | kart, galaxy, combat, stuffie battle, ember, opera entry — one mode per commit, shims per mode; ratchet arms in `ci.sh`. | per-mode probes + suite green per commit; scaffold bodies live only in shims | per-mode shim restore |
| **M3 — arena family** | `ArenaModeAdapter`/`CanvasModeAdapter` wrap the `games/*` satellites and the K2 kit; `_enter_arena` switch and `_process` branches dissolve into shims/director. | `probe_audit`, per-game probes, `probe_passive` + suite green; `_process` under 100 lines | adapter rows removable per game; dispatch shim restore |
| **M4 — services** | Real ObjectiveService, FxService (pooled, tiered), RewardService, GameInput, StageKit replace the delegate bodies; call sites migrate; main originals become shims. | suite green per commit; `m._` cross-call baseline recorded then ratcheted; FX allocation grep clean; both-tier visual spot-check | per-service delegate restore |
| **M5 — typed state** | Two pilot modes swap `g["…"]` ephemeral keys for typed state; their probes updated in the same commits; the rule applies to every later-migrated mode. | pilot probes + suite green; g-key budget ratchets down | revert pilot commits |
| **M6 — finale** | Day One, venue, and start-menu glue become modes/rows (shim windows apply); ratchet blocks in `probes.yml`; budgets set to the measured floor. | Day One/start-menu probes + suite green; `main.gd` ≤ 9,000 at package end; §9.1 passes | shim restore per glue family |

Shim-deletion cleanups (closing each window after its promotion cycle) are
separate small commits with probe-callsite updates, each individually
revertible.

## 11. Owner review points

Reserved for explicit confirmation; the recommended default ships unless
overruled:

1. **Ephemeral-state law** (§5.6): mode instances own their dying state —
   the codified version of what standalone nodes already do. The Phase-7
   mold stays binding for RefCounted satellites.
2. **Services as owned objects, not autoloads.** Autoloads were rejected:
   probes instantiate `main.tscn` fresh per run, and global singletons
   would leak state across the probe isolation this repo fought to
   establish.
3. **Ratchet numbers, the waiver mechanism, and the shim-window length**
   (one promotion cycle) in §6–§7.
4. **Registry as `const` script** rather than a JSON resource:
   analyzer-checked, typo-safe, diff-reviewable.
5. **The agent-assignment model** (§8): Luna agents on implementation,
   single-writer governance, independent Stage R review — confirm or
   reassign lanes.
6. **`@abstract` on the contract's identity method** (engine 4.5 feature;
   `ENGINE_ADOPTION_4_7_2026-08-30.md` Tier 1): marking
   `GameMode.mode_id()` abstract turns a mis-declared mode into a
   load-time error instead of a silent registry miss. The lifecycle
   methods stay concrete no-ops by design. Recommended: adopt at M0.

---

The platform makes the MiniGame contract's own sentence physically true in
code: *what is identical across games is not the simulation but the
plumbing.* After M6, the plumbing exists once, growth lands in mode files
and registry rows, every step of the road there has a recorded way back,
an independent re-audit confirms each step met its spec, and the
coordinator's size is governed by a gate instead of good intentions.
