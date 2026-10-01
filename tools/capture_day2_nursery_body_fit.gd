extends SceneTree
## Static native sampling/contact diagnostics; not production gameplay acceptance.

const OUT := "res://assets_src/imagegen/day2_nursery_body_20261001/"
var cases: Array[Dictionary] = []

class Fit:
	extends Control
	var atlas: Texture2D
	var babies: Array[Texture2D] = []
	var feet: Array[Vector2] = []
	var poses: Array = []
	var measurements: Array[Dictionary] = []

	func _draw() -> void:
		measurements.clear()
		var column: float = size.x / 4.0
		var extent: float = minf(350.0, column * 1.06)
		for index: int in range(4):
			var pose: Dictionary = poses[index]
			var cell: Array = pose["cell"]
			var hip: Array = pose["hip_xy"]
			var palm: Array = pose["palm_xy"]
			var pivot := Vector2(column * (float(index) + 0.5), 435.0)
			var origin: Vector2 = pivot - Vector2(float(hip[0]), float(hip[1])) * extent / 627.0
			var socket: Vector2 = origin + Vector2(float(palm[0]), float(palm[1])) * extent / 627.0
			# Atlas sampling and whole-cell scaling preserve all native source pixels.
			draw_texture_rect_region(atlas, Rect2(origin, Vector2.ONE * extent),
				Rect2(float(cell[0]) * 627.0, float(cell[1]) * 627.0, 627, 627))
			if index > 0:
				var baby: int = (index - 1) % 3
				draw_texture_rect(babies[baby], Rect2(socket - feet[baby] * 72.0, Vector2.ONE * 72.0), false)
			# Diagnostic guides are drawn separately and never become replacement pixels.
			draw_line(pivot + Vector2(-7, 0), pivot + Vector2(7, 0), Color(0.18, 0.12, 0.30), 2)
			draw_line(pivot + Vector2(0, -7), pivot + Vector2(0, 7), Color(0.18, 0.12, 0.30), 2)
			var font: Font = ThemeDB.fallback_font
			draw_string(font, Vector2(column * index + 20, 60), String(pose["name"]), HORIZONTAL_ALIGNMENT_LEFT, -1, 25, Color(0.16, 0.10, 0.28))
			measurements.append({"pose": pose["name"], "cell_extent": extent,
				"pivot_xy": [pivot.x, pivot.y], "palm_xy": [socket.x, socket.y],
				"body_rect": [origin.x, origin.y, extent, extent], "baby_present": index > 0})

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT + "fit-captures")
	var contract: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(OUT + "fit-contract.json"))
	var image: Image = Image.load_from_file(OUT + "candidates/attempt-01.png")
	assert(image.get_size() == Vector2i(1254, 1254))
	var fit := Fit.new()
	fit.atlas = ImageTexture.create_from_image(image)
	fit.poses = contract["poses"]
	for path: String in OperaNurseryCatch.BABY_PATHS:
		var baby: Texture2D = load(path) as Texture2D
		fit.babies.append(baby)
		var used: Rect2i = baby.get_image().get_used_rect()
		fit.feet.append(Vector2(used.position.x + used.size.x * 0.5, used.end.y) / baby.get_size())
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
		var path := "fit-captures/%dx720.webp" % width
		var native: Image = root.get_texture().get_image()
		assert(native.save_webp(OUT + path, false) == OK)
		cases.append({"path": path, "dimensions": [width, 720],
			"sha256": FileAccess.get_sha256(OUT + path), "measurements": fit.measurements.duplicate(true)})
	var receipt := {"schema": "reef.nursery-body-fit.receipt.v1", "cases": cases,
		"renderer": RenderingServer.get_current_rendering_method(), "engine": Engine.get_version_info()["string"],
		"source_sha256": FileAccess.get_sha256(OUT + "candidates/attempt-01.png"),
		"contract_sha256": FileAccess.get_sha256(OUT + "fit-contract.json"),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_body_fit.gd"),
		"method": "Static independently held source keys on nursery backdrop; manually estimated sockets, original babies, unchanged atlas pixels. No input, gameplay commits, animated action or normal route acceptance."}
	var file := FileAccess.open(OUT + "fit-captures/receipt.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	print("NURSERY_BODY_FIT|RESULT|CAPTURED|2|NOT_ACCEPTED")
	quit()
