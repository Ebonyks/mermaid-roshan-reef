# Fable Handoff — Pearl Castle Exact-Ratio Native-2K Regeneration

**Owner amendment date:** 2026-07-26  
**Scope:** eight accessible Pearl Castle room/environment sources and their
runtime Sprite3D layers  
**Status:** blocked at the built-in generator's native-long-edge gate; no
native-2K asset accepted and no rejected generated environment feeds runtime.
The separate 4.5/5 item-style pass selects a same-source repaired legacy Main
Hall clean plate and two replacement fountain cards; it does not satisfy or
bypass this environment-master gate.

## Binding output contract

For each room:

1. Preserve the approved 1024×576 composite unchanged as the reference.
2. Regenerate the complete room from that reference at the exact approved
   aspect ratio with a native long edge of at least 2048 pixels. All eight
   castle references are exactly 16:9, so the smallest conforming canvas is
   2048×1152. A larger exact-16:9 canvas is also valid within one-pixel
   rounding tolerance.
3. Do not enlarge, interpolate, AI-upscale, pad, extend the canvas, letterbox,
   crop, or otherwise transform the lower-resolution raster to satisfy the
   size gate. Render the replacement natively.
4. Change resolution/detail fidelity only. Preserve composition, viewpoint,
   camera height/lens, palette, lighting, object identities/counts/shapes and
   placement, silhouettes, negative space, navigation lane, interaction
   sockets, and semantic depth boundaries.
5. Reject any output whose decoded long edge is below 2048 or whose ratio
   differs from the approved reference by more than one pixel of rounding,
   even when the visual result is good. A 1774×887 result remains rejected.
6. Preserve every rejected or accepted generator record: decoded dimensions,
   SHA-256, generator path, exact prompt, reference path/hash, and review
   result.
7. Run visual and programmatic invariance checks before acceptance. Only the
   accepted native-2K file may feed a runtime `Sprite3D`.

Do not force 2:1, square, portrait, POT, or 16:9 unless it is the approved
source ratio. Master files do not need to be power-of-two.

## Runtime organization after acceptance

The accepted exact-ratio master becomes the sole source for rebuilding:

- one opaque exact-ratio clean architecture master;
- mutually exclusive item, midground, and foreground layer masters;
- lossless, non-overlapping runtime tiles whenever a master or layer violates
  the repository's runtime texture-size/POT rule;
- adjacent unshaded `Sprite3D` cards that reconstruct each tiled layer
  seam-free at one coherent authored Z.

The full accepted master is preserved and never replaced by its tiles.
Every runtime tile is copied losslessly without scaling, has a longest edge no
greater than 1024 pixels, records its source rectangle and SHA-256, and shares
the layer's pixels-per-meter. Speedy-tier cost is controlled by loading only
the active room, culling invisible cards, and using import/compression controls
where valid. Resolution must not be lowered as a performance fix.

For the castle's exact-16:9 source ratio, the source plane remains
20.0×11.25 world units. A 2048×1152 master is 102.4 pixels per meter on both
axes and fills the 1280×720 Storybook UI without stretch, crop, padding,
letterbox, or canvas extension. Touch projection, walk-lane mapping, sockets,
object masks, camera parallax, tile adjacency, and seam evidence must be
reaudited against the accepted source.

### Redesigned Main Hall 2×4 background exception

The redesigned Main Hall is one 40.0×11.255980861-world-unit horizontal level
made from two separate screen masters. Its approved concept reference is
1672×941, so each production master must preserve the 1672:941 ratio and have
a native long edge of at least 2048. At the minimum width, one-pixel rounding
produces 2048×1153, not 2048×1152. Preserve both masters; do not merge them
into one ultrawide generation source. Each minimum-size screen master crops
losslessly into a 2×2 group with 1024-pixel columns and 576/577-pixel rows.
Together the eight cards form one logical two-row by four-column background
grid:

- Screen A: global columns 0 and 1;
- Screen B: global columns 2 and 3;
- tile world width: 10.0; row heights follow the actual 576/577 pixel split;
- tile-center X coordinates: -15.0, -5.0, 5.0, 15.0;
- tile-center Y coordinates: derived from the unequal lossless row heights;
- all cards: identical pixels-per-meter, unshaded, one background Z.

