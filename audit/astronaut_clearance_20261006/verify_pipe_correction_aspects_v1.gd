extends SceneTree

const AstronautSurface := preload("res://scripts/opera_astronaut_surface.gd")
var test_save := ""
var test_width := 1280
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
	print("ASTRO_CARD_DIAGNOSTIC|", JSON.stringify({"stage": main.living_stage_id, "game": main.game, "rect": str(card.get_global_rect()), "fade_alpha": main.fade_rect.modulate.a if main.fade_rect != null else -1.0, "fade_filter": main.fade_rect.mouse_filter if main.fade_rect != null else -1}))
	var fade_deadline := Time.get_ticks_msec() + 4000
	while main.fade_rect != null and (main.fade_rect.modulate.a > 0.02 or main.fade_rect.mouse_filter != Control.MOUSE_FILTER_IGNORE) and Time.get_ticks_msec() < fade_deadline:
		await create_timer(0.05).timeout
	_check("room fade permits real card input", main.fade_rect == null or (main.fade_rect.modulate.a <= 0.02 and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE))
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
	var final_house := main.opera_game as OperaHouse
	print("ASTRO_CARD_DIAGNOSTIC|", JSON.stringify({"stage": main.living_stage_id, "game": main.game, "house": final_house != null, "act": final_house != null and final_house.act != null, "surface": str(final_house.act.career_world_2d.surface) if final_house != null and final_house.act != null and final_house.act.career_world_2d != null else "absent", "fade_alpha": main.fade_rect.modulate.a if main.fade_rect != null else -1.0}))
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
	if not await _drop(surface, tile, cell):
		return false
	return await _settle_contact(world, tile, cell)


func _settle_contact(world: OperaCareerWorld2D, tile: String, cell: int) -> bool:
	var surface := world.surface as AstronautSurface
	var scale := world.player_actor.scale
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
		var transform := world.player_actor.get_global_transform_with_canvas()
		var minimum := Vector2(INF, INF)
		var maximum := Vector2(-INF, -INF)
		for corner: Vector2 in [Vector2.ZERO, Vector2(world.player_actor.size.x, 0.0), world.player_actor.size, Vector2(0.0, world.player_actor.size.y)]:
			var point := transform * corner
			minimum = minimum.min(point)
			maximum = maximum.max(point)
		var bounds := Rect2(minimum, maximum - minimum)
		contacts[-1]["actor_viewport_bounds"] = [bounds.position.x, bounds.position.y, bounds.size.x, bounds.size.y]
		contacts[-1]["viewport"] = [test_width, 720]
		_check("whole figure control fits actual viewport at%d" % cell, get_root().get_visible_rect().encloses(bounds))
		_check("actual full-figure contact geometry and size at%d" % cell, float(contact["distance"]) <= 4.0 and world.player_actor.scale.is_equal_approx(scale) and region == Rect2(256, 512, 256, 256))
		_check("repeated same commit is rejected at%d" % cell, not world._commit_astronaut_pipe_work(token, world.phase_index, cell))
	return valid


