class_name LivingWorldCatalog
extends RefCounted

# Machine-readable source of truth for the stage census. Every row names two
# quiet continuous accents and one passive-only surprise. The runtime renderer
# consumes these rows and the trusted probe audits them independently.

const EXPECTED_STAGE_COUNT := 99


static func build() -> Dictionary:
	var specs: Dictionary = {}
	_add_rows(specs, "entry", 21, [
		["intro.storybook", "Storybook Introduction", "scripts/main.gd:_build_intro; scripts/intro_overlay.gd",
			"Corner bubbles breathe beside the illustrated pages.", "bubble",
			"A tiny page-star slowly turns near the far margin.", "sparkle",
			"A shy storybook moon peeks over the bottom edge.", "moon"],
	])
	_add_rows(specs, "reef", 6, [
		["reef.pearl_plaza", "Pearl Plaza", "scripts/reef_districts.gd:REGION_CENTERS.pearl; build_macro_structures/build_flora",
			"Shell-garden bubbles rise in a slow loose pair.", "bubble",
			"Pearl-shop glints breathe at the opposite edge.", "shell",
			"A tiny plaza fish crosses the quiet foreground.", "fish"],
		["reef.kelp_gardens", "Norwegian Kelp Gardens", "scripts/reef_districts.gd:REGION_CENTERS.kelp; build_groves/build_flora",
			"A cold-water kelp frond leans with the current.", "frond",
			"Lantern-pod bubbles drift upward one at a time.", "bubble",
			"A small leaf-fish peeks from the kelp aisle.", "fish"],
		["reef.wreck_canyon", "Wreck Canyon", "scripts/reef_districts.gd:REGION_CENTERS.wreck; build_macro_structures",
			"Fine wreck dust drifts beside the ravine.", "sparkle",
			"A loose sea frond rocks near the broken ship.", "frond",
			"A curious little fish loops past the treasure debris.", "fish"],
		["reef.moon_pool", "Moon Pool Grotto", "scripts/reef_districts.gd:REGION_CENTERS.moon; build_macro_structures/build_flora",
			"The moon-shell rim gives off a slow soft shimmer.", "moon",
			"Anemone fronds sway within the quiet bowl.", "frond",
			"A crescent glint rises once from the pearl nest.", "sparkle"],
		["reef.rainbow_bazaar", "Rainbow Bazaar Flats", "scripts/reef_districts.gd:REGION_CENTERS.rainbow; build_flora",
			"Coral-bouquet tips nod in the flat current.", "flower",
			"Race-gateway ribbons drift without calling attention.", "ribbon",
			"A rainbow fish makes one gentle edge-to-edge pass.", "fish"],
		["reef.ice_shelf", "Norwegian Ice Shelf", "scripts/reef_districts.gd:REGION_CENTERS.ice; build_macro_structures/build_flora",
			"Small snow crystals turn above the fjord hummocks.", "snow",
			"Cold-current ripples pulse beside the ice sheet.", "ripple",
			"A single crystal catches light and softly blooms.", "crystal"],
	])
	_add_rows(specs, "sky_promenade", 6, [
		["sky.promenade_runway", "Sky Lagoon Promenade — Runway Shore", "scripts/arena/sky_lagoon_promenade.gd:_build_runway_screen/_build_ambient_life",
			"Painted shore firs continue their restrained sway.", "frond",
			"Pearl-plane bubbles drift near the runway edge.", "bubble",
			"A tiny cloud glides once above the pearl-plane dock.", "cloud"],
		["sky.promenade_playground", "Sky Lagoon Promenade — Playground Lawn", "scripts/arena/sky_lagoon_promenade.gd:_build_playground_screen/_build_ambient_life",
			"Flowering currant cards nod along the lawn.", "flower",
			"The painted cloud family moves almost imperceptibly.", "cloud",
			"A loose playground ribbon bounces once, then settles.", "ribbon"],
		["sky.promenade_castle", "Sky Lagoon Promenade — Castle Approach", "scripts/arena/sky_lagoon_promenade.gd:_build_castle_screen/_build_ambient_life",
			"Castle-side fir tips sway beside the mural.", "frond",
			"Pearl highlights breathe along the drawbridge margin.", "sparkle",
			"A little castle flag peeks out and gives one wave.", "flag"],
	])
	_add_rows(specs, "sky_legacy", 6, [
		["sky.gatehouse", "Sky Lagoon Ocean Gatehouse", "scripts/arena/sky_lagoon.gd:_build_ocean_kingdom_gates",
			"Gateway water rings expand softly beside the runes.", "ripple",
			"Shell ornaments shimmer at a second slow rhythm.", "shell",
			"A gate bubble carries a tiny star upward once.", "bubble"],
		["sky.courtyard", "Sky Lagoon Main Courtyard", "scripts/arena/sky_lagoon.gd:_build_lagoon_terrain/_build_pearl_castle",
			"Courtyard flower heads move in the breeze.", "flower",
			"High lagoon clouds drift along the opposite edge.", "cloud",
			"A distant pearl fish crosses behind the lawn.", "fish"],
		["sky.playground", "Sky Lagoon East Playground", "scripts/arena/sky_lagoon.gd:_build_pearl_castle; g.toys",
			"Playground pennants make a tiny continuous wave.", "flag",
			"Toy-side flowers nod independently.", "flower",
			"A loose ribbon makes one happy hop by the toys.", "ribbon"],
		["sky.fairy_pond", "Sky Lagoon Fairy Pond", "scripts/arena/sky_lagoon.gd:_build_fairy_pond",
			"Fairy-pond rings spread in a very slow cadence.", "ripple",
			"Waterside flowers rock at a second cadence.", "flower",
			"A small butterfly circles the pond edge once.", "butterfly"],
		["sky.castle_exterior", "Pearl Castle Exterior", "scripts/arena/sky_lagoon.gd:_build_pearl_castle; g.entry/g.back_entry",
			"Pearl tower glints wax and wane softly.", "sparkle",
			"Castle flags breathe in the high breeze.", "flag",
			"A crown-shaped glimmer rises over one tower.", "crown"],
		["sky.rainbow_junction", "Rainbow Junction", "scripts/arena/sky_lagoon.gd:_build_pearl_castle; kart_legA/kart_legB/bw_portal_pos/ember_portal_pos",
			"Portal ribbons drift in opposing slow arcs.", "ribbon",
			"Gateway stars pulse out of phase.", "sparkle",
			"A tiny rainbow fish slips between the quiet gateways.", "fish"],
		["sky.alpine_village", "Alpine Christmas Village", "scripts/arena/sky_lagoon.gd:_build_christmas_village",
			"Village snowflakes turn lazily at the frame edge.", "snow",
			"Warm window-lantern light breathes without flashing.", "lantern",
			"A little chimney curl rises once from a cottage.", "steam"],
		["sky.alpine_mountain", "Alpine Mountain and Magic Cave", "scripts/arena/sky_lagoon.gd:_build_alpine_mountain/_build_alpine_snowfield",
			"Mountain snow crystals drift down slowly.", "snow",
			"Magic-cave facets shimmer at a second rhythm.", "crystal",
			"A cave star peeks out, circles once, and returns.", "sparkle"],
	])
	_add_rows(specs, "north", 6, [
		["north.mountain_pass", "Northern Mountain Pass and Fjords", "scripts/arena/northern_kingdom.gd:_build_mountain_pass/_build_fjords",
			"Pass snow drifts gently beside the painted peaks.", "snow",
			"Fjord water rings expand below at long intervals.", "ripple",
			"A tiny cloud slides once between two distant peaks.", "cloud"],
		["north.magic_forest", "Northern Magic Forest", "scripts/arena/northern_kingdom.gd:_build_magic_forest/_build_forest_pois",
			"Forest leaves sway in the existing canopy breeze.", "leaf",
			"Trail wisps shimmer at a separate slow rhythm.", "sparkle",
			"A shy mushroom leans out from the undergrowth.", "mushroom"],
		["north.spirit_clearing_a", "Rose Spirit Clearing", "scripts/arena/northern_kingdom.gd:_build_spirit_clearings; CLEARING_A",
			"Rose clearing motes orbit the stone ring slowly.", "sparkle",
			"Nearby leaves rock around the open circle.", "leaf",
			"The rose altar heart rises once and settles.", "heart"],
		["north.spirit_clearing_b", "Frost Spirit Clearing", "scripts/arena/northern_kingdom.gd:_build_spirit_clearings; CLEARING_B",
			"Blue clearing motes orbit the standing stones.", "sparkle",
			"Cool mist ripples across the open floor.", "ripple",
			"A snow crystal makes one quiet circle over the altar.", "snow"],
		["north.riverside_town", "Northern Riverside Town and Mill", "scripts/arena/northern_kingdom.gd:_build_town/_build_mill",
			"Millside water ripples turn at an easy pace.", "ripple",
			"Town chimney steam curls upward continuously.", "steam",
			"A little mill pennant gives one extra wave.", "flag"],
		["north.ice_castle_exterior", "Northern Ice Castle Exterior", "scripts/arena/northern_kingdom.gd:_build_castle",
			"Ice-castle crystals catch light in alternating pulses.", "crystal",
			"Snow settles past the high walls.", "snow",
			"A tiny crown glint travels once across the battlement.", "crown"],
		["north.grand_hall", "Northern Ice Castle Grand Hall", "scripts/arena/northern_kingdom.gd:_build_grand_hall; g.north_hall_center",
			"Hall crystals breathe with soft cold light.", "crystal",
			"High banners move almost imperceptibly.", "curtain",
			"A small snow-star descends once from the mezzanine.", "snow"],
	])
	_add_castle_room_rows(specs)
	_add_rows(specs, "overlay", 19, [
		["overlay.craft_studio", "Creature Craft Studio", "scripts/craft_studio.gd; ReefMain.craft_layer",
			"Paint-palette spots breathe at the screen margin.", "paint",
			"Paper ribbons drift beside the easel panel.", "ribbon",
			"A tiny painted fish swims once along the bottom.", "fish"],
		["overlay.wardrobe", "Royal Wardrobe", "scripts/wardrobe_ui.gd; ReefMain.wardrobe_layer",
			"Closet ribbons sway beside the outfit cards.", "ribbon",
			"Mirror sparkles pulse at a second rhythm.", "sparkle",
			"A little crown peeks once from behind the wardrobe.", "crown"],
		["overlay.sticker_book", "Sticker Book", "scripts/main.gd:_open_sticker_book; ReefMain.stickers_layer",
			"Book corners breathe like gently turning pages.", "book",
			"Sticker stars drift along the outside margin.", "sparkle",
			"A tiny sticker star hops once between pages.", "sparkle"],
	])
	_add_rows(specs, "overlay", 26, [
		["overlay.critter_book", "Critter Collection Book", "scripts/collection_system.gd; ReefMain.collection_layer",
			"Collection-book pages breathe at a slow cadence.", "book",
			"Small habitat bubbles rise near the page edge.", "bubble",
			"A miniature fish crosses one open page.", "fish"],
		["overlay.companion_picker", "Stuffie Companion Picker", "scripts/companion.gd; ReefMain.companion_layer",
			"Paw marks pulse softly beside the picker.", "paw",
			"Stuffie hearts drift at a second gentle pace.", "heart",
			"A tiny paw bounces once from behind a card.", "paw"],
		["overlay.companion_care", "Stuffie Care Menu and Moment", "scripts/companion.gd:open_care_menu/_draw_care_menu; ReefMain.companion_care_layer",
			"Bath-and-care bubbles rise gently.", "bubble",
			"Comfort hearts pulse at another rhythm.", "heart",
			"A little paw peeks in once to say hello.", "paw"],
	])
	_add_rows(specs, "minigame", 6, [
		["minigame.fetch", "Wacky and Chuck Fetch Arena", "scripts/games/fetch.gd; scripts/main.gd:_start_game_now",
			"Toy-side bubbles rise behind the fetch field.", "bubble",
			"A loose play ribbon rocks at the opposite edge.", "ribbon",
			"A small ball-like sparkle makes one soft bounce.", "sparkle"],
		["minigame.dolls", "Sleepy Dolls Nursery", "scripts/games/dolls.gd; scripts/main.gd:_start_game_now",
			"Nursery ribbons sway in a sleepy rhythm.", "ribbon",
			"Dream bubbles drift upward near the dolls.", "bubble",
			"A tiny moon peeks in once, then tucks away.", "moon"],
		["minigame.brawl", "Toy Castle Brawl", "scripts/games/fairy.gd; scripts/main.gd:_start_game_now game=brawl",
			"Toy-castle flags move in the distant breeze.", "flag",
			"Soft arena dust glints at another tempo.", "sparkle",
			"A little toy crown makes one harmless hop.", "crown"],
		["minigame.seek", "Hide-and-Seek Garden", "scripts/games/seek.gd; scripts/main.gd:_start_game_now",
			"Garden leaves sway along the hiding places.", "leaf",
			"Small flowers nod independently.", "flower",
			"A butterfly peeks from one edge and slips away.", "butterfly"],
		["minigame.race_sunset", "Sunset Swim Race", "scripts/games/slide_race.gd; scripts/main.gd:_start_game_now game=race",
			"Sunset water ripples trail along the race edge.", "wave",
			"Course flags drift at a calm second rhythm.", "flag",
			"A distant fish makes one unhurried crossing.", "fish"],
		["minigame.shop", "Pearl Shop", "scripts/games/shop.gd; scripts/main.gd:_start_game_now",
			"Shop-shell highlights breathe behind the counter.", "shell",
			"Tiny price pearls bob without prompting.", "bubble",
			"A wrapped candy rolls out once and rolls back.", "candy"],
		["minigame.treasure", "Secret Cave Treasure Hunt", "scripts/games/treasure.gd; scripts/main.gd:_start_game_now",
			"Cave crystals shimmer in alternating pairs.", "crystal",
			"Fine treasure dust drifts beside the walls.", "sparkle",
			"A little shell glint rises once from the chest.", "shell"],
		["minigame.melody", "Rainbow Melody Stage", "scripts/games/melody.gd; scripts/main.gd:_start_game_now",
			"Music notes drift slowly above the stage edge.", "note",
			"Rainbow ribbons rock at a second tempo.", "ribbon",
			"A bright note bounces once across the footlights.", "note"],
		["minigame.slide_ice", "Penguin Ice Slide", "scripts/games/slide_race.gd; g.fr.theme=ice",
			"Slide snowflakes turn lazily beside the ice.", "snow",
			"Cold speed ribbons drift along the far edge.", "ribbon",
			"A baby-penguin snow puff makes one gentle hop.", "snow"],
		["minigame.slide_rainbow", "Rainbow Fish Slide", "scripts/games/slide_race.gd; g.fr.theme=rainbow",
			"Rainbow ribbons drift beside the long slide.", "ribbon",
			"Small water bubbles climb the opposite margin.", "bubble",
			"A little fish coasts once through the rainbow edge.", "fish"],
		["minigame.fairy_flight", "Fairy Pond Flight Panels", "scripts/games/fairy.gd; game=fairyshoot phase=fly",
			"Pond flowers sway below the scrolling panels.", "flower",
			"Fairy sparkles drift at a separate slow pace.", "sparkle",
			"A butterfly companion loops past once.", "butterfly"],
		["minigame.fairy_boss", "Fairy Flower Clearing", "scripts/games/fairy.gd; game=fairyshoot phase=boss_*",
			"Giant-flower petals breathe around the clearing.", "flower",
			"Magic motes drift near the quiet arena edge.", "sparkle",
			"A tiny bud peeks up once and settles safely.", "flower"],
	])
	_add_rows(specs, "picture_game", 8, [
		["picture.snowman", "Snowman Picture Game", "scripts/games/picture_games.gd:start_snowman",
			"Small snowflakes turn outside the play area.", "snow",
			"Cold sparkles drift at a second rhythm.", "sparkle",
			"A tiny snow crystal bounces once near the corner.", "snow"],
		["picture.garden", "Garden Picture Game", "scripts/games/picture_games.gd:start_garden",
			"Garden leaves sway beside the touch targets.", "leaf",
			"Flowers nod independently at the far edge.", "flower",
			"A butterfly makes one quiet visit to the margin.", "butterfly"],
		["picture.trampoline", "Trampoline Picture Game", "scripts/games/picture_games.gd:start_trampoline",
			"Party ribbons float outside the bounce area.", "ribbon",
			"Small stars breathe at the opposite edge.", "sparkle",
			"A soft star makes one trampoline-like bounce.", "sparkle"],
		["picture.xmas", "Christmas Picture Game", "scripts/games/picture_games.gd:start_xmas",
			"Snow drifts gently around the picture frame.", "snow",
			"Warm lantern light breathes at a second pace.", "lantern",
			"A tiny present-ribbon wiggles once and rests.", "ribbon"],
	])
	_add_rows(specs, "dance", 41, [
		["dance.rhythm_stage", "Rhythm Dance Stage", "scripts/games/dance_engine.gd",
			"Stage notes drift slowly outside the dance lanes.", "note",
			"Footlight stars pulse gently at another tempo.", "sparkle",
			"A little music note orbits once around the stage edge.", "note"],
	])
	_add_rows(specs, "kart", 6, [
		["kart.ocean_circuit", "Ocean Kart Circuit", "scripts/kart.gd:_build_track/_build_ocean_props; kart_ground=terrain",
			"Course flags make a restrained continuous wave.", "flag",
			"Ocean bubbles trail along the far guardrail.", "bubble",
			"A tiny fish crosses once beyond the circuit.", "fish"],
		["kart.rainbow_road", "Floating Rainbow Road", "scripts/kart.gd:_build_track/_build_butterfly_world; kart_ground=float",
			"Rainbow-road ribbons drift in the star field.", "ribbon",
			"Distant stars pulse out of phase.", "sparkle",
			"A little cloud glides once below the floating road.", "cloud"],
	])
	_add_rows(specs, "galaxy", 6, [
		["galaxy.butterfly_garden", "Butterfly Garden Planet", "scripts/galaxy.gd:_build_planet/_build_decor; _mode=planet",
			"Garden butterflies continue a slow edge flutter.", "butterfly",
			"Planet flowers nod at an independent rhythm.", "flower",
			"A shy butterfly makes one close visit, then returns.", "butterfly"],
		["galaxy.star_hall", "Butterfly Castle Star Hall", "scripts/galaxy.gd:_build_hall; _mode=hall",
			"Star-hall points rotate slowly along the margin.", "sparkle",
			"High cloud wisps drift at another pace.", "cloud",
			"A small crystal star traces one orbit above the hall.", "crystal"],
	])
	_add_rows(specs, "combat", 6, [
		["combat.ice_berry", "Ice-Berry Combat Arena", "scripts/combat_arena.gd:start kind=ice",
			"Cold crystals shimmer beyond the arena ring.", "crystal",
			"Small snow motes drift along the outer edge.", "snow",
			"A soft snow-star rises once, safely outside play.", "snow"],
		["combat.pepper", "Pepper Combat Arena", "scripts/combat_arena.gd:start kind=fire",
			"Pepper-lantern glow breathes beyond the arena.", "lantern",
			"Warm embers drift slowly at the opposite edge.", "ember",
			"A tiny ember curls upward once and disappears.", "ember"],
	])
	_add_rows(specs, "stuffie", 6, [
		["stuffie.sparring_den", "Stuffie Sparring Den", "scripts/stuffie_battle.gd:_build_arena",
			"Den pennants sway gently around the safe ring.", "flag",
			"Stuffie paw marks pulse at a second rhythm.", "paw",
			"A friendly heart bounces once at the arena edge.", "heart"],
	])
	_add_rows(specs, "ember", 6, [
		["ember.fortress_planet", "Ember Fortress Planet", "scripts/ember_fortress.gd:_build_planet/_build_fortress",
			"Far embers drift beside the charcoal fortress.", "ember",
			"Fortress lanterns breathe in a staggered rhythm.", "lantern",
			"A tiny lava spark rises once over the distant wall.", "ember"],
	])
	_add_ice_dungeon(specs)
	_add_ember_dungeon(specs)
	_add_opera_acts(specs)
	return specs


