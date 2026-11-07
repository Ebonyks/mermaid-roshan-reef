extends RefCounted
## Authored room journeys. Prop stations are lap fractions, never a cyclic scatter.
## Reused source contours stay untouched; the towel cabinet fills one inventoried gap.

const ZONES := {
	"playroom": [
		{"name": "Building blocks", "road": Color("#b7a6d8"), "ground": Color("#ead9ad"), "surface": 0, "props": [
			{"id": "play_blocks", "path": "res://assets/racer/context_v2/play_blocks.png", "crop": Rect2(8, 13, 1008, 997), "w": 300.0, "max_h": 320.0, "at": 0.03, "lat": -340.0},
			{"id": "room_playroom_item_stacking_toy", "path": "res://assets/flats/castle/rooms/room_playroom_item_stacking_toy.png", "crop": Rect2(15, 10, 92, 144), "w": 180.0, "max_h": 320.0, "at": 0.13, "lat": 300.0},
			{"id": "play_blocks", "path": "res://assets/racer/context_v2/play_blocks.png", "crop": Rect2(8, 13, 1008, 997), "w": 180.0, "max_h": 320.0, "at": 0.21, "lat": -310.0},
		]},
		{"name": "Stuffie nook", "road": Color("#e7b4c4"), "ground": Color("#cda3c7"), "surface": 1, "props": [
			{"id": "room_playroom_item_stuffie_nook", "path": "res://assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png", "crop": Rect2(8, 15, 240, 159), "w": 440.0, "max_h": 320.0, "at": 0.29, "lat": -400.0},
			{"id": "pillows", "path": "res://assets/opera/worlds/nursery_quality_20261019/pillows.png", "crop": Rect2(4, 4, 1013, 117), "w": 280.0, "max_h": 320.0, "at": 0.39, "lat": -330.0},
			{"id": "room_playroom_item_stacking_toy", "path": "res://assets/flats/castle/rooms/room_playroom_item_stacking_toy.png", "crop": Rect2(15, 10, 92, 144), "w": 120.0, "max_h": 320.0, "at": 0.45, "lat": 295.0},
		]},
		{"name": "Tent camp", "road": Color("#86b6b1"), "ground": Color("#dfc798"), "surface": 2, "props": [
			{"id": "play_tent", "path": "res://assets/racer/context_v2/play_tent.png", "crop": Rect2(8, 38, 1008, 947), "w": 410.0, "max_h": 320.0, "at": 0.54, "lat": -400.0},
			{"id": "pillows", "path": "res://assets/opera/worlds/nursery_quality_20261019/pillows.png", "crop": Rect2(4, 4, 1013, 117), "w": 250.0, "max_h": 320.0, "at": 0.63, "lat": 310.0},
			{"id": "play_blocks", "path": "res://assets/racer/context_v2/play_blocks.png", "crop": Rect2(8, 13, 1008, 997), "w": 110.0, "max_h": 320.0, "at": 0.7, "lat": -290.0},
		]},
		{"name": "Music and toy parade", "road": Color("#d2b472"), "ground": Color("#b6b2d6"), "surface": 3, "props": [
			{"id": "room_playroom_item_stacking_toy", "path": "res://assets/flats/castle/rooms/room_playroom_item_stacking_toy.png", "crop": Rect2(15, 10, 92, 144), "w": 230.0, "max_h": 320.0, "at": 0.79, "lat": -350.0},
			{"id": "opera_musicbox", "path": "res://assets/opera/worlds/props/goal_ballerina.png", "crop": Rect2(71, 14, 370, 492), "w": 220.0, "max_h": 320.0, "at": 0.88, "lat": -350.0},
			{"id": "room_playroom_item_stuffie_nook", "path": "res://assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png", "crop": Rect2(8, 15, 240, 159), "w": 260.0, "max_h": 320.0, "at": 0.95, "lat": 345.0},
		]},
	],
	"kitchen": [
		{"name": "Breakfast china", "road": Color("#9ebdb6"), "ground": Color("#e5cead"), "surface": 0, "props": [
			{"id": "kitchen_teapot", "path": "res://assets/racer/context_v2/kitchen_teapot.png", "crop": Rect2(8, 113, 1008, 798), "w": 310.0, "max_h": 320.0, "at": 0.04, "lat": -370.0},
			{"id": "kitchen_pitcher", "path": "res://assets/opera/worlds/chef_quality_20261019/pitcher_empty.png", "crop": Rect2(18, 44, 219, 166), "w": 190.0, "max_h": 320.0, "at": 0.13, "lat": -310.0},
			{"id": "bowl_empty", "foot_y": 0.895, "path": "res://assets/opera/worlds/chef_quality_20261019/bowl_empty.png", "crop": Rect2(8, 43, 495, 460), "w": 140.0, "max_h": 320.0, "at": 0.2, "lat": 300.0},
		]},
		{"name": "Copper oven bakery", "road": Color("#d6a26e"), "ground": Color("#b99586"), "surface": 2, "props": [
			{"id": "kitchen_oven", "path": "res://assets/opera/worlds/chef_quality_20261019/oven_cool.png", "crop": Rect2(51, 8, 410, 496), "w": 300.0, "max_h": 320.0, "at": 0.29, "lat": 370.0},
			{"id": "cake_frosted", "path": "res://assets/opera/worlds/chef_quality_20261019/cake_frosted.png", "crop": Rect2(82, 11, 346, 494), "w": 220.0, "max_h": 320.0, "at": 0.38, "lat": 340.0},
			{"id": "piping_bag", "path": "res://assets/opera/worlds/chef_quality_20261019/piping_bag.png", "crop": Rect2(9, 26, 494, 459), "w": 160.0, "max_h": 320.0, "at": 0.45, "lat": -330.0},
		]},
		{"name": "Cool fridge corner", "road": Color("#a5c5cf"), "ground": Color("#b9c3b3"), "surface": 3, "props": [
			{"id": "room_kitchen_item_fridge", "path": "res://assets/flats/castle/rooms/room_kitchen_item_fridge.png", "crop": Rect2(3, 2, 135, 256), "w": 230.0, "max_h": 320.0, "at": 0.54, "lat": -370.0},
			{"id": "bowl_stirred", "foot_y": 0.895, "path": "res://assets/opera/worlds/chef_quality_20261019/bowl_stirred.png", "crop": Rect2(9, 44, 494, 458), "w": 190.0, "max_h": 320.0, "at": 0.63, "lat": -330.0},
			{"id": "kitchen_pitcher", "path": "res://assets/opera/worlds/chef_quality_20261019/pitcher_empty.png", "crop": Rect2(18, 44, 219, 166), "w": 160.0, "max_h": 320.0, "at": 0.7, "lat": 310.0},
		]},
		{"name": "Shell sink and drying corner", "road": Color("#79b5c4"), "ground": Color("#deceb2"), "surface": 0, "props": [
			{"id": "room_kitchen_item_sink", "path": "res://assets/flats/castle/rooms/room_kitchen_item_sink.png", "crop": Rect2(16, 7, 164, 93), "w": 370.0, "max_h": 320.0, "at": 0.79, "lat": -400.0},
			{"id": "bowl_empty", "foot_y": 0.895, "path": "res://assets/opera/worlds/chef_quality_20261019/bowl_empty.png", "crop": Rect2(8, 43, 495, 460), "w": 180.0, "max_h": 320.0, "at": 0.87, "lat": -320.0},
			{"id": "kitchen_teapot", "path": "res://assets/racer/context_v2/kitchen_teapot.png", "crop": Rect2(8, 113, 1008, 798), "w": 180.0, "max_h": 320.0, "at": 0.94, "lat": 320.0},
		]},
	],
	"mermaid_pool": [
		{"name": "Shell changing alcove", "road": Color("#b7a6d7"), "ground": Color("#ecd0b1"), "surface": 1, "props": [
			{"id": "pool_towel_cabinet", "path": "res://assets/racer/zones_v1/pool_towel_cabinet.png", "crop": Rect2(177, 8, 669, 1008), "w": 245.0, "max_h": 320.0, "at": 0.045, "lat": -365.0},
			{"id": "pool_flower", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_flower_float.png", "crop": Rect2(5, 7, 94, 69), "w": 130.0, "max_h": 320.0, "at": 0.13, "lat": 300.0},
		]},
		{"name": "Seahorse fountain garden", "road": Color("#6ccbd0"), "ground": Color("#9ac0bd"), "surface": 0, "props": [
			{"id": "pool_seahorse", "path": "res://assets/racer/context_v2/pool_seahorse.png", "crop": Rect2(210, 8, 603, 1008), "w": 190.0, "max_h": 320.0, "at": 0.29, "lat": -355.0},
			{"id": "pool_fountain", "path": "res://assets/flats/castle/rooms/room_main_hall_item_fountain_left_v2.png", "crop": Rect2(0, 3, 214, 179), "w": 320.0, "max_h": 320.0, "at": 0.37, "lat": -390.0},
			{"id": "room_mermaid_pool_item_bubble_fountain", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_bubble_fountain.png", "crop": Rect2(59, 16, 61, 94), "w": 170.0, "max_h": 320.0, "at": 0.45, "lat": 330.0},
		]},
		{"name": "Floating flower shallows", "road": Color("#56b9ca"), "ground": Color("#518da9"), "surface": 3, "props": [
			{"id": "pool_flower", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_flower_float.png", "crop": Rect2(5, 7, 94, 69), "w": 175.0, "max_h": 320.0, "at": 0.54, "lat": -330.0},
			{"id": "pool_star", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_star_float.png", "crop": Rect2(10, 9, 70, 49), "w": 155.0, "max_h": 320.0, "at": 0.62, "lat": 310.0},
			{"id": "pool_flower", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_flower_float.png", "crop": Rect2(5, 7, 94, 69), "w": 120.0, "max_h": 320.0, "at": 0.7, "lat": -290.0},
		]},
		{"name": "Rainbow waterfall return", "road": Color("#9bc9cd"), "ground": Color("#d5b4c8"), "surface": 2, "props": [
			{"id": "room_mermaid_pool_item_waterfall", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_waterfall.png", "crop": Rect2(9, 10, 121, 166), "w": 310.0, "max_h": 320.0, "at": 0.82, "lat": 400.0},
			{"id": "pool_star", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_star_float.png", "crop": Rect2(10, 9, 70, 49), "w": 135.0, "max_h": 320.0, "at": 0.87, "lat": 305.0},
			{"id": "room_mermaid_pool_item_bubble_fountain", "path": "res://assets/flats/castle/rooms/room_mermaid_pool_item_bubble_fountain.png", "crop": Rect2(59, 16, 61, 94), "w": 190.0, "max_h": 320.0, "at": 0.94, "lat": -335.0},
		]},
	],
	"opera_hall": [
		{"name": "Pearl lobby", "road": Color("#c5a184"), "ground": Color("#b58d9d"), "surface": 0, "props": [
			{"id": "opera_cup", "path": "res://assets/opera/worlds/props/goal_racer.png", "crop": Rect2(29, 15, 454, 490), "w": 250.0, "max_h": 320.0, "at": 0.04, "lat": -355.0},
			{"id": "room_opera_hall_item_chandelier", "lift": 140.0, "path": "res://assets/flats/castle/rooms/room_opera_hall_item_chandelier.png", "crop": Rect2(24, 5, 140, 83), "w": 300.0, "max_h": 320.0, "at": 0.13, "lat": -405.0},
			{"id": "opera_cup", "path": "res://assets/opera/worlds/props/goal_racer.png", "crop": Rect2(29, 15, 454, 490), "w": 160.0, "max_h": 320.0, "at": 0.2, "lat": 315.0},
		]},
		{"name": "Rehearsal music boxes", "road": Color("#be95c9"), "ground": Color("#a9a3c4"), "surface": 1, "props": [
			{"id": "opera_musicbox", "path": "res://assets/opera/worlds/props/goal_ballerina.png", "crop": Rect2(71, 14, 370, 492), "w": 290.0, "max_h": 320.0, "at": 0.29, "lat": -375.0},
			{"id": "opera_microphone", "path": "res://assets/opera/worlds/props/goal_popstar.png", "crop": Rect2(167, 14, 177, 491), "w": 160.0, "max_h": 320.0, "at": 0.37, "lat": 330.0},
			{"id": "opera_musicbox", "path": "res://assets/opera/worlds/props/goal_ballerina.png", "crop": Rect2(71, 14, 370, 492), "w": 160.0, "max_h": 320.0, "at": 0.45, "lat": -310.0},
		]},
		{"name": "Footlight stage", "road": Color("#cfaa77"), "ground": Color("#725e89"), "surface": 2, "props": [
			{"id": "room_opera_hall_item_curtains", "path": "res://assets/flats/castle/rooms/room_opera_hall_item_curtains.png", "crop": Rect2(13, 11, 168, 176), "w": 400.0, "max_h": 320.0, "at": 0.54, "lat": -425.0},
			{"id": "opera_footlights", "path": "res://assets/flats/castle/rooms/room_opera_hall_item_footlights.png", "crop": Rect2(14, 1, 166, 21), "w": 240.0, "max_h": 320.0, "at": 0.61, "lat": -340.0},
			{"id": "opera_footlights", "path": "res://assets/flats/castle/rooms/room_opera_hall_item_footlights.png", "crop": Rect2(14, 1, 166, 21), "w": 240.0, "max_h": 320.0, "at": 0.69, "lat": 340.0},
		]},
		{"name": "Backstage magic wing", "road": Color("#8b9eac"), "ground": Color("#9d869f"), "surface": 3, "props": [
			{"id": "goal_magician", "path": "res://assets/opera/worlds/props/goal_magician.png", "crop": Rect2(68, 16, 375, 488), "w": 240.0, "max_h": 320.0, "at": 0.79, "lat": -380.0},
			{"id": "room_opera_hall_item_curtains", "path": "res://assets/flats/castle/rooms/room_opera_hall_item_curtains.png", "crop": Rect2(13, 11, 168, 176), "w": 270.0, "max_h": 320.0, "at": 0.87, "lat": 370.0},
			{"id": "opera_microphone", "path": "res://assets/opera/worlds/props/goal_popstar.png", "crop": Rect2(167, 14, 177, 491), "w": 150.0, "max_h": 320.0, "at": 0.95, "lat": -315.0},
		]},
	],
}
