extends SceneTree
## Non-destructive whole-canvas normalization; preserve the native generation.
const SOURCE := "res://assets_src/imagegen/day1_pool_skimmer_v2_20261001/pool-skimmer-attempt-01.png"
const OUTPUT := "res://assets_src/imagegen/day1_pool_skimmer_v2_20261001/normalized1024/pool-skimmer.png"

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var source_sha256: String = FileAccess.get_sha256(SOURCE)
	assert(source_sha256 == "522b5f6b9a4d241e3ec0fd3515655e744a08fd34aaa3e2a81c6203d54bdbb8f7")
	var image: Image = Image.load_from_file(SOURCE)
	assert(image.get_size() == Vector2i(1536, 1024))
	assert(not FileAccess.file_exists(OUTPUT))
	assert(DirAccess.make_dir_recursive_absolute(OUTPUT.get_base_dir()) == OK)
	image.resize(1024, 683, Image.INTERPOLATE_LANCZOS)
	assert(image.save_png(OUTPUT) == OK)
	assert(FileAccess.get_sha256(SOURCE) == source_sha256)
	var harness: String = "res://tools/normalize_day_one_pool_skimmer_candidate.gd"
	var provenance: Dictionary = {"source": SOURCE, "source_sha256": source_sha256,
		"source_dimensions": [1536, 1024], "output": OUTPUT,
		"output_sha256": FileAccess.get_sha256(OUTPUT), "output_dimensions": [1024, 683],
		"method": "Official Godot4.7.2 Lanczos whole-canvas resize; nearest integer output height. No crop, subject translation or local pixel repair.",
		"harness": harness, "harness_sha256": FileAccess.get_sha256(harness),
		"engine": Engine.get_version_info(), "runtime_bound": false,
		"technical_qualification": "Longest edge1024 meets asset size limit. Height683 is NPOT: no VRAM compression/mode2; explicit uncompressed import required before a future runtime copy. Fixture uses ImageTexture only; no device/import/performance pass."}
	var file: FileAccess = FileAccess.open(OUTPUT.get_base_dir().path_join("PROVENANCE.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(provenance, "\t") + "\n")
	file.close()
	print("POOL_SKIMMER_NORMALIZE|PASS|native source preserved|1024x683 RGBA review derivative")
	quit(0)
