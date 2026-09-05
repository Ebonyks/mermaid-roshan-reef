# Grand Puff Dusty Attic arena — prompt and provenance

Date: 2026-08-30  
Generation method: OpenAI built-in ImageGen  
Use case: `stylized-concept`  
License: project original, all rights reserved  
External URL: none

## Recorded gap

Grand Puff's runtime used a purple clear color behind a primitive spatial
octagon, repeated glowing posts, box crates, sphere dust mounds, and a duplicate
nest. It did not match the painted Pearl Castle rooms. No reusable 2D Dusty
Attic arena existed.

## Bound references

| Image | Role | Path | SHA-256 |
|---|---|---|---|
| 1 | Castle architecture, palette, materials, contour, and painted style | `assets/flats/castle/rooms/room_craft_room_background.png` | `006B736E59E261C2670717F268C76B39640B903373B1A75781CD464E135DDD0D` |
| 2 | Existing gameplay framing and primitive-arena diagnosis only | `audit/day_one_gameplay_2026-08-29/visuals/boss/01_showing_rise.png` | `9A5637CB55536A5CE8D456A4325378DE7D3D674C1DB6FBD4432F3C41D0F492FD` |
| 3 | Soft localized dusty-scuff language only | `assets/castle/dirty_cleanup_2d/targets/target_floor_scuff.png` | `629CCD46D94DEE0E1966455BECFAAE7FB2C6A528FAAAD70CA612467255A41BF3` |

## Final prompt

```text
Use case: stylized-concept
Asset type: production game background for one fixed-camera true-2D boss arena in Mermaid Roshan: Reef of Light
Primary request: Generate a NEW complete square 2048 x 2048 painted background for Grand Puff's Dusty Attic arena inside the established Pearl Castle. This is the dust-bunny boss challenge, so the room must feel like the same castle after long-neglected dust has accumulated.
Input images: Image 1 is the authoritative castle architecture, palette, material, contour, and painted-storybook style reference; Image 2 is the existing gameplay framing reference only and shows the primitive arena composition being replaced; Image 3 is a valid runtime grime reference for the soft localized dusty-scuff language only.
Scene/backdrop: A broad octagonal attic chamber built from the same lavender pearl-brick castle, shell capitals, rounded ivory columns, warm pearl trim, pastel stone/board floor, and toy-playset proportions. A low octagonal ring is painted into the floor by architecture and inlay, not a floating platform. Put a large quiet open play area in the center and lower-middle. Bank soft smoky lavender-grey dust in corners and wall bases; add a few gentle floor scuffs, dusty footprints, pale cobweb arcs, muted grime on lower bricks, and several forgotten rounded pearl storage trunks against the far walls. Dust looks fluffy and magical, never disgusting, scary, photoreal, or brown sludge. The room is visibly dirtier than the clean castle but unmistakably the same castle.
Style/medium: polished 2D children's storybook environment painting; rounded slightly asymmetrical forms; broad painted value bands; confident deep indigo/plum contours; aqua, blue-grey, and lavender shadows; high-key pastel toy playset; match Image 1, not 3D concept art.
Composition/framing: square master with all essential architecture and the complete arena readable within the central 16:9 safe area for a 1280 x 720 crop. Fixed three-quarter/front perspective similar to Image 2 but flattened into a coherent 2D room. The back wall, side walls, floor ring, and open central play band must all read clearly. Quiet central and lower-middle playable band, detailed clusters only at far edges and corners. No foreground object may occlude the central play band.
Lighting/mood: warm diffuse pearl-castle daylight with soft aqua window glow and gentle lavender shadows; playful mystery, safe and inviting, no dramatic spotlight, no vignette, no crushed shadows.
Color palette: dusty lavender pearl brick, warm ivory and shell pink architecture, muted aqua/mint accents, peach and pale gold trim, smoky grey-purple dust; small saturation peaks only at trim.
Materials/textures: hand-painted pearl brick, shell-carved wood/stone, rounded pastel floor inlay, soft fluffy dust banks, restrained cobwebs and scuffs.
Constraints: environment background only; no Mermaid Roshan; no Grand Puff; no dust-bunny character; no people or creatures; no HUD; no buttons; no icons; no labels; no letters; no digits; no logos; no watermark. Do not copy any character or UI from the references. Do not paint interactive targets, a boss nest, reward star, hand pointer, glowing objective, or separate foreground prop into the center. Keep the background calmer and lower-contrast than gameplay characters and touch cues. One complete flattened image with no seams. Original design consistent with the supplied project's established art.
Avoid: 3D render, photorealism, generic medieval dungeon, dark horror attic, purple void, primitive polygon arena, repeated glowing posts, checkerboard plank disk, dirty brown mud, green slime, heavy fog, dramatic bloom, clutter across the play band, text, characters, UI.
```

## Outputs and processing

- `dusty_attic_arena_native_1254.png`: selected native 1254×1254 RGB
  generation, SHA-256
  `9CB4B02DC4A56E1436EA0A6B21DCCF4EF751716D213E3FF7624571F15A9E2CB6`.
- `assets/flats/castle/boss/dusty_attic_arena_2048.png`: 2048×2048 RGB
  power-of-two runtime master, SHA-256
  `A6F4BB59DF43E63CEDBF9A164526475B91985C85C73CAC7E061F830D60EF4122`.
- Production processing is one uniform whole-canvas Lanczos resize. No crop,
  mask, isolated transform, compositing, or protected-source pixel insertion.

## Runtime refinement

- Storage boxes remain painted into the far background; no duplicate runtime
  crate meshes or stickers are added.
- Three generous invisible hotspots align to three authored pearl chests in
  the unobstructed left storage cluster. Right-wall chests remain scenery
  because the persistent HUD owns that screen region. Only a small sparkle cue
  is drawn; there are no floor splotch targets and no duplicate chest sprites
  or meshes.
- Cleaning the three chests, together with the four cleaned Day One castle
  rooms, awards the optional `Castle Sparkle` sticker through the existing
  `stickers` save dictionary.
- The painted platform bevel is reinforced with two low-alpha Canvas lines.
  True-octagon containment tightens to radius 23.5 with a 3.2-unit inset; there
  is no fall, reset, health loss, or lost cleanup progress.
- Mild background response remains bounded to six horizontal and three
  vertical pixels, with twelve low-alpha dust motes.
