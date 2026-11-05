# Boxer ("The Friendly Championship Bout"): comparative findings

All runs are scripted harness runs on :60, `dev` @ 93166ab. The 10 rubric runs used `REEF_INPUT=touch_only` (non-device input) because the default finger path soft-locks; three `finger_path_*` runs use the device path. Every run starts from a fresh profile, so persistence is from code.

## 0. P0 defect: the emulated mouse claims the left glove (reproduced)

`project.godot` has `emulate_mouse_from_touch=true`, as on Android. For each finger press Godot delivers the emulated `InputEventMouseButton` (device -1) before the `InputEventScreenTouch` it came from. In `scripts/opera_boxing_surface.gd`:
1. `configure()` sets `_saw_screen_touch=false` (line 99) every phase.
2. The first emulated press reaches `_gui_input` (lines 412-421); the guard at line 415 needs `_saw_screen_touch`, so it does not fire.
3. Line 418 calls `_handle_press(MOUSE_FINGER)`; `_choose_hand` (lines 490-505) gives glove 0 to finger -101 (lines 438-439).
4. The real touch then sets the flag (line 401) and gets glove 1.
5. The emulated release and motion are then dropped (lines 415-416, 424-425); glove 0 stays owned and `_choose_hand` skips it (line 493).
6. GLOVE GUIDE needs both gloves, so it never finishes (fill stays 0.5). Other phases lose the left glove and the first punch but accept either glove.

Headless repro (about 3 s, no game edits), in the project folder:
`./Godot_v4.7.2-stable_linux.x86_64 --headless --resolution 1280x720 --path . -s res://audit_local/glove_repro/repro.gd -- variant=shipped`
prints `recv[0] MouseButton device=-1 saw_touch_before=false -> owners={-101:0}` then `recv[1] ScreenTouch -> {-101:0, 0:1}`; result `guide_done=[false,true]`. Controls: `emulate=0` and `variant=fixed` both give `[true,true]`.

Device-path runs: `finger_path_expert-1` 120 s still in GLOVE GUIDE, 207 touches, 193 dead (frame `boxer_glove_guide_STUCK_fingerpath_12s.png`). On a tablet the only exits are leaving the career or app focus loss (lines 287-289).

**Fix:** return early for every `InputEventMouse` with `device == InputEvent.DEVICE_ID_EMULATION`, as `kart_canvas_2d.gd:171` already does, and remove `and _saw_screen_touch` from lines 415 and 424. Add a GLOVE GUIDE watchdog that clears owners after 8 s without progress. Needs confirming on the tablet; if the tablet build shows the same order, Boxer is currently unwinnable on device.

Harness note: `reef_play.gd:695-699` (`_top_control_at`) pushed a real mouse motion that let one finger-path child run finish; that run is an artifact, not evidence the device path works.

## 1. Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours, device path | PLAYED | 4 | 0 | 1 | 4 | 0 | 0 | 1 | 0 | 4 | 4 | Never leaves GLOVE GUIDE; 193/207 touches dead |
| Ours, as designed (touch_only) | PLAYED | 4 | 4 | 4 | 4 | 4 | 3 | 1 | 3 | 4 | 4 | 9/9 play runs complete in 49.5-71.8 s (slow 332.8 s); idle and random never win |
| GCompris ballcatch | PLAYED | 2 | 5 | 3 | 1 | 1 | 4 | - | - | 4 | 1 | Expert level 7; child-sim stuck at level 2 (1 win, 12-13 losses/min); 0 hints |
| GCompris play_rhythm L1 | PLAYED | 2 | 5 | - | 2 | 1 | - | - | - | - | 2 | Errors <=108 ms pass, 150-164 ms mostly fail, +300 ms fails 6/6 |
| Punch-Out!! (Wii) | DOCUMENTED | 4 | 5 | - | - | 1 | - | 3 | - | - | 1 | Help only after 100 lost fights |

