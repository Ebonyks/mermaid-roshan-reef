class_name ReefKartTrack
extends RefCounted
## The Pearl Canal Circuit: the Racer career's own in-game world painting
## (assets_src/imagegen/opera_codex_2026-08-02/native/world_racer_native.png,
## drawn in game from the POT tiles assets/opera/worlds/backdrops/
## world_racer_c*r*.png) laid out flat for driving.
##
## The course is data: a closed Catmull-Rom centre line in world units over a
## 2048-unit square, the water lane's half-width, the tan stone curb (a slow
## apron) and the lilac wall (a soft rail). Every pearl row, item source and
## landmark is tied to a control point of the course, so painted floor art and
## physics always agree.
##
## Reading of the painting (owner rule 2026-11-03: tracks must resemble the
## in-game setting closely). An aqua water lane with pale lane lines runs
## between tan stone curbs on lilac stone foundations. The race starts under
## the pearl-studded shell arch at the left (the career's "pearl starting
## arch"). The front straight runs east past three gem buoys (teal, lavender,
## pink) to the pink checkered-ribbon arch. An S-bend climbs to the east pearl
## arch. The raised back straight, with its pearl-studded lilac railing, bows
## north behind the pearl-dome pavilion in the sandy infield. The west pearl
## arch leads down the western S-bend and round the corner to the line.
## Coral, clams, rocks and pennants line the outside. It reproduces no
## commercial circuit.

const WORLD_SIZE := 2048.0
const SAMPLES := 720
const ROAD_HALF := 112.0
const RAIL := 140.0
const FIELD_SIZE := 128
## Field distances are stored as a fraction of FIELD_FAR; cells beyond
## FIELD_REACH of every centre sample read as plain outside ground.
const FIELD_FAR := RAIL * 1.6
const FIELD_REACH := 200.0
const TRACK_ROOT := "res://assets/racer/tracks/pearl_canal/"
const PAINTED_FLOOR := TRACK_ROOT + "floor.png"
const PAINTED_SKYLINE := TRACK_ROOT + "skyline.png"

enum Terrain { ROAD, APRON, RAIL }

## Driving order (counter-clockwise on the map): 64 points about 67 units
## apart, sampled from four corners of radius 180, the front straight, the
## north-bowed back straight and two S-bends that meet the corners tangentially
## (see TRACK.md section 2). Dense points keep the spline on the true arcs.
## Point 0 is the start/finish line under the pearl starting arch, heading east
## along the front straight.
const POINTS: Array[Vector2] = [
	Vector2(760, 1650), Vector2(827, 1650), Vector2(894, 1650),
	Vector2(962, 1650), Vector2(1029, 1650), Vector2(1097, 1650),
	Vector2(1164, 1650), Vector2(1232, 1650), Vector2(1299, 1650),
	Vector2(1367, 1650), Vector2(1434, 1650), Vector2(1502, 1650),
	Vector2(1569, 1650), Vector2(1636, 1641), Vector2(1695, 1609),
	Vector2(1737, 1557), Vector2(1759, 1493), Vector2(1764, 1426),
	Vector2(1780, 1361), Vector2(1796, 1295), Vector2(1796, 1228),
	Vector2(1777, 1163), Vector2(1750, 1102), Vector2(1727, 1038),
	Vector2(1722, 971), Vector2(1736, 905), Vector2(1753, 840),
	Vector2(1760, 773), Vector2(1745, 708), Vector2(1707, 652),
	Vector2(1651, 615), Vector2(1586, 600), Vector2(1518, 598),
	Vector2(1451, 592), Vector2(1384, 583), Vector2(1317, 574),
	Vector2(1250, 566), Vector2(1183, 561), Vector2(1116, 560),
	Vector2(1048, 564), Vector2(981, 572), Vector2(914, 581),
	Vector2(847, 590), Vector2(780, 597), Vector2(713, 600),
	Vector2(647, 608), Vector2(587, 640), Vector2(544, 691),
	Vector2(522, 754), Vector2(516, 822), Vector2(501, 887),
	Vector2(485, 953), Vector2(484, 1020), Vector2(502, 1084),
	Vector2(529, 1146), Vector2(552, 1210), Vector2(558, 1277),
	Vector2(545, 1343), Vector2(527, 1408), Vector2(520, 1475),
	Vector2(534, 1540), Vector2(571, 1596), Vector2(627, 1635),
	Vector2(692, 1650),
]
## What stands at the named control points (see TRACK.md section 2).
const START_POINT := 0
const BUOY_POINTS: Array[int] = [4, 6, 8]
const RIBBON_POINT := 12
const EAST_ARCH_POINT := 31
const WEST_ARCH_POINT := 44

