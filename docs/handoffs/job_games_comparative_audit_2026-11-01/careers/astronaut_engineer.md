# Astronaut Engineer ("The Rocket Repair Race"): comparative findings

Phases: PIPES (3 boards: drag or tap-place pre-rotated tiles), PATCH (5 taps), VALVE (circles, 1.8 revolutions), LAUNCH (hold 4.5 s). 10 scripted runs; rendered on :58 for expert-1, child_sim-1, idle-1.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 4 | 4 | 2 | 3 | 2 | 4 | 1 | 2 | 3 | 3 | Expert 38.6/56.5 s; child 50.4-54.5 s for 3 of 5; **2 of 5 child-sims stuck 600 s in PIPES**; 0/521 actions with sound |
| PipeWalker 1.0 (10x10) | PLAYED | 4 | 4 | 4 | 0 | 0 | 4 | 4 | 3 | 1 | 4 | Tap rotates a tile; the connected network recolours within one frame of each 300 ms rotation; expert 19.5-20.3 s; child-sim 0 of 4 solved in 60 s; 10 distinct boards in 10 runs; 58 px cells |
| GCompris canal_lock | PLAYED | 4 | 4 | 3 | 1 | 1 | 2 | 1 | 2 | 2 | 5 | Valves and gates raise the water and the boat rides it; order matters; expert 28.9 s; child 2 of 4 won; 3 text pages before input |
| Thinkrolls Space | DOCUMENTED | - | - | - | 1 | 3 | - | 5 | - | - | - | 200+ mazes on 7 planets; unlimited retries; "no instructions or in-game help" (Common Sense Media) |
| Pok Pok Marble Machine / DUPLO Space | DOCUMENTED | - | - | - | - | - | - | - | - | - | - | Mechanics UNVERIFIED |

PipeWalker note: the packaged build scrambles only one tile per board, so the reference agent scrambled every tile before each run; expert play was solver-driven.

Ours: D9 pipe cells 112 px, tray tiles 84 px, on a 712x560 board (43% of the screen); PATCH leaks about 40 px; valve wheel about 60 px; the LAUNCH rocket is a 45x90 px sprite while the large painted rocket stays still. D6 longest wait 2.2-2.3 s; 24-33% of the session allows no input.

## Where the references are objectively better
1. **Instant causality.** PipeWalker recolours the connected network within one frame after each 300 ms rotation, partial progress included. Ours steps fuel every 1.2 s while incomplete, so a correct placement can wait up to 1.2 s to show its effect.
2. **A visible consequence.** canal_lock draws the water level, animates it for 3.5 s and the boat rides it; lights show "gate open". Our VALVE is a 1.8-revolution circle with no visible coolant result.
3. **A rule to discover.** In canal_lock order matters (two valves cannot be open together). Our PATCH, VALVE and LAUNCH have no decision.
4. **Variety.** PipeWalker generated 10 distinct boards in 10 runs; Thinkrolls (documented) 200+ levels. Ours: the same 3 boards (`PIPE_ROUNDS`) in all 10 runs.
5. **Touch sound.** canal_lock valve sound at +0.02 s; PipeWalker on each rotation. Ours: 0 of 521 pipe placements, patch taps, circles and holds started a sound.

## Where ours is better (keep)
In-game help (fuel waits at the gap, the needed cell twinkles after 8 s, a wrong pipe returns after 16 s, voiced prompts); neither played reference ever hints (PipeWalker child-sim 0 of 4 solved; canal_lock slow run not won in 152 s; idle 60 s unchanged in both). Large targets (PipeWalker cells 58 px, canal_lock open-gate stub 50x31 px whose hit box moves). Gradual board steps; no text intro (canal_lock needs 3 text pages).

## Redesign guide (by impact)
1. **Fix the pipe help (soft-lock).** When the next cell is fixed or will not accept the flow, `_pipe_hint_cell()` returns the last non-fixed flow cell; when no tray tile fits, `_pipe_demo_tray_slot()` demonstrates moving the stray on-board tile that fits; the 16 s auto-return also sends back off-path tiles. *Check:* `child_sim 2` and `child_sim 5` finish in 120 s or less; a unit probe with grid SE,H,H,SW / NW,IMP,"",H asserts hint cell 3.
2. **Sound:** pipe click, fuel gurgle per step, patch "tink", valve clicks, rising launch tone. *Check:* 95% within 0.1 s.
3. **PATCH, VALVE and LAUNCH on the painted rocket at 120 px or more;** LAUNCH as 3 staged taps or a drag-up instead of a 4.5 s hold. *Check:* hit rects at least 120 px; no contact over 2 s.
4. **Seeded board variants** (2-3 per round, same difficulty). *Check:* 5 seeds give 3 or more boards.
5. **Show the new rule before board 2** (the imp settles onto its cell).
6. **Fuel advances the moment a correct pipe lands** (150 ms or less) and colours each newly connected segment, keeping the wait-at-gap. *Check:* placement to visible fluid in the new cell 0.3 s or less.
7. **VALVE fills a coolant tank toward a painted line;** a rocket lamp turns green at the line. *Check:* a frame at 50% of the gesture shows the tank half full.
8. **Never move or shrink a hit box when its object changes state** (canal_lock's counter-example). *Check:* the same coordinates register before and after a state change.

## Defects
- **A. Pipe help points at a fixed pipe (soft-lock).** `reef_play.sh astronaut child_sim 2 OUT fast 600`: board 2 ends as grid `["SE","H","H","SW","NW","IMP","","H",...]`, tray `["NE"]`. Flow comes from SW into the fixed exit H at cell 7, which does not accept it; hint and ghost target cell 7 (the demo drop is rejected); auto-return skips fixed cells and resets `pipe_wait_t` to 8 forever. 110 dead touches and 57 re-hints in 600 s.
- **B. Pipe help demonstrates a wrong tile.** `REEF_DEBUG=1 reef_play.sh astronaut child_sim 5 OUT fast 90`: the only SE elbow was dropped off-path on cell 8, so no tray tile fits cell 0; the demo falls back to slot 0 (a wrong tile) and auto-return never removes off-path tiles. (The harness planner never moves the stray; a child might by chance.)
- **C. Unexplained slow VALVE:** rendered expert-1 17.6 s (first circle earned nothing for 12.4 s) vs 3.7 s fast. Not reproduced; probe it.
- **D. One-tap Back exit.**
