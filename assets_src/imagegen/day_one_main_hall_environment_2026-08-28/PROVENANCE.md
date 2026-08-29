# Day One Main Hall environment edit evidence — 2026-08-28

## Dirty Screen A attempt 01

Method: built-in Codex `image_gen` EDIT mode, exactly one call. The sole input
was the approved clean Main Hall Screen A edit target, viewed before editing:

- Target: `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png`
- Target SHA-256: `6E840715F1FF580A21E8DF3406B5C23733BF584D5046345F7239D72913C04C5D`

Result ID available from the tool output:
`01a0489b-cded-7f33-8675-a6b1fb0d94f5/exec-744a7d47-127d-4bb5-ac69-f6edbb304673`.

Native output preserved unchanged as
`dirty_screen_a_attempt_01_native.png` — SHA-256
`3D1A7EB4231B49B3665FB66519C276E97BE7C1D9A877BBE839FAEF7AEC37BB6`.
Read-only metadata: 1672x941 PNG, RGB mode, 2,470,065 bytes, matching the
target's dimensions and aspect ratio exactly. Output corner pixels were
`[(47, 43, 54), (37, 33, 43), (55, 48, 62), (67, 56, 68)]`; no alpha channel
is expected for this flattened background.

Exact edit prompt:

```text
Use case: precise-object-edit
Asset type: complete Day One dirty-state background for the Godot 4 Canvas2D Pearl Castle Main Hall, screen A.
Input images: Image 1 is the edit target, the approved clean Main Hall Screen A.
Primary request: Create a complete neglected-castle version by changing only cleanliness, upkeep, and fixture illumination.
Invariants: Preserve Image 1's exact wide composition and aspect ratio; preserve every doorway, open corridor, plaque, window, aquarium, column, moulding, floor edge, red runner, perspective, camera, silhouette, palette relationships, and polished pastel children's storybook rendering. Do not move, resize, replace, add, or remove architecture.
Dirty state: Add broad integrated matte lavender-grey dust and soft soot accumulated naturally inside stone recesses, wall corners, upper moulding creases, pearl-trim seams, column bases, floor edges, and lightly across the runner. Dull the polished floor in irregular dusty areas. Make the warm shell-light ambience visibly uneven and subdued so the hall reads immediately as long unattended. The room should look clearly dirty and in need of help, but safe, magical, and child-friendly.
Continuity: Keep both vertical screen edges compositionally compatible with the original so the two-screen panorama can join seamlessly. Keep all changes away from the extreme left and right edge strips.
Constraints: Do not add isolated decal-sheet marks, tappable UI, new fixtures, characters, creatures, props, text, cracks, structural damage, slime, photorealistic grime, horror, fog blankets, rectangular overlays, frames, guides, logos, or watermarks. Return one complete flattened background image, not transparency.

Preserve native output unchanged under a new source evidence directory assets_src/imagegen/day_one_main_hall_environment_2026-08-28/dirty_screen_a_attempt_01_native.png, add PROVENANCE.md via apply_patch with target/prompt/result ID/hash/dimensions/mode and read-only visual/geometry observations. Do not normalize, tile, integrate, or touch runtime/code/license files yet. Report.
```

Read-only image comparison against the target: shape is identical; all
1,573,352 pixels differ because the edit globally subdued illumination and
deepened the palette. Mean absolute RGB delta was 51.38, with mean channel
delta `[-60.30, -39.35, -51.03]`. The left and right 32px edge strips remain
the same geometry and were not cropped or shifted; their mean absolute deltas
were 46.86 and 55.51 respectively, versus 51.39 in the interior. This is a
full-frame flattened RGB image, not transparency.

Visual review: all original doorways, corridors, aquarium, columns, mouldings,
red runner, floor edge, and perspective remain in place. The room reads as
clearly neglected through broad subdued lavender-grey/soot darkening in the
upper wall, recesses, trim, columns, runner, and floor. The changes are
integrated rather than isolated decals or rectangular overlays, with no added
characters, props, text, UI, or structural damage. The edit is preserved as a
candidate for Sol review; no normalization, tiling, runtime integration, or
license/code changes were made.

## Historical dirty attempt 01 (superseded; not runtime) (2026-08-28)

The earlier candidate pair was `dirty_screen_a_attempt_01_native.png`
(SHA-256 `3D1A7EB4231B49B3665FB66519C276E97BE7C1D9A877BBE839FAEFAF7EC37BB6`)
and `dirty_screen_b_attempt_01_native.png`
(SHA-256 `C5EF71641039D1A4DB451EEA74EFDCD3D377C52A2E74E3AC26E14C6093BEF28F`),
each 1672x941 RGB. Sol accepted the integrated neglect language and the
dirty-to-dirty panorama continuity. The measured mixed-state seam failures
(clean A->dirty B MAE 60.8, band 107; dirty A->clean B MAE 52.98, band 88.76)
and `dirty_screen_b_attempt_01_native.png`; it is preserved source evidence
only. Its globally dark Screen A and mixed-state seam evidence are superseded
by the v2 candidates below and are not runtime art.

