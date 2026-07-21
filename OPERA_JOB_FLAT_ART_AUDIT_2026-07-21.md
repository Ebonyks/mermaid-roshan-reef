# Opera House job flat-art audit — 2026-07-21

## Outcome

All twelve playable, non-boss Opera House jobs now have a three-sheet flat
prototype package:

1. Roshan outfit and silhouette design.
2. Core subgame props and mechanical states.
3. Stage dressing, guidance, retry, and completion states.

This is 36 accepted 4 x 4 sheets and 576 individually sliced model-reference
cards. Every accepted sheet scores at least 4.7/5 against a 4.5 pass threshold;
the computer-audit maximum remains 4.9. No boss assets were generated.

The full-set contact sheet is
`audit/opera_job_flat_contact_sheet_2026-07-21.png`; the exact per-card mapping
is `audit/opera_job_flat_prototype_ledger_2026-07-21.csv`.

## Scope source and continuity correction

The live source of truth is `scripts/opera_house.gd`, not the older request
note. The playable jobs audited are:

- Floor 1: Pastry Chef, Detective, Ballerina, Candy Maker.
- Floor 2: Doctor, Farmer, Boxer, Magician.
- Floor 3: Painter, Astronaut Engineer, Racecar Driver, Pop Star.

`OPERA_ASSET_REQUESTS_2026-07-19.md` still named an older Opera Star act in the
Boxer slot. This delivery corrects that stale section to match the shipped
Boxer / “The Championship Bout” implementation.

Deferred by owner instruction: Curtain Dragon, Shadow Phantom, and Midnight
Maestro boss fights.

## Audit method

Every generation was reviewed at native resolution, then all accepted images
were reviewed together in a fixed 6 x 6 contact sheet. The combined pass
checked:

- Roshan identity, continuous mermaid anatomy, clean hands, and uncropped poses.
- Job-specific silhouette diversity; no outfit may read as a simple recolor.
- Exact correspondence to the live one-touch mechanic and its ordered states.
- Consistent coral/teal/cream/plum palette, navy field/outline, aqua/lavender
  shadows, and restrained shell/pearl/brass ornament.
- Non-reader guidance and a gentle retry loop rather than failure imagery.
- Rounded, low-complexity construction suitable for later Mobile-safe 3D work.
- No boss content, copied franchise motifs, text-dependent signage, logos,
  realistic rendering, or accidental backpack imagery.

Automatic rejection applied to wrong species, wrong sequence/order, bipedal
Roshan anatomy, duplicate filler, clipped cells, frightening/punitive states,
and any score below 4.5.

## Accepted scores

| Floor | Job | Outfit | Gameplay | Stage/states | Continuity result |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | Pastry Chef | 4.7 | 4.8 | 4.8 | Three layer colors, stir, oven, toppings, and cake reveal align. |
| 1 | Detective | 4.8 | 4.8 | 4.8 | Six box silhouettes, three clues, decoys, chest, and tiara are distinct. |
| 1 | Ballerina | 4.8 | 4.8 | 4.8 | Four icon-plus-color tiles support watch/repeat without reading. |
| 1 | Candy Maker | 4.7 | 4.8 | 4.8 | Press states, broad safe timing zone, seven candy silhouettes, and shelf states align. |
| 2 | Doctor | 4.8 | 4.8 | 4.8 | One five-armed coral starfish patient persists through listen, warmth, kiss, bandage, and recovery. |
| 2 | Farmer | 4.7 | 4.8 | 4.8 | Piggy pose cycle, five foods, toss arc, three parallax layers, and picnic finale align. |
| 2 | Boxer | 4.8 | 4.8 | 4.8 | Padded ring, three round lamps, friendly imp bop, and belt reward match the live act. |
| 2 | Magician | 4.7 | 4.7 | 4.8 | Bunny-fish remains a finned fish with rabbit ears across shuffle and reveal states. |
| 3 | Painter | 4.8 | 4.8 | 4.8 | All order cues use plum, coral, cream; canvas milestones and splats align. |
| 3 | Astronaut Engineer | 4.8 | 4.8 | 4.8 | Straight, elbow, ring pieces each have matching sockets and fitted states; valve launches bubbles. |
| 3 | Racecar Driver | 4.8 | 4.8 | 4.8 | Tail-safe kart, controls, boost, finish, and reward add Opera identity without rebuilding the engine. |
| 3 | Pop Star | 4.8 | 4.8 | 4.8 | Pearl microphone and four direction/color arrows drive the concert sequence without text. |

