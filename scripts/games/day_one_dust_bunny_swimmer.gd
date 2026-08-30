class_name DayOneDustBunnySwimmer
extends Node2D
## Shared true-2D swimming dust bunny for the Day One pool and filled bathtub.

signal comic_reaction_finished

const SWIMMER_TEXTURE_PATH := \
	"res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png"
const COMIC_REACTION_SECONDS := 0.68

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
var _waterline_uv := 1.0
var _reaction_active := false
var _reaction_count := 0
var _comic_no: Label = null


func setup(swim_bounds: Rect2, start_position: Vector2,
		display_width: float, travel: Vector2, depth_z: int,
		ripple_size: Vector2, ripple_color: Color = Color(
			0.54, 0.93, 0.96, 0.32), waterline_uv: float = 1.0) -> bool:
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
	_waterline_uv = clampf(waterline_uv, 0.45, 1.0)
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
	_apply_waterline_fade()
	add_child(_sprite)
	set_meta("true_2d", true)
	set_meta("shared_swimmer_asset", SWIMMER_TEXTURE_PATH)
	set_meta("swim_bounds", _swim_bounds)
	set_meta("simple_animation", "bounded_bob_paddle")
	set_meta("comic_reaction", "one_shot_spin_whee")
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
		"waterline_uv": _waterline_uv,
		"submerged_lower_body": _waterline_uv < 0.99,
		"drain_reaction_active": _reaction_active,
		"drain_reaction_count": _reaction_count,
		"drain_reaction_played_once": _reaction_count == 1,
		"reaction_duration_ms": int(COMIC_REACTION_SECONDS * 1000.0),
		"comic_shout": "WHEE!" if _reaction_count > 0 else "",
		"comic_no_visible": _comic_no != null
			and is_instance_valid(_comic_no) and _comic_no.visible,
	}


func play_comic_no() -> bool:
	if _sprite == null or not is_instance_valid(_sprite) \
			or _reaction_active or _reaction_count > 0:
		return false
	_reaction_active = true
	_reaction_count = 1
	set_process(false)
	_build_comic_no()
	var reaction: Tween = create_tween().set_parallel(true)
	reaction.tween_property(_sprite, "rotation", TAU * 2.0,
		COMIC_REACTION_SECONDS).set_trans(Tween.TRANS_BACK).set_ease(
		Tween.EASE_IN_OUT)
	reaction.tween_property(_sprite, "scale", _base_scale * Vector2(1.10, 0.90),
		0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	reaction.tween_property(self, "position:y", _rest_position.y - 12.0,
		0.20).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	reaction.chain().tween_callback(_finish_comic_no)
	return true


func fade_out(duration: float = 0.36) -> void:
	if not visible:
		return
	set_process(false)
	var fade: Tween = create_tween()
	fade.tween_property(self, "modulate:a", 0.0, maxf(duration, 0.01))
	fade.tween_callback(set_visible.bind(false))


func _apply_waterline_fade() -> void:
	if _sprite == null or _waterline_uv >= 0.99:
		return
	var shader := Shader.new()
	shader.code = "shader_type canvas_item;\n" \
		+ "uniform float waterline_uv = 0.70;\n" \
		+ "void fragment() {\n" \
		+ "  vec4 pixel = texture(TEXTURE, UV);\n" \
		+ "  float water_fade = 1.0 - smoothstep(waterline_uv, " \
		+ "waterline_uv + 0.18, UV.y);\n" \
		+ "  COLOR = vec4(pixel.rgb, pixel.a * water_fade);\n" \
		+ "}\n"
	var material := ShaderMaterial.new()
	material.shader = shader
	material.set_shader_parameter("waterline_uv", _waterline_uv)
	_sprite.material = material


func _build_comic_no() -> void:
	_comic_no = Label.new()
	_comic_no.name = "ComicNoBurst"
	# The drain is a required success beat, so its comic reaction celebrates
	# motion instead of suggesting that the child's correct tap was a failure.
	_comic_no.text = "WHEE!"
	_comic_no.position = Vector2(24.0, -86.0)
	_comic_no.pivot_offset = Vector2(36.0, 24.0)
	_comic_no.scale = Vector2.ONE * 0.45
	_comic_no.z_index = 4
	_comic_no.add_theme_font_size_override("font_size", 42)
	_comic_no.add_theme_color_override("font_color", Color(1.0, 0.82, 0.24))
	_comic_no.add_theme_color_override("font_outline_color",
		Color(0.24, 0.10, 0.42))
	_comic_no.add_theme_constant_override("outline_size", 8)
	add_child(_comic_no)
	var pop: Tween = _comic_no.create_tween()
	pop.tween_property(_comic_no, "scale", Vector2.ONE, 0.18) \
		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	pop.tween_interval(0.20)
	pop.tween_property(_comic_no, "modulate:a", 0.0, 0.24)


func _finish_comic_no() -> void:
	position = _rest_position
	if _sprite != null and is_instance_valid(_sprite):
		_sprite.rotation = 0.0
		_sprite.scale = _base_scale
	_reaction_active = false
	if _comic_no != null and is_instance_valid(_comic_no):
		_comic_no.queue_free()
	_comic_no = null
	set_process(true)
	comic_reaction_finished.emit()


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
