# Fable Castle item style audit — 2026-07-28

## Verdict

All 28 effective touch-item sprites now meet the subjective 4.5/5 Pearl Castle style gate. The audit found two legacy outliers—the paired Main Hall pedestal fountains—and replaced them with existing approved bubble-fountain pixels. The original fountain files remain preserved.

## Rubric

The score averages palette harmony, outline/edge language, rounded shell/pearl shape language, hand-painted texture, and room perspective/scale/function fit. A score below 4.5 is not eligible for runtime.

## Touch-item inventory

| Room | Item | Legacy | Decision | Effective | Runtime file |
|---|---|---:|---|---:|---|
| bubble_bath | bathtub | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_bubble_bath_item_bathtub.png` |
| bubble_bath | sink | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_bubble_bath_item_sink.png` |
| bubble_bath | toilet | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_bubble_bath_item_toilet.png` |
| craft_room | idea_board | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_craft_room_item_idea_board.png` |
| craft_room | paint_table | 4.6 | reuse | 4.6 | `assets/flats/castle/rooms/room_craft_room_item_paint_table.png` |
| craft_room | palette | 4.6 | reuse | 4.6 | `assets/flats/castle/rooms/room_craft_room_item_palette.png` |
| kitchen | fridge | 4.9 | reuse | 4.9 | `assets/flats/castle/rooms/room_kitchen_item_fridge.png` |
| kitchen | oven | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_kitchen_item_oven.png` |
| kitchen | pan_1 | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_kitchen_item_pan_1.png` |
| kitchen | pan_2 | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_kitchen_item_pan_2.png` |
| kitchen | pan_3 | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_kitchen_item_pan_3.png` |
| kitchen | pan_4 | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_kitchen_item_pan_4.png` |
| kitchen | sink | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_kitchen_item_sink.png` |
| library | magic_book | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_library_item_magic_book.png` |
| library | pearl_lamp | 4.6 | reuse | 4.6 | `assets/flats/castle/rooms/room_library_item_pearl_lamp.png` |
| library | pearl_table | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_library_item_pearl_table.png` |
| main_hall | fountain_left | 3.3 | replace | 4.7 | `assets/flats/castle/rooms/room_main_hall_item_fountain_left_v2.png` |
| main_hall | fountain_right | 3.3 | replace | 4.7 | `assets/flats/castle/rooms/room_main_hall_item_fountain_right_v2.png` |
| main_hall | throne | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_main_hall_item_throne.png` |
| mermaid_pool | bubble_fountain | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_mermaid_pool_item_bubble_fountain.png` |
| mermaid_pool | flower_float | 4.6 | reuse | 4.6 | `assets/flats/castle/rooms/room_mermaid_pool_item_flower_float.png` |
| mermaid_pool | waterfall | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_mermaid_pool_item_waterfall.png` |
| opera_hall | chandelier | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_opera_hall_item_chandelier.png` |
| opera_hall | curtains | 4.8 | reuse | 4.8 | `assets/flats/castle/rooms/room_opera_hall_item_curtains.png` |
| opera_hall | stage_star | 4.5 | reuse | 4.5 | `assets/flats/castle/rooms/room_opera_hall_item_stage_star.png` |
| playroom | blocks | 4.5 | reuse | 4.5 | `assets/flats/castle/rooms/room_playroom_item_blocks.png` |
| playroom | stacking_toy | 4.7 | reuse | 4.7 | `assets/flats/castle/rooms/room_playroom_item_stacking_toy.png` |
| playroom | stuffie_nook | 4.9 | reuse | 4.9 | `assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png` |

## Replacement notes

- `fountain_left_v2` is a tight-alpha extraction of the richer shell fountain already present in the approved dressed Main Hall concept. It is downsampled once to the established 1024-wide runtime scale; it is not enlarged.
- `fountain_right_v2` mirrors that same existing extraction; it does not introduce a new object design.
- `scripts/arena/castle_rooms_25d.gd` selects these two explicit textures while keeping item IDs, touch mapping, foreground-band behavior, animation, sound, and save behavior unchanged. Their Z=4.15 placement sits just ahead of Z=4.0 side dressing and avoids coplanar sorting.
- `room_main_hall_background_v2.png` repairs only the two vacated legacy-fountain silhouettes from surrounding pixels in the immutable room composite. The original clean plate is preserved. This remains a legacy 1024×576 structural plate and does not claim to pass the blocked native-2K environment gate.

## Replacement asset evidence

| File | Dimensions | SHA-256 |
|---|---:|---|
| `assets/flats/castle/rooms/room_main_hall_item_fountain_left_v2.png` | 214×182 | `8e56d9ae12fb0345c24cd35ee694652fad91d2a4c46514854d456965e182c639` |
| `assets/flats/castle/rooms/room_main_hall_item_fountain_right_v2.png` | 214×182 | `db446ec5632d095c12b5f92698dc1e530e7058a9c7b4510f2285ce7e559a5130` |
| `assets/flats/castle/rooms/room_main_hall_background_v2.png` | 1024×576 | `7962c32560873058dfd72ee9dfeb77783964f441f537562efda0d473664fe72a` |

## Foreground/depth-dressing consistency

All 16 foreground Sprite3D card files were inventoried. They are scored as eight composited room pairs because their masks divide non-overlapping source-pixel ownership; a single card (especially Craft-left) is not intended to read as a standalone prop.

| Room | Pair score | Result |
|---|---:|---|
| bubble_bath | 4.7 | PASS |
| craft_room | 4.6 | PASS |
| kitchen | 4.8 | PASS |
| library | 4.7 | PASS |
| main_hall | 4.5 | PASS |
| mermaid_pool | 4.8 | PASS |
| opera_hall | 4.8 | PASS |
| playroom | 4.8 | PASS |

## Evidence

- Machine inventory: `audit/castle_sprite3d/castle_item_style_audit.json`
- Accepted contact sheet: `audit/castle_sprite3d/castle_item_style_accepted_contact.png`
- Main Hall resting-layer proof: `audit/castle_sprite3d/main_hall_item_style_replacement_composite.png`
- Exact dimensions, alpha bounds, alpha-pixel counts, and SHA-256 hashes are recorded for every item and foreground card.
