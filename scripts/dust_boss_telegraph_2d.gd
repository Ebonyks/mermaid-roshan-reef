class_name DustBossTelegraph2D
extends "res://scripts/encounter_telegraph_2d.gd"

## Grand Puff sends a purple aiming cue from his feet, locks it, then attacks.
## Geometry is inherited unchanged; this layer has no input or reward authority.
const DUST := preload("res://assets/opera/worlds/props/fx_dust_puff.png")
const VORTEX := preload("res://assets/effects/grand_puff/purple_vortex_v4.png")
const INK := Color("594273")
const LILAC := Color("dfc9ee")
const MAX_EDGE_PUFFS: int = 48
var edge_points := PackedVector2Array()
var _edge_source := PackedVector2Array()
var _boss_floor := Vector2.ZERO
var _encounter_visible: bool = false
var _shape: String = "circle"
var _launch_origin := Vector2.ZERO
var _was_warning: bool = false
var _story_time: float = 0.0
var _shed_time: float = 0.0
var _shed_from := Vector2.ZERO
var _story_redraw: float = 0.0

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func set_telegraph(data: Dictionary) -> void:
	var previous_rounds: int = _puffs
	var starting: bool = bool(data.get("visible", false)) and (not _was_warning or (_active and not bool(data.get("active", false))))
	super.set_telegraph(data)
	_boss_floor = _as_point(data.get("boss_point", Vector2.ZERO))
	_encounter_visible = bool(data.get("encounter_visible", false))
	_shape = String(data.get("shape", "circle"))
	if starting:
		_launch_origin = _boss_floor
	_was_warning = _visible
	if _puffs > previous_rounds:
		_shed_time = 0.85
		_shed_from = _boss_floor
	if _edge_source != _points:
		_edge_source = PackedVector2Array(_points)
		_cache_edge_points()

func _cache_edge_points() -> void:
	edge_points.clear()
	if _points.size() < 3:
		return
	var perimeter: float = 0.0
	for i: int in _points.size():
		perimeter += _points[i].distance_to(_points[(i + 1) % _points.size()])
	var count: int = clampi(ceili(perimeter / 30.0), 16, MAX_EDGE_PUFFS)
	var segment: int = 0
	var consumed: float = 0.0
	for i: int in count:
		var distance: float = perimeter * float(i) / float(count)
		var length: float = _points[segment].distance_to(_points[(segment + 1) % _points.size()])
		while consumed + length < distance and segment < _points.size() - 1:
			consumed += length
			segment += 1
			length = _points[segment].distance_to(_points[(segment + 1) % _points.size()])
		edge_points.append(_points[segment].lerp(_points[(segment + 1) % _points.size()],
			clampf((distance - consumed) / maxf(length, 0.01), 0.0, 1.0)))

func _process(delta: float) -> void:
	_story_time += delta
	_shed_time = maxf(0.0, _shed_time - delta)
	_story_redraw += delta
	if _story_redraw >= 1.0 / 30.0:
		_story_redraw = fmod(_story_redraw, 1.0 / 30.0)
		queue_redraw()

func _draw() -> void:
	if not draw_floor or not _encounter_visible:
		return
	# Three small banks of his own dust replace the detached progress display.
	# Each earned exchange sheds one; the boss's authored reaction owns the beat.
	for i: int in maxi(0, _total - _puffs):
		var offset := Vector2(float(i - 1) * 24.0, 5.0 + sin(_story_time * 1.6 + float(i)) * 2.0)
		_stamp(_boss_floor + offset, Vector2(43.0, 22.0), 0.52)
	if _shed_time > 0.0:
		var flight: float = 1.0 - _shed_time / 0.85
		for i: int in range(3):
			var point: Vector2 = _shed_from + Vector2((float(i) - 1.0) * flight * 85.0,
				-sin(flight * PI) * 38.0 + flight * 15.0)
			_stamp(point, Vector2(34.0, 24.0) * (1.0 + flight * 0.4), (1.0 - flight) * 0.7)
	if _visible and not edge_points.is_empty():
		_draw_danger()

func _draw_danger() -> void:
	var arrival: float = EncounterWarningCue2D.aim_progress(_progress)
	var locked: bool = EncounterWarningCue2D.is_locked(_progress) or _active
	var flash: float = EncounterWarningCue2D.lock_brightness(_progress, _active)
	if _shape == "lane" and _points.size() == 4:
		_draw_charge(arrival, locked, flash)
	else:
		_draw_jump(arrival, locked, flash)