This subdivision lets the native high-resolution master satisfy the runtime
texture-size limit without changing the art, camera, world size, doors, props,
hotspots, or navigation. It is a lossless crop only, never an upscale or a
source of additional detail. Reproduce it with
`tools/slice_castle_hall_2x4.py` and require pixel-exact reconstruction before
runtime acceptance. The remaining individual rooms keep their 20.0×11.25
source planes and use only the tile count required by their accepted masters.

The 2026-07-28 prop-compatibility amendment also changes the approved Main
Hall composition reference. Use
`audit/castle_sprite3d/main_hall_screen_a_clear_preview.png` and
`main_hall_screen_b_clear_preview.png`, both 1672×941, as the two composition
references. The older `*_dressed_preview.png` files are rejected because they
mix destination-room item families in the hub and obstruct projected doorway
approaches. The cleanup creates no replacement props: destination furniture
returns to its source room, while the large above-door symbols carry room
identity. Exact hashes, generator paths, removal decisions, and protected
rectangles are recorded in
`audit/castle_sprite3d/main_hall_prop_compatibility_audit.json`.

## Preserved approved references

| Room source | Dimensions | SHA-256 |
|---|---:|---|
| `assets/flats/castle/rooms/room_main_hall.png` | 1024×576 | `7b284cd4530faf38ee8b06e3613f5c81dddf40fc73a64aaf943496c98acfe1a0` |
| `assets/flats/castle/rooms/room_opera_hall.png` | 1024×576 | `5878289852a911c50714aecddce1e9e63702425f3376e92205315e19a52c20cf` |
| `assets/flats/castle/rooms/room_kitchen.png` | 1024×576 | `ea92418db28e8aa5a769cf085e8a843d51d3ae5e92be37c4d51447a1812d6738` |
| `assets/flats/castle/rooms/room_library.png` | 1024×576 | `e285f03aa260f9ad3586a5bea75935b98edc99324e14d704d2542bdd97e8570d` |
| `assets/flats/castle/rooms/room_playroom.png` | 1024×576 | `5c7797c3be3586daca648f4fa4ab1161368f1c99fee719b42ba5efd27f5eaf6f` |
| `assets/flats/castle/rooms/room_craft_room.png` | 1024×576 | `916522a6fab6691866e8ff768056a5725bfbb76044dba869935eb7b585420eae` |
| `assets/flats/castle/rooms/room_mermaid_pool.png` | 1024×576 | `4ed0f6ce0fb79c35cb55f9c18c56518252df1a8e478de1ef8c06d3cf4a9e0e0d` |
| `assets/flats/castle/rooms/room_bubble_bath.png` | 1024×576 | `3ecd80b1be8444ae924e4fc05c86129d4ee3742e6708c3c3e38b84862e7bf4da` |

## Dimension-gate attempt log

Both attempts used the built-in image-generation edit path with the approved
Main Hall PNG as the sole reference. Neither output was copied into the
project. The original generator files remain under Codex's generated-image
store.

| Attempt | Generator path | Decoded output | SHA-256 | Result |
|---|---|---:|---|---|
| Main Hall A | `builtin:image_gen.imagegen` | 1774×887 RGB | `54fc467b6af905d91d1bcfb35366951b0d7542b6b499eaca1966db999d102a2e` | Rejected: long edge below 2048 and 2:1 ratio differs from the approved 16:9 |
| Main Hall B | `builtin:image_gen.imagegen` | 1774×887 RGB | `e32eb829c577d3c67abdd937f73ded5922bc4a2515cd45f2c7c8c76bdc7a8a02` | Rejected: long edge below 2048 and repeated the wrong 2:1 ratio |
| Main Hall C | `builtin:image_gen.imagegen` | 1672×941 RGB | `711fe5811ffce1b595400b995aa040a90af9998b3225d788a352d26313cd8ae4` | Rejected: ratio is within 0.5-pixel rounding tolerance, but long edge is below 2048 |

Visual review found both rejected results broadly preserved the pastel room,
central axis, navigation lane, and landmark layout. They also changed small
portrait/furnishing details, so they would still require invariance review
after passing the dimension gate. Programmatic invariance scoring was not run:
native long-edge and exact-ratio validation is the first gate and failed. The
fixed-size prompts below are retained verbatim as rejected historical records;
they were written under the superseded rule and must not be reused.

