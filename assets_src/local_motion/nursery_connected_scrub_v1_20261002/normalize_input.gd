extends SceneTree

func _initialize() -> void:
	var source: Image = Image.load_from_file("res://assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/native.png")
	if source == null or source.get_size() != Vector2i(1254, 1254):
		quit(2)
		return
	source.convert(Image.FORMAT_RGBA8)
	source.resize(448, 448, Image.INTERPOLATE_LANCZOS)
	var mat: Image = Image.create(896, 512, false, Image.FORMAT_RGBA8)
	mat.fill(Color("dfedf1"))
	mat.blend_rect(source, Rect2i(0, 0, 448, 448), Vector2i(224, 32))
	mat.convert(Image.FORMAT_RGB8)
	var error: Error = mat.save_png("res://assets_src/local_motion/nursery_connected_scrub_v1_20261002/inputs/NUR-SCRUB-A1.png")
	print("NUR_INPUT_NORMALIZATION|", error, "|whole-canvas uniform448, centered896x512 RGB mat")
	quit(error)
