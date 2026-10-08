extends SceneTree

const AstronautSurface := preload("res://scripts/opera_astronaut_surface.gd")
const PipeWork := preload("res://scripts/opera_astronaut_pipe_work.gd")
var capture_width: int = int(OS.get_environment("ASTRO_NATIVE_WIDTH"))
var test_save: String = "res://tmp/astronaut_native_birthday_capture_v9_20261007/%dx720/reef_save.json" % capture_width
var main: ReefMain
var rows: Array[Dictionary] = []
var snapshots: Array[Dictionary] = []
var contact_requests: Array[Dictionary] = []
var failed := 0
var valve_contacts: Array[Dictionary] = []
var patch_contacts: Array[Dictionary] = []
var capture_root: String = "res://tmp/astronaut_native_birthday_capture_v9_20261007/%dx720/frames" % capture_width
var capture_manifest: String = "res://audit/astronaut_clearance_20261006/NATIVE_BIRTHDAY_CAPTURE_V9_%d_MANIFEST.json" % capture_width
const DENSE_CAPS := [24, 24, 32, 16]
var capture_running := true
var capture_rows: Array[Dictionary] = []
var capture_keys: Dictionary = {}
var dense_counts := [0, 0, 0, 0]
var last_capture_msec := 0
var last_progress := -1.0
var action_until_msec := 0
var capture_errors: Array[String] = []
var direction_rows: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")
	call_deferred("_capture_loop")

func _check(label: String, ok: bool) -> void:
	rows.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
	print("ASTRO_SAVE_CHECK|", label, "|", "PASS" if ok else "FAIL")

func _frames(count: int) -> void:
	for _frame: int in range(count):
		await process_frame

