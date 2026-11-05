# Racecar Driver (ours) vs. racing references: comparative findings

- Build: dev @ 93166ab, harness `reef_play.sh` (finger path = `Input.parse_input_event` with touch->mouse emulation on), display :56.
- All ours runs are SCRIPTED policies, not a child. Fast = headless 60 Hz fixed ticks; rendered = Xvfb :56, llvmpipe.
- Runs: `runs.jsonl` (10 RUBRIC lines). Rendered: expert-1, child_sim-1, idle-1. Fast: the rest.
  Extra diagnostic (not one of the 10): `diag_hold_only/` = one finger held on the steering band centre for the whole race, never steering.
- "child-sim-5" fills the replay slot: every run starts from a fresh profile, so persistence was judged from code (career star bit only; no kept artifact).
- References: SuperTuxKart 1.4 and Extreme Tux Racer 0.8.3 PLAYED by the ref_racer agent (`../ref_racer/runs.jsonl`, frames in `../ref_racer/frames/`); Mario Kart 8 Deluxe / World DOCUMENTED only (`../ref_commercial/documented_findings.md`); Toca Cars and Blaze Axle City Racers DOCUMENTED only (`../ref_commercial/reference_map.md`), not scored. `ref_racer/findings.md` (arrived late, no score table) is folded in; the STK/ETR scores below are mine from its runs.jsonl and frames.

## What our Racer is today (it is NOT what the Oct 17 DIAGNOSIS describes)

DIAGNOSIS §4 (baseline 7a65b9f) describes a top-down painted circuit, no camera, a 770x126 steering bar and 19 px of steering. At 93166ab the RACE is a chase-view planar projection (`scripts/kart_canvas_2d.gd`: "Chase view is a planar projection into Canvas"), the kart about 170 px wide behind Roshan, speed zoom, boost pads, castle-room sectors with their own backdrops, a lap-flag and pearl-count HUD with digits, a 120 px turbo button, and an invisible steering band (`OperaRacerSurface.STEERING_RECT` 830x250 at y 430). Frames: `frames/racer_race_chase_view_hud_digits.png`. TUNE (circle) and TO THE LINE (swipe) are unchanged generic chores in the room (`frames/racer_tune_open_dot_target_roshan_away.png`). This matters for the redesign guide: the build has moved toward option C (behind-the-kart pseudo-perspective) that RACER.md §3 rejected, and toward the "following camera" the owner did not choose in Q5.

## Measurements (10 runs + 1 diagnostic)

| run | mode | done | game s | inputs | dead | hints | RACE s (open->end) | score / rival | tier |
|---|---|---|---|---|---|---|---|---|---|
| expert-1 | r | yes | 62.1 | 7 | 0 | 1 | 33.7 | 1511 / 346 | 3 |
| expert-2 | f | yes | 47.1 | 6 | 0 | 0 | 33.7 | 2719 / 344 | 3 |
| child-sim-1 | r | yes | 50.6 | 6 | 0 | 0 | 34.7 | 1543 / 356 | 3 |
| child-sim-2..5 | f | 4/4 | 49.5-57.2 | 6-8 | 0-1 | 0-1 | 33.8-34.5 | 2740-2795 / 347-355 | 3 |
| slow-1 | f | yes | 139.8 | 7 | 0 | 9 | 52.6 | 2876 / 523 | 3 |
| random-tapper-1 | f | no | 136.4 | 229 | 207 | 14 | (never reached) | - | - |
| idle-1 | r | no | 120 (cap) | 0 | 0 | 12 | (never reached) | - | - |
| diag hold-only | f | yes | 48.3 | 6 | 0 | 0 | 34.7 | 2801 / 356 | 3 |

