# Living-World Stage Audit — 2026-07-27

## Result and source of truth

The repository contains **111 distinct playable or substantially authored
stage/area presentations**. Every row below has **exactly two new quiet
continuous animations (A1/A2) and one new idle-only event (I)**. Existing
motion was inspected, but is not used to reduce that 2+1 completion floor.

The machine-readable source of truth is
`scripts/living_world_catalog.gd:LivingWorldCatalog.build()`. Runtime selection
and true-idle handling are in
`scripts/living_world.gd:LivingWorldDirector`. The single bounded renderer is
`scripts/living_world_canvas.gd:LivingWorldCanvas`, mounted at the exact node
path `ReefMain/LivingWorldLayer/LivingWorldCanvas`.

`scripts/main.gd` owns every mutable field prefixed `living_`, calls
`LivingWorldDirector.note_input()` at the beginning of `_input()`, calls
`note_activity()` from `_on_touch_world()` and `_on_touch_manual_move()`, and
calls `tick()` before the early returns in `_process()`. This means the intro,
kart, overlays, touch UI, held virtual stick, keyboard, mapped or raw
controller, and interactions all share the same reset contract.
The existing `scripts/interaction_director.gd` and
`scripts/tap_move_director.gd` paths remain intact; this pass observes their
input callbacks without replacing or duplicating their touch interactions.

| Group | Distinct stages |
|---|---:|
| Storybook entry | 1 |
| Reef districts | 6 |
| Current Sky Lagoon promenade | 3 |
| Substantially authored legacy Sky Lagoon | 8 |
| Northern Kingdom | 7 |
| Pearl Castle interior | 21 |
| Full-screen activity spaces | 6 |
| World minigames | 12 |
| Picture games | 4 |
| Dance | 1 |
| Kart | 2 |
| Galaxy | 2 |
| Standalone combat | 2 |
| Stuffie arena | 1 |
| Ember planet | 1 |
| Ice dungeon rooms | 10 |
| Ember dungeon rooms | 6 |
| Opera lobby floors | 3 |
| Opera acts | 15 |
| **Total** | **111** |

## Per-stage inventory and completed work

“Live” means reachable in the present normal flow. “Authored legacy” means the
area remains substantially designed and its resolver works whenever the
legacy `level2` courtyard phase is rebuilt, although the current entry route
selects the painted promenade first.

### Entry and reef

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `intro.storybook` — Live | Illustrated story pages, page frame, corner decoration | `scripts/main.gd:_build_intro`; `scripts/intro_overlay.gd` | A1 corner bubbles breathe; A2 page-star turns; I a moon peeks over the page edge |
| `reef.pearl_plaza` — Live | Shell gardens, barrel sponges, pearl-shop ship, central plaza | `scripts/reef_districts.gd:REGION_CENTERS.pearl`, `build_macro_structures()`, `build_flora()` | A1 shell bubbles rise; A2 shop-shell glints breathe; I a tiny plaza fish crosses |
| `reef.kelp_gardens` — Live | Norwegian kelp threshold, lantern pods, cold-water kelp aisles | `scripts/reef_districts.gd:REGION_CENTERS.kelp`, `build_groves()`, `build_flora()` | A1 kelp frond leans; A2 pod bubbles drift; I a leaf-fish peeks out |
| `reef.wreck_canyon` — Live | Broken ship, treasure debris, diagonal ravine shoulders | `scripts/reef_districts.gd:REGION_CENTERS.wreck`, `build_macro_structures()` | A1 wreck dust drifts; A2 loose frond rocks; I a curious fish loops past |
| `reef.moon_pool` — Live | Eroded moon-shell arch, pearl nest, anemone bowl | `scripts/reef_districts.gd:REGION_CENTERS.moon`, `build_macro_structures()`, `build_flora()` | A1 moon-shell shimmer; A2 anemone sway; I a crescent glint rises |
| `reef.rainbow_bazaar` — Live | Race gateway, coral bouquets, starfish flats | `scripts/reef_districts.gd:REGION_CENTERS.rainbow`, `build_flora()` | A1 coral tips nod; A2 gateway ribbons drift; I a rainbow fish passes |
| `reef.ice_shelf` — Live | Fjord crystal hummocks, frozen-current sheets, cold-water benthos | `scripts/reef_districts.gd:REGION_CENTERS.ice`, `build_macro_structures()`, `build_flora()` | A1 snow crystals turn; A2 current ripples pulse; I one facet softly blooms |

