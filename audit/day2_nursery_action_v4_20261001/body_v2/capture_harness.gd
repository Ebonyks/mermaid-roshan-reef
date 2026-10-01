extends SceneTree
## Live finger0 traces after an explicit catch-phase/open fixture.
## Frames are native Mobile diagnostics, not cinematic or normal-route acceptance.

const OUT := "res://audit/day2_nursery_action_v4_20261001/body_v2/"
var main: ReefMain
var world: OperaCareerWorld2D
var all_cases: Array[Dictionary] = []
var failures: int = 0
var source_start: Dictionary = {}

func source_fingerprints() -> Dictionary:
	var hashes: Dictionary = {}
	for path: String in ["res://scripts/opera_nursery_catch.gd",
		"res://scripts/opera_nursery_care.gd", "res://scripts/opera_career_world_2d.gd",
		"res://tools/capture_day2_nursery_care.gd", OperaNurseryCare.DATA]:
		hashes[path] = FileAccess.get_sha256(path)
	return hashes

func _init() -> void:
	call_deferred("_run")

func frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame

func _check(name: String, condition: bool) -> void:
	if not condition:
		failures += 1
	print("NURSERY_CONTACT|", "OK" if condition else "FAIL", "|", name)

func _touch(point: Vector2, kind: String, index: int = 0) -> void:
	var event: InputEvent
	if kind == "drag":
		var drag := InputEventScreenDrag.new()
		drag.index = index
		drag.position = point
		event = drag
	else:
		var touch := InputEventScreenTouch.new()
		touch.index = index
		touch.position = point
		touch.pressed = kind == "down"
		event = touch
	root.push_input(event, true)

