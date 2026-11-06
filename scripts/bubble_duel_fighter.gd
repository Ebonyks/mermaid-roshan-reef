class_name BubbleDuelFighter
extends RefCounted
## A bout's transient state. Velocities are logical units per original 30 Hz tick.

var profile: Dictionary = {}
var slot: int = 0
var human: int = -1
var team: int = 0
var position := Vector2.ZERO
var previous := Vector2.ZERO
var velocity := Vector2.ZERO
var facing: float = 1.0
var direction: float = 0.0
var bubbles: int = 2
var survivor_side: int = 1
var spares: int = 4
var inflation: float = 100.0
var charge: float = 0.0
var invincible: int = 0
var held: int = 0
var swallowed: bool = false
var lost: bool = false
var unlimited_rescues: bool = false
var floating: bool = false
var auto_timer: int = 0
var sway: float = 0.0
var kick_edge: bool = false
var kick_direction: float = 0.0
var power_edge: bool = false
var power_held: bool = false
var gear: String = "classic"
var max_vx: float = 6.0
var max_vy: float = 5.0
var strength: float = 3.0
var kick_age: float = 100.0
var pose_time: float = 100.0
var pose_duration: float = 16.0 / 15.0
var moving_pose: bool = false
var draw_clock: float = 0.0
var previous_fin := Vector2.ZERO
var previous_sway: float = 0.0
var previous_facing: float = 1.0
var charms_used: int = 0
var hover_last: bool = false
var kick_count: int = 0
var ceiling_bounces: int = 0
var body_bounces: int = 0
var pops: int = 0
var rescues: int = 0
var consumed_inputs: int = 0
var ceiling_release: bool = false
var cpu_skill: float = 0.0
var cpu_reflex: float = 0.0
var history := PackedVector2Array()
var history_cursor: int = 0
var history_count: int = 0
var rng := RandomNumberGenerator.new()
var draw_offset := Vector2.ZERO
var fin_center := Vector2(0.0, 12.5)
var fin_half := Vector2(8.0, 3.5)
var body_box := Rect2(-7.0, -9.0, 14.0, 20.0)
var shot_tip := Vector2(10.0, -20.0)


func _init() -> void:
	history.resize(10)


func reset(at: Vector2, launch: float = -20.0) -> void:
	position = at
	previous = at
	velocity = Vector2(0.0, launch)
	bubbles = 2
	survivor_side = 1
	inflation = 100.0
	charge = 0.0
	invincible = 0
	held = 0
	swallowed = false
	lost = false
	floating = false
	auto_timer = 0
	sway = 0.0
	kick_age = 100.0
	pose_time = 100.0
	charms_used = 0
	kick_count = 0
	ceiling_bounces = 0
	body_bounces = 0
	pops = 0
	rescues = 0
	consumed_inputs = 0
	history_count = 0
	history_cursor = 0
	clear_controls()


func clear_controls() -> void:
	direction = 0.0
	kick_edge = false
	kick_direction = 0.0
	power_edge = false
	power_held = false


func drag_tier() -> float:
	return 1.0 if bubbles >= 2 else (1.2 if bubbles == 1 else 2.0)