- Every completed run: cheer "STANDING OVATION", tier 3, rival never first. Fast-mode scores rise with time spent: expert 2719 < child-sims 2740-2795 < hold-only 2801 < slow 2876.
- RACE is one continuous touch for about 34-37 s (2 touch-downs: the hotspot tap plus one held finger).
- No-input-possible share: 15-22% (longest 2.4 s, countdown).
- Idle: Roshan auto-walks at 20.2 s; the identical line `op_racer_tune_up_stage` plays at 0.1, 9.2 s, then every 9.0 s (13 plays in 120 s); the demo is a 25 px white dot with an 80 px faint ring (`frames/racer_idle_30s_ghost_dot.png`). Nothing completes.
- Random tapper: 207 of 229 taps (90%) dead in TUNE; 0 progress; at 136.4 s a random tap ended the act ("house finished without a win"). The same seed-1 tap timeline ended Pop Star and Ballerina at exactly 136.4 s too, so it is a shared exit control (the 112x112 px Back button, top left; confirmed by replaying the harness RNG: tap #229 lands inside it), not a career bug.

## 1. Scores (0-5; PLAYED vs DOCUMENTED kept distinct)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Ours: Racecar Driver** | played (scripted) | 2 | 1 | 3 | 3 | 3 | 4 | 1 | 2 | 3 | 2 | Steer = hold an invisible band; race 33.7-34.7 s for expert, child, hold-only; hold-only scores above expert; 0 dead touches in 8 completions but 90% dead for random taps; 9 s identical re-prompt; 47-57 s sessions; all tier 3; trophy podium, no kept artifact; 36 s continuous hold |
| SuperTuxKart 1.4 (Novice) | PLAYED (scripted bot, keyboard) | 4 | 4 | 2 | 0 | 0 | 2 | 4 | 2 | 1 | 0 | Expert 2nd in 72.5 s, AI finished ahead; child-sims 0/4 finished (pinned on a fence 105+ s, `stk_r03_*`); random never left the start; idle no hint, no end (`stk_r09_sheet_idle_no_hint.png`); text tutorial and WRONG WAY banner; items vary |
| Extreme Tux Racer 0.8.3 | PLAYED (scripted bot, keyboard) | 3 | 0 | - | 0 | 1 | 3 | 2 | 1 | 1 | 0 | Idle was the best of 10 runs (58.61 s, 13 pts); steering bots slower or unfinished; text menus |
| Mario Kart 8 DX / World | DOCUMENTED | 5 | 4 | - | - | 4 | - | - | - | - | 2 | Smart Steering + Auto-Accelerate; antenna shows the assist; controller only |

Means (scored dimensions only): ours 2.4; SuperTuxKart 1.9; ETR 1.2 (9 dims); Mario Kart 3.75 (4 documented dims, not comparable).

## 2. Where the reference is objectively better

1. **Input decides the outcome (D2).** SuperTuxKart: expert bot 72.5 s and 2nd of 4; four child-sim bots 0/4 finished; random keys never left the start straight; idle never finished. Ours: RACE open->end 33.7 s (expert) vs 34.3-34.7 s (child-sims) vs 34.7 s (hold-only, never steering): a 1.0 s (3%) spread, and hold-only scored 2801, above the expert's 2719; slow scored highest (2876). Steering quality does not change the result a child can see.
2. **The opponent is real (D2, D8).** SuperTuxKart expert-1: the AI Konqi finished first (1:10.6 vs our bot 1:12.5), so placing is earned. Ours: rival score 344-356 vs player 1511-2801 in all 8 completions; he never finishes first; every completion is tier 3 "STANDING OVATION" (`DL-INT-14`'s imp win rule is still not implemented).
3. **Variety between runs (D7).** SuperTuxKart runs differ by items collected, being hit (dizzy stars, brief slowdown), rank and finish time (`stk_r01_item_icon_top_center.png`, `stk_r01_finish_rank_text.png`). Ours: 8 completions, one outcome (tier 3, same cheer, same podium frame `frames/racer_finale_trophy.png`); only the pearl count varies (13 vs 21 in rendered runs).
4. **Position is readable without text (D8, D9).** SuperTuxKart shows a column of racer faces that reorders live, and a minimap with faces (ref_racer findings item 4). Ours: the rival is not on screen during the race; the HUD shows a lap digit and a pearl count in digits (`frames/racer_race_chase_view_hud_digits.png`).
5. **A start ritual that rewards timing without punishing eagerness (D2).** SuperTuxKart: a character holds the 3-light countdown; pressing within 0.3-0.5 s of Go gives a boost; pumping during Set costs nothing (ref_racer item 3, `stk_r01_countdown_set.png`). Ours logs a `kart_rocket_start` voice line at the start (12.8 s in expert-2), but the held-finger policies all got the same result, so no start skill is visible in the outcome.
6. **Assist is visible when it acts (D5, DOCUMENTED).** Mario Kart's Smart Steering antenna bends when it corrects. Ours keeps the kart on the road with no visible sign of help, so neither child nor adult can tell help from skill. (Documented, not measured.)

Not counted as better: SuperTuxKart's rescue bird (puts the kart back in 1-2 s, ref_racer item 2) solves a problem ours does not have, because our kart cannot leave the road. Otherwise both played references are keyboard games with text menus and no mercy.

## 3. Where ours is better (keep these)

1. **No fail state:** 8/8 non-idle, non-random runs finished (47-62 s, slow 140 s). SuperTuxKart child-sims 0/4; ETR expert-1 and child-sim-2 unfinished.
2. **Voiced re-prompt and auto-walk:** idle gets a spoken prompt every 9 s and an auto-walk at 20 s. SuperTuxKart and ETR idle runs got no hint at all for 100 s and 58 s.
3. **Short, bounded session:** 47-57 s for child-sims, longest no-input wait 2.4 s. SuperTuxKart child-sim waits up to 110 s pinned with no rescue.
4. **One finger, no reading to play:** SuperTuxKart needs keys and shows text (tutorial dialog `stk_01_tutorial_offer.png`, WRONG WAY).
5. **Speed presentation:** chase view with speed zoom and boost pads already gives motion the Oct 17 build lacked.
6. **Idle never wins:** ETR's idle run won (58.61 s); ours idle never completes.

## 4. Redesign guide (ordered by impact for a 4-year-old)

Status vs. the Oct 17 rebuild spec (`docs/handoffs/codex_minigame_rebuilds_2026-10-17/RACER.md`, SHARED_SYSTEMS.md): **COVERS** (spec already requires it; my measurement confirms it is needed), **CONTRADICTS** (spec says or implies the opposite), **MISSES** (spec silent).

1. **Make steering change what she sees and what happens.** Lanes with rings, ramps and gentle bumps; the imp can finish first and the race restarts. *Spec: COVERS* (RACER §5, acceptance 3 "hold only is slower than lane-changing child"). Add my numbers as the baseline the probe must beat: today hold-only = 34.7 s and outscores expert. Acceptance: probe runs expert lane-chooser, hold-only and idle; lane-chooser finishes at least 15% faster than hold-only, hold-only loses attempt 1 to the imp, idle never moves.
2. **Rebase the spec on the current chase-view build before building.** *Spec: CONTRADICTS the build / is STALE.* DIAGNOSIS §4 describes a circuit and 19 px steering that no longer ship; the build at 93166ab is a chase view (option C, rejected in RACER §3) with sector backdrops and speed zoom. The owner chose the side-scroller over "a following camera over the existing painted circuit" (Q5), but this third variant (chase view through castle rooms) was not on the table. Action: one owner question with a 30 s capture of the current chase view next to the side-scroll pilot; do not retire working speed presentation silently. Acceptance: owner decision recorded in OWNER_DECISIONS before MR4 starts.
3. **No 35 s held finger.** Kart keeps driving 3 s after any touch; holding is never required. *Spec: COVERS* (RACER §5 "Driving", "hold anywhere to drive" retires). Measured today: one continuous touch of 34-37 s in every completion. Acceptance: harness `expert` with lane taps only (no hold) completes; longest single touch in the run under 1.5 s.
4. **Idle help must escalate and show a hand, at 6-8 s.** Today: same line every 9.0 s, 13 times in 120 s, demo = 25 px dot. *Spec: partly COVERS* (race idle: karts stop, "Tap a lane to drive!"); *MISSES* the pre-race parts (paddock, colour, wheels) and escalation. Add: re-prompt at 7 s; on the 2nd re-prompt a 120 px painted hand taps the actual target; on the 3rd the target pulses and Roshan points at it. Acceptance: idle probe logs re-prompts at 7 s +-0.5, a different visual on the 2nd and 3rd, and no progress.
5. **Roshan does the pit work at the kart.** TUNE frame: Roshan stands at x 640 while the wrench target sits on the kart at x 300 (`frames/racer_tune_open_dot_target_roshan_away.png`). *Spec: COVERS* (pit stop; acceptance 9 "each wheel counts only after Roshan's contact").
6. **Random taps must not leave the game.** All three of my careers exited at 136.4 s under the same random-tap timeline. *Spec: MISSES* (DL-UI-05 covers Back cancelling input, not accidental exits). Add a two-step or hold-to-leave Back for the child surface (parent gesture). Acceptance: 10 random-tapper seeds x 300 s, 0 accidental exits; deliberate exit still under 2 s for an adult.
7. **Make the imp's progress readable without digits.** HUD shows lap "1" and pearl count digits (`frames/racer_race_chase_view_hud_digits.png`); the rival is not visible during the race. *Spec: COVERS* (imp kart beside her in the same lanes; wordless medals).
8. **Probe on the device input path.** *Spec: CONTRADICTS.* SHARED_SYSTEMS §10 says new probes drive touches "through `_gui_input`". That path skips Godot's touch->mouse emulation, which is exactly where the Boxer glove defect lives (emulated mouse press claims glove 0 before the touch). Probes for the three rebuilds must inject `InputEventScreenTouch/Drag` through `Input.parse_input_event` with `emulate_mouse_from_touch` on (as `audit_local/reef_play.gd` does). Acceptance: each new probe has one leg run on that path and asserts per-finger ownership tables contain no `-101` owner after release.

## 5. Defects found (Racer)

- **D-R1 Outcome independent of play (design defect, not a crash).** Repro: `REPRO_RACER_HOLD_ONLY=1 /home/claude/audit_work/scripts_ours_56/repro_play.sh racer expert 1 OUT fast 200` -> completes, RACE 34.7 s, score 2801, tier 3; compare `expert-2` 2719.
- **D-R2 Score rewards slowness.** slow-1 2876 > hold-only 2801 > child-sims 2740-2795 > expert 2719 (fast mode). Score appears to grow with time on track.
- **Rendered vs fast score scale differs** (1511-1543 rendered vs 2719-2876 fast for the same race length), so score is frame-rate dependent. Repro: compare `expert-1/run.json` (rendered) with `expert-2/run.json` (fast) `performance_result`.
- **Race landmark lines reuse castle room-entry clips** (`castle_gallery_enter`, `castle_movie_enter`) 8 times per 36 s race (`kart_canvas_2d.gd:94`). Not verified by ear (no audio device); flag for a listen.
- TUNE took 17.9 s in the rendered expert run vs 2.3 s fast (low llvmpipe frame rate makes the circle steps large); likely environment, but on a slow tablet the circle crank may also drop steps. Not confirmed on device.

## 6. Limits

- Scripted policies, not a child; one finger only (turbo never used).
- No audio device: voice is logged from code requests, not heard.
- The ref_racer findings.md has no score table; the STK/ETR scores are mine from its runs.jsonl and frames, judged for a 4-year-old.
- Mario Kart, Toca Cars, Blaze: documented only, never played.
- Persistence: judged from code (fresh profile per run).
