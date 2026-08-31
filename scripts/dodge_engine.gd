class_name DodgeEngine
extends RefCounted
# Reusable one-finger dodge grammar. Gameplay supplies a predicted landing in
# its own 2D movement plane; this owns timing, gesture acceptance, and eased
# displacement. It never awards progress and never applies harm.

const SWIPE_MIN_PX := 54.0
const HORIZONTAL_DOMINANCE := 1.5
const READY_LEAD_T := 0.92
const LATE_GRACE_T := 0.16
const DANGER_RADIUS := 10.5
const LANDING_HIT_RADIUS := 4.2
const DODGE_DISTANCE := 7.5
const DODGE_T := 0.34

var landing := Vector2.ZERO
var threat_position := Vector2.ZERO
var threat_position_valid := false
var time_to_land := INF
var available := false
var accepted := false
var landing_resolved := true
var motion_t := DODGE_T
var motion_dir := Vector2.ZERO
var motion_progress := 1.0
var accepted_count := 0
var rejected_count := 0

func begin_landing(predicted_landing: Vector2, eta: float) -> void:
	landing = predicted_landing
	threat_position = Vector2.ZERO
	threat_position_valid = false
	time_to_land = maxf(0.0, eta)
	available = false
	accepted = false
	landing_resolved = false
	motion_t = DODGE_T
	motion_dir = Vector2.ZERO
	motion_progress = 1.0


func set_threat_position(position: Vector2) -> void:
	threat_position = position
	threat_position_valid = true

func update_window(eta: float, player_position: Vector2) -> bool:
	time_to_land = eta
	var danger_origin := landing
	if threat_position_valid:
		danger_origin = threat_position
	available = not accepted and not landing_resolved \
		and eta <= READY_LEAD_T and eta >= -LATE_GRACE_T \
		and player_position.distance_to(danger_origin) <= DANGER_RADIUS
	return available

func try_swipe(from: Vector2, to: Vector2) -> bool:
	var stroke: Vector2 = to - from
	var horizontal: float = absf(stroke.x)
	var vertical: float = absf(stroke.y)
	if not available or accepted or horizontal < SWIPE_MIN_PX \
			or horizontal < vertical * HORIZONTAL_DOMINANCE:
		rejected_count += 1
		return false
	accepted = true
	available = false
	motion_t = 0.0
	motion_progress = 0.0
	motion_dir = Vector2(1.0 if stroke.x >= 0.0 else -1.0, 0.0)
	accepted_count += 1
	return true

func consume_motion(delta: float) -> Vector2:
	if motion_t >= DODGE_T or motion_dir == Vector2.ZERO:
		return Vector2.ZERO
	var prior: float = motion_progress
	motion_t = minf(DODGE_T, motion_t + maxf(0.0, delta))
	var u: float = motion_t / DODGE_T
	motion_progress = 0.5 - 0.5 * cos(u * PI)
	return motion_dir * DODGE_DISTANCE * (motion_progress - prior)

func cancel_motion() -> void:
	motion_t = DODGE_T
	motion_dir = Vector2.ZERO
	motion_progress = 1.0

func resolve_landing(player_position: Vector2) -> bool:
	if landing_resolved:
		return false
	landing_resolved = true
	available = false
	threat_position_valid = false
	return not accepted and player_position.distance_to(landing) <= LANDING_HIT_RADIUS

func reset() -> void:
	landing = Vector2.ZERO
	threat_position = Vector2.ZERO
	threat_position_valid = false
	time_to_land = INF
	available = false
	accepted = false
	landing_resolved = true
	motion_t = DODGE_T
	motion_dir = Vector2.ZERO
	motion_progress = 1.0