The Caribbean and Norwegian kingdom routes are ecosystem ownership/entry
variants over these six persistent districts; they do not create duplicate
stages.

### Sky Lagoon

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `sky.promenade_runway` — Live | Painted shore, Day One pearl plane, and one drifting cloud card | `scripts/arena/sky_lagoon_promenade.gd:_build_runway_screen()`, `_build_ambient_life()`; route x `< -25` | A1 plane gently bobs; A2 water remains painted into the cohesive plate; I one cloud crosses the clear sky corridor |
| `sky.promenade_playground` — Live | Painted lawn, enlarged slide, single-seat mermaid swing, and low seesaw | `scripts/arena/sky_lagoon_promenade.gd:_build_playground_screen()`, `_build_ambient_life()`; route x `[-25,25)` | A1 swing pumps with Roshan's two-hand pose; A2 slide has five tail-bounce steps; I the seesaw rocks on activation |
| `sky.promenade_castle` — Live | Castle approach and full stained-glass drawbridge card, with one PNW tree card | `scripts/arena/sky_lagoon_promenade.gd:_build_castle_screen()`, `_build_ambient_life()`; route x `>= 25` | A1 the castle-side tree sways; A2 the single cloud continues across the shared sky; I the stained-glass door highlights on first press |
| `sky.gatehouse` — Authored legacy | Courtyard gatehouse, two ocean-kingdom gates and runes | `scripts/arena/sky_lagoon.gd:_build_ocean_kingdom_gates()`; local z `>145` | A1 water rings spread; A2 shell ornaments shimmer; I a star bubble rises |
| `sky.courtyard` — Authored legacy | Rolling meadow, rivers, path, lanterns, trees, main courtyard | `scripts/arena/sky_lagoon.gd:_build_lagoon_terrain()`, `_build_pearl_castle()` | A1 flowers move; A2 clouds drift; I a distant fish crosses |
| `sky.playground` — Authored legacy | East playground toys and their open lawn | `scripts/arena/sky_lagoon.gd:_build_pearl_castle()`; `ReefMain.g.toys` | A1 pennants wave; A2 flowers nod; I a toy ribbon hops |
| `sky.fairy_pond` — Authored legacy | Pond, reeds/flowers, fairy dressing | `scripts/arena/sky_lagoon.gd:_build_fairy_pond()` | A1 pond rings spread; A2 flowers rock; I a butterfly circles once |
| `sky.castle_exterior` — Authored legacy | Pearl towers, banners, main door, moat and hidden back hatch | `scripts/arena/sky_lagoon.gd:_build_pearl_castle()`; `g.entry`, `g.back_entry` | A1 tower glints breathe; A2 flags move; I a crown glimmer rises |
| `sky.rainbow_junction` — Authored legacy | Rainbow kart legs, Butterfly gateway, Ember gateway, opera door | `scripts/arena/sky_lagoon.gd:_build_pearl_castle()`; `kart_legA/B`, `bw_portal_pos`, `ember_portal_pos` | A1 opposing ribbons drift; A2 portal stars pulse; I a fish slips between gates |
| `sky.alpine_village` — Authored legacy | Three chalets, square, decorated tree, snowfield, pines | `scripts/arena/sky_lagoon.gd:_build_christmas_village()`; `g.alpine_village_center` | A1 snow turns; A2 windows breathe; I chimney steam rises |
| `sky.alpine_mountain` — Authored legacy | Toy-Alps crags, snowfield, magic cave entrance/room | `scripts/arena/sky_lagoon.gd:_build_alpine_mountain()`, `_build_alpine_snowfield()`; `g.alpine_mountain_center` | A1 snow falls; A2 cave crystals shimmer; I a cave star orbits once |

The promenade’s existing fir/currant sway, cloud wrap and plane bob were
verified in `_tick_ambient_life()`. The added A1/A2 remain additional coverage.
Day/night dressing is a reusable visual variant, not another map.

