# Pop Star (ours) vs. rhythm and echo references: comparative findings

- Build: dev @ 93166ab; harness `reef_play.sh` finger path (device-like `Input.parse_input_event` with touch->mouse emulation); display :56.
- Ours runs are SCRIPTED policies. Rendered (Xvfb :56): expert-1, child_sim-1, idle-1; fast: the rest. Lines in `runs.jsonl`.
- "child-sim-5" fills the replay slot: fresh profile per run; persistence judged from code (career star; echo checkpoint prefix inside a visit, nothing kept between visits).
- References PLAYED by the ref_rhythm agent (`../ref_rhythm/runs.jsonl`, frames `../ref_rhythm/frames/`): Blinken 23.08.5 (Simon), GCompris 4.0 "Melody" (xylophone echo), GCompris 4.0 "Play rhythm" (level 1, 90 BPM). Performous 1.3.0: PARTIAL (3 runs played, 7 UNPLAYED; timing invalid under host load; the ref agent scored it partly from source). Rhythm Heaven: DOCUMENTED only (`../ref_commercial/documented_findings.md`). `ref_rhythm/findings.md` arrived late; its scores and measurements are used below.

## What our Pop Star is today

Seven activities: practice SOUND CHECK (hold), DANCE (tap the lit arrow), RHYTHM (untimed 3-star echo), then on stage the same three again plus ENCORE (circle), with the rival imp racing a mirrored widget (two progress bars in the top HUD). Same as DIAGNOSIS §2 except the action panel is now full-stage art (frames below). Verses are fixed: `[0,2]`, `[0,1,2]`, `[2,1,0]` (`opera_gesture_surface.gd:120`), sung 0.55 s apart, answered "in ANY tempo".

## Measurements

| run | mode | done | game s | inputs | dead | hints | DANCE pr/st s | RHYTHM pr/st s | tier (cheer) | no-input % |
|---|---|---|---|---|---|---|---|---|---|---|
| expert-1 | r | yes | 56.5 | 34 | 0 | 0 | 3.5 / 2.0 | 12.3 / 9.2 | 3 (STANDING OVATION) | 60.5 |
| expert-2 | f | yes | 49.4 | 34 | 0 | 0 | 2.8 / 1.3 | 10.1 / 7.6 | 3 | 64.4 |
| child-sim-1 | r | yes | 82.9 | 45 | 1 | 0 | 7.8 / 4.5 | 25.5 / 14.3 | 2 (STANDING OVATION) | 51.0 |
| child-sim-2..5 | f | 4/4 | 69.5-77.6 | 39-49 | 0-2 | 0 | 6.2-7.8 / 5.0-7.6 | 14.9-21.7 / 10.4-15.8 | 1,1,1,2 (all STANDING OVATION) | 49.5-56.1 |
| slow-1 | f | yes | 526.2 | 34 | 0 | 43 | 103 / 88 | 146 / 118 | 1 (WARM CHEERS, rival first) | 6.0 |
| random-tapper-1 | f | no | 136.4 | 229 | 188 | 2 | - | - | - | 1.2 |
| idle-1 | r | no | 120 (cap) | 0 | 0 | 12 | - | - | - | 2.6 |

