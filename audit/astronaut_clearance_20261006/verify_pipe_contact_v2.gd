extends SceneTree

const AstronautSurface := preload("res://scripts/opera_astronaut_surface.gd")
const TEST_SAVE := "res://tmp/astronaut_pipe_contact_v2_20261007/reef_save.json"
var main: ReefMain
var rows: Array[Dictionary] = []
var contacts: Array[Dictionary] = []
var failed := 0


func _init() -> void:
	call_deferred("_run")


func _check(label: String, ok: bool) -> void:
	rows.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
	print("ASTRO_PIPE_CHECK|", label, "|", "PASS" if ok else "FAIL")


func _frames(count: int) -> void:
	for index in range(count):
		await process_frame


func _touch(control: Control, at: Vector2, pressed: bool, finger := 7) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
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
	_check("actual birthday card is visible", card != null and card.is_visible_in_tree() and not card.disabled)
	if card == null:
		return null
	await _tap(card)
	var deadline := Time.get_ticks_msec() + 6000
	while Time.get_ticks_msec() < deadline:
		var house := main.opera_game as OperaHouse
		var fade_ready := main.fade_rect == null or (main.fade_rect.modulate.a <= 0.02 and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)
		if house != null and house.act != null and fade_ready:
			var world := house.act.career_world_2d
			if world != null and world.surface is AstronautSurface:
				_check("production world requires pipe contact", world.career_id == "astronaut" and world.using_chapter_two_phases and (world.surface as AstronautSurface).pipe_contact_required and world.astronaut_pipe_work != null)
				if not world.task_open and world.armed_station >= 0:
					var hotspot := world.station_nodes[world.armed_station] as OperaWorldHotspot2D
					await _tap(hotspot.touch_button)
				var approach_deadline := Time.get_ticks_msec() + 8000
				while not world.task_open and Time.get_ticks_msec() < approach_deadline:
					await create_timer(0.05).timeout
				_check("actual object touch opens pipe after room approach", world.task_open and world.phase_index == 0)
				await create_timer(1.1).timeout
				return world
		await create_timer(0.05).timeout
	_check("birthday route enters within deadline", false)
	return null


func _drop(surface: AstronautSurface, tile: String, cell: int) -> bool:
	var slot: int = surface.pipe_tray.find(tile)
	if slot < 0:
		return false
	var start: Vector2 = surface._pipe_tray_rect(slot).get_center()
	var finish: Vector2 = surface._pipe_cell_rect(cell).get_center()
	_touch(surface, start, true)
	await process_frame
	if surface.pipe_drag_tile != tile:
		return false
	var drag := InputEventScreenDrag.new()
	drag.index = 7
	drag.position = surface.get_global_transform_with_canvas() * finish
	drag.relative = finish - start
	Input.parse_input_event(drag)
	await process_frame
	_touch(surface, finish, false)
	await process_frame
	return surface.pipe_work_cell == cell and String(surface.pipe_grid[cell]).is_empty()


func _place(world: OperaCareerWorld2D, tile: String, cell: int) -> bool:
	var surface := world.surface as AstronautSurface
	var scale := world.player_actor.scale
	if not await _drop(surface, tile, cell):
		return false
	var token := surface.pipe_work_request_id
	_check("early world commit is rejected at%d" % cell, not world._commit_astronaut_pipe_work(token, world.phase_index, cell))
	var deadline := Time.get_ticks_msec() + 3000
	while surface.pipe_work_cell >= 0 and Time.get_ticks_msec() < deadline:
		await create_timer(0.02).timeout
	var contact: Dictionary = world.astronaut_pipe_work.last_contact
	var valid: bool = String(surface.pipe_grid[cell]) == tile and contact.get("request_id", -1) == token
	if valid:
		var jaw: Vector2 = contact["jaw"]
		var target: Vector2 = contact["target"]
		var region: Rect2 = contact["atlas_region"]
		contacts.append({"request_id": token, "round": surface.pipe_round, "cell": cell,
			"jaw_viewport": [jaw.x, jaw.y], "target_viewport": [target.x, target.y],
			"distance": contact["distance"], "scale": [scale.x, scale.y],
			"atlas_region": [region.position.x, region.position.y, region.size.x, region.size.y]})
		_check("actual full-figure contact geometry and size at%d" % cell, float(contact["distance"]) <= 4.0 and world.player_actor.scale.is_equal_approx(scale) and region == Rect2(256, 512, 256, 256))
		_check("repeated same commit is rejected at%d" % cell, not world._commit_astronaut_pipe_work(token, world.phase_index, cell))
	return valid


