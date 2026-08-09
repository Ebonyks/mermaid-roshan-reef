# RELEASE GATE — codex/opera-art-regeneration

## 1. VERDICT

**DO-NOT-PROMOTE.**

Two of the three grammars this branch introduces can put the child in a state she cannot get out of, and the branch's marquee content (the detective crown hunt) is unreachable on a real playthrough. All four auditors are reporting on a genuinely 12-file branch — the "deleted the combat wing" alarm in the two-dot diff is an artifact of a stale base and is **not** a defect (blast-radius, contract and merge-safety all independently confirmed this; I concur).

I spot-checked the two most severe claims by reading the files. **Both are real, and one is worse than reported.**

---

## 2. BLOCKERS

### B1 — Pipe puzzle has one-move unrecoverable dead ends, with no undo and no reset
`scripts/opera_gesture_surface.gd:1222` (`var fueled := cell in _pipe_flow_cells()` gating liftability), `:1143-1150` (edge/imp = "blocked", never "back up"), `:205` + `:1174-1175` (`_pipe_setup_round()` only on configure and after a *won* round).

**I verified this by hand, not by trusting the auditor.** Both kills reproduce exactly:

- **Round 2** (`PIPE_ROUNDS[1]`, `:81`): entry cell 4 is fixed `NW`; mouths are `(0,-1)`/`(-1,0)`, in_dir `(1,0)`, so out_dir resolves to `(0,-1)` — fuel goes **up into cell 0**. Tray contains `SW` (mouths down+left). `SW` in cell 0 accepts from below → cell 0 joins `pipe_flow` → `fueled == true` → the `not fueled` guard at `:1222` makes it permanently un-liftable. Its out_dir is `(-1,0)` → col `-1` → `_pipe_next_step()` returns `[]` forever. **Round dead.** `SW` is the round's spare/distractor tile, so this is a natural first move.
- **Round 3** (`PIPE_ROUNDS[2]`, `:82`): fixed `H` at cell 4 → fuel exits right into cell 5. Tray's `H` in cell 5 accepts, then points at cell 6 = `"IMP"`, which is not in `PIPE_MOUTHS` → blocked. Cell 5 fueled → un-liftable. **Round dead.** This is the single most obvious move on the board.

There is no reset, no undo, and I confirmed there is **no global stuck-child escape**: the only idle response is a 9 s repeating voice hint (`opera_career_world_2d.gd:2079-2083`), and any imp tap resets `idle_t` (`:1302`). The sole exit is tapping the sleeping imp — `gesture.emit("pipe", 0.0, 0.6)` → `gain = maxf(0.04, 0.0)` (`opera_career_world_2d.gd:1321`) against the astronaut PIPES goal of `3.0` (`:126`) = **75 taps** with zero feedback that it is doing anything. And `_pipe_hint_cell()` (`:1259-1280`) has no imp/edge test, so in the round-3 case it pulses the gold "put a tile here" twinkle **on the napping imp, forever**.

Why it matters: this is a 4-year-old, alone, on a beat with no exit. Minimum fix: allow lifting a fueled tile (truncate `pipe_flow` at that cell), or add a reset when `pipe_wait_t` exceeds the hint window.

### B2 — Pipe tray: the one-finger placement path is dead, and every tap duplicates a tile off-screen
`scripts/opera_gesture_surface.gd:1205-1212`, `:1241-1256`, `:1110`.

Verified against the input router (`_gui_input` `:539-556` → `_press`/`_release` on the same tap). A tap on a tray slot sets `pipe_drag_tile`/`pipe_tray_sel` **without removing the tile**; `_release` then fires at the same point, `_pipe_cell_at` returns `-1` (the tray sits below the grid), `pipe_drag_from` is `-1`, so control reaches `else: pipe_tray.append(pipe_drag_tile)` and clears `pipe_tray_sel`. Consequences:

- The advertised tap-tile-then-tap-cell path (`:1231-1238`) can **never** fire — the release always clears the selection first. The only working placement is a sustained ~400 px drag, which is not a one-finger contract for this child.
- **`:1231-1238` is the only code in the file that ever removes from `pipe_tray`, and it is unreachable.** Therefore `pipe_tray` is monotonically non-decreasing across every interaction — including successful drag-places (`:1245-1248` never removes). It is an infinite dispenser.
- `_pipe_tray_rect` is `x = 120 + slot*104` (`:1110`) on an 852 px surface with no `clip_contents`. Slot 7 already spans 848–940. A mashing child grows an ever-lengthening row of untouchable tiles running off the surface and across the stage.

