# Combat tutorial generated art provenance (2026-08-01)

## Scope and reuse audit

This batch answers requests 1-4 in
`COMBAT_TUTORIAL_CODEX_ASSETS_2026-08-01.md`.

- No existing arena background fits the requested lavender training-grotto
  composition with a quiet central stage.
- No existing raster ghost hand or matching icon-only TAP/HOLD chips were found.
- Request 5 (`sparring_imp_band.png`) was deliberately skipped. The shipped
  mischief imp is `assets/dungeon/mischief_imp.glb`; there is no editable face
  sheet from which to make the requested cheap, attribution-preserving raster
  derivative. The standard imp remains the approved fallback.
- Approved Pearl Castle room masters were inventoried for style guidance. A
  reference-backed built-in generation call was attempted for the backdrop but
  stopped before generation because the Windows tool sandbox could not read the
  local reference paths. No failed-call artifact was created. The accepted call
  therefore encoded the project's approved style rules directly in its prompt.

Generation method: OpenAI built-in image generation (not the API/CLI fallback).
The generated art is project original. No external or protected project pixels
are present in the generated deliverables.

## 1. Training grotto backdrop

- Built-in generation id: `exec-a65ad6ab-3db2-4d65-b09b-f33c50e8655b`
- Native preservation master:
  `training_grotto_backdrop_native.png`, 1774x887 RGB,
  SHA-256 `b4f2e9e56581732a01ea3d3d97b3580f2d4457c19e351d0040e1f9367c4b56fd`
- Runtime derivative:
  `assets/castle/training/training_grotto_backdrop.png`, 2048x1024 RGB,
  SHA-256 `0bf0a0218b8733323d5a0fdbf4740c30117081a1976b0e904248186669f25009`
- Processing: one whole-canvas 2:1 high-quality bicubic resize. No crop,
  masking, compositing, local repaint, or subject movement.

```text
Use case: stylized-concept
Asset type: finished 2D game environment backdrop for Mermaid Roshan's child-friendly combat tutorial
Primary request: Create one complete wide underwater sparring grotto backdrop for a friendly practice class.
Scene/backdrop: cozy lavender and periwinkle underwater training nook carved into a rounded grotto; broad coral-stone pillars only at the outer sides; one small rack of oversized toy bubble wands off to a side; a few soft kelp pennants high along the side walls; sparse bubbles and gentle broad cyan god-rays.
Composition/framing: straight-on wide side-stage view, exact 2:1 composition intended for 2048x1024. Keep the central 55% of the image deliberately empty, quiet, and low-detail so a separate 3D octagonal arena, player, and practice imp can stand in front. Leave a broad clean floor/horizon zone; frame details at edges only. No painted arena, ring, platform, podium, or character.
Style/medium: polished flat-color children's storybook cel illustration matching an established pastel underwater toy-playset game; rounded readable silhouettes; two or three broad value bands; crisp deliberate shadow shapes; thin clean dark-indigo contours; extremely restrained grain inside color regions only; matte-to-satin surfaces; readable at 1280x720 on a mobile device.
Lighting/mood: welcoming, safe, calm practice room; high-key underwater cyan fill; gentle lavender shadows; warm pearl-cream highlights; no menace.
Color palette: lavender, periwinkle, aqua, pearl cream, small muted coral-pink accents; avoid all-blue monotony and avoid neon over large areas.
Constraints: one complete full-frame opaque image; seamless single composition; no characters, creatures, hands, weapons, throne, UI, signs, letters, numbers, text, logo, watermark, vignette, border, or copyrighted symbols. No photorealism, horror, gritty detail, hard black shadows, glossy plastic, thick white sticker rim, watercolor wash as primary shading, or painterly broken edges.
```

## 2. Ghost hand

- Built-in generation id: `exec-6675f577-dabd-441e-af8f-563d17aa3508`
- Native chroma master:
  `ghost_hand_chroma_native.png`, 1254x1254 RGB,
  SHA-256 `8390d740ef2747ba8ad944c66dc92da42e9eb0e803749086b66f98afabc879b0`
- Native alpha master:
  `ghost_hand_alpha_native.png`, 1254x1254 RGBA,
  SHA-256 `345972c6311edf6885ce81b2951f4d1b2322582573bf353ad3bd2c92c12da617`
- Runtime derivative: `assets/castle/training/ghost_hand.png`, 512x512
  RGBA, SHA-256
  `e484d14899d8137448128314536132dbd16f970cb1f0fabea006e9d51b5435b9`
- Processing: background removed with the installed Codex chroma helper using
  border auto-key, soft matte, thresholds 12/220, and despill; then one
  whole-canvas high-quality bicubic resize. Runtime corner alpha is zero.

```text
Use case: stylized-concept
Asset type: transparent game tutorial pointer sprite, displayed at about 64 pixels
Primary request: a single cute chubby cartoon child's hand performing a friendly one-finger tap gesture.
Scene/backdrop: perfectly flat uniform solid #00ff00 chroma-key background across the entire square canvas for local background removal. No floor plane.
Subject: one pearl-cream, skin-tone-neutral little hand with the wrist entering from the upper center, palm facing the viewer, index finger extended straight downward toward a tap target, thumb and the other three fingers softly curled into one simple rounded mitten-like mass. Anatomically clear: exactly one hand, five fingers total, no fingernails. A very small warm pearl highlight and a restrained pale-gold glow close around the silhouette.
Style/medium: polished flat-color children's storybook cel game sprite; oversized four-year-old-readable silhouette; two broad value bands; thick clean dark navy-purple outline; crisp edges; friendly toy-playset feeling.
Composition/framing: centered, upright, fully contained with generous equal padding; fingertip points down; no cropping; square 1:1 composition intended for 512x512.
Constraints: the background must be exactly one uniform #00ff00 color with no shadows, gradients, texture, reflections, lighting variation, vignette, floor, or objects. Do not use #00ff00 anywhere in the hand or glow. No cast shadow, contact shadow, reflection, extra hands, extra fingers, missing fingers, face, character, sleeve, jewelry, text, logo, watermark, sticker border, photoreal skin, skin tone, pores, or realistic fingernails.
```