### Attempt A exact prompt

```text
Use case: stylized-concept
Asset type: native 2K game-environment source composite for later Sprite3D card extraction
Input images: Image 1 is the approved Main Hall edit target and the sole visual reference.
Primary request: Re-render Image 1 natively as an exact 2048x1024 landscape raster. This is a strict resolution and detail-fidelity pass only, not an enlargement, interpolation, AI upscale, crop, or padded version of Image 1.
Style/medium: preserve exactly the same pastel hand-painted storybook illustration style, line quality, material rendering, and level of stylization.
Composition/framing: preserve the same straight-on viewpoint, camera height, perspective, central staircase and throne axis, normalized landmark positions, silhouettes, negative space, open lower-middle navigation lane, and front/mid/back depth boundaries. Author the complete 2:1 canvas natively; keep all existing landmarks visible and do not use borders or padding.
Lighting/color: preserve the existing lavender stone palette, warm cream columns and gold trim, soft even indoor lighting, shadow directions, and contrast.
Object invariants: preserve every existing object identity, count, shape, relative scale, and placement, including throne, red carpet and stairs, upper balcony, all columns, two side doors, two shell fountains, chandeliers, banners, wall lamps, and side furnishings.
Constraints: add nothing, remove nothing, redesign nothing, move nothing semantically, and change no story or gameplay affordance. No characters, text, labels, logos, watermark, frame, border, or empty padding. Output must be exactly 2048x1024 pixels and natively generated at that resolution.
```

### Attempt B exact prompt

```text
Use case: stylized-concept
Asset type: native-resolution game environment source composite
Input images: Image 1 is the approved Main Hall edit target and the sole visual reference.
Primary request: Generate a fresh native raster whose file canvas is EXACTLY 2048 pixels wide and EXACTLY 1024 pixels tall. The prior attempt returned 1774x887 and is rejected. Do not return 1774x887, 1792x896, 1536x1024, or any other size. Do not resize, resample, interpolate, upscale, crop, pad, letterbox, or border Image 1; render the scene from scratch directly on a native 2048x1024 canvas.
Style/medium: preserve exactly the same pastel hand-painted storybook illustration style, line quality, material rendering, and level of stylization.
Composition/framing: preserve the same straight-on viewpoint, camera height, perspective, central staircase and throne axis, normalized landmark positions, silhouettes, negative space, open lower-middle navigation lane, and front/mid/back depth boundaries. Author the complete 2:1 canvas natively with all landmarks visible.
Lighting/color: preserve the lavender stone palette, warm cream columns and gold trim, soft even indoor lighting, shadow directions, and contrast.
Object invariants: preserve every existing object identity, count, shape, relative scale, and placement, including throne, red carpet and stairs, upper balcony, all columns, two side doors, two shell fountains, chandeliers, banners, wall lamps, and side furnishings.
Constraints: resolution-only/detail-fidelity pass. Add nothing, remove nothing, redesign nothing, and change no gameplay affordance. No characters, text, labels, logos, watermark, frame, border, empty padding, or letterboxing. REQUIRED OUTPUT FILE DIMENSIONS: 2048x1024 exactly.
```

### Attempt C exact prompt

