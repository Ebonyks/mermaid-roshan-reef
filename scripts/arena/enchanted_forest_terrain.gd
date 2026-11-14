extends Node2D
## The same polygons define the shore, the safe floor, and the route on the map.

const GROUND := preload("res://assets/shaders/sky_lagoon_grove_ground.gdshader")
const GRASS := preload("res://assets/terrain/up_grass_col.jpg")
const WATER := preload("res://assets/flats/sky_lagoon/day_one_demo/painted_water_v5.png")
const STONE := preload("res://assets/terrain/up_flagstone_col.jpg")
const LAWN := preload("res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png")

const STOPS: Array[Vector2] = [
	Vector2(660, 1190), Vector2(3350, 1200), Vector2(5960, 1180),
	Vector2(1500, 1115), Vector2(2390, 1235), Vector2(4220, 1135), Vector2(5080, 1260),
]
const RADII: Array[Vector2] = [
	Vector2(440, 303), Vector2(455, 321), Vector2(473, 325),
	Vector2(403, 294), Vector2(405, 312), Vector2(390, 286), Vector2(416, 318),
]
const LINKS: Array[Vector2i] = [
	Vector2i(0, 3), Vector2i(3, 4), Vector2i(4, 1), Vector2i(1, 5),
	Vector2i(5, 6), Vector2i(6, 2),
]
const BENDS: Array[Vector2] = [
	Vector2(1060, 1135), Vector2(1965, 1180), Vector2(2850, 1198),
	Vector2(3780, 1150), Vector2(4650, 1200), Vector2(5520, 1245),
]
const BRIDGE := BENDS[2]
const BRIDGE_APPROACH := BRIDGE + Vector2(-292, 20)
const STREAM_HALF := 66.0
const LILY_BASIN := STOPS[4] + Vector2(-48, 141)
const MOAT_CENTER := STOPS[2] + Vector2(8, -208)
const MOAT_OUTER := Vector2(324, 201)
const MOAT_ISLAND := Vector2(232, 112)
const CASTLE_GATE := STOPS[2] + Vector2(0, -111)
const CASTLE_BRIDGE_HALF := 48.0
const FARM_BEDS: Array[Rect2] = [
	Rect2(STOPS[1] + Vector2(-279, -243), Vector2(558, 127)),
	Rect2(STOPS[1] + Vector2(-238, 76), Vector2(476, 99)),
]
const V1_PLAYABLE_AREA := 657846.0
const FUTURE_GATES: Array[Vector2] = [Vector2(5186, 1023), Vector2(4290, 1355)]
const FUTURE_DIRECTIONS: Array[Vector2] = [Vector2(0.29, -0.957), Vector2(0.31, 0.951)]
const GATE_HALF_WIDTH := 55.0
const FUTURE_TRACE_START: Array[Vector2] = [Vector2(5027, 1253), Vector2(4159, 1143)]
const CABIN_TRAIL_JOIN := Vector2(5256.0, 827.0)
const FIRWOOD_TRAIL_END := Vector2(4393.0, 1557.0)
const QUERY_START := 100
const QUERY_END := 101

var outline := PackedVector2Array()
var safe_outline := PackedVector2Array()
var water_inlets: Array[PackedVector2Array] = []
var _floor_exclusions: Array[PackedVector2Array] = []
var graph := AStar2D.new()
var bridge_open := false
var _weather_materials: Array[ShaderMaterial] = []
var _trail_samples: Array[PackedVector2Array] = []
var _water_marks: Node2D
var _wind_time := 0.0


