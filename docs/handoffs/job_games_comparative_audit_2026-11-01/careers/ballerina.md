# Ballerina (ours) vs. show-then-copy references: comparative findings

- Build: dev @ 93166ab; harness `reef_play.sh` finger path; display :56. Ours runs are SCRIPTED policies.
- Rendered (Xvfb :56): expert-1, child_sim-1, idle-1; fast: the rest. `runs.jsonl` holds the 10 RUBRIC lines. child_sim-3 crashed at Godot start-up on its first attempt (signal 11, "propagate_notification ... caller thread", before any game frame; log `../../scripts_ours_56/crash_ballerina_child_sim3_attempt1.log`) and was rerun; treated as an environment fault, not a game defect.
- "child-sim-5" fills the replay slot (fresh profile per run; persistence judged from code).
- Extra runs (not among the 10): `softlock_scan/child_sim-7..18` (fast, 300 s cap) and `softlock_repro/` (deterministic reproduction, below).
- References: no ballet game could be played. Nearest PLAYED comparables for "watch, then copy" are from ref_rhythm (Blinken, GCompris Melody, GCompris Play rhythm; `../ref_rhythm/runs.jsonl`). Just Dance Kids: DOCUMENTED only (`../ref_commercial/documented_findings.md`). Toca Dance: DOCUMENTED only, not scored. `ref_rhythm/findings.md` arrived late and is folded in.

## Soft-lock: CONFIRMED, wider than reported, with a deterministic reproduction

**Brief's claim:** child_sim seed 7 soft-locks in RIBBON TRAIL (ribbon 0.99999869 < 1.0). **Confirmed**, and GRAND TWIRL has the same defect.

Mechanism (code at 93166ab):
- `OperaBalletSurface._mode_complete()` returns true at `ribbon_progress >= 0.999` / `twirl_progress >= 0.999` (`scripts/opera_ballet_surface.gd:282-290`); from then on `_input_blocked()` and `_drag()` reject all input (`:315`, `:347`) and `restart_demo()` returns early (`:113`).
- The world only advances when `phase_progress >= goal` with goal 1.0 (`scripts/opera_career_world_2d.gd:3510`). `phase_progress` is the sum of the surface's deltas, so it equals the surface value (for example 0.9995).
- The world already has the fix ("The authored specialist endpoint is authoritative ... can be 0.99999994 and input is already correctly blocked", `:3486-3491`), but only `if using_chapter_two_phases`. The Opera freeplay and Hall paths never get it.
- Ribbon: the progress is the nearest point on the curve to the finger; a finger that stops a hair before the end (last ~1 px of curve) projects to [0.999, 1.0). Twirl: progress grows by angle steps; any step that lands in [0.999, 1.0) instead of crossing 1.0 locks it (the `delta <= 0.0001` guard then rejects the remainder).

Reproduction (deterministic, same finger path and expert policy; only the gesture end point changes; script `audit_local/ours56/softlock_repro.gd`, wrapper `/home/claude/audit_work/scripts_ours_56/repro_play.sh`, no game file edited):

| command | result |
|---|---|
| `REPRO_RIBBON_END=0.9995 repro_play.sh ballerina expert 1 OUT fast 120` | LOCKED in practice RIBBON TRAIL at 41.9 s: ribbon 0.99950, world 0.99950, `mode_complete` true, `input_blocked` true; 17 re-prompts to 120 s |
| `REPRO_RIBBON_END=1.0 ...` (control) | completes, 47.6 s |
| `REPRO_TWIRL_END=0.9995 ...` | LOCKED in practice GRAND TWIRL at 49.3 s: twirl 0.99950, world 0.99950 |
| `REPRO_TWIRL_END=1.0 ...` (control) | completes, 47.4 s |
| stock policy, rendered (`softlock_repro/ribbon_end_0.9995_rendered`, ribbon end ignored in rendered because window coordinates land on the end pixel) | stock expert circle LOCKED in stage GRAND TWIRL at 72.4 s, twirl 0.99923; frame `frames/ballet_SOFTLOCK_twirl_ring_full_61s.png` shows the ring drawn full while the game re-prompts every 7 s |

Frequency with the stock harness:

| policy / mode | runs | locked | where |
|---|---|---|---|
| child_sim, fast (seeds 2,3,4,5,7-18) | 16 | **14** | 11 RIBBON TRAIL (7 practice, 4 stage), 3 GRAND TWIRL (stage 2, practice 1) |
| child_sim, rendered (seed 1) | 1 | 0 | |
| expert / slow (fast and rendered) | 4 | 0 (+1 rendered twirl lock in the repro run's stock twirl) | |

Locked values seen: ribbon 0.99999476-0.99999976; twirl 0.99926-0.99933. Locked runs show 77-87 re-prompts in 550 s for a task that cannot accept input (`child_sim-2..5`). Fast mode samples drags at 60 Hz with float coordinates, which is closer to a tablet's touch stream than the 30 fps rendered runs; the twirl lock also occurred in rendered mode.

**Fix (small, before any rebuild):** remove the `using_chapter_two_phases and` condition at `opera_career_world_2d.gd:3486`, or have the surface snap `ribbon_progress`/`twirl_progress` to exactly 1.0 and emit the remainder when it crosses 0.999. Acceptance: the four repro commands above all complete; 50 fast child_sim seeds and 10 rendered child_sim seeds complete with 0 locks.

## Measurements (10 runs)

| run | mode | done | game s | inputs | dead | hints | assists | no-input % | note |
|---|---|---|---|---|---|---|---|---|---|
| expert-1 | r | yes | 49.0 | 13 | 0 | 4 | 0 | 78.9 | |
| expert-2 | f | yes | 46.0 | 15 | 0 | 7 | 2 | 82.1 | "hints" are mostly per-round pose demos |
| child-sim-1 | r | yes | 55.1 | 15 | 0 | 6 | 2 | 77.9 | |
| child-sim-2 | f | **LOCK** | 600 cap | 16 | 0 | 87 | 3 | 98.5 | stage RIBBON 0.9999976 |
| child-sim-3 | f | **LOCK** | 600 cap | 10 | 0 | 84 | 2 | 99.0 | practice TWIRL 0.99926 |
| child-sim-4 | f | **LOCK** | 600 cap | 17 | 0 | 85 | 4 | 98.0 | stage TWIRL 0.99926 |
| child-sim-5 | f | **LOCK** | 600 cap | 7 | 0 | 86 | 1 | 99.4 | practice RIBBON 0.9999897 |
| slow-1 | f | yes | 209.8 | 13 | 0 | 35 | 15 | 33.8 | |
| random-tapper-1 | f | no | 136.4 | 229 | 138 | 34 | 4 | 59.0 | **completed PEARL MIRROR (3 rounds) by random taps in 124.6 s**; exited at 136.4 s |
| idle-1 | r | no | 120 cap | 0 | 0 | 13 | 3 | 24.6 | 7 s re-prompts with the demo, no progress |

- Expert: about 8-10 s of possible input in a 46-49 s session. Dead time comes from a 3.3 s voice hold between every phase (`ballet_voice_hold_seconds`), 2.15 s of blocked demo before each of the 3 pose rounds (twice), and walk/open beats.
- Targets: pose portraits about 190-220 px circles; ribbon corridor 116 px; resume pearl 128 px; twirl ring 116 px wide at radius 150-190 px; widened by 28-30 px at assist level 2 (`frames/ballet_pearl_mirror_open.png`, `ballet_grand_twirl_open.png`).
- Roshan: about 180 px tall in the bottom-left corner of the stage, partly cut by the frame edge, holding a still pose while a code-drawn ribbon fills the stage (`frames/ballet_stage_ribbon_trail_roshan_in_corner.png`).
- The PEARL MIRROR demo moves a ghost from the target portrait to the correct answer, which then glows (`frames/ballet_idle_31s.png`).

## 1. Scores (0-5; PLAYED vs DOCUMENTED kept distinct)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Ours: Ballerina** | played (scripted) | 2 | 2 | 3 | 3 | 1 | 1 | 1 | 2 | 4 | 4 | Portrait quiz, fixed wave trace, ring orbit; random taps cleared PEARL MIRROR; 0 dead touches in child runs, 60% for random; 7 s re-prompt with demo; 14/16 fast child-sims soft-locked; 79-82% no-input for expert; same content every run; cheer only; 116-220 px targets; tap, drag, circle |
| Blinken (Simon) | PLAYED, nearest comparable (ref_rhythm scores) | 2 | 4 | 3 | 1 | 1 | 2 | 2 | 1 | 4 | 5 | Watch then repeat; game over on one wrong pad; no soft-lock in 10 runs |
| GCompris Melody | PLAYED, nearest comparable (ref_rhythm scores) | 3 | 4 | 2 | 2 | 3 | 2 | 3 | 2 | 4 | 5 | Listen then copy; random 0 credit; wrong = same tune again; one silent stall after an off-bar tap (run 5); no soft-lock |
| GCompris Play rhythm | PLAYED, nearest comparable (ref_rhythm scores) | 3 | 5 | 3 | 1 | 1 | 3 | 2 | 2 | 2 | 4 | Demo then copy in time; late or early child fails forever; no soft-lock in 10 runs |
| Performous dance (Beginner) | PARTIAL (ref_rhythm scores; timing invalid) | 3 | 3 | 3 | 1 | 3 | 3 | 1 | 2 | 1 | 1 | Dance mat/keys; text menus; songs never stop early |
| Just Dance Kids | DOCUMENTED | 4 | - | - | 4 | 3 | - | - | - | - | 1 | Cue glows on the leader's body; complicated moves removed for 4+; Wii Remote |

Means (scored dims): ours 2.3; Blinken 2.5; Melody 3.0; Play rhythm 2.6; Performous 2.1 (partial); Just Dance Kids 3.0 (4 documented dims, not comparable). Reference scores are the ref_rhythm agent's, judged for a 4-year-old; they rate echo/rhythm games, not ballet, so treat them as the nearest played bar.

## 2. Where the reference is objectively better

1. **Every run reaches a defined state (D5, D6).** Blinken, Melody and Play rhythm: 30 played runs, each ended in success, a game over, or a screen waiting for input that would accept it (Melody run 5 stalled silently after an off-bar tap, but a new tap restarts the answer). Ours: 14 of 16 fast child-sim runs (and 1 rendered stock twirl) ended with input blocked and no way forward, 77-87 re-prompts per locked run.
2. **Random input cannot pass the "copy" step (D2).** Melody: 118 random taps, 0 credit; Blinken: random taps hit game over at 6.0 s; Play rhythm: 0 attempts credited. Ours: random taps completed all 3 PEARL MIRROR rounds in 124.6 s (214 taps), because the demo shows and lights the answer and only 2-3 large portraits are offered.
3. **The cue is on the dancer (D1, D4; DOCUMENTED).** Just Dance Kids lights the leader's hand; the child copies a body. Ours shows a portrait card and keeps Roshan as a 180 px still figure in the corner (`frames/ballet_stage_ribbon_trail_roshan_in_corner.png`).
4. **Content changes between plays (D7).** Blinken draws a new sequence each game. Ours: the same 3 pose rounds, the same sine curve and the same ring in all 10 runs, each played twice per visit.

## 3. Where ours is better (keep these)

1. **No game over** (Blinken ends on one wrong pad and asks for a typed name).
2. **Idle help at the right cadence:** ours re-prompts every 7 s with the ghost demo (the only one of my three careers inside the 6-8 s target); all three played references are silent for 60 s idle.
3. **Assistance widens instead of failing:** after 5 s / 10 s without progress the corridor grows 28 px and the ring 30 px (`opera_ballet_surface.gd:166,196`); Play rhythm replays the same tune with the same window after every fail.
4. **Large, separated targets:** portraits about 190-220 px, ribbon corridor 116 px, ring 116 px; all above the ~120 px rubric bar except the ring's width, which is generous for a drag.
5. **Banked, monotonic progress:** lifting mid-ribbon and resuming at the 128 px pearl keeps progress (when it does not lock).

## 4. Redesign guide (ordered by impact for a 4-year-old)

Status vs. the Oct 17 spec (`BALLERINA.md`, `SHARED_SYSTEMS.md`): COVERS / CONTRADICTS / MISSES.

1. **Hotfix the soft-lock in the shipping game now.** *Spec: MISSES.* BALLERINA §10 retires RIBBON TRAIL and GRAND TWIRL, but nothing is built and the live game locks 14/16 fast child-sim runs. The spec also tells the rebuild to carry forward "monotonic progress" from this surface without naming the bug class: a surface that declares completion and a world that does not. Add to SHARED_SYSTEMS §1: "one completion authority: when an activity blocks input as complete, the host advances within one frame". Acceptance: the four repro commands complete; 50 fast + 10 rendered child_sim seeds, 0 locks; a probe asserts `surface._input_blocked() and not phase_advance_pending` never holds for more than 0.5 s.
2. **Never re-prompt a task that cannot accept input.** Locked runs got 77-87 identical prompts. *Spec: MISSES.* Gate idle re-prompts on "input possible"; if blocked for more than 2 s, log a stuck event and force-advance. Acceptance: in the repro, 0 re-prompts after the lock and the phase advances within 2 s.
3. **Cut the dead time.** Expert: 79-82% of the session has no possible input (3.3 s voice hold between all 6 phases, 2.15 s blocked demo per pose round). *Spec: partly COVERS* (no blocked portrait demo; Roshan moves on touch-down) but *MISSES* a budget, and its own rule "taps arriving while a move is still being danced are ignored" with a beat-landing of up to 0.71 s re-creates blocked time. Accept the first touch of the next step immediately (queue it to the next beat) instead of ignoring it. Acceptance: expert probe run has input possible for at least 50% of the session; no blocked wait over 1.5 s outside curtain and bow.
4. **The demo must not perform the answer.** Random taps cleared PEARL MIRROR. *Spec: COVERS* (retire PEARL MIRROR; acceptance 3: a 5 Hz tapper completes only Point steps). Add my number as the baseline: today random completes the copy step in 124.6 s.
5. **Roshan dances, centre stage, full size.** *Spec: COVERS* (§4 hit region 260x300, §7 centre stage). Today 180 px in a corner, cut by the frame.
6. **Remove the practice duplication.** 6 phases = 3 twice. *Spec: COVERS* (SHARED §5).
7. **Vary the routine between visits.** *Spec: partly COVERS* (fixed phrase order in §5; variety only in the later "make your own dance" encore). *MISSES* variety in the first build: shuffle the recital phrases from the five moves (keep 2-3 steps). Acceptance: 10 seeded visits give at least 4 distinct phrase orders.
8. **Twirl-off rule check.** *Spec: possible CONTRADICTION to verify on device:* "at least 270 degrees within 2 s" is 2.4 rad/s minimum; the child-sim circles at 2.6-4 rad/s pass, but a slow, careful 4-year-old may not. Make the 2 s window a mercy-widened value (2 s -> 4 s after two tries) like the other fallbacks. Acceptance: a scripted 1.5 rad/s circle completes a Twirl after two tries.
9. **Probes on the device input path; random taps must not exit.** Shared with Racer and Pop Star (exit at 136.4 s under the same random timeline). *Spec: CONTRADICTS (probe path, SHARED §10 `_gui_input`) / MISSES (exit).*

## 5. Defects found (Ballerina)

- **B1 RIBBON TRAIL soft-lock** (confirmed). Repro: `REPRO_RIBBON_END=0.9995 /home/claude/audit_work/scripts_ours_56/repro_play.sh ballerina expert 1 OUT fast 120`. Stock: `reef_play.sh ballerina child_sim 7 OUT fast 300`.
- **B2 GRAND TWIRL soft-lock** (new). Repro: `REPRO_TWIRL_END=0.9995 .../repro_play.sh ballerina expert 1 OUT fast 120`. Stock: `reef_play.sh ballerina child_sim 4 OUT fast 600` (stage), seed 3 (practice), seed 14 (stage); rendered stock expert in `softlock_repro/ribbon_end_0.9995_rendered`.
- **B3 Endless re-prompts while locked** (77-87 per run).
- **B4 Random taps complete PEARL MIRROR** (design defect): `reef_play.sh ballerina random_tapper 1 OUT fast 600`.
- Environment: one Godot start-up crash (signal 11) before the game loaded; rerun was clean.

## 6. Limits

- Scripted policies, one finger; no ballet reference could be played, so the played comparables are memory/echo/rhythm games and Just Dance Kids is documented only.
- No audio device; voice logged from code.
- The lock frequency is for the harness's drag model (60 Hz, float coordinates, 8-22 px wobble). A real child's rate is unknown; the mechanism needs only the final touch to land within about 1 px before the ribbon end, or one twirl step to land within 0.001 of a full turn.
