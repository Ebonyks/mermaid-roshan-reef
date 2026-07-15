# Art Remediation Batch 03

_Working date: 2026-07-14_

This pass starts from `ART_STYLE_AUDIT.md` and targets every visible raster,
texture, card, panorama, or procedural-card family below 4/5 in the full game
inventory. The 0/5 and 1/5 search is intentionally global. The second-pass
quality gate below applies only to the new artwork generated in this batch; it
does not regrade every existing game item. Direct book art, family art,
child-owned toys, and source-derived craft creatures remain protected. A
generated PNG is not treated as a substitute for a GLB's geometry, rig,
collision, or animation contract.

## First-pass 1/5 replacements

| Original | Replacement candidate | Runtime role | Status |
|---|---|---|---|
| `assets/terrain/leaf.png` | `001_terrain_leaf_mask.png` | seagrass alpha/color mask used by `_aq_mat()` and `_sway_mat()` | generated and normalized |
| `assets/mg/k_bush2.png` | `002_mg_bush_round.png` | garden picture-game bush icon | generated and normalized |

The existing audit contains no 0/5 rows. These two candidates are review-only
until the owner approves wiring them into the runtime paths.

## Full sub-4 raster remediation set

| Candidate | Covers | Intended use |
|---|---|---|
| `003_terrain_dirt_blank` | `up_dirt_col.jpg` | blank-canvas painted dirt tile |
| `004_terrain_grass_blank` | `up_grass_col.jpg`, `grass.jpg` | blank-canvas painted grass tile |
| `005_terrain_sand_blank` | `up_sand_col.jpg` | clean painted sand tile |
| `006_terrain_snow_blank` | `up_snow_col.jpg`, `up_snowsoft_col.jpg` | clean painted snow tile |
| `007_rainbow_road_tile` | missing `up_rainbowroad_col.jpg` / stripe fallback | painted road tile |
| `008_beachball_matte` | `beachball.png` | matte toy beachball |
| `009_terrain_flower_card` | `assets/terrain/flower.png`, `flower2.png` | world-facing flower card, separate from book art |
| `010_terrain_polyp_repeat_v2` | `polyp.png` | sparse, repeat-safe coral tile |
| `011_terrain_star_detail` | `star_detail.png` | low-contrast star detail mask |
| `012_fruit_family_sheet` | four galaxy fruit skins | painted fruit family reference/atlas |
| `013_crystal_facet_sheet` | four galaxy crystal materials | painted facet material reference |
| `014_sky_lagoon_day_painted` | visible day sky presentation | painted panorama candidate |
| `015_sky_lagoon_dusk_painted` | visible dusk sky presentation | painted panorama candidate |
| `016_procedural_anemone_card` | glow-tip anemones | repeated marine card |
| `017_procedural_urchin_card` | procedural urchins | repeated marine card |
| `018_procedural_giant_fish_card` | giant silhouette fish | background ambient card |
| `019_slide_grass_card` | slide-arena grass bunch | foreground foliage card |
| `020_ui_motif_strip` | HUD panels, touch controls, sticker toast | shell/ribbon/bubble/star motif reference strip |
| `021_kart_motif_strip` | finish checker, boost strips, hazards | shell/ribbon/bubble/star race motifs |
| `022_mg_cohesive_icon_sheet` | `coal`, `flower*`, `k_flower*`, `k_pine`, `k_sprout`, `star`, `sun`, `tree`, `xtree` | picture-game icon family reference |
| `023_mg_ornament_set` | `orn1.png`-`orn5.png` | five detachable Christmas ornaments |
| `024_mg_rainbow_swatch` | `rainbow_swatch.png` | soft paint-choice control |
| `025_mg_fish_body_layer` | `fish_body.png` | craft recolor body layer |
| `026_mg_fish_fins_layer` | `fish_fins.png` | craft recolor fins layer |
| `027_mg_seed_sprout_family` | `seed.png`, `sprout.png`, `k_sprout.png` | garden growth stages |
| `028_butterfly_complete_frames` | `butterfly.png`, `galaxy/butterfly1.glb`, `butterfly2.glb` wing treatment | complete-anatomy animation/card reference |
| `029_beetle_family_cards` | galaxy beetle/ladybug skins | book-family beetle cards |
| `030_leaf_material_sheet` | nature and galaxy tropical leaf material gaps | leaf/frond reference for rebake |
| `031_castle_surface_atlas` | castle kit flags, towers, walls, gates | painted surface reference for model rebake |
| `032_furniture_surface_atlas` | bookcase, chair, table | painted surface reference for model rebake |
| `033_park_surface_atlas` | bench, fountain, hedge pieces | painted surface reference for model rebake |
| `034_ship_surface_atlas` | barrel, chest, cave rock, ghost, wreck | gentle painted surface reference for model rebake |
| `035_vehicle_livery_atlas` | motorcycle, gokart, monstertruck | matte painted livery reference for model rebake |