### Northern Kingdom

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `north.mountain_pass` — Live | Fjords, mountain pass, backdrop peaks, waterfall approach | `scripts/arena/northern_kingdom.gd:_build_fjords()`, `_build_mountain_pass()`; `PASS_LOCAL` | A1 snow drifts; A2 fjord rings spread; I a cloud crosses the peaks |
| `north.magic_forest` — Live | Dense forest, stream, waterfall/pond, POI chain, wisp trail | `scripts/arena/northern_kingdom.gd:_build_magic_forest()`, `_build_forest_pois()` | A1 leaves sway; A2 wisps shimmer; I a mushroom peeks out |
| `north.spirit_clearing_a` — Live | Rose-tinted standing-stone ring, altar and heart mote | `scripts/arena/northern_kingdom.gd:_build_spirit_clearings()`; `CLEARING_A` | A1 rose motes orbit; A2 leaves rock; I the altar heart rises |
| `north.spirit_clearing_b` — Live | Frost-tinted standing-stone ring, altar and heart mote | `scripts/arena/northern_kingdom.gd:_build_spirit_clearings()`; `CLEARING_B` | A1 blue motes orbit; A2 cool mist ripples; I one snow crystal circles |
| `north.riverside_town` — Live | Houses, river, bridges, mill island and water wheel | `scripts/arena/northern_kingdom.gd:_build_town()`, `_build_mill()`; `TOWN_LOCAL` | A1 mill water ripples; A2 chimney steam curls; I a mill pennant waves |
| `north.ice_castle_exterior` — Live | Frozen fountain forecourt, keep, walls and roofs | `scripts/arena/northern_kingdom.gd:_build_castle()`; `CASTLE_LOCAL` | A1 crystals alternate; A2 snow settles; I a crown glint crosses |
| `north.grand_hall` — Live | Ice centerpiece, chandeliers, stairs, mezzanine, bedrooms, thrones | `scripts/arena/northern_kingdom.gd:_build_grand_hall()`; `g.north_hall_center` | A1 hall crystals breathe; A2 banners move; I a snow-star descends |

Existing wisp, leaf, mill-wheel and chandelier motion was verified in
`NorthernKingdom.tick()` and remains separate from the new 2+1 layer.

