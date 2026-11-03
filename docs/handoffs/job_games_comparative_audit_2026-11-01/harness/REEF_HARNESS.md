# Reef of Light Opera playthrough harness (`reef_play`)

Plays one of OUR 15 Opera careers end to end with a chosen input policy and writes measurable
logs (`run.json`) plus frames. Built for the comparative audit (RUBRIC.md, 10 runs per career).

Files
- `/home/claude/audit_work/harness/reef_play.sh`: wrapper (use this).
- `/home/claude/ebonyks/mermaid-roshan-reef/audit_local/reef_play.gd`: the SceneTree script
  (untracked folder; no repo file is edited).
- `/home/claude/audit_work/harness/verification/`: the verification runs quoted below.

## Usage

```
reef_play.sh CAREER POLICY SEED OUT_DIR [MODE] [MAX_SECONDS]
  CAREER       costume key or career name, case/space-insensitive:
               chef detective ballerina candymaker doctor farmer boxer magician painter
               astronaut racer popstar nursery geologist teacher
               (also "Pastry Chef", "Stuffie Surgeon", "Racecar Driver", "Pop Star",
                "Nursery Nurse", "Astronaut Engineer", "Candy Maker", ...)
  POLICY       expert | child_sim | slow | random_tapper | idle
  SEED         integer (drives the policy RNG and Godot's global RNG)
  OUT_DIR      created if missing; run.json, isolation.json, godot.log, frames/ are replaced
  MODE         fast (default) | rendered
  MAX_SECONDS  game-time cap (default 600); the run stops at the win or at this cap
Env: REEF_DISPLAY=56 (rendered mode; use YOUR display), REEF_INPUT=finger|touch_only,
     REEF_FPS=60 (fast mode tick), REEF_RENDER_FIXED_FPS=N (optional deterministic rendered run),
     REEF_DEBUG=1 (adds a surface state snapshot to every action event), REEF_KEEP_USERDIR=1.
```

Examples
```
H=/home/claude/audit_work/harness/reef_play.sh
$H boxer child_sim 3 /home/claude/audit_work/results/boxer/ours/child-sim-1 fast 600
REEF_DISPLAY=56 $H racer idle 1 /home/claude/audit_work/results/racer/ours/idle-1 rendered 90
# RUBRIC protocol for one career (fast; add rendered runs for the frames you cite):
for r in "expert 1" "expert 2" "child_sim 1" "child_sim 2" "child_sim 3" "child_sim 4" \
         "slow 1" "random_tapper 1" "idle 1"; do set -- $r; $H popstar $1 $2 out/popstar_$1_$2 fast 600; done
```
"replay-1" (second run after a completed one) is NOT a persistent replay: every run starts from a
fresh empty profile (see isolation). Use a second seed and compare; say so in findings.

Costs (2 CPUs, llvmpipe): fast mode = 15-40 s wall per completed career (game runs ~20-40x real
time); a stuck run costs ~4 s wall per 100 game s. Rendered = ~2x wall per game second (llvmpipe
runs below real time) plus ~10 s start-up; ~1.5 MB per PNG, ~45-65 MB per 90-150 s run.
One game instance at a time.

## Modes

- `fast`: `--headless --fixed-fps 60`. Game time is exact 1/60 s ticks, independent of wall time.
  No frames (headless has no renderer). Audio uses the Dummy driver; global
  `AudioServer.playback_speed_scale` is continuously set to the measured game/wall ratio so voice
  clips last their game-time length (approximate, +-0.25 s).
- `rendered`: real window on the Xvfb display (`--max-fps 30`), real-time deltas. PNG frames:
  `frames/f_<game seconds>_<tag>.png` with tags `tick` (every 3 s), `pNN_open_<phase>` (0.6 s
  after the activity opens), `pNN_done_<phase>` (0.15 s after completion), `finale` (2 s after the
  win). Each capture stalls the frame ~0.2 s (total in `frame_capture_ms_total`).
  Display builds open the title menu (CanvasLayer 20) over everything; the harness dismisses it
  with the menu's own `_dismiss_menu()` (headless never builds it).

## How inputs are delivered (the "finger")

