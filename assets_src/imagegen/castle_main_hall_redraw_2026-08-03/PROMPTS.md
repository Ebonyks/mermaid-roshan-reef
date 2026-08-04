# Castle Main Hall redraw — 2026-08-03

Generator: OpenAI built-in ImageGen (`image_gen.imagegen`). The native files
below are preserved byte-for-byte from the generator cache. No CLI or API
fallback was used.

## Acceptance ledger

| Role | Dimensions | SHA-256 | Decision |
|---|---:|---|---|
| `concept_reference_1774x887.png` | 1774×887 | `734A26F8AE41157A0A3F070E6CFDD61ED927462BA21F9071C880D46BAB1AC618` | reference only; two-screen ratio was too narrow |
| `rejected_screen_a_square_1254x1254.png` | 1254×1254 | `1E2B2D8016AC7F3F811755747AEC9CA5C4DD8A03BEBCF11C884C66385F47D8E5` | rejected; wrong 1:1 playable-screen ratio |
| `superseded_decorated_screen_a_native_1672x941.png` | 1672×941 | `80A8F6D0A01BDA6908C1763462ACECF5CA96068BDC0A20A133AA31A711BC6A5A` | composition-approved intermediate; superseded because detachable props were baked in |
| `superseded_decorated_screen_b_native_1672x941.png` | 1672×941 | `2416CD4475B02C31399ED9C7FA6718E779B33D2BB4C6CB3D5FDAC2BD70128381` | composition-approved intermediate; superseded because detachable props were baked in |
| `accepted_screen_a_native_1672x941.png` | 1672×941 | `6E840715F1FF580A21E8DF3406B5C23733BF584D5046345F7239D72913C04C5D` | accepted clean native left screen |
| `accepted_screen_b_native_1672x941.png` | 1672×941 | `7E77E4C29BBBDCAF2230031A760137A28371532DEBEFDA971AB1B251DF3EE2AD` | accepted clean native right screen |
| `screen_a_production_master_2048x1152.png` | 2048×1152 | `577ACDF482AFB923E888189351501D3DB69FCC9E8AE5D5BD401F64AAFD76069A` | preserved accepted first-stage whole-canvas normalization; feeds the strict 2K master |
| `screen_b_production_master_2048x1152.png` | 2048×1152 | `8726F60DF470DACD34ED3BF8D1EA40DBA0D374F1F1B0FB1504A99C134E12E885` | preserved accepted first-stage whole-canvas normalization; feeds the strict 2K master |
| `main_hall_production_master_4096x1152.png` | 4096×1152 | `0BED0ED409C966A2BAE7505788F91B86725227B16A46054D85AA672963BFC54C` | preserved prior stitch; no longer a runtime input |
| `screen_a_production_master_3641x2048.png` | 3641×2048 | `F8B3AF85316F0C3E549227A31FE378B83A3500C3379808657C7EAC9662FC2C4D` | preserved rejected normalization; cumulative native-ratio error was 1.151316px |
| `screen_b_production_master_3641x2048.png` | 3641×2048 | `89915458278908EF9ED105386AD205227496EDAD828CE97FFE92E9AB9ED02637` | preserved rejected normalization; cumulative native-ratio error was 1.151316px |
| `main_hall_production_master_7282x2048.png` | 7282×2048 | `E3D91BC5119016C5A1C8BD6FE08A4C1D1964CC16497DF3F31515D4BDC1F10D31` | preserved rejected stitch; never feeds runtime |
| `screen_a_production_master_3640x2048.png` | 3640×2048 | `46C0A3443029A5699BF440E9ABB8289046BD42D4E62195B2D36CE261883EB948` | accepted exact-source-ratio-compliant per-playable-screen 2K master |
| `screen_b_production_master_3640x2048.png` | 3640×2048 | `FF8B69B80ACDA82D156086A33C74AE8F5CC8699ED1CF4D6B69239B7058962F46` | accepted exact-source-ratio-compliant per-playable-screen 2K master |
| `main_hall_production_master_7280x2048.png` | 7280×2048 | `297CD6D181288EF6CC364A71A89FDB4DA168F688249CA910995E71F6F769A9DD` | accepted continuous two-screen strict 2K production master |

