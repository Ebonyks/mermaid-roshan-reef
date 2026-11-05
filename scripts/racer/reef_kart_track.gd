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
var gate_s: Array[float] = []

static var _field_cache: ImageTexture = null


func _init() -> void:
	_build_centerline()
	_build_features()


func _catmull(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2
		+ (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)


func _build_centerline() -> void:
	# Dense pass, then resample uniformly by arc length so every sample is the
	# same distance apart and projection windows have a fixed meaning.
	var dense := PackedVector2Array()
	var count := POINTS.size()
	for index in range(count):
		var p0 := POINTS[(index - 1 + count) % count]
		var p1 := POINTS[index]
		var p2 := POINTS[(index + 1) % count]
		var p3 := POINTS[(index + 2) % count]
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
	return wrap_s(point_s[clampi(point, 0, POINTS.size() - 1)] + offset)


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


## INTERIM_PLACEHOLDER floor data until the painted course floor exists:
## a single-channel distance field, distance from the centre line divided by
## FIELD_FAR. The floor shader turns it into the painting's bands (aqua water
## lane with pale lines, tan stone curb, lilac wall, sand with coral and
## rocks). Built once per process (about 175k cheap steps: every third centre
## sample against nearby 16-unit cells) and never used when PAINTED_FLOOR
## exists. Bilinear filtering keeps the band edges smooth.
func floor_field() -> ImageTexture:
	if _field_cache != null:
		return _field_cache
	var cell := WORLD_SIZE / float(FIELD_SIZE)
	var distances := PackedFloat32Array()
	distances.resize(FIELD_SIZE * FIELD_SIZE)
	distances.fill(FIELD_FAR)
	var reach := int(ceil(FIELD_REACH / cell))
	for sample in range(0, SAMPLES, 3):
		var p := center[sample]
		var cx := int(p.x / cell)
		var cy := int(p.y / cell)
		for gy in range(maxi(0, cy - reach), mini(FIELD_SIZE, cy + reach + 1)):
			var wy := (float(gy) + 0.5) * cell - p.y
			for gx in range(maxi(0, cx - reach), mini(FIELD_SIZE, cx + reach + 1)):
				var wx := (float(gx) + 0.5) * cell - p.x
				var d := sqrt(wx * wx + wy * wy)
				var key := gy * FIELD_SIZE + gx
				if d < distances[key]:
					distances[key] = d
	var bytes := PackedByteArray()
	bytes.resize(FIELD_SIZE * FIELD_SIZE)
	for key in range(FIELD_SIZE * FIELD_SIZE):
		bytes[key] = clampi(int(round(distances[key] / FIELD_FAR * 255.0)), 0, 255)
	var image := Image.create_from_data(FIELD_SIZE, FIELD_SIZE, false, Image.FORMAT_L8, bytes)
	_field_cache = ImageTexture.create_from_image(image)
	return _field_cache