func _case(width: int, intentional: bool) -> void:
	root.size = Vector2i(width, 720)
	DisplayServer.window_set_size(root.size)
	await frames(3)
	var id := ("catch" if intentional else "passive") + "-%dx720" % width
	DirAccess.make_dir_recursive_absolute(OUT + "captures/" + id)
	var house := OperaHouse.new()
	main.add_child(house)
	_check(id + " normal freeplay caller starts", house.start(main, 15, Callable()))
	world = house.act.career_world_2d
	world.set_process(false)
	world.phase_index = 1
	world.active = true
	world.reveal_t = 0.0
	world.phase_gap = 0.0
	world._arm_phase()
	world._open_task()
	await frames(3)
	var catch: OperaNurseryCatch = world.nursery_catch
	_check(id + " exact source atlas and three measured feet loaded",
		catch.textures.size() == 3 and catch.baby_feet.size() == 3
		and catch.pillows_texture is AtlasTexture
		and (catch.pillows_texture as AtlasTexture).region == Rect2(6, 115, 1014, 117))
	world.set_process(true)
	var records: Array[Dictionary] = []
	var events: Array[Dictionary] = []
	var down: bool = false
	var last := Vector2.ZERO
	var saw_five: bool = false
	var saw_settle: bool = false
	var prior_key := -1
	var prior_transfers := -1
	var seen_keys: Array[int] = []
	var duration: float = 26.0 if intentional else 8.0
	for step: int in range(int(duration * 30.0)):
		var at_time := float(step) / 30.0
		if intentional and world.phase_index == 1 and catch.active and at_time >= 0.3:
			var x: float = catch.lowest_baby_x()
			var local := Vector2(x if x >= 0.0 else 0.5, 0.7) * catch.size
			last = catch.get_global_transform_with_canvas() * local
			_touch(last, "drag" if down else "down")
			down = true
			events.append({"t": at_time, "finger": 0, "kind": "drag" if step > 9 else "down",
				"viewport_xy": [last.x, last.y]})
		elif down:
			_touch(last, "up")
			down = false
			events.append({"t": at_time, "finger": 0, "kind": "up", "viewport_xy": [last.x, last.y]})
		await process_frame
		if catch.caught == 5:
			saw_five = true
			if world.phase_index == 1 and catch.transfers.is_empty():
				saw_settle = true
		var key: int = catch.care.key if catch.care != null else -1
		var key_changed: bool = key != prior_key or catch.transfers.size() != prior_transfers
		if not seen_keys.has(key):
			seen_keys.append(key)
		# Native key boundaries plus regular2fps samples. No omitted authored
		# key is silently filled by interpolation; unobserved intervals stay gaps.
		if step % 15 == 0 or key_changed:
			await RenderingServer.frame_post_draw
			var path := "captures/%s/%04d.webp" % [id, records.size()]
			var image: Image = root.get_texture().get_image()
			var error: Error = image.save_webp(OUT + path, false)
			_check("native frame save " + path, error == OK)
			records.append({"image": path, "frame": records.size(), "driver_t": at_time,
				"care_key": key, "sole_roshan_body": not world.player_actor.visible,
				"care_hand": [catch.catch_point().x, catch.catch_point().y],
				"sha256": FileAccess.get_sha256(OUT + path), "phase": world.phase_index,
				"progress": world.phase_progress, "caught": catch.caught, "missed": catch.missed,
				"catcher_x": catch.catcher_x, "elapsed": catch.elapsed,
				"catch_bounds": [catch.position.x, catch.position.y, catch.size.x, catch.size.y],
				"fallers": catch.fallers.duplicate(true), "transfers": catch.transfers.duplicate(true),
				"safe_landings": catch.safe_landings.duplicate(true), "settled": catch.settled.duplicate(),
				"support_planes": [OperaNurseryCatch.CATCH_Y, catch._pillow_plane()]})
		prior_key = key
		prior_transfers = catch.transfers.size()
	if down:
		_touch(last, "up")
	if intentional:
		_check(id + " genuine single touch catches five", saw_five and catch.missed == 0)
		_check(id + " final transfer settles before next phase", saw_settle and world.phase_index == 2)
		_check(id + " all receiving and lowering authored keys were sampled", seen_keys.has(1)
			and seen_keys.has(2) and seen_keys.has(3) and seen_keys.has(4) and seen_keys.has(5)
			and seen_keys.has(6) and seen_keys.has(7))
		_check(id + " normal route Roshan returns for feeding", world.player_actor.visible)
	else:
		_check(id + " passive play never catches or advances", catch.caught == 0 and catch.missed > 0
			and world.phase_index == 1 and world.phase_progress == 0.0)
	var receipt := {"id": id, "intentional": intentional, "dimensions": [width, 720],
		"capture_fps": 2.0, "frames": records, "events": events,
		"method": "Ordinary OperaHouse freeplay setup, explicit catch/open fixture, then viewport finger0 input only. Fixed30fps processing. Main HUD/player hidden; no graphics/action/owner acceptance inferred.",
		"saw_five": saw_five, "saw_final_settle_before_advance": saw_settle}
	var file := FileAccess.open(OUT + id + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	all_cases.append({"id": id, "frames": records.size(), "inputs": events.size()})
	house._leave_early()
	await frames(3)

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	source_start = source_fingerprints()
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, "res://tmp/day2_nursery_contact_save.json")
	root.add_child(main)
	await frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.chapter2_active = false
	main.set_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	await _case(1280, true)
	await _case(1600, true)
	var source_end: Dictionary = source_fingerprints()
	_check("all production/harness/contact data bytes stayed unchanged throughout both captures", source_end == source_start)
	var file := FileAccess.open(OUT + "capture_index.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info(),
		"renderer": RenderingServer.get_current_rendering_method(),
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_care.gd"),
		"world_sha256": FileAccess.get_sha256("res://scripts/opera_career_world_2d.gd"),
		"catch_sha256": FileAccess.get_sha256("res://scripts/opera_nursery_catch.gd"),
		"source_start": source_start, "source_end": source_end,
		"cases": all_cases, "failures": failures, "owner_accepted": false}, "\t") + "\n")
	file.close()
	main.queue_free()
	await frames(3)
	print("NURSERY_CONTACT|RESULT|", "PASS" if failures == 0 else "FAIL")
	quit(1 if failures else 0)