## Pearl rows: control point, along-course offset, lateral offset (right of
## travel is positive), count and spacing. Rows sit on straights, on the
## S-bends' crossover points or on the outside of a corner, where a kart at
## full speed can hold the lane. Every row is at least 55 units from the
## starting lane (-36), so a kart that is never steered collects none. The
## first row, on the left of the front straight, faces the gem buoys on the
## right: pearls one side, items the other.
const PEARL_ROWS: Array[Dictionary] = [
	{"at": 2, "offset": 0.0, "lat": -96.0, "count": 4, "gap": 52.0},
	{"at": 22, "offset": -78.0, "lat": 60.0, "count": 4, "gap": 52.0},
	{"at": 34, "offset": 0.0, "lat": 70.0, "count": 5, "gap": 52.0},
	{"at": 41, "offset": 0.0, "lat": 30.0, "count": 4, "gap": 52.0},
	{"at": 54, "offset": -78.0, "lat": -96.0, "count": 4, "gap": 52.0},
	{"at": 61, "offset": -52.0, "lat": 60.0, "count": 5, "gap": 52.0},
]
## Rows of three item bubbles under each pearl arch (the "gates").
const ITEM_ROW_POINTS: Array[int] = [EAST_ARCH_POINT, WEST_ARCH_POINT]
const ITEM_LATS: Array[float] = [-64.0, 0.0, 64.0]
## The three gem buoys on the front straight also deal an item.
const BUOY_LAT := 40.0
const BUOY_COLORS: Array[String] = ["teal", "lavender", "pink"]
## Painted landmarks staged as upright cards once Codex has isolated them
## from the painting. at = control point, offset = along-course units from it,
## lat = lateral offset of the card centre, w/h = world size, lift = height of
## the card's lower edge above the ground, spans = an arch over the lane (the
## kart drives through its transparent opening). Flat features such as the
## sandy infield belong to the painted floor. Missing art is skipped; spanning
## arches then get an interim drawing.
const LANDMARKS: Array[Dictionary] = [
	{"id": "pearl_start_arch", "at": START_POINT, "offset": 0.0, "lat": 0.0, "w": 330.0, "h": 250.0, "spans": true},
	{"id": "coral_cluster", "at": 6, "offset": 0.0, "lat": 230.0, "w": 200.0, "h": 150.0},
	{"id": "pearl_clam", "at": 8, "offset": 0.0, "lat": -250.0, "w": 170.0, "h": 110.0},
	{"id": "ribbon_arch", "at": RIBBON_POINT, "offset": 0.0, "lat": 0.0, "w": 330.0, "h": 250.0, "spans": true},
	{"id": "coral_cluster", "at": 22, "offset": 0.0, "lat": 230.0, "w": 200.0, "h": 150.0},
	{"id": "pearl_arch", "at": EAST_ARCH_POINT, "offset": 0.0, "lat": 0.0, "w": 330.0, "h": 260.0, "spans": true},
	{"id": "pennant", "at": 35, "offset": 0.0, "lat": 250.0, "w": 110.0, "h": 190.0},
	{"id": "pavilion", "at": 38, "offset": 0.0, "lat": -330.0, "w": 340.0, "h": 320.0},
	{"id": "pennant", "at": 41, "offset": 0.0, "lat": 250.0, "w": 110.0, "h": 190.0},
	{"id": "pearl_arch", "at": WEST_ARCH_POINT, "offset": 0.0, "lat": 0.0, "w": 330.0, "h": 260.0, "spans": true},
	{"id": "coral_cluster", "at": 54, "offset": 0.0, "lat": 230.0, "w": 200.0, "h": 150.0},
	{"id": "pearl_clam", "at": 61, "offset": 0.0, "lat": 230.0, "w": 170.0, "h": 110.0},
	# Painted reef clusters at fixed stations fill the depth between the road and open water.
	{"id": "reef_shell_terrace", "at": 1, "offset": 0.0, "lat": 415.0, "w": 375.0, "h": 166.0},
	{"id": "reef_coral_ledge", "at": 4, "offset": 0.0, "lat": -490.0, "w": 410.0, "h": 209.0},
	{"id": "reef_fan", "at": 10, "offset": 0.0, "lat": -365.0, "w": 278.0, "h": 244.0},
	{"id": "reef_pearl_garden", "at": 15, "offset": 0.0, "lat": 402.0, "w": 420.0, "h": 188.0},
	{"id": "reef_coral_ledge", "at": 20, "offset": 0.0, "lat": 472.0, "w": 450.0, "h": 225.0},
	{"id": "reef_blue_shelf", "at": 23, "offset": 0.0, "lat": -340.0, "w": 262.0, "h": 170.0},
	{"id": "reef_fan", "at": 27, "offset": 0.0, "lat": 395.0, "w": 302.0, "h": 242.0},
	{"id": "reef_shell_terrace", "at": 32, "offset": 0.0, "lat": 427.0, "w": 389.0, "h": 165.0},
	{"id": "reef_pearl_garden", "at": 35, "offset": 0.0, "lat": -495.0, "w": 420.0, "h": 175.0},
	{"id": "reef_blue_shelf", "at": 40, "offset": 0.0, "lat": -395.0, "w": 320.0, "h": 171.0},
	{"id": "reef_coral_ledge", "at": 42, "offset": 0.0, "lat": 467.0, "w": 425.0, "h": 220.0},
	{"id": "reef_shell_terrace", "at": 46, "offset": 0.0, "lat": -390.0, "w": 370.0, "h": 168.0},
	{"id": "reef_pearl_garden", "at": 50, "offset": 0.0, "lat": 435.0, "w": 405.0, "h": 173.0},
	{"id": "reef_fan", "at": 53, "offset": 0.0, "lat": -405.0, "w": 285.0, "h": 235.0},
	{"id": "reef_blue_shelf", "at": 57, "offset": 0.0, "lat": 402.0, "w": 309.0, "h": 187.0},
	{"id": "reef_coral_ledge", "at": 60, "offset": 0.0, "lat": -480.0, "w": 440.0, "h": 215.0},
]
const CHECKPOINTS := 8

