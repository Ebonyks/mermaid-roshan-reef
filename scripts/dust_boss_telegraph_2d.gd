class_name DustBossTelegraph2D
extends "res://scripts/encounter_telegraph_2d.gd"

## The encounter supplies a locked footprint and its clocks. This Canvas
## layer draws the warning and carries the sneeze to its locked target.
const DUST := preload("res://assets/opera/worlds/props/fx_dust_puff.png")
const GERM := preload("res://assets/effects/grand_puff/cold_germ.svg")
const GOO := preload("res://assets/effects/grand_puff/cold_goo.svg")
const SNEEZE := preload("res://assets/audio/sfx/grand_puff_sneeze.ogg")
const MIST := Color("c3f3df")
const INK := Color("2c5862")
const LOCK_LIGHT := Color("d3fff2")
const MAX_EDGE_PUFFS: int = 48
const RELEASE_AT: float = 0.25
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
var _strike_progress: float = 0.0
var _released: bool = false
var _release_from := Vector2.ZERO
var _landing_point := Vector2.ZERO
var _release_side: float = -1.0
var _cold_sfx: AudioStreamPlayer

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if draw_overlay:
		_cold_sfx = AudioStreamPlayer.new()
		_cold_sfx.name = "GrandPuffColdSfx"
		_cold_sfx.bus = &"SFX"
		_cold_sfx.volume_db = -9.0
		add_child(_cold_sfx)

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
	if draw_overlay:
		var default_landing: Vector2 = _points[1].lerp(_points[2], 0.5) \
			if _shape == "lane" and _points.size() == 4 else _center
		_landing_point = _as_point(data.get("landing_point", default_landing))
		_strike_progress = clampf(float(data.get("strike_progress", 0.0)), 0.0, 1.0)
		if not _visible or not _active:
			_released = false
		elif not _released and _strike_progress >= RELEASE_AT:
			# Freeze the painted plume socket on release. The moving actor and
			# player cannot drag either end of an already airborne puff.
			_release_from = _as_point(data.get("plume_point", _boss_floor))
			_release_side = float(data.get("plume_side", -1.0))
			_released = true
			if _cold_sfx != null:
				_cold_sfx.stream = SNEEZE
				_cold_sfx.pitch_scale = 0.92 if _shape == "lane" else 1.0
				_cold_sfx.play()

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
	if not _encounter_visible:
		return
	if draw_overlay and _released and _active and _visible:
		_draw_germ_flight()
	if not draw_floor:
		return
	# These dust banks still mean cleaning progress, separate from cold clouds.
	for i: int in maxi(0, _total - _puffs):
		var offset := Vector2(float(i - 1) * 24.0, 5.0 + sin(_story_time * 1.6 + float(i)) * 2.0)
		_stamp(DUST, _boss_floor + offset, Vector2(43.0, 22.0), Color(1, 1, 1, 0.52))
	if _shed_time > 0.0:
		var flight: float = 1.0 - _shed_time / 0.85
		for i: int in range(3):
			var point: Vector2 = _shed_from + Vector2((float(i) - 1.0) * flight * 85.0,
				-sin(flight * PI) * 38.0 + flight * 15.0)
			_stamp(DUST, point, Vector2(34.0, 24.0) * (1.0 + flight * 0.4),
				Color(1, 1, 1, (1.0 - flight) * 0.7))
	if _visible and not edge_points.is_empty():
		_draw_danger()

func _draw_danger() -> void:
	var arrival: float = EncounterWarningCue2D.aim_progress(_progress)
	var locked: bool = EncounterWarningCue2D.is_locked(_progress) or _active
	var flash: float = EncounterWarningCue2D.lock_brightness(_progress, _active)
	var urgency: float = EncounterWarningCue2D.imminence(_progress, _active)
	var outline := PackedVector2Array()
	if _shape == "lane" and _points.size() == 4:
		if arrival < 0.02:
			_stamp(DUST, _launch_origin, Vector2(35, 23), Color(MIST, 0.55))
			return
		outline = PackedVector2Array([_points[0], _points[0].lerp(_points[1], arrival),
			_points[3].lerp(_points[2], arrival), _points[3]])
	else:
		var center: Vector2 = warning_center()
		for point: Vector2 in _points:
			outline.append(center + (point - _center) * lerpf(0.28, 1.0, arrival))
	draw_colored_polygon(outline, Color(MIST, 0.12 + flash * 0.12))
	outline.append(outline[0])
	var ink: Color = INK.lerp(Color("ad5162"), urgency)
	draw_polyline(outline, Color(ink, 0.70 + flash * 0.24), 3.0 + urgency, true)
	if locked:
		var rim: Color = LOCK_LIGHT.lerp(Color("ffcaa1"), urgency)
		draw_polyline(outline, Color(rim, 0.48 + flash * 0.46), 1.35, true)

func warning_center() -> Vector2:
	var arrival: float = EncounterWarningCue2D.aim_progress(_progress)
	var bend: Vector2 = (_center - _launch_origin).normalized().orthogonal()
	return _launch_origin.lerp(_center, arrival) + bend * sin(arrival * PI) * 22.0

func release_target() -> Vector2:
	return _landing_point

func _draw_germ_flight() -> void:
	var travel: float = inverse_lerp(RELEASE_AT, 1.0, _strike_progress)
	var target: Vector2 = release_target()
	var wide: bool = _shape == "lane"
	# Draw the trailing drops first, then the large, readable leading glob.
	for i: int in range(3, -1, -1):
		var t: float = travel - float(i) * 0.11
		if t < 0.0:
			continue
		var point: Vector2 = _germ_path(target, t)
		var spread: float = sin(t * PI) * float(i)
		point += Vector2(-_release_side * 6.0, -5.0) * spread
		var edge: float = lerpf(29.0, 74.0 if wide else 64.0, t) / (1.0 + float(i) * 0.66)
		var angle: float = (_germ_path(target, t + 0.01) - _germ_path(target, t)).angle()
		_stamp(GOO, point, Vector2(edge, edge * 0.84), Color.WHITE, angle)
		if i > 0:
			_stamp(GERM, point + Vector2(-_release_side * 12.0, -11.0) * sin(t * PI),
				Vector2.ONE * (13.0 + spread), Color.WHITE, t * 2.0)

func _germ_path(target: Vector2, progress: float) -> Vector2:
	var outward: float = 8.0 if _shape == "lane" else 34.0
	return _release_from.lerp(target, progress) \
		+ Vector2(_release_side * outward, -24.0) * sin(progress * PI)

func _stamp(texture: Texture2D, point: Vector2, dimensions: Vector2,
		tint: Color, rotation: float = 0.0) -> void:
	draw_set_transform(point, rotation, dimensions / texture.get_size())
	draw_texture(texture, -texture.get_size() * 0.5, tint)
	draw_set_transform(Vector2.ZERO)
