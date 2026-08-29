# Stuffie Room dirty-state perspective set

## Scope

These ten complete, character-free 16:9 location authorities establish the
Stuffie Room as a spatially coherent place instead of a single front-facing
stage. They belong only to the visibly dirty state before Baby Eagle's final
trailing gust. They are reference anchors, not approved final cinematic frames.

All normalized authorities are `1024x576` RGB. Each native `1672x941`
generation is preserved unchanged under `source_masters/`. Normalization is one
whole-canvas Lanczos resize; no subject, prop or room element was isolated,
moved, painted over or composited during normalization.

## Camera authorities

| ID | Normalized authority | View and depth role | SHA-256 |
|---|---|---|---|
| `P01_LEFT_DOORWAY` | `STUFFIE_ROOM_DIRTY_ANGLE_01_LEFT_DOORWAY.png` | Child-height left entrance oblique; near left basket, distant right tunnel | `9ce191db5ec0ce53cd38589bec2e8152eab3f86ffb4504471a7a7763f4fe134b` |
| `P02_RIGHT_DOORWAY` | `STUFFIE_ROOM_DIRTY_ANGLE_02_RIGHT_DOORWAY.png` | Opposite entrance oblique; near right basket, distant left tent | `312b76fc759063f94fb225096c1b77fea9c49b5b919c156d981a1302cae7e9de` |
| `P03_LOW_FLOOR` | `STUFFIE_ROOM_DIRTY_ANGLE_03_LOW_FLOOR.png` | Floor-level central depth lane toward the shell nook | `439d136b9b253169eab5e6cb61a084291a8a71f1d65b0adeca53cb700e36298e` |
| `P04_BALCONY` | `STUFFIE_ROOM_DIRTY_ANGLE_04_BALCONY.png` | High left-balcony overlook with rail and column foreground | `7ac71388beccbd5ea4e1f6febea94a3ed3a7e1f84dfbab8399d7034b751a8937` |
| `P05_LEFT_BASKET` | `STUFFIE_ROOM_DIRTY_ANGLE_05_LEFT_BASKET.png` | Over-left-basket foreground toward nook and right side | `bde5a1db5222ea485b0bcb1806e63a65c05cabe5260fad92b23e67e7501367fc` |
| `P06_RIGHT_BASKET` | `STUFFIE_ROOM_DIRTY_ANGLE_06_RIGHT_BASKET.png` | Over-right-basket foreground toward nook and left side | `d738e68b24d746c7c55bcde469dd8023714528747754582656b2cdaaf7055ecc` |
| `P07_CENTER_LIGHT` | `STUFFIE_ROOM_DIRTY_ANGLE_07_CENTER_LIGHT.png` | Low upward view establishing ceiling height and all three lights | `39df32fce3c4e909fd0dac9acdc5bfdfcd106065842a6888ee547183a2913c28` |
| `P08_TENT_PEEK` | `STUFFIE_ROOM_DIRTY_ANGLE_08_TENT_PEEK.png` | Intimate view outward through the rear-left tent flap | `2d1fdfa444e9fa7adfff6b331ea8a62ffb951eebc729de3243b18d83e2534254` |
| `P09_REVERSE_ENTRANCE` | `STUFFIE_ROOM_DIRTY_ANGLE_09_REVERSE_ENTRANCE.png` | Reverse view from the shell nook toward the single entrance wall | `eb17c41f11bfb66c6c82a91567cd81e9162d77d84060b0e784ddf42518aa8835` |
| `P10_REAR_RIGHT` | `STUFFIE_ROOM_DIRTY_ANGLE_10_REAR_RIGHT.png` | Rear-right lateral wide with tunnel/blocks foreground and tent depth | `9902f6786998640ef1522aece30dd3b558420c26770970275d7427561ce0a11f` |

## Spatial continuity locks

- The original front-wide authorities remain the primary geography truth.
- The opposite wall has one broad rounded, pearl-trimmed entrance centered
  between the two foreground basket positions. `P09` is its authority.
- A perspective may occlude a landmark, but it may not relocate, duplicate or
  redesign one. Exactly three ceiling lights and two aqua baskets exist.
- These images remain dirty. Never use one after the clean reveal in `SH050`.
- A later clean-angle set requires new full-frame generations for the matching
  viewpoints; do not erase dirt or composite the clean front plate into these.

## Generation provenance

- Date: `2026-08-29`
- Method: Codex built-in image generation with two project-local references
- Use case: `illustration-story`
- Image 1 / primary appearance authority:
  `../STUFFIE_ROOM_DIRTY_GEOGRAPHY.png`, SHA-256
  `f50ae511d59f4f328d017041bef7469aadb3320ab7bd403c0c82f43a1692578b`
- Image 2 / fixed-architecture supporting authority:
  `../STUFFIE_ROOM_CLEAN_GEOGRAPHY.png`, SHA-256
  `5c7797c3be3586daca648f4fa4ab1161368f1c99fee719b42ba5efd27f5eaf6f`
- Human review: required before any perspective becomes an accepted motion
  starting frame

### Shared prompt

