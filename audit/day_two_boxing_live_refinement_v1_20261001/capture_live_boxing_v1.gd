extends SceneTree
## Current production appearance and actual local touch chronology in all boxing modes.
const OUT := "res://audit/day_two_boxing_live_refinement_v1_20261001/native_actions_v1/"
var main: ReefMain
var world: OperaCareerWorld2D
var surface: OperaBoxingSurface
var actions: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var images: Array[Image] = []
var inputs: Array[Dictionary] = []
var current_hand := 0
func _initialize() -> void:
	_run.call_deferred()
func _wait_frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame
func _run() -> void:
	Engine.max_fps = 60
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait_frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	var saved_stars: int = main.opera_stars
	var config: Dictionary = {}
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume", "")) == "boxer":
			config = act.duplicate(true)
	assert(not config.is_empty())
	for width: int in [1280, 1600]:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		await _wait_frames(6)
		var competition: OperaCompetition = OperaCompetition.new()
		competition.configure("boxer")
		world = OperaCareerWorld2D.new()
		main.add_child(world)
		world.setup(main, config, competition, Callable())
		await _wait_frames(6)
		world.set_process(false)
		for index: int in range(world.phases.size()):
			var mode: String = String(world.phases[index].get("mode", ""))
			assert(mode in OperaBoxingSurface.SUPPORTED_MODES)
			for hand: int in [0, 1]:
				current_hand = hand
				world.phase_index = index
				world.active = true
				world.reveal_t = 0.0
				world.phase_advance_pending = false
				world.phase_gap = 0.0
				world._arm_phase()
				world._open_task()
				await _wait_frames(8)
				await create_timer(0.6).timeout
				surface = world.surface as OperaBoxingSurface
				assert(surface != null)
				assert(surface._puff_texture.resource_path == OperaBoxingSurface.PUFF_PATH)
				assert(surface._left_glove_texture.resource_path == OperaBoxingSurface.LEFT_GLOVE_PATH)
				assert(surface._right_glove_texture.resource_path == OperaBoxingSurface.RIGHT_GLOVE_PATH)
				if mode == "boxing_imp":
					for _opening: int in range(720):
						if surface.imp_is_open():
							break
						await process_frame
					assert(surface.imp_is_open())
				var first: int = frames.size()
				var start: int = Time.get_ticks_usec()
				await _capture(width, mode, start)
				var from: Vector2 = surface.glove_rest_position(hand)
				var target: Vector2 = surface.guide_target_position(hand) if mode == "boxing_guide" else surface.active_target_position()
				_touch(from, true, width, mode)
				assert(int(surface.touch_owners.get(0, -1)) == hand)
				await _capture(width, mode, start)
				for step: int in range(1, 9):
					var drag: InputEventScreenDrag = InputEventScreenDrag.new()
					drag.index = 0
					drag.position = from.lerp(target, float(step) / 8.0)
					surface._gui_input(drag)
					inputs.append({"type":"drag", "width":width, "mode":mode, "hand":hand, "local_xy":[drag.position.x, drag.position.y], "timestamp_us":Time.get_ticks_usec()})
					await _capture(width, mode, start)
				if mode == "boxing_guard":
					for _guard_wait: int in range(300):
						if world.phase_progress > 0.0:
							break
						await _capture(width, mode, start)
				_touch(target, false, width, mode)
				for settle: int in range(120):
					await _capture(width, mode, start)
					if settle >= 20 and surface._impact_t <= 0.0:
						break
				for _final_render: int in range(3):
					await _capture(width, mode, start)
				var expected_hits: int = 0 if mode == "boxing_guard" else 1
				print("BOXING_LIVE_ACTION|"+JSON.stringify({"width":width,"mode":mode,"hand":hand,"hits":surface.landed_punches,"progress":world.phase_progress,"stars":main.opera_stars}))
				assert(surface.landed_punches == expected_hits)
				assert(world.phase_progress == 1.0)
				assert(surface._impact_t <= 0.0 and surface.touch_owners.is_empty())
				assert(main.opera_stars == saved_stars)
				actions.append({"width":width,"mode":mode,"hand":hand,"first_frame":first,"last_frame":frames.size()-1,"landed_punches":surface.landed_punches,"phase_progress":world.phase_progress,"stars_unchanged":main.opera_stars==saved_stars,"qualification":"Actual local press/drag/release production handler on current textures and renderer in explicit catalog phase fixture; ordinary HUD route/root input/device/owner acceptance separate."})
		world.close()
		world.queue_free()
		await _wait_frames(4)
	assert(actions.size() == 20)
	for i: int in range(images.size()):
		var path: String = "frame_%04d.webp" % i
		assert(images[i].save_webp(OUT+path,true) == OK)
		frames[i]["path"] = path
		frames[i]["sha256"] = FileAccess.get_sha256(OUT+path)
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"CURRENT_PRODUCTION_20_LOCAL_HANDLER_ACTIONS","actions":actions,"frames":frames,"inputs":inputs,"stars_unchanged":main.opera_stars==saved_stars},"\t")+"\n")
	file.close()
	main.queue_free()
	await _wait_frames(3)
	print("BOXING_LIVE|PASS|20 all-mode both-hand cases|current source")
	quit(0)
func _touch(at: Vector2, pressed: bool, width: int, mode: String) -> void:
	var touch: InputEventScreenTouch = InputEventScreenTouch.new()
	touch.index = 0
	touch.position = at
	touch.pressed = pressed
	surface._gui_input(touch)
	inputs.append({"type":"down" if pressed else "up","width":width,"mode":mode,"hand":current_hand,"local_xy":[at.x,at.y],"timestamp_us":Time.get_ticks_usec()})
func _capture(width: int, mode: String, start_us: int) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	images.append(root.get_texture().get_image())
	frames.append({"index":frames.size(),"width":width,"mode":mode,"hand":current_hand,"seconds":float(Time.get_ticks_usec()-start_us)/1000000.0,"hits":surface.landed_punches,"progress":world.phase_progress,"impact_time":surface._impact_t,"declared_draw_alpha":surface._impact_t/0.52,"impact_position":[surface._impact_position.x,surface._impact_position.y],"imp_state":surface._imp_state,"glove_positions":[[surface.glove_positions[0].x,surface.glove_positions[0].y],[surface.glove_positions[1].x,surface.glove_positions[1].y]],"touch_owners":surface.touch_owners.duplicate(true),"finished":surface.finished})
