class_name OperaVenueNavigation
extends RefCounted
## A small, deterministic walk graph: balcony lanes, stair treads and lift
## landings are the only cross-floor edges. Foyer visibility edges avoid
## furniture with clearance for Roshan's feet. No physics or navmesh bake.

const FLOOR_Y: Array[float] = [512.0, 389.0, 270.0, 151.0]
const LIVE_ORDER: Array[int] = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17]
const FOYER := Rect2(170.0, 512.0, 980.0, 194.0)
const OBSTACLES: Array[Rect2] = [
	Rect2(162.0, 545.0, 206.0, 105.0),
	Rect2(583.0, 550.0, 134.0, 118.0),
	Rect2(917.0, 545.0, 195.0, 105.0),
]
const CLEARANCE := 12.0
const LEFT_LIFT := 263.0
const RIGHT_LIFT := 1010.0
var graph := AStar2D.new()
var node_floors: Dictionary = {}
var unlocked_floor := 0


static func stage_for_mask(mask: int) -> int:
	# Count the specific first four/eight/twelve, never repeated wins, retired
	# bits, or out-of-order stars from an older save.
	for floor_number in range(1, 4):
		for ordinal in range(floor_number * 4):
			if (mask & (1 << LIVE_ORDER[ordinal])) == 0:
				return floor_number - 1
	return 3


static func floor_for_act(act_index: int) -> int:
	var ordinal := LIVE_ORDER.find(act_index)
	return ordinal / 4 if ordinal >= 0 else -1


func rebuild(max_floor: int) -> void:
	unlocked_floor = clampi(max_floor, 0, 3)
	graph.clear()
	node_floors.clear()
	for floor_number in range(unlocked_floor + 1):
		var previous := -1
		for x: float in [263.0, 356.0, 452.0, 576.0, 698.0, 820.0, 918.0, 1010.0]:
			var id := _add(Vector2(x, FLOOR_Y[floor_number]), floor_number)
			if previous >= 0:
				graph.connect_points(previous, id)
			previous = id
	# Inflate furniture before testing sight lines, including their corners.
	for obstacle: Rect2 in OBSTACLES:
		var rect := obstacle.grow(CLEARANCE + 2.0)
		for corner: Vector2 in [rect.position, Vector2(rect.end.x, rect.position.y),
				rect.end, Vector2(rect.position.x, rect.end.y)]:
			if FOYER.has_point(corner):
				_add(corner, 0)
	for corner: Vector2 in [Vector2(400, 700), Vector2(880, 700), Vector2(650, 700)]:
		_add(corner, 0)
	var ids := graph.get_point_ids()
	for a: int in ids:
		if int(node_floors[a]) != 0:
			continue
		for b: int in ids:
			if b > a and int(node_floors[b]) == 0 \
					and clear_segment(graph.get_point_position(a), graph.get_point_position(b)):
				graph.connect_points(a, b)
	if unlocked_floor >= 1:
		_stair(Vector2(263, 512), Vector2(356, 389))
		_stair(Vector2(1010, 512), Vector2(918, 389))
	if unlocked_floor >= 2:
		graph.connect_points(_at(Vector2(LEFT_LIFT, FLOOR_Y[1])),
			_at(Vector2(LEFT_LIFT, FLOOR_Y[2])))
	if unlocked_floor >= 3:
		graph.connect_points(_at(Vector2(RIGHT_LIFT, FLOOR_Y[2])),
			_at(Vector2(RIGHT_LIFT, FLOOR_Y[3])))


func project(point: Vector2, floor_number: int) -> Vector2:
	if floor_number > 0:
		return Vector2(clampf(point.x, LEFT_LIFT, RIGHT_LIFT), FLOOR_Y[floor_number])
	var result := Vector2(clampf(point.x, FOYER.position.x, FOYER.end.x),
		clampf(point.y, FOYER.position.y, FOYER.end.y))
	for obstacle: Rect2 in OBSTACLES:
		var rect := obstacle.grow(CLEARANCE + 1.0)
		if not rect.has_point(result):
			continue
		var options: Array[Vector2] = [Vector2(rect.position.x, result.y),
			Vector2(rect.end.x, result.y), Vector2(result.x, rect.position.y),
			Vector2(result.x, rect.end.y)]
		var best := INF
		for option: Vector2 in options:
			if FOYER.has_point(option) and option.distance_squared_to(result) < best:
				best = option.distance_squared_to(result)
				point = option
		result = point
	return result


func floor_at(point: Vector2) -> int:
	for floor_number in range(3, 0, -1):
		if point.y < (FLOOR_Y[floor_number] + FLOOR_Y[floor_number - 1]) * 0.5:
			return floor_number
	return 0


func route(start: Vector2, start_floor: int, target: Vector2,
		target_floor: int) -> PackedVector2Array:
	if target_floor < 0 or target_floor > unlocked_floor:
		return PackedVector2Array()
	var nearest := graph.get_closest_point(start)
	var in_transit := int(node_floors[nearest]) == -1 \
		and graph.get_point_position(nearest).distance_to(start) < 0.1
	var from := start if in_transit else project(start, start_floor)
	var to := project(target, target_floor)
	var start_id := _add(from, -1) if in_transit else _temporary(from, start_floor)
	if in_transit:
		graph.connect_points(start_id, nearest)
	var end_id := _temporary(to, target_floor)
	var result := graph.get_point_path(start_id, end_id)
	graph.remove_point(start_id)
	graph.remove_point(end_id)
	node_floors.erase(start_id)
	node_floors.erase(end_id)
	return result


func clear_segment(a: Vector2, b: Vector2) -> bool:
	for obstacle: Rect2 in OBSTACLES:
		var rect := obstacle.grow(CLEARANCE)
		if rect.has_point(a) or rect.has_point(b):
			return false
		var corners := PackedVector2Array([rect.position,
			Vector2(rect.end.x, rect.position.y), rect.end,
			Vector2(rect.position.x, rect.end.y)])
		for i in range(4):
			if Geometry2D.segment_intersects_segment(a, b, corners[i], corners[(i + 1) % 4]) != null:
				return false
	return true


func _temporary(point: Vector2, floor_number: int) -> int:
	var ids := graph.get_point_ids()
	var id := _add(point, floor_number)
	for other: int in ids:
		if int(node_floors[other]) == floor_number \
				and (floor_number > 0 or clear_segment(point, graph.get_point_position(other))):
			graph.connect_points(id, other)
	return id


func _add(point: Vector2, floor_number: int) -> int:
	var id := graph.get_available_point_id()
	graph.add_point(id, point)
	node_floors[id] = floor_number
	return id


func _at(point: Vector2) -> int:
	return graph.get_closest_point(point)


func _stair(bottom: Vector2, top: Vector2) -> void:
	var previous := _at(bottom)
	var end := _at(top)
	for step in range(1, 5):
		# Transit nodes are excluded from arbitrary same-floor shortcuts.
		var id := _add(bottom.lerp(top, float(step) / 5.0), -1)
		graph.connect_points(previous, id)
		previous = id
	graph.connect_points(previous, end)
