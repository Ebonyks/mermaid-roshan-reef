extends SceneTree
## Mobile-renderer visual evidence for the complete Day One bathroom rescue.
## Captures are review artifacts only and never become runtime assets.

const SINK_CENTER := Vector2(642.0, 280.0)
const TUB_CENTER := Vector2(310.0, 349.0)

var failures: int = 0
var capture_root: String = ""


func _init() -> void:
	call_deferred("_run")


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_BATHROOM_SHOTS|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		(" (%s)" % detail) if detail != "" else ""])


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
		not image.is_empty() and image.get_size() == Vector2i(1280, 720)
		and save_error == OK,
		"size=%s path=%s" % [image.get_size(), path])


func _run() -> void:
	_check("real Mobile viewport is available",
		DisplayServer.get_name() != "headless", DisplayServer.get_name())
	if failures > 0:
		quit(1)
		return
	root.size = Vector2i(1280, 720)
	await _frames(4)
	capture_root = OS.get_environment("DAY_ONE_BATHROOM_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path(
			"user://day_one_bathroom_shots")
	_check("capture directory",
		DirAccess.make_dir_recursive_absolute(capture_root) == OK,
		capture_root)

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
		"day_one_current_room": "bathroom",
		"day_one_completed_rooms": [],
		"day_one_bathroom_cleanup_step": 0,
		"day_one_bathroom_supply_hunt_step": 0,
		"day_one_bathroom_tools_authorized": false,
	})
	main.pearl_count = main.PEARL_TOTAL
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	main._castle_rooms_ref().show_room("bubble_bath", false)
	await _frames(8)
	main._sync_day_one_bathroom_cleanup()
	await _frames(5)
	main.set_process(false)

	var cleanup: DayOneBathroomCleanup = main._day_one_bathroom_cleanup
	_check("fresh entry mounts dirty rescue", cleanup != null)
	if cleanup == null:
		main.queue_free()
		quit(1)
		return
	var entry: Dictionary = cleanup.audit_snapshot()
	_check("entry is dirty with one basket target",
		bool(entry.get("sink_grime_visible", false))
		and bool(entry.get("tub_grime_visible", false))
		and int(entry.get("active_target_count", 0)) == 1
		and bool(entry.get("localized_fixture_grime", false))
		and bool(entry.get("basket_clear_of_action_zone", false)))
	var dirty_plate_entry: Dictionary = \
		cleanup.day_one_bathroom_plate_snapshot()
	_check("entry uses the separate full dirty 2D room plate",
		bool(dirty_plate_entry.get("dirty_plate_visible", false))
		and bool(dirty_plate_entry.get("true_2d", false))
		and not bool(dirty_plate_entry.get("contains_tub_swimmer", true))
		and bool(dirty_plate_entry.get("separate_animated_bunny", false))
		and bool(dirty_plate_entry.get("bunny_depth_occluded", false))
		and bool(dirty_plate_entry.get("clean_fixture_pixels_occluded", false))
		and not bool(dirty_plate_entry.get(
			"clean_fixture_layer_visible", true))
		and dirty_plate_entry.get("texture_size", Vector2i.ZERO)
			== Vector2i(1024, 576))
	_check("entry bath visibly contains one depth-occluded mermaid bunny",
		bool(dirty_plate_entry.get("dirty_plate_visible", false))
		and bool(dirty_plate_entry.get("separate_animated_bunny", false))
		and bool(dirty_plate_entry.get("bunny_depth_occluded", false)))
	var elevator: Control = main.castle_room_stage.get_node_or_null(
		"ElevatorButton") as Control
	var elevator_pointer: Control = main.castle_room_stage.get_node_or_null(
		"ElevatorPointer") as Control
	_check("rescue hides competing lower-corner controls",
		main.castle_room_action_button != null
		and not main.castle_room_action_button.visible
		and main.castle_room_action_button.disabled
		and main.castle_room_action_button.mouse_filter \
			== Control.MOUSE_FILTER_IGNORE
		and elevator != null and not elevator.visible
		and elevator is BaseButton and (elevator as BaseButton).disabled
		and elevator.mouse_filter == Control.MOUSE_FILTER_IGNORE
		and elevator_pointer != null and not elevator_pointer.visible
		and elevator_pointer.mouse_filter == Control.MOUSE_FILTER_IGNORE,
		"action=%s/%s elevator=%s/%s pointer=%s" % [
			main.castle_room_action_button.visible
			if main.castle_room_action_button != null else null,
			main.castle_room_action_button.disabled
			if main.castle_room_action_button != null else null,
			elevator.visible if elevator != null else null,
			(elevator as BaseButton).disabled
			if elevator is BaseButton else null,
			elevator_pointer.visible if elevator_pointer != null else null])
	await _capture("00_dirty_basket_prompt")

	_check("basket tap starts real handoff", cleanup.probe_tap_basket())
	await create_timer(0.16).timeout
	await _capture("01_sponge_travels_to_sink")
	await create_timer(0.28).timeout
	_check("circle guide is live",
		bool(cleanup.cleaning_audit_snapshot().get(
			"circle_demo_visible", false)))
	await _capture("02_sink_circle_guide")

	var sink_points: Array[Vector2] = []
	for index: int in range(49):
		var angle: float = float(index) / 48.0 * TAU * 1.2
		sink_points.append(SINK_CENTER
			+ Vector2(cos(angle), sin(angle)) * 120.0)
	_check("live sink gesture completes",
		cleanup.probe_cleaning_sink_circle(sink_points))
	await _capture("03_sink_clean_sponge_returns")
	await create_timer(0.48).timeout
	await _capture("04_brush_travels_to_tub")
	await create_timer(0.30).timeout
	_check("tub drain tap is live before brush arrows",
		bool(cleanup.cleaning_audit_snapshot().get("tub_drain_ready", false))
		and bool(cleanup.cleaning_audit_snapshot().get(
			"one_tap_drain_target_visible", false))
		and bool(cleanup.cleaning_audit_snapshot().get(
			"brush_parked_on_tub_rim", false))
		and not bool(cleanup.cleaning_audit_snapshot().get(
			"back_and_forth_arrows_visible", true)))
	await _capture("05_tub_drain_prompt")
	_check("tub tap starts the bunny's comic reaction", cleanup.probe_tap_tub())
	await create_timer(0.16).timeout
	_check("comic No and one spin are visible",
		int(cleanup.cleaning_audit_snapshot().get(
			"drain_reaction_count", 0)) == 1
		and String(cleanup.cleaning_audit_snapshot().get(
			"comic_shout", "")) == "NO!")
	await _capture("06_bunny_no_spin")
	await create_timer(0.92).timeout
	_check("tub arrows are live",
		bool(cleanup.cleaning_audit_snapshot().get(
			"back_and_forth_arrows_visible", false))
		and bool(cleanup.cleaning_audit_snapshot().get("tub_drained", false)))
	await _capture("07_tub_arrow_guide")

	var tub_points: Array[Vector2] = [
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
		TUB_CENTER + Vector2(-210.0, 0.0),
	]
	var cleaning: DayOneBathroomCleaning = cleanup._cleaning_stage
	_check("three forgiving tub reversals complete",
		cleaning != null and cleaning.probe_tub_strokes(tub_points, 0.75))
	await create_timer(0.12).timeout
	var clean_plate_finale: Dictionary = cleanup.day_one_bathroom_plate_snapshot()
	_check("completion permanently reveals the distinct clean room state",
		not bool(clean_plate_finale.get("dirty_plate_visible", true))
		and bool(clean_plate_finale.get(
			"clean_fixture_layer_visible", false)))
	await _capture("08_whole_room_sparkle")
	await create_timer(0.96).timeout
	_check("finale exposes direct pool picture",
		main._day_one_pool_route_button != null
		and main._day_one_pool_route_button.visible)
	var pool_preview: Sprite2D = null
	var pool_frame: Sprite2D = null
	if main._day_one_pool_route_button != null:
		pool_preview = main._day_one_pool_route_button.get_node_or_null(
			"ApprovedPoolRoomPreview") as Sprite2D
		pool_frame = main._day_one_pool_route_button.get_node_or_null(
			"ApprovedShellPoolFrame") as Sprite2D
	var pool_preview_size: Vector2 = Vector2.ZERO
	if pool_preview != null and pool_preview.texture != null:
		pool_preview_size = pool_preview.texture.get_size() * pool_preview.scale
	var pool_pointer: Sprite2D = null
	if main._day_one_pool_route_button != null:
		pool_pointer = main._day_one_pool_route_button.get_node_or_null(
			"PoolRouteGhostHand") as Sprite2D
	_check("pool route identifies the actual room preview",
		main._day_one_pool_route_button != null
		and String(main._day_one_pool_route_button.get_meta(
			"route_preview_kind", "")) == "actual_pool_room"
		and String(main._day_one_pool_route_button.get_meta(
			"route_preview_asset", ""))
			== "res://assets/flats/castle/rooms/room_mermaid_pool.png"
		and pool_preview != null
		and bool(pool_preview.get_meta("approved_pool_room_preview", false))
		and String(pool_preview.get_meta("actual_destination_room", ""))
			== "mermaid_pool"
		and pool_preview.texture != null
		and pool_preview.centered
		and not pool_preview.region_enabled
		and is_equal_approx(pool_preview.scale.x, pool_preview.scale.y)
		and is_equal_approx(pool_preview.scale.x, 0.15)
		and pool_preview_size.x <= main._day_one_pool_route_button.size.x
		and pool_preview_size.y <= main._day_one_pool_route_button.size.y
		and pool_frame != null
		and bool(pool_frame.get_meta("approved_reused_shell_frame", false))
		and pool_pointer != null
		and pool_pointer.position.y
			< pool_preview.position.y - pool_preview_size.y * 0.5)
	_check("pool route keeps competing controls owned by Day One",
		main.castle_room_action_button != null
		and not main.castle_room_action_button.visible
		and main.castle_room_action_button.disabled
		and main.castle_room_action_button.mouse_filter \
			== Control.MOUSE_FILTER_IGNORE
		and elevator != null and not elevator.visible
		and elevator is BaseButton and (elevator as BaseButton).disabled
		and elevator.mouse_filter == Control.MOUSE_FILTER_IGNORE
		and elevator_pointer != null and not elevator_pointer.visible
		and elevator_pointer.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	await _capture("09_clean_pool_route")

	main.queue_free()
	await _frames(4)
	print("DAY_ONE_BATHROOM_SHOTS|RESULT: %s failures=%d output=%s" % [
		"PASS" if failures == 0 else "FAIL", failures, capture_root])
	quit(1 if failures > 0 else 0)
