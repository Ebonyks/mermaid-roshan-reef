extends SceneTree

const AstronautSurface := preload("res://scripts/opera_astronaut_surface.gd")
const TEST_SAVE := "res://tmp/astronaut_partial_save_20261006/reef_save.json"
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
		var fade_ready := main.fade_rect == null or main.fade_rect.modulate.a <= 0.02
		if house != null and house.act != null and fade_ready:
			var world := house.act.career_world_2d
			if world != null:
				_check("unforced production route selects Astronaut Canvas surface", world.surface is AstronautSurface and world.career_id == "astronaut" and main.opera_return_room == "mermaid_pool")
				await _frames(2)
				var hotspot := world.station_nodes[world.armed_station] as OperaWorldHotspot2D
				await _tap(hotspot.touch_button)
				var open_deadline := Time.get_ticks_msec() + 8000
				while not world.task_open and Time.get_ticks_msec() < open_deadline:
					await create_timer(0.05).timeout
				_check("real object touch opens the pipe activity after approach", world.task_open and world.surface.mode == "pipe")
				await create_timer(0.5).timeout
				return world
		await create_timer(0.05).timeout
	_check("production career entry finishes within deadline", false)
	return null

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
	var value := {"label": label, "phase_index": world.phase_index, "phase_progress": world.phase_progress, "pipe_round": surface.pipe_round, "grid": surface.pipe_grid.duplicate(), "tray": surface.pipe_tray.duplicate(), "held": surface.held, "owner": surface.active_touch_index, "star_mask": main.opera_stars, "pearls": main.pearl_count}
	snapshots.append(value)
	print("ASTRO_SAVE_STATE|", JSON.stringify(value))
	return value

func _run() -> void:
	get_root().size = Vector2i(1280, 720)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	# Replace SaveState before _ready; the real user save is never read or written.
	main._save_state = SaveState.new(main, TEST_SAVE)
	get_root().add_child(main)
	await _frames(2)
	main.day_one_active = false
	main._skip_intro()
	main.chapter2_active = false
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
	_check("board one first H is placed by viewport drag", await _place(surface, "H", 5))
	_check("board one second H is placed by viewport drag", await _place(surface, "H", 6))
	var deadline := Time.get_ticks_msec() + 6000
	while (surface.pipe_round != 1 or surface.pipe_pause > 0.0) and Time.get_ticks_msec() < deadline:
		await create_timer(0.05).timeout
	_check("real engine time earns exactly one board", surface.pipe_round == 1 and is_equal_approx(world.phase_progress, 1.0))
	_check("board two partial SE is placed by viewport drag", await _place(surface, "SE", 0))
	var before := _snapshot(world, "before_save")
	_check("production write succeeds at isolated path", main._write_save())
	var saved := FileAccess.get_file_as_string(TEST_SAVE)
	print("ASTRO_SAVE_FILE|", JSON.stringify({"path": TEST_SAVE, "sha256": FileAccess.get_sha256(TEST_SAVE), "keys": (JSON.parse_string(saved) as Dictionary).keys()}))
	# Exercise the production navigation cancel callback; this is not a visual back-button claim.
	(main.opera_game as OperaHouse)._leave_early()
	await create_timer(0.5).timeout
	_check("production cancel returns to Mermaid Pool", main.opera_game == null and main.game == "level2" and main.castle_room_id == "mermaid_pool" and main.castle_room_layer.visible)
	main._load_save()
	var resumed := await _enter()
	if resumed != null and resumed.task_open:
		var after := _snapshot(resumed, "after_load_reentry")
		_check("save/load preserves earned first board", after["pipe_round"] == before["pipe_round"] and is_equal_approx(float(after["phase_progress"]), float(before["phase_progress"])))
		_check("save/load preserves released partial pipe layout", after["grid"] == before["grid"] and after["tray"] == before["tray"])
		_check("cancel/save/load invents no career reward", after["star_mask"] == before["star_mask"] and after["pearls"] == before["pearls"])
	await _finish()

func _finish() -> void:
	print("ASTRO_SAVE_RESULT|", JSON.stringify({"checks": rows.size(), "failures": failed, "rows": rows, "snapshots": snapshots, "scope": "Headless production route/mechanic/save diagnostic only; isolated synthetic save, fixture story prerequisites, production cancel callback; no current native visual/whole action or target-device acceptance"}))
	if main != null and is_instance_valid(main):
		if main.opera_game != null:
			(main.opera_game as OperaHouse)._leave_early()
		main.queue_free()
	main = null
	await _frames(4)
	quit(1 if failed > 0 else 0)