Existing Batch 02 candidates can be promoted into this set where they satisfy
the same role: the complete butterfly frames, beetle cards, Christmas tree and
ornament set, fish body/fins layers, flowers, sprout stages, and reward icons.

The normalized Batch 03 `final/` folder contains 44 files: 43 accepted review
outputs plus the retained rejected original coral tile for visual comparison.
The exact-role `replacement_candidates/` folder contains 54 mapped PNGs.

## Non-raster sub-4 findings

These remain audit findings, but are not safe to solve by generating a flat PNG:

- legacy kart aquatic models and Butterfly World legacy coral/rock: route to the
  existing GEN2 role paths;
- legacy character GLBs: retire from normal play or replace through the rigged
  source-faithful model pipeline;
- castle, furniture, park, ship, vehicle, and crystal GLBs: require model-aware
  material/geometry passes;
- craft creatures: preserve owner-derived identity and improve the live shader;
- rainbow shader: remove metallic/chrome response in code;
- HUD and procedural architecture: implement the approved raster motifs in the
  UI/material paths after review.

No protected source art is included in the generation queue.

## Second-pass audit of new generations

This is the quality gate for Batch 03 candidates only. A candidate passes when
it is at least 4/5 against the style guide, has a readable functional role, and
does not introduce a new composition or keying problem.

| New candidates | Score | Result |
|---|---:|---|
| `001`-`009`, `011`-`019` | 4 | Pass; suitable for owner review in their intended texture/card roles |
| `010_terrain_polyp_repeat` | 3 | Reject; too densely patterned for a phone-scale coral repeat. Superseded by `010_terrain_polyp_repeat_v2` |
| `010_terrain_polyp_repeat_v2` | 4 | Pass; sparse two- or three-form tile with calm negative space and readable cel-painted bands |
| `020`-`029` | 4 | Pass; cohesive motifs, minigame layers, complete butterflies, and beetle cards meet the second-pass threshold |
| `030`-`035` | 4 | Pass as material/reference sheets; they still require model-aware rebake before runtime use |

The original `010_terrain_polyp_repeat` is the only below-4 candidate in this
second-pass audit; its redraw now passes as `010_terrain_polyp_repeat_v2`.
Existing game assets are not being regraded or regenerated by this second-pass
rule.

## Exhaustive below-4 audit inventory

The following is the complete below-4 inventory from the current project audit.
Grouped rows retain the same grouping and score as `ART_STYLE_AUDIT.md`; every
runtime-facing asset in a grouped row is included.

### Characters and creature models

| Score | Items | Remediation |
|---:|---|---|
| 3 | `assets/characters/roshan_v3.glb`, `roshan_v2.glb` | rig/model pass; do not replace with a bitmap |
| 2 | `assets/characters/roshan.glb`, `fairy.glb`, `huluu.glb` | retire legacy normal-play paths; use preferred model or protected cutout |
| 3 | `assets/characters/lamb.glb`, `chuck_poodle_rigged.glb` | source-faithful model/material pass |
| 2 | `assets/characters/chuck_poodle.glb`, `chuck_poodle_slim.glb` | keep as fallback only |
| 3 | GEN2 `dolphin.glb`, `whale.glb`, `penguin.glb` | brighten albedo, separate local color, strengthen contour |
| 3 | GEN2 `craft_kitty*`, `craft_birdie*` | owner-derived identity; improve live shader, no auto-generated replacement |

### Cross-mode legacy aquatic paths

| Score | Items | Remediation |
|---:|---|---|
| 2 | Kart legacy coral, seaweed, shell, rock, and sand-dollar roles | route through `AQ_GEN2`/preferred GEN2 role functions |
| 2 | Kart legacy `ClownFish`, `Dory`, `Tuna`, `Carp` | route to approved creature cards/models |
| 2 | Kart legacy `SpiralShell.glb` pickup | route to GEN2 spiral shell |
| 3 | Butterfly World legacy `Coral1-6`, `Rock2` | route to GEN2 painted roles |
| 2 | Remaining direct `assets/aquatic/*.glb` fallback family | do not add new consumers; retire or route by role |

