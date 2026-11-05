# Reference playthroughs (played in the cloud workspace)

Five reference agents installed and played these games on virtual displays on 2026-11-01. Real-time games were driven by scripted bots; turn-based ones by screenshot and click. Mouse or keyboard input, not touch. The sections below are the agents' own findings files, unedited except for heading levels. Raw runs.jsonl and frames stay in the audit workspace.

---

## From `ref_creative/findings.md`

### Creative references: findings (transcribed from the ref_creative agent's report)

Played for real: Tux Paint, KTuberling, GCompris simplepaint/erase/redraw; 10 scripted mouse-input runs each on :55.
Evidence: runs.jsonl, touches/*.json, frames/ (90 PNGs). Latencies are relative only (VM load average 15-16);
Tux Paint slow-1 latencies excluded. Mouse input, not touch.

### Scores (D1-D10, 0-5; "ours" left for the career agent)

| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Rating evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Tux Paint | 5 | 5 | 4 | 2 | 3 | 4 | 5 | 4 | 2 | 4 | 4.36 stars, 1.6M+ Android installs (https://appgoblin.info/apps/org.tuxpaint.android); Linux Journal Readers' Choice Best Kid-Friendly Application 2010, 2011 (https://tuxpaint.org/reviews/) |
| KTuberling | 4 | 5 | 3 | 1 | 3 | 5 | 4 | 1 | 2 | 5 | No award or store rating found (https://apps.kde.org/ktuberling) |
| GCompris simplepaint / erase / redraw | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 2 | 3 | 4 | 4.38 stars, 1.2M+ installs (https://appgoblin.info/apps/net.gcompris.full); Open trophy 2003 (https://gcompris.net/wiki/Press_kit) |

### Where the references are objectively better
1. The child's marks are the artwork: Tux Paint stroke appears 0.027 s after the finger moves, sound within 0.055 s (21 of 21 strokes). Our PAINT reveals a fixed sunrise.
2. Work is kept and shown again: Tux Paint's Open gallery (236x97 px thumbnails) held 12 pictures across sessions; a saved picture was reopened and extended after relaunch. Our GALLERY keeps nothing.
3. Decorating is free: KTuberling Pizzeria takes unlimited toppings anywhere, movable again, each name spoken 0.19 s after pickup. Pastry Chef TOP uses 7 fixed anchors.
4. Two gestures work: KTuberling accepts drag-and-drop and tap-to-pick / tap-to-place.
5. Tap to fill: Tux Paint fills a region in one tap (0.17 s); the Painter prototype needs a 0.22 s hold.
6. The reveal varies: GCompris erase shuffles 6 photos per level; ours is always the same sunrise.

### Where ours is better (references' weaknesses)
- No reference re-hinted in 3 x 60 s idle runs or 37 long pauses.
- Text dialogs block children: one Tux Paint modal ate 14 touches.
- KTuberling lost the creation on quit and silently deleted 2 of 10 toppings dropped off the board.
- Tux Paint at 96 px buttons pushes Undo and Save below a scroll arrow.

### Kid-safety configuration observed
Tux Paint: --noquit --noprint --simpleshapes --uppercase --noshortcuts --buttonsize=64 --autosave --startblank.

### Recommendations (each needs a probe check)
- Paint into a layer instead of revealing a fixed picture.
- Tap-to-fill.
- Save automatically into a gallery wall the child sees again.
- Spoken, instant stamps; never discard a drop.
- 4-6 choices at 120 px or more.

### Pastry Chef and Candy Maker borrowing
- Free toppings inside a cake mask, each name spoken.
- Icing colour drawn by the child's stroke.
- A three-colour flavour choice carried through every candy phase.
- Randomised sort order.

---

## From `ref_rhythm/findings.md`

### Reference playthroughs: music, rhythm and dance (for Pop Star and Ballerina)

Agent: ref_rhythm, display :52, 2026-11-01. Runs: `runs.jsonl` (40 lines). Frames: `frames/`.
"Ours" rows are left blank for the career agents.

What was actually played:

| Reference | Build | Runs | How |
|---|---|---|---|
| Blinken (KDE Simon clone) | Ubuntu 4:23.08.5 | 10 played | Scripted: pad lights read from the screen at about 25 Hz, taps by xdotool. Levels 1, 2 and "?" |
| GCompris "Melody" (xylophone echo, id `melody`) | gcompris-qt 4.0 | 10 played | Scripted: the 5 % bar bounce of each demo note detected by frame difference, answers tapped back |
| GCompris "Play rhythm" (drum in time, id `play_rhythm`) | gcompris-qt 4.0 | 10 played | Scripted XTest timelines synced to the end of the on-screen demo: 0, +50, +150, +300, -150 ms, random jitter, slow, random, idle, replay |
| Performous drums and dance | 1.3.0 | 3 played, 7 UNPLAYED | Songs: self-authored CC0 charts (118 BPM drums and dance, 84 BPM 3/4 dance). The song clock stalled under host load, so no timing result is valid. Timing rules quoted from the 1.3.0 source |

Other GCompris music ids present but not used: `play_piano`, `piano_composition`,
`note_names` (notation reading), `memory-sound` (sound pairs), `instruments`,
`explore_world_music`. `melody` is the call-and-answer one and `play_rhythm` the
keep-a-beat one.

No audio device was present for Blinken and GCompris, so nothing about sound is
judged from listening. Sound statements come from the source (GCompris QML
extracted from its `.rcc` resources) or the installed sound files. Performous ran
against a private PulseAudio null sink.

### 1. Scores (0-5, judged for one 4-year-old on a tablet)

| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours: Pop Star |  |  |  |  |  |  |  |  |  |  | (career agent) |
| Ours: Ballerina |  |  |  |  |  |  |  |  |  |  | (career agent) |
| Blinken | 2 | 4 | 3 | 1 | 1 | 2 | 2 | 1 | 4 | 5 | see 1a |
| GCompris Melody | 3 | 4 | 2 | 2 | 3 | 2 | 3 | 2 | 4 | 5 | see 1b |
| GCompris Play rhythm | 3 | 5 | 3 | 1 | 1 | 3 | 2 | 2 | 2 | 4 | see 1c |
| Performous (partial; D2, D5 and D6 mostly from source) | 3 | 3 | 3 | 1 | 3 | 3 | 1 | 2 | 1 | 1 | see 1d |

### 1a. Blinken evidence
- D1, echo-tap on four coloured pads. It is a memory toy with tones; nothing is played in time.
- D2: idle run 9 saw one flash, then nothing for 58 s. The random tapper (run 8) lost in 6.0 s: 7 of its 8 taps landed during the countdown or demo and were ignored, and the first tap on a wrong pad ended the game. Expert runs reached round 10 in 75 s (runs 1, 2, 10). Child-sim runs ended on rounds 1, 5, 6 and 6 (runs 3 to 6).
- D3: pad lights a median 125 ms after the tap command (p90 136 ms, n = 164; includes about 40 ms of capture period). One response for every correct tap, so there is no good/better/best. Taps during the 2 s countdown or the demo are silent and dead.
- D4: every instruction is written on the notepad: "Press Start to begin", "Remember this sequence...", "Repeat the sequence" (`frames/blinken_r03_demo_flash.png`). Start and level are text buttons. Idle hints seen in 60 s: 0 (`frames/blinken_r09_idle60s_no_rehint.png`).
- D5: one wrong pad ends the game. All four pads flash, a typed "Enter Your Name" dialog opens, then a high-score table (`frames/blinken_r03_gameover_nameprompt.png`, `frames/blinken_r03_highscores.png`). The only mercy is that there is no answer time limit: run 7 waited 10 to 21 s between taps without penalty.
- D6: the demo plays at a constant 364 ms per note (n = 135 intervals, 332 to 397 ms; round 10 is as fast as round 2). The next demo starts about 2.0 s after the last correct tap. In the expert run input was possible at most 40 % of the time, so dead time was at least 60 %.
- D7: levels 1 and 2 grow one random sequence; level "?" draws a new sequence every round (run 10: R, GY, BRB, BBBR ...).
- D8: two-digit LCD round count; the high score needs a typed name.
- D9: four quarter-ellipse pads of roughly 400 x 200 px in a 900 x 720 window, strong colours.
- D10: single taps only.

### 1b. GCompris Melody evidence
- D1: tap xylophone bars to echo a tune. Level 1 uses 2 of the 4 painted bars (the source sets `numberOfParts = 2` below level 3) and 3 notes; level n has n + 2 notes.
- D2: the idle run heard the tune once and then nothing for 60 s. The random tapper made 118 taps and got 0 score ticks. The expert finished level 1 (5 tunes) in about 50 s (runs 1, 2, 10). Child-sims finished 2 to 5 tunes in 80 s.
- D3: a tapped bar shrinks to 95 % and back in 300 ms (`Melody.qml`) and plays its note. That bounce is the only visual and it is hard to see. A second tap on the same bar within 300 ms is ignored. Taps are disabled while the tune plays. A correct answer gets a score tick and a sound (`frames/melody_r01_success_tick.png`); a wrong one gets a crash sound and the red `ErrorRectangle`.
- D4: no spoken instruction in the default install; the voice pack is an optional download offered at first launch, which this run declined. The tune starts by itself 4.3 to 6.0 s after the window appears. The Repeat (lips) button replays it. Idle re-hints in 60 s: 0.
- D5: a wrong answer replays the same tune with unlimited tries and keeps progress, but the tune does not get slower or shorter. A tap that hits no bar leaves the answer short, and the game waits with no prompt. In child-sim run 5 an off-bar tap at 22.2 s left the answer at 2 of 3 notes, and nothing happened until the child started over.
- D6: one tune every 10.0 s (demo starts at 4.7, 14.8, 24.8 and 34.8 s in run 1). Each tune takes 2 s of intro and knock, 3.3 s of tune at 1.1 s per note, about 1.2 s of answer, then about 3.5 s of score animation. Dead time is at least 72 % for the expert and 68 % for a child-sim.
- D7: random tunes; 10 levels that grow longer and add bars.
- D8: a 0/5 to 5/5 counter and a bonus animation. Progress is not kept between launches: run 10 relaunched without `--start-level` and began at level 1.
- D9: bars about 150 x 330 px.
- D10: tap only.

### 1c. GCompris Play rhythm evidence
- D1: tap one drum in time with a red line moving across written notes (quarter, eighth, half at 90 BPM). The child's first tap starts the music, so the first note is always on time.
- D2: the idle run sat on the dimmed "I am Ready" overlay for 60 s (`frames/rhythm_r09_idle_ready_overlay.png`). The random tapper's 97 taps earned no credited rhythm. Timing alone decides the outcome; see the timing table in section 2.
- D3: the drum squashes for 100 ms and a synthesized drum sounds on every tap. After each attempt every note gets a green check or a red mark (`frames/rhythm_r01_success.png`), and a fail plays a crash.
- D4: the instruction is text only ("Follow the vertical line and click on the drum or press space key...") and play starts from a text button ("I am Ready") (`frames/rhythm_r01_ready_overlay_text.png`). There is no voice and no idle hint.
- D5: none. After a fail the same rhythm replays at the same tempo with the same window, without limit: 12 straight fails in 60 s at -150 ms (run 6) and 6 at +300 ms (run 4) (`frames/rhythm_r04_late300_same_tune_again.png`). A BPM stepper exists, but it is a small adult control next to the drum.
- D6: perfect play finished level 1 (3 rhythms) 21.7 s after Ready, at about 7 s per cycle, with input possible for about 1.5 s of each.
- D7: 3 rhythms per level in shuffled order. 9 levels alternate between the moving line and a metronome only.
- D8: an x/3 counter and per-note check marks.
- D9: the drum is about 148 x 65 px, under the 120 px target height. The notation is small.
- D10: tap only, but it asks for quick, exact taps, which young children find hard.

### 1d. Performous evidence (partial)
- Played: the idle drum run, the join flow and menus, and one drum and one dance attempt. The 38.6 s song took about 120 s of wall time, and the dance clock read 00:05 after about 120 s (`frames/performous_dance_r02_clock_stalled.png`; 254 ALSA underruns in the Performous log). No timing result from Performous is valid.
- D2: observed. An idle drummer's lane disappears after 20 missed notes, at game clock 00:22 (`frames/performous_drums_idle_lane_t14.png`, then `frames/performous_drums_idle_dropped_t22.png`). The source sets `death_delay = 20` in `instrumentgraph.cc`.
- D4: observed. "PRESS A BUTTON TO JOIN THE GAME", and a text menu (Ready! / Medium / Lefty-mode / Quit) driven by the I, O, U and P keys (`frames/performous_join_prompt.png`, `frames/performous_drum_difficulty_menu.png`). The chosen difficulty did not carry over from one song to the next.
- D5 (from source, `guitargraph.cc`): drums have a "Kids" difficulty (`frames/performous_kids_difficulty.png`). In it "we don't care about the correct pad", the penalty for a wrong hit is halved because "kids tend to play a lot of extra notes just for the fun of it", and points are computed as if the timing error were half as large. The window stays ±150 ms. Songs never stop early (no fail), but any miss resets the streak.
- D9 and D10: built for keyboards, plastic instruments and dance mats, not touch.

### 2. Where the references are objectively better, and what they show

Timing measured in GCompris Play rhythm (level 1, 90 BPM). Errors are measured
tap to tap against the chart, first note at 0 by construction:

| Timeline | Runs | Attempts | Passed | Notes |
|---|---|---|---|---|
| 0 ms | 1, 7, 10 | 10 | 9 | The one fail had a 271 ms host stall |
| +50 ms, sd 20 | 2 | 4 | 3 | Failed at +81 ms on an eighth note |
| +80 ms, sd 120 | 5 | 5 | 2 | Passed only when both errors were 40 ms or less |
| +150 ms | 3 | 4 | 1 | |
| +300 ms | 4 | 6 | 0 | Same rhythm replayed 6 times |
| -150 ms | 6 | 12 | 0 | Same rhythm replayed 12 times in 60 s |

Why it is this strict: a tap counts if the moving line is inside the next note's
glyph box (`play_rhythm.js` `checkAnswer`). The note boxes are about 70 px wide and
their centres about 168 px apart (measured on screen), so the window is about ±21 % of
the note's length: about ±139 ms for a quarter and ±69 ms for an eighth at 90 BPM.
The window is set in pixels and follows the animation, so it changes with frame rate
and screen size. Performous (from source) uses a fixed ±150 ms on both sides, with 7
dance grades (Perfect under 15 ms, then Excellent, Great, Good, OK, Late/Early, Way
off up to 150 ms).

Advantages that can be measured:

1. **Idle never wins, in every reference.** Blinken (1 flash, then 58 s of nothing),
   Melody (0 ticks in 60 s), Play rhythm (0 attempts in 60 s) and Performous (the
   lane is removed after 20 missed notes). The random tapper never won either:
   Blinken lost in 6.0 s, Melody got 0 ticks from 118 taps, Play rhythm credited 0
   rhythms from 97 taps.
2. **Fast, constant demo tempo in the child's own tapping band.** Blinken plays every
   demo at 364 ms per note (332 to 397 ms, n = 135), inside the 300 to 500 ms band in
   REFERENCES section 5. It does not slow down for longer sequences.
3. **Per-note result after each attempt.** Play rhythm marks each note with a check
   or a cross right after the attempt (`frames/rhythm_r01_success.png`), so a child
   can see which hit was off without reading.
4. **The child starts the clock.** In Play rhythm the first tap starts the music, so
   the first note can never be early or late. It was credited in all 41 scripted
   attempts.
5. **Wrong answers cost nothing.** Melody and Play rhythm replay the same item after
   a wrong answer, with unlimited tries and the score kept.
6. **A real easy mode for young drummers.** Performous Kids drums count any pad, halve
   the penalty and score at half the error (source quotes in 1d).
7. **Simple, large input.** Blinken and Melody are tap-only on targets of 150 px or
   more. Blinken lit the tapped pad a median 125 ms after the tap.

Counter-examples, also measured. Each is a rule our rebuild specs already break, and
should keep breaking:

- **No help after failure.** Play rhythm replayed one rhythm 12 times at -150 ms and
  6 times at +300 ms with no wider window, slower tempo or skip. Melody replays the
  same tune at the same speed. Blinken ends the game on one wrong pad.
- **No idle re-hint.** 0 hints in 60 s in all three GCompris and Blinken idle runs.
  The short-answer stall is the same failure: an off-target tap leaves the answer
  incomplete and the game waits silently (Melody run 5; a discarded Blinken pilot run
  sat 56 s after a tap at (839,152) missed a pad).
- **Reading and typing.** Blinken notepad text, its typed name prompt and its text
  buttons; GCompris "I am Ready" and its instruction text; Performous join text and
  difficulty menu. Melody has no voice unless the optional pack is downloaded.
- **Dead input.** Taps during demos and countdowns get no response. Melody ignores a
  second tap on the same bar within 300 ms.
- **High dead time.** At least 60 % in Blinken and at least 72 % in Melody (expert
  play).
- **Removing the player for idling.** Performous drops the lane after 20 missed notes.

### 3. Where ours is better (keep these)

These come from the rebuild specs read for this audit, not from playing our build.
The career agents should confirm them in play.

- Pop Star's planned echo ("listen, then play it back") keeps the harmless replay that
  Melody and Play rhythm also have. It adds escalating help (ribbons, glow, memory),
  Mercy 1 (wider windows) and Mercy 2 (the band waits). No reference has any
  escalation.
- Pop Star's planned window, 0.20 s early to 0.32 s late, would have credited every
  +150, +300 and -150 ms attempt that Play rhythm failed (18 attempts, 1 passed).
- The Ballerina spec judges no timing at all: Roshan's animation lands on the beat.
  This avoids the strict-window failures above.
- Voiced cues and a 7 s re-invite are specified for both careers. Every reference
  scored 0 re-hints.
- Neither spec has reading, typed input, game over or removal of the player.

### 4. Redesign recommendations (Godot 2D, hard rules respected)

1. **Pop Star: let the child start the answer bar at Mercy 2.** Like Play rhythm,
   treat her first hit on the right drum as beat 1 of the answer, and judge the rest
   against that. Acceptance: a scripted child whose first hit is 0.6 s late, with the
   rest at the right spacing, completes the phrase; a child who is idle or mashes does
   not.
2. **Pop Star echo: never leave a short answer hanging.** If an answer has 1 or 2 of
   its 3 notes and no touch has come for 3 s, replay the phrase with the voice line
   and the ghost hand. Acceptance: a probe that sends 2 of 3 correct hits and then
   nothing sees the phrase replay within 3.5 s and a hint within 7 s. No credit is
   given.
3. **Pop Star: show a result for each note.** After each echo answer or chorus bar,
   put a short sparkle or a soft "dum" mark on each cue's drum (wordless), like the
   Play rhythm checks. Acceptance: the frame 300 ms after the last hit shows one mark
   per cue, each on its own drum.
4. **Pop Star: keep demos inside the child's tempo band.** Call notes go on 118 BPM
   beats (508 ms). Never play a call faster than 330 ms per note (Blinken's floor).
   Acceptance: a chart check confirms every call interval is at least 0.33 s and at
   most 1.0 s.
5. **Pop Star chorus: borrow Performous Kids at the lowest help level.** At Mercy 2
   in choruses only, credit any drum hit inside the window. The echo keeps checking
   which drum. Acceptance: in a chorus at Mercy 2, a scripted child hitting the wrong
   drum on time completes the section; in an echo verse it does not.
6. **Both careers: no dead touches during demos.** Any touch during a demo or call
   gets the drum or Roshan's anticipation response and the "listen" pose, with no
   credit. Acceptance: a probe tapping during a demo logs a sound and motion event
   within 100 ms for every tap and no progress.
7. **Ballerina: keep the no-timing rule, and prove it.** The evidence is the 0 of 18
   passes at ±150 to 300 ms in Play rhythm. Acceptance: probe test 2 in BALLERINA.md
   §11 with offsets of +0.3 s and -0.3 s still completes every step, and the action
   frame lands on the beat.
8. **Ballerina: wait between steps; never drop the dancer.** An idle child must never
   lose Roshan from the stage (unlike the Performous lane drop). Acceptance: with
   120 s of zero input, Roshan stays visible, Lamma re-invites at least 10 times, and
   no step is credited.

### 5. Mapping each objective advantage to Pop Star and to Ballerina

| # | Advantage (section 2) | Pop Star | Ballerina |
|---|---|---|---|
| 1 | Idle and random never win | Applies directly: echo and chorus must not advance on 0 input or 5 Hz mashing (POP_STAR §11 tests 1 and 3) | Applies: tests 1 and 3 in BALLERINA §11. A 5 Hz tapper may complete Point steps only |
| 2 | Demo tempo of 330 to 400 ms per note | Call phrases on 118 BPM beats (508 ms) sit just above Blinken's 364 ms and inside the 300 to 500 ms band. Do not speed calls up as a reward | Lamma's demonstration of a step should take one waltz beat (714 ms at 84 BPM), not a Blinken flash. Use the same no-speed-up rule |
| 3 | Per-note result after each attempt | Marks on each drum after an answer bar (rec. 3) | Not a timing result: each step's bubble shows a glow when the step is done. No marks for timing |
| 4 | Child starts the clock | Mercy 2 phase reset (rec. 1) | Already the model: each step's action starts at touch-down and resolves on the next beat |
| 5 | Wrong answers cost nothing | Echo phrase replays; already specified | A wrong gesture makes Lamma show the step again; already specified |
| 6 | Kids drums: any pad counts | Lowest chorus mercy only (rec. 5). Never in echo verses, where the drum is the memory task | Equivalent: any gesture on Roshan during the ribbon dance counts. Recital steps keep their gesture |
| 7 | Tap-only, large targets, about 125 ms feedback | Drums of at least 200 x 200 base px; response within 2 frames (spec is stricter than Blinken) | Roshan's hit area of at least 260 x 300 px; anticipation frame within 2 frames |

### 6. Why each reference counts as well rated

- **GCompris**: 4.5 of 5 from 39 SourceForge reviews, plus SourceForge's Open
  Source Excellence badge (100,000 downloads)
  (https://sourceforge.net/projects/gcompris/reviews). Its press kit lists it as an
  official GNU project (2002) and winner of best educational software at the 2003
  Open trophy in Soissons (https://gcompris.net/wiki/Press_kit).
- **Performous**: 5.0 of 5 from 9 SourceForge reviews
  (https://sourceforge.net/projects/performous/reviews).
- **Blinken**: weakly rated on its own: 3 of 5 from 3 reviews on the Linux Mint
  community site (https://community.linuxmint.com/software/view/blinken), and no
  SourceForge rating (https://sourceforge.net/app/blinken/). It was played because the
  brief named it as the closest form of the echo. The design it copies, Simon (1978),
  was in Games magazine's "Top 100 Games of 1980" (https://en.wikipedia.org/wiki/Simon_(game))
  and a National Toy Hall of Fame finalist in 2011 and 2012
  (https://en.wikipedia.org/wiki/National_Toy_Hall_of_Fame).

### 7. Limits

- **Host load.** Load average was 5 to 17 on 2 CPUs (other agents) for most runs.
  Blinken and GCompris judge on their own animation clocks, so a stall can loosen or
  tighten their windows. The one 271 ms stall is flagged in the data. Performous's
  audio clock stalled outright, so its runs 4 to 10 are UNPLAYED. Its timing claims
  are documented from source only (`dancegraph.cc`, `guitargraph.cc` and
  `instrumentgraph.cc` at tag 1.3.0 on GitHub).
- **Performous songs.** These are self-authored CC0 click-track charts (118 BPM
  drums and dance, 84 BPM 3/4 dance), built by `make_songs.py` from code. StepMania's
  bundled songs ("Goin' Under", "Springtime", "MechaTribe Assault") were downloaded
  from the StepMania GitHub repository into their own folder, but no per-track licence
  was found there, so they were not played.
- **Audio.** Blinken and GCompris ran with no audio output, so sound responses are
  taken from the source and were not heard.
- **Detection.** Detection is scripted and visual: the Melody demo is read from a 5 %
  bar bounce, which some frames missed under load. Melody expert-2 and child runs 2 and
  3 were rerun for this reason. Melody dead touches were not counted reliably.
- **Startup time.** GCompris took 29 to 48 s to start here under software rendering.
  That time is excluded from every timing above.
- **Level coverage.** Play rhythm attempts after level 1 (metronome mode) are not
  scored. Blinken level 2 played the same as level 1 at our speeds; no time limit was
  found at levels 1 or 2.
- **Not measured.** No reference was tested on a phone or with a child.

---

## From `ref_racer/findings.txt`

### Racer references, actually played: SuperTuxKart 1.4 and Extreme Tux Racer 0.8.3
(Saved as findings.txt: the subagent harness blocks writing findings.md. Content is Markdown.)

Comparison target: our Racecar Driver career, "The Opera Grand Prix" (current build: painted circuit,
770x126 steering bar, Turbo button, 2 laps, hold-to-drive, `scripts/opera_racer_surface.gd`; owner-chosen
rebuild: three-lane side-scroller with auto-drive, `docs/handoffs/codex_minigame_rebuilds_2026-10-17/RACER.md`).
The "ours" row is left blank for the career agent who plays our racer.

**What was played and how (be clear):** 20 playthroughs, display :51, 1280x720 windowed, llvmpipe, no audio.
Every race run was SCRIPTED: a closed-loop bot I wrote (`scripts/stk_driver.py`, `scripts/etr_driver.py`)
reads the screen with mss (road colour for STK, herring blue for ETR) and presses keys through XTest;
slow-1 and random-tapper used timed/random key scripts; idle had no input. Menus were clicked by me.
No human drove. Per-run data: `runs.jsonl`. Frames: `frames/`.

**Settings:** STK: Novice, 1 lap, 4 karts, Tux, Lighthouse (launched with `-N`, which bypasses the track lock),
graphics lowered (dynamic lights, light scatter off, geometry level 2, anisotropic 0, FPS shown). STK ran at
3-11 fps and its race clock at about 0.35x wall time, so child latencies were scaled to 0.5-0.95 s of game time.
ETR: Practice, Bunny Hill (the first course), keyboard; ran at about real time.
STK has no keyboard assist; its touch build has `multitouch_auto_acceleration` (default false) and an on-screen
steering wheel (config.xml), not testable here.

### Why these count as well rated

| Game | Evidence | Source |
|---|---|---|
| SuperTuxKart | SourceForge: 4.9 / 5 from 115 reviews (112 five-star); "Open Source Excellence" badge | https://sourceforge.net/projects/supertuxkart/reviews |
| SuperTuxKart | Google Play: about 4.07 stars, about 10K ratings, about 1.3M installs (third-party tracker, rounded) | https://appgoblin.info/apps/org.supertuxkart.stk |
| Extreme Tux Racer | SourceForge: 5.0 / 5 from 6 ratings; "Open Source Excellence" badge (small sample) | https://sourceforge.net/projects/extremetuxracer/ |
| Extreme Tux Racer | Softpedia editor review: 4, "very good" | https://www.softpedia.com/reviews/linux/Extreme-Tux-Racer--85748.shtml |

### 1. Scores (0-5, judged for one 4-year-old, one finger)

| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Opera Grand Prix) | | | | | | | | | | | (career agent) |
| SuperTuxKart (Novice) | 4 | 5 | 3 | 1 | 1 | 2 | 4 | 3 | 2 | 1 | see notes below |
| Extreme Tux Racer (Practice) | 3 | 1 | 2 | 1 | 2 | 4 | 1 | 1 | 2 | 2 | see notes below |

Evidence notes, SuperTuxKart:
- D1 4: real steering plus accelerate. The kart answers each key at once; item pickups and hits show (`stk_r01_sheet_expert.png`).
- D2 5: idle made 0 progress in 1:39 of game time (`stk_r09_sheet_idle_no_hint.png`). Random tapping, 432 keys, made 0 progress (`stk_r08_...`). The expert bot came 2nd in 72.5 s. 0 of 4 child-sims finished.
- D3 3: the item icon shows top-centre (`stk_r01_item_icon_top_center.png`) and a hit shows dizzy stars. There is no touch-point effect, and audio could not be measured.
- D4 1: the first launch is a privacy text dialog, typing a name, then a text Yes/No for the tutorial (`stk_00_firstrun_privacy_text.png`, `stk_01_tutorial_offer.png`). Tutorial hints are text bars only, with no re-hint during 10-20 s pauses (`stk_r07_*`).
- D5 1: Novice karts run at max speed x0.6 and power x0.7 (`kart_characteristics.xml` "easy"), and the easy AI is speed-capped when ahead (`stk_config.xml` first-speed-cap). But there is no automatic rescue when pinned: 3 of 3 un-coached child-sims were pinned at the first bend by 0:08 and stayed 58-110 s (`stk_r03_*`, `stk_r05_*`). The manual rescue is kind but needs a key (`stk_r06_manual_rescue_bird_sequence.png`).
- D6 2: an expert lap takes 72.5 s. Load to Go is about 12-15 s wall, including a flyover and about 3 s of countdown. A stuck or idle race never ends (r03, r09).
- D7 4: 4 random AI karts per seed, random items, and finishing positions that varied (2nd, 4th). 16 karts (6 locked) and 18 tracks shown.
- D8 3: "You finished the race in rank 2!" and the camera swings to face the kart (`stk_r01_finish_rank_text.png`). The results table is text. Highscore persisted in `highscore.xml`, and locked karts and tracks give collection hooks.
- D9 2: menu icons are large pictures (kart faces about 90 px, the Novice baby penguin about 140 px), but every screen also has text. The HUD rank number sits inside the speed dial, and the minimap is small.
- D10 1: driving needs continuous holds (accelerate) plus continuous corrective steering.

Evidence notes, Extreme Tux Racer:
- D1 3: lean and steer a sliding penguin downhill, one axis plus optional paddle and brake.
- D2 1: idle was the best of all 10 runs, finishing in 58.61 s with 8 herring and 13 pts, "Position 1 in highscore list" (`etr_r09_*`). Engaged bots scored worse: 64.50 s with 4 herring and 0 pts; 74.84 s with 9 herring and 0 pts; 70.59 s with 5 herring and 0 pts.
- D3 2: the herring counter ticks and Tux flops on tree hits. No other contact effect was seen at 2 fps.
- D4 1: player/character select, main menu and help are all text (`etr_00_*`, `etr_01_*`, `etr_02_*`). There is no tutorial. The START banner is visual.
- D5 2: gravity is the mercy, because you always finish. That is autopilot. Event mode adds herring and time thresholds (`events.lst`, Bunny Hill needs 20-23 herring within 37-30 s), so it can be failed; documented only, not played.
- D6 4: there is no countdown and sliding starts at once. Runs last 58-90 s, and loading took about 5-8 s.
- D7 1: the same course and the same herring layout every run. Only time and herring count changed.
- D8 1: a text results box (`etr_r09_idle_finish_results_text.png`) and a camera pull-away. Nothing is made or kept, and persistence is unverified.
- D9 2: the herring are readable on white snow, but the HUD numbers are small and the menus are text.
- D10 2: nothing is required, but steering meaningfully means holding arrow keys.

### Forgiveness measurements (what the brief asked to measure)

| Measure | SuperTuxKart | Extreme Tux Racer |
|---|---|---|
| Steering error | Kart leaves the road and is pinned against a fence or slope. 3/3 un-coached child-sims were pinned within 8 s of game time (`stk_r03/r04/r05`) | Off the fall line into trees or rock, Tux flops and slows but keeps sliding. No pin seen |
| Wall / obstacle | Collision impulse type "normal" (pushes back, `stk_config.xml`). Head-on into a fence = permanent stall | Tree contact: flop and slowdown, then continue |
| Rescue / respawn | Manual key only. Bird lifts the kart and drops it on the road facing forward in about 1-2 s game (rescue duration 1.2 s). 4 rescues in r06 | None, and none needed (gravity) |
| Can the player lose? | Yes: finishing places (2nd, 4th seen). A stuck player never finishes and the race never ends | Practice: no. Events: herring and time thresholds (documented) |
| Item pickup feedback | Gift box breaks, item icon top-centre. Boxes return after 2.0 s (`item-return-time`) | Herring counter +1 |
| Start ritual | Track flyover, then a bird carrying a 3-light signal, "Ready! / Set! / Go!". Pressing in time gives a start boost (`startup time 0.3/0.5 s`, boost 8/4). Pumping during "Set" gave no penalty (`stk_r03_set_go_early_press.png`) | START banner, no countdown. Tux starts by himself |
| Speed presentation | 3D chase camera, speed arc in the rank dial, a column of racer faces in race order, minimap with face icons | 3D chase camera, km/h dial |
| Finish celebration | Rank banner (text) and camera turns to face the kart, then a text table | Camera pulls away, then a text score box |
| Time to first meaningful input | First launch: privacy dialog, name entry, tutorial dialog. Later launches: main menu at about 8 s, then 8 clicks over 5 screens, then about 12-15 s load and about 3-5 s intro and countdown | Menu at about 18 s (including load), 3 clicks, about 5-8 s load, then immediate |

### 2. Where the references are objectively better

1. **Input decides the result (STK).** Idle: 0 m of progress in 1:39 (r09). Random tapping (432 keys): 0 progress (r08). A competent line: finished 2nd in 72.5 s (r01). Our current build finishes both laps on a hold (DIAGNOSIS §4, scorecard C5).
2. **A diegetic, fast, forward-facing recovery (STK).** The rescue bird puts the kart back on the road, facing the right way, in about 1-2 s of game time, with no lost lap progress (`stk_r06_manual_rescue_bird_sequence.png`). The rescue is shown as a character doing something rather than a reset.
3. **A start ritual with a reward for timing and no punishment for eagerness (STK).** There is a flyover, then a character-held 3-light countdown. A press within 0.3 s or 0.5 s of Go gives a boost of 8 or 4, and pumping the pedal during "Set" cost nothing (r03).
4. **Position is visible without reading (STK).** A left-hand column of racer faces reorders live, and the minimap shows faces (`stk_r01_sheet_expert.png`). Our race has no visible standing until the end.
5. **Pickups refill (STK).** Gift boxes sit in rows across the full road width and return 2.0 s after being taken, so a trailing kart still finds them.
6. **Zero dead time from start to motion (ETR).** There is no countdown, and Tux is moving within about 1 s of the START banner (`etr_r09_start_banner_no_countdown.png`). Every run ended in 58-90 s.
7. **Visible, temporary hit reactions (both).** STK shows dizzy stars, and ETR has the belly flop. The kart or penguin keeps going (`stk_r01_sheet_expert.png` around 0:20, `etr_r01_*`).

### 3. Where ours is better (keep these)

1. **No text anywhere in the loop.** Both references need reading from first launch: STK's privacy, name and tutorial dialogs and its text-only tutorial hints; ETR's menus are all text.
2. **No stuck state.** STK left a pinned player for 110 s with no hint, rescue or end (r03). The lane design's "bumps never stop the kart" plus a 3 s glide-and-invite rule avoids this structurally.
3. **Idle does not win (lane design).** ETR is the counter-example: doing nothing beat every engaged policy (58.61 s and 13 pts against 0 pts for all three engaged finishes). RACER.md acceptance test 1 already forbids this, so keep it.
4. **Discrete targets instead of continuous steering.** Continuous steering failed 3 of 3 times for latency-plus-error child-sims in STK, and ETR's continuous herring-seeking was slower than no input. Three tap lanes remove both failure modes.
5. **Short, bounded session.** The lane race targets about 45 s and restarts within 2 s if the imp wins. STK races can run without end when stuck or idle.

### 4. Redesign recommendations (Godot 2D, hard rules respected)

1. **Countdown character and Go boost.** The imp or a friendly fish holds three pearl lights. A lane tap within 0.3 s of "Go" gives a 1.0 s bubble boost, within 0.5 s a 0.5 s boost, and a tap during "Set" has no penalty and gives a normal start.
   *Acceptance:* probe taps at Go+0.2 s and logs a `boost` event; probe taps during "Set" and logs no penalty, with start speed equal to the no-tap start.
2. **Wordless position strip.** Two face medallions (Roshan, imp) at the top-left reorder within 0.2 s when one passes the other, with a pop and a chime.
   *Acceptance:* a scripted pass swaps the medallion order within 0.2 s, and a captured frame shows the order matching the karts' x positions.
3. **Refilling rings.** A boost ring the imp takes reappears within 2.0 s, so Roshan, behind him, still finds it.
   *Acceptance:* the probe logs the ring hidden at contact and visible again in 2.0 s or less.
4. **The guard ETR proves we need.** Auto-drive must never collect a ring or pearl the child did not steer to.
   *Acceptance:* a "never change lane" policy collects at most 1/3 of the pearls and is slower than the scripted engaged child in every one of 10 seeds. Idle for 60 s gives no movement and no result.
5. **Recovery as a character beat, not a reset.** When the kart is slowed by a bump, a helper (a seahorse, say) visibly nudges it back to speed within 0.8 s, like STK's rescue bird but automatic, and with no stop.
   *Acceptance:* across 10 bump contacts, speed never reaches 0, the nudge sprite is visible in the bump frame, and time to recover base speed is 0.8 s or less.
6. **Re-hint cadence (STK's tutorial had none).** After the 3 s glide-and-stop, Roshan's voice invitation plays and then repeats every 6-8 s, with a hand ghost tapping the best lane.
   *Acceptance:* idle for 60 s logs the first invitation at 3 s (plus or minus 0.5 s) and repeats at intervals of 6-8 s.
7. **Finish beat that faces the child.** On crossing, the camera or sprite turns Roshan to face the viewer within 0.5 s (STK swings its camera to the kart's front), then confetti and the trophy.
   *Acceptance:* the finish capture at +0.5 s shows the front-facing pose, and no text appears in the frame.

### 5. Limits

- **Bots, not people.** No race was driven by a human. The child-sims are crude: they have no reverse or recovery behaviour. Their failures measure how forgiving the game is, not how a real child would play.
- **No audio device.** Sound feedback (D3) is unmeasured for both games.
- **Slow STK.** Software rendering ran STK at 3-11 fps and its clock at about 0.35x. Later in the session, other agents' load (load average 12-15 on 2 CPUs) slowed STK to about 0.04x, which invalidated the replay race (r10). Only its menu path and persistence facts are used. STK finished once in 10 runs, so the finish sequence is from r01 only.
- **ETR stability and persistence.** ETR segfaulted about 30 s into r03. ETR's highscore and options files were never written because runs were ended by killing the process, so its persistence is unverified. ETR r05 and r07 finish stats were not captured (finish camera seen, results box missed).
- **STK lock bypass.** The `-N` launch bypassed STK's track lock: Lighthouse is locked in the normal menu flow (`stk_r10_track_select_locks.png`).
- **Untested and unplayed.** STK's Android touch controls (steering wheel, auto-accelerate option) were not testable. ETR event mode (the real fail state) was documented from `events.lst`, not played.
- **Disk.** Raw videos were deleted after frames were cut; ETR stderr logs (about 8 GB of repeated OpenAL errors) were cut to their first 100 lines (`work/*.log.head`).

---

## From `ref_gcompris_a/findings.md`

### Reference playthroughs vs Teacher / Detective / Magician (agent ref_gcompris_a, display :53)

STATUS: FINAL for Teacher and Magician; Detective = photo_hunter final, explore_farm_animals numbers being appended as its last runs finish (section marked).
The "Ours" rows are intentionally blank (another agent plays our careers).

### How the references were played (applies to every section)
- GCompris-qt 4.0 (Debian 4.0-1build3): `gcompris-qt --launch <id> [--start-level N] -w --software-renderer`, 1280x720, private config: virtual number keyboard ON (as on a tablet), background music OFF (so effects and voices can be measured), en_US voice pack present = voices DID play.
- Real play: bots look at screenshots (template/colour/background-subtraction vision; never game internals), decide, and tap with xdotool. 60 protocol runs (10 per reference) + 1 targeted probe. All scripted bot input; nothing is "documented only". Per-run logs: runs.jsonl; raw event logs and (later runs) FLAC audio in raw_logs/.
- Sound measurement: a private PulseAudio null sink was recorded each run; every sound segment was identified by cross-correlation against the game's own .wav/.ogg resources extracted from its .rcc files, so runs.jsonl names which effect/voice played and when (tap_to_audio_s, audio_segments). Sync +/-30 ms via beep markers.
- Visual latency: 15 fps video during each expert-1 run; first changed frame within 60 px of the tap.
- Load times (30-60 s) are software-rendering artefacts of this VM; not used as evidence.
- Policies: expert-1/2, child-sim-1..4 (0.5-0.9 s latency, 25 % taps 40-120 px off target, 12-20 % deliberate wrong choices), slow-1 (10-20 s pauses), random-tapper-1 (2 Hz anywhere, 60 s), idle-1 (60 s), replay-1 (relaunched WITHOUT --start-level to test persistence).
- Limitation of child-sim: it models motor error and wrong choices, not search or comprehension difficulty (e.g. it knows where the photo_hunter differences are).

### Why these references count as well rated
- GCompris: education trophy, Trophees du Libre 2003 (https://mail.kde.org/pipermail/gcompris-devel/2003-May/000954.html); GNU project since 2002, "best educational software at the Open trophy at Soissons" (press kit https://gcompris.net/wiki/Press_kit).
- Google Play net.gcompris.full: 4.3 header / 4.5 ratings section, about 2.17K reviews, 1M+ downloads, rated 3+ (https://play.google.com/store/apps/details?id=net.gcompris.full); AppGoblin 4.38 stars, 2.2K ratings, 1.2M installs (https://appgoblin.info/apps/net.gcompris.full); KDE: https://apps.kde.org/gcompris/
- Tuxmath and gbrainy were launched for a fit check and rejected for Teacher: Tuxmath opens on text menus ("Play Alone", "Math Command Training Academy"...) and is timed typed arithmetic (frames/fitcheck_tuxmath_*.png; https://en.wikipedia.org/wiki/Tux,_of_Math_Command); gbrainy is an adult brain-teaser trainer whose answers are typed into an "Answer:" field (frames/fitcheck_gbrainy_*.png; https://wiki.gnome.org/Apps/gbrainy). Neither has a non-reader counting or pattern mode, so both Teacher slots use GCompris activities.

### Activity ids used
- Teacher: `enumerate` (levels 1-3: count up to 2/3/4 fruit, answer on 0-9 keypad) and `frieze` (level 1 "Copy this frieze", level 2 "Copy and complete this frieze").
- Magician: `magic-hat-plus` (levels 1-4) and `memory` (levels 1-2; flip cards to find the hidden twin = the closest GCompris has to "follow the hidden object"; GCompris has NO shell game / follow-the-hat activity).
- Detective: `photo_hunter` (find the differences, pictures 1-4) and `explore_farm_animals` (level 1 tap every animal in one farm scene, level 2 "click on the farm animal that makes the sound you hear").

=====================================================================
### TEACHER ("The Castle Learning Circle": count, match, complete the pattern)

### 1. Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence (short) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Teacher) | | | | | | | | | | | |
| GCompris enumerate | 2 | 4 | 2 | 1 | 2 | 4 | 4 | 2 | 2 | 4 | numeral keypad; wrong answer silent; 0 re-hints in 60 s |
| GCompris frieze | 4 | 4 | 2 | 1 | 1 | 2 | 3 | 2 | 2 | 4 | builds/continues the whole row; no voice at all; 90 taps/level |

Evidence, enumerate (runs 1-10):
- D1 count fruit, then tap a numeral key (numeral recognition needed). Grouping fruit by drag is possible but never prompted.
- D2 idle 60 s: 0 progress; random-tapper 84 taps: 0 progress, app quit at 46.7 s (hit exit). Expert 4 items in 30.6 s; child-sims 28.7-46.3 s.
- D3 correct key: completetask.wav at median 0.082 s (p90 0.095, n=32), box turns green, score wiggles (visual 0.133 s, expert-1 video). Wrong key: no sound, no motion, the wrong digit just sits on a white box (frames/enumerate_01_expert-1_wrong_1.png). Re-tapping the focused answer box changes nothing: 42/90 measured taps had no visible change at the touch point.
- D4 only voice = generic 4.5 s intro (intro/enumerate.ogg) when the activity opens; per-item objective is text ("Enumerate up to 2 fruit."). No demo. Idle-1: 0/27 screen changes, 0 sounds in 60 s; slow-1 with 25 s gaps: 0 unprompted sounds. No re-hint exists.
- D5 no fail and unlimited retries, but no help, no narrowing, never steps down; strictly linear (4 correct -> next level).
- D6 expert 7.6 s/item; fruit fly in for 1-3 s per item; level bonus 2-3 s then auto-advance.
- D7 11 fruit types, random count and placement each item.
- D8 chime per item; random praise voice per level (8 clips: good/great/awesome/perfect/fantastic/super/waytogo/congratulation) about 2.3 s after the last answer. Nothing kept; replay-1 restarted at level 1 after earlier runs reached level 3 (no persistence).
- D9 keys 123x62 px, answer box 194x96, fruit about 90-110 px. The 106 px exit button sits right above the keypad: child-sim-1 quit the app on its 2nd tap (off-target tap at 322,630; frames/enumerate_03_child-sim-1_correct_1.png is black).
- D10 taps only (focus box then key).

Evidence, frieze (runs 1-10; runs 2-3 re-run after a bot fix, old ones in raw_logs/superseded):
- D1 tap a palette shape; it flies into the next empty slot (0.133 s). Level 2 shows 4 of 8 and the child continues the pattern = real "complete the pattern" (frames/frieze_01_expert-1_complete_task_10.png).
- D2 idle 0 progress; random 110 taps in 61 s: 0 friezes. Expert 9.5 s per 8-token frieze (20 in 189 s; 10 in 98.8 s); child-sims 40-70 s per frieze.
- D3 token taps are silent: 993/1059 taps had no sound within 0.6 s. Only OK makes sound: completetask median 0.065 s (p90 0.103). Wrong = crash.wav + red flash; nothing shows WHICH token is wrong.
- D4 no voice at all (frieze has no intro voice file); text "Copy this frieze." The model row is the only demonstration. Idle 0/27 changes, 0 sounds.
- D5 errors must be found by the child and removed with an X that only removes the LAST token. A child-sim that did not self-check (superseded run 3) failed 7/7 OK presses in 332 s; checking child-sims had 0-4 failed OKs.
- D6 a level = 10 friezes x 9 taps; child-sims needed 202-348 s for half a level (5 friezes); slow-1 did 3 friezes in 455 s.
- D7 random 2-shape AB patterns, palette order shuffled per item, 14 levels; level 3 adds memorise-then-copy behind a TEXT button "I am Ready" (frames/frieze_obs_level3_text_button_I_am_Ready.png).
- D8 chime per frieze, praise voice per level; the built row vanishes.
- D9 palette cells 83x83 px at 84 px pitch; OK and undo 83 px. Off-target child taps often landed on the neighbouring token (11-16 off-target taps per child run).
- D10 taps only, but 8 accurate taps in a row per item.

### 2. Where the references are objectively better
1. Pattern depth: frieze level 2 makes the child place all 8 tokens and continue a half-shown row; expert 9.5 s/row, child about 40-70 s/row. (Our design doc: pattern "only asks for the next item".)
2. Answer-sound latency: 0.065-0.082 s median, p90 at most 0.103 s on every accepted answer.
3. Per-item variety: new fruit type (11), count and placement on every enumerate item; frieze shuffles palette order every item, so the correct choice is never at a fixed position.
4. Tokens visibly travel from palette to slot (0.133 s), linking the choice to its destination.

### 3. Where ours is better (keep) - measured reference weaknesses
1. Zero re-hints: 0 sounds and 0 screen changes over 60 s idle in both; slow-1 gaps of 22-25 s produced nothing. Ours has an idle reminder.
2. Wrong answers: enumerate is silent and motionless; frieze plays a crash without locating the error. Ours points with golden help and keeps counted state.
3. No spoken per-item objective (frieze: no voice at all; enumerate: only the generic intro).
4. No persistence: relaunch restarts at level 1.
5. Chrome next to play targets ends sessions (enumerate child-sim-1; enumerate random-tapper at 46.7 s).
6. Counting is answered with written numerals on a keypad.

### 4. Redesign recommendations
1. Add a "continue the row" pattern item after 3 clean next-item wins: 4 of 8 tokens shown, each tap flies a token into the next slot within 0.15 s with a voiced token name; auto-check on the last slot (no OK). Acceptance: probe taps 4 tokens; each tap yields a sound event <=100 ms and the slot index advances; completing the row triggers the existing celebration without an extra button.
2. Wrong token = that slot shakes and the token returns to the palette; earlier tokens stay. Acceptance: probe puts a wrong token in slot 2 of 4; within 0.5 s only slot 2 is empty and a help voice plays; 0 progress lost.
3. Shuffle target and distractor positions per item. Acceptance: over 10 items the correct card occupies every position at least twice.
4. Keep any exit/menu control at least 150 px from every lesson target and require a hold or two-step for exit. Acceptance: probe asserts min rect distance >= 150 px; a single tap on exit never leaves the lesson.

### 5. Limits
- Load time unmeasurable (software rendering). Voices were the downloaded en_US pack; on a fresh offline tablet GCompris would have no voices until it downloads them.
- Frieze child-sim runs used a 5-frieze cap (half a level) to keep each run under about 6 min.

=====================================================================
### MAGICIAN ("The Grand Illusion Duel": follow the hat through a shuffle, cabinet reveal)

### 1. Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence (short) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Magician) | | | | | | | | | | | |
| GCompris magic-hat-plus | 2 | 4 | 2 | 1 | 2 | 3 | 3 | 2 | 1 | 4 | stars stay counted on screen; 32 px answer cells; hat 60 px from exit/help |
| GCompris memory | 3 | 4 | 4 | 2 | 3 | 4 | 3 | 2 | 4 | 5 | hidden-location recall; flip sound at 0.002 s; 188x268 px cards |

Evidence, magic-hat-plus (runs 1-10 + probe run 99):
- D1 tap hat, stars fly under it, then tap answer stars and OK. The counters above stay lit the whole time, so it is visible addition, not "where did it go" (frames/magic-hat-plus_03_child-sim-1_hat_closed.png).
- D2 idle 0 progress; random 111 taps in 61 s: 0 questions. Expert 4 questions, child-sims 48-63 s for 3.
- D3 hat tap -> star-flight sound (smudge.wav) about 0.55 s later; answer-star taps silent (199/216 taps had no sound within 0.6 s; star just turns gold); correct OK -> praise voice about 0.6 s, then next level.
- D4 5.2 s intro voice (intro/magic-hat-plus.ogg) + text "Click on the hat to begin the game"; no demo; idle 0/29 screen changes, 0 sounds.
- D5 no fail; wrong answer -> see probe below (try-again voice, no correction help); no step-down.
- D6 hat animation 2.4-5.5 s per question with no useful input (dead time); one question per level.
- D7 random counts per question; 8 levels.
- D8 praise voice from 8 clips + flower per level; nothing kept.
- D9 answer cells 32x32 px at 38 px pitch. The hat (about 90x115 px at 240,530) is about 60 px above the help and exit buttons: child-sim-3's stray tap opened a full-screen TEXT help dialog that blocked play for the rest of the run (frames/magic-hat-plus_05_child-sim-3_after_wrong_1.png); child-sim-4's stray tap at (249,640) quit the app after 1 question.
- D10 taps only.

Evidence, memory (runs 1-10):
- D1 flip a card, remember where its twin is hidden; level 1 = 6 cards, level 2 = 8.
- D2 idle 0 progress; random-tapper quit the app after 24 taps (13.4 s). Expert-2 6 cards in 23.4 s (0 mismatches); child-sims 31-38 s with 1-2 mismatched turns.
- D3 card_flip.wav at median 0.002 s after the tap (n=71, p90 0.031), card visibly turns; a matched pair plays win.wav and both cards vanish; a mismatch flips back after about 1.5-2 s with no error sound.
- D4 2.3 s intro voice; no demo; idle 0/28 changes, 0 sounds.
- D5 no fail, mismatches cost nothing; no hint after repeated misses.
- D6 23-38 s per level, then flower bonus and auto-advance.
- D7 shuffled positions and pictures each run.
- D8 big flower bonus + praise voice per level (frames/memory_01_expert-1_level_1_end.png); no keepsake; replay starts at level 1.
- D9 cards 188x268 px (largest targets in this audit); bottom row ends about 40 px above the bar.
- D10 single taps.

### 2. Where the references are objectively better
1. Memory: every tap answered by sound in 0.002 s median (p90 0.031 s) and a visible flip; card targets 188x268 px.
2. Memory hides the object and asks for its location after a delay = real object permanence. (Our TRACK keeps the answer glowing and accepts taps during the 1.5 s shuffle, per OPERA_MECHANICS_REAUDIT.)
3. Memory and magic-hat block answers until the reveal finishes: magic-hat accepts no answer during its 2.4-5.5 s flight (the answer row only matters after "?"), the gating our TRACK lacks.
4. Positions randomised every run (memory), so replay does not teach coordinates.

### 3. Where ours is better (keep)
1. Theatrical arc (vanish, track, rope, cabinet, portal) vs one repeated mechanic per activity.
2. Re-hints and voiced per-step guidance: references 0 sounds / 0 changes in 60 s idle.
3. Large single-object targets for the trick itself vs 32 px answer cells.
4. Bar chrome next to the hat broke 2 of 4 magic-hat child-sim runs (text dialog / app exit).

### 4. Redesign recommendations
1. TRACK: hide the subject under one of 3 hats, shuffle, accept taps only after the shuffle ends, and remove the glow during the child's turn. Acceptance: probe tap during shuffle = 0 progress and no sound of success; tap after shuffle on correct hat = success sound <=100 ms.
2. Wrong hat: lift that hat to show it is empty, then lift the correct one slowly and replay the shuffle at half speed; never fail. Acceptance: probe wrong tap -> empty-hat reveal within 0.3 s, correct-hat reveal within 1.5 s, next attempt shuffle duration >= 2x previous.
3. Randomise start lane and swap sequence per attempt. Acceptance: 10 probe replays produce at least 3 different start lanes and at least 5 distinct swap sequences.

### 5. Limits
- magic-hat-plus wrong-answer behaviour comes from the targeted probe (run 99 in runs.jsonl; frames magic-hat-plus_99_*); no child-sim produced a wrong OK by chance.
- GCompris has no follow-the-object shuffle; memory is the nearest analogue.

=====================================================================
### DETECTIVE ("The Two-Detective Mystery": room-scale lens search, clue dragging, evidence board)

### 1. Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence (short) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Detective) | | | | | | | | | | | |
| GCompris photo_hunter | 3 | 4 | 4 | 1 | 1 | 4 | 1 | 2 | 1 | 4 | 8-97 px difference boxes; miss = brick sound + mark at the tap; same picture every launch |

Evidence, photo_hunter (runs 1-10):
- D1 search two pictures and tap each difference; on a hit the difference appears on both pictures and circles mark it (frames/photo_hunter_01_expert-1_first_found.png).
- D2 idle 0 progress; random-tapper 110 taps found 2 differences by chance (51 misses) but completed no picture; expert-2 picture pair in 21.1 s; child-sims 25-29 s for 2 pictures.
- D3 hit -> bleep.wav median 0.002-0.009 s; miss -> brick.wav plus a mark at the tap point (frames/photo_hunter_06_child-sim-4_miss_feedback.png); found-mark visual about 0.4 s (fade).
- D4 3.8 s intro voice; text instruction; no demo; idle 1/27 changes (start-up settle only), 0 sounds. The hint (lightbulb) button opens a slider overlay but is never offered.
- D5 no fail, unlimited misses, but no automatic help; no step-down.
- D6 about 7-15 s per picture for an expert; 2-4 differences each.
- D7 10 fixed pictures in fixed order; replay-1 got the same first picture and the same 3 differences as every other run.
- D8 praise voice per picture; nothing kept.
- D9 difference hit boxes from the level data x 451 px card: picture 1 = 62x62, 14x14 (hit area clamped to about 20 px), 47x32; picture 4 = 27x13, 8x20, 71x21, 39x33 px. Far below 120 px.
- D10 taps only.

Note: the explore_farm_animals sound-search runs for Detective were still in progress when this file was committed; they are not scored here.

### 2. Where the references are objectively better
1. Miss feedback at the touch point: photo_hunter answers every miss with brick.wav and a mark where the finger landed (child-sims: every off-target tap answered), ours only scores dwell on true clues.
2. A found item changes the scene permanently (difference appears + circle stays; farm animals get a gold star where tapped, frames/explore_farm_animals_01_expert-1_after_discover.png) so progress is readable in the room itself.
3. Hit sound latency 0.002-0.009 s median.

### 3. Where ours is better (keep)
1. Targets: photo_hunter differences 8-97 px (several under 30 px) vs our room-scale clues; photo_hunter would fail the 120 px guide by a factor of 4-15.
2. Re-hints: 0 unprompted sounds/changes in idle and in 20 s slow gaps for both references; ours escalates after 12 s.
3. Evidence board (drag clue to destination) has no counterpart in the references (tap-only).
4. Variety: photo_hunter is a fixed picture sequence; ours already plans clue-set variation.

### 4. Redesign recommendations
1. Every off-target lens dwell or tap gets a soft "nothing here" sound and a small mark at the touch point; repeated misses in the same area (3 within 5 s) trigger the existing glisten on the nearest clue. Acceptance: probe tap on empty floor -> sound <=100 ms and a mark at the tap; 3 misses -> clue glisten within 0.5 s.
2. Found clues leave a permanent in-room marker (star/stamp) until the case ends. Acceptance: after finding clue 1, screenshot at +10 s still shows the marker at the clue position.
3. Add a voiced "find the thing that makes this sound" clue (farm level-2 pattern): play a sound, the child finds its source in the room; repeat button always visible. Acceptance: probe plays clue sound; tapping the source within 3 tries completes; repeat replays within 100 ms.

### 5. Limits
- Child-sim knows where differences/animals are; it measures motor error, not search difficulty. The 8-20 px photo_hunter differences would be much harder for a real 4-year-old than these runs show.
- explore_farm_animals sound identification by the bot used audio correlation with occasional failures ("sound-id failures" in notes); the bot then used the repeat button, which is also what a child can do.

---

## From `ref_gcompris_b/findings.md`

### Reference playthroughs (GCompris 4.0 + PipeWalker 1.0) vs. Nursery, Farmer, Candy Maker, Astronaut

Agent: ref_gcompris_b, display :54. Rows for "ours" are left blank on purpose; another agent plays our careers.
Where a comparison to ours is made, ours is cited from audit/OPERA_MECHANICS_REAUDIT_2026-09-05.md (code-derived), not from play.

### How runs were made (honest scope)
- GCompris 4.0 (Debian 4.0-1build3), `gcompris-qt -f --software-renderer -s --launch <id> --start-level 1`, 1280x720 Xvfb, llvmpipe.
  Cold start to first frame: 40-60 s on this box (software rendering; not representative of a tablet).
- Input: xdotool mouse (= one finger). Sound: an isolated null-sink PulseAudio server on /tmp/xdg54 was started midway
  (after ballcatch/clickgame/football runs), so sound-onset latencies are measured from recordings for farm, babyshapes,
  babymatch, canal lock and one football probe; for ballcatch/clickgame sound events are taken from source code.
  Capture calibration: 3 test beeps at known times were detected within 20 ms.
- Source read for rules/timings: GCompris tag V4.0 (github.com/KDE/gcompris), PipeWalker tag v1.0 (github.com/artemsen/pipewalker).
- Policies per RUBRIC: expert-1/2, child-sim-1..4 (500-900 ms latency, 25% taps off by 40-120 px, wrong choices 10-30%),
  slow-1 (10-20 s pauses), random-tapper-1 (~2 Hz), idle-1 (60 s), replay-1.
- Scripted/oracle parts, stated plainly:
  - ballcatch: Qt MultiPointTouchArea under Xvfb mouse emulation does not register a second, later tap on the other hand
    (verified: gaps 50/200/400/600 ms all lost; only same-xdotool-call taps registered). Child/slow runs therefore send the
    two "hand" taps as Left/Right arrow key events with the child's timing (same code path, ballcatch.js processKey);
    off-target taps are judged against the measured hand boxes. Expert/replay runs used real mouse taps in one xdotool call.
  - clickgame: fish located by frame differencing; score read by OCR (unreliable on levels 3+, so dead-touch counts there are approximate).
  - explore_farm_animals quiz: the "child knows the sound" oracle is a spectral fingerprint of each animal's sound recorded in
    the explore phase, matched against the recorded question sound (9/9 correct in all expert runs, confirmed by the 1/9..9/9 counter).
  - babyshapes/babymatch: tray pieces identified by an image-feature classifier; "pieces_flagged_wrong" in runs.jsonl comes from my
    placement model and can undercount (frame bs_child-sim-1_flagged.png shows 2 red X marks where the model logged 1).
- Activity ids used: `ballcatch`, `clickgame` (Nursery); `football`, `explore_farm_animals` (Farmer); `babyshapes`, `babymatch`
  (Candy Maker); `canal_lock` (Astronaut, partially played, see Astronaut limits); `/usr/games/pipewalker` (Astronaut, see limits).

### Why these references count as well rated
- GCompris: received the award for best educational software at the Open trophy in Soissons (2003), is an official GNU project,
  and is described as a Unesco "treasure of the world" (https://gcompris.net/wiki/Press_kit). Google Play listing
  net.gcompris.full: 4.38 stars from 2.2K ratings, 1.2M installs (https://appgoblin.info/apps/net.gcompris.full).
  SourceForge: 4.5/5 from 39 reviews (https://sourceforge.net/projects/gcompris/). Audience stated as children 2-10.
- PipeWalker: SourceForge 5.0/5 from 5 reviews (https://sourceforge.net/projects/pipewalker/reviews); Linux Mint community
  7 reviews, six 5s and one 4 (https://community.linuxmint.com/software/view/pipewalker). Small sample; it is a well-liked
  adult/teen puzzle, not a preschool title, and is scored here against the 4-year-old audience.

---------------------------------------------------------------------------------------------------

### Nursery Nurse ("The Moonbeam Nursery") vs. ballcatch and clickgame

### Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Nursery) | | | | | | | | | | | (other agent) |
| GCompris ballcatch "Make Tux catch the ball" | 1 | 3 | 3 | 1 | 0 | 2 | 1 | 2 | 3 | 1 | Verb is "touch both hands within a window", not catching; L1 window 900 ms, L2 350 ms (ballcatch.js). Child-sim 4/4: 1 win at L1 then 12-13 straight losses at L2 in 60 s, no easing (runs 3-6). Idle 60 s: 0.00 mean pixel change, no hint (run 9). |
| GCompris clickgame "Click on me" (fish) | 3 | 4 | 3 | 2 | 3 | 4 | 3 | 2 | 2 | 4 | Tap moving fish. L1 (5 fish) cleared expert 5.8/6.9 s vs child 15.2-20.7 s; L2 cleared child 38-57 s (runs 1-6). Fish bounce forever, misses free. Fish 94-405 px wide but 53-152 px tall (f01 = 96x76). Idle: fish swim, nothing advances (run 9). |

D-evidence detail:
- ballcatch D3: tapped hand slides immediately; "smudge" only on the second hand; the ball does not fly until the window timer
  expires (900 ms at L1), flies 1.0 s, then 0.5 s pause, then tux_good/tux_bad image + random voice; next attempt possible at
  about 3.0 s after the tap (contact sheet of 16 frames at 250 ms; level digit changes at frame 11 = 3.0 s). Lose frame: frames/bc_child-sim-1_lose.png.
- ballcatch D4: text-only intro ("Press left and right arrow keys at the same time...") that must be closed with a text "Start" button (320x90 px); keyboard arrow pictograms are drawn but are not touch targets.
- ballcatch D10/D2: two simultaneous touches are required past level 1. Experts (single-call taps) cleared L1-L6/L7 then failed every attempt at L7 (60 ms) / L8 (30 ms) for the rest of 75 s (runs 1, 2, 10: wins 6, 7, 4). There is no end state; levels wrap.
- ballcatch D9: hands 155x210 px (frame bc_child-sim-1_lose.png). Random tapper: 4 of 98 taps hit a hand (run 8).
- clickgame D3: hit = drip.wav + fish fades 500 ms + score badge animation (frames/cg_expert-1_tap_burst.png shows fish gone ~0.25 s after tap); the particle burst in Fish.qml did not render under the software renderer. Miss = nothing at all (child L1 misses 2-5 per run).
- clickgame D4: no intro, playable at the first frame (0 s), but no voice instruction and no re-hint ever.
- clickgame D5: fish speed at L1 about 50-60 px/s, horizontal only; nothing ever escapes despite the description; no slow-down after misses; difficulty only rises (L2 7 fish, vertical motion, 1500 ms base; L6 18 fish, 400 ms).

### Where the reference is objectively better (than ours as documented)
1. Zero time to first input (clickgame): fish are tappable on the first rendered frame and the first catch happened at 0.41 s (expert-1) / 1.2 s with child latency. Ours: first baby reaches the catch line about 4.2 s after spawn (reaudit, Nursery section). A child who taps right away gets nothing to do in ours for ~4 s.
2. The success response is attached to the object touched and is shorter than ours' miss handling: clickgame hit = sound + fish fade within one frame; ours plays a three-second Faron miss line per missed baby (reaudit). Clickgame spends 0 s on misses.
3. Many simultaneous valid targets (5-18 fish) mean a sloppy tap still often hits something: child-sim L1 success 50-71% of taps without any assist. Ours has one target lane at a time for the first two catches.
(ballcatch has no advantage over ours: it requires two simultaneous fingers and never adapts.)

### Where ours is better (keep)
- Adaptive mercy: ours slows babies, spawns near the cradle and widens the catch after two misses (reaudit); ballcatch keeps the same 350 ms window through 12-13 consecutive losses (runs 3-6) and clickgame never slows.
- Ours is one-finger throughout; ballcatch is not past level 1.
- Ours shows caught babies accumulating in the cradle; ballcatch has no persistent progress and clickgame only a numeric 1/5 badge.
- Ours has a voiced objective; both references are text or nothing.

### Redesign recommendations (Godot 2D, hard rules respected)
1. Make the first baby catchable immediately: spawn it already low (catch line reachable in <= 1.5 s) or let the very first touch anywhere glide the cradle under it. Acceptance: probe logs first possible catch <= 1.5 s after phase open.
2. Respond to every touch at the touch point within 100 ms even when it is not a catch (cradle wiggle + soft chime), as clickgame does for hits; never play a voice line for a miss more than once per 10 s. Acceptance: probe counts silent touches = 0; miss VO count per 60 s child-sim <= 2.
3. Optional "many easy targets" warm-up: two babies drifting slowly on clouds for the first catch, so a random tap near either works. Acceptance: random-tapper policy gets >= 1 catch in 60 s, idle gets 0.

### Limits
- ballcatch second-tap registration could not be done with mouse emulation (see scope); key events stood in for the child's two taps.
- No audio device at the time of these runs; sound behaviour comes from source code.

---------------------------------------------------------------------------------------------------

### Farmer ("The Piggy Picnic Challenge") vs. football and explore_farm_animals

### Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Farmer) | | | | | | | | | | | (other agent) |
| GCompris football "Kick the ball into the goal" | 4 | 4 | 3 | 1 | 2 | 2 | 3 | 2 | 2 | 4 | Pull-back slingshot. Expert 3 goals in 36.4/45.9/53.9 s (5-7 kicks); child 1-2 goals in 60 s (7-10 kicks); 3 child drags started off the ball and did nothing (runs 1-6, 10). Idle: ball never moves (run 9). |
| GCompris explore_farm_animals | 2 | 4 | 4 | 2 | 2 | 3 | 2 | 3 | 1 | 5 | Tap 9 animals (sound + photo panel), then "find the animal you hear". Expert full 83-92 s, 9/9; child explores in 52-58 s then 4-7/9 correct with 1-5 wrong in the remaining ~100 s (runs 1-6, 10). |

D-evidence detail:
- football D1/D3: drag from the ball draws a red direction/power line while pulling (frames/fb_mid_pull_aim_line.png); release plays brick.wav at -0.02 s (recorded probe) and the ball leaves opposite to the pull; power saturates at a 20 px pull (football.js: min(10, 0.5*len)).
- football D5/D6: Tux goalkeeper bounces the ball back at 2x speed (football.js); friction 0.995 per 16 ms means a kick often keeps rolling > 9 s (several TIMEOUT events, longest wait 9.7-10.8 s in every non-idle run). Goal = whole right edge (540 px). Tux grows each level (height 10*(5+2*level)*ratio).
- football D9: only grab target is the 69 px ball (50*ratio 1.385); a drag that starts beside it is silently ignored.
- football D4: no intro, no demo of "pull back", no voice; a child's natural "push toward goal" flick sends the ball backwards.
- farm D3: tap animal -> its recorded sound at +0.12 s, photo panel slides in over 1.2 s (frames/fa_expert-1_panel.png); quiz correct -> completetask.wav, measured onset median about 0.07 s (0.0-0.9 s) + 600 ms spin; wrong -> crash.wav + red error box, same question stays (frames/fa_child-sim-1_wrong.png).
- farm D9: animal hit boxes from board1.qml x 480 px play area: owl 34x38, cat 58x48, chicken 91x58, sheep 77x77, horse 96x91, duck 118x67 px; none reaches 120 px. Child-sim missed animals 0-2 times in explore and several times in the quiz (dead 4-7 per run).
- farm D4: instructions are text banners ("Click on each farm animal to discover them.", "Click on the farm animal that makes the sound you hear."); the photo panel's description paragraph is not voiced; closing the panel needs the 78 px X or a tap off the photo (tapping the photo only toggles its size; child-sim hit this in run 3 at 11.4 s).
- farm D8: a star appears under each explored animal (frames/fa_expert-1_explore_done.png), a visible "collection" of what was met; OK button then unlocks the quiz.
- slow-1 (10-20 s pauses): no re-hint at all in either game; in the quiz the question sound is never replayed unless the child presses the lips button (run 7: 0 answers in 166 s).

### Where the reference is objectively better
1. football shows the aim before release: a live line from ball to finger encodes direction and power during the whole pull (frame fb_mid_pull_aim_line.png). Ours' TOSS documents anticipation and release but no continuous trajectory preview (reaudit Farmer, TOSS). Child-sim kicks that were aimed within +-25 deg scored 1-2 goals per minute with no other help.
2. football's target is large and fixed: the goal is the full 540 px right edge, so success depends on direction, not precision. Ours' target is a pig; reaudit notes repeated single target setup but no size figure (to compare against).
3. explore_farm_animals gives each object its own sound on first touch (+0.12 s) and marks it with a persistent star, so "what have I done" is visible without numbers. Ours' TOSS/HERD do not leave a visible per-object record (reaudit cons: crops do not persist into the picnic).
4. Ball physics give emergent variety: rebounds off walls and the keeper produced different ball positions on every kick across 10 runs (no two kick results identical in runs 1-6), while ours' TOSS repeats one setup four times (reaudit).

### Where ours is better (keep)
- Return-on-miss: ours loops a missed vegetable back without consuming it; football leaves the ball wherever it stopped (often >9 s rolling), and the keeper actively knocks it back.
- Ours has a voiced objective and a guided pull; football has no onboarding, and a push-toward-goal flick (what a 4-year-old tries first) sends the ball the wrong way.
- Target sizes: farm animals are 34-118 px; ours' anchored stations are authored for one finger.
- Ours ends in care (picnic); farm quiz is a test with crash sounds for errors.

### Redesign recommendations
1. TOSS: while the finger is pulled back, draw a dotted arc from vegetable to landing point that updates every frame and turns green when it would land in the pig's trough zone. Acceptance: probe drag captures >= 1 frame mid-pull with the arc visible; a release while green succeeds 100% in probe.
2. Make the receiving area big and forgiving: trough/blanket zone >= 240 px wide; pig walks to the vegetable if it lands within 150 px. Acceptance: child-sim (+-25 deg aim, 60-250 px pull) succeeds >= 60% of tosses.
3. Persist each completed toss as a visible token (vegetable stays in trough; crop planted in PLANT is the one tossed). Acceptance: after TOSS ends, 4 tossed vegetables are visible in the same scene; screenshot check.
4. Accept a forward flick as well as a pull-back (map both to "toward the pig") so the child's first instinct works. Acceptance: probe flick toward pig scores.

### Limits
- football was run before the audio server existed; release sound latency comes from one recorded probe (-0.02 s).
- farm audio identity relied on recorded-sound fingerprints (stated above).

---------------------------------------------------------------------------------------------------

### Candy Maker ("The Candy Workshop Cup") vs. babyshapes and babymatch

### Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Candy Maker) | | | | | | | | | | | (other agent) |
| GCompris babyshapes (level 1: chocolate, cookie, butter, orange, jam, baby bottle onto blue silhouettes) | 3 | 4 | 2 | 1 | 3 | 4 | 2 | 2 | 3 | 4 | Expert 17.7/19.4 s, replay 13.4 s; child 25.6-69.2 s, all 4 won; slow 121.9 s won; random 60 s placed 1 piece, wrong, never won (runs 1-10). |
| GCompris babymatch (level 1: lamp->bulb, post box->postcard, sailboat->motorboat) | 2 | 4 | 2 | 1 | 3 | 4 | 2 | 2 | 3 | 4 | Expert 7.7/9.1 s, child 12.1-26.9 s, all won; random never won; idle nothing (runs 1-10). |

D-evidence detail (same engine, babymatch.js / DragListItem.qml):
- D3: on grab, scroll.wav at +0.03 s, piece shrinks and goes 50% transparent; while over the board the nearest spot highlights;
  on release the piece snaps (430 ms) with no sound. Right or wrong, the drop looks identical (frame bs_child-sim-1_first_drop.png).
- D5: drop magnet = nearest spot within 200*ratio = 277 px, so 40-120 px aim errors never missed a spot in 8 child runs; but a wrong
  silhouette is accepted silently and only flagged after the child taps OK (red glow + X, no sound; frames/bs_child-sim-1_flagged.png, bm_child-sim-1_flagged.png). Dropping onto an occupied spot pushes the previous piece back to the tray.
- D4: one text box "Drag and Drop the items to match them." disappears on first press; no voice, no demo, no idle hint (idle 60 s: 0 audio events, frames/bs_idle_t60.png).
- D9: tray icons about 95 px, silhouettes about 100 px, OK button 98 px (bs4 layout); tray pager arrow 37x80 px; babymatch drop markers are 16 px pink dots (the magnet compensates).
- D8: OK -> flower image + random praise voice at +0.45 to +1.17 s (recorded), auto-advance to the next board 1.6 s later. Nothing made is kept.
- D7: tray order shuffled every run (babymatch.js Math.random); boards fixed; 7 levels (level 2 shown in frames after win).

### Where the reference is objectively better
1. Forgiving drop geometry: any release within 277 px of a spot lands on the nearest spot; child-sim drops never "missed" (0 of ~40 child drops fell back for distance). Ours' SORT rejects a wrong bin by returning the piece (good) but the reaudit gives no magnet radius; if our bins require release inside the bin art, the reference's nearest-spot rule is measurably more tolerant.
2. Direct shape-to-silhouette correspondence: each target is the exact outline of one object (6 distinct outlines), so the matching rule is visible without words. Ours sorts into 3 bins by shape class with a fixed sequence `[0,1,2,2,0,1]` (reaudit).
3. Randomised presentation: tray order differs every run (10/10 runs had different first piece order in logs) whereas ours replays the same six-piece order (reaudit con).

### Where ours is better (keep)
- Immediate error handling: ours returns a wrong piece at once and keeps it in hand; the references accept a wrong drop silently and reveal it only after OK (babyshapes child-sim-1 needed 2 OK presses and 69 s; child-sim-3 2 OK presses).
- No text-reading OK step: the references require finding and tapping an unlabelled green OK icon (98 px) to finish; ours completes on the last correct drop.
- Ours is part of a production arc (pour -> sort -> wrap -> share); the references end at a flower.

### Redesign recommendations
1. Add a nearest-bin magnet to SORT: on release, snap to the nearest bin within ~250 px (1280x720 space) instead of requiring the bin rect; keep the immediate return for a wrong bin. Acceptance: child-sim drops with 40-120 px error land in a bin 100%; wrong-bin returns stay immediate (<100 ms).
2. Show the candy's outline on its bin (a silhouette slot per shape) so the matching rule is pictorial. Acceptance: a person with sound off can name the bin for each candy from a screenshot.
3. Shuffle the six-piece order per run (already a P1 in the reaudit); the references prove the cost is nil. Acceptance: 10 replays produce >= 5 distinct orders.
4. Do not copy the OK-to-check step.

### Limits
- Candy-specific references (pouring, wrapping) are not in GCompris; only the sort/shape phase is compared.

---------------------------------------------------------------------------------------------------

### Astronaut Engineer ("The Rocket Repair Race") vs. canal_lock and PipeWalker

### Scores
| Game | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours (Astronaut) | | | | | | | | | | | (other agent) |
| GCompris canal_lock | 4 | 4 | 3 | 1 | 1 | 2 | 1 | 2 | 2 | 5 | Operate valves/gates so the water level carries Tux's boat up. Expert 6 taps, 28.9 s (runs 1, 2, 10); child-sim 2/4 won in 105.8/120.6 s, 2/4 not won in 152 s with 6 and 22 invalid "crash" taps (runs 3-6); slow-1 not won in 152 s; random never; idle nothing (runs 7-9). |
| PipeWalker 1.0 (10x10, default "Network" skin) | 4 | 4 | 4 | 0 | 0 | 4 | 4 | 3 | 1 | 4 | Tap rotates a pipe tile; tiles connected to the server turn blue and monitors light. Expert solved 57-60 scrambled cells in 19.5-20.3 s (75-76 clicks); child-sim 0/4 solved in 60 s (still wrong 42-47 of 48-59) (runs 1-6); slow-1 fixed 2 of 69, random fixed 4 of 58 with 61/98 taps outside pipes, idle unchanged, replay (new board) 19.6 s (runs 7-10). |

D-evidence detail:
- canal_lock D1/D3: valve tap -> lock.wav at median +0.02 s; water in the chamber rises/falls over 3.5 s and the boat rises with it; traffic light turns green when a gate opens (frames/cl_expert-1_win.png). Invalid action -> crash.wav only: no motion, no highlight of the blocking part (frames/cl_child-sim-1_crash_no_visual.png and -2/-3/-4).
- canal_lock D4: 3 pages of text intro ("The vertical colored bars represent the water locks...") with Next/Skip text buttons before the first input; no voice, no demo, no re-hint (idle 60 s: 0 audio events, frames/cl_idle_t60.png).
- canal_lock D9: bars are 50 px wide with 28 px invisible margins (106 px); an OPEN gate shrinks to a ~50x31 px stub and its hit box moves down with it, so tapping where the gate was does nothing (frames/cl_open_gate_hitbox_stub.png; my first scripted runs tapped the old position 100+ times with no response). The boat (about 150x40 px) is the "go" control and nothing marks it as tappable.
- canal_lock D6: every gate/water/boat step is a 3.5 s animation; boat taps during a boat move are ignored; the expert's 28.9 s is ~75% waiting (5 waits of ~4.3 s).
- canal_lock D7: one fixed scenario; after the win the boat swaps to a "logs" boat for the return trip (boat2.svg), the only variation.
- PipeWalker D3: each tap starts a 300 ms rotation (cell.hpp rotation_time = 300) and plays clatz.wav when it lands; connectivity is recomputed every frame (Level::update -> trace_state) so the lit/blue network grows or shrinks immediately after each rotation; win = fireworks + complete.wav (frames/pw_expert-1_end.png vs pw_expert-1_start.png).
- PipeWalker D4/D5: no instructions, no hint, no highlight of the next useful tile; idle 60 s: board static (run 9).
- PipeWalker D9/D10: the smallest board (10x10 at 1280x720) gives 58.4 px cells; a plain tap rotates counter-clockwise only (clockwise needs a right click), so a wrong-way tap costs 3 more taps.
- PipeWalker D7: every level id generates a different board (ids 3-12 used across runs, all different).

### Where the reference is objectively better
1. Per-tap causality latency: in PipeWalker the connected network recolours within one frame after the 300 ms rotation, on every tap, including partial progress (some monitors lit). Ours: fuel advances every 1.2 s while incomplete and 0.35 s once complete (reaudit, Astronaut), so a correct placement can wait up to 1.2 s to show its effect.
2. canal_lock shows *why* the boat can move: the controlled quantity (water height) is drawn, animates for 3.5 s, and the boat physically rides it; green/red lights encode "gate open". Ours' VALVE is a 1.8-revolution rotation with no visible water/coolant consequence (reaudit cons: late phases reduce cognitive depth).
3. Order matters in canal_lock (two valves cannot be open together; a gate opens only at equal level), so the child discovers a rule by trying; ours' PATCH/VALVE/LAUNCH have no decision (reaudit).
4. Variety: PipeWalker generated 10 distinct boards in 10 runs; ours has three fixed pipe boards.

### Where ours is better (keep)
- Assistance: ours twinkles the needed cell after 8 s and returns a wrong pipe after 16 s (reaudit); neither reference ever hints (slow-1 canal: not won in 152 s; PipeWalker child-sim 0/4).
- Invalid-action feedback: ours shows fuel waiting at the gap; canal_lock gives only a crash sound with no visual reason.
- Targets: ours' pipe stations are large; PipeWalker cells are 58 px and canal's open-gate stub is 31 px tall.
- Ours' boards step up gradually (2 straight pieces, then bend + obstacle); PipeWalker's smallest board starts at 48-60 wrong cells.
- No text intro in ours; canal_lock needs 3 text pages dismissed.

### Redesign recommendations
1. Advance coolant the moment a correct pipe is placed (<= 150 ms) and colour every newly connected segment, keeping the wait-at-gap behaviour. Acceptance: probe measures placement -> fluid visible in the new cell <= 0.3 s.
2. Give VALVE a visible consequence: rotating fills a glass coolant tank toward a painted line and a lamp on the rocket turns from red to green at the line. Acceptance: screenshot at 50% of the gesture shows the tank half full; lamp green only at completion.
3. One rule beat in the late phases: two valves, only one can be open (like canal_lock), with a visual block (the other valve wobbles and a small lock icon appears at it) instead of a sound-only refusal. Acceptance: invalid tap produces motion at the touched object within 100 ms and no voice.
4. Never move or shrink a hit box when its object changes state; keep >= 120 px boxes for open and closed valves. Acceptance: probe taps the same coordinates before/after a state change and both register.
5. Generate pipe boards procedurally within the three difficulty steps. Acceptance: 10 replays give >= 5 distinct layouts with the same piece counts.

### Limits
- PipeWalker as packaged (Debian 1.0-1) scrambles only the server tile on a new level (source: `#ifdef DEBUG` path in Game::reset_level rotates only the sender; observed: fresh boards needed exactly 1 rotation). For runs I pre-scrambled every tile with 0-3 counter-clockwise taps (setup, not counted), saved, relaunched, and played that board. The solver used PipeWalker's own saved state (pipewalker.ini); expert play is solver-driven.
- canal_lock state was re-read from the screen each step (gate/valve/water/boat pixels). In child runs, events labelled "ignored: animation still running" were still sent to the game; only boat moves actually lock input in the game, so some of those were real gate toggles that the next screen read caught. Dead-touch counts for canal child runs are therefore upper bounds.
- The PipeWalker "Plumbing" skin (water to taps) exists but the default "Network" skin was played.

---------------------------------------------------------------------------------------------------

### Cross-career summary of measured reference behaviour (for the "ours" agent to compare)
| Measure | ballcatch | clickgame | football | farm explore | babyshapes | babymatch | canal_lock | PipeWalker |
|---|---|---|---|---|---|---|---|---|
| Time to first possible input | text intro + Start | 0 s | 0 s | 0 s (text banner) | 0 s (text box) | 0 s | 3 text pages | 0 s |
| Sound on valid touch | 2nd hand only | yes (drip) | release -0.02 s | +0.12 s / ~0.07 s | on grab +0.03 s, none on drop | same | +0.02 s | on rotation end (~0.3 s) |
| Error response | try-again voice, same level | none (miss = nothing) | ball keeps rolling | crash + red box, same Q | silent until OK, then red X | same | crash sound only | none |
| Idle 60 s | nothing | nothing | nothing | nothing | nothing | nothing | nothing | nothing |
| Adaptive easing | none | none | none (keeper grows) | none | none | none | none | none |
| Smallest key target | hands 155x210 | fish 53 px tall | ball 69 px | owl 34x38 | pager 37x80 | drop dot 16 px (277 px magnet) | open gate 50x31 | cell 58 px |
| Expert / child-sim completion | L6-L8 / stuck L2 | L1 6 s / 15-21 s | 3 goals 36-54 s / 1-2 goals in 60 s | 83-92 s / 4-7 of 9 | 13-19 s / 26-69 s | 7-9 s / 12-27 s | 29 s / 2 of 4 in 106-121 s | 20 s / 0 of 4 |