### Pearl Castle interior

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `castle.grand_hall` — Live | Throne, treasure, chandeliers, stairs, portraits and hall furniture | `scripts/arena/castle_hall.gd:build()` | A1 chandelier shells shimmer; A2 curtains breathe; I a crown glides over the throne |
| `castle.music_room` — Live | Seven-key swim xylophone, star bells, song star, opera gate | `scripts/arena/castle_hall.gd:build_music_room()`; local center `(-43.5,0,-5)` | A1 notes drift; A2 star bells pulse; I one note bounces along the rail |
| `castle.royal_bedroom` — Live | Canopy bed, bedside table/lamp, toy chest, wardrobe/vanity | `scripts/arena/castle_hall.gd:build_bedroom()`; local center `(46,0,-17)` | A1 canopy cloth breathes; A2 lamp stars pulse; I a dream moon peeks |
| `castle.upper_star_chamber` — Live | Rear-west upper chamber and star dressing | `scripts/arena/castle_hall.gd:build_expansion()`; y `30..48`, z `<-36`, x `<0` | A1 stars turn; A2 pearl dust drifts; I one star orbits |
| `castle.upper_cloud_lounge` — Live | Rear-east upper lounge and cloud furniture | `scripts/arena/castle_hall.gd:build_expansion()`; y `30..48`, z `<-36`, x `>=0` | A1 pouf wisps rise; A2 bubbles drift; I a cloud crosses |
| `castle.upper_library` — Live | West upper shelves, books and reading furniture | `scripts/arena/castle_hall.gd:build_expansion()`; y `30..48`, x `<-35` | A1 page corners breathe; A2 shelf dust glints; I a book opens and closes |
| `castle.upper_toy_gallery` — Live | East upper displays and toy furniture | `scripts/arena/castle_hall.gd:build_expansion()`; y `30..48`, x `>35` | A1 ribbons rock; A2 display stars pulse; I a gear turns once |
| `castle.upper_gallery` — Live | Upper circulation, balcony rails and stair hub | `scripts/arena/castle_hall.gd:build_expansion()`; remaining y `30..48` | A1 banners sway; A2 rail glints travel; I a shell glint rises |
| `castle.dreaming_corridor` — Live | Five bedroom doors, shell chandeliers, pet basket, front corridor | `scripts/arena/castle_hall.gd:build_dreaming_floor()`; y `>=48`, z `>-51` | A1 chandeliers breathe; A2 dream bubbles drift; I a moon passes the doors |
| `castle.dream_huluu` — Live | Rose bed/rug, Huluu cutout, tiara keepsake | `scripts/arena/castle_hall.gd:build_dreaming_floor()`; `bedrooms[0]`, cx `-36` | A1 canopy cloth moves; A2 tiara glints; I a bedside heart rises |
| `castle.dream_daddy` — Live | Blue bed/rug, Daddy cutout, toy-chest keepsake | `scripts/arena/castle_hall.gd:build_dreaming_floor()`; `bedrooms[1]`, cx `-18` | A1 curtains breathe; A2 chest stars pulse; I a shell peeks out |
| `castle.dream_mama_baby` — Live | Lilac bed/rug, Mama/Baby cutout, cradle keepsake | `scripts/arena/castle_hall.gd:build_dreaming_floor()`; `bedrooms[2]`, cx `0` | A1 cradle ribbon rocks; A2 bubbles rise; I a moon bobs above the cradle |
| `castle.dream_kareem` — Live | Green bed/rug, Kareem cutout, star keepsake | `scripts/arena/castle_hall.gd:build_dreaming_floor()`; `bedrooms[3]`, cx `18` | A1 room stars breathe; A2 canopy sways; I the keepsake star orbits |
| `castle.dream_evie` — Live | Pearl bed/rug, Evie/Lamb-a' cutout, music-box keepsake | `scripts/arena/castle_hall.gd:build_dreaming_floor()`; `bedrooms[4]`, cx `36` | A1 notes drift; A2 window bubbles rise; I a heart-note bounces |
| `castle.undercroft` — Live | Stone undercroft behind the grand hall and basement descent | `scripts/arena/castle_hall.gd:build_expansion()`; base floor local z `>8` | A1 dust glints drift; A2 shell carvings breathe; I a shy fish peeks |
| `castle.basement_corridor` — Live | Cobble corridor, repeated shell arches/lanterns, dungeon gate | `scripts/arena/castle_hall.gd:build_basement_wing()`; local y `<-8`, center lane | A1 lanterns stagger; A2 cobble dust drifts; I a mote travels to the gate |
| `castle.pantry` — Live | Stocked shelf, jars and storage barrels | `scripts/arena/castle_hall.gd:build_basement_wing()`; local center `(-17,-18,-2)` | A1 jar highlights move; A2 barrel dust floats; I a candy rolls out and back |
| `castle.kitchen` — Live | Counter, sink, stove, soup pot, kettle, pan set, tea table | `scripts/arena/castle_hall.gd:build_basement_wing()`; local center `(17,-18,-2)` | A1 soup steam curls; A2 kettle glints breathe; I a steam heart rises |
| `castle.bubble_bath` — Live | Bathtub/water, duck, vanity, towels and tiled walls | `scripts/arena/castle_hall.gd:build_basement_wing()`; local center `(-17,-18,-28)` | A1 bath bubbles rise; A2 tub rings spread; I a heart bubble floats up |
| `castle.craft_room` — Live | Craft easel, paint rack and paper/tea table | `scripts/arena/castle_hall.gd:build_basement_wing()`; local center `(17,-18,-28)` | A1 palette glints move; A2 easel ribbons rock; I a painted star pops up |
| `castle.royal_loo` — Live hidden room | Secret privy, toilet, tile, basin water | `scripts/arena/castle_hall.gd:build_basement_wing()`, `build_toilet()`; local center about `(-30.25,-18,-28)` | A1 tile highlights breathe; A2 water rings expand; I one clean bubble rises |

### Full-screen activity spaces

These are substantial interactive presentations, not transient HUD chrome.
Their canvas layer is raised above the host overlay but remains
`MOUSE_FILTER_IGNORE`.

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `overlay.craft_studio` — Live | Fish/cat/bird canvas, palette rows, easel controls | `scripts/craft_studio.gd`; `ReefMain.craft_layer` | A1 palette spots breathe; A2 paper ribbons drift; I a painted fish swims by |
| `overlay.wardrobe` — Live | Outfit cards, mirror, wardrobe frame | `scripts/wardrobe_ui.gd`; `ReefMain.wardrobe_layer` | A1 closet ribbons sway; A2 mirror stars pulse; I a crown peeks out |
| `overlay.sticker_book` — Live | Open achievement book and sticker grid | `scripts/main.gd:_open_sticker_book()`; `ReefMain.stickers_layer` | A1 pages breathe; A2 sticker stars drift; I one sticker hops |
| `overlay.critter_book` — Live | Habitat categories, critter rows and collection stage | `scripts/collection_system.gd`; `ReefMain.collection_layer` | A1 pages breathe; A2 habitat bubbles rise; I a fish crosses a page |
| `overlay.companion_picker` — Live | Stuffie cards, color rows and selected companion preview | `scripts/companion.gd` picker build; `ReefMain.companion_layer` | A1 paw marks pulse; A2 hearts drift; I a paw peeks from a card |
| `overlay.companion_care` — Live | Tamagotchi status/choice stage plus its brief feed/bath/hug/rest presentation | `scripts/companion.gd:open_care_menu()`, `_draw_care_menu()`; `ReefMain.companion_care_layer` | A1 care bubbles rise; A2 comfort hearts pulse; I a paw peeks in |

