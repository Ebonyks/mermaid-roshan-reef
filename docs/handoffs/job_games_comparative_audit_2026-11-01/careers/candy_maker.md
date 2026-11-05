# Candy Maker ("The Candy Workshop Cup"): comparative findings

Phases: SYRUP (tilt-pour, about 5 s), SORT (6 drags in the fixed order [0,1,2,2,0,1]), WRAP (circles, 1.8 revolutions), SHARE (6 anchored taps). 10 scripted runs; rendered on :58 for expert-1, child_sim-1, idle-1.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 3 | 2 | 2 | 3 | 4 | 4 | 1 | 2 | 2 | 3 | Expert 23.6/28.3 s vs child 31.9-38.2 s; SYRUP phase 4.99-5.05 s in every fast run; 0/111 actions with sound |
| GCompris babyshapes | PLAYED | 3 | 4 | 2 | 1 | 2 | 4 | 3 | 1 | 4 | 4 | Drag 6 foods onto ~100 px silhouettes; expert 17.7-19.5 s, child 25.6-69.3 s; order differs per run; wrong piece flagged only at OK; idle: no demo |
| KTuberling Pizzeria | PLAYED | 4 | 5 | 3 | 1 | 3 | 5 | 4 | 1 | 2 | 5 | Toppings anywhere on ~720x540; sound 14/14 (median 0.172 s); off-board drops silently deleted |
| Dr. Panda Candy Factory | DOCUMENTED | 3 | 3 | - | - | 4 | - | 4 | 3 | - | - | 60+ designs; friends taste and react; App Store 3.6; iOS only as fetched |

## Where the references are objectively better
1. **Touch sound.** KTuberling 14 of 14 (median 0.17 s); ours 0 of 111 sort drops, share taps, circles and pours.
2. **Variety and choice.** Babyshapes changes order every run (expert-1 starts with baby_bottle, expert-2 with marmelade, replay with orange); KTuberling unlimited placement; Dr. Panda 60+ designs. Ours: one sort order, one mold, the same red candy in every finale.
3. **Target size.** Babyshapes 95-100 px on a 1155x720 canvas; KTuberling pizza about 720x540. Ours: bins 86x63 px with about 30 px icons; the candy is 44 px (84 px grab zone) and spawns over the blurred margin.
4. **Input matters.** The SYRUP phase took 4.99-5.05 s in every fast run (5.35-5.42 s rendered): the pour is timed by a constant (`CANDYMAKER_POUR_SECONDS`, 3.0 s; the pour itself 3.6-3.8 s), not by the child's tilt.

## Where ours is better (keep)
Immediate wrong-bin feedback (candy returns, demo replays; child SORT 9.2-15.2 s vs babyshapes child 69.3 s and 2 OK presses); nothing is ever deleted; voiced re-hints every 9 s.

## Redesign guide (by impact)
1. **One flavour colour and mold choice before SYRUP, carried through** SORT, WRAP, SHARE and the finale; seeded random sort order with the first match highlighted. *Check:* 5 seeds give 3 or more orders; finale candy colour equals the chosen flavour.
2. **Ballerina-size canvas:** bins and candy at least 120 px; candy spawns inside the painted area. *Check:* every hit rect at least 120 px; spawn point within the painted region.
3. **Sound:** glug while pouring, a pitched pop per correct sort, crinkle per wrap turn, "yum" per friend. *Check:* 95% within 0.1 s.
4. **Pour fill proportional to tilt angle and time.** *Check:* SYRUP differs by more than 20% between expert and child.
5. **WRAP as two end-twists** instead of a circle quota. *Check:* no circle quota; each twist visibly tightens one end.
6. **SHARE recipients taste and react** (Dr. Panda pattern). *Check:* each recipient plays a distinct reaction animation and sound.

## Defects
One-tap Back exit (candy random_tapper ended at 136.4 s). No soft-lock seen.
