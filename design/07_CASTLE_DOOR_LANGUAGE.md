# Pearl Castle door language — Act One

Status: owner-directed implementation language, 2026-08-22.

## The four promises

The door treatment answers one question before a non-reader taps: “What will
happen if I go there?” Meaning is carried by both colour and motion, never by
text alone.

| State | Promise | Door treatment | Motion | Tap result |
|---|---|---|---|---|
| Blocked | You cannot go here yet | Deep lavender veil with layered pearl-grey fog | Slow sideways drift; one brief flutter on tap | Stays in the hall; kind spoken feedback |
| Open | You may visit, but nothing important is waiting | The authored painted door, unchanged | None | Enter normally |
| Bonus | You may visit and an optional reward is still waiting | Deep ocean-blue edge glow | Slow “breathing” halo with four rising bubbles | Enter normally |
| Plot | Go here next to continue the story; this is the recommended route | Gold edge glow with a restrained moving rainbow sheen and a bouncing gold star | Faster pulse than Bonus, but no full-screen flash | Enter the existing plot beat |

Open is deliberately the quiet state. The environment already says “door”; a
second badge would turn every route into visual noise. Blocked is the only state
that obscures the opening. Bonus and Plot preserve the room painting and add a
perimeter cue.

## Act One sequence

The Crown Star is the existing unlock boundary. This preserves the current
spoken promise that the castle becomes Roshan’s and she may “explore every
room,” without adding or migrating save data.

### First arrival, before the Crown Star

Exactly four destinations are live:

- Royal Hall — Plot. It owns the Crown welcome and is the recommended next step.
- Stuffie Playroom — Bonus. Baby Eagle’s rescue is optional and the blue glow
  remains until that saved rescue is complete.
- Royal Kitchen — Open. It is safe free play with no urgent promise.
- Royal Library — Open. It is safe free play with no urgent promise.

Opera Hall, Dream House Wing, Craft Room, Mermaid Pool, Bubble Bath, Dining
Room, both bedrooms, and Movie Lounge are Blocked. The shell elevator applies
the same policy, so it cannot bypass a sealed physical door.

### Crown awarded

Every ordinary Castle destination changes from Blocked to Open immediately.
The transition is derived from the existing `level2_done_once` save flag.

Royal Hall remains Plot while an existing Royal Hall event is waiting, in this
order: companion welcome, then the one-time combat tutorial. Once no event is
armed, Royal Hall becomes Blocked and its resting mist returns. Future Act One
story controllers may arm the existing one-shot Royal Hall event hook; doing so
automatically changes the door back to Plot without creating a new route.

Stuffie Playroom remains Bonus until Baby Eagle’s saved rescue is complete,
then becomes Open. Replays and ordinary room activities do not light a door
unless an explicit, uncollected bonus is registered.

## Hierarchy and accessibility rules

- At most one Plot door may be active in a hall view. Plot outranks Bonus;
  Bonus outranks quiet Open; Blocked is legible but not attention-seeking.
- Colour is redundant with motion: fog drift, no motion, blue breathing/bubbles,
  and gold pulse/rainbow sweep are distinguishable in greyscale or peripheral
  vision.
- Cues never add a second touch target. They are input-transparent and follow
  the exact projected rectangle of the existing door/button.
- A blocked tap gives visible flutter plus short spoken feedback. It never
  silently eats input and never costs progress.
- The implementation is CanvasItem-only and procedural. It reuses the approved
  painted doors, adds no generated art, requires no licence entry, and adds no
  new 3D debt or transparent full-screen layer.
- Direct room calls and elevator choices fail closed through the same resolver;
  visual state and reachability cannot disagree.
