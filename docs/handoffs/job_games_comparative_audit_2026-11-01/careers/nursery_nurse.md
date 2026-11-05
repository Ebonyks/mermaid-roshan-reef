# Nursery Nurse ("The Moonbeam Nursery"): comparative findings

Phases: WASH HANDS (hold 3.4 s), CATCH BABIES (slide the cradle under 5 babies), FEED (hold 4.0 s), BURP (4 pats at least 0.55 s apart), BEDTIME (3 blanket swipes down). 10 scripted runs; rendered on :58 for expert-1, child_sim-1, idle-1.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 4 | 3 | 2 | 3 | 4 | 4 | 1 | 2 | 2 | 3 | 8/10 completed in 46-74 s; idle never wins; 0/116 in-activity actions got a sound; 392x232 card; fixed lanes |
| GCompris ballcatch | PLAYED | 2 | 4 | 3 | 1 | 1 | 3 | 2 | 1 | 4 | 1 | Needs left and right presses close together; child-sim 1 win / 12-13 losses per 60 s; idle: no change, no hint; ~170 px buttons |
| Sago Mini Babies | DOCUMENTED | 4 | - | - | - | - | - | 3 | 4 | - | 4 | Bottle, tap-and-swipe diaper, bath, burps; dressed-up photo replaces the wall portrait |

Ours: D2 expert 46.2 and 48.2 s vs child 51.0-74.2 s (mean 57.3). CATCH took 19.7 s in all 5 fast play runs (spawn timer sets the pace; slow-1 42.5 s); only rendered child_sim-1 missed babies (3 misses, 32.5 s vs 16.7 s). WASH and FEED mostly 5.3-5.9 s regardless of policy (child_sim-2 FEED 7.45 s; slow 16.8 and 36.0 s). D4 re-hints every 9.0-9.1 s; the room hotspot is a faint ring of about 60 px. D6 longest no-input span 2.55-2.66 s; 37% of the session allows no input. D7 `SPAWN_LANES` is fixed and the 3 baby sprites come in fixed order. D8 the finale shows no babies; the only reward is a star. D9 cribs about 95x55 px, babies 86 px, cradle 116 px. The 2026-09 cyan-band framing defect is gone.

## Where the references are objectively better
1. **Touch sound.** Ours: 0 of 116 cradle drags, pats, holds and swipes started a non-voice sound within 0.3 s; the gesture and catch surfaces contain no sound code. KTuberling: 14 of 14 touches, median 0.172 s. Sago (documented) babies burp audibly; our burp is a silent bounce.
2. **A kept artifact.** Sago keeps a photo on the wall (documented). Ours keeps a star only.
3. **Target size.** Ballcatch about 170 px on a full-screen field; ours 86-116 px inside a card covering 9.9% of the screen.

## Where ours is better (keep)
Idle help (auto-walk at 20.1 s, voiced re-hint every 9 s; ballcatch idle: nothing for 60 s); one finger works (8/8 completed vs about 1 ballcatch win per minute); mercy without failure (after 2 misses babies fall slower, the zone widens, misses land on pillows).

## Redesign guide (by impact)
1. **Ballerina-size canvas for every Nursery phase** (`_apply_panel_layout`). *Check:* surface at least 854x660; every crib, blanket, baby and cradle hit rect at least 120 px.
2. **A sound per accepted pat, catch, stroke, wash and gulp within 100 ms.** *Check:* 95% or more of in-activity actions start non-voice audio within 0.1 s (now 0 of 116).
3. **Replace the holds:** WASH as rub strokes, FEED as tilting the bottle by drag. *Check:* no phase needs more than 2.0 s of continuous contact; expert and child WASH/FEED times differ by more than 20%.
4. **Show and keep the care:** the finale shows the 3 tucked babies; a nursery photo appears on the room wall next visit. *Check:* finale frame shows 3 babies; the save flag and the wall frame exist.
5. **Vary each visit:** seeded lanes and crib order. *Check:* 5 seeds give at least 3 sequences.
6. **Faster, clearer re-hint:** 7 s; hotspot glow at least 120 px with 3:1 contrast. *Check:* idle first hint at 8 s or earlier.
7. **Ghost cradle in CATCH** that slides to the lowest baby's x. *Check:* rendered idle frame shows the ghost moving sideways.

## Defects
One-tap Back exit: Back is a 112 px top-left button that leaves on one tap (`navigation_controller.gd` `press()` calls `_leave_current_activity`); random_tapper-1 ended at 136.4 s. Confirmed by replaying the harness RNG: tap #229 lands inside Back. Nursery keeps no free-play checkpoint, so progress is lost.

## Limits
In fast mode the child cradle never missed; CATCH difficulty comes from one rendered run. Sound measured as player starts under the dummy driver.
