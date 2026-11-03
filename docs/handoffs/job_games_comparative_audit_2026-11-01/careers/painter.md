# Painter ("The Sunrise Paint-Off"): comparative findings

Build `dev` @ 93166ab. Phases: PAINT (paint_reveal: clear 38 of 60 cells), STAMPS (5 free taps), GALLERY (choice; contest starts here); `opera_career_world_2d.gd:320-323`.
10 scripted harness runs on the finger path, fresh profile each; rendered on :59 for expert-1, child_sim-1, idle-1; child_sim seed 5 replaces replay-1.
References PLAYED (scripted mouse input): Tux Paint, KTuberling, GCompris simplepaint/erase/redraw. DOCUMENTED only: Crayola Create and Play, Pok Pok, Chicory.

## Measured (ours)

| Run | Done | Game time | Inputs | Dead | Hints | Notes |
|---|---|---|---|---|---|---|
| expert-1 / expert-2 | yes | 17.2 / 14.3 s | 10 | 0 | 0 | Task time 2.8 / 1.6 s |
| child_sim-1..5 | 5 of 5 | 16.5-19.7 s | 10-11 | 0-1 | 0 | |
| slow-1 | yes | 144.7 s | 10 | 0 | 10 | |
| random_tapper-1 | no | 136.4 s | 229 | 194 | 11 | Left via Back |
| idle-1 | no | 75.1 s | 0 | 0 | 7 | Reprompt 9.2 s, auto-walk 20.2 s, re-hint every ~9.1 s; canvas stays at 0 |

- The painting is pixel-identical between seeds (mean diff 0.000); `support_career_painted_art.gd:294-331`.
- Stamp area differs on 18% of pixels between runs, but `tap_marks` is cleared when the next phase opens (`opera_gesture_surface.gd:506`).
- The gallery lane is deterministic (`opera_career_world_2d.gd:2737`); result score 950, tier 3, in 8 of 8 completed runs.
- No save key holds any of the artwork.

## Scores (0-5)

| Game | Basis | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ours | PLAYED | 2 | 2 | 2 | 3 | 4 | 2 | 1 | 1 | 2 | 4 |
| Tux Paint | PLAYED | 5 | 5 | 4 | 2 | 3 | 4 | 5 | 4 | 2 | 4 |
| KTuberling | PLAYED | 4 | 5 | 3 | 1 | 3 | 5 | 4 | 1 | 2 | 5 |
| GCompris paint/erase | PLAYED | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 2 | 3 | 4 |
| Crayola Create and Play | DOCUMENTED | 4 | - | - | - | - | - | 4 | 3 | - | - |
| Chicory | DOCUMENTED | 4 | - | - | - | - | - | - | - | - | - |

Ours: D1 the brush wipes cloud puffs off a fixed sunrise; D3 no touch sound effects and a tap on the canvas does nothing; D6 86% of the expert session allows no input; D7 one picture; D8 nothing kept; D9 canvas about 134x145 px, gallery frames about 84x86 px.

## Where the references are objectively better
1. **Marks become the picture.** Tux Paint draws a stroke 0.027 s after the finger moves. Ours is pixel-identical between seeds.
2. **Work is kept.** Tux Paint's gallery held 12 pictures across a relaunch and a saved picture was reopened and extended. Ours erases stamps at GALLERY (expert-1 frame f_0015.33) and shows the stock sunrise in the finale (f_0019.22).
3. **Sound on touch.** Tux Paint: sound on 21 of 21 strokes (median 0.055 s, range 0.025-0.11 s); KTuberling names each item in 0.19 s. Ours: no task touch made a sound (58 logged task actions).
4. **A tap paints.** GCompris paints a cell per tap; Tux Paint fills a region in one tap (0.17 s). Ours: 229 random taps, 0 coverage (drag-only).
5. **Canvas size.** Tux Paint about 1020x565 px; KTuberling about 720x550 px. Ours about 134x145 px (2.1% of the screen) on a card at the left edge.
6. **Variety.** GCompris erase shuffles 6 photos per level. Ours: 1 sunrise in 10 of 10 runs, 1 stamp, the same gallery lane 7 of 7 times.
7. **Time spent making.** Tux Paint expert-1: 21 inputs in 16.6 s, longest wait 1.2 s (other play runs 1.6-4.0 s). Ours: 1.6 s of task time in 14.3 s; Roshan walks 2.1-2.5 s per phase plus 2.2 s gaps.

## Where ours is better (keep)
- Voiced re-hints: the references gave 0 re-hints in 3 idle runs of 60 s and 37 long pauses.
- It never plays itself; idle never wins.
- No text modals: a Tux Paint modal ate 14 touches; Tux Paint child-sim-3 had 27 dead touches, ours 0-1 per child run.
- Free, overlapping stamps; studio room art.

## Redesign guide (by impact; each with its acceptance check)
1. **Paint into a kept layer.** Draw into an Image on a canvas of at least 560x420 px placed on the easel she tapped. Tap = dab, drag = stroke. Done at 40-60% coverage. *Check:* two seeds differ on more than 10% of canvas pixels; one tap raises coverage.
2. **One artwork everywhere.** Stamps in canvas coordinates; the same texture in GALLERY and the finale; save a ring of 6 to a new additive key (e.g. `opera_painter_gallery`) shown on a gallery wall. *Check:* finale crops differ between seeds; after relaunch the wall matches the finale (diff under 2%).
3. **Make GALLERY a real choice.** Three different frames, each at least 140 px, all valid. *Check:* lanes 0, 1 and 2 each complete and give different finales.
4. **Sound on every touch** (brush loop, stamp pop, fanfare). *Check:* non-voice audio starts within 0.10 s of 90% or more of touches.
5. **Choices.** Three paint pots and two stamp kinds, each at least 120 px, named by voice. *Check:* at least 3 distinct palettes across 10 seeds.
6. **All phases on one easel, no walking between them.** *Check:* expert no-input share 50% or less.
7. **Re-hint at 7 s** (now about 9.1 s). *Check:* idle interval 6-8 s.
8. **Checkpoint the phase and the canvas.** *Check:* Back mid-STAMPS then return resumes at STAMPS with the canvas intact.

## Defects
1. Back fires on button_down and leaves without a checkpoint (`pause_menu.gd:29`, `opera_career_world_2d.gd:5362`). Repro: `reef_play.sh painter random_tapper 1 OUT fast 600`, ends at about 136.3 s.
2. Drag-only paint: a tap on the canvas paints nothing (`opera_gesture_surface.gd:4400-4457`).
3. Stamps are erased before GALLERY (`opera_gesture_surface.gd:506`).
4. The canvas opens away from the tapped easel: gazebo at about x 470-545, card opens at x 135-330.

## Limits
Scripted runs, not a child. Audio judged from player-start logs under the dummy driver, not heard. Persistence from code.
