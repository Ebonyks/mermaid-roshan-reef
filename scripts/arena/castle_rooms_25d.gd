class_name CastleRooms25D
extends RefCounted
# Picture-first Pearl Castle room shell. Every in-world image is a Sprite3D
# card at real scene depth. Main Hall background tiles are the sole shaded
# receiver exception for its touch-controlled light pool; characters, props,
# and effects remain unshaded. Controls are reserved for touch routing, the
# Storybook elevator, and other interface chrome. No model or mesh art is
# created or loaded by this satellite.

const ROOM_ART := "res://assets/flats/castle/rooms/"
const ROOM_TILE_ROOT := ROOM_ART + "background_tiles/"
const HALL_TILE_ROOT := "res://assets/flats/castle/main_hall_2screen/tiles/"
const HALL_ART_ROOT := "res://assets/flats/castle/main_hall_2screen/"
const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")
const ART_TO_STAGE := 1.25
const ART_SIZE := Vector2(1024.0, 576.0)
const WORLD_WIDTH := 20.0
const WORLD_HEIGHT := 11.25
const CAMERA_DISTANCE := 18.0
const CAMERA_FOV := 58.109
const CARD_PIXEL_SIZE := WORLD_WIDTH / ART_SIZE.x
const ROOM_TILE_NATIVE_SIZE := Vector2(1024.0, 576.0)
const ROOM_TILE_LOGICAL_SIZE := Vector2(512.0, 288.0)
const ROOM_TILE_PIXEL_SIZE := CARD_PIXEL_SIZE * 0.5
const WORLD_ORIGIN := Vector3(0.0, 2000.0, 0.0)
const BACKGROUND_Z := 0.0
const ITEM_Z := 0.55
const PLAYER_BACK_Z := 1.25
const MIDGROUND_Z := 2.0
const PLAYER_FRONT_Z := 3.15
const FOREGROUND_Z := 4.0
const EFFECT_Z := 4.35
const LIGHT_FIXTURE_Z := 0.72
const MIRROR_INSERT_Z := 0.24
const HALL_LIGHT_Z := 7.0
const PLAYER_STAGE_HEIGHT := 270.0
const HALL_PLAYER_STAGE_HEIGHT := 190.0
const SHADOW_STAGE_SIZE := Vector2(210.0, 38.0)
const HALL_VIEW_SIZE := Vector2(1672.0, 941.0)
const HALL_LOGICAL_SIZE := Vector2(3344.0, 941.0)
const HALL_STAGE_SCALE := 1280.0 / HALL_VIEW_SIZE.x
const HALL_CARD_PIXEL_SIZE := WORLD_WIDTH / HALL_VIEW_SIZE.x
const HALL_WALK := Rect2(60.0, 615.0, 3224.0, 300.0)
const HALL_FILL_COLOR := Color(0.60, 0.52, 0.90)
const HALL_FILL_ENERGY := 0.72
const HALL_FILL_OFF_ENERGY := 0.42
const HALL_SCONCE_COLOR := Color(1.0, 0.74, 0.43)
const HALL_GLOW_FULL := 1.12
const HALL_GLOW_SPEEDY := 0.75
const HALL_BLOOM_FULL := 0.24
const HALL_BLOOM_SPEEDY := 0.11
const HALL_GLOW_OFF := 0.24
const HALL_BLOOM_OFF := 0.015
const HALL_TILE_FILES: Array[String] = [
	"runtime_bleed/main_hall_room_led_r0_c0_bleed.png",
	"runtime_bleed/main_hall_room_led_r0_c1_bleed.png",
	"runtime_bleed/main_hall_room_led_r0_c2_bleed.png",
	"runtime_bleed/main_hall_room_led_r0_c3_bleed.png",
	"main_hall_room_led_r1_c0.png",
	"main_hall_room_led_r1_c1.png",
	"main_hall_room_led_r1_c2.png",
	"main_hall_room_led_r1_c3.png",
]
const HALL_LIGHT_CLUSTERS: Array[Dictionary] = [
	{"id": "a_left", "half": "a", "pos": Vector2(330.0, 335.0),
		"max_energy": 4.6},
	{"id": "a_right", "half": "a", "pos": Vector2(1320.0, 335.0),
		"max_energy": 4.6},
	{"id": "b_left", "half": "b", "pos": Vector2(1970.0, 335.0),
		"max_energy": 4.6},
	{"id": "b_right", "half": "b", "pos": Vector2(2780.0, 335.0),
		"max_energy": 4.6},
]
const HALL_STRUCTURE_CARDS: Array[Dictionary] = [
	{"id": "screen_join_column", "pos": Vector2(1672.0, 470.5),
		"z": 0.20, "scale": 1.0, "shaded": true,
		"tex_path": HALL_ART_ROOT + "castle_join_column_cutout_reuse.png",
		"role": "architectural_join_divider"},
	{"id": "screen_join_floor_inlay", "pos": Vector2(1672.0, 780.5),
		"z": 0.21, "scale": 1.0, "shaded": true,
		"tex_path": HALL_ART_ROOT + "castle_join_floor_inlay_reuse.png",
		"role": "architectural_join_inlay"},
	{"id": "playroom_portal_bridge", "pos": Vector2(1672.0, 384.0),
		"z": 0.28, "scale": 0.96, "shaded": true,
		"tex_path": HALL_ART_ROOT + "castle_playroom_portal_cutout_reuse.png",
		"role": "architectural_bridge"},
	{"id": "playroom_portal_marker", "pos": Vector2(1672.0, 270.0),
		"z": 0.68, "scale": 0.09, "shaded": false,
		"tex_path": "res://assets/mg/star.png",
		"role": "playroom_door_marker"},
]
const HALL_PORTALS: Array[Dictionary] = [
	{"id": "opera_hall", "name": "Opera Hall",
		"rect": Rect2(420.0, 105.0, 420.0, 535.0),
		"foot": Vector2(630.0, 650.0)},
	{"id": "library", "name": "Royal Library",
		"rect": Rect2(1010.0, 315.0, 250.0, 330.0),
		"foot": Vector2(1135.0, 660.0)},
	{"id": "kitchen", "name": "Royal Kitchen",
		"rect": Rect2(1270.0, 315.0, 250.0, 330.0),
		"foot": Vector2(1395.0, 660.0)},
	{"id": "playroom", "name": "Stuffie Playroom",
		"rect": Rect2(1550.0, 236.0, 244.0, 414.0),
		"foot": Vector2(1672.0, 670.0)},
	{"id": "craft_room", "name": "Craft Room",
		"rect": Rect2(1955.0, 265.0, 280.0, 385.0),
		"foot": Vector2(2095.0, 670.0)},
	{"id": "mermaid_pool", "name": "Mermaid Pool",
		"rect": Rect2(2360.0, 265.0, 280.0, 385.0),
		"foot": Vector2(2500.0, 670.0)},
	{"id": "bubble_bath", "name": "Bubble Bath",
		"rect": Rect2(2665.0, 265.0, 280.0, 385.0),
		"foot": Vector2(2805.0, 670.0)},
	{"id": "__throne", "name": "Huluu's throne",
		"rect": Rect2(3000.0, 90.0, 330.0, 570.0),
		"foot": Vector2(3090.0, 690.0)},
]
const HALL_ITEMS: Array[Dictionary] = [
	{"id": "tapestry_right", "name": "Royal shell tapestry",
		"pos": Vector2(2612.0, 142.0), "z": MIRROR_INSERT_Z,
		"tex_path": HALL_ART_ROOT + "castle_royal_tapestry_reuse.png",
		"scale": 0.72, "anim": "sway", "sound": "chime.ogg", "pitch": 1.55,
		"hotspot_size": Vector2(105.0, 190.0),
		"symbol": "*", "color": Color(1.0, 0.80, 0.91)},
	{"id": "sconce_a0", "name": "Pearl shell light",
		"pos": Vector2(260.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": HALL_ART_ROOT + "castle_shell_sconce_integrated_reuse.png",
		"scale": 1.15, "anim": "light", "sound": "chime.ogg", "pitch": 1.65,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "a_left",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_a1", "name": "Pearl shell light",
		"pos": Vector2(1012.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": HALL_ART_ROOT + "castle_shell_sconce_integrated_reuse.png",
		"scale": 1.15, "anim": "light", "sound": "chime.ogg", "pitch": 1.72,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "a_right",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_a2", "name": "Pearl shell light",
		"pos": Vector2(1476.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": HALL_ART_ROOT + "castle_shell_sconce_integrated_reuse.png",
		"scale": 1.15, "anim": "light", "sound": "chime.ogg", "pitch": 1.78,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "a_right",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_b0", "name": "Pearl shell light",
		"pos": Vector2(2048.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": HALL_ART_ROOT + "castle_shell_sconce_integrated_reuse.png",
		"scale": 1.15, "anim": "light", "sound": "chime.ogg", "pitch": 1.65,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "b_left",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_b1", "name": "Pearl shell light",
		"pos": Vector2(2415.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": HALL_ART_ROOT + "castle_shell_sconce_integrated_reuse.png",
		"scale": 1.15, "anim": "light", "sound": "chime.ogg", "pitch": 1.72,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "b_left",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_b2", "name": "Pearl shell light",
		"pos": Vector2(2888.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": HALL_ART_ROOT + "castle_shell_sconce_integrated_reuse.png",
		"scale": 1.15, "anim": "light", "sound": "chime.ogg", "pitch": 1.78,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "b_right",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
]
const HALL_DUST_BUNNY_SPAWNS: Array[Dictionary] = [
	{"id": "sleepy_bunny", "name": "Sleeping dust bunny",
		"pos": Vector2(720.0, 790.0), "z": 2.65,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_sleepy.png",
		"scale": 0.34, "dust_bunny_role": "sleeping_static",
		"contact_offset": Vector2(0.0, 74.0),
		"contact_radius": Vector2(132.0, 92.0),
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.55,
		"color": Color(0.86, 0.72, 1.0)},
	{"id": "shell_bunny", "name": "Shell-hide dust bunny",
		"pos": Vector2(1140.0, 790.0), "z": 3.05,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_shell_hide.png",
		"scale": 0.32, "dust_bunny_role": "shell_static",
		"contact_offset": Vector2(0.0, 74.0),
		"contact_radius": Vector2(132.0, 92.0),
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.45,
		"color": Color(0.60, 0.92, 1.0)},
	{"id": "runner_bunny", "name": "Running dust bunny",
		"pos": Vector2(1820.0, 790.0), "z": 2.85,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_hop.png",
		"scale": 0.32, "dust_bunny_role": "runner",
		"contact_offset": Vector2(0.0, 74.0),
		"contact_radius": Vector2(142.0, 98.0),
		"patrol_x": Vector2(1820.0, 2580.0), "run_speed": 220.0,
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.70,
		"color": Color(1.0, 0.75, 0.86)},
]
const ROOMS: Array[Dictionary] = [
	{"id": "main_hall", "name": "Main Hall", "icon": "♛",
		"tex": "room_main_hall_background_v2.png", "action": "throne", "action_icon": "♛"},
	{"id": "opera_hall", "name": "Opera Hall", "icon": "🎭",
		"tex": "room_opera_hall_background.png", "action": "opera",
		"action_icon": "🎭"},
	{"id": "kitchen", "name": "Royal Kitchen", "icon": "🍲",
		"tex": "room_kitchen_background.png", "action": "kitchen",
		"action_icon": "🍲"},
	{"id": "library", "name": "Royal Library", "icon": "📚",
		"tex": "room_library_background.png", "action": "library",
		"action_icon": "📚"},
	{"id": "playroom", "name": "Stuffie Playroom", "icon": "🧸",
		"tex": "room_playroom_background.png", "action": "stuffies",
		"action_icon": "🧸"},
	{"id": "craft_room", "name": "Craft Room", "icon": "🎨",
		"tex": "room_craft_room_background.png", "action": "craft",
		"action_icon": "🎨"},
	{"id": "mermaid_pool", "name": "Mermaid Pool", "icon": "💦",
		"tex": "room_mermaid_pool_background.png", "action": "pool",
		"action_icon": "💦"},
	{"id": "bubble_bath", "name": "Bubble Bath", "icon": "🛁",
		"tex": "room_bubble_bath_background.png", "action": "bath",
		"action_icon": "🫧"},
]
const ROOM_LAYOUTS := {
	"main_hall": {
		"walk": Rect2(165.0, 475.0, 950.0, 190.0), "mid_foot_y": -1.0,
		"mid": [],
		"front": [
			{"tex": "room_main_hall_front_left.png", "pos": Vector2(0.0, 0.0)},
			{"tex": "room_main_hall_front_right.png", "pos": Vector2(750.0, 0.0)},
		],
	},
	"opera_hall": {
		"walk": Rect2(180.0, 455.0, 920.0, 215.0), "mid_foot_y": -1.0,
		"mid": [],
		"front": [
			{"tex": "room_opera_hall_front_left.png", "pos": Vector2(0.0, 252.0)},
			{"tex": "room_opera_hall_front_right.png", "pos": Vector2(750.0, 252.0)},
		],
	},
	"kitchen": {
		"walk": Rect2(205.0, 450.0, 870.0, 215.0), "mid_foot_y": -1.0,
		"mid": [],
		"front": [
			{"tex": "room_kitchen_front_left.png", "pos": Vector2(0.0, 354.0)},
			{"tex": "room_kitchen_front_right.png", "pos": Vector2(650.0, 324.0)},
		],
	},
	"library": {
		"walk": Rect2(175.0, 440.0, 930.0, 230.0), "mid_foot_y": 548.0,
		"mid": [],
		"front": [
			{"tex": "room_library_front_left.png", "pos": Vector2(0.0, 273.0)},
			{"tex": "room_library_front_right.png", "pos": Vector2(724.0, 273.0)},
		],
	},
	"playroom": {
		"walk": Rect2(165.0, 425.0, 950.0, 245.0), "mid_foot_y": 530.0,
		"mid": [],
		"front": [
			{"tex": "room_playroom_front_left.png", "pos": Vector2(0.0, 319.0)},
			{"tex": "room_playroom_front_right.png", "pos": Vector2(777.0, 319.0)},
		],
	},
	"craft_room": {
		"walk": Rect2(175.0, 420.0, 930.0, 250.0), "mid_foot_y": 510.0,
		"mid": [],
		"front": [
			{"tex": "room_craft_room_front_left.png", "pos": Vector2(0.0, 316.0)},
			{"tex": "room_craft_room_front_right.png", "pos": Vector2(720.0, 316.0)},
		],
	},
	"mermaid_pool": {
		"walk": Rect2(170.0, 400.0, 940.0, 270.0), "mid_foot_y": 535.0,
		"mid": [
			{"tex": "room_mermaid_pool_mid_pool.png", "pos": Vector2(0.0, 212.0)},
		],
		"front": [
			{"tex": "room_mermaid_pool_front_left.png", "pos": Vector2(0.0, 378.0)},
			{"tex": "room_mermaid_pool_front_right.png", "pos": Vector2(819.0, 378.0)},
		],
	},
	"bubble_bath": {
		"walk": Rect2(170.0, 405.0, 940.0, 265.0), "mid_foot_y": -1.0,
		"mid": [],
		"front": [
			{"tex": "room_bubble_bath_front_left.png", "pos": Vector2(0.0, 358.0)},
			{"tex": "room_bubble_bath_front_right.png", "pos": Vector2(798.0, 358.0)},
		],
	},
}
const ROOM_ITEMS := {
	"main_hall": [
		{"id": "throne", "name": "Royal throne", "pos": Vector2(430, 150),
			"z": 0.55,
			"anim": "pulse", "sound": "chime.ogg", "pitch": 1.25,
			"symbol": "✦", "color": Color(1.0, 0.82, 0.32)},
		{"id": "fountain_left", "name": "Left fountain", "pos": Vector2(88, 371),
			"z": 4.15,
			"tex": "room_main_hall_item_fountain_left_v2.png",
			"hotspot_offset": Vector2(18, 8),
			"hotspot_size": Vector2(220, 180),
			"anim": "splash", "sound": "ui_tap.ogg", "pitch": 1.8,
			"symbol": "○", "color": Color(0.50, 0.91, 1.0)},
		{"id": "fountain_right", "name": "Right fountain", "pos": Vector2(722, 371),
			"z": 4.15,
			"tex": "room_main_hall_item_fountain_right_v2.png",
			"hotspot_offset": Vector2(18, 8),
			"hotspot_size": Vector2(220, 180),
			"anim": "splash", "sound": "ui_tap.ogg", "pitch": 2.0,
			"symbol": "○", "color": Color(0.50, 0.91, 1.0)},
	],
	"opera_hall": [
		{"id": "curtains", "name": "Stage curtains", "pos": Vector2(414, 100),
			"z": 0.65,
			"anim": "sway", "sound": "purr.wav", "pitch": 1.4,
			"symbol": "♪", "color": Color(1.0, 0.67, 0.78)},
		{"id": "chandelier", "name": "Pearl chandelier", "pos": Vector2(418, 0),
			"z": 1.10,
			"anim": "sway", "sound": "chime.ogg", "pitch": 1.7,
			"symbol": "✦", "color": Color(1.0, 0.90, 0.44)},
		{"id": "stage_star", "name": "Stage star", "pos": Vector2(463, 286),
			"z": 0.75,
			"anim": "pulse", "sound": "chime.ogg", "pitch": 2.1,
			"symbol": "★", "color": Color(1.0, 0.82, 0.30)},
	],
	"kitchen": [
		{"id": "sink", "name": "Shell sink", "pos": Vector2(0, 114),
			"z": 0.75,
			"anim": "splash", "sound": "ui_tap.ogg", "pitch": 2.2,
			"symbol": "○", "color": Color(0.45, 0.90, 1.0)},
		{"id": "soup_pot", "name": "Bubbling soup", "pos": Vector2(294, 143),
			"z": 1.35,
			"anim": "bounce", "sound": "buzz.ogg", "pitch": 1.65,
			"symbol": "●", "color": Color(1.0, 0.58, 0.30)},
		{"id": "teapot", "name": "Royal teapot", "pos": Vector2(780, 165),
			"z": 1.10,
			"anim": "wiggle", "sound": "chime.ogg", "pitch": 1.55,
			"symbol": "○", "color": Color(0.61, 0.91, 0.90)},
	],
	"library": [
		{"id": "magic_book", "name": "Magic storybook", "pos": Vector2(445, 145),
			"z": 0.80,
			"anim": "hover", "sound": "chime.ogg", "pitch": 1.8,
			"symbol": "✦", "color": Color(0.81, 0.66, 1.0)},
		{"id": "pearl_table", "name": "Reading pearl", "pos": Vector2(392, 315),
			"z": MIDGROUND_Z,
			"anim": "pulse", "sound": "purr.wav", "pitch": 1.6,
			"symbol": "○", "color": Color(1.0, 0.91, 0.62)},
		{"id": "pearl_lamp", "name": "Pearl lamp", "pos": Vector2(0, 225),
			"z": 0.65,
			"anim": "pulse", "sound": "chime.ogg", "pitch": 2.0,
			"symbol": "✦", "color": Color(1.0, 0.88, 0.48)},
	],
	"playroom": [
		{"id": "stuffie_nook", "name": "Stuffie friends", "pos": Vector2(380, 140),
			"z": 0.75,
			"anim": "bounce", "sound": "penguin_giggle.ogg", "pitch": 1.35,
			"symbol": "♡", "color": Color(1.0, 0.58, 0.74)},
		{"id": "stacking_toy", "name": "Stacking toy", "pos": Vector2(218, 284),
			"z": MIDGROUND_Z,
			"anim": "wiggle", "sound": "hop_boing.ogg", "pitch": 1.25,
			"symbol": "★", "color": Color(1.0, 0.79, 0.30)},
		{"id": "blocks", "name": "Toy blocks", "pos": Vector2(626, 320),
			"z": MIDGROUND_Z,
			"anim": "bounce", "sound": "hop_boing.ogg", "pitch": 1.55,
			"symbol": "✦", "color": Color(0.54, 0.91, 0.78)},
	],
	"craft_room": [
		{"id": "idea_board", "name": "Idea board", "pos": Vector2(377, 103),
			"z": 0.70,
			"anim": "pulse", "sound": "chime.ogg", "pitch": 1.7,
			"symbol": "✦", "color": Color(1.0, 0.78, 0.45)},
		{"id": "paint_table", "name": "Paint jars", "pos": Vector2(400, 272),
			"z": MIDGROUND_Z,
			"anim": "bounce", "sound": "buy.ogg", "pitch": 1.5,
			"symbol": "●", "color": Color(0.60, 0.90, 0.82)},
		{"id": "palette", "name": "Rainbow palette", "pos": Vector2(0, 320),
			"z": FOREGROUND_Z,
			"anim": "wiggle", "sound": "buzz.ogg", "pitch": 1.9,
			"symbol": "●", "color": Color(1.0, 0.55, 0.72)},
	],
	"mermaid_pool": [
		{"id": "waterfall", "name": "Rainbow waterfall", "pos": Vector2(285, 45),
			"z": 0.65,
			"anim": "splash", "sound": "ui_tap.ogg", "pitch": 1.7,
			"symbol": "○", "color": Color(0.52, 0.91, 1.0)},
		{"id": "flower_float", "name": "Flower float", "pos": Vector2(371, 218),
			"z": MIDGROUND_Z,
			"anim": "spin", "sound": "chime.ogg", "pitch": 2.0,
			"symbol": "✦", "color": Color(1.0, 0.62, 0.78)},
		{"id": "bubble_fountain", "name": "Bubble fountain", "pos": Vector2(553, 183),
			"z": MIDGROUND_Z,
			"anim": "splash", "sound": "ui_tap.ogg", "pitch": 2.25,
			"symbol": "○", "color": Color(0.72, 0.94, 1.0)},
	],
	"bubble_bath": [
		{"id": "bathtub", "name": "Bubble bathtub", "pos": Vector2(76, 157),
			"z": 1.25,
			"anim": "splash", "sound": "penguin_giggle.ogg", "pitch": 1.3,
			"symbol": "○", "color": Color(0.64, 0.92, 1.0)},
		{"id": "sink", "name": "Shell sink", "pos": Vector2(440, 137),
			"z": 0.80,
			"anim": "splash", "sound": "ui_tap.ogg", "pitch": 2.3,
			"symbol": "○", "color": Color(0.52, 0.92, 1.0)},
		{"id": "toilet", "name": "Royal toilet", "pos": Vector2(753, 154),
			"z": 1.00,
			"anim": "wiggle", "sound": "fart.ogg", "pitch": 1.15,
			"symbol": "○", "color": Color(1.0, 0.72, 0.86)},
	],
}

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func is_open() -> bool:
	return m.castle_room_layer != null and is_instance_valid(m.castle_room_layer)

func open(start_room: String = "main_hall") -> void:
	if is_open():
		resume(start_room)
		return
	m.castle_room_id = start_room
	m.castle_room_menu_open = false
	m.castle_room_buttons.clear()
	m.g["castle_dust_bunnies_cleared"] = {}
	m.g["castle_dust_bunny_runner_time"] = 0.0
	m.castle_room_layer = CanvasLayer.new()
	m.castle_room_layer.layer = 14
	m.add_child(m.castle_room_layer)
	var root := Control.new()
	root.name = "CastleRooms25D"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_STOP
	root.gui_input.connect(_on_room_input)
	m.castle_room_layer.add_child(root)
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	m.castle_room_stage = StorybookUI.add_stage(root, viewport_size)
	_build_stage()
	m._set_world_controls_enabled(false, "castle_rooms")
	if m.player != null:
		m.player.vel = Vector3.ZERO
		m.player.visible = false
	if m.hud_layer != null:
		m.hud_layer.visible = false
	show_room(start_room, false)
	_activate_castle_environment()
	_sync_hall_lighting()

func resume(room_id: String = "") -> void:
	if not is_open():
		open("main_hall" if room_id == "" else room_id)
		return
	m.castle_room_layer.visible = true
	if m.castle_room_world_root != null:
		m.castle_room_world_root.visible = true
	if m.castle_room_camera != null:
		m.castle_room_camera.make_current()
	_activate_castle_environment()
	m._set_world_controls_enabled(false, "castle_rooms")
	if m.player != null:
		m.player.visible = false
	if m.hud_layer != null:
		m.hud_layer.visible = false
	if room_id != "":
		show_room(room_id, false)

func suspend() -> void:
	_restore_previous_environment()
	if is_open():
		m.castle_room_layer.visible = false
	if m.castle_room_world_root != null:
		m.castle_room_world_root.visible = false
	if m.castle_room_camera != null:
		m.castle_room_camera.current = false
	m._set_world_controls_enabled(true, "castle_rooms")

func close() -> void:
	_restore_previous_environment()
	if is_open():
		m.castle_room_layer.queue_free()
	if m.castle_room_camera != null:
		m.castle_room_camera.current = false
	if m.castle_room_world_root != null \
			and is_instance_valid(m.castle_room_world_root):
		m.castle_room_world_root.queue_free()
	m.castle_room_layer = null
	m.castle_room_stage = null
	m.castle_room_world_root = null
	m.castle_room_camera = null
	m.castle_room_background = null
	m.castle_room_background_tiles.clear()
	m.castle_room_detail_tiles.clear()
	m.castle_room_light_nodes.clear()
	m.castle_room_environment = null
	m.castle_room_previous_environment = null
	m.castle_room_mid_layer = null
	m.castle_room_front_layer = null
	m.castle_room_item_visual_layer = null
	m.castle_room_item_effect_layer = null
	m.castle_room_item_hotspot_layer = null
	m.castle_room_door_hotspot_layer = null
	m.castle_room_door_hotspots.clear()
	m.castle_room_item_sprites.clear()
	m.castle_room_prop_sfx = null
	m.castle_room_player_sprite = null
	m.castle_room_player_shadow = null
	m.castle_room_action_button = null
	m.castle_room_menu_panel = null
	m.castle_room_buttons.clear()
	m.castle_room_menu_open = false
	m.g.erase("castle_dust_bunnies_cleared")
	m.g.erase("castle_dust_bunny_runner_time")
	m._set_world_controls_enabled(true, "castle_rooms")
	if m.player != null:
		m.player.visible = true
		if m.player.cam != null:
			m.player.cam.make_current()
	if m.hud_layer != null:
		m.hud_layer.visible = true

func tick(delta: float) -> void:
	if m.player != null:
		m.player.vel = Vector3.ZERO
	_update_dust_bunny_runner(delta)
	_check_dust_bunny_contacts()
	_update_camera_parallax(delta)
	_update_touch_hotspots()
	_update_hall_portals()
	_sync_hall_lighting()

func _build_stage() -> void:
	var stage: Control = m.castle_room_stage
	m.castle_room_world_root = Node3D.new()
	m.castle_room_world_root.name = "CastleRoomsSprite3DWorld"
	m.castle_room_world_root.position = WORLD_ORIGIN
	m.add_child(m.castle_room_world_root)

	m.castle_room_camera = Camera3D.new()
	m.castle_room_camera.name = "CastleRoomsCamera"
	m.castle_room_camera.position = Vector3(0.0, 0.0, CAMERA_DISTANCE)
	m.castle_room_camera.projection = Camera3D.PROJECTION_PERSPECTIVE
	m.castle_room_camera.fov = CAMERA_FOV
	m.castle_room_camera.keep_aspect = Camera3D.KEEP_WIDTH
	m.castle_room_camera.near = 0.1
	m.castle_room_camera.far = 40.0
	m.castle_room_world_root.add_child(m.castle_room_camera)
	m.castle_room_camera.make_current()
	_build_castle_environment()

	m.castle_room_background = _new_card("RoomBackdrop",
		load(ROOM_ART + "room_main_hall_background_v2.png") as Texture2D)
	m.castle_room_background.position = Vector3(0.0, 0.0, BACKGROUND_Z)
	m.castle_room_background.pixel_size = CARD_PIXEL_SIZE
	m.castle_room_background.set_meta("source_asset_role", "clean_background")
	m.castle_room_world_root.add_child(m.castle_room_background)
	_build_hall_background_tiles()
	_build_hall_lighting()

	m.castle_room_item_visual_layer = Node3D.new()
	m.castle_room_item_visual_layer.name = "TouchableRoomProps"
	m.castle_room_world_root.add_child(m.castle_room_item_visual_layer)
	m.castle_room_mid_layer = Node3D.new()
	m.castle_room_mid_layer.name = "RoomMidground"
	m.castle_room_world_root.add_child(m.castle_room_mid_layer)

	var shadow_texture: Texture2D = load(ROOM_ART + "room_actor_shadow.png")
	m.castle_room_player_shadow = _new_card("RoshanContactShadow", shadow_texture)
	m.castle_room_player_shadow.modulate = Color(0.24, 0.25, 0.48, 0.58)
	m.castle_room_player_shadow.cast_shadow = \
		GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	m.castle_room_player_shadow.set_meta("castle_player_shadow", true)
	m.castle_room_player_shadow.set_meta("source_asset_role", "actor_shadow")
	m.castle_room_world_root.add_child(m.castle_room_player_shadow)

	m.castle_room_player_sprite = _new_card("RoshanCutout",
		load(m.skin_sprite_path()) as Texture2D)
	m.castle_room_player_sprite.name = "RoshanCutout"
	m.castle_room_player_sprite.cast_shadow = \
		GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
	m.castle_room_player_sprite.set_meta("source_asset_role", "character")
	m.castle_room_world_root.add_child(m.castle_room_player_sprite)
	if m.skin_id == "classic":
		var animator := ROSHAN_SPRITE_LOOP.new()
		animator.name = "AlwaysAliveSpriteLoop"
		m.castle_room_player_sprite.add_child(animator)
		animator.setup_sprite_3d(
			m.castle_room_player_sprite, false,
			m.castle_room_player_sprite)
	var idle := m.castle_room_player_sprite.create_tween().set_loops()
	idle.tween_property(m.castle_room_player_sprite, "rotation:z", -0.012,
		0.85).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	idle.tween_property(m.castle_room_player_sprite, "rotation:z", 0.012,
		0.85).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	m.castle_room_front_layer = Node3D.new()
	m.castle_room_front_layer.name = "RoomForeground"
	m.castle_room_world_root.add_child(m.castle_room_front_layer)
	m.castle_room_item_effect_layer = Node3D.new()
	m.castle_room_item_effect_layer.name = "TouchablePropEffects"
	m.castle_room_world_root.add_child(m.castle_room_item_effect_layer)
	m.castle_room_item_hotspot_layer = Control.new()
	m.castle_room_item_hotspot_layer.name = "TouchablePropHotspots"
	m.castle_room_item_hotspot_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.castle_room_item_hotspot_layer.z_index = 24
	stage.add_child(m.castle_room_item_hotspot_layer)
	m.castle_room_door_hotspot_layer = Control.new()
	m.castle_room_door_hotspot_layer.name = "MainHallDoorHotspots"
	m.castle_room_door_hotspot_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.castle_room_door_hotspot_layer.z_index = 25
	stage.add_child(m.castle_room_door_hotspot_layer)
	_build_hall_portals()
	m.castle_room_prop_sfx = AudioStreamPlayer.new()
	m.castle_room_prop_sfx.name = "CastleRoomPropSfx"
	m.castle_room_prop_sfx.bus = "SFX"
	m.castle_room_prop_sfx.volume_db = -10.0
	m.castle_room_prop_sfx.process_mode = Node.PROCESS_MODE_ALWAYS
	m.castle_room_layer.add_child(m.castle_room_prop_sfx)

	m.castle_room_action_button = Button.new()
	m.castle_room_action_button.name = "RoomAction"
	m.castle_room_action_button.position = Vector2(72.0, 520.0)
	StorybookUI.style_icon_button(m.castle_room_action_button, "♛", "gold",
		Vector2(132.0, 132.0), "Touch the room")
	m.castle_room_action_button.pressed.connect(activate_current_room)
	m.castle_room_action_button.z_index = 30
	stage.add_child(m.castle_room_action_button)

	var exit_button := Button.new()
	exit_button.name = "CourtyardExit"
	exit_button.position = Vector2(28.0, 28.0)
	StorybookUI.style_back_button(exit_button, "Castle courtyard")
	exit_button.pressed.connect(_exit_to_courtyard)
	exit_button.z_index = 30
	stage.add_child(exit_button)

	var elevator := Button.new()
	elevator.name = "ElevatorButton"
	elevator.position = Vector2(1116.0, 544.0)
	StorybookUI.style_icon_button(elevator, "↕", "primary",
		Vector2(136.0, 136.0), "Castle elevator")
	elevator.pressed.connect(_toggle_menu)
	elevator.z_index = 30
	stage.add_child(elevator)
	var elevator_pointer := Label.new()
	elevator_pointer.name = "ElevatorPointer"
	elevator_pointer.text = "▼"
	elevator_pointer.position = Vector2(1155.0, 490.0)
	StorybookUI.style_label(elevator_pointer, 48, StorybookUI.GOLD, 5)
	elevator_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	elevator_pointer.z_index = 30
	stage.add_child(elevator_pointer)
	var point := elevator_pointer.create_tween().set_loops()
	point.tween_property(elevator_pointer, "position:y", 502.0, 0.55).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	point.tween_property(elevator_pointer, "position:y", 490.0, 0.55).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

	m.castle_room_menu_panel = StorybookUI.add_panel(stage,
		Rect2(348.0, 125.0, 584.0, 470.0), StorybookUI.INK_SOFT,
		Color(0.94, 0.98, 1.0, 0.98), 42)
	m.castle_room_menu_panel.z_index = 40
	m.castle_room_menu_panel.visible = false
	_build_room_buttons(m.castle_room_menu_panel)

func _build_hall_background_tiles() -> void:
	m.castle_room_background_tiles.clear()
	for index in range(HALL_TILE_FILES.size()):
		var texture: Texture2D = load(HALL_TILE_ROOT + HALL_TILE_FILES[index])
		if texture == null:
			continue
		var row: int = index / 4
		var column: int = index % 4
		var top_left := Vector2(float(column) * 836.0,
			0.0 if row == 0 else 470.0)
		var tile: Sprite3D = _new_card(
			"MainHallTile_r%d_c%d" % [row, column], texture)
		var center: Vector2 = top_left + texture.get_size() * 0.5
		tile.position = _hall_art_to_world(center, BACKGROUND_Z)
		tile.pixel_size = HALL_CARD_PIXEL_SIZE
		tile.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
		tile.shaded = true
		tile.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		tile.visible = false
		tile.set_meta("source_asset_role", "clean_background_tile")
		tile.set_meta("source_master_grid", "2x4")
		# The approved source rectangles remain exact and non-overlapping.
		# Top cards append the first approved pixel row from the card beneath
		# them, producing a one-pixel render overlap that closes a Mobile raster
		# crack without scaling, interpolation, crop, or generated art.
		var source_size := Vector2(836.0, 470.0 if row == 0 else 471.0)
		tile.set_meta("source_art_rect", Rect2(top_left, source_size))
		tile.set_meta("render_art_rect",
			Rect2(top_left, texture.get_size()))
		tile.set_meta("runtime_seam_bleed_pixels", 1 if row == 0 else 0)
		tile.set_meta("depth_z", BACKGROUND_Z)
		m.castle_room_world_root.add_child(tile)
		m.castle_room_background_tiles.append(tile)

func _build_hall_lighting() -> void:
	m.castle_room_light_nodes.clear()
	var fill := DirectionalLight3D.new()
	fill.name = "CastleLavenderAmbientFill"
	fill.light_color = HALL_FILL_COLOR
	fill.light_energy = HALL_FILL_ENERGY
	fill.shadow_enabled = false
	fill.set_meta("castle_light_role", "ambient_fill")
	m.castle_room_world_root.add_child(fill)
	m.castle_room_light_nodes.append(fill)
	for cluster_data: Dictionary in HALL_LIGHT_CLUSTERS:
		var light := SpotLight3D.new()
		var cluster_id: String = String(cluster_data["id"])
		light.name = "CastlePearlLight_" + cluster_id
		light.position = _hall_art_to_world(
			cluster_data["pos"] as Vector2, HALL_LIGHT_Z)
		var max_energy: float = float(cluster_data.get("max_energy", 2.5))
		light.light_color = HALL_SCONCE_COLOR
		light.light_energy = max_energy
		light.light_indirect_energy = 0.0
		light.spot_range = 12.5
		light.spot_angle = 52.0
		light.spot_angle_attenuation = 1.05
		light.shadow_enabled = true
		light.shadow_bias = 0.045
		light.set_meta("castle_light_role", "touch_cluster")
		light.set_meta("cluster_id", cluster_id)
		light.set_meta("hall_half", String(cluster_data["half"]))
		light.set_meta("max_energy", max_energy)
		m.castle_room_world_root.add_child(light)
		m.castle_room_light_nodes.append(light)

func _build_castle_environment() -> void:
	var environment := Environment.new()
	environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color(0.055, 0.035, 0.105)
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color(0.45, 0.38, 0.64)
	environment.ambient_light_energy = 0.22
	m._wind_waker_bloom(environment, HALL_GLOW_FULL,
		HALL_BLOOM_FULL, 0.74)
	m._apply_scene_grade(environment, "warm_pastel")
	environment.adjustment_saturation = 1.08
	environment.adjustment_contrast = 1.18
	environment.adjustment_brightness = 0.91
	environment.set_meta("castle_glow_profile", "dramatic_storybook")
	environment.set_meta("castle_glow_full",
		Vector2(HALL_GLOW_FULL, HALL_BLOOM_FULL))
	environment.set_meta("castle_glow_speedy",
		Vector2(HALL_GLOW_SPEEDY, HALL_BLOOM_SPEEDY))
	m.castle_room_environment = environment

func _activate_castle_environment() -> void:
	if m.we_node == null or m.castle_room_environment == null:
		return
	if m.we_node.environment == m.castle_room_environment:
		return
	m.castle_room_previous_environment = m.we_node.environment
	m.we_node.environment = m.castle_room_environment

func _restore_previous_environment() -> void:
	if m.we_node == null or m.castle_room_environment == null:
		return
	if m.we_node.environment != m.castle_room_environment:
		return
	m.we_node.environment = m.castle_room_previous_environment \
		if m.castle_room_previous_environment != null else m.world_env
	m.castle_room_previous_environment = null

func _set_hall_background_visible(visible: bool) -> void:
	for tile: Sprite3D in m.castle_room_background_tiles:
		if tile != null and is_instance_valid(tile):
			tile.visible = visible
	for tile: Sprite3D in m.castle_room_detail_tiles:
		if tile != null and is_instance_valid(tile):
			tile.visible = not visible
	if m.castle_room_background != null:
		m.castle_room_background.visible = false
	if m.castle_room_door_hotspot_layer != null:
		m.castle_room_door_hotspot_layer.visible = visible

func _clear_room_background_tiles() -> void:
	for tile: Sprite3D in m.castle_room_detail_tiles:
		if tile != null and is_instance_valid(tile):
			tile.free()
	m.castle_room_detail_tiles.clear()

func _build_room_background_tiles(room_id: String) -> void:
	_clear_room_background_tiles()
	for row in range(2):
		for column in range(2):
			var file_name := "room_%s_background_r%d_c%d.png" % [
				room_id, row, column]
			var texture: Texture2D = load(ROOM_TILE_ROOT + file_name)
			if texture == null:
				continue
			var logical_top_left := Vector2(
				float(column) * ROOM_TILE_LOGICAL_SIZE.x,
				float(row) * ROOM_TILE_LOGICAL_SIZE.y)
			var logical_center := logical_top_left \
				+ ROOM_TILE_LOGICAL_SIZE * 0.5
			var tile := _new_card(
				"RoomTile_%s_r%d_c%d" % [room_id, row, column],
				texture)
			tile.position = _art_to_world(logical_center, BACKGROUND_Z)
			tile.pixel_size = ROOM_TILE_PIXEL_SIZE
			# Mip edge sampling causes a one-pixel dark hairline where opaque
			# cards meet. Linear sampling without mipmaps keeps adjacent source
			# texels continuous at this fixed camera distance.
			tile.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
			tile.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			tile.set_meta("source_asset_role", "clean_background_tile")
			tile.set_meta("source_master_grid", "2x2_2k")
			tile.set_meta("source_art_rect",
				Rect2(logical_top_left, ROOM_TILE_LOGICAL_SIZE))
			tile.set_meta("native_texture_size", ROOM_TILE_NATIVE_SIZE)
			tile.set_meta("depth_z", BACKGROUND_Z)
			m.castle_room_world_root.add_child(tile)
			m.castle_room_detail_tiles.append(tile)

func _build_hall_portals() -> void:
	if m.castle_room_door_hotspot_layer == null:
		return
	m.castle_room_door_hotspots.clear()
	for portal_data: Dictionary in HALL_PORTALS:
		var button := Button.new()
		button.name = "HallDoor_" + String(portal_data["id"])
		button.flat = true
		button.focus_mode = Control.FOCUS_NONE
		button.tooltip_text = String(portal_data["name"])
		button.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
		button.set_meta("uses_own_sfx", true)
		button.pressed.connect(_enter_hall_portal.bind(
			String(portal_data["id"]), portal_data["foot"] as Vector2))
		m.castle_room_door_hotspot_layer.add_child(button)
		m.castle_room_door_hotspots.append({
			"button": button,
			"data": portal_data,
		})
	m.castle_room_door_hotspot_layer.visible = false

func _build_room_buttons(panel: Panel) -> void:
	var index := 0
	for room: Dictionary in ROOMS:
		var button := Button.new()
		button.name = "Room_" + String(room["id"])
		button.position = Vector2(28.0 + float(index % 3) * 176.0,
			30.0 + float(index / 3) * 140.0)
		StorybookUI.style_icon_button(button, String(room["icon"]), "secondary",
			Vector2(144.0, 118.0), String(room["name"]))
		button.pressed.connect(show_room.bind(String(room["id"]), true))
		panel.add_child(button)
		m.castle_room_buttons[String(room["id"])] = button
		index += 1
	var bedrooms := Button.new()
	bedrooms.name = "Room_BedroomsFuture"
	bedrooms.position = Vector2(28.0 + float(index % 3) * 176.0,
		30.0 + float(index / 3) * 140.0)
	StorybookUI.style_icon_button(bedrooms, "☾", "locked",
		Vector2(144.0, 118.0), "Bedrooms are dreaming")
	bedrooms.disabled = true
	bedrooms.focus_mode = Control.FOCUS_NONE
	panel.add_child(bedrooms)

func show_room(room_id: String, announce: bool = true) -> void:
	var room: Dictionary = _room(room_id)
	if room.is_empty() or m.castle_room_background == null:
		return
	m.castle_room_id = room_id
	if m.castle_room_prop_sfx != null:
		m.castle_room_prop_sfx.stop()
	var hall_mode: bool = room_id == "main_hall"
	if not hall_mode:
		m.castle_room_background.texture = load(ROOM_ART + String(room["tex"]))
		m.castle_room_camera.position = Vector3(0.0, 0.0, CAMERA_DISTANCE)
		_build_room_background_tiles(room_id)
	else:
		_clear_room_background_tiles()
	_set_hall_background_visible(hall_mode)
	_rebuild_depth_layers(room_id)
	_rebuild_touch_items(room_id)
	m.castle_room_action_button.visible = not hall_mode
	if not hall_mode:
		StorybookUI.style_icon_button(m.castle_room_action_button,
			String(room["action_icon"]), "gold", Vector2(132.0, 132.0),
			String(room["name"]))
	_update_selected_buttons()
	if m.castle_room_menu_open:
		_toggle_menu()
	if hall_mode:
		for tile: Sprite3D in m.castle_room_background_tiles:
			tile.modulate.a = 0.25
			m.create_tween().tween_property(
				tile, "modulate:a", 1.0, 0.24)
	else:
		var fade := m.create_tween()
		for tile: Sprite3D in m.castle_room_detail_tiles:
			tile.modulate.a = 0.25
			fade.parallel().tween_property(
				tile, "modulate:a", 1.0, 0.24)
	_center_player()
	_update_hall_portals()
	_sync_hall_lighting()
	if announce:
		m._ui_tap()
		m.show_msg("Pearl Castle", String(room["name"]), "home")

func _room(room_id: String) -> Dictionary:
	for room: Dictionary in ROOMS:
		if String(room["id"]) == room_id:
			return room
	return {}

func _update_selected_buttons() -> void:
	for room_id_value: Variant in m.castle_room_buttons:
		var room_id := String(room_id_value)
		var button: Button = m.castle_room_buttons[room_id] as Button
		if button != null:
			StorybookUI.set_selected(button, room_id == m.castle_room_id)

func _toggle_menu() -> void:
	m._ui_tap()
	m.castle_room_menu_open = not m.castle_room_menu_open
	var elevator_pointer: Label = m.castle_room_stage.get_node_or_null("ElevatorPointer") as Label
	if elevator_pointer != null:
		elevator_pointer.visible = false
	if m.castle_room_menu_panel != null:
		m.castle_room_menu_panel.visible = m.castle_room_menu_open
		if m.castle_room_menu_open:
			m.castle_room_menu_panel.scale = Vector2(0.82, 0.82)
			m.castle_room_menu_panel.pivot_offset = m.castle_room_menu_panel.size * 0.5
			var pop := m.create_tween()
			pop.tween_property(m.castle_room_menu_panel, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _on_room_input(event: InputEvent) -> void:
	if m.castle_room_menu_open:
		return
	if event is InputEventMouseButton and (event as InputEventMouseButton).pressed:
		_walk_cutout_to((event as InputEventMouseButton).position)
	elif event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		_walk_cutout_to((event as InputEventScreenTouch).position)

func _walk_cutout_to(screen_position: Vector2) -> void:
	if m.castle_room_player_sprite == null:
		return
	var local_position: Vector2 = _screen_to_stage(screen_position)
	if _is_wide_hall():
		var hall_position: Vector2 = _stage_to_hall_art(local_position)
		var hall_foot := Vector2(
			clampf(hall_position.x, HALL_WALK.position.x, HALL_WALK.end.x),
			clampf(hall_position.y, HALL_WALK.position.y, HALL_WALK.end.y))
		_position_player_at_foot(hall_foot, true)
		return
	var layout: Dictionary = ROOM_LAYOUTS.get(m.castle_room_id, {})
	var walk: Rect2 = layout.get("walk", Rect2(170.0, 450.0, 940.0, 215.0))
	var foot_x: float = clampf(local_position.x, walk.position.x, walk.end.x)
	var foot_y: float = clampf(local_position.y, walk.position.y, walk.end.y)
	_position_player_at_foot(Vector2(foot_x, foot_y), true)

func _position_player_at_foot(foot: Vector2, tweened: bool) -> void:
	if m.castle_room_player_sprite == null:
		return
	if _is_wide_hall():
		_position_hall_player_at_foot(foot, tweened)
		return
	var layout: Dictionary = ROOM_LAYOUTS.get(m.castle_room_id, {})
	var walk: Rect2 = layout.get("walk", Rect2(170.0, 450.0, 940.0, 215.0))
	var depth: float = inverse_lerp(walk.position.y, walk.end.y, foot.y)
	var target_scale: float = lerpf(0.72, 1.05, depth)
	var player_z: float = _player_depth_for_foot(
		foot.y, walk, float(layout.get("mid_foot_y", -1.0)))
	var player_center := Vector2(foot.x,
		foot.y - PLAYER_STAGE_HEIGHT * target_scale * 0.5)
	var target_position: Vector3 = _stage_to_world(player_center, player_z)
	var texture_scale: float = _player_texture_scale()
	var target_sprite_scale := Vector3.ONE * texture_scale * target_scale
	var old_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", foot) as Vector2
	var current_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"current_stage_foot", old_foot) as Vector2
	var going_right: bool = foot.x >= old_foot.x
	m.castle_room_player_sprite.flip_h = not going_right
	var shadow: Sprite3D = _player_shadow()
	var shadow_z: float = player_z - 0.04
	var shadow_position: Vector3 = _stage_to_world(
		Vector2(foot.x, foot.y - 7.0), shadow_z)
	var shadow_scale := _shadow_scale(target_scale)
	var distance: float = old_foot.distance_to(foot)
	var duration: float = clampf(distance / 520.0, 0.12, 0.85)
	m.castle_room_player_sprite.set_meta("stage_foot", foot)
	m.castle_room_player_sprite.set_meta("depth_ratio", depth)
	m.castle_room_player_sprite.set_meta("walking", tweened)
	if not tweened:
		m.castle_room_player_sprite.position = target_position
		m.castle_room_player_sprite.scale = target_sprite_scale
		m.castle_room_player_sprite.pixel_size = _pixel_size_for_depth(player_z)
		if shadow != null:
			shadow.position = shadow_position
			shadow.scale = shadow_scale
			shadow.pixel_size = _pixel_size_for_depth(shadow_z)
		m.castle_room_player_sprite.set_meta("current_stage_foot", foot)
		m.castle_room_player_sprite.set_meta("walking", false)
		return
	var movement_tween := m.create_tween().set_parallel(true)
	movement_tween.tween_method(
		_set_player_current_foot, current_foot, foot, duration
	).set_trans(Tween.TRANS_SINE)
	movement_tween.tween_property(m.castle_room_player_sprite, "position",
		target_position, duration).set_trans(Tween.TRANS_SINE)
	movement_tween.tween_property(m.castle_room_player_sprite, "scale",
		target_sprite_scale, duration).set_trans(Tween.TRANS_SINE)
	movement_tween.tween_property(m.castle_room_player_sprite, "pixel_size",
		_pixel_size_for_depth(player_z), duration).set_trans(Tween.TRANS_SINE)
	if shadow != null:
		movement_tween.tween_property(shadow, "position", shadow_position,
			duration).set_trans(Tween.TRANS_SINE)
		movement_tween.tween_property(shadow, "scale", shadow_scale,
			duration).set_trans(Tween.TRANS_SINE)
		movement_tween.tween_property(shadow, "pixel_size",
			_pixel_size_for_depth(shadow_z), duration).set_trans(Tween.TRANS_SINE)
	movement_tween.chain().tween_callback(_finish_player_walk)

func _position_hall_player_at_foot(foot: Vector2, tweened: bool) -> void:
	var depth: float = inverse_lerp(
		HALL_WALK.position.y, HALL_WALK.end.y, foot.y)
	var target_scale: float = lerpf(0.72, 1.05, depth)
	var player_z: float = _player_depth_for_foot(
		foot.y, HALL_WALK, -1.0)
	var desired_art_height: float = HALL_PLAYER_STAGE_HEIGHT / HALL_STAGE_SCALE
	var player_center := Vector2(
		foot.x, foot.y - desired_art_height * target_scale * 0.5)
	var target_position: Vector3 = _hall_art_to_world(
		player_center, player_z)
	var texture_scale: float = _player_texture_scale()
	var target_sprite_scale := Vector3.ONE * texture_scale * target_scale
	var old_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", foot) as Vector2
	var current_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"current_stage_foot", old_foot) as Vector2
	m.castle_room_player_sprite.flip_h = foot.x < old_foot.x
	var shadow: Sprite3D = _player_shadow()
	var shadow_z: float = player_z - 0.04
	var shadow_position: Vector3 = _hall_art_to_world(
		Vector2(foot.x, foot.y - 7.0 / HALL_STAGE_SCALE), shadow_z)
	var shadow_scale := _shadow_scale(target_scale)
	var distance_stage: float = old_foot.distance_to(foot) * HALL_STAGE_SCALE
	var duration: float = clampf(distance_stage / 520.0, 0.12, 1.05)
	m.castle_room_player_sprite.set_meta("stage_foot", foot)
	m.castle_room_player_sprite.set_meta("depth_ratio", depth)
	m.castle_room_player_sprite.set_meta("walking", tweened)
	m.castle_room_player_sprite.set_meta("coordinate_space", "hall_art")
	if not tweened:
		m.castle_room_player_sprite.position = target_position
		m.castle_room_player_sprite.scale = target_sprite_scale
		m.castle_room_player_sprite.pixel_size = _pixel_size_for_depth(player_z)
		if shadow != null:
			shadow.position = shadow_position
			shadow.scale = shadow_scale
			shadow.pixel_size = _pixel_size_for_depth(shadow_z)
		m.castle_room_player_sprite.set_meta("current_stage_foot", foot)
		m.castle_room_player_sprite.set_meta("walking", false)
		return
	var movement_tween := m.create_tween().set_parallel(true)
	movement_tween.tween_method(
		_set_player_current_foot, current_foot, foot, duration
	).set_trans(Tween.TRANS_SINE)
	movement_tween.tween_property(
		m.castle_room_player_sprite, "position", target_position,
		duration).set_trans(Tween.TRANS_SINE)
	movement_tween.tween_property(
		m.castle_room_player_sprite, "scale", target_sprite_scale,
		duration).set_trans(Tween.TRANS_SINE)
	movement_tween.tween_property(
		m.castle_room_player_sprite, "pixel_size",
		_pixel_size_for_depth(player_z), duration).set_trans(Tween.TRANS_SINE)
	if shadow != null:
		movement_tween.tween_property(
			shadow, "position", shadow_position,
			duration).set_trans(Tween.TRANS_SINE)
		movement_tween.tween_property(
			shadow, "scale", shadow_scale,
			duration).set_trans(Tween.TRANS_SINE)
		movement_tween.tween_property(
			shadow, "pixel_size", _pixel_size_for_depth(shadow_z),
			duration).set_trans(Tween.TRANS_SINE)
	movement_tween.chain().tween_callback(_finish_player_walk)

func _center_player() -> void:
	if m.castle_room_player_sprite == null:
		return
	if _is_wide_hall():
		m.castle_room_player_sprite.flip_h = false
		_position_player_at_foot(Vector2(380.0, 835.0), false)
		m.castle_room_camera.position = Vector3(
			_hall_camera_x_for_foot(380.0), 0.0, CAMERA_DISTANCE)
		return
	var layout: Dictionary = ROOM_LAYOUTS.get(m.castle_room_id, {})
	var walk: Rect2 = layout.get("walk", Rect2(170.0, 450.0, 940.0, 215.0))
	var foot := Vector2(walk.get_center().x, walk.end.y - 20.0)
	m.castle_room_player_sprite.flip_h = false
	_position_player_at_foot(foot, false)

func _rebuild_depth_layers(room_id: String) -> void:
	for container: Node3D in [m.castle_room_mid_layer, m.castle_room_front_layer]:
		if container != null:
			for child: Node in container.get_children():
				child.free()
	if room_id == "main_hall":
		for piece_data: Dictionary in HALL_STRUCTURE_CARDS:
			_add_hall_structure_piece(piece_data)
		return
	var layout: Dictionary = ROOM_LAYOUTS.get(room_id, {})
	for piece_data: Dictionary in layout.get("mid", []):
		_add_layer_piece(m.castle_room_mid_layer, piece_data, MIDGROUND_Z)
	for piece_data: Dictionary in layout.get("front", []):
		_add_layer_piece(m.castle_room_front_layer, piece_data, FOREGROUND_Z)

func _add_hall_structure_piece(piece_data: Dictionary) -> void:
	if m.castle_room_mid_layer == null:
		return
	var texture: Texture2D = load(String(piece_data["tex_path"]))
	if texture == null:
		return
	var piece := _new_card(
		"HallStructure_" + String(piece_data["id"]), texture)
	var depth_z: float = float(piece_data["z"])
	piece.position = _hall_art_to_world(
		piece_data["pos"] as Vector2, depth_z)
	piece.pixel_size = _pixel_size_for_depth(depth_z)
	piece.scale = Vector3.ONE * float(piece_data.get("scale", 1.0))
	piece.shaded = bool(piece_data.get("shaded", false))
	piece.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	piece.set_meta("source_asset_role", String(piece_data["role"]))
	piece.set_meta("source_object_id",
		"main_hall:" + String(piece_data["id"]))
	piece.set_meta("depth_z", depth_z)
	m.castle_room_mid_layer.add_child(piece)

func _rebuild_touch_items(room_id: String) -> void:
	if m.castle_room_item_visual_layer != null:
		for child: Node in m.castle_room_item_visual_layer.get_children():
			child.free()
	if m.castle_room_item_hotspot_layer != null:
		for child: Node in m.castle_room_item_hotspot_layer.get_children():
			child.free()
	if m.castle_room_item_effect_layer != null:
		for child: Node in m.castle_room_item_effect_layer.get_children():
			child.free()
	m.castle_room_item_sprites.clear()
	var items: Array = []
	if room_id == "main_hall":
		items.append_array(HALL_ITEMS)
		items.append_array(HALL_DUST_BUNNY_SPAWNS)
	else:
		items = ROOM_ITEMS.get(room_id, [])
	for item_data_value: Variant in items:
		var item_data: Dictionary = item_data_value
		_add_touch_item(room_id, item_data)
	_update_touch_hotspots()

func _add_touch_item(room_id: String, item_data: Dictionary) -> void:
	if m.castle_room_item_visual_layer == null \
			or m.castle_room_item_hotspot_layer == null:
		return
	var item_id: String = String(item_data["id"])
	var bunny_role: String = String(item_data.get("dust_bunny_role", ""))
	if bunny_role != "":
		var cleared: Dictionary = m.g.get(
			"castle_dust_bunnies_cleared", {}) as Dictionary
		if bool(cleared.get(item_id, false)):
			return
	var texture_file: String = String(item_data.get(
		"tex", "room_" + room_id + "_item_" + item_id + ".png"))
	var texture_path: String = String(item_data.get(
		"tex_path", ROOM_ART + texture_file))
	var texture: Texture2D = load(texture_path)
	if texture == null:
		return
	var piece: Sprite3D = _new_card("Animated_" + item_id, texture)
	var source_position: Vector2 = item_data["pos"]
	var item_z: float = float(item_data.get("z", ITEM_Z))
	var visual_scale: float = float(item_data.get("scale", 1.0))
	if room_id == "main_hall":
		piece.position = _hall_art_to_world(source_position, item_z)
		piece.pixel_size = _pixel_size_for_depth(item_z)
		piece.scale = Vector3.ONE * visual_scale
		piece.set_meta("depth_z", item_z)
	else:
		_place_art_card(piece, source_position, item_z)
		piece.scale = Vector3.ONE * visual_scale
	piece.set_meta("source_asset_role", "unique_object")
	piece.set_meta("source_object_id", room_id + ":" + item_id)
	if bunny_role != "":
		piece.set_meta("dust_bunny_role", bunny_role)
		piece.set_meta("spawn_guide_id", item_id)
	piece.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
	if item_data.has("light_cluster"):
		if not m.castle_room_light_states.has(item_id):
			m.castle_room_light_states[item_id] = true
		_apply_sconce_visual(piece, bool(m.castle_room_light_states[item_id]))
	m.castle_room_item_visual_layer.add_child(piece)

	var hotspot: Button = null
	if not bool(item_data.get("proximity_only", false)):
		hotspot = Button.new()
		hotspot.name = "Touch_" + item_id
		hotspot.flat = true
		hotspot.focus_mode = Control.FOCUS_NONE
		hotspot.tooltip_text = String(item_data["name"])
		hotspot.set_meta("uses_own_sfx", true)
		var hotspot_offset: Vector2 = item_data.get(
			"hotspot_offset", Vector2.ZERO)
		hotspot.position = (source_position + hotspot_offset) * ART_TO_STAGE
		hotspot.size = item_data.get("hotspot_size", Vector2(112.0, 112.0))
		hotspot.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
		hotspot.pressed.connect(_activate_room_item.bind(item_id))
		m.castle_room_item_hotspot_layer.add_child(hotspot)
	var contact_offset: Vector2 = item_data.get(
		"contact_offset", Vector2.ZERO) as Vector2
	m.castle_room_item_sprites[item_id] = {
		"sprite": piece,
		"hotspot": hotspot,
		"data": item_data,
		"contact_foot": source_position + contact_offset,
		"art_rect": (
			Rect2(source_position - texture.get_size() * visual_scale * 0.5,
				texture.get_size() * visual_scale)
			if room_id == "main_hall"
			else Rect2(source_position, texture.get_size() * visual_scale)
		),
	}
	_update_touch_hotspot(m.castle_room_item_sprites[item_id])

func _activate_room_item(item_id: String) -> void:
	var record: Dictionary = m.castle_room_item_sprites.get(item_id, {})
	if record.is_empty():
		return
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	var item_data: Dictionary = record.get("data", {})
	if sprite == null or bool(sprite.get_meta("busy", false)):
		return
	if item_data.has("light_cluster"):
		_toggle_hall_sconce(item_id, sprite, item_data)
		return
	sprite.set_meta("busy", true)
	_play_item_sfx(String(item_data.get("sound", "ui_tap.ogg")),
		float(item_data.get("pitch", 1.0)))
	_item_burst(sprite.position,
		Color(item_data.get("color", StorybookUI.GOLD)), 6)
	_animate_item(sprite, String(item_data.get("anim", "pulse")))

func _toggle_hall_sconce(item_id: String, sprite: Sprite3D,
		item_data: Dictionary) -> void:
	var now_on: bool = not bool(m.castle_room_light_states.get(item_id, true))
	m.castle_room_light_states[item_id] = now_on
	sprite.set_meta("busy", true)
	_apply_sconce_visual(sprite, now_on)
	_play_item_sfx(String(item_data.get("sound", "chime.ogg")),
		float(item_data.get("pitch", 1.0)) * (1.0 if now_on else 0.82))
	_animate_item(sprite, "light")
	_sync_hall_lighting()

func _apply_sconce_visual(sprite: Sprite3D, is_on: bool) -> void:
	if sprite == null:
		return
	# Values above 1.0 make the pearl itself feed the Environment glow buffer.
	# The same accepted fixture texture remains on the same card; no button-like
	# halo sprite, extra transparent card, or per-frame material is introduced.
	sprite.modulate = Color(1.30, 1.14, 0.90, 1.0) \
		if is_on else Color(0.36, 0.34, 0.44, 0.48)
	sprite.set_meta("castle_light_on", is_on)
	sprite.set_meta("castle_bloom_emitter", is_on)

func _sync_hall_lighting() -> void:
	if m.castle_room_light_nodes.is_empty():
		return
	var hall_visible: bool = is_open() and m.castle_room_id == "main_hall"
	var visible_half := "a"
	if m.castle_room_camera != null and m.castle_room_camera.position.x >= 0.0:
		visible_half = "b"
	var half_fixture_count := 0
	var half_lit_count := 0
	for item_data: Dictionary in HALL_ITEMS:
		if not item_data.has("light_cluster"):
			continue
		var cluster_half := ""
		var item_cluster: String = String(item_data["light_cluster"])
		for cluster_data: Dictionary in HALL_LIGHT_CLUSTERS:
			if String(cluster_data["id"]) == item_cluster:
				cluster_half = String(cluster_data["half"])
				break
		if cluster_half != visible_half:
			continue
		half_fixture_count += 1
		if bool(m.castle_room_light_states.get(
				String(item_data["id"]), true)):
			half_lit_count += 1
	var half_light_ratio: float = float(half_lit_count) \
		/ maxf(1.0, float(half_fixture_count))
	var speedy_shadow_used := false
	for light: Light3D in m.castle_room_light_nodes:
		if light == null or not is_instance_valid(light):
			continue
		var role: String = String(light.get_meta("castle_light_role", ""))
		if role == "ambient_fill":
			light.visible = hall_visible
			light.light_energy = lerpf(
				HALL_FILL_OFF_ENERGY, HALL_FILL_ENERGY, half_light_ratio)
			continue
		var cluster_id: String = String(light.get_meta("cluster_id", ""))
		var fixture_count := 0
		var lit_count := 0
		for item_data: Dictionary in HALL_ITEMS:
			if String(item_data.get("light_cluster", "")) != cluster_id:
				continue
			fixture_count += 1
			if bool(m.castle_room_light_states.get(
					String(item_data["id"]), true)):
				lit_count += 1
		var energy_ratio: float = float(lit_count) / maxf(1.0, float(fixture_count))
		var half_matches: bool = String(
			light.get_meta("hall_half", "")) == visible_half
		light.visible = hall_visible and half_matches and lit_count > 0
		var max_energy: float = float(light.get_meta("max_energy", 2.5))
		light.light_energy = lerpf(0.55, max_energy, energy_ratio)
		if not light.visible:
			light.shadow_enabled = false
		elif m.quality == "speedy":
			light.shadow_enabled = not speedy_shadow_used
			speedy_shadow_used = true
		else:
			light.shadow_enabled = true
	_sync_castle_environment(hall_visible, half_light_ratio)

func _sync_castle_environment(hall_visible: bool,
		half_light_ratio: float) -> void:
	var environment: Environment = m.castle_room_environment
	if environment == null:
		return
	var speedy: bool = m.quality == "speedy"
	if hall_visible:
		var glow_target: float = HALL_GLOW_SPEEDY if speedy else HALL_GLOW_FULL
		var bloom_target: float = HALL_BLOOM_SPEEDY if speedy \
			else HALL_BLOOM_FULL
		environment.glow_intensity = lerpf(
			HALL_GLOW_OFF, glow_target, half_light_ratio)
		environment.glow_bloom = lerpf(
			HALL_BLOOM_OFF, bloom_target, half_light_ratio)
		environment.glow_hdr_threshold = lerpf(
			0.98, 0.74, half_light_ratio)
		environment.ambient_light_energy = lerpf(
			0.12, 0.22, half_light_ratio)
		environment.adjustment_contrast = lerpf(
			1.12, 1.20, half_light_ratio)
		environment.adjustment_brightness = lerpf(
			0.84, 0.91, half_light_ratio)
	else:
		# Destination rooms keep the castle's warm storybook finish, but their
		# painted practical lights do not receive the Main Hall's dramatic lift.
		environment.glow_intensity = 0.48 if speedy else 0.66
		environment.glow_bloom = 0.055 if speedy else 0.09
		environment.glow_hdr_threshold = 0.90
		environment.ambient_light_energy = 0.28
		environment.adjustment_contrast = 1.10
		environment.adjustment_brightness = 0.94

func _play_item_sfx(sound_file: String, pitch: float) -> void:
	if m.castle_room_prop_sfx == null:
		return
	var path := "res://assets/audio/" + sound_file
	if not ResourceLoader.exists(path):
		return
	m.castle_room_prop_sfx.stream = load(path)
	m.castle_room_prop_sfx.pitch_scale = pitch
	m.castle_room_prop_sfx.play()

func _animate_item(sprite: Sprite3D, animation: String) -> void:
	var origin_position: Vector3 = sprite.position
	var origin_scale: Vector3 = sprite.scale
	var origin_rotation: float = sprite.rotation.z
	var lift: float = _stage_distance_to_world(18.0, sprite.position.z)
	var tween := sprite.create_tween()
	match animation:
		"light":
			tween.tween_property(sprite, "scale",
				origin_scale * Vector3(1.035, 1.035, 1.0),
				0.12).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
			tween.tween_property(sprite, "scale", origin_scale,
				0.16).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		"wiggle":
			tween.tween_property(sprite, "rotation:z", origin_rotation - 0.10, 0.10)
			tween.tween_property(sprite, "rotation:z", origin_rotation + 0.12, 0.16)
			tween.tween_property(sprite, "rotation:z", origin_rotation, 0.12)
		"bounce":
			tween.tween_property(sprite, "position:y", origin_position.y + lift,
				0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			tween.tween_property(sprite, "position:y", origin_position.y, 0.22).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
		"hover":
			tween.tween_property(sprite, "position:y",
				origin_position.y + lift * 0.84, 0.28).set_trans(
				Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
			tween.tween_property(sprite, "position:y", origin_position.y, 0.34).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		"spin":
			tween.tween_property(sprite, "rotation:z", origin_rotation + TAU,
				0.65).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
		"sway":
			tween.tween_property(sprite, "rotation:z", origin_rotation - 0.055,
				0.17).set_trans(Tween.TRANS_SINE)
			tween.tween_property(sprite, "rotation:z", origin_rotation + 0.055,
				0.28).set_trans(Tween.TRANS_SINE)
			tween.tween_property(sprite, "rotation:z", origin_rotation,
				0.17).set_trans(Tween.TRANS_SINE)
		"splash":
			tween.tween_property(sprite, "scale",
				origin_scale * Vector3(1.04, 0.94, 1.0),
				0.13).set_trans(Tween.TRANS_SINE)
			tween.tween_property(sprite, "scale",
				origin_scale * Vector3(0.98, 1.05, 1.0),
				0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			tween.tween_property(sprite, "scale", origin_scale, 0.18).set_trans(Tween.TRANS_SINE)
		_:
			tween.tween_property(sprite, "scale", origin_scale * 1.10, 0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			tween.tween_property(sprite, "scale", origin_scale, 0.22).set_trans(Tween.TRANS_SINE)
	tween.tween_callback(_finish_item_animation.bind(
		sprite, origin_position, origin_scale, origin_rotation))

func _finish_item_animation(sprite: Sprite3D, origin_position: Vector3,
		origin_scale: Vector3, origin_rotation: float) -> void:
	if not is_instance_valid(sprite):
		return
	sprite.position = origin_position
	sprite.scale = origin_scale
	sprite.rotation.z = origin_rotation
	sprite.set_meta("busy", false)

func _item_burst(center: Vector3, color: Color, count: int) -> void:
	if m.castle_room_item_effect_layer == null:
		return
	var star_texture: Texture2D = load("res://assets/mg/star.png")
	for index in range(count):
		var mote: Sprite3D = _new_card("TouchSparkle", star_texture)
		mote.set_meta("source_asset_role", "transient_effect")
		mote.pixel_size = _pixel_size_for_depth(EFFECT_Z)
		mote.scale = Vector3.ONE * randf_range(0.018, 0.032)
		mote.modulate = color
		mote.position = Vector3(
			center.x + randf_range(-0.75, 0.75),
			center.y + randf_range(-0.20, 0.35),
			EFFECT_Z)
		m.castle_room_item_effect_layer.add_child(mote)
		var drift := mote.create_tween().set_parallel(true)
		drift.tween_property(mote, "position", mote.position + Vector3(
			randf_range(-0.45, 0.45),
			1.0 + float(index % 3) * 0.16, 0.0), 0.72)
		drift.tween_property(mote, "modulate:a", 0.0, 0.72)
		drift.chain().tween_callback(mote.queue_free)

func _add_layer_piece(container: Node3D, piece_data: Dictionary,
		depth_z: float) -> void:
	if container == null:
		return
	var texture: Texture2D = load(ROOM_ART + String(piece_data["tex"]))
	if texture == null:
		return
	var piece: Sprite3D = _new_card(
		String(piece_data["tex"]).get_basename(), texture)
	var piece_position: Vector2 = piece_data["pos"]
	_place_art_card(piece, piece_position, depth_z)
	piece.set_meta("source_asset_role",
		"foreground_region" if depth_z >= FOREGROUND_Z else "midground_region")
	container.add_child(piece)

func _update_depth_sort() -> void:
	if m.castle_room_player_sprite == null:
		return
	if bool(m.castle_room_player_sprite.get_meta("walking", false)):
		return
	var foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", Vector2(640.0, 640.0)) as Vector2
	_position_player_at_foot(foot, false)

func _player_shadow() -> Sprite3D:
	return m.castle_room_player_shadow

func _new_card(card_name: String, texture: Texture2D) -> Sprite3D:
	var card := Sprite3D.new()
	card.name = card_name
	card.texture = texture
	card.centered = true
	card.shaded = false
	card.no_depth_test = false
	card.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	card.alpha_cut = SpriteBase3D.ALPHA_CUT_OPAQUE_PREPASS
	card.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	card.set_meta("castle_world_sprite3d", true)
	return card

func _place_art_card(card: Sprite3D, source_position: Vector2,
		depth_z: float) -> void:
	if card == null or card.texture == null:
		return
	var texture_size: Vector2 = card.texture.get_size()
	var center_art: Vector2 = source_position + texture_size * 0.5
	card.position = _art_to_world(center_art, depth_z)
	card.pixel_size = _pixel_size_for_depth(depth_z)
	card.set_meta("source_art_rect", Rect2(source_position, texture_size))
	card.set_meta("depth_z", depth_z)

func _pixel_size_for_depth(depth_z: float) -> float:
	var projection_ratio: float = (CAMERA_DISTANCE - depth_z) / CAMERA_DISTANCE
	var base_pixel_size: float = HALL_CARD_PIXEL_SIZE \
		if _is_wide_hall() else CARD_PIXEL_SIZE
	return base_pixel_size * maxf(0.1, projection_ratio)

func _art_to_world(art_position: Vector2, depth_z: float) -> Vector3:
	var projection_ratio: float = (CAMERA_DISTANCE - depth_z) / CAMERA_DISTANCE
	var base_position := Vector2(
		(art_position.x - ART_SIZE.x * 0.5) * CARD_PIXEL_SIZE,
		(ART_SIZE.y * 0.5 - art_position.y) * CARD_PIXEL_SIZE)
	return Vector3(base_position.x * projection_ratio,
		base_position.y * projection_ratio, depth_z)

func _hall_art_to_world(art_position: Vector2, depth_z: float) -> Vector3:
	var projection_ratio: float = (CAMERA_DISTANCE - depth_z) / CAMERA_DISTANCE
	var base_position := Vector2(
		(art_position.x - HALL_LOGICAL_SIZE.x * 0.5)
			* HALL_CARD_PIXEL_SIZE,
		(HALL_VIEW_SIZE.y * 0.5 - art_position.y)
			* HALL_CARD_PIXEL_SIZE)
	var camera_anchor_x: float = _hall_camera_x_for_foot(art_position.x)
	return Vector3(
		camera_anchor_x
			+ (base_position.x - camera_anchor_x) * projection_ratio,
		base_position.y * projection_ratio,
		depth_z)

func _stage_to_world(stage_position: Vector2, depth_z: float) -> Vector3:
	return _art_to_world(stage_position / ART_TO_STAGE, depth_z)

func _stage_to_hall_art(stage_position: Vector2) -> Vector2:
	var camera_center_art: float = HALL_LOGICAL_SIZE.x * 0.5
	if m.castle_room_camera != null:
		camera_center_art += m.castle_room_camera.position.x \
			/ HALL_CARD_PIXEL_SIZE
	var view_left: float = camera_center_art - HALL_VIEW_SIZE.x * 0.5
	return Vector2(
		view_left + stage_position.x / HALL_STAGE_SCALE,
		stage_position.y / HALL_STAGE_SCALE)

func _hall_camera_x_for_foot(foot_x: float) -> float:
	var center_art: float = clampf(
		foot_x, HALL_VIEW_SIZE.x * 0.5,
		HALL_LOGICAL_SIZE.x - HALL_VIEW_SIZE.x * 0.5)
	return (center_art - HALL_LOGICAL_SIZE.x * 0.5) \
		* HALL_CARD_PIXEL_SIZE

func _is_wide_hall() -> bool:
	return m.castle_room_id == "main_hall"

func _screen_to_stage(screen_position: Vector2) -> Vector2:
	if m.castle_room_stage == null:
		return screen_position
	return m.castle_room_stage.get_global_transform_with_canvas().affine_inverse() \
		* screen_position

func _stage_distance_to_world(stage_distance: float, depth_z: float) -> float:
	var stage_scale: float = HALL_STAGE_SCALE \
		if _is_wide_hall() else ART_TO_STAGE
	return stage_distance / stage_scale * _pixel_size_for_depth(depth_z)

func _player_texture_scale() -> float:
	if m.castle_room_player_sprite == null \
			or m.castle_room_player_sprite.texture == null:
		return 1.0
	var stage_scale: float = HALL_STAGE_SCALE \
		if _is_wide_hall() else ART_TO_STAGE
	var desired_stage_height: float = HALL_PLAYER_STAGE_HEIGHT \
		if _is_wide_hall() else PLAYER_STAGE_HEIGHT
	var desired_art_height: float = desired_stage_height / stage_scale
	var frame_height: float = \
		m.castle_room_player_sprite.texture.get_height() \
		/ float(maxi(1, m.castle_room_player_sprite.vframes))
	return desired_art_height \
		/ maxf(1.0, frame_height)

func _player_depth_for_foot(foot_y: float, walk: Rect2,
		mid_foot_y: float) -> float:
	if mid_foot_y > walk.position.y and mid_foot_y < walk.end.y:
		if foot_y < mid_foot_y:
			return lerpf(PLAYER_BACK_Z, MIDGROUND_Z - 0.02,
				inverse_lerp(walk.position.y, mid_foot_y, foot_y))
		return lerpf(MIDGROUND_Z + 0.02, PLAYER_FRONT_Z,
			inverse_lerp(mid_foot_y, walk.end.y, foot_y))
	return lerpf(PLAYER_BACK_Z, PLAYER_FRONT_Z,
		inverse_lerp(walk.position.y, walk.end.y, foot_y))

func _shadow_scale(depth_scale: float) -> Vector3:
	if m.castle_room_player_shadow == null \
			or m.castle_room_player_shadow.texture == null:
		return Vector3.ONE
	var texture_size: Vector2 = m.castle_room_player_shadow.texture.get_size()
	var stage_scale: float = HALL_STAGE_SCALE \
		if _is_wide_hall() else ART_TO_STAGE
	var desired_art_size: Vector2 = SHADOW_STAGE_SIZE / stage_scale
	return Vector3(
		desired_art_size.x / maxf(1.0, texture_size.x) * depth_scale,
		desired_art_size.y / maxf(1.0, texture_size.y) * depth_scale,
		1.0)

func _set_player_current_foot(foot: Vector2) -> void:
	if m.castle_room_player_sprite != null \
			and is_instance_valid(m.castle_room_player_sprite):
		m.castle_room_player_sprite.set_meta("current_stage_foot", foot)

func _finish_player_walk() -> void:
	if m.castle_room_player_sprite != null \
			and is_instance_valid(m.castle_room_player_sprite):
		var foot: Vector2 = m.castle_room_player_sprite.get_meta(
			"stage_foot", Vector2.ZERO) as Vector2
		m.castle_room_player_sprite.set_meta("current_stage_foot", foot)
		m.castle_room_player_sprite.set_meta("walking", false)

func _update_dust_bunny_runner(delta: float) -> void:
	if not _is_wide_hall() or delta <= 0.0:
		return
	var runner_record: Dictionary = m.castle_room_item_sprites.get(
		"runner_bunny", {}) as Dictionary
	if runner_record.is_empty():
		return
	var runner_sprite: Sprite3D = runner_record.get("sprite") as Sprite3D
	var runner_data: Dictionary = runner_record.get("data", {}) as Dictionary
	if runner_sprite == null or not is_instance_valid(runner_sprite):
		return
	var elapsed: float = float(m.g.get(
		"castle_dust_bunny_runner_time", 0.0)) + delta
	m.g["castle_dust_bunny_runner_time"] = elapsed
	var patrol_x: Vector2 = runner_data.get(
		"patrol_x", Vector2(1820.0, 2580.0)) as Vector2
	var run_speed: float = float(runner_data.get("run_speed", 220.0))
	var segment_length: float = maxf(1.0, patrol_x.y - patrol_x.x)
	var travel: float = fposmod(elapsed * run_speed, segment_length * 2.0)
	var moving_right: bool = travel <= segment_length
	var runner_x: float = patrol_x.x + travel if moving_right \
		else patrol_x.y - (travel - segment_length)
	var source_position: Vector2 = runner_data.get(
		"pos", Vector2(1820.0, 790.0)) as Vector2
	var runner_center := Vector2(
		runner_x, source_position.y + absf(sin(elapsed * 8.0)) * 14.0)
	var depth_z: float = float(runner_data.get("z", 2.85))
	runner_sprite.position = _hall_art_to_world(runner_center, depth_z)
	runner_sprite.pixel_size = _pixel_size_for_depth(depth_z)
	runner_sprite.flip_h = not moving_right
	var contact_offset: Vector2 = runner_data.get(
		"contact_offset", Vector2.ZERO) as Vector2
	runner_record["contact_foot"] = runner_center + contact_offset
	var card_size: Vector2 = runner_sprite.texture.get_size() \
		* float(runner_data.get("scale", 1.0))
	runner_record["art_rect"] = Rect2(
		runner_center - card_size * 0.5, card_size)
	runner_record["runner_direction"] = 1.0 if moving_right else -1.0
	m.castle_room_item_sprites["runner_bunny"] = runner_record

func _check_dust_bunny_contacts() -> void:
	if not _is_wide_hall() or m.castle_room_player_sprite == null:
		return
	var player_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"current_stage_foot",
		m.castle_room_player_sprite.get_meta("stage_foot", Vector2.ZERO)
	) as Vector2
	var touched_ids: Array[String] = []
	for item_id_value: Variant in m.castle_room_item_sprites:
		var item_id: String = String(item_id_value)
		var record: Dictionary = m.castle_room_item_sprites[item_id] as Dictionary
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if String(item_data.get("dust_bunny_role", "")) == "":
			continue
		var contact_foot: Vector2 = record.get(
			"contact_foot", Vector2(-10000.0, -10000.0)) as Vector2
		var contact_radius: Vector2 = item_data.get(
			"contact_radius", Vector2(120.0, 88.0)) as Vector2
		var contact_delta: Vector2 = player_foot - contact_foot
		var normalized_distance: float = (
			contact_delta.x * contact_delta.x
				/ maxf(1.0, contact_radius.x * contact_radius.x)
			+ contact_delta.y * contact_delta.y
				/ maxf(1.0, contact_radius.y * contact_radius.y)
		)
		if normalized_distance <= 1.0:
			touched_ids.append(item_id)
	for item_id: String in touched_ids:
		_explode_dust_bunny(item_id)

func _explode_dust_bunny(item_id: String) -> void:
	var record: Dictionary = m.castle_room_item_sprites.get(
		item_id, {}) as Dictionary
	if record.is_empty():
		return
	var item_data: Dictionary = record.get("data", {}) as Dictionary
	if String(item_data.get("dust_bunny_role", "")) == "":
		return
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite == null or not is_instance_valid(sprite) \
			or bool(sprite.get_meta("exploding", false)):
		return
	var cleared: Dictionary = m.g.get(
		"castle_dust_bunnies_cleared", {}) as Dictionary
	if bool(cleared.get(item_id, false)):
		return
	cleared[item_id] = true
	m.g["castle_dust_bunnies_cleared"] = cleared
	sprite.set_meta("exploding", true)
	var hotspot: Button = record.get("hotspot") as Button
	if hotspot != null and is_instance_valid(hotspot):
		hotspot.visible = false
		hotspot.disabled = true
		hotspot.queue_free()
	m.castle_room_item_sprites.erase(item_id)
	_play_item_sfx(String(item_data.get("sound", "hop_boing.ogg")),
		float(item_data.get("pitch", 1.5)))
	var burst_color := Color(item_data.get("color", StorybookUI.GOLD))
	_item_burst(sprite.position, burst_color, 12)
	var origin_scale: Vector3 = sprite.scale
	var fade_color: Color = sprite.modulate
	fade_color.a = 0.0
	var vanish := sprite.create_tween().set_parallel(true)
	vanish.tween_property(sprite, "scale", origin_scale * 1.45,
		0.24).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	vanish.tween_property(sprite, "rotation:z", sprite.rotation.z + 0.42,
		0.24).set_trans(Tween.TRANS_SINE)
	vanish.tween_property(sprite, "modulate", fade_color, 0.24)
	vanish.chain().tween_callback(sprite.queue_free)


func _update_camera_parallax(delta: float) -> void:
	if m.castle_room_camera == null or m.castle_room_player_sprite == null:
		return
	var foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", StorybookUI.CANVAS_SIZE * 0.5) as Vector2
	if _is_wide_hall():
		var hall_target := Vector3(
			_hall_camera_x_for_foot(foot.x),
			(0.5 - foot.y / HALL_VIEW_SIZE.y) * 0.045,
			CAMERA_DISTANCE)
		var hall_weight: float = clampf(delta * 3.5, 0.0, 1.0)
		m.castle_room_camera.position = m.castle_room_camera.position.lerp(
			hall_target, hall_weight)
		return
	var target := Vector3(
		(foot.x / StorybookUI.CANVAS_SIZE.x - 0.5) * 0.08,
		(0.5 - foot.y / StorybookUI.CANVAS_SIZE.y) * 0.035,
		CAMERA_DISTANCE)
	var weight: float = clampf(delta * 3.5, 0.0, 1.0)
	m.castle_room_camera.position = m.castle_room_camera.position.lerp(
		target, weight)

func _update_touch_hotspots() -> void:
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[item_id_value]
		_update_touch_hotspot(record)

func _update_touch_hotspot(record: Dictionary) -> void:
	if m.castle_room_camera == null or m.castle_room_stage == null:
		return
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	var hotspot: Button = record.get("hotspot") as Button
	if sprite == null or hotspot == null or sprite.texture == null:
		return
	if m.castle_room_camera.is_position_behind(sprite.global_position):
		hotspot.visible = false
		return
	hotspot.visible = true
	var center_screen: Vector2 = m.castle_room_camera.unproject_position(
		sprite.global_position)
	var texture_size: Vector2 = sprite.texture.get_size()
	var half_x_world: Vector3 = sprite.global_transform.basis.x \
		* (texture_size.x * sprite.pixel_size * 0.5)
	var half_y_world: Vector3 = sprite.global_transform.basis.y \
		* (texture_size.y * sprite.pixel_size * 0.5)
	var edge_x_screen: Vector2 = m.castle_room_camera.unproject_position(
		sprite.global_position + half_x_world)
	var edge_y_screen: Vector2 = m.castle_room_camera.unproject_position(
		sprite.global_position + half_y_world)
	var center_stage: Vector2 = _screen_to_stage(center_screen)
	var edge_x_stage: Vector2 = _screen_to_stage(edge_x_screen)
	var edge_y_stage: Vector2 = _screen_to_stage(edge_y_screen)
	var hit_size := Vector2(
		maxf(112.0, absf(edge_x_stage.x - center_stage.x) * 2.0 + 34.0),
		maxf(112.0, absf(edge_y_stage.y - center_stage.y) * 2.0 + 34.0))
	var hit_position: Vector2 = center_stage - hit_size * 0.5
	hit_position.x = clampf(hit_position.x, 0.0,
		StorybookUI.CANVAS_SIZE.x - hit_size.x)
	hit_position.y = clampf(hit_position.y, 0.0,
		StorybookUI.CANVAS_SIZE.y - hit_size.y)
	hotspot.position = hit_position
	hotspot.size = hit_size

func _update_hall_portals() -> void:
	if m.castle_room_door_hotspot_layer == null:
		return
	var hall_visible: bool = _is_wide_hall() and is_open()
	m.castle_room_door_hotspot_layer.visible = hall_visible
	if not hall_visible or m.castle_room_camera == null \
			or m.castle_room_world_root == null:
		return
	for record: Dictionary in m.castle_room_door_hotspots:
		var button: Button = record.get("button") as Button
		var portal_data: Dictionary = record.get("data", {})
		if button == null or portal_data.is_empty():
			continue
		var art_rect: Rect2 = portal_data["rect"]
		var world_top_left: Vector3 = m.castle_room_world_root.to_global(
			_hall_art_to_world(art_rect.position, BACKGROUND_Z))
		var world_bottom_right: Vector3 = m.castle_room_world_root.to_global(
			_hall_art_to_world(art_rect.end, BACKGROUND_Z))
		var stage_top_left: Vector2 = _screen_to_stage(
			m.castle_room_camera.unproject_position(world_top_left))
		var stage_bottom_right: Vector2 = _screen_to_stage(
			m.castle_room_camera.unproject_position(world_bottom_right))
		var left: float = minf(stage_top_left.x, stage_bottom_right.x)
		var top: float = minf(stage_top_left.y, stage_bottom_right.y)
		var right: float = maxf(stage_top_left.x, stage_bottom_right.x)
		var bottom: float = maxf(stage_top_left.y, stage_bottom_right.y)
		var projected := Rect2(left, top, right - left, bottom - top)
		var canvas_rect := Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
		button.visible = projected.intersects(canvas_rect)
		if button.visible:
			var clipped: Rect2 = projected.intersection(canvas_rect)
			button.position = clipped.position
			button.size = Vector2(
				maxf(112.0, clipped.size.x),
				maxf(112.0, clipped.size.y))

func _enter_hall_portal(portal_id: String, foot: Vector2) -> void:
	if not _is_wide_hall() or m.castle_room_menu_open:
		return
	m._ui_tap()
	var old_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", foot) as Vector2
	var duration: float = clampf(
		old_foot.distance_to(foot) * HALL_STAGE_SCALE / 520.0,
		0.12, 1.05)
	_position_player_at_foot(foot, true)
	var transition := m.create_tween()
	transition.tween_interval(duration + 0.04)
	if portal_id == "__throne":
		transition.tween_callback(activate_current_room)
	else:
		transition.tween_callback(show_room.bind(portal_id, true))

func activate_current_room() -> void:
	var room: Dictionary = _room(m.castle_room_id)
	var action: String = String(room.get("action", ""))
	m._ui_tap()
	match action:
		"opera":
			suspend()
			m._start_opera()
		"craft":
			m._open_craft_studio()
		"stuffies":
			m._companion_ref().open_picker(true)
		"throne":
			if bool(m.g.get("crown_won", false)):
				m.show_msg("Roshan", "A royal wave from the throne!", "win")
				_burst("✦", Color(1.0, 0.78, 0.30))
			else:
				_award_crown()
		"kitchen":
			m.show_msg("Roshan", "Something delicious is bubbling!", "talk")
			_burst("♡", Color(1.0, 0.50, 0.48))
		"library":
			m.show_msg("Roshan", "A whole room of storybooks!", "talk")
			_burst("✦", Color(0.52, 0.94, 0.78))
		"pool":
			m.show_msg("Roshan", "Splash in the mermaid pool!", "win")
			_burst("○", Color(0.45, 0.90, 1.0))
		"bath":
			m.show_msg("Roshan", "Bubble party in the royal bath!", "win")
			_burst("○", Color(0.66, 0.92, 1.0))

func _award_crown() -> void:
	if bool(m.g.get("crown_won", false)):
		return
	m.g["crown_won"] = true
	m.level2_done_once = true
	m._write_save()
	if m.voice != null:
		m.voice.pitch_scale = 1.15
		m.voice.play()
	_burst("★", Color(1.0, 0.78, 0.30))
	m.show_msg("Pearl Castle",
		"The Crown Star is yours! This castle is YOURS now — explore every room!",
		"win")

func _burst(_symbol: String, color: Color) -> void:
	if m.castle_room_item_effect_layer == null:
		return
	_item_burst(_stage_to_world(Vector2(640.0, 500.0), EFFECT_Z),
		color, 9)

func _exit_to_courtyard() -> void:
	m._ui_tap()
	close()
	m._return_to_courtyard()
