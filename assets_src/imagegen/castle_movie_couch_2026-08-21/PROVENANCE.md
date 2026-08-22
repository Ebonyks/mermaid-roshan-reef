# Rear-facing cloud settee provenance — 2026-08-21

Purpose: fill the verified movie-lounge asset gap. The approved runtime set
contained only a front-facing couch, which visually faced away from the TV.

- Method: OpenAI built-in ImageGen, precise-object-edit.
- Design reference: `assets/flats/castle/dream_house/cloud_settee.png`.
- Result id: `exec-fc1a303b-50c7-49e1-b425-c4f167c00475.png`.
- Native source: `native/cloud_settee_back_native.png`, SHA-256
  `BB3FC580AF3C01D6351E314C1A0D567A180172F16334301023B6B0E732C206ED`.
- Runtime derivative: `assets/flats/castle/dream_house/cloud_settee_back.png`,
  SHA-256 `6A5BB0798122941EF73EAC3FDE9019161F20438B450ECE61A09468B62B66FF69`.
- Derivation: whole-image Lanczos normalization to 1024 px longest side,
  followed by border-connected neutral-background extraction with
  `tools/extract_connected_chroma.py --key F8F8F8 --threshold 24`.
- Alpha review: 1024x799 RGBA; alpha extrema 0..255; nontransparent bounding
  box `(43, 65, 980, 693)`, so the complete couch has clear padding on all
  four sides.

Final generation prompt:

> Create the exact same cloud settee viewed from directly behind, so the couch
> visibly faces away from the player and toward a television on the back wall.
> Preserve the couch identity, proportions, cream cloud upholstery, teal
> seating family, lavender base, gold trim, pearl feet, shell ornament
> language, polished pastel storybook rendering, and plum/navy outlines.
> Center the isolated complete couch with every foot visible and no cropping.
> Do not add a TV, room, character, text, watermark, shadow, or extra object.