func _ready() -> void:
	outline = _footprint()
	water_inlets.append(_oval(LILY_BASIN, Vector2(138, 65), 4))
	var inset: Array[PackedVector2Array] = Geometry2D.offset_polygon(outline, -18.0)
	safe_outline = inset[0]
	for inlet: PackedVector2Array in water_inlets:
		_floor_exclusions.append(Geometry2D.offset_polygon(inlet, 18.0)[0])
	for bed: Rect2 in FARM_BEDS:
		var floor: Rect2 = _bed_floor(bed)
		_floor_exclusions.append(PackedVector2Array([
			floor.position, Vector2(floor.end.x, floor.position.y),
			floor.end, Vector2(floor.position.x, floor.end.y),
		]))
	for index: int in range(STOPS.size()):
		graph.add_point(index, STOPS[index])
	for index: int in range(LINKS.size()):
		var link: Vector2i = LINKS[index]
		var bend_id: int = STOPS.size() + index
		graph.add_point(bend_id, BENDS[index])
		graph.connect_points(link.x, bend_id)
		graph.connect_points(bend_id, link.y)
	var shelf: PackedVector2Array = _shelf()
	_surface(shelf, GRASS, 1, -12, Color.WHITE)
	_ridge_lip(shelf)
	_bank(LILY_BASIN, Vector2(153, 78), 4, 0, Color("#aaa889"))
	_water_pool(LILY_BASIN, Vector2(138, 65), 4, 1)
	_trail()
	_future_trails()
	_link_farm_aisles()
	var spring := Vector2(_stream_center(955.0), 952.0)
	var spring_radius := Vector2(77, 38)
	var creek_bank: PackedVector2Array = _merge(_stream_shape(81.0), _oval(spring, Vector2(97, 52), 8))
	var bank: Polygon2D = _surface(creek_bank, STONE, 8, 4, Color("#b6b197"))
	var bank_paint: ShaderMaterial = bank.material as ShaderMaterial
	bank_paint.set_shader_parameter("water_footprint", Vector4(BRIDGE.x, BRIDGE.y, STREAM_HALF, -1))
	bank_paint.set_shader_parameter("spring_footprint", Vector4(spring.x, spring.y, spring_radius.x, spring_radius.y))
	var creek: PackedVector2Array = _merge(_stream_shape(STREAM_HALF), _oval(spring, spring_radius, 8))
	var stream: Polygon2D = _surface(creek, WATER, 0, 5, Color.WHITE)
	var stream_paint: ShaderMaterial = stream.material as ShaderMaterial
	stream_paint.set_shader_parameter("water_footprint", Vector4(BRIDGE.x, BRIDGE.y, STREAM_HALF, -1))
	stream_paint.set_shader_parameter("spring_footprint", Vector4(spring.x, spring.y, spring_radius.x, spring_radius.y))
	_water_marks = Node2D.new()
	_water_marks.name = "MovingSpringAndStreamGlints"
	_water_marks.z_index = 6
	_water_marks.draw.connect(_draw_water_marks)
	add_child(_water_marks)
	_paved_place(STOPS[0] + Vector2(-111, -25), Vector2(273, 116), 0)
	_paved_place(STOPS[2] + Vector2(33, 51), Vector2(248, 103), 2)
	_build_moat()


func _water_pool(center: Vector2, radius: Vector2, seed: int, layer: int) -> void:
	var pool: Polygon2D = _surface(_oval(center, radius, seed), WATER, 0, layer, Color.WHITE)
	var paint: ShaderMaterial = pool.material as ShaderMaterial
	paint.set_shader_parameter("water_footprint", Vector4(center.x, center.y, radius.x, radius.y))
	paint.set_shader_parameter("bank_seed", float(seed))


func _build_moat() -> void:
	var bank_radius: Vector2 = MOAT_OUTER + Vector2(43, 32)
	_bank(MOAT_CENTER, bank_radius, 2, 4, Color("#b0b18f"))
	_water_pool(MOAT_CENTER, MOAT_OUTER, 2, 5)
	_surface(_oval(MOAT_CENTER + Vector2(0, 11), MOAT_ISLAND + Vector2(12, 6), 2),
		STONE, 2, 6, Color("#aaa891"))
	_surface(_oval(MOAT_CENTER, MOAT_ISLAND, 2), GRASS, 1, 7, Color("#a9b69a"))


