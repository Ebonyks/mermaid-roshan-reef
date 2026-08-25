class_name DayOneDustBunnySwimmer
extends Node2D
## Shared true-2D swimming dust bunny for the Day One pool and filled bathtub.

const SWIMMER_TEXTURE_PATH := \
	"res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png"

var _sprite: Sprite2D = null
var _swim_bounds := Rect2()
var _rest_position := Vector2.ZERO
var _travel := Vector2.ZERO
var _base_scale := Vector2.ONE
var _safe_center_bounds := Rect2()
var _footprint_center_offset := Vector2.ZERO
var _footprint_half_extents := Vector2.ZERO
var _ripple_size := Vector2.ZERO
var _ripple_color := Color(0.54, 0.93, 0.96, 0.32)
var _elapsed := 0.0


func setup(swim_bounds: Rect2, start_position: Vector2,
		display_width: float, travel: Vector2, depth_z: int,
		ripple_size: Vector2, ripple_color: Color = Color(
			0.54, 0.93, 0.96, 0.32)) -> bool:
	var texture: Texture2D = load(SWIMMER_TEXTURE_PATH) as Texture2D
	if texture == null:
		push_error("Missing Day One swimming dust bunny: %s" % SWIMMER_TEXTURE_PATH)
		return false
	name = "DayOneDustBunnySwimmer"
	_swim_bounds = swim_bounds
	_rest_position = Vector2(
		clampf(start_position.x, swim_bounds.position.x, swim_bounds.end.x),
		clampf(start_position.y, swim_bounds.position.y, swim_bounds.end.y))
	_travel = Vector2(maxf(travel.x, 0.0), maxf(travel.y, 0.0))
	_ripple_size = ripple_size
	_ripple_color = ripple_color
	position = _rest_position
	z_index = depth_z
	_sprite = Sprite2D.new()
	_sprite.name = "SwimmingDustBunnyCutout"
	_sprite.texture = texture
	_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_sprite.offset = Vector2(-38.0, 0.0)
	var safe_width: float = maxf(texture.get_size().x, 1.0)
	var uniform_scale: float = maxf(display_width, 1.0) / safe_width
	_base_scale = Vector2.ONE * uniform_scale
	# Reserve the largest possible paddle frame, including the authored body
	# offset and the maximum rotation. Movement clamps the complete visible
	# cutout, not just this Node2D's anchor, inside the owning water basin.
	_footprint_center_offset = _sprite.offset * _base_scale
	var half_size: Vector2 = texture.get_size() * _base_scale * 0.5
	half_size *= Vector2(1.015, 1.012)
	var max_rotation := 0.025
	_footprint_half_extents = Vector2(
		absf(cos(max_rotation)) * half_size.x
			+ absf(sin(max_rotation)) * half_size.y,
		absf(sin(max_rotation)) * half_size.x
			+ absf(cos(max_rotation)) * half_size.y)
	_footprint_half_extents += Vector2.ONE * (
		_footprint_center_offset.length() * sin(max_rotation))
	var safe_min := _swim_bounds.position + _footprint_half_extents \
		- _footprint_center_offset
	var safe_max := _swim_bounds.end - _footprint_half_extents \
		- _footprint_center_offset
	_safe_center_bounds = Rect2(safe_min, (safe_max - safe_min).max(Vector2.ZERO))
	_rest_position = Vector2(
		clampf(start_position.x, safe_min.x, safe_max.x),
		clampf(start_position.y, safe_min.y, safe_max.y))
	position = _rest_position
	_sprite.scale = _base_scale
	add_child(_sprite)
	set_meta("true_2d", true)
	set_meta("shared_swimmer_asset", SWIMMER_TEXTURE_PATH)
	set_meta("swim_bounds", _swim_bounds)
	set_meta("simple_animation", "bounded_bob_paddle")
	set_process(true)
	queue_redraw()
	return true


func audit_snapshot() -> Dictionary:
	var footprint := Rect2(
		position + _footprint_center_offset - _footprint_half_extents,
		_footprint_half_extents * 2.0)
	return {
		"present": _sprite != null and is_instance_valid(_sprite),
		"asset": SWIMMER_TEXTURE_PATH,
		"true_2d": true,
		"depth_z": z_index,
		"animation": "bounded_bob_paddle",
		"bounds": _swim_bounds,
		"position": position,
		"inside_bounds": _swim_bounds.has_point(position),
		"safe_center_bounds": _safe_center_bounds,
		"footprint": footprint,
		"fully_contained": not footprint.has_area()
			or _swim_bounds.encloses(footprint),
		"display_width": _sprite.texture.get_size().x * _base_scale.x
			if _sprite != null and _sprite.texture != null else 0.0,
		"visible": visible,
		"opacity": modulate.a,
	}


func fade_out(duration: float = 0.36) -> void:
	if not visible:
		return
	set_process(false)
	var fade: Tween = create_tween()
	fade.tween_property(self, "modulate:a", 0.0, maxf(duration, 0.01))
	fade.tween_callback(set_visible.bind(false))


func _process(delta: float) -> void:
	_elapsed += maxf(delta, 0.0)
	var desired := _rest_position + Vector2(
		sin(_elapsed * 0.72) * _travel.x,
		sin(_elapsed * 1.38 + 0.7) * _travel.y)
	position = Vector2(
		clampf(desired.x, _safe_center_bounds.position.x,
			_safe_center_bounds.end.x),
		clampf(desired.y, _safe_center_bounds.position.y,
			_safe_center_bounds.end.y))
	if _sprite == null:
		return
	var paddle: float = sin(_elapsed * 2.6)
	_sprite.rotation = paddle * 0.025
	_sprite.scale = _base_scale * Vector2(
		1.0 + paddle * 0.015, 1.0 - paddle * 0.012)


func _draw() -> void:
	if _ripple_size.x <= 0.0 or _ripple_size.y <= 0.0:
		return
	var radius: float = _ripple_size.x * 0.5
	var vertical_scale: float = _ripple_size.y / maxf(_ripple_size.x, 1.0)
	draw_set_transform(Vector2(0.0, 13.0), 0.0, Vector2(1.0, vertical_scale))
	draw_arc(Vector2.ZERO, radius, 0.0, TAU, 40, _ripple_color, 3.0, true)
	draw_arc(Vector2.ZERO, radius * 0.70, 0.15, TAU - 0.20, 32,
		Color(_ripple_color.r, _ripple_color.g, _ripple_color.b,
			_ripple_color.a * 0.68), 2.0, true)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
