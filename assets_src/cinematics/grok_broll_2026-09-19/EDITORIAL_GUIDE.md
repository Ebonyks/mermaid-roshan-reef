# Cutting A-roll and alternate B coverage

These are proposed edit decisions, **not measured existing-clip timecodes**. A and B depict the same event. Usually replace part of an A shot with B; do not play both complete actions back-to-back. Keep the original V2 event order and gameplay gates.

## Picture rhythm

For a normal four-second action, begin with roughly 0.8–1.2 seconds of the A setup, use about 0.8–1.8 seconds of B for the contact or detail, then return only if the A endpoint has the identical resulting state. `PLAN.json` gives phase markers and suggested source spans; re-conform to measured output. A clock match alone is insufficient.

The planned 24 fps/96-frame beat spans are [0,18), [18,78), [78,96). They describe direction, not audited delivered frames. If the actual output is a different frame rate, record it and re-index natively; do not use optical flow or duplicate frames to conceal action gaps. Preserve native output and hashes.

Use one strong insert, not frantic A/B/A/B switching. Avoid a cut of less than about 0.7 seconds unless the action remains immediately readable. Give the new rainbow friend and the fully cleaned castle longer breathing room: usually 2–4 seconds of an earned endpoint. Never pad an unfinished action with a frozen frame. No added film duration is implied by 144 seconds of proposed raw B coverage.

## Scene-specific cuts

| Scene | Best B use | Protect |
|---|---|---|
| Arrival | Low-quarter touchdown, then same grounded plane | Both passengers stay seated; no new exit or second landing |
| Bathroom | Oblique hand/bristle contact; higher tub/drain view | Sink → tub → drain → toilet state chain; water must visibly fall |
| Pool | Low net/litter contact; graded lane views; mouth-plug grip | Flower/star are toys, not litter; waterfall lanes stay cleared; seahorse stays dry at plug-removal cut |
| Craft | Counter height, high-oblique and shoulder views | Four specific supplies; three named surfaces; SMALL STOCKED rear table, not a bare new desk |
| Eagle | Paired restraint contacts, then two-shot wingbeat | Exactly two pinning dust bunnies, not metal pins; one original-book Eagle |
| Giant bunny | Oblique ensemble with all four helpers; lower reveal | Do not replace teamwork with four static solos; suds cover ears, casing collapses during jump; giant gone at landing |
| Hall cleanup | Floor paper, elevated web, medium stain, wide finish | Five companions; each previous mess stays removed; four small left arches/one royal right arch |
| Chapter 2 | Party reaction, rocket contact, royal blocking, claw/candle insert | Protection is already won before theft; King ≠ Daddy; only candle leaves, cake and five strawberries persist |

For DRAIN, rescue, JUMP/LAND and candle theft, keep a continuous causal span whenever an alternate cut cannot preserve exact contact/state. A beautiful insert that conceals the important action is not a useful edit. The B JUMP opening must represent the approved SOAP endpoint world state from its new camera; B LAND must match JUMP's trajectory, not restart the hop. Each new viewpoint needs its own approved whole frame, not a transformed copy of the previous view.

## Spatial checks before splicing

1. Identify a foreground anchor, active contact and a background fixture in both setups. Check adjacency against actual room art, not inferred storyboard geometry.
2. Preserve the A action hemisphere, eyeline and travel direction. Treat proposed angle/elevation values as targets only. If a setup crosses the axis, redesign it or use an explicitly approved neutral establishing view; do not flip pixels.
3. Compare last A/first B frames at the intended splice: same grip, brush orientation, object count, waterline, cleaned fraction, tail direction, airborne trajectory and character size.
4. Do not remove a character from the world because a close view crops them. `cast_instances` describes world presence; mark any framing occlusion in the exact candidate review.
5. Keep action-specific sources separate from layout: a grime texture is not a room angle, a source panorama is not an acted 16:9 frame, and an endpoint is not an action opening.

## Sound continuity

Use a single continuous ambience bed across the cut. Match bathroom splashes/drain gurgle, net drips, brush strokes, cloth friction, light wing movement and gentle landing dust to visible contact. Let an incoming sound lead the cut slightly or an outgoing sound trail it when useful; never play two impacts for one contact. Keep effects soft and child-friendly. The boss reveal can move from wet brushing to light foam pops, a small buoyant accent and a gentle landing, followed by quiet celebration.

Grok generates foley/room tone only, no speech or imitation of the protected family voices. Reuse authorized exact in-game recordings later in the editor, non-destructively and with source/timecode attribution. Music is an editorial layer, not regenerated inconsistently per shot.

## Review and handback

Use `RESHOOT_RETURN_TEMPLATE.json`. Record native fps, file/prompt/input hashes and exact frame ranges for defects. Pair the reviewed A clip hash and cut frame with the B clip hash and cut frame. Mark only `EDIT_REFERENCE_CANDIDATE` after a rough editorial check; this never grants full-frame delivery acceptance. Return corrective requests on GitHub and keep all past attempts.
