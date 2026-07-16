# Art Generation Batch 02 — Functional 100-Asset Review Block

This is a review block for future model, skin, card, and texture work. It is
deliberately functional: every entry has one intended runtime role and a
placement context. These are not automatic replacements and must not overwrite
existing runtime files.

## Canonical exclusions

- Do not regenerate or restyle direct book assets. This includes the carrot,
  watering can, friendship flower, story portraits, source characters, and any
  other confirmed page-derived object. Their source fidelity is 5/5 by policy.
- Do not auto-generate stuffed animals or dolls. Those will be derived from the
  child's own toys under a separate owner-approved workflow.
- The paper-cat result from Batch 01 is rejected at 1/5 and is not a reference.
- The xmas picture game has one unadorned tree board, five detachable ornaments,
  and the protected friendship flower topper. Do not create a pre-decorated
  bulb-covered tree for this game.

## Christmas functional decision

| Runtime role | Existing code path | Batch 02 treatment |
|---|---|---|
| Empty tree placement board | `scripts/games/picture_games.gd:_mg_build_xmas()` loads `assets/mg/xtree.png` | Generate one replacement candidate for the empty board only |
| Five ornaments | `_mg_build_xmas()` loads `assets/mg/orn1.png` through `orn5.png`; `_mg_xmas_tap()` places the same item at a spot | Generate five individually readable detachable ornament sprites |
| Topper | `_mg_xmas_flower()` loads `assets/book/friendship_flower.png` | Preserve the book asset; no generated replacement |
| Snowy village pines | `scripts/arena/sky_lagoon.gd:_village_pine()` | Generate winter scenery variants without ornaments; they are not the minigame board |
| Decorated Christmas tree | No live functional consumer found | Excluded as redundant |

## 100-asset review manifest

