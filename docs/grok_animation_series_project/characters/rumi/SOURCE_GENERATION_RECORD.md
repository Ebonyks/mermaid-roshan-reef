# Violet Tide generation record

Generation method: OpenAI built-in image generation, 2026-07-26.

Reference inputs: three local still images supplied by the owner. They were used
only as visual references and are not committed to the repository.

## Full-body identity anchor

```text
Use case: stylized-concept
Asset type: full-body 2D game character sprite and visual identity anchor for a touch-first Godot game for a 4-year-old
Input images: Images 1-3 are reference images for the recognizable hairstyle, facial attitude, purple palette, and confident performer energy only; do not copy any logos, text, branded costume graphics, or exact outfit.
Primary request: transform the referenced character inspiration into a child-friendly mermaid core character, as an intentionally transitional early prototype that can evolve toward an original identity.
Subject: one young-adult mermaid heroine with a friendly, reassuring smile; expressive almond eyes; bold brows; pointed ears; a large sculptural violet-purple braided high ponytail with a soft lavender gradient; small star-shell earrings. Replace the human lower body completely with one long, elegant mermaid tail. Tail is turquoise and deep aqua at the waist, transitioning through lavender to a broad coral-pink split fin, with large readable scales and two small side fins. Original costume: cropped lavender-and-navy sea-jacket with rounded shoulders and entirely original coral-comet, three-shell, and wave patches; modest high-neck pearly white shell top; small gold three-shell clasp; no bare midriff emphasis. Hands relaxed and fully visible.
Style/medium: polished 2D storybook game sprite, cel-shaded, Wind-Waker-inspired pastel toy-diorama sensibility, clean dark navy-purple outline, soft aqua/lavender shadows, pre-drawn highlight accents, friendly rounded forms, not photorealistic, not 3D render, no anime screenshot imitation.
Composition/framing: single character only, full body from top of hair through entire tail fin, centered, three-quarter front hero pose, all anatomy visible, generous padding on every side, strong uncluttered silhouette readable as a 160px-tall mobile sprite.
Lighting/mood: bright soft undersea studio light, warm and safe, confident older-sister energy suitable for a preschool audience.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for local background removal. One uniform color only; no ground plane, shadows, gradients, bubbles, props, texture, reflection, or lighting variation in background.
Constraints: preserve the key identity cues from the reference images (violet sculptural braided ponytail, strong brows, almond eyes, confident expression) while making the mermaid costume and symbols wholly original; opaque subject with crisp edges; do not use #00ff00 anywhere on the subject; no cast shadow; no contact shadow; no text; no letters; no logo; no watermark; no copyrighted symbols; no backpack; no wings; no legs; exactly two arms, two hands, one continuous tail, and one split tail fin.
Avoid: sexualized pose or clothing, exposed cleavage, crop-top emphasis, hyper-realism, extra limbs, duplicate character, muddy detail, tiny motifs, signature, checkerboard background.
```

Built-in output:
`call_k44jhs3Yus1tvrFrMMNoBdZ7.png`

## Eight-frame starter animation sheet

```text
Use case: identity-preserve
Asset type: 2D game sprite animation sheet for a touch-first Godot game for a 4-year-old
Input images: Image 1 is the exact approved character anchor. Preserve this character's identity, face, proportions, hairstyle, jacket, shell top, palette, tail design, patches, and rendering style in every frame.
Primary request: create exactly eight separate full-body animation frames of the same mermaid in a precise 4-column by 2-row sprite-sheet grid.
Grid and actions, reading left to right:
Top row frames 1-2: IDLE loop - frame 1 relaxed neutral hover; frame 2 gentle rise with tail tip curling slightly and braid floating upward.
Top row frames 3-4: WAVE loop - frame 3 right hand lifted beside face; frame 4 broad friendly open-palm wave and bigger smile.
Bottom row frames 5-8: SWIM loop moving toward screen-right in three-quarter side view - frame 5 tail bends down, frame 6 tail centered, frame 7 tail bends up, frame 8 tail centered with braid and sleeve lag; arms comfortably forward/alongside, clear slow dolphin-kick rhythm.
Subject: exact same violet braided-ponytail mermaid from Image 1, same original lavender/navy jacket, pearly high-neck top, turquoise-to-lavender tail, coral split fin, same friendly confident expression.
Style/medium: same polished 2D storybook cel-shaded game-sprite style as Image 1, clean dark navy-purple outline, soft aqua/lavender shadows, opaque painted character; not 3D; no motion blur.
Composition/framing: exact 4x2 grid; eight characters total, one per cell; every cell equal size; same character scale and head size in every frame; full body including all hair and tail fin visible in every cell; centered inside each cell; generous equal padding; poses never cross cell boundaries; no overlapping characters; no cropped anatomy; no perspective camera change.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background across the entire canvas. One uniform color only; no cell borders, no grid lines, no shadows, no gradients, no floor planes, no bubbles, no props, no texture, no reflection, no lighting variation.
Constraints: maintain character consistency across all eight frames; broad preschool-readable movements; do not use #00ff00 anywhere in the character; no cast shadow; no text; no labels; no numbers; no letters; no logo; no watermark; no copyrighted symbols; no wings; no legs; exactly two arms, two hands, one continuous mermaid tail and one split tail fin per frame.
Avoid: more or fewer than eight frames, inconsistent costumes, changing hairstyle, extra limbs, duplicated body parts, missing hands, separate props, tiny characters, sheet title, annotations, checkerboard background, sexualized pose.
```

Built-in output:
`call_lrZ3ms8FHYXIkTuN80Co6hQy.png`

## Post-processing

- Removed the flat chroma background locally.
- Protected enclosed turquoise scale highlights from global chroma removal by
  selecting only large connected key-color regions.
- Applied a soft 0.65 px matte and edge despill.
- Resampled the full-body sprite to 576 x 1024.
- Packed the eight animation cells into a 1024 x 768 atlas.