var id := "pearl_canal"
var room: Dictionary
var world_size := WORLD_SIZE
var _control_points := PackedVector2Array(POINTS)
var center := PackedVector2Array()
var tangents := PackedVector2Array()
var cumulative := PackedFloat32Array()
var curvatures := PackedFloat32Array()
var point_s := PackedFloat32Array()
var length := 0.0
var pearls: Array[Dictionary] = []
var bubbles: Array[Dictionary] = []
var buoys: Array[Dictionary] = []
var landmarks: Array[Dictionary] = []
var roadside: Array[Dictionary] = []
var gate_s: Array[float] = []
var shortcut: Dictionary = {}
var boost_pads: Array[Dictionary] = []
var obstacles: Array[Dictionary] = []

static var _field_cache: ImageTexture = null
static var _room_fields: Dictionary = {}


func _init(course: Dictionary = {}) -> void:
	room = course.duplicate(true)
	if not room.is_empty():
		room["zones"] = preload("res://scripts/racer/reef_kart_zones.gd").ZONES[String(room["id"])]
	if not room.is_empty():
		id = String(room["id"])
		world_size = float(room["world_size"])
		_control_points.clear()
		var scale := float(room["scale"])
		var shift: Vector2 = room["shift"]
		for point: Vector2 in room["points"]:
			_control_points.append(point * scale + shift)
	_build_centerline()
	if room.is_empty():
		_build_features()
	else:
		_build_course_challenges()
		_build_room_features()