func warning_center() -> Vector2:
	var arrival: float = EncounterWarningCue2D.aim_progress(_progress)
	var bend: Vector2 = (_center - _launch_origin).normalized().orthogonal()
	return _launch_origin.lerp(_center, arrival) + bend * sin(arrival * PI) * 22.0

func _painted_stroke(path: PackedVector2Array, widths: PackedFloat32Array, flash: float, strength: float = 1.0) -> void:
	if path.size() < 2:
		return
	var left := PackedVector2Array()
	var right := PackedVector2Array()
	for i: int in path.size():
		var tangent: Vector2 = path[mini(i + 1, path.size() - 1)] - path[maxi(0, i - 1)]
		var normal: Vector2 = tangent.normalized().orthogonal()
		left.append(path[i] + normal * widths[i])
		right.append(path[i] - normal * widths[i])
	# Explicit short quads avoid triangulating a long concave spiral.
	var light := Color(0.78 + flash * 0.16, 0.73 + flash * 0.19, 0.90 + flash * 0.10, 0.94)
	var shade := Color(0.65 + flash * 0.18, 0.57 + flash * 0.22, 0.79 + flash * 0.17, 0.94)
	light *= _attack_tint()
	shade *= _attack_tint()
	light.a *= strength
	shade.a *= strength
	for i: int in range(path.size() - 1):
		if path[i].distance_squared_to(path[i + 1]) < 0.001:
			continue
		# Reuse the opaque painted core as the stream material; no repeated stamps.
		var u0: float = lerpf(0.40, 0.60, float(i) / float(path.size() - 1))
		var u1: float = lerpf(0.40, 0.60, float(i + 1) / float(path.size() - 1))
		draw_primitive(PackedVector2Array([left[i], left[i + 1], right[i + 1], right[i]]),
			PackedColorArray([light, light, shade, shade]),
			PackedVector2Array([Vector2(u0, 0.72), Vector2(u1, 0.72),
				Vector2(u1, 0.80), Vector2(u0, 0.80)]), VORTEX)
	var contour := PackedVector2Array(left)
	for i: int in range(right.size() - 1, -1, -1):
		contour.append(right[i])
	contour.append(contour[0])
	draw_polyline(contour, Color(_attack_ink(), 0.66 * strength), 2.0 + _imminence() * 0.8, true)

func _draw_jump(arrival: float, locked: bool, flash: float) -> void:
	var center: Vector2 = warning_center()
	var scale: float = lerpf(0.28, 1.0, arrival)
	var axis_x: Vector2 = (_points[0] - _points[_points.size() / 2]) * 0.5 * scale
	var axis_y: Vector2 = (_points[_points.size() / 4] - _points[_points.size() * 3 / 4]) * 0.5 * scale
	var outline := PackedVector2Array()
	for point: Vector2 in _closed_points:
		outline.append(center + (point - _center) * scale)
	draw_colored_polygon(outline, Color(0.66, 0.48, 0.79, 0.10 + flash * 0.11))
	if locked:
		draw_polyline(outline, Color(_attack_ink(), 0.45 + flash * 0.24), 2.4 + _imminence() * 1.6, true)
		draw_polyline(outline, Color(_attack_light(), flash * 0.65), 1.2, true)
	_draw_vortex(center, axis_x * 1.02, axis_y * 1.02, arrival * TAU * 1.5,
		flash if locked else 0.35)
	if not locked:
		for i: int in range(3):
			var lag: float = maxf(0.0, arrival - 0.07 * float(i + 1))
			var bend: Vector2 = (_center - _launch_origin).normalized().orthogonal()
			var point: Vector2 = _launch_origin.lerp(_center, lag) + bend * sin(lag * PI) * 22.0
			_stamp(point + Vector2(0, 7), Vector2(25, 14) * (1.0 - float(i) * 0.17), (1.0 - arrival) * 0.32)

func _lane_point(along: float, across: float) -> Vector2:
	return _points[0].lerp(_points[1], along).lerp(_points[3].lerp(_points[2], along), across)

