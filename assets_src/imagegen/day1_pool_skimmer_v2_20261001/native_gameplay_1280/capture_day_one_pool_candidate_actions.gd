extends "res://tools/capture_day_one_pool_candidate_fit.gd"

func _bind_candidates() -> void:
	var main: ReefMain = root.get_node_or_null("Main") as ReefMain
	assert(main != null)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var pool: DayOnePoolCleanup = rooms.day_one_pool_cleanup
	assert(pool != null and pool.skimmer_activity != null)
	var records: Array = JSON.parse_string(FileAccess.get_file_as_string(
		CANDIDATE_ROOT + "SELECTED_SOURCE_RECORDS_V2.json")) as Array
	assert(records.size() == 5)
	for item: Variant in records:
		var record: Dictionary = item as Dictionary
		var source_path: String = "res://" + str(record["planned_native_path"])
		var source_hash: String = str(record["sha256"])
		assert(FileAccess.get_sha256(source_path) == source_hash)
		var texture: ImageTexture = ImageTexture.create_from_image(Image.load_from_file(source_path))
		texture.set_meta("audit_source_path", source_path)
		texture.set_meta("audit_source_sha256", source_hash)
		var slot: int = int(SLOT_BY_NAME[str(record["name"])])
		var sprite: Sprite2D = pool.skimmer_activity._trash_sprites[slot]
		sprite.texture = texture
		pool.skimmer_activity._fit_sprite(sprite, PoolSkimmerActivity.TRASH_MAX_SIZES[slot])
		candidate_bindings.append({"slot": slot, "source": source_path, "sha256": source_hash,
			"scale": [sprite.scale.x, sprite.scale.y], "rotation": sprite.rotation,
			"modulate": [sprite.modulate.r, sprite.modulate.g, sprite.modulate.b, sprite.modulate.a]})
	candidate_bound = true

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
	# Gameplay-only diagnostic: clip playback is separately audited; all writes are in the disposable test home.
	for movie_id: String in DayOneStoryClips.clip_ids():
		main.day_one_story_clips_seen[movie_id] = true
	main._day_one_cancel_story_clips()
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(root.size)
	await _frames(6)
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
	# Let the first actual flight finish, then request each remaining item separately.
	await create_timer(0.7).timeout
	for trash_index: int in range(1, 6):
		await _capture_live_item(trash_index, cleanup)
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
		_check("actual seahorse completed tug %d" % (_tug_index + 1),
			await _wait_for_seahorse_tug(cleanup.seahorse_activity, _tug_index + 1))
	await _frames(3)
	await _capture("05_seahorse_tug_midway")
	for _tug_index: int in range(4):
		_check("seahorse release tug", cleanup.seahorse_activity.probe_tap())
		_check("actual seahorse completed tug %d" % (_tug_index + 5),
			await _wait_for_seahorse_tug(cleanup.seahorse_activity, _tug_index + 5))
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


func _capture_live_item(index: int, cleanup: DayOnePoolCleanup) -> void:
	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	var touch: InputEventScreenTouch = InputEventScreenTouch.new()
	touch.index = 0
	touch.pressed = true
	touch.position = skimmer._trash_contact_position(index)
	skimmer._gui_input(touch)
	touch.pressed = false
	skimmer._gui_input(touch)
	var started: int = Time.get_ticks_msec()
	var next_sample: int = started
	var collection_seen: int = -1
	var sample: int = 0
	while Time.get_ticks_msec() - started < 12000:
		await process_frame
		var now: int = Time.get_ticks_msec()
		var collected: bool = is_instance_valid(skimmer) and (int(skimmer.audit_snapshot()["mask"]) & (1 << index)) != 0
		if collected and collection_seen < 0:
			collection_seen = now
		if now >= next_sample:
			await RenderingServer.frame_post_draw
			var name: String = "item_%02d_sample_%03d" % [index, sample]
			var harness: String = (get_script() as Script).resource_path
			ART_TRACE.save_frame_receipt(root, name, capture_root,
				harness, "res://scripts/probe_day_one_pool_shots.gd")
			var receipt_path: String = capture_root.path_join(name + ".json")
			var receipt: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(receipt_path)) as Dictionary
			receipt["elapsed_wall_ms"] = now - started
			receipt["collection_seen_elapsed_ms"] = collection_seen - started if collection_seen >= 0 else -1
			receipt["requested_item"] = index
			receipt["pool_activity_snapshot"] = cleanup.audit_snapshot()
			receipt["candidate_bindings"] = candidate_bindings
			receipt["qualification"] = "Scripted local touch request on real disposable activity; unpaused native samples targeted every80ms, actual elapsed times recorded. File IO affects cadence. Exact overriding harness and candidate_bindings identify source dimensions, hashes and any layout changes. This is not full-rate/performance, ordinary narrative, every elapsed frame or phone/child/owner acceptance. Production files and trusted probe are unchanged."
			var file: FileAccess = FileAccess.open(receipt_path, FileAccess.WRITE)
			file.store_string(JSON.stringify(receipt, "\t") + "\n")
			file.close()
			sample += 1
			next_sample = Time.get_ticks_msec() + 80
		if collection_seen >= 0 and now - collection_seen > 650:
			break
	_check("sequential native item %d actually collected" % index, collection_seen >= 0)
