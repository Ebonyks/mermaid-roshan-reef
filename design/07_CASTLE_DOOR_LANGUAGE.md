# Pearl Castle door language — Act One

Status: owner-corrected sequencing; mismatched shimmer gate retired while
state glows remain active, 2026-08-29.

## The four promises

The treatment answers one question before a non-reader taps: “What happens if
I go there?” Colour, motion, and touch behavior carry the same meaning.

| State | Promise | Treatment | Tap |
|---|---|---|---|
| Blocked | You cannot go here yet | Dark lavender veil with drifting pearl-grey fog | Stays in the hall; fog flutters and Daddy speaks kindly |
| Open | You may visit; nothing important is waiting | Authored door with no added effect | Enters normally |
| Bonus | One optional reward is waiting here | Soft ruby-red doorway glow that breathes once every 4.4 seconds; no frame trace | Enters normally |
| Plot | This is the recommended next story destination | Soft gold doorway glow; former mismatched rainbow shimmer gate removed | Enters the current story beat |

Blocked is visible but never glows. Open is deliberately quiet. Bonus and Plot
remain visible highlights, and the Castle may own **at most one highlighted
door at a time**. Their glow remains fully inside the doorway opening and does
not trace or touch the painted frame. A sequencer must choose one destination
before assigning either state; individual rooms may not light themselves
independently.

## Authoritative Act One order

The existing `DayOneDirector` owns progression and save restoration. The door
language reflects that state; it does not create a parallel Crown-based route.

| Beat | Sole Plot door | Completion authority |
|---|---|---|
| 1 | Bubble Bath | Day One `bathroom` tutorial complete |
| 2 | Mermaid Pool | Day One `pool` cleanup complete |
| 3 | Stuffie Playroom | Baby Eagle is physically rescued from both dust bunnies; `stuffie_wins["rescued_eagle"]` and Day One `stuffie` complete |
| 4 | Craft Room | Day One `art` activity complete |
| 5 | Royal Hall back door | All four rooms complete; Giant Dust Bunny event armed |

At every beat:

- completed destinations are Open and keep no highlight;
- the current destination is the sole gold/rainbow Plot door;
- future destinations and every other early Castle room are Blocked;
- the shell elevator mirrors the physical doors and cannot bypass the order;
- completing a beat transfers the highlight immediately to the next door.

Baby Eagle is never a red bonus during this sequence. Her rescue is the third
required plot beat and therefore uses the gold/rainbow treatment. The red
Bonus state remains available for a future sequencer to nominate one optional
reward after the current plot highlight has cleared; it may never coexist with
another persistent highlight.

After Day One ends, ordinary Castle rooms become quiet Open destinations.
Royal Hall uses Plot only while an existing story event is armed; otherwise its
authored resting mist remains Blocked.

## Implementation rules

- `CastleDoorLanguage` is the single state resolver used by physical doors,
  elevator cards, and direct child-facing room routes.
- `CastleDoorCue` is an input-transparent procedural Canvas control. It adds no
  art asset, touch target, save key, or spatial rendering debt.
- The former shared procedural arch path is removed. It did not match the
  painted doorway frames. Bonus and Plot retain diffuse interior glows, but no
  edge or shimmer may claim to follow the frame until exact masks or authored
  cues are built from each painted-frame silhouette.
- The glow geometry leaves transparent margins inside its Control bounds so
  clipping can never expose a rectangular false frame.
- Blocked fog may fill the doorway opening, but it must not draw a synthetic
  frame-tracing outline.
- The Day One dirt dressing no longer draws independent door glows. It owns
  grime and dust-bunny dressing only.
- A blocked touch always produces a local fog flutter, spoken feedback, and no
  progress mutation.
- Saved partial Baby Eagle rescue remains safe: each cleared pin is restored,
  but owning another companion never skips this required plot rescue.
