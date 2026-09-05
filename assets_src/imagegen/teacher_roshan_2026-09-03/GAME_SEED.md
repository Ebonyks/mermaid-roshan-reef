# Teacher Roshan — Opera learning-game seed

This asset is the character base, not a shipped Opera act. A later act can use
the existing `teacher` atlas key without regenerating Roshan.

## Child-facing promise

Teacher Roshan hosts three short, voice-led, one-finger activities. Nothing is
lost on a wrong tap: she demonstrates the answer, celebrates the attempt, and
offers the same idea again with a simpler choice.

1. **Letter lagoon** — hear one letter sound, then tap the matching large card.
2. **Pearl counting** — hear a number from 1–5, then tap the matching pearl
   group; each pearl lights and counts aloud.
3. **Shape stage** — drag or tap a circle, triangle, or square into its large
   matching silhouette.

Every objective needs a recorded `_say()` cue and a moving visual pointer. The
learning cards, numerals, and shapes should be separate high-contrast 2D assets,
not baked into the Roshan atlas. This keeps text exact, supports future lesson
sets, and lets the pointer gestures target empty scene space cleanly.