| # | Asset | Intended role | Family |
|---:|---|---|---|
| 1 | `coral_branch_mint` | modular border reef card | immersive coral |
| 2 | `coral_branch_blush` | modular border reef card | immersive coral |
| 3 | `coral_branch_lavender` | modular reef card | immersive coral |
| 4 | `coral_mound_pink` | low reef cluster card | immersive coral |
| 5 | `coral_tube_teal` | vertical seabed prop | immersive coral |
| 6 | `coral_fan_mint` | side silhouette reef prop | immersive coral |
| 7 | `coral_fan_violet` | alternate side silhouette | immersive coral |
| 8 | `coral_soft_fingers` | rounded foreground prop | immersive coral |
| 9 | `sea_lettuce_flat` | separate foliage card | immersive coral |
| 10 | `kelp_ribbon_aqua` | tall background foliage card | immersive coral |
| 11 | `seagrass_tuft_mint` | low foreground repeat | immersive coral |
| 12 | `anemone_glow_tip` | repeated marine focal prop | immersive coral |
| 13 | `anemone_lavender` | alternate anemone prop | immersive coral |
| 14 | `anemone_striped_coral` | alternate anemone prop | immersive coral |
| 15 | `sponge_tube_cluster` | repeated vertical prop | immersive coral |
| 16 | `sponge_barrel_round` | low seabed prop | immersive coral |
| 17 | `urchin_lavender` | pickup-adjacent marine prop | marine keepsake |
| 18 | `sand_dollar_pale` | readable collectible/decal | marine keepsake |
| 19 | `shell_spiral_small` | shell pickup/decal | marine keepsake |
| 20 | `starfish_coral` | shell pickup/decal | marine keepsake |
| 21 | `fish_clown_side` | kart/reef ambient fish card | underwater creature |
| 22 | `fish_blue_gold_side` | kart/reef ambient fish card | underwater creature |
| 23 | `fish_pink_round_side` | kart/reef ambient fish card | underwater creature |
| 24 | `ray_small_side` | gentle ambient silhouette | underwater creature |
| 25 | `turtle_baby_side` | gentle ambient silhouette | underwater creature |
| 26 | `jellyfish_lilac` | slow ambient card | underwater creature |
| 27 | `shrimp_coral_side` | small ambient card | underwater creature |
| 28 | `hermit_crab_shell` | small collectible-adjacent prop | underwater creature |
| 29 | `octopus_round_side` | ambient creature card | underwater creature |
| 30 | `whale_distant_side` | distant background silhouette | underwater creature |
| 31 | `fish_school_left` | repeating background strip | underwater creature |
| 32 | `fish_school_right` | mirrored-safe alternate strip | underwater creature |
| 33 | `bubble_cluster_three` | success/ambient overlay | water effect |
| 34 | `bubble_column_segment` | vertical scene overlay | water effect |
| 35 | `marine_snow_sparse` | low-contrast repeat texture | water effect |
| 36 | `caustic_ripple_round` | water-light decal | water effect |
| 37 | `pearl_pickup_round` | reward pickup | marine keepsake |
| 38 | `shell_pickup_pink` | reward pickup | marine keepsake |
| 39 | `compass_keepsake` | treasure prop | marine keepsake |
| 40 | `anchor_keepsake` | treasure prop | marine keepsake |
| 41 | `bush_round_modular` | garden/world background prop | terrestrial plant |
| 42 | `shrub_woody_open` | garden/world prop | terrestrial plant |
| 43 | `shrub_orange_flower` | garden/world prop | terrestrial plant |
| 44 | `shrub_coral_red_flower` | garden/world prop | terrestrial plant |
| 45 | `succulent_rosette` | potted garden prop | terrestrial plant |
| 46 | `cactus_paddle_small` | potted garden prop | terrestrial plant |
| 47 | `aloe_potted` | potted garden prop | terrestrial plant |
| 48 | `snake_plant_potted` | potted garden prop | terrestrial plant |
| 49 | `tree_broadleaf_small` | village/garden scenery | terrestrial plant |
| 50 | `tree_pine_snowless` | warm-season scenery, no bulbs | terrestrial plant |
| 51 | `seedling_two_leaf` | garden growth-stage card | terrestrial plant |
| 52 | `palm_leaf_sheet` | tropical foliage card | terrestrial plant |
| 53 | `monstera_leaf_sheet` | tropical foliage card | terrestrial plant |
| 54 | `fern_frond_sheet` | tropical foliage card | terrestrial plant |
| 55 | `broadleaf_single_card` | tropical foliage card | terrestrial plant |
| 56 | `grass_tuft_tropical` | foreground foliage card | terrestrial plant |
| 57 | `mushroom_pair_soft` | garden/forest prop | terrestrial plant |
| 58 | `hedge_segment_round` | boundary scenery prop | terrestrial plant |
| 59 | `soil_patch_empty` | blank modular planting base | terrain prop |
| 60 | `pot_shadow_base` | reusable potted-plant grounding card | terrain prop |
| 61 | `xmas_tree_empty_board` | xmas minigame placement board | seasonal minigame |
| 62 | `ornament_round_purple` | detachable xmas tap target | seasonal minigame |
| 63 | `ornament_finial_rose` | detachable xmas tap target | seasonal minigame |
| 64 | `ornament_round_pearl_blue` | detachable xmas tap target | seasonal minigame |
| 65 | `ornament_star_warm_gold` | detachable xmas tap target | seasonal minigame |
| 66 | `ornament_teardrop_lavender` | detachable xmas tap target | seasonal minigame |
| 67 | `snow_cap_overlay_wide` | separate winter foliage overlay | seasonal scenery |
| 68 | `snowdrift_round_low` | snowy ground dressing | seasonal scenery |
| 69 | `snowball_small` | snowman/game prop | snowman minigame |
| 70 | `coal_piece_round` | snowman face tap target | snowman minigame |
| 71 | `scarf_blue_simple` | snowman visual accent | snowman minigame |
| 72 | `pine_snow_cap_card` | snowy village background tree | seasonal scenery |
| 73 | `winter_bare_branch` | snowy village framing prop | seasonal scenery |
| 74 | `gift_box_plain` | winter village prop | seasonal scenery |
| 75 | `winter_sparkle_fourpoint` | seasonal success overlay | seasonal scenery |
| 76 | `seed_round_icon` | garden tap target | garden minigame |
| 77 | `flower_round_pink` | garden growth result | garden minigame |
| 78 | `flower_round_orange` | garden growth result | garden minigame |
| 79 | `flower_round_lavender` | garden growth result | garden minigame |
| 80 | `flower_round_aqua` | garden growth result | garden minigame |
| 81 | `flower_round_coral` | garden growth result | garden minigame |
| 82 | `sprout_growth_stage` | garden intermediate stage | garden minigame |
| 83 | `leaf_pair_growth_stage` | garden intermediate stage | garden minigame |
| 84 | `sun_soft_round` | garden background card | garden minigame |
| 85 | `star_reward_soft` | trampoline target card | trampoline minigame |
| 86 | `rainbow_swatch_soft` | paint-choice control | craft minigame |
| 87 | `fish_body_painted` | craft recolor layer | craft minigame |
| 88 | `fish_fins_painted` | craft recolor layer | craft minigame |
| 89 | `butterfly_monarch_open_complete` | complete animation frame | butterfly family |
| 90 | `butterfly_monarch_closed_complete` | complete animation frame | butterfly family |
| 91 | `butterfly_blue_open_complete` | complete animation frame | butterfly family |
| 92 | `butterfly_blue_closed_complete` | complete animation frame | butterfly family |
| 93 | `beetle_stag_side` | garden ambient card | beetle family |
| 94 | `beetle_ladybird_side` | garden ambient card | beetle family |
| 95 | `beetle_jewel_side` | garden ambient card | beetle family |
| 96 | `reef_rock_small` | modular seabed prop | rocks/ground |
| 97 | `reef_rock_broad` | modular seabed prop | rocks/ground |
| 98 | `reef_rock_shelf` | background reef ledge card | rocks/ground |
| 99 | `water_ripple_ring` | touch/surface feedback overlay | water effect |
| 100 | `seabed_blank_aqua` | repeat-safe empty seabed card | rocks/ground |

## Prompt contract for this block

Every generated asset must be an isolated opaque subject on a flat removable
chroma key, with no cast shadow, ground patch, neighboring object, text, or
watermark. Use the book-derived motif family for anatomy and silhouette, but use
the existing game's cel-shaded translation: navy/plum contour, aqua/lavender
colored shadows, two or three broad flat value bands, restrained texture, and
phone-readable shape. All output is review-only until placed in a runtime scene.

Generated output will be copied to a versioned staging directory, normalized to
the project's 1024px maximum, alpha-validated, and documented in
`ASSET_LICENSES.md`.
