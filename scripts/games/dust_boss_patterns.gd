class_name DustBossPatterns
extends RefCounted

## Pure Vector2 attack sequencer for Grand Puff. Targets are captured when a
## tell begins and never follow the player afterward. The returned dictionaries
## are also the rendering contract for the 2D danger overlay and headless probes.

const LANDING_RADIUS: float = 5.2
const LANE_HALF_WIDTH: float = 4.4
const LANE_HALF_LENGTH: float = 23.0
const MIN_TELL_TIME: float = 1.4

var phase_index: int = 0
var step_index: int = 0
var tell_time: float = MIN_TELL_TIME
var elapsed: float = 0.0
var active: bool = false
var resolved: bool = false
var geometry: Dictionary = {}
var arena_limit: float = 0.0


func begin_phase(phase: int, player_position: Vector2,
		boss_position: Vector2, arena_radius: float) -> void:
	phase_index = clampi(phase, 0, 2)
	arena_limit = maxf(0.0, arena_radius * cos(PI / 8.0) - 2.6)
	step_index = 0
	_begin_step(player_position, boss_position, arena_radius)
	geometry["safe_point"] = _safe_point()


func advance_combo(player_position: Vector2, boss_position: Vector2,
		arena_radius: float) -> bool:
	if step_index + 1 >= step_count():
		active = false
		geometry = {}
		return false
	step_index += 1
	arena_limit = maxf(0.0, arena_radius * cos(PI / 8.0) - 2.6)
	_begin_step(player_position, boss_position, arena_radius)
	geometry["safe_point"] = _safe_point()
	return true


func tick(delta: float) -> void:
	if active:
		elapsed += maxf(0.0, delta)


func tell_finished() -> bool:
	return active and elapsed >= tell_time


func step_count() -> int:
	return 1 if phase_index == 0 else 2


func contains(point: Vector2, clearance: float = 0.0) -> bool:
	if geometry.is_empty():
		return false
	# Include the painted boundary despite dot-product rounding at clipped tips.
	var padding: float = maxf(0.0, clearance) + 0.01
	var kind: String = String(geometry.get("kind", ""))
	if kind == "landing_circle":
		var center: Vector2 = geometry.get("center", Vector2.ZERO) as Vector2
		return point.distance_to(center) <= float(geometry.get("radius", 0.0)) + padding
	if kind == "swept_lane":
		var lane_center: Vector2 = geometry.get("center", Vector2.ZERO) as Vector2
		var direction: Vector2 = geometry.get("direction", Vector2.RIGHT) as Vector2
		var offset: Vector2 = point - lane_center
		return absf(offset.dot(direction)) <= float(geometry.get("half_length", 0.0)) + padding \
			and absf(offset.dot(Vector2(-direction.y, direction.x))) \
			<= float(geometry.get("half_width", 0.0)) + padding
	return false


func readout() -> Dictionary:
	var result: Dictionary = geometry.duplicate(true)
	result["phase"] = phase_index
	result["step"] = step_index
	result["step_count"] = step_count()
	result["tell_elapsed"] = elapsed
	result["tell_duration"] = tell_time
	result["progress"] = clampf(elapsed / maxf(tell_time, 0.01), 0.0, 1.0)
	result["active"] = active
	result["locked"] = active
	result["resolved"] = resolved
	result["safe_point"] = geometry.get("safe_point", Vector2.ZERO)
	return result


func _safe_point() -> Vector2:
	if geometry.is_empty():
		return Vector2.ZERO
	var origin: Vector2 = geometry.get("locked_center",
		geometry.get("center", Vector2.ZERO)) as Vector2
	var best := Vector2.ZERO
	var best_distance: float = INF
	# Search nearby stage-valid destinations instead of assuming that an inward
	# or perpendicular offset survives corner clamping. Every returned point is
	# verified against the exact same danger predicate used at impact.
	for ring: float in [8.0, 12.0, 18.0, 24.0]:
		for i in range(32):
			var angle: float = TAU * float(i) / 32.0
			var candidate: Vector2 = _clamp_to_octagon(origin \
				+ Vector2(cos(angle), sin(angle)) * ring)
			var travel: float = candidate.distance_to(origin)
			if not contains(candidate, 1.2) and travel < best_distance:
				best = candidate
				best_distance = travel
		if best_distance < INF:
			return best
	return _clamp_to_octagon(Vector2.ZERO)


func _clamp_to_octagon(point: Vector2) -> Vector2:
	var result: Vector2 = point
	for _pass in range(2):
		for i in range(8):
			var normal := Vector2(cos(float(i) * PI / 4.0),
				sin(float(i) * PI / 4.0))
			var excess: float = result.dot(normal) - arena_limit
			if excess > 0.0:
				result -= normal * excess
	return result


func _begin_step(player_position: Vector2, boss_position: Vector2,
		arena_radius: float) -> void:
	elapsed = 0.0
	active = true
	resolved = false
	tell_time = MIN_TELL_TIME + (0.15 if phase_index == 0 else 0.0)
	if phase_index == 2 and step_index == 1:
		var locked_center: Vector2 = player_position
		var travel: Vector2 = player_position - boss_position
		if travel.length_squared() < 0.01:
			travel = -boss_position if boss_position.length_squared() > 0.01 else Vector2.DOWN
		travel = travel.normalized()
		var lane_from: Vector2 = boss_position
		var travel_length: float = _ray_to_octagon_edge(
			lane_from, travel, arena_radius)
		var lane_to: Vector2 = lane_from + travel * travel_length
		var lane_center: Vector2 = (lane_from + lane_to) * 0.5
		geometry = {
			"kind": "swept_lane",
			"shape": "lane",
			"center": lane_center,
			"locked_center": locked_center,
			"direction": travel,
			"from": lane_from,
			"to": lane_to,
			"half_width": LANE_HALF_WIDTH,
			"half_length": travel_length * 0.5,
		}
		return
	# Player positions already come from the stage's valid walkable region.
	# Preserve the exact snapshot even at an edge: shrinking the target center
	# inward lets a stationary edge camper evade without moving.
	var locked_center: Vector2 = player_position
	geometry = {
		"kind": "landing_circle",
		"shape": "circle",
		"center": locked_center,
		"radius": LANDING_RADIUS,
	}


func _ray_to_octagon_edge(from: Vector2, direction: Vector2,
		arena_radius: float) -> float:
	var limit: float = arena_radius * cos(PI / 8.0) - 2.6
	var distance: float = arena_radius * 2.0
	for i in range(8):
		var normal := Vector2(cos(float(i) * PI / 4.0),
			sin(float(i) * PI / 4.0))
		var denominator: float = direction.dot(normal)
		if denominator > 0.0001:
			distance = minf(distance,
				(limit - from.dot(normal)) / denominator)
	return maxf(0.5, distance)