func _run() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	main._save_state = SaveState.new(main, TEST_SAVE)
	var seed: Dictionary = {"won": {}, "found": {}, "pearls": 0, "plays": 0,
		"day_one_active": false, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER.duplicate(),
		"day_one_giant_dust_bunny_boss_triggered": true,
		"day_one_giant_dust_bunny_boss_defeated": true, "chapter2_party_piece_mask": 0x244D}
	seed = main._save_state._normalise_save(seed)
	var file := FileAccess.open(TEST_SAVE, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed))
	file.close()
	get_root().add_child(main)
	await _frames(2)
	main.day_one_active = false
	main._skip_intro()
	_check("explicit prior-six-jobs fixture makes Astronaut next", main.chapter2_active and main._chapter_two_ref().next_party_act() == 11)
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	await _frames(12)
	main._castle_rooms_ref().show_room("mermaid_pool", false)
	await _frames(3)
	var world := await _enter()
	if world == null or not world.task_open:
		await _finish()
		return
	var surface := world.surface as AstronautSurface
	await create_timer(0.4).timeout
	_check("passive time grants no placement or board", world.phase_progress == 0.0 and surface.pipe_round == 0 and String(surface.pipe_grid[5]).is_empty())
	_check("real released tile remains pending before work", await _drop(surface, "H", 5))
	var first_token := surface.pipe_work_request_id
	var before_repeat := surface.progress_snapshot()
	_touch(surface, surface._pipe_tray_rect(0).get_center(), true, 9)
	await process_frame
	_touch(surface, surface._pipe_tray_rect(0).get_center(), false, 9)
	await process_frame
	_check("second finger cannot stack pending work", surface.pipe_work_request_id == first_token and surface.progress_snapshot() == before_repeat)
	_check("pending world commit is rejected", not world._commit_astronaut_pipe_work(first_token, 0, 5))
	_check("save before contact conserves source tile", before_repeat["grid"][5] == "" and (before_repeat["tray"] as Array).count("H") == 2 and main._write_save())
	surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_check("focus loss cancels unearned approach", surface.pipe_work_cell == -1 and not world.astronaut_pipe_work.busy() and surface.pipe_tray.count("H") == 2)
	await create_timer(0.9).timeout
	_check("canceled work cannot commit later", String(surface.pipe_grid[5]).is_empty() and world.phase_progress == 0.0 and not world._commit_astronaut_pipe_work(first_token, 0, 5))
	surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_check("new intent after focus can request again", await _drop(surface, "H", 5))
	paused = true
	await create_timer(0.25, true, false, true).timeout
	_check("actual tree pause cancels unearned work", surface.pipe_work_cell == -1 and not world.astronaut_pipe_work.busy() and surface.pipe_tray.count("H") == 2 and world.phase_progress == 0.0)
	paused = false
	await _frames(2)
	var routes: Array = [[["H", 5], ["H", 6]], [["SE", 0], ["H", 1], ["SW", 2], ["NE", 6]], [["NW", 5], ["SE", 1], ["H", 2], ["NW", 3]]]
	for round_index in range(routes.size()):
		for placement: Array in routes[round_index]:
			_check("genuine local board%d placement %s at%d" % [round_index + 1, placement[0], placement[1]], await _place(world, String(placement[0]), int(placement[1])))
			if failed > 0:
				await _finish()
				return
		var deadline := Time.get_ticks_msec() + 6000
		while surface.pipe_round < round_index + 1 and Time.get_ticks_msec() < deadline:
			await create_timer(0.025).timeout
		_check("normal engine earns board%d once" % (round_index + 1), surface.pipe_round == round_index + 1 and is_equal_approx(world.phase_progress, float(round_index + 1)))
		if round_index < routes.size() - 1:
			await create_timer(1.15).timeout
	_check("earned pipe action keeps birthday rocket unlit", not main.chapter2_candle_lit and main.opera_stars == 0 and main.pearl_count == 0)
	await _finish()


func _finish() -> void:
	print("ASTRO_PIPE_RESULT|", JSON.stringify({"checks": rows.size(), "failures": failed, "rows": rows, "contacts": contacts,
		"scope": "Current source genuine birthday card/object/pipe input after explicit prior-six-jobs fixture. Candidate authored jaw geometry, deferred placement, interruption and conservation only; native visual/full-route/device/child/owner/fullCI acceptance pending."}))
	if main != null and is_instance_valid(main):
		if main.opera_game != null:
			(main.opera_game as OperaHouse)._leave_early()
		main.queue_free()
	main = null
	await _frames(4)
	quit(1 if failed > 0 else 0)
