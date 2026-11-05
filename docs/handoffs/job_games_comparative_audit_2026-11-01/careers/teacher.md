# Teacher ("The Castle Learning Circle"): comparative findings

Setup: `dev` @ 93166ab, reef_play harness. Rendered on :57: expert-1, child_sim-1, idle-1; fast: the other 7. child_sim-5 stands in for replay-1 (fresh profile each run), so persistence is judged from code. All runs scripted.

## 1. Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours: Teacher | PLAYED | 3 | 3 | 3 | 3 | 4 | 2 | 2 | 2 | 3 | 4 | 2.9 |
| GCompris enumerate | PLAYED | 2 | 4 | 2 | 1 | 2 | 4 | 4 | 2 | 2 | 4 | 2.7 |
| GCompris frieze | PLAYED | 4 | 4 | 2 | 1 | 1 | 2 | 3 | 2 | 2 | 4 | 2.5 |
| Khan Academy Kids | DOCUMENTED | 3 | - | - | - | 4 | - | 5 | - | - | - | - |
| LEGO DUPLO Number Train | DOCUMENTED | 3 | - | - | - | - | - | 3 | - | - | 4 | - |
| PBS KIDS Games | DOCUMENTED | - | - | - | - | - | - | 4 | - | - | - | - |

Ours:
- D1 tapping an answer card and touch-counting each pearl, each number voiced.
- D2 idle never wins (90 s, 8 hints); wrong answers pay 0; but the 2-choice PATTERN was solved by random_tapper at 29.3 s. Expert 15.2-17.3 s, child 17.0-22.2 s, same outcome.
- D3 voice or help hand on each pearl and wrong answer; 7 dead touches across 5 child runs (all 40-120 px from a pearl); correct PATTERN/MATCH answers start no sound within 0.25 s; number voices queue behind the prompt (up to 1.9 s late in expert-1 COUNT).
- D4 all prompts voiced; first input 2.2-2.7 s; no demo before the first try; help hand first at 7 s after the board opens; re-hints every 9 s.
- D5 a wrong pick shows the hand on the correct card at once and never subtracts; no autopilot.
- D6 15-22 s over 4 phases with 12.9-13.3 s of no-input time (65-85%).
- D7 the same 4 lessons in all 10 runs (sequence 0 on a fresh profile); code rotates shapes and tiers per saved round.
- D8 finale is an empty board plus "A lovely learning day!".
- D9 answer cards 210x170 px; pearls drawn at about 56 px with a 72 px hit circle (`opera_teacher_surface.gd:170`).
- D10 taps only; a tap is dropped if the finger slides more than 38 px (`:156`).

## 2. Where the references are objectively better
1. **Practice per session.** Ours: 4 answers in 15.2 s (12.9 s dead). GCompris enumerate: 12 answers in 100.9 s; frieze: 20 rows of 8 tokens in 189.4 s.
2. **Variety.** Ours: 1 lesson set across 10 runs, down to identical tap coordinates (PATTERN at (577,540)). GCompris changes fruit type and count every item (11 fruit types).
3. **Pattern depth.** Our ABAB with 2 cards fell to random tapping in 29.3 s; frieze level 2 makes the child continue the row; random taps solved 0 friezes in 61 s.
4. **Answer sound latency.** GCompris completetask at a median 0.073-0.082 s; ours no sound within 0.25 s on correct PATTERN/MATCH.
5. **Starting quantities.** Fresh-profile ours counts 1 pearl and adds 1+1; GCompris level 1 already asks counts to 2, then 3.

## 3. Where ours is better (keep)
Re-hints (references: 0 sounds and 0 changes in 60 s idle); every objective voiced (GCompris uses text; frieze has no voice); no numerals to read (GCompris uses a 0-9 keypad with 62 px keys); fewer dead touches (0 for experts vs enumerate 13 of 28); wrong answers teach at once (enumerate is silent; frieze crashes without saying which token); play targets far from exit (GCompris exit about 60 px from play targets ended 1 of 4 child sims).

## 4. Redesign guide (by impact)
1. **Three lessons per phase** (sequence +1, +2). *Check:* fast expert 35-60 s; no-input share under 40%.
2. **Vary the fresh-profile start** by seed or day. *Check:* seeds 1-3 give 2 or more PATTERN answers and COUNT quantities.
3. **Play the guide hand once on open; re-hint at 7 s.** *Check:* idle-1 shows help within 1 s of phase open.
4. **Make PATTERN un-guessable without reading:** 3 cards, or fill 2 missing slots. *Check:* random_tapper does not finish PATTERN in 60 s.
5. **Answer every touch:** ripple and sound for board misses; 120 px pearl hit area; chime under 100 ms on correct answers; number voices cut in instead of queueing. *Check:* 0 dead touches in child_sim-2..5; sound within 0.15 s of every correct tap.
6. **A kept item:** a class sticker on the library wall that persists. *Check:* visible in the finale and on the next visit (real save).

## 5. Defects
- One-tap Back exit (button geometry `navigation_controller.gd:117-120`; exit logic `press()` at lines 61-85, fired from `pause_menu.gd:29`): random_tapper seed 1 ends at 136.37 s here and in the 12 other careers checked. Repro: `reef_play.sh teacher random_tapper 1 OUT fast 600`.
- Floor taps delay the auto-walk: in random_tapper-1, COUNT was armed at 31.5 s but opened at 95.5 s.

## 6. Limits
GCompris scores from ref_gcompris_a (frieze runs 2-3 being re-run at hand-off). Khan Academy Kids, PBS KIDS and LEGO DUPLO documented only. Tier persistence from code (`teacher_lesson_plan.gd`).
