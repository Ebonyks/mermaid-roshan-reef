# Master design — target architecture: the Mode Platform

- **Document ID:** `TA-2026-08-26`
- **Status:** `BINDING_DOMAIN` for game-code structure, produced on direct
  owner request 2026-08-26 ("develop comprehensive remodeling of game code to
  address flaws… architecture change to facilitate continued expansion with
  no increase of this file"). Section 9 lists the specific design decisions
  reserved for explicit owner confirmation; everything else binds as each
  migration step lands green.
- **Subordinate to:** `SECURITY.md`, the save/protected-content/workflow
  rules, direct owner decisions, and
  `06_COMPREHENSIVE_DESIGN_LANGUAGE.md`. `03_TECHNICAL_ARCHITECTURE.md`
  describes what the code **is**; this document specifies what it
  **becomes** and the law that keeps it there.
- **Companions:** analysis and evidence in
  `../audit/MASTER_AUDIT_2026-08-26.md`; execution packages in
  `../CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` (Stage C);
  rules `DL-CODE-01`–`DL-CODE-12`.
- **What this is not:** not a rewrite authorization. Every step below is a
  mechanical, behavior-preserving move under `DL-CODE-06`, gated by the
  trusted suite, reachable one branch at a time. It is also not a universal
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
| Mode start/stop | a hand-copied `_start_X_now` / `_end_X` pair per mode (`_start_kart_game_now`, `_start_galaxy_now`, `_start_combat`, `_start_dungeon_now`, `_start_opera_now`, …) — the same music-save / `game = id` / HUD-off / hide-player / instantiate / `finish_cb` sequence seven-plus times | ~30 lines on main |
| Tick dispatch | the ~300-line `_process` and the `_enter_arena` switch route by string id | edits to both |
| Interaction/touch registration | `_populate_touch_interactables` and friends on main | edits on main |
| Cross-cutting services | `_say`, `_set_objective`, `_sparkle_burst`, `_reward`, `_write_save`, and six builder helpers are **private methods of main**, called ~6,400 times from satellites as `m._…` | main can never shrink below the sum of its services |
| Ephemeral state | the `g` scratch dictionary (409 distinct string keys) plus main-side fields | new keys, new fields |

The audit history proves the consequence: the shrink program ran for six
weeks under a standing target and still lost ground (8,239 → 10,499 lines),
because every shrink was a one-off extraction while every new feature paid
the five seams again. `MA-CODE-001` and `MA-CODE-002` are the ledger of that
arithmetic. Shrinking harder is not the fix. **Changing where growth lands
is.**

## 1. The growth law

> **Adding an activity, wing, or zone touches `main.gd` zero times.**
> A new mode is: one mode script (plus its art and its probe) and one
> registry row. Dispatch, teardown, music hand-off, HUD hand-off, pause
> Leave, save wiring, touch registration, and the probe surface are platform
> plumbing that exists exactly once.

This is the property the owner asked for, it is testable (§8), and it is
enforced by a ratchet gate (§6) so it cannot silently regress the way the
line-count target did. Everything else in this document exists to make this
law true mechanically.

## 2. What stays true

- **One contract, few engines.** The MiniGame contract (03 §2) already names
  the six planks every game shares — lifecycle, GameInput, reward funnel,
  mercy hooks, voice+pointer, probe surface. Today those planks are prose
  plus copy-paste; the platform turns them into runtime objects. The K2
  Canvas kit, HitEngine, StorybookUI, camera composition, and every per-mode
  simulation remain exactly what they are.
- **The Phase-7 satellite mold is unchanged** for RefCounted satellites:
  logic only, durable state on main, teardown-owned nodes, a probe.
- **Standalone mode nodes already own their ephemeral state** (03 §1 lists
  them: `kart`, `galaxy`, `combat_arena`, `dungeon_level`, `stuffie_battle`,
  `ember_fortress`, `opera_*`). The platform generalizes that existing
  reality; it does not overturn the mold. The dividing line is sharpened in
  §4.5: *durable* progress lives on main/`save_state` through the reward
  funnel; *ephemeral* mode state lives on the mode instance and dies with
  it.
- **The save contract, no-fail rules, non-reader rules, true-2D migration,
  and owner decisions are untouched.** The platform is medium-neutral
  plumbing: a spatial legacy mode and a Canvas mode ride the same director
  while `MA-2D-002` converts their interiors on its own schedule.
- **Extract, don't rewrite.** Every migration step moves existing bodies
  behind a uniform doorway. No simulation is rewritten to fit the platform;
  a mode that fits badly keeps a thin adapter instead.

## 3. Target shape

```text
scenes/main.tscn
└── ReefMain — coordinator (steady-state target < 2,500 lines)
    ├── owns: save-backed fields · world root · shrinking legacy g/mg scratch
    ├── ModeDirector ──reads──> ModeRegistry (declarative, one row per mode)
    │     └── current GameMode instance
    │           ├── standalone node modes (dungeon, kart, galaxy, opera, …)
    │           ├── ArenaModeAdapter → games/* satellites (fetch, dolls, …)
    │           └── CanvasModeAdapter → K2 kit (picture games, dance)
    ├── Services — owned objects created in _ready(), passed by reference
    │     ├── objective   say + pointer + picture card in ONE call
    │     ├── fx          pooled bursts/celebrations, tier-aware
    │     ├── reward      the _reward funnel + medals + save writes
    │     ├── input       GameInput: the one composite one-finger read
    │     ├── stage       StageKit: the builder helpers main lends out today
    │     └── promoted existing satellites: audio_director, medal_system,
    │         interaction_director, camera_kit, storybook_ui, save_state
    └── world builders — per-zone, extracted on the true-2D schedule
```

Main keeps three jobs for good: **owning durable state**, **composing the
world root**, and **hosting the director and services**. It stops being the
place where mode plumbing accumulates.

## 4. The contracts

Interface sketches are normative in shape, not in exact spelling; the M0
branch fixes final signatures. All new files are typed GDScript with the
repo's tab/style rules.

### 4.1 `GameMode` — the uniform doorway

```gdscript
## scripts/platform/game_mode.gd — extends Node.
## The plumbing every activity presents to the ModeDirector.
## The simulation inside stays the mode's own business.
class_name GameMode
extends Node

var ctx: ModeContext                    # main, services, cfg, finish callable

func mode_id() -> String: return ""     # matches its ModeRegistry key
func enter(context: ModeContext) -> void: pass    # build; never touches HUD/music directly
func tick(delta: float) -> void: pass   # driven by the director, not by main._process branches
func leave_neutral() -> void: pass      # pause-menu Leave: never a loss, never a free win
func end(win: bool) -> void: pass       # completion; rewards ONLY via ctx.services.reward
func probe_surface() -> Dictionary: return {}     # analytic objective state for bots (DL-CODE-10)
func serialize() -> Dictionary: return {}         # durable fields only, additive keys (DL-SAVE-01)
func restore(data: Dictionary) -> void: pass
```

`ModeContext` is a small typed object: `main: ReefMain`,
`services: Services`, `cfg: Dictionary`, `finish: Callable`. Modes reach
services through it and **never** call `m._private_method()` — that habit is
what welded 6,400 call sites to main's internals.

### 4.2 `ModeRegistry` — data, not code

```gdscript
## scripts/platform/mode_registry.gd — const data. Adding a mode = adding a row.
const MODES := {
	"dungeon": {
		"script": "res://scripts/dungeon_level.gd",
		"family": "standalone",          # standalone | arena | canvas
		"music": "dungeon_ice",          # director saves/restores the prior cue
		"hide_player": true,
		"hud": false,
		"medal_id": "dungeon",
		"tier": "budget-note: room-local; no ambient over cap",   # DL-CODE-08
		"probe": "probe_dungeon",        # ratchet gate verifies roster membership
	},
	# … one row per mode
}
```

`castle_career_routes.gd` is the in-repo precedent — an immutable route
registry that already centralizes thirteen careers' identity without owning
their state. The ModeRegistry generalizes that proven pattern to every mode.
A `const` script (not JSON) is deliberate: typos fail the analyzer instead
of failing silently at runtime.

### 4.3 `ModeDirector` — the seven copies become one body

`start(id)` performs, once, the exact sequence every `_start_X_now` copy
performs today: guard against re-entry, save the current music cue and play
the row's, set `main.game = id`, apply the row's HUD/player visibility,
instantiate the row's script, call `enter(ctx)`. `end()` and
`leave_neutral()` perform the one teardown `_end_X` repeats: restore music,
restore HUD/player, null the handle, `_clear_game`-equivalent reclamation.
The pause menu's per-mode branch list collapses to one call:
`director.leave_neutral()`. Estimated size: ~150 lines, written once.

### 4.4 Services — main's lending library moves out

| Service | Absorbs (from main) | Retires |
|---|---|---|
| `objective` | `_set_objective`, `_say` routing, the golden pointer, the picture card | the possibility of a text-only objective — voice + pointer + card become one call, so rule `DL-AGE-01`/L2 holds by construction |
| `fx` | `_sparkle_burst`, celebration bursts, contact shadows | per-call node/mesh/material allocation (`MA-PERF-002`): pooled ring, cached materials, tier-aware counts |
| `reward` | `_reward`, medal awards, save-write triggers | scattered reward writes; the funnel becomes an object with one door |
| `input` | the composite touch/stick/pad/key read | the re-implemented input reads (`MA-CODE-002`, the old OW-8 debt) |
| `stage` | `_l2_box`, `_castle_mat`, `_up_mat`, `_soft_mat`, `_wall_solid`, `_cyl_solid` | the inverted dependency: ~280 cross-module calls into main-side private builders |

Migration is delegate-first: each main method becomes a two-line forward to
the service the day the service lands, call sites migrate mechanically over
following commits, then the delegate is deleted. At no point does behavior
change.

### 4.5 Typed mode state — the end of the scratch dictionary

The sharpened ownership line:

- **Durable** (anything the child would miss after an app kill): on main's
  save-backed fields, written through `services.reward`/`save_state`,
  append-only keys. Unchanged.
- **Ephemeral** (this round's timers, positions, phase counters): typed
  `var`s on the mode instance — created at `enter`, dead at `end`. This is
  already how every standalone node behaves; it becomes the rule for
  migrated modes.

The `g` dictionary is frozen at its audited baseline (409 keys,
`MA-CODE-004`) and shrinks per migrated mode; the ratchet gate watches the
count. `mg` follows the same path when the K2 kit migrates.

## 5. Where everything goes — the mapping

| Today | Target home | Step | What dissolves |
|---|---|---|---|
| `_start_X_now` / `_end_X` × 7+ | ModeDirector + registry rows | M1–M2 | the scaffold clone family |
| `_enter_arena` switch, `_tick_game` dispatch, `_process` mode branches | `director.tick()` → `mode.tick()` (arena family via `ArenaModeAdapter`) | M3 | ~400 lines of dispatch on main |
| pause-menu per-mode Leave branches | `GameMode.leave_neutral()` | M1–M3 | one branch list |
| six builder helpers + ~280 `m._` calls | `services.stage` (StageKit) | M4 | the inverted dependency |
| `_sparkle_burst` + celebration copies | `services.fx`, pooled + tiered | M4 (executes WP-B5) | `MA-PERF-002` |
| `_set_objective` / HUD strings / pointer | `services.objective` | M4 | text-without-voice gaps |
| `day_one_*` glue (~30 funcs), venue + start-menu routing | Day One modes + registry rows | M6 (executes WP-B1) | the newest accretion |
| `g["…"]` ephemeral keys | typed state on each migrated mode | M5 (executes WP-B4) | silent-typo state |
| `opera_gesture_surface.gd` 6,185 lines | per-career surface modules behind its dispatcher (WP-B2) | parallel | orthogonal to the platform; unchanged plan |
| reef/world builders on main | per-zone builders on the true-2D schedule | `MA-2D-002` | unchanged plan |

## 6. Enforcement — the structure ratchet

The line-count target failed because nothing failed when it was missed. The
remodel therefore ships with teeth: **`tools/audit_structure.py`** (stdlib
Python, seconds to run) reading **`tools/structure_budget.json`**.

Checks, all fail-closed once armed:

1. `scripts/main.gd` line count ≤ its budget.
2. No `.gd` file over 3,000 lines without a `# DECOMPOSITION_PLAN:` header
   naming its intended modules (`DL-CODE-02`).
3. Distinct `g["…"]` key count ≤ its budget.
4. Cross-module calls to underscore-private `ReefMain` methods ≤ budget.
5. Every `ModeRegistry` row names a probe present in a trusted roster.
6. **Budgets only decrease.** The JSON carries an append-only history; a
   budget may be lowered in the same commit as the extraction that earned
   it, and raised only by an explicit owner-visible waiver entry naming the
   finding, the reason, and an expiry (`DL-QA-08` shape).

Arming schedule: report-only at M0 (prints `STRUCTURE|` lines into the CI
log), blocking in `scripts/ci.sh` at M2, blocking in
`.github/workflows/probes.yml` at M6 — that last wire-up is a workflow edit
and follows the same explicit-task boundary discipline as WP-A3.
`DL-CODE-12` makes the ratchet a standing rule.

## 7. Migration plan — M0 through M6

One step per branch, full suite green at every head, behavior identical
unless a step says otherwise (none does). Order chosen so the pattern is
proven on the cheapest real mode before anything load-bearing moves.

| Step | Work | Proof gate |
|---|---|---|
| **M0 — skeleton** | Add `scripts/platform/` (GameMode, ModeContext, ModeRegistry, ModeDirector, Services façade whose members delegate to today's main methods). Add `tools/audit_structure.py` + budget file, report-only. Add trusted `probe_mode_platform`: registers a synthetic throwaway mode, enters, ticks, leaves neutrally, asserts no reward and clean teardown. Pure addition — zero existing lines change. | Suite green; new probe green three consecutive runs; gate prints baselines |
| **M1 — pilot** | Route **dungeon** (the cleanest 17-line glue) through the director; delete `_start_dungeon_now`/`_end_dungeon`; its pause-Leave branch collapses. | `probe_dungeon` + suite green; `main.gd` net negative; director handles guard/music/HUD identically (diff of probe transcripts) |
| **M2 — standalone family** | One mode per commit: kart, galaxy, combat, stuffie battle, ember, opera entry. Scaffold family fully dissolves. Ratchet arms in `ci.sh`. | Each mode's probes + suite green per commit; scaffold grep count reaches zero |
| **M3 — arena family** | `ArenaModeAdapter` wraps the existing `_start_game → _tick_game → _end_game` satellites (fetch, dolls, seek, melody, slide, treasure, shop, fairy, brawl) and the K2 canvas kit behind the same doorway; `_enter_arena` switch and `_process` mode branches dissolve. | `probe_audit`, per-game probes, `probe_passive` + suite green; `_process` under 100 lines |
| **M4 — services** | StageKit, ObjectiveService, FxService (pooled — executes WP-B5), RewardDirector object. Delegate-first, then call-site migration, then delegate deletion. | Suite green per commit; `m._` private-call budget ratchets down; FX pooling verified by allocation grep + visual spot-check both tiers |
| **M5 — typed state** | Two pilot modes swap `g["…"]` for typed state (executes WP-B4); rule applies to every subsequently migrated mode. | Pilot-mode probes + suite green; g-key budget ratchets down |
| **M6 — finale** | Day One, venue, and start-menu glue become modes/rows (executes WP-B1); ratchet blocks in `probes.yml`; budgets set at the measured post-migration floor; steady-state `main.gd` target < 2,500 tracked by decrement-per-extraction from there. | Day One/start-menu probes (gated by WP-A1) + suite green; the growth-law test in §8 passes |

Sizing: M0–M1 are each one focused branch; M2 and M3 are one-mode-per-commit
trains; M4 is the largest (three services, call-site sweeps); M5–M6 close.
Every step's rollback is `git revert` of a behavior-identical branch.

## 8. Acceptance — how we know the remodel worked

1. **The growth-law test, run for real:** on a throwaway branch, add a
   trivial hidden test mode (one file + one registry row). The diff must
   show `main.gd` untouched, and `probe_mode_platform` must drive it through
   enter/tick/leave with zero reward. This test is the definitive acceptance
   for §1 and gets repeated at every future audit round.
2. The ratchet is blocking end-to-end, budgets monotone, with zero waivers
   outstanding past expiry.
3. Scaffold, dispatch-switch, and builder-inversion counts are zero for
   migrated families (grep-verifiable).
4. The next master-audit round re-measures §4-of-the-round metrics and finds
   `main.gd` below its M6 floor with the trend line pointing down.
5. Nothing else moved: probe verdicts byte-stable across every migration
   commit, save files from before M0 load unchanged, and no invariant
   finding opened against the platform.

## 9. Owner review points

Reserved for explicit confirmation; the recommended default ships unless
overruled:

1. **Ephemeral-state law** (§4.5): confirm that mode instances own their
   dying state — the codified version of what standalone nodes already do.
   The Phase-7 mold stays binding for RefCounted satellites.
2. **Services as owned objects, not autoloads.** Recommended: owned objects
   on main. Autoloads were considered and rejected: probes instantiate
   `main.tscn` fresh per run and global singletons would leak state across
   probe boundaries the isolation work fought hard to close.
3. **Ratchet numbers and the waiver mechanism** (§6): initial budgets are
   the audited baselines; only the owner accepts a budget increase.
4. **Registry as `const` script** rather than a JSON resource (§4.2):
   analyzer-checked, typo-safe, diff-reviewable. JSON is the fallback if the
   owner prefers data files.

---

The platform makes the MiniGame contract's own sentence physically true in
code: *what is identical across games is not the simulation but the
plumbing.* After M6, the plumbing exists once, growth lands in mode files
and registry rows, and the coordinator's size is governed by a gate instead
of good intentions.
