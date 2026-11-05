# Racer voice: existing clips only

Owner rule, 2026-11-03: new requests must reorganize existing material, not
ask for new content. This packet requests no new recordings. It maps the
existing generated Racer clips (texts from `tools/make_voices.py`) to race
moments and lists what has no clip.

## 1. Wired now (scripts/opera_racer_surface.gd `RACE_VOICES`)

| Moment | Clip | Spoken text | Cooldown |
|---|---|---|---|
| RACE phase opens (career world, unchanged) | `roshan_op_racer_steer.ogg` | "Swipe to steer through the coral gates!" | phase start |
| A zoom fires | `roshan_op_racer_work.ogg` | "Zoom! Round the corner and away!" | 12 s |
| The imp takes the lead | `imp_op_racer_steal.ogg` | "Catch me! You won't! ...you might!" | 15 s |
| The imp spins (his lap-2 wobble or a sparkle hit) | `imp_op_racer_copy.ogg` | "Whoa whoa WHOA — how do you stop this thing?" | 10 s |

No reaction plays in the first 4 s of driving, so the instruction is heard
whole. Lines go through `main._say()`, so the audio director's cooldown and
required-line rules apply. The "coral gates" in the instruction are the
in-game painting's arches: the race starts under the pearl starting arch and
a row of item bubbles stands under each pearl arch.

## 2. Existing clips that no longer fit (do not wire)

| Clip | Text | Why not |
|---|---|---|
| `roshan_op_racer_turbo.ogg` | "Tap TURBO when the marker hits green!" | There is no marker; the bubble works any time |
| `roshan_op_racer_finish.ogg` | "Tap the zoom strips and cross the line!" | The course has no zoom strips (the painting has none) |
| `roshan_op_racer_lap_two.ogg` | "Loop the loop! Draw big racing circles!" | Belongs to the circle-drawing phase |
| `imp_op_racer_arrive.ogg` | "I was sent to learn the FAST. I am already fast!" | 3.4 s, longer than the 1.8 s imp-win beat |
| `imp_op_racer_bop.ogg` | "Pit stop! Pit stop! I need a pit stop!" | Reserved for the bop phase |

## 3. Gaps (owner decision; nothing requested)

1. No clip teaches the red brake or the item bubble. The guide hand teaches
   the stick; the bubble pulses when an item is ready.
2. No clip marks the imp winning a race (the restart beat is visual: his face
   bounces for 1.8 s, then the lights count down again).
3. No clip says "this way" when she faces backwards (the yellow arrow shows
   the way and the kart turns itself round).
4. "Swipe to steer" still describes the stick only loosely (she slides a
   finger sideways). A new line would need an owner decision; until then the
   existing recorded instruction stays exact and the probe pins it.