## 3. TAP chip

- Built-in generation id: `exec-78053977-8ae0-4286-a180-34969f1080b7`
- Native chroma master:
  `verb_chip_tap_chroma_native.png`, 1254x1254 RGB,
  SHA-256 `c22bbdc4002efcb7295604cbccc711341b8218d02b526994a8f59c60fb58e45c`
- Native alpha master:
  `verb_chip_tap_alpha_native.png`, 1254x1254 RGBA,
  SHA-256 `20e156fed86bfe7d04a8d9729f83e497cc357a95f9f2cae0eb865fed1c30b1c2`
- Runtime derivative: `assets/castle/training/verb_chip_tap.png`, 256x256
  RGBA, SHA-256
  `375a002f998abd97c3fe1333ea30199d223e91e3269a9dfc01b269b71e74092e`
- Processing: same chroma-helper settings and whole-canvas resize as the hand.
  Runtime corner alpha is zero.

```text
Use case: stylized-concept
Asset type: transparent decorative game UI chip, displayed at 48-72 pixels
Primary request: one hot-pink round bubble button carrying the TAP action identity.
Scene/backdrop: perfectly flat uniform solid #00ff00 chroma-key background across the entire square canvas for local background removal. No floor plane.
Subject: a single plump circular hot-pink bubble chip with a centered simple five-point star softly impressed into its face, like a shallow pearl-cream and blush-pink embossed mark. The star is part of the chip, not a separate floating object. One restrained upper-left pearl highlight, two broad cel value bands, and a clean dark navy-purple outer outline.
Style/medium: polished flat-color children's storybook game UI icon; rounded toy-playset form; crisp silhouette; child-readable at 48 pixels; matte-to-satin bubble finish, not realistic glass or shiny plastic.
Composition/framing: exactly one centered front-facing circular chip; generous equal padding; fully contained; square 1:1 composition intended for 256x256.
Color palette: hot pink and coral-pink body, pearl-cream star impression, lavender shadow, dark navy-purple outline. Do not use green in the subject.
Constraints: background must be exactly one uniform #00ff00 color with no shadow, gradient, texture, reflection, floor, lighting variation, vignette, or objects. No cast shadow, contact shadow, extra stars, ring, arrows, hands, characters, words, letters, numbers, text, logo, watermark, frame, thick white sticker border, photorealism, glass transparency, glitter noise, or tiny detail.
```

## 4. HOLD/CHARGE chip

- Built-in generation id: `exec-67f579f1-ac37-4dac-94d0-7d54ab68bf3e`
- Native chroma master:
  `verb_chip_hold_chroma_native.png`, 1254x1254 RGB,
  SHA-256 `082517bbfc9804e7a8359890a32f0c33fa0ec296d75ec603b2404cb7f476d07d`
- Native alpha master:
  `verb_chip_hold_alpha_native.png`, 1254x1254 RGBA,
  SHA-256 `35ab65b5c80b7bf4e55870cd57d3d4e95d312cf1afc3e1d9972209956c830494`
- Runtime derivative: `assets/castle/training/verb_chip_hold.png`, 256x256
  RGBA, SHA-256
  `75f649ef6352670a5881e1792d7082ffc696ee30a5e89cf07b54eb289da07ed1`
- Processing: same chroma-helper settings and whole-canvas resize as the hand.
  Runtime corner alpha is zero.

```text
Use case: stylized-concept
Asset type: transparent decorative game UI chip, displayed at 48-72 pixels
Primary request: one lavender calm bubble button carrying the three-stage HOLD/CHARGE action identity.
Scene/backdrop: perfectly flat uniform solid #00ff00 chroma-key background across the entire square canvas for local background removal. No floor plane.
Subject: a single plump circular lavender bubble chip with a bold smooth progress arc wrapping around roughly three quarters of its outer face. The arc begins warm gold, transitions through peach, and ends hot pink, clearly communicating a held press charging through stages. Leave one clean visible gap in the arc. The chip's center remains simple and blank. One restrained upper-left pearl highlight, two broad cel value bands, and a clean dark navy-purple outer outline.
Style/medium: polished flat-color children's storybook game UI icon; rounded toy-playset form; crisp silhouette; child-readable at 48 pixels; matte-to-satin bubble finish, not realistic glass or shiny plastic.
Composition/framing: exactly one centered front-facing circular chip; generous equal padding; fully contained; square 1:1 composition intended for 256x256.
Color palette: lavender and periwinkle body, gold-to-peach-to-hot-pink ring arc, pearl highlight, cool lavender shadow, dark navy-purple outline. Do not use green in the subject.
Constraints: background must be exactly one uniform #00ff00 color with no shadow, gradient, texture, reflection, floor, lighting variation, vignette, or objects. No cast shadow, contact shadow, star, arrows, hands, characters, words, letters, numbers, text, logo, watermark, frame, thick white sticker border, photorealism, glass transparency, glitter noise, or tiny detail.
```

