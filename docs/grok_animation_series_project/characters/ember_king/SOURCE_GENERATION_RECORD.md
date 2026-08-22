# Ember King animation generation record

Generation method: OpenAI built-in image generation, 2026-08-22.

Reference inputs were the project-owned `EMBER_KING_IDENTITY.png` and
`EMBER_KING_MOTION_AUTHORITY.png`. The 1536×1024 generated master remains in
the local Codex provenance cache and is identified by SHA-256
`12b2a56cfd0516956eed43cb9daded8b22329882d084e0eedd7ee41411a25de5`.
It is not committed because the repository texture rule caps non-POT long
edges at 1024. A separate cape-payoff replacement master has SHA-256
`01db65c4c117b67bbe8dd4888fbfaa57146f3d1d6395e62fb95611fe67e2c00f`.

## Eight-pose source prompt

```text
Use case: identity-preserve
Asset type: production 2D character animation sprite sheet for the Mermaid Roshan Grok animation series and Godot-compatible frame extraction
Input images: Image 1 is the exact approved Ember King V6 identity authority. Image 2 is motion vocabulary only. Preserve Image 1's face, stocky-athletic proportions, red/coral scales, cream muzzle and belly, black asymmetrical emo fringe, obsidian horn crown and shell, charcoal vest and cuffs, chain belt, enormous aubergine split cape, palette, linework, and child-friendly antagonist personality in every frame.
Primary request: create exactly eight separate full-body animation frames of the same Ember King in an exact 4-column by 2-row sprite-sheet grid.
Grid: frames 1–2 are a bored slouch and compressed breath/eye-roll idle; frames 3–6 are left contact, compression, awkward passing overstep and right-contact recovery for a looping heavy walk; frames 7–8 are cape-fan anticipation and theatrical sideways payoff.
Style: polished 1990s Japanese shōjo television-animation painted-cel treatment interpreted through the exact Mermaid Roshan storybook identity; organic plum/navy contours, two or three value bands, high-key coral and aubergine, lavender shadows, restrained pearl highlights.
Composition: exact 4x2 grid; one equal-scale full-body character in each cell; consistent three-quarter screen-right orientation and baseline; full horns, cape, shell, hands, feet and tail; no crossing, cropping, overlap, borders or labels.
Backdrop: genuinely transparent with preserved alpha; no ground plane, scenery, gradients, texture, checkerboard, or lighting variation.
Constraints: exactly eight frames; no candle, cake, prop, weapon, text, logo, watermark, extra character, green body, roar, shell spin, predatory charge, injury, violent impact, extra limbs, missing hands, costume/crown/shell/cape drift, photorealism, 3D or horror lighting.
```

## Cape-payoff replacement prompt

```text
Use case: identity-preserve
Asset type: replacement animation key frame for the exact Ember King
Input images: Image 1 is the exact identity authority. Image 2 is the current runtime atlas; its bottom-right pose controls only the intended cape-fan action.
Primary request: one and only one full-body cape-fan payoff. The King plants in three-quarter screen-right view and completes one broad theatrical sideways sweep of the enormous aubergine split cape. Both hands and feet remain visible; the shell edge remains readable; a few tiny rounded warm ember accents may trail the cape. This is a warm gust and comic display, not an attack.
Composition: one centered character, entire cape arc and all anatomy visible, at least 12 percent empty padding on every side, genuinely transparent background.
Constraints: no candle, cake, prop, weapon, second pose, extra character/limb, missing hand, hidden shell, clipping, shell spin, violent attack, blur, drift, photorealism, 3D or horror lighting.
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

- Frames 01–08: SHA-256 `6a009946b4c32893655e1fd281b95224fccd3894f37eead7a81e0a5238d05b34`.
- Frames 09–16: SHA-256 `639afa1e0ff1ef2a1cdb3c9e9c59dde01a4f0ba71b23790597c2d0c74a7bd3f2`.

Rule-compliant 1024×682 project copies are committed under `source_masters/`;
their hashes are `bc62692c4ad8b903495bd1ff204126b952e87437131452c11f9c54e4591b84bc`
and `40f075eb4acf3f6f1fccbaf0dca3eefd96d43304746520c9c6e83ffeb42bee6b`.

### Frames 01–08 final prompt

```text
Use case: stylized-concept. Asset type: production 2D heavy walk-cycle sprite sheet, Ember King frames 01-08 of 16. Generate the first eight consecutive frames of one seamless 16-frame screen-right heavy blundering walk for the exact referenced King, not a pose collection. Preserve exact face, lighter stocky-athletic coral-red body, cream muzzle/belly, black emo fringe, obsidian horn crown, natural volcanic shell, charcoal vest/cuffs, chain belt, ember clasp and enormous aubergine split cape; no tie or candle. Exact 4x2 grid, equal cells, common scale/baseline and transparent background. Consecutive phases: right broad contact/left toe push; right foot slap; weight drop; deepest squash/left peel; left swing begins; left knee passes/right heel lifts; left knee leads/high point; left lower leg opens. Feet lead, torso/belly compress second, shell follows and cape arrives one to two frames last. Keep the attitude bored, funny and child-friendly. Match Mermaid Roshan storybook cutout art. No text, border, attack, fall, shell spin, extra limbs, drift, photorealism or 3D.
```

### Frames 09–16 final prompt

```text
Use case: stylized-concept. Asset type: production 2D heavy walk-cycle sprite sheet, Ember King frames 09-16 of 16. Continue directly from frames 01-08 and complete the opposite half-step into a seamless loop. Preserve every identity, cape and costume invariant. Exact 4x2 grid, equal cells, same screen-right view, scale/baseline and transparent background. Consecutive phases: left broad contact/right toe push; left foot slap; weight drop; deepest squash/right peel; right swing begins; right knee passes/left heel lifts; right knee leads/high point; right lower leg opens toward frame 01. Continue fluid asymmetric cape folds with one-to-two-frame lag. Match Mermaid Roshan storybook cutout art. No text, border, tie, candle, attack, fall, shell spin, extra limbs, drift, photorealism or 3D.
```
