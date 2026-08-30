# Day One Stuffie Room — Baby Eagle rescue pose provenance

Date: 2026-08-22
Generator: Codex built-in ImageGen (`image_gen` tool)
Reference authority: `assets/book/baby_eagle.png` (identity, facial design,
feather pattern, palette, outline, proportions, and painted style only)
Protected-source status: unchanged

## Accepted native generation

- Path: `baby_eagle_pinned_native.png`
- SHA-256: `5C87CB4ABC676DCFDB04AE9B317B97A4A88A1384CB509F156CDD6E9A42B3C721`
- Native geometry: 1536x1024 RGBA
- Review: accepted as one complete, connected Baby Eagle with the backpack
  absent, both wings available for separate runtime bunny overlap, alert/hopeful
  expression, preserved mint/yellow/pink identity palette, and real transparent
  pixels outside the subject.

Accepted prompt:

> Use case: background-extraction
> Asset type: production transparent Sprite2D character cutout for a preschool storybook game
> Input images: Image 1 is the exact generated pinned Baby Eagle character to preserve; Image 2 is the identity and color authority.
> Primary request: remove only the white-and-light-gray checkerboard background from Image 1 and return the same complete pinned Baby Eagle on a genuinely transparent alpha background.
> Constraints: preserve the character from Image 1 exactly—same pose, anatomy, silhouette, facial expression, proportions, feather colors, outlines, scale, and placement. Do not redraw, crop, add, remove, or change any part of Baby Eagle. No checkerboard pixels, white matte, gray matte, halo, floor, shadow, props, dust bunnies, text, border, or watermark. Exactly one character. Outside the character must be real transparency, not a depicted transparency grid.

The accepted extraction used a first-pass generated pose as its edit target. The
first-pass prompt requested the canonical Baby Eagle without her backpack, low
on her tummy, with both wings slightly outstretched for separate runtime dust
bunny overlap; exactly one complete, unhurt character; no props, bunnies,
scenery, shadow, text, or cropped anatomy.

## Rejected first-pass delivery

- Generator-side path: `exec-2905c960-a005-4e57-a251-2d7b527ca24f.png`
- SHA-256: `A0A3CD2454A8D960C3860660C510CE71AC06179B6CE32C60285AF894DB9F8490`
- Rejection: RGB file with a painted checkerboard and no alpha channel. It was
  used only as the accepted extraction's pose input and is not a runtime asset.

## Runtime derivative

- Path: `../../../assets/castle/day_one_stuffie/baby_eagle_pinned.png`
- SHA-256: `DAB2D2CD9C89D1B74DEF2CB9EF6E4ADB0930DEB7099DDE1F457309665690A0AC`
- Geometry: 1024x768 RGBA
- Transform: the complete flattened accepted native image was proportionally
  reduced to fit inside 960x672 with Lanczos resampling, centered on a new
  transparent 1024x768 canvas, and PNG-optimized. No subject-local mask,
  repaint, warp, crop, or compositing was performed.
