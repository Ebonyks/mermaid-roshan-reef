class_name CastleRooms25D
extends RefCounted
# Picture-first Pearl Castle room shell. Every in-world image is a Sprite3D
# card at real scene depth. Main Hall background tiles are the sole shaded
# receiver exception for its touch-controlled light pool; characters, props,
# and effects remain unshaded. Controls are reserved for touch routing, the
# single contextual Back control, and other interface chrome. No model or mesh art is
# created or loaded by this satellite.

const ROOM_ART := "res://assets/flats/castle/rooms/"
const INTERACTION_ART := "res://assets/flats/castle/interactions/"
const DREAM_HOUSE_ART := "res://assets/flats/castle/dream_house/"
const ROOM_TILE_ROOT := ROOM_ART + "background_tiles/"
const HALL_TILE_ROOT := "res://assets/flats/castle/main_hall_2screen/tiles/"
const HALL_ART_ROOT := "res://assets/flats/castle/main_hall_2screen/"
const CASTLE_PORTAL_CUTOUT_SHADER := preload(
	"res://shaders/castle_portal_cutout.gdshader")
const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")
const CASTLE_FIXTURE_BLOOM_SHADER := preload(
	"res://shaders/castle_fixture_bloom.gdshader")
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
const ROOM_BACKGROUND_GRIDS := {
	"kitchen": {
		"rows": 3,
		"columns": 4,
		"native_size": Vector2(1024.0, 768.0),
		"logical_size": Vector2(256.0, 192.0),
		"pixel_size": CARD_PIXEL_SIZE * 0.25,
		"source_grid": "3x4_4k",
	},
}
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
const HALL_FILL_COLOR := Color(0.78, 0.72, 0.94)
const HALL_FILL_ENERGY := 0.78
const HALL_FILL_OFF_ENERGY := 0.42
const HALL_SCONCE_COLOR := Color(1.0, 0.74, 0.43)
const HALL_GLOW_FULL := 1.28
const HALL_GLOW_SPEEDY := 0.95
const HALL_BLOOM_FULL := 0.30
const HALL_BLOOM_SPEEDY := 0.18
const HALL_GLOW_OFF := 0.24
const HALL_BLOOM_OFF := 0.015
const HALL_SCREEN_SOURCE_RECTS: Array[Rect2] = [
	Rect2(376.0, 212.0, 1672.0, 941.0),
	Rect2(376.0, 147.0, 1672.0, 941.0),
]
const HALL_TILE_FILES: Array[String] = [
	"runtime_bleed/main_hall_room_led_r0_c0_bleed.png",
	"runtime_bleed/main_hall_room_led_r0_c1_bleed.png",
	"runtime_bleed/main_hall_room_led_r0_c2_bleed.png",
	"runtime_bleed/main_hall_room_led_r0_c3_bleed.png",
	"runtime_bleed/main_hall_room_led_r1_c0_bleed.png",
	"runtime_bleed/main_hall_room_led_r1_c1_bleed.png",
	"runtime_bleed/main_hall_room_led_r1_c2_bleed.png",
	"runtime_bleed/main_hall_room_led_r1_c3_bleed.png",
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
	{"id": "family_wing_entry", "pos": Vector2(220.0, 470.0),
		"z": 0.01, "scale": 1.0, "shaded": false,
		"tex_path": DREAM_HOUSE_ART + "family_wing_hall_insert.png",
		"role": "registered_family_gallery_door"},
	{"id": "playroom_portal_bridge", "pos": Vector2(1672.0, 490.0),
		"z": 0.01, "scale": 0.96, "shaded": false,
		"tex_path": HALL_ART_ROOT + "castle_playroom_portal_cutout_reuse.png",
		"shader": "portal_cutout",
		"role": "registered_playroom_door"},
	{"id": "playroom_portal_marker", "pos": Vector2(1672.0, 376.0),
		"z": 0.68, "scale": 0.15, "shaded": false,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_family.png",
		"role": "playroom_door_marker"},
]
const HALL_PORTALS: Array[Dictionary] = [
	# Rects trace the painted doorway frames (arch band + posts) in hall art
	# pixels, measured from the composited main_hall_2screen tiles. Floating
	# room plaques above each arch are deliberately excluded.
	{"id": "family_gallery", "name": "Dream House Wing",
		"rect": Rect2(115.0, 310.0, 220.0, 420.0),
		"foot": Vector2(220.0, 720.0)},
	{"id": "opera_hall", "name": "Opera Hall",
		"rect": Rect2(455.0, 105.0, 375.0, 510.0),
		"foot": Vector2(630.0, 650.0)},
	{"id": "library", "name": "Royal Library",
		"rect": Rect2(1030.0, 318.0, 215.0, 290.0),
		"foot": Vector2(1135.0, 660.0)},
	{"id": "kitchen", "name": "Royal Kitchen",
		"rect": Rect2(1288.0, 320.0, 180.0, 290.0),
		"foot": Vector2(1395.0, 660.0)},
	{"id": "playroom", "name": "Stuffie Playroom",
		"rect": Rect2(1577.0, 319.0, 187.0, 325.0),
		"foot": Vector2(1672.0, 670.0)},
	{"id": "craft_room", "name": "Craft Room",
		"rect": Rect2(1985.0, 325.0, 225.0, 280.0),
		"foot": Vector2(2095.0, 670.0)},
	{"id": "mermaid_pool", "name": "Mermaid Pool",
		"rect": Rect2(2395.0, 340.0, 195.0, 265.0),
		"foot": Vector2(2500.0, 670.0)},
	{"id": "bubble_bath", "name": "Bubble Bath",
		"rect": Rect2(2685.0, 300.0, 185.0, 300.0),
		"foot": Vector2(2805.0, 670.0)},
	{"id": "__throne", "name": "Huluu's throne",
		"rect": Rect2(3000.0, 90.0, 330.0, 570.0),
		"foot": Vector2(3090.0, 690.0)},
]
const HALL_ITEMS: Array[Dictionary] = [
	{"id": "tapestry_right", "name": "Royal shell tapestry",
		"pos": Vector2(2612.0, 142.0), "z": MIRROR_INSERT_Z,
		"tex_path": INTERACTION_ART + "main_hall_tapestry_atlas.png",
		"scale": 0.72, "semantic_action": "unfurl_cloth",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.125, "sound": "castle/curtain_swish.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(105.0, 190.0),
		"symbol": "*", "color": Color(1.0, 0.80, 0.91)},
	{"id": "sconce_a0", "name": "Pearl shell light",
		"pos": Vector2(260.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": INTERACTION_ART + "main_hall_sconce_atlas.png",
		"scale": 0.8, "semantic_action": "toggle_shell_light",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.1025, "sound": "castle/light_switch.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "a_left",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_a1", "name": "Pearl shell light",
		"pos": Vector2(1012.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": INTERACTION_ART + "main_hall_sconce_atlas.png",
		"scale": 0.8, "semantic_action": "toggle_shell_light",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.1025, "sound": "castle/light_switch.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "a_right",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_a2", "name": "Pearl shell light",
		"pos": Vector2(1476.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": INTERACTION_ART + "main_hall_sconce_atlas.png",
		"scale": 0.8, "semantic_action": "toggle_shell_light",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.1025, "sound": "castle/light_switch.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "a_right",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_b0", "name": "Pearl shell light",
		"pos": Vector2(2048.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": INTERACTION_ART + "main_hall_sconce_atlas.png",
		"scale": 0.8, "semantic_action": "toggle_shell_light",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.1025, "sound": "castle/light_switch.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "b_left",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_b1", "name": "Pearl shell light",
		"pos": Vector2(2415.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": INTERACTION_ART + "main_hall_sconce_atlas.png",
		"scale": 0.8, "semantic_action": "toggle_shell_light",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.1025, "sound": "castle/light_switch.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "b_left",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
	{"id": "sconce_b2", "name": "Pearl shell light",
		"pos": Vector2(2888.0, 215.0), "z": LIGHT_FIXTURE_Z,
		"tex_path": INTERACTION_ART + "main_hall_sconce_atlas.png",
		"scale": 0.8, "semantic_action": "toggle_shell_light",
		"frames": 8, "hframes": 4, "vframes": 2,
		"frame_duration": 0.1025, "sound": "castle/light_switch.ogg",
		"sound_frame": 0, "pitch": 1.0,
		"hotspot_size": Vector2(112.0, 128.0), "light_cluster": "b_right",
		"symbol": "*", "color": Color(1.0, 0.78, 0.48)},
]
const HALL_DUST_BUNNY_SPAWNS: Array[Dictionary] = [
	{"id": "sleepy_bunny", "name": "Sleeping dust bunny",
		"pos": Vector2(900.0, 830.0), "z": 2.65,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_sleepy.png",
		"scale": 0.34, "dust_bunny_role": "sleeping_static",
		"contact_offset": Vector2(0.0, 60.0),
		"contact_radius": Vector2(132.0, 92.0),
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.55,
		"color": Color(0.86, 0.72, 1.0)},
	{"id": "shell_bunny", "name": "Shell-hide dust bunny",
		"pos": Vector2(1340.0, 830.0), "z": 3.05,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_shell_hide.png",
		"scale": 0.32, "dust_bunny_role": "shell_static",
		"contact_offset": Vector2(0.0, 60.0),
		"contact_radius": Vector2(132.0, 92.0),
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.45,
		"color": Color(0.60, 0.92, 1.0)},
	{"id": "runner_bunny", "name": "Running dust bunny",
		"pos": Vector2(1850.0, 830.0), "z": 2.85,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_hop.png",
		"scale": 0.32, "dust_bunny_role": "runner",
		"contact_offset": Vector2(0.0, 60.0),
		"contact_radius": Vector2(142.0, 98.0),
		"patrol_x": Vector2(1850.0, 2550.0), "run_speed": 220.0,
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.70,
		"color": Color(1.0, 0.75, 0.86)},
]
# Dust-bunny AI (owner task 2026-08-02). Every bunny is a one-hit-point critter
# that hops slowly, never chases Roshan and never hurts her. The three founders
# above stay authored at their spawn-guide coordinates; every other bunny is
# generated at runtime from the variant table below, and the Codex art already
# painted into this hall decides how each variant behaves:
#   * shell sconces (main_hall_sconce_atlas) — switching one ON wakes the
#     sleepers near it, makes shell bunnies duck back under their shell, and
#     makes hoppers drift toward the dark half of the hall;
#   * the royal shell tapestry — unfurling it startles every bunny near it;
#   * the painted doorways (HALL_PORTALS) — generated bunnies never spawn in a
#     door approach or on Roshan's arrival mark;
#   * dust_bunny_family.png — a family huddle is a nursery: while it is alive
#     it passively puffs out new pups on a faster clock.
const HALL_BUNNY_ART := "res://assets/castle/dirty_cleanup_2d/critters/" \
	+ "dust_bunnies/"
const HALL_BUNNY_HP := 1
const HALL_BUNNY_LIVE_CAP := 5
const HALL_BUNNY_SEED_BASE := 20260802
const HALL_BUNNY_HOP_DISTANCE := 46.0
const HALL_BUNNY_HOP_TIME := 0.46
const HALL_BUNNY_REST_TIME := 0.62
const HALL_BUNNY_HOP_HEIGHT := 16.0
const HALL_BUNNY_WAKE_TIME := 0.42
const HALL_BUNNY_LIGHT_REACH := 620.0
const HALL_BUNNY_LIGHT_WAKE := 0.35
const HALL_BUNNY_SHY_RADIUS := 340.0
const HALL_BUNNY_STARTLE_RADIUS := 560.0
const HALL_BUNNY_SETTLE_TIME := 5.0
const HALL_BUNNY_FLEE_TIME := 2.4
const HALL_BUNNY_HOLD_TIME := 3.2
const HALL_BUNNY_NURSERY_INTERVAL := 9.0
const HALL_BUNNY_DRIFT_INTERVAL := 13.0
const HALL_BUNNY_SPAWN_CLEARANCE := 150.0
const HALL_BUNNY_DOOR_CLEARANCE := 90.0
const HALL_BUNNY_START_CLEARANCE := 260.0
const HALL_BUNNY_START_FOOT := Vector2(380.0, 835.0)
# Generated cards sit low enough that even at the top of a hop they stay clear
# of every painted door approach band, whatever x the generator picks, and their
# contact feet stay inside HALL_WALK.
const HALL_BUNNY_FOOT_BAND := Vector2(834.0, 852.0)
const HALL_BUNNY_SPAWN_X_RANGE := Vector2(240.0, 3120.0)
const HALL_BUNNY_VARIANTS: Array[Dictionary] = [
	{"role": "hopper", "weight": 3, "tex": "dust_bunny_hop.png",
		"scale": 0.32, "z": 2.85, "pitch": 1.70, "range": 420.0,
		"color": Color(1.0, 0.75, 0.86)},
	{"role": "shy_hopper", "weight": 2, "tex": "dust_bunny_hop.png",
		"scale": 0.28, "z": 3.15, "pitch": 1.82, "range": 300.0,
		"color": Color(0.98, 0.86, 1.0)},
	{"role": "sleeping_static", "weight": 2, "tex": "dust_bunny_sleepy.png",
		"scale": 0.34, "z": 2.65, "pitch": 1.55, "range": 380.0,
		"color": Color(0.86, 0.72, 1.0)},
	{"role": "shell_static", "weight": 2, "tex": "dust_bunny_shell_hide.png",
		"scale": 0.32, "z": 3.05, "pitch": 1.45, "range": 0.0,
		"color": Color(0.60, 0.92, 1.0)},
	{"role": "family_nursery", "weight": 1, "tex": "dust_bunny_family.png",
		"scale": 0.30, "z": 2.45, "pitch": 1.35, "range": 0.0,
		"color": Color(1.0, 0.90, 0.72)},
]
const HALL_BUNNY_TRAVEL_ROLES: Array[String] = [
	"runner", "hopper", "shy_hopper"]
const PLAYROOM_RESCUE_ITEMS: Array[Dictionary] = [
	{"id": "baby_eagle_rescue", "name": "Baby Eagle",
		"pos": Vector2(367.0, 85.0), "z": 1.55,
		"tex_path": "res://assets/book/baby_eagle.png",
		"scale": 0.42, "rescue_role": "baby_eagle",
		"proximity_only": true,
		"color": Color(0.54, 0.91, 1.0)},
	{"id": "eagle_pin_left", "name": "Left pinning dust bunny",
		"pos": Vector2(189.0, 109.0), "z": 2.45,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_hop.png",
		"scale": 0.26, "dust_bunny_role": "playroom_pin_left",
		"rescue_bunny": true,
		"contact_foot": Vector2(445.0, 450.0),
		"contact_radius": Vector2(82.0, 62.0),
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.55,
		"color": Color(0.86, 0.72, 1.0)},
	{"id": "eagle_pin_right", "name": "Right pinning dust bunny",
		"pos": Vector2(323.0, 109.0), "z": 2.50,
		"tex_path": "res://assets/castle/dirty_cleanup_2d/critters/"
			+ "dust_bunnies/dust_bunny_hop.png",
		"scale": 0.26, "flip_h": true,
		"dust_bunny_role": "playroom_pin_right",
		"rescue_bunny": true,
		"contact_foot": Vector2(579.0, 450.0),
		"contact_radius": Vector2(82.0, 62.0),
		"proximity_only": true, "sound": "hop_boing.ogg", "pitch": 1.72,
		"color": Color(1.0, 0.75, 0.86)},
]
const MOVIE_IMAGES: Array[String] = [
	"res://assets/book/hall/p_slide.jpg",
	"res://assets/book/hall/p_trampoline.jpg",
	"res://assets/book/hall/p_garden.jpg",
	"res://assets/book/hall/p_snowman.jpg",
	"res://assets/book/hall/p_xmas.jpg",
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
	{"id": "dining_room", "name": "Family Dining Room", "icon": "🍽️",
		"tex": "room_dining_room_background.png", "action": "dining",
		"action_icon": "🍽️"},
	{"id": "royal_bedroom", "name": "Royal Bedroom", "icon": "🌙",
		"tex": "room_royal_bedroom_background.png", "action": "sleep",
		"action_icon": "🌙"},
	{"id": "sleepover_bedroom", "name": "Sleepover Bedroom", "icon": "🛏️",
		"tex": "room_sleepover_bedroom_background.png", "action": "sleep",
		"action_icon": "🛏️"},
	{"id": "movie_lounge", "name": "Cloud Movie Lounge", "icon": "🎬",
		"tex": "room_movie_lounge_background.png", "action": "movie",
		"action_icon": "🎬"},
	{"id": "family_gallery", "name": "Dream House Wing", "icon": "\u2302",
		"tex": "room_family_gallery_background.png", "action": "",
		"action_icon": "\u2302"},
]
const ROOM_PARENTS := {
	"family_gallery": "main_hall",
	"dining_room": "family_gallery",
	"royal_bedroom": "family_gallery",
	"sleepover_bedroom": "family_gallery",
	"movie_lounge": "family_gallery",
}
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
	"family_gallery": {
		"walk": Rect2(70.0, 500.0, 1140.0, 165.0),
		"mid_foot_y": -1.0,
		"mid": [],
		"front": [],
	},
	"dining_room": {
		"walk": Rect2(130.0, 390.0, 1020.0, 280.0), "mid_foot_y": 520.0,
		"mid": [],
		"front": [],
	},
	"royal_bedroom": {
		"walk": Rect2(125.0, 390.0, 1030.0, 280.0), "mid_foot_y": 525.0,
		"mid": [],
		"front": [],
	},
	"sleepover_bedroom": {
		"walk": Rect2(100.0, 410.0, 1080.0, 260.0), "mid_foot_y": 530.0,
		"mid": [],
		"front": [],
	},
	"movie_lounge": {
		"walk": Rect2(120.0, 420.0, 1040.0, 250.0), "mid_foot_y": 530.0,
		"mid": [],
		"front": [],
	},
}
const ROOM_ITEMS := {
	"opera_hall": [
		{"id": "curtains", "name": "Stage curtains", "pos": Vector2(414, 100),
			"z": 0.65,
			"symbol": "♪", "color": Color(1.0, 0.67, 0.78)},
		{"id": "chandelier", "name": "Pearl chandelier", "pos": Vector2(418, 0),
			"z": 1.10,
			"symbol": "✦", "color": Color(1.0, 0.90, 0.44)},
		{"id": "stage_star", "name": "Stage star", "pos": Vector2(490, 309),
			"z": 0.75, "hotspot_offset": Vector2(-26.0, 6.0),
			"hotspot_size": Vector2(96.0, 80.0),
			"symbol": "★", "color": Color(1.0, 0.82, 0.30)},
		{"id": "footlights", "name": "Stage footlights",
			"pos": Vector2(414, 286), "z": 0.72,
			"hotspot_offset": Vector2(0.0, -16.0),
			"hotspot_size": Vector2(196.0, 45.0),
			"color": Color(1.0, 0.86, 0.44)},
	],
	"kitchen": [
		{"id": "sink", "name": "Shell sink", "pos": Vector2(62, 176),
			"z": 0.75,
			"symbol": "○", "color": Color(0.45, 0.90, 1.0)},
		{"id": "pan_1", "name": "Copper pan", "pos": Vector2(300, 132),
			"z": 0.90,
			"symbol": "○", "color": Color(1.0, 0.72, 0.28)},
		{"id": "pan_2", "name": "Copper pan", "pos": Vector2(337, 132),
			"z": 0.92,
			"symbol": "○", "color": Color(1.0, 0.72, 0.28)},
		{"id": "pan_3", "name": "Copper pan", "pos": Vector2(379, 132),
			"z": 0.94,
			"symbol": "○", "color": Color(1.0, 0.72, 0.28)},
		{"id": "pan_4", "name": "Copper pan", "pos": Vector2(418, 132),
			"z": 0.96,
			"symbol": "○", "color": Color(1.0, 0.72, 0.28)},
		{"id": "oven", "name": "Warm oven", "pos": Vector2(289, 244),
			"z": 1.05,
			"symbol": "●", "color": Color(1.0, 0.58, 0.30)},
		{"id": "fridge", "name": "Royal refrigerator", "pos": Vector2(631, 84),
			"z": 0.95,
			"hotspot_offset": Vector2(8, 8),
			"hotspot_size": Vector2(190.0, 300.0),
			"symbol": "✦", "color": Color(0.61, 0.94, 0.90)},
	],
	"library": [
		{"id": "magic_book", "name": "Magic storybook", "pos": Vector2(445, 145),
			"z": 0.80,
			"symbol": "✦", "color": Color(0.81, 0.66, 1.0)},
		{"id": "pearl_table", "name": "Reading pearl", "pos": Vector2(392, 315),
			"z": MIDGROUND_Z,
			"symbol": "○", "color": Color(1.0, 0.91, 0.62)},
		{"id": "pearl_lamp", "name": "Pearl lamp", "pos": Vector2(4, 225),
			"z": 0.65, "hotspot_offset": Vector2(-8.0, -16.0),
			"hotspot_size": Vector2(112.0, 112.0),
			"symbol": "✦", "color": Color(1.0, 0.88, 0.48)},
		{"id": "book_stack", "name": "Stack of storybooks",
			"pos": Vector2(13, 365), "z": MIDGROUND_Z,
			"color": Color(0.81, 0.66, 1.0)},
	],
	"playroom": [
		{"id": "stuffie_nook", "name": "Stuffie friends", "pos": Vector2(380, 140),
			"z": 0.75,
			"symbol": "♡", "color": Color(1.0, 0.58, 0.74)},
		{"id": "stacking_toy", "name": "Stacking toy", "pos": Vector2(218, 284),
			"z": MIDGROUND_Z,
			"symbol": "★", "color": Color(1.0, 0.79, 0.30)},
		{"id": "blocks", "name": "Toy blocks", "pos": Vector2(626, 320),
			"z": MIDGROUND_Z,
			"symbol": "✦", "color": Color(0.54, 0.91, 0.78)},
		{"id": "play_tent", "name": "Play tent",
			"pos": Vector2(105, 235), "z": 0.72,
			"color": Color(1.0, 0.72, 0.88)},
	],
	"craft_room": [
		{"id": "idea_board", "name": "Idea board", "pos": Vector2(377, 103),
			"z": 0.70,
			"symbol": "✦", "color": Color(1.0, 0.78, 0.45)},
		{"id": "paint_table", "name": "Paint jars", "pos": Vector2(400, 272),
			"z": MIDGROUND_Z,
			"symbol": "●", "color": Color(0.60, 0.90, 0.82)},
		{"id": "palette", "name": "Rainbow palette", "pos": Vector2(0, 320),
			"z": FOREGROUND_Z,
			"symbol": "●", "color": Color(1.0, 0.55, 0.72)},
		{"id": "ribbon_rack", "name": "Ribbon rack",
			"pos": Vector2(270, 82), "z": 0.76,
			"color": Color(1.0, 0.62, 0.82)},
	],
	"mermaid_pool": [
		{"id": "waterfall", "name": "Rainbow waterfall", "pos": Vector2(285, 45),
			"z": 0.65,
			"symbol": "○", "color": Color(0.52, 0.91, 1.0)},
		{"id": "flower_float", "name": "Flower float", "pos": Vector2(371, 218),
			"z": MIDGROUND_Z, "hotspot_offset": Vector2(4.0, 12.0),
			"hotspot_size": Vector2(88.0, 88.0),
			"symbol": "✦", "color": Color(1.0, 0.62, 0.78)},
		{"id": "bubble_fountain", "name": "Bubble fountain", "pos": Vector2(553, 183),
			"z": MIDGROUND_Z,
			"symbol": "○", "color": Color(0.72, 0.94, 1.0)},
		{"id": "star_float", "name": "Star float",
			"pos": Vector2(468, 260), "z": MIDGROUND_Z + 0.03,
			"hotspot_offset": Vector2(0.0, -17.5),
			"hotspot_size": Vector2(80.0, 80.0),
			"color": Color(1.0, 0.82, 0.40)},
	],
	"bubble_bath": [
		{"id": "bathtub", "name": "Bubble bathtub", "pos": Vector2(76, 157),
			"z": 1.25,
			"symbol": "○", "color": Color(0.64, 0.92, 1.0)},
		{"id": "sink", "name": "Shell sink", "pos": Vector2(440, 137),
			"z": 0.80,
			"symbol": "○", "color": Color(0.52, 0.92, 1.0)},
		{"id": "toilet", "name": "Royal toilet", "pos": Vector2(753, 154),
			"z": 1.00,
			"symbol": "○", "color": Color(1.0, 0.72, 0.86)},
		{"id": "rubber_duck", "name": "Rubber duck",
			"pos": Vector2(279, 207), "z": 1.30,
			"hotspot_offset": Vector2(-35.5, -36.0),
			"hotspot_size": Vector2(112.0, 112.0),
			"color": Color(1.0, 0.82, 0.32)},
	],
	"family_gallery": [
		{"id": "gallery_dining_door", "name": "Family Dining Room",
			"pos": Vector2(25.0, 115.0), "z": 0.86, "scale": 0.64,
			"tex_path": DREAM_HOUSE_ART + "family_portal_dining.png",
			"hotspot_size": Vector2(250.0, 412.0),
			"roleplay_action": "enter_room",
			"room_destination": "dining_room",
			"roleplay_foot": Vector2(188.0, 620.0),
			"sound": "castle/curtain_swish.ogg",
			"color": Color(1.0, 0.72, 0.76)},
		{"id": "gallery_royal_bedroom_door", "name": "Royal Bedroom",
			"pos": Vector2(260.0, 115.0), "z": 0.87, "scale": 0.64,
			"tex_path": DREAM_HOUSE_ART + "family_portal_royal_bedroom.png",
			"hotspot_size": Vector2(250.0, 412.0),
			"roleplay_action": "enter_room",
			"room_destination": "royal_bedroom",
			"roleplay_foot": Vector2(481.0, 620.0),
			"sound": "castle/curtain_swish.ogg",
			"color": Color(0.72, 0.88, 1.0)},
		{"id": "gallery_sleepover_door", "name": "Sleepover Bedroom",
			"pos": Vector2(495.0, 115.0), "z": 0.88, "scale": 0.64,
			"tex_path": DREAM_HOUSE_ART + "family_portal_sleepover_bedroom.png",
			"hotspot_size": Vector2(250.0, 412.0),
			"roleplay_action": "enter_room",
			"room_destination": "sleepover_bedroom",
			"roleplay_foot": Vector2(775.0, 620.0),
			"sound": "castle/curtain_swish.ogg",
			"color": Color(0.80, 0.72, 1.0)},
		{"id": "gallery_movie_door", "name": "Cloud Movie Lounge",
			"pos": Vector2(730.0, 115.0), "z": 0.89, "scale": 0.64,
			"tex_path": DREAM_HOUSE_ART + "family_portal_movie_lounge.png",
			"hotspot_size": Vector2(250.0, 412.0),
			"roleplay_action": "enter_room", "room_destination": "movie_lounge",
			"roleplay_foot": Vector2(1069.0, 620.0),
			"sound": "castle/curtain_swish.ogg",
			"color": Color(1.0, 0.82, 0.42)},
	],
	"dining_room": [
		{"id": "dining_table", "name": "Family feast table",
			"pos": Vector2(280.0, 187.0), "z": 2.05, "scale": 0.70,
			"tex_path": DREAM_HOUSE_ART + "dining_table.png",
			"hotspot_offset": Vector2(17.0, 30.0),
			"hotspot_size": Vector2(430.0, 320.0),
			"roleplay_action": "eat_meal", "roleplay_foot": Vector2(512.0, 555.0),
			"sound": "chime.ogg", "pitch": 1.12,
			"color": Color(1.0, 0.68, 0.76)},
		{"id": "provisions_hutch", "name": "Royal buffet",
			"pos": Vector2(-58.0, 84.0), "z": 0.82, "scale": 0.50,
			"tex_path": DREAM_HOUSE_ART + "provisions_hutch.png",
			"roleplay_action": "serve_meal", "sound": "castle/page_flip.ogg",
			"pitch": 1.18, "color": Color(0.58, 0.94, 0.82)},
		{"id": "dining_seat_left", "name": "Cloud dining seat",
			"pos": Vector2(60.0, 256.0), "z": 2.32, "scale": 0.38,
			"tex_path": DREAM_HOUSE_ART + "dining_seat.png",
			"proximity_only": true},
		{"id": "dining_seat_right", "name": "Cloud dining seat",
			"pos": Vector2(555.0, 256.0), "z": 2.32, "scale": 0.38,
			"tex_path": DREAM_HOUSE_ART + "dining_seat.png",
			"flip_h": true, "proximity_only": true},
		{"id": "dining_chandelier", "name": "Pearl chandelier",
			"pos": Vector2(299.0, -72.0), "z": 0.72, "scale": 0.45,
			"tex_path": DREAM_HOUSE_ART + "shell_chandelier.png",
			"proximity_only": true},
		{"id": "meal_plate_0", "name": "Dinner plate",
			"pos": Vector2(332.0, 292.0), "z": 2.46, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "meal_plate.png",
			"roleplay_plate": 0, "proximity_only": true},
		{"id": "meal_plate_1", "name": "Dinner plate",
			"pos": Vector2(397.0, 278.0), "z": 2.47, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "meal_plate.png",
			"roleplay_plate": 1, "proximity_only": true},
		{"id": "meal_plate_2", "name": "Dinner plate",
			"pos": Vector2(462.0, 278.0), "z": 2.48, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "meal_plate.png",
			"roleplay_plate": 2, "proximity_only": true},
		{"id": "meal_plate_3", "name": "Dinner plate",
			"pos": Vector2(527.0, 292.0), "z": 2.49, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "meal_plate.png",
			"roleplay_plate": 3, "proximity_only": true},
		{"id": "meal_plate_4", "name": "Dinner plate",
			"pos": Vector2(382.0, 320.0), "z": 2.50, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "meal_plate.png",
			"roleplay_plate": 4, "proximity_only": true},
		{"id": "meal_plate_5", "name": "Dinner plate",
			"pos": Vector2(472.0, 320.0), "z": 2.51, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "meal_plate.png",
			"roleplay_plate": 5, "proximity_only": true},
	],
	"royal_bedroom": [
		{"id": "canopy_bed", "name": "Royal canopy bed",
			"pos": Vector2(270.0, 28.0), "z": 1.20, "scale": 0.72,
			"tex_path": DREAM_HOUSE_ART + "canopy_bed.png",
			"roleplay_action": "sleep", "roleplay_foot": Vector2(515.0, 530.0),
			"sound": "chime.ogg", "pitch": 0.82,
			"color": Color(0.74, 0.84, 1.0)},
		{"id": "shell_wardrobe", "name": "Shell wardrobe",
			"pos": Vector2(33.0, 63.0), "z": 0.92, "scale": 0.55,
			"tex_path": DREAM_HOUSE_ART + "shell_wardrobe.png",
			"roleplay_action": "dress_up", "sound": "castle/curtain_swish.ogg",
			"color": Color(1.0, 0.67, 0.82)},
		{"id": "bedside_table", "name": "Bedside pearl light",
			"pos": Vector2(663.0, 90.0), "z": 1.42, "scale": 0.42,
			"tex_path": DREAM_HOUSE_ART + "bedside_table.png",
			"roleplay_action": "bedside_light",
			"sound": "castle/light_switch.ogg",
			"color": Color(1.0, 0.88, 0.48)},
		{"id": "reading_cushion", "name": "Cosy story cushion",
			"pos": Vector2(664.0, 235.0), "z": 2.25, "scale": 0.28,
			"tex_path": DREAM_HOUSE_ART + "story_cushion.png",
			"roleplay_action": "relax", "roleplay_foot": Vector2(885.0, 535.0),
			"sound": "castle/page_flip.ogg",
			"color": Color(0.82, 0.70, 1.0)},
	],
	"sleepover_bedroom": [
		{"id": "dream_bed_0", "name": "Pink dream bed",
			"pos": Vector2(-126.0, 159.0), "z": 1.90, "scale": 0.42,
			"tex_path": DREAM_HOUSE_ART + "dream_bed_0.png",
			"roleplay_action": "sleep", "roleplay_foot": Vector2(210.0, 555.0),
			"sound": "chime.ogg", "pitch": 0.82,
			"color": Color(1.0, 0.70, 0.84)},
		{"id": "dream_bed_1", "name": "Pearl dream bed",
			"pos": Vector2(177.0, 154.0), "z": 1.92, "scale": 0.42,
			"tex_path": DREAM_HOUSE_ART + "dream_bed_1.png",
			"roleplay_action": "sleep", "roleplay_foot": Vector2(512.0, 555.0),
			"sound": "chime.ogg", "pitch": 0.86,
			"color": Color(0.74, 0.88, 1.0)},
		{"id": "dream_bed_2", "name": "Purple dream bed",
			"pos": Vector2(479.0, 159.0), "z": 1.94, "scale": 0.42,
			"tex_path": DREAM_HOUSE_ART + "dream_bed_2.png",
			"roleplay_action": "sleep", "roleplay_foot": Vector2(814.0, 555.0),
			"sound": "chime.ogg", "pitch": 0.90,
			"color": Color(0.78, 0.70, 1.0)},
		{"id": "sleepover_chandelier", "name": "Pearl chandelier",
			"pos": Vector2(299.0, -77.0), "z": 0.72, "scale": 0.38,
			"tex_path": DREAM_HOUSE_ART + "shell_chandelier.png",
			"proximity_only": true},
	],
	"movie_lounge": [
		{"id": "movie_picture", "name": "Family home movie",
			"pos": Vector2(255.0, -122.0), "z": 0.48, "scale": 0.40,
			"tex_path": "res://assets/book/hall/p_slide.jpg",
			"proximity_only": true},
		{"id": "movie_screen", "name": "Home movie screen",
			"pos": Vector2(152.0, 30.0), "z": 0.76, "scale": 0.92,
			"tex_path": DREAM_HOUSE_ART + "movie_screen_frame.png",
			"hotspot_offset": Vector2(30.0, 30.0),
			"hotspot_size": Vector2(660.0, 340.0),
			"roleplay_action": "watch_movie",
			"sound": "castle/page_flip.ogg",
			"color": Color(1.0, 0.82, 0.42)},
		{"id": "cloud_settee_left", "name": "Left cloud couch",
			"pos": Vector2(45.0, 301.0), "z": 2.12, "scale": 0.52,
			"tex_path": DREAM_HOUSE_ART + "cloud_settee.png",
			"roleplay_action": "relax", "roleplay_foot": Vector2(260.0, 555.0),
			"sound": "castle/curtain_swish.ogg",
			"color": Color(0.72, 0.88, 1.0)},
		{"id": "cloud_settee_right", "name": "Right cloud couch",
			"pos": Vector2(549.0, 301.0), "z": 2.12, "scale": 0.52,
			"tex_path": DREAM_HOUSE_ART + "cloud_settee.png",
			"flip_h": true, "roleplay_action": "relax",
			"roleplay_foot": Vector2(764.0, 555.0),
			"sound": "castle/curtain_swish.ogg",
			"color": Color(0.72, 0.88, 1.0)},
		{"id": "cloud_pouf", "name": "Cloud play pouf",
			"pos": Vector2(308.0, 297.0), "z": 2.52, "scale": 0.32,
			"tex_path": DREAM_HOUSE_ART + "cloud_pouf.png",
			"roleplay_action": "relax", "roleplay_foot": Vector2(512.0, 560.0),
			"sound": "castle/toy_blocks.ogg",
			"color": Color(1.0, 0.72, 0.88)},
	],
}

const INTERACTION_SPECS := {
	"opera_hall:curtains": {"semantic_action": "open_stage_curtains",
		"sound": "castle/curtain_swish.ogg", "frame_duration": 0.125,
		"sound_frame": 0},
	"opera_hall:chandelier": {"semantic_action": "chandelier_light_chase",
		"sound": "castle/light_switch.ogg", "frame_duration": 0.1025,
		"sound_frame": 0, "pitch": 1.0},
	"opera_hall:stage_star": {"semantic_action": "marquee_star_light_chase",
		"sound": "castle/light_switch.ogg", "frame_duration": 0.1025,
		"sound_frame": 0, "pitch": 1.0},
	"opera_hall:footlights": {"semantic_action": "stage_footlight_chase",
		"sound": "castle/light_switch.ogg", "frame_duration": 0.1025,
		"sound_frame": 0, "pitch": 1.0},
	"kitchen:sink": {"semantic_action": "turn_faucet_and_run_water",
		"sound": "castle/faucet_water.ogg", "frame_duration": 0.15,
		"sound_frame": 0},
	"kitchen:pan_1": {"semantic_action": "swing_pan_on_hook",
		"sound": "castle/pan_clang.ogg", "frame_duration": 0.115,
		"sound_frame": 0, "pitch": 1.0, "hotspot_group": "pan_rack",
		"hotspot_owner": true, "hotspot_offset": Vector2(-14.0, -14.5),
		"hotspot_size": Vector2(176.0, 112.0)},
	"kitchen:pan_2": {"semantic_action": "swing_pan_on_hook",
		"sound": "castle/pan_clang.ogg", "frame_duration": 0.115,
		"sound_frame": 0, "pitch": 1.0, "hotspot_group": "pan_rack",
		"hotspot_owner": false},
	"kitchen:pan_3": {"semantic_action": "swing_pan_on_hook",
		"sound": "castle/pan_clang.ogg", "frame_duration": 0.115,
		"sound_frame": 0, "pitch": 1.0, "hotspot_group": "pan_rack",
		"hotspot_owner": false},
	"kitchen:pan_4": {"semantic_action": "swing_pan_on_hook",
		"sound": "castle/pan_clang.ogg", "frame_duration": 0.115,
		"sound_frame": 0, "pitch": 1.0, "hotspot_group": "pan_rack",
		"hotspot_owner": false},
	"kitchen:oven": {"semantic_action": "open_oven_door_and_warm_fire",
		"sound": "castle/oven_door.ogg", "frame_duration": 0.1625,
		"sound_frame": 0},
	"kitchen:fridge": {"semantic_action": "unlatch_and_open_fridge_door",
		"sound": "castle/fridge_open.ogg", "close_sound": "castle/fridge_close.ogg",
		"frame_duration": 0.145,
		"sound_frame": 0},
	"library:magic_book": {"semantic_action": "open_book_and_turn_pages",
		"sound": "castle/page_flip.ogg", "frame_duration": 0.095,
		"sound_frame": 0},
	"library:pearl_table": {"semantic_action": "wake_reading_pearl",
		"sound": "castle/light_switch.ogg", "frame_duration": 0.1025,
		"sound_frame": 0, "pitch": 1.0},
	"library:pearl_lamp": {"semantic_action": "toggle_pearl_lamp",
		"sound": "castle/light_switch.ogg", "frame_duration": 0.1025,
		"sound_frame": 0, "pitch": 1.0},
	"library:book_stack": {"semantic_action": "open_top_book_and_turn_pages",
		"sound": "castle/page_flip.ogg", "frame_duration": 0.095,
		"sound_frame": 0, "pitch": 1.0},
	"playroom:stuffie_nook": {"semantic_action": "stuffie_friends_wave",
		"sound": "castle/toy_blocks.ogg", "frame_duration": 0.1375,
		"sound_frame": 0, "pitch": 1.0},
	"playroom:stacking_toy": {"semantic_action": "lift_and_restack_rings",
		"sound": "castle/toy_blocks.ogg", "frame_duration": 0.1375,
		"sound_frame": 0},
	"playroom:blocks": {"semantic_action": "topple_and_restack_blocks",
		"sound": "castle/toy_blocks.ogg", "frame_duration": 0.1375,
		"sound_frame": 0, "pitch": 1.0},
	"playroom:play_tent": {"semantic_action": "open_and_close_tent_flap",
		"sound": "castle/curtain_swish.ogg", "frame_duration": 0.125,
		"sound_frame": 0, "pitch": 1.0},
	"craft_room:idea_board": {"semantic_action": "flip_idea_notes",
		"sound": "castle/page_flip.ogg", "frame_duration": 0.095,
		"sound_frame": 0, "pitch": 1.0},
	"craft_room:paint_table": {"semantic_action": "stir_paint_with_brush",
		"sound": "castle/craft_brush.ogg", "frame_duration": 0.12,
		"sound_frame": 0},
	"craft_room:palette": {"semantic_action": "mix_palette_colors",
		"sound": "castle/craft_brush.ogg", "frame_duration": 0.12,
		"sound_frame": 0, "pitch": 1.0},
	"craft_room:ribbon_rack": {"semantic_action": "unroll_and_retract_ribbon",
		"sound": "castle/ribbon_roll.ogg", "frame_duration": 0.1325,
		"sound_frame": 0},
	"mermaid_pool:waterfall": {"semantic_action": "surge_waterfall_flow",
		"sound": "castle/bubble_water.ogg", "frame_duration": 0.185,
		"sound_frame": 0},
	"mermaid_pool:flower_float": {"semantic_action": "open_flower_and_make_ripples",
		"sound": "castle/bubble_water.ogg", "frame_duration": 0.185,
		"sound_frame": 0, "pitch": 1.0},
	"mermaid_pool:bubble_fountain": {"semantic_action": "raise_and_pop_bubbles",
		"sound": "castle/bubble_water.ogg", "frame_duration": 0.185,
		"sound_frame": 0, "pitch": 1.0},
	"mermaid_pool:star_float": {"semantic_action": "float_and_make_ripples",
		"sound": "castle/bubble_water.ogg", "frame_duration": 0.185,
		"sound_frame": 0, "pitch": 1.0},
	"bubble_bath:bathtub": {"semantic_action": "turn_taps_and_fill_bubbles",
		"sound": "castle/bubble_water.ogg", "frame_duration": 0.185,
		"sound_frame": 0},
	"bubble_bath:sink": {"semantic_action": "turn_faucet_and_run_water",
		"sound": "castle/faucet_water.ogg", "frame_duration": 0.15,
		"sound_frame": 0, "pitch": 1.0},
	"bubble_bath:toilet": {"semantic_action": "flap_seat_and_flush",
		"sound": "castle/toilet_flush.ogg", "frame_duration": 0.225,
		"sound_frame": 0},
	"bubble_bath:rubber_duck": {"semantic_action": "squeak_dive_and_pop_up",
		"sound": "castle/duck_squeak.ogg", "frame_duration": 0.0775,
		"sound_frame": 0, "pitch": 1.0},
}
const INTERACTION_GRIDS_3X3: Array[String] = [
	"bubble_bath:bathtub",
	"craft_room:idea_board",
	"craft_room:palette",
	"playroom:stuffie_nook",
]

const KITCHEN_RECIPES: Array[Dictionary] = [
	{"id": "pearl_cake", "name": "Pearl Cake", "icon": "🧁", "uses": ""},
	{"id": "carrot_cake", "name": "Carrot Cake", "icon": "🥕",
		"uses": "carrots"},
]
const KITCHEN_FOOD_ICONS := {
	"carrots": "🥕",
	"sugar": "🍬",
}

var m: ReefMain
var fixture_rigs: CastleFixtureRigs
var kitchen_menu_layer: CanvasLayer = null
var kitchen_menu_stage: Control = null
var kitchen_act: OperaAct = null
var fridge_close_input_blocker: Control = null

func _init(main: ReefMain) -> void:
	m = main
	fixture_rigs = CastleFixtureRigs.new(main)

func is_open() -> bool:
	return m.castle_room_layer != null and is_instance_valid(m.castle_room_layer)


func _fridge_close_is_blocked() -> bool:
	return (
		fridge_close_input_blocker != null
		and is_instance_valid(fridge_close_input_blocker)
		and fridge_close_input_blocker.visible
	)


func _on_fridge_close_blocker_input(_event: InputEvent) -> void:
	if not _fridge_close_is_blocked():
		return
	fridge_close_input_blocker.accept_event()
	m.get_viewport().set_input_as_handled()


func _set_fridge_close_blocked(blocked: bool) -> void:
	if not blocked:
		if (
				fridge_close_input_blocker != null
				and is_instance_valid(fridge_close_input_blocker)
		):
			fridge_close_input_blocker.mouse_filter = Control.MOUSE_FILTER_IGNORE
			fridge_close_input_blocker.visible = false
			fridge_close_input_blocker.queue_free()
		fridge_close_input_blocker = null
		return
	if _fridge_close_is_blocked() or m.castle_room_layer == null:
		return
	var blocker := Control.new()
	blocker.name = "FridgeCloseInputBlocker"
	blocker.mouse_filter = Control.MOUSE_FILTER_STOP
	blocker.focus_mode = Control.FOCUS_NONE
	blocker.z_index = 1000
	blocker.set_meta("castle_fridge_close_input_gate", true)
	blocker.gui_input.connect(_on_fridge_close_blocker_input)
	m.castle_room_layer.add_child(blocker)
	blocker.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fridge_close_input_blocker = blocker


func open(start_room: String = "main_hall") -> void:
	if is_open():
		resume(start_room)
		return
	m.castle_room_id = start_room
	m.castle_room_buttons.clear()
	m.g["castle_dust_bunnies_cleared"] = {}
	m.g["castle_dust_bunny_runner_time"] = 0.0
	if not m.g.has("castle_dining_plates"):
		m.g["castle_dining_plates"] = 0
	if not m.g.has("castle_movie_index"):
		m.g["castle_movie_index"] = 0
	if not m.g.has("castle_bedside_light_on"):
		m.g["castle_bedside_light_on"] = false
	m.g["castle_roleplay_sleeping"] = false
	# One colony per castle visit: the founders plus a generated tail. The visit
	# serial only seeds the generator, so a later visit brings a different mix of
	# sleepers, shell hiders and hoppers without any save-file state.
	m.g["castle_visit_serial"] = int(m.g.get("castle_visit_serial", 0)) + 1
	m.g["castle_dust_bunny_colony"] = []
	m.g["castle_dust_bunny_spawn_clock"] = 0.0
	m.g["castle_dust_bunny_spawn_serial"] = 0
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
	# combat wing 2026-08: the castle's chain engine (pop-chain, pips, pitch
	# ladder, haptics for bunny pops). Never registered in main.hit_engines —
	# the castle layer owns its own touch path.
	m.castle_dust_he = HitEngine.new(m)
	m.castle_dust_he.camera = m.castle_room_camera

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
	_close_kitchen_menu()
	_set_fridge_close_blocked(false)
	_restore_previous_environment()
	if is_open():
		m.castle_room_layer.visible = false
	if m.castle_room_world_root != null:
		m.castle_room_world_root.visible = false
	if m.castle_room_camera != null:
		m.castle_room_camera.current = false
	m._set_world_controls_enabled(true, "castle_rooms")
	m._set_world_controls_enabled(true, "kitchen_fridge_close")

func close() -> void:
	_close_kitchen_menu()
	_set_fridge_close_blocked(false)
	fixture_rigs.teardown()
	_restore_previous_environment()
	if bool(m.g.get("castle_roleplay_sleeping", false)):
		m._set_world_controls_enabled(true, "castle_roleplay_sleep")
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
	m.castle_room_link_layer = null
	m.castle_room_door_hotspots.clear()
	m.castle_room_item_sprites.clear()
	m.castle_room_prop_sfx = null
	m.castle_room_player_sprite = null
	m.castle_room_player_shadow = null
	m.castle_room_action_button = null
	m.castle_room_back_button = null
	m.castle_room_buttons.clear()
	m.g.erase("castle_dust_bunnies_cleared")
	m.g.erase("castle_dust_bunny_runner_time")
	m.g.erase("castle_dining_plates")
	m.g.erase("castle_movie_index")
	m.g.erase("castle_bedside_light_on")
	m.g.erase("castle_roleplay_sleeping")
	m.g.erase("castle_dust_bunny_colony")
	m.g.erase("castle_dust_bunny_spawn_clock")
	m.g.erase("castle_dust_bunny_spawn_serial")
	if m.castle_dust_he != null:
		m.castle_dust_he.teardown()
		m.castle_dust_he = null
	if m.castle_partner != null:
		m.castle_partner.detach()
		m.castle_partner = null
	m._set_world_controls_enabled(true, "castle_rooms")
	m._set_world_controls_enabled(true, "kitchen_fridge_close")
	if m.player != null:
		m.player.visible = true
		if m.player.cam != null:
			m.player.cam.make_current()
	if m.hud_layer != null:
		m.hud_layer.visible = true

func tick(delta: float) -> void:
	if m.player != null:
		m.player.vel = Vector3.ZERO
	fixture_rigs.tick(delta)
	if m.castle_dust_he != null:
		m.castle_dust_he.tick(delta)   # pop-chain window decay
	if m.castle_partner != null:
		m.castle_partner.tick(delta)
	_update_dust_bunny_runner(delta)
	_update_dust_bunny_colony(delta)
	_update_dust_bunny_spawner(delta)
	_check_dust_bunny_contacts()
	_update_camera_parallax(delta)
	_update_touch_hotspots()
	_update_hall_portals()
	_sync_hall_lighting()

func physics_tick(delta: float) -> void:
	fixture_rigs.physics_tick(delta)


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
	m.castle_room_link_layer = Control.new()
	m.castle_room_link_layer.name = "DreamHouseRoomLinks"
	m.castle_room_link_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.castle_room_link_layer.z_index = 26
	stage.add_child(m.castle_room_link_layer)
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

	m.castle_room_back_button = Button.new()
	m.castle_room_back_button.name = "CastleBack"
	m.castle_room_back_button.position = Vector2(28.0, 28.0)
	StorybookUI.style_back_button(
		m.castle_room_back_button, "Castle courtyard")
	m.castle_room_back_button.pressed.connect(_go_back)
	m.castle_room_back_button.z_index = 30
	stage.add_child(m.castle_room_back_button)

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
		# Runtime cards append the approved neighbor edge to the right and/or
		# beneath them. The one-pixel two-axis overlap closes Mobile raster
		# cracks without scaling, interpolation, crop, or generated art.
		var source_size := Vector2(836.0, 470.0 if row == 0 else 471.0)
		var bleed_pixels := Vector2i(1 if column < 3 else 0, 1 if row == 0 else 0)
		tile.set_meta("source_art_rect", Rect2(top_left, source_size))
		var screen_index: int = column / 2
		var local_column: int = column % 2
		var screen_source_rect: Rect2 = HALL_SCREEN_SOURCE_RECTS[
			screen_index]
		tile.set_meta("source_screen_id", "a" if screen_index == 0 else "b")
		tile.set_meta("source_master_rect", Rect2(
			screen_source_rect.position + Vector2(
				float(local_column) * 836.0,
				0.0 if row == 0 else 470.0),
			source_size))
		tile.set_meta("render_art_rect",
			Rect2(top_left, texture.get_size()))
		tile.set_meta("runtime_seam_bleed_pixels", bleed_pixels)
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
	environment.ambient_light_color = Color(0.70, 0.62, 0.78)
	environment.ambient_light_energy = 0.26
	m._wind_waker_bloom(environment, HALL_GLOW_FULL,
		HALL_BLOOM_FULL, 0.58)
	# The shell cards carry true HDR spatial emission. A higher scale lets the
	# Mobile renderer spread that energy into the wall while the low-emission
	# shell body keeps its drawn pink/gold detail.
	environment.glow_hdr_scale = 4.20
	m._apply_scene_grade(environment, "warm_pastel")
	environment.adjustment_saturation = 0.50
	environment.adjustment_contrast = 1.20
	environment.adjustment_brightness = 1.12
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
	var grid: Dictionary = ROOM_BACKGROUND_GRIDS.get(room_id, {})
	var rows: int = int(grid.get("rows", 2))
	var columns: int = int(grid.get("columns", 2))
	var native_size: Vector2 = grid.get(
		"native_size", ROOM_TILE_NATIVE_SIZE)
	var logical_size: Vector2 = grid.get(
		"logical_size", ROOM_TILE_LOGICAL_SIZE)
	var tile_pixel_size: float = float(grid.get(
		"pixel_size", ROOM_TILE_PIXEL_SIZE))
	var source_grid: String = String(grid.get("source_grid", "2x2_2k"))
	for row in range(rows):
		for column in range(columns):
			var file_name := "room_%s_background_r%d_c%d.png" % [
				room_id, row, column]
			var texture: Texture2D = load(ROOM_TILE_ROOT + file_name)
			if texture == null:
				continue
			var logical_top_left := Vector2(
				float(column) * logical_size.x,
				float(row) * logical_size.y)
			# Source tiles stay at their native <=1024 dimensions. Expand the
			# rendered quad by one native pixel toward each interior neighbor,
			# anchored at its top-left, to close clear raster gaps without
			# duplicating or resampling any source asset.
			var overlap_pixels := Vector2(
				1.0 if column < columns - 1 else 0.0,
				1.0 if row < rows - 1 else 0.0)
			var native_to_logical: Vector2 = logical_size / native_size
			var render_logical_size: Vector2 = logical_size \
				+ overlap_pixels * native_to_logical
			var render_center: Vector2 = logical_top_left \
				+ render_logical_size * 0.5
			var tile := _new_card(
				"RoomTile_%s_r%d_c%d" % [room_id, row, column],
				texture)
			tile.position = _art_to_world(render_center, BACKGROUND_Z)
			tile.scale = Vector3(
				render_logical_size.x / logical_size.x,
				render_logical_size.y / logical_size.y, 1.0)
			tile.pixel_size = tile_pixel_size
			# Mip edge sampling causes a one-pixel dark hairline where opaque
			# cards meet. Linear sampling without mipmaps keeps adjacent source
			# texels continuous at this fixed camera distance.
			tile.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
			tile.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			tile.set_meta("source_asset_role", "clean_background_tile")
			tile.set_meta("render_art_rect",
				Rect2(logical_top_left, render_logical_size))
			tile.set_meta("runtime_seam_overlap_pixels", Vector2i(
				int(overlap_pixels.x), int(overlap_pixels.y)))
			tile.set_meta("source_master_grid", source_grid)
			tile.set_meta("source_art_rect",
				Rect2(logical_top_left, logical_size))
			tile.set_meta("native_texture_size", native_size)
			tile.set_meta("depth_z", BACKGROUND_Z)
			m.castle_room_world_root.add_child(tile)
			m.castle_room_detail_tiles.append(tile)

func _build_hall_portals() -> void:
	if m.castle_room_door_hotspot_layer == null:
		return
	m.castle_room_door_hotspots.clear()
	for portal_data: Dictionary in HALL_PORTALS:
		var portal_id: String = String(portal_data["id"])
		var button := Button.new()
		button.name = "HallDoor_" + portal_id
		button.flat = true
		button.focus_mode = Control.FOCUS_NONE
		button.tooltip_text = String(portal_data["name"])
		button.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
		button.set_meta("uses_own_sfx", true)
		button.pressed.connect(_enter_hall_portal.bind(
			portal_id, portal_data["foot"] as Vector2))
		m.castle_room_door_hotspot_layer.add_child(button)
		if portal_id != "__throne":
			m.castle_room_buttons[portal_id] = button
		m.castle_room_door_hotspots.append({
			"button": button,
			"data": portal_data,
		})
	m.castle_room_door_hotspot_layer.visible = false

func _rebuild_room_links(_room_id: String) -> void:
	if m.castle_room_link_layer == null:
		return
	for child: Node in m.castle_room_link_layer.get_children():
		m.castle_room_link_layer.remove_child(child)
		child.queue_free()
	m.castle_room_link_layer.visible = false

func show_room(room_id: String, announce: bool = true) -> void:
	if _fridge_close_is_blocked():
		return
	var room: Dictionary = _room(room_id)
	if room.is_empty() or m.castle_room_background == null:
		return
	m.castle_room_id = room_id
	if m.castle_room_prop_sfx != null:
		m.castle_room_prop_sfx.stop()
	var hall_mode: bool = room_id == "main_hall"
	if m.castle_room_back_button != null:
		var parent_id: String = String(ROOM_PARENTS.get(
			room_id, "main_hall"))
		var parent_room: Dictionary = _room(parent_id)
		var back_hint := "Castle courtyard" if hall_mode \
			else String(parent_room.get("name", "Main Hall"))
		m.castle_room_back_button.tooltip_text = back_hint
		m.castle_room_back_button.set_meta("parent_hint", back_hint)
	if not hall_mode:
		m.castle_room_background.texture = load(ROOM_ART + String(room["tex"]))
		m.castle_room_camera.position = Vector3(0.0, 0.0, CAMERA_DISTANCE)
		_build_room_background_tiles(room_id)
	else:
		_clear_room_background_tiles()
	_set_hall_background_visible(hall_mode)
	_rebuild_depth_layers(room_id)
	_rebuild_touch_items(room_id)
	_rebuild_room_links(room_id)
	if room_id == "dining_room":
		_sync_dining_plates()
	elif room_id == "royal_bedroom":
		_sync_bedside_light()
	elif room_id == "movie_lounge":
		_sync_movie_picture()
	m.castle_room_action_button.visible = not hall_mode \
		and room_id != "family_gallery" \
		and (room_id != "playroom" or _playroom_rescue_done())
	if not hall_mode:
		StorybookUI.style_icon_button(m.castle_room_action_button,
			String(room["action_icon"]), "gold", Vector2(132.0, 132.0),
			String(room["name"]))
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
		if room_id == "playroom" and not _playroom_rescue_done():
			m.show_msg("Baby Eagle",
				"Chirp! Two dust bunnies have me! Swim over and bump both away!",
				"talk")
		else:
			m.show_msg("Pearl Castle", String(room["name"]), "home")

func _room(room_id: String) -> Dictionary:
	for room: Dictionary in ROOMS:
		if String(room["id"]) == room_id:
			return room
	return {}

func _on_room_input(event: InputEvent) -> void:
	if _fridge_close_is_blocked():
		return
	if event is InputEventMouseButton and (event as InputEventMouseButton).pressed:
		_walk_cutout_to((event as InputEventMouseButton).position)
	elif event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		_walk_cutout_to((event as InputEventScreenTouch).position)

func _walk_cutout_to(screen_position: Vector2) -> void:
	if m.castle_room_player_sprite == null:
		return
	# combat wing 2026-08: a tap on a bunny card pops it on the spot — the
	# game-wide tap-the-creature verb now works here too. Walking into a
	# bunny still pops it as well (the motor-inclusive floor stays).
	var bunny_id: String = _dust_bunny_id_from_camera_ray(screen_position)
	if bunny_id != "":
		_explode_dust_bunny(bunny_id)
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

# The probe-proven card picker, kept verbatim below but returning the picked
# bunny's id; the foot variant wraps it for the walking route and the probes.
func _dust_bunny_foot_from_camera_ray(screen_position: Vector2) -> Vector2:
	var item_id: String = _dust_bunny_id_from_camera_ray(screen_position)
	if item_id == "":
		return Vector2.INF
	var record: Dictionary = m.castle_room_item_sprites.get(
		item_id, {}) as Dictionary
	return record.get("contact_foot", Vector2.INF) as Vector2

func _dust_bunny_id_from_camera_ray(screen_position: Vector2) -> String:
	if m.castle_room_camera == null:
		return ""
	var ray_origin: Vector3 = m.castle_room_camera.project_ray_origin(
		screen_position)
	var ray_direction: Vector3 = m.castle_room_camera.project_ray_normal(
		screen_position)
	var nearest_distance: float = INF
	var nearest_id: String = ""
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[item_id_value] \
			as Dictionary
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if String(item_data.get("dust_bunny_role", "")) == "":
			continue
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		if sprite == null or sprite.texture == null or not sprite.visible:
			continue
		var basis: Basis = sprite.global_transform.basis
		var normal: Vector3 = basis.z.normalized()
		var denominator: float = ray_direction.dot(normal)
		if absf(denominator) <= 0.00001:
			continue
		var hit_distance: float = (
			sprite.global_position - ray_origin).dot(normal) / denominator
		if hit_distance <= 0.0 or hit_distance >= nearest_distance:
			continue
		var hit_point: Vector3 = ray_origin + ray_direction * hit_distance
		var relative: Vector3 = hit_point - sprite.global_position
		var texture_size: Vector2 = sprite.texture.get_size()
		var half_width: float = basis.x.length() \
			* texture_size.x * sprite.pixel_size * 0.5
		var half_height: float = basis.y.length() \
			* texture_size.y * sprite.pixel_size * 0.5
		if absf(relative.dot(basis.x.normalized())) > half_width \
				or absf(relative.dot(basis.y.normalized())) > half_height:
			continue
		nearest_distance = hit_distance
		nearest_id = String(item_id_value)
	return nearest_id

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
	if String(piece_data.get("shader", "")) == "portal_cutout":
		var portal_material := ShaderMaterial.new()
		portal_material.shader = CASTLE_PORTAL_CUTOUT_SHADER
		portal_material.set_shader_parameter("portal_texture", texture)
		piece.material_override = portal_material
		piece.set_meta("castle_transparent_portal_cutout", true)
	piece.set_meta("source_asset_role", String(piece_data["role"]))
	piece.set_meta("source_object_id",
		"main_hall:" + String(piece_data["id"]))
	piece.set_meta("depth_z", depth_z)
	m.castle_room_mid_layer.add_child(piece)

func _rebuild_touch_items(room_id: String) -> void:
	fixture_rigs.rebuild_begin()
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
		items.append_array(_hall_dust_bunny_colony())
	else:
		var room_items: Array = ROOM_ITEMS.get(room_id, []) as Array
		items = room_items.duplicate()
		if room_id == "playroom":
			_restore_playroom_rescue_clears()
			if not _playroom_rescue_done():
				items.append_array(PLAYROOM_RESCUE_ITEMS)
	for item_data_value: Variant in items:
		var item_data: Dictionary = item_data_value
		_add_touch_item(room_id, item_data)
	_update_touch_hotspots()

func _add_touch_item(room_id: String, item_data: Dictionary) -> void:
	if m.castle_room_item_visual_layer == null \
			or m.castle_room_item_hotspot_layer == null:
		return
	var item_id: String = String(item_data["id"])
	var interaction_key := room_id + ":" + item_id
	var interaction_spec: Dictionary = INTERACTION_SPECS.get(
		interaction_key, {}) as Dictionary
	var v2_visual: Dictionary = fixture_rigs.visual_spec(room_id, item_id)
	if not interaction_spec.is_empty() or not v2_visual.is_empty():
		item_data = item_data.duplicate(true)
		item_data.merge(interaction_spec, true)
	if not v2_visual.is_empty():
		var grid: Array = v2_visual.get("grid", [1, 1]) as Array
		item_data["v2_visual"] = v2_visual
		item_data["semantic_action"] = String(v2_visual.get(
			"semantic_action", item_data.get("semantic_action", "")))
		item_data["frames"] = int(v2_visual.get("authored_frame_count", 8))
		item_data["timeline_sequence"] = v2_visual.get(
			"timeline_sequence", []) as Array
		item_data["timeline_frames"] = int(v2_visual.get(
			"timeline_frame_count", item_data["frames"]))
		item_data["hframes"] = int(grid[0])
		item_data["vframes"] = int(grid[1])
		item_data["tex_path"] = "res://" + String(v2_visual["sheet"])
		item_data["rest_frame"] = int(v2_visual.get("rest_frame", 0))
		var manifest_sound: String = String(v2_visual.get("sound", ""))
		if manifest_sound != "":
			item_data["sound"] = manifest_sound.trim_prefix("assets/audio/")
		var manifest_close_sound: String = String(
			v2_visual.get("close_sound", ""))
		if manifest_close_sound != "":
			item_data["close_sound"] = manifest_close_sound.trim_prefix(
				"assets/audio/")
		item_data["sound_frame"] = int(v2_visual.get("sound_frame", 0))
		item_data["pitch"] = float(v2_visual.get("pitch", 1.0))
		item_data["close_pitch"] = float(v2_visual.get("close_pitch", 1.0))
		item_data["frame_duration"] = float(v2_visual.get(
			"frame_duration_seconds", item_data.get("frame_duration", 0.10)))
		if interaction_key == "kitchen:fridge":
			item_data["open_hold_step"] = int(
				v2_visual.get("open_hold_step", 4))
	elif not interaction_spec.is_empty():
		item_data["frames"] = 8
		item_data["timeline_frames"] = 8
		item_data["hframes"] = 3 if interaction_key in INTERACTION_GRIDS_3X3 else 4
		item_data["vframes"] = 3 if interaction_key in INTERACTION_GRIDS_3X3 else 2
		item_data["tex_path"] = INTERACTION_ART + room_id + "_" \
			+ item_id + "_atlas.png"
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
	if not v2_visual.is_empty():
		piece.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	piece.hframes = int(item_data.get("hframes", 1))
	piece.vframes = int(item_data.get("vframes", 1))
	piece.frame = int(item_data.get("rest_frame", 0))
	var source_position: Vector2 = item_data["pos"]
	var item_z: float = float(item_data.get("z", ITEM_Z))
	var authored_visual_scale: float = float(item_data.get("scale", 1.0))
	var runtime_scale: float = float(v2_visual.get("runtime_scale", 1.0))
	var visual_scale := authored_visual_scale * runtime_scale
	var reference_size := _v2_vector2(
		v2_visual.get("placement_size", []), _sprite_frame_size(piece))
	var placement_center: Vector2
	if room_id == "main_hall":
		var hall_offset := _v2_vector2(
			v2_visual.get("hall_center_offset", []), Vector2.ZERO)
		placement_center = source_position \
			+ hall_offset * authored_visual_scale
		piece.position = _hall_art_to_world(placement_center, item_z)
		piece.pixel_size = _pixel_size_for_depth(item_z)
		piece.scale = Vector3.ONE * visual_scale
		piece.set_meta("depth_z", item_z)
	else:
		if not v2_visual.is_empty():
			var center_offset := _v2_vector2(
				v2_visual.get("runtime_center_offset", []),
				reference_size * 0.5)
			placement_center = source_position + center_offset
			piece.position = _art_to_world(placement_center, item_z)
			piece.pixel_size = _pixel_size_for_depth(item_z)
			piece.set_meta("source_art_rect",
				Rect2(source_position, reference_size))
			piece.set_meta("depth_z", item_z)
		else:
			_place_art_card(piece, source_position, item_z)
			placement_center = source_position + reference_size * 0.5
	piece.scale = Vector3.ONE * visual_scale
	piece.flip_h = bool(item_data.get("flip_h", false))
	piece.set_meta("source_asset_role", "physical_room_door"
		if item_data.has("room_destination") else "unique_object")
	piece.set_meta("source_object_id", room_id + ":" + item_id)
	piece.set_meta("semantic_action", String(item_data.get(
		"semantic_action", "")))
	piece.set_meta("roleplay_action", String(item_data.get(
		"roleplay_action", "")))
	piece.set_meta("castle_physical_door", item_data.has("room_destination"))
	piece.set_meta("room_destination", String(item_data.get(
		"room_destination", "")))
	piece.set_meta("frames", int(item_data.get("frames", 1)))
	piece.set_meta("hframes", piece.hframes)
	piece.set_meta("vframes", piece.vframes)
	piece.set_meta("frame_duration", float(item_data.get(
		"frame_duration", 0.10)))
	piece.set_meta("sound", String(item_data.get("sound", "")))
	piece.set_meta("sound_frame", int(item_data.get("sound_frame", 0)))
	piece.set_meta("animation_frame_count", int(item_data.get("frames", 1)))
	piece.set_meta("animation_frame_duration", float(item_data.get(
		"frame_duration", 0.10)))
	piece.set_meta("animation_frames_visited", [])
	piece.set_meta("fixed_pivot_animation", not interaction_spec.is_empty()
		or item_data.has("semantic_action")
		or item_data.has("roleplay_action"))
	if bunny_role != "":
		piece.set_meta("dust_bunny_role", bunny_role)
		piece.set_meta("spawn_guide_id", item_id)
		# One hit point, always. A single contact with Roshan's foot clears the
		# bunny; nothing a dust bunny does can ever damage her back.
		piece.set_meta("dust_bunny_hp", HALL_BUNNY_HP)
		piece.set_meta("dust_bunny_state",
			"asleep" if bunny_role == "sleeping_static" else (
				"hidden" if bunny_role == "shell_static" else "resting"))
	piece.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
	if item_data.has("room_destination"):
		piece.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	if item_data.has("light_cluster"):
		piece.shaded = false
		piece.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		var fixture_material := ShaderMaterial.new()
		fixture_material.shader = CASTLE_FIXTURE_BLOOM_SHADER
		fixture_material.set_shader_parameter("fixture_texture", texture)
		piece.material_override = fixture_material
		piece.set_meta("castle_fixture_material", fixture_material)
		_sync_sconce_frame_uv(piece)
		if not m.castle_room_light_states.has(item_id):
			m.castle_room_light_states[item_id] = true
		_apply_sconce_visual(piece, bool(m.castle_room_light_states[item_id]))
	m.castle_room_item_visual_layer.add_child(piece)
	if item_data.has("roleplay_plate"):
		var plate_index: int = int(item_data["roleplay_plate"])
		piece.visible = plate_index < int(m.g.get(
			"castle_dining_plates", 0))

	var hotspot: Button = null
	var hotspot_group: String = String(item_data.get("hotspot_group", ""))
	var owns_hotspot: bool = hotspot_group == "" \
		or bool(item_data.get("hotspot_owner", false))
	if not bool(item_data.get("proximity_only", false)) and owns_hotspot:
		hotspot = Button.new()
		hotspot.name = "Touch_" + (
			hotspot_group if hotspot_group != "" else item_id)
		hotspot.flat = true
		hotspot.focus_mode = Control.FOCUS_NONE
		hotspot.tooltip_text = "Copper pan rack" \
			if hotspot_group == "pan_rack" else String(item_data["name"])
		hotspot.set_meta("uses_own_sfx", true)
		hotspot.set_meta("hotspot_group", hotspot_group)
		hotspot.set_meta("physical_door", item_data.has("room_destination"))
		hotspot.set_meta("room_destination", String(item_data.get(
			"room_destination", "")))
		var hotspot_offset: Vector2 = item_data.get(
			"hotspot_offset", Vector2.ZERO)
		hotspot.position = (source_position + hotspot_offset) * ART_TO_STAGE
		hotspot.size = item_data.get("hotspot_size", Vector2(112.0, 112.0))
		hotspot.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
		hotspot.pressed.connect(_activate_room_item.bind(item_id))
		m.castle_room_item_hotspot_layer.add_child(hotspot)
	var contact_offset: Vector2 = item_data.get(
		"contact_offset", Vector2.ZERO) as Vector2
	var contact_foot: Vector2 = item_data.get(
		"contact_foot", source_position + contact_offset) as Vector2
	var contact_radius: Vector2 = item_data.get(
		"contact_radius", Vector2(120.0, 88.0)) as Vector2
	if room_id != "main_hall":
		contact_foot *= ART_TO_STAGE
		contact_radius *= ART_TO_STAGE
	var frame_size: Vector2 = _sprite_frame_size(piece)
	var visual_size: Vector2 = reference_size * authored_visual_scale
	var visual_center: Vector2 = source_position \
		if room_id == "main_hall" \
		else source_position + reference_size * 0.5
	var visible_frame_rect := Rect2(Vector2.ZERO, frame_size)
	if not v2_visual.is_empty():
		var visible_min := Vector2(INF, INF)
		var visible_max := Vector2(-INF, -INF)
		var valid_bbox_count := 0
		for bbox_value: Variant in v2_visual.get("frame_bboxes", []):
			var bbox: Array = bbox_value as Array
			if bbox.size() != 4:
				continue
			visible_min.x = minf(visible_min.x, float(bbox[0]))
			visible_min.y = minf(visible_min.y, float(bbox[1]))
			visible_max.x = maxf(visible_max.x, float(bbox[2]))
			visible_max.y = maxf(visible_max.y, float(bbox[3]))
			valid_bbox_count += 1
		if valid_bbox_count > 0:
			visible_frame_rect = Rect2(
				visible_min, visible_max - visible_min)
	if piece.flip_h:
		visible_frame_rect.position = Vector2(
			frame_size.x - visible_frame_rect.end.x,
			visible_frame_rect.position.y)
	var rendered_art_rect := Rect2(
		placement_center + (visible_frame_rect.position
			- frame_size * 0.5) * visual_scale,
		visible_frame_rect.size * visual_scale)
	var authored_hotspot_size: Vector2 = item_data.get(
		"hotspot_size", reference_size) as Vector2
	var authored_hotspot_offset: Vector2 = item_data.get(
		"hotspot_offset",
		(reference_size - authored_hotspot_size) * 0.5) as Vector2
	var hotspot_local_center := authored_hotspot_offset \
		+ authored_hotspot_size * 0.5 - frame_size * 0.5
	var hotspot_local_size := authored_hotspot_size
	if not v2_visual.is_empty():
		var reference_center := source_position \
			if room_id == "main_hall" \
			else source_position + reference_size * 0.5
		var hotspot_reference_center := reference_center \
			+ (authored_hotspot_offset + authored_hotspot_size * 0.5 \
				- reference_size * 0.5) * authored_visual_scale
		hotspot_local_center = (hotspot_reference_center - placement_center) \
			/ maxf(0.001, visual_scale)
		hotspot_local_size = authored_hotspot_size \
			/ maxf(0.001, runtime_scale)
	m.castle_room_item_sprites[item_id] = {
		"sprite": piece,
		"hotspot": hotspot,
		"data": item_data,
		"contact_foot": contact_foot,
		"contact_radius": contact_radius,
		"frame_size": frame_size,
		"hotspot_size": authored_hotspot_size,
		"hotspot_offset": authored_hotspot_offset,
		"hotspot_local_center_pixels": hotspot_local_center,
		"hotspot_local_size_pixels": hotspot_local_size,
		"reference_size": reference_size,
		"placement_center": placement_center,
		"art_rect": Rect2(
			visual_center - visual_size * 0.5, visual_size),
		"render_art_rect": rendered_art_rect,
	}
	var stored_record: Dictionary = m.castle_room_item_sprites[item_id]
	stored_record["fixture_rig"] = fixture_rigs.build(
		interaction_key, piece, item_data, source_position, reference_size,
		item_z, Callable(self, "_art_to_world"))
	if bunny_role != "":
		_init_dust_bunny_behavior(
			stored_record, room_id, item_data, source_position, visual_scale)
	_update_touch_hotspot(stored_record)
	if room_id == "playroom" and item_id == "baby_eagle_rescue":
		_add_playroom_rescue_pointer()

func _activate_room_item(item_id: String) -> void:
	if _fridge_close_is_blocked():
		return
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
	if item_id == "throne" and m.castle_room_id == "main_hall":
		# Touching the Royal throne opens the replayable sparring class.
		_play_item_sfx(String(item_data.get("sound", "chime.ogg")),
			float(item_data.get("pitch", 1.25)))
		_item_burst(sprite.position,
			Color(item_data.get("color", StorybookUI.GOLD)), 8)
		var launch := m.create_tween()
		launch.tween_interval(0.45)
		launch.tween_callback(_start_combat_tutorial)
		return
	var roleplay_action: String = String(item_data.get(
		"roleplay_action", ""))
	if roleplay_action != "":
		_activate_roleplay_item(
			roleplay_action, item_id, sprite, item_data)
		return
	var hotspot_group: String = String(item_data.get("hotspot_group", ""))
	if hotspot_group != "":
		_activate_item_group(hotspot_group, item_id)
		return
	var interaction_key := String(sprite.get_meta("source_object_id", ""))
	fixture_rigs.activate(interaction_key)
	_item_burst(sprite.position,
		Color(item_data.get("color", StorybookUI.GOLD)), 6)
	# A prop coming to life next to a dust bunny scares it off — the painted
	# shell tapestry is the loud one in this hall.
	if _is_wide_hall():
		_startle_dust_bunnies(
			(item_data.get("pos", Vector2.ZERO) as Vector2).x,
			HALL_BUNNY_STARTLE_RADIUS)
	_play_sprite_atlas_sequence(sprite, item_data, true,
		m.castle_room_id == "kitchen" and item_id == "fridge")

func _activate_roleplay_item(roleplay_action: String, item_id: String,
		sprite: Sprite3D, item_data: Dictionary) -> void:
	match roleplay_action:
		"enter_room":
			_enter_gallery_room(sprite, item_data)
		"serve_meal":
			_serve_dining_meal(sprite, item_data)
		"eat_meal":
			_eat_dining_meal(sprite, item_data)
		"sleep":
			_start_roleplay_sleep(sprite, item_data)
		"watch_movie":
			_cycle_home_movie(sprite, item_data)
		"relax":
			_relax_on_furniture(sprite, item_data)
		"dress_up":
			_roleplay_prop_bounce(sprite, item_data)
			_item_burst(sprite.position, Color(1.0, 0.67, 0.82), 8)
			m.show_msg("Roshan",
				"Pretend dress-up time! A crown, a cape, or both!", "talk")
		"bedside_light":
			_toggle_bedside_light(sprite, item_data)
		_:
			push_warning("Unknown castle role-play action: %s (%s)" % [
				roleplay_action, item_id])

func _enter_gallery_room(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	if sprite == null or not is_instance_valid(sprite) \
			or bool(sprite.get_meta("busy", false)):
		return
	var destination: String = String(item_data.get("room_destination", ""))
	if _room(destination).is_empty():
		return
	sprite.set_meta("busy", true)
	for hotspot_node: Node in m.castle_room_item_hotspot_layer.get_children():
		var door_hotspot: Button = hotspot_node as Button
		if door_hotspot != null:
			door_hotspot.disabled = true
	_play_item_sfx(String(item_data.get("sound", "ui_tap.ogg")),
		float(item_data.get("pitch", 1.0)))
	var roleplay_foot: Vector2 = item_data.get(
		"roleplay_foot", Vector2(640.0, 620.0)) as Vector2
	var old_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", roleplay_foot) as Vector2
	var duration: float = clampf(
		old_foot.distance_to(roleplay_foot) / 520.0,
		0.12, 0.85)
	_position_player_at_foot(roleplay_foot, true)
	_item_burst(sprite.position,
		Color(item_data.get("color", StorybookUI.GOLD)), 8)
	var transition := m.create_tween()
	transition.tween_interval(duration + 0.04)
	transition.tween_callback(show_room.bind(destination, true))

func _roleplay_prop_bounce(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	if sprite == null or not is_instance_valid(sprite) \
			or bool(sprite.get_meta("busy", false)):
		return
	sprite.set_meta("busy", true)
	_play_item_sfx(String(item_data.get("sound", "ui_tap.ogg")),
		float(item_data.get("pitch", 1.0)))
	var original_scale: Vector3 = sprite.scale
	var bounce := sprite.create_tween()
	bounce.tween_property(sprite, "scale", original_scale * 1.08,
		0.14).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	bounce.tween_property(sprite, "scale", original_scale,
		0.20).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	bounce.tween_callback(_finish_roleplay_prop_bounce.bind(
		sprite, original_scale))

func _finish_roleplay_prop_bounce(sprite: Sprite3D,
		original_scale: Vector3) -> void:
	if sprite == null or not is_instance_valid(sprite):
		return
	sprite.scale = original_scale
	sprite.set_meta("busy", false)

func _serve_dining_meal(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	m.g["castle_dining_plates"] = 6
	_sync_dining_plates()
	_roleplay_prop_bounce(sprite, item_data)
	_item_burst(sprite.position, Color(0.58, 0.94, 0.82), 10)
	m.show_msg("Roshan",
		"Dinner is served! Everyone gets a plate at the family table.",
		"hungry")

func _eat_dining_meal(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	var plate_count: int = int(m.g.get("castle_dining_plates", 0))
	if plate_count <= 0:
		_serve_dining_meal(sprite, item_data)
		return
	plate_count -= 1
	m.g["castle_dining_plates"] = plate_count
	_sync_dining_plates()
	var roleplay_foot: Vector2 = item_data.get(
		"roleplay_foot", Vector2(512.0, 555.0)) as Vector2
	_position_player_at_foot(roleplay_foot, true)
	_roleplay_prop_bounce(sprite, item_data)
	_item_burst(sprite.position, Color(1.0, 0.68, 0.76), 7)
	if plate_count == 0:
		m.show_msg("Roshan",
			"Yum! The feast is finished. We can serve another one!", "win")
	else:
		m.show_msg("Roshan",
			"Yum! One happy bite at the family table.", "hungry")

func _sync_dining_plates() -> void:
	var plate_count: int = clampi(
		int(m.g.get("castle_dining_plates", 0)), 0, 6)
	m.g["castle_dining_plates"] = plate_count
	for plate_index in range(6):
		var item_id := "meal_plate_%d" % plate_index
		var record: Dictionary = m.castle_room_item_sprites.get(
			item_id, {}) as Dictionary
		var plate: Sprite3D = record.get("sprite") as Sprite3D
		if plate != null:
			plate.visible = plate_index < plate_count

func _start_roleplay_sleep(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	if bool(m.g.get("castle_roleplay_sleeping", false)):
		return
	if m.castle_room_stage == null:
		return
	m.g["castle_roleplay_sleeping"] = true
	sprite.set_meta("busy", true)
	_play_item_sfx(String(item_data.get("sound", "chime.ogg")),
		float(item_data.get("pitch", 0.84)))
	var roleplay_foot: Vector2 = item_data.get(
		"roleplay_foot", Vector2(512.0, 555.0)) as Vector2
	_position_player_at_foot(roleplay_foot, true)
	m._set_world_controls_enabled(false, "castle_roleplay_sleep")
	m.show_msg("Roshan",
		"Cosy bedtime in the dream house... zzz.", "talk")

	var overlay := ColorRect.new()
	overlay.name = "DreamHouseSleepFade"
	overlay.position = Vector2.ZERO
	overlay.size = StorybookUI.CANVAS_SIZE
	overlay.color = Color(0.035, 0.025, 0.12, 0.0)
	overlay.mouse_filter = Control.MOUSE_FILTER_STOP
	overlay.z_index = 80
	m.castle_room_stage.add_child(overlay)
	var sleepy_marks := Label.new()
	sleepy_marks.name = "DreamHouseSleepMarks"
	sleepy_marks.text = "z   Z   z"
	sleepy_marks.position = Vector2(490.0, 245.0)
	sleepy_marks.size = Vector2(300.0, 120.0)
	sleepy_marks.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(
		sleepy_marks, 72, Color(0.78, 0.88, 1.0), 5)
	sleepy_marks.modulate.a = 0.0
	sleepy_marks.z_index = 81
	m.castle_room_stage.add_child(sleepy_marks)

	if m.castle_room_player_sprite != null:
		var tuck := m.castle_room_player_sprite.create_tween()
		tuck.tween_interval(0.28)
		tuck.tween_property(
			m.castle_room_player_sprite, "rotation:z", -0.14, 0.32)
	var dream := overlay.create_tween()
	dream.tween_property(overlay, "color:a", 0.90,
		0.58).set_trans(Tween.TRANS_SINE)
	dream.parallel().tween_property(
		sleepy_marks, "modulate:a", 1.0, 0.42)
	dream.tween_callback(_flip_roleplay_sleep_time)
	dream.tween_interval(0.35)
	dream.tween_property(overlay, "color:a", 0.0,
		0.72).set_trans(Tween.TRANS_SINE)
	dream.parallel().tween_property(
		sleepy_marks, "modulate:a", 0.0, 0.52)
	dream.tween_callback(_finish_roleplay_sleep.bind(
		overlay, sleepy_marks, sprite))

func _flip_roleplay_sleep_time() -> void:
	m._set_night(not m.is_night)

func _finish_roleplay_sleep(overlay: ColorRect, sleepy_marks: Label,
		sprite: Sprite3D) -> void:
	if overlay != null and is_instance_valid(overlay):
		overlay.queue_free()
	if sleepy_marks != null and is_instance_valid(sleepy_marks):
		sleepy_marks.queue_free()
	if sprite != null and is_instance_valid(sprite):
		sprite.set_meta("busy", false)
	if m.castle_room_player_sprite != null:
		m.castle_room_player_sprite.rotation.z = 0.0
	_center_player()
	m.g["castle_roleplay_sleeping"] = false
	m._set_world_controls_enabled(true, "castle_roleplay_sleep")
	_burst("✦", Color(0.78, 0.88, 1.0))
	if m.is_night:
		m.show_msg("Roshan",
			"What a lovely nap! The moon is shining now.", "win")
	else:
		m.show_msg("Roshan",
			"Good morning! The dream house is ready to play.", "win")

func _sync_movie_picture() -> void:
	if MOVIE_IMAGES.is_empty():
		return
	var movie_index: int = posmod(
		int(m.g.get("castle_movie_index", 0)), MOVIE_IMAGES.size())
	m.g["castle_movie_index"] = movie_index
	var record: Dictionary = m.castle_room_item_sprites.get(
		"movie_picture", {}) as Dictionary
	var picture: Sprite3D = record.get("sprite") as Sprite3D
	if picture == null:
		return
	var picture_texture: Texture2D = load(MOVIE_IMAGES[movie_index]) as Texture2D
	if picture_texture != null:
		picture.texture = picture_texture
		picture.set_meta("movie_index", movie_index)
		picture.set_meta("protected_original_displayed_directly", true)

func _cycle_home_movie(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	var movie_index: int = int(m.g.get("castle_movie_index", 0))
	m.g["castle_movie_index"] = posmod(
		movie_index + 1, MOVIE_IMAGES.size())
	_sync_movie_picture()
	_roleplay_prop_bounce(sprite, item_data)
	_item_burst(sprite.position, Color(1.0, 0.82, 0.42), 8)
	m.show_msg("Roshan",
		"Movie night! Pick a cloud couch and watch our family adventure.",
		"talk")

func _relax_on_furniture(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	var roleplay_foot: Vector2 = item_data.get(
		"roleplay_foot", Vector2(512.0, 555.0)) as Vector2
	_position_player_at_foot(roleplay_foot, true)
	_roleplay_prop_bounce(sprite, item_data)
	_item_burst(sprite.position,
		Color(item_data.get("color", Color(0.78, 0.86, 1.0))), 6)
	m.show_msg("Roshan",
		"Cloud-couch cuddle time! We can relax as long as we like.", "talk")

func _toggle_bedside_light(sprite: Sprite3D,
		item_data: Dictionary) -> void:
	var light_on: bool = not bool(m.g.get(
		"castle_bedside_light_on", false))
	m.g["castle_bedside_light_on"] = light_on
	sprite.modulate = Color(1.12, 1.03, 0.78, 1.0) if light_on \
		else Color(0.64, 0.66, 0.80, 1.0)
	_roleplay_prop_bounce(sprite, item_data)
	_item_burst(sprite.position, Color(1.0, 0.88, 0.48), 6)
	m.show_msg("Roshan",
		"Bedtime pearl light on!" if light_on \
		else "Bedtime pearl light off. So cosy!", "talk")

func _sync_bedside_light() -> void:
	var record: Dictionary = m.castle_room_item_sprites.get(
		"bedside_table", {}) as Dictionary
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite == null:
		return
	sprite.modulate = Color(1.12, 1.03, 0.78, 1.0) \
		if bool(m.g.get("castle_bedside_light_on", false)) \
		else Color(0.64, 0.66, 0.80, 1.0)

func _activate_item_group(hotspot_group: String, _owner_item_id: String) -> void:
	var group_records: Array[Dictionary] = []
	for record_value: Variant in m.castle_room_item_sprites.values():
		var record: Dictionary = record_value as Dictionary
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if String(item_data.get("hotspot_group", "")) != hotspot_group:
			continue
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		if sprite == null or bool(sprite.get_meta("busy", false)):
			return
		group_records.append(record)
	if group_records.is_empty():
		return
	for record: Dictionary in group_records:
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if sprite != null:
			fixture_rigs.activate(String(
				sprite.get_meta("source_object_id", "")))
		_play_sprite_atlas_sequence(
			sprite, item_data, bool(item_data.get("hotspot_owner", false)), false)

func _toggle_hall_sconce(item_id: String, sprite: Sprite3D,
		item_data: Dictionary) -> void:
	var now_on: bool = not bool(m.castle_room_light_states.get(item_id, true))
	m.castle_room_light_states[item_id] = now_on
	_apply_sconce_visual(sprite, now_on)
	var playback_data: Dictionary = item_data.duplicate(true)
	var sequence: Array[int] = []
	if now_on:
		for frame_index in range(8):
			sequence.append(frame_index)
	else:
		for frame_index in range(7, -1, -1):
			sequence.append(frame_index)
	playback_data["timeline_sequence"] = sequence
	playback_data["timeline_frames"] = sequence.size()
	playback_data["rest_frame"] = 7 if now_on else 0
	playback_data["pitch"] = 1.0
	_play_sprite_atlas_sequence(sprite, playback_data, true, false)
	_sync_hall_lighting()
	# Light dictates dust-bunny behaviour: a shell sconce coming on wakes the
	# sleepers under it. Switching one off never wakes anything.
	if now_on:
		_wake_dust_bunnies_near(
			(item_data.get("pos", Vector2.ZERO) as Vector2).x,
			HALL_BUNNY_LIGHT_REACH)

func _sync_sconce_frame_uv(sprite: Sprite3D) -> void:
	if sprite == null or not is_instance_valid(sprite):
		return
	if not sprite.has_meta("castle_fixture_material"):
		return
	var material: ShaderMaterial = sprite.get_meta(
		"castle_fixture_material", null) as ShaderMaterial
	if material == null:
		return
	var columns: int = maxi(1, sprite.hframes)
	var rows: int = maxi(1, sprite.vframes)
	var frame_column: int = sprite.frame % columns
	var frame_row: int = int(sprite.frame / columns)
	var frame_uv := Vector4(
		float(frame_column) / float(columns),
		float(frame_row) / float(rows),
		float(frame_column + 1) / float(columns),
		float(frame_row + 1) / float(rows))
	material.set_shader_parameter("fixture_uv_rect", frame_uv)
	sprite.set_meta("fixture_uv_rect", frame_uv)

func _apply_sconce_visual(sprite: Sprite3D, is_on: bool) -> void:
	if sprite == null:
		return
	if not bool(sprite.get_meta("busy", false)):
		sprite.frame = 7 if is_on else 0
	_sync_sconce_frame_uv(sprite)
	# The Mobile renderer did not reliably carry an HDR Sprite3D modulate into
	# the Environment glow buffer. A true unshaded spatial emission on this
	# same fixture card produces localized bloom without a halo/button card.
	var material: ShaderMaterial = sprite.get_meta(
		"castle_fixture_material", null) as ShaderMaterial
	if material != null:
		material.set_shader_parameter(
			"fixture_tint",
			Color(1.0, 0.96, 0.90, 1.0)
				if is_on else Color(0.48, 0.46, 0.58, 0.78))
		material.set_shader_parameter(
			"emission_color", Color(1.0, 0.67, 0.30))
		material.set_shader_parameter(
			"emission_energy",
			5.6 if is_on and m.quality != "speedy"
				else 4.8 if is_on else 0.0)
	sprite.modulate = Color.WHITE
	sprite.set_meta("castle_light_on", is_on)
	sprite.set_meta("castle_bloom_emitter", is_on)
	sprite.set_meta(
		"castle_emission_energy",
		5.6 if is_on and m.quality != "speedy"
			else 4.8 if is_on else 0.0)

func _sync_hall_lighting() -> void:
	if m.castle_room_light_nodes.is_empty():
		return
	var hall_visible: bool = is_open() and m.castle_room_id == "main_hall"
	var camera_center_art: float = HALL_LOGICAL_SIZE.x * 0.5
	if m.castle_room_camera != null:
		camera_center_art += m.castle_room_camera.position.x \
			/ HALL_CARD_PIXEL_SIZE
	# Pick the two nearest authored fixture clusters inside the current camera
	# neighborhood. At the A/B seam this deliberately selects A-right and
	# B-left, preventing the former whole-screen hard lighting boundary while
	# preserving the two-spot Mobile budget.
	var active_cluster_ids: Array[String] = []
	var cluster_radius: float = HALL_VIEW_SIZE.x * 0.62
	for _slot in range(2):
		var nearest_id := ""
		var nearest_distance := INF
		for cluster_data: Dictionary in HALL_LIGHT_CLUSTERS:
			var cluster_id: String = String(cluster_data["id"])
			if cluster_id in active_cluster_ids:
				continue
			var cluster_position: Vector2 = cluster_data["pos"] as Vector2
			var distance: float = absf(cluster_position.x - camera_center_art)
			if distance <= cluster_radius and distance < nearest_distance:
				nearest_id = cluster_id
				nearest_distance = distance
		if nearest_id != "":
			active_cluster_ids.append(nearest_id)
	var active_fixture_count := 0
	var active_lit_count := 0
	for item_data: Dictionary in HALL_ITEMS:
		if not item_data.has("light_cluster"):
			continue
		var item_cluster: String = String(item_data["light_cluster"])
		var item_id: String = String(item_data["id"])
		var item_record: Dictionary = m.castle_room_item_sprites.get(
			item_id, {})
		var item_sprite: Sprite3D = item_record.get("sprite") as Sprite3D
		var item_is_on: bool = bool(m.castle_room_light_states.get(
			item_id, true))
		if item_sprite != null:
			_apply_sconce_visual(item_sprite, item_is_on)
		if item_cluster not in active_cluster_ids:
			continue
		active_fixture_count += 1
		if item_is_on:
			active_lit_count += 1
	var active_light_ratio: float = float(active_lit_count) \
		/ maxf(1.0, float(active_fixture_count))
	var speedy_shadow_used := false
	for light: Light3D in m.castle_room_light_nodes:
		if light == null or not is_instance_valid(light):
			continue
		var role: String = String(light.get_meta("castle_light_role", ""))
		if role == "ambient_fill":
			light.visible = hall_visible
			light.light_energy = lerpf(
				HALL_FILL_OFF_ENERGY, HALL_FILL_ENERGY, active_light_ratio)
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
		var cluster_is_active: bool = cluster_id in active_cluster_ids
		light.visible = hall_visible and cluster_is_active and lit_count > 0
		var max_energy: float = float(light.get_meta("max_energy", 2.5))
		light.light_energy = lerpf(0.55, max_energy, energy_ratio)
		if not light.visible:
			light.shadow_enabled = false
		elif m.quality == "speedy":
			light.shadow_enabled = not speedy_shadow_used
			speedy_shadow_used = true
		else:
			light.shadow_enabled = true
	_sync_castle_environment(hall_visible, active_light_ratio)

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
			0.98, 0.58, half_light_ratio)
		environment.ambient_light_energy = lerpf(
			0.12, 0.26, half_light_ratio)
		environment.adjustment_saturation = lerpf(
			0.66, 0.50, half_light_ratio)
		environment.adjustment_contrast = lerpf(
			1.12, 1.20, half_light_ratio)
		environment.adjustment_brightness = lerpf(
			0.84, 1.12, half_light_ratio)
	else:
		# Destination rooms keep the castle's warm storybook finish, but their
		# painted practical lights do not receive the Main Hall's dramatic lift.
		# These rooms are pure unshaded painting: no light touches the cards, so
		# this grade is the ONLY thing between the approved PNG and the child.
		# 2026-08-02 (LIGHTING_2P5D_AUDIT §1.7/§E1): the previous 1.08/1.10/0.94
		# stack drove 21.5% of room pixels into single-channel clipping that the
		# source art did not have — saturated lavender walls losing their blue
		# channel read as a hue shift, not as a brighter room. Held near unity
		# now; the rooms get their richness from the paint.
		environment.glow_intensity = 0.48 if speedy else 0.66
		environment.glow_bloom = 0.055 if speedy else 0.09
		environment.glow_hdr_threshold = 0.90
		environment.ambient_light_energy = 0.28
		environment.adjustment_saturation = 1.02
		environment.adjustment_contrast = 1.02
		environment.adjustment_brightness = 0.98

func _play_item_sfx(sound_file: String, pitch: float) -> void:
	if m.castle_room_prop_sfx == null:
		return
	var path := sound_file
	if not path.begins_with("res://"):
		path = "res://" + path if path.begins_with("assets/audio/") 			else "res://assets/audio/" + path
	if not ResourceLoader.exists(path):
		return
	m.castle_room_prop_sfx.stream = load(path)
	m.castle_room_prop_sfx.pitch_scale = pitch
	m.castle_room_prop_sfx.play()

func _timeline_sequence(item_data: Dictionary,
		available_frames: int) -> Array[int]:
	var sequence: Array[int] = []
	var raw_sequence: Array = item_data.get("timeline_sequence", []) as Array
	if raw_sequence.is_empty():
		var count: int = clampi(int(item_data.get(
			"timeline_frames", item_data.get("frames", available_frames))), 1, 12)
		for frame_index in range(count):
			sequence.append(clampi(frame_index, 0, available_frames - 1))
	else:
		for frame_value: Variant in raw_sequence:
			sequence.append(clampi(int(frame_value), 0, available_frames - 1))
			if sequence.size() >= 12:
				break
	if sequence.is_empty():
		sequence.append(0)
	return sequence


func _play_sprite_atlas_sequence(sprite: Sprite3D, item_data: Dictionary,
		play_sound: bool, open_kitchen_menu_after: bool) -> void:
	if sprite == null or not is_instance_valid(sprite) \
			or bool(sprite.get_meta("busy", false)):
		return
	var available_frames: int = maxi(1, sprite.hframes * sprite.vframes)
	var sequence := _timeline_sequence(item_data, available_frames)
	var timeline_count: int = sequence.size()
	var frame_duration: float = maxf(
		0.01, float(item_data.get("frame_duration", 0.10)))
	var interaction_key := String(sprite.get_meta("source_object_id", ""))
	var terminal_step := timeline_count - 1
	if open_kitchen_menu_after:
		terminal_step = mini(terminal_step,
			int(item_data.get("open_hold_step", terminal_step)))
	sprite.set_meta("busy", true)
	sprite.frame = sequence[0]
	_sync_sconce_frame_uv(sprite)
	fixture_rigs.apply_frame(interaction_key, 0, timeline_count)
	var visited: Array[int] = [sequence[0]]
	var timeline_visited: Array[int] = [0]
	sprite.set_meta("animation_frames_visited", visited)
	sprite.set_meta("animation_timeline_steps_visited", timeline_visited)
	if play_sound and int(item_data.get("sound_frame", 0)) == 0:
		_play_item_sfx(String(item_data.get("sound", "ui_tap.ogg")),
			float(item_data.get("pitch", 1.0)))
	if terminal_step <= 0:
		_finish_sprite_atlas_sequence(
			sprite, item_data, open_kitchen_menu_after, terminal_step)
		return
	var tween := sprite.create_tween()
	for timeline_step in range(1, terminal_step + 1):
		tween.tween_interval(frame_duration)
		tween.tween_callback(_show_item_atlas_frame.bind(
			sprite, item_data, timeline_step, play_sound))
	tween.tween_interval(frame_duration)
	tween.tween_callback(_finish_sprite_atlas_sequence.bind(
		sprite, item_data, open_kitchen_menu_after, terminal_step))


func _show_item_atlas_frame(sprite: Sprite3D, item_data: Dictionary,
		timeline_step: int, play_sound: bool) -> void:
	if sprite == null or not is_instance_valid(sprite):
		return
	var available_frames: int = maxi(1, sprite.hframes * sprite.vframes)
	var sequence := _timeline_sequence(item_data, available_frames)
	var step := clampi(timeline_step, 0, sequence.size() - 1)
	var atlas_frame: int = sequence[step]
	sprite.frame = atlas_frame
	_sync_sconce_frame_uv(sprite)
	var visited: Array = sprite.get_meta("animation_frames_visited", []) as Array
	visited.append(atlas_frame)
	sprite.set_meta("animation_frames_visited", visited)
	var timeline_visited: Array = sprite.get_meta(
		"animation_timeline_steps_visited", []) as Array
	timeline_visited.append(step)
	sprite.set_meta("animation_timeline_steps_visited", timeline_visited)
	var interaction_key := String(sprite.get_meta("source_object_id", ""))
	fixture_rigs.apply_frame(interaction_key, step, sequence.size())
	if play_sound and step == int(item_data.get("sound_frame", 0)):
		_play_item_sfx(String(item_data.get("sound", "ui_tap.ogg")),
			float(item_data.get("pitch", 1.0)))


func _finish_sprite_atlas_sequence(sprite: Sprite3D, item_data: Dictionary,
		open_kitchen_menu_after: bool, terminal_step: int) -> void:
	if sprite == null or not is_instance_valid(sprite):
		return
	var available_frames: int = maxi(1, sprite.hframes * sprite.vframes)
	var sequence := _timeline_sequence(item_data, available_frames)
	var interaction_key := String(sprite.get_meta("source_object_id", ""))
	if open_kitchen_menu_after:
		var step := clampi(terminal_step, 0, sequence.size() - 1)
		sprite.frame = sequence[step]
		fixture_rigs.apply_frame(interaction_key, step, sequence.size())
	else:
		var rest_frame: int = int(item_data.get("rest_frame", 0))
		sprite.frame = clampi(rest_frame, 0, available_frames - 1)
		fixture_rigs.apply_frame(interaction_key, 0, sequence.size())
	if sprite.has_meta("active_close_tween"):
		sprite.remove_meta("active_close_tween")
	_sync_sconce_frame_uv(sprite)
	sprite.set_meta("busy", false)
	if bool(sprite.get_meta(
			"enable_world_controls_after_close", false)):
		sprite.remove_meta("enable_world_controls_after_close")
		_set_fridge_close_blocked(false)
		m._set_world_controls_enabled(true, "kitchen_fridge_close")
	if open_kitchen_menu_after and m.castle_room_id == "kitchen":
		_open_kitchen_menu()


func _close_fridge_visual() -> bool:
	var record: Dictionary = m.castle_room_item_sprites.get("fridge", {})
	if record.is_empty():
		return false
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	var item_data: Dictionary = record.get("data", {}) as Dictionary
	if sprite == null or bool(sprite.get_meta("busy", false)):
		return false
	var rest_frame: int = int(item_data.get("rest_frame", 0))
	if sprite.frame == rest_frame:
		return false
	var available_frames: int = maxi(1, sprite.hframes * sprite.vframes)
	var sequence := _timeline_sequence(item_data, available_frames)
	var start_step: int = clampi(
		int(item_data.get("open_hold_step", 4)), 0, sequence.size() - 1)
	var frame_duration: float = maxf(
		0.01, float(item_data.get("frame_duration", 0.10)))
	sprite.set_meta("busy", true)
	sprite.set_meta("enable_world_controls_after_close", true)
	sprite.set_meta("animation_frames_visited", [sequence[start_step]])
	sprite.set_meta("animation_timeline_steps_visited", [start_step])
	_play_item_sfx(String(item_data.get(
		"close_sound", "castle/fridge_close.ogg")),
		float(item_data.get("close_pitch", 0.94)))
	var tween := sprite.create_tween()
	sprite.set_meta("active_close_tween", tween)
	for timeline_step in range(start_step + 1, sequence.size()):
		tween.tween_interval(frame_duration)
		tween.tween_callback(_show_item_atlas_frame.bind(
			sprite, item_data, timeline_step, false))
	tween.tween_interval(frame_duration)
	tween.tween_callback(_finish_sprite_atlas_sequence.bind(
		sprite, item_data, false, sequence.size() - 1))

	return true

func _item_burst(center: Vector3, color: Color, count: int) -> void:
	if m.castle_room_item_effect_layer == null:
		return
	var star_texture: Texture2D = load("res://assets/mg/star.png")
	for index in range(count):
		var mote: Sprite3D = _new_card("TouchSparkle", star_texture)
		mote.set_meta("source_asset_role", "transient_effect")
		var local_effect_z := center.z + 0.035
		mote.pixel_size = _pixel_size_for_depth(local_effect_z)
		mote.scale = Vector3.ONE * randf_range(0.018, 0.032)
		mote.modulate = color
		mote.position = Vector3(
			center.x + randf_range(-0.75, 0.75),
			center.y + randf_range(-0.20, 0.35),
			local_effect_z)
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
	# Discard below the painted silhouette before depth testing. Opaque prepass
	# made routing-mask pixels participate in depth and could erase Roshan even
	# where the card appeared to contain only background.
	card.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	card.alpha_scissor_threshold = 0.5
	card.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	card.set_meta("castle_world_sprite3d", true)
	return card

func _place_art_card(card: Sprite3D, source_position: Vector2,
		depth_z: float) -> void:
	if card == null or card.texture == null:
		return
	var frame_size: Vector2 = _sprite_frame_size(card)
	var center_art: Vector2 = source_position + frame_size * 0.5
	card.position = _art_to_world(center_art, depth_z)
	card.pixel_size = _pixel_size_for_depth(depth_z)
	card.set_meta("source_art_rect", Rect2(source_position, frame_size))
	card.set_meta("depth_z", depth_z)
	# Depth is geometric here but was never tonal: every plane rendered at pure
	# white, so a framing prop 4 units in front of the wall read as a sticker on
	# it (LIGHTING_2P5D_AUDIT_2026-08-02 §W2/§E2). The rig multiplies the card
	# by its plane's tint — background stays the untouched reference, foreground
	# settles back. Light fixtures opt themselves out inside the rig.
	m.light_rig().apply_to_card(card, "castle_room", depth_z,
		String(card.get_meta("intensity_class", "")))

func _v2_vector2(value: Variant, fallback: Vector2) -> Vector2:
	if value is Array:
		var values: Array = value as Array
		if values.size() >= 2:
			return Vector2(float(values[0]), float(values[1]))
	return fallback

func _sprite_frame_size(sprite: Sprite3D) -> Vector2:
	if sprite == null or sprite.texture == null:
		return Vector2.ZERO
	return sprite.texture.get_size() / Vector2(
		float(maxi(1, sprite.hframes)), float(maxi(1, sprite.vframes)))

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

func _init_dust_bunny_behavior(record: Dictionary, room_id: String,
		item_data: Dictionary, source_position: Vector2,
		visual_scale: float) -> void:
	var role: String = String(item_data.get("dust_bunny_role", ""))
	record["bunny_role"] = role
	record["hp"] = int(item_data.get("hp", HALL_BUNNY_HP))
	record["bunny_scale"] = visual_scale
	record["bunny_center"] = source_position
	record["bunny_base_y"] = source_position.y
	record["bunny_depth"] = float(item_data.get("z", ITEM_Z))
	record["bunny_clock"] = 0.0
	record["bunny_flee"] = 0.0
	record["bunny_flee_direction"] = 1.0
	record["bunny_settle"] = 0.0
	record["bunny_wake"] = 0.0
	record["bunny_hop_time"] = 0.0
	record["bunny_direction"] = 1.0
	record["bunny_hop_from"] = source_position.x
	record["bunny_hop_to"] = source_position.x
	# Deterministic per-spawn rhythm: no two neighbours hop on the same beat,
	# and a probe run reproduces the same colony beat for beat.
	record["bunny_rest_scale"] = 0.80 + 0.60 * fposmod(
		source_position.x * 0.017, 1.0)
	# Rest starts full so the first ticked frame already carries a hop.
	record["bunny_rest"] = HALL_BUNNY_REST_TIME * 2.0
	if room_id != "main_hall":
		# Playroom pinning bunnies are authored set dressing for the Baby Eagle
		# rescue; they hold their painted pose.
		record["bunny_travels"] = false
		record["bunny_state"] = "pinned"
		return
	var hop_range: float = float(item_data.get("hop_range", 420.0))
	var bounds := Vector2(
		source_position.x - hop_range, source_position.x + hop_range)
	if item_data.has("patrol_x"):
		bounds = item_data["patrol_x"] as Vector2
	record["bunny_bounds"] = Vector2(
		maxf(bounds.x, HALL_BUNNY_SPAWN_X_RANGE.x),
		minf(bounds.y, HALL_BUNNY_SPAWN_X_RANGE.y))
	record["bunny_travels"] = role in HALL_BUNNY_TRAVEL_ROLES
	record["bunny_state"] = "asleep" if role == "sleeping_static" else (
		"hidden" if role == "shell_static" else (
			"resting" if role in HALL_BUNNY_TRAVEL_ROLES else "huddled"))

func _hall_player_foot() -> Vector2:
	if m.castle_room_player_sprite == null \
			or not is_instance_valid(m.castle_room_player_sprite):
		return Vector2(-100000.0, -100000.0)
	return m.castle_room_player_sprite.get_meta(
		"current_stage_foot",
		m.castle_room_player_sprite.get_meta(
			"stage_foot", Vector2(-100000.0, -100000.0))) as Vector2

func _hall_light_level_at(art_x: float) -> float:
	# The painted shell sconces are the only light authority in this hall, so
	# they are what the bunnies read when deciding to sleep, hide or hop away.
	var level := 0.0
	for item_data: Dictionary in HALL_ITEMS:
		if not item_data.has("light_cluster"):
			continue
		if not bool(m.castle_room_light_states.get(
				String(item_data["id"]), true)):
			continue
		var fixture_x: float = (item_data["pos"] as Vector2).x
		level = maxf(level, clampf(
			1.0 - absf(fixture_x - art_x) / HALL_BUNNY_LIGHT_REACH, 0.0, 1.0))
	return level

func _update_dust_bunny_colony(delta: float) -> void:
	if not _is_wide_hall() or delta <= 0.0:
		return
	m.g["castle_dust_bunny_runner_time"] = float(m.g.get(
		"castle_dust_bunny_runner_time", 0.0)) + delta
	var player_foot: Vector2 = _hall_player_foot()
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) == "":
			continue
		_update_dust_bunny(record, delta, player_foot)

func _update_dust_bunny(record: Dictionary, delta: float,
		player_foot: Vector2) -> void:
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite == null or not is_instance_valid(sprite) \
			or bool(sprite.get_meta("exploding", false)):
		return
	record["bunny_clock"] = float(record.get("bunny_clock", 0.0)) + delta
	record["bunny_flee"] = maxf(
		0.0, float(record.get("bunny_flee", 0.0)) - delta)
	var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
	var light: float = _hall_light_level_at(center.x)
	if bool(record.get("bunny_travels", false)):
		_update_dust_bunny_travel(record, delta, player_foot, light)
	else:
		_update_dust_bunny_idle(record, delta, player_foot, light)

func _update_dust_bunny_idle(record: Dictionary, delta: float,
		player_foot: Vector2, light: float) -> void:
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	var role: String = String(record.get("bunny_role", ""))
	var state: String = String(record.get("bunny_state", ""))
	var base_scale: float = float(record.get("bunny_scale", 1.0))
	var clock: float = float(record.get("bunny_clock", 0.0))
	if state == "waking":
		var wake: float = float(record.get("bunny_wake", 0.0)) + delta
		record["bunny_wake"] = wake
		var wake_ratio: float = clampf(wake / HALL_BUNNY_WAKE_TIME, 0.0, 1.0)
		var stretch: float = sin(wake_ratio * PI)
		sprite.scale = Vector3(
			base_scale * (1.0 - 0.10 * stretch),
			base_scale * (1.0 + 0.22 * stretch), 1.0)
		if wake_ratio >= 1.0:
			sprite.scale = Vector3.ONE * base_scale
			sprite.texture = load(HALL_BUNNY_ART + "dust_bunny_hop.png")
			record["bunny_travels"] = true
			record["bunny_state"] = "resting"
			record["bunny_rest"] = HALL_BUNNY_REST_TIME * 2.0
			sprite.set_meta("dust_bunny_state", "hopping")
		return
	var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
	if role == "shell_static":
		# The shell is a hiding place: bright light or an approaching mermaid
		# pulls the bunny back under it, darkness lets it peek out again.
		var hiding: bool = light >= HALL_BUNNY_LIGHT_WAKE \
			or absf(player_foot.x - center.x) <= HALL_BUNNY_SHY_RADIUS
		record["bunny_state"] = "hidden" if hiding else "peeking"
		sprite.set_meta("dust_bunny_state", String(record["bunny_state"]))
		var shell_target: float = base_scale * (0.90 if hiding
			else 1.06 + 0.02 * sin(clock * 2.2))
		sprite.scale = sprite.scale.lerp(
			Vector3.ONE * shell_target, clampf(delta * 6.0, 0.0, 1.0))
		return
	# Sleeping huddles and the family nursery only breathe. They never travel,
	# so their card never leaves its authored spot.
	var breath: float = 0.035 * sin(clock * 1.7)
	sprite.scale = Vector3(
		base_scale * (1.0 + breath), base_scale * (1.0 - breath), 1.0)
	sprite.set_meta("dust_bunny_state", state)

func _update_dust_bunny_travel(record: Dictionary, delta: float,
		player_foot: Vector2, light: float) -> void:
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	var base_scale: float = float(record.get("bunny_scale", 1.0))
	var base_y: float = float(record.get("bunny_base_y", 830.0))
	var remaining: float = delta
	var guard := 0
	while remaining > 0.0 and guard < 8:
		guard += 1
		if String(record.get("bunny_state", "resting")) == "hopping":
			var hop_time: float = float(record.get("bunny_hop_time", 0.0))
			var step: float = minf(remaining, HALL_BUNNY_HOP_TIME - hop_time)
			hop_time += step
			remaining -= step
			record["bunny_hop_time"] = hop_time
			if hop_time >= HALL_BUNNY_HOP_TIME:
				record["bunny_state"] = "resting"
				record["bunny_rest"] = 0.0
		else:
			var rest_limit: float = HALL_BUNNY_REST_TIME \
				* float(record.get("bunny_rest_scale", 1.0))
			var rest: float = float(record.get("bunny_rest", 0.0))
			var rest_step: float = minf(remaining, maxf(0.0, rest_limit - rest))
			rest += rest_step
			remaining -= rest_step
			record["bunny_rest"] = rest
			if _settle_dust_bunny_if_dark(record, rest_step, light):
				return
			if rest >= rest_limit:
				_start_dust_bunny_hop(record, player_foot, light)
			elif rest_step <= 0.0:
				break
	var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
	if String(record.get("bunny_state", "resting")) == "hopping":
		var hop_ratio: float = clampf(
			float(record.get("bunny_hop_time", 0.0)) / HALL_BUNNY_HOP_TIME,
			0.0, 1.0)
		center = Vector2(
			lerpf(float(record.get("bunny_hop_from", center.x)),
				float(record.get("bunny_hop_to", center.x)), hop_ratio),
			base_y - sin(hop_ratio * PI) * HALL_BUNNY_HOP_HEIGHT)
		sprite.scale = Vector3(
			base_scale * (1.0 - 0.06 * sin(hop_ratio * PI)),
			base_scale * (1.0 + 0.09 * sin(hop_ratio * PI)), 1.0)
	else:
		center = Vector2(float(record.get("bunny_hop_to", center.x)), base_y)
		sprite.scale = Vector3.ONE * base_scale
	record["bunny_center"] = center
	_apply_dust_bunny_center(record, center)

func _settle_dust_bunny_if_dark(record: Dictionary, delta: float,
		light: float) -> bool:
	# An awake sleeper that finds a dark, quiet corner curls back up. Turning a
	# shell sconce on is what stirs the hall; turning them off calms it.
	if String(record.get("bunny_role", "")) != "sleeping_static":
		return false
	var settle: float = float(record.get("bunny_settle", 0.0))
	if light < HALL_BUNNY_LIGHT_WAKE \
			and float(record.get("bunny_flee", 0.0)) <= 0.0:
		settle += delta
	else:
		settle = 0.0
	record["bunny_settle"] = settle
	if settle < HALL_BUNNY_SETTLE_TIME:
		return false
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	record["bunny_settle"] = 0.0
	record["bunny_travels"] = false
	record["bunny_state"] = "asleep"
	if sprite != null and is_instance_valid(sprite):
		sprite.texture = load(HALL_BUNNY_ART + "dust_bunny_sleepy.png")
		sprite.scale = Vector3.ONE * float(record.get("bunny_scale", 1.0))
		sprite.set_meta("dust_bunny_state", "asleep")
	var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
	center.y = float(record.get("bunny_base_y", center.y))
	record["bunny_center"] = center
	_apply_dust_bunny_center(record, center)
	return true

func _start_dust_bunny_hop(record: Dictionary, player_foot: Vector2,
		light: float) -> void:
	var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
	var bounds: Vector2 = record.get(
		"bunny_bounds", HALL_BUNNY_SPAWN_X_RANGE) as Vector2
	var direction: float = float(record.get("bunny_direction", 1.0))
	var role: String = String(record.get("bunny_role", ""))
	var player_gap: float = player_foot.x - center.x
	var hold: float = maxf(0.0, float(record.get("bunny_hold", 0.0))
		- HALL_BUNNY_HOP_TIME - HALL_BUNNY_REST_TIME)
	record["bunny_hold"] = hold
	if float(record.get("bunny_flee", 0.0)) > 0.0:
		direction = float(record.get("bunny_flee_direction", direction))
	elif hold > 0.0:
		# Just turned around at the end of its patch: keep going that way for a
		# few hops instead of bouncing against the same edge every hop.
		pass
	elif absf(player_gap) <= HALL_BUNNY_SHY_RADIUS and absf(player_gap) > 1.0 \
			and role != "runner":
		# Shy, never dangerous: a bunny that notices Roshan hops away from her,
		# always slower than she swims, so she can still catch every one.
		direction = -signf(player_gap)
	else:
		var dark_step: float = HALL_BUNNY_HOP_DISTANCE * 2.0
		var left_light: float = _hall_light_level_at(center.x - dark_step)
		var right_light: float = _hall_light_level_at(center.x + dark_step)
		if absf(left_light - right_light) > 0.05:
			direction = -1.0 if left_light < right_light else 1.0
		elif light >= HALL_BUNNY_LIGHT_WAKE and direction == 0.0:
			direction = 1.0
	if direction == 0.0:
		direction = 1.0
	var target: float = center.x + direction * HALL_BUNNY_HOP_DISTANCE
	if target < bounds.x or target > bounds.y:
		direction = -direction
		target = center.x + direction * HALL_BUNNY_HOP_DISTANCE
		record["bunny_hold"] = HALL_BUNNY_HOLD_TIME
	record["bunny_direction"] = direction
	record["bunny_hop_from"] = center.x
	record["bunny_hop_to"] = clampf(target, bounds.x, bounds.y)
	record["bunny_hop_time"] = 0.0
	record["bunny_state"] = "hopping"
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite != null and is_instance_valid(sprite):
		sprite.set_meta("dust_bunny_state", "hopping")

func _apply_dust_bunny_center(record: Dictionary, center: Vector2) -> void:
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite == null or not is_instance_valid(sprite):
		return
	var item_data: Dictionary = record.get("data", {}) as Dictionary
	var depth_z: float = float(record.get(
		"bunny_depth", float(item_data.get("z", ITEM_Z))))
	sprite.position = _hall_art_to_world(center, depth_z)
	sprite.pixel_size = _pixel_size_for_depth(depth_z)
	sprite.flip_h = float(record.get("bunny_direction", 1.0)) < 0.0
	var contact_offset: Vector2 = item_data.get(
		"contact_offset", Vector2.ZERO) as Vector2
	record["contact_foot"] = center + contact_offset
	if sprite.texture != null:
		var card_size: Vector2 = sprite.texture.get_size() \
			* float(record.get("bunny_scale", 1.0))
		record["art_rect"] = Rect2(center - card_size * 0.5, card_size)
	record["runner_direction"] = float(record.get("bunny_direction", 1.0))

func _wake_dust_bunnies_near(art_x: float, reach: float) -> void:
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) != "sleeping_static":
			continue
		if String(record.get("bunny_state", "")) != "asleep":
			continue
		var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
		if absf(center.x - art_x) > reach:
			continue
		record["bunny_state"] = "waking"
		record["bunny_wake"] = 0.0
		record["bunny_settle"] = 0.0
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		if sprite != null and is_instance_valid(sprite):
			sprite.set_meta("dust_bunny_state", "waking")

func _startle_dust_bunnies(art_x: float, radius: float) -> void:
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) == "":
			continue
		var center: Vector2 = record.get("bunny_center", Vector2.ZERO) as Vector2
		if absf(center.x - art_x) > radius:
			continue
		record["bunny_flee"] = HALL_BUNNY_FLEE_TIME
		record["bunny_flee_direction"] = 1.0 if center.x >= art_x else -1.0
		record["bunny_settle"] = 0.0
		if String(record.get("bunny_state", "")) == "asleep":
			record["bunny_state"] = "waking"
			record["bunny_wake"] = 0.0

func _hall_dust_bunny_colony() -> Array:
	var colony: Array = m.g.get("castle_dust_bunny_colony", []) as Array
	if not colony.is_empty():
		return colony
	var visit_serial: int = int(m.g.get("castle_visit_serial", 1))
	var rng := RandomNumberGenerator.new()
	rng.seed = HALL_BUNNY_SEED_BASE + visit_serial * 7919
	for founder: Dictionary in HALL_DUST_BUNNY_SPAWNS:
		colony.append(founder.duplicate(true))
	var extra_count: int = 1 + visit_serial % 2
	for index in range(extra_count):
		var spawn: Dictionary = _make_generated_dust_bunny(
			rng, "dust_bunny_gen_%d" % (index + 1), colony, -1.0)
		if spawn.is_empty():
			break
		colony.append(spawn)
	m.g["castle_dust_bunny_colony"] = colony
	return colony

func _pick_hall_bunny_variant(rng: RandomNumberGenerator) -> Dictionary:
	var total := 0
	for variant: Dictionary in HALL_BUNNY_VARIANTS:
		total += int(variant.get("weight", 1))
	var roll: int = rng.randi_range(0, maxi(0, total - 1))
	for variant: Dictionary in HALL_BUNNY_VARIANTS:
		roll -= int(variant.get("weight", 1))
		if roll < 0:
			return variant
	return HALL_BUNNY_VARIANTS[0]

func _hall_bunny_free_spans(colony: Array) -> Array:
	# Doors, Roshan's arrival mark and the bunnies already placed carve the hall
	# floor into the spans a new bunny may drift into.
	var blocked: Array[Vector2] = [Vector2(
		HALL_BUNNY_START_FOOT.x - HALL_BUNNY_START_CLEARANCE,
		HALL_BUNNY_START_FOOT.x + HALL_BUNNY_START_CLEARANCE)]
	for portal: Dictionary in HALL_PORTALS:
		var foot: Vector2 = portal.get("foot", Vector2.ZERO) as Vector2
		blocked.append(Vector2(
			foot.x - HALL_BUNNY_DOOR_CLEARANCE,
			foot.x + HALL_BUNNY_DOOR_CLEARANCE))
	var cleared: Dictionary = m.g.get(
		"castle_dust_bunnies_cleared", {}) as Dictionary
	for entry_value: Variant in colony:
		var entry: Dictionary = entry_value as Dictionary
		# A cleared bunny gives its patch of floor back to the colony.
		if bool(cleared.get(String(entry.get("id", "")), false)):
			continue
		var entry_position: Vector2 = entry.get("pos", Vector2.ZERO) as Vector2
		blocked.append(Vector2(
			entry_position.x - HALL_BUNNY_SPAWN_CLEARANCE,
			entry_position.x + HALL_BUNNY_SPAWN_CLEARANCE))
	blocked.sort_custom(func(a: Vector2, b: Vector2) -> bool: return a.x < b.x)
	var spans: Array[Vector2] = []
	var cursor: float = HALL_BUNNY_SPAWN_X_RANGE.x
	for band: Vector2 in blocked:
		if band.x > cursor:
			spans.append(Vector2(
				cursor, minf(band.x, HALL_BUNNY_SPAWN_X_RANGE.y)))
		cursor = maxf(cursor, band.y)
		if cursor >= HALL_BUNNY_SPAWN_X_RANGE.y:
			break
	if cursor < HALL_BUNNY_SPAWN_X_RANGE.y:
		spans.append(Vector2(cursor, HALL_BUNNY_SPAWN_X_RANGE.y))
	var usable: Array[Vector2] = []
	for span: Vector2 in spans:
		if span.y - span.x >= 70.0:
			usable.append(span)
	return usable

func _hall_bunny_spawn_x(rng: RandomNumberGenerator, colony: Array,
		preferred_x: float) -> float:
	var spans: Array = _hall_bunny_free_spans(colony)
	if spans.is_empty():
		return -1.0
	if preferred_x >= 0.0:
		var best: Vector2 = spans[0] as Vector2
		var best_gap := INF
		for span: Vector2 in spans:
			var gap: float = absf(
				clampf(preferred_x, span.x, span.y) - preferred_x)
			if gap < best_gap:
				best_gap = gap
				best = span
		return clampf(preferred_x, best.x + 30.0, best.y - 30.0)
	var total := 0.0
	for span: Vector2 in spans:
		total += span.y - span.x
	var roll: float = rng.randf() * total
	for span: Vector2 in spans:
		var width: float = span.y - span.x
		if roll <= width:
			return span.x + clampf(
				rng.randf() * width, 30.0, maxf(30.0, width - 30.0))
		roll -= width
	var last: Vector2 = spans[spans.size() - 1] as Vector2
	return (last.x + last.y) * 0.5

func _has_live_dust_bunny_role(role: String) -> bool:
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) == role:
			return true
	return false

func _live_dust_bunny_count() -> int:
	var count := 0
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) != "":
			count += 1
	return count

func hall_dust_bunny_ids() -> Array[String]:
	var ids: Array[String] = []
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) != "":
			ids.append(String(item_id_value))
	return ids

func _make_generated_dust_bunny(rng: RandomNumberGenerator, item_id: String,
		colony: Array, preferred_x: float) -> Dictionary:
	var variant: Dictionary = _pick_hall_bunny_variant(rng)
	if String(variant["role"]) == "family_nursery" \
			and _has_live_dust_bunny_role("family_nursery"):
		variant = HALL_BUNNY_VARIANTS[0]
	var spawn_x: float = _hall_bunny_spawn_x(rng, colony, preferred_x)
	if spawn_x < 0.0:
		return {}
	var spawn_y: float = rng.randf_range(
		HALL_BUNNY_FOOT_BAND.x, HALL_BUNNY_FOOT_BAND.y)
	var visual_scale: float = float(variant["scale"]) \
		* rng.randf_range(0.92, 1.06)
	var depth_z: float = clampf(
		float(variant["z"]) + rng.randf_range(-0.14, 0.14), 2.35, 3.15)
	var role: String = String(variant["role"])
	return {
		"id": item_id,
		"name": "Dust bunny",
		"pos": Vector2(spawn_x, spawn_y),
		"z": depth_z,
		"tex_path": HALL_BUNNY_ART + String(variant["tex"]),
		"scale": visual_scale,
		"dust_bunny_role": role,
		"generated_dust_bunny": true,
		"hp": HALL_BUNNY_HP,
		"hop_range": float(variant["range"]),
		"contact_offset": Vector2(0.0, 60.0),
		"contact_radius": Vector2(132.0, 92.0),
		"proximity_only": true,
		"sound": "hop_boing.ogg",
		"pitch": float(variant["pitch"]) * rng.randf_range(0.94, 1.06),
		"color": variant["color"],
	}

func _update_dust_bunny_spawner(delta: float) -> void:
	# Passive generation: the hall keeps making new dust bunnies on its own, so
	# clearing one is never the end of the game and never a score to protect.
	if not _is_wide_hall() or delta <= 0.0:
		return
	if _live_dust_bunny_count() >= HALL_BUNNY_LIVE_CAP:
		m.g["castle_dust_bunny_spawn_clock"] = 0.0
		return
	var interval: float = HALL_BUNNY_NURSERY_INTERVAL \
		if _has_live_dust_bunny_role("family_nursery") \
		else HALL_BUNNY_DRIFT_INTERVAL
	var clock: float = float(m.g.get(
		"castle_dust_bunny_spawn_clock", 0.0)) + delta
	if clock < interval:
		m.g["castle_dust_bunny_spawn_clock"] = clock
		return
	m.g["castle_dust_bunny_spawn_clock"] = 0.0
	_spawn_passive_dust_bunny()

func _spawn_passive_dust_bunny() -> Dictionary:
	var colony: Array = _hall_dust_bunny_colony()
	var spawn_serial: int = int(m.g.get(
		"castle_dust_bunny_spawn_serial", 0)) + 1
	m.g["castle_dust_bunny_spawn_serial"] = spawn_serial
	var rng := RandomNumberGenerator.new()
	rng.seed = HALL_BUNNY_SEED_BASE \
		+ int(m.g.get("castle_visit_serial", 1)) * 7919 \
		+ spawn_serial * 104729
	# A family huddle raises its own pups right beside it.
	var preferred_x := -1.0
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[
			item_id_value] as Dictionary
		if String(record.get("bunny_role", "")) != "family_nursery":
			continue
		var nursery_center: Vector2 = record.get(
			"bunny_center", Vector2.ZERO) as Vector2
		preferred_x = nursery_center.x + rng.randf_range(-190.0, 190.0)
		break
	var spawn: Dictionary = _make_generated_dust_bunny(
		rng, "dust_bunny_drift_%d" % spawn_serial, colony, preferred_x)
	if spawn.is_empty():
		return {}
	colony.append(spawn)
	m.g["castle_dust_bunny_colony"] = colony
	_add_touch_item("main_hall", spawn)
	var record: Dictionary = m.castle_room_item_sprites.get(
		String(spawn["id"]), {}) as Dictionary
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite != null and is_instance_valid(sprite):
		var target_scale: Vector3 = sprite.scale
		sprite.scale = target_scale * 0.2
		var puff := sprite.create_tween()
		puff.tween_property(sprite, "scale", target_scale,
			0.32).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		_item_burst(sprite.position,
			Color(spawn.get("color", StorybookUI.GOLD)), 6)
		_play_item_sfx("hop_boing.ogg", float(spawn.get("pitch", 1.6)) * 0.85)
	return spawn

func _check_dust_bunny_contacts() -> void:
	if m.castle_room_player_sprite == null:
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
		var contact_radius: Vector2 = record.get(
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
		_damage_dust_bunny(item_id, 1)

func _damage_dust_bunny(item_id: String, amount: int) -> void:
	# Dust bunnies have exactly one hit point and Roshan has none to lose: a
	# single bump clears the bunny, and a bunny can never hurt her back.
	var record: Dictionary = m.castle_room_item_sprites.get(
		item_id, {}) as Dictionary
	if record.is_empty():
		return
	if String(record.get("bunny_role", "")) == "" \
			and String((record.get("data", {}) as Dictionary).get(
				"dust_bunny_role", "")) == "":
		return
	var hp: int = int(record.get("hp", HALL_BUNNY_HP)) - maxi(1, amount)
	record["hp"] = hp
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite != null and is_instance_valid(sprite):
		sprite.set_meta("dust_bunny_hp", hp)
	if hp > 0:
		return
	_explode_dust_bunny(item_id)

func _explode_dust_bunny(item_id: String, partner_pop: bool = false) -> void:
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
	# combat wing 2026-08: bunny pops join the shared pop-chain (tap and
	# walk-contact count equally), pay one pearl, and a quick trio — chain
	# level 3 — earns a little TRIO celebration. Rescue pins keep their own
	# reward flow and stay pearl-free.
	if not bool(item_data.get("rescue_bunny", false)):
		m.pearl_count += 1
	if not partner_pop and m.castle_dust_he != null:
		var chain_level: int = m.castle_dust_he.note_hit(sprite.global_position)
		if chain_level >= 3:
			_item_burst(sprite.position, Color(StorybookUI.GOLD), 16)
			m._audio_ref()._fanfare()
			Juice.shake(m.castle_room_camera)
		if m.castle_partner != null:
			m.castle_partner.note_child_pop()
	# Daddy's bubble debuts after her first own pop of the visit (staged
	# teach): the castle is his home, and his DADDY SPLASH super rests on an
	# 18 s cooldown between waves of hearts.
	if not partner_pop and m.castle_partner == null and m.castle_room_id == "main_hall":
		m.castle_partner = PartnerAssist.new(m)
		m.castle_partner.attach("daddy", Callable(self, "_daddy_splash"))
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
	if bool(item_data.get("rescue_bunny", false)):
		m.stuffie_wins["rescued_" + item_id] = true
		_check_playroom_rescue_complete()
		if not _playroom_rescue_done():
			m._write_save()

# DADDY SPLASH (PartnerAssist fires this only from the child's tap on his
# bubble): a wave of hearts pops every ordinary dust bunny in the current
# room. Rescue pins are deliberately excluded — freeing the Baby Eagle is
# HER moment ("I know you can do it!"), Daddy never takes it from her.
func _daddy_splash(_partner_kind: String) -> void:
	var ids: Array[String] = []
	for item_id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[item_id_value] \
			as Dictionary
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if String(item_data.get("dust_bunny_role", "")) == "":
			continue
		if bool(item_data.get("rescue_bunny", false)):
			continue
		ids.append(String(item_id_value))
	for item_id: String in ids:
		var record2: Dictionary = m.castle_room_item_sprites.get(
			item_id, {}) as Dictionary
		var sprite: Sprite3D = record2.get("sprite") as Sprite3D
		if sprite != null and is_instance_valid(sprite):
			_item_burst(sprite.position, Color(0.98, 0.62, 0.78), 10)
		_explode_dust_bunny(item_id, true)
	Juice.shake(m.castle_room_camera)

func _playroom_rescue_done() -> bool:
	return m.companion_id != "" \
		or bool(m.stuffie_wins.get("rescued_eagle", false))

func _restore_playroom_rescue_clears() -> void:
	if _playroom_rescue_done():
		return
	var cleared: Dictionary = m.g.get(
		"castle_dust_bunnies_cleared", {}) as Dictionary
	for item_id: String in ["eagle_pin_left", "eagle_pin_right"]:
		if bool(m.stuffie_wins.get("rescued_" + item_id, false)):
			cleared[item_id] = true
	m.g["castle_dust_bunnies_cleared"] = cleared
	if bool(cleared.get("eagle_pin_left", false)) \
			and bool(cleared.get("eagle_pin_right", false)):
		m.stuffie_wins["rescued_eagle"] = true
		m._write_save()

func _add_playroom_rescue_pointer() -> void:
	if m.castle_room_item_effect_layer == null \
			or m.castle_room_item_effect_layer.get_node_or_null(
				"BabyEagleRescuePointer") != null:
		return
	var star_texture: Texture2D = load("res://assets/mg/star.png")
	if star_texture == null:
		return
	var pointer: Sprite3D = _new_card(
		"BabyEagleRescuePointer", star_texture)
	pointer.position = _art_to_world(Vector2(512.0, 210.0), 2.72)
	pointer.pixel_size = _pixel_size_for_depth(2.72)
	pointer.scale = Vector3.ONE * 0.052
	pointer.modulate = Color(1.0, 0.86, 0.32, 0.94)
	pointer.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	pointer.set_meta("source_asset_role", "tutorial_pointer")
	pointer.set_meta("source_object_id", "playroom:baby_eagle_pointer")
	m.castle_room_item_effect_layer.add_child(pointer)
	var base_position: Vector3 = pointer.position
	var pulse: Tween = pointer.create_tween().set_loops()
	pulse.tween_property(pointer, "position:y", base_position.y + 0.28,
		0.42).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	pulse.parallel().tween_property(pointer, "scale", Vector3.ONE * 0.060,
		0.42).set_trans(Tween.TRANS_SINE)
	pulse.tween_property(pointer, "position:y", base_position.y,
		0.42).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	pulse.parallel().tween_property(pointer, "scale", Vector3.ONE * 0.052,
		0.42).set_trans(Tween.TRANS_SINE)

func _check_playroom_rescue_complete() -> void:
	if m.castle_room_id != "playroom" or _playroom_rescue_done():
		return
	var cleared: Dictionary = m.g.get(
		"castle_dust_bunnies_cleared", {}) as Dictionary
	if not bool(cleared.get("eagle_pin_left", false)) \
			or not bool(cleared.get("eagle_pin_right", false)):
		return
	m.stuffie_wins["rescued_eagle"] = true
	m._write_save()
	if m.castle_room_action_button != null:
		m.castle_room_action_button.visible = true
	var pointer: Node = m.castle_room_item_effect_layer.get_node_or_null(
		"BabyEagleRescuePointer") \
		if m.castle_room_item_effect_layer != null else null
	if pointer != null:
		pointer.queue_free()
	var eagle_record: Dictionary = m.castle_room_item_sprites.get(
		"baby_eagle_rescue", {}) as Dictionary
	var eagle: Sprite3D = eagle_record.get("sprite") as Sprite3D
	m.castle_room_item_sprites.erase("baby_eagle_rescue")
	m.show_msg("Baby Eagle",
		"Chirp! You saved me! Let us learn how stuffie friends come along!",
		"win")
	if eagle == null or not is_instance_valid(eagle):
		_open_playroom_stuffie_tutorial()
		return
	_item_burst(eagle.position, Color(0.54, 0.91, 1.0), 16)
	var target_color: Color = eagle.modulate
	target_color.a = 0.0
	var fly: Tween = eagle.create_tween().set_parallel(true)
	fly.tween_property(eagle, "position:y", eagle.position.y + 1.25,
		0.72).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	fly.tween_property(eagle, "scale", eagle.scale * 1.12,
		0.72).set_trans(Tween.TRANS_SINE)
	fly.tween_property(eagle, "modulate", target_color,
		0.72).set_delay(0.34)
	fly.chain().tween_callback(
		_finish_playroom_eagle_departure.bind(eagle))

func _finish_playroom_eagle_departure(eagle: Sprite3D) -> void:
	if eagle != null and is_instance_valid(eagle):
		eagle.queue_free()
	_open_playroom_stuffie_tutorial()

func _open_playroom_stuffie_tutorial() -> void:
	if not is_open() or m.castle_room_id != "playroom" \
			or m.companion_id != "":
		return
	m.g["stuffie_rescue_tutorial"] = true
	m.g["stuffie_rescue_tutorial_step"] = 0
	m._companion_ref().open_picker(true, "eagle", "adopt")


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
	var frame_size: Vector2 = record.get(
		"frame_size", _sprite_frame_size(sprite)) as Vector2
	var authored_size: Vector2 = record.get(
		"hotspot_size", frame_size) as Vector2
	var authored_offset: Vector2 = record.get(
		"hotspot_offset", (frame_size - authored_size) * 0.5) as Vector2
	var local_center_pixels: Vector2 = record.get(
		"hotspot_local_center_pixels",
		authored_offset + authored_size * 0.5 - frame_size * 0.5) as Vector2
	var local_size_pixels: Vector2 = record.get(
		"hotspot_local_size_pixels", authored_size) as Vector2
	if sprite.flip_h:
		local_center_pixels.x = -local_center_pixels.x
	var hotspot_world_center: Vector3 = sprite.global_position \
		+ sprite.global_transform.basis.x \
			* (local_center_pixels.x * sprite.pixel_size) \
		- sprite.global_transform.basis.y \
			* (local_center_pixels.y * sprite.pixel_size)
	var center_screen: Vector2 = m.castle_room_camera.unproject_position(
		hotspot_world_center)
	var half_x_world: Vector3 = sprite.global_transform.basis.x \
		* (local_size_pixels.x * sprite.pixel_size * 0.5)
	var half_y_world: Vector3 = sprite.global_transform.basis.y \
		* (local_size_pixels.y * sprite.pixel_size * 0.5)
	var edge_x_screen: Vector2 = m.castle_room_camera.unproject_position(
		hotspot_world_center + half_x_world)
	var edge_y_screen: Vector2 = m.castle_room_camera.unproject_position(
		hotspot_world_center + half_y_world)
	var center_stage: Vector2 = _screen_to_stage(center_screen)
	var edge_x_stage: Vector2 = _screen_to_stage(edge_x_screen)
	var edge_y_stage: Vector2 = _screen_to_stage(edge_y_screen)
	var hit_size := Vector2(
		maxf(88.0, absf(edge_x_stage.x - center_stage.x) * 2.0),
		maxf(88.0, absf(edge_y_stage.y - center_stage.y) * 2.0))
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
			var hit_size := Vector2(
				maxf(112.0, clipped.size.x),
				maxf(112.0, clipped.size.y))
			var hit_position: Vector2 = clipped.get_center() - hit_size * 0.5
			hit_position.x = clampf(hit_position.x, 0.0,
				StorybookUI.CANVAS_SIZE.x - hit_size.x)
			hit_position.y = clampf(hit_position.y, 0.0,
				StorybookUI.CANVAS_SIZE.y - hit_size.y)
			button.position = hit_position
			button.size = hit_size

func _enter_hall_portal(portal_id: String, foot: Vector2) -> void:
	if _fridge_close_is_blocked():
		return
	if not _is_wide_hall():
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

func kitchen_action_label() -> String:
	if kitchen_act != null and is_instance_valid(kitchen_act):
		return kitchen_act.action_label()
	return "COOK"

func _open_kitchen_menu() -> void:
	if kitchen_menu_layer != null or kitchen_act != null:
		return
	m._set_world_controls_enabled(false, "kitchen_fridge_menu")
	kitchen_menu_layer = CanvasLayer.new()
	kitchen_menu_layer.name = "KitchenFridgeMenu"
	kitchen_menu_layer.layer = 29
	m.add_child(kitchen_menu_layer)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_STOP
	kitchen_menu_layer.add_child(root)
	var dim := ColorRect.new()
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.color = StorybookUI.DIM
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	root.add_child(dim)
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	kitchen_menu_stage = StorybookUI.add_stage(root, viewport_size)
	StorybookUI.add_panel(kitchen_menu_stage,
		Rect2(52.0, 36.0, 1176.0, 648.0), StorybookUI.MINT,
		Color(0.94, 0.98, 1.0, 0.99), 44)

	var title := Label.new()
	title.text = "✨  🧊  What shall we cook?  🍰  ✨"
	StorybookUI.style_label(title, 45, StorybookUI.INK, 4)
	title.position = Vector2(105.0, 65.0)
	title.size = Vector2(980.0, 70.0)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	kitchen_menu_stage.add_child(title)

	var close_button := Button.new()
	close_button.name = "KitchenFridgeBackButton"
	StorybookUI.style_back_button(close_button, "Back to the kitchen")
	close_button.position = Vector2(1090.0, 55.0)
	close_button.pressed.connect(_close_kitchen_menu)
	kitchen_menu_stage.add_child(close_button)

	var available: Array[Dictionary] = []
	for recipe: Dictionary in KITCHEN_RECIPES:
		var uses: String = String(recipe["uses"])
		if uses == "" or int(m.opera_pantry.get(uses, 0)) > 0:
			available.append(recipe)
	var card_width := 300.0
	var card_gap := 34.0
	var cards_width: float = float(available.size()) * card_width \
		+ float(maxi(0, available.size() - 1)) * card_gap
	var first_x: float = (1280.0 - cards_width) * 0.5
	for index in range(available.size()):
		var recipe: Dictionary = available[index]
		var recipe_button := Button.new()
		recipe_button.name = "KitchenRecipe_" + String(recipe["id"])
		recipe_button.text = "%s\n%s" % [
			String(recipe["icon"]), String(recipe["name"])]
		recipe_button.position = Vector2(
			first_x + float(index) * (card_width + card_gap), 180.0)
		recipe_button.size = Vector2(card_width, 278.0)
		recipe_button.add_theme_font_size_override("font_size", 40)
		recipe_button.set_meta("picture_first", true)
		recipe_button.set_meta("recipe_id", String(recipe["id"]))
		StorybookUI.style_button(recipe_button, "gold", 40, 34)
		recipe_button.pressed.connect(
			_launch_kitchen_recipe.bind(String(recipe["id"])))
		kitchen_menu_stage.add_child(recipe_button)

	var pantry_parts: Array[String] = []
	for food_key_value: Variant in KITCHEN_FOOD_ICONS:
		var food_key := String(food_key_value)
		var count: int = int(m.opera_pantry.get(food_key, 0))
		if count > 0:
			pantry_parts.append("%s ×%d" % [
				String(KITCHEN_FOOD_ICONS[food_key]), count])
	var pantry := Label.new()
	pantry.name = "KitchenPantryInventory"
	pantry.text = "🧺  " + (
		"     ".join(pantry_parts) if not pantry_parts.is_empty()
		else "✨  🧁")
	pantry.set_meta("food_counts", m.opera_pantry.duplicate(true))
	StorybookUI.style_label(pantry, 36, StorybookUI.INK_SOFT, 3)
	pantry.position = Vector2(150.0, 515.0)
	pantry.size = Vector2(980.0, 70.0)
	pantry.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	kitchen_menu_stage.add_child(pantry)

	var pointer := Label.new()
	pointer.text = "☝"
	StorybookUI.style_label(pointer, 54, StorybookUI.GOLD, 3)
	pointer.position = Vector2(first_x + card_width * 0.5 - 32.0, 125.0)
	kitchen_menu_stage.add_child(pointer)
	var point: Tween = pointer.create_tween().set_loops()
	point.tween_property(pointer, "position:y", 138.0, 0.55).set_trans(
		Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	point.tween_property(pointer, "position:y", 125.0, 0.55).set_trans(
		Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	m._say("roshan", "talk", 0.0)

func _close_kitchen_menu() -> bool:
	var closing_fridge: bool = _close_fridge_visual()
	if kitchen_menu_layer != null and is_instance_valid(kitchen_menu_layer):
		kitchen_menu_layer.queue_free()
	kitchen_menu_layer = null
	kitchen_menu_stage = null
	if closing_fridge:
		_set_fridge_close_blocked(true)
		m._set_world_controls_enabled(false, "kitchen_fridge_close")
	m._set_world_controls_enabled(true, "kitchen_fridge_menu")
	return closing_fridge

func _wait_for_fridge_close() -> void:
	var record: Dictionary = m.castle_room_item_sprites.get("fridge", {})
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	if sprite == null:
		_set_fridge_close_blocked(false)
		m._set_world_controls_enabled(true, "kitchen_fridge_close")
		return
	var deadline_ms: int = Time.get_ticks_msec() + 3000
	while is_instance_valid(sprite) \
			and bool(sprite.get_meta("busy", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await m.get_tree().process_frame
	if not is_instance_valid(sprite):
		_set_fridge_close_blocked(false)
		m._set_world_controls_enabled(true, "kitchen_fridge_close")
		return
	if bool(sprite.get_meta("busy", false)):
		var close_tween: Tween = sprite.get_meta(
			"active_close_tween", null) as Tween
		if close_tween != null:
			close_tween.kill()
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		var sequence: Array[int] = _timeline_sequence(
			item_data, maxi(1, sprite.hframes * sprite.vframes))
		_finish_sprite_atlas_sequence(
			sprite, item_data, false, sequence.size() - 1)

func _kitchen_recipe(recipe_id: String) -> Dictionary:
	for recipe: Dictionary in KITCHEN_RECIPES:
		if String(recipe["id"]) == recipe_id:
			return recipe
	return {}

func _launch_kitchen_recipe(recipe_id: String) -> void:
	var recipe: Dictionary = _kitchen_recipe(recipe_id)
	if recipe.is_empty() or kitchen_act != null:
		return
	var uses: String = String(recipe["uses"])
	if uses != "" and int(m.opera_pantry.get(uses, 0)) <= 0:
		return
	var closing_fridge: bool = _close_kitchen_menu()
	if closing_fridge:
		await _wait_for_fridge_close()
	suspend()
	m.game = "kitchen_cooking"
	var config: Dictionary = (OperaHouse.ACTS[0] as Dictionary).duplicate(true)
	config["name"] = String(recipe["name"])
	config["act_tag"] = String(recipe["name"]) + "  "
	config["shell"] = false
	config["rescue"] = ""
	config["gift"] = ""
	config["uses"] = uses
	config["voice"] = (
		"Chef hat on! Let us make the %s together — every step is a "
		+ "different kitchen gesture!") % String(recipe["name"])
	config["win_line"] = (
		"Our %s is ready! Back into the royal kitchen it goes."
		% String(recipe["name"]))
	kitchen_act = OperaAct.new()
	kitchen_act.name = "KitchenCookingPortalAct"
	m.add_child(kitchen_act)
	kitchen_act.tree_exited.connect(_finish_kitchen_recipe)
	kitchen_act.start(m, config, Callable(self, "_finish_kitchen_recipe"))

func _finish_kitchen_recipe() -> void:
	if kitchen_act == null:
		return
	kitchen_act = null
	m.game = "level2"
	resume("kitchen")
	m.show_msg("Roshan", "Something delicious is ready!", "win")

# Suspend the castle, run the sparring class, and come home to the hall.
# The same cutaway pattern the kitchen and opera hall already use.
func _start_combat_tutorial() -> void:
	if m.combat_tutorial_game != null:
		return
	suspend()
	var tut := CombatTutorial.new()
	m.combat_tutorial_game = tut
	m.add_child(tut)
	tut.start(m, func() -> void:
		m.combat_tutorial_game = null
		resume("main_hall")
		m.show_msg("Roshan", "A royal wave from the throne!", "win"))

func activate_current_room() -> void:
	if _fridge_close_is_blocked():
		return
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
			if not _playroom_rescue_done():
				m.show_msg("Baby Eagle",
					"Bump both dust bunnies away first! I know you can do it!",
					"talk")
			elif m.companion_id == "":
				_open_playroom_stuffie_tutorial()
			else:
				m._companion_ref().open_picker(
					true, m.companion_id, "adopt")
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
		"dining":
			_activate_room_item(
				"provisions_hutch"
				if int(m.g.get("castle_dining_plates", 0)) <= 0
				else "dining_table")
		"sleep":
			_activate_room_item(
				"dream_bed_1"
				if m.castle_room_id == "sleepover_bedroom"
				else "canopy_bed")
		"movie":
			_activate_room_item("movie_screen")

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

func _go_back() -> void:
	if m.castle_room_id == "main_hall":
		_exit_to_courtyard()
	else:
		var parent_id: String = String(ROOM_PARENTS.get(
			m.castle_room_id, "main_hall"))
		show_room(parent_id, true)

func _exit_to_courtyard() -> void:
	if _fridge_close_is_blocked():
		return
	m._ui_tap()
	close()
	m._return_to_courtyard()
