# Job games: comparative playthrough audit (2026-11-01)

- **Status:** `SUPPORTING_CURRENT` evidence and `PROPOSED / CANDIDATE` redesign guidance. It grants no
  device, child or owner acceptance and changes no game file.
- **Prepared by:** Claude, as analysis and written guidance only (CLAUDE.md "Claude writes, Codex builds").
  Recipient: Codex, and the owner for the decisions in section 6.
- **Evidence baseline:** `dev` at `93166ab` (2026-11-01).
- **Owner request (2026-11-01):** take the minigame evaluation to the next step: install the well-rated
  comparable games, run sub-agent audits with 10 playthroughs of each reference and of each job game,
  find where the published games are objectively superior, and write a guide to redesign and enhance
  every job game.
- **Readable copy:** the same guide as a Claude doc: https://claude.ai/artifact/McisMmbs3Sii3efXsWFzLy

## 1. Verdict

Across the 15 live Opera careers, the played references beat ours on two dimensions that decide whether
a 4-year-old wants to play again: **agency** (input changes the result; references 3.9 vs ours 2.5) and
**variety** (something changes between visits; 2.7 vs 1.2). Ours already beats them on **onboarding a
non-reader** (3.1 vs 1.2) and **mercy** (3.0 vs 1.9): no reference re-hinted in any idle run, and most
needed reading. Keep our voice-and-ghost-hand teaching; borrow the references' consequences, variety,
per-touch sound and kept creations.

Three careers have P0 blocking defects and four more have P1 defects (section 4). Fix those before any redesign.

## 2. What was played

| Tier | How | Titles |
|---|---|---|
| Played in the cloud | Installed on a virtual display; turn-based games played by screenshot and click, real-time games by scripted input timelines with captured frames | SuperTuxKart 1.4, Extreme Tux Racer, GCompris 4.0 (enumerate, frieze, magic-hat-plus, memory, photo_hunter, ballcatch, clickgame, football, explore_farm_animals, babyshapes, babymatch, melody, play_rhythm, simplepaint/erase/redraw, canal_lock), Tux Paint, KTuberling, Blinken, PipeWalker, Performous (3 of 10 runs played; only the idle run valid for timing) |
| Documented | Official pages, store listings and reviews actually fetched; marked DOCUMENTED and never mixed with played scores | Toca Boca Jr titles, Sago Mini, LEGO DUPLO World, Khan Academy Kids, Hidden Folks, Lost in Play, Dr. Panda, MagisterApp, Tinybop, Thinkrolls, Punch-Out!!, Mario Kart, Just Dance Kids |
| Our game | Godot 4.7.2 build of `dev` driven by `harness/reef_play.gd` through the real touch and emulated-mouse paths, headless and rendered | All 15 careers, 10 runs each (plus diagnostic probes) |
| PC round (pending) | Commercial titles on the owner's PC via computer use | Shortlist in `PC_ROUND.md`; none installed at the time of writing |

The 10 runs per game: expert x2, simulated child x4-5 (500-900 ms reaction, about 25% of taps 40-120 px
off target, occasional wrong choices), slow (10-20 s pauses), random tapper (about 2 Hz), idle. Scoring:
`RUBRIC.md`, ten dimensions 0-5, each with an evidence note. No run was played by a child or a person.

## 3. Scorecard

| Career | Ours (mean) | Best played reference (mean) | Biggest measured gap | File |
|---|---|---|---|---|
| Boxer | 3.5 as designed; 1.8 on the device path | GCompris play_rhythm (2.6) | 0 of 2 clean device-path runs finished; 193 of 207 touches dead | [boxer.md](careers/boxer.md) |
| Geologist | 3.3 | none played | 3 of 4 phases share one voice line; finds not kept | [geologist.md](careers/geologist.md) |
| Teacher | 2.9 | GCompris enumerate (2.7) | 4 answers in a 15 s session (12 in 101 s in the enumerate expert run); random taps solved PATTERN in 29.3 s | [teacher.md](careers/teacher.md) |
| Magician | 2.8 | GCompris memory (3.4) | 0 correct answers in 592 taps still finished TRACK | [magician.md](careers/magician.md) |
| Astronaut Engineer | 2.8 | PipeWalker (2.8) | 2 of 5 child runs stuck 600 s in PIPES | [astronaut_engineer.md](careers/astronaut_engineer.md) |
| Nursery Nurse | 2.8 | GCompris clickgame (3.0) | 0 of 116 in-activity actions made a sound | [nursery_nurse.md](careers/nursery_nurse.md) |
| Detective | 2.7 | GCompris photo_hunter (2.5) | The rival timer wiped 2 placed clues; clues sit outside the painting | [detective.md](careers/detective.md) |
| Farmer | 2.6 | GCompris explore_farm_animals (2.8) | Any aim lands on the same pig | [farmer.md](careers/farmer.md) |
| Candy Maker | 2.6 | KTuberling (3.3) | SYRUP ends on a fixed timed pour (4.99-5.05 s in every fast run), whatever the tilt | [candy_maker.md](careers/candy_maker.md) |
| Pastry Chef | 2.5 | KTuberling (3.3) | Finale cake identical between seeds; 10.4 s MIX hold | [pastry_chef.md](careers/pastry_chef.md) |
| Racecar Driver | 2.4 | SuperTuxKart (1.9) | Hold-only scored 2801, above expert 2719 | [racecar_driver.md](careers/racecar_driver.md) |
| Painter | 2.3 | Tux Paint (3.8) | Painting pixel-identical between seeds; 0 of 63 touches made a sound | [painter.md](careers/painter.md) |
| Stuffie Surgeon | 2.3 | none played | BANDAGE 0.8 s at 60 fps, 8.3 s at 15 fps | [stuffie_surgeon.md](careers/stuffie_surgeon.md) |
| Pop Star | 2.3 | GCompris melody (3.0) | 10-20 s gaps still earn full rhythm credit | [pop_star.md](careers/pop_star.md) |
| Ballerina | 2.3 | GCompris melody (3.0) | 14 of 16 child seeds soft-locked | [ballerina.md](careers/ballerina.md) |

