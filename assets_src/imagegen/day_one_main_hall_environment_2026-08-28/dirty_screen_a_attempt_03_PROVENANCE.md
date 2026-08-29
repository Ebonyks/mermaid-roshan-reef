# Dirty Main Hall Screen A — attempt 03

## Source and generation

- Attempt: Dirty Screen A attempt 03, Luna correction pass.
- Image 1 absolute edit target: `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png`
- Image 1 SHA-256: `6E840715F1FF580A21E8DF3406B5C23733BF584D5046345F7239D72913C04C5D`
- Image 2 brightness/localized-zone reference only: `assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_02_native.png`
- Image 2 SHA-256: `A5A5200652B387A1A21191C2E7109C20FA9F9038147F481122027386F1932952`
- Image 3 integrated-neglect vocabulary reference only: `assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_01_native.png`
- Image 3 SHA-256: `3D1A7EB4231B49B3665FB66519C276E97BE7C1D9A877BBE839FAEFAF7EC37BB6`
- Built-in image generation result ID: `01a0489b-cded-7f33-8675-a6b1fb0d94f5/exec-d1b2a60f-9769-404f-a069-021b088e64d3`
- Native result: `dirty_screen_a_attempt_03_native.png`
- Native result SHA-256: `0ADE349BE2B4C95D5199C2418DC358483881529E9FB1BAF46E66EB1AAEC21BB0`
- Native result metadata: PNG, RGB, 1671×941, 2,696,922 bytes.
- Generation method: exactly one built-in `image_gen` precise-object edit with the three local inputs in the roles above; native output copied unchanged.

## Exact prompt

```text
Use case: precise-object-edit
Asset type: interactive Day One neglected-state background for the Godot 4 Canvas2D Pearl Castle Main Hall, Screen A.

Input images:
- Image 1: absolute edit target — assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png.
- Image 2: brightness and localized-zone reference only — assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_02_native.png. Never inherit its 1671-pixel width.
- Image 3: integrated-neglect vocabulary reference only — assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_01_native.png. Use its distributed dust language, never its heavy global darkness.

Primary request: Create a brighter but unmistakably unattended Screen A with exactly five clearly readable, surface-integrated remedy zones. The whole room must read neglected at first glance, while the five zones remain the only high-salience cleanable areas.

Absolute output contract: return exactly 1672×941 RGB. Do not crop, rescale, extend, reframe, or shift the camera. Preserve Image 1’s exact aquarium, three small doorways, Opera doorway, corridors, plaques, columns, mouldings, wall blocks, runner edges, floor horizon, perspective, and every architectural boundary.

Global neglect: retain Image 2’s colorful, reassuring exposure and the aquarium as a bright safety anchor, but increase distributed matte lavender-grey dust across upper moulding creases, pearl-trim seams, wall recesses, column bases, floor edges, and runner fibers until the room reads clearly long unattended at normal gameplay size. Keep it substantially brighter and less ominous than Image 3. Achieve neglect through painted surface accumulation, not a global dark grade, vignette, fog, or desaturation.

Exactly five high-salience Screen A remedy zones:
1. Upper-trim cluster centered at (290,145), maximum 160×110: visibly dull and dust a compact group of existing shell-and-pearl trim forms. Preserve their geometry and add no fixture.
2. Upper-trim cluster centered at (670,145), maximum 160×110: a distinctly shaped second dusty/dulled trim cluster, equally readable but not duplicated.
3. Wall zone centered at (1450,320), maximum 190×150: one broad soft lavender-grey soot accumulation integrated within the existing stone blocks.
4. Runner zone centered at (1450,700), maximum 220×100: one clearly visible matte dusty scuff contained entirely inside the red runner.
5. Floor zone centered at (650,820), maximum 220×140: one broad dull dusty patch following the floor perspective.

Target readability: each of the five zones must remain plainly distinguishable when the complete image is viewed at 25% scale. Each zone needs one coherent silhouette and stronger local value contrast than the surrounding ambient dust, without looking pasted on. Do not add any sixth high-salience dirt group. Ambient neglect elsewhere must remain subordinate.

Safety and placement: keep every remedy at least 24 pixels inside its permitted zone and clear of door apertures, plaques, columns, runner edges, architectural boundaries, and image edges. Keep the extreme left and right 64-pixel strips free of localized marks and vertical exposure bands so the future Screen B edit can join cleanly.

Style: preserve the polished pastel children’s storybook medium, warm lavender/aqua/gold relationships, and calm magical mood. No frightening darkness.

Constraints: no isolated sticker/decal appearance, new fixtures, characters, creatures, props, text, cracks, structural damage, slime, horror, photorealistic grime, fog blanket, rectangular overlay, frame, guide, logo, or watermark. Return one complete flattened RGB background.
```

## Read-only review

- The complete hall remains visually intact: bright aquarium safety anchor, three small doorways and Opera doorway, corridors, plaques, columns, mouldings, wall blocks, runner, floor horizon, camera, and perspective are retained. No new fixtures, characters, creatures, props, text, stickers, decals, frames, guides, logos, or watermarks were observed.
- The five remedy areas are visibly localized and integrated into existing surfaces: two upper-trim clusters, a broad right wall accumulation, a contained runner scuff, and a broad perspective-following floor patch. The lower floor zone is the clearest; the other four remain readable at full view. Distributed dust is brighter and less ominous than the heavy darkness of Image 3.
- Output mean RGB: `[152.58, 122.66, 141.42]`; clean-target mean RGB: `[158.56, 120.78, 142.00]`. On the shared 1671-pixel width, mean signed output-minus-target delta is `[-5.99, 1.88, -0.57]`; mean absolute RGB delta is `11.89`. Left/right 64-pixel edge mean absolute deltas are `9.03` / `8.15`, with no visible edge-strip marks or exposure bands.
- Zone read-only mean absolute RGB deltas versus the clean target: sleepy-light 1 `(210,90)-(370,200)` `16.16`; sleepy-light 2 `(590,90)-(750,200)` `15.67`; wall `(1355,245)-(1545,395)` `18.44`; runner `(1335,650)-(1555,750)` `13.86`; floor `(540,750)-(760,890)` `21.50`.
- Technical outcome: style, landmarks, brightness, localization, and visual continuity are promising, but the explicit exact-canvas contract is not fully satisfied because the native output is 1671×941 instead of 1672×941. Preserve as source evidence for Sol review; do not crop, resize, extend, normalize, tile, integrate, or otherwise edit this native file.

No runtime, code, or license files were changed.
