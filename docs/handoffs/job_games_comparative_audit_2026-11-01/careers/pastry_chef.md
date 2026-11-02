# Pastry Chef ("The Castle Bake-Off"): comparative findings

Phases: MIX (pour), STIR (circle, 2 turns), BAKE (oven), FROST (trace), TOP (7 anchored taps) (`opera_career_world_2d.gd:270-275`). Free play uses the generic surface, not OperaChefSurface.
10 scripted runs; rendered on :59 for expert-1, child_sim-1, idle-1. References: KTuberling Pizzeria PLAYED; Toca Kitchen 2, Cooking Mama: Let's cook!, Dr. Panda Restaurant 3 DOCUMENTED.

## Measured (ours)

| Run | Done | Game time | Hints | Result tier | Notes |
|---|---|---|---|---|---|
| expert-2 (fast) | yes | 35.0 s | 0 | 3 | 0 dead touches |
| child_sim-2..5 (fast) | yes | 41.0-43.9 s | 1-2 | 3, 3, 3, 2 | 0 dead touches |
| child_sim-1 (rendered) | yes | 62.4 s | 14 | 1 | FROST 21.5 s |
| expert-1 (rendered) | yes | 80.7 s | 59 | 1 | FROST 43.6 s with 62 traces |
| slow-1 | yes | 256.0 s | 17 | 1 | |
| random_tapper-1 | no | 136.4 s | | | Left via Back |
| idle-1 | no | 75.2 s | 7 | | Reprompt 9.2 s, auto-walk 20.2 s; bowl stays empty |

- MIX took 12.32-12.39 s in every fast run: a 10.4-10.5 s continuous hold, input-invariant, about 29% of an expert session.
- Finale cake region, expert-1 vs child_sim-1: diff 0.000. TOP-done cake differs on 0.4% of pixels (animation only).
- The finale shows a 2-tier pink and purple goal cake; she frosted and topped a 6-tier rainbow cake (expert-1 frames p05_done_top vs finale).
- Oven timing changes only confetti size (`opera_gesture_surface.gd:1055-1058`). Nothing is saved.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 4 | 2 | 2 | 3 | 3 | 3 | 1 | 1 | 3 | 3 |
| KTuberling Pizzeria | PLAYED | 4 | 5 | 3 | 1 | 3 | 5 | 4 | 1 | 2 | 5 |
| Toca Kitchen 2 | DOCUMENTED | 4 | 4 | - | 2 | - | - | 4 | 3 | - | - |
| Cooking Mama: Let's cook! | DOCUMENTED | 5 | - | - | 4 | 4 | 2 | 4 | - | - | - |
| Dr. Panda Restaurant 3 | DOCUMENTED | 3 | - | - | - | - | - | - | 3 | - | - |

Ours: D3 only the MIX completion chime, 0 touch sounds on STIR, BAKE, FROST or TOP in 7 completed runs; D9 bowl about 185x155 px, pitcher 110x95, cake 143x260, 7 anchors in a 125x155 px area with the top two 24-27 px apart; D10 the 10.4 s hold.
Documented: Toca Kitchen 2 (Common Sense Media) 3 guests, 16 foods, tools, guest reactions, "sequence can be complicated"; Cooking Mama finger swirl/stir, Mama demos, no game overs, 30+ recipes, ads every few minutes.

## Where the references are objectively better
1. **Free decorating.** KTuberling: 12 toppings placed anywhere and movable (expert-2, 29.3 s). Ours: 7 fixed anchors; TOP-done cake differs by 0.4% between seeds.
2. **Sound and naming per placement.** KTuberling speaks each item in 0.19 s. Ours: 0 sounds on 7 topping taps.
3. **The thing made is the thing shown.** KTuberling's pizza stays on screen. Ours swaps in a different cake at the finale.
4. **Variety.** Toca Kitchen 2: 16 foods, 3 guests; Cooking Mama: 30+ recipes (DOCUMENTED). Ours: 1 recipe, 1 cake in 10 of 10 runs.
5. **Gestures.** KTuberling accepts tap-to-place or drag. Ours requires a 10.4 s hold for MIX.

## Where ours is better (keep)
- A coherent 5-step transformation; no burn state.
- Voiced prompts and re-hints (references: 0 re-hints).
- 0 dead touches in completed runs (KTuberling 9-11 by their rule, and it silently deleted dropped toppings).
- Closed sessions of 35-44 s.

## Redesign guide (by impact)
1. **Show her cake in the finale** (the frosted, topped tiers instead of goal_chef). *Check:* finale cake crop matches the TOP-done crop and differs from goal_chef.png.
2. **Free toppings.** A tray of 3-4 kinds, each at least 120 px; tap a kind then tap or drag anywhere inside the cake mask; voice or sound per placement; done after 5-7; off-cake drops return without loss. *Check:* two seeds differ on more than 3% of the cake region.
3. **Frosting colour choice.** Three pots before FROST, carried to the finale. *Check:* three choices give three finale hues.
4. **MIX as 3-5 tip-pours.** Each pour banks progress; 5 s or less total; release never loses fill. *Check:* expert MIX 5 s or less; no single hold over 2 s required.
5. **Touch sound** (whisk swish, oven ding, piping squeeze, topping plop). *Check:* sound within 0.10 s of 90% or more of touches.
6. **Fix FROST frame-rate sensitivity** (see defects). *Check:* 10 fps probe 3 s or less with 0 re-hints; rendered expert 5 s or less.
7. **Free-play checkpoint so Back never loses progress.** *Check:* Back mid-TOP then return resumes at TOP.
8. **Later:** a guest who tastes and reacts (Toca Kitchen 2 pattern).

## Defects
1. Back exits with no checkpoint (random_tapper seed 1, about 136.3 s).
2. FROST is frame-pacing sensitive: the rule rejects any drag sample advancing more than 18% of the path (`opera_gesture_surface.gd:1816-1846`). Fixed-fps expert FROST: 60 fps 2.57 s / 0 re-hints; 30 fps 2.5 s / 0; 20 fps 3.5 s / 1; 10 fps 5.3 s / 4. Rendered under host load: 43.6 s / 59. Fix: subdivide each sample along the corridor instead of rejecting large steps. Verify on the tablet.
3. Finale cake mismatch (above).

## Limits
Scripted runs; sound from logs; the cheer tier (the only varying result) drops with slow play but is not a fail state; DOCUMENTED rows are not one-to-one comparable with PLAYED rows.
