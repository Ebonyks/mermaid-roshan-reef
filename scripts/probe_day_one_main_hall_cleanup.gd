extends SceneTree
## Focused Stage 1 Main Hall contract probe. It covers both additive director
## state and the live Canvas2D cleanup controller.

const DIRECTOR_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")

var checks_failed: int = 0


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _run() -> void:
	_check_director_contract()
	_check_wall_a_source_pixels()
	await _check_live_castle_contract()
	_print_result()
	quit(1 if checks_failed > 0 else 0)


func _check_director_contract() -> void:
	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = DIRECTOR_SCRIPT.new(main) as DayOneDirector
	var expected: Array[String] = [
		"light_left", "light_right", "light_b_left", "light_b_right",
		"wall_a", "runner_a", "floor_a", "wall_b", "floor_b",
		"sleepy_bunny", "shell_bunny", "runner_bunny",
	]
	_check("exact twelve target IDs", director.hall_target_ids() == expected)
	var category_counts := {"light": 0, "scrub": 0, "bunny": 0}
	for target_id: String in expected:
		var category: String = director.hall_target_category(target_id)
		category_counts[category] = int(category_counts.get(category, 0)) + 1
	_check("four lights five scrubs three bunnies",
		category_counts == {"light": 4, "scrub": 5, "bunny": 3})
	_check("fresh hall starts dirty", director.hall_cleanup_mask == 0
		and not director.hall_cleanup_complete())
	_check("director keeps current activity usable",
		director.can_enter_room("bathroom"))
	_check("castle doors gate activities before hall",
		not main.day_one_can_enter_castle_room("bubble_bath"))
	_check("mask transition is idempotent",
		director.clean_hall_target("wall_a")
		and not director.clean_hall_target("wall_a")
		and director.hall_target_clean("wall_a"))
	var partial: Dictionary = director.serialize_state()
	_check("partial mask persists", int(partial.get(
		"day_one_hall_cleanup_mask", 0)) == director.hall_target_bit("wall_a"))
	for target_id: String in expected:
		director.clean_hall_target(target_id)
	var hall_events: int = 0
	for event: Dictionary in director.drain_events():
		if String(event.get("event", "")) == DayOneDirector.EVENT_HALL_COMPLETE:
			hall_events += 1
	_check("complete mask has one completion event",
		director.hall_cleanup_complete() and hall_events == 1)
	_check("castle door opens after hall prerequisite",
		main.day_one_can_enter_castle_room("bubble_bath"))
	var fresh_patch: Dictionary = DIRECTOR_SCRIPT.normalise_save_patch({})
	_check("fresh missing hall key defaults zero",
		int(fresh_patch.get("day_one_hall_cleanup_mask", -1)) == 0)
	var legacy_patch: Dictionary = DIRECTOR_SCRIPT.normalise_save_patch({
		"day_one_active": true,
		"day_one_current_room": "bathroom",
	})
	_check("legacy missing hall key migrates complete",
		int(legacy_patch.get("day_one_hall_cleanup_mask", 0)) == 0xFFF)
	var inactive_patch: Dictionary = DIRECTOR_SCRIPT.normalise_save_patch({
		"day_one_active": false,
	})
	_check("inactive missing hall key migrates complete",
		int(inactive_patch.get("day_one_hall_cleanup_mask", 0)) == 0xFFF)
	var partial_patch: Dictionary = DIRECTOR_SCRIPT.normalise_save_patch({
		"day_one_active": true,
		"day_one_hall_cleanup_mask": 0x12,
	})
	_check("explicit partial hall key is preserved",
		int(partial_patch.get("day_one_hall_cleanup_mask", 0)) == 0x12)
	main.free()


