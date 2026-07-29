# Mermaid Roshan 2.5D generation provenance

The quadrupled animation expansion is documented separately in
`PROMPTS_4X.md`.

- Date: 2026-07-26
- Tool path: OpenAI built-in image generation (`image_gen`)
- Use case: `stylized-concept`
- References: five user-provided Mermaid Roshan multi-view PNGs named
  `Gemini_Generated_Image_*.png`. The reference files remain outside the
  repository and were used only for identity, costume, proportions, palette,
  line-art, and viewpoint continuity.
- Background removal: the generated flat green chroma background was removed
  with the Codex image-generation skill's `remove_chroma_key.py` helper using
  border auto-sampling, soft matte, thresholds 12/220, and despill.
- Runtime normalization: Lanczos resampling to 1024x512 or 1024x1024.
  `roshan_base.png` is a lossless 256x256 crop of directional frame 0.

## Directional atlas

Generation output: `call_SCMC9O1ZtRUrcZJA0vuFZyNf.png`

```text
Use case: stylized-concept
Asset type: 2.5D game character directional sprite atlas
Input images: Images 1-5 are identity, costume, proportions, palette, line-art, and multi-view references for the same Mermaid Roshan character.
Primary request: Create one production-ready 4-by-2 sprite atlas of Mermaid Roshan in eight evenly spaced cells. All eight cells show the exact same character, costume, proportions, face, tiara, brown hair with the same rainbow ponytail, pink ruffled top, pearlescent lavender/aqua scaled tail, and rainbow fins. Poses in reading order: front neutral hover; front three-quarter facing left; left profile; back three-quarter facing left; full back; back three-quarter facing right; right profile; front three-quarter facing right.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background filling the entire canvas for local background removal.
Style/medium: polished children's storybook game sprite, clean dark plum outline, soft cel shading, match the supplied references exactly.
Composition/framing: exact 4 columns by 2 rows; one full-body character centered in each equal cell; identical apparent height, scale, baseline, and padding in every cell; no overlaps; generous space around every silhouette.
Constraints: background must be one uniform #00ff00 with no shadows, gradients, texture, checkerboard, reflections, floor plane, or lighting variation. Crisp opaque silhouettes and clean edges. No cast shadows. No grid lines, labels, text, icons, sparkles, watermarks, or extra objects. Do not use exact #00ff00 anywhere in the character. Preserve child-friendly anatomy and the reference design; do not redesign or age up the character.
Avoid: missing arms or fins, fused hands, duplicate limbs, cropped tail, pose drift, costume drift, inconsistent face or hair.
```

## Swim atlas

Generation output: `call_1SRVfyKkVuX8bDhDDeHBDZ7E.png`

```text
Use case: stylized-concept
Asset type: 2.5D game character swimming animation sprite atlas
Input images: Image 1 is the approved Mermaid Roshan directional atlas and is the primary identity/style anchor. Images 2-4 are the original front, back, and profile references.
Primary request: Create one production-ready 4-by-2 sprite atlas for a seamless Mermaid Roshan swim loop. The exact same character appears in all eight cells. Top row is front three-quarter view, four keyframes in reading order: (1) relaxed glide with arms low; (2) both arms reaching forward/up together while the tail curls right; (3) arms sweeping outward at shoulder height while the tail passes center; (4) arms sweeping down/back while the tail curls left. Bottom row repeats those four exact swim phases from a back three-quarter view. Preserve her exact face, age, proportions, tiara, brown hair with rainbow ponytail, pink ruffled top, pearlescent lavender/aqua scaled tail, and rainbow fins from Image 1.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background filling the entire canvas for local background removal.
Style/medium: polished children's storybook game sprite, clean dark plum outline, soft cel shading, match Image 1 exactly.
Composition/framing: exact 4 columns by 2 rows; one full-body character centered in each equal cell; identical apparent height, scale, tail-root position, baseline, and padding in every cell; clear readable limb silhouettes; no overlaps.
Constraints: background is one uniform #00ff00 with no shadows, gradients, texture, checkerboard, reflections, floor, or lighting variation. Crisp opaque silhouettes. No cast shadows. No grid lines, labels, text, icons, sparkles, watermarks, bubbles, or props. Do not use exact #00ff00 in the character. No costume, facial, anatomy, or scale drift. Both arms and both hands must remain distinct and child-friendly.
Avoid: extra or missing limbs, fused hands, cropped fins, hairstyle changes, alternate costumes, dramatic perspective, motion blur.
```

## Gesture atlas

Generation output: `call_6wOowY3Ap1zMTcufYI890BO8.png`

