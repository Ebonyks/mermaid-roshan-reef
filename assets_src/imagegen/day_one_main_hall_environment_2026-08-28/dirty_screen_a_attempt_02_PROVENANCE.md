# Dirty Main Hall Screen A — Luna correction pass

## Source and generation

- Attempt: Dirty Screen A attempt 02, Luna correction pass.
- Edit target: `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png`
- Target SHA-256: `6E840715F1FF580A21E8DF3406B5C23733BF584D5046345F7239D72913C04C5D`
- Built-in image generation result ID: `01a0489b-cded-7f33-8675-a6b1fb0d94f5/exec-b2c154ea-d6b5-4ca4-85e5-160eb10fbc2b`
- Native result: `dirty_screen_a_attempt_02_native.png`
- Native result SHA-256: `A5A5200652B387A1A21191C2E7109C20FA9F9038147F481122027386F1932952`
- Native result file size: 2,812,507 bytes.
- Native result metadata: PNG, RGB, 1671×941 (the requested 1672×941 width is short by one pixel).
- Generation method: one built-in `image_gen` precise-object edit; no reference image other than the clean Screen A target; native output copied unchanged.

## Exact prompt

```text
Use case: precise-object-edit
Asset type: interactive Day One dirty-state background for Godot 4 Canvas2D Pearl Castle Main Hall, Screen A.
Input images: Image 1 is the approved clean Screen A edit target.
Primary request: Create a neglected-but-magical version by changing only cleanliness and four specified maintenance areas, while keeping the image globally as bright and colorful as Image 1.
Absolute invariants: preserve the exact 1672x941 canvas, global exposure, lighting direction, palette, camera, perspective, architecture, aquarium, every doorway and corridor, plaques, columns, mouldings, floor and runner edges. No global darkening, vignette, fog, color grade, or reduced saturation. Do not move any landmark.
Integrated dirty atmosphere: add restrained matte lavender-grey dust and soft soot naturally in wall-stone recesses, upper moulding creases, pearl-trim seams, column bases, floor edges, and runner fibers. The room must read clearly unattended, but dust remains localized to surfaces and does not change the overall illumination.
Exactly five clearly readable remedy zones, integrated into the existing surfaces and centered approximately at these Screen A pixel coordinates:
1. sleepy-light cluster at (290,145), maximum 160x110: dull and dust the existing shell-and-pearl trim there without adding a fixture.
2. sleepy-light cluster at (670,145), maximum 160x110: dull and dust the existing shell-and-pearl trim there without adding a fixture.
3. wall remedy at (1450,320), maximum 190x150: one broad naturally accumulated lavender-grey soot/dust area within the existing wall blocks.
4. runner remedy at (1450,700), maximum 220x100: one broad dusty scuffed area contained within the red runner.
5. floor remedy at (650,820), maximum 220x140: one broad dull dusty patch following the floor perspective.
Keep every remedy at least 24 pixels inside its tile-safe zone; do not cross door apertures, signs, columns, runner edges, architectural edges, or image edges. Do not place new marks within the extreme 64-pixel left or right edge strips.
Style: preserve the polished pastel children's storybook medium and existing painted surface texture. Neglect is safe, calm, child-friendly, and clearly cleanable.
Constraints: no isolated stickers or decal-sheet appearance, no new fixtures, characters, creatures, props, text, cracks, damage, slime, horror, rectangular overlays, frames, guides, logos, or watermarks. Return one complete flattened RGB background.

Save unchanged native to assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_02_native.png. Append provenance (prompt, target/result IDs, hashes, dimensions/mode, read-only landmark/global-exposure/local-zone observations). No normalization/tiling/code/license changes.
```

## Read-only review

- The result remains a complete flattened RGB background with the aquarium, doorways/corridors, plaques, columns, mouldings, runner, floor edges, camera, and perspective visibly retained; no new fixtures, characters, props, text, decals, frames, guides, logos, or watermarks were observed.
- The five requested remedy areas are visibly localized and surface-integrated on the upper trim, right wall, runner, and lower floor; the floor patch at approximately `(650,820)` is the clearest. The treatment is soft, matte, pastel, calm, and child-safe rather than photorealistic or damaged.
- Output mean RGB: `[147.24, 115.22, 138.18]`; clean-target mean RGB: `[158.56, 120.78, 142.00]`. On the shared 1671-pixel width, mean signed output-minus-target delta is `[-11.32, -5.56, -3.82]`; mean absolute RGB delta is `11.81`. Left/right 64-pixel edge mean absolute deltas are `8.33` / `10.29`, with no visible edge-strip mark.
- Zone read-only mean absolute RGB deltas versus the clean target: sleepy-light 1 `(210,90)-(370,200)` `19.57`; sleepy-light 2 `(590,90)-(750,200)` `16.33`; wall `(1355,245)-(1545,395)` `21.89`; runner `(1335,650)-(1555,750)` `11.43`; floor `(540,750)-(760,890)` `18.74`.
- Technical outcome: visual/localization review is promising, but the explicit exact-canvas contract is not fully satisfied because the native output is 1671×941 instead of 1672×941. Preserve as source evidence and send to Sol for review; do not normalize, crop, resize, tile, integrate, or otherwise edit this native file.

No runtime, code, or license files were changed.
