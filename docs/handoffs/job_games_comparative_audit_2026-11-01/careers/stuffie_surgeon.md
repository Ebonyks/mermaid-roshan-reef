# Stuffie Surgeon ("The Stuffie Surgeon Relay"): comparative findings

Finger path, scripted harness runs on :60. References DOCUMENTED only (Toca Pet Doctor, Dr. Panda Hospital); the PC round is pending.

## Measured (ours)
- Expert 27.5 s (fast). Expert-1 rendered 115.8 s because BANDAGE took 84.9 s with 144 rejected strokes at the low rendered frame rate.
- Child-sim 38.8, 46.6, 48.1, 54.6 s; child-sim-1 rendered 82.1 s. Slow 213.2 s.
- Idle never wins in 90 s: auto-walk at 20 s opens WASH at 21.4 s, then 7 re-hints.
- Random tapper: 196 of 229 taps dead; exited via Back at 136.4 s.
- Child phase times: WASH 3.6-3.9 s, FIND 3.1-4.8 s, X-RAY 1.5-3.6 s, CAST 3.3-4.5 s, BANDAGE 5.8-46.4 s (6-39 rejected strokes).

BANDAGE frame-rate dependence (expert, same 700 px/s trace):

| Frame rate | BANDAGE time | Rejected strokes |
|---|---|---|
| 60 fps | 0.8 s | 0 |
| 30 fps | 0.9 s | 0 |
| 20 fps | 3.2 s | 5 |
| 15 fps | 8.3 s | 15 |

Cause: the route is uv 0.79-0.93 of a 221 px patient rect (`support_career_painted_art.gd:81`), 31 px in x with +-14 px of sine; `_authored_trace_drag` rejects any sample advancing more than 18% (`opera_gesture_surface.gd:1835`), a 5.6 px x-step per frame. Slower frames merge motion into larger steps, which are rejected.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 3 | 3 | 3 | 3 | 2 | 3 | 1 | 2 | 1 | 2 |
| Toca Pet Doctor | DOCUMENTED | 4 | 2 | - | 3 | 4 | - | 4 | 3 | - | 4 |
| Dr. Panda Hospital | DOCUMENTED | 4 | - | 2 | 3 | 3 | - | 4 | 4 | - | 4 |

Ours: D1 FIND is "tap the glowing one", not a diagnosis. D2 idle and random never win; expert 27.5 s vs child 38.8-54.6 s, same outcome. D3 0-1 dead touches in play runs but 86% of random taps get no response (the activity is a small card in the room). D4 5 voiced prompts and a ghost hand; first input at 1.3 s; re-hint 9 s. D5 0 assist events in all runs; BANDAGE never widens. D6 no input possible for 66.5% of the expert session (3-6 s walks between phases). D7 1 patient (a starfish) in 10/10. D8 healed starfish takes the curtain call; no checkpoint, nothing kept. D9 FIND plushies about 75 px, BANDAGE 31x29 px. D10 a 3.6 s continuous hold plus a precision trace.
Documented: Toca Pet Doctor 15 animals, swipe/hold/tap, "slowly wind bandages", no instructions, no points; Dr. Panda Hospital X-ray swipe, magnet, shots, 10 games (3 free), stickers per cure.

## Where the references are objectively better
1. **Variety.** Toca 15 animals, Dr. Panda 10 games; ours 1 patient, 1 sequence in 10/10.
2. **A kept reward.** Dr. Panda stickers per cure; Toca animals can be cared for again. Ours saves nothing, not even mid-career progress.
3. **Bandage leniency.** Toca is documented among the easiest for ages 2-4. Our BANDAGE takes 5.8-46.4 s for a child while the other phases take 1.5-4.8 s, and is 10x slower at 15 fps (reference side documented, not measured).

## Where ours is better (keep)
A spoken objective every phase (both references have "no instructions"); no paywall (Dr. Panda: 3 of 10 games free); 27.5-54.6 s sessions; an immediate re-demo 1.1-1.5 s after a wrong stroke.

## Redesign guide (by impact)
1. **BANDAGE: subdivide the stroke and enlarge the route.** Interpolate previous-to-current in steps of 2% or less before the 18% cap; draw the route across a full-size close-up, 300 px or more. *Check:* `REEF_FPS=15` expert BANDAGE 1.5 s or less with 0 re-hints; child seeds 1-5 at most 8 s; route bbox at least 300 px.
2. **Full-screen close-ups for every task**, targets 140 px or more. *Check:* random-tapper dead share 40% or less (now 86%); FIND plushies at least 140 px.
3. **Mercy escalation.** After 3 rejected strokes double the corridor and slow the ghost; after 6 each stroke advances 20%. *Check:* at most 6 re-hints per child BANDAGE.
4. **FIND as diagnosis.** A symptom animation, then no glow; glow returns after 6 s idle. *Check:* frames show no glow at first, glow at +6 s.
5. **Variety and keeps.** 3 patients x 2 ailments plus a saved sticker wall. *Check:* 10 seeds show at least 3 patients; the save holds stickers.
6. **Re-hint at 7 s (now 9), a doctor checkpoint, a hold on Back.**

## Defects
- BANDAGE frame-rate rejection. Repro: `REEF_FPS=15 reef_play.sh doctor expert 1 <d> fast 300` gives 8.3 s with 15 re-hints.
- One-tap Back exit (random_tapper seed 1, tap #229).

## Limits
References documented only; rendered expert time reflects host load (load average 7-16).