### B3 — Detective's guided retry amputates 6 of 10 phases and hands her a widget the act doesn't contain
`scripts/opera_career_world_2d.gd:160` (`"detective": 9`), `:2111` (`phase_index = _finale_start()`), `:1503`, `:2103-2109`, `:2117`.

Verified the tables directly. Detective's `PHASES` entry has **10 phases**, modes: `bop, talk, lens, bop, talk, lens, talk, lens, bop, bop` — **there is no `choice` phase anywhere in the career**, and index 9 is `TEAM CORNER`, `mode: "bop"`, `combat {count: 4, captain: true}`. Two failures compound:

- `competition_progress()` returns a hard `0.0` for any `phase_index < _finale_start()` (`:1244-1246`), so the rival's wall-clock progress is unopposed until phase 9. The three `talk` beats alone hold 16.6 s (`:49-51, 54-56, 58-60`), every phase now holds 2.2 s on completion (`:1361`), and the rival fires at ~43 s. She is teleported from roughly CLOCK/TRAIL TRICK straight to phase 9, silently skipping ASK ROSALINA, FOUNTAIN, ASK CHUCK, STAIRS and the CROWN CHASE climax — the majority of what commit `811a00a9` exists to add.
- `begin_guided_retry()` hard-codes `surface.configure("choice", ...)` and holds `target_choice` for 3.6 s as "the ACTUAL answer." Since detective has no `choice` phase, the child watches a three-lane answer widget belonging to nothing, hears "solve the same mystery with the sparkle memory," and is dropped into a captain fight. `phase_progress = 2.0` (`:2117`) additionally pre-credits 2 of 6 bop hits she never landed.

No save corruption (the star still awards), but the branch's headline content does not ship.

### B4 — Chef BAKE completes itself while she is still walking to the oven
`scripts/opera_gesture_surface.gd:340-353`; `scripts/opera_career_world_2d.gd:866-867`.

Verified: `_arm_phase` calls `_bind_widget` **before** the wander walk (`:864-867`), so `surface.configure("oven", ...)` starts the bake clock immediately even with `action_panel.visible = false`. `_process` runs `oven_t += delta/8.0`, then 1.2 s grace, then `gesture.emit("oven", 999.0, 0.7)` with **no touch at all**. In `_on_gesture` that opens the card by itself and `gain = maxf(0.04, 999.0)` blasts past the goal of 6.0. A child who dawdles 9.2 s in the wander layer — a layer that exists to encourage dawdling — never gets to bake the cake. Oven is the only mode whose surface emits without input.

### B5 — Opera kart race never sets `m.game = "kart"`
`scripts/opera_career_world_2d.gd:2232-2254`; guard at `scripts/main.gd:7020`.

Verified both sides: `_start_kart_race()` sets `race_active`, `root.visible`, `m.kart_completion_committed` and builds the `KartGame`, but never assigns `m.game` or `m.kart_game`. `main.gd:7020 if game == "kart": ... return` is the suspension guard, so the entire reef/lagoon simulation ticks every frame underneath a full 3D kart race plus the opera CanvasLayer — the heaviest frame in the game, at the one place the codebase explicitly optimised for. Secondary: the action label falls through to `game == "opera"` (`main.gd:7223`), so the only button that fires turbo shows `SPARKLE`/`DANCE` to a non-reader for the whole race.

Also fix the ordering while you are in there: `race_active = true` / `root.visible = false` (`:2232-2233`) are set **before** the kart is constructed (`:2240-2254`). Any failure in between leaves the child on a blank, permanently unresponsive screen with no recovery. Set them after `start()` is issued.

### B6 — Do not fast-forward, and do not trust this branch's recorded green
Merge-safety proved zero conflicts (`git merge-tree` exit 0, one auto-merge in `scripts/audio_director.gd`, disjoint hunks). But the branch is 29 behind and its `scripts/ci.sh:58` predates the combat wing and castle V4. **This must land as a real merge, and promotion must be gated on a fresh full `probes.yml` run on the merged commit**, not on the branch's own result. A fast-forward or two-dot diff-apply would delete the combat SFX pack, `combat_tutorial.gd`, `partner_assist.gd`, and 88 castle V3 files.

---

## 3. NON-BLOCKING (fix after)

