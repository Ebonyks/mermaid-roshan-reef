class_name CastleDoorCue
extends Control
## Input-transparent Canvas cue for one existing painted castle door.

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const ARCH_SEGMENTS := 24
const BONUS_PERIOD_SECONDS := 4.4
const PLOT_PERIOD_SECONDS := 3.2
const PLOT_SHIMMER_PERIOD_SECONDS := 4.6
const BONUS_OUTER_COLOR := Color(0.96, 0.34, 0.39)
const BONUS_INNER_COLOR := Color(1.00, 0.62, 0.58)
const PLOT_OUTER_COLOR := Color(1.00, 0.72, 0.16)
const PLOT_INNER_COLOR := Color(1.00, 0.84, 0.34)
const RAINBOW: Array[Color] = [
	Color(1.00, 0.36, 0.44),
	Color(1.00, 0.66, 0.24),
	Color(1.00, 0.88, 0.34),
	Color(0.42, 0.88, 0.62),
	Color(0.34, 0.72, 1.00),
	Color(0.66, 0.48, 1.00),
]

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
			_draw_bonus()
		DoorLanguage.PLOT:
			_draw_plot()


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
	draw_polyline(_arch_points(3.0),
		Color(0.34, 0.31, 0.52, 0.35 + flutter * 0.28),
		2.0 + flutter * 2.0, true)


func _draw_bonus() -> void:
	var breath: float = _motion_wave(BONUS_PERIOD_SECONDS)
	var outer_tint := BONUS_OUTER_COLOR
	outer_tint.a = 0.20 + breath * 0.22
	draw_polyline(_arch_points(5.0), outer_tint,
		4.0 + breath * 2.0, true)
	var inner_tint := BONUS_INNER_COLOR
	inner_tint.a = 0.46 + breath * 0.22
	draw_polyline(_arch_points(8.0), inner_tint, 1.6, true)


func _draw_plot() -> void:
	var pulse: float = _motion_wave(PLOT_PERIOD_SECONDS)
	var outer := Rect2(Vector2(4.0, 4.0), size - Vector2(8.0, 8.0))
	var outer_tint := PLOT_OUTER_COLOR
	outer_tint.a = 0.18 + pulse * 0.16
	draw_polyline(_arch_points(4.0), outer_tint,
		5.0 + pulse * 2.0, true)
	var inner_tint := PLOT_INNER_COLOR
	inner_tint.a = 0.86 + pulse * 0.10
	draw_polyline(_arch_points(8.0), inner_tint, 2.5, true)
	var sheen_progress: float = fposmod(
		motion_time / PLOT_SHIMMER_PERIOD_SECONDS, 1.0)
	var sheen_x: float = lerpf(-size.x * 0.45, size.x * 1.35,
		sheen_progress)
	var band_width: float = maxf(1.5, size.x * 0.008)
	for index: int in range(RAINBOW.size()):
		var start := Vector2(sheen_x + float(index) * band_width, outer.end.y)
		var finish := Vector2(start.x + size.x * 0.34, outer.position.y)
		var tint: Color = RAINBOW[index]
		tint.a = 0.28
		draw_line(start, finish, tint, band_width, true)
	var star_center := Vector2(size.x * 0.5,
		maxf(16.0, outer.position.y + 12.0
			+ sin(motion_time * TAU / 3.6) * 1.5))
	var star_radius: float = 8.5 + pulse * 1.5
	var points := PackedVector2Array()
	for index: int in range(8):
		var angle: float = -PI * 0.5 + float(index) * TAU / 8.0
		var radius: float = star_radius if index % 2 == 0 else star_radius * 0.38
		points.append(star_center + Vector2(cos(angle), sin(angle)) * radius)
	draw_colored_polygon(points, Color(1.0, 0.90, 0.44, 0.98))


func _motion_wave(period_seconds: float) -> float:
	return 0.5 + 0.5 * sin(motion_time * TAU / period_seconds)


func _arch_points(inset: float) -> PackedVector2Array:
	var left: float = inset
	var right: float = maxf(left + 1.0, size.x - inset)
	var bottom: float = maxf(inset + 1.0, size.y - inset)
	var center := Vector2(size.x * 0.5, size.y * 0.34)
	var radius_x: float = maxf(1.0, (right - left) * 0.5)
	var radius_y: float = minf(maxf(1.0, size.y * 0.20),
		maxf(1.0, center.y - inset))
	var points := PackedVector2Array()
	points.append(Vector2(left, bottom))
	points.append(Vector2(left, center.y))
	for index: int in range(ARCH_SEGMENTS + 1):
		var angle: float = PI + PI * float(index) / float(ARCH_SEGMENTS)
		points.append(center + Vector2(cos(angle) * radius_x,
			sin(angle) * radius_y))
	points.append(Vector2(right, bottom))
	return points
