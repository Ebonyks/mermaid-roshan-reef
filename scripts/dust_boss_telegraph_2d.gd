class_name DustBossTelegraph2D
extends "res://scripts/encounter_telegraph_2d.gd"

## Grand Puff gathers his own painted dust along the locked landing boundary.
## Geometry is inherited unchanged; this layer has no input or reward authority.
const DUST := preload("res://assets/opera/worlds/props/fx_dust_puff.png")
const MAX_EDGE_PUFFS: int = 48
var edge_points := PackedVector2Array()
var _edge_source := PackedVector2Array()
var _boss_floor := Vector2.ZERO
var _encounter_visible: bool = false
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
	super.set_telegraph(data)
	_boss_floor = _as_point(data.get("boss_point", Vector2.ZERO))
	_encounter_visible = bool(data.get("encounter_visible", false))
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
	# A quiet ink seam fixes the true edge; painted wisps supply the visual mass.
	# No growing outer countdown or filled rectangle changes the apparent hitbox.
	draw_polyline(_closed_points, Color(0.43, 0.32, 0.58, 0.58), 2.0, true)
	var gather: float = 1.0 if _active else _progress
	for i: int in edge_points.size():
		var phase: float = float(i) * 0.72 - _story_time * (3.0 if _active else 1.6)
		var breath: float = 0.5 + 0.5 * sin(phase)
		var inward: Vector2 = (_center - edge_points[i]).normalized()
		var point: Vector2 = edge_points[i] + inward * (3.0 + breath * 2.0)
		var width: float = 38.0 + gather * 6.0 + breath * 3.0
		_stamp(point, Vector2(width, width * 0.70), 0.65 + gather * 0.22)
	# Sparse moving wisps make the interior read as charged dust, not a UI bar.
	for i: int in range(3):
		var fraction: float = fmod(_story_time * 0.15 + float(i) / 3.0, 1.0)
		var edge: Vector2 = edge_points[(i * edge_points.size() / 3) % edge_points.size()]
		var point: Vector2 = edge.lerp(_center, 0.35 + fraction * 0.5)
		_stamp(point, Vector2(42.0, 20.0), sin(fraction * PI) * 0.22)

func _stamp(point: Vector2, dimensions: Vector2, alpha: float) -> void:
	draw_set_transform(point, 0.0, dimensions / DUST.get_size())
	draw_texture(DUST, -DUST.get_size() * 0.5, Color(1.0, 1.0, 1.0, alpha))
	draw_set_transform(Vector2.ZERO)
