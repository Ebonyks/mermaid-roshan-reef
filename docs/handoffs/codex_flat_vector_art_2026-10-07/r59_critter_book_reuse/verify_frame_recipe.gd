extends SceneTree

func digest(bytes: PackedByteArray) -> String:
	var hash: HashingContext = HashingContext.new()
	hash.start(HashingContext.HASH_SHA256)
	hash.update(bytes)
	return hash.finish().hex_encode()

# Exact source-owned _trim body, read-only here.
func _trim(path: String) -> Image:
	var image: Image = Image.load_from_file(path)
	image.convert(Image.FORMAT_RGBA8)
	return image.get_region(image.get_used_rect())

# Source _export_component's padded=false branch replayed in memory;
# no save_png, asset write or source-builder execution.
func expected_component(image: Image, limit: int) -> Image:
	var scaled: Image = image.duplicate() as Image
	var ratio: float = minf(float(limit) / scaled.get_width(), float(limit) / scaled.get_height())
	scaled.resize(maxi(1, roundi(scaled.get_width() * ratio)), maxi(1, roundi(scaled.get_height() * ratio)), Image.INTERPOLATE_LANCZOS)
	return scaled

func _initialize() -> void:
	var rows: Array[Dictionary] = []
	var failures: int = 0
	for key: String in ["wardrobe_panel", "wardrobe_card"]:
		var native_path: String = "res://assets_src/fashion_designer/skin_engine_v2/native/" + key + ".png"
		var runtime_path: String = "res://assets/fashion/skin_engine_v2/ui/" + key + ".png"
		var expected: Image = expected_component(_trim(native_path), 256 if key == "wardrobe_card" else 1024)
		var actual: Image = Image.load_from_file(runtime_path)
		actual.convert(Image.FORMAT_RGBA8)
		var equal: bool = expected.get_size() == actual.get_size() and expected.get_data() == actual.get_data()
		if not equal:
			failures += 1
		rows.append({"key": key, "native_path": native_path, "native_file_sha256": FileAccess.get_sha256(native_path), "runtime_path": runtime_path, "runtime_file_sha256": FileAccess.get_sha256(runtime_path), "expected_size": str(expected.get_size()), "actual_size": str(actual.get_size()), "expected_rgba8_sha256": digest(expected.get_data()), "actual_rgba8_sha256": digest(actual.get_data()), "decoded_rgba8_exact": equal})
	var report: Dictionary = {"engine": Engine.get_version_info(), "display": DisplayServer.get_name(), "rows": rows, "failures": failures, "method": "Current source trim/Lanczos padded=false recipe replay in memory. Source export writer never executed. No PNG/source writes; one JSON evidence output only. Approval/provider revision/owner/device remain unresolved."}
	var file: FileAccess = FileAccess.open(OS.get_environment("R59_RECIPE_OUT"), FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t") + "\n")
	file.close()
	print("R59_RECIPE_REPLAY failures=", failures)
	quit(0 if failures == 0 else 1)