- Child-sim mean 75.2 s (5 runs) vs expert 49.4-56.5 s; every completion ends "STANDING OVATION" except slow-1 (tier 1, the rival finished first, nothing restarted).
- Expert runs: no input is possible for 60-64% of the session (demos, voice holds, phase transitions); longest single wait 3.6-4.0 s.
- Idle: auto-walk at 20.2 s; the identical line `op_popstar_sound_check_stage` 13 times (0, 9.2 s, then every 9.0 s); demo = a 25 px dot on a mic about 40x70 px (`frames/popstar_idle_31s_tiny_mic_hold_target.png`). No progress.
- Random tapper: 188/229 taps dead (82%), SOUND CHECK never completes (80 ms taps cannot fill a hold), act exited at 136.4 s by a random tap (shared exit control, see racer findings).
- Targets (from harness tap coordinates and frames): practice echo stars at x 938/1048/1158 (110 px centre spacing; third star's ring cut by the right edge, `frames/popstar_practice_rhythm_star_at_edge.png`); stage stars 133 px apart over painted arrow tiles that are not targets in that phase (`frames/popstar_stage_rhythm_stars_over_arrow_tiles.png`); practice DANCE arrows about 100 px, 130 px apart; practice SOUND CHECK mic about 40x70 px while Roshan stands about 500 px away.

## 1. Scores (0-5; PLAYED vs DOCUMENTED kept distinct)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Ours: Pop Star** | played (scripted) | 2 | 2 | 3 | 3 | 3 | 2 | 1 | 2 | 2 | 3 | Hold/lit-arrow/untimed echo/circle; slow 10-20 s gaps get full RHYTHM credit; 0-2 dead per child run, 82% dead for random; 9 s identical re-prompt; 60-64% no-input for expert, 7 phases with 3 repeats; fixed verses; same cheer at tier 1; 110 px stars, 40 px mic; mostly taps plus a 3.8 s hold |
| Blinken (Simon) | PLAYED (ref_rhythm scores) | 2 | 4 | 3 | 1 | 1 | 2 | 2 | 1 | 4 | 5 | Recall decides (expert round 10, child 1-6); pad lights a median 125 ms after the tap; text "Remember this sequence"; one wrong pad = game over + typed-name dialog; pads about 400x200 px; >= 60% dead time |
| GCompris Melody | PLAYED (ref_rhythm scores) | 3 | 4 | 2 | 2 | 3 | 2 | 3 | 2 | 4 | 5 | Xylophone echo; 118 random taps 0 credit; idle 60 s silent; wrong = same tune again; bars about 150x330 px (`melody_r01_demo.png`); >= 72% dead time |
| GCompris Play rhythm | PLAYED (ref_rhythm scores) | 3 | 5 | 3 | 1 | 1 | 3 | 2 | 2 | 2 | 4 | Timing decides: 0 ms 9/10, +150 ms 1/4, +300 ms 0/6, -150 ms 0/12, same rhythm replayed; text "I am Ready"; drum about 148x65 px |
| Performous 1.3.0 | PARTIAL (timing invalid; D2, D5, D6 mostly from source; ref_rhythm scores) | 3 | 3 | 3 | 1 | 3 | 3 | 1 | 2 | 1 | 1 | Kids drums count any pad; idle lane dropped after 20 misses; text join menus; song clock stalled under host load |
| Rhythm Heaven | DOCUMENTED | 3 | 5 | - | 3 | 4 | - | - | - | - | 3 | Practice rounds; skip after 3 failures; adult-tuned windows |

Means (scored dims): ours 2.3; Blinken 2.5; GCompris Melody 3.0; GCompris Play rhythm 2.6; Performous 2.1 (partial); Rhythm Heaven 3.6 (5 documented dims, not comparable). Reference scores are the ref_rhythm agent's (`../ref_rhythm/findings.md` §1), kept as given so all career agents compare against the same numbers; ours are mine from these runs.

## 2. Where the reference is objectively better

1. **Timing is a real skill (D1, D2).** GCompris Play rhythm judged every tap: on-time 9/10 attempts passed, +150 ms late 1/4, +300 ms late 0/6, -150 ms early 0/12. Ours RHYTHM has no beat: slow-1 answered with 10-20 s pauses between notes and got the same credit as the expert (RHYTHM 146 s / 118 s vs 10.1 s / 7.6 s); DANCE has no timing either.
2. **Random input earns nothing, and the answer is not shown (D2).** Melody: 118 random taps, 0 credit; Blinken: random taps hit game over at 6.0 s. Ours DANCE lights the correct arrow (`frames/popstar_practice_dance_answer_lit.png`): the expert clears 6 arrows in 1.3-2.8 s by following the light, and a wrong lane still pays a progress crumb (`_miss_pay`, DIAGNOSIS §2).
3. **Sequences vary and grow (D7).** Blinken: a new random sequence every game, growing to 10 notes in 75 s (expert). Ours: the same three verses in the same order in all 10 runs, played twice (practice and stage).
4. **Bigger, edge-safe targets (D9).** Blinken pads about 400x200 px; Melody bars about 150x330 px with gaps. Ours: practice stars 110 px apart (under the ~120 px rubric minimum) with the third at the screen edge; the practice hold target is a painted mic about 40x70 px.
5. **Demo tempo inside the child's own tapping band (D4, D6).** Blinken plays every demo note at 364 ms (332-397 ms, n = 135, ref_rhythm §1a). Ours sings the echo stars 0.55 s apart (`opera_gesture_surface.gd`, `echo_show_t = 0.55`), slightly slower than the 300-500 ms band in REFERENCES §5. (Small gap.)

Not a reference advantage: dead time. Blinken (>= 60%) and Melody (>= 72%) waste as much of an expert's session as ours (60-64%).

## 3. Where ours is better (keep these)

1. **No game over:** 8/8 non-idle, non-random runs finished; Blinken ended child-sim-2 at 10.3 s and random at 6.0 s (run logs), then asked for a typed name (`blinken_r03_gameover_nameprompt.png`).
2. **Idle help exists:** voiced re-prompt every 9 s and auto-walk at 20 s. Blinken, Melody and Play rhythm idle runs: nothing for 60 s (`blinken_r09_idle60s_no_rehint.png`, `rhythm_r09_idle_ready_overlay.png`).
3. **A late child is not stuck forever:** ours has no window to miss; Play rhythm's +300 ms child failed 6/6 with the same rhythm replayed and a crash sound (`rhythm_r04_late300_same_tune_again.png`).
4. **Kind error handling:** a wrong star replays the verse with no penalty sound; Melody plays a crash sound and red flash.
5. **No reading:** every objective is voiced; the references use text ("Remember this sequence", "I am Ready", score digits).

## 4. Redesign guide (ordered by impact for a 4-year-old)

Status vs. the Oct 17 spec (`POP_STAR.md`, `SHARED_SYSTEMS.md`): COVERS / CONTRADICTS / MISSES.

1. **Put the echo on the beat with late-leaning windows, and keep the "band waits" floor.** *Spec: COVERS* (BeatKit windows -0.20/+0.32 s; Mercy 2; acceptance 3a). The played reference shows both halves: timing makes it a skill (Play rhythm), and without mercy a late child fails forever (0/6 at +300 ms). Add that reference case as a named regression: a scripted child always +300 ms late completes every section after at most 4 vamps; a child +150 ms late completes without a vamp (inside +0.32 s).
2. **Cut the dead time.** Expert: 60-64% of the session has no possible input (the references are no better: Blinken >= 60%, Melody >= 72%, so this is a target, not a copied advantage). *Spec: MISSES* an explicit budget (it estimates ~90 s and says repeats are music, but sets no measurable limit, and keeps a walk-on, rehearsal and count-in). Add acceptance: in an expert probe run, time that is neither an input window nor a sung call bar is at most 25% of the session, and no silent wait exceeds 3 s outside the count-in.
3. **Drop the practice duplication and the stage-long rival race.** Today 7 phases, 3 played twice; the rival "won" slow-1 and nothing changed. *Spec: COVERS* (SHARED §5, contest drum-off with a real restart).
4. **Targets at least 200 px and inside a safe area.** Today 110 px star spacing, third star cut by the edge, 40x70 px mic. *Spec: COVERS* (drums >= 200x200, positions fixed). Add: every target's hit rect at least 40 px inside the 1280x720 canvas and clear of the 112 px Back button. Acceptance: geometry probe over all states.
5. **Vary the phrases between visits.** *Spec: MISSES / partly CONTRADICTS*: it carries the fixed verses `[0,2]`, `[0,1,2]`, `[2,1,0]` forward; Blinken's per-game random sequence is what makes a replay a new game. Keep 2-3 notes, but draw from a pool (all 2-note pairs and 3-note orders that sound good in the triad), never the same set twice in a row. Acceptance: 10 seeded visits show at least 5 distinct verse sets, all within 2-3 notes.
6. **No answer lights and no crumbs for wrong taps.** DANCE retires; wrong taps credit nothing. *Spec: COVERS* (§10 retires DANCE; principle 5).
7. **Re-prompt at 7 s and escalate.** Today the same line every 9.0 s, 13 times, with a 25 px dot. *Spec: COVERS* the 7 s re-invite with a ghost hand on the next drum; *MISSES* escalation after repeated idling (2nd: hand taps the drum; 3rd: Daddy plays the drum and Roshan points). Acceptance: idle probe sees 3 distinct prompt states in 30 s and no progress.
8. **Celebration must match the show.** Today tiers 1, 2 and 3 all say "STANDING OVATION". *Spec: COVERS* (wordless medals; the band-waited medal).
9. **Never leave a short answer hanging; mark each note.** From the ref_rhythm agent's measured Melody stall (an off-target tap left an answer at 2 of 3 notes and the game waited silently) and Play rhythm's per-note checks. *Spec: MISSES* (no partial-answer timeout; no per-note result). Acceptance (ref_rhythm rec. 2, 3): 2 of 3 correct hits then nothing -> the phrase replays within 3.5 s; the frame 300 ms after an answer shows one wordless mark per cue on its own drum.
10. **Random taps must not exit; probes on the device path.** Shared with Racer and Ballerina: the seed-1 random timeline exited all three careers at 136.4 s; and SHARED §10's `_gui_input` probes skip the touch->mouse emulation path where the Boxer glove defect lives. *Spec: MISSES (exit) / CONTRADICTS (probe path).* Acceptance as in the racer findings, item 6 and 8.

## 5. Defects found (Pop Star)

- **Wrong stars in the wrong place:** stage RHYTHM shows echo stars floating over the painted DANCE arrow tiles, which are not targets in that phase (`frames/popstar_stage_rhythm_stars_over_arrow_tiles.png`); a child may tap the arrows. Repro: `reef_play.sh popstar expert 1 OUT rendered 200`, frame `p06_open_rhythm`.
- **Practice third star partly off-screen** (ring cut at the right edge): `frames/popstar_practice_rhythm_star_at_edge.png`.
- **Rival "wins" without consequence:** slow-1 `performance_result` player_first=false, cheer WARM CHEERS, no restart. Repro: `reef_play.sh popstar slow 1 OUT fast 600`.
- No soft-lock, crash or dead phase seen in 10 runs.

## 6. Limits

- Scripted policies; one finger. No audio device: voice and chimes logged from code, not heard; tap-to-sound latency not measured on our side (Blinken's 125 ms median comes from screen capture).
- Reference scores are the ref_rhythm agent's; its findings.md arrived after my first draft and was folded in.
- Performous unplayed (environment); Rhythm Heaven, Patapon and other console titles documented only.