The menu and its brief care state rebuild the same `companion_care_layer`;
they are phases of one authored presentation, not duplicate stages.

### World minigames, picture games and dance

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `minigame.fetch` — Live | Fetch field, thrown toy, Wacky/Chuck and arena dressing | `scripts/games/fetch.gd`; `scripts/main.gd:_start_game_now()` | A1 bubbles rise; A2 play ribbon rocks; I a ball-star bounces |
| `minigame.dolls` — Live | Nursery arena, sleepy dolls and return points | `scripts/games/dolls.gd`; `scripts/main.gd:_start_game_now()` | A1 nursery ribbons sway; A2 dream bubbles rise; I a moon peeks |
| `minigame.brawl` — Live | Toy castle arena, imps, partner and wave dressing | `scripts/games/fairy.gd`; `game == "brawl"` | A1 castle flags move; A2 dust glints; I a toy crown hops |
| `minigame.seek` — Live | Garden hiding places, friend and foliage | `scripts/games/seek.gd`; `scripts/main.gd:_start_game_now()` | A1 leaves sway; A2 flowers nod; I a butterfly peeks |
| `minigame.race_sunset` — Designed/probed | Sunset swim course and race markers | `scripts/games/slide_race.gd`; `game == "race"` | A1 water ripples trail; A2 flags drift; I a fish crosses |
| `minigame.shop` — Live | Manta shop, item displays and shell counter | `scripts/games/shop.gd`; `scripts/main.gd:_start_game_now()` | A1 shell highlights breathe; A2 price pearls bob; I a candy rolls out/back |
| `minigame.treasure` — Live | Secret cave, crystals, debris and treasure chest | `scripts/games/treasure.gd`; `scripts/main.gd:_start_game_now()` | A1 crystals alternate; A2 treasure dust drifts; I a shell glint rises |
| `minigame.melody` — Live | Rainbow music stage, note targets and stage dressing | `scripts/games/melody.gd`; `scripts/main.gd:_start_game_now()` | A1 notes drift; A2 ribbons rock; I a bright note bounces |
| `minigame.slide_ice` — Live | Ice slide, penguin chase and cold course props | `scripts/games/slide_race.gd`; `g.fr.theme == "ice"` | A1 snow turns; A2 speed ribbons drift; I a snow puff hops |
| `minigame.slide_rainbow` — Live | Rainbow slide, fish pickups and water course | `scripts/games/slide_race.gd`; `g.fr.theme == "rainbow"` | A1 ribbons drift; A2 bubbles rise; I a fish coasts by |
| `minigame.fairy_flight` — Live | Three scrolling pond panels, fairy avatar, flowers/motes | `scripts/games/fairy.gd`; `game == "fairyshoot"`, `g.phase == "fly"` | A1 flowers sway; A2 motes drift; I a butterfly loops once |
| `minigame.fairy_boss` — Live | Flower clearing, bud/petals and boss presentation | `scripts/games/fairy.gd`; `g.phase == "boss_*"` | A1 petals breathe; A2 motes drift; I a small bud peeks |
| `picture.snowman` — Live | Snowman roll/chase picture stage and controls | `scripts/games/picture_games.gd:start_snowman()` | A1 snow turns; A2 cold stars drift; I a crystal bounces |
| `picture.garden` — Live | Garden picture, flowers and touch targets | `scripts/games/picture_games.gd:start_garden()` | A1 leaves sway; A2 flowers nod; I a butterfly visits |
| `picture.trampoline` — Live | Trampoline picture, bounce targets and party frame | `scripts/games/picture_games.gd:start_trampoline()` | A1 ribbons float; A2 stars breathe; I one star bounces |
| `picture.xmas` — Live | Christmas picture, seasonal props and touch targets | `scripts/games/picture_games.gd:start_xmas()` | A1 snow drifts; A2 lantern light breathes; I a gift ribbon wiggles |
| `dance.rhythm_stage` — Live | Full-screen dance lanes, notes and footlights | `scripts/games/dance_engine.gd`; `DanceEngine.active` | A1 notes drift; A2 footlights pulse; I a note orbits once |

