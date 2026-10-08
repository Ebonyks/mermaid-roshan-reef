extends SceneTree

const AstronautSurface := preload("res://scripts/opera_astronaut_surface.gd")
const TEST_SAVE := "res://tmp/astronaut_birthday_patch_readability_v1_20261007/reef_save.json"
var main: ReefMain
var rows: Array[Dictionary] = []
var snapshots: Array[Dictionary] = []
var contact_requests: Array[Dictionary] = []
var failed := 0
var valve_contacts: Array[Dictionary] = []
var patch_contacts: Array[Dictionary] = []

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

func _circle(surface: AstronautSurface, steps: int, verify_contact := true) -> void:
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
	if verify_contact:
		var world := (main.opera_game as OperaHouse).act.career_world_2d
		var contact: Dictionary = world.astronaut_valve_work.last_contact
		_check("real circle motion commits only at whole-figure valve contact", not contact.is_empty() and float(contact.get("distance", INF)) <= 4.0 and int(contact.get("frame", -1)) in [0, 1] and contact.get("generation", -1) == surface.valve_input_generation)

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
	contact_requests.append({"request_id": request, "round": round_before, "cell": cell,
		"wait_msec": Time.get_ticks_msec() - started_msec, "sampled_contact_valid": contact_ok,
		"candidate_distance": contact.get("distance", null), "accepted_visual_action": false})
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
	await _patch_controls(world)
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
		await _tap_at(surface, surface._target_anchor_point(index), false)
	_check("three remaining rapid taps queue without premature repair", surface.patch_targets == [2, 3, 4] and is_equal_approx(world.phase_progress, 2.0))
	await _drain_patch(world)
	var remaining_contacts := patch_contacts.filter(func(row: Dictionary) -> bool: return int(row["target"]) >= 2)
	_check("three remaining queued repairs drain through individual live contacts", surface.patch_targets.is_empty() and remaining_contacts.size() == 3 and remaining_contacts.all(func(row: Dictionary) -> bool: return bool(row["valid"])))
	_check("remaining real leak touches finish PATCH", world.phase_advance_pending and is_equal_approx(world.phase_progress, 5.0))
	_check("normal hold advances to VALVE", await _wait_phase(world, 2))
	await _open_current(world)
	surface = world.surface as AstronautSurface
	await _valve_controls(world)
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
	_check("all actual valve commits bind live pose geometry and constant size", not valve_contacts.is_empty() and valve_contacts.all(func(row: Dictionary) -> bool: return bool(row["valid"])))
	print("ASTRO_BIRTHDAY_RESULT|", JSON.stringify({"checks": rows.size(), "failures": failed, "rows": rows, "snapshots": snapshots, "contact_requests": contact_requests, "valve_contacts": valve_contacts, "patch_contacts": patch_contacts, "scope": "Genuine birthday picture/object route after explicit prior-six-jobs fixture; four mechanics, save/load, pause, completion/return and context isolation. No phase/progress injection. Current pipe request/contact timing only; native acting, device/child/owner and full-suite acceptance pending."}))
	if main != null and is_instance_valid(main):
		if main.opera_game != null:
			(main.opera_game as OperaHouse)._leave_early()
		main.queue_free()
	main = null
	await _frames(4)
	quit(1 if failed > 0 else 0)

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

func _early_arcs(surface: AstronautSurface) -> void:
	var center: Vector2 = surface._circle_pivot()
	var previous := center + Vector2(110, 0)
	_touch(surface, previous, true)
	await process_frame
	for step in range(1, 7):
		var point := center + Vector2.from_angle(float(step) * TAU / 36.0) * 110.0
		await _drag(surface, point, previous)
		previous = point
	_touch(surface, previous, false)
	await process_frame

