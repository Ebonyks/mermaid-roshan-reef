extends SceneTree
## Source-only lowering study. Explicit held span, five authored transitions.
## No gameplay input, award, binding, interpolation or cinematic acceptance.
const FOLDER := "res://assets_src/imagegen/day2_nursery_lower_bridge_v2_20261001/"

class Study extends Control:
	var rows: Array[Dictionary] = []
	var textures: Array[Texture2D] = []
	var baby: Texture2D
	var current := 0
	var geometry: Array[Dictionary] = []

	func _draw() -> void:
		geometry.clear()
		var row: Dictionary = rows[current]
		var side: float = float(row["side"])
		var hip_xy: Array = row["hip_xy"]
		var palm_xy: Array = row["palm_xy"]
		for index: int in range(2):
			var extent: float = 250.0 if index == 0 else 500.0
			var infant_extent: float = 72.0 if index == 0 else 144.0
			var pivot := Vector2(size.x * (0.25 if index == 0 else 0.75),
				440.0 if index == 0 else 580.0)
			var origin: Vector2 = pivot - Vector2(float(hip_xy[0]), float(hip_xy[1])) * extent / side
			var palm: Vector2 = origin + Vector2(float(palm_xy[0]), float(palm_xy[1])) * extent / side
			draw_texture_rect(textures[current], Rect2(origin, Vector2.ONE * extent), false)
			draw_texture_rect(baby, Rect2(palm - Vector2(0.55224609375, 0.912109375) * infant_extent,
				Vector2.ONE * infant_extent), false)
			draw_string(ThemeDB.fallback_font, Vector2(size.x * float(index) * 0.5 + 16.0, 54.0),
				"250px whole card / 72px baby" if index == 0 else "2x diagnostic detail",
				HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color(0.15, 0.1, 0.3))
			geometry.append({"extent": extent, "baby_extent": infant_extent,
				"pivot": [pivot.x, pivot.y], "palm": [palm.x, palm.y]})
		draw_string(ThemeDB.fallback_font, Vector2(16, 26),
			"UNBOUND SOURCE STUDY: " + String(row["name"]),
			HORIZONTAL_ALIGNMENT_LEFT, -1, 20, Color(0.15, 0.1, 0.3))

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	assert(not FileAccess.file_exists(FOLDER + "MANIFEST.json"), "Packet is sealed")
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://assets/opera/worlds/nursery/refinement_v2/care_keys.json"))
	var chain: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(FOLDER + "CHAIN_V2_DATA.json"))
	var study := Study.new()
	var first: Dictionary = (data["poses"] as Array)[3].duplicate(true)
	first.merge({"name": "Current hold key3", "side": 512.0}, true)
	study.rows.append(first)
	for source: Dictionary in chain["poses"]:
		var row: Dictionary = source.duplicate(true)
		row.merge({"name": row["label"], "side": row["review_side"]}, true)
		study.rows.append(row)
	var last: Dictionary = (data["poses"] as Array)[4].duplicate(true)
	last.merge({"name": "Current first lower key4", "side": 512.0}, true)
	study.rows.append(last)
	for row: Dictionary in study.rows:
		study.textures.append(ImageTexture.create_from_image(Image.load_from_file("res://" + String(row["path"]))))
	study.baby = ImageTexture.create_from_image(Image.load_from_file(
		"res://assets_src/imagegen/day2_nursery_babies_v2_20261001/baby_0_review.png"))
	var backdrop := OperaWorldBackdrop2D.new()
	root.add_child(backdrop)
	backdrop.setup("nursery", "")
	root.add_child(study)
	var cases: Array[Dictionary] = []
	for width: int in [1280, 1600]:
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		backdrop.size = Vector2(width, 720)
		study.size = Vector2(width, 720)
		var folder := "motion_fit/%dx720/" % width
		DirAccess.make_dir_recursive_absolute(FOLDER + folder)
		var samples: Array[Dictionary] = []
		for frame: int in range(45):
			study.current = clampi(frame - 14, 0, 5)
			study.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var path := folder + "%04d.webp" % frame
			assert(root.get_texture().get_image().save_webp(FOLDER + path, false) == OK)
			samples.append({"frame": frame, "authored_key": study.current,
				"path": path, "sha256": FileAccess.get_sha256(FOLDER + path),
				"geometry": study.geometry.duplicate(true), "source": study.rows[study.current]["path"],
				"source_sha256": FileAccess.get_sha256("res://" + String(study.rows[study.current]["path"]))})
		cases.append({"dimensions": [width, 720], "frames": samples})
	var receipt := {"engine": Engine.get_version_info()["string"],
		"renderer": RenderingServer.get_current_rendering_method(), "review_playback_fps": 30,
		"timeline": "0-14 quiet hold;15-19 five authored changes;20-44 endpoint quiet hold. At30fps the five changes occupy0.167s, matching the existing hold/lower slot. This diagnostic is assembled from authored complete gameplay figures; no pixels are blended.",
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_lower_motion_fit.gd"),
		"chain_sha256": FileAccess.get_sha256(FOLDER + "CHAIN_V2_DATA.json"), "cases": cases,
		"qualification": "Source-only fixed-pivot study with production-size72px infant and2x inspection. No touch, gameplay, runtime binding, save, action pass, owner/device/child or cinematic delivery claim."}
	var file := FileAccess.open(FOLDER + "motion_fit/receipt.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	print("NURSERY_LOWER_MOTION_FIT|CAPTURED|90|UNBOUND_SOURCE_ONLY")
	quit()
