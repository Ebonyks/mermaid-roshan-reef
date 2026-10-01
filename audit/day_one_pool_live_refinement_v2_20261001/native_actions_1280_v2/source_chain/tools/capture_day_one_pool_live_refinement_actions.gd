extends SceneTree
## Actual production bindings. Local touch requests, isolated save, clips marked seen.
## Lossless viewport readbacks are buffered; measured cadence is not a device benchmark.

var capture_root: String
var images: Array[Image] = []
var frames: Array[Dictionary] = []
var actions: Array[Dictionary] = []
var checks: Array[Dictionary] = []

func _initialize() -> void:
	_run.call_deferred()

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
	main._castle_rooms_ref().show_room("mermaid_pool", false)
	await _frames(12)
	var cleanup: DayOnePoolCleanup = main._castle_rooms_ref().day_one_pool_cleanup
	_check("actual dirty pool mounted", is_instance_valid(cleanup))
	assert(is_instance_valid(cleanup))
	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	var bindings: Array[Dictionary] = []
	for index: int in range(skimmer._trash_sprites.size()):
		var sprite: Sprite2D = skimmer._trash_sprites[index]
		var atlas: AtlasTexture = sprite.texture as AtlasTexture
		assert(atlas != null)
		bindings.append({"slot": index, "atlas_path": atlas.atlas.resource_path,
			"atlas_sha256": FileAccess.get_sha256(atlas.atlas.resource_path),
			"region": [atlas.region.position.x, atlas.region.position.y, atlas.region.size.x, atlas.region.size.y],
			"scale": [sprite.scale.x, sprite.scale.y], "rotation": sprite.rotation})
	bindings.append({"role": "skimmer", "path": skimmer._skimmer.texture.resource_path,
		"sha256": FileAccess.get_sha256(skimmer._skimmer.texture.resource_path),
		"scale": [skimmer._skimmer.scale.x, skimmer._skimmer.scale.y]})
	_check("production activity depth210", skimmer.z_index == 210)
	await _sample(-1, 0, -1)
	for index: int in range(6):
		await _record_action(index, cleanup)
	await _frames(4)
	_check("all six progress bits saved", main.day_one_pool_skimmer_mask == 63)
	_check("waterfall unlocked after final landing", String(cleanup.audit_snapshot().get("current_activity", "")) == "waterfall")
	_check("six stored items persist in waterfall", skimmer._visible_basket_contents() == 6 and skimmer.visible)
	await _sample(-2, 0, -1)
	main.queue_free()
	await _frames(4)
	for index: int in range(images.size()):
		var filename: String = "frame_%04d.webp" % index
		var path: String = capture_root.path_join(filename)
		assert(images[index].save_webp(path, true, 1.0) == OK)
		frames[index]["path"] = filename
		frames[index]["sha256"] = FileAccess.get_sha256(path)
	images.clear()
	var harness: String = (get_script() as Script).resource_path
	var failures: int = 0
	for check: Dictionary in checks:
		if not bool(check["pass"]):
			failures += 1
	var receipt: Dictionary = {"schema": "reef.native-live-pool-refinement.v1",
		"harness": harness, "harness_sha256": FileAccess.get_sha256(harness),
		"engine": Engine.get_version_info(), "dimensions": [1280, 720],
		"runtime_bindings": bindings, "actions": actions, "frames": frames,
		"checks": checks, "checks_failed": failures,
		"qualification": "Actual production textures/controllers; no fixture texture, position, depth or action override. Six real asynchronous local Control touch requests, not ordinary HUD traversal. Isolated save and story clips marked seen. Complete images buffered until actions finish. Measured readback cadence, not phone performance. No interpolation/repeats. Direct visual opinions and device/child/owner acceptance separate."}
	var file: FileAccess = FileAccess.open(capture_root.path_join("ACTION_RECEIPT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	print("POOL_LIVE_REFINEMENT|RESULT: %s failures=%d frames=%d" % ["PASS" if failures == 0 else "FAIL", failures, frames.size()])
	quit(1 if failures > 0 else 0)

func _record_action(index: int, cleanup: DayOnePoolCleanup) -> void:
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
	var collected_at: int = -1
	var settled_at: int = -1
	var start_frame: int = frames.size()
	while Time.get_ticks_msec() - started < 10000 and frames.size() < 1200:
		await RenderingServer.frame_post_draw
		var now: int = Time.get_ticks_msec()
		if (int(skimmer.audit_snapshot()["mask"]) & (1 << index)) != 0 and collected_at < 0:
			collected_at = now
		if collected_at >= 0 and not skimmer.has_pending_transfer() and settled_at < 0:
			settled_at = now
		if now >= next_sample:
			await _sample(index, now - started, collected_at - started if collected_at >= 0 else -1, skimmer)
			next_sample = now + 33
		if settled_at >= 0 and now - settled_at >= 250:
			break
	_check("item%d collected" % index, collected_at >= 0)
	_check("item%d transfer settled" % index, settled_at >= 0)
	_check("item%d visible in basket" % index, skimmer._basket_contents[index].visible)
	actions.append({"requested_item": index, "start_frame": start_frame,
		"end_frame_exclusive": frames.size(), "collection_seen_elapsed_ms": collected_at - started if collected_at >= 0 else -1,
		"settled_seen_elapsed_ms": settled_at - started if settled_at >= 0 else -1,
		"observed_elapsed_ms": Time.get_ticks_msec() - started})

func _sample(item: int, elapsed: int, caught: int, skimmer: PoolSkimmerActivity = null) -> void:
	var read_start: int = Time.get_ticks_msec()
	images.append(root.get_texture().get_image())
	var snapshot: Dictionary = skimmer.audit_snapshot() if is_instance_valid(skimmer) else {}
	var row: Dictionary = {"requested_item": item, "elapsed_wall_ms": elapsed,
		"native_engine_frame": Engine.get_process_frames(), "image_read_ms": Time.get_ticks_msec() - read_start,
		"collection_seen_elapsed_ms": caught, "skimmer_snapshot": snapshot}
	if is_instance_valid(skimmer) and skimmer.has_pending_transfer():
		var piece: Sprite2D = skimmer._trash_sprites[skimmer._transport_index]
		row["carried_position"] = [piece.position.x, piece.position.y]
		row["carried_scale"] = [piece.scale.x, piece.scale.y]
		row["drop_time"] = skimmer._drop_time
	frames.append(row)

func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _check(label: String, passed: bool) -> void:
	checks.append({"name": label, "pass": passed})
	print("POOL_LIVE_REFINEMENT|%s|%s" % ["PASS" if passed else "FAIL", label])
