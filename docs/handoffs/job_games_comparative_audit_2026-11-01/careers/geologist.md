# Geologist ("The Crystal Cave Discovery"): comparative findings

Finger path, scripted harness runs on :60. References DOCUMENTED only (MagisterApp dinosaur apps, Tinybop The Earth); PC round pending.

## Measured (ours)
- Expert 31.3 s rendered, 29.5 s fast. Child-sim 38.5, 39.9, 40.6, 42.1 s; 41.0 s rendered. Slow 258.0 s.
- Idle never wins in 90 s (auto-walk opens RIVER at 21.9 s, then 7 re-hints).
- Random tapper: RIVER opened only at 68.7 s; 83 of 229 taps dead; Back exit at 136.4 s.
- 0 dead touches and 0 hints in all 7 non-slow play runs.

| Phase | Expert | Child-sim |
|---|---|---|
| RIVER | 1.6-3.0 s | 2.1-4.8 s |
| FOSSIL | 4.9-5.6 s | 8.9-11.6 s |
| PAN | 3.7-4.0 s | 4.2-5.5 s |
| GEODE | 1.6-2.5 s | 4.0-7.0 s |

- No input possible for 52-53% of the expert session, 37-41% of child sessions; longest wait 2.3-2.6 s.
- Voice: RIVER, PAN and GEODE all say "A secret grotto! The stones want to play!"; FOSSIL says "Brush it back and forth. Swish, swish!", reused from the bathroom. No objective is named for 3 of 4 phases.
- River demo: a white dot of about 24 px moves one 88 px cell from the spring and back; the route to the pool is never shown. Any connected wet path is accepted (`_river_connected` BFS), so a straight swipe works.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 4 | 3 | 4 | 2 | 3 | 4 | 2 | 3 | 4 | 4 |
| MagisterApp Jurassic | DOCUMENTED | 4 | - | - | - | - | - | 3 | 4 | - | - |
| MagisterApp Ice Age | DOCUMENTED | 4 | - | - | - | - | - | - | 3 | - | - |
| Tinybop The Earth | DOCUMENTED | 4 | - | - | 2 | - | - | 3 | - | - | 3 |

Ours: D2 idle and random never win; expert about 30 s vs child about 40 s, same outcome. D3 0 dead touches in play; 36% of random taps dead. D4 no voiced objective for 3 phases; the ghost is a 24 px dot. D5 no struggle seen, so mercy is untested. D7 the same fossil, geode and pan in 10/10. D8 the ammonite and geode are revealed but the finale shows crystals only; a mid-career checkpoint exists (`opera_career_world_2d.gd:5129-5141`, resumed at 759-762). D9 work slab 860x490 px, river cells 88x76, seam radius 56, brush 44-46. D10 PAN needs 9 reversals of 46 px or more (about 2 Hz shaking). The background is code-drawn stripes.
Documented: MagisterApp Jurassic dig, assemble skeletons piece by piece, view in 3D, 5 dinosaurs free (reviewers: most locked, pop-ups); Tinybop erode/deposit/dig layers, "too complicated", made for ages 6-8.

## Where the references are objectively better
1. **A kept, assembled discovery.** MagisterApp skeletons stay viewable. Ours shows the ammonite for about 1 s; it and the geode are absent from the finale and the save.
2. **Variety.** MagisterApp 5 free dinosaurs; Tinybop 4 volcano types. Ours 1 fossil, 1 geode, 1 pan in 10/10.

## Where ours is better (keep)
8/8 play runs complete with 0 dead touches; no paywall or pop-ups; large targets; a mid-career checkpoint; 30-42 s sessions.

## Redesign guide (by impact)
1. **Record voiced objectives for all 4 phases.** *Check:* `phases[].voice` shows 4 distinct keys, each naming the action.
2. **River ghost:** a hand of 120 px or more tracing the whole route from spring to pool. *Check:* idle frame at the first re-hint shows the hand over 3 or more cells.
3. **Show and keep the finds:** fossil and geode in the finale and saved to the castle collection. *Check:* finale frame shows both; save holds both after a non-dev run.
4. **Seeded variety:** 3 fossils, 3 geode colours, 2 river layouts. *Check:* 10 seeds give at least 3 combinations.
5. **PAN: 6 reversals instead of 9.** *Check:* child PAN 4 s or less at no more than 1.5 Hz.
6. **Cut walks between phases.** *Check:* expert no-input share 35% or less (now 52%).
7. **Painted cave backdrop; a hold on Back.**

## Defects
One-tap Back exit (random_tapper seed 1, tap #229); the geologist checkpoint makes it recoverable.

## Limits
References documented only; child-sims never struggled, so mercy is untested.