static func _add_ice_dungeon(specs: Dictionary) -> void:
	_add_rows(specs, "ice_dungeon", 6, [
		["dungeon.ice.00", "Frozen Foyer", "scripts/dungeon_level.gd:ROOMS[0]; scripts/combat_arena.gd",
			"Foyer ice facets shimmer beyond the combat ring.", "crystal",
			"Fine snow drifts at an independent pace.", "snow",
			"A tiny frost star rises once behind the room edge.", "snow"],
		["dungeon.ice.01", "Crystal Chimes", "scripts/dungeon_level.gd:ROOMS[1]; scripts/dungeon_puzzle_room.gd",
			"Crystal-note glints breathe beside the chimes.", "crystal",
			"Small notes drift outside the choice pads.", "note",
			"One crystal note makes a quiet orbit.", "note"],
		["dungeon.ice.02", "Frozen River", "scripts/dungeon_level.gd:ROOMS[2]; scripts/dungeon_puzzle_room.gd",
			"River ripples move slowly behind the path.", "ripple",
			"Snow crystals drift at another cadence.", "snow",
			"A little ice floe glint crosses once.", "crystal"],
		["dungeon.ice.03", "Popcorn Ambush", "scripts/dungeon_level.gd:ROOMS[3]; scripts/combat_arena.gd",
			"Soft arena dust sparkles outside the fight.", "sparkle",
			"Cold wall crystals breathe independently.", "crystal",
			"A harmless popcorn-like star makes one bounce.", "sparkle"],
		["dungeon.ice.04", "Pepper Lanterns", "scripts/dungeon_level.gd:ROOMS[4]; scripts/dungeon_puzzle_room.gd",
			"Pepper lanterns breathe without flashing.", "lantern",
			"Warm steam curls near the room edge.", "steam",
			"One lantern spark rises gently and fades.", "ember"],
		["dungeon.ice.05", "Turtle Gallery", "scripts/dungeon_level.gd:ROOMS[5]; scripts/dungeon_puzzle_room.gd",
			"Shell highlights move slowly along the gallery.", "shell",
			"Pearl bubbles climb at another cadence.", "bubble",
			"A tiny turtle-shell glint peeks once from the side.", "shell"],
		["dungeon.ice.06", "Claw Guardian", "scripts/dungeon_level.gd:ROOMS[6]; scripts/combat_arena.gd",
			"Warm arena embers drift beyond the safe ring.", "ember",
			"Guardian-shell glints pulse softly.", "shell",
			"A small claw-colored spark curls upward once.", "ember"],
		["dungeon.ice.07", "Moon Rune Vault", "scripts/dungeon_level.gd:ROOMS[7]; scripts/dungeon_puzzle_room.gd",
			"Moon runes breathe along the vault edge.", "moon",
			"Pair-card stars shimmer at a second pace.", "sparkle",
			"A crescent makes one slow orbit above the tiles.", "moon"],
		["dungeon.ice.08", "Elemental Door", "scripts/dungeon_level.gd:ROOMS[8]; scripts/dungeon_puzzle_room.gd",
			"Ice crystals and warm embers alternate gently.", "crystal",
			"Door-rune stars pulse at another rhythm.", "ember",
			"A two-color star crosses the door once.", "sparkle"],
		["dungeon.ice.09", "Dragon-Turtle Throne", "scripts/dungeon_level.gd:ROOMS[9]; scripts/combat_arena.gd",
			"Throne embers drift beyond the final arena.", "ember",
			"Dragon-shell highlights breathe slowly.", "shell",
			"A tiny crown glint rises once behind the throne.", "crown"],
	])


