# Personalized Castle Banner Style Audit — 2026-08-10

## Authority and scope

The active personalized banner implementation was compared against
`ART_STYLE_GUIDE.md`, `ART_STYLE_AUDIT.md`, `design/02_ART_DIRECTION.md`, the
approved Craft Room and Stuffie Playroom paintings, and the approved royal
tapestry reuse. The runtime inventory found four copies of the purple shell
banner: two in Craft Room and two in Stuffie Playroom. No other active room
contains that design.

## Previous implementation versus the master language

| Criterion | Previous personalized banner | Master requirement | V2 response |
|---|---|---|---|
| Shape | Generic straight flag with an eleven-point procedural hem | Broad rounded masses, shell structure, gentle asymmetry | Fan-shell capital, pearl finials, rounded cloth and a calm three-point scallop |
| Line | Hard double vector stroke | Smooth plum/navy material-related contour | Painted plum edge with restrained gold and cream trim |
| Value/material | Flat fill or radial rainbow wedges | Three high-key value families, tactile storybook material | Authored cloth folds, pearl highlights and lavender/aqua shadow bands |
| Castle grammar | Gold rod only | Shells as structural joints; restrained ceremonial gold | Shell capital and pearl hardware carry the construction, not a shell sticker |
| Emblems | Platform emoji glyphs with inconsistent rendering | Child-readable painted silhouettes, no text, stable visual family | Eight authored motifs with shared brush, value and contour behavior |
| Rainbow hierarchy | Full-saturation radial fill | Rainbow reserved for identity/focal delight and kept out of large ordinary fields | Muted cloth transition plus one centered emblem focal point |
| Runtime medium | Custom `Control._draw()` world decoration | Unshaded `Sprite3D` cards at intentional depth | Two authored, mipmapped `Sprite3D` cards per banner: cloth and selected emblem |

## Individual design audit

- Rainbow: six broad warm-to-cool bands; no text or extra decoration.
- Shell: broad seven-rib fan silhouette with pearl center; directly matches the
  castle's structural shell family.
- Kitty and puppy: clearly distinct plush/craft faces, readable at banner size;
  neither substitutes a generic emoji or protected character.
- Star and heart: single broad silhouettes with one highlight family and a cool
  lower shadow; no dense surface detail.
- Crown: three readable points, pearl terminals, restrained gold and a small
  shell joint; no copied franchise symbol.
- Butterfly: complete four-wing anatomy, body and antennae, simplified into
  countable color regions for phone readability.

All six cloth choices and all eight motif choices resolve through the same
authored component family, covering 48 saved combinations without regenerating
near-duplicate complete banners. Runtime textures are 256x512 banners and
256x256 motifs, lossless with alpha-border repair and mipmaps enabled.

## Deployment and validation

The four active copies are registered in `ROOM_BANNER_RECTS` and created under
`CastleLogoWorldDisplay`. The personalized cards sit just in front of the
painted room background, remain input-transparent, and are freed/rebuilt on room
changes. `probe_interaction.gd` verifies both rooms, the saved color/symbol pair,
the authored V2 texture paths, and removal from rooms without the baked design.

This is a production candidate, not an owner-awarded 5/5. Owner acceptance still
requires device/runtime capture review under the master audit rules.
