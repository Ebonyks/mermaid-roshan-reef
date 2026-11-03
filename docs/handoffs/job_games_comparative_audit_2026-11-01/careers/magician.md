# Magician ("The Grand Illusion Duel"): comparative findings

Setup as Teacher (10 scripted runs on :57, plus targeted probes in `ours_magician/probe/`). Both 2026-09-05 TRACK defects were re-tested and are still present.

## 1. Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours: Magician | PLAYED | 3 | 2 | 2 | 4 | 2 | 4 | 2 | 3 | 3 | 3 | 2.8 |
| GCompris magic-hat-plus | PLAYED | 2 | 4 | 3 | 1 | 2 | 3 | 3 | 2 | 1 | 4 | 2.5 |
| GCompris memory | PLAYED (partial) | - | - | - | - | - | - | - | - | - | - | - |
| Toca Lab: Elements | DOCUMENTED | 3 | 3 | - | - | 4 | - | 5 | - | - | - | - |
| Lost in Play | DOCUMENTED | 2 | 4 | - | 4 | 3 | - | 3 | - | - | 4 | - |

Ours:
- D1 hold the wand, track the hat, trace the rope, pull the cabinet, circle the portal: theatrical, but TRACK is "tap the glow".
- D2 idle never wins (90 s); always-wrong taps finish TRACK; medals are inverted by frame rate (rendered expert-1 Bronze with 13 misses, rendered child_sim-1 Silver); no run reached Gold.
- D3 rendered expert-1 and child_sim-1 started 0 sound effects within 0.25 s across 27 actions each; only ui_tap on hotspots and yay at the finale.
- D4 3 voiced practice phases before the stage; first input 1.2-1.7 s; ghost hand per gesture; re-hints every 9 s.
- D5 wrong taps pay progress (autopilot by mashing); a ROPE soft-lock exists.
- D6 47.6-65.5 s over 8 phases; dead time 30-39%; longest wait 2.2-2.3 s.
- D7 identical every run: TRACK lanes 1,0,2,1,0; only the medal varies.
- D8 lamb reveal and medal card; nothing kept.
- D9 lanes 131 px (practice), 159 px (stage); the VANISH wand is a thin stick at the room's right edge; the rope is about 30 px thick.
- D10 VANISH needs a continuous 3.8-4.2 s hold; the rest are drags, circles, taps.

GCompris magic-hat-plus: input gated during the 2.4-5.5 s hat animation; wrong answers never advance (child-sim-3 made 9 wrong OKs and still had to answer correctly, 116.5 s); praise voice about 0.6 s after OK; 32x32 px answer cells; text prompt; 0 hints in 60 s idle; stray taps opened a text help screen and quit the app (2 of 4 child sims).

## 2. Where the references are objectively better
1. **Wrong answers do not advance.** GCompris: 9 wrong OKs and still 3/3 required; memory mismatches gain nothing. Ours (probes `wrong-expert-1`, `-2`, `wrong-child_sim-3`): 0 correct answers out of 592/596/202 taps, yet both TRACKs complete in 77.3-80.6 s each (0.05 per wrong tap, at most once per 0.6 s, 100 taps to the goal of 5.0; `opera_gesture_surface.gd:414-419, 1002`), Bronze "WARM CHEERS". Each wrong tap also re-flashes the answer.
2. **Input is gated while hidden information moves.** GCompris accepts no input during the hat animation. Ours (probes `early-expert-1/-2`): 10/10 taps at 0.32-0.42 s into the 1.5 s shuffle paid 1.0; TRACK took 1.95 s (stage) and 2.98-3.05 s (practice) vs 8.0-9.0 s for a waiting expert. The press path has no shuffle gate (`opera_gesture_surface.gd:997-1002`); the answer hat is drawn at its lane for the whole 2.2 s flash (`:2709-2712`); the ghost hand points at it mid-shuffle.
3. **Real hiding.** GCompris memory hides cards (4-pair level 23-38 s, 0 dead touches). Ours never hides the answer and does not move the hats: a glow glides between lanes.
4. **Answer sound.** GCompris praise about 0.6 s after OK and completetask about 0.08 s; ours 0 sounds on 10/10 correct TRACK taps.

## 3. Where ours is better (keep)
Larger targets (131-159 px vs 32 px); voice and re-hints (GCompris text, 0 hints in 61.8 s idle); practice before the stage and 8 distinct tricks; no text dead ends near play targets.

## 4. Redesign guide (by impact)
1. **Gate TRACK and make the shuffle real.** Ignore choice presses while `shuffle_t > 0`; hats really swap places and the glow stays off for a 2 s child turn. Correct taps pay 1; wrong taps pay 0 and replay the shuffle slowly with the glow on; after 2 misses slow the next shuffle; never fail. *Check:* the early probe banks 0 during shuffles; the wrong probe never completes TRACK in 300 s; child_sim still finishes in under 90 s.
2. **Fix the ROPE threshold.** Accept `trace_journey >= 0.999` for magician, ballerina and every authored trace (`opera_career_world_2d.gd:3638` lists only chef and doctor), or snap to 1.0. *Check:* `reef_play.sh magician child_sim 2 OUT fast 90` completes.
3. **Make ROPE frame-rate independent** (subdivide samples instead of rejecting jumps over 18%, `opera_gesture_surface.gd:1835`). *Check:* rendered expert-1 has 0-1 touch re-hints in ROPE, as in fast mode.
4. **Per-touch sound:** a sparkle under 100 ms on each correct hat, rope segment, cabinet pull and portal turn. *Check:* audio start within 0.15 s of every scoring gesture.
5. **VANISH as a short hold or tap-and-wave** under 1.5 s, with the wand inside the room near Roshan. *Check:* child finishes VANISH with 1 input; wand at least 120 px wide in the open frame.
6. **Seeded variety** of subject, hat and lane order. *Check:* 3 seeds show 2 or more first lanes.

## 5. Defects
- TRACK accepts early answers; wrong answers advance (section 2).
- ROPE soft-lock (1 of 10 runs). Repro: `reef_play.sh magician child_sim 2 OUT fast 90`: stage ROPE stops at `trace_journey` 0.99963 with `phase_progress` 4.998 vs goal 5.0; the surface ignores input at 0.999 or above (`opera_gesture_surface.gd:1820`) but the world needs 1.0. 604 dead touches in 558 s. Same family as the Ballerina soft-lock.
- ROPE rejects fast swipes at low frame rate (rendered expert-1: 9 re-hints, 13 misses, Bronze; fast expert-2: 1 and 1, Silver).
- One-tap Back exit.

## 6. Limits
Probes used a private copy of the harness. Magic-hat scores from ref_gcompris_a partial runs (its expert runs crashed on a bot exception). Toca Lab and Lost in Play documented only.