Mean rubric score by dimension, all 15 careers vs the 21 played reference activities (scored by the reference agents):

| Dimension | Ours | References | References minus ours |
|---|---|---|---|
| D7 Variety | 1.2 | 2.7 | +1.5 |
| D2 Agency | 2.5 | 3.9 | +1.4 |
| D10 Gesture fit | 3.3 | 3.8 | +0.5 |
| D3 Touch feedback | 2.7 | 2.9 | +0.2 |
| D6 Pacing | 3.1 | 3.1 | 0.0 |
| D1 Core verb | 3.1 | 3.0 | -0.1 |
| D8 Payoff, kept | 2.1 | 2.0 | -0.1 |
| D9 Readability | 2.7 | 2.2 | -0.5 |
| D5 Mercy | 3.0 | 1.9 | -1.1 |
| D4 Onboarding | 3.1 | 1.2 | -1.9 |

D3 scores credit our voice and visual responses; the measured non-voice sound counts (section 5) are the
sharper evidence that touch feedback is a gap.

## 4. Blocking defects (fix first)

| ID | Career | Defect | Reproduction | Fix direction |
|---|---|---|---|---|
| P0-1 | Boxer | The touch-emulated mouse press reaches `opera_boxing_surface.gd` before its touch and claims glove 0 forever (lines 99, 415, 418, 438-439, 493); GLOVE GUIDE can never finish on the finger path | `audit_local/glove_repro/repro.gd -- variant=shipped` prints `guide_done=[false,true]` (see careers/boxer.md) | Drop every `DEVICE_ID_EMULATION` mouse event, as `kart_canvas_2d.gd:171` does; add a GLOVE GUIDE watchdog. Confirm on the tablet |
| P0-2 | Ballerina | RIBBON TRAIL and GRAND TWIRL stop at progress 0.999x; the surface blocks input at 0.999 but the world needs 1.0; the snap at `opera_career_world_2d.gd:3486` applies only to Chapter 2 phases | 14 of 16 fast child seeds; `REPRO_RIBBON_END=0.9995` locks, `=1.0` completes (careers/ballerina.md) | Snap to 1.0 (or accept 0.999) for every authored trace; never re-prompt while input is blocked |
| P0-3 | Astronaut | The pipe hint and ghost target a fixed pipe that cannot accept the flow; auto-return skips fixed and off-path tiles | `reef_play.sh astronaut child_sim 2 OUT fast 600` (110 dead touches, 57 re-hints) | Hint the last non-fixed flow cell; demonstrate moving a stray tile; return off-path tiles |
| P1-1 | Magician | TRACK pays early taps during the shuffle and pays wrong taps (0.05 each); ROPE has the same 0.999 vs 1.0 lock | probes in careers/magician.md; `reef_play.sh magician child_sim 2 OUT fast 90` | Gate input while `shuffle_t > 0`; wrong taps pay 0; extend the 0.999 rule (`opera_career_world_2d.gd:3638`) |
| P1-2 | Detective | The rival's guided retry sets `phase_progress = 0.0` (`opera_career_world_2d.gd:4822`) and discards placed clues | `reef_play.sh detective slow 1 OUT fast 900` | Keep placed clues; progress never decreases |
| P1-3 | Pastry, Surgeon, Magician | Authored traces reject any drag sample that advances more than 18% (`opera_gesture_surface.gd:1816-1846, 1835`), so FROST, BANDAGE and ROPE slow sharply at low frame rates | `REEF_FPS=15 reef_play.sh doctor expert 1 OUT fast 300` | Subdivide each sample along the corridor before the cap |
| P1-4 | All | One tap on the 112 px Back button ends the career; 10 careers keep no free-play checkpoint (Pastry, Detective, Candy, Surgeon, Farmer, Boxer, Painter, Astronaut, Racer, Nursery; only Teacher, Geologist, Ballerina, Magician and Pop Star do) | random_tapper seed 1 exits all 15 careers at 136.37 s (tap #229 lands inside Back; replayed from the harness RNG) | Require a 1 s hold on Back; checkpoint every career phase |

## 5. Patterns that lift several careers at once

| Pattern | Measured | Reference | Shared fix |
|---|---|---|---|
| Silent touches | 0 of 849 in-activity actions started a non-voice sound in Nursery, Farmer, Candy and Astronaut; Painter none on any task touch; Pastry only the MIX chime | KTuberling 14 of 14 (median 0.17 s); Tux Paint 21 of 21 (median 0.055 s) | A shared touch-sound helper on the gesture and catch surfaces: a sound within 100 ms of every accepted touch |
| Small play card | In Nursery, Farmer, Candy and Surgeon a 392x232 card (9.9% of the screen) with 44-95 px targets; Painter canvas 134x145 px | GCompris ballcatch and babyshapes use 95-170 px targets on a full canvas (other GCompris activities are smaller, which is not a model) | A Ballerina-size surface (854x660 or more) and 120 px minimum hit rects |
| Same every visit | Identical sequence, board, picture or patient in every completed run (fresh profiles) in nearly every career | GCompris reshuffles every run | Seeded variants per visit |
| The made thing disappears | Painter and Pastry finales show stock art (pixel diff 0.000 between seeds); Geologist finds and Nursery babies absent from the finale | Tux Paint kept 12 pictures across relaunch | Carry the child's creation into the finale; save it to an additive key shown in the castle |
| Input does not change the result | Racer hold-only 2801 vs expert 2719; Painter score 950 in 8 of 8; Farmer toss same pig at any aim | SuperTuxKart idle and mashing make 0 progress | Graded, no-fail outcomes that show a different result |
| Long holds and walks | Holds of 3.4-10.4 s (WASH, FEED, LAUNCH, MIX); 15-86% of expert sessions allow no input (Painter 86%) | Tux Paint expert run: longest wait 1.2 s | Short repeated actions; keep phases at one station |

Keep: voiced prompts, ghost-hand demos, the 20 s auto-walk and re-hints (move them from about 9 s to 7 s),
no fail states, and the large targets where they already exist.

## 6. Work order and owner decisions

| Step | Work | Gate |
|---|---|---|
| W0 | Fix P0-1, P0-2, P0-3 with probes from the reproduction lines; verify Boxer on the tablet | Each repro passes; one finger finishes GLOVE GUIDE on the tablet |
| W1 | Fix P1-1 to P1-4 | Repros pass; random_tapper seed 1 survives tap #229 |
| W2 | Shared systems: touch sound, full-size surface with 120 px targets, seeded variants, kept creations, 7 s re-hint | Section 5 checks per career |
| W3 | Per-career top three (careers/*.md), weakest first: Painter, Pastry, Surgeon, then the rest. Racer, Pop Star and Ballerina follow the 2026-10-17 rebuild packet with the corrections in their files | Each file's acceptance checks |
| W4 | PC round: play the commercial shortlist and revise the DOCUMENTED rows | PC_ROUND.md |

Owner decisions this audit needs:
1. Whether kept creations (paintings, cakes, finds, patients) get a shared castle gallery or a per-room display.
2. Whether "graded outcomes" may show a lesser result for weak play (never a failure), as SuperTuxKart and Ball catch do, or whether every outcome stays equal.
3. Which commercial titles to buy or trial for the PC round.

## 7. Files

| File | Role |
|---|---|
| `README.md` | This entry point |
| `RUBRIC.md` | The ten scoring dimensions and the 10-run protocol |
| `careers/*.md` | One findings file per career: scores, measurements, where the reference is better, where ours is better, ranked redesign with acceptance checks, defects |
| `REFERENCES_PLAYED.md` | Reference playthrough findings from the cloud agents |
| `REFERENCES_DOCUMENTED.md` | Commercial reference map and documented scores |
| `PC_ROUND.md` | The PC install shortlist for commercial titles |
| `harness/` | The playthrough harness (`reef_play.gd`, wrapper, usage) used for our 150 runs |
| `.gdignore` | Keeps Godot from importing this folder |

Raw run logs (runs.jsonl per game, about 2 GB of frames) stay in the audit workspace and are summarised
in the career files.