```text
Use case: stylized-concept
Asset type: native-resolution game-environment master for later lossless Sprite3D card extraction
Input image: Image 1 is the approved Main Hall edit target and the sole visual reference.
Primary request: Re-render Image 1 natively with an exact 16:9 decoded PNG canvas whose long edge is at least 2048 pixels. Target exactly 2048 pixels wide by 1152 pixels tall. This is a strict native-resolution and detail-fidelity pass only. It must not be an enlargement, interpolation, resampling, AI upscale, crop, pad, canvas extension, letterbox, border, or transformation of the low-resolution raster.
Style/medium: preserve exactly the same pastel hand-painted storybook illustration style, pre-drawn line work, material rendering, palette, and level of stylization.
Composition/framing: preserve the complete existing 16:9 composition exactly—the same straight-on viewpoint, camera height and lens, central staircase and throne axis, normalized landmark positions, silhouettes, negative space, open lower-middle navigation lane, interaction sockets, and front/mid/back depth boundaries. Keep every landmark fully visible in the same relative place. Do not crop, extend, fill, or reframe any edge.
Lighting/color: preserve the existing lavender stone palette, warm cream columns and gold trim, soft even indoor lighting, shadow directions, and contrast.
Object invariants: preserve every existing object identity, count, shape, relative scale, orientation, and placement, including the throne, red carpet and stairs, upper balcony, all columns, two side doors, two shell fountains, chandeliers, banners, wall lamps, and side furnishings.
Constraints: add nothing, remove nothing, redesign nothing, move nothing semantically, and change no story or gameplay affordance. No characters beyond the existing throne portrait, no new portraits, text, labels, logos, watermark, frame, border, empty padding, or letterboxing. REQUIRED DECODED OUTPUT: exactly 2048x1152 pixels (16:9), natively rendered at that resolution.
```

## Acceptance evidence required per room

### Programmatic

- decoded long edge is at least 2048 pixels;
- decoded aspect ratio matches the approved reference within the recorded
  one-pixel rounding tolerance;
- source and accepted SHA-256 recorded;
- accepted file is not a byte-identical or resampled derivative of the
  low-resolution reference;
- normalized color-histogram, perceptual-hash, edge-map, and landmark-anchor
  comparisons recorded;
- navigation-lane occupancy and all interaction/depth sockets remain within
  their approved normalized tolerances;
- rebuilt layer manifest reports non-empty ownership masks, zero cross-card
  pixel ownership, and an accepted native-2K runtime path;
- each runtime tile records an exact non-overlapping source rectangle,
  dimensions no greater than 1024 pixels on either axis, and SHA-256;
- lossless tile reconstruction is byte-identical to its accepted layer master;
- runtime seam capture shows no gap, overlap, scale discontinuity, or
  filtering line between adjacent `Sprite3D` cards;
- runtime node inventory remains unshaded Sprite3D-only world art.

Resampling is permitted only inside the audit comparison calculation or
contact sheet. It may never create a runtime asset.

### Visual

Create a reference/accepted/edge-overlay contact sheet for each room and review:

- camera/viewpoint and architectural vanishing points;
- palette, illumination direction, and shadow character;
- every named prop and environmental landmark;
- silhouettes and relative scale;
- open navigation lane and UI-safe negative space;
- foreground/midground/background boundaries;
- touch-item sockets and player occlusion crossings.

Record the reviewer decision and any rejection reason. Do not repair a failed
output with paint-over, interpolation, padding, or upscale; regenerate from the
approved reference and exact prompt.

## 2x4 maximum-native cell attempt — 2026-07-28

All eight logical Main Hall cells were submitted independently through the
built-in `image_gen.imagegen` edit path at its requested maximum native
landscape resolution. Each call used the exact source cell as image 1 and its
complete dressed screen as context image 2. Every decoded PNG is 1672×941 RGB:
the 16:9 ratio is within the one-pixel rounding tolerance, but its native long
edge is 376 pixels short of the required 2048. No output was enlarged.

| Cell | Dimensions | SHA-256 | RGB MAE vs normalized source | dHash distance | Decision |
|---|---:|---|---:|---:|---|
| r0c0 | 1672×941 | `83f2d9b95cd99db37ba9f96f030e3f4d04b655473d505b0ebd6896deaf51d50f` | 18.5734 | 3/64 | reject |
| r0c1 | 1672×941 | `e1a3babc9b309b956af7cf9db907423b8a8e7350d5ad3df662047776556494e5` | 31.6635 | 15/64 | reject |
| r0c2 | 1672×941 | `4bfd66471c196b7469bee075e4d9cf0a44a2647ec11651fe280e79044c4b55c1` | 19.4743 | 5/64 | reject |
| r0c3 | 1672×941 | `dc18adb9776fad775723fa40fb645db65980b1d4c70b6486a7094c84577f622f` | 27.9637 | 15/64 | reject |
| r1c0 | 1672×941 | `6a7d0f07ff6830f7026cc6b393e51b561b021cd91a97a9fe18542e784fe279e4` | 45.9073 | 16/64 | reject |
| r1c1 | 1672×941 | `ecbba7a51902f5fe092369b6a1c981b567d20d7912cfa70b1ef32f524dfd0ff7` | 27.2586 | 20/64 | reject |
| r1c2 | 1672×941 | `ea29287f4c4e43cfa409cdef3eb2ac4b03cfb0287ea84a65c96cb8a74240eccf` | 23.8841 | 10/64 | reject |
| r1c3 | 1672×941 | `37c883e1899d22a92ced947f5c13b309e7eca5caf3a9bc3916fdc1ff12a56373` | 7.5064 | 4/64 | reject |

