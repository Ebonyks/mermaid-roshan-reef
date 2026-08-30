extends SceneTree
## Mobile-renderer visual evidence for the Day One Art Studio intake gates.

var failures := 0
var capture_root := ""


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(name: String) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path: String = capture_root.path_join(name + ".png")
	var save_error: Error = image.save_png(path)
	_check("capture %s" % name, not image.is_empty() and save_error == OK,
		"size=%s path=%s" % [image.get_size(), path])


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
	if customizer != null:
		# Follow the same public close/confirm callback as the gold heart button.
		customizer.visible = true
		customizer.close()
	await _frames(12)
	_check("customization accepted", main.day_one_art_customization_completed)
	_check("studio completion opens boss route",
		main.day_one_boss_door_ready() and main.castle_room_id == "main_hall")
	await _capture("07_main_hall_boss_wayfinding")
	main.queue_free()
	await _frames(4)
	print("DAY_ONE_ART_STUDIO_SHOTS|RESULT: %s failures=%d output=%s" % [
		"PASS" if failures == 0 else "FAIL", failures, capture_root])
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_ART_STUDIO_SHOTS|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		(" (%s)" % detail) if detail != "" else "",
	])