func _check_wall_a_source_pixels() -> void:
	var dirty: Image = Image.load_from_file(ProjectSettings.globalize_path(
		"res://assets/castle/day_one_main_hall/dirty_tiles/"
		+ "dirty_main_hall_day_one_r0_c3.png"))
	var clean: Image = Image.load_from_file(ProjectSettings.globalize_path(
		"res://assets/castle/day_one_main_hall/clean_tiles/"
		+ "clean_main_hall_day_one_r0_c3.png"))
	if dirty == null or clean == null or dirty.is_empty() or clean.is_empty():
		_check("wall_a dirty and clean source tiles load", false)
		return
	var changed_samples: int = 0
	var total_delta: float = 0.0
	for sample_y: int in range(16):
		var y: int = clampi(610 + sample_y * 24, 0, dirty.get_height() - 1)
		for sample_x: int in range(16):
			var x: int = clampi(230 + sample_x * 28, 0,
				dirty.get_width() - 1)
			var dirty_color: Color = dirty.get_pixel(x, y)
			var clean_color: Color = clean.get_pixel(x, y)
			var delta: float = absf(dirty_color.r - clean_color.r) \
				+ absf(dirty_color.g - clean_color.g) \
				+ absf(dirty_color.b - clean_color.b)
			total_delta += delta
			if delta > 0.08:
				changed_samples += 1
	_check("wall_a authored source region has visible clean difference",
		changed_samples >= 20 and total_delta / 256.0 > 0.12)


