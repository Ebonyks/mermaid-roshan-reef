class_name DustBossTelegraph2D
extends Control

## A small, screen-space warning layer for Grand Puff's landing attacks.
## The battle controller owns the projection; this node only draws it.

const NAVY := Color("#302854")
const PEACH := Color("#F5A77F")
const PEACH_DARK := Color("#D96D62")
const CYAN := Color("#70E5E2")
const PIP_EMPTY := Color(0.84, 0.91, 0.95, 0.78)

var _data: Dictionary = {
	"visible": false,
	"shape": "circle",
	"points": PackedVector2Array(),
	"progress": 0.0,
	"active": false,
	"safe_point": Vector2.ZERO,
	"player_point": Vector2.ZERO,
	"puffs": 3,
	"phase": 0,
}

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	queue_redraw()

func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		queue_redraw()

func set_telegraph(data: Dictionary) -> void:
	_data["visible"] = bool(data.get("visible", false))
	var shape: String = String(data.get("shape", "circle"))
	_data["shape"] = "lane" if shape == "lane" else "circle"
	var points_value: Variant = data.get("points", PackedVector2Array())
	if points_value is PackedVector2Array:
		_data["points"] = points_value
	else:
		_data["points"] = PackedVector2Array()
	_data["progress"] = clampf(float(data.get("progress", 0.0)), 0.0, 1.0)
	_data["active"] = bool(data.get("active", false))
	_data["safe_point"] = _as_point(data.get("safe_point", Vector2.ZERO))
	_data["player_point"] = _as_point(data.get("player_point", Vector2.ZERO))
	_data["puffs"] = clampi(int(data.get("puffs", 3)), 0, 3)
	_data["phase"] = clampi(int(data.get("phase", 0)), 0, 2)
	queue_redraw()

func _as_point(value: Variant) -> Vector2:
	return value if value is Vector2 else Vector2.ZERO

func _draw() -> void:
	if not bool(_data["visible"]):
		_draw_pips()
		return
	var points: PackedVector2Array = _data["points"]
	if points.size() < 3:
		_draw_pips()
		return
	var active: bool = bool(_data["active"])
	var fill_alpha := 0.30 if active else 0.20
	var edge := PEACH_DARK if active else PEACH
	var width := 8.0 if active else 5.0
	_draw_warning_shape(points, Color(PEACH.r, PEACH.g, PEACH.b, fill_alpha), edge, width)
	_draw_progress(points, edge, width + 3.0)
	_draw_countdown_dots(points, edge)
	if _has_safe_destination():
		_draw_safe_pointer(active)
	_draw_pips()

func _draw_warning_shape(points: PackedVector2Array, fill: Color,
		edge: Color, width: float) -> void:
	if String(_data["shape"]) == "circle":
		draw_colored_polygon(points, fill)
		draw_polyline(_closed(points), NAVY, width + 6.0, true)
		draw_polyline(_closed(points), edge, width, true)
	else:
		# A lane is intentionally broad and quiet: its polygon reads as a place
		# to leave, rather than a collection of small hazards.
		draw_colored_polygon(points, Color(fill.r, fill.g, fill.b, fill.a * 0.82))
		draw_polyline(_closed(points), NAVY, width + 6.0, true)
		draw_polyline(_closed(points), edge, width, true)

func _closed(points: PackedVector2Array) -> PackedVector2Array:
	var result := PackedVector2Array(points)
	if result.size() > 0:
		result.append(result[0])
	return result

func _draw_progress(points: PackedVector2Array, color: Color, width: float) -> void:
	var progress: float = float(_data["progress"])
	if progress <= 0.01:
		return
	var closed := _closed(points)
	var count: int = maxi(2, int(roundf(float(points.size()) * progress)) + 1)
	count = mini(count, closed.size())
	var partial := PackedVector2Array()
	for i in range(count):
		partial.append(closed[i])
	draw_polyline(partial, color, width, true)

func _draw_countdown_dots(points: PackedVector2Array, color: Color) -> void:
	var count: int = 6 if String(_data["shape"]) == "circle" else 4
	var center := _centroid(points)
	for i in range(count):
		var t := (float(i) + 0.5) / float(count)
		var point := _perimeter_point(points, t)
		var radius := 7.0 if bool(_data["active"]) else 5.0
		draw_circle(point, radius, color)
		draw_circle(point, radius + 2.0, Color(NAVY.r, NAVY.g, NAVY.b, 0.55), false, 2.0)
	# Keep the countdown visually anchored even when a narrow lane is used.
	if String(_data["shape"]) == "lane":
		draw_circle(center, 5.0, Color(PEACH_DARK.r, PEACH_DARK.g, PEACH_DARK.b, 0.9))

func _centroid(points: PackedVector2Array) -> Vector2:
	var center := Vector2.ZERO
	for point in points:
		center += point
	return center / float(maxi(1, points.size()))

func _perimeter_point(points: PackedVector2Array, ratio: float) -> Vector2:
	var lengths := 0.0
	for i in range(points.size()):
		lengths += points[i].distance_to(points[(i + 1) % points.size()])
	var target := lengths * clampf(ratio, 0.0, 1.0)
	var walked := 0.0
	for i in range(points.size()):
		var next := points[(i + 1) % points.size()]
		var segment := points[i].distance_to(next)
		if walked + segment >= target:
			return points[i].lerp(next, (target - walked) / maxf(0.01, segment))
		walked += segment
	return points[0]

func _has_safe_destination() -> bool:
	var safe: Vector2 = _data["safe_point"]
	return safe != Vector2.ZERO

func _draw_safe_pointer(active: bool) -> void:
	var safe: Vector2 = _data["safe_point"]
	var player: Vector2 = _data["player_point"]
	if player != Vector2.ZERO and player.distance_to(safe) > 20.0:
		draw_dashed_line(player, safe, Color(CYAN.r, CYAN.g, CYAN.b, 0.80),
			4.0, 12.0, true)
	draw_circle(safe, 19.0 if active else 15.0, Color(CYAN.r, CYAN.g, CYAN.b, 0.25))
	draw_circle(safe, 19.0 if active else 15.0, CYAN, false, 5.0)
	var diamond := PackedVector2Array([
		safe + Vector2(0.0, -12.0), safe + Vector2(12.0, 0.0),
		safe + Vector2(0.0, 12.0), safe + Vector2(-12.0, 0.0)])
	draw_colored_polygon(diamond, Color(CYAN.r, CYAN.g, CYAN.b, 0.9))

func _draw_pips() -> void:
	# Remaining boss rounds, separate from Roshan's performance stars.
	var center := Vector2(size.x * 0.5, 150.0)
	for i in range(3):
		var point := center + Vector2(float(i - 1) * 34.0, 0.0)
		var filled: bool = i < int(_data["puffs"])
		draw_circle(point, 11.0, CYAN if filled else PIP_EMPTY)
		draw_circle(point, 11.0, NAVY, false, 3.0)