func plantable(point: Vector2) -> bool:
	if not contains(point):
		return false
	return point.y < 928.0 or absf(point.x - _stream_center(point.y)) > STREAM_HALF + 17.0


func moat_water_at(point: Vector2) -> bool:
	var at: Vector2 = point - MOAT_CENTER
	if absf(point.x - STOPS[2].x) < CASTLE_BRIDGE_HALF and at.y > 75.0:
		return false
	return ((at / MOAT_OUTER).length_squared() < 1.05
		and (at / MOAT_ISLAND).length_squared() > 0.86)


func _paved_place(center: Vector2, radius: Vector2, variant: int) -> void:
	var paving: Polygon2D = _surface(_oval(center, radius, variant),
		STONE, 5, 4, Color(1.0, 0.98, 0.96, 0.84))
	var material: ShaderMaterial = paving.material as ShaderMaterial
	material.set_shader_parameter("patch_world", Vector4(center.x, center.y, radius.x, radius.y))


func _surface(vertices: PackedVector2Array, tex: Texture2D, kind: int, depth: int, tint: Color) -> Polygon2D:
	var mesh := Polygon2D.new()
	mesh.polygon = vertices
	mesh.z_index = depth
	var mat := ShaderMaterial.new()
	mat.shader = GROUND
	mat.set_shader_parameter("surface_texture", tex)
	mat.set_shader_parameter("paint_detail", LAWN)
	mat.set_shader_parameter("surface_kind", kind)
	mat.set_shader_parameter("surface_tint", tint)
	mesh.material = mat
	add_child(mesh)
	if kind in [0, 1]:
		_weather_materials.append(mat)
	return mesh


func _bank(center: Vector2, radius: Vector2, seed: int, depth: int, tint: Color) -> void:
	var bank: Polygon2D = _surface(_oval(center, radius, seed), STONE, 6, depth, tint)
	var paint: ShaderMaterial = bank.material as ShaderMaterial
	paint.set_shader_parameter("patch_world", Vector4(center.x, center.y, radius.x, radius.y))


func _trail() -> void:
	var curve := Curve2D.new()
	curve.bake_interval = 21.0
	curve.add_point(STOPS[0] - Vector2(100, 0))
	for index: int in range(LINKS.size()):
		var link: Vector2i = LINKS[index]
		var tangent: Vector2 = (STOPS[link.y] - STOPS[link.x]).normalized() * 100.0
		curve.add_point(BENDS[index], -tangent, tangent)
		curve.add_point(STOPS[link.y], Vector2(-86, 0), Vector2(86, 0))
	curve.add_point(STOPS[2] + Vector2(100, -5))
	_paint_trail(curve.get_baked_points(), 54.0, -1)



func _future_trails() -> void:
	var traces: Array[PackedVector2Array] = [
		PackedVector2Array([FUTURE_TRACE_START[0], Vector2(5092, 1189), Vector2(5146, 1108),
			FUTURE_GATES[0], Vector2(5213, 933), Vector2(5224, 866),
			CABIN_TRAIL_JOIN, CABIN_TRAIL_JOIN + Vector2(35.0, -19.0)]),
		PackedVector2Array([FUTURE_TRACE_START[1], Vector2(4201, 1205), Vector2(4263, 1282),
			FUTURE_GATES[1], Vector2(4325, 1424), Vector2(4360, 1490), FIRWOOD_TRAIL_END]),
	]
	for branch: int in range(traces.size()):
		var trace: PackedVector2Array = traces[branch]
		var curve := Curve2D.new()
		curve.bake_interval = 14.0
		for index: int in range(trace.size()):
			var tangent: Vector2 = (trace[mini(index + 1, trace.size() - 1)] - trace[maxi(0, index - 1)]) * 0.18
			curve.add_point(trace[index], -tangent, tangent)
		_paint_trail(curve.get_baked_points(), 37.0, branch)


