# Day One Main Hall environment edit evidence — Screen B — 2026-08-28

## Dirty Screen B attempt 01

Method: built-in Codex `image_gen` EDIT mode, exactly one call. Both inputs were
viewed before editing and supplied in the requested order:

- Image 1 edit target: `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_b_native_1672x941.png`
- Target SHA-256: `7E77E4C29BBBDCAF2230031A760137A28371532DEBEFDA971AB1B251DF3EE2AD`
- Image 2 continuity reference only: `assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_01_native.png`
- Continuity reference SHA-256: `3D1A7EB4231B49B3665FB66519C276E97BE7C1D9A877BBE839FAEF7AEC37BB6`

Result ID available from the tool output:
`01a0489b-cded-7f33-8675-a6b1fb0d94f5/exec-5017598c-35f8-4e92-b75c-dc4d018af773`.

Native output preserved unchanged as
`dirty_screen_b_attempt_01_native.png` — SHA-256
`C5EF71641039D1A4DB451EEA74EFDCD3D377C52A2E74E3AC26E14C6093BEF28F`.
Read-only metadata: 1672x941 PNG, RGB mode, 2,399,614 bytes. Dimensions and
aspect ratio match the clean Screen B target exactly. Output corner pixels were
`[(28, 28, 38), (41, 37, 44), (68, 59, 74), (68, 57, 70)]`; this is a
flattened background and has no alpha channel.

Exact edit prompt:

```text
Use case: precise-object-edit
Asset type: complete Day One dirty-state background for the Godot 4 Canvas2D Pearl Castle Main Hall, screen B.

Input images:
- Image 1: edit target — the approved clean Main Hall Screen B.
- Image 2: continuity reference only — accepted dirty Screen A. Use Image 2 only to match neglect intensity, illumination, palette, and the panorama join; never copy its architecture or objects.

Primary request: Create the matching complete neglected-castle version of Image 1 by changing only cleanliness, upkeep, and fixture illumination.

Invariants: Preserve Image 1’s exact 1672x941 composition, every small doorway and open corridor, plaque, large curtained arch, stairs, columns, mouldings, floor edge, red runner, perspective, camera, silhouette, and polished pastel children’s storybook rendering. Do not move, resize, replace, add, or remove architecture.

Dirty-state continuity: Match Image 2’s broad integrated matte lavender-grey dust, restrained soot, subdued uneven shell-light ambience, dull trim, lightly dusty runner, and irregularly dulled floor. Screen B must feel like the same unattended hall at the same moment—not cleaner, darker, smokier, or more damaged than Screen A.

Join requirement: Match Image 2’s rightmost edge to Image 1’s leftmost edge by continuing the same wall value, upper soot density, horizontal trim brightness, baseboard treatment, runner exposure, and floor haze at corresponding heights. Keep the leftmost 64 pixels free of new localized marks, objects, or vertical exposure bands. Preserve Image 1’s left-edge geometry exactly; create no seam, duplicated architecture, or copied Screen A fixture.

Child-safety requirement: The hall may look clearly neglected and in need of help, but must remain safe, magical, calm, and readable for a four-year-old.

Constraints: Do not add isolated decals, tappable UI, characters, creatures, props, text, cracks, structural damage, slime, photorealistic grime, horror, fog blankets, rectangular overlays, frames, guides, logos, or watermarks. Return one complete flattened RGB background image, not transparency.

Preserve unchanged as assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_b_attempt_01_native.png. Append full provenance. Do not normalize, tile, integrate, or alter runtime/code/license files. Report metadata/hash and read-only continuity/geometry observations.
```

Read-only comparison against the clean Screen B target: array shape is
identical and all 1,573,352 pixels differ because the edit applies broad
subdued illumination and accumulated grime. Mean absolute RGB delta is 52.49;
mean channel delta is `[-65.38, -38.93, -50.54]`. The leftmost 64px strip has
no added localized geometry or vertical exposure band by visual inspection;
its target-difference mean is 54.47. The output remains a complete flattened
RGB background with no transparency or composited decal sheet.

Read-only continuity measurement against dirty Screen A's rightmost column and
dirty Screen B's leftmost column: mean absolute RGB edge difference 7.57, max
43, with sampled row means `[6.33, 6.67, 17.33, 2.67, 3.00, 3.00]` at rows
0, 100, 300, 500, 700, and 900. Dirty Screen B's mean RGB is `[89.93, 75.35,
84.34]`; dirty Screen A's is `[98.27, 81.42, 90.97]`, so B is moderately
darker overall and requires Sol review for same-moment illumination parity.

Visual review: the four small doorways, open corridors, large curtained arch,
stairs, columns, mouldings, red runner, floor edge, and perspective remain
recognizable and in their original positions. Broad matte lavender-grey/soot
darkening is integrated across upper wall recesses, trim, columns, runner, and
floor; there are no added characters, props, text, UI, structural cracks, or
rectangular overlays. The result is preserved as a candidate for Sol review;
no normalization, tiling, runtime integration, or code/license changes were
made.