func _touch(control: Control, at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 7
	event.pressed = pressed
	event.position = control.get_global_transform_with_canvas() * at
	Input.parse_input_event(event)

func _tap(control: Control) -> void:
	_touch(control, control.size * 0.5, true)
	await process_frame
	_touch(control, control.size * 0.5, false)
	await process_frame

func _enter() -> OperaCareerWorld2D:
	var routes := main._castle_career_routes_ref()
	routes.sync()
	await _frames(3)
	var card := routes.button_for_act(11)
	_check("real Mermaid Pool career card is visible", card != null and card.is_visible_in_tree() and not card.disabled)
	if card == null:
		return null
	await _tap(card)
	var deadline := Time.get_ticks_msec() + 6000
	while Time.get_ticks_msec() < deadline:
		var house := main.opera_game as OperaHouse
		var fade_ready := main.fade_rect == null or (main.fade_rect.modulate.a <= 0.02 and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)
		var layers_ready := main.living_stage_id == "opera.act.11" and main.living_layer != null and main.living_layer.layer == 11
		if house != null and house.act != null and fade_ready and layers_ready:
			var world := house.act.career_world_2d
			if world != null:
				_check("unforced production route selects Astronaut Canvas surface", world.surface is AstronautSurface and world.career_id == "astronaut" and main.opera_return_room == "mermaid_pool" and world.using_chapter_two_phases and world._astronaut_save_context() == "chapter2:chapter2_astronaut_rocket")
				if not world.using_chapter_two_phases or world.surface == null:
					return null
				_check("all birthday phases own an existing physical station", world.phases.size() == 4 and world.station_for_phase.size() == 4)
				# Earned completion resumes through the world's own hold/callback.
				var hold_deadline := Time.get_ticks_msec() + 4000
				while world.phase_advance_pending and Time.get_ticks_msec() < hold_deadline:
					await create_timer(0.05).timeout
				await _frames(2)
				await _open_current(world)
				return world
		await create_timer(0.05).timeout
	_check("production career entry finishes within deadline", false)
	return null

func _open_current(world: OperaCareerWorld2D) -> void:
	if not world.task_open and world.armed_station >= 0:
		var hotspot := world.station_nodes[world.armed_station] as OperaWorldHotspot2D
		await _tap(hotspot.touch_button)
	var deadline := Time.get_ticks_msec() + 8000
	while not world.task_open and Time.get_ticks_msec() < deadline:
		await create_timer(0.05).timeout
	_check("real object touch opens current phase after approach", world.task_open)
	await create_timer(1.1).timeout

func _wait_phase(world: OperaCareerWorld2D, target: int) -> bool:
	var deadline := Time.get_ticks_msec() + 6000
	while world.phase_index != target and Time.get_ticks_msec() < deadline:
		await create_timer(0.05).timeout
	return world.phase_index == target

func _round_trip(world: OperaCareerWorld2D, label: String) -> OperaCareerWorld2D:
	var before := _snapshot(world, label + "_before_save")
	_check(label + " production save succeeds", main._write_save())
	(main.opera_game as OperaHouse)._leave_early()
	await create_timer(0.4).timeout
	_check(label + " returns to exact room", main.opera_game == null and main.castle_room_id == "mermaid_pool" and main.game == "level2")
	main._load_save()
	var restored := await _enter()
	if restored != null:
		var after := _snapshot(restored, label + "_after_reload")
		if int(before["phase_index"]) == int(after["phase_index"]):
			_check(label + " restores the exact widget fill", is_equal_approx(float(before["fill"]), float(after["fill"])))
	return restored

func _drag(surface: AstronautSurface, at: Vector2, previous: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 7
	event.position = surface.get_global_transform_with_canvas() * at
	event.relative = at - previous
	Input.parse_input_event(event)
	await create_timer(0.025).timeout

func _circle(surface: AstronautSurface, steps: int) -> void:
	var world := (main.opera_game as OperaHouse).act.career_world_2d
	var observer: Callable = _observe_valve.bind(world)
	if not surface.gesture.is_connected(observer):
		surface.gesture.connect(observer)
	var pivot: Vector2 = surface._circle_pivot()
	var previous := pivot + Vector2(110, 0)
	_touch(surface, previous, true)
	await process_frame
	for step in range(1, steps + 1):
		var point := pivot + Vector2.from_angle(float(step) * TAU / 36.0) * 110.0
		await _drag(surface, point, previous)
		previous = point
		if surface.completion_accepted:
			break
	_touch(surface, previous, false)
	await process_frame
	await _drain_valve(surface)
	var contact: Dictionary = world.astronaut_valve_work.last_contact
	_check("native real circle commits through whole-figure valve contact", not contact.is_empty() and float(contact.get("distance", INF)) <= 4.0 and int(contact.get("frame", -1)) in [0, 1] and contact.get("generation", -1) == surface.valve_input_generation)

func _place(surface: AstronautSurface, tile: String, cell: int) -> bool:
	var slot: int = surface.pipe_tray.find(tile)
	if slot < 0:
		return false
	var start: Vector2 = surface._pipe_tray_rect(slot).get_center()
	var finish: Vector2 = surface._pipe_cell_rect(cell).get_center()
	_touch(surface, start, true)
	await process_frame
	if surface.pipe_drag_tile != tile or surface.active_touch_index != 7:
		surface.cancel_input()
		return false
	var drag := InputEventScreenDrag.new()
	drag.index = 7
	drag.position = surface.get_global_transform_with_canvas() * finish
	drag.relative = finish - start
	Input.parse_input_event(drag)
	await process_frame
	_touch(surface, finish, false)
	await process_frame
	var request: int = surface.pipe_work_request_id
	var round_before: int = surface.pipe_round
	var started_msec: int = Time.get_ticks_msec()
	var deferred: bool = surface.pipe_contact_required and surface.pipe_work_cell == cell \
		and surface.pipe_drag_tile == tile and String(surface.pipe_grid[cell]).is_empty()
	_check("released board%d tile at%d waits for owned contact" % [round_before + 1, cell], deferred)
	if not deferred:
		return false
	var deadline: int = started_msec + 3000
	while surface.pipe_work_cell >= 0 and Time.get_ticks_msec() < deadline:
		await create_timer(0.02).timeout
	var house := main.opera_game as OperaHouse
	var world: OperaCareerWorld2D = house.act.career_world_2d if house != null and house.act != null else null
	var contact: Dictionary = world.astronaut_pipe_work.last_contact if world != null and world.astronaut_pipe_work != null else {}
	var contact_ok: bool = surface.pipe_work_cell < 0 and surface.pipe_work_request_id == request \
		and contact.get("request_id", -1) == request and contact.get("cell", -1) == cell \
		and contact.get("phase_index", -1) == 0 and float(contact.get("distance", INF)) <= 4.0 \
		and contact.get("atlas_region", Rect2()) == Rect2(256, 512, 256, 256)
	_check("board%d tile at%d commits through sampled live contact" % [round_before + 1, cell], contact_ok)
	var helper: PipeWork = world.astronaut_pipe_work if world != null else null
	var actor: TextureRect = world.player_actor if world != null else null
	var release_owned: bool = helper != null and actor != null and helper.state == "release" \
		and actor.position.is_equal_approx(helper.work_position) and actor.scale.is_equal_approx(helper.entry_scale) \
		and not world.actor_tweens.has("player") and world.player_animator.current_animation == "work" \
		and world.player_animator.current_frame == 2
	_check("board%d tile at%d preserves owned release position and pose" % [round_before + 1, cell], release_owned)
	contact_requests.append({"request_id": request, "round": round_before, "cell": cell,
		"wait_msec": Time.get_ticks_msec() - started_msec, "sampled_contact_valid": contact_ok,
		"candidate_distance": contact.get("distance", null), "accepted_visual_action": false})
	if round_before > 0:
		await RenderingServer.frame_post_draw
		_capture_frame("pipe_board%d_cell%d_committed" % [round_before + 1, cell], world)
	return String(surface.pipe_grid[cell]) == tile and surface.pipe_drag_tile.is_empty()

func _snapshot(world: OperaCareerWorld2D, label: String) -> Dictionary:
	var surface := world.surface as AstronautSurface
	var value := {"label": label, "phase_index": world.phase_index, "phase_progress": world.phase_progress, "pipe_round": surface.pipe_round, "targets": surface.target_placed.duplicate(), "angle": surface.crank_rotation, "fill": surface.widget_fill, "grid": surface.pipe_grid.duplicate(), "tray": surface.pipe_tray.duplicate(), "held": surface.held, "owner": surface.active_touch_index, "star_mask": main.opera_stars, "pearls": main.pearl_count}
	snapshots.append(value)
	print("ASTRO_SAVE_STATE|", JSON.stringify(value))
	return value

func _run() -> void:
	get_root().size = Vector2i(capture_width, 720)
	_check("native display backend is active", DisplayServer.get_name() != "headless")
	_check("native pilot uses Mobile rendering", RenderingServer.get_current_rendering_method() == "mobile")
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	# Explicit prior-story fixture. Production route/input owns all work earned here.
	main._save_state = SaveState.new(main, test_save)
	var source_save: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tmp/astronaut_partial_save_repair_20261006/reef_save.json")) as Dictionary
	var seed: Dictionary = {"won": {}, "found": {}, "pearls": 0, "plays": 0,
		"day_one_active": false,
		"day_one_completed_rooms": DayOneDirector.ROOM_ORDER.duplicate(),
		"day_one_giant_dust_bunny_boss_triggered": true,
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_party_piece_mask": 0x244D,
		"opera_astronaut_checkpoints": source_save.get("opera_astronaut_checkpoints", {})}
	seed = main._save_state._normalise_save(seed)
	var file := FileAccess.open(test_save, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed))
	file.close()
	var ordinary_before: Dictionary = (seed["opera_astronaut_checkpoints"] as Dictionary)["ordinary"].duplicate(true)
	get_root().add_child(main)
	await _frames(2)
	var continue_button: Button = main.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button if main.start_menu_layer != null else null
	_check("native visible Continue button is available", main.start_menu_active and continue_button != null and continue_button.is_visible_in_tree() and not continue_button.disabled)
	await RenderingServer.frame_post_draw
	_capture_frame("start_menu_before_continue", null)
	if continue_button != null:
		await _tap(continue_button)
	var menu_deadline: int = Time.get_ticks_msec() + 6000
	while main.start_menu_active and Time.get_ticks_msec() < menu_deadline:
		await create_timer(0.05).timeout
	_check("real Continue touch dismisses native title", not main.start_menu_active and main.start_menu_layer == null)
	if main.start_menu_active:
		await _finish()
		return
	main.day_one_active = false
	main._skip_intro()
	_check("valid prior-story fixture reaches Astronaut next", main.chapter2_active and main._chapter_two_ref().next_party_act() == 11 and main.chapter2_party_piece_mask == 0x244D)
	if failed > 0:
		await _finish()
		return
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	await _frames(12)
	main._castle_rooms_ref().show_room("mermaid_pool", false)
	await _frames(3)
	_check("explicit empty and unknown-mode overrides remain rejected", not ChapterTwoCareerSceneAdapter.validate_config_overrides("astronaut", {"phase_overrides": []}) and not ChapterTwoCareerSceneAdapter.validate_config_overrides("astronaut", {"phase_overrides": [{"name": "BROKEN", "mode": "unknown", "goal": 1.0}]}))
	var world := await _enter()
	if world == null or not world.task_open:
		await _finish()
		return
	var surface := world.surface as AstronautSurface
	var routes: Array = [
		[["H", 5], ["H", 6]],
		[["SE", 0], ["H", 1], ["SW", 2], ["NE", 6]],
		[["NW", 5], ["SE", 1], ["H", 2], ["NW", 3]],
	]
	for round_index in range(routes.size()):
		for placement: Array in routes[round_index]:
			_check("genuine board%d placement %s at%d" % [round_index + 1, placement[0], placement[1]], await _place(surface, String(placement[0]), int(placement[1])))
		var deadline := Time.get_ticks_msec() + 6000
		while surface.pipe_round < round_index + 1 and Time.get_ticks_msec() < deadline:
			await create_timer(0.025).timeout
		_check("engine earns board%d exactly once" % (round_index + 1), surface.pipe_round == round_index + 1 and is_equal_approx(world.phase_progress, float(round_index + 1)))
		if round_index == 0:
			_check("board transition has an earned credit and pending next board", surface.pipe_pause > 0.0)
			world = await _round_trip(world, "pipe_transition")
			surface = world.surface as AstronautSurface
			_check("transition save preserves board credit and canonical next stock", surface.pipe_round == 1 and is_equal_approx(world.phase_progress, 1.0) and surface.pipe_tray == surface.PIPE_ROUNDS[1]["tray"])
			if failed > 0:
				await _finish()
				return
		elif round_index < 2:
			await create_timer(1.05).timeout
	_check("third board completes only the pipe phase", world.phase_advance_pending and main.opera_stars == 0 and main.pearl_count == 0)
	world = await _round_trip(world, "completed_pipes")
	surface = world.surface as AstronautSurface
	_check("earned pipe completion resumes normal PATCH handoff", world.phase_index == 1 and surface.mode == "tap" and not world.phase_advance_pending)
	if failed > 0:
		await _finish()
		return
	for index in range(2):
		await _tap_at(surface, surface._target_anchor_point(index))
	_check("two real leak touches earn exactly two patches", is_equal_approx(world.phase_progress, 2.0) and surface.target_placed[0] and surface.target_placed[1])
	var patch_mask := surface.target_placed.duplicate()
	world = await _round_trip(world, "partial_patch")
	surface = world.surface as AstronautSurface
	_check("PATCH phase and exact repaired leaks survive reload", world.phase_index == 1 and is_equal_approx(world.phase_progress, 2.0) and surface.target_placed == patch_mask and not surface.held)
	if failed > 0:
		await _finish()
		return
	await _tap_at(surface, surface._target_anchor_point(0))
	_check("already patched leak cannot pay twice", is_equal_approx(world.phase_progress, 2.0))
	for index in range(2, 5):
		await _tap_at(surface, surface._target_anchor_point(index))
	_check("remaining real leak touches finish PATCH", world.phase_advance_pending and is_equal_approx(world.phase_progress, 5.0))
	_check("normal hold advances to VALVE", await _wait_phase(world, 2))
	await _open_current(world)
	surface = world.surface as AstronautSurface
	_check("native production valve reaches actual local wrench contact", surface.valve_contact_required and await _wait_valve(world))
	await create_timer(0.4).timeout
	_check("native passive local contact never turns or pays", is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation) and surface.valve_arcs.is_empty())
	await _circle(surface, 10)
	var valve_progress := world.phase_progress
	var valve_angle := surface.crank_rotation
	_check("real arc earns partial valve turn", valve_progress > 0.1 and valve_progress < 1.8)
	world = await _round_trip(world, "partial_valve")
	surface = world.surface as AstronautSurface
	_check("VALVE progress and angle survive reload", world.phase_index == 2 and is_equal_approx(world.phase_progress, valve_progress) and is_equal_approx(surface.crank_rotation, valve_angle) and not surface.held)
	if failed > 0:
		await _finish()
		return
	await _circle(surface, 58)
	_check("real circles finish VALVE", world.phase_advance_pending and world.phase_progress >= 1.8)
	_check("normal hold advances to READY PARK", await _wait_phase(world, 3))
	await _open_current(world)
	surface = world.surface as AstronautSurface
	_check("birthday finale is swipe and parked unlaunched", surface.mode == "swipe" and String(world.phases[3].get("rocket_state", "")) == "parked_ready_unlaunched" and not main.chapter2_candle_lit)
	_check("birthday parking binds the complete rocket and floor route", surface.widget_mover != null and surface.widget_mover.resource_path == "res://assets/opera/worlds/props/goal_astronaut.png" and surface.last_contextual_draw_route == "push:park_astronaut" and surface.widget_backdrop == null)
	await _push(surface, -0.10)
	_check("wrong direction cannot park or ignite the rocket", is_zero_approx(world.phase_progress) and is_zero_approx(surface.long_push_journey) and not main.chapter2_candle_lit)
	await _push(surface, 0.35)
	await RenderingServer.frame_post_draw
	_capture_frame("park_successful_partial", world)
	var park_progress := world.phase_progress
	var park_journey := surface.long_push_journey
	_check("genuine motion earns partial parking journey", park_progress > 1.0 and park_progress < 3.0)
	_touch(surface, surface._long_push_start_hit_rect().get_center(), true)
	paused = true
	await _frames(2)
	_check("engine pause cancels parking finger and preserves work", not surface.held and surface.active_touch_index == -1 and is_equal_approx(world.phase_progress, park_progress))
	await RenderingServer.frame_post_draw
	_capture_frame("park_paused_preserved", world)
	paused = false
	_touch(surface, surface._long_push_start_hit_rect().get_center(), false)
	await _frames(2)
	_check("stale parking release cannot earn work", is_equal_approx(world.phase_progress, park_progress))
	world = await _round_trip(world, "partial_park")
	surface = world.surface as AstronautSurface
	_check("READY PARK progress and journey survive save/re-entry", world.phase_index == 3 and is_equal_approx(world.phase_progress, park_progress) and is_equal_approx(surface.long_push_journey, park_journey) and not surface.held and surface.active_touch_index == -1)
	await RenderingServer.frame_post_draw
	_capture_frame("park_restored_partial", world)
	_check("saved legacy parking context restores the rocket skin", surface.visual_context == "push_racer" and surface.widget_mover != null and surface.widget_mover.resource_path == "res://assets/opera/worlds/props/goal_astronaut.png" and surface.last_contextual_draw_route == "push:park_astronaut")
	if failed > 0:
		await _finish()
		return
	await create_timer(0.5).timeout
	_check("passive parked hold cannot complete or ignite", is_equal_approx(world.phase_progress, park_progress) and not world.phase_advance_pending and not main.chapter2_candle_lit)
	await _push(surface, 1.01 - surface.long_push_journey)
	_check("fresh parking motion completes final phase", world.phase_advance_pending and world.phase_progress >= 5.0)
	var finish_deadline := Time.get_ticks_msec() + 8000
	while main.opera_game != null and Time.get_ticks_msec() < finish_deadline:
		await create_timer(0.05).timeout
	_check("natural birthday finish records only story result", main.opera_game == null and main.castle_room_id == "mermaid_pool" and main.chapter2_party_piece_mask == (0x244D | (1 << 11)) and main.opera_stars == 0 and main.pearl_count == 0)
	_check("all four birthday phase bits persist and Detective is next", main.chapter2_job_phase_masks[6] == 0x0F and main._chapter_two_ref().next_party_act() == 1 and not main._chapter_two_ref().can_start_chapter2_act(11))
	_check("completion never starts party or lights candle", not main.chapter2_party_started and not main.chapter2_candle_lit and main.chapter2_party_event_phase == 0)
	var records: Dictionary = main.save_data.get("opera_astronaut_checkpoints", {})
	_check("birthday finish clears only its checkpoint", not records.has("chapter2:chapter2_astronaut_rocket") and records.get("ordinary", {}) == ordinary_before)
	main._load_save()
	_check("story result and ordinary checkpoint survive reload", main.chapter2_party_piece_mask == (0x244D | (1 << 11)) and main.chapter2_job_phase_masks[6] == 0x0F and not main.chapter2_candle_lit and (main.save_data.get("opera_astronaut_checkpoints", {}) as Dictionary).get("ordinary", {}) == ordinary_before)
	await _finish()

