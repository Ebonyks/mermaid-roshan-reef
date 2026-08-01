class_name WaterMotion
extends RefCounted
# Shared, Mobile-safe water motion language.
#
# Water surfaces are GPU animated. Jolt has no fluid surface solver, so it is
# reserved for the small physical Sprite3D/standee garnish fleet; making the
# water sheet itself a physics body would add solver work without improving
# the image. The two presets intentionally cover the whole game:
#   still - pools, fountains, baths and sheltered pond water
#   rough - ocean, fjords, rivers, moat and exposed lake water

const STILL := "still"
const ROUGH := "rough"
const WATER_SHADER: Shader = preload("res://assets/shaders/toon_water.gdshader")
const RIPPLE_TEXTURE: Texture2D = preload("res://assets/terrain/up_water_nrm.jpg")
const CAUSTICS_TEXTURE: Texture2D = preload("res://assets/terrain/caustics.png")

const PRESETS := {
	STILL: {
		"wobble_height": 0.07,
		"wobble_speed": 0.48,
		"scroll_speed": 0.015,
		"ripple_scale": 0.055,
		"normal_strength": 0.28,
		"wave_mix": 0.22,
		"surface_variation": 0.045,
		"crest_strength": 0.025,
		"sparkle": 0.20,
	},
	ROUGH: {
		"wobble_height": 0.42,
		"wobble_speed": 1.05,
		"scroll_speed": 0.052,
		"ripple_scale": 0.045,
		"normal_strength": 0.72,
		"wave_mix": 0.82,
		"surface_variation": 0.11,
		"crest_strength": 0.12,
		"sparkle": 0.38,
	},
}


static func material(deep: Color, shallow: Color, alpha: float,
		preset: String, quality: String, overrides: Dictionary = {}) -> ShaderMaterial:
	var resolved_preset: String = preset if PRESETS.has(preset) else STILL
	var settings: Dictionary = PRESETS[resolved_preset]
	var water := ShaderMaterial.new()
	water.shader = WATER_SHADER
	water.set_shader_parameter("deep_color", deep)
	water.set_shader_parameter("shallow_color", shallow)
	water.set_shader_parameter("alpha_base", alpha)
	water.set_shader_parameter("ripple", RIPPLE_TEXTURE)
	water.set_shader_parameter("caustics", CAUSTICS_TEXTURE)
	for key: String in settings:
		water.set_shader_parameter(key, settings[key])
	for key: String in overrides:
		water.set_shader_parameter(key, overrides[key])
	water.set_shader_parameter("use_depth",
		quality != "speedy" and DisplayServer.get_name() != "headless")
	water.set_meta("reef_water_material", true)
	water.set_meta("water_animation_preset", resolved_preset)
	return water


static func retune_tree(root: Node, quality: String) -> void:
	# Quality changes are rare, so a one-time tree walk is cheaper and safer
	# than retaining every arena material after its scene has been freed.
	if root == null:
		return
	var stack: Array[Node] = [root]
	var use_depth: bool = quality != "speedy" \
		and DisplayServer.get_name() != "headless"
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is GeometryInstance3D:
			var material_override: Material = \
				(node as GeometryInstance3D).material_override
			if material_override is ShaderMaterial \
					and material_override.has_meta("reef_water_material"):
				(material_override as ShaderMaterial).set_shader_parameter(
					"use_depth", use_depth)
		for child: Node in node.get_children():
			stack.append(child)


static func configure_sprite(sprite: Sprite3D, preset: String,
		phase: float = 0.0) -> void:
	if sprite == null:
		return
	var resolved_preset: String = preset if PRESETS.has(preset) else STILL
	sprite.set_meta("water_animation_preset", resolved_preset)
	sprite.set_meta("water_animation_phase", phase)
	sprite.set_meta("water_animation_base_position", sprite.position)
	sprite.set_meta("water_animation_base_scale", sprite.scale)
	sprite.set_meta("water_animation_base_rotation", sprite.rotation.z)


static func tick_sprite(sprite: Sprite3D, time: float) -> void:
	if sprite == null or not is_instance_valid(sprite) \
			or not sprite.has_meta("water_animation_preset"):
		return
	if bool(sprite.get_meta("busy", false)):
		return
	var preset: String = String(sprite.get_meta(
		"water_animation_preset", STILL))
	var phase: float = float(sprite.get_meta("water_animation_phase", 0.0))
	var base_position: Vector3 = sprite.get_meta(
		"water_animation_base_position", sprite.position)
	var base_scale: Vector3 = sprite.get_meta(
		"water_animation_base_scale", sprite.scale)
	var base_rotation: float = float(sprite.get_meta(
		"water_animation_base_rotation", sprite.rotation.z))
	var rough: bool = preset == ROUGH
	var speed: float = 1.25 if rough else 0.58
	var wave: float = sin(time * speed + phase)
	var counter_wave: float = sin(time * speed * 1.63 + phase + 1.4)
	var lift: float = 0.035 if rough else 0.012
	var stretch_x: float = 0.012 if rough else 0.004
	var stretch_y: float = 0.018 if rough else 0.006
	var rock: float = 0.006 if rough else 0.002
	sprite.position = base_position + Vector3(0.0, wave * lift, 0.0)
	sprite.scale = Vector3(
		base_scale.x * (1.0 + wave * stretch_x),
		base_scale.y * (1.0 - counter_wave * stretch_y),
		base_scale.z)
	sprite.rotation.z = base_rotation + counter_wave * rock
