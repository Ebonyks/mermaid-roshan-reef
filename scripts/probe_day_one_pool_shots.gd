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
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path: String = capture_root.path_join(name + ".png")
	var save_error: Error = image.save_png(path)
	_check("capture %s" % name,
		not image.is_empty() and save_error == OK,
		"size=%s path=%s" % [image.get_size(), path])


func _run() -> void:
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
	for step_index: int in range(1, 5):
		_check("advance state %d" % step_index,
			cleanup.probe_advance_current_step())
		await _frames(8)
		if step_index == 1:
			_check("clean rainbow remains hidden before fountain cleanup",
				clean_waterfall != null and not clean_waterfall.visible)
		elif step_index == 2:
			_check("clean rainbow returns only after fountain cleanup",
				clean_waterfall != null and clean_waterfall.visible)
		if step_index < 4:
			await _capture("%02d_%s" % [
				step_index,
				["pool_clear", "fountain_clear", "seahorse_last"][
					step_index - 1],
			])
		else:
			await _capture("04_waterfall_reveal_active")
			await _frames(72)
			await _capture("05_rumi_reveal")
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