func _push(surface: AstronautSurface, amount: float) -> void:
	var at := surface._long_push_start_hit_rect().get_center()
	_touch(surface, at, true)
	await process_frame
	var lane := surface._long_push_end() - surface._long_push_start()
	for index in range(12):
		if surface.completion_accepted:
			break
		var previous := at
		at += lane * amount / 12.0
		await _drag(surface, at, previous)
		await process_frame
	_touch(surface, at, false)
	await process_frame

func _tap_at(surface: AstronautSurface, at: Vector2, wait_work := true) -> void:
	var house := main.opera_game as OperaHouse
	var world: OperaCareerWorld2D = house.act.career_world_2d
	var observer := _observe_patch.bind(world)
	if surface.mode == "tap" and not surface.gesture.is_connected(observer):
		surface.gesture.connect(observer)
	_touch(surface, at, true)
	await process_frame
	_touch(surface, at, false)
	await process_frame
	if wait_work and surface.mode == "tap":
		await _drain_patch(world)

func _finish() -> void:
	_check("all five observed PATCH commits retain live contact and constant size", patch_contacts.size() == 5 and patch_contacts.all(func(row: Dictionary) -> bool: return bool(row["valid"])))
	_check("native observed valve commits retain live pose geometry and size", not valve_contacts.is_empty() and valve_contacts.all(func(row: Dictionary) -> bool: return bool(row["valid"])))
	_direction_checks()
	if main != null and is_instance_valid(main) and main.opera_game == null:
		var fade_deadline: int = Time.get_ticks_msec() + 4000
		while main.fade_rect != null and main.fade_rect.modulate.a > 0.02 and Time.get_ticks_msec() < fade_deadline:
			await create_timer(0.05).timeout
		await RenderingServer.frame_post_draw
		_capture_frame("room_return" if not main.start_menu_active and not main.intro_active else "diagnostic_end_overlay", null)
	capture_running = false
	var manifest := {"schema": "reef.astronaut.native_birthday_pilot.v1", "capture_method": "RenderingServer.frame_post_draw/get_root.texture.get_image.save_png", "display_server": DisplayServer.get_name(), "rendering_method": RenderingServer.get_current_rendering_method(), "rendering_driver": RenderingServer.get_current_rendering_driver_name(), "engine": Engine.get_version_info(), "viewport": [get_root().size.x, get_root().size.y], "dense_counts": dense_counts, "frames": capture_rows, "errors": capture_errors, "diagnostic_only": true, "original_behavior_assertions": 103, "direction_observations": direction_rows, "strict_visual_acceptance": false}
	var manifest_file := FileAccess.open(capture_manifest, FileAccess.WRITE)
	if manifest_file != null:
		manifest_file.store_string(JSON.stringify(manifest, "\t"))
		manifest_file.close()
	else:
		capture_errors.append("Cannot write native capture manifest")
	print("ASTRO_NATIVE_CAPTURE|", JSON.stringify({"frames": capture_rows.size(), "dense_counts": dense_counts, "errors": capture_errors, "display": DisplayServer.get_name(), "rendering_method": RenderingServer.get_current_rendering_method()}))
	print("ASTRO_BIRTHDAY_RESULT|", JSON.stringify({"checks": rows.size(), "failures": failed, "rows": rows, "snapshots": snapshots, "contact_requests": contact_requests, "valve_contacts": valve_contacts, "patch_contacts": patch_contacts, "scope": "Genuine birthday picture/object route after explicit prior-six-jobs fixture; four mechanics, save/load, pause, completion/return and context isolation. No phase/progress injection. Current pipe request/contact timing only; native acting, device/child/owner and full-suite acceptance pending."}))
	if main != null and is_instance_valid(main):
		if main.opera_game != null:
			(main.opera_game as OperaHouse)._leave_early()
		main.queue_free()
	main = null
	await _frames(4)
	quit(1 if failed > 0 else 0)