```text
Use case: illustration-story
Asset type: complete 16:9 cinematic location-perspective authority for Mermaid Roshan animation
Input images: Image 1 is the complete dirty-state room and primary appearance authority; Image 2 confirms the same room's fixed architecture and clean-state shapes only.
Primary request: Generate a newly painted full-frame perspective of the exact same Stuffie Room from the camera angle specified below. Reconstruct true spatial depth; do not crop, paste, warp, mirror, or merely skew the reference.
Scene invariants: the same lavender castle playroom, centered shell-shaped stuffie nook on the far wall, exactly three shell-and-pearl ceiling lights, two large aqua stuffie baskets, rear-left navy play tent, cubby shelves, stacking rings, blocks, rainbow tunnel, arched aqua windows, pearl columns and upper balcony rail. Preserve object designs, proportions, palette and plausible relative positions as seen from the new viewpoint.
State invariants: this is the BEFORE-cleaning dirty version. Preserve dim grey-lavender light, readable cobwebs, dusty floor film, footprints and smudges, soft lint/dust piles, harmless paper/fabric scraps, overfilled baskets, displaced toys and rumpled nook. Keep it warm, whimsical and child-safe.
Style: polished flat 2D pastel watercolor/gouache storybook illustration, navy-violet contours, broad painted value bands, restrained cel shading; no 3D render look.
Constraints: no characters, no Baby Eagle, no Roshan, no Dust Bunnies, no text, no UI, no watermark, no extra light, basket, door, bed, throne, pool, exterior landscape or invented landmark.
```

### Exact camera suffixes

1. `LEFT DOORWAY OBLIQUE WIDE`: camera just inside the screen-left entrance at
   child eye height, aimed diagonally across the room toward the shell nook and
   far-right rainbow tunnel. The left foreground aqua basket is close and large
   at the lower-left edge; the right basket recedes across the floor. Strong
   converging floor-brick lines and staggered columns establish depth. Keep all
   three ceiling lights spatially plausible and the central acting lane readable.
2. `RIGHT DOORWAY OBLIQUE WIDE`: camera just inside the screen-right entrance
   at child eye height, aimed diagonally across the room toward the shell nook
   and rear-left tent. The right foreground aqua basket is close and large at
   the lower-right edge; the left basket recedes across the floor. Strong
   converging floor-brick lines and layered columns establish depth. This is the
   opposite physical viewpoint, not a mirrored copy; keep banners, tent, blocks,
   windows and lights on their correct room sides.
3. `LOW CENTRAL FLOOR DOLLY`: camera only a few inches above the central floor,
   placed between the two foreground baskets and aimed straight toward the shell
   nook. Floor bricks and dusty footprints dominate the lower half and lead deep
   into the room; both basket rims frame the near left and right edges, stacking
   rings and blocks sit midground, and the shell nook rises in the distance.
   Wide cinematic lens without fisheye distortion.
4. `HIGH BALCONY OVERLOOK`: camera on the upper screen-left balcony, looking
   diagonally downward across the rail into the room. The pearl rail and a nearby
   column create a close foreground layer; the two aqua baskets, tent, blocks,
   tunnel and shell nook spread below in a readable floor plan. Show substantial
   floor depth and all three hanging lights at plausible heights without turning
   this into a top-down diagram.
5. `LEFT BASKET OVER-RIM`: camera at preschool eye height immediately behind
   and slightly above the left aqua basket, looking over its overflowing stuffies
   diagonally toward the central shell nook and the distant right basket. The
   basket rim and stuffies form a strong near foreground; stacking rings and tent
   sit midground; shell nook and right-side tunnel recede. Keep enough visible
   floor for a transitional camera move.
6. `RIGHT BASKET OVER-RIM`: camera at preschool eye height immediately behind
   and slightly above the right aqua basket, looking over its overflowing
   stuffies diagonally toward the central shell nook and the distant left basket.
   The basket rim and stuffies form a strong near foreground; blocks and rainbow
   tunnel sit midground; shell nook, tent and left basket recede. This is a
   physically distinct right-side view, not a mirrored duplicate.
7. `UPWARD CENTRAL-LIGHT ESTABLISHER`: camera low in the central acting lane,
   tilted upward about 35 degrees. The center shell-and-pearl light is the
   dominant near overhead feature; left and right lights recede in perspective,
   with ceiling bricks, upper balcony rails, columns, cobwebs and the top of the
   shell nook establishing vertical depth. Keep a narrow lower band of floor and
   recognizable room props so this still reads as the same room, not a
   ceiling-only image.
8. `TENT-FLAP PEEK`: camera just inside the rear-left navy play tent, looking
   outward through its curved open flap across the dirty room. The soft dark tent
   fabric and a few nearby stuffed toys frame the foreground edges; stacking
   rings and left basket are nearer, the shell nook is across the middle distance,
   and the right basket/tunnel recede farther away. Child-height, intimate but
   still a broad readable room view.
9. `SHELL-NOOK SIDE REVERSE DIAGONAL`: camera near the right edge of the central
   shell nook, at child eye height, aimed diagonally outward across the open floor
   toward both foreground aqua baskets and the room entrance wall. The scalloped
   shell edge, cubbies and a few stuffies form the close foreground; floor bricks
   and scattered mess lead toward the baskets. Reveal a simple matching lavender
   entrance wall with one broad rounded pearl-trim doorway centered between the
   baskets, consistent with the room, without adding any other door or landmark.
   Keep the three established ceiling lights visible in spatial perspective.
10. `FAR-CORNER LATERAL WIDE`: camera tucked into the rear-right corner beside
    the rainbow tunnel, looking laterally across the room toward the rear-left
    tent and diagonally past the shell nook. The tunnel edge and blocks are near
    foreground, the shell nook is midground, and tent, left basket and entrance
    lane recede. Strong layered occlusion and converging floor lines; preserve
    both baskets where physically visible and keep exactly three ceiling lights.

Each call appended one corresponding camera suffix to the shared prompt.
`P09` additionally authorized the single matching entrance doorway described in
the spatial continuity locks. Native source hashes are preserved by the package
inventory beside the normalized authority hashes.