The independent generations also changed crop-edge architecture and object
placement. Only 2 of 10 internal seam comparisons pass the source-relative
boundary tolerance. The r1c1 candidate is an unconditional visual rejection:
it changes Roshan's identity, pose, outfit, and scale despite an explicit
preservation instruction. These failures demonstrate that generating cells
independently cannot reproduce the approved two-screen art seam-free.

Evidence:

- accepted alignment baseline reconstructed from the exact lossless crops:
  `audit/castle_sprite3d/main_hall_2x4_exact_reconstruction_screen_a.png`
  and
  `audit/castle_sprite3d/main_hall_2x4_exact_reconstruction_screen_b.png`;
  both are pixel-identical to their respective complete source screen;
- manifest:
  `audit/castle_sprite3d/main_hall_2x4_max_native_audit.json`;
- exact final prompts:
  `audit/castle_sprite3d/main_hall_2x4_max_native_prompts.md`;
- rejected native candidate contact:
  `audit/castle_sprite3d/main_hall_2x4_REJECTED_max_native_contact.png`;
- 50/50 source/candidate landmark overlays:
  `audit/castle_sprite3d/main_hall_2x4_REJECTED_invariance.png`;
- rejected independent-cell seam proof:
  `audit/castle_sprite3d/main_hall_2x4_REJECTED_independent_cell_seams.png`;
- reproducible audit:
  `tools/audit_castle_hall_max_cells.py`.

## Main Hall polish source update — 2026-07-28

The Main Hall's approved low-resolution composition sources have advanced
from the clear-layout screens to the masked polished bases:

| Source for native regeneration | Dimensions | SHA-256 |
|---|---:|---|
| `audit/castle_sprite3d/main_hall_screen_a_polished_base.png` | 1672×941 | `9644872778c7fd121699204da2aaf5aa14a81443acad56749a7507cc6eb9fa53` |
| `audit/castle_sprite3d/main_hall_screen_b_polished_base.png` | 1672×941 | `c724f36aa745cb6974a8ed01cdf31f09ba30f8e8354c1031fe0a63ae88d0fd2c` |

These sources preserve the accepted architecture and door locations while
standardizing the banner crest, door-plaque frame, and destination symbols.
Screen A also removes the old baked foreground fountain so production can
restore the existing higher-quality fountain as an independent depth card.
Every pixel outside the documented masks is exact relative to the accepted
clear layout. Exact masks, candidates, hashes, and invariance metrics are in
`audit/castle_sprite3d/main_hall_polish_interaction_manifest.json`.

The production request remains one complete native master per screen at the
same 1672:941 ratio, with decoded long edge ≥2048. The minimum
one-pixel-rounded dimensions remain 2048×1153. Do not include the foreground
fountain, wishing stars, pearl-shell chimes, contact shadows, Roshan, doors,
or elevator HUD in either regenerated background master. Reconstruct those
from independent unshaded Sprite3D cards after the accepted full master has
been losslessly tiled.

## Current blocker

The built-in path's observed maximum landscape output remains 1672×941. All
eight cell candidates therefore fail the native-long-edge gate, and their
independent composition drift also fails content invariance and seam
reconstruction. They remain audit-only files; no generated cell changed the
2x4 runtime background plan or Sprite3D wiring. The independent item-style
repair documented in `FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md` changes
only the legacy Main Hall clean plate/fountain paths and does not promote a
generated cell. Do not silently switch to a CLI/API fallback
or derive runtime tiles from a rejected output. Resume only when the built-in
path can produce a truly native exact-ratio long-edge ≥2048 result, when a
single accepted screen master can be losslessly sliced, or when the owner
explicitly authorizes a different generation path.