func _capture_loop() -> void:
	while capture_running:
		await RenderingServer.frame_post_draw
		if not capture_running or main == null or not is_instance_valid(main):
			continue
		var house := main.opera_game as OperaHouse
		var world: OperaCareerWorld2D = house.act.career_world_2d if house != null and house.act != null else null
		if world == null or not is_instance_valid(world) or not world.task_open or world.action_panel == null or not world.action_panel.is_visible_in_tree() or world.action_panel.modulate.a < 0.98:
			continue
		if main.fade_rect != null and main.fade_rect.modulate.a > 0.02:
			continue
		var phase: int = world.phase_index
		if phase < 0 or phase >= DENSE_CAPS.size():
			continue
		var surface := world.surface as AstronautSurface
		if surface == null:
			continue
		_observe_direction(world)
		var now: int = Time.get_ticks_msec()
		var state: String = world.astronaut_pipe_work.state if world.astronaut_pipe_work != null else ""
		var open_key := "phase%d_open" % phase
		if not capture_keys.has(open_key):
			_capture_frame(open_key, world)
			capture_keys[open_key] = true
		var key := open_key
		if not state.is_empty():
			key = "phase%d_pipe_%s" % [phase, state]
		elif world.astronaut_patch_work != null and world.astronaut_patch_work.busy():
			key = "phase%d_patch_%s" % [phase, world.astronaut_patch_work.state]
		elif world.astronaut_valve_work != null and world.astronaut_valve_work.busy():
			var valve_state: String = world.astronaut_valve_work.state
			if valve_state == "contact" and not surface.valve_arcs.is_empty():
				valve_state = "turn"
			key = "phase%d_valve_%s" % [phase, valve_state]
		elif world.phase_advance_pending:
			key = "phase%d_completed" % phase
		elif surface.held:
			key = "phase%d_input_held" % phase
		if not capture_keys.has(key):
			_capture_frame(key, world)
			capture_keys[key] = true
			last_capture_msec = now
		if not is_equal_approx(last_progress, world.phase_progress):
			last_progress = world.phase_progress
			action_until_msec = now + 1000
		var action_active: bool = not state.is_empty() or world.astronaut_patch_work.busy() or surface.held or now < action_until_msec or world.phase_advance_pending
		if action_active and now - last_capture_msec >= 34 and dense_counts[phase] < DENSE_CAPS[phase]:
			_capture_frame("phase%d_action_%03d" % [phase, dense_counts[phase]], world)
			dense_counts[phase] += 1
			last_capture_msec = now

