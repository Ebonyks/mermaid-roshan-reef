extends SceneTree
## Crop local ImageGen healing patches; preserve all original background tiles.

const SOURCE := "res://assets_src/imagegen/opera_door_icons_20261017/foyer_icons_above_doors.png"
const OUTPUT := "res://assets/flats/castle/opera_house_venue_2d/badge_repairs/"
const BADGE_X: Array[int] = [357, 459, 565, 667]
const BADGE_Y: Array[int] = [70, 195, 328]
const ORIGINAL_SIZE := Vector2(1024.0, 576.0)


func _initialize() -> void:
	var source := Image.load_from_file(SOURCE)
	if source == null or source.is_empty():
		push_error("Missing local badge-healing source")
		quit(1)
		return
	var output := OUTPUT
	var args := OS.get_cmdline_user_args()
	if not args.is_empty():
		output = args[0].trim_suffix("/") + "/"
	if DirAccess.make_dir_recursive_absolute(output) != OK:
		push_error("Cannot create patch directory")
		quit(1)
		return
	var native_scale := Vector2(source.get_size()) / ORIGINAL_SIZE
	var patches: Array[Dictionary] = []
	for row in range(3):
		for column in range(4):
			var original_rect := Rect2(float(BADGE_X[column] - 22),
				float(BADGE_Y[row] - 22), 44.0, 50.0)
			var native_rect := Rect2i(
				Vector2i((original_rect.position * native_scale).round()),
				Vector2i((original_rect.size * native_scale).round()))
			var patch := source.get_region(native_rect)
			var filename := "door_badge_heal_r%d_c%d.png" % [row, column]
			var path := output + filename
			if patch.save_png(path) != OK:
				push_error("Cannot save badge-healing patch")
				quit(1)
				return
			patches.append({"filename": filename, "row": row, "column": column,
				"source_rect_native": [native_rect.position.x, native_rect.position.y,
					native_rect.size.x, native_rect.size.y],
				"runtime_rect": [original_rect.position.x * 1.25,
					original_rect.position.y * 1.25, 55.0, 62.5],
				"sha256": FileAccess.get_sha256(path)})
	var manifest := {"role": "local_painted_badge_healing_patches",
		"source": SOURCE.trim_prefix("res://"), "source_sha256": FileAccess.get_sha256(SOURCE),
		"native_source_size": [source.get_width(), source.get_height()],
		"derivation": "Native integer crops only; no whole-background replacement or upscaling. Engine feathers patch edges and reuses original round icon crops separately.",
		"preserved_background": "The eight original background_tiles PNGs remain byte-identical. Existing native-background resolution debt is unchanged, not satisfied.",
		"patches": patches}
	var file := FileAccess.open(output + "manifest.json", FileAccess.WRITE)
	if file == null:
		push_error("Cannot save local patch manifest")
		quit(1)
		return
	file.store_string(JSON.stringify(manifest, "\t") + "\n")
	file.close()
	print("OPERA_BADGE_PATCHES|ALL OK|12 native crops; original background preserved")
	quit(0)
