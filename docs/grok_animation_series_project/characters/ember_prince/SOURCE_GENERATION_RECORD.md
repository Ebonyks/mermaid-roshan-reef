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