func _v2(value: Vector2) -> Array:
	return [value.x, value.y]

func _rect(value: Rect2) -> Array:
	return [value.position.x, value.position.y, value.size.x, value.size.y]

func _transform(value: Transform2D) -> Array:
	return [_v2(value.x), _v2(value.y), _v2(value.origin)]

func _capture_frame(label: String, world: OperaCareerWorld2D) -> void:
	var image := get_root().get_texture().get_image()
	if image == null or image.is_empty():
		capture_errors.append("Empty viewport: " + label)
		return
	var path := "%s/%04d_%s.png" % [capture_root, capture_rows.size(), label]
	var error: Error = image.save_png(path)
	if error != OK:
		capture_errors.append("PNG write error%d: %s" % [error, label])
		return
	var file := FileAccess.open(path, FileAccess.READ)
	var bytes: int = file.get_length() if file != null else 0
	if file != null:
		file.close()
	var row := {"label": label, "path": path.trim_prefix("res://"), "sha256": FileAccess.get_sha256(path), "bytes": bytes, "dimensions": [image.get_width(), image.get_height()], "monotonic_msec": Time.get_ticks_msec(), "process_frame": Engine.get_process_frames(), "rendered_frame": Engine.get_frames_drawn(), "viewport_instance": get_root().get_instance_id(), "main_instance": main.get_instance_id(), "living_stage": main.living_stage_id, "castle_room": main.castle_room_id, "viewport_canvas_transform": _transform(get_root().get_canvas_transform()), "candle_lit": main.chapter2_candle_lit, "return_fade_alpha": main.fade_rect.modulate.a if main.fade_rect != null else 0.0, "party_started": main.chapter2_party_started, "star_mask": main.opera_stars, "pearls": main.pearl_count}
	if world != null and is_instance_valid(world):
		var actor := world.player_actor
		var surface := world.surface as AstronautSurface
		var atlas := actor.texture as AtlasTexture if actor != null else null
		var state: Dictionary = {"world_instance": world.get_instance_id(), "phase_index": world.phase_index, "phase_progress": world.phase_progress, "phase_advance_pending": world.phase_advance_pending, "task_open": world.task_open, "phase_name": String(world.phases[world.phase_index].get("name", "")), "actor_instance": actor.get_instance_id() if actor != null else 0, "actor_position": _v2(actor.position) if actor != null else [], "actor_size": _v2(actor.size) if actor != null else [], "actor_scale": _v2(actor.scale) if actor != null else [], "actor_flip_h": actor.flip_h if actor != null else false, "actor_z_index": actor.z_index if actor != null else 0, "actor_canvas_transform": _transform(actor.get_global_transform_with_canvas()) if actor != null else [], "actor_atlas_region": _rect(atlas.region) if atlas != null else [], "actor_atlas_source": atlas.atlas.resource_path if atlas != null else "", "surface_instance": surface.get_instance_id() if surface != null else 0, "surface_canvas_transform": _transform(surface.get_global_transform_with_canvas()) if surface != null else [], "surface_mode": surface.mode if surface != null else "", "held": surface.held if surface != null else false, "touch_owner": surface.active_touch_index if surface != null else -1, "widget_fill": surface.widget_fill if surface != null else 0.0, "target_placed": surface.target_placed.duplicate() if surface != null else [], "crank_rotation": surface.crank_rotation if surface != null else 0.0, "long_push_journey": surface.long_push_journey if surface != null else 0.0, "pipe_grid": surface.pipe_grid.duplicate() if surface != null else [], "pipe_round": surface.pipe_round if surface != null else -1, "pipe_work_cell": surface.pipe_work_cell if surface != null else -1}
		if surface != null and surface.mode == "pipe":
			state["pipe_cached_paths"] = surface._pipe_body_paths.size()
			state["pipe_cached_styles"] = surface._pipe_guide_style != null and surface._pipe_tray_style != null and surface._pipe_selected_style != null
			state["pipe_loaded_tile_textures"] = surface.pipe_tiles.size()
			state["pipe_tank_texture"] = surface.pipe_tank_texture.resource_path if surface.pipe_tank_texture != null else ""
			state["pipe_intake_texture"] = surface.pipe_intake_texture.resource_path if surface.pipe_intake_texture != null else ""
		if world.astronaut_pipe_work != null:
			state["pipe_work_state"] = world.astronaut_pipe_work.state
			state["pipe_work_position"] = _v2(world.astronaut_pipe_work.work_position)
			state["pipe_work_flip"] = world.astronaut_pipe_work.work_flip
			state["pipe_travel_start"] = _v2(world.astronaut_pipe_work.travel_start)
			state["pipe_entry_position"] = _v2(world.astronaut_pipe_work.entry_position)
			state["generic_player_tween_owned"] = world.actor_tweens.has("player")
			state["pipe_request_id"] = world.astronaut_pipe_work.request_id
			state["pipe_work_state_t"] = world.astronaut_pipe_work.state_t
			state["pipe_last_contact"] = world.astronaut_pipe_work.last_contact.duplicate(true)
		if world.astronaut_valve_work != null:
			state["valve_state"] = world.astronaut_valve_work.state
			state["valve_work_position"] = _v2(world.astronaut_valve_work.work_position)
			state["valve_entry_scale"] = _v2(world.astronaut_valve_work.entry_scale)
			state["valve_pending_arcs"] = surface.valve_arcs.size()
			state["valve_generation"] = surface.valve_input_generation
			state["valve_last_contact"] = world.astronaut_valve_work.last_contact.duplicate(true)
		if world.astronaut_patch_work != null:
			state["patch_state"] = world.astronaut_patch_work.state
			state["patch_state_t"] = world.astronaut_patch_work.state_t
			state["patch_work_position"] = _v2(world.astronaut_patch_work.work_position)
			state["patch_entry_scale"] = _v2(world.astronaut_patch_work.entry_scale)
			state["patch_queue"] = surface.patch_targets.duplicate()
			state["patch_generation"] = surface.patch_generation
			state["patch_last_contact"] = world.astronaut_patch_work.last_contact.duplicate(true)
			state["patch_draw_route"] = surface.last_contextual_draw_route
			state["surface_alpha"] = surface.modulate.a
			state["surface_self_alpha"] = surface.self_modulate.a
			state["panel_alpha"] = world.action_panel.modulate.a
			state["widget_mover_path"] = surface.widget_mover.resource_path if surface.widget_mover != null else ""
			state["patch_repair_source"] = surface.target_piece_textures[2].resource_path \
				if surface.target_piece_textures.size() > 2 and surface.target_piece_textures[2] != null else ""
		row["live_state"] = state
	capture_rows.append(row)
	print("ASTRO_NATIVE_FRAME|", JSON.stringify({"label": label, "path": row["path"], "sha256": row["sha256"], "monotonic_msec": row["monotonic_msec"]}))

