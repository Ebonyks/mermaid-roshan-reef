# Fable Handoff — Main Hall Prop Compatibility and Clearance Audit

**Date:** 2026-07-28  
**Scope:** redesigned two-screen Pearl Castle Main Hall  
**Result:** corrected composition reference; no destination-room furniture
remains around the hub entrances

## Owner-facing result

The former doorway-vignette pass is rejected. It mixed props from seven room
sets in the Main Hall and treated different world depths as permission to
project objects across entrance approaches.

The corrected screens use one hub vocabulary:

- lavender castle architecture, cream/gold columns, chandeliers, banners, and
  shell wall lamps;
- Main Hall coral vases and shell fountains only;
- the unchanged far-right throne and stair;
- large destination pictograms mounted above the doors;
- the omnipresent Storybook elevator as HUD, not world furniture.

No new prop design was introduced. Existing destination assets remain
unchanged in `assets/flats/castle/rooms/` and are used only inside their source
rooms.

## Compatibility decisions

| Prior hub group | Source family | Decision |
|---|---|---|
| Console, stool, books, reading chair, magic book, pearl lamp/table | Library | Remove from hub; retain in Library |
| Tea table, teapot, cups | Kitchen | Remove from hub; retain in Kitchen |
| Stage star and footlights | Opera | Remove from hub; Opera masks above the arch are sufficient |
| Blocks, stacker, stuffie basket | Playroom | Remove from hub; teddy sign above the arch is sufficient |
| Idea board, paint cart, jars, palette furniture | Craft Room | Remove from hub; palette sign above the arch is sufficient |
| Coral clusters, planters, small bubble fountain | Mermaid Pool | Remove from hub; droplet sign above the arch is sufficient |
| Towel baskets and shell chair | Bubble Bath | Remove from hub; bubble sign above the arch is sufficient |
| Large Screen B foreground fountain | Main Hall | Remove this instance because its near-depth projection covered the Stuffie approach; preserve the matching Screen A fountain |

The only retained loose groups are:

- Screen A: far-left coral vase, one between-bay shell fountain, and one
  far-foreground shell fountain;
- Screen B: far-left coral vase/pearl-table group;
- Screen B far right: throne and stair as fixed architecture.

## Door-clearance contract

The protected region is the complete corridor mouth, gold threshold, and
direct landing to the red carpet. It is measured in the 1672×941 concept
space.

| Screen | Destination | Protected rectangle `(left, top, right, bottom)` |
|---|---|---|
| A | Opera | `(749, 438, 1029, 685)` |
| A | Library | `(1187, 442, 1360, 685)` |
| A | Kitchen | `(1383, 442, 1534, 685)` |
| B | Stuffie Playroom | `(198, 440, 358, 685)` |
| B | Craft Room | `(648, 440, 805, 685)` |
| B | Mermaid Pool | `(957, 440, 1112, 685)` |
| B | Bubble Bath | `(1180, 440, 1336, 685)` |
| B | Throne stair | `(1419, 478, 1672, 685)` |

The placement audit reports zero intersections between these rectangles and
all retained loose decor. The test uses projected 2D bounds, so a nearer
Sprite3D card cannot pass merely because its world Z is different.

## Accepted review evidence

| File | Dimensions | SHA-256 |
|---|---:|---|
| `audit/castle_sprite3d/main_hall_screen_a_clear_preview.png` | 1672×941 | `69aa7e6d3c1566f493683cc6f3df092da7869bf1872bf14e39b5062b5a45444e` |
| `audit/castle_sprite3d/main_hall_screen_b_clear_preview.png` | 1672×941 | `1f5467fc24c9ceea0a2803a6aa5b1417c0d667fc10e3c252767246f5a31c34e2` |
| `audit/castle_sprite3d/main_hall_2x1_interface_concept_clear.png` | 1814×620 | `dd6d0e04b2ec3758d61a9ca40bc060804a48fbd15d6b7b7c0f0a0126a18f334d` |
| `audit/castle_sprite3d/main_hall_door_clearance_audit.png` | 1660×566 | `a7486eee89e9ea02f53b84d9d87e151f36a28c53f6674a72e8320335c8d0375f` |
| `audit/castle_sprite3d/main_hall_dressing_invariance_audit.png` | 1540×692 | `1c23ae47c382fc32323dac4eff73be329c7cc3bc2d1d3d028d69bae548e6a240` |

The previous `main_hall_screen_*_dressed_preview.png` files are preserved as
rejected comparison evidence. They must not feed the tile slicer or be shown
as the approved layout.

The reproducible audit is `tools/audit_castle_hall_dressing.py`; the complete
machine-readable record is
`audit/castle_sprite3d/main_hall_prop_compatibility_audit.json`.

The final screens are minimal composites, not full-canvas replacements.
Screen A's edit mask covers 10.81% of the pixels and Screen B's covers 24.39%.
Every pixel outside those feathered masks is byte-identical to the tightened
reference (`outside_mask_max_channel_delta: 0` for both screens).

## Runtime boundary

