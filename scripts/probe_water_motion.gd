extends SceneTree
# Headless contract for the two shared water presets and Sprite3D fallback.

const WaterMotionLogic = preload("res://scripts/water_motion.gd")

var failed := false


func _init() -> void:
	var still: ShaderMaterial = WaterMotionLogic.material(
		Color(0.1, 0.3, 0.5), Color(0.4, 0.8, 0.9),
		0.8, WaterMotionLogic.STILL, "speedy")
	var rough: ShaderMaterial = WaterMotionLogic.material(
		Color(0.1, 0.3, 0.5), Color(0.4, 0.8, 0.9),
		0.8, WaterMotionLogic.ROUGH, "speedy")
	_check(still.has_meta("reef_water_material"),
		"still material is registered as shared water")
	_check(String(still.get_meta("water_animation_preset")) == "still",
		"still preset identity")
	_check(String(rough.get_meta("water_animation_preset")) == "rough",
		"rough preset identity")
	_check(float(rough.get_shader_parameter("wobble_height")) >
		float(still.get_shader_parameter("wobble_height")),
		"rough water has the larger swell")
	_check(not bool(still.get_shader_parameter("use_depth")),
		"Speedy water avoids a depth-texture read")
	var sprite := Sprite3D.new()
	WaterMotionLogic.configure_sprite(sprite, WaterMotionLogic.STILL, 0.4)
	var base_scale: Vector3 = sprite.scale
	WaterMotionLogic.tick_sprite(sprite, 1.0)
	_check(sprite.scale != base_scale, "Sprite3D water fallback moves")
	print("WATER_MOTION|RESULT|", "FAIL" if failed else "OK")
	quit(1 if failed else 0)


func _check(ok: bool, label: String) -> void:
	print("WATER_MOTION|", label, "|", "OK" if ok else "FAIL")
	if not ok:
		failed = true
