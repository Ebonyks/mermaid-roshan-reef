# Reef Grand Prix PC handling study

The published PC race used the Opera child-assist setting of 0.75. At that setting the stick moved a target lane and the controller supplied the full steering command to follow that lane. The kart also accelerated with every input released. A 22% analog deadzone hid light steering and the chase camera eased toward the kart at 7.5/s. A rail contact rotated the body back toward the road.

Nintendo exposes Smart Steering and Auto-Accelerate as distinct driver aids. The PC study uses that distinction to test agency, with manual steering and accelerator input as the default. The comparison uses observable behavior as a reference and makes no claim about Nintendo's internal tuning. [Nintendo driving techniques](https://www.nintendo.com/jp/topics/article/65243d29-a9f1-4c40-a788-34485b9320e0)

## Play the selected build

| Action | Controller | Keyboard |
| --- | --- | --- |
| Steer | Left stick or D-pad | Left/right or A/D |
| Gas | A or RT | W or up |
| Brake, then reverse with gas released | B or LT | S or down |
| Drift | Hold RB while turning at speed | Hold Shift while turning at speed |
| Use an item | X or LB | Space or Enter |
| Pause | Start | Esc |

Hold the drift until the gold tire cue and **BOOST READY**, then release it for a short boost. Braking, a hard rail hit, and pause/disconnect can cancel a drift. After a pause, release held driving controls once to drive again.

## Ten sequential variants

The probe runs in Godot 4.7.2-stable at 60 simulation steps/s on Windows. It compares the published handling path with ten cumulative changes. A fixed straightaway fixture measures heading and speed. A repeatable turn measures drift slip and boost release. The lap driver uses steering, accelerator and brake commands, with the second kart parked. It starts on the grid and earns two laps through the race loop on all four courses. Diagnostic setup states and the route-following test driver serve only the probe. Response times measure simulation steps, with no controller, display, Bluetooth or USB latency included.

| Run | Change from previous run | Measured result and decision |
| --- | --- | --- |
| Baseline | Published lane assist and automatic throttle | Moved 376.43 units in 2 seconds with no input. The chassis turned 2.55 degrees in 10 ticks under a 0.72 steering command. Reversal took 83 ms. Rail contact rotated it 23.3 degrees in one step. |
| 1 | Manual throttle and velocity-based motion | Neutral stayed at 0 units. The same turn reached 14.03 degrees and reversal took 67 ms. Rail contact preserved heading. Head-on recovery timed out beyond 3 seconds. |
| 2 | Analog deadzone 22% to 10% | An 18% stick command reached 0.6 degrees of yaw in 50 ms. It stayed below the threshold for the baseline and run 1. |
| 3 | Faster steering response | Reversal fell from 67 to 33 ms. The turn reached 15.42 degrees in 10 ticks. |
| 4 | More maximum yaw | The 10-tick turn reached 17.45 degrees. Normal side slip increased from 5.15 to 5.83 degrees, which motivated more tire grip. |
| 5 | More normal grip | Side slip fell to 4.66 degrees. All four guided races still finished without touching a rail. |
| 6 | Less grip while drifting | Peak slip rose from 6.72 to 9.89 degrees in the drift fixture. Regular steering kept 4.66 degrees of slip. |
| 7 | Longer coast after gas release | From 220 units/s, speed after 0.75 seconds rose from 111.25 to 136 units/s. The published path accelerated to 300 over the same interval. |
| 8 | Small rebound off the rail | Inward speed after the fixture contact rose from 3.02 to 18.10 units/s. The body kept its heading. |
| 9 | Faster chase camera | The camera reached half of a fixed yaw step in 50 ms, down from 100 ms. |
| 10 | Low-speed steering and earlier drift reward | Drove clear of the head-on rail fixture in 2.00 seconds where runs 1–9 timed out. The medium drift earned a boost. Short and cancelled drifts earned none. Selected. |

## Selected tune in the game

The kart uses the driver's steering and throttle to update heading and velocity. Velocity carries through a turn and grip changes while drifting. The track projection locates the kart, applies shoulder slowdown and rail contact, and tracks progress. At the rail, the normal component of velocity rebounds and the player still owns the heading. Kart-to-kart contact exchanges normal momentum. The PC Imp uses a lower initial pace with the existing retry ramp. The separate Opera story race retains its child-assist driving path.

| Course | Guided two-lap time including countdown | Rail bumps | Largest one-tick progress change |
| --- | ---: | ---: | ---: |
| Playroom Speedway | 27.12 s | 0 | 5.01 units |
| Copper Pan Circuit | 48.15 s | 0 | 5.02 units |
| Seahorse Bridgeway | 93.48 s | 0 | 5.16 units |
| Footlight Finale | 88.05 s | 0 | 5.23 units |

The long courses initially required two Imp restarts in the solo gamepad test. The PC Imp's opening pace was reduced from 0.965 to 0.89. The final solo probe completes every course and also verifies that the Imp can win against a parked player. The same probe checks two independent controllers, item and brake ownership, PC keyboard throttle, P2 completing a race, and cancellation when a controller disconnects.

A seeded two-player stress pass changes throttle, brake, steer, drift, and item requests every 13 ticks for 2,400 ticks on each course. It measured 14,615 kart-ticks at the rail across 19,200 kart-ticks. Position and velocity stayed finite, all four races stayed below one completed lap under those inputs, and peak progress in one tick was 12.95 units on Seahorse Bridgeway. The scripted limits were 124.1 units of lateral offset and 32 units of progress per tick.

## Verification and acceptance

The final build passes 40 actual-PC-scene input checks, 45 original Canal checks, and all 82 trusted game probes across the full suite and one standalone Opera rerun. The full suite recorded a Windows exit 127 before the Opera verdict. The isolated rerun used the same touch settings and returned zero with its complete pass verdict. An earlier suite attempt stopped when Windows ran out of space while writing audio-test fixtures.

Five desktop Forward Mobile frames cover independent throttle, drift, the charged cue and release. No physical gamepads were connected. Physical USB/Bluetooth response, tablet performance, hand-played cornering, observed-child and owner acceptance remain open.

## What to measure in the next handling pass

1. **Physical response.** Compare wired USB and Bluetooth on the same PC using a filmed stick reversal and the first visible yaw change. The current 33 ms number covers the simulation threshold. If the game feels slower in hand, separate controller delivery, frame pacing and display response before changing the steering again.
2. **Corner confidence.** Drive a slalom and one tight turn in each vehicle. Compare brake entry, countersteering, drift release and ability to recover when starting a corner too late. Keep the early manual wall case as a regression.
3. **Tablet separately.** Measure the shipping touch controls, touch-to-screen timing and hands-on comfort on the target device before applying PC tuning to the touch career.

Run the study using the approved Godot executable with `--headless -s scripts/probe_reef_kart_handling.gd`. The [impact record](../../../design/audit_impacts/reef-kart-pc-handling-20261104.json) binds the measured logs, capture hashes and remaining acceptance gaps.
