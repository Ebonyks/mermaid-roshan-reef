class_name RainbowSliceEffect
extends Node2D

# One generated, alpha-backed brush ribbon is stretched only along the swipe's
# measured screen-space segment. The line width stays equal to the gameplay
# band, so the flourish never promises reach that the slice does not have.
const TEXTURE: Texture2D = preload("res://assets/fx/combat/rainbow_slice.png")
const SPARKLE_SHADER: Shader = preload("res://shaders/rainbow_slice_sparkle.gdshader")
const REVEAL_T := 0.075
const ACTIVE_ALPHA := 0.78
const SPENT_COLOR := Color(0.72, 0.74, 0.80, 0.30)
const SPARKLE_MIN := 4
const SPARKLE_MAX := 8

var visual_length := 0.0
var visual_width := 0.0
var spent := false
var stripe: Line2D = null
var sparkle_count := 0
var sparkle_seed := 0
var sparkle_positions: Array[Vector2] = []
var sparkles: Node2D = null
var sparkle_material: ShaderMaterial = null

func configure(from: Vector2, to: Vector2, width: float, lifetime: float,
		is_spent: bool = false, seed_value: int = 1) -> void:
	position = from
	var span: Vector2 = to - from
	visual_length = span.length()
	visual_width = width
	spent = is_spent
	rotation = span.angle()

	stripe = Line2D.new()
	stripe.width = width
	stripe.begin_cap_mode = Line2D.LINE_CAP_ROUND
	stripe.end_cap_mode = Line2D.LINE_CAP_ROUND
	stripe.points = PackedVector2Array([Vector2.ZERO, Vector2(visual_length, 0.0)])
	if spent:
		stripe.default_color = SPENT_COLOR
	else:
		stripe.texture = TEXTURE
		stripe.texture_mode = Line2D.LINE_TEXTURE_STRETCH
		stripe.modulate.a = ACTIVE_ALPHA
	add_child(stripe)
	if not spent:
		_add_sparkles(seed_value, lifetime)

	# The painted slash races outward from the child's finger, flashes at full
	# reach, then clears quickly enough to keep the next target readable.
	stripe.scale = Vector2(0.08, 1.0)
	var tween: Tween = create_tween()
	tween.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(stripe, "scale:x", 1.0, REVEAL_T)
	tween.tween_property(stripe, "modulate:a", 0.0, maxf(0.01, lifetime - REVEAL_T))
	tween.tween_callback(queue_free)

func _add_sparkles(seed_value: int, lifetime: float) -> void:
	sparkle_seed = seed_value
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value
	sparkle_count = clampi(int(round(visual_length / 70.0)) + 2,
		SPARKLE_MIN, SPARKLE_MAX)
	sparkles = Node2D.new()
	sparkles.name = "IridescentSparkles"
	add_child(sparkles)
	# Screen position already gives every glint a distinct point in the color
	# wave, so one shared material per slice keeps draw-state churn bounded.
	sparkle_material = ShaderMaterial.new()
	sparkle_material.shader = SPARKLE_SHADER
	sparkle_material.set_shader_parameter("phase", rng.randf())
	for index in range(sparkle_count):
		# Even cells keep the whole swipe lively; seeded jitter makes consecutive
		# slices distinct without clustering every glint at one end.
		var cell_t: float = (float(index) + rng.randf_range(0.22, 0.78)) \
			/ float(sparkle_count)
		var center := Vector2(
			visual_length * lerpf(0.08, 0.92, cell_t),
			rng.randf_range(-visual_width * 0.22, visual_width * 0.22))
		var radius: float = rng.randf_range(7.0, minf(14.0, visual_width * 0.13))
		var sparkle := Polygon2D.new()
		sparkle.name = "Sparkle%d" % index
		sparkle.polygon = _star_points(radius)
		sparkle.color = Color(1.0, 0.96, 0.84, 0.94)
		sparkle.position = center
		sparkle.rotation = rng.randf_range(-0.22, 0.22)
		sparkle.material = sparkle_material
		sparkles.add_child(sparkle)
		sparkle_positions.append(center)

		# Glints arrive just behind the painted reveal at their point on the line.
		var delay: float = REVEAL_T * cell_t * 0.85
		sparkle.scale = Vector2(0.08, 0.08)
		sparkle.modulate.a = 0.0
		var tween: Tween = sparkle.create_tween()
		tween.tween_interval(delay)
		tween.set_parallel(true)
		tween.tween_property(sparkle, "scale", Vector2.ONE, 0.055) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		tween.tween_property(sparkle, "modulate:a", 1.0, 0.035)
		tween.set_parallel(false)
		tween.tween_property(sparkle, "scale", Vector2(0.62, 0.62),
			maxf(0.02, lifetime - delay - 0.055))
		tween.parallel().tween_property(sparkle, "modulate:a", 0.0,
			maxf(0.02, lifetime - delay - 0.055))

func _star_points(radius: float) -> PackedVector2Array:
	var waist: float = radius * 0.22
	return PackedVector2Array([
		Vector2(0.0, -radius), Vector2(waist, -waist),
		Vector2(radius, 0.0), Vector2(waist, waist),
		Vector2(0.0, radius), Vector2(-waist, waist),
		Vector2(-radius, 0.0), Vector2(-waist, -waist),
	])
