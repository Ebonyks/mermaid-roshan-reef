class_name EncounterNavigation2D
extends RefCounted

## Tap-to-go in a host's 2D play space. The four-corner homography also bridges
## existing projected stages without adding spatial world logic to new modes.
var destination := Vector2.ZERO
var travelling: bool = false
var bounds := Rect2(-26.0, -26.0, 52.0, 52.0)
var _a: float = 1.0
var _b: float = 0.0
var _c: float = 0.0
var _d: float = 0.0
var _e: float = 1.0
var _f: float = 0.0
var _g: float = 0.0
var _h: float = 0.0

func set_projection(area: Rect2, corners: PackedVector2Array) -> void:
	if corners.size() != 4:
		return
	bounds = area
	var p0: Vector2 = corners[0]
	var p1: Vector2 = corners[1]
	var p2: Vector2 = corners[2]
	var p3: Vector2 = corners[3]
	var dx1: float = p1.x - p2.x
	var dx2: float = p3.x - p2.x
	var dx3: float = p0.x - p1.x + p2.x - p3.x
	var dy1: float = p1.y - p2.y
	var dy2: float = p3.y - p2.y
	var dy3: float = p0.y - p1.y + p2.y - p3.y
	var denominator: float = dx1 * dy2 - dx2 * dy1
	_g = 0.0
	_h = 0.0
	if absf(denominator) > 0.0001:
		_g = (dx3 * dy2 - dx2 * dy3) / denominator
		_h = (dx1 * dy3 - dx3 * dy1) / denominator
	_a = p1.x - p0.x + _g * p1.x
	_b = p3.x - p0.x + _h * p3.x
	_c = p0.x
	_d = p1.y - p0.y + _g * p1.y
	_e = p3.y - p0.y + _h * p3.y
	_f = p0.y

func screen_to_floor(point: Vector2) -> Vector2:
	var a: float = _a - point.x * _g
	var b: float = _b - point.x * _h
	var d: float = _d - point.y * _g
	var e: float = _e - point.y * _h
	var x: float = point.x - _c
	var y: float = point.y - _f
	var determinant: float = a * e - b * d
	if absf(determinant) < 0.0001:
		return bounds.get_center()
	var uv := Vector2((x * e - b * y) / determinant,
		(a * y - x * d) / determinant)
	return bounds.position + uv * bounds.size

func move_to(point: Vector2) -> void:
	destination = point
	travelling = true

func cancel() -> void:
	travelling = false

func direction_for_step(current: Vector2, speed: float, delta: float) -> Vector2:
	if not travelling:
		return Vector2.ZERO
	var offset: Vector2 = destination - current
	if offset.length() <= 0.12:
		travelling = false
		return Vector2.ZERO
	return offset / maxf(offset.length(), maxf(speed * delta, 0.001))
