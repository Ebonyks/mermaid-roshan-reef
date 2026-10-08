extends SceneTree

const AstronautSurface := preload("res://scripts/opera_astronaut_surface.gd")
const TEST_SAVE := "res://tmp/astronaut_birthday_save_v3_20261007/reef_save.json"
var main: ReefMain
var rows: Array[Dictionary] = []
var snapshots: Array[Dictionary] = []
var failed := 0

func _init() -> void:
	call_deferred("_run")

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
	return String(surface.pipe_grid[cell]) == tile and surface.pipe_drag_tile.is_empty()

func _snapshot(world: OperaCareerWorld2D, label: String) -> Dictionary:
	var surface := world.surface as AstronautSurface
	var value := {"label": label, "phase_index": world.phase_index, "phase_progress": world.phase_progress, "pipe_round": surface.pipe_round, "targets": surface.target_placed.duplicate(), "angle": surface.crank_rotation, "fill": surface.widget_fill, "grid": surface.pipe_grid.duplicate(), "tray": surface.pipe_tray.duplicate(), "held": surface.held, "owner": surface.active_touch_index, "star_mask": main.opera_stars, "pearls": main.pearl_count}
	snapshots.append(value)
	print("ASTRO_SAVE_STATE|", JSON.stringify(value))
	return value

func _run() -> void:
	get_root().size = Vector2i(1280, 720)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	# Explicit prior-story fixture. Production route/input owns all work earned here.
	main._save_state = SaveState.new(main, TEST_SAVE)
	var source_save: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tmp/astronaut_partial_save_repair_20261006/reef_save.json")) as Dictionary
	var seed: Dictionary = {"won": {}, "found": {}, "pearls": 0, "plays": 0,
		"day_one_active": false,
		"day_one_completed_rooms": DayOneDirector.ROOM_ORDER.duplicate(),
		"day_one_giant_dust_bunny_boss_triggered": true,
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_party_piece_mask": 0x244D,
		"opera_astronaut_checkpoints": source_save.get("opera_astronaut_checkpoints", {})}
	seed = main._save_state._normalise_save(seed)
	var file := FileAccess.open(TEST_SAVE, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed))
	file.close()
	var ordinary_before: Dictionary = (seed["opera_astronaut_checkpoints"] as Dictionary)["ordinary"].duplicate(true)
	get_root().add_child(main)
	await _frames(2)
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
	await _push(surface, 0.35)
	var park_progress := world.phase_progress
	var park_journey := surface.long_push_journey
	_check("genuine motion earns partial parking journey", park_progress > 1.0 and park_progress < 3.0)
	_touch(surface, surface._long_push_start_hit_rect().get_center(), true)
	paused = true
	await _frames(2)
	_check("engine pause cancels parking finger and preserves work", not surface.held and surface.active_touch_index == -1 and is_equal_approx(world.phase_progress, park_progress))
	paused = false
	_touch(surface, surface._long_push_start_hit_rect().get_center(), false)
	await _frames(2)
	_check("stale parking release cannot earn work", is_equal_approx(world.phase_progress, park_progress))
	world = await _round_trip(world, "partial_park")
	surface = world.surface as AstronautSurface
	_check("READY PARK progress and journey survive save/re-entry", world.phase_index == 3 and is_equal_approx(world.phase_progress, park_progress) and is_equal_approx(surface.long_push_journey, park_journey) and not surface.held and surface.active_touch_index == -1)
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

func _tap_at(surface: AstronautSurface, at: Vector2) -> void:
	_touch(surface, at, true)
	await process_frame
	_touch(surface, at, false)
	await process_frame

func _finish() -> void:
	print("ASTRO_BIRTHDAY_RESULT|", JSON.stringify({"checks": rows.size(), "failures": failed, "rows": rows, "snapshots": snapshots, "scope": "Genuine birthday picture/object route after explicit prior-six-jobs fixture; four mechanics, save/load, pause, completion/return and context isolation. No phase/progress injection. Native acting/contact, device/child/owner and full-suite acceptance pending."}))
	if main != null and is_instance_valid(main):
		if main.opera_game != null:
			(main.opera_game as OperaHouse)._leave_early()
		main.queue_free()
	main = null
	await _frames(4)
	quit(1 if failed > 0 else 0)