func _observe_direction(world: OperaCareerWorld2D) -> void:
	var helper: PipeWork = world.astronaut_pipe_work
	var actor: TextureRect = world.player_actor
	if helper == null or actor == null or helper.state not in ["approach", "anticipation", "contact_a", "contact_b", "release", "return"]:
		return
	if direction_rows.size() >= 4096:
		capture_errors.append("Direction observation cap exhausted")
		return
	var travel: bool = helper.state in ["approach", "return"]
	var destination: Vector2 = helper.entry_position if helper.state == "return" else helper.work_position
	var displacement: float = destination.x - helper.travel_start.x
	var expected_flip: bool = displacement > 0.0 if travel else helper.work_flip
	direction_rows.append({"request_id": helper.request_id, "state": helper.state,
		"process_frame": Engine.get_process_frames(), "rendered_frame": Engine.get_frames_drawn(),
		"monotonic_msec": Time.get_ticks_msec(), "position": _v2(actor.position),
		"destination": _v2(destination), "travel_start": _v2(helper.travel_start),
		"horizontal_displacement": displacement, "travel": travel,
		"flip_h": actor.flip_h, "expected_flip": expected_flip,
		"animation": world.player_animator.current_animation,
		"frame": world.player_animator.current_frame,
		"scale": _v2(actor.scale), "entry_scale": _v2(helper.entry_scale),
		"scale_preserved": actor.scale.is_equal_approx(helper.entry_scale)})

