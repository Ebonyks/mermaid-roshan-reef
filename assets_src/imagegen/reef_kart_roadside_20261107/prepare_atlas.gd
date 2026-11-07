extends SceneTree

func _initialize() -> void:
	var source := Image.load_from_file("res://assets_src/imagegen/reef_kart_roadside_20261107/painted_fascias_native.png")
	if source == null or source.is_empty():
		quit(1)
		return
	var result := Image.create(1024, 512, false, Image.FORMAT_RGB8)
	var half := source.get_size() / 2
	for row in range(2):
		for column in range(2):
			var origin := Vector2i(column * half.x, row * half.y)
			var tile := source.get_region(Rect2i(origin + Vector2i(3, 3), half - Vector2i(6, 6)))
			tile.resize(512, 256, Image.INTERPOLATE_LANCZOS)
			tile.convert(Image.FORMAT_RGB8)
			result.blit_rect(tile, Rect2i(Vector2i.ZERO, tile.get_size()), Vector2i(column * 512, row * 256))
	print("FASCIA|source=", source.get_size(), "|runtime=", result.get_size())
	quit(result.save_png("res://assets/racer/roadside_v1/fascias.png"))