The production transform is a documented two-stage, whole-canvas Pillow
Lanczos normalization: accepted native 1672×941 to the preserved 2048×1152
master, then that accepted master to exactly 3640×2048. This was explicitly
authorized by the owner for this situation. There was no crop, padding,
canvas extension, local retouch, seam blend, subject movement, or AI upscale,
and no new art was generated. The first step has a 0.612440-pixel height
rounding error relative to the native ratio. The second step has a 0.5-pixel
height rounding error relative to the accepted 16:9 production ratio. The
cumulative native-to-final ratio check has a 0.588517-pixel height rounding
error. All three checks are inside the one-pixel tolerance. The two final
screens are then pasted side by side without scaling into the 7280×2048
master.

## Architectural screen A (superseded decorated intermediate)

Generator cache path:
`C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\exec-b51a1996-5fdc-4503-b16f-0941c1e08795.png`

References:

- rejected architectural draft, SHA-256 `1E2B2D8016AC7F3F811755747AEC9CA5C4DD8A03BEBCF11C884C66385F47D8E5`
- full continuous concept, SHA-256 `734A26F8AE41157A0A3F070E6CFDD61ED927462BA21F9071C880D46BAB1AC618`
- `audit/castle_sprite3d/rooms_1_contact.png`, SHA-256 `57EDC9BB0DCD72A3CE05683A0E3CF8D2C6AA20C09D4C4EC7A52AF76D19E0EEA9`
- `audit/castle_sprite3d/rooms_2_contact.png`, SHA-256 `9647F1EC9056C5D2F73091B1F9EAFBE124F995BF75213ABA21907CFC6AF26DD1`

Final prompt:

> Create the FINAL LEFT PLAYABLE SCREEN of the Mermaid Roshan castle Main Hall as one complete, clean, flattened 2D storybook environment plate.
>
> CANVAS IS MANDATORY: true 16:9 LANDSCAPE, target 2048 x 1152 pixels. Do not return square, portrait, 2:1, or a crop of a square composition. Design for a 16:9 gameplay viewport.
>
> Image 1 is the accepted architectural/art-direction draft for this half. Preserve its exact identity: luminous lavender shell-and-pearl castle stone, cream-gold trim, aqua accents, storybook hand-painted polish, warm consistent lighting, the same three normal arched room entrances followed by one Opera Hall entrance exactly twice their visual size, the same blank cream scalloped plaque sockets above each entrance, the same open corridor depth, aquarium window at far left, continuous red runner, lavender floor, and discreet floor toys. Images 3 and 4 are the style authority for the existing castle rooms. Image 2 is a composition guide for how both halves belong to one continuous hall.
>
> Recompose Image 1 horizontally into a genuine 16:9 screen without stretching anything: retain natural proportions and expand the useful architectural spacing. Keep all four entrances fully visible and fully reachable. The Opera entrance must be entirely inside this screen, not cut by the right edge. Reserve a simple 8 percent wide continuation band at the extreme right containing only uninterrupted lavender wall, base trim, runner, and floor so the next screen can join cleanly. No column, doorway, lamp, planter, toy, or other readable object may touch or cross that right boundary band.
>
> Reduce dead ceiling and dead floor while still keeping the complete foreground interaction lane. Door signage will be separate Sprite3D cards: leave every plaque socket blank and unmarked. Do not paint icons, letters, logos, text, UI, characters, throne, labels, arrows, interface controls, or watermarks. Do not introduce any new room or duplicate a studio. Keep lighting fixtures visually integrated and discreet, not button-like. Keep geometry straight, symmetrical where intended, polished, and free of AI artifacts.

## Architectural screen B (superseded decorated intermediate)

Generator cache path:
`C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\exec-a0c42314-ea24-492a-8962-9a8d92a4241b.png`

References:

