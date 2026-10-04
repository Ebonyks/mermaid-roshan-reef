extends RefCounted
# Room ancestry is the shipping CastleRooms25D graph, not an invented portal.
const ROOM_ROOT := "res://assets/flats/castle/rooms/background_tiles/"
const HALL_ROOT := "res://assets/flats/castle/main_hall_redraw_2026-08-03/tiles/"
const SKY_ROOT := "res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_"
const SECTORS := [
	{"id":"movie_lounge", "place":"movie_lounge", "until":0.07, "room":"movie_lounge", "columns":2, "road":Color("#e5c8c9"), "edge":Color("#b989bb"), "next":"family_gallery"},
	{"id":"family_gallery_out", "place":"family_gallery", "until":0.14, "room":"family_gallery", "columns":2, "road":Color("#e9d8c8"), "edge":Color("#b99cc7"), "next":"main_hall"},
	{"id":"main_hall_out", "place":"main_hall", "until":0.23, "hall":true, "window":1, "columns":4, "road":Color("#e6d9ce"), "edge":Color("#b997c7"), "next":"mermaid_pool"},
	{"id":"mermaid_pool", "place":"mermaid_pool", "until":0.32, "room":"mermaid_pool", "columns":4, "road":Color("#e9d6c1"), "edge":Color("#c7a1c5"), "next":"main_hall"},
	{"id":"main_hall_front", "place":"main_hall", "until":0.40, "hall":true, "window":1, "columns":4, "road":Color("#e6d9ce"), "edge":Color("#b997c7"), "next":"castle_bridge"},
	{"id":"castle_bridge_out", "place":"castle_bridge", "until":0.49, "sky":true, "window":2, "columns":2, "road":Color("#e9dabc"), "edge":Color("#ad95bf"), "next":"sky_lagoon"},
	{"id":"sky_lagoon", "place":"sky_lagoon", "until":0.68, "sky":true, "window":1, "columns":2, "road":Color("#e2d9b7"), "edge":Color("#8cafaa"), "next":"castle_bridge"},
	{"id":"castle_bridge_home", "place":"castle_bridge", "until":0.77, "sky":true, "window":2, "columns":2, "road":Color("#e9dabc"), "edge":Color("#ad95bf"), "next":"main_hall"},
	{"id":"main_hall_home", "place":"main_hall", "until":0.87, "hall":true, "window":0, "columns":4, "road":Color("#e6d9ce"), "edge":Color("#b997c7"), "next":"family_gallery"},
	{"id":"family_gallery_home", "place":"family_gallery", "until":0.94, "room":"family_gallery", "columns":2, "road":Color("#e9d8c8"), "edge":Color("#b99cc7"), "next":"movie_lounge"},
	{"id":"movie_lounge_finish", "place":"movie_lounge", "until":1.0, "room":"movie_lounge", "columns":2, "road":Color("#e5c8c9"), "edge":Color("#b989bb"), "next":"movie_lounge"},
]
const HAZARDS := [
	{"u":0.27, "kind":"crab"}, {"u":0.30, "kind":"geyser"},
	{"u":0.54, "kind":"whirl"}, {"u":0.58, "kind":"kelp"},
	{"u":0.63, "kind":"crab"}, {"u":0.66, "kind":"geyser"},
]
static func index_at(u: float) -> int:
	var wrapped := fposmod(u, 1.0)
	for i in range(SECTORS.size()):
		if wrapped < float(SECTORS[i]["until"]):
			return i
	return SECTORS.size() - 1

static func sector_at(u: float) -> Dictionary:
	return SECTORS[index_at(u)]

static func backdrop_paths(sector: Dictionary) -> Array[String]:
	var paths: Array[String] = []
	var columns: int = int(sector["columns"])
	var start: int = int(sector.get("window", 0)) * columns
	for row in range(2):
		for col in range(columns):
			if bool(sector.get("sky", false)):
				paths.append(SKY_ROOT + "r%d_c%d.png" % [row, start + col])
			elif bool(sector.get("hall", false)):
				paths.append(HALL_ROOT + "main_hall_room_led_r%d_c%d.png" % [row, start + col])
			else:
				paths.append(ROOM_ROOT + "room_%s_background_r%d_c%d.png" % [sector["room"], row, col])
	return paths

static func connected(a: String, b: String) -> bool:
	if a == b:
		return true
	var links := [["movie_lounge", "family_gallery"], ["family_gallery", "main_hall"],
		["main_hall", "mermaid_pool"], ["main_hall", "castle_bridge"],
		["castle_bridge", "sky_lagoon"]]
	for pair in links:
		if a in pair and b in pair:
			return true
	return false