static func _add_ember_dungeon(specs: Dictionary) -> void:
	_add_rows(specs, "ember_dungeon", 6, [
		["dungeon.ember.00", "Cinder Gate Imps", "scripts/ember_fortress.gd:ROOMS[0]; scripts/combat_arena.gd",
			"Gate embers drift around the outer room.", "ember",
			"Charcoal lanterns breathe at a second pace.", "lantern",
			"A small cinder rises once and disappears.", "ember"],
		["dungeon.ember.01", "Lava Stepping Stones", "scripts/ember_fortress.gd:ROOMS[1]; scripts/dungeon_puzzle_room.gd",
			"Lava-edge waves move in a slow analytic rhythm.", "wave",
			"Cooling crystals breathe beside the path.", "crystal",
			"A tiny steam curl rises once from a stepping stone.", "steam"],
		["dungeon.ember.02", "Ember Chimes", "scripts/ember_fortress.gd:ROOMS[2]; scripts/dungeon_puzzle_room.gd",
			"Fire-crystal glints breathe beside the chimes.", "crystal",
			"Warm notes drift outside the choice pads.", "note",
			"One ember note bounces once and fades.", "note"],
		["dungeon.ember.03", "Ash Imp Ambush", "scripts/ember_fortress.gd:ROOMS[3]; scripts/combat_arena.gd",
			"Ash motes drift beyond the combat ring.", "sparkle",
			"Low cinders rise at an independent pace.", "ember",
			"A harmless ash star makes one soft hop.", "sparkle"],
		["dungeon.ember.04", "Door of Fire and Ice", "scripts/ember_fortress.gd:ROOMS[4]; scripts/dungeon_puzzle_room.gd",
			"Warm embers and cold facets breathe in balance.", "ember",
			"Elemental door stars pulse at a second rhythm.", "crystal",
			"A tiny steam heart rises once between the elements.", "heart"],
		["dungeon.ember.05", "The Molten Throne", "scripts/ember_fortress.gd:ROOMS[5]; scripts/combat_arena.gd",
			"Molten-throne embers drift outside the final ring.", "ember",
			"King-shell glints pulse slowly.", "shell",
			"A little fire crown rises once behind the throne.", "crown"],
	])