The retired `PictureGames` “slide” stub immediately delegates to the live
rainbow slide and is not double-counted.

### Kart, Galaxy, standalone combat, Stuffie and Ember planet

| ID / reachability | Existing stage inventory | Exact builder/location | Added A1; A2; idle-only I |
|---|---|---|---|
| `kart.ocean_circuit` — Live | Terrain circuit, ocean props, rails, ramps and pickups | `scripts/kart.gd:_build_track()`, `_build_ocean_props()`; `kart_ground == "terrain"` | A1 course flags wave; A2 bubbles trail; I a fish crosses beyond the rail |
| `kart.rainbow_road` — Live | Floating rainbow road, clouds/stars, ramps and gateways | `scripts/kart.gd:_build_track()`, `_build_butterfly_world()`; `kart_ground == "float"` | A1 ribbons drift; A2 stars pulse; I a cloud glides under the road |
| `galaxy.butterfly_garden` — Live | Spherical garden planet, flowers, bugs/butterflies, home ring | `scripts/galaxy.gd:_build_planet()`, `_build_decor()`; `_mode == "planet"` | A1 butterflies flutter; A2 flowers nod; I a shy butterfly visits |
| `galaxy.star_hall` — Live | Butterfly castle hall, star fixtures and ice gate | `scripts/galaxy.gd:_build_hall()`; `_mode == "hall"` | A1 stars turn; A2 cloud wisps drift; I a crystal-star orbits |
| `combat.ice_berry` — Live | Octagonal cold arena and ice swarm | `scripts/combat_arena.gd:start()`; `kind == "ice"` | A1 crystals shimmer; A2 snow drifts; I a snow-star rises |
| `combat.pepper` — Live | Octagonal warm arena and pepper guardian | `scripts/combat_arena.gd:start()`; `kind == "fire"` | A1 lantern glow breathes; A2 embers drift; I an ember curls upward |
| `stuffie.sparring_den` — Live | Safe den ring, imps/boss and companion arena | `scripts/stuffie_battle.gd:_build_arena()` | A1 pennants sway; A2 paws pulse; I a friendly heart bounces |
| `ember.fortress_planet` — Live | Volcanic sphere, charcoal fortress, vents, lava and lanterns | `scripts/ember_fortress.gd:_build_planet()`, `_build_fortress()` | A1 embers drift; A2 lanterns breathe; I a lava spark rises |

Ocean/rainbow kart direction, kart selection/countdown/podium, Stuffie ladder
rounds, Galaxy quest completion, and combat enemy phases reuse their stage and
are documented variants rather than duplicate areas. The Galaxy script’s
existing butterfly idle visit was verified; the new idle event remains a
separate director event.

### Pearl Castle ice dungeon

All ten rooms are sequenced by `scripts/dungeon_level.gd:ROOMS` and built by
`DungeonLevel` using `scripts/combat_arena.gd` or
`scripts/dungeon_puzzle_room.gd`.

| ID / reachability | Existing room inventory / exact table row | Added A1; A2; idle-only I |
|---|---|---|
| `dungeon.ice.00` — Live | Frozen Foyer; `DungeonLevel.ROOMS[0]`, ice combat ring | A1 ice facets shimmer; A2 snow drifts; I a frost star rises |
| `dungeon.ice.01` — Live | Crystal Chimes; `ROOMS[1]`, sequence crystals/pads | A1 crystal glints breathe; A2 notes drift; I one note orbits |
| `dungeon.ice.02` — Live | Frozen River; `ROOMS[2]`, path stones and river | A1 river ripples move; A2 snow drifts; I an ice glint crosses |
| `dungeon.ice.03` — Live | Popcorn Ambush; `ROOMS[3]`, spiral combat arena | A1 arena dust glints; A2 wall crystals breathe; I a harmless star bounces |
| `dungeon.ice.04` — Live | Pepper Lanterns; `ROOMS[4]`, height-order lantern puzzle | A1 lanterns breathe; A2 steam curls; I a lantern spark rises |
| `dungeon.ice.05` — Live | Turtle Gallery; `ROOMS[5]`, rotating shell statues | A1 shell highlights travel; A2 bubbles rise; I a shell glint peeks |
| `dungeon.ice.06` — Live | Claw Guardian; `ROOMS[6]`, fire guardian arena | A1 embers drift; A2 shell glints pulse; I one warm spark curls up |
| `dungeon.ice.07` — Live | Moon Rune Vault; `ROOMS[7]`, matching moon tiles | A1 moon runes breathe; A2 card stars shimmer; I a crescent orbits |
| `dungeon.ice.08` — Live | Elemental Door; `ROOMS[8]`, ice/fire copy puzzle | A1 ice/fire accents alternate; A2 door stars pulse; I a two-color star crosses |
| `dungeon.ice.09` — Live | Dragon-Turtle Throne; `ROOMS[9]`, dual boss throne | A1 throne embers drift; A2 shell highlights breathe; I a crown glint rises |

