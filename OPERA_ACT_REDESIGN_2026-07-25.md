# Opera acts — full redesign to the Pipe Dream standard

Supersedes the one-line gimmicks in `OPERA_JOB_GIMMICKS_2026-07-25.md`.

**What changed.** That doc gave each act one new verb. One verb produces one
gesture repeated, which is what the owner correctly called basic. The standard
set by the Vet Rescue and Pipe Dream rebuilds is different:

> Design the game the career actually implies, then build whatever it needs —
> grid, queue, flow simulation, case board, whatever. Do not start from the
> existing builder and swap a verb.

Two acts already meet it. The rest are specified below. Every beat names its
gesture, and no act repeats a gesture twice.

## The rhythm every shelled act runs

RESCUE (imps are guarding someone) → GIFT (the freed friends hand something
over) → MAKE (the act runs on exactly that gift). Gifts persist in
`m.opera_pantry`, saved.

| Act | Rescues | Gift | Used for |
| --- | --- | --- | --- |
| Pastry Chef | the farmers | carrots | they go in the bowl — it becomes a carrot cake |
| Painter | another painter | their paints | the pots she paints with; the finished canvas is then HUNG in the gallery |
| Detective | stagehands | lanterns | they light the dark Prop Library: the lens dwell drops from 0.7s to 0.45s |
| Magician | usher crabs | silk scarves | the rope trick — they hold the ends, so every pull is shorter |
| Astronaut | bubble engineers | spare pipes | *(to wire: extra queue pieces)* |
| **Doctor** | **— none —** | **—** | the rescue in that act is the injured animal herself |

The Doctor deliberately has no cages. Its story was already specified: chase the
imps out, then FIND the hurt animal. Bolting caged nurses onto the front of that
would be a second rescue in an act that already has one.

## The six acts that could not run the rhythm — barriers found and resolved

Ballerina, Candy Maker, Farmer, Boxer, Racecar and Pop Star have no
`shell: true`, so they had no way to run rescue → gift → make. Six concrete
construction barriers, all now cleared:

| # | Barrier | Resolution |
| --- | --- | --- |
| 1 | `_build_captives()` was only reachable from `_build_backstage()`, and cage positions were corridor coordinates (`BACKSTAGE_X0`). Acts without a corridor had nowhere to put anyone. | Cages now place relative to the act's own play area when the rescue is on-stage. |
| 2 | `stage_phase` was binary — nine sites branch on `== "brawl"` (movement, clamp, input routing, HUD, pointer, rescue-arrow). No third state existed. | Added `"rescue"`; every one of those branches now accepts it. |
| 3 | Ten acts call `set_drag_mode(true)` at BUILD time. A rescue running first would find the stick dead and Roshan unable to swim to the imps — the exact bug that stalled the Magician. | All routed through `_set_drag()`, which records what the act wants and withholds it until the rescue ends. |
| 4 | Boxer shares the `imps` array between the rescue and its ring waves; `_box_wave()` calls `imps.clear()`. | The rescue completes before the warm-up gate, so the first wave clears an array the rescue is already done with. |
| 5 | Farmer's game is a 2D `CanvasLayer` that covers the whole screen, hiding any 3D rescue behind it. | `farm_layer` is hidden for the rescue and restored when the stage is handed back. |
| 6 | Racecar and Pop Star give the entire screen — camera, HUD, input — to KartGame / DanceEngine. No beat can be inserted inside them. | The rescue happens BEFORE the handoff tap; both early-returns are gated on `stage_phase != "rescue"`. |

All six now open with a rescue: dancers → ribbons, sweet-shop mice → sugar,
farmers → carrots, the ring crew → gloves, pit crew → spare wheels, the band →
instruments.

## Done

**Doctor — the Vet Rescue.** find the hurt animal → carry to the fluoroscope →
read the x-ray → wrap the cast → seal with coban. *(built, unverified)*

**Astronaut Engineer — Pipe Dream.** 4×3 grid, unreorderable 3-deep queue, a
fuse, real connectivity, leaks instead of failure. *(built, unverified)*

---

## Pastry Chef — "The Great Cake Show"

*Cooking Mama's actual structure: a chain where **every step is a different
gesture**. Currently one circular stir with taps either side.*

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **Sift** | scrub | rub back and forth across the sieve; flour snows into the bowl until the meter fills |
| 2 | **Pour** | hold | tip the milk jug and HOLD; a line on the bowl shows enough. Overfilling just slops and giggles |
| 3 | **Stir** | circular drag | *(built)* batter thickens through four visible states |
| 4 | **Bake** | timed tap | slide the tin in, watch it rise through the oven door, tap when it turns golden. Early = "not yet!", late = still fine, just fewer sparkles |
| 5 | **Pipe** | trace | drag along a dotted guide round the cake edge; frosting follows the finger |
| 6 | **Decorate** | drag-and-drop | drag cherries onto the marked spots |

Six gestures, none repeated. Build-and-payoff pacing.

## Detective — "The Missing Tiara"

*Hidden object is only half the genre; the other half is **deduction**.
Currently: find three clues, chest opens. Nothing is deduced.*

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **Search** | drag lens + dwell | *(built)* three clues hide among six boxes |
| 2 | **Match to the friend** | drag-and-drop | *(built)* drag each clue card up to the friend whose colour bar matches it; a wrong pairing slides back with a "hmm?" |
| 3 | *(folded into beat 2)* | — | the original split into "pin" then "match" was two drag-and-drops in a row, which breaks the no-gesture-twice rule. One drag does both. |
| 4 | **Name them** | tap | *(built)* two clues belong to one friend and one to another, so the board can be COUNTED, not read. The friends come down to the stage and she swims over and taps the one holding the most |
| 5 | **Happy ending** | — | they were only borrowing it for the show; the tiara comes back and everyone laughs |