- accepted screen A, SHA-256 `80A8F6D0A01BDA6908C1763462ACECF5CA96068BDC0A20A133AA31A711BC6A5A`
- `concept_right_reference_887x887.png`, SHA-256 `EA728541FD57934A7B973CDF6BB12E77D676CF244DC613004E3AD33A638C60AD`
- the same two approved room contact sheets and hashes listed above

Final prompt:

> Create the FINAL RIGHT PLAYABLE SCREEN of the Mermaid Roshan castle Main Hall as one complete, clean, flattened 2D storybook environment plate.
>
> CANVAS IS MANDATORY: true 16:9 LANDSCAPE, target 2048 x 1152 pixels. Do not return square, portrait, 2:1, or a crop of a square composition. Design for a 16:9 gameplay viewport.
>
> Image 1 is the ACCEPTED LEFT SCREEN and is the absolute continuity authority. This new right screen must look like the same uninterrupted hall photographed by the same camera one screen farther right: identical lavender shell-stone wall texture and scale, identical cream-gold trim profiles, identical aqua/lavender palette, identical warm lighting direction and exposure, identical ceiling bands and heights, identical wall/floor horizon, identical red runner height and trim, identical lavender floor perspective and pattern density, and identical painterly storybook finish. At the extreme left, begin with an 8 percent wide simple continuation band containing only uninterrupted wall, base trim, runner, and floor matching Image 1's extreme right. No column, doorway, lamp, planter, toy, or readable object may touch or cross that left boundary band.
>
> Image 2 is only the layout guide for this half. Preserve its functional identity: four fully visible, evenly spaced NORMAL-SIZE arched room entrances with deep open corridors; each entrance has one blank cream scalloped plaque socket above it; then at the far right a generous raised shell-and-pearl royal dais/alcove reserved for the existing Huluu throne Sprite3D. The throne itself must NOT be painted into this background. Images 3 and 4 are the style authority for existing castle rooms.
>
> All four doors must be fully visible, easy to approach, and free of props in front. Do not duplicate any room or studio. Keep a broad unobstructed navigation lane. Add only a few discreet, child-friendly floor interactions near the lower edge, away from entrances and the throne socket, using the same toy vocabulary as Image 1. Reduce dead ceiling and floor while preserving the full foreground lane.
>
> Door signage will be separate Sprite3D cards: leave every plaque socket blank and unmarked. Do not paint icons, letters, logos, text, UI, characters, throne, labels, arrows, interface controls, or watermarks. Keep lighting fixtures visually integrated and discreet, not button-like. Match the exact number/design/height language of Image 1 rather than inventing a third lamp family. Keep geometry straight, polished, and free of AI artifacts.

## Accepted clean screen A

Generator cache path:
`C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\exec-b6c0d3d0-687d-4a0d-bf45-22e0d68077aa.png`

Reference: superseded decorated screen A, SHA-256
`80A8F6D0A01BDA6908C1763462ACECF5CA96068BDC0A20A133AA31A711BC6A5A`.

Final prompt:

> Edit Image 1 into the final CLEAN ARCHITECTURAL BACKGROUND PLATE for the LEFT 16:9 playable screen of Mermaid Roshan's castle Main Hall.
>
> This is a strict object-separation cleanup, not a redesign. Preserve exactly the 1672:941 landscape aspect, camera, composition, geometry, three normal doors plus the double-size Opera door, open corridor depths, blank cream plaque sockets, aquarium window architecture, lavender shell-stone texture, cream-gold moldings, columns, wall/floor horizon, red runner, floor perspective, lighting tone, palette, and painterly storybook finish.
>
> REMOVE AND HEAL ONLY EVERY DETACHABLE PROP so those approved objects can be reinserted as separate Sprite3D cards at real scene depth: remove all wall sconces and their painted glows; remove the hanging chandelier; remove both pearl niche lamps; remove every coral/plant vase, urn, and planter; remove all foreground toys, blocks, boats, loose pearls, coral clusters, and shell toys.
>
> Heal each vacated area seamlessly with the exact surrounding wall, trim, doorway, runner, railing, or floor texture and lighting. Keep the aquarium window and all architectural shell/pearl moldings. Keep every door fully open and free of objects. Keep all blank sign sockets unchanged. Add nothing. Move nothing. Do not repaint, restyle, relight, crop, stretch, label, or alter any door. No icons, text, signs, UI, characters, throne, lamps, furniture, props, or watermarks. Return one complete true 16:9 flattened background plate, not a square image.

