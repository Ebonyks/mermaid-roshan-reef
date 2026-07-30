# Codex critique — Fable Pearl Castle animation and interactivity handoff

**Date:** 2026-07-29
**Reviewed source:** `FABLE_CASTLE_ANIMATION_INTERACTIVITY_HANDOFF_2026-07-29.md`
**Implementation baseline:** `origin/dev` at `1b385231`

## Decision

Accept the brief's diagnosis and its shared-system direction, but do not
commission or derive the proposed art batch yet. Prove the interaction language
with approved cards and painted-scene reaction zones first.

The implemented pass therefore adds:

- one bounded, data-driven ambient tick for existing approved `Sprite3D` cards;
- one round-robin invitation glint, retained at a slower rate on Speedy;
- immediate sparkle and pitch escalation for taps received while a prop is busy;
- two or more 112-pixel-minimum reaction zones over readable painted features in
  every destination room;
- a real cozy light toggle on the existing Royal Library pearl lamp;
- wordless object-and-Roshan moments for kitchen, library, pool, and bath;
- one effect-card cap and a Speedy ambient-work reduction;
- acceptance-probe coverage for motion, reaction zones, rapid taps, hotspot
  size, Speedy scaling, and the effect cap.

No original or runtime art was modified, no new image was generated, and no
new audio was added.

## What the Fable brief gets right

1. The primary problem is interaction language, not room composition. Existing
   props are attractive and readable, but their complete stillness makes them
   look finished rather than touchable.
2. A single ambient tick is the correct mobile architecture. Per-card looping
   tweens would be harder to suspend, budget, reset exactly, and probe.
3. Text-only room actions are not a payoff for this non-reader. Kitchen,
   library, pool, and bath need visible and audible cause-and-effect.
4. The local castle hotspot system should remain local. Re-enabling the global
   3D interaction registry would break an already-probed ownership boundary.
5. Existing art and pitch-shifted sound families should be exhausted before
   requesting more generated assets.

## Corrections

### The baseline is already slightly stale

The handoff audited `223bfe82`. Current `origin/dev` includes `1b385231`,
which animates Roshan's primary 2.5D sprite in the castle. The suggested
transform-only travel bob is therefore not a first-pass gap and could fight the
new frame animation.

### The claimed miss rate is not measured

The statement that roughly 80 percent of taps land on nothing is plausible but
has no tap telemetry, coordinate map, or adversarial sampling evidence. It
should not justify a large extraction batch by itself. This pass instead adds
explicit, probe-visible reaction zones over the most obvious inert features.
Their locations can be adjusted after device playtesting without regenerating
art.

### The derived-art phase is too broad for art finalization

The proposed duck, pans, kettle, potion shelf, toy-bin heads, curtains,
balconies, ribbons, book spines, chairs, brush pot, glow zone, signs, and fish
would require many clean extractions and repaired backgrounds. That work risks:

- placing a moving cutout over the same object still painted underneath;
- style or texture drift while healing approved masters;
- introducing overlap and depth errors before the interaction system is proven;
- consuming art-finalization time on optional reactions.

Those candidates remain valid only after a device test shows that a localized
reaction on the approved painting is insufficient. Any accepted extraction
must still use a new path, preserve its master, record provenance, and remove
the painted duplicate cleanly.

### The two budget rules conflict

The brief calls invitation glints the shared discoverability language, then
turns ambient motes off entirely on Speedy. It also proposes four-live-mote
ambient limits alongside 9–14-mote room parties. The implemented rule is
clearer:

- ambient transform work is halved on Speedy;
- one invitation glint remains, but arrives less often;
- all transient effect cards share a hard cap of 18 normally and 10 on Speedy.

### Queued replay is delayed feedback

Replaying a full animation for every tap queued during `busy` can leave a prop
moving and sounding after the child has stopped, while holding the prop busy
for several seconds. Rapid taps now receive feedback immediately: each tap
gets a small sparkle response and a stepped pitch, with a combo cap of three.
The original authored transform completes once and resets exactly.

### Shared moments should precede bespoke spectacles

Four separate art-heavy parties are unnecessary to establish a wordless
payoff. The implemented helper sequences the room's existing touch props,
plays a room-colored finale burst, and gives Roshan a landing hop. The result
is room-specific because the approved objects and sounds differ, while the
runtime and probe contract remain shared.

## Deliberately deferred

- background extraction or healing;
- new ripple, bubble, fish, open-book, duck, pan, curtain, or ribbon art;
- new duck, droplet, or page-flip audio;
- extra world `Light3D` nodes;
- per-card ambient tweens;
- fountain re-homing in the wide hall until its exact overlap with the current
  two-screen master is visually audited.

The unused legacy `ROOM_ITEMS["main_hall"]` configuration was removed. Its
approved source files remain untouched for a later measured placement pass.