Deduction a non-reader can do: pictures matched to pictures. **No villain** —
the culprit is a friend with a good reason, per the no-fail-states spirit.

## Magician — "The Magic Hat Trick"

*A stage magician performs a **routine of different tricks**. Currently one
trick, three times.*

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **The Vanish** | drag | *(built)* drag a hat over the bunny-fish |
| 2 | **The Shuffle** | track + tap | *(built)* follow it through the dance |
| 3 | **The Rope** | pull-apart drag | *(built)* three knots; drag your finger out wide and each one melts. The usher crabs' silk scarves hold the far ends, so every pull is 45% shorter — the gift is a real helping hand |
| 4 | **The Cabinet** | rhythm tap | *(built)* tap the star wand three times ON the beat; the doors swing wider each time and the bunny-fish comes out enormous. The wand pulses on the beat, so it plays with the phone muted |

Four tricks, four gestures. Call-and-response pacing.

## Painter — "Paint the Sunrise"

*Kids' painting genres are colour-by-number, scratch-reveal and free paint.
Currently only the third.*

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **Sketch** | trace | *(built)* a ten-dot arch hangs over the canvas; the charcoal line sets wherever the finger has passed |
| 2 | **Fill** | **hold**-to-flood | *(built)* three panels wear a circle, a star and a heart; the easel calls one shape and she holds on the matching panel while the colour rises. Specified as a tap, but splatter is already a tap — and the rising colour is better feedback than a region blinking on |
| 3 | **Paint** | drag-to-paint | *(built)* the free sky band, coverage-based |
| 4 | **Splatter** | tap | *(built)* the sparkle-paint finale |
| 5 | **Frame it** | drag-and-drop | drag the gold frame onto the canvas; the gallery curtain drops and the audience gasps |

## Ballerina — "The Dance Recital"

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **Barre warm-up** | hold | *(built)* two slow positions, very forgiving |
| 2 | **The echo** | watch + hold | *(built)* repeat the lit tile phrase |
| 3 | **The ribbon** | trace | *(built)* a 12-dot S-curve hangs in the air; trace it and a bright streak follows the finger |
| 4 | **The twirl** | circular drag | *(built)* three full turns of finger travel; a ring of petals falls on each one |

## Candy Maker — "The Candy Parade"

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **Mix the syrup** | hold | *(built)* swim to the sparkling bottle and HOLD; it tips and pours to its line. The belt does not start until all three are in |
| 2 | **Sort the belt** | drag-and-drop | *(built)* colour chutes, accelerating belt |
| 3 | **Twist the wrappers** | rotational drag | *(built)* three-quarters of a turn per wrapper, three wrappers |
| 4 | **Load the parade cart** | **timed tap** | *(built)* the cart rolls back and forth under the chute; tap when it is underneath. Specified as a second drag-and-drop, which the sort already owns — the cart keeps rolling, so a miss is another pass, never a loss |

## Farmer — "The Piggy Picnic"

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 1 | **Plant** | drag-and-drop | *(built)* four seeds, four furrow holes; any seed suits any hole, because this beat is about the MOTION, not a matching puzzle. The slingshot does not arm until the field is planted |
| 2 | **Feed** | charge-and-release | *(built)* slingshot lob to the trotting piggies |
| 3 | **The mud puddle** | swipe up | *(built)* three piggies, three upward flicks. Up only — down is the boxer's duck |
| 4 | **Home to the barn** | **scrub** | *(built)* sweep back and forth to shoo the herd home; the gate swings wider as the sweeping adds up. Specified as a drag, which the planting already owns |

## Boxer — "The Championship Bout"

Already three beats (bag → rounds on the beat → belt). One addition:

| # | Beat | Gesture | Detail |
|---|---|---|---|
| 2b | **Duck** | swipe down | *(built)* between rounds a big glove swings across; swipe to duck under it — the only defensive verb in the opera. The glove crosses on its own clock, so a child who never swipes just takes a giggling bonk off the bubble shield and the next round rings in |

## Racecar Driver / Pop Star

Borrowed engines that are already good. Additions only:
- **Racecar** — two laps *(built)*; add a pit-stop beat between laps: drag a
  fresh wheel on, tap the fuel bubble.
- **Pop Star** — hold-the-note long arrows, plus an encore verse if the first
  round is clean.

---

## Rules every redesign keeps

1. **No gesture twice in one act.** If two beats want the same verb, one beat
   is wrong.
2. **No fail states.** Every miss is a giggle, a slide-back, a puff, a leak, or
   a pause — never a loss, never a restart.
3. **Difficulty is speed and quantity, never precision.** A four-year-old's
   finger is imprecise; the game must never punish that.
4. **No reading.** Every instruction is a picture, a pointer and a voice line.
5. **Both probe drivers learn a beat before the beat ships**, and each new beat
   asserts that the *previous* input no longer trivially completes it.
6. **Scenery stays in the envelope** (`|x| ≥ 19`, `z ≤ -15.5`, `z ≥ 17`) and
   act one stays inside `_descendants(act) < 170` — batch repeats via `_multi()`.

## Build order

Chef first — six gestures, the largest single jump in quality, and the act the
child meets first on Floor 1. Then Detective (deduction), Magician (routine),
Painter (sketch/fill), then the shorter additions to Ballerina, Candy, Farmer,
Boxer, Racecar and Pop Star.
