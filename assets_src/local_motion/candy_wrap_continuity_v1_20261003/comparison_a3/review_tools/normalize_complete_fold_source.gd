extends SceneTree

func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	assert(args.size() == 2)
	var source: Image = Image.load_from_file(args[0])
	assert(source != null and source.get_size() == Vector2i(1254, 1254))
	var normalized: Image = source.duplicate()
	normalized.resize(448, 448, Image.INTERPOLATE_LANCZOS)
	var mat: Image = Image.create(896, 512, false, Image.FORMAT_RGBA8)
	mat.fill(Color("dfedf1"))
	mat.blend_rect(normalized, Rect2i(0, 0, 448, 448), Vector2i(224, 32))
	mat.convert(Image.FORMAT_RGB8)
	assert(mat.save_png(args[1]) == OK)
	print("CANDY_FOLD_INPUT|PASS|whole1254x1254 source uniformly448x448 on896x512 model mat")
	quit(0)