### Ember Fortress dungeon

All six rooms are defined by `scripts/ember_fortress.gd:ROOMS` and reuse the
same bounded `DungeonLevel` sequencer.

| ID / reachability | Existing room inventory / exact table row | Added A1; A2; idle-only I |
|---|---|---|
| `dungeon.ember.00` — Live | Cinder Gate Imps; `EmberFortressLevel.ROOMS[0]`, ring combat | A1 embers drift; A2 lanterns breathe; I a cinder rises |
| `dungeon.ember.01` — Live | Lava Stepping Stones; `ROOMS[1]`, path and lava | A1 lava waves move; A2 cooling crystals breathe; I steam rises once |
| `dungeon.ember.02` — Live | Ember Chimes; `ROOMS[2]`, fire-crystal sequence | A1 crystal glints breathe; A2 warm notes drift; I a note bounces |
| `dungeon.ember.03` — Live | Ash Imp Ambush; `ROOMS[3]`, spiral combat arena | A1 ash motes drift; A2 cinders rise; I an ash star hops |
| `dungeon.ember.04` — Live | Door of Fire and Ice; `ROOMS[4]`, elemental copy puzzle | A1 elements breathe; A2 door stars pulse; I a steam heart rises |
| `dungeon.ember.05` — Live | The Molten Throne; `ROOMS[5]`, dual final boss | A1 embers drift; A2 king-shell glints pulse; I a fire crown rises |

### Pearl Opera House

The lobby is built in `scripts/opera_house.gd:_build_lobby()`,
`_build_doors()` and `_build_lifts()`. Each act is selected by
`scripts/opera_house.gd:ACTS` and performed by `scripts/opera_act.gd`.

| ID / reachability | Existing stage inventory / exact location | Added A1; A2; idle-only I |
|---|---|---|
| `opera.lobby_floor_1` — Live | Lagoon Lights doors, medallion, lift landing; `FLOOR_YS[0]` | A1 curtains breathe; A2 marquee stars pulse; I a ticket ribbon crosses |
| `opera.lobby_floor_2` — Live | Starlight Balcony doors, medallion and rail; `FLOOR_YS[1]` | A1 banners sway; A2 sconces shimmer; I a moon glides behind the rail |
| `opera.lobby_floor_3` — Live | Moonbeam Gallery doors, finale medallion and lift; `FLOOR_YS[2]` | A1 curtains drift; A2 high stars breathe; I a note floats to the medallion |
| `opera.act.00` — Live | The Great Cake Show; `ACTS[0]`, kitchen/worktable/cake props | A1 steam curls; A2 frosting stars breathe; I a candy decoration bounces |
| `opera.act.01` — Live | The Missing Tiara; `ACTS[1]`, clue boxes/treasure props | A1 detective lanterns breathe; A2 tiara glints drift; I a crown peeks out |
| `opera.act.02` — Live | The Dance Recital; `ACTS[2]`, echo pads and recital stage | A1 ribbons sway; A2 footlights pulse; I a ballet ribbon orbits |
| `opera.act.03` — Live | The Candy Parade; `ACTS[3]`, candy press/parade props | A1 candies rock; A2 ribbons drift; I a candy rolls along the apron |
| `opera.act.04` — Live | The Curtain Dragon; `ACTS[4]`, boss curtains and dragon set | A1 curtains breathe; A2 warm glints pulse; I a friendly ember peeks out |
| `opera.act.05` — Live | The Plushy Checkup; `ACTS[5]`, clinic/plushy beds | A1 hearts breathe; A2 paw marks drift; I a comfort heart rises |
| `opera.act.06` — Live | The Piggy Picnic; `ACTS[6]`, picnic blanket/farm props | A1 leaves sway; A2 flowers nod; I a flower bounces in |
| `opera.act.07` — Live | The Championship Bout; `ACTS[7]`, safe show ring | A1 pennants wave; A2 footlights breathe; I a victory star bounces |
| `opera.act.08` — Live | The Magic Hat Trick; `ACTS[8]`, hats and magic props | A1 magic stars drift; A2 hat ribbons rock; I a butterfly appears |
| `opera.act.09` — Live | The Shadow Phantom; `ACTS[9]`, moonlit shadow set | A1 curtains breathe; A2 crescents travel; I a moon peeks out |
| `opera.act.10` — Live | Paint the Sunrise; `ACTS[10]`, palette/canvas/sunrise set | A1 palette spots breathe; A2 sunrise ribbons drift; I a painted star rises |
| `opera.act.11` — Live | The Bubble Rocket; `ACTS[11]`, rocket engineering set | A1 bubbles drift; A2 stars pulse; I a rocket arcs across the rafters |
| `opera.act.12` — Live | The Opera Grand Prix; `ACTS[12]`, embedded race stage | A1 flags wave; A2 course ribbons drift; I a victory star crosses |
| `opera.act.13` — Live | The Starlight Concert; `ACTS[13]`, concert/rhythm stage | A1 notes drift; A2 stars pulse; I a bright note orbits |
| `opera.act.14` — Live | The Grand Finale; `ACTS[14]`, maestro/finale stage | A1 grand curtains breathe; A2 notes drift; I a crown-star rises |

