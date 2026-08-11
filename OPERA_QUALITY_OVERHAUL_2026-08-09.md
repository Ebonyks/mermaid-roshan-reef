# Opera House quality overhaul — 2026-08-09

## Child-facing contract

The shipping path remains a one-finger, non-reader, no-fail theatre adventure.
Its shared identity is the Opera House: painted career worlds, Roshan's costume,
wordless golden teaching, a short complication, a stage finale, applause, and a
saved star. The playable verb now belongs to the career instead of using the
same brawl with different clothes.

## Measured baseline and result

| Measure | Previous shipping table | Overhauled table |
|---|---:|---:|
| Career games | 13 | 13 |
| Total phases | 86 | 52 |
| Identical `bop` combat phases | 29 | 1 (Boxer only) |
| Careers opening with combat | 13 | 0 |
| Distinct runtime modes | 15 | 19 |
| Generated Roshan costume frames used at runtime | 0 | 208 |

The shorter 52-beat table removes filler; it does not remove the career arc.
Shared primitives such as tap, hold, swipe, choice, and circle remain useful
motor-language similarities, but each career has a signature engine and a
different sequence/rhythm around those primitives.

## Career fit audit

| Career | Signature play | Supporting beats | Why it fits |
|---|---|---|---|
| Chef | Pour and remove-at-gold oven | Stir, frost, top | A complete cake-making sequence; no unrelated chase |
| Detective | Free magnifying-lens search | Case board, crown chest | Observe, connect, resolve |
| Ballerina | Watch-and-repeat four-step phrase | Held pose, ribbon arc, twirl | Memory and graceful sustained motion rather than combat |
| Candy Maker | Drag candies to shape bins | Syrup pour, wrapper twist, sharing | Sorting and confection work are visually causal |
| Plushy Doctor | Sweep the X-ray scanner | Wash, choose patient, cast, bandage | A gentle clinic sequence with no scary consequence |
| Farmer | Pull-back vegetable lob | Plant, herd, picnic | Distinct safe arc physics and animal care |
| Boxer | Left/right focus-mitt rhythm with duck | One friendly title bout, belt | The only job where padded combat is thematically correct |
| Magician | Follow the shuffled hat | Vanish hold, rope, cabinet, portal | Attention and transformation form a coherent trick show |
| Painter | Stroke-to-reveal coverage canvas | Stamps, gallery choice | Marks reveal the actual painting rather than filling a generic meter |
| Astronaut Engineer | Connect fuel pipes | Patch, valve, launch hold | Logical construction leads visibly to launch |
| Racecar Driver | Existing short kart engine | Wrench turn, push to line | Preparation leads to one real lap; no imitation race meter |
| Nursery Nurse | Safe falling-baby cradle | Wash, feed, paced pat, tuck | Cooperative care only; no imp fight or baby chase |
| Pop Star | Listen-and-echo star phrase | Soundcheck, dance cue, encore | Call-and-response distinguishes music from generic tapping |

## Runtime quality corrections

- Competition clocks now begin when the visible finale begins. Detective's
  guided retry can no longer be consumed during hidden setup.
- Every task is assigned to a named painted landmark. Blind left-to-right
  station assignment no longer sends a job to an unrelated prop.
- Nursery has authored route/station data, reachable burp visuals, a downward
  bedtime swipe, and no pasted-in combat beats.
- Demonstration hands now show the real operation: directional swipe, held
  pitcher, oven mitt timing, pipe placement, and echo response. Stationary
  presses cannot earn swipe/circle/hold progress.
- Action cards choose the safer side of the stage and are probed against the
  actor's visual rectangle. Roshan is no longer hidden/cut off by the card.
- The 1280×720 stage is uniformly scaled and centered at other aspect ratios;
  character proportions are never stretched to fill the viewport.
- A dialogue-skip press is consumed before task input, preventing one touch
  from both skipping a line and scoring underneath it.
- Generic `talk.ogg` is no longer treated as an exact recording of arbitrary
  instructions, so captions remain available when an exact line is absent.

## Costume-animation acceptance

All 13 costumes use the same explicit 4×4 contract: idle, travel, work, cheer;
four chronological frames per row. Every accepted native and runtime cell was
reviewed at full resolution for identity, costume continuity, one continuous
mermaid tail, no human legs, attached props, and stray artifacts. Rejected
Chef, Ballerina, Candy Maker, Farmer, Nursery, Painter, and Astronaut attempts
were regenerated rather than repaired by hiding/cropping. The immutable hashes
and rejection reasons are in
`assets_src/imagegen/opera_roshan_animation_2026-08-09/OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json`.

`python tools/audit_opera_roshan_animation.py` is a hard local release gate. It
reopens all 208 runtime cells, requires 14px or more alpha-safe padding, rejects
duplicate frames, verifies source/pack/runtime hashes, and refuses delivery
without every semantic human-review checkbox.

## Remaining device review

The automated gates cover causality, no passive wins, topology, clipping,
animation state changes, teardown, and save behavior. Final owner review on the
Lenovo Tab M11 should still judge touch comfort, voice/caption balance, and
whether Nursery's wide-tail atlas reads large enough at the actual viewing
distance. Those are presentation sign-offs, not known gameplay blockers.