These 1672×941 files are composition proofs, not accepted runtime masters.
They remain below the native long-edge ≥2048 gate. Production must preserve
their 1672:941 ratio; at the minimum long edge the one-pixel-rounded size is
2048×1153. The two masters then split losslessly into eight background cards
with 1024-pixel columns and 576/577-pixel rows.

The background grid does not absorb doors, throne, props, foregrounds,
characters, or interactions. Those remain separate unshaded Sprite3D cards at
real depth. Every runtime prop placement must rerun the projected-clearance
test before acceptance.

## 2026-07-28 polish and child-foreground correction

The clear-layout screens remain the source of truth for architecture and
door placement, but the polished play previews now supersede them for visual
language:

- every navy banner uses the same open white shell, one pearl, and exactly
  three aqua wave lines; meaningless marks were removed;
- every standard destination uses the same cream scalloped medallion, gold
  rim, and thick navy outline;
- the double-width Opera entrance keeps that language in one proportionally
  wider masks plaque;
- the Craft plaque now reads as a saturated five-color palette with a visible
  brush instead of the thin bow-like mark;
- the old baked foreground fountain on Screen A was removed only inside a
  documented mask and replaced with the existing higher-quality Main Hall
  fountain as its own depth card.

The bottom play strip now contains four child-readable touch objects per
screen: one Main Hall shell fountain, two wishing stars, and one pearl-shell
chime. These deliberately reuse a small shared Main Hall vocabulary instead
of borrowing furniture from the destination rooms. Every object has a
separate contact-shadow card, a minimum 132-pixel visual touch dimension, a
larger forgiving hit target, a no-reading animation/sound response, and zero
projected overlap with any door approach or the elevator HUD.

Node-type inventory for this correction:

| Node family | Count | Required type |
|---|---:|---|
| Touchable world props | 8 | unshaded `Sprite3D` |
| Contact shadows | 8 | unshaded `Sprite3D` |
| Omnipresent elevator control | 1 reusable instance per view | `Control` HUD |
| New `Sprite2D`, `AnimatedSprite2D`, `TextureRect`, `Polygon2D`, model, GLB, or mesh world art | 0 | prohibited |

The exact placements, Z values, hit rectangles, animation hooks, sound hooks,
source files, node types, hashes, and clearance results are recorded in
`audit/castle_sprite3d/main_hall_polish_interaction_manifest.json`.
`tools/build_castle_hall_polish_interactions.py` reproduces the masked polish,
interaction layers, full-resolution previews, and review board.

| Accepted composition evidence | Dimensions | SHA-256 |
|---|---:|---|
| `audit/castle_sprite3d/main_hall_screen_a_fullres_play_preview.png` | 1672×941 | `d4604e079e379024245ccac06f50bcb2bead3e842ada002a7b88ebf59280534c` |
| `audit/castle_sprite3d/main_hall_screen_b_fullres_play_preview.png` | 1672×941 | `3dfd3efb91c017760f3e983c5c0593186fddda4665dfb46c4a3fe1b9a3c2499b` |
| `audit/castle_sprite3d/main_hall_polish_interaction_audit.png` | 1660×565 | `188903bb084274fa862d77ab72dea41c053db350cd39c1ecead1d1510a397849` |

The review board places the two views side by side for comparison. It is not
a source image. The two individual preview files above retain the complete
1672×941 reference pixels and must be reviewed individually when judging
resolution.

Screen A changes only inside the union of its sign-polish and old-fountain
cleanup masks (19.9446% of the canvas). Screen B changes only inside its sign
polish mask (16.0820%). Every pixel outside those allowed masks is exact
relative to the accepted clear screen, with maximum channel delta 0.

Accepted edit generator paths:

- Screen A sign polish:
  `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_QQYv0wEGH8jaBy4ovIe5qKch.png`
- Screen B sign polish:
  `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_wVSgrwXyhKfXqyuAz9nU4uQW.png`
- Screen A foreground fountain removal:
  `C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_j5lATVWphekpgw0QNrcSai86.png`

These remain composition proofs below the native long-edge ≥2048 gate. They
must not be resized, tiled, imported, or used by the runtime. Production must
regenerate the accepted polished bases natively at the preserved 1672:941
ratio (minimum one-pixel-rounded target 2048×1153), then reconstruct the
foreground play strip from the independent Sprite3D cards listed in the
manifest.

## Room-led visual-polish supersession — 2026-07-28

The projected clearance results and node-type inventory above remain valid.
The full-resolution play previews no longer represent the accepted visual
finish. Their repeated lavender wall module, compressed value range, and
equally spaced foreground objects do not match the quality or density of the
finished Castle rooms.

The wishing-star/fountain/chime row is specifically rejected as a final
foreground composition. It is retained only as mechanical evidence that
large Sprite3D touch targets can clear the entrances and HUD. The replacement
uses two or three asymmetric activity islands per screen, with one large
primary target per island and open movement between groups.

The Main Hall remains a single coherent asset family. “Room-led” means using
the rooms' shared shell architecture, palette, material variety, round prop
scale, and depth rhythm. It does not permit moving destination furniture into
the hub or pasting room images into doorways.

See `FABLE_CASTLE_VISUAL_POLISH_INTERVENTION_2026-07-28.md` and
`audit/castle_sprite3d/castle_room_led_reference_board.png`.
