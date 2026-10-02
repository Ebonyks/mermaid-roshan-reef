extends SceneTree
## Actual production surface and all four ordinary career phases. Only entry
## fixture and isolated test save home are supplied; no phase forcing, source
## injection, replacement surface, background overlay or completion callback patch.
const OUT := "res://audit/job_geology_river_runtime_v1_20261002/attempt_01/"
var main: ReefMain
var width_now := 1280
var records: Array[Dictionary] = []
var events: Array[Dictionary] = []

func _initialize() -> void:
	_run.call_deferred()

func _wait(count: int) -> void:
	for _i: int in range(count):
		await process_frame

func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = at
	event.pressed = pressed
	Input.parse_input_event(event)
	await _wait(2)

func _surface_touch(surface: Control, at: Vector2, pressed: bool) -> void:
	await _touch(surface.get_global_transform_with_canvas() * at, pressed)

func _drag(surface: Control, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * at
	Input.parse_input_event(event)
	await _wait(2)

func _segment(surface: Control, start: Vector2, end: Vector2) -> void:
	for step: int in range(1, 11):
		await _drag(surface, start.lerp(end, float(step) / 10.0))

func _freeze(node: Node, states: Dictionary) -> void:
	states[node] = [node.is_processing(), node.is_physics_processing()]
	node.set_process(false)
	node.set_physics_process(false)
	for child: Node in node.get_children():
		_freeze(child, states)

func _capture(world: OperaCareerWorld2D, state_name: String) -> void:
	var states: Dictionary = {}
	_freeze(world, states)
	await _wait(2)
	var image := root.get_texture().get_image()
	var phase := String((world.phases[mini(world.phase_index, world.phases.size() - 1)] as Dictionary)["name"])
	var name := "geologist_%d_%s_%s.webp" % [width_now, phase.to_lower(), state_name]
	assert(image.save_webp(OUT + "native_views/" + name, true) == OK)
	var surface := world.surface as OperaGeologySurface
	records.append({"id": name.trim_suffix(".webp"), "path": "native_views/" + name,
		"viewport": [width_now,720], "phase": phase, "phase_index": world.phase_index,
		"state": state_name, "task_open": world.task_open, "phase_progress": world.phase_progress,
		"surface": surface.progress_snapshot(), "right_half_rect": [surface._geode_right_rect().position.x,
			surface._geode_right_rect().position.y, surface._geode_right_rect().size.x, surface._geode_right_rect().size.y],
		"geode_texture": OperaGeologySurface.GEODE_PATH, "surface_script": surface.get_script().resource_path,
		"player_visible": world.player_actor.visible, "player_position": [world.player_actor.position.x,world.player_actor.position.y],
		"qualification": "Native Mobile desktop production render through actual viewport inputs and ordinary phase advancement. Career entry is a supplied fixture; castle/story entrance, physical device and child review not established.",
		"direct_native_review": false, "scores": {}, "owner_acceptance": null})
	for raw_node: Variant in states:
		var node := raw_node as Node
		var state := states[raw_node] as Array
		node.set_process(bool(state[0]))
		node.set_physics_process(bool(state[1]))
	print("GEODE_RUNTIME_CAPTURE|", name, "|", surface.progress(), "|", world.phase_advance_pending)

func _open(world: OperaCareerWorld2D) -> void:
	for tick: int in range(300):
		var candidate := world._active_hotspot()
		if candidate != null and candidate.visible:
			break
		await _wait(1)
	var hot := world._active_hotspot()
	assert(hot != null and hot.visible and not world.task_open)
	await _capture(world, "invitation")
	var at := hot.touch_button.get_global_transform_with_canvas() * (hot.touch_button.size * 0.5)
	await _touch(at, true)
	await _touch(at, false)
	for tick: int in range(360):
		if world.task_open:
			break
		await _wait(1)
	assert(world.task_open)
	await _wait(8)
	await _capture(world, "task_open")
	events.append({"event":"viewport_invitation_arrival_open","phase_index":world.phase_index,"task_open":world.task_open})

func _work(world: OperaCareerWorld2D) -> void:
	var surface := world.surface as OperaGeologySurface
	match surface.mode:
		"geology_river":
			await _surface_touch(surface, surface.river_path_point(0), true)
			for point: int in range(1, OperaGeologySurface.RIVER_PATH.size()):
				await _segment(surface, surface.river_path_point(point - 1), surface.river_path_point(point))
			await _surface_touch(surface, surface.pointer_pos, false)
		"geology_fossil":
			var cell := Vector2(OperaGeologySurface.FOSSIL_RECT.size.x / OperaGeologySurface.FOSSIL_GRID_COLS,
				OperaGeologySurface.FOSSIL_RECT.size.y / OperaGeologySurface.FOSSIL_GRID_ROWS)
			var at := OperaGeologySurface.FOSSIL_RECT.position + cell * 0.5
			await _surface_touch(surface, at, true)
			for row: int in range(OperaGeologySurface.FOSSIL_GRID_ROWS):
				var column := OperaGeologySurface.FOSSIL_GRID_COLS - 1 if row % 2 == 0 else 0
				var next := OperaGeologySurface.FOSSIL_RECT.position + (Vector2(column,row) + Vector2(0.5,0.5)) * cell
				await _segment(surface, at, next)
				at = next
				if row == 0:
					await _capture(world, "partial_brush")
			await _surface_touch(surface, at, false)
			assert(surface.fossil_stage == 1)
			await _capture(world, "brushed")
			for piece: int in range(3):
				await _surface_touch(surface, surface.fossil_piece_home(piece), true)
				await _segment(surface, surface.fossil_piece_home(piece), surface.fossil_piece_target(piece))
				await _surface_touch(surface, surface.fossil_piece_target(piece), false)
				if piece < 2:
					await _capture(world, "one_piece" if piece == 0 else "two_pieces")
		"geology_pan":
			var center := OperaGeologySurface.PAN_RECT.get_center()
			var at := center
			await _surface_touch(surface, at, true)
			for swing: int in range(OperaGeologySurface.PAN_REQUIRED_REVERSALS + 1):
				var direction := 1.0 if swing % 2 == 0 else -1.0
				var next := center + Vector2(direction * 150.0, 0.0)
				await _segment(surface, at, next)
				at = next
				if swing < 2:
					await _capture(world, "pan_right" if swing == 0 else "pan_left")
				if swing == 3:
					await _capture(world, "partial_pan")
			await _surface_touch(surface, at, false)
		"geology_geode":
			await _wait(120)
			assert(is_zero_approx(surface.progress()) and not world.phase_advance_pending)
			events.append({"event":"passive_open_no_progress","phase_index":world.phase_index})
			for seam: int in range(OperaGeologySurface.GEODE_SEAM_SPOTS.size()):
				var at := surface.geode_seam_spot(seam)
				await _surface_touch(surface, at, true)
				await _surface_touch(surface, at, false)
			await _capture(world, "five_seams_ready")
			var at := surface.geode_half_center()
			await _surface_touch(surface, at, true)
			await _segment(surface, at, at + Vector2(25,0))
			await _surface_touch(surface, at + Vector2(25,0), false)
			assert(is_equal_approx(surface.geode_pull,25))
			await _capture(world, "early_crack")
			var saved := surface.progress_snapshot()
			surface.cancel_input()
			surface.configure("geology_geode", Color.WHITE)
			surface.restore_progress(JSON.parse_string(JSON.stringify(saved)) as Dictionary)
			surface.armed_only = false
			assert(is_equal_approx(surface.geode_pull,25) and surface.touch_owner == -1)
			events.append({"event":"released_partial_json_restore25","phase_index":world.phase_index})
			for target: float in [65.0,95.0,120.0]:
				at = surface.geode_half_center()
				var amount := target - surface.geode_pull
				await _surface_touch(surface, at, true)
				await _segment(surface, at, at + Vector2(amount,0))
				await _surface_touch(surface, at + Vector2(amount,0), false)
				assert(is_equal_approx(surface.geode_pull,target))
				if target < 120.0:
					await _capture(world, "middle_open" if target == 65.0 else "full_interior_before_award")
	assert(surface._completion_emitted and world.phase_advance_pending)
	assert(world.player_actor.position.x < 310.0,
		"Celebration actor must remain outside the opaque work panel")
	await _capture(world, "earned_completion")
	events.append({"event":"intentional_completed","phase_index":world.phase_index,"progress":surface.progress()})

func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--width="):
			width_now = arg.trim_prefix("--width=").to_int()
	root.size = Vector2i(width_now,720)
	DisplayServer.window_set_size(root.size)
	assert(DirAccess.make_dir_recursive_absolute(OUT + "native_views/") == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	main.save_data["opera_geology_checkpoint"] = {}
	var config: Dictionary = {}
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume","")) == "geologist":
			config = act.duplicate(true)
	assert(not config.is_empty())
	var competition := OperaCompetition.new()
	competition.configure("geologist")
	var world := OperaCareerWorld2D.new()
	main.add_child(world)
	world.setup(main,config,competition,Callable())
	await _wait(20)
	assert(world.phase_index == 0 and world.phases.size() == 4)
	for phase: int in range(4):
		assert(world.phase_index == phase)
		await _open(world)
		await _work(world)
		if phase < 3:
			for tick: int in range(240):
				if world.phase_index == phase + 1:
					break
				await _wait(1)
			assert(world.phase_index == phase + 1)
			events.append({"event":"ordinary_advance_after_hold","phase_index":world.phase_index})
	var checkpoint: Dictionary = main.save_data.get("opera_geology_checkpoint",{}) as Dictionary
	var file := FileAccess.open(OUT + "CAPTURE_%d.json" % width_now,FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"ORDINARY_FOUR_PHASE_NATIVE_ROUTE_CAPTURED_REVIEW_PENDING",
		"views":records,"events":events,"final_checkpoint":checkpoint,
		"qualification":"Main entry staged in an isolated test save home. Production world/surface/art retained; all phase transitions and work use actual viewport inputs. Not physical device/child/owner or castle/story entry evidence."},"\t"))
	file.close()
	print("GEODE_RUNTIME_ROUTE|ALL4_INTENTIONAL_PHASES|",width_now,"|",records.size(),"|PASS_CAPTURE_REVIEW_PENDING")
	quit(0)
