extends SceneTree

func _initialize() -> void:
	var image: Image = Image.load_from_file("res://assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/native.png")
	assert(not image.is_empty())
	image.resize(1024, 1024, Image.INTERPOLATE_LANCZOS)
	assert(image.save_png("res://assets/opera/worlds/nursery/wash_connected_v1_20261002/rub_palm02.png") == OK)
	print("NURSERY_WASH|PALM02_WHOLE_CANVAS_NORMALIZATION|PASS")
	quit(0)
