# Day One standing Baby Eagle provenance

Date: 2026-08-28
Tool: OpenAI built-in ImageGen
License: Project-generated © Mermaid Roshan LLC, all rights reserved
External source URL: none

## Identity reference

- `assets/castle/day_one_stuffie/baby_eagle_pinned.png`
- SHA-256: `DAB2D2CD9C89D1B74DEF2CB9EF6E4ADB0930DEB7099DDE1F457309665690A0AC`
- Role: sole identity, palette, anatomy, rendering, linework, feather-pattern,
  face, eye, beak, crest, wing, leg, and style authority.
- The protected reference was not modified.

## Generation

Initial built-in result:
`exec-3238f2cf-e9ef-4ce3-86f6-1622d276e6ea.png`.
It established the accepted standing pose but painted a checkerboard backdrop,
so it was rejected as delivery art and is not stored in the repository.

Initial prompt:

> Create a new full-body standing idle pose of Baby Eagle, based exactly on
> the supplied pinned Baby Eagle reference. Baby Eagle has just been freed and
> is calmly standing upright, happy and safe, with both wings relaxed slightly
> away from the body for a gentle idle animation. Preserve the exact identity,
> rainbow palette, anatomy, face, linework, and polished 2D storybook style.
> Return a complete backpack-free character on genuine transparency with no
> dust bunnies, props, shadow, text, watermark, or cropping.

Accepted alpha-correction result:
`exec-cbd3d9cf-0289-4111-8c9c-95fb87b0d231.png`.

Correction prompt:

> Remove only the light gray checkerboard background and return the standing
> Baby Eagle as a genuinely transparent RGBA PNG cutout. Preserve the Baby
> Eagle character pixels, pose, anatomy, expression, palette, linework,
> proportions, and framing exactly. Keep the complete backpack-free character
> fully inside the canvas with clean antialiased alpha; add nothing.

## Accepted files

- `baby_eagle_standing_idle_native.png`: 1087×1447 RGBA accepted native;
  SHA-256 `C235C882B0639BF25EF22A3BEBDA8BE669F1A16D21CEDEB446B8774241DFD2C2`.
- `assets/castle/day_one_stuffie/baby_eagle_standing_idle.png`: 770×1024
  RGBA runtime derivative; SHA-256
  `90C54412AA59317B45D3D670ADA181EE7EDE20BA5FE91F051E61D81F70F0EF76`.

Runtime normalization was a proportional whole-canvas Lanczos downscale with
FFmpeg 8.1.2 (`scale=-2:1024:flags=lanczos`). No subject-local transform,
repaint, crop, relight, or recomposition was applied.

## Review

- Backpack absent: pass
- Full body, both wings, and both feet present: pass
- Identity, palette, and storybook family continuity: pass
- Genuine RGBA alpha: verified with FFprobe
- Runtime longest edge ≤1024 pixels: pass
- Owner/human review: pending
