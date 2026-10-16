# Pearl Castle door language — Act One

Status: owner-corrected sequencing and frame-registered runtime treatment,
2026-10-15; restoration candidate from the unmerged 2026-08-29 correction.

## The four promises

The treatment answers one question before a non-reader taps: “What happens if
I go there?” Colour, motion, and touch behavior carry the same meaning.

| State | Promise | Treatment | Tap |
|---|---|---|---|
| Blocked | You cannot go here yet | Dark lavender veil with drifting pearl-grey fog | Stays in the hall; fog flutters and Daddy speaks kindly |
| Open | You may visit; nothing important is waiting | Authored door with no added effect | Enters normally |
| Bonus | One optional reward is waiting here | Restrained ruby-red frame glow that breathes once every 4.4 seconds | Enters normally |
| Plot | This is the recommended next story destination | Brighter gold frame glow with one alpha-masked rainbow sheen crossing every 4.6 seconds | Enters the current story beat |

Blocked is visible but never glows. Open is deliberately quiet. Bonus and Plot
remain visible highlights, and the Castle may own **at most one highlighted
door at a time**. A sequencer must choose one destination before assigning
either state; individual rooms may not light themselves independently.

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
- `CastleDoorCue` is an input-transparent Canvas control. It adds no touch
  target, save key, or spatial rendering debt.
- Physical hall doors use three exact crops of the approved Main Hall painting:
  small, Opera, and Royal. The shader derives its emission mask from the same
  painted gold/pearl pixels, so no generic arch is stretched between families.
- The red Bonus cue is deliberately quieter than Plot. Plot keeps a gold base;
  its rainbow is a narrow moving sheen multiplied by the frame mask, never a
  diagonal rectangle or a free-standing gate.
- Physical blocked fog is family-shaped and confined to the doorway opening.
  Elevator cards retain their compact card-local treatment.
- Visual cues keep the complete projected doorway rect while the viewport
  clips it. Touch hitboxes alone use the viewport intersection, so camera pans
  cannot resize or recenter the art.
- Physical glow visuals render above the painted background but below door
  signs, Roshan, props, and touch controls.
- The Day One dirt dressing no longer draws independent door glows. It owns
  grime and dust-bunny dressing only.
- A blocked touch always produces a local fog flutter, spoken feedback, and no
  progress mutation.
- Saved partial Baby Eagle rescue remains safe: each cleared pin is restored,
  but owning another companion never skips this required plot rescue.

## Restoration evidence

The original painted-frame correction `10ddff27` never entered dev ancestry.
The 2026-10-15 restoration keeps later attention feedback and input/state behavior.
[Impact and exact validation](audit_impacts/restore-doorframes-20261015.json)
tracks current verification and remaining device/child/owner acceptance. The wider
Door Guidance v2 handoff remains a separate proposal.