static func _add_castle_room_rows(specs: Dictionary) -> void:
	var source := "scripts/arena/castle_rooms_25d.gd:ROOMS/ROOM_ITEMS"
	# Castle's opaque picture stage owns layer 14. Ambient accents must paint
	# above it, while the phone pause control remains authoritative on layer 16.
	_add_rows(specs, "castle_room", 15, [
		["castle.room.main_hall", "Pearl Castle Main Hall", source,
			"Pearl lights breathe beside the royal doors.", "shell",
			"High banners sway at a second slow rhythm.", "flag",
			"A tiny crown glint crosses the hall once.", "crown"],
		["castle.room.opera_hall", "Pearl Castle Opera Hall", source,
			"Stage curtains breathe around the career pictures.", "curtain",
			"Footlight stars pulse softly out of phase.", "sparkle",
			"A music note floats once above the stage.", "note"],
		["castle.room.kitchen", "Pearl Castle Royal Kitchen", source,
			"Soup-pot steam curls beside the career pictures.", "steam",
			"Copper-pan glints breathe at another pace.", "sparkle",
			"A tiny candy rolls once along the counter.", "candy"],
		["castle.room.library", "Pearl Castle Royal Library", source,
			"Book corners move in the quiet room air.", "book",
			"Reading-pearl stars breathe near the table.", "sparkle",
			"A clue ribbon peeks once from a storybook.", "ribbon"],
		["castle.room.playroom", "Pearl Castle Stuffie Playroom", source,
			"Stuffie hearts breathe beside the toy nook.", "heart",
			"Play-tent ribbons rock at a second pace.", "ribbon",
			"A padded glove bounces once by the blocks.", "paw"],
		["castle.room.craft_room", "Pearl Castle Craft Room", source,
			"Palette colors shimmer beside the easel.", "paint",
			"Craft ribbons sway at a second rhythm.", "ribbon",
			"A painted star pops up once from the table.", "sparkle"],
		["castle.room.mermaid_pool", "Pearl Castle Mermaid Pool", source,
			"Pool rings spread slowly beneath the waterfall.", "ripple",
			"Floating flowers breathe at another cadence.", "flower",
			"A rocket bubble rises once from the fountain.", "bubble"],
		["castle.room.bubble_bath", "Pearl Castle Bubble Bath", source,
			"Bath bubbles rise in a gentle uneven pair.", "bubble",
			"Tub-water rings expand at a second rhythm.", "ripple",
			"A tiny bedtime moon peeks over the tub.", "moon"],
		["castle.room.family_gallery", "Pearl Castle Family Gallery", source,
			"Doorway ribbons drift along the family wing.", "ribbon",
			"Portrait stars breathe beside the room portals.", "sparkle",
			"A tiny home heart crosses the gallery once.", "heart"],
		["castle.room.dining_room", "Pearl Castle Family Dining Room", source,
			"Table highlights breathe beside the feast.", "sparkle",
			"Chandelier pearls sway at a second pace.", "shell",
			"A little farm flower rises once by a plate.", "flower"],
		["castle.room.royal_bedroom", "Pearl Castle Royal Bedroom", source,
			"Canopy cloth moves in a sleepy rhythm.", "curtain",
			"Bedside stars breathe very softly.", "sparkle",
			"A dream moon peeks over the bed once.", "moon"],
		["castle.room.sleepover_bedroom", "Pearl Castle Sleepover Bedroom", source,
			"Dream-bed ribbons rock continuously.", "ribbon",
			"Sleepy bubbles rise at another pace.", "bubble",
			"A tiny heart floats once between the beds.", "heart"],
		["castle.room.movie_lounge", "Pearl Castle Cloud Movie Lounge", source,
			"Cloud-settee wisps breathe beside the screen.", "cloud",
			"Movie-frame stars pulse at a second rhythm.", "sparkle",
			"A checkered ribbon crosses the screen once.", "flag"],
	])