func _direction_checks() -> void:
	var right_seen := false
	var left_seen := false
	var travel_ok := true
	var work_ok := true
	var scale_ok := true
	var work_seen := false
	for row: Dictionary in direction_rows:
		var flip_ok: bool = bool(row["flip_h"]) == bool(row["expected_flip"])
		if bool(row["travel"]):
			right_seen = right_seen or float(row["horizontal_displacement"]) > 1.0
			left_seen = left_seen or float(row["horizontal_displacement"]) < -1.0
			travel_ok = travel_ok and flip_ok and String(row["animation"]) == "travel"
		else:
			work_seen = true
			work_ok = work_ok and flip_ok and String(row["animation"]) == "work"
		scale_ok = scale_ok and bool(row["scale_preserved"])
	_check("native observer sees both horizontal travel directions", right_seen and left_seen)
	_check("every observed travel frame faces its actual destination", not direction_rows.is_empty() and travel_ok)
	_check("every observed wrench state retains viewport-fit work facing", work_seen and work_ok)
	_check("all observed whole-figure states preserve entry scale", not direction_rows.is_empty() and scale_ok)

func _drain_valve(surface: AstronautSurface) -> void:
	var deadline: int = Time.get_ticks_msec() + 5000
	while not surface.valve_arcs.is_empty() and not surface.completion_accepted and Time.get_ticks_msec() < deadline:
		await create_timer(0.025).timeout

