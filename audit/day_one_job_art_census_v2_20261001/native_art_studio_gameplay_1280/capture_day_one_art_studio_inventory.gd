extends "res://scripts/probe_day_one_art_studio_shots.gd"
const ART_TRACE := preload("res://tools/job_art_scene_trace.gd")

func _capture(name: String) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	ART_TRACE.save_frame_receipt(root, name, capture_root,
		"res://tools/capture_day_one_art_studio_inventory.gd", "res://scripts/probe_day_one_art_studio_shots.gd")
	var receipt_path: String = capture_root.path_join(name + ".json")
	var receipt: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(receipt_path)) as Dictionary
	receipt["qualification"] = str(receipt["qualification"]) + " Gameplay-only: story clips marked seen in isolated save and window forced1280x720. Original probe gestures/assertions retained."
	var file: FileAccess = FileAccess.open(receipt_path, FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()

func _run() -> void:
	capture_root = OS.get_environment("DAY_ONE_ART_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path("user://day_one_art_studio_shots")
	_check("capture directory",
		DirAccess.make_dir_recursive_absolute(capture_root) == OK, capture_root)
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	root.add_child(main)
	await _frames(3)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await _frames(3)
	# Qualified gameplay-only diagnostic in an isolated save; ordinary clips remain a separate lane.
	for movie_id: String in DayOneStoryClips.clip_ids():
		main.day_one_story_clips_seen[movie_id] = true
	main._day_one_cancel_story_clips()
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(root.size)
	await _frames(6)
	main._day_one_ref().restore_state({
		"day_one_active": true,
		"day_one_completed_rooms": ["bathroom", "pool", "stuffie"],
		"day_one_art_collected_materials": {},
		"day_one_art_cleaned_grime": {},
		"day_one_art_desk_unlocked": false,
		"day_one_art_customization_completed": false,
	})
	main.pearl_count = 10
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	main._castle_rooms_ref().show_room("craft_room", false)
	await _frames(12)
	_check("studio opened", main._open_day_one_art_studio())
	await _frames(4)
	var studio: DayOneArtStudio = main._day_one_art_studio
	_check("studio mounted", studio != null)
	if studio == null:
		main.queue_free()
		quit(1)
		return
	await _capture("00_loose_supplies")

	for material_id: String in DayOneDirector.ART_MATERIAL_IDS:
		_check("collect %s" % material_id,
			main.day_one_record_art_cleanup("material", material_id))
	studio.refresh_from_state()
	await _capture("01_grime_revealed")

	for grime_id: String in ["left_counter", "desk_counter"]:
		_check("clean %s" % grime_id,
			main.day_one_record_art_cleanup("grime", grime_id))
	studio.refresh_from_state()
	await _capture("02_last_grime")
	_check("clean right_counter",
		main.day_one_record_art_cleanup("grime", "right_counter"))
	studio.refresh_from_state()
	await _capture("03_glowing_desk")

	studio._on_desk_pressed()
	await _frames(8)
	await _capture("04_customizer_bubbles")
	var customizer: AttackCustomizer = main._attack_customizer
	_check("customizer mounted", customizer != null)
	if customizer != null:
		customizer.attack_color = Color(1.0, 0.48, 0.55, 1.0)
		customizer.attack_effect = "splashes"
		customizer._refresh_choices()
		await _capture("05_customizer_splashes")
		# Gameplay impacts occur after confirmation, not behind the modal. Hide
		# only the review surface here so the next capture sees the live FX layer.
		customizer.visible = false

	var hit_engine := HitEngine.new(main)
	hit_engine.show_attack_feedback_2d(Vector2(640.0, 360.0),
		Color(1.0, 0.48, 0.55, 1.0), "splashes")
	await _frames(4)
	await _capture("06_splash_attack_frame")
	main.queue_free()
	await _frames(4)
	print("DAY_ONE_ART_STUDIO_SHOTS|RESULT: %s failures=%d output=%s" % [
		"PASS" if failures == 0 else "FAIL", failures, capture_root])
	quit(1 if failures > 0 else 0)

