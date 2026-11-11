# Touch pointer contract — 2026-11-11

Owner report: *"problems with bounded and unbounded areas being unclear …
inconsistent object interaction … not effective support for both pointing and
tapping, as well as point and drag. Both need to be compatible working
systems."*

Follows `TOUCH_AUDIT_2026-08-03.md`. Hybrid touch only; Classic stays the
untouched runtime rollback.

## What was wrong

| symptom | cause |
| --- | --- |
| Point-and-drag worked in some places and not others | Three separate hold/drag-to-travel readers (`sky_lagoon_promenade._tick_hold_travel`, `side_scroll` walk, `side_scroll` swim) each polled Godot's **emulated mouse**, which only knows the first finger and nothing about who owns it. The swim reader skipped the reserved-zone guard (`MA-TOUCH-002`). The free-swim reef and arenas had **no** drag travel at all: a world drag there only fed combat slices. |
| Same drag gesture meant two things | In the lower-left thumb bay a drag is an invisible relative stick; elsewhere it did nothing. Nothing on screen showed which one you were in. |
| Edges were invisible | A tap past the reef dome or arena wall was silently clamped (`TapMoveDirector._clamp_target`); a tap past either end of the Lagoon path was silently snapped. She just stopped short. |
| Objects behaved differently by place | Reef: first tap selects **and swims to** the object, second tap uses it. Lagoon: first tap only selected; she stayed where she was. |

## The contract now

**One owner.** `touch_ui.gd` publishes the primary open-world finger as
`world_point()` — `{pos, start, held, moved, consumed, serial}`. It never
includes the action bubble, thumb bay, pause corner, extra fingers, or a press
that fired on an enemy/opaque stage.

**Tap and point are one gesture family.**

| gesture | meaning |
| --- | --- |
| quick unmoved press | **tap** — released as `world_touched` (select / go there) |
| held ≥ `HOLD_MS` (200 ms) or moved past `TAP_SLOP` | **point** — she follows the finger for as long as it is down |
| point that *landed on* a toy/friend and has not moved | still a **select**, resolved as the tap on lift |
| a point that was used for travel | never also fires a tap on lift (`mark_world_point_steered`) |
| moved world drag in combat | still a blade **slice** on lift, as before |

Every travel surface reads that one channel:

* free swim + arenas — `ReefMain._tick_touch_follow` → `TapMoveDirector.follow_screen`
  re-aims the same assisted route a tap starts (same projection, clamp, steering);
* Sky Lagoon promenade — `_tick_hold_travel`;
* side-scroll stages — `SideScrollStage.travel_pointer()` (Classic/desktop keep
  the legacy reader behind `reserved_zone_hit`).

**Visible boundaries.** A screen-space destination ring (`TravelGoalMarker`)
shows every free-travel promise, tapped or dragged:

* mint ring — "she is going here";
* lavender ring crossed by an ink bar, with one small wobble — "this is as far
  as the world goes": the finger asked for somewhere past the edge, and the ring
  sits where she will actually stop. Roshan also says *"This is as far as I can
  swim!"* (at most every 9 s).

The ring is heartbeat-driven: it vanishes within a few frames of its route
ending, so it can never go stale across transitions or overlays. Object routes
keep their own focus ring/cue instead.

**Visible stick.** The thumb-bay ring now appears under the finger while it
is actually steering, so the relative stick is visibly a different verb from
pointing.

**One object language.** First touch = choose it and go to it; arrive; second
touch or the action bubble = use it. The Lagoon now walks her to a chosen toy
(stopping short of the castle doorstep so choosing the castle does not also
enter it). The Reef route marker keeps its deliberate one-tap exit.

## Guards

`probe_touch_router.gd` → `_pointer_contract_gate`: reserved controls never
become a point; a quick press is exactly one tap; a drag is a moving point that
steers her under the finger and shows the marker; a still hold past `HOLD_MS`
steers; neither steering gesture fires a tap on lift; an edge-clamped route
reports and shows the edge ring; the ring disappears after its route ends.
Unlike the emulated-mouse path, the router channel is fully exercised by the
headless synthetic touches the stress probes already inject.

Still worth one minute on the real phone: hold and drag on open water in the
reef, the Lagoon, and a side-scroll stage; drag past the reef edge.
