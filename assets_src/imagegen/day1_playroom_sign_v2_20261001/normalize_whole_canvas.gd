extends SceneTree
func _initialize() -> void:
	var source: Image = Image.load_from_file("res://assets_src/imagegen/day1_playroom_sign_v2_20261001/attempt_02_native.png")
	assert(source != null)
	source.convert(Image.FORMAT_RGBA8)
	source.resize(175, 175, Image.INTERPOLATE_LANCZOS)
	var result: Image = Image.create(256, 256, false, Image.FORMAT_RGBA8)
	result.fill(Color.TRANSPARENT)
	result.blit_rect(source, Rect2i(Vector2i.ZERO, source.get_size()), Vector2i((256-175)/2,(256-175)/2))
	assert(result.save_png("res://assets_src/imagegen/day1_playroom_sign_v2_20261001/attempt_02_whole_canvas_256.png") == OK)
	print("PLAYROOM_SIGN_WHOLE_CANVAS|PASS")
	quit(0)
