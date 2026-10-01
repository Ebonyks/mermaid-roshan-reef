extends SceneTree
## Technical uniform whole-canvas normalization; no subject isolation or repair.
const BASE := "res://assets_src/imagegen/day2_boxing_single_gloves_v1_20261001/"
func _initialize() -> void:
	var rows: Array[Dictionary] = []
	for pair: Array in [["left_attempt_02_native.png", "left_whole_canvas_1024.png"], ["right_attempt_01_native.png", "right_whole_canvas_1024.png"]]:
		var source: String = BASE + String(pair[0])
		var output: String = BASE + String(pair[1])
		assert(not FileAccess.file_exists(output))
		var image: Image = Image.load_from_file(source)
		assert(image != null and image.get_width() == 1254 and image.get_height() == 1254)
		image.resize(1024, 1024, Image.INTERPOLATE_LANCZOS)
		assert(image.save_png(output) == OK)
		rows.append({"source":source,"source_sha256":FileAccess.get_sha256(source),"output":output,"output_sha256":FileAccess.get_sha256(output),"source_size":[1254,1254],"output_size":[1024,1024],"operation":"One uniform whole-canvas Lanczos1254-square to1024-square transform; no crop/mask/warp/subject repair", "runtime_bound":false})
	var file: FileAccess = FileAccess.open(BASE + "NORMALIZATION_PROFILE.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"NON_RUNTIME_WHOLE_CANVAS_CANDIDATES","files":rows},"\t") + "\n")
	file.close()
	print("BOXING_GLOVE_NORMALIZE|PASS|two complete1024POT candidates; native originals preserved")
	quit(0)
