extends "res://tools/capture_day_one_pool_normalized_layout_fit.gd"
## Unpaused native collection studies; encode images only after all six actions.
## Readback still affects cadence. Actual timestamps are authoritative, not30fps intent.

var buffered_images: Array[Image] = []
var buffered_rows: Array[Dictionary] = []
var action_rows: Array[Dictionary] = []

func _run() -> void:
	Engine.max_fps = 60
	capture_root = OS.get_environment("DAY_ONE_POOL_CAPTURE_OUT")
	assert(capture_root != "")
	assert(DirAccess.make_dir_recursive_absolute(capture_root) == OK)
	var main: ReefMain = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _frames(3)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await _frames(3)
	for movie_id: String in DayOneStoryClips.clip_ids():
		main.day_one_story_clips_seen[movie_id] = true
	main._day_one_cancel_story_clips()
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(root.size)
	await _frames(6)
	main._day_one_ref().restore_state({"day_one_active": true,
		"day_one_completed_rooms": ["bathroom"], "day_one_pool_cleanup_step": 0,
		"day_one_pool_skimmer_mask": 0, "day_one_pool_waterfall_mask": 0,
		"day_one_pool_seahorse_tugs": 0})
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
		quit(1)
		return
	await _capture("00_initial_layout")
	for index: int in range(6):
		await _record_action(index, cleanup)
	await _frames(4)
	_check("all six collection bits", main.day_one_pool_skimmer_mask == 63)
	_check("waterfall unlocked", String(cleanup.audit_snapshot().get("current_activity", "")) == "waterfall")
	await _capture("01_pool_clear")
	main.queue_free()
	await _frames(4)
	# No encoding, scene hashing or disk writes occur during the action spans above.
	for index: int in range(buffered_images.size()):
		var filename: String = "frame_%04d.webp" % index
		var output_path: String = capture_root.path_join(filename)
		var error: Error = buffered_images[index].save_webp(output_path, true, 1.0)
		assert(error == OK)
		buffered_rows[index]["path"] = filename
		buffered_rows[index]["sha256"] = FileAccess.get_sha256(output_path)
	buffered_images.clear()
	var harness: String = "res://tools/capture_day_one_pool_buffered_actions.gd"
	var receipt: Dictionary = {"schema": "reef.native-buffered-action-study.v1",
		"harness": harness, "harness_sha256": FileAccess.get_sha256(harness),
		"engine": Engine.get_version_info(), "dimensions": [1280, 720],
		"candidate_bindings": candidate_bindings, "actions": action_rows,
		"frames": buffered_rows, "checks_failed": failures,
		"layout_profile_sha256": FileAccess.get_sha256(CANDIDATE_ROOT + "NORMALIZED_LAYOUT_PROFILE.json"),
		"qualification": "Disposable512px/z210/can575,330 fixture; all six real asynchronous local-touch requests. Gameplay clips marked seen; isolated save home. All images buffered until actions finish. GPU readback and concurrent system work still affect cadence; use exact timestamps. No interpolated/repeated/generated video frames, performance/phone/child/owner or live-binding acceptance. The inherited sparse fixture's feedback uses the original can coordinate; initial ribbon remains behind Roshan. Complete source/control chain preserved separately."}
	var file: FileAccess = FileAccess.open(capture_root.path_join("ACTION_RECEIPT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	print("POOL_BUFFERED_ACTIONS|RESULT: %s failures=%d frames=%d" % ["PASS" if failures == 0 else "FAIL", failures, buffered_rows.size()])
	quit(1 if failures > 0 else 0)

func _record_action(index: int, cleanup: DayOnePoolCleanup) -> void:
	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	assert(is_instance_valid(skimmer))
	var touch: InputEventScreenTouch = InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = true
	touch.position = skimmer._trash_contact_position(index)
	skimmer._gui_input(touch)
	touch.pressed = false
	skimmer._gui_input(touch)
	var started: int = Time.get_ticks_msec()
	var next_sample: int = started
	var collected_at: int = -1
	var start_frame: int = buffered_rows.size()
	while Time.get_ticks_msec() - started < 10000 and buffered_rows.size() < 1100:
		await RenderingServer.frame_post_draw
		var now: int = Time.get_ticks_msec()
		var snapshot: Dictionary = skimmer.audit_snapshot() if is_instance_valid(skimmer) else {}
		var collected: bool = (int(snapshot.get("mask", main_mask(cleanup))) & (1 << index)) != 0
		if collected and collected_at < 0:
			collected_at = now
		if now >= next_sample:
			var read_start: int = Time.get_ticks_msec()
			var image: Image = root.get_texture().get_image()
			buffered_images.append(image)
			buffered_rows.append({"requested_item": index, "elapsed_wall_ms": now - started,
				"native_engine_frame": Engine.get_process_frames(), "image_read_ms": Time.get_ticks_msec() - read_start,
				"collection_seen_elapsed_ms": collected_at - started if collected_at >= 0 else -1,
				"skimmer_snapshot": snapshot})
			next_sample = now + 33
		if collected_at >= 0 and now - collected_at >= 900:
			break
	_check("native item %d actually collected" % index, collected_at >= 0)
	action_rows.append({"requested_item": index, "start_frame": start_frame,
		"end_frame_exclusive": buffered_rows.size(), "collection_seen_elapsed_ms": collected_at - started if collected_at >= 0 else -1,
		"observed_elapsed_ms": Time.get_ticks_msec() - started})

func main_mask(cleanup: DayOnePoolCleanup) -> int:
	var snapshot: Dictionary = cleanup.audit_snapshot().get("skimmer", {}) as Dictionary
	return int(snapshot.get("mask", 0))