Ours (designed): D2 a punch outside the opening "bonks" and does not count (lines 540-546); expert 49.5-54.3 s vs child 56.5-71.8 s, same outcome. D3 0 dead touches, 43-47 audio starts per run, no graded quality (every accepted punch = 1.0). D4 5 voiced prompts and a ghost hand; first input 2.0 s after open; idle re-hint 9 s. D5 assists at 5 s and 10 s widen targets 18 px (line 588), add 0.45 s windup and 0.5 s opening; time-based, so experts get them too. D6 TITLE IMP floor 21.4-23.3 s for 7 inputs; SOFT GUARD a fixed 9.6 s in the 5 fast runs (rendered 9.8 and 13.7 s, slow 54.1 s); 21-28% of the session allows no input. D7 identical sequence in 10/10. D8 belt curtain call; nothing kept; no boxer checkpoint. D9 gloves about 100x120 px, acceptance radius 78 px. D10 one-finger drags; the guard is a 3.2 s still hold.

## 2. Where the references are objectively better
1. **They work on their real input path.** No soft-lock in 20 played reference runs; every attempt resolved within about 2.5 s. Ours: 0 of 2 clean device-path runs finished.
2. **Timing matters.** Ballcatch expert level 7 vs child level 2; play_rhythm expert 3/3 vs +300 ms 0/6; Punch-Out!! awards stars for perfect timing (DOCUMENTED). Ours: TITLE IMP 21.4 s expert vs 23.1-31.1 s child, same outcome, no reward for good timing.
3. **Variety.** Punch-Out!! has a roster. Ours: 1 opponent, 1 sequence in 10/10.
4. **Time to first action.** Ballcatch first tap at 0.29 s, a throw every ~4.6 s. Ours opens GLOVE GUIDE at 2.0-2.6 s and the first imp opening comes 2.9 s later.

Timing-window evidence: ours telegraphs with a 1.15 s windup (1.6 s assisted) plus bell and crouch, a 0.38 s charge, and a 1.7 s opening (2.2 s assisted) (lines 362-374, `imp_is_open` line 229); 4 distinct imp poses. That window is 11-15x wider than play_rhythm's 110-150 ms, which is right for a 4-year-old.

## 3. Where ours is better (keep)
No fail state (references lose 12-13 rounds per minute for a child-sim or replay the same rhythm with no slow-down); a telegraph before every opening; one finger (ballcatch needs two hands at once); a voiced prompt per phase; 156-228 px targets.

## 4. Redesign guide (by impact)
1. **Fix the glove claim + watchdog** (section 0). *Check:* `repro.gd` prints `guide_done=[true,true]`; `reef_play.sh boxer expert 1 <d> fast 120` on default finger input completes 5 phases with 0 dead touches; on the tablet one finger finishes GLOVE GUIDE in under 10 s.
2. **Shorten TITLE IMP:** 4 openings (or 2 punches per opening); first windup at +0.5 s. *Check:* expert 12 s or less (now 21.4); child 16 s or less (now 23-31).
3. **Make SOFT GUARD react to the child:** start the count 0.6 s after a glove enters the bubble, with a voiced "block!". *Check:* expert 5 s or less (now 9.6 s in fast runs).
4. **Graded, no-fail timing:** a "best" effect for a punch in the first 0.5 s of the opening. *Check:* a probe punching at +0.2 s vs +1.5 s logs different feedback keys; idle still never wins.
5. **Seeded variety:** jab order, guard side, 3 imp costumes. *Check:* 10 seeds show at least 3 jab orders.
6. **Boxer checkpoint and a 1 s hold on Back.** *Check:* random_tapper seed 1 survives tap #229.

## 5. Other defects
One-tap exit: random tap #229 at (101.5, 116.6) hits Back and ends the career (confirmed by replaying the harness RNG).

## 6. Limits
The "designed" row is non-device input; child_sim waits for `imp_is_open`, so bonks are under-sampled; not verified on the tablet; no PC-installable boxing reference exists for ages 3-6.