- **Talk beats swallow every touch.** `opera_career_world_2d.gd:917-927` shows `wander_layer` at `MOUSE_FILTER_STOP`, but `_wander_input` returns immediately when `task_open` (`:2142`). Detective spends 16.6 s across three beats on a fully inert screen. Advances on its own timer, so not a lock — but it is the worst-feeling minute in the branch.
- **Wander stations at 157–237 px (farmer FEED/PICNIC, painter FILL).** Real, but **not** the hard block the no-fail audit calls it: `_wander_input:2170-2172` sets `wander_dest = station_pos` **unclamped**, bypassing `_stage_feet_at_x`. A tap within 120 px of the marker foot walks her exactly onto the station and opens the task. Only the top ~third of the 96×192 marker art misses, and a retry lands. Degraded discoverability, not a dead end.
- **The 20 s glide assist is a no-op** (`:2072-2076`): `_glide_roshan_to` never writes `wander_feet`, which is what `:2211` reads; and `_set_glide_rotation` trips the settle branch at `:2200-2208`, re-banking the old rest every frame. Harmless now that the marker tap works, but it is dead safety-net code.
- **Echo star hit circles overlap** (`opera_gesture_surface.gd:1400-1407`): 109.8 px spacing against a 74 px radius, first-match wins, so a tap visually nearer the right star resolves to the left. Cost of the code's ambiguity is a full verse replay.
- **Mashing stalls the oven** (`:341-343`, `:443`): taps below 45 % heat hold `oven_peek`, freezing `oven_t`. Faster than ~1.4 Hz keeps the cake permanently under the ready band.
- **`kart.gd:2327, 2351, 2364`** print English at a non-reader on the `minimal_hud` path, defeating the flag's stated purpose.
- **Kart environment leak** (`opera_career_world_2d.gd:2124-2127` `queue_free()` bypassing `KartGame._teardown()`). I agree with both auditors that it is **latent** — no reachable mid-race exit today. One line (`kart_node._teardown(-1)`) closes it; do it before anyone adds a back button.
- **Racer's stated 2D safety fallback does not exist** (`:2226-2231` comment vs `:943` hiding the panel). Unreachable on the tablet, but the comment is a lie that will mislead the next agent.
- **Eight widget textures missing** (`opera_gesture_surface.gd:213-220`). Verified safe: `_load_widget_texture` gates on `ResourceLoader.exists` and both consumers have real vector fallbacks. Ship-with-programmer-art is a choice, not a bug.
- **Ledger row `assets_src/concepts/OPERA_LOGICAL_REBUILD_LEDGER_2026-08-04.csv:29-30`** points future audio work at `assets/audio/voices/`, a house-rule protected directory. Amend the rows.

---

## 4. WHAT THE AUDITORS MISSED

1. **The worktree is not clean right now.** Merge-safety reported `git status --porcelain --untracked-files=all` as empty; as of my check there is an untracked `scripts/probe_opera_2d_audit.gd`. Almost certainly an audit artifact, but **do not `git add -A` before merging** — an unreviewed probe would land silently.

2. **`pipe_tray` can only ever grow.** The auditors caught the duplication symptom; none noticed that `:1231-1238` is the *only* `pipe_tray.remove_at` in the file and it is unreachable, which means the documented "tray = needed tiles + at most one" invariant is not merely violated on mashing — it never holds at all, on any interaction, from the first tile placed.

3. **Zero probe coverage for the pipe grammar.** `grep` across all probes: the only occurrence of "pipe" in `probe_opera_2d.gd` is a comment at `:363`. No probe places a tile, so neither B1 nor B2 could ever have been caught. Every probe drives beats through `_show_phase()` (`:795-799` = `_arm_phase` + `_open_task` in one synchronous step), which also skips wander entirely and has no wall clock — so B3, B4 and the wander findings are all structurally invisible to CI. **A probe that exercises pipe placement should be a merge condition, not a follow-up.**

4. **The no-fail audit overstates the wander stations as "STUCK."** The unclamped marker-tap branch at `:2170-2172` is a working escape. Correcting this matters, because fixing a non-bug at the expense of the geometry would be wasted work — the real fix is marker hit-area, not station placement.

5. **Blast-radius's Finding 3 (dialogue queue draining into the lagoon) is real and the cheapest fix on this list.** `clear_dialogue()` and `skip_dialogue()` have zero callers anywhere in `scripts/`, and `tick_dialogue` runs above every `game` early-return. One line — `m.clear_dialogue()` in `OperaCareerWorld2D.close()` — closes it. Bundle it with the B-list.