func _wait_valve(world: OperaCareerWorld2D) -> bool:
	var deadline: int = Time.get_ticks_msec() + 3500
	while Time.get_ticks_msec() < deadline:
		var surface := world.surface as AstronautSurface
		if world.astronaut_valve_work != null and world.astronaut_valve_work.contact_eligible(surface.valve_input_generation, world.phase_index, -1):
			return true
		await create_timer(0.02).timeout
	return false

func _observe_valve(kind: String, amount: float, _quality: float, world: OperaCareerWorld2D) -> void:
	if kind != "circle":
		return
	var surface := world.surface as AstronautSurface
	# Raw signal attempts are negative controls, never accepted contact rows.
	if not surface.valve_commit_active:
		return
	var helper = world.astronaut_valve_work
	var valid: bool = helper.contact_eligible(surface.valve_input_generation, world.phase_index, -1) and amount > 0.0 and not world.actor_tweens.has("player")
	valve_contacts.append({"generation": surface.valve_input_generation, "phase": world.phase_index,
		"amount": amount, "progress": world.phase_progress, "angle": surface.crank_rotation,
		"frame": world.player_animator.current_frame, "scale": str(world.player_actor.scale),
		"work_position": str(helper.work_position), "actor_position": str(world.player_actor.position),
		"valid": valid, "time_msec": Time.get_ticks_msec()})


func _drain_patch(world: OperaCareerWorld2D) -> void:
	var deadline: int = Time.get_ticks_msec() + 10000
	var surface := world.surface as AstronautSurface
	while is_instance_valid(world) and world.phase_index == 1 and Time.get_ticks_msec() < deadline:
		if surface.patch_targets.is_empty() and not world.astronaut_patch_work.busy():
			return
		await create_timer(0.02).timeout

func _observe_patch(kind: String, amount: float, _quality: float, world: OperaCareerWorld2D) -> void:
	var surface := world.surface as AstronautSurface
	if kind != "tap" or surface.patch_commit_target < 0:
		return
	var helper = world.astronaut_patch_work
	var target: int = surface.patch_commit_target
	var valid: bool = amount == 1.0 and helper.contact_eligible(surface.patch_generation, world.phase_index, target) and not world.actor_tweens.has("player")
	patch_contacts.append({"generation": surface.patch_generation, "target": target,
		"phase": world.phase_index, "valid": valid, "scale": world.player_actor.scale,
		"frame": world.player_animator.current_frame, "time_msec": Time.get_ticks_msec()})
