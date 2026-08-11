# Personalized Castle Banner V2 Provenance

Generated 2026-08-10 with the OpenAI built-in ImageGen tool in Codex. These
assets are project-original. No external URL or third-party artwork is used.

## Banner source

- Result ID/file: `exec-e98c465b-c981-4419-aec7-f3084a27e699.png`
- Preserved keyed file: `castle_personal_banner_keyed.png`
- Keyed SHA-256: `6FE9BAA03CC0BE764D3AEE8C048A0490C67FBFF7962DC1AC99A47588998A249D`
- Transparent file: `castle_personal_banner_master.png`
- Transparent SHA-256: `976C92554046D2288A321E60733E7A97FADEF0DAAAAA3188BBA307D5FB08EDAC`
- Style references: `assets/flats/castle/rooms/room_craft_room.png`,
  `assets/flats/castle/rooms/room_playroom.png`, and
  `assets/flats/castle/main_hall_2screen/castle_royal_tapestry_reuse.png`
- Matte command: `remove_chroma_key.py --input castle_personal_banner_keyed.png --out castle_personal_banner_master.png --auto-key border --tolerance 38`

Exact prompt:

> Create one isolated, complete vertical personalized castle wall banner asset for a preschool underwater storybook game, using the attached craft-room, playroom, and approved royal tapestry images only as visual style references.
>
> SUBJECT AND COMPOSITION
> - Exactly one front-facing narrow vertical hanging banner, centered and fully visible, with generous empty margin on every side.
> - Straight restrained gold hanging rod with one rounded pearl finial at each end.
> - Warm pearl-and-shell-cream frame language, including a small fan-shell capital centered above the cloth.
> - One broad, rounded hanging cloth panel with a gently scalloped three-point lower edge; slightly handmade asymmetry.
> - A large blank circular pearl medallion centered in the upper-middle of the cloth. The medallion must be empty so a separate child-selected emblem can be layered later.
> - Two or three quiet painted fold/value bands only. No tiny decoration.
>
> STYLE
> - Match the Mermaid Roshan pearl-castle language visible in the references: polished 2D storybook painting, high-key pastel toy playset, broad painted color blocks, soft tactile cloth, smooth deep-plum/navy contours, aqua/lavender shadows, restrained ceremonial gold, cream pearls.
> - Strong readable silhouette at about 90 x 180 screen pixels.
> - Clean confident outer contour, no white sticker rim, no photorealism, no 3D render, no vector-flat UI appearance.
> - Cloth should be a pale near-neutral lavender-white so runtime tinting into pink, gold, mint, ocean blue, or purple preserves painted folds.
> - The blank medallion should remain warm pearl cream and visually separate from the tintable cloth.
>
> OUTPUT / KEYING
> - Put the object on a perfectly flat solid #FF00FF magenta background.
> - Magenta is background only and must not appear anywhere on the banner.
> - No shadows cast onto the background.
> - No text, letters, numbers, logos, characters, extra banners, room scene, border, grid, labels, or watermark.
> - Entire object must fit inside the canvas with nothing cropped.

## Motif source

- Result ID/file: `exec-bafd870f-b87c-459b-88bb-9fef570bb262.png`
- Preserved keyed file: `castle_banner_motifs_keyed.png`
- Keyed SHA-256: `3A7E5A81C1D34AE1E6878728C50B069DC0D37BA5CB624C51028905B3F094A532`
- Transparent file: `castle_banner_motifs_master.png`
- Transparent SHA-256: `19A79F613C6246D8CC7EF386C09D6E297E6BA3CFEED891812375443852B37602`
- Style references: `assets/flats/castle/rooms/room_craft_room.png`,
  `assets/flats/castle/rooms/room_playroom.png`, `assets/mg/star.png`,
  `assets/mg/rainbow_swatch.png`, and `assets/mg/butterfly.png`
- Matte command: `remove_chroma_key.py --input castle_banner_motifs_keyed.png --out castle_banner_motifs_master.png --auto-key border --tolerance 38`

Exact prompt:

> Create one clean production sprite sheet containing exactly eight separate painted emblem motifs for a preschool underwater castle banner. Use the attached castle rooms and approved existing star, rainbow fin, and butterfly assets as visual-style references, but redraw a cohesive banner-emblem family rather than copying pixels.
>
> LAYOUT — EXACT
> - Flat solid #FF00FF magenta background.
> - Exactly 4 equal columns and 2 equal rows, with no visible grid or dividers.
> - Exactly one motif centered in each cell, consistent apparent size, generous magenta clearance around every motif.
> - Top row, left to right: (1) small arched six-band rainbow, (2) broad fan shell, (3) friendly child-made plush kitty face, (4) friendly child-made plush puppy face.
> - Bottom row, left to right: (5) five-point star, (6) simple rounded heart, (7) three-point pearl princess crown, (8) complete butterfly with four wings, body, and antennae.
> - Do not swap, omit, repeat, merge, or add motifs.
>
> STYLE
> - Polished 2D storybook painting matching Mermaid Roshan castle art: broad rounded readable masses, gentle handmade asymmetry, two or three calm value bands, subtle brush texture, high-key pearl/coral/aqua/lavender palette.
> - Confident smooth deep-indigo or plum contour, with sparse interior lines.
> - Each emblem should read clearly when displayed at about 42 pixels wide.
> - Keep species/object identity clear. Kitty and puppy must be distinct; no unicorn horn. Butterfly must have complete anatomy but simplified pattern.
> - Warm cream highlights and cool lavender/aqua shadows. Small restrained gold accents are allowed.
> - No photorealism, no 3D render, no generic emoji look, no flat vector icon look, no white sticker rim.
>
> OUTPUT / KEYING
> - Magenta is background only and must not occur in any motif.
> - No cast shadows on the background.
> - No words, letters, numbers, captions, cell labels, borders, frames, banners, shields, logos, characters, scenery, watermark, or extra objects.
> - All eight motifs fully visible and uncropped.

## Runtime derivation

`tools/build_castle_banner_art.py` crops alpha bounds, recolors only the cool
neutral cloth while preserving the authored folds and warm pearl/gold hardware,
creates the muted rainbow treatment, resizes the six complete banners to
256x512, and splits the motif master into eight 256x256 transparent icons. No
protected source asset is modified or copied into the output.
