extends RefCounted
# Room ancestry is the shipping CastleRooms25D graph, not an invented portal.
const ROOM_ROOT := "res://assets/flats/castle/rooms/background_tiles/"
const HALL_ROOT := "res://assets/flats/castle/main_hall_redraw_2026-08-03/tiles/"
const SKY_ROOT := "res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_"
const SECTORS := [
	{"id":"movie_lounge", "place":"movie_lounge", "until":0.20, "room":"movie_lounge", "columns":2, "road":Color("#e5c8c9"), "edge":Color("#b989bb"), "next":"family_gallery"},
	{"id":"gallery_out", "place":"family_gallery", "until":0.36, "room":"family_gallery", "columns":2, "road":Color("#e9d8c8"), "edge":Color("#b99cc7"), "next":"royal_bedroom"},
	{"id":"royal_bedroom", "place":"royal_bedroom", "until":0.64, "room":"royal_bedroom", "columns":2, "road":Color("#e6d0d9"), "edge":Color("#b997c7"), "next":"family_gallery"},
	{"id":"gallery_home", "place":"family_gallery", "until":0.82, "room":"family_gallery", "columns":2, "road":Color("#e9d8c8"), "edge":Color("#b99cc7"), "next":"movie_lounge"},
	{"id":"lounge_finish", "place":"movie_lounge", "until":1.0, "room":"movie_lounge", "columns":2, "road":Color("#e5c8c9"), "edge":Color("#b989bb"), "next":"movie_lounge"},
]
const HAZARDS: Array[Dictionary] = []
const FURNITURE := [
	{"u":0.105, "lat":-5.0, "half_width":2.5, "art":"res://assets/flats/castle/dream_house/cloud_settee.png"},
	{"u":0.50, "lat":5.0, "half_width":2.0, "art":"res://assets/flats/castle/dream_house/bedside_table.png"},
	{"u":0.915, "lat":4.5, "half_width":2.5, "art":"res://assets/flats/castle/dream_house/cloud_settee.png"},
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
	return a == b or (a == "family_gallery" and b in ["movie_lounge", "royal_bedroom"]) \
		or (b == "family_gallery" and a in ["movie_lounge", "royal_bedroom"])
