# Chapter 2 Eight-Career Production Spine

Status: current implementation authority for Chapter 2 birthday preparation.
Owner direction incorporated through 2026-08-30.
Supersedes the sequence, tutorial prelude, thirteen-career checklist, generic
Candy Maker result, and early-Detective assumptions in the two earlier Chapter
2 planning documents. Those files remain option/history records only.

## Story promise

Defeating the giant Dust Bunny cleans the castle and begins Mermaid Roshan's
birthday chapter. Eight short occupation games prepare one visible party. Each
game teaches its own touch verb, produces a persistent scene object, and never
depends on the normal Opera freeplay stars. The cake is one exact object built
in stages and later reused unchanged. The unlit rainbow candle is the last
missing party piece. Astronaut Roshan's already-built rocket lights it only at
the party; after a readable lit hold, the Ember King takes the still-glowing
candle because he wants it for his own birthday party. The cake and every other
preparation remain safe.

## Locked roster, bits, and order

Chapter 2 reuses the stable Opera bit identities but owns an independent story
mask. Global Opera follows `OPERA_ACTIVE_STAR_MASK` in
[`scripts/save_state.gd`](../scripts/save_state.gd); do not copy the historical
thirteen-career mask into new work. Chapter 2 is exactly `0x2C4F` and keeps its
eight-job sequence independently of later global career additions.

| Step | Bit | Career | Scene | Persistent result |
| ---: | ---: | --- | --- | --- |
| 1 | 6 | Farmer | Sky Lagoon strawberry grove | five fresh strawberries delivered in a basket |
| 2 | 0 | Pastry Chef | Castle Kitchen | the actual tiered cake, stacked and frosted |
| 3 | 3 | Candy Maker | cake-decorating workstation | those strawberries candied and placed; final cake locked |
| 4 | 10 | Painter | Craft Room to Main Hall | painted/stamped birthday banner hung in Main Hall |
| 5 | 2 | Ballerina | Stuffie Playroom | stuffies mirror, twirl, bow, and keep their dance staging |
| 6 | 13 | Pop Star | Opera stage with Rumi | sound check, musical echo, and party-song staging |
| 7 | 11 | Astronaut Engineer | Mermaid Pool/Main Hall launch station | candle-lighting rocket built, tested, and parked unlaunched |
| 8 | 1 | Detective | Royal Library | final missing unlit rainbow candle revealed in the magic storybook |

Canonical sequence array: `[6, 0, 3, 10, 2, 13, 11, 1]`.

The first visible/unlocked wave is Farmer, Chef, Candy Maker, and Painter
(`0x0449`). Finishing Painter reveals the second wave: Ballerina, Pop Star,
Astronaut, and Detective. Within either wave, only the next required story job
can launch or earn progress, so the single cake and late-candle causality stay
intact while the Opera House still opens with four career possibilities.

Only the next required career can earn Chapter 2 progress. Ballerina and
Detective activate through their authored room plot surface; this is not a
general room-ability clause. Their first in-story phase teaches the ability and
their completion records the learned skill. There is no duplicate four-game
tutorial prelude.

## Opera mechanic reuse

- Farmer: reuse large tap/hold/placement surfaces for five berry pickups,
  washing, basket loading, and delivery. No piggy picnic result.
- Chef: reuse pour, circle, oven, tap, and swipe for mix, stir, bake tiers,
  stack, and frost.
- Candy Maker: reuse pour, sort, circle, and tap for sugar coating, strawberry
  sorting, glaze, and final cake placement. No candy bag or guest favour.
- Painter: reuse paint reveal, stamps, and choice for the real birthday banner.
- Ballerina: reuse Pearl Mirror, Ribbon Trail, and Grand Twirl with stuffies
  visibly mirroring and bowing.
- Pop Star: reuse sound-check hold, staging choice, echo, and encore circle.
  Rumi responds through approved animation and notes; no invented Rumi voice.
- Astronaut: reuse pipe, patch, valve, and ready/park gestures. Career
  completion never launches or lights the candle.
- Detective: reuse lens, case-board, and reveal mechanics reskinned to rainbow
  wax clues, magic storybook, and the unlit candle. No crown result.

## Persistent construction authority

- `chapter2_strawberry_mask`: five pickups, required `0x1F`.
- `chapter2_cake_piece_mask`: bit 0 batter mixed, bit 1 batter stirred, bit 2
  six red/orange/yellow/green/blue/violet tiers baked, bit 3 those same tiers
  stacked in order, bit 4 frosted, bit 5 strawberries candied, bit 6 candied
  strawberries placed; required `0x7F`. Legacy field aliases remain readable,
  but the visible state never substitutes a differently coloured three-tier
  placeholder.
- `chapter2_job_phase_masks`: fixed eight-entry phase-resume record keyed by
  the canonical sequence ordinal.
- `chapter2_party_piece_mask`: career-result mask `0x2C4F`.
- `chapter2_party_event_phase`: 0 preparation, 1 candle found, 2 ignition/lit
  hold, 3 scout seen, 4 Ember King take complete. Legacy booleans are derived
  compatibility mirrors.

Every meaningful milestone saves immediately and reconstructs the same visual
state after exit, focus loss, or app restart. Later states cannot erase earlier
ones. Malformed/future bits mask away, impossible later event states heal back
to the highest causally supported phase, and unrelated save keys survive.

The active final cake candidate is
`assets/chapter2/birthday/chapter2_grand_five_strawberry_cake.png`: six tiers
in top-to-bottom red, orange, yellow, green, blue, violet order, with exactly
the five Farmer/Candy Maker strawberries and no baked candle. The earlier
ten-strawberry 4.9/5 test model remains preserved but is superseded for story
continuity. Exact hashes, generation, derivation, and review evidence are in
the 2026-08-31 cake-progression provenance package. Owner/device/child
acceptance remain separate gates.

## Blocking acceptance gates

- Exact Godot 4.7.2 parser/analyzer/import and trusted probe suite.
- Strict-order, wrong-room/world, passive/no-input, re-entry, and teardown
  probes; no progress from hints or time alone.
- Save tests at every berry, cake, job-phase, candle, ignition, scout, and take
  boundary, including malformed types and backup recovery.
- True Canvas/2D and Mobile/Speedy no-regression; `NO_REGRESSION` never means
  the repository's remaining global 2D debt is satisfied.
- Scene captures at every cake layer and all eight persistent party states,
  followed by human identity/topology/style review.
- One-finger targets at least 96 px, no fail states or timers, immediate visual
  cue, moving pointer, and approved scene-specific voice for every required
  objective. Generic `roshan/talk` is a fallback implementation gap, not sound
  acceptance.
- Target Lenovo device 30 fps, repeated enter/leave/re-enter, owner review, and
  four-year-old comprehension/play acceptance.
