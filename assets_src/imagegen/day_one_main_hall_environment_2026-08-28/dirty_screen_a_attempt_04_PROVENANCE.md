# Dirty Main Hall Screen A — attempt 04

## Generation status

- Attempt: Dirty Screen A attempt 04, Luna correction pass.
- Requested method: exactly one built-in `image_gen` precise-object edit with three local references.
- Image 1 edit target: `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png` (SHA-256 `6E840715F1FF580A21E8DF3406B5C23733BF584D5046345F7239D72913C04C5D`).
- Image 2 placement/readability reference: `assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_03_native.png` (SHA-256 `0ADE349BE2B4C95D5199C2418DC358483881529E9FB1BAF46E66EB1AAEC21BB0`).
- Image 3 brightness/softness reference: `assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_02_native.png` (SHA-256 `A5A5200652B387A1A21191C2E7109C20FA9F9038147F481122027386F1932952`).
- Tool outcome: the single built-in edit call returned without a new image content block or result ID, and no new PNG appeared in the image-generation cache. The newest cache entry remains the prior A3 result `exec-d1b2a60f-9769-404f-a069-021b088e64d3.png`, unchanged at 2,696,922 bytes and SHA-256 `0ADE349BE2B4C95D5199C2418DC358483881529E9FB1BAF46E66EB1AAEC21BB0`.
- Native output: not emitted; `dirty_screen_a_attempt_04_native.png` was intentionally not created so no older candidate is misrepresented as this attempt.

## Exact prompt requested

```text
Use case: precise-object-edit
Asset type: interactive Day One dirty-state background for the Godot 4 Canvas2D Pearl Castle Main Hall, Screen A.

Input images:
- Image 1: absolute edit target — assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png.
- Image 2: placement/readability reference only — assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_03_native.png. Preserve its five-zone locations and approximate salience, but do not copy its stippled texture, oversized floor patch, or 1671-pixel width.
- Image 3: brightness/softness reference only — assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_02_native.png.

Primary correction: retain five readable remedy zones while replacing every granular, speckled, noisy, or pasted-looking treatment with broad low-frequency storybook paint integrated into the original surface.

Absolute output contract: return exactly 1672×941 RGB. Preserve Image 1’s exact canvas, camera, aquarium, doorways, corridors, plaques, columns, mouldings, wall blocks, runner edges, floor horizon, perspective, and architectural boundaries. Never inherit either reference’s 1671-pixel width.

Surface treatment: preserve the original wall, trim, runner, and floor texture scale. Existing painted patterns must remain visible through the neglect. Use only two or three broad matte lavender-grey value bands per remedy, with soft surface-colored transitions. No stippling, pointillism, grain cloud, pixel noise, sprayed texture, detached particles, hard cutout edge, or new material.

Exactly five remedies:
1. Trim cluster at (290,145): maximum 130×80; softly dull a compact group of existing shell forms.
2. Trim cluster at (670,145): maximum 130×80; a different compact dull cluster with equal readability.
3. Wall zone at (1450,320): maximum 155×105; one broad low-frequency accumulation following existing stone-block shading.
4. Runner zone at (1450,700): maximum 175×65; one matte scuff that follows the runner weave and remains entirely inside its edges.
5. Floor zone at (650,820): maximum 185×105; one restrained perspective-aligned dusty area. It may be the strongest zone, but must not become a large sprayed oval or obscure the floor pattern.

Readability gate: all five remedies remain distinguishable at 25% full-image scale, but none may dominate the room or appear as a sticker. Each remedy has one coherent silhouette; ambient dust elsewhere remains lower contrast.

Global read: the room must look unattended at first glance through restrained distributed dust in upper creases, trim seams, column bases, floor edges, and runner fibers. Preserve Image 3’s bright, colorful, reassuring exposure; do not apply global darkening, vignette, fog, desaturation, or a color grade.

Keep all remedies clear of doors, plaques, columns, runner boundaries, architectural edges, and the extreme 64-pixel vertical edge strips. No sixth high-salience dirt group.

Constraints: no new fixtures, characters, creatures, props, text, cracks, damage, slime, horror, photorealistic grime, overlays, frames, guides, logos, or watermarks. Return one complete flattened RGB background.
```

No runtime, code, license, or pixel files were changed by this non-emitting attempt.