func _catmull(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2
		+ (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)


func _build_centerline() -> void:
	# Dense pass, then resample uniformly by arc length so every sample is the
	# same distance apart and projection windows have a fixed meaning.
	var dense := PackedVector2Array()
	var count := _control_points.size()
	for index in range(count):
		var p0 := _control_points[(index - 1 + count) % count]
		var p1 := _control_points[index]
		var p2 := _control_points[(index + 1) % count]
		var p3 := _control_points[(index + 2) % count]
		for step in range(24):
			dense.append(_catmull(p0, p1, p2, p3, float(step) / 24.0))
	var dense_len := PackedFloat32Array()
	dense_len.resize(dense.size() + 1)
	dense_len[0] = 0.0
	for index in range(dense.size()):
		dense_len[index + 1] = dense_len[index] \
			+ dense[index].distance_to(dense[(index + 1) % dense.size()])
	length = dense_len[dense.size()]
	point_s.resize(count)
	for index in range(count):
		point_s[index] = dense_len[index * 24]
	center.resize(SAMPLES)
	cumulative.resize(SAMPLES)
	var cursor := 0
	for sample in range(SAMPLES):
		var target := length * float(sample) / float(SAMPLES)
		while cursor < dense.size() - 1 and dense_len[cursor + 1] < target:
			cursor += 1
		var seg := maxf(0.0001, dense_len[cursor + 1] - dense_len[cursor])
		var t := clampf((target - dense_len[cursor]) / seg, 0.0, 1.0)
		center[sample] = dense[cursor].lerp(dense[(cursor + 1) % dense.size()], t)
		cumulative[sample] = target
	tangents.resize(SAMPLES)
	curvatures.resize(SAMPLES)
	for sample in range(SAMPLES):
		var before := center[(sample - 1 + SAMPLES) % SAMPLES]
		var after := center[(sample + 1) % SAMPLES]
		tangents[sample] = (after - before).normalized()
	var spacing := length / float(SAMPLES)
	for sample in range(SAMPLES):
		var a := tangents[(sample - 2 + SAMPLES) % SAMPLES]
		var b := tangents[(sample + 2) % SAMPLES]
		# Signed curvature: positive turns right (clockwise on screen).
		curvatures[sample] = a.angle_to(b) / (4.0 * spacing)


## Course distance of a control point plus an along-course offset.
func s_of(point: int, offset: float = 0.0) -> float:
	return wrap_s(point_s[clampi(point, 0, _control_points.size() - 1)] + offset)


func _build_features() -> void:
	pearls.clear()
	for row: Dictionary in PEARL_ROWS:
		var start := s_of(int(row["at"]), float(row["offset"]))
		for index in range(int(row["count"])):
			var s := wrap_s(start + float(index) * float(row["gap"]))
			pearls.append({"s": s, "lat": float(row["lat"]),
				"pos": point_at(s, float(row["lat"])), "respawn_t": 0.0})
	bubbles.clear()
	gate_s.clear()
	for point: int in ITEM_ROW_POINTS:
		var s := s_of(point)
		gate_s.append(s)
		for lat: float in ITEM_LATS:
			bubbles.append({"s": s, "lat": lat, "pos": point_at(s, lat), "respawn_t": 0.0})
	buoys.clear()
	for index in range(BUOY_POINTS.size()):
		var s := s_of(BUOY_POINTS[index])
		buoys.append({"s": s, "lat": BUOY_LAT, "pos": point_at(s, BUOY_LAT),
			"color": BUOY_COLORS[index], "respawn_t": 0.0})
	landmarks.clear()
	for spec: Dictionary in LANDMARKS:
		var s := s_of(int(spec["at"]), float(spec.get("offset", 0.0)))
		var entry := spec.duplicate()
		entry["s"] = s
		entry["pos"] = point_at(s, float(spec["lat"]))
		landmarks.append(entry)


func _build_course_challenges() -> void:
	var cut: Dictionary = room["cut"]
	var start_s := s_of(int(cut["in"]))
	var end_s := s_of(int(cut["out"]), float(cut.get("out_offset", 0.0)))
	var start := point_at(start_s, float(cut["entry_lat"]))
	var end := point_at(end_s, float(cut["exit_lat"]))
	var direction := start.direction_to(end)
	var across := Vector2(-direction.y, direction.x)
	var distance := start.distance_to(end)
	shortcut = {"start_s": start_s, "end_s": end_s, "start": start, "end": end,
		"along": direction, "across": across, "length": distance, "half": float(cut["half"])}
	for spec: Dictionary in room["boosts"]:
		var s := s_of(int(spec["at"]), float(spec["offset"]))
		boost_pads.append({"pos": point_at(s, float(spec["lat"])), "along": tangent_at(s),
			"half": Vector2(30.0, 35.0), "duration": 0.85})
	var boost: Vector2 = room["cut_boost"]
	boost_pads.append({"pos": start + direction * (distance * boost.x) + across * boost.y,
		"along": direction, "half": Vector2(34.0, 30.0), "duration": 0.7})
	for spec: Dictionary in room["obstacles"]:
		for prop: Dictionary in room["props"]:
			if prop["id"] != spec["prop"]:
				continue
			var obstacle := prop.duplicate()
			obstacle["s"] = s_of(int(spec["at"]), float(spec["offset"]))
			obstacle["lat"] = spec["lat"]
			obstacle["sway"] = spec.get("sway", 0.0)
			obstacle["radius"] = spec["radius"]
			obstacle["w"] = float(spec["radius"]) * 2.0
			obstacle["max_h"] = 66.0
			obstacle["phase"] = float(obstacles.size()) * PI
			obstacle["pos"] = obstacle_position(obstacle, 0.0)
			obstacle["course_obstacle"] = true
			obstacles.append(obstacle)
			landmarks.append(obstacle)
			break


func obstacle_position(obstacle: Dictionary, race_time: float) -> Vector2:
	var lateral := float(obstacle["lat"]) + float(obstacle["sway"]) \
		* sin(race_time * 1.55 + float(obstacle["phase"]))
	return point_at(float(obstacle["s"]), lateral)


func shortcut_local(pos: Vector2) -> Vector2:
	var offset := pos - (shortcut["start"] as Vector2)
	return Vector2(offset.dot(shortcut["along"]), offset.dot(shortcut["across"]))


func clears_shortcut(pos: Vector2, clearance: float) -> bool:
	if shortcut.is_empty():
		return true
	var local := shortcut_local(pos)
	var nearest := Vector2(clampf(local.x, 0.0, float(shortcut["length"])), 0.0)
	return local.distance_to(nearest) >= float(shortcut["half"]) + clearance


func _build_room_features() -> void:
	for point: int in room["items"]:
		var s := s_of(point)
		gate_s.append(s)
		for lat: float in ITEM_LATS:
			bubbles.append({"s": s, "lat": lat, "pos": point_at(s, lat), "respawn_t": 0.0})
	var row := 0
	for point: int in room["pearls"]:
		var lat := -74.0 if row % 2 == 0 else 74.0
		for index in range(4):
			var s := s_of(point, float(index) * 45.0)
			pearls.append({"s": s, "lat": lat, "pos": point_at(s, lat), "respawn_t": 0.0})
		row += 1
	for zone_index in range(room["zones"].size()):
		var zone: Dictionary = room["zones"][zone_index]
		for prop: Dictionary in zone["props"]:
			var s := length * float(prop["at"])
			var clearance := RAIL + float(prop["w"]) * 0.5 + 14.0
			var lateral := float(prop["lat"])
			var pos := point_at(s, lateral)
			# A fixture may move outward or across the lane to clear an adjacent
			# switchback. Its authored section and station never change.
			var found := false
			for side: float in [1.0, -1.0]:
				for offset: float in [0.0, 70.0, 150.0, 240.0, 340.0, 460.0]:
					pos = point_at(s, (lateral + signf(lateral) * offset) * side)
					if _clear_of_road(pos, clearance):
						found = true
						break
				if found:
					break
			if not _clear_of_road(pos, clearance):
				push_warning("Room fixture has no clear placement: " + String(prop["id"]))
				continue
			var entry := prop.duplicate()
			entry["s"] = s
			entry["pos"] = pos
			entry["zone"] = zone_index
			landmarks.append(entry)
	landmarks.append({"id": "course_finish_arch", "path": TRACK_ROOT + "billboards/pearl_start_arch.png",
		"s": 0.0, "pos": point_at(0.0), "w": 330.0, "h": 250.0, "spans": true})
	landmarks.append({"id": "course_finish_banner", "path": "res://assets/kart/finish_banner.png",
		"s": 0.0, "pos": point_at(0.0), "w": 300.0, "h": 56.0, "lift": 177.0, "spans": true})
	_build_turn_markers()


func _build_turn_markers() -> void:
	var previous := -1000.0
	var count := 0
	for index in range(_control_points.size()):
		var s := s_of(index)
		var bend := curvature_at(s)
		if absf(bend) < 0.002 or s - previous < 440.0:
			continue
		var at := wrap_s(s - 75.0)
		var pos := point_at(at, -signf(bend) * 225.0)
		if not _clear_of_road(pos, 200.0):
			continue
		landmarks.append({"id": "turn_marker", "path": "res://assets/racer/context_v2/turn_marker.png",
			"crop": Rect2(8, 134, 1008, 755), "s": at, "pos": pos, "w": 110.0,
			"flip_h": bend < 0.0})
		previous = s
		count += 1
		if count >= 10:
			break


func _clear_of_road(pos: Vector2, clearance: float) -> bool:
	if not clears_shortcut(pos, maxf(0.0, clearance - RAIL)):
		return false
	for sample in range(0, SAMPLES, 3):
		if pos.distance_squared_to(center[sample]) < clearance * clearance:
			return false
	return true


func wrap_s(s: float) -> float:
	return fposmod(s, length)


func _sample_index(s: float) -> int:
	return int(floor(wrap_s(s) / length * float(SAMPLES))) % SAMPLES


func point_at(s: float, lateral: float = 0.0) -> Vector2:
	var exact := wrap_s(s) / length * float(SAMPLES)
	var index := int(floorf(exact)) % SAMPLES
	var t := exact - floorf(exact)
	var p := center[index].lerp(center[(index + 1) % SAMPLES], t)
	var tan := tangents[index].lerp(tangents[(index + 1) % SAMPLES], t).normalized()
	return p + Vector2(-tan.y, tan.x) * lateral


func tangent_at(s: float) -> Vector2:
	var exact := wrap_s(s) / length * float(SAMPLES)
	var index := int(floorf(exact)) % SAMPLES
	var t := exact - floorf(exact)
	return tangents[index].lerp(tangents[(index + 1) % SAMPLES], t).normalized()


## Heading convention: 0 faces up the map (-y); positive turns clockwise.
func heading_at(s: float) -> float:
	var t := tangent_at(s)
	return atan2(t.x, -t.y)


func curvature_at(s: float) -> float:
	return curvatures[_sample_index(s)]


## The line a confident racer takes: toward the inside of the next bend.
func racing_lat(s: float) -> float:
	var ahead := 0.0
	for offset: float in [60.0, 140.0, 220.0]:
		ahead += curvature_at(s + offset)
	ahead /= 3.0
	if absf(ahead) < 0.0012:
		return 0.0
	# Positive curvature turns right, and right of travel is positive lateral.
	return clampf(signf(ahead) * minf(1.0, absf(ahead) / 0.004), -1.0, 1.0) \
		* ROAD_HALF * 0.48


## Nearest centre-line position to `p`, searched only within `window` world
## units of `hint_s` so a kart can never jump across to another part of the
## course. Returns Vector2(s, lateral).
func project(p: Vector2, hint_s: float, window: float = 420.0) -> Vector2:
	var spacing := length / float(SAMPLES)
	var span := int(ceil(window / spacing))
	var base := _sample_index(hint_s)
	var best := base
	var best_d := INF
	for offset in range(-span, span + 1):
		var index := (base + offset + SAMPLES) % SAMPLES
		var d := center[index].distance_squared_to(p)
		if d < best_d:
			best_d = d
			best = index
	# Refine on the two neighbouring segments.
	var best_s := cumulative[best]
	var best_lat := 0.0
	var best_err := INF
	for neighbour: int in [best - 1, best]:
		var i0 := (neighbour + SAMPLES) % SAMPLES
		var i1 := (i0 + 1) % SAMPLES
		var a := center[i0]
		var b := center[i1]
		var ab := b - a
		var t := clampf((p - a).dot(ab) / maxf(0.0001, ab.length_squared()), 0.0, 1.0)
		var q := a + ab * t
		var err := q.distance_squared_to(p)
		if err < best_err:
			best_err = err
			best_s = cumulative[i0] + t * spacing
			var tan := ab.normalized()
			best_lat = (p - q).dot(Vector2(-tan.y, tan.x))
	return Vector2(wrap_s(best_s), best_lat)


func terrain_at_lat(lateral: float) -> int:
	var lateral_abs := absf(lateral)
	if lateral_abs <= ROAD_HALF:
		return Terrain.ROAD
	if lateral_abs <= RAIL:
		return Terrain.APRON
	return Terrain.RAIL


func checkpoint_of(s: float) -> int:
	return clampi(int(floor(wrap_s(s) / length * float(CHECKPOINTS))), 0, CHECKPOINTS - 1)


## Road-distance data for the shared boundary markings, including painted Canal.
## Room courses use a 512-square field with every centre sample; the original
## Canal retains its cached 128-square field. Values encode distance divided
## by FIELD_FAR. Bilinear filtering smooths the curb and shoulder contours.
func floor_field() -> ImageTexture:
	var is_room := not room.is_empty()
	if is_room and _room_fields.has(id):
		return _room_fields[id] as ImageTexture
	if not is_room and _field_cache != null:
		return _field_cache
	var resolution := 512 if is_room else FIELD_SIZE
	var cell := world_size / float(resolution)
	var distances := PackedFloat32Array()
	distances.resize(resolution * resolution)
	distances.fill(FIELD_FAR)
	var phases := PackedFloat32Array()
	phases.resize(resolution * resolution)
	var reach := int(ceil(FIELD_REACH / cell))
	var stride := 1 if is_room else 3
	for sample in range(0, SAMPLES, stride):
		var p := center[sample]
		var cx := int(p.x / cell)
		var cy := int(p.y / cell)
		for gy in range(maxi(0, cy - reach), mini(resolution, cy + reach + 1)):
			var wy := (float(gy) + 0.5) * cell - p.y
			for gx in range(maxi(0, cx - reach), mini(resolution, cx + reach + 1)):
				var wx := (float(gx) + 0.5) * cell - p.x
				var d := sqrt(wx * wx + wy * wy)
				var key := gy * resolution + gx
				if d < distances[key]:
					distances[key] = d
					phases[key] = TAU * float(sample) / float(SAMPLES)
	var bytes := PackedByteArray()
	var channels := 3 if is_room else 1
	bytes.resize(resolution * resolution * channels)
	for key in range(resolution * resolution):
		bytes[key * channels] = clampi(roundi(distances[key] / FIELD_FAR * 255.0), 0, 255)
		if is_room:
			bytes[key * channels + 1] = roundi((cos(phases[key]) * 0.5 + 0.5) * 255.0)
			bytes[key * channels + 2] = roundi((sin(phases[key]) * 0.5 + 0.5) * 255.0)
	var format := Image.FORMAT_RGB8 if is_room else Image.FORMAT_L8
	var image := Image.create_from_data(resolution, resolution, false, format, bytes)
	var texture := ImageTexture.create_from_image(image)
	if is_room:
		_room_fields[id] = texture
	else:
		_field_cache = texture
	return texture