## Clean-v2 registered twin candidates (2026-08-28; pending Sol review)

The clean-v2 twins were generated from the v2 dirty candidates as complete
flattened replacement frames, preserving the new warm lamps and removing the
surface messes. Native outputs are preserved unchanged:

- `clean_screen_a_v2_native.png`, 1672x941 RGB, SHA-256
  `219D09158CF0CA044E0145922CF34E04DD0ED20D960DE3EB0E94E6753453FBE5`.
- `clean_screen_b_v2_native.png`, 1667x943 RGB, SHA-256
  `D9B0EAA8DCAF2E13042EC5EFFD1FA0EF2F9A01E809805952DD2F2A32508EA725`.

Screen B was normalized only as a production whole-canvas transform to the
registered 1672x941 frame size; the native source remains preserved above.
The normalized intermediate is
`clean_v2_build/clean_screen_b_v2_normalized_1672x941.png`, SHA-256
`2FF8CE3C06D274325B2956AEDD81E81AF8CD766A8D84F8DFC03F605AFBBFDF1E`.
The existing approved whole-canvas Lanczos registration then produced the
`clean_v2_build/clean_main_hall_panorama_7280x2048.png` master (SHA-256
`E1B338EDE843A9768CCE0E9708BF4F724687CCD204510D0E084CBAA5DB1D0CAB`) and
sixteen exact non-overlapping `clean_main_hall_day_one_r{row}_c{column}.png`
runtime tiles at 910x1024. `clean_v2_build/build_manifest.json` and
`audit_manifest.json` record the transform chain, hashes, and pixel-exact
reconstruction. No source original was modified and no clean pixels are
copied into the dirty plates; runtime uses the clean family only for registered
per-target reveals and the final all-target state.

## Authoritative v2 native plate record (2026-08-28; pending Sol review)

The four native v2 plates used by the current source/build records are:

- Dirty Screen A v2: `dirty_screen_a_v2_native.png`, 1672x941 RGB, SHA-256
  `E9F424610A9735F181015D8F7DE596F850DF27669040BCC92FFA329FFA0940CA`.
  Built-in ImageGen output ID: `exec-5a5a746c-c62c-443e-a871-3e8dbe4b4fda`.
  Prompt request: complete flattened dirty Main Hall Screen A; preserve the
  approved architecture/composition; add readable integrated dust, runner,
  floor, wall, and fixture grime while retaining bright storybook lighting,
  with no UI, decals, new props, or global dark tint.
- Dirty Screen B v2: `dirty_screen_b_attempt_02_native.png`, 1667x943 RGB,
  SHA-256 `85B781A1F41BC8BA5A18739C34304C20C642F730BC31E656291E9EE4BC9B7E92`.
  Built-in ImageGen output ID: `exec-295f8581-f51a-4057-860c-2196de405336`.
  Prompt request: matching complete flattened dirty Screen B with the same
  concrete mess language and bright hall treatment, preserving the A/B join
  and removing the prior wall-splash clip.
- Clean Screen A v2: `clean_screen_a_v2_native.png`, 1672x941 RGB, SHA-256
  `219D09158CF0CA044E0145922CF34E04DD0ED20D960DE3EB0E94E6753453FBE5`.
  Built-in ImageGen output ID: `exec-1305d597-bfa8-47d2-b39d-d1dd912c0207`.
  Prompt request: complete flattened clean twin of dirty A; preserve the new
  lamps and architecture while removing the individually named surface messes.
- Clean Screen B v2: `clean_screen_b_v2_native.png`, 1667x943 RGB, SHA-256
  `D9B0EAA8DCAF2E13042EC5EFFD1FA0EF2F9A01E809805952DD2F2A32508EA725`.
  Built-in ImageGen output ID: `exec-b3107d3e-e4bd-4738-9266-7a5ae8bed074`.
  Prompt request: complete flattened clean twin of dirty B; preserve the new
  lamps and A/B registration while removing the individually named messes.

The v2 dirty build now uses both bright dirty plates and passes the strict
whole-canvas registration audit: 7280x2048 panorama, exact 2x8 reconstruction,
and center-seam gate all pass. Clean-v2 normalization also passes its audit;
Screen B's native 1667x943 frame is preserved and normalized whole-canvas to
1672x941 before registration. These are implementation candidates only; no
Sol acceptance is claimed here.
