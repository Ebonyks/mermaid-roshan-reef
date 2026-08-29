extends SceneTree
## Non-headless Mobile-renderer evidence for Stage 1's dirty Main Hall.

var failures := 0
var capture_root := ""


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(name: String) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path: String = capture_root.path_join(name + ".png")
	var error: Error = image.save_png(path)
	var ok: bool = not image.is_empty() and error == OK
	if not ok:
		failures += 1
	print("HALL_CAPTURE|%s: %s path=%s" % [
		name, "OK" if ok else "FAIL", path])


func _check_partial_wall_pixels() -> void:
	var dirty_path: String = capture_root.path_join("dirty_left.png")
	var partial_path: String = capture_root.path_join(
		"partial_wall_a_clean_left.png")
	var dirty: Image = Image.load_from_file(dirty_path)
	var partial: Image = Image.load_from_file(partial_path)
	if dirty == null or partial == null or dirty.is_empty() \
			or partial.is_empty():
		failures += 1
		print("HALL_CAPTURE|wall_a framebuffer evidence: FAIL images_missing")
		return
	var changed_samples: int = 0
	var total_delta: float = 0.0
	var sample_count: int = 0
	# The capture is a 2x presentation of the 1280x720 storybook canvas. This
	# rectangle encloses wall_a while excluding Roshan and the floor targets.
	for y: int in range(250, mini(700, dirty.get_height()), 8):
		for x: int in range(1800, mini(2400, dirty.get_width()), 8):
			sample_count += 1
			var before: Color = dirty.get_pixel(x, y)
			var after: Color = partial.get_pixel(x, y)
			var delta: float = absf(before.r - after.r) \
				+ absf(before.g - after.g) \
				+ absf(before.b - after.b)
			total_delta += delta
			if delta > 0.08:
				changed_samples += 1
	var sample_count_ok: bool = sample_count > 0
	var mean_delta: float = total_delta / float(maxi(sample_count, 1))
	var changed_ratio: float = float(changed_samples) \
		/ float(maxi(sample_count, 1))
	var passed: bool = sample_count_ok and changed_ratio >= 0.04 \
		and mean_delta >= 0.05
	if not passed:
		failures += 1
	var evidence: String = "HALL_CAPTURE|wall_a framebuffer evidence: %s " \
		% ["OK" if passed else "FAIL"]
	evidence += "samples=%d mean_delta=%.3f changed=%.1f%%" % [sample_count,
		mean_delta, changed_ratio * 100.0]
	print(evidence)

	# Check a fixed upper-left wall lamp/stonework ROI that is outside wall_a.
	# This region has no actor, bunny, pointer, or animated gameplay elements,
	# so a partial clean must leave it pixel-stable while wall_a changes.
	var stable_changed_samples: int = 0
	var stable_total_delta: float = 0.0
	var stable_sample_count: int = 0
	for y: int in range(180, mini(390, dirty.get_height()), 8):
		for x: int in range(620, mini(860, dirty.get_width()), 8):
			stable_sample_count += 1
			var before: Color = dirty.get_pixel(x, y)
			var after: Color = partial.get_pixel(x, y)
			var delta: float = absf(before.r - after.r) \
				+ absf(before.g - after.g) \
				+ absf(before.b - after.b)
			stable_total_delta += delta
			if delta > 0.08:
				stable_changed_samples += 1
	var stable_count_ok: bool = stable_sample_count > 0
	var stable_mean_delta: float = stable_total_delta \
		/ float(maxi(stable_sample_count, 1))
	var stable_changed_ratio: float = float(stable_changed_samples) \
		/ float(maxi(stable_sample_count, 1))
	var stable_passed: bool = stable_count_ok and stable_mean_delta <= 0.03 \
		and stable_changed_ratio <= 0.02
	if not stable_passed:
		failures += 1
	print("HALL_CAPTURE|outside-target stability: %s samples=%d " \
		% ["OK" if stable_passed else "FAIL", stable_sample_count] \
		+ "mean_delta=%.3f changed=%.1f%%" % [stable_mean_delta,
			stable_changed_ratio * 100.0])


func _run() -> void:
	if DisplayServer.get_name() == "headless":
		print("HALL_CAPTURE|FAIL: a real display is required")
		quit(1)
		return
	capture_root = OS.get_environment("CASTLE_DAY_ONE_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path(
			"user://day_one_main_hall_capture")
	DirAccess.make_dir_recursive_absolute(capture_root)
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	root.add_child(main)
	await _frames(2)
	main._skip_intro()
	await _frames(2)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		await _frames(2)
	main.pearl_count = 10
	main.trophies = 5
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main.day_one_active = true
	main.day_one_hall_cleanup_mask = 0
	main.day_one_hall_shock_seen = false
	main.day_one_hall_celebration_done = false
	main._enter_castle_interior_now(false)
	await _frames(4)
	await _capture("dirty_shock_left")
	await create_timer(2.3).timeout
	await _capture("dirty_left")
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var cleanup: DayOneMainHallCleanup = main.day_one_main_hall_cleanup
	cleanup.call("_clean_target", "wall_a")
	await _frames(8)
	var wall_a_progress := 0.0
	for tile: Sprite2D in main.castle_room_background_tiles:
		var progress: Dictionary = tile.get_meta(
			"day_one_hall_reveal_progress", {}) as Dictionary
		wall_a_progress = maxf(wall_a_progress,
			float(progress.get("wall_a", 0.0)))
	print("HALL_CAPTURE|partial wall_a bit=%s progress=%.1f modal=%s shock=%s" % [
		main._day_one_ref().hall_target_clean("wall_a"), wall_a_progress,
		main.day_one_hall_cleanup_modal, cleanup.get("_shock_blocked")])
	await _capture("partial_wall_a_clean_left")
	_check_partial_wall_pixels()
	rooms._position_hall_player_at_foot(Vector2(2960.0, 835.0), false)
	await _frames(75)
	await _capture("dirty_right")
	rooms._explode_dust_bunny("sleepy_bunny")
	rooms._explode_dust_bunny("shell_bunny")
	rooms._explode_dust_bunny("runner_bunny")
	for target_id: String in DayOneDirector.HALL_LIGHT_TARGET_IDS:
		cleanup.call("_clean_target", target_id)
	for target_id: String in DayOneDirector.HALL_SCRUB_TARGET_IDS:
		if target_id != "floor_b":
			cleanup.call("_clean_target", target_id)
	cleanup.call("_clean_target", "floor_b")
	await _frames(8)
	await _capture("clean_right_completion")
	rooms._position_hall_player_at_foot(Vector2(380.0, 835.0), false)
	await _frames(75)
	await _capture("clean_left")
	main.queue_free()
	await _frames(3)
	print("HALL_CAPTURE|RESULT: %s output=%s" % [
		"PASS" if failures == 0 else "FAIL", capture_root])
	quit(1 if failures > 0 else 0)


func _init() -> void:
	call_deferred("_run")