func _draw_charge(arrival: float, locked: bool, flash: float) -> void:
	if arrival < 0.02:
		_stamp(_launch_origin, Vector2(24, 14), 0.3)
		return
	if locked:
		draw_colored_polygon(_points, Color(0.61, 0.43, 0.75, 0.08 + flash * 0.09))
		draw_polyline(_closed_points, Color(_attack_ink(), 0.15 + flash * 0.20 + _imminence() * 0.16), 2.0 + _imminence(), true)
	for side: int in range(2):
		var ribbon := PackedVector2Array()
		var widths := PackedFloat32Array()
		for i: int in range(33):
			var t: float = float(i) / 32.0
			var along: float = arrival * t
			var inset: float = 0.045 + sin(t * PI) * 0.06 + sin(t * TAU * 1.3) * 0.012
			var across: float = inset if side == 0 else 1.0 - inset
			across = lerpf(across, 0.5, smoothstep(0.70, 1.0, t) * 0.32)
			var point: Vector2 = _lane_point(along, across)
			var gather: float = smoothstep(0.0, 0.18, t) * smoothstep(0.0, 0.25, arrival)
			point = _launch_origin.lerp(point, gather)
			ribbon.append(point)
			widths.append((0.6 + pow(maxf(0.0, sin(t * PI)), 0.7) * 9.0) * smoothstep(0.0, 0.10, arrival))
		_painted_stroke(ribbon, widths, flash)
	# Broad painted crests unfold in order; no tiny repeated dust stamps.
	for wave: int in range(2):
		var unfold: float = smoothstep(0.13 + float(wave) * 0.20, 0.48 + float(wave) * 0.20, arrival)
		if unfold > 0.02:
			_draw_charge_cloud(arrival * (0.39 + float(wave) * 0.25),
				0.40 * unfold, 0.045 * unfold, 0.44 * unfold, flash)
	var opening: float = smoothstep(0.30, 1.0, arrival)
	if opening > 0.02:
		_draw_charge_cloud(arrival - opening * 0.060,
			0.50 * opening, 0.095 * opening, opening, flash)

func _draw_charge_cloud(along: float, span: float, depth: float,
		strength: float, flash: float) -> void:
	var center: Vector2 = _lane_point(along, 0.5)
	var across: Vector2 = (_lane_point(along, 1.0) - _lane_point(along, 0.0)) * span
	var backwards: Vector2 = (_lane_point(0.0, 0.5) - _lane_point(1.0, 0.5)) * depth
	var quad := PackedVector2Array([center - across - backwards,
		center + across - backwards, center + across + backwards, center - across + backwards])
	var tint := Color(0.68 + flash * 0.16, 0.55 + flash * 0.20,
		0.92 + flash * 0.08, strength * (0.80 + flash * 0.20))
	tint *= _attack_tint()
	draw_polygon(quad, PackedColorArray([tint, tint, tint, tint]),
		PackedVector2Array([Vector2.ZERO, Vector2.RIGHT, Vector2.ONE, Vector2.DOWN]), DUST)

func _draw_vortex(center: Vector2, axis_x: Vector2, axis_y: Vector2,
		angle: float, flash: float) -> void:
	var quad := PackedVector2Array()
	var uv := PackedVector2Array([Vector2.ZERO, Vector2.RIGHT, Vector2.ONE, Vector2.DOWN])
	for corner: Vector2 in [Vector2(-1, -1), Vector2(1, -1), Vector2(1, 1), Vector2(-1, 1)]:
		var turned: Vector2 = corner.rotated(angle)
		quad.append(center + axis_x * turned.x + axis_y * turned.y)
	var tint := Color(lerpf(0.70, 1.0, flash), lerpf(0.65, 1.0, flash),
		lerpf(0.86, 1.0, flash), lerpf(0.82, 1.0, flash))
	tint *= _attack_tint()
	draw_polygon(quad, PackedColorArray([tint, tint, tint, tint]), uv, VORTEX)

func _imminence() -> float:
	return EncounterWarningCue2D.imminence(_progress, _active)

func _attack_tint() -> Color:
	return Color.WHITE.lerp(Color(1.22, 0.98, 0.58), _imminence())

func _attack_ink() -> Color:
	return INK.lerp(Color("a84958"), _imminence())

func _attack_light() -> Color:
	return LILAC.lerp(Color("ffc29c"), _imminence())

func _stamp(point: Vector2, dimensions: Vector2, alpha: float, tint: Color = Color.WHITE) -> void:
	draw_set_transform(point, 0.0, dimensions / DUST.get_size())
	draw_texture(DUST, -DUST.get_size() * 0.5, Color(tint, alpha))
	draw_set_transform(Vector2.ZERO)