static func _add_opera_acts(specs: Dictionary) -> void:
	# Career worlds own opaque layer 10; their ambient/idle accents paint above
	# that world and below the layer-12 caption HUD and layer-13 pause control.
	_add_rows(specs, "opera_act", 11, [
		["opera.act.00", "The Great Cake Show", "scripts/opera_house.gd:ACTS[0]; scripts/opera_career_world_2d.gd",
			"Cake-show steam curls beyond the worktable.", "steam",
			"Frosting sparkles breathe near the curtains.", "sparkle",
			"A tiny candy decoration bounces once across the apron.", "candy"],
		["opera.act.01", "The Missing Tiara", "scripts/opera_house.gd:ACTS[1]; scripts/opera_career_world_2d.gd",
			"Detective lanterns breathe beside the clue boxes.", "lantern",
			"Tiara glints drift at a second rhythm.", "crown",
			"A small crown peeks once from behind a prop.", "crown"],
		["opera.act.02", "The Dance Recital", "scripts/opera_house.gd:ACTS[2]; scripts/opera_career_world_2d.gd",
			"Recital ribbons sway outside the dance pads.", "ribbon",
			"Footlight stars pulse at another tempo.", "sparkle",
			"A ballet ribbon makes one gentle orbit.", "ribbon"],
		["opera.act.03", "The Candy Parade", "scripts/opera_house.gd:ACTS[3]; scripts/opera_career_world_2d.gd",
			"Wrapped candies rock beside the parade route.", "candy",
			"Parade ribbons drift at a second cadence.", "ribbon",
			"A smiley candy rolls once along the stage edge.", "candy"],
		["opera.act.05", "The Stuffie Surgeon Relay", "scripts/opera_house.gd:ACTS[5]; scripts/opera_career_world_2d.gd",
			"Sewing hearts breathe beside the stuffie stations.", "heart",
			"Soft paw patches drift at an independent pace.", "paw",
			"A little comfort patch rises once from backstage.", "heart"],
		["opera.act.06", "The Piggy Picnic", "scripts/opera_house.gd:ACTS[6]; scripts/opera_career_world_2d.gd",
			"Picnic leaves sway beyond the blanket.", "leaf",
			"Flower heads nod at another rhythm.", "flower",
			"A tiny picnic flower bounces once into view.", "flower"],
		["opera.act.07", "The Championship Bout", "scripts/opera_house.gd:ACTS[7]; scripts/opera_career_world_2d.gd",
			"Championship pennants wave outside the ring.", "flag",
			"Footlight stars breathe at a second pace.", "sparkle",
			"A friendly victory star makes one soft bounce.", "sparkle"],
		["opera.act.08", "The Magic Hat Trick", "scripts/opera_house.gd:ACTS[8]; scripts/opera_career_world_2d.gd",
			"Magic stars drift around the curtain margins.", "sparkle",
			"Hat ribbons rock at an independent rhythm.", "ribbon",
			"A tiny butterfly appears once from the stage edge.", "butterfly"],
		["opera.act.10", "Paint the Sunrise", "scripts/opera_house.gd:ACTS[10]; scripts/opera_career_world_2d.gd",
			"Paint-palette spots breathe beside the canvas.", "paint",
			"Sunrise ribbons drift at a second pace.", "ribbon",
			"A tiny painted star rises once from the palette.", "sparkle"],
		["opera.act.11", "The Bubble Rocket", "scripts/opera_house.gd:ACTS[11]; scripts/opera_career_world_2d.gd",
			"Rocket bubbles drift beyond the work area.", "bubble",
			"Distant stars pulse at an independent rhythm.", "sparkle",
			"A tiny rocket makes one quiet arc across the rafters.", "rocket"],
		["opera.act.12", "The Opera Grand Prix", "scripts/opera_house.gd:ACTS[12]; scripts/opera_career_world_2d.gd",
			"Grand-prix flags wave along the stage guardrail.", "flag",
			"Course ribbons drift at a second rhythm.", "ribbon",
			"A victory star crosses once behind the track.", "sparkle"],
		["opera.act.13", "The Starlight Concert", "scripts/opera_house.gd:ACTS[13]; scripts/opera_career_world_2d.gd",
			"Concert notes drift outside the rhythm lanes.", "note",
			"Starlight points pulse at another tempo.", "sparkle",
			"A bright note makes one orbit above the footlights.", "note"],
		["opera.act.15", "The Moonbeam Nursery", "scripts/opera_house.gd:ACTS[15]; scripts/opera_career_world_2d.gd",
			"Moon-and-star mobiles sway beside the baby cribs.", "moon",
			"Tiny dream bubbles drift at an independent pace.", "bubble",
			"A sleepy golden star settles once above the beds.", "sparkle"],
		["opera.act.16", "The Crystal Cave Discovery", "scripts/opera_house.gd:ACTS[16]; scripts/opera_career_world_2d.gd",
			"Crystal points breathe softly beyond the specimen tables.", "sparkle",
			"Cave bubbles drift at a second quiet rhythm.", "bubble",
			"One tiny fossil shell makes a gentle discovery turn.", "shell"],
	])


