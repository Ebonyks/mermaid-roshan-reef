extends SceneTree
## Declared-timeline native inspection only; never a live-game or cinematic pass.
const SOURCE := "res://assets_src/imagegen/day2_nursery_faron_motionkeys_20261001/"
const OUT := SOURCE + "motion_fit/"

class Lift extends Control:
	var helpers: Array[Texture2D] = []
	var baby: Texture2D
	var palms: Array[Vector2] = [Vector2(635, 790), Vector2(617, 772), Vector2(597, 754),
		Vector2(635, 742), Vector2(673, 731), Vector2(686, 704), Vector2(701, 656), Vector2(715, 619)]
	var baby_foot := Vector2(0.55224609375, 0.912109375)
	var pose := 0
	var frame_index := 0
	var geometry: Array[Dictionary] = []

	func _draw() -> void:
		geometry.clear()
		for view: int in range(2):
			var extent: float = 190.0 if view == 0 else 380.0
			var infant_extent: float = 60.0 if view == 0 else 120.0
			var center: float = size.x * (0.25 if view == 0 else 0.75)
			var origin := Vector2(center - extent * 0.5, 230.0 if view == 0 else 130.0)
			var palm: Vector2 = origin + palms[pose] * extent / 1254.0
			draw_texture_rect(helpers[pose], Rect2(origin, Vector2.ONE * extent), false)
			draw_texture_rect(baby, Rect2(palm - baby_foot * infant_extent, Vector2.ONE * infant_extent), false)
			geometry.append({"pose": pose, "card_extent": extent, "baby_extent": infant_extent,
				"origin": [origin.x, origin.y], "palm": [palm.x, palm.y],
				"native_pad": [palms[pose].x, palms[pose].y]})
		draw_string(ThemeDB.fallback_font, Vector2(28, 42), "Faron authored lift study / frame %d / pose %d" % [frame_index, pose],
			HORIZONTAL_ALIGNMENT_LEFT, -1, 24, Color(0.15, 0.1, 0.3))
		draw_string(ThemeDB.fallback_font, Vector2(28, 680), "190px helper + 60px infant / 2x detail. Source study; no live return, input or owner acceptance.",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 19, Color(0.15, 0.1, 0.3))

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	assert(not FileAccess.file_exists(SOURCE + "MANIFEST.json"), "Source packet sealed")
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(SOURCE + "selected_fit/receipt.json")) as Dictionary
	var sources: Array = fixture["sources"] as Array
	var fit := Lift.new()
	for index: int in range(sources.size()):
		var record: Dictionary = sources[index] as Dictionary
		var path: String = "res://" + str(record["path"])
		assert(FileAccess.get_sha256(path) == str(record["sha256"]))
		var texture: Texture2D = ImageTexture.create_from_image(Image.load_from_file(path))
		if index < 8:
			fit.helpers.append(texture)
		else:
			fit.baby = texture
	var back := OperaWorldBackdrop2D.new()
	root.add_child(back)
	back.setup("nursery", "")
	root.add_child(fit)
	var captures: Array[Dictionary] = []
	for width: int in [1280, 1600]:
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		back.size = Vector2(width, 720)
		fit.size = Vector2(width, 720)
		var destination: String = OUT + "%dx720/" % width
		DirAccess.make_dir_recursive_absolute(destination)
		for frame: int in range(48):
			fit.frame_index = frame
			fit.pose = 0 if frame < 6 else mini(7, 1 + (frame - 6) / 3)
			fit.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var path: String = destination + "%04d.webp" % frame
			var image: Image = root.get_texture().get_image()
			assert(image.save_webp(path, false) == OK)
			captures.append({"path": path.trim_prefix("res://"), "sha256": FileAccess.get_sha256(path),
				"dimensions": [width, 720], "declared_timeline_frame": frame,
				"pose": fit.pose, "source": sources[fit.pose], "geometry": fit.geometry.duplicate(true)})
	for item: Dictionary in sources:
		assert(FileAccess.get_sha256("res://" + str(item["path"])) == str(item["sha256"]))
	var file := FileAccess.open(OUT + "receipt.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(), "frames": captures, "sources": sources,
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_faron_lift_motion.gd"),
		"fixture_sha256": FileAccess.get_sha256(SOURCE + "selected_fit/receipt.json"),
		"profile_sha256": FileAccess.get_sha256(SOURCE + "TIMED_STUDY_PROFILE.json"),
		"declared_review_fps": 30,
		"method": "48 forced native render captures per aspect under the predeclared exposure profile. Each changed character state uses one complete generated figure; no blend/interpolation/warp. Canonical lossless WebP source-study frames.",
		"qualification": "Fixed-reference standalone lift only; elapsed native capture speed is not30fps runtime performance. No full safe-return action, input/progress/interrupt route, cinematic/device/child/owner acceptance."}, "\t") + "\n")
	file.close()
	print("NURSERY_FARON_LIFT_MOTION|CAPTURED|NOT_ACCEPTED")
	quit()
