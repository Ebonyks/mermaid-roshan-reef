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
	root.size = Vector2i(1280, 720)
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
	var polish: DayOneRoomPolish = main._day_one_room_polish
	_check("new rainbow-spill task mounted first", polish != null
		and String(polish.audit_snapshot().get("task_id", ""))
		== "rainbow_paint_spill")
	await _capture("00a_dirty_rainbow_spill")
	_check("one tap completes rainbow-spill task", polish != null
		and polish.probe_complete())
	await create_timer(1.35).timeout
	_check("rainbow-spill task saves immediately",
		main.day_one_room_polish_is_complete("art"))
	_check("studio opened", main._day_one_art_studio != null
		or main._open_day_one_art_studio())
	await _frames(4)
	var studio: DayOneArtStudio = main._day_one_art_studio
	_check("studio mounted", studio != null)
	if studio == null:
		main.queue_free()
		quit(1)
		return
	await _capture("00_loose_supplies")
	var entry_snapshot: Dictionary = studio.audit_snapshot()
	_check("grime is visible from dirty entry",
		bool(entry_snapshot.get("grime_visible_from_entry", false)))
	studio._on_material_pressed("pink_paint")
	_check("inactive material cannot skip the ordered pointer",
		not bool(main.day_one_art_collected_materials.get("pink_paint", false)))

	for material_id: String in DayOneDirector.ART_MATERIAL_IDS:
		studio._on_material_pressed(material_id)
		_check("collect active %s" % material_id,
			bool(main.day_one_art_collected_materials.get(material_id, false)))
		_check("exactly one Art target remains active",
			int(studio.audit_snapshot().get("active_target_count", 0)) == 1)
	await _capture("01_grime_revealed")

	studio._on_grime_pressed("right_counter")
	_check("inactive grime cannot skip the ordered pointer",
		not bool(main.day_one_art_cleaned_grime.get("right_counter", false)))
	for grime_id: String in ["left_counter", "desk_counter"]:
		studio._on_grime_pressed(grime_id)
		_check("clean active %s" % grime_id,
			bool(main.day_one_art_cleaned_grime.get(grime_id, false)))
		_check("exactly one Art target remains active",
			int(studio.audit_snapshot().get("active_target_count", 0)) == 1)
	await _capture("02_last_grime")
	studio._on_grime_pressed("right_counter")
	_check("clean active right_counter",
		bool(main.day_one_art_cleaned_grime.get("right_counter", false)))
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

	var hit_engine := HitEngine.new(main)
	hit_engine.show_attack_feedback_2d(Vector2(640.0, 360.0),
		Color(1.0, 0.48, 0.55, 1.0), "splashes")
	await _frames(4)
	await _capture("06_splash_attack_frame")
	if customizer != null:
		# Use the same public close path as the large picture-only confirm button;
		# its callback completes the saved room and removes temporary cleanup art.
		customizer.close()
	await create_timer(0.42).timeout
	await _capture("07_whole_room_sparkle")
	await create_timer(0.72).timeout
	_check("art room completed after picture confirmation",
		main._day_one_ref().is_room_completed("art"))
	_check("completion settles in the clean studio before any optional picker",
		main.castle_logo_layer == null)
	await _capture("08_clean_art_room")
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