func _run() -> void:
	test_width = OS.get_environment("ASTRO_PIPE_WIDTH").to_int()
	_check("requested aspect is supported", test_width in [1280, 1600])
	if failed > 0:
		await _finish()
		return
	test_save = "res://tmp/astronaut_pipe_correction_aspects_v1_20261007/%dx720/reef_save.json" % test_width
	get_root().size = Vector2i(test_width, 720)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	main._save_state = SaveState.new(main, test_save)
	var seed: Dictionary = {"won": {}, "found": {}, "pearls": 0, "plays": 0,
		"day_one_active": false, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER.duplicate(),
		"day_one_giant_dust_bunny_boss_triggered": true,
		"day_one_giant_dust_bunny_boss_defeated": true, "chapter2_party_piece_mask": 0x244D}
	seed = main._save_state._normalise_save(seed)
	var file := FileAccess.open(test_save, FileAccess.WRITE)
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
	_check("actual expanded viewport has requested width", get_root().get_visible_rect().size == Vector2(test_width, 720))
	_check("board1 H5 contact succeeds", await _place(world, "H", 5))
	_check("board1 H6 contact succeeds", await _place(world, "H", 6))
	var deadline := Time.get_ticks_msec() + 6000
	while surface.pipe_round < 1 and Time.get_ticks_msec() < deadline:
		await create_timer(0.025).timeout
	_check("board1 earns exactly one credit", surface.pipe_round == 1 and world.phase_progress == 1.0)
	await create_timer(1.15).timeout
	if failed > 0:
		await _finish()
		return
	var stock: Dictionary = _inventory(surface)
	_check("board2 exact authored free stock starts intact", stock == {"H": 2, "SE": 1, "SW": 1, "NE": 1})
	_check("wrong SW0 still requires actual local contact", await _place(world, "SW", 0))
	deadline = Time.get_ticks_msec() + 3000
	while 0 not in surface._pipe_flow_cells() and Time.get_ticks_msec() < deadline:
		await create_timer(0.025).timeout
	_check("engine fuel actually enters wrong SW0", 0 in surface._pipe_flow_cells() and String(surface.pipe_grid[0]) == "SW")
	await create_timer(0.4).timeout
	_check("fueled wrong plan earns no extra credit or loses stock", world.phase_progress == 1.0 and surface.pipe_round == 1 and not world.phase_advance_pending and _inventory(surface) == stock)
	_check("wrong fueled pipe can be lifted toward correct cell", await _drag_grid(surface, 0, surface._pipe_cell_rect(2).get_center()) and surface.pipe_work_cell == 2 and surface.pipe_drag_tile == "SW" and surface.pipe_drag_from == 0)
	var old_token := surface.pipe_work_request_id
	var pending: Dictionary = surface.progress_snapshot()
	_check("pending relocation snapshot restores source not target", pending["grid"][0] == "SW" and pending["grid"][2] == "" and _inventory(surface) == stock and 0 not in surface._pipe_flow_cells())
	_check("pending relocation uses normal save owner", main._write_save())
	var disk: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(test_save)) as Dictionary
	var record: Dictionary = (disk.get("opera_astronaut_checkpoints", {}) as Dictionary).get("chapter2:chapter2_astronaut_rocket", {})
	var mechanic: Dictionary = record.get("mechanic", {})
	_check("actual saved pending relocation preserves source and credit", not mechanic.is_empty() and mechanic["grid"][0] == "SW" and mechanic["grid"][2] == "" and record.get("progress", -1) == 1.0)
	paused = true
	await create_timer(0.2, true, false, true).timeout
	_check("actual pause restores original wrong piece without credit", surface.pipe_work_cell == -1 and not world.astronaut_pipe_work.busy() and String(surface.pipe_grid[0]) == "SW" and String(surface.pipe_grid[2]).is_empty() and world.phase_progress == 1.0 and _inventory(surface) == stock)
	paused = false
	await create_timer(0.8).timeout
	_check("canceled relocation cannot commit later", String(surface.pipe_grid[2]).is_empty() and not world._commit_astronaut_pipe_work(old_token, 0, 2) and world.phase_progress == 1.0)
	_check("off-grid drag returns wrong piece to selected tray", await _drag_grid(surface, 0, surface._pipe_tray_rect(0).get_center()) and String(surface.pipe_grid[0]).is_empty() and surface.pipe_tray.count("SW") == 1 and surface.pipe_tray_sel >= 0 and String(surface.pipe_tray[surface.pipe_tray_sel]) == "SW" and surface.pipe_work_cell == -1 and _inventory(surface) == stock)
	await _tap_at(surface, surface._pipe_cell_rect(2).get_center())
	_check("selected-tile tap requests owned contact", surface.pipe_work_cell == 2 and surface.pipe_drag_tile == "SW" and String(surface.pipe_grid[2]).is_empty())
	_check("selected-tile correction commits locally", await _settle_contact(world, "SW", 2))
	_check("corrected SW keeps exact stock and unearned board", _inventory(surface) == stock and world.phase_progress == 1.0 and String(surface.pipe_grid[0]).is_empty())
	for placement: Array in [["SE", 0], ["H", 1], ["NE", 6]]:
		_check("remaining corrected route %s at%d" % [placement[0], placement[1]], await _place(world, String(placement[0]), int(placement[1])))
		if failed > 0:
			await _finish()
			return
	deadline = Time.get_ticks_msec() + 6000
	while surface.pipe_round < 2 and Time.get_ticks_msec() < deadline:
		await create_timer(0.025).timeout
	_check("genuine correction finishes board2 exactly once", surface.pipe_round == 2 and world.phase_progress == 2.0 and not world.phase_advance_pending)
	_check("correction does not award career pearls or light candle", main.opera_stars == 0 and main.pearl_count == 0 and not main.chapter2_candle_lit)
	await _finish()


func _inventory(surface: AstronautSurface) -> Dictionary:
	var result: Dictionary = {}
	for value: Variant in surface.pipe_tray:
		var tile := String(value)
		result[tile] = int(result.get(tile, 0)) + 1
	for cell in range(surface.pipe_grid.size()):
		var tile := String(surface.pipe_grid[cell])
		if not surface.pipe_fixed[cell] and surface.PIPE_MOUTHS.has(tile):
			result[tile] = int(result.get(tile, 0)) + 1
	if not surface.pipe_drag_tile.is_empty():
		var tile := surface.pipe_drag_tile
		result[tile] = int(result.get(tile, 0)) + 1
	return result


func _tap_at(surface: AstronautSurface, at: Vector2) -> void:
	_touch(surface, at, true)
	await process_frame
	_touch(surface, at, false)
	await process_frame


func _drag_grid(surface: AstronautSurface, cell: int, finish: Vector2) -> bool:
	var start: Vector2 = surface._pipe_cell_rect(cell).get_center()
	_touch(surface, start, true)
	await process_frame
	if surface.pipe_drag_tile != "SW" or surface.pipe_drag_from != cell:
		return false
	var drag := InputEventScreenDrag.new()
	drag.index = 7
	drag.position = surface.get_global_transform_with_canvas() * finish
	drag.relative = finish - start
	Input.parse_input_event(drag)
	await process_frame
	_touch(surface, finish, false)
	await process_frame
	return true


func _finish() -> void:
	print("ASTRO_PIPE_RESULT|", JSON.stringify({"width": test_width, "height": 720, "checks": rows.size(), "failures": failed, "rows": rows, "contacts": contacts,
		"scope": "Current headless1280x720and1600x720 birthday card/object/wrong-plan input after explicit prior-six-jobs fixture. Fueled wrong-pipe lifting, pending source save/pause conservation, selected-tile correction, sampled whole-figure control bounds and normal board credit only. No native pixels/visual/fullchapter/device/child/owner/fullCI acceptance."}))
	if main != null and is_instance_valid(main):
		if main.opera_game != null:
			(main.opera_game as OperaHouse)._leave_early()
		main.queue_free()
	main = null
	await _frames(4)
	quit(1 if failed > 0 else 0)
