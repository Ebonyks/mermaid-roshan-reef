extends SceneTree
## Mobile-renderer visual evidence for every Day One pool-cleaning state.

var failures: int = 0
var capture_root: String = ""
var fixture_main: ReefMain = null


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
	var profile_root: String = OS.get_environment("POOL_CAPTURE_PROFILE_ROOT").replace("\\", "/").to_lower()
	var user_data: String = ProjectSettings.globalize_path("user://").replace("\\", "/")
	print("POOL_PROFILE|" + user_data)
	if not profile_root.is_empty() and not user_data.to_lower().begins_with(profile_root + "/"):
		_check("isolated profile is active before scene load", false, user_data)
		quit(1)
		return
	var shape: Vector2i = Vector2i(1280, 800) if OS.get_environment("POOL_CAPTURE_TALL") == "1" else Vector2i(1280, 720)
	DisplayServer.window_set_size(shape)
	root.size = shape
	# Explicit direct-room visual fixture: selected story footage is canceled
	# only here so it cannot occlude a purported gameplay capture (MA-CI-008).
	process_frame.connect(_cancel_fixture_clips)
	print("POOL_CAPTURE|fixture=direct_room|clips=cancelled|shape=%s|renderer=%s" % [shape, RenderingServer.get_current_rendering_method()])
	capture_root = OS.get_environment("DAY_ONE_POOL_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path("user://day_one_pool_shots")
	var dir_error: Error = DirAccess.make_dir_recursive_absolute(capture_root)
	_check("capture directory", dir_error == OK, capture_root)
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	fixture_main = main
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
	await create_timer(1.0).timeout
	await _capture("00c_missed_piece_hand")
	if OS.get_environment("POOL_CAPTURE_MOTION") == "1":
		await _capture_motion("dirty", 12.0)

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
	var middle_deadline: int = Time.get_ticks_msec() + 10000
	while cleanup.seahorse_activity._taps < 4 and Time.get_ticks_msec() < middle_deadline:
		await process_frame
	_check("four requested tugs have each reached contact", cleanup.seahorse_activity._taps == 4)
	await _capture("05_seahorse_tug_midway")
	for _tug_index: int in range(4):
		_check("seahorse release tug", cleanup.seahorse_activity.probe_tap())
	await _frames(5)
	await _capture("06_seahorse_trash_release")
	var reveal_deadline: int = Time.get_ticks_msec() + 8000
	while Time.get_ticks_msec() < reveal_deadline:
		await process_frame
		if bool(cleanup.audit_snapshot().get("finale_started", false)) \
				and float(cleanup.audit_snapshot().get("tint_ratio", 1.0)) <= 0.05:
			break
	_check("the clean-pool light has returned",
		float(cleanup.audit_snapshot().get("tint_ratio", 1.0)) <= 0.05)
	await _capture("07_rainbow_reveal_active")
	await create_timer(0.3).timeout
	# Rumi rises once, in the room-completion clip (owner QP-1), so the room's
	# reveal frame shows the clean pool without her.
	_check("reveal capture precedes next-room overlay",
		bool(cleanup.audit_snapshot().get("reveal_beat_holding", false))
		and not bool(cleanup.audit_snapshot().get("in_room_rumi_rise", true)))
	await _capture("08_clean_pool_reveal")
	# Same exact painted fixtures at four advancing times, for flow-direction
	# and settle inspection. A single still cannot establish continuous motion.
	for sample: int in range(4):
		await create_timer(0.15).timeout
		await _capture("08_water_motion_%d" % sample)
	# Directly stage the post-clip persistent friend; this is composition and
	# registration evidence, never proof of the selected clip or normal route.
	main.day_one_pool_rumi_met = true
	main.day_one_completed_rooms["pool"] = true
	main.day_one_cleaned_rooms["pool"] = true
	rooms._clear_day_one_pool_cleanup()
	rooms._sync_day_one_persistent_rumi()
	_check("persistent Rumi is actually visible after the clip fixture", is_instance_valid(rooms._day_one_persistent_rumi) and rooms._day_one_persistent_rumi.is_visible_in_tree())
	_check("post-clip Rumi has a live visible hotspot", is_instance_valid(rooms._day_one_persistent_rumi_hotspot) and rooms._day_one_persistent_rumi_hotspot.is_visible_in_tree())
	var greetings: int = int(main.g.get("day_one_persistent_rumi_greeting_count", 0))
	for point: Vector2 in [Vector2(460.0, 410.0), Vector2(490.0, 429.0), Vector2(719.0, 405.0)]:
		await _route_touch(main.castle_room_world_root.get_global_transform_with_canvas() * point)
	_check("native petal and star taps are never stolen by Rumi",
		int(main.g.get("day_one_persistent_rumi_greeting_count", 0)) == greetings)
	var rumi_button: Button = rooms._day_one_persistent_rumi_hotspot
	await _route_touch(rumi_button.get_global_transform_with_canvas() * (rumi_button.size * 0.5))
	_check("native Rumi body touch greets once", int(main.g.get("day_one_persistent_rumi_greeting_count", 0)) == greetings + 1)
	await create_timer(1.5).timeout
	await _frames(8)
	await _capture("09_persistent_rumi_rest")
	if OS.get_environment("POOL_CAPTURE_MOTION") == "1":
		rooms._on_day_one_persistent_rumi_pressed()
		await _capture_motion("clean", 4.0)
	rooms._on_day_one_persistent_rumi_pressed()
	await _capture("10a_rumi_greet_start")
	await create_timer(0.26).timeout
	await _capture("10b_rumi_greet_reach")
	await create_timer(0.26).timeout
	await _capture("10_persistent_rumi_greeting")
	await create_timer(0.26).timeout
	await _capture("10d_rumi_greet_return")
	await create_timer(0.26).timeout
	await _capture("10e_rumi_greet_rest")
	await create_timer(1.2).timeout
	await _capture("11_persistent_rumi_settled")
	main.queue_free()
	await _frames(4)
	print("DAY_ONE_POOL_SHOTS|RESULT: %s failures=%d output=%s" % [
		"PASS" if failures == 0 else "FAIL", failures, capture_root])
	quit(1 if failures > 0 else 0)


func _cancel_fixture_clips() -> void:
	if is_instance_valid(fixture_main) and fixture_main._day_one_story_clip != null:
		fixture_main._day_one_cancel_story_clips()


func _route_touch(point: Vector2) -> void:
	var touch := InputEventScreenTouch.new()
	touch.index = 0
	touch.position = point
	touch.pressed = true
	root.push_input(touch)
	await process_frame
	touch.pressed = false
	root.push_input(touch)
	await _frames(3)


func _capture_motion(label: String, seconds: float) -> void:
	var directory: String = capture_root.path_join("motion_" + label)
	DirAccess.make_dir_recursive_absolute(directory)
	var start: int = Time.get_ticks_msec()
	var frame: int = 0
	var images: Array[Image] = []
	var times: Array[float] = []
	while float(Time.get_ticks_msec() - start) / 1000.0 < seconds:
		await RenderingServer.frame_post_draw
		var elapsed: float = float(Time.get_ticks_msec() - start) / 1000.0
		images.append(root.get_viewport().get_texture().get_image())
		times.append(elapsed)
		await create_timer(1.0 / 12.0).timeout
	# Encode PNGs after sampling, so PNG compression cannot stall the animation
	# whose timing is being reviewed. Actual timestamps remain the timing source.
	for index: int in range(images.size()):
		images[index].save_png(directory.path_join("%04d.png" % index))
		print("POOL_MOTION|%s|%d|%.4f" % [label, index, times[index]])


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_POOL_SHOTS|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		(" (%s)" % detail) if detail != "" else "",
	])
