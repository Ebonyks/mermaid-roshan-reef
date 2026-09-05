class_name EncounterTelegraph2D
extends Control

## Reusable screen-space language for avoid-then-act encounters.
## Callers own world geometry and projection. This renderer owns no gameplay.

const NAVY := Color("#302854")
const PEACH := Color("#F5A77F")
const PEACH_DARK := Color("#D96D62")
const CYAN := Color("#70E5E2")
const PIP_EMPTY := Color(0.84, 0.91, 0.95, 0.78)
const SAFE_HAND := preload("res://assets/castle/training/ghost_hand.png")

var _visible := false
var _active := false
var _points := PackedVector2Array()
var _closed_points := PackedVector2Array()
var _countdown_points := PackedVector2Array()
var _center := Vector2.ZERO
var _progress := 0.0
var _safe_point := Vector2.ZERO
var _player_point := Vector2.ZERO
var _safe_visible := false
var _puffs := 3
var _total := 3
var _pulse_t := 0.0
var _redraw_accum := 0.0
var _redraw_interval := 0.0
var _safe_hand: TextureRect
var draw_floor: bool = true
var draw_overlay: bool = true


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_safe_hand = TextureRect.new()
	_safe_hand.name = "EncounterSafeHand"
	_safe_hand.texture = SAFE_HAND
	_safe_hand.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_safe_hand.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_safe_hand.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_safe_hand.size = Vector2(76.0, 76.0)
	_safe_hand.pivot_offset = _safe_hand.size * 0.5
	_safe_hand.visible = false
	add_child(_safe_hand)
	queue_redraw()


func _process(delta: float) -> void:
	if not _visible:
		return
	_pulse_t = fmod(_pulse_t + delta, TAU)
	if _safe_hand != null and _safe_hand.visible:
		_safe_hand.position.y = _safe_point.y - 92.0 + sin(_pulse_t * 4.0) * 7.0
		_safe_hand.rotation = sin(_pulse_t * 2.0) * 0.06
	_redraw_accum += delta
	if _redraw_interval <= 0.0:
		_redraw_accum = 0.0
		queue_redraw()
	elif _redraw_accum >= _redraw_interval:
		_redraw_accum = fmod(_redraw_accum, _redraw_interval)
		queue_redraw()


func configure_quality(quality: String) -> void:
	# Speedy targets 30 fps. Do not redraw this full-viewport CanvasItem more
	# often than the target even if its caller ticks at a higher desktop rate.
	_redraw_interval = 1.0 / 30.0 if quality.to_lower() == "speedy" else 0.0
	_redraw_accum = 0.0


func set_telegraph(data: Dictionary) -> void:
	var presentation_changed: bool = _visible != bool(data.get("visible", false)) \
		or _active != bool(data.get("active", false)) \
		or _puffs != int(data.get("puffs", _total)) \
		or _total != maxi(1, int(data.get("total", 3)))
	_visible = bool(data.get("visible", false))
	_active = bool(data.get("active", false))
	var value: Variant = data.get("points")
	var geometry_changed: bool = value is PackedVector2Array \
		and (value as PackedVector2Array) != _points
	if not (value is PackedVector2Array):
		geometry_changed = not _points.is_empty()
	if geometry_changed:
		if value is PackedVector2Array:
			_points = value as PackedVector2Array
		else:
			_points.clear()
		_closed_points = PackedVector2Array(_points)
		if not _points.is_empty():
			_closed_points.append(_points[0])
		_center = _calculate_centroid()
		if _countdown_points.size() != _closed_points.size():
			_countdown_points.resize(_closed_points.size())
	_progress = clampf(float(data.get("progress", 0.0)), 0.0, 1.0)
	var countdown_scale: float = lerpf(1.28, 1.0, _progress)
	for index: int in _countdown_points.size():
		_countdown_points[index] = _center \
			+ (_closed_points[index] - _center) * countdown_scale
	_safe_point = _as_point(data.get("safe_point", Vector2.ZERO))
	_player_point = _as_point(data.get("player_point", Vector2.ZERO))
	_safe_visible = bool(data.get("safe_visible", _safe_point != Vector2.ZERO)) \
		and _safe_point != Vector2.ZERO
	_total = maxi(1, int(data.get("total", 3)))
	_puffs = clampi(int(data.get("puffs", _total)), 0, _total)
	_update_safe_hand()
	# Discrete state changes must redraw even after the animation loop stops:
	# clear the last floor warning and fill the final earned progress marker.
	if _redraw_interval <= 0.0 or geometry_changed or presentation_changed:
		queue_redraw()


func _as_point(value: Variant) -> Vector2:
	return value if value is Vector2 else Vector2.ZERO


func _update_safe_hand() -> void:
	if _safe_hand == null:
		return
	_safe_hand.visible = draw_overlay and _visible and _safe_visible and not _active
	_safe_hand.position = _safe_point - Vector2(38.0, 92.0)


func _draw() -> void:
	if _visible and _points.size() >= 3:
		if draw_floor:
			_draw_danger()
		if draw_overlay and _safe_visible:
			_draw_safe_destination()
	if draw_overlay:
		_draw_pips()


func _draw_danger() -> void:
	var pulse: float = 0.5 + 0.5 * sin(_pulse_t * (8.0 if _active else 3.2))
	var fill_alpha: float = 0.34 if _active else 0.18
	var edge: Color = PEACH_DARK if _active else PEACH
	var width: float = 9.0 if _active else 6.0
	draw_colored_polygon(_points, Color(PEACH.r, PEACH.g, PEACH.b, fill_alpha))
	draw_polyline(_closed_points, NAVY, width + 6.0, true)
	draw_polyline(_closed_points, edge, width, true)
	# One closing outline reads as time remaining without decorative counters.
	draw_polyline(_countdown_points, Color(edge.r, edge.g, edge.b,
		0.50 + pulse * (0.36 if _active else 0.16)), width + 2.0, true)
	if _active:
		draw_circle(_center, 24.0 + pulse * 14.0,
			Color(PEACH_DARK.r, PEACH_DARK.g, PEACH_DARK.b, 0.18 + pulse * 0.18))


func _calculate_centroid() -> Vector2:
	var center := Vector2.ZERO
	for point: Vector2 in _points:
		center += point
	return center / float(maxi(1, _points.size()))


func _draw_safe_destination() -> void:
	var pulse: float = 0.5 + 0.5 * sin(_pulse_t * 4.0)
	if _player_point != Vector2.ZERO and _player_point.distance_to(_safe_point) > 42.0:
		draw_dashed_line(_player_point, _safe_point,
			Color(CYAN.r, CYAN.g, CYAN.b, 0.74), 7.0, 18.0, true)
	draw_circle(_safe_point, 33.0 + pulse * 6.0,
		Color(CYAN.r, CYAN.g, CYAN.b, 0.20 + pulse * 0.08))
	draw_circle(_safe_point, 32.0 + pulse * 5.0, NAVY, false, 9.0, true)
	draw_circle(_safe_point, 32.0 + pulse * 5.0, CYAN, false, 6.0, true)
	draw_circle(_safe_point, 8.0 + pulse * 2.0, CYAN)


func _draw_pips() -> void:
	var spacing := 34.0
	var center := Vector2(size.x * 0.5, 54.0)
	var first_x: float = center.x - float(_total - 1) * spacing * 0.5
	for index: int in range(_total):
		var point := Vector2(first_x + float(index) * spacing, center.y)
		var filled: bool = index < _puffs
		draw_circle(point, 11.0, CYAN if filled else PIP_EMPTY)
		draw_circle(point, 11.0, NAVY, false, 3.0)