static func future_gate_at(point: Vector2, reach := 0.0) -> int:
	for index: int in range(FUTURE_GATES.size()):
		var delta: Vector2 = point - FUTURE_GATES[index]
		var direction: Vector2 = FUTURE_DIRECTIONS[index]
		if delta.dot(direction) >= -reach and delta.dot(direction) <= 340.0 \
				and absf(delta.cross(direction)) <= GATE_HALF_WIDTH + 14.0:
			return index
	return -1


static func future_approach(point: Vector2, index: int) -> Vector2:
	var direction: Vector2 = FUTURE_DIRECTIONS[index]
	var sideways := Vector2(-direction.y, direction.x)
	var along: float = clampf((point - FUTURE_GATES[index]).dot(sideways), -36.0, 36.0)
	return FUTURE_GATES[index] + sideways * along - direction * 16.0


func _paint_trail(points: PackedVector2Array, half_width: float, branch: int) -> void:
	_trail_samples.append(points)
	var vertices := PackedVector2Array()
	var fades := PackedColorArray()
	var quads: Array[PackedInt32Array] = []
	for item: int in range(points.size()):
		var step: Vector2 = points[mini(item + 1, points.size() - 1)] - points[maxi(item - 1, 0)]
		var normal := Vector2(-step.y, step.x).normalized()
		var width: float = half_width + sin(item * 0.23) * 3.0 + sin(item * 0.81) * 1.9
		if branch == -1:
			width *= lerpf(0.76, 1.0, smoothstep(1020.0, 1840.0, points[item].x))
		elif branch == 0:
			width *= lerpf(0.51, 1.0, smoothstep(CABIN_TRAIL_JOIN.y, CABIN_TRAIL_JOIN.y + 170.0, points[item].y))
		elif branch == 1:
			width *= lerpf(1.0, 0.68, smoothstep(1355.0, FIRWOOD_TRAIL_END.y, points[item].y))
		var remaining: float = float(points.size() - item - 1)
		var alpha: float = smoothstep(0.0, 3.0 if branch < 0 else 1.8, remaining)
		if branch >= 0:
			alpha *= smoothstep(0.0, 3.0, float(item))
		for lane: float in [-1.0, -0.75, 0.75, 1.0]:
			vertices.append(points[item] + normal * width * lane)
			fades.append(Color(1, 1, 1, 0.0 if absf(lane) == 1.0 else alpha))
		if item > 0:
			for band: int in range(3):
				var first: int = (item - 1) * 4 + band
				quads.append(PackedInt32Array([first, first + 1, first + 5, first + 4]))
	var trail: Polygon2D = _surface(vertices, STONE, 7, 3, Color("#f6f0e1"))
	trail.polygons = quads
	trail.vertex_colors = fades
	var paint: ShaderMaterial = trail.material as ShaderMaterial
	paint.set_shader_parameter("valley_main_trail", branch == -1)
	if branch >= 0:
		paint.set_shader_parameter("trail_dirt_range",
			Vector2(CABIN_TRAIL_JOIN.y + 8.0, CABIN_TRAIL_JOIN.y + 163.0) if branch == 0
			else Vector2(FIRWOOD_TRAIL_END.y - 24.0, FIRWOOD_TRAIL_END.y - 185.0))
		if branch == 0:
			paint.set_shader_parameter("trail_crest_y", CABIN_TRAIL_JOIN.y)



func clear_of_trail(point: Vector2) -> bool:
	for index: int in range(_trail_samples.size()):
		if _near_trail(point, index, 59.0 if index == 0 else 43.0):
			return false
	return true


func _near_trail(point: Vector2, index: int, width: float) -> bool:
	for sample: Vector2 in _trail_samples[index]:
		if sample.distance_squared_to(point) < width * width:
			return true
	return false


