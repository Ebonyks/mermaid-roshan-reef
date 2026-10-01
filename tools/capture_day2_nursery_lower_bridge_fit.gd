extends SceneTree
## Independently held authored sources; no interpolation, runtime binding or action award.
const FOLDER := "res://assets_src/imagegen/day2_nursery_lower_bridge_v2_20261001/"
var receipts: Array[Dictionary] = []

class Fit extends Control:
	var rows: Array[Dictionary] = []
	var textures: Array[Texture2D] = []
	var baby: Texture2D
	var measurements: Array[Dictionary] = []

	func _draw() -> void:
		measurements.clear()
		var width: float = size.x / 3.0
		for index: int in range(rows.size()):
			var row: Dictionary = rows[index]
			var extent: float = float(row["extent"])
			var side: float = float(row["side"])
			var hip: Array = row["hip_xy"]
			var palm: Array = row["palm_xy"]
			var pivot := Vector2(width * (float(index % 3) + 0.5),
				270.0 + float(index / 3) * 350.0)
			var origin: Vector2 = pivot - Vector2(float(hip[0]), float(hip[1])) * extent / side
			var socket: Vector2 = origin + Vector2(float(palm[0]), float(palm[1])) * extent / side
			draw_texture_rect(textures[index], Rect2(origin, Vector2.ONE * extent), false)
			draw_texture_rect(baby, Rect2(socket - Vector2(0.55224609375, 0.912109375) * 80.0,
				Vector2.ONE * 80.0), false)
			draw_string(ThemeDB.fallback_font,
				Vector2(width * float(index % 3) + 16.0, 30.0 + float(index / 3) * 350.0),
				String(row["name"]), HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color(0.15, 0.1, 0.3))
			draw_circle(pivot, 2.0, Color(0.8, 0.2, 0.3))
			var relative: Vector2 = socket - pivot
			measurements.append({"index": index, "name": row["name"], "path": row["path"],
				"card_extent": extent, "canvas_side": side, "hip": [pivot.x, pivot.y],
				"palm": [socket.x, socket.y], "hip_relative_palm_screen_px": [relative.x, relative.y],
				"source_sha256": FileAccess.get_sha256("res://" + String(row["path"]))})

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	assert(not FileAccess.file_exists(FOLDER + "MANIFEST.json"), "Packet is sealed")
	DirAccess.make_dir_recursive_absolute(FOLDER + "native_fit/")
	var contract: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://assets/opera/worlds/nursery/refinement_v2/care_keys.json"))
	var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(FOLDER + "PACK_REPORT.json"))
	var fit := Fit.new()
	var first: Dictionary = (contract["poses"] as Array)[3].duplicate(true)
	first.merge({"name": "Current hold key3", "extent": 250.0, "side": 512.0}, true)
	fit.rows.append(first)
	for index: int in range(4):
		var row: Dictionary = (pack["poses"] as Array)[index].duplicate(true)
		row.merge({"name": "Unbound bridge %d" % index,
			"extent": pack["common_new_review_card_extent_px"], "side": 1024.0}, true)
		fit.rows.append(row)
	var last: Dictionary = (contract["poses"] as Array)[4].duplicate(true)
	last.merge({"name": "Current first lower key4", "extent": 250.0, "side": 512.0}, true)
	fit.rows.append(last)
	for row: Dictionary in fit.rows:
		var image: Image = Image.load_from_file("res://" + String(row["path"]))
		assert(image != null and not image.is_empty())
		fit.textures.append(ImageTexture.create_from_image(image))
	var infant: Image = Image.load_from_file(
		"res://assets_src/imagegen/day2_nursery_babies_v2_20261001/baby_0_review.png")
	fit.baby = ImageTexture.create_from_image(infant)
	var back := OperaWorldBackdrop2D.new()
	root.add_child(back)
	back.setup("nursery", "")
	root.add_child(fit)
	for width: int in [1280, 1600]:
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		back.size = Vector2(width, 720)
		fit.size = Vector2(width, 720)
		fit.queue_redraw()
		for _frame: int in range(3):
			await process_frame
		await RenderingServer.frame_post_draw
		var path := "%dx720.webp" % width
		assert(root.get_texture().get_image().save_webp(FOLDER + "native_fit/" + path, false) == OK)
		receipts.append({"path": path, "dimensions": [width, 720],
			"sha256": FileAccess.get_sha256(FOLDER + "native_fit/" + path),
			"geometry": fit.measurements.duplicate(true)})
	var file := FileAccess.open(FOLDER + "native_fit/receipt.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(), "cases": receipts,
		"pack_sha256": FileAccess.get_sha256(FOLDER + "PACK_REPORT.json"),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_lower_bridge_fit.gd"),
		"declared_transition_tolerance_screen_px": 8.0,
		"qualification": "Manual anatomical landmarks, +/-5 new native pixels; common whole-image size from first-pose painted height. Independently held hip-aligned sources show approximate contact/pose differences. No live binding, complete action, input, progress or device/child/owner acceptance."}, "\t") + "\n")
	file.close()
	print("NURSERY_LOWER_BRIDGE_FIT|RESULT|CAPTURED|NOT_ACCEPTED")
	quit()