### Terrain and raster textures

| Score | Items | Candidate |
|---:|---|---|
| 3 | `up_dirt_col.jpg`, `up_grass_col.jpg`, `up_sand_col.jpg`, `up_snow_col.jpg`, `up_snowsoft_col.jpg` | `003`-`006` |
| 3 | missing `up_rainbowroad_col.jpg` / procedural stripe fallback | `007` |
| 2 | `grass.jpg` | `004` |
| 2 | `beachball.png` | `008` |
| 2 | `flower.png`, `flower2.png` | `009` |
| 1 | `leaf.png` | `001` |
| 3 | `polyp.png` | `010` |
| 3 | `star_detail.png` | `011` |
| 3 | nature and galaxy tropical leaf material stand-ins | `030` family sheets |

### Castle, furniture, park, nature, ship, galaxy, and vehicle families

| Score | Items | Remediation |
|---:|---|---|
| 3 | castle kit flags, tower pieces, walls, and gates | model-aware painted material/geometry pass |
| 3 | furniture `bookcase.glb`, `chair.glb`, `table.glb` | model-aware painted material pass |
| 3 | park `bench.glb`, `fountain.glb`, hedge pieces | model-aware painted material pass |
| 3 | nature `plant_bush.glb`, `grass_leafsLarge.glb` | rebake with `030` leaf family |
| 3 | nature cliff and rock GLBs | model-aware painted material pass or GEN2 route |
| 3 | nature flowers, mushrooms, large bush, pine | model-aware painted material pass |
| 3 | ship barrel, chest, cave rock, ghost, wreck | model-aware painted material pass; keep ghost/wreck gentle |
| 3 | galaxy crystals | `013` painted facet sheet plus material rebake |
| 2 | galaxy `butterfly1.glb`, `butterfly2.glb` | `028` complete-anatomy cards / wing rebake |
| 3 | galaxy fruit family | `012` painted family sheet |
| 3 | galaxy `beetle.glb`, `ladybug.glb` | `029` book-family beetle cards / wing-case rebake |
| 3 | galaxy tropical plants | `030` leaf family sheets / material rebake |
| 3 | vehicles `motorcycle.glb`, `gokart.glb` | model-aware livery and surface pass |
| 2 | vehicle `monstertruck.glb` | model-aware silhouette/material pass |
| 2 | rainbow paint shader | code change: remove metallic/chrome response |

### 2D minigame, sky, UI, and procedural art

| Score | Items | Candidate |
|---:|---|---|
| 2 | `fish_body.png`, `fish_fins.png` | `025`, `026` |
| 3 | `seed.png` | `027` / existing Batch 02 seed candidate |
| 3 | `butterfly.png` | `028` complete-anatomy card; preserve the runtime animation contract |
| 2 | `coal.png`, `flower.png`-`flower4.png`, `k_bush.png`, `k_flower1.png`, `k_flower2.png`, `k_pine.png`, `k_sprout.png`, `star.png`, `sun.png`, `tree.png`, `xtree.png`, `sprout.png` | `022`, plus exact candidates in `replacement_candidates/assets_mg/` |
| 1 | `k_bush2.png` | `002` |
| 2 | `orn1.png`-`orn5.png` | `023`, plus exact candidates in `replacement_candidates/assets_mg/` |
| 2 | `rainbow_swatch.png` | `024` |
| 2 | `lagoon_day_2k.hdr`, `lagoon_dusk_2k.hdr` visible presentation | `014`, `015`; retain HDR only as non-visible lighting data if needed |
| 2 | procedural glow-tip anemones and urchins | `016`, `017` |
| 2 | procedural giant fish and slide-arena grass | `018`, `019` |
| 3 | box/cylinder castle and arena architecture | model-aware pass |
| 3 | HUD panels, labels, touch controls, sticker toast | `020` motif reference plus UI implementation |
| 2 | kart finish checker, boost strips, generic hazards | `021` motif reference plus UI/material implementation |

### Protected and non-generation exceptions

All direct book art, family/friend cutouts, story scenes, the book watering can,
book carrot, friendship flower, and protected character art remain 5/5 by source
fidelity. Stuffed animals and dolls remain excluded from automatic generation.
The model/code rows above are still part of this audit; they are not silently
counted as fixed merely because a visually similar PNG exists.
