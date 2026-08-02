class_name DustBunnyAI
extends RefCounted
# Deterministic analytic brain for the second enemy family. A dust bunny rests,
# telegraphs with its squash frame, and hops either around its play space or
# gently toward Roshan. Contact reports a bubble-shield bump; it never removes
# progress, health, or control.

const HOP_TIME := 0.67
const HOP_HEIGHT := 1.35
const MAX_HOP_DISTANCE := 5.2
const BUMP_RANGE := 1.65
const REST_MIN := 0.45
const REST_MAX := 1.15

var pos: Vector3 = Vector3.ZERO
var facing_x: float = 1.0

var _center: Vector3 = Vector3.ZERO
var _base_y: float = 0.0
var _radius: float = 12.0
var _state: StringName = &"rest"
var _timer: float = 0.2
var _hop_from: Vector3 = Vector3.ZERO
var _hop_to: Vector3 = Vector3.ZERO
var _hop_count: int = 0
var _attack_hop: bool = false
var _bump_sent: bool = false
var _rng: RandomNumberGenerator = RandomNumberGenerator.new()


func setup(start: Vector3, arena_center: Vector3, arena_radius: float,
		seed_value: int = 1, initial_delay: float = 0.2) -> void:
	pos = start
	_center = arena_center
	_base_y = start.y
	_radius = maxf(arena_radius, 2.0)
	_state = &"rest"
	_timer = maxf(initial_delay, 0.0)
	_hop_from = start
	_hop_to = start
	_hop_count = 0
	_attack_hop = false
	_bump_sent = false
	_rng.seed = seed_value


func tick(delta: float, player_pos: Vector3) -> Dictionary:
	var out: Dictionary = {
		"action": &"",
		"bump": false,
		"landed": false,
	}
	if _state == &"rest":
		_timer -= delta
		if _timer <= 0.0:
			_begin_hop(player_pos)
			out["action"] = &"hop"
		return out
	_timer = maxf(0.0, _timer - delta)
	var progress: float = clampf(1.0 - _timer / HOP_TIME, 0.0, 1.0)
	pos = _hop_from.lerp(_hop_to, progress)
	pos.y = _base_y + sin(progress * PI) * HOP_HEIGHT
	if _attack_hop and not _bump_sent:
		var player_flat: Vector3 = player_pos
		player_flat.y = _base_y
		if pos.distance_to(player_flat) <= BUMP_RANGE:
			_bump_sent = true
			out["bump"] = true
	if progress >= 1.0:
		pos = _hop_to
		pos.y = _base_y
		_state = &"rest"
		_timer = _rng.randf_range(REST_MIN, REST_MAX)
		out["landed"] = true
	return out


func _begin_hop(player_pos: Vector3) -> void:
	_hop_from = pos
	_hop_from.y = _base_y
	_attack_hop = _hop_count % 3 == 0
	_hop_count += 1
	if _attack_hop:
		var toward: Vector3 = player_pos - _hop_from
		toward.y = 0.0
		if toward.length() > MAX_HOP_DISTANCE:
			toward = toward.normalized() * MAX_HOP_DISTANCE
		_hop_to = _hop_from + toward
	else:
		var angle: float = _rng.randf_range(0.0, TAU)
		var distance: float = _rng.randf_range(2.0, MAX_HOP_DISTANCE)
		_hop_to = _hop_from + Vector3(sin(angle) * distance, 0.0, cos(angle) * distance)
	_clamp_hop_to_arena()
	facing_x = _hop_to.x - _hop_from.x
	_bump_sent = false
	_state = &"hop"
	_timer = HOP_TIME


func _clamp_hop_to_arena() -> void:
	var flat: Vector2 = Vector2(_hop_to.x - _center.x, _hop_to.z - _center.z)
	if flat.length() > _radius:
		flat = flat.normalized() * _radius
	_hop_to.x = _center.x + flat.x
	_hop_to.y = _base_y
	_hop_to.z = _center.z + flat.y
