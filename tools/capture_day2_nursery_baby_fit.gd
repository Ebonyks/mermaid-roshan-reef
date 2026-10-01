extends SceneTree
## Native static socket sampling; neither animation nor production input acceptance.
const OUT := "res://audit/day2_nursery_baby_fit_v1_20261001/"
var receipts: Array[Dictionary] = []

class Fit extends Control:
	var textures: Array[Texture2D] = []
	var babies: Array[Texture2D] = []
	var feet: Array[Vector2] = []
	var poses: Array = []
	var measurements: Array[Dictionary] = []

	func _draw() -> void:
		measurements.clear()
		var cell_width: float = size.x / 4.0
		var extent := 250.0
		for index: int in range(8):
			var pose: Dictionary = poses[index]
			var hip: Array = pose["hip_xy"]
			var palm: Array = pose["palm_xy"]
			var pivot := Vector2(cell_width * (float(index % 4) + 0.5),
				230.0 + float(index / 4) * 350.0)
			var origin: Vector2 = pivot - Vector2(float(hip[0]), float(hip[1])) * extent / 512.0
			var socket: Vector2 = origin + Vector2(float(palm[0]), float(palm[1])) * extent / 512.0
			draw_texture_rect(textures[index], Rect2(origin, Vector2.ONE * extent), false)
			if index > 0:
				var baby: int = (index - 1) % 3
				draw_texture_rect(babies[baby], Rect2(socket - feet[baby] * 80.0,
					Vector2.ONE * 80.0), false)
			draw_line(pivot + Vector2(-5, 0), pivot + Vector2(5, 0), Color(0.2, 0.1, 0.3), 1)
			draw_line(pivot + Vector2(0, -5), pivot + Vector2(0, 5), Color(0.2, 0.1, 0.3), 1)
			draw_circle(socket, 2.0, Color(0.9, 0.2, 0.4))
			draw_string(ThemeDB.fallback_font, Vector2(cell_width * float(index % 4) + 20,
				30.0 + float(index / 4) * 350.0), "Key %d" % index,
				HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color(0.15, 0.1, 0.3))
			measurements.append({"key": index, "origin": [origin.x, origin.y],
				"hip": [pivot.x, pivot.y], "palm": [socket.x, socket.y], "extent": extent,
				"baby_present": index > 0})

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	var contract: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://assets/opera/worlds/nursery/refinement_v2/care_keys.json"))
	var fit := Fit.new()
	fit.poses = contract["poses"]
	for pose: Dictionary in fit.poses:
		var image: Image = Image.load_from_file("res://" + String(pose["path"]))
		assert(image.get_size() == Vector2i(512, 512))
		fit.textures.append(ImageTexture.create_from_image(image))
	var baby_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://assets_src/imagegen/day2_nursery_babies_v2_20261001/PACK_REPORT.json"))
	for baby_pose: Dictionary in baby_pack["poses"]:
		var baby_image: Image = Image.load_from_file("res://" + String(baby_pose["path"]))
		assert(baby_image.get_size() == Vector2i(1024, 1024))
		fit.babies.append(ImageTexture.create_from_image(baby_image))
		var foot: Array = baby_pose["visible_foot_uv"]
		fit.feet.append(Vector2(float(foot[0]), float(foot[1])))
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
		var native: Image = root.get_texture().get_image()
		assert(native.save_webp(OUT + path, false) == OK)
		receipts.append({"path": path, "dimensions": [width, 720],
			"sha256": FileAccess.get_sha256(OUT + path), "geometry": fit.measurements.duplicate(true)})
	var file := FileAccess.open(OUT + "receipt.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(), "cases": receipts,
		"contract_sha256": FileAccess.get_sha256("res://assets/opera/worlds/nursery/refinement_v2/care_keys.json"),
		"baby_pack_sha256": FileAccess.get_sha256("res://assets_src/imagegen/day2_nursery_babies_v2_20261001/PACK_REPORT.json"),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_baby_fit.gd"),
		"method": "Eight independently held native sampling/socket fits with new source-only infant candidates,250px care body and80px infant cards.50pct painted support metadata, unchanged source pixels; no action, input, progress, phone budget or creative acceptance."}, "\t") + "\n")
	file.close()
	print("NURSERY_CARE_FIT|RESULT|CAPTURED|NOT_ACCEPTED")
	quit()