static func _add_rows(specs: Dictionary, group: String, canvas_layer: int, rows: Array) -> void:
	for value in rows:
		var row: Array = value
		_add(
			specs,
			String(row[0]),
			String(row[1]),
			group,
			String(row[2]),
			String(row[3]),
			String(row[4]),
			String(row[5]),
			String(row[6]),
			String(row[7]),
			String(row[8]),
			canvas_layer
		)


static func _add(specs: Dictionary, id: String, display_name: String, group: String,
		source: String, animation_a: String, motif_a: String, animation_b: String,
		motif_b: String, idle_description: String, idle_motif: String,
		canvas_layer: int) -> void:
	var seed: int = absi(int(hash(id)))
	var motions := ["peek", "rise", "cross", "orbit", "bounce", "burst"]
	specs[id] = {
		"id": id,
		"name": display_name,
		"group": group,
		"source": source,
		"canvas_layer": canvas_layer,
		"palette": _palette(group),
		"animations": [
			{"id": "%s.ambient_a" % id, "description": animation_a, "motif": motif_a},
			{"id": "%s.ambient_b" % id, "description": animation_b, "motif": motif_b},
		],
		"idle_event": {
			"id": "%s.idle_%s" % [id, idle_motif],
			"description": idle_description,
			"motif": idle_motif,
			"motion": motions[seed % motions.size()],
			"delay": 16.0 + float(seed % 7),
			"duration": 2.7 + float(seed % 4) * 0.2,
			"cooldown": 30.0 + float(seed % 13),
		},
	}