Every input is an `InputEventScreenTouch` (down/up) or `InputEventScreenDrag` (move, ~30 Hz
samples with relative/velocity) passed to `Input.parse_input_event()` at window coordinates
(canvas point -> `CanvasItem.get_global_transform_with_canvas()` -> root screen transform).
This is the tablet path: viewport GUI hit-testing, Godot's touch->mouse emulation (enabled, as on
Android), whatever overlay is on top. One finger (index 0) only. Targets come from the game's own
geometry (hotspot `visual_pos`, surface helper rects such as `_target_anchor_point`,
`pose_option_rects`, `choice_rect`, `_pipe_tray_rect`, `ribbon_point`, the ghost-finger
`_demo_finger_pose()` path, etc.). The policy reads game state; it never calls game logic,
`_gui_input`, `_on_gesture` or `_open_task` (the probe's shortcuts are not used).
`REEF_INPUT=touch_only` turns touch->mouse emulation off (diagnostic only, NOT the device path).

Room flow per phase: tap the glowing hotspot (Roshan walks there, the object opens the task),
then the activity. Per-career planners: boxing (glove rest -> target drag; guard holds;
imp waits for the open star), ballet (matching pose card, ribbon path, twirl circle), teacher
(join, count each counter, answer), geology (river path, brush zig-zag + fossil pieces, pan
swings, seams + pull), detective lens (drag glass to next clue, dwell), nursery catch (cradle
follows the lowest baby), racer (steering drag, inside-line controller from the probe, no
turbo), pipes (same diagnosis as the game's 8 s hint, without waiting), generic surface modes
(tap/choice/hold/pour/oven/circle/swipe/trace/long push/paint/candy sort/farm lob/echo/dance)
and a ghost-finger mimic fallback (also used 35% of the time after 25 s without progress).

## Policies

| policy | behaviour |
|---|---|
| expert | 0.12-0.22 s between actions, exact targets, fast drags (1100 px/s), waits for valid moments (shuffle over, golden oven, listening turn, piece not in flight) |
| child_sim | 0.5-0.9 s reaction before each action; 25% of taps (and drag starts, 10-35 px) off target by 40-120 px; 15% wrong choice where a choice exists (lanes, pose cards, teacher answers, echo stars, dance pads, candy bins, pipe tile); drags 380-620 px/s with 8-22 px sinusoidal wobble + jitter; 10% of drags lifted early (40-80% of the way); 20% of holds released after 0.8-2.5 s; circles 2.6-4 rad/s for 3-8 s with radius wobble; late, noisy steering/cradle following |
| slow | expert accuracy, 10-20 s pause before every action (including the hotspot tap) |
| random_tapper | a tap (80 ms) at a uniform random canvas point every 0.38-0.62 s (~2 Hz); never drags |
| idle | no input at all until MAX_SECONDS |

## Output: `run.json`

Top level: `career, career_name, act_index, policy, seed, mode, input_path, rendered, completed,
seconds` (game seconds to the win, or to the cap), `session_seconds, wall_seconds, total_inputs`
(touch-downs), `total_drag_moves, dead_touches, hints, assists_or_mercy_events,
longest_no_input_wait {seconds,start_s,phase}, no_input_total_s, no_input_pct` (of `seconds`),
`phase_count, phases[], voice_lines[], voice_line_count, audio_starts, audio_start_log[]`,
`performance_result, performance_stats` (two-act careers), `frames[], save_isolation,
problems[], events[]`.

`phases[]` (one entry per phase attempt; a detective guided retry opens a new entry):
`n, index, name, mode, part` (practice/stage for two-act careers), `finale, start_s` (phase
armed), `open_s` (activity opened; = start_s when it opens in place), `end_s, seconds, outcome`
(completed / won / rival_solved_guided_retry / end), `inputs, drag_moves, dead_touches, hints,
assists_or_mercy_events, hint_events[{t,kind}], assist_events[{t,kind}], voice[]` (voice keys
requested while that phase was live).

Definitions (heuristic where noted)
- dead touch: a touch-down after which, from press until 0.4 s after lift, NOTHING observable
  responded: no audio stream started, no surface signal (`gesture`, `race_event`,
  `progress_changed`, teacher/nursery signals), no phase/progress/task change, no walk or
  hotspot intent, no lens move, no rehint (demo restart), no feedback flash, no change in a
  list of visible surface state fields (carried piece, glove position, placed tile, fill...).
  It cannot see purely cosmetic shader/tween reactions; treat counts as "no state, sound or
  progress response". The first dead touch of a run logs `first_dead_touch_top_control` (the
  Control the GUI picks at that point).
- hints: `room_reprompt_9s` (spoken prompt again at 9 s idle before the task), `idle_rehint_Ns`
  (world idle timer, 7 s ballerina / 9 s others, demo + prompt), `surface_rehint` /
  `touch_rehint` (the surface restarted its ghost-finger demo by itself / right after a touch,
  i.e. a wrong-touch rehint), `lens_glisten_12s`, `voice_<key>` for help/hint/peek lines.
- assists_or_mercy_events: `auto_walk_to_station_20s` (Roshan walks herself to the object),
  `assist_level_N` (boxing/ballet surface assist escalation), `teacher_help_shown`,
  `guided_retry_after_rival_win`.
- longest_no_input_wait: longest continuous span (until the win) in which no meaningful input
  was possible: phase advance/reveal pending, hotspot opening, Roshan walking to a requested
  object, talk beats, surface `armed_only` / `completion_accepted` / `_input_blocked()`, echo or
  dance not in the listening turn, kart race not live. Expert runs therefore measure the game's
  own dead time.
- voice_lines: every `_say`, `show_msg`, `say_sequence` and `play_success_yay` request (logged by
  a subclass of the game's AudioDirector installed before `main._ready`), including requests the
  director then suppresses. `audio_starts` counts actual AudioStreamPlayer starts (any bus).
- events: start, phase_armed, phase_open, phase_complete, every action (`kind`, from/to),
  dead_touch, assist, auto_interaction, stuck (25 s without progress; with state snapshot), won,
  timeout.

`isolation.json`: real user-dir fingerprint before/after, temp user dir, whether a save was written.

## Save isolation (verified)

Two layers: (1) the act starts through `OperaHouse.start(..., {"reward_policy": "dev_playtest"})`,
the engine's own isolated replay (no stars, mastery, checkpoints or save writes); (2) the wrapper
points `XDG_DATA_HOME` at a fresh temp dir, so `user://` (the save) is empty and private per run
and deleted afterwards. Verified on all 15 careers: `save_exists_after=false` in the temp dir and
the real `~/.local/share/godot/app_userdata/Mermaid Roshan Reef of Light` fingerprint unchanged.
Consequence: every run is a first-time fresh profile.

## Verification (2026-11-01, display :56)

fast, expert, seed 1, finger path (`verification/fast_expert/<career>/`):

| career | completes | game s | phases | inputs | dead | longest wait s | problems |
|---|---|---|---|---|---|---|---|
| chef | yes | 35.4 | 5 | 17 | 0 | 2.2 | |
| detective | yes | 22.0 | 3 | 10 | 0 | 3.5 | |
| ballerina | yes | 45.7 | 6 | 14 | 0 | 5.5 | |
| candymaker | yes | 23.6 | 4 | 18 | 0 | 2.2 | |
| doctor | yes | 27.5 | 5 | 15 | 0 | 3.7 | |
| farmer | yes | 27.1 | 4 | 17 | 0 | 3.6 | |
| boxer | NO | (300 cap) | 1 | 606 | 565 | 1.9 | stuck in GLOVE GUIDE, see below |
| boxer (REEF_INPUT=touch_only) | yes | 49.9 | 5 | 21 | 0 | 2.6 | diagnostic path |
| magician | yes | 48.6 | 8 | 21 | 0 | 2.2 | |
| painter | yes | 14.4 | 3 | 10 | 0 | 2.4 | |
| astronaut | yes | 38.6 | 4 | 21 | 0 | 2.2 | |
| racer | yes | 47.2 | 3 | 6 | 0 | 2.4 | |
| popstar | yes | 48.4 | 7 | 34 | 0 | 3.6 | |
| nursery | yes | 46.1 | 5 | 21 | 0 | 2.6 | |
| geologist | yes | 28.0 | 4 | 16 | 0 | 2.3 | |
| teacher | yes | 15.4 | 4 | 13 | 0 | 2.2 | |

child_sim seed 7, fast: 13/14 non-boxer careers complete (20-78 s); ballerina soft-locks (below).
Rendered (`verification/rendered/`): racer child_sim completes in 60.1 s (3 phases, 0 dead,
28 frames: room hotspot, kart race in progress, curtain call); racer idle and boxer idle never
complete in 90 s (auto-walk assist at 20 s opens the task, then 9 s rehints only); boxer
child_sim stuck in GLOVE GUIDE (72 dead touches; frame shows the right glove guided, the left
glove frozen).

## Careers that cannot be driven on the device path, and workarounds

1. Boxer (every policy, finger path): the boxing surface accepts emulated mouse events until it
   has seen a touch. Godot dispatches the emulated mouse press BEFORE the touch it came from, so
   the very first finger press claims glove 0 for the phantom `MOUSE_FINGER` (-101); its emulated
   release is then ignored (`_saw_screen_touch` is now true), so glove 0 stays owned forever and
   GLOVE GUIDE (needs both gloves) can never finish. `touch_owner_snapshot()` after the first
   press shows `{-101: 0, 0: 1}`. This is very likely a real tablet defect (Android touches go
   through the same `Input.parse_input_event` emulation), not a harness artifact; verify on device.
   Workaround for auditing the rest of Boxer: `REEF_INPUT=touch_only` (completes all 5 phases).
   Report both and label the touch_only runs as non-device input.
2. Ballerina stage RIBBON TRAIL can soft-lock (seen with child_sim seed 7, fast;
   `verification/ballerina_child_sim_seed7_softlock/`): `ribbon_progress` ends at 0.99999869, the
   surface reports `_mode_complete()` and blocks input, but `phase_progress` 0.999998 < goal 1.0
   so the world never advances; only 7 s rehints follow. Real game defect (float epsilon), reached
   by drag sampling; not every seed hits it.

## Known limits

- Policies are models driven by game-state oracles; `expert` is near-perfect, `child_sim` is a
  stochastic approximation of a 4-year-old, not a child. Say "scripted" in findings.
- One finger only: racer turbo (second finger) and multi-touch are never used.
- Dead-touch, hint and assist detection are heuristics from state, signals and audio (see above).
- Fast mode audio timing is scaled, not exact; rendered mode runs below real time on llvmpipe and
  frame captures add ~0.2 s hitches (use REEF_RENDER_FIXED_FPS=30 for deterministic rendered runs).
- Every run is a fresh profile (no persistence across runs by design).
- Chapter 2 story variants and the Castle room entrances are not exercised: the harness starts the
  freeplay act directly through OperaHouse (dev_playtest), like probe_opera_2d.gd.
- If a future build changes a surface's helper names, that planner falls back to the ghost-finger
  mimic and the run shows `stuck` events; check `problems[]` and `events[]` before trusting a run.
