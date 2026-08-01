# Pearl Opera Nursery — Generated Art Provenance

Date: 2026-08-01
Method: OpenAI built-in image generation, followed by deterministic chroma
removal and lossless-alpha sizing/splitting. These are runtime character and
interaction cutouts, not cinematic frames.

## Why generation was needed

The repository inventory had protected Faron/baby story art, a portrait-format
nursery reference, and Roshan's medical outfit. It did not have an Opera-ready
nursery-nurse Roshan, an adult Nurse Faron cutout, or separated baby sprites
that could support the catch/feed/burp/bed loop. The room itself is code-native
to satisfy the per-screen background-resolution rule without spending another
generation on a raster plate.

No file in `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified. Those files were identity and age
references only.

## Accepted generations

### Nursery Nurse Roshan

- Generation id: `exec-891faa38-07ee-44e0-a42f-f6d1df100715`
- Identity/style references: existing project-authored
  `assets/opera/worlds/actors/roshan_doctor.png` and
  `assets/opera/worlds/actors/roshan_farmer.png`.
- Recorded generation brief: one complete isolated 2D storybook cutout of
  Mermaid Roshan, matching her child identity, face, hair, crown and rainbow
  tail; a clearly non-medical aqua/lavender nursery smock; warm baby bottle and
  peach burp cloth; rounded shapes, navy/purple outlines, pastel cel shading;
  no stethoscope, X-ray, cast, syringe, readable text, extra people, crop, or
  shadow; flat bright-green chroma field.
- Native accepted frame: `roshan_nursery_nurse_chroma.png`.
- Non-destructive alpha master: `roshan_nursery_nurse_alpha.png`.
- Runtime derivative: `assets/opera/worlds/actors/roshan_nursery.png`.

### Nurse Faron

- Generation id: `exec-a7126a92-4250-464a-917d-484b6a1aac3d`
- Identity/style references: protected
  `assets/characters/friends/mama_baby.png` for Faron's adult blonde/burgundy
  identity and the accepted Nursery Nurse Roshan generation for render style.
- Recorded generation brief: one complete isolated adult mermaid Nurse Faron,
  preserving her blonde hair, mature face and burgundy tail; cream/aqua nursery
  apron; calmly cradling exactly one mint-swaddled baby; warm, competent,
  cooperative expression; polished pastel storybook cel shading and dark
  plum/navy outline; no medical equipment, extra babies, crop, text, or shadow;
  flat bright-green chroma field.
- Native accepted frame: `faron_nursery_nurse_chroma.png`.
- Non-destructive alpha master: `faron_nursery_nurse_alpha.png`.
- Runtime derivative: `assets/opera/worlds/actors/faron_nursery.png`.

### Baby trio

- Generation id: `exec-e3f2699f-6989-4c4e-babd-0c5f1ce29b16`
- Identity/age references: protected `assets/book/baby_doll.png`,
  `assets/book/baby_doll2.png`, and `assets/book/baby_doll3.png`.
- Recorded generation brief: exactly three separate, equally spaced,
  full-body swaddled newborn baby cutouts in mint, peach and lavender; same
  infant age/readability as the project references; safe happy/sleepy faces,
  distinct silhouettes and generous empty lane separation; polished pastel
  storybook cel shading and dark outline; no adult, props, extra limbs, overlap,
  text, crop, or shadow; flat bright-green chroma field.
- Native accepted frame: `nursery_baby_trio_chroma.png`.
- Non-destructive alpha master: `nursery_baby_trio_alpha.png`.
- Runtime derivatives: `assets/opera/worlds/nursery/baby_0.png` through
  `baby_2.png`.

## Human visual acceptance

| Asset | Identity/anatomy/topology | Style and gameplay readability | Decision |
| --- | --- | --- | --- |
| Nursery Nurse Roshan | Roshan face, hair, crown, two arms and single rainbow tail remain coherent | bottle and burp cloth read at card size; aqua/lavender nursery smock has no medical silhouette | accepted |
| Nurse Faron | adult proportions, blonde identity, two arms and single burgundy tail remain coherent; exactly one held baby | warm competent nurse pose reads separately from Roshan; cream/aqua apron matches nursery palette | accepted |
| Three-baby sheet | exactly three isolated infants, complete swaddles, coherent faces and limbs, no overlap between equal lanes | mint/peach/lavender silhouettes remain distinct at 320×320 and on the dark catch panel | accepted |

No accepted subject is cropped, scary, text-dependent, branded, or confused
with Stuffie Surgeon's X-ray/cast language.

## Deterministic derivation and acceptance

The skill chroma helper removed only the flat green field with a soft matte and
despill. `tools/prepare_opera_nursery_art.py` then fits whole isolated subjects
onto transparent canvases (512×512 actors), or splits the deliberately authored
three equal baby lanes before fitting each whole baby to 320×320. It performs
no subject warping, repainting, compositing with protected pixels, or destructive
overwrite.

`python tools/prepare_opera_nursery_art.py --check-only` validates dimensions,
transparent corners, plausible subject coverage, and green-key residue. Accepted
coverage is 0.370 (Roshan), 0.269 (Faron), and 0.318 for each baby; all five
runtime files have zero detected key-residue pixels. See `SHA256SUMS` for source,
alpha-master and runtime hashes.
