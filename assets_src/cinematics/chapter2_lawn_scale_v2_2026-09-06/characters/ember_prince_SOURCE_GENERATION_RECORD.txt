# Ember Prince animation generation record

Generation method: OpenAI built-in image generation, 2026-08-22.

Reference inputs were the project-owned `EMBER_PRINCE_IDENTITY.png` and
`EMBER_PRINCE_MOTION_AUTHORITY.png`. The 1536×1024 generated master remains in
the local Codex provenance cache and is identified by SHA-256
`d5d0b51bc19373ec703fcf7ac5a3a717426864a8ed068e6f976d8c9c4148dc96`.
It is not committed because the repository texture rule caps non-POT long
edges at 1024.

## Eight-pose source prompt

```text
Use case: identity-preserve
Asset type: production 2D character animation sprite sheet for the Mermaid Roshan Grok animation series and Godot-compatible frame extraction
Input images: Image 1 is the exact approved Ember Prince V4 identity authority. Image 2 is motion vocabulary only. Preserve Image 1's face, lanky proportions, red/coral scales, cream muzzle, short obsidian horns, asymmetrical black emo hair, charcoal/aubergine mall-punk jacket, ember-heart clasp, slim trousers, boots, tail, and guarded personality in every frame.
Non-negotiable anatomy: the compact vertically elongated obsidian shell grows from exposed coral-red back skin. A continuous visible coral-red skin halo surrounds it. The jacket center-back panel is absent. No fabric exists beneath, behind, across or over the shell. Coat tails begin below the opening and split around the visible red-skinned tail root.
Primary request: create exactly eight separate full-body animation frames of the same Ember Prince in an exact 4-column by 2-row sprite-sheet grid.
Grid: frames 1–2 are a guarded hand-at-clasp idle and backward glance; frames 3–6 are left contact, passing, right contact and opposite passing for a sleek level walk; frames 7–8 are low Cinderstep anticipation and a precise soft diagonal landing.
Style: polished 1990s Japanese shōjo television-animation painted-cel treatment interpreted through the exact Mermaid Roshan storybook identity; organic plum/navy contours, two or three value bands, high-key coral/charcoal/aubergine, lavender shadows and restrained highlights.
Composition: exact 4x2 grid; one equal-scale full-body character in each cell; consistent screen-right orientation and baseline; full horns, hair, hands, shell, coat tails, boots and tail; no crossing, cropping, overlap, borders or labels.
Backdrop: genuinely transparent with preserved alpha; no ground plane, shadow, scenery, gradients, texture, checkerboard or lighting variation.
Constraints: exactly eight frames; no candle, cake, prop, weapon, text, logo, watermark, extra character, shared fascination, shell curl/spin, backpack shell, straps, harness, mounting rim, fabric under shell, teleportation, attack, violent impact, extra limbs, missing hands, identity drift, photorealism, 3D or horror lighting.
```

## Post-processing

`../../tools/build_ember_royals_animation.py` removes only the border-connected
bright neutral checker field, creates an RGBA matte, normalizes cells to
256×384, packs the 1024×768 atlas, exports individual frames, and assembles the
silent GIF/MP4 loops. Exact derivative hashes are in
`../EMBER_ROYALS_ANIMATION_MANIFEST.json`.

## Sixteen-frame walk expansion

Generated with the OpenAI built-in image workflow on 2026-08-22 as two
consecutive eight-frame sheets. Original cache masters:

- Frames 01–08: SHA-256 `8b11cfc073c32bb658673005621a0dd5b937518088cc40db5b3bfb1218edac03`.
- Frames 09–16: SHA-256 `c85836f932cb7f7490b6eed4055acfba7eaffff59424cba6df831dc670717105`.

Rule-compliant 1024×682 project copies are committed under `source_masters/`;
their hashes are `34207100c237479f22e298ed85813c64f9d5a80791f8de85856f513e0d1f8f7f`
and `fa0f67966c452a0f181a7816af5db41b97790dae9098dd14f0dd8993f1e25f2c`.

### Frames 01–08 final prompt

```text
Use case: stylized-concept. Asset type: production 2D game character walk-cycle sprite sheet, Ember Prince frames 01-08 of 16. Generate the first eight consecutive frames of one seamless 16-frame screen-right walk for the exact referenced Prince, not a pose collection. Preserve exact face, lanky coral-red turtle-dragon anatomy, emo hair, horns, cream muzzle, amber eyes, sleeveless charcoal/aubergine open-back jacket, ember-heart clasp, trousers, boots, split coat tails, long tail and compact natural shell. The shell grows from exposed red back skin with a continuous skin halo; jacket center-back is absent; no fabric may sit beneath, behind, across or over it. Exact 4x2 grid, equal cells, screen-right side view, common scale/baseline and transparent background. Consecutive phases: right heel contact/left toe push; right foot lowering; right foot flat and settle; right-knee compression/left toe-off; left swing begins; left knee passes under hips/right heel lifts; left knee leads/high point; left lower leg opens. Use quiet heel-to-toe contacts, real hip translation, small vertical arc, fixed planted foot, opposite arm swing and staggered shell/hair/coat/tail overlap. Match Mermaid Roshan storybook cutout art. No text, border, candle, attack, teleportation, blur, extra limbs, drift, photorealism or 3D.
```

### Frames 09–16 final prompt

```text
Use case: stylized-concept. Asset type: production 2D game character walk-cycle sprite sheet, Ember Prince frames 09-16 of 16. Continue directly from frames 01-08 and complete the opposite half-step into a seamless loop. Preserve every identity and open-back shell-topology invariant. Exact 4x2 grid, equal cells, same screen-right side view, scale/baseline and transparent background. Consecutive phases: left heel contact/right toe push; left foot lowering; left foot flat and settle; left-knee compression/right toe-off; right swing begins; right knee passes under hips/left heel lifts; right knee leads/high point; right lower leg opens toward frame 01. Continue staggered shell, hair, coat-tail and tail-tip overlap without synchronized snapping. Match Mermaid Roshan storybook cutout art. No text, border, candle, attack, teleportation, blur, extra limbs, drift, photorealism or 3D.
```
