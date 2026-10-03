class_name DayOneFixtureScrub
extends Polygon2D
## Reveals the existing clean fixture only along the child's live tool path.
## The dirty room stays underneath; no source artwork is edited or replaced.

const MASK_SCALE := 0.25
const BRUSH_RADIUS := 32.0
const SCRUB_SHADER := """
shader_type canvas_item;
render_mode unshaded;
uniform sampler2D scrub_mask : filter_linear, repeat_disable;
uniform bool dirt_layer = false;
uniform vec2 mask_origin = vec2(0.0);
uniform vec2 mask_extent = vec2(1.0);
void fragment() {
	float cleaned = texture(scrub_mask, mask_origin + UV * mask_extent).r;
	COLOR.a *= dirt_layer ? 1.0 - cleaned : cleaned;
}
"""

var has_scrub_marks: bool = false
var is_clean: bool = false
var _mask: Image = null
var _mask_texture: ImageTexture = null
var _grime: Sprite2D = null


func setup_scrub(clean: bool) -> void:
	if clean:
		finish_scrub()
		return
	var mask_size: Vector2i = Vector2i(texture.get_size() * MASK_SCALE)
	_mask = Image.create(mask_size.x, mask_size.y, false, Image.FORMAT_L8)
	_mask.fill(Color.BLACK)
	_mask_texture = ImageTexture.create_from_image(_mask)
	var shader := Shader.new()
	shader.code = SCRUB_SHADER
	var scrub_material := ShaderMaterial.new()
	scrub_material.shader = shader
	scrub_material.set_shader_parameter("scrub_mask", _mask_texture)
	material = scrub_material
	# Draw the zero-alpha mask at room entry, warming the shader before touch.
	visible = true


func scrub_segment(from: Vector2, to: Vector2) -> void:
	if is_clean or _mask == null:
		return
	var start: Vector2 = from * MASK_SCALE
	var end: Vector2 = to * MASK_SCALE
	var radius: float = BRUSH_RADIUS * MASK_SCALE
	var low: Vector2i = Vector2i((start.min(end) - Vector2.ONE * radius).floor())
	var high: Vector2i = Vector2i((start.max(end) + Vector2.ONE * radius).ceil())
	var changed: bool = false
	for y: int in range(maxi(0, low.y), mini(_mask.get_height(), high.y + 1)):
		for x: int in range(maxi(0, low.x), mini(_mask.get_width(), high.x + 1)):
			var pixel := Vector2(x, y)
			var nearest: Vector2 = Geometry2D.get_closest_point_to_segment(pixel, start, end)
			var strength: float = 1.0 - smoothstep(radius * 0.7, radius,
				pixel.distance_to(nearest))
			# Keep the last residue until the intentional gesture gate completes.
			strength = minf(strength, 0.96)
			if strength > _mask.get_pixel(x, y).r:
				_mask.set_pixel(x, y, Color(strength, strength, strength))
				changed = true
	if changed:
		has_scrub_marks = true
		_mask_texture.update(_mask)
		visible = true


func finish_scrub() -> void:
	is_clean = true
	visible = true
	material = null
	if is_instance_valid(_grime):
		_grime.material = null
	_grime = null
	_mask = null
	_mask_texture = null


func mask_grime(grime: Sprite2D) -> void:
	if is_clean or not is_instance_valid(grime) or _mask_texture == null:
		return
	_grime = grime
	var grime_material: ShaderMaterial = grime.material as ShaderMaterial
	if grime_material == null:
		grime_material = ShaderMaterial.new()
		grime_material.shader = (material as ShaderMaterial).shader
		grime.material = grime_material
	var half_size: Vector2 = grime.texture.get_size() * 0.5
	var origin: Vector2 = to_local(grime.to_global(-half_size)) / texture.get_size()
	var end: Vector2 = to_local(grime.to_global(half_size)) / texture.get_size()
	grime_material.set_shader_parameter("scrub_mask", _mask_texture)
	grime_material.set_shader_parameter("dirt_layer", true)
	grime_material.set_shader_parameter("mask_origin", origin)
	grime_material.set_shader_parameter("mask_extent", end - origin)


func reveal_at(source_point: Vector2) -> float:
	if is_clean:
		return 1.0
	if _mask == null:
		return 0.0
	var pixel: Vector2i = Vector2i(source_point * MASK_SCALE)
	if pixel.x < 0 or pixel.y < 0 or pixel.x >= _mask.get_width() \
			or pixel.y >= _mask.get_height():
		return 0.0
	return _mask.get_pixel(pixel.x, pixel.y).r
