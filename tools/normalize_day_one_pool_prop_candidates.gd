extends SceneTree
## Whole-canvas review resolution normalization; no source/pixel repair or live binding.
const FAMILY := "res://assets_src/imagegen/day1_pool_trash_v2_20261001/"
const OUTPUT := FAMILY + "normalized512/"

func _init() -> void:
	var records: Array = JSON.parse_string(FileAccess.get_file_as_string(
		FAMILY + "SELECTED_SOURCE_RECORDS_V2.json")) as Array
	assert(records.size() == 5)
	assert(DirAccess.make_dir_recursive_absolute(OUTPUT) == OK)
	var provenance: Array[Dictionary] = []
	for item: Variant in records:
		var record: Dictionary = item as Dictionary
		var source_path: String = "res://" + str(record["planned_native_path"])
		var expected: String = str(record["sha256"])
		assert(FileAccess.get_sha256(source_path) == expected)
		var image: Image = Image.load_from_file(source_path)
		assert(not image.is_empty() and image.get_size() == Vector2i(1254, 1254))
		var native_dimensions: Vector2i = image.get_size()
		image.resize(512, 512, Image.INTERPOLATE_LANCZOS)
		var output_path: String = OUTPUT + str(record["name"]) + ".png"
		assert(image.save_png(output_path) == OK)
		assert(FileAccess.get_sha256(source_path) == expected)
		provenance.append({"name": record["name"], "source_path": source_path,
			"source_sha256": expected, "native_dimensions": [native_dimensions.x, native_dimensions.y],
			"output_path": output_path, "output_sha256": FileAccess.get_sha256(output_path),
			"output_dimensions": [512, 512], "method": "WHOLE_CANVAS_LANCZOS_RESOLUTION_NORMALIZATION",
			"scale": 512.0 / 1254.0, "crop": false, "translation": false,
			"subject_repair": false, "native_alpha_preserved_by_resampling": true,
			"runtime_bound": false, "owner_accepted": false})
	var receipt: Dictionary = {"engine": Engine.get_version_info()["string"],
		"tool": "res://tools/normalize_day_one_pool_prop_candidates.gd",
		"tool_sha256": FileAccess.get_sha256("res://tools/normalize_day_one_pool_prop_candidates.gd"),
		"source_records_sha256": FileAccess.get_sha256(FAMILY + "SELECTED_SOURCE_RECORDS_V2.json"),
		"qualification": "Non-production POT review derivatives only. Selected native source opinions remain provisional. No crop, limb/subject warp, redesign, source replacement or live binding. New512px native context and device/child/owner acceptance remain pending.",
		"items": provenance}
	var file: FileAccess = FileAccess.open(OUTPUT + "PROVENANCE.json", FileAccess.WRITE)
	assert(file != null)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	print("POOL_PROP_NORMALIZE|5 complete source images ->512px POT review derivatives; native hashes unchanged")
	quit(0)
