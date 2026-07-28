# Opera acts — the 2-4 minute pacing standard

Owner standard 2026-07-25: **every career act is a 2-4 minute performance with
its own pacing and its own beats.** The previous target was a 1-2 minute show
(`probe_opera_balance` band 55-140s); that band is now **120-240s**.

"Longer" must not mean "more of the same". An act that presses fourteen
candies instead of seven is twice as long and half as good. Each act gets
**three or four distinct beats with different verbs**, in the shape the act's
own accepted `stage_states` / `gameplay` cards already describe.

## Measured baseline (run 687, band 55-140s, 10 simulated children per act)

| Act | median | vs 120s floor | note |
| --- | ---: | --- | --- |
| Ballerina | 51.5s | −57% | |
| Candy Maker | 77.2s | −36% | |
| Curtain Dragon (boss) | 62.0s | −48% | |
| Farmer | 87.5s | −27% | closest to band |
| Boxer | 39.5s | −67% | shortest act in the house |
| Shadow Phantom (boss) | 44.9s | −63% | |
| Midnight Maestro (boss) | 58.4s | −51% | the *grand finale* |
| Pastry Chef | — | — | no data (see below) |
| Detective | — | — | no data |
| Doctor | — | — | no data |
| Magician | — | — | no data |
| Painter | — | — | no data |
| Astronaut Engineer | — | — | no data |
| Racecar Driver | skipped | — | kart engine, own tuning |
| Pop Star | skipped | — | dance engine, own tuning |

**Every act that reported is under the new floor**, most by half or more. The
owner's read was right.

The six with no data were `NEVER-COMPLETED` — all six are exactly the acts with
`shell: true`, stalled in the backstage brawl with zero taps. Fixed in
`fe7230e`: imps spawned outside the corridor `_clamp_player()` lets Roshan
reach (a real gameplay bug on six-imp acts, not just a probe artifact), and the
sim required an arrival threshold the chasing imps make unreachable. Numbers
for all thirteen land on the next run.

## The beat plan

Each act below lists its beats and the accepted cards that specify them, so
this doubles as the art request for the concurrent codex background/texture
work. Beat 0 is the existing backstage imp brawl where `shell: true`.

| Act | Beat 1 | Beat 2 | Beat 3 | Beat 4 |
| --- | --- | --- | --- | --- |
| **Pastry Chef** | bring layers in order (`vanilla/coral/plum_layer`, `recipe_board`) | stir the bowl (`bowl_stirring`, `whisk`) | **bake — load the oven and watch it rise** (`oven_closed`, `oven_open`, `oven_success`) | toppings + **piping ribbon** (`topping_targets`, `piping_ribbon`, `finished_cake`) |
| **Detective** | search the six boxes for three clues (`six_box_display`, `box_wiggle`, `fish_surprise`) | **pin the clues to the case board** (`case_board_empty` → `case_board_complete`) | open the chest, tiara reveal (`chest_pedestal`, `tiara_reveal`) | |
| **Ballerina** | **barre warm-up, two easy steps** (`practice_barre_unit`) | echo rounds (`watch_state`, `repeat_state`, `correct_step_ripple`) | **twirl finale + bouquet** (`twirl_effect`, `curtain_call_bouquet`) | |
| **Candy Maker** | press the batch (`candy_hopper`, `press_platform`, `timing_pointer`) | **wrap them** (`wrapping_station`, `wrapping_swirl`) | **load the parade cart** (`parade_cart`, `parade_arch`, `parade_tableau`) | |
| **Doctor** | **wash hands** (`handwashing_basin`) | four-step checkup (`four_step_board`, listen/warmth/kiss/bandage states) | **the next patient off the waiting bench** (`waiting_bench` — the card implies a queue, not one plush) | recovery tableau (`before_after`, `recovery_tableau`) |
| **Farmer** | feed the piggies (`piggy_approach`, `fed_piggy_hop`) | **the mud-puddle stretch** (`mud_puddle`, `fence_segment`, `hay_stack`) | **barn finale** (`barn_flat`, `piggy_finale`, `sunset_curtain_call`) | |
| **Boxer** | **training-bag warm-up** (`training_bag_rig`) | the rounds (`round_progress_lights`, `imp_peek_state`, `bop_state`, `bell_stand`) | **belt ceremony** (`belt_reward`, `victory_podium`) | |
| **Magician** | hat shuffle rounds (`hat_pedestal_rail`, `watch/swap/selector_state`) | **decoy round with the rolling mirror** (`decoy_state`, `rolling_mirror`) | **cabinet final reveal** (`trick_cabinet`, `final_reveal`, `bunny_fish_reveal`) | |
| **Painter** | ordered swipes (`color_order_board`, pots, loaded brushes) | **rinse between colours** (`rinse_cup`, `rinse_station`) | splat finale (`splat_stamp_set`, `splat_state`) | **frame it** (`framed_sunrise`, `gallery_reveal`) |
| **Astronaut Engineer** | fit the pipes (`pipe_wall`, ghost slots, `workbench`) | spin the valve, build pressure (`valve_spin`, `pressure_lamps`) | **countdown + launch** (`prelaunch_glow`, `bubble_launch`, `rocket_reveal`) | |
| **Racecar Driver** | kart engine — raise to **two laps** (`lap_complete`, `progress_lamps`) | | | |
| **Pop Star** | dance engine — add the **encore verse** (`encore_reveal`) already wished for in the asset request | | | |

## Rules these beats must keep

- No fail states. A missed beat wobbles, giggles and re-shows the answer.
- No reading. Every new beat fires a `_say()` voice line and a visual pointer.
- Beats are *different verbs*, not repetitions of the previous beat.
- A beat that adds a wait (oven, pressure, countdown) must give the child
  something to do or watch during it — never a blank timer.
- New scenery stays inside the `|x| >= 19` / `z <= -15.5` envelope and the
  act-one mobile node budget (`_descendants(act) < 170`).
- Emissive only; no new OmniLights; decorative tiers cull on Speedy.

## Order of work

1. ~~Fix the ruler, set the band~~ — done, `fe7230e`.
2. Re-measure all thirteen acts against 120-240s.
3. Implement beats, shortest act first (Boxer 39.5s, then the three bosses),
   re-measuring after each so the band is hit by content and not by padding.
