# Day One room corrections — asset provenance

Date: 2026-08-30

All source references are project-owned. Protected originals remain unchanged.

## Stuffie banner-free wall source

- Gap: the approved Playroom background bakes two personalized room banners
  into the opaque wall. Dirty-state suppression could not be achieved by
  hiding an existing node, and a code-painted rectangle did not meet the
  authored-wall quality gate.
- Reference role: appearance/layout reference only —
  `assets/flats/castle/interactions_v4/backgrounds/room_playroom_background.png`
  (`bd0baef94bad5c9257c0ab20d239513bd42ef465584fec6f012d990993ce797b`).
- Tool: OpenAI built-in ImageGen precise-object edit.
- Result identifier: `exec-e2fcc147-2979-489a-823b-8d5f7497ff2d`.
- Preserved native result:
  `playroom_banner_free_generated_source.png`, 1672×941 RGB,
  SHA-256 `e4e7a245de3724c750c1aec257166200e1e4873cabf6fa8b9f1f5326e8aea2ec`.
- Exact submitted prompt: `PLAYROOM_BANNER_EDIT_PROMPT.txt`.
- Prompt SHA-256:
  `b5506755babcf844e8a0dd04ead3ed284eeb11a843cc5657bae7b1257eda3d17`.
- Review decision: accepted only as a wall-healing source. It never replaces
  the complete approved runtime room and contributes no character, fixture,
  floor, or banner pixels.

Runtime patches were non-destructively cropped from the healed source at twice
their logical source-canvas coverage, given a narrow feathered alpha boundary,
and displayed only over the two baked-banner wall regions while the rescue is
dirty. No protected or approved original was modified.

- `assets/castle/day_one_room_corrections_2026-08-30/playroom_banner_cover_left.png`
  — 200×376 RGBA; SHA-256
  `2f63dfc876e4c7e95042af56df51ac493d00ed63dae7e41706a87c36bb8755a4`.
- `assets/castle/day_one_room_corrections_2026-08-30/playroom_banner_cover_right.png`
  — 208×376 RGBA; SHA-256
  `c24a47f6dcee1aca42bccbc8cdd5ed37a18157a5e9372e405fd5ad59d2882824`.

## Craft table alpha-clean variants

No generation was used. The approved table RGB and original runtime cards are
preserved exactly at their existing paths. The deterministic builder and hash
manifest are:

- `build_craft_table_alpha_clean.py`
- `craft_table_alpha_cleanup_manifest.json`

Method: recover RGB only from the exact approved
`assets/flats/castle/rooms/room_craft_room.png` crop; promote the existing
source-card alpha core; preserve its two-pixel antialias fringe; union only the
broad physical tabletop/body polygons already accepted in
`assets_src/castle/depth_cards/static_depth_card_refinement.json`; zero all
other alpha and hidden RGB. This repairs torn inner silhouettes without
redrawing or inventing table pixels.

- `assets/castle/day_one_room_corrections_2026-08-30/craft_table_front_left_alpha_clean.png`
  — 304×260 RGBA; SHA-256
  `7719f14fd566179f9175e3cfaea80371235aea1ba5fb6e32cda405a1b81f663c`.
- `assets/castle/day_one_room_corrections_2026-08-30/craft_table_front_right_alpha_clean.png`
  — 304×260 RGBA; SHA-256
  `0edb1e06cee535887ceea4e3e449f6bfe08d7919a806fe333b67b28ab19ef104`.

The ignored isolation sheet proves background-only, each source table, the
rejected palette duplicate, and the final two single owners:
`audit/day_one_room_transitions_v2_2026-08-29/visuals/correction_v3/art_layer_isolation/01_table_ownership_isolation.png`.