func _ridge_lip(shelf: PackedVector2Array) -> void:
	var outline := PackedVector2Array()
	var stations: int = shelf.size() - 2
	for index: int in range(stations):
		outline.append(shelf[index])
	for index: int in range(stations - 1, -1, -1):
		var crest: Vector2 = shelf[index]
		var thickness: float = 10.0 + 5.0 * sin(crest.x * 0.014) + 3.0 * sin(crest.x * 0.035)
		outline.append(crest + Vector2(0.0, thickness))
	var lip: Polygon2D = _surface(outline, GRASS, 1, -11, Color("#becba9"))
	lip.name = "PaintedRidgeLip"
	lip.antialiased = true


func set_wind_time(time: float) -> void:
	_wind_time = time
	for material: ShaderMaterial in _weather_materials:
		material.set_shader_parameter("water_time", time)
	_water_marks.queue_redraw()


func _draw_water_marks() -> void:
	for index: int in range(10):
		var phase: float = fposmod(_wind_time * (0.17 + 0.011 * (index % 3)) + index * 0.23, 1.0)
		var y: float = 991.0 + phase * 650.0
		if absf(y - BRIDGE.y) < 47.0:
			continue
		var x: float = _stream_center(y) + sin(index * 2.4) * 36.0
		var length: float = 17.0 + 10.0 * sin(index * 1.9)
		var ink := Color(0.83, 0.97, 0.88, sin(phase * PI) * 0.43)
		_water_marks.draw_polyline(PackedVector2Array([
			Vector2(x - length * 0.45, y - 1.0), Vector2(x, y),
			Vector2(x + length * 0.55, y - 1.7)]), ink, 2.0, true)
	var spring := Vector2(_stream_center(955.0), 952.0)
	for index: int in range(3):
		var t: float = fposmod(_wind_time * 0.41 + index / 3.0, 1.0)
		for stroke: int in range(2):
			var points := PackedVector2Array()
			for step: int in range(12):
				var angle: float = float(step) / 11.0 * 2.4 + stroke * PI + 0.23 * index
				var ripple: Vector2 = Vector2.from_angle(angle) * Vector2(8.0 + 55.0 * t, 4.0 + 23.0 * t)
				points.append(spring + ripple * (1.0 + 0.045 * sin(angle * 3.0)))
			_water_marks.draw_polyline(points, Color(0.77, 0.94, 0.87, sin(t * PI) * 0.30), 1.9, true)


func walk_area() -> float:
	var area: float = _area(safe_outline)
	for inlet: PackedVector2Array in _floor_exclusions:
		area -= _area(inlet)
	for creek: PackedVector2Array in Geometry2D.intersect_polygons(safe_outline, _stream_shape(STREAM_HALF + 1.0, true)):
		area -= _area(creek)
		if bridge_open:
			var deck := PackedVector2Array([BRIDGE + Vector2(-122, -41), BRIDGE + Vector2(122, -41),
				BRIDGE + Vector2(122, 41), BRIDGE + Vector2(-122, 41)])
			for contact: PackedVector2Array in Geometry2D.intersect_polygons(creek, deck):
				area += _area(contact)
	return area


func _area(shape: PackedVector2Array) -> float:
	var twice := 0.0
	for index: int in range(shape.size()):
		twice += shape[index].cross(shape[(index + 1) % shape.size()])
	return absf(twice) * 0.5


