# Farmer ("The Piggy Picnic Challenge"): comparative findings

Phases: PLANT (5 seeds, drag or tap the hole), TOSS (pull back and release, 4 throws), HERD (swipe), PICNIC (3 anchored taps). 10 scripted runs; rendered on :58 for expert-1, child_sim-1, idle-1.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 3 | 2 | 2 | 3 | 4 | 3 | 1 | 2 | 2 | 4 | 8/10 completed; expert 29.4/32.4 s vs child 33.8-38.0 s; all 5 child-sims STANDING OVATION; 62-66% of the session allows no input |
| GCompris football | PLAYED | 3 | 5 | 2 | 1 | 1 | 2 | 3 | 1 | 2 | 4 | Pull-drag kick, direction and power decide; expert 3 goals in 36.4/45.9 s; child 1-2 goals, unfinished at 66-71 s; idle: no hint; drag off the 69 px ball gets no feedback |
| GCompris explore_farm_animals | PLAYED | 2 | 3 | 3 | 1 | 2 | 2 | 2 | 1 | 3 | 4 | Tap an animal for photo and sound; expert 90-92 s; child unfinished at 155-162 s; no re-prompt |
| Sago Mini Farm | DOCUMENTED | 3 | - | - | - | - | - | - | - | - | - | Tap the rain cloud to grow crops, feed animals; "no particular activities to complete" |
| LEGO DUPLO World (Farm) | DOCUMENTED | - | - | - | - | - | - | - | - | - | - | Farm mechanics UNVERIFIED |

## Where the references are objectively better
1. **Aim changes the outcome.** Football: expert 3 goals in 5-6 kicks, child 1-2 goals in 7-10. Ours: any pull of 25.5 px or more within about +-57 degrees lands on the same pig (`_farm_release`); TOSS took 8.9 s / 5.0 inputs for experts vs 9.1 s / 5.2 for children. The fixed flight animation (4 x 0.9 s + 3 x 0.42 s = 4.86 s) sets the pace.
2. **Play area.** Football field about 1100x540 px. Ours: PLANT is a code-drawn plot of about 300x150 px with an 84 px tap zone, while Roshan kneels at the large painted 3x3 beds, which do not respond to touch. The painting is letterboxed to about 1040x580, so roughly 35% of the screen is blur.
3. **Effort.** HERD finished 0.4 s after opening with one swipe (open and done frames share timestamp 24.98).
4. **Touch sound.** The farm-animals tap plays the animal's sound; ours: 0 of 101 in-activity actions.

## Where ours is better (keep)
Children finish (5 of 5, mean 35.1 s; football child 0 of 4 in 66-71 s); idle help (auto-walk 20.1 s, re-hint every 9 s; references nothing); short waits (3.6-4.0 s vs football 9.7-10.8 s) and 0 dead touches; gentle misses (a missed vegetable returns; tapping a hole plants directly).

## Redesign guide (by impact)
1. **Aimable toss:** three pigs at different distances; landing follows pull length and angle; a short throw still lands safely near a pig, which waddles over. *Check:* expert and child land on different pigs; landing x correlates with pull length (r > 0.8 in a probe sweep).
2. **HERD as a guided drag:** pigs follow the finger along the lane for at least 3 s; one swipe cannot finish. *Check:* expert HERD at least 2.5 s; idle cannot progress.
3. **Plant in the painted beds on a full canvas** (at least 854x660; holes, seeds, vegetables at least 120 px; a tapped hole flies the seed in). *Check:* probe hit rects at least 120 px; the planted bed shows a sprout in the room.
4. **Sound per action** (seed plop, vegetable crunch, oink and trot). *Check:* 95% within 0.1 s.
5. **Crop continuity and variety:** the planted crop becomes the tossed food, picnic snack and finale prop (today always corn); seeded hole order and pig positions. *Check:* 5 seeds give 3 or more layouts; finale prop matches the crop.
6. **Re-hint at 7 s; a strong hotspot glow** (today a faint ring).

## Defects
One-tap Back exit: random_tapper seed 1 ended at 136.37 s (tap #229 inside Back). Farmer keeps no free-play checkpoint.
