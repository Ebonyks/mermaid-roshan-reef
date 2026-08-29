class_name CastleDoorCue
extends Control
## Input-transparent Canvas cue for one existing painted castle door.

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const BONUS_PERIOD_SECONDS := 4.4
const PLOT_PERIOD_SECONDS := 3.2
const BONUS_GLOW_COLOR := Color(0.98, 0.26, 0.34)
const PLOT_GLOW_COLOR := Color(1.00, 0.72, 0.16)

var door_state: String = DoorLanguage.OPEN
var motion_time := 0.0
var feedback_time := 0.0


func _init() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = true
	_sync_visibility()


func set_door_state(next_state: String) -> void:
	var normalized: String = DoorLanguage.normalize(next_state)
	set_meta("castle_door_state", normalized)
	if door_state == normalized:
		return
	door_state = normalized
	_sync_visibility()
	queue_redraw()


func pulse_blocked_feedback() -> void:
	feedback_time = 0.72
	queue_redraw()


func _sync_visibility() -> void:
	# The glow fills the doorway opening without drawing a synthetic frame edge.
	# The rejected arch-shaped shimmer gate stays removed until an exact painted-
	# frame mask exists for every doorway.
	visible = door_state != DoorLanguage.OPEN
	set_process(visible)


func _process(delta: float) -> void:
	motion_time += maxf(0.0, delta)
	feedback_time = maxf(0.0, feedback_time - maxf(0.0, delta))
	queue_redraw()


func _draw() -> void:
	if size.x < 2.0 or size.y < 2.0:
		return
	match door_state:
		DoorLanguage.BLOCKED:
			_draw_blocked()
		DoorLanguage.BONUS:
			_draw_bonus_glow()
		DoorLanguage.PLOT:
			_draw_plot_glow()


func _draw_blocked() -> void:
	var flutter: float = feedback_time / 0.72
	draw_rect(Rect2(Vector2.ZERO, size),
		Color(0.07, 0.05, 0.15, 0.16 + flutter * 0.10), true)
	for index: int in range(5):
		var phase: float = motion_time * (0.34 + float(index) * 0.025) \
			+ float(index) * 1.37
		var center := Vector2(
			fposmod(size.x * (0.12 + float(index) * 0.22)
				+ sin(phase) * size.x * 0.10, size.x),
			size.y * (0.22 + float(index % 3) * 0.27)
				+ cos(phase * 0.71) * size.y * 0.06)
		var radius: float = maxf(18.0, minf(size.x, size.y) *
			(0.18 + float(index % 2) * 0.05))
		draw_set_transform(center, sin(phase * 0.55) * 0.08,
			Vector2(1.75, 0.52 + flutter * 0.08))
		draw_circle(Vector2.ZERO, radius,
			Color(0.52, 0.52, 0.72, 0.22 + flutter * 0.10))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_bonus_glow() -> void:
	_draw_doorway_glow(BONUS_GLOW_COLOR,
		_motion_wave(BONUS_PERIOD_SECONDS), 0.18)


func _draw_plot_glow() -> void:
	_draw_doorway_glow(PLOT_GLOW_COLOR,
		_motion_wave(PLOT_PERIOD_SECONDS), 0.24)


func _draw_doorway_glow(color: Color, pulse: float,
		peak_alpha: float) -> void:
	var center := Vector2(size.x * 0.5, size.y * 0.58)
	# Leave generous transparent margins on every side. The previous ellipse
	# reached the Control bounds and clip_contents exposed those bounds as a
	# false rectangular door frame.
	var radius_x: float = maxf(1.0, size.x * 0.38)
	var top_budget: float = maxf(1.0, center.y - size.y * 0.10)
	var bottom_budget: float = maxf(1.0,
		size.y - center.y - size.y * 0.08)
	var radius_y: float = maxf(1.0, minf(size.y * 0.34,
		minf(top_budget, bottom_budget)))
	var glow_scale := Vector2(radius_x / radius_y, 1.0)
	for layer: int in range(9):
		var radius_fraction: float = 1.0 - float(layer) * 0.09
		var tint := color
		tint.a = peak_alpha * (0.11 + float(layer) * 0.025) \
			* (0.62 + pulse * 0.38)
		draw_set_transform(center, 0.0, glow_scale)
		draw_circle(Vector2.ZERO, radius_y * radius_fraction, tint,
			true, -1.0, true)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _motion_wave(period_seconds: float) -> float:
	return 0.5 + 0.5 * sin(motion_time * TAU / period_seconds)