Each opera act’s backstage rescue and main performance are phases of the same
authored set and story, so each act counts once. Embedded dance or kart logic
keeps the opera act ID while that act owns the visible presentation.

## Idle, cleanup and safety contract

- Delay is deterministic per stage in the bounded range **16–22 seconds**.
- Each surprise plays once for **2.7–3.3 seconds**, then stops.
- Per-stage cooldown is **30–42 seconds**.
- Any screen touch/drag, pressed mouse interaction, keyboard press, controller
  button/axis, held movement key, held virtual stick/action, touch travel, or
  explicit world/manual-move callback resets idle time. Input also cancels an
  in-progress surprise.
- Pauses, fades, sleep/hug/finale poses, missing stages and stage exits hide
  and reset the canvas. A rebuild reconfigures the same two-node rig.
- The idle path calls no reward, objective, dialogue, save, failure, audio,
  interaction or progress API.

`scripts/probe_living_world.gd` independently checks the exact 111-ID set,
group totals, two distinct ambient contracts and one unique idle contract per
stage, dynamic source-table counts, real input resets, passive progress
snapshots, all-stage entry, repeated rebuilds, long-idle repetition bounds,
zero timer/tween/particle ownership, and exit cleanup. `scripts/ci.sh` runs it
as a trusted probe, and `.github/workflows/probes.yml` runs the same probe in
the pinned GitHub Godot environment.

## Mobile and visual audit

- Exactly one `CanvasLayer` and one `Control`; no stage-local duplication.
- No `Timer`, `Tween`, `AnimationPlayer`, particles, physics bodies, materials,
  lights or audio were added.
- Motion is deterministic analytic sine/drift math. Idle scheduling uses the
  existing main process tick and numeric state only.
- Two small low-alpha motifs sit in opposing margins; one bounded idle motif
  appears briefly. Motifs never occupy the objective card or intercept touch.
- Raster texture cost is zero and transparent overdraw is confined to three
  small code-drawn shapes. The layer is hidden during transition states.
- All new visuals are first-party runtime 2D `CanvasItem` geometry in the
  established aqua/lavender/gold pastel outline language.

## Asset and protected-content audit

No raster, audio, book, voice, friend-character or third-party asset was added,
modified, recompressed or replaced. Therefore this pass has no new asset file
requiring an `ASSET_LICENSES.md` entry. The code-drawn motifs are original
first-party program geometry. Nothing under `assets/book/`,
`assets/audio/voices/`, or `assets/characters/friends/` changed, no 3D asset
was introduced or modified, and Gabby was not reintroduced.

## Intentional non-stages

Pause, HUD/objective cards, speech/toasts, fade covers, sleep/hug/finale
cutscenes, trophy poses, loading/transport moments, kart selection/countdown/
podium phases, and one-frame transitions are transient control states rather
than playable areas. The director suspends during those states instead of
turning them into ambient stages.