func _valve_controls(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as AstronautSurface
	surface.gesture.connect(_observe_valve.bind(world))
	_check("production valve requires live local contact", surface.valve_contact_required and await _wait_valve(world))
	await create_timer(0.4).timeout
	_check("passive local contact never turns valve or grants work", is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation) and surface.valve_arcs.is_empty())
	surface.gesture.emit("tap", 100.0, 1.0)
	surface.gesture.emit("circle", 100.0, 1.0)
	_check("wrong-mode and direct circle signals cannot award valve work", is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation))
	for corruption in ["position", "pose"]:
		_check("local contact is ready before " + corruption + " negative", await _wait_valve(world))
		var generation: int = surface.valve_input_generation
		if corruption == "position":
			world.player_actor.position += Vector2(40, 0)
		else:
			world.player_animator.show_pose("idle", 0)
		await _circle(surface, 6, false)
		_check("live " + corruption + " mismatch cancels arcs without rotation or credit", is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation) and surface.valve_arcs.is_empty() and not surface.held)
		_check("stale " + corruption + " generation never commits", is_zero_approx(world._commit_astronaut_valve_motion(generation, world.phase_index, 0.1)))
	_check("fresh local contact recovers after negative controls", await _wait_valve(world))
	surface.cancel_input()
	await _early_arcs(surface)
	_check("early released real circle queues without remote work", not surface.valve_arcs.is_empty() and is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation) and not surface.held)
	paused = true
	await _frames(2)
	_check("engine pause discards pending valve arcs and contact owner", surface.valve_arcs.is_empty() and not surface.held and surface.active_touch_index == -1 and not world.astronaut_valve_work.busy() and is_zero_approx(world.phase_progress))
	paused = false
	await create_timer(0.4).timeout
	_check("paused request never turns or pays after resume", is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation))
	surface.cancel_input()
	await _early_arcs(surface)
	_check("normal early release preserves requested arcs for approach", not surface.valve_arcs.is_empty() and is_zero_approx(world.phase_progress) and is_zero_approx(surface.crank_rotation) and not surface.held)
	await _drain_valve(surface)
	_check("released real arcs execute exactly once at local contact", is_equal_approx(world.phase_progress, 5.0 / 36.0) and is_equal_approx(surface.crank_rotation, 5.0 * TAU / 36.0) and surface.valve_arcs.is_empty())

func _patch_controls(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as AstronautSurface
	await create_timer(0.3).timeout
	_check("passive PATCH time leaves every leak unrepaired", is_zero_approx(world.phase_progress) and surface.patch_targets.is_empty() and surface.target_placed.all(func(x: bool) -> bool: return not x))
	surface.gesture.emit("tap", 100.0, 1.0)
	surface.gesture.emit("circle", 100.0, 1.0)
	_check("raw signals cannot bypass PATCH work", is_zero_approx(world.phase_progress) and not world.phase_advance_pending)
	await _tap_at(surface, Vector2.ZERO, false)
	_check("outside tap requests no PATCH work", surface.patch_targets.is_empty() and is_zero_approx(world.phase_progress))
	await _tap_at(surface, surface._target_anchor_point(0), false)
	_check("quick PATCH release retains request without premature repair", surface.patch_targets == [0] and not surface.target_placed[0] and is_zero_approx(world.phase_progress) and not surface.held)
	await _tap_at(surface, surface._target_anchor_point(0), false)
	_check("repeated pending leak cannot stack work", surface.patch_targets == [0])
	await _tap_at(surface, surface._target_anchor_point(1), false)
	_check("distinct quick leak taps queue separately", surface.patch_targets == [0, 1] and is_zero_approx(world.phase_progress))
	paused = true
	await _frames(2)
	_check("actual pause discards pending leaks without repairs", surface.patch_targets.is_empty() and not surface.held and surface.active_touch_index == -1 and not world.astronaut_patch_work.busy() and is_zero_approx(world.phase_progress))
	paused = false
	await create_timer(0.25).timeout
	_check("resume cannot repair stale PATCH requests", surface.patch_targets.is_empty() and is_zero_approx(world.phase_progress))
	await _tap_at(surface, surface._target_anchor_point(0), false)
	surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_check("focus loss clears pending PATCH owner", surface.patch_targets.is_empty() and not world.astronaut_patch_work.busy() and is_zero_approx(world.phase_progress))
	surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	await _tap_at(surface, surface._target_anchor_point(0), false)
	_check("focus recovery accepts fresh PATCH request", surface.patch_targets == [0])
	surface.cancel_input()
	await create_timer(0.25).timeout
	_check("explicit cancellation preserves unrepaired PATCH mask", surface.patch_targets.is_empty() and is_zero_approx(world.phase_progress) and not surface.target_placed[0])
	for corruption in ["position", "pose"]:
		await _tap_at(surface, surface._target_anchor_point(0), false)
		var generation: int = surface.patch_generation
		_check("wrong PATCH phase rejects request: " + corruption, not world._commit_astronaut_patch_work(generation, world.phase_index + 1, 0))
		var deadline: int = Time.get_ticks_msec() + 2500
		while world.astronaut_patch_work.state != "contact_b" and Time.get_ticks_msec() < deadline:
			await create_timer(0.01).timeout
		_check("real PATCH contact interval precedes perturbation: " + corruption, world.astronaut_patch_work.state == "contact_b")
		if corruption == "position":
			world.player_actor.position += Vector2(40, 0)
		else:
			world.player_animator.show_pose("idle", 0)
		await create_timer(0.4).timeout
		_check("live PATCH " + corruption + " mismatch cancels without repair", surface.patch_targets.is_empty() and not surface.target_placed[0] and is_zero_approx(world.phase_progress) and world.astronaut_patch_work.last_contact.is_empty())
		_check("canceled PATCH token rejects later commit: " + corruption, not world._commit_astronaut_patch_work(generation, world.phase_index, 0))

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
