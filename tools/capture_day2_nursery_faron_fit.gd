extends SceneTree
## Source-only native Canvas comparison; no production binding or action acceptance.
const SOURCE := "res://assets_src/imagegen/day2_nursery_faron_v2_20261001/"
const OUT := SOURCE + "native_fit/"
var receipts: Array[Dictionary] = []

class Fit extends Control:
	var helpers: Array[Texture2D] = []
	var baby: Texture2D
	var roshan: Texture2D
	var baby_foot := Vector2(0.55224609375, 0.912109375)
	var measurements: Array[Dictionary] = []

	func _draw() -> void:
		measurements.clear()
		var cell_width: float = size.x / 3.0
		var names: Array[String] = ["Original / baked infant", "Attempt 1 / style rejected",
			"Attempt 2 / empty", "Attempt 2 / separate infant",
			"Current Roshan / same infant", "Attempt 2 / detail view"]
		for index: int in range(6):
			var origin := Vector2(cell_width * float(index % 3), float(index / 3) * 350.0)
			var extent: float = 190.0
			var texture: Texture2D = helpers[mini(index, 2)]
			if index == 4:
				extent = 250.0
				texture = roshan
			elif index == 5:
				extent = 300.0
			var card_origin: Vector2 = origin + Vector2((cell_width - extent) * 0.5, 45.0)
			draw_texture_rect(texture, Rect2(card_origin, Vector2.ONE * extent), false)
			var socket: Vector2 = card_origin + Vector2(715.0, 619.0) * extent / 1254.0
			var baby_extent: float = 60.0
			if index == 4:
				socket = card_origin + Vector2(102.0, 278.0) * extent / 512.0
				baby_extent = 80.0
			if index in [3, 4]:
				draw_texture_rect(baby, Rect2(socket - baby_foot * baby_extent,
					Vector2.ONE * baby_extent), false)
			draw_string(ThemeDB.fallback_font, origin + Vector2(16.0, 30.0), names[index],
				HORIZONTAL_ALIGNMENT_LEFT, -1, 19, Color(0.15, 0.1, 0.3))
			measurements.append({"case": index, "name": names[index], "card_extent": extent,
				"origin": [card_origin.x, card_origin.y], "baby_present": index in [3, 4],
				"palm": [socket.x, socket.y], "baby_card_extent": baby_extent,
				"socket_method": "Manual native palm sampling; static diagnostic only"})

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	assert(not FileAccess.file_exists(SOURCE + "MANIFEST.json"), "Review packet is sealed")
	DirAccess.make_dir_recursive_absolute(OUT)
	var fit := Fit.new()
	var paths: Array[String] = ["res://assets/opera/worlds/actors/faron_nursery.png",
		SOURCE + "attempt-01.png", SOURCE + "attempt-02.png",
		"res://assets/opera/worlds/nursery/refinement_v2/care_01.png",
		"res://assets_src/imagegen/day2_nursery_babies_v2_20261001/baby_0_review.png"]
	var source_receipts: Array[Dictionary] = []
	for index: int in range(paths.size()):
		var image: Image = Image.load_from_file(paths[index])
		assert(image != null and not image.is_empty())
		var texture: Texture2D = ImageTexture.create_from_image(image)
		if index < 3:
			fit.helpers.append(texture)
		elif index == 3:
			fit.roshan = texture
		else:
			fit.baby = texture
		source_receipts.append({"path": paths[index].trim_prefix("res://"),
			"sha256": FileAccess.get_sha256(paths[index]),
			"dimensions": [image.get_width(), image.get_height()]})
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
		"sources": source_receipts,
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_faron_fit.gd"),
		"method": "Correct native alpha on actual nursery backdrop; helpers190px, Roshan250px, source-only infant60/80px and helper detail300px. Manual static sockets. No ordinary live helper binding, pickup/return action, input, progress or device/child/owner acceptance."}, "\t") + "\n")
	file.close()
	print("NURSERY_FARON_FIT|RESULT|CAPTURED|NOT_ACCEPTED")
	quit()
