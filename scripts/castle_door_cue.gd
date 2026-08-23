class_name CastleDoorCue
extends Control
# Lightweight CanvasItem-only door cues. They sit over the existing painted
# door without adding to the Castle's measured spatial migration debt.

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
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
	set_process(true)
	_sync_visibility()


func set_door_state(next_state: String) -> void:
	var normalized: String = DoorLanguage.normalize(next_state)
	if door_state == normalized:
		return
	door_state = normalized
	set_meta("castle_door_state", door_state)
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
	var veil_alpha: float = 0.24 + flutter * 0.14
	draw_rect(Rect2(Vector2.ZERO, size),
		Color(0.07, 0.05, 0.15, veil_alpha), true)
	var wisp_count := 5
	for index: int in range(wisp_count):
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
	draw_rect(Rect2(Vector2(2.0, 2.0), size - Vector2(4.0, 4.0)),
		Color(0.34, 0.31, 0.52, 0.42 + flutter * 0.28), false,
		2.0 + flutter * 2.0)


func _draw_bonus() -> void:
	var breath: float = 0.5 + 0.5 * sin(motion_time * 1.7)
	var outer := Rect2(Vector2(5.0, 5.0), size - Vector2(10.0, 10.0))
	draw_rect(outer, Color(0.18, 0.50, 1.0, 0.22 + breath * 0.14),
		false, 10.0 + breath * 3.0)
	draw_rect(outer.grow(-5.0), Color(0.34, 0.72, 1.0, 0.80),
		false, 3.0)
	for index: int in range(4):
		var phase: float = fposmod(
			motion_time * (0.18 + float(index) * 0.015)
				+ float(index) * 0.23, 1.0)
		var bubble := Vector2(
			outer.position.x + outer.size.x * (0.20 + float(index) * 0.20),
			outer.end.y - outer.size.y * phase)
		draw_circle(bubble, 3.5 + float(index % 2) * 2.0,
			Color(0.56, 0.86, 1.0, 0.34 + breath * 0.22), false, 1.8)


func _draw_plot() -> void:
	var pulse: float = 0.5 + 0.5 * sin(motion_time * 2.7)
	var outer := Rect2(Vector2(4.0, 4.0), size - Vector2(8.0, 8.0))
	draw_rect(outer, Color(1.0, 0.72, 0.16, 0.22 + pulse * 0.18),
		false, 12.0 + pulse * 4.0)
	draw_rect(outer.grow(-5.0), Color(1.0, 0.84, 0.34, 0.96),
		false, 4.0)
	var sheen_x: float = fposmod(motion_time * size.x * 0.22,
		size.x * 1.8) - size.x * 0.45
	var band_width: float = maxf(2.0, size.x * 0.012)
	for index: int in range(RAINBOW.size()):
		var start := Vector2(sheen_x + float(index) * band_width,
			outer.end.y)
		var finish := Vector2(start.x + size.x * 0.42, outer.position.y)
		var tint: Color = RAINBOW[index]
		tint.a = 0.38
		draw_line(start, finish, tint, band_width, true)
	var star_center := Vector2(size.x * 0.5,
		maxf(18.0, outer.position.y + 14.0 + sin(motion_time * 3.0) * 4.0))
	var star_radius: float = 10.0 + pulse * 3.0
	var points := PackedVector2Array()
	for index: int in range(8):
		var angle: float = -PI * 0.5 + float(index) * TAU / 8.0
		var radius: float = star_radius if index % 2 == 0 else star_radius * 0.38
		points.append(star_center + Vector2(cos(angle), sin(angle)) * radius)
	draw_colored_polygon(points, Color(1.0, 0.90, 0.44, 0.98))
