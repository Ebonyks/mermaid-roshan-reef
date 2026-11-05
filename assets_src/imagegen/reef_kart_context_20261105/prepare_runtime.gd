extends SceneTree

const SOURCE := "res://assets_src/imagegen/reef_kart_context_20261105/"
const OUTPUT := "res://assets/racer/context_v2/"
const IDS := ["item_capsule", "kelp_trap", "turn_marker", "play_blocks", "play_tent", "kitchen_teapot", "pool_seahorse"]

func _initialize() -> void:
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var records: Array[Dictionary] = []
	for id: String in IDS:
		var source_path := SOURCE + id + "_native.png"
		var image := Image.load_from_file(source_path)
		if image == null:
			push_error("Missing native " + id)
			quit(1)
			return
		image.convert(Image.FORMAT_RGBA8)
		var native_size := image.get_size()
		var crop := _visible_bounds(image).grow(8).intersection(Rect2i(Vector2i.ZERO, native_size))
		var object := image.get_region(crop)
		var factor := 1008.0 / float(maxi(object.get_width(), object.get_height()))
		var size := Vector2i(maxi(1, roundi(object.get_width() * factor)), maxi(1, roundi(object.get_height() * factor)))
		object.resize(size.x, size.y, Image.INTERPOLATE_LANCZOS)
		var result := Image.create(1024, 1024, false, Image.FORMAT_RGBA8)
		result.fill(Color.TRANSPARENT)
		var origin := (Vector2i(1024, 1024) - size) / 2
		result.blit_rect(object, Rect2i(Vector2i.ZERO, size), origin)
		var target := OUTPUT + id + ".png"
		var status := result.save_png(target)
		if status != OK:
			push_error("Cannot save " + target)
			quit(1)
			return
		records.append({"id": id, "source": source_path, "source_size": [native_size.x, native_size.y],
			"source_sha256": FileAccess.get_sha256(source_path), "crop": [crop.position.x, crop.position.y, crop.size.x, crop.size.y],
			"runtime": target, "runtime_sha256": FileAccess.get_sha256(target),
			"content_rect": [origin.x, origin.y, size.x, size.y], "size": [1024, 1024],
			"operation": "Alpha threshold 0.06 only selects crop bounds, add eight source pixels, preserve all pixels inside crop, proportional Lanczos export centered on transparent 1024 square. Native preserved."})
	var manifest := FileAccess.open(SOURCE + "runtime_exports.json", FileAccess.WRITE)
	manifest.store_string(JSON.stringify({"exports": records}, "\t") + "\n")
	print("RACER_ART_EXPORT|ALL OK|count=", records.size())
	quit()

func _visible_bounds(image: Image) -> Rect2i:
	var low := image.get_size()
	var high := Vector2i(-1, -1)
	for y in range(image.get_height()):
		for x in range(image.get_width()):
			if image.get_pixel(x, y).a >= 0.06:
				low.x = mini(low.x, x)
				low.y = mini(low.y, y)
				high.x = maxi(high.x, x)
				high.y = maxi(high.y, y)
	return Rect2i(low, high - low + Vector2i.ONE)
