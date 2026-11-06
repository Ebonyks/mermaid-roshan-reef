class_name BubbleDuelMotion
extends RefCounted
## Fresh implementation of the owner-supplied mechanical description.
## Integrate at exactly 30 Hz; rendering and input capture may run faster.
## No target seeking, position snapping, held-key thrust or hard speed clamp.

const RATE: float = 30.0
const STEP: float = 1.0 / RATE
const WRAP_MIN: float = -15.0
const WRAP_MAX: float = 415.0
const WRAP_SPAN: float = 430.0
const SURFACE: float = 20.0
const LOST_Y: float = 400.0
const RESPAWN_Y: float = 300.0

var gravity: float = 0.25
var strength_scale: float = 1.0
var lateral: float = 0.75
var softcap: float = 0.9
var ceiling_bounce: float = 0.8
var ceiling_drag: float = 0.8
var speed_scale: float = 1.0
var pop_hop: float = 2.0


func configure(values: Dictionary) -> bool:
	var limits: Dictionary = {
		"gravity": Vector2(0.15, 0.4), "strength_scale": Vector2(0.7, 1.4),
		"lateral": Vector2(0.4, 1.0), "softcap": Vector2(0.8, 0.97),
		"ceiling_bounce": Vector2(0.55, 1.0), "ceiling_drag": Vector2(0.6, 1.0),
		"speed_scale": Vector2(0.7, 1.4), "pop_hop": Vector2(1.0, 3.5),
	}
	for key: Variant in values:
		if not limits.has(key):
			return false
		var value: Variant = values[key]
		if not (value is float or value is int) or not is_finite(float(value)):
			return false
		var interval: Vector2 = limits[key]
		if float(value) < interval.x or float(value) > interval.y:
			return false
	for key: Variant in values:
		set(StringName(key), float(values[key]))
	return true


func kick(fighter: BubbleDuelFighter, axis: float) -> bool:
	if fighter.held > 0 or fighter.lost or fighter.swallowed:
		return false
	var force: float = fighter.strength * strength_scale * (fighter.inflation + 50.0) / 150.0
	var count: float = float(fighter.bubbles)
	if fighter.bubbles > 0:
		fighter.velocity.y -= force * (count + 6.0) / 8.0
	fighter.velocity.x += force * clampf(axis, -1.0, 1.0) * lateral * (count + 2.0) / 4.0
	if absf(axis) > 0.001:
		fighter.facing = signf(axis)
	fighter.kick_age = 0.0
	if fighter.pose_time >= fighter.pose_duration:
		fighter.pose_time = 0.0
	fighter.kick_count += 1
	return true


func integrate(fighter: BubbleDuelFighter, drift: float, stage: int = 0, kind_gravity: bool = false) -> void:
	fighter.previous = fighter.position
	if fighter.lost:
		return
	fighter.kick_age += STEP
	fighter.pose_time += STEP
	if fighter.swallowed:
		return
	fighter.position += fighter.velocity + Vector2(0.0, drift)
	var fall: float = gravity * (1.0 if fighter.bubbles > 0 else 1.25)
	if kind_gravity and fighter.human >= 0:
		fall *= 0.9
	if fighter.floating:
		fall = 0.0
	fighter.velocity.y += fall
	var drag: float = fighter.drag_tier()
	if absf(fighter.velocity.y) > fighter.max_vy * speed_scale * drag:
		fighter.velocity.y *= softcap
	if absf(fighter.velocity.x) > fighter.max_vx * speed_scale * drag:
		fighter.velocity.x *= softcap
	fighter.floating = false
	if fighter.position.x > WRAP_MAX:
		fighter.position.x = WRAP_MIN
	if fighter.position.x < WRAP_MIN:
		fighter.position.x = WRAP_MAX
	if fighter.position.y < SURFACE:
		fighter.position.y = SURFACE
		if fighter.velocity.y < 0.0:
			fighter.velocity.y *= -ceiling_bounce
			fighter.velocity.x *= ceiling_drag
			fighter.ceiling_bounces += 1
	if fighter.bubbles > 0 and fighter.charge < 100.0:
		fighter.charge += 1.0
	if fighter.invincible > 0:
		fighter.invincible -= 1
	fighter.sway = (fighter.sway * 3.0 - 6.0 * fighter.velocity.x) / 4.0
	match stage:
		1:
			if fighter.inflation < 125.0:
				fighter.inflation += 0.1
		2:
			if fighter.inflation > 50.0:
				fighter.inflation -= 0.1
		3:
			fighter.inflation = clampf(fighter.inflation + pow(fighter.position.y / 400.0, 3.0) - 0.15, 50.0, 140.0)
	if fighter.position.y > LOST_Y:
		rescue(fighter)


func rescue(fighter: BubbleDuelFighter) -> void:
	if fighter.spares > 0 or fighter.unlimited_rescues:
		if not fighter.unlimited_rescues:
			fighter.spares -= 1
		fighter.position.y = RESPAWN_Y
		fighter.previous = fighter.position
		fighter.velocity = Vector2(0.0, -25.0)
		fighter.bubbles = 2
		fighter.survivor_side = 1
		fighter.inflation = 100.0
		fighter.invincible = 50
		fighter.swallowed = false
		fighter.held = 0
		fighter.kick_age = 0.0
		fighter.pose_time = 0.0
		fighter.rescues += 1
	else:
		fighter.lost = true
		fighter.charge = 0.0
		fighter.position.y = LOST_Y + 50.0


static func wrapped_dx(distance: float) -> float:
	while distance > WRAP_SPAN * 0.5:
		distance -= WRAP_SPAN
	while distance < -WRAP_SPAN * 0.5:
		distance += WRAP_SPAN
	return distance
