extends SceneTree
## Mobile-renderer visual evidence for every Day One pool-cleaning state.

var failures: int = 0
var capture_root: String = ""


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(name: String) -> void:
	var was_paused: bool = paused
	paused = true
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path: String = capture_root.path_join(name + ".png")
	var save_error: Error = image.save_png(path)
	_check("capture %s" % name,
		not image.is_empty() and save_error == OK,
		"size=%s path=%s" % [image.get_size(), path])
	paused = was_paused


func _run() -> void:
	Engine.max_fps = 60
	capture_root = OS.get_environment("DAY_ONE_POOL_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path("user://day_one_pool_shots")
	var dir_error: Error = DirAccess.make_dir_recursive_absolute(capture_root)
	_check("capture directory", dir_error == OK, capture_root)
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
		"day_one_completed_rooms": ["bathroom"],
		"day_one_pool_cleanup_step": 0,
		"day_one_pool_skimmer_mask": 0,
		"day_one_pool_waterfall_mask": 0,
		"day_one_pool_seahorse_tugs": 0,
	})
	main.pearl_count = 10
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("mermaid_pool", false)
	await _frames(12)
	var cleanup: DayOnePoolCleanup = rooms.day_one_pool_cleanup
	_check("dirty pool mounted", cleanup != null)
	if cleanup == null:
		main.queue_free()
		quit(1)
		return
	var waterfall_record: Dictionary = main.castle_room_item_sprites.get(
		"waterfall", {}) as Dictionary
	var clean_waterfall: Sprite2D = waterfall_record.get("sprite") as Sprite2D
	_check("dirty state fully hides clean rainbow waterfall",
		clean_waterfall != null and not clean_waterfall.visible)
	await _capture("00_dirty_arrival")

	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	var touch := InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = true
	touch.position = PoolSkimmerActivity.TRASH_POSITIONS[0]
	skimmer._gui_input(touch)
	touch.pressed = false
	skimmer._gui_input(touch)
	await create_timer(0.22).timeout
	_check("approach cannot collect remotely", int(skimmer.audit_snapshot()["mask"]) == 0)
	await _capture("00a_roshan_approaching_trash")
	var scoop_deadline: int = Time.get_ticks_msec() + 8000
	while Time.get_ticks_msec() < scoop_deadline:
		await process_frame
		if float(skimmer.audit_snapshot()["scoop_time"]) > 0.08:
			break
	_check("Roshan reaches the visible scoop", float(skimmer.audit_snapshot()["scoop_time"]) > 0.0)
	skimmer.set_process(false)
	await _capture("00b_roshan_scooping_trash")
	skimmer.set_process(true)
	var catch_deadline: int = Time.get_ticks_msec() + 4000
	while Time.get_ticks_msec() < catch_deadline:
		await process_frame
		if int(skimmer.audit_snapshot()["mask"]) == 1:
			break
	_check("skimmer first catch after travel and scoop", int(skimmer.audit_snapshot()["mask"]) == 1)
	await _frames(2)
	await _capture("01_skimmer_catch")
	for _trash_index: int in range(5):
		_check("skimmer remaining catch", cleanup.skimmer_activity.probe_collect_next())
	await _frames(40)
	_check("waterfall unlocked after pool clear",
		String(cleanup.audit_snapshot().get("current_activity", "")) == "waterfall")
	await _capture("02_pool_clear_waterfall_dirty")

	_check("waterfall first scrub lane",
		cleanup.waterfall_activity.probe_clear_next_lane())
	await _frames(4)
	await _capture("03_waterfall_scrub")
	_check("waterfall second scrub lane",
		cleanup.waterfall_activity.probe_clear_next_lane())
	_check("waterfall final scrub lane",
		cleanup.waterfall_activity.probe_clear_next_lane())
	await _frames(34)
	_check("seahorse unlocked after waterfall clear",
		String(cleanup.audit_snapshot().get("current_activity", "")) == "seahorse")
	_check("rainbow flow remains stopped during rescue",
		clean_waterfall != null and clean_waterfall.visible)
	await _capture("04_waterfall_clear_static")

	for _tug_index: int in range(4):
		_check("seahorse opening tug", cleanup.seahorse_activity.probe_tap())
	await _frames(3)
	await _capture("05_seahorse_tug_midway")
	for _tug_index: int in range(4):
		_check("seahorse release tug", cleanup.seahorse_activity.probe_tap())
	await _frames(5)
	await _capture("06_seahorse_trash_release")
	var reveal_deadline: int = Time.get_ticks_msec() + 8000
	while Time.get_ticks_msec() < reveal_deadline:
		await process_frame
		if is_instance_valid(cleanup._rumi) and cleanup._rumi.modulate.a >= 0.8:
			break
	_check("Rumi is visible during her reveal",
		is_instance_valid(cleanup._rumi) and cleanup._rumi.modulate.a >= 0.8)
	await _capture("07_rainbow_reveal_active")
	await create_timer(0.3).timeout
	_check("reveal capture precedes next-room overlay",
		is_instance_valid(cleanup._rumi) and cleanup._rumi.animation == &"swim")
	await _capture("08_rumi_reveal")
	main.queue_free()
	await _frames(4)
	print("DAY_ONE_POOL_SHOTS|RESULT: %s failures=%d output=%s" % [
		"PASS" if failures == 0 else "FAIL", failures, capture_root])
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_POOL_SHOTS|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		(" (%s)" % detail) if detail != "" else "",
	])
