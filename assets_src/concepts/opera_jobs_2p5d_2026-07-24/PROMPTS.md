# Opera job 2.5D environment generation record

Date: 2026-07-24

## Purpose

This package corrects the regular Opera job spatial design. The twelve jobs
are short 2.5D side-scrolling story worlds, not mechanics arranged on twelve
literal stages. Literal stages are reserved for the later boss-fight phase.

Every accepted job has:

- `<job>_2p5d_scene_key_2026-07-24.png` — `1024 x 576`;
- `<job>_environment_texture_kit_2026-07-24.png` — `1024 x 1024`.

The source images were generated at `1672 x 941` and `1254 x 1254` with
OpenAI built-in image generation, then high-quality resampled to the
repository-safe dimensions above. The external generated cache is provenance
only and is not required by Claude.

## Shared scene-key prompt contract

Create a wide, polished flat-image prototype for one Mermaid Roshan Opera job
as a 2.5D side-scrolling story world rather than a performance stage.

Binding requirements:

- one continuous, clearly readable left-to-right route;
- a small shell-and-curtain entry portal only at far left;
- broad child-readable mechanic clearings;
- multiple large job-specific landmarks;
- an empty completion destination at far right;
- distinct far parallax, scenic midground, playable midground, and foreground;
- coral, teal, cream, and plum palette;
- navy-purple outlines and aqua/lavender shadows;
- restrained brass, pearl, rope, and shell accents;
- rounded cel-shaded pastel toy-diorama forms;
- simple enough to model for the Mobile renderer;
- no characters, audience, text, UI, logos, copied franchise imagery, full
  proscenium, stage deck, photorealism, or tiny clutter.

## Shared environment-kit prompt contract

Create a strict uniform four-column by four-row contact sheet with exactly
sixteen equal-sized cells and straight dark-blue dividers:

- cells 1–8: large route and landmark modules;
- cells 9–10: two parallax background plates;
- cells 11–16: broad material swatches or repeating guidance trim.

No merged cells, labels, characters, audience, or boss content.

## Job contracts and accepted generation IDs

| Job | Route and continuity lock | Scene generation ID | Kit generation ID |
| --- | --- | --- | --- |
| Pastry Chef | Frosting promenade, mixing bowl, oven bridge, layer rack/lift, cake reveal | `call_CfG2EbP0eSGXS6wA3skUuEGW` | `call_ibxFXXjo7UvqhFamPAHJqZSD` |
| Detective | Moonlit archive, search alcoves, magnifier tower, bookcase passage, chest vault | `call_quj7GEhzA1a6Ctr4R5ic8QQI` | `call_FMNoYul97XmjB1YoOEl1ASJf` |
| Ballerina | Rhythm garden and four identities: coral shell, teal wave, plum ribbon, cream pearl | `call_TIfSQT6p2jNiAIrEPP9U9Stw` | `call_J0YK5OIdIzJ2vE8AlDZFG7eu` |
| Candy Maker | Hopper, press/gauge, conveyor, wrapper village, display destination | `call_caSM3J7jTXajq7dAftGuZIA7` | `call_VBkz698hKhwVUqaoFJeBY2Ck` |
| Doctor | One coral five-armed patient at arrival; later care sequence empty | `call_ZJjyOrA01ZkvJUtY4VJXJuLL` | `call_eeMwULt0cNYtvSFH2mp7qrwG` |
| Farmer | Meadow, orchard, barn, mud lane, exactly nine empty picnic pads; runtime piggies/food | `call_myPg0E4A0RvxcC1ESciZt57X` | `call_6glv8BmPJR3lgeYiCYsOa6Yu` |
| Boxer | Padded route, soft bags, exactly three practice pads, bridge, bell, victory plaza | `call_Qd9ozJpqdDQPtm8N5fxof5vD` | `call_z3LFIy4xHIfAK9FJYitUJZsb` |
| Magician | Three hats in plum/teal/coral order, mirrors, cabinets, swap trail, empty reveal lagoon | `call_aCiGFK2ZicDPB2h8MKbBqsFa` | `call_2Z6i6HlrFIkBunNKMzsRucMl` |
| Painter | Paint stations in plum/coral/cream order, canvas bridge, rinse creek, gallery | `call_0GxlsnEXseDmptUBClcHgvrP` | `call_7i0KV8vHD6jQozRjt2fSOnJl` |
| Astronaut Engineer | Straight/elbow/ring pipes and sockets; bubble propulsion; no flame | `call_W2nqTQeYZcNrMscqB5ix49Dj` | `call_7nkZjpfXh0cu3yLaCxaAQsUD` |
| Racecar Driver | Pit lane, straight, banked curve, bubble bridge, grandstand, finish plaza | `call_3ABac2u57gvM3fszEhkjd7Tw` | `call_0NG9aHYwh3qYYvfnOY47L4mF` |
| Pop Star | Mic promenade, exactly four mapped arrows, speakers, rainbow bridge, city catwalk | `call_IsoCnEn1fL2e0GuN215OssZd` | `call_UqO18bVOqEbn6p1YUO6CRfdU` |

## Automatic rejection record

These candidates were rejected and were not copied into the repository:

| Candidate | Generation ID | Score | Rejection reason |
| --- | --- | ---: | --- |
| Doctor scene v1 | `call_raqwwSWXfJyGEVvGAIcvZI4m` | 4.0 | Duplicated the starfish patient across later care stations |
| Farmer scene v1 | `call_180wa8NsEjdHbGmTTpSzg7W2` | 3.9 | Showed substantially more than nine piggy placements |
| Farmer kit v1 | `call_2nIBS5BYzPeXsoGUBVrlJ5lj` | 4.2 | Baked the wrong food-basket count into the environment |
| Boxer kit v1 | `call_glJqVhUcyN3AqZyIbQ80Y43l` | 4.4 | Omitted the three required practice pads |
| Painter kit v1 | `call_AvFczkTptV3B0oqkYGHu39Xo` | 4.4 | Used merged cells instead of a uniform 4 x 4 kit |

The accepted Farmer kit has nine empty pads and zero baskets. The accepted
Boxer kit has exactly three pads. The accepted Painter kit has sixteen equal
cells.

## Regeneration guidance

Use the accepted repository image as the primary image reference. Preserve its
layout, silhouette, color balance, continuity locks, and lack of characters.
Regenerate only when a modeling angle, tiling study, or construction breakdown
is genuinely missing.

Automatically reject a replacement that:

- scores below 4.5/5;
- returns the job to a literal stage;
- changes a binding count, order, species, color mapping, or object state;
- adds boss content or characters to environment-only art;
- becomes realistic, over-detailed, or expensive to reproduce in 3D;
- uses merged cells in an environment kit;
- adds text, brands, or copied franchise imagery.
