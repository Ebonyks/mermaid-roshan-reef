extends SceneTree
## Bounded fresh-profile entry observation. No progress setters or callbacks.
const OUT := "res://assets_src/review/fashion_walkthrough_20261007/native/"
var events: Array[Dictionary] = []

func _initialize() -> void:
	call_deferred("_run")

func _shot(id: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var pixels: Image = root.get_texture().get_image()
	pixels.save_png(OUT + id + ".png")
	print("NATURAL_FASHION|CAPTURE|", id)

func _tap(button: Button) -> void:
	var point: Vector2 = button.get_global_rect().get_center()
	events.append({"target": String(button.name), "rect": str(button.get_global_rect()), "point": str(point), "ms": Time.get_ticks_msec(), "input": "InputEventMouseMotion + InputEventMouseButton press/release"})
	var motion := InputEventMouseMotion.new()
	motion.position = point
	Input.parse_input_event(motion)
	await process_frame
	var down := InputEventMouseButton.new()
	down.button_index = MOUSE_BUTTON_LEFT
	down.position = point
	down.pressed = true
	Input.parse_input_event(down)
	await create_timer(0.15).timeout
	var up := InputEventMouseButton.new()
	up.button_index = MOUSE_BUTTON_LEFT
	up.position = point
	up.pressed = false
	Input.parse_input_event(up)
	await process_frame

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1280, 720)
	var main: ReefMain = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	current_scene = main
	await create_timer(4.0).timeout
	await _shot("11-fresh-launch")
	var button: Button = root.find_child("StartMenuNewGameButton", true, false) as Button
	if button != null and button.is_visible_in_tree() and not button.disabled:
		await _tap(button)
		await create_timer(3.0).timeout
		await _shot("12-new-game-input")
		await create_timer(32.0).timeout
		await _shot("13-after-opening")
	var live: ReefMain = current_scene as ReefMain
	var observation: Dictionary = {"events": events, "user_data_dir": OS.get_user_data_dir(), "engine": Engine.get_version_info(), "renderer": RenderingServer.get_current_rendering_method(), "has_saved_game": live.has_saved_game if live != null else null, "day_one_active": live.day_one_active if live != null else null, "castle_room_id": live.castle_room_id if live != null else null, "route_limit": "Bounded fresh-profile observation only; no Fashion entry or Chapter 2 completion manufactured."}
	var file: FileAccess = FileAccess.open(OUT + "natural_input_observation.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(observation, "\t") + "\n")
	print("NATURAL_FASHION|RESULT|OBSERVED_ENTRY_ONLY")
	quit()