Mean accepted sheet score: 4.78/5. Lowest accepted score: 4.7/5. All 36
accepted sheets clear the 4.5 threshold.

## Rejected and regenerated sheets

| Rejected sheet | Score | Finding | Accepted correction |
| --- | ---: | --- | --- |
| Doctor outfit draft | 4.1 | Two interaction poses substituted an axolotl-like plush. | Regenerated against the accepted five-armed starfish gameplay sheet. |
| Doctor stage draft | 3.9 | Most patient states became teddy bears, breaking the live starfish sequence. | Regenerated with a strict one-species patient lock; every patient is now a coral starfish plush. |
| Painter stage draft | 4.3 | The order board showed coral, cream, plum, contradicting the shipped sequence. | Regenerated with plum, coral, cream locked across pots, board, pointer, swipe, and retry. |

Rejected raw images remain outside the repository in the generation cache and
are recorded in the batch `PROMPTS.md`.

## Cross-job consistency and variety

- Roshan's face, hair, rainbow streak, tail scales, and split fin remain stable
  across all twelve outfits.
- Each job uses a different dominant silhouette: chef toque, detective
  cape/cap, ballerina petal tutu, candy parade cap/vest, clinic coat, woven farm
  hat, padded boxer vest/gloves, magician top hat/cape, painter beret/smock,
  bubble helmet/tool belt, open racing helmet/jacket, and pop stage ribbons.
- Shell/pearl/brass details provide Opera House family resemblance without
  becoming the primary shape of every prop.
- Effects are broad authored ribbons, ripples, bubbles, and glows. They avoid
  dense transparent particle stacks that would be expensive on Speedy tier.
- Generic stars are absent as a repeated motif; pictograms come from the job
  itself. The Starlight Concert uses direction arrows, pearls, sound rings, and
  rainbow light rather than star mascots.
- No boss silhouette, boss prop, boss reward, or boss interaction appears in
  the accepted package.

## Non-reader and no-fail continuity

- Color is paired with shape or direction whenever it carries gameplay meaning.
- Each objective has an isolated golden shell/pearl pointer concept.
- Retry states reset, breathe, or return the prop; they never show a red X,
  injury, loss text, score penalty, or frightening response.
- Completion is communicated with an authored reveal, reward pedestal, pearl
  bloom, bow marker, bubbles, or short confetti state.
- 3D implementation must still fire the existing `_say()` voice line and a
  visual pointer when the job begins; the concepts do not replace that runtime
  accessibility requirement.

## Mobile and 3D translation constraints

- All 36 accepted source sheets are 1024 x 1024; all 576 cards are 256 x 256.
- Prototype rasters are review/model-reference art under `assets_src/.gdignore`,
  not runtime sprite replacements.
- Prefer instanced shared stage modules and job-specific hero props.
- Use opaque matte materials and limited emissive planes; no new OmniLights.
- Bubble/ribbon/confetti effects need strict Speedy-tier caps and no deep
  transparency layering.
- Roshan outfit concepts are design references for the character pipeline.
  They do not authorize overwriting protected book art, voices, or friend
  cutouts.
- Collision should follow interaction affordances only: floor/ring/track,
  large machines, and touch targets. Decorative scenic flats should not become
  physics bodies.

## Packaging verification

`python tools/slice_opera_job_prototypes.py` completed with:

```text
OPERA_JOB_FLAT|sheets=36|cards=576
```

The generated ledger contains 576 accepted rows, and a dimension audit found
no source sheet above the repository's 1024-pixel limit.
