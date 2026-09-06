class_name StageNavigation2D
extends RefCounted
## A stage's accessible space is an explicitly authored network of floor lanes.
## Furniture, walls, scenery and water are outside that network. Touches are
## projected onto lanes; routes traverse their junctions, never a direct chord.
## Rebuild only when stage geometry changes, not during movement.

const EPSILON: float = 0.05
var branches: Array[PackedVector2Array] = []

func configure(lanes: Array[PackedVector2Array]) -> void:
	branches.clear()
	for lane: PackedVector2Array in lanes:
		if lane.size() >= 2:
			branches.append(lane.duplicate())

func nearest_point(point: Vector2) -> Vector2:
	var best: Vector2 = point
	var distance: float = INF
	for lane: PackedVector2Array in branches:
		for index in range(1, lane.size()):
			var candidate: Vector2 = Geometry2D.get_closest_point_to_segment(
				point, lane[index - 1], lane[index])
			var candidate_distance: float = point.distance_squared_to(candidate)
			if candidate_distance < distance:
				distance = candidate_distance
				best = candidate
	return best

func contains_point(point: Vector2, tolerance: float = EPSILON) -> bool:
	return not branches.is_empty() and point.distance_to(nearest_point(point)) <= tolerance

func route(from: Vector2, target: Vector2) -> PackedVector2Array:
	if branches.is_empty():
		return PackedVector2Array()
	var start: Vector2 = nearest_point(from)
	var finish: Vector2 = nearest_point(target)
	var vertices: Array[Vector2] = [start, finish]
	var segments: Array[PackedVector2Array] = []
	for lane: PackedVector2Array in branches:
		for point: Vector2 in lane:
			_add_vertex(vertices, point)
		for index in range(1, lane.size()):
			if lane[index - 1].distance_to(lane[index]) > EPSILON:
				segments.append(PackedVector2Array([lane[index - 1], lane[index]]))
	# Authoring a crossing means a junction. A bridge that passes OVER another
	# path must use separate stage networks; overlapping planes cannot be guessed.
	for first in range(segments.size()):
		for second in range(first + 1, segments.size()):
			var intersection: Variant = Geometry2D.segment_intersects_segment(
				segments[first][0], segments[first][1], segments[second][0], segments[second][1])
			if intersection is Vector2:
				_add_vertex(vertices, intersection as Vector2)
	var graph := AStar2D.new()
	for index in range(vertices.size()):
		graph.add_point(index, vertices[index])
	for segment: PackedVector2Array in segments:
		var members: Array[int] = []
		for index in range(vertices.size()):
			var closest: Vector2 = Geometry2D.get_closest_point_to_segment(vertices[index], segment[0], segment[1])
			if closest.distance_to(vertices[index]) <= EPSILON:
				members.append(index)
		members.sort_custom(func(a: int, b: int) -> bool:
			return segment[0].distance_squared_to(vertices[a]) < segment[0].distance_squared_to(vertices[b]))
		for index in range(1, members.size()):
			graph.connect_points(members[index - 1], members[index])
	# Unreachable destinations fail closed. No teleport or through-scenery fallback.
	return graph.get_point_path(0, 1)

func _add_vertex(vertices: Array[Vector2], point: Vector2) -> void:
	for existing: Vector2 in vertices:
		if existing.distance_to(point) <= EPSILON:
			return
	vertices.append(point)