## Accepted clean screen B

Generator cache path:
`C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\exec-9c6c2d15-dd2b-407e-8cb3-513f49391777.png`

References: accepted clean screen A, SHA-256
`6E840715F1FF580A21E8DF3406B5C23733BF584D5046345F7239D72913C04C5D`,
and superseded decorated screen B, SHA-256
`2416CD4475B02C31399ED9C7FA6718E779B33D2BB4C6CB3D5FDAC2BD70128381`.

Final prompt:

> Edit Image 2 into the final CLEAN ARCHITECTURAL BACKGROUND PLATE for the RIGHT 16:9 playable screen of Mermaid Roshan's castle Main Hall. Image 1 is the just-approved clean left screen and is the absolute continuity authority at the join.
>
> This is a strict object-separation cleanup, not a redesign. Preserve exactly Image 2's 1672:941 landscape aspect, camera, composition, four normal doors, open corridor depths, blank cream plaque sockets, empty far-right royal dais/alcove for the existing Huluu throne Sprite3D, lavender shell-stone texture, cream-gold moldings, columns, wall/floor horizon, red runner and dais carpet, floor perspective, palette, and painterly storybook finish. Match Image 1's clean boundary, exposure, texture scale, trim heights, runner height, and floor tone.
>
> REMOVE AND HEAL ONLY EVERY DETACHABLE PROP so approved objects can be reinserted as separate Sprite3D cards at real scene depth: remove all wall sconces and their painted glows; remove the hanging chandelier; remove both pearl niche lamps beside the throne alcove; remove every coral/plant vase, urn, and planter; remove all foreground toys, blocks, boats, loose pearls, coral clusters, and shell toys.
>
> Heal each vacated area seamlessly with the exact surrounding wall, trim, doorway, runner, stairs, railing, or floor texture and lighting. Keep all architectural shell/pearl moldings and the empty throne dais. Keep every door fully open and free of objects. Keep all blank sign sockets unchanged. Add nothing. Move nothing. Do not repaint, restyle, relight, crop, stretch, label, or alter any door. No icons, text, signs, UI, characters, throne, lamps, furniture, props, or watermarks. Return one complete true 16:9 flattened background plate, not a square image.

## Tiling and seam evidence

`tools/build_audit_castle_main_hall_redraw_2k.py` is the blocking,
redraw-specific deterministic pipeline. It re-derives the accepted 2048×1152
masters from their native sources pixel-exactly, builds the two 3640×2048
whole-canvas masters, stitches 7280×2048, and losslessly splits the result into
16 non-overlapping runtime cards arranged as two rows by eight columns. The
all eight columns are 910 pixels wide, and both row heights are 1024. The A/B
boundary is exactly x=3640 after column 3,
and every runtime card has a longest edge of 1024 or less.

The accepted audit reports zero changed reconstruction channels and maximum
reconstruction delta zero. Screen A/B content-invariance MAE is 0.286388 /
0.274822 with correlation 0.999907 / 0.999918 after audit-only normalization
back to the accepted prior size. The independently authored center join has
edge MAE 7.292806, p95 20, and 32-pixel band delta 9.717615. A second
`--audit-only` invocation reproduced every output hash exactly.

Portable manifests and review proofs:

- `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_strict_2k_build_manifest.json`
- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_audit.json`
- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_transform_overlay.png`
- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_grid_proof.png`
- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_seam_proof.png`
- `audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_reconstruction_proof.png`

The preserved 4096×1152 and rejected 7282×2048 masters are provenance only.
Rejected 1025px bleed experiments remain audit-only and do not feed Godot.
