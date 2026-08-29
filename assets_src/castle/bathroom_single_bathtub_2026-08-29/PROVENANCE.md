# Bubble Bath single-bathtub background heal

Generated and integrated 2026-08-29 to remove both lower-corner shell towel
baskets whose phone-scale silhouettes read as extra bathtubs. No protected
original was modified. The approved room, fixtures, lighting, and palette
remain the composition authority.

## Generated left-floor source

- Path: `generated_floor_heal_source.png`
- Source: OpenAI built-in ImageGen precise-object edit of
  `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r1_c0.png`
- SHA-256: `c8a8dbeae73ba06235b392522ee016aac7712654afb271b3e76a45fac123b85e`
- Native dimensions: 1254x1254 RGB
- License: project original, all rights reserved
- URL: none; generated in-project

Prompt:

> Remove only the large blurred shell towel-basket footprint occupying the
> lower-left and lower-center foreground. Heal it into continuous empty
> coral-pink and lavender shell-tile floor matching the existing perspective,
> grout lines, painted value bands, and warm lighting. Preserve all unaffected
> art and tile-edge continuity. Add no basket, towels, shell furniture,
> bathtub-like silhouette, object, character, text, or watermark.

## Accepted native-tile repair

- Path: `room_bubble_bath_background_r1_c0_healed.png`
- SHA-256: `2befaa3f39ad3af15c42d6eae0fa6f9eceadf87be6e6f0684df44f4dbf4c2a6d`
- Dimensions: 910x1024 RGB
- Input tile SHA-256:
  `86d4ce581893d25058f24db56d468848084bb3aea69724fe59418719ca0bf0c8`
- Derivation: the complete generated source was Lanczos-normalized to the
  native tile canvas, then composited only over the retired towel-basket
  footprint with a feathered top/right mask. The top and right neighbor seams
  remain source-owned; the changed left and bottom borders are exterior master
  boundaries, not tile joins.
- Runtime integration:
  `tools/repair_castle_room_native_backgrounds.py` installs the reviewed tile
  into the canonical 3640x2048 Bubble Bath master before the deterministic room
  and V4 delivery builders slice and hash runtime tiles.

## Generated right-floor source

- Path: `generated_floor_heal_right_source.png`
- Source: OpenAI built-in ImageGen precise-object edit of
  `assets/flats/castle/interactions_v4/background_tiles/room_bubble_bath_background_r1_c3.png`
- SHA-256: `37574d30ced66f28636a1518810e61688ba018074195631c2738971f95d8a7a5`
- Native dimensions: 1254x1254 RGB
- License: project original, all rights reserved
- URL: none; generated in-project

Prompt:

> Remove the entire large bathtub-like shell towel basket in the lower center
> and lower right, including its open shell lid, container, towels/blurred
> fill, attached coral, purple floor pad, and smeared footprint. Heal the
> region into continuous empty coral-pink and lavender shell-tile floor that
> matches the existing perspective, grout, texture, lighting, and gradients.
> Preserve the small wall-side shell basket, purple plant pot, wall, baseboard,
> unaffected floor, and complete top/left tile-edge continuity. Add no object,
> shell furniture, basket, towels, bathtub-like silhouette, character, text,
> or watermark.

## Accepted right native-tile repair

- Path: `room_bubble_bath_background_r1_c3_healed.png`
- SHA-256: `0da1a692deb8fc32b1efefbd55faf9aed3db635e01cc06073f848301184ef7e3`
- Dimensions: 910x1024 RGB
- Input tile SHA-256:
  `099ee04e50b82e5404fb267f4a8624760c2ba4af633350ef829370ff8997ae9e`
- Derivation: the complete generated source was Lanczos-normalized to the
  native tile canvas, then composited only over the retired right shell-basket
  footprint with feathered top/left boundaries. The complete top join and the
  source-owned left join remain unchanged; the right and bottom borders are
  exterior master boundaries.
- Runtime integration: the same deterministic repair tool installs this tile
  at native master position `(2730, 1024)` before runtime slicing and hashing.

Human visual approval remains controlled by
`assets_src/castle/interactions_v4/castle_interaction_frame_approval_ledger.json`.
