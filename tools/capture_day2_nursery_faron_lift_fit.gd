extends SceneTree
## Unbound complete-source contact study. The same whole-canvas reference is fixed.
const SOURCE := "res://assets_src/imagegen/day2_nursery_faron_motionkeys_20261001/"
const OUT := SOURCE + "selected_fit/"
var receipts: Array[Dictionary] = []

class Fit extends Control:
	var helpers: Array[Texture2D] = []
	var baby: Texture2D
	var palms: Array[Vector2] = [Vector2(635, 790), Vector2(617, 772),
		Vector2(597, 754), Vector2(635, 742), Vector2(673, 731),
		Vector2(686, 704), Vector2(701, 656), Vector2(715, 619)]
	var names: Array[String] = ["Low reach", "Early lift", "Middle lift", "Lateral bridge",
		"Near held", "Rise A", "Rise B", "Existing held"]
	var baby_foot := Vector2(0.55224609375, 0.912109375)
	var detail := false
	var empty := false
	var measurements: Array[Dictionary] = []

	func _draw() -> void:
		measurements.clear()
		var columns: int = 4
		var extent: float = 300.0 if detail else 190.0
		var infant_extent: float = extent * 60.0 / 190.0
		var cell_width: float = size.x / float(columns)
		var count: int = 8
		for case_index: int in range(count):
			var index: int = case_index % 8
			var origin := Vector2(cell_width * float(case_index % columns), float(case_index / columns) * 350.0)
			var card_origin: Vector2 = origin + Vector2((cell_width - extent) * 0.5, 40.0)
			var socket: Vector2 = card_origin + palms[index] * extent / 1254.0
			var baby_present: bool = not empty
			draw_texture_rect(helpers[index], Rect2(card_origin, Vector2.ONE * extent), false)
			if baby_present:
				draw_texture_rect(baby, Rect2(socket - baby_foot * infant_extent,
					Vector2.ONE * infant_extent), false)
			draw_string(ThemeDB.fallback_font, origin + Vector2(10.0, 27.0), names[index],
				HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color(0.15, 0.1, 0.3))
			measurements.append({"case": case_index, "source_index": index, "name": names[index],
				"card_extent": extent, "origin": [card_origin.x, card_origin.y],
				"baby_present": baby_present, "baby_card_extent": infant_extent,
				"manual_native_palm": [palms[index].x, palms[index].y],
				"screen_palm": [socket.x, socket.y],
				"method": "Manual visible receiving-pad point; fixed whole-canvas reference and unchanged source pixels"})

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	assert(not FileAccess.file_exists(SOURCE + "MANIFEST.json"), "Review packet is sealed")
	DirAccess.make_dir_recursive_absolute(OUT)
	var fit := Fit.new()
	var paths: Array[String] = [SOURCE + "low-reach-attempt-01.png", SOURCE + "lift-early-attempt-01.png",
		SOURCE + "lift-middle-attempt-01.png", SOURCE + "lateral-bridge-attempt-02.png",
		SOURCE + "lift-near-held-attempt-01.png", SOURCE + "rise-bridge-a-attempt-02.png",
		SOURCE + "rise-bridge-b-attempt-02.png",
		"res://assets_src/imagegen/day2_nursery_faron_v2_20261001/attempt-02.png",
		"res://assets_src/imagegen/day2_nursery_babies_v2_20261001/baby_0_review.png"]
	var sources: Array[Dictionary] = []
	for index: int in range(paths.size()):
		var image: Image = Image.load_from_file(paths[index])
		assert(image != null and not image.is_empty())
		var texture: Texture2D = ImageTexture.create_from_image(image)
		if index < 8:
			fit.helpers.append(texture)
		else:
			fit.baby = texture
		sources.append({"path": paths[index].trim_prefix("res://"),
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
		for mode: String in ["empty", "contact", "detail"]:
			fit.detail = mode == "detail"
			fit.empty = mode == "empty"
			fit.queue_redraw()
			for _frame: int in range(3):
				await process_frame
			await RenderingServer.frame_post_draw
			var path := "%dx720-%s.webp" % [width, mode]
			var native: Image = root.get_texture().get_image()
			assert(native.save_webp(OUT + path, false) == OK)
			receipts.append({"path": path, "dimensions": [width, 720],
				"sha256": FileAccess.get_sha256(OUT + path), "geometry": fit.measurements.duplicate(true)})
	for source: Dictionary in sources:
		assert(FileAccess.get_sha256("res://" + str(source["path"])) == str(source["sha256"]))
	var steps: Array[float] = []
	for index: int in range(1, fit.palms.size()):
		steps.append(fit.palms[index].distance_to(fit.palms[index - 1]) * 190.0 / 1254.0)
	var file := FileAccess.open(OUT + "receipt.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(), "cases": receipts, "sources": sources,
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_faron_lift_fit.gd"),
		"support_steps_at_190px": steps, "previously_declared_draft_target_px": 8.0,
		"qualification": "Manual static receiving pads on unbound complete source figures; 190px helper/60px infant plus300px detail. No native-size live-world assertion, pickup route, temporal playback, input, progress, cinematic or device/child/owner acceptance."}, "\t") + "\n")
	file.close()
	print("NURSERY_FARON_LIFT_FIT|RESULT|CAPTURED|NOT_ACCEPTED")
	quit()