func safe_point(point: Vector2, previous := Vector2.INF) -> Vector2:
	var gate: int = future_gate_at(point)
	if gate >= 0:
		point = future_approach(point, gate)
	if moat_water_at(point):
		var at: Vector2 = point - MOAT_CENTER
		var inner: bool = previous != Vector2.INF and ((previous - MOAT_CENTER) / MOAT_ISLAND).length() < 1.0
		var edge: Vector2 = MOAT_ISLAND * 0.88 if inner else MOAT_OUTER * 1.05
		point = MOAT_CENTER + (at / edge).normalized() * edge
	var shore: float = _stream_center(point.y)
	var west: bool = point.x < shore
	var crossing: bool = previous != Vector2.INF and (previous.x < _stream_center(previous.y)) != west
	if not bridge_open and crossing:
		west = previous.x < _stream_center(previous.y)
		point.x = shore + (-1.0 if west else 1.0) * (STREAM_HALF + 5.0)
	elif _water_at(point):
		point.x = shore + (-1.0 if west else 1.0) * (STREAM_HALF + 5.0)
	if contains(point):
		return point
	for inlet: PackedVector2Array in _floor_exclusions:
		if Geometry2D.is_point_in_polygon(point, inlet):
			return _dry_edge(point, inlet)
	var edge: Vector2 = _dry_edge(point, safe_outline)
	return previous if previous != Vector2.INF and not contains(edge) else edge


func water_surface_at(point: Vector2) -> bool:
	if moat_water_at(point) or (point.y >= 925.0 and _water_at(point)):
		return true
	for inlet: PackedVector2Array in water_inlets:
		if Geometry2D.is_point_in_polygon(point, inlet):
			return true
	return false


func _water_at(point: Vector2) -> bool:
	return (absf(point.x - _stream_center(point.y)) < STREAM_HALF + 1.0
		and (not bridge_open or absf(point.y - BRIDGE.y) > 41.0))


func _stream_center(y: float) -> float:
	var distance: float = y - BRIDGE.y
	return BRIDGE.x + sin(distance * 0.0061) * 45.0 + sin(distance * 0.011) * 14.0


func _stream_shape(half_width: float, collision := false) -> PackedVector2Array:
	var bank := PackedVector2Array()
	var opposite := PackedVector2Array()
	for index: int in range(48):
		var y: float = (824.0 if collision else 944.0) + index * 31.0
		var x: float = _stream_center(y)
		var width: float = half_width
		if not collision:
			width *= lerpf(0.42, 1.0, smoothstep(944.0, 1050.0, y))
			width += sin(index * 1.4) * 2.4
		bank.append(Vector2(x - width, y))
		opposite.append(Vector2(x + width, y))
	opposite.reverse()
	bank.append_array(opposite)
	return bank


func _dry_edge(point: Vector2, shape: PackedVector2Array) -> Vector2:
	var nearest := Vector2.INF
	for index: int in range(shape.size()):
		var a: Vector2 = shape[index]
		var b: Vector2 = shape[(index + 1) % shape.size()]
		var edge: Vector2 = Geometry2D.get_closest_point_to_segment(point, a, b)
		if edge.distance_squared_to(point) < nearest.distance_squared_to(point):
			nearest = edge
	return nearest + (nearest - point).normalized() * 1.4


func contains(point: Vector2) -> bool:
	if future_gate_at(point) >= 0 or moat_water_at(point) or _water_at(point):
		return false
	if not Geometry2D.is_point_in_polygon(point, safe_outline):
		# Keep the painted main lane continuous through narrow seams in the inset.
		if _trail_samples.is_empty() or not _near_trail(point, 0, 42.0) \
				or not Geometry2D.is_point_in_polygon(point, outline):
			return false
	for inlet: PackedVector2Array in _floor_exclusions:
		if Geometry2D.is_point_in_polygon(point, inlet):
			return false
	return true



func _bed_floor(bed: Rect2) -> Rect2:
	return Rect2(bed.position + Vector2(11.0, 20.0), bed.size - Vector2(22.0, 15.0))


func _link_farm_aisles() -> void:
	for bed: Rect2 in FARM_BEDS:
		var perimeter: Rect2 = _bed_floor(bed).grow(8.0)
		for corner: Vector2 in [perimeter.position, Vector2(perimeter.end.x, perimeter.position.y),
				perimeter.end, Vector2(perimeter.position.x, perimeter.end.y)]:
			if not contains(corner):
				continue
			var neighbors: PackedInt64Array = graph.get_point_ids()
			var id: int = graph.get_available_point_id()
			graph.add_point(id, corner)
			for neighbor: int in neighbors:
				var at: Vector2 = graph.get_point_position(neighbor)
				if at.distance_squared_to(corner) < 640.0 * 640.0 and _clear_segment(at, corner):
					graph.connect_points(id, neighbor)