static func _palette(group: String) -> Array:
	match group:
		"reef":
			return [Color(0.54, 0.92, 0.95), Color(0.74, 0.62, 0.94), Color(1.0, 0.86, 0.55)]
		"sky_promenade", "sky_legacy":
			return [Color(0.56, 0.86, 0.82), Color(0.78, 0.72, 0.96), Color(1.0, 0.82, 0.58)]
		"north", "ice_dungeon":
			return [Color(0.72, 0.92, 1.0), Color(0.78, 0.72, 0.96), Color(1.0, 0.9, 0.68)]
		"ember", "ember_dungeon":
			return [Color(1.0, 0.54, 0.26), Color(0.72, 0.42, 0.58), Color(1.0, 0.78, 0.38)]
		"castle", "castle_room", "opera_act":
			return [Color(0.86, 0.72, 0.96), Color(0.58, 0.9, 0.94), Color(1.0, 0.82, 0.5)]
		"overlay", "entry", "picture_game", "dance":
			return [Color(0.72, 0.9, 1.0), Color(0.94, 0.7, 0.92), Color(1.0, 0.86, 0.52)]
		"kart", "galaxy":
			return [Color(0.56, 0.9, 1.0), Color(0.8, 0.62, 1.0), Color(1.0, 0.88, 0.42)]
		"combat":
			return [Color(0.68, 0.88, 1.0), Color(1.0, 0.56, 0.34), Color(1.0, 0.84, 0.5)]
		"stuffie":
			return [Color(0.82, 0.72, 1.0), Color(0.62, 0.9, 0.88), Color(1.0, 0.68, 0.78)]
		_:
			return [Color(0.62, 0.9, 1.0), Color(0.88, 0.7, 0.96), Color(1.0, 0.86, 0.52)]
