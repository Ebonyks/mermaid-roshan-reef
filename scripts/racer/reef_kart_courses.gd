extends RefCounted

const ROOMS := "res://assets/flats/castle/rooms/"
const COURSES := [
	{
		"id": "playroom", "pattern": 1, "wall_height": 0.47, "name": "Playroom Speedway", "room": "Castle Playroom",
		"hint": "Block slalom, stuffie nook, tent deck and toy parade",
		# Broad oval inspiration, now with an authored block slalom and tent approach.
		"points": [
			Vector2(640, 830), Vector2(850, 792), Vector2(1040, 844), Vector2(1150, 807),
			Vector2(1230, 732), Vector2(1260, 630), Vector2(1230, 528), Vector2(1150, 453),
			Vector2(1040, 430), Vector2(850, 468), Vector2(640, 412), Vector2(430, 430),
			Vector2(240, 430), Vector2(130, 453), Vector2(50, 528), Vector2(20, 630),
			Vector2(50, 732), Vector2(130, 807), Vector2(240, 830), Vector2(430, 830),
		],
		"scale": 1.25, "shift": Vector2(220, 350), "world_size": 2048.0,
		"items": [5, 15], "pearls": [2, 7, 12, 17],
		"palette": [Color("#a185c5"), Color("#675088"), Color("#f2d99f"),
			Color("#559d98"), Color("#6da8a2"), Color("#70818f")],
		"props": [
			{"id": "play_blocks", "path": "res://assets/racer/context_v2/play_blocks.png", "w": 158.0, "crop": Rect2(8, 13, 1008, 997)},
			{"id": "play_tent", "path": "res://assets/racer/context_v2/play_tent.png", "w": 218.0, "crop": Rect2(8, 38, 1008, 947)},
		],
	},
	{
		"id": "kitchen", "pattern": 2, "wall_height": 0.53, "name": "Copper Pan Circuit", "room": "Castle Kitchen",
		"hint": "Breakfast china, warm bakery, cool fridge corner and shell sink",
		# SNES Mario Circuit 1. Start up the east straight, run the long
		# diagonal, then follow the west straight into the return hook.
		"points": [
			Vector2(936, 632), Vector2(936, 542), Vector2(912, 481), Vector2(840, 439),
			Vector2(724, 380), Vector2(604, 321), Vector2(482, 259), Vector2(359, 199),
			Vector2(251, 149), Vector2(186, 145), Vector2(127, 169), Vector2(89, 223),
			Vector2(80, 303), Vector2(80, 432), Vector2(80, 563), Vector2(80, 699),
			Vector2(93, 778), Vector2(135, 807), Vector2(191, 790), Vector2(290, 741),
			Vector2(398, 685), Vector2(481, 652), Vector2(531, 660), Vector2(568, 709),
			Vector2(621, 816), Vector2(678, 930), Vector2(732, 974), Vector2(809, 991),
			Vector2(880, 982), Vector2(926, 950), Vector2(936, 871), Vector2(936, 755),
		],
		"scale": 2.15, "shift": Vector2(25, -40), "world_size": 2304.0,
		"items": [7, 14, 26], "pearls": [5, 12, 17, 21, 28],
		"palette": [Color("#a89179"), Color("#70697a"), Color("#f7d999"),
			Color("#618e85"), Color("#88b3a1"), Color("#896d94")],
		"props": [
			{"id": "kitchen_teapot", "path": "res://assets/racer/context_v2/kitchen_teapot.png", "w": 178.0, "crop": Rect2(8, 113, 1008, 798)},
			{"id": "kitchen_oven", "path": "res://assets/opera/worlds/chef_quality_20261019/oven_cool.png", "w": 174.0, "crop": Rect2(51, 8, 410, 496)},
			{"id": "kitchen_cake", "path": "res://assets/opera/worlds/props/goal_chef.png", "w": 158.0, "crop": Rect2(11, 50, 490, 455)},
			{"id": "kitchen_pitcher", "path": "res://assets/opera/worlds/chef_quality_20261019/pitcher_empty.png", "w": 154.0, "crop": Rect2(18, 44, 219, 166)},
		],
	},
	{
		"id": "mermaid_pool", "pattern": 3, "wall_height": 0.32, "name": "Seahorse Bridgeway", "room": "Mermaid Pool",
		"hint": "Towel alcove, fountain garden, float shallows and waterfall return",
		# SNES Donut Plains 3. Two straight crossings followed by the
		# central S and the southern hook. Bridge decks are continuous.
		"points": [
			Vector2(145, 600), Vector2(121, 541), Vector2(104, 483), Vector2(128, 412),
			Vector2(159, 355), Vector2(203, 294), Vector2(206, 249), Vector2(200, 211),
			Vector2(226, 173), Vector2(276, 168), Vector2(356, 188), Vector2(490, 188),
			Vector2(630, 188), Vector2(744, 167), Vector2(802, 173), Vector2(865, 205),
			Vector2(903, 260), Vector2(921, 326), Vector2(920, 390), Vector2(878, 427),
			Vector2(796, 456), Vector2(663, 456), Vector2(526, 456), Vector2(450, 456),
			Vector2(389, 464), Vector2(356, 491), Vector2(374, 537), Vector2(425, 590),
			Vector2(475, 626), Vector2(530, 630), Vector2(579, 626), Vector2(612, 655),
			Vector2(641, 711), Vector2(689, 748), Vector2(749, 760), Vector2(826, 765),
			Vector2(895, 788), Vector2(932, 829), Vector2(937, 875), Vector2(919, 906),
			Vector2(865, 924), Vector2(799, 923), Vector2(717, 931), Vector2(635, 918),
			Vector2(555, 899), Vector2(503, 869), Vector2(469, 812), Vector2(436, 790),
			Vector2(402, 791), Vector2(373, 826), Vector2(352, 889), Vector2(323, 966),
			Vector2(276, 997), Vector2(218, 997), Vector2(170, 968), Vector2(151, 914),
			Vector2(149, 842), Vector2(144, 770), Vector2(137, 694), Vector2(140, 648),
		],
		"scale": 3.25, "shift": Vector2(40, -55), "world_size": 3456.0,
		"items": [13, 23, 36, 51], "pearls": [4, 16, 27, 34, 43, 57],
		"palette": [Color("#47becb"), Color("#246a9b"), Color("#f5d8a7"),
			Color("#255574"), Color("#3e779a"), Color("#62a7b9")],
		"bridges": [Rect2(356, 142, 319, 92), Rect2(447, 411, 337, 92)],
		"props": [
			{"id": "pool_seahorse", "path": "res://assets/racer/context_v2/pool_seahorse.png", "w": 124.0, "crop": Rect2(210, 8, 603, 1008)},
			{"id": "pool_fountain", "path": "res://assets/flats/castle/rooms/room_main_hall_item_fountain_left_v2.png", "w": 226.0, "crop": Rect2(0, 3, 214, 179)},
			{"id": "pool_star", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_star_float.png", "w": 90.0, "crop": Rect2(10, 9, 70, 49)},
			{"id": "pool_flower", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_flower_float.png", "w": 100.0, "crop": Rect2(5, 7, 94, 69)},
		],
	},
	{
		"id": "opera_hall", "pattern": 4, "wall_height": 0.45, "name": "Footlight Finale", "room": "Opera Hall",
		"hint": "Pearl lobby, music rehearsal, footlight stage and backstage",
		# SNES Rainbow Road. Follow the main loop and the inside line of
		# the split on the bottom straight. Rounded corners suit kart scale.
		"points": [
			Vector2(64, 504), Vector2(64, 366), Vector2(64, 238), Vector2(72, 158),
			Vector2(119, 121), Vector2(211, 120), Vector2(348, 120), Vector2(491, 120),
			Vector2(632, 120), Vector2(717, 122), Vector2(747, 162), Vector2(750, 252),
			Vector2(750, 371), Vector2(746, 454), Vector2(713, 493), Vector2(622, 500),
			Vector2(507, 500), Vector2(391, 500), Vector2(330, 510), Vector2(320, 553),
			Vector2(320, 631), Vector2(323, 697), Vector2(371, 731), Vector2(466, 731),
			Vector2(600, 731), Vector2(737, 731), Vector2(865, 731), Vector2(929, 736),
			Vector2(958, 775), Vector2(958, 845), Vector2(958, 937), Vector2(946, 989),
			Vector2(898, 1004), Vector2(813, 1004), Vector2(679, 1004), Vector2(543, 1004),
			Vector2(468, 976), Vector2(378, 972), Vector2(282, 972), Vector2(211, 981),
			Vector2(151, 1004), Vector2(101, 999), Vector2(67, 968), Vector2(64, 886),
			Vector2(64, 746), Vector2(64, 624),
		],
		"scale": 2.9, "shift": Vector2(60, -95), "world_size": 3072.0,
		"items": [6, 17, 27, 39], "pearls": [3, 10, 15, 24, 33, 44],
		"palette": [Color("#ae88b5"), Color("#694679"), Color("#ffd58d"),
			Color("#373658"), Color("#554567"), Color("#66537b")],
		"props": [
			{"id": "opera_musicbox", "path": "res://assets/opera/worlds/props/goal_ballerina.png", "w": 170.0, "crop": Rect2(71, 14, 370, 492)},
			{"id": "opera_microphone", "path": "res://assets/opera/worlds/props/goal_popstar.png", "w": 110.0, "crop": Rect2(167, 14, 177, 491)},
			{"id": "opera_cup", "path": "res://assets/opera/worlds/props/goal_racer.png", "w": 134.0, "crop": Rect2(29, 15, 454, 490)},
			{"id": "opera_footlights", "path": "res://assets/flats/castle/rooms/room_opera_hall_item_footlights.png", "w": 140.0, "crop": Rect2(14, 1, 166, 21)},
		],
	},
]


static func room_art(course: Dictionary) -> Texture2D:
	return load(ROOMS + "room_%s_background.png" % course["id"]) as Texture2D
