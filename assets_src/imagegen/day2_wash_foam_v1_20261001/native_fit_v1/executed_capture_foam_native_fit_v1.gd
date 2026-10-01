extends SceneTree
## Unbound existing-art comparison in actual career nodes; no production edits.
const OUT := "res://tmp/wash_foam_native_fit_v1/native_views/"
const CANDIDATE := "res://assets_src/imagegen/day2_wash_foam_v1_20261001/attempt_02_whole_canvas_1024x608.png"
var main: ReefMain
var views: Array[Dictionary] = []
func _initialize() -> void:
	_run.call_deferred()
func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame
func _snapshot(world: OperaCareerWorld2D, width: int, name: String, detail: Dictionary) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path: String = "%s_%d_%s.webp" % [world.career_id, width, name]
	assert(image.save_webp(OUT + path, true) == OK)
	var row: Dictionary = detail.duplicate(true)
	row["path"] = path
	row["sha256"] = FileAccess.get_sha256(OUT + path)
	row["viewport"] = [image.get_width(), image.get_height()]
	row["career"] = world.career_id
	row["phase_index"] = world.phase_index
	row["phase_name"] = String(world.phases[world.phase_index].get("name", ""))
	row["phase_progress"] = world.phase_progress
	row["task_open"] = world.task_open
	row["qualification"] = "Current native career fixture, renderer and actual invitation/activity nodes. Candidate overrides are diagnostic only. No played root route, complete action, persistence, phone, child or owner acceptance."
	views.append(row)
func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	var saved_stars: int = main.opera_stars
	var candidate_texture: Texture2D = ImageTexture.create_from_image(Image.load_from_file(CANDIDATE))
	assert(candidate_texture.get_size() == Vector2(1024, 608))
	for width: int in [1280, 1600]:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		await _frames(5)
		for career: String in ["doctor", "nursery"]:
			var config: Dictionary = {}
			for act: Dictionary in OperaHouse.ACTS:
				if String(act.get("costume", "")) == career:
					config = act.duplicate(true)
			assert(not config.is_empty())
			var competition: OperaCompetition = OperaCompetition.new()
			competition.configure(career)
			var world: OperaCareerWorld2D = OperaCareerWorld2D.new()
			main.add_child(world)
			world.setup(main, config, competition, Callable())
			await _frames(8)
			world.set_process(false)
			world.phase_index = 0
			world.active = true
			world.reveal_t = 0.0
			world.phase_advance_pending = false
			world.phase_gap = 0.0
			world._arm_phase()
			await _frames(8)
			await create_timer(0.65).timeout
			var hotspot: OperaWorldHotspot2D = world._active_hotspot()
			assert(hotspot != null and hotspot.armed and hotspot.presentation == "effect")
			hotspot.set_process(false)
			hotspot.elapsed = 0.35
			var original: Texture2D = hotspot.object_texture
			var original_size: Vector2 = hotspot.object_size
			assert(original.get_size() == Vector2(1024, 608))
			for variant: Dictionary in [{"name":"original", "cell":-1, "extent":0.0}, {"name":"fresh_foam02", "cell":-2, "extent":0.0}]:
				var cell: int = int(variant["cell"])
				if cell == -1:
					hotspot.object_texture = original
					hotspot.object_size = original_size
				else:
					hotspot.object_texture = candidate_texture
					hotspot.object_size = original_size
				hotspot.queue_redraw()
				var canvas_center: Vector2 = hotspot.get_global_transform_with_canvas() * hotspot.object_center
				await _snapshot(world, width, String(variant["name"]), {"source":hotspot.source_path if cell == -1 else CANDIDATE, "source_sha256":FileAccess.get_sha256(hotspot.source_path if cell == -1 else CANDIDATE), "atlas_cell":cell, "cell_region":[float(cell % 4) * 256.0, 0.0, 256.0, 256.0] if cell >= 0 else [], "draw_size":[hotspot.object_size.x,hotspot.object_size.y], "hotspot_canvas_center":[canvas_center.x,canvas_center.y], "visible":hotspot.is_visible_in_tree(), "armed":hotspot.armed})
			hotspot.object_texture = original
			hotspot.object_size = original_size
			assert(hotspot.object_texture.resource_path == hotspot.source_path)
			assert(main.opera_stars == saved_stars)
			world.close()
			world.queue_free()
			await _frames(4)
	assert(views.size() == 8)
	var file: FileAccess = FileAccess.open(OUT + "CAPTURE_RECEIPT.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"EIGHT_UNBOUND_FRESH_FOAM_INVITATION_VIEWS", "views":views, "stars_unchanged":main.opera_stars==saved_stars, "sequence_score":null}, "\t") + "\n")
	file.close()
	print("FRESH_FOAM_NATIVE_FIT|PASS 8 unbound source/native views; no sequence acceptance")
	main.queue_free()
	await _frames(3)
	quit(0)