func route(start: Vector2, target: Vector2) -> PackedVector2Array:
	if _clear_segment(start, target):
		return PackedVector2Array([target])
	var nodes: PackedInt64Array = graph.get_point_ids()
	graph.add_point(QUERY_START, start)
	graph.add_point(QUERY_END, target)
	for index: int in nodes:
		var point: Vector2 = graph.get_point_position(index)
		if _clear_segment(start, point):
			graph.connect_points(QUERY_START, index)
		if _clear_segment(target, point):
			graph.connect_points(QUERY_END, index)
	var path: PackedVector2Array = graph.get_point_path(QUERY_START, QUERY_END)
	graph.remove_point(QUERY_START)
	graph.remove_point(QUERY_END)
	for index: int in range(1, path.size()):
		if not _clear_segment(path[index - 1], path[index]):
			return PackedVector2Array()
	if not path.is_empty():
		path.remove_at(0)
	return path


func _clear_segment(a: Vector2, b: Vector2) -> bool:
	if not contains(a) or not contains(b):
		return false
	for boundary: PackedVector2Array in _floor_exclusions:
		for index: int in range(boundary.size()):
			if Geometry2D.segment_intersects_segment(a, b, boundary[index], boundary[(index + 1) % boundary.size()]) != null:
				return false
	var checks: int = maxi(1, ceili(a.distance_to(b) / 22.0))
	for index: int in range(1, checks):
		if not contains(a.lerp(b, float(index) / checks)):
			return false
	return true


func _footprint() -> PackedVector2Array:
	var boundary: PackedVector2Array = _oval(STOPS[0], RADII[0], 0)
	for index: int in range(LINKS.size()):
		var link: Vector2i = LINKS[index]
		boundary = _merge(boundary, _track(_link_points(index), 141.0))
		boundary = _merge(boundary, _oval(STOPS[link.y], RADII[link.y], link.y))
	return boundary


func _link_points(index: int) -> PackedVector2Array:
	var link: Vector2i = LINKS[index]
	return PackedVector2Array([STOPS[link.x], BENDS[index], STOPS[link.y]])


func _merge(base: PackedVector2Array, addition: PackedVector2Array) -> PackedVector2Array:
	var merged: Array[PackedVector2Array] = Geometry2D.merge_polygons(base, addition)
	for candidate: PackedVector2Array in merged:
		if not Geometry2D.is_polygon_clockwise(candidate):
			return candidate
	return base


func _oval(center: Vector2, radii: Vector2, seed: int) -> PackedVector2Array:
	var shape := PackedVector2Array()
	for index: int in range(64):
		var angle: float = index * TAU / 64.0
		var rough: float = 1.0 + sin(angle * 5.0 + seed) * 0.045 + sin(angle * 11.0) * 0.019
		shape.append(center + Vector2.from_angle(angle) * radii * rough)
	return shape


func _track(points: PackedVector2Array, half_width: float) -> PackedVector2Array:
	var result: Array[PackedVector2Array] = Geometry2D.offset_polyline(points, half_width,
		Geometry2D.JOIN_ROUND, Geometry2D.END_ROUND)
	return result[0]


func _shelf() -> PackedVector2Array:
	var border := PackedVector2Array()
	for index: int in range(108):
		var x: float = -1100.0 + index * 82.0
		border.append(Vector2(x, ridge_height(x)))
	border.append(Vector2(border[-1].x, 2400.0))
	border.append(Vector2(border[0].x, 2400.0))
	return border


static func ridge_height(x: float) -> float:
	return 874.0 + sin(x * 0.0022) * 43.0 + sin(x * 0.0071) * 18.0 \
		- smoothstep(5190.0, 5750.0, x) * 112.0