```text
Use case: stylized-concept
Asset type: 2.5D game character gesture animation key-pose atlas
Input images: Image 1 is the approved Mermaid Roshan directional identity atlas and is the primary identity/style anchor. Image 2 is the approved swim atlas and establishes character scale. Image 3 is the original clasped-hands reference.
Primary request: Create one production-ready 4-by-4 sprite atlas. The exact same Mermaid Roshan character appears once in each of sixteen equal cells, front three-quarter view, with consistent design and scale. Poses in strict reading order, left-to-right then top-to-bottom: (1) wave one hand overhead; (2) cheer with both arms raised; (3) clap hands together at chest; (4) graceful twirl pose with arms spread; (5) curious look to one side; (6) giggle with both hands near mouth; (7) sleepy curled hover with eyes closed and hands tucked; (8) point/reach one arm clearly forward; (9) collect/scoop with both hands reaching forward; (10) surprised soft boing with hands lifted; (11) twirl a lock of rainbow hair with one hand; (12) hum happily with clasped hands and eyes softly closed; (13) playful sideways flop with arms lifted; (14) carry pose with both hands cupped overhead/forward under an imaginary toy; (15) seated pose with tail curled beneath and hands gripping an imaginary bar; (16) gentle neutral hover reset. No props or imaginary objects are drawn.
Subject invariants: preserve the exact child character, face, age, body proportions, tiara, brown hair with rainbow ponytail, pink ruffled top, pearlescent lavender/aqua scaled tail, and rainbow fins from Images 1-2.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background filling the entire canvas for local background removal.
Style/medium: polished children's storybook game sprite, clean dark plum outline, soft cel shading, matching Images 1-2 exactly.
Composition/framing: exact 4 columns by 4 rows; one full-body character centered in each cell; identical apparent height, scale, tail-root position, and padding except the intentional sideways flop; no overlaps; clear readable hands and arm silhouettes.
Constraints: background is one uniform #00ff00 with no shadows, gradients, texture, checkerboard, reflections, floor, or lighting variation. Crisp opaque silhouettes. No cast shadows. No grid lines, labels, numbers, text, icons, sparkles, watermarks, bubbles, or props. Do not use exact #00ff00 in the character. No costume, identity, facial, anatomy, or scale drift. Both arms and both hands distinct.
Avoid: extra/missing/fused limbs, cropped fins, hairstyle changes, alternate clothes, dramatic camera changes, motion blur.
```

## Playground atlas

Generation output: `call_TP6JGFfi1TSjrQaIDTzFu0uw.png`

```text
Use case: stylized-concept
Asset type: 2.5D game character playground interaction key-pose atlas
Input images: Image 1 is the approved Mermaid Roshan directional identity atlas and is the primary identity/style anchor. Image 2 is the approved gesture atlas and establishes action-pose style and scale. Image 3 is the original profile reference.
Primary request: Create one production-ready 4-by-2 sprite atlas. The exact same Mermaid Roshan character appears once in each of eight equal cells, mostly side/front-three-quarter so her hands read clearly. Poses in strict reading order: (1) swing pose, seated/hovering with tail curled beneath and both hands gripping two imaginary swing ropes above; (2) climb pose, body reaching upward with both hands and tail coiled to spring; (3) ride pose, delighted with both arms raised overhead and tail streaming; (4) landing pose, arms floating back down and tail softly curled; (5) digging pose A, leaning forward with left hand scooping down; (6) digging pose B, leaning forward with right hand scooping down; (7) seated ride pose with tail curled beneath and both hands gripping an imaginary horizontal bar; (8) dry-land hop pose with arms lifted for balance and tail coiled like a spring. No ropes, bars, toys, sand, props, or imaginary objects are drawn.
Subject invariants: preserve exact child face, age, proportions, tiara, brown hair with rainbow ponytail, pink ruffled top, pearlescent lavender/aqua scaled tail, and rainbow fins from Image 1.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background filling the entire canvas for local background removal.
Style/medium: polished children's storybook game sprite, clean dark plum outline, soft cel shading, match the approved atlases exactly.
Composition/framing: exact 4 columns by 2 rows; one full-body character centered in each equal cell; identical apparent height and scale; generous padding; no overlaps; hands and arms distinct and readable.
Constraints: background is one uniform #00ff00 with no shadows, gradients, texture, checkerboard, reflections, floor, or lighting variation. Crisp opaque silhouettes. No cast shadows. No grid lines, labels, text, icons, sparkles, watermarks, bubbles, or props. Do not use exact #00ff00 in the character. No costume, identity, facial, anatomy, or scale drift.
Avoid: extra/missing/fused limbs, cropped fins, hairstyle changes, alternate clothes, dramatic perspective, motion blur.
```
