# Detective ("The Two-Detective Mystery"): comparative findings

Setup as Teacher (10 scripted runs on :57). GCompris photo_hunter (find the differences) was PLAYED 10 times by the reference agent. Hidden Folks and Lost in Play are DOCUMENTED. Hidden Folks and Lost in Play are DOCUMENTED; Hidden Folks is on the PC shortlist.

## 1. Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours: Detective | PLAYED | 3 | 3 | 3 | 3 | 2 | 3 | 1 | 3 | 2 | 4 | 2.7 |
| GCompris photo_hunter | PLAYED | 3 | 4 | 4 | 1 | 1 | 4 | 1 | 2 | 1 | 4 | 2.5 |
| Hidden Folks | DOCUMENTED | 4 | 4 | 4 | - | 3 | - | 5 | - | 2 | 4 | - |
| Lost in Play | DOCUMENTED | 3 | 4 | - | 4 | 3 | - | 3 | - | - | 4 | - |

Documented: Hidden Folks 32 areas, 300+ targets, reacting scenery, hints from the target strip; Common Sense Media 8+ (riddles need reading). Lost in Play: no dialogue or narration, hint system, rated 9+.

Ours:
- D1 sweeping a lens and dwelling 0.45 s is a true search verb, but the clues are not on painted objects.
- D2 idle never wins (90 s, 10 hints); expert 21.9-24.3 s, child 24.1-28.9 s; random taps alone finished SEARCH in 20.7 s because the lens jumps to each tap.
- D3 0 dead touches in non-random runs; chime per clue found; CASE BOARD drags and the CROWN tap start no sound within 0.25 s; random tapper 157 of 229 touches dead.
- D4 2-line intro, first input 3.6-4.4 s; the ghost lens goes to the real clue, glisten at 12 s; idle re-hints repeat the identical line 7 times in 90 s.
- D5 the rival clock (par 40 s, `opera_competition.gd:20-28`) triggers a guided retry that sets `phase_progress = 0.0` (`opera_career_world_2d.gd:4822`).
- D6 22-29 s over 3 phases; longest wait 3.5-3.9 s.
- D7 identical in 10/10: lens stops at x 462/791/1078 (y 134), same board order, chest at (184,312).
- D8 curtain call with tiara and the rival's bow; nothing kept.
- D9 the painted room covers only about x 325-982, y 178-572 (655x394 px, 28% of the screen), framed by navy bands; all 3 clues sit in the navy band at y 58-72, 106-120 px above the painting, one also right of it at x 1078; the crown chest sits in the blurred margin; lens capture radius 112 px.
- D10 one-finger drag with dwell, drag-to-silhouette, a tap.

## 2. Where the references are objectively better (documented side marked)
0. **Played (photo_hunter):** every miss gets brick.wav and a mark at the touch point; a hit sounds at a median 0.002-0.009 s; a found difference stays circled in the scene, so progress is readable without numbers. Ours scores only dwell on true clues and is silent on CASE BOARD drags.
1. **Search content.** Hidden Folks (DOCUMENTED) 300+ targets in 32 areas; ours 3 fixed clue spots, identical in all 10 runs.
2. **Targets are in the scene.** Hidden Folks (DOCUMENTED) hides targets in the drawn scene; ours puts 3 of 3 clues outside the painted rectangle (y 58-72 vs painting top y 178).
3. **No timed failure.** Neither documented reference has a rival timer. In our slow-1 run the child placed 2 of 3 clues (80.9 s, 100.7 s); the rival "solved" at 109.5 s; the retry needed all 3 drags again (130.5, 148.3, 167.0 s). random_tapper triggered the same retry at 115.2 s.

## 3. Where ours is better (keep)
Large targets (112 px capture vs photo_hunter 8-97 px difference boxes, several under 30 px; Hidden Folks targets are miniature); spoken story with nothing to read; a ghost lens that travels to the actual next clue and cannot score; a forgiving board (a wrong drop eases home over 0.38 s with no loss).

## 4. Redesign guide (by impact)
1. **Remove the progress reset.** The rival reveal may play, but placed clues stay and the retry starts from the current count. *Check:* in the slow-1 repro, CASE BOARD after the retry needs only the remaining drags (1, not 3); a test asserts `phase_progress` never decreases.
2. **Put the clues on the painting.** Remap `clue_spots` and `DETECTIVE_ROOM_OBJECTS` to the actual drawn rect for detective (`StagePaths.BLEED` assumes 9-91% width and full height), or rebuild a full-frame source. *Check:* every clue point lies inside the painted rect on a painted object in an open-search frame.
3. **Rotate 3 of the 8 authored clue spots per run** (seeded) and shuffle the board order. *Check:* 3 seeds give 2 or more first-clue positions.
4. **Sound and motion on every board drop and the chest tap** under 100 ms. *Check:* audio start within 0.15 s of each clue_board gesture.
5. **The lens follows a drag only, never teleports on tap.** *Check:* random_tapper finds 0 clues in 60 s; child result unchanged.
6. **Vary idle re-hints** among 2-3 lines; move to 7 s. *Check:* no line repeats back to back in idle-1.

## 5. Defects
- Guided retry discards placed clues. Repro: `reef_play.sh detective slow 1 OUT fast 900` (CASE BOARD retry at 113.1 s). The retry voice ("corners him first, watch, then trap him together") describes the old bop finale, not the board.
- Clues outside the painting (D9).
- One-tap Back exit (random_tapper-1 ends at 136.37 s).

## 4b. Added from the played reference
7. **Answer misses at the touch point:** a soft "nothing here" sound and a small mark; 3 misses within 5 s trigger the glisten on the nearest clue. *Check:* a tap on empty floor gives sound within 100 ms and a mark; 3 misses give a glisten within 0.5 s.
8. **Found clues leave a permanent in-room marker** until the case ends. *Check:* a frame 10 s after clue 1 still shows the marker.

## 6. Limits
photo_hunter is a fixed picture sequence and a weak search reference; documented scores are not one-to-one comparable with played ones. The PC round (Hidden Folks) should close this gap first.