func _check_live_castle_contract() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	main._skip_intro()
	await _frames(2)
	main.day_one_active = true
	main.day_one_current_room_id = "bathroom"
	main.day_one_completed_rooms = {}
	main.day_one_cleaned_rooms = {}
	main.day_one_hall_cleanup_mask = 0
	main.day_one_hall_shock_seen = false
	main.day_one_hall_celebration_done = false
	main._enter_castle_interior_now(false)
	await _frames(3)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var cleanup: DayOneMainHallCleanup = main.day_one_main_hall_cleanup
	_check("live cleanup controller attaches", cleanup != null
		and is_instance_valid(cleanup))
	if cleanup == null or not is_instance_valid(cleanup):
		main.queue_free()
		return
	var buttons: Dictionary = cleanup.get("_buttons") as Dictionary
	_check("only nine non-bunny overlay buttons exist", buttons.size() == 9
		and not buttons.has("sleepy_bunny")
		and not buttons.has("shell_bunny")
		and not buttons.has("runner_bunny"))
	var hitboxes_ok := true
	for button_value: Variant in buttons.values():
		var button: Button = button_value as Button
		hitboxes_ok = hitboxes_ok and button != null \
			and button.size.x >= 144.0 and button.size.y >= 144.0
	_check("every remedy hitbox is at least 144 square", hitboxes_ok)
	var geometry_ok := true
	for target: Dictionary in DayOneMainHallCleanup.TARGETS:
		if String(target["kind"]) == "bunny":
			continue
		var target_id: String = String(target["id"])
		var target_button: Button = buttons.get(target_id) as Button
		var expected_center: Vector2 = target["pos"] as Vector2
		geometry_ok = geometry_ok and target_button != null \
			and target_button.get_meta("day_one_hall_art_center",
			Vector2(-1.0, -1.0)) == expected_center
	_check("nine remedy centers use registered joined-art coordinates", geometry_ok)
	var dirty_tiles_ok := true
	for tile: Sprite2D in main.castle_room_background_tiles:
		dirty_tiles_ok = dirty_tiles_ok \
			and String(tile.get_meta("day_one_hall_state", "")) == "dirty"
	_check("one live tile set starts wholly dirty",
		main.castle_room_background_tiles.size() == 16 and dirty_tiles_ok)
	var item_sprites: Dictionary = main.castle_room_item_sprites
	_check("three live dust bunnies are present",
		item_sprites.has("sleepy_bunny") and item_sprites.has("shell_bunny")
		and item_sprites.has("runner_bunny"))
	var shock: Sprite2D = cleanup.get("_shock_sprite") as Sprite2D
	_check("shock modal owns input and hides idle Roshan",
		main.day_one_hall_cleanup_modal and shock != null
		and not main.castle_room_player_sprite.visible)
	_check("shock uses approved gesture-b frames 4 through 7",
		shock != null and String(shock.get_meta("gesture_sheet", "")) == "gesture_b"
		and shock.get_meta("gesture_frames", []) == [4, 5, 6, 7])
	rooms._go_back()
	await _frames(1)
	_check("shock modal blocks the visible Back button",
		rooms.is_open() and main.castle_room_id == "main_hall"
		and main.day_one_hall_cleanup_modal)
	await create_timer(2.35).timeout
	await _frames(2)
	_check("shock teardown restores actor and input",
		not main.day_one_hall_cleanup_modal
		and main.castle_room_player_sprite.visible
		and cleanup.get("_shock_sprite") == null)
	var bunny_toured := false
	for index: int in range(16):
		cleanup.set("_affordance_time", float(index) * 2.4)
		cleanup.call("_update_affordance", 0.0)
		var halo: Sprite2D = cleanup.get("_affordance_halo") as Sprite2D
		if halo != null and String(halo.get_meta(
				"affordance_target", "")) in DayOneDirector.HALL_BUNNY_TARGET_IDS:
			bunny_toured = true
			break
	_check("native cleanup affordance tours a bunny", bunny_toured)
	rooms._activate_room_item("sleepy_bunny")
	await _frames(2)
	_check("bunny tap poofs and persists its bit",
		not main.castle_room_item_sprites.has("sleepy_bunny")
		and main._day_one_ref().hall_target_clean("sleepy_bunny"))
	rooms._explode_dust_bunny("shell_bunny")
	rooms._explode_dust_bunny("runner_bunny")
	cleanup.call("_clean_target", "wall_a")
	await _frames(2)
	var wall_a_revealed := false
	for tile: Sprite2D in main.castle_room_background_tiles:
		var progress: Dictionary = tile.get_meta(
			"day_one_hall_reveal_progress", {}) as Dictionary
		if float(progress.get("wall_a", 0.0)) >= 1.0:
			var tile_material: ShaderMaterial = tile.material as ShaderMaterial
			var rect0: Vector4 = tile_material.get_shader_parameter(
				"reveal_rect_0") as Vector4 if tile_material != null \
				else Vector4.ZERO
			print("HALL|wall_a shader=", tile_material != null,
				" rect0=", rect0)
			wall_a_revealed = true
			break
	_check("wall_a visibly reveals clean registered pixels before target 12",
		wall_a_revealed)
	rooms.show_room("bubble_bath", false)
	rooms.show_room("main_hall", false)
	await _frames(3)
	var partial_rebuilt := false
	for tile: Sprite2D in main.castle_room_background_tiles:
		var progress: Dictionary = tile.get_meta(
			"day_one_hall_reveal_progress", {}) as Dictionary
		if float(progress.get("wall_a", 0.0)) >= 1.0:
			partial_rebuilt = true
			break
	_check("partial saved hall state reconstructs its clean reveal", partial_rebuilt)
	for target_id: String in DayOneDirector.HALL_LIGHT_TARGET_IDS:
		cleanup.call("_clean_target", target_id)
	for target_id: String in DayOneDirector.HALL_SCRUB_TARGET_IDS:
		if target_id != "floor_b" and target_id != "wall_a":
			cleanup.call("_clean_target", target_id)
	cleanup.call("_clean_target", "floor_b")
	await _frames(2)
	var clean_tiles_ok := true
	for tile: Sprite2D in main.castle_room_background_tiles:
		clean_tiles_ok = clean_tiles_ok \
			and String(tile.get_meta("day_one_hall_state", "")) == "clean"
	_check("twelfth remedy atomically restores all sixteen clean tiles",
		main._day_one_ref().hall_cleanup_complete() and clean_tiles_ok)
	var sweep_count := 0
	for child: Node in main.castle_room_item_effect_layer.get_children():
		if String(child.get_meta("castle_burst_profile", "")) \
				== "day_one_hall_cleanup":
			sweep_count += 1
	_check("completion sweep spans the hall with bounded motes",
		sweep_count == 27)
	var bath_pointer: Label = cleanup.get_node_or_null(
		"DayOneBubbleBathPointer") as Label
	_check("completion always leaves a Bubble Bath pointer",
		bath_pointer != null and bath_pointer.visible)
	_check("hall cleanup preserves the Bathroom story step",
		main.day_one_current_room_id == "bathroom")
	_check("Bubble Bath becomes the active plot door",
		rooms.active_door_highlight_id() == "bubble_bath"
		and main.day_one_can_enter_castle_room("bubble_bath"))
	cleanup.teardown()
	await _frames(2)
	_check("cleanup teardown releases the modal",
		not main.day_one_hall_cleanup_modal)
	main.queue_free()
	await _frames(2)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("HALL|", label, ": ", ("OK" if ok else "FAIL"))


func _print_result() -> void:
	print("HALL|RESULT: ", ("PASS" if checks_failed == 0 else "FAIL"),
		" checks_failed=", checks_failed)
