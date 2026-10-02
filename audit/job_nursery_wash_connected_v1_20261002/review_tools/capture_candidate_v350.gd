extends SceneTree
## Unmodified career-room setup, actual viewport touch and natural process/render clocks.
## Main/menu arrival remains fixture setup; no direct task-open or manual controller ticks.
const OUT := "res://audit/job_nursery_wash_connected_v1_20261002/candidate_capture_v1/native_frames/"
var main: ReefMain
var frames: Array[Dictionary] = []
var images: Array[Image] = []
var cases: Array[Dictionary] = []
var failed := false

func _initialize() -> void:
	_run.call_deferred()

func _wait(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _touch(at: Vector2, pressed: bool) -> void:
	var event: InputEventScreenTouch = InputEventScreenTouch.new()
	event.index = 0
	event.pressed = pressed
	event.position = at
	Input.parse_input_event(event)

func _screen_center(control: Control) -> Vector2:
	return control.get_global_transform_with_canvas() * (control.size * 0.5)

func _capture(world: OperaCareerWorld2D, ident: String, tick: int,
		event: String, started: int) -> void:
	await RenderingServer.frame_post_draw
	var pixels: Image = root.get_texture().get_image()
	var measured: int = Time.get_ticks_usec()
	images.append(pixels)
	var actor: OperaRoshanActor = world.player_animator
	var phase: Dictionary = world.phases[world.phase_index]
	frames.append({"path":"%s/%04d.webp" % [ident,tick], "case":ident,
		"capture_index":tick, "capture_ticks_usec":measured,
		"measured_elapsed_seconds":float(measured-started)/1000000.0,
		"event":event, "phase_index":world.phase_index,
		"phase_name":String(phase.get("name","")),
		"phase_progress":world.phase_progress, "task_open":world.task_open,
		"interaction_requested":world.interaction_requested,
		"hotspot_opening":world.hotspot_opening, "wander_walking":world.wander_walking,
		"wander_feet":[world.wander_feet.x,world.wander_feet.y],
		"phase_advance_pending":world.phase_advance_pending,
		"surface_held":world.surface.held,
		"surface_completion":world.surface.completion_accepted,
		"wash_state": (world.surface as OperaNurserySurface).wash_state if world.surface is OperaNurserySurface else "shared_control",
		"player_visible":world.player_actor.visible,
		"player_animation":actor.current_animation, "player_frame":actor.current_frame,
		"player_position":[world.player_actor.position.x,world.player_actor.position.y],
		"player_size":[world.player_actor.size.x,world.player_actor.size.y],
		"viewport":[pixels.get_width(),pixels.get_height()]})

func _flush() -> void:
	assert(frames.size()==images.size())
	for index: int in range(images.size()):
		var path: String = OUT + String(frames[index]["path"])
		assert(DirAccess.make_dir_recursive_absolute(path.get_base_dir())==OK)
		assert(images[index].save_webp(path,true)==OK)
		frames[index]["sha256"] = FileAccess.get_sha256(path)
	images.clear()

func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT)==OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
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
	var original_stars: int = main.opera_stars
	for width: int in [1280,1600]:
		root.size = Vector2i(width,720)
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(root.size)
		await _wait(4)
		for run_mode: String in ["opera_training","birthday_story_catalog"]:
			for career: String in ["doctor","nursery"]:
				var config: Dictionary = {}
				for act: Dictionary in OperaHouse.ACTS:
					if String(act.get("costume",""))==career:
						config = act.duplicate(true)
				assert(not config.is_empty())
				var context: Dictionary = {"chapter":"chapter2"} if run_mode=="birthday_story_catalog" else {}
				var competition: OperaCompetition = OperaCompetition.new()
				competition.configure(career)
				var world: OperaCareerWorld2D = OperaCareerWorld2D.new()
				main.add_child(world)
				world.setup(main,config,competition,Callable(),[],{},context)
				await _wait(38)
				var ident: String = "%s_%s_%d" % [run_mode,career,width]
				var first: int = frames.size()
				var started: int = Time.get_ticks_usec()
				var opened: int = -1
				var accepted: int = -1
				var advanced: int = -1
				var press_sent := false
				var wash_pressed := false
				var nav_point := Vector2.ZERO
				var wash_point := Vector2.ZERO
				var passive_ok := true
				var local_frames: Array[Dictionary] = []
				for tick: int in range(720):
					var event := "natural_passive"
					if tick<15 and (world.phase_progress>0.0 or world.task_open):
						passive_ok = false
					if tick==15 and world.armed_station>=0:
						var hotspot: OperaWorldHotspot2D = world.station_nodes[world.armed_station] as OperaWorldHotspot2D
						nav_point = _screen_center(hotspot.touch_button)
						_touch(nav_point,true)
						press_sent = true
						event = "viewport_hotspot_press"
					elif tick==16 and press_sent:
						_touch(nav_point,false)
						event = "viewport_hotspot_release"
					if world.task_open and opened<0:
						opened = tick
						event = "actual_task_opened_after_route"
					if opened>=0 and tick==opened+15:
						wash_point = _screen_center(world.surface)
						_touch(wash_point,true)
						wash_pressed = true
						event = "viewport_wash_press"
					if world.phase_advance_pending and accepted<0:
						accepted = tick
						event = "first_earned_completion"
					elif accepted>=0 and tick==accepted+1 and wash_pressed:
						_touch(wash_point,false)
						wash_pressed = false
						event = "viewport_wash_release"
					if world.phase_index>0 and advanced<0:
						advanced = tick
						event = "actual_next_phase_armed"
					await _capture(world,ident,tick,event,started)
					if advanced>=0 and tick>=advanced+12:
						break
					if tick>=360 and opened<0:
						break
					await process_frame
				if wash_pressed:
					_touch(wash_point,false)
				var stars_ok: bool = main.opera_stars==original_stars
				var case_ok: bool = passive_ok and stars_ok and opened>15 and accepted>opened and advanced>accepted
				if not case_ok:
					failed = true
				print("WASH_ROOT_ROUTE|",ident,"|", "PASS" if case_ok else "FAIL", "|opened=",opened,"|accepted=",accepted,"|next=",advanced)
				world.set_process(false)
				world.surface.set_process(false)
				world.player_animator.set_process(false)
				# Freeze scene before disk encoding. Encoding is outside recorded timing.
				for index: int in range(first,frames.size()):
					local_frames.append(frames[index])
				cases.append({"id":ident,"status":"PASS_ROUTE_INPUT_PROCESS" if case_ok else "FAIL_PRESERVED", "first_record":first,"frame_count":frames.size()-first,"opened_frame":opened,"accepted_frame":accepted,"advanced_frame":advanced,"passive_start_ok":passive_ok,"stars_unchanged":stars_ok,"hotspot_viewport_point":[nav_point.x,nav_point.y],"wash_viewport_point":[wash_point.x,wash_point.y],"using_chapter_two_phases":world.using_chapter_two_phases,"phase_names":world.phases.map(func(p: Dictionary)->String:return String(p.get("name","")))})
				# Flush only this case, retaining the whole ordered metadata library.
				var all_records: Array[Dictionary] = frames
				frames = local_frames
				_flush()
				frames = all_records
				world.close()
				world.queue_free()
				await _wait(4)
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"FAIL_PRESERVED" if failed else "PASS_EIGHT_NATIVE_ROOM_ROUTES", "cases":cases,"frames":frames,"qualification":"Actual viewport Input.parse_input_event for physical hotspot and wash hold; production route, opening callback, natural clocks and measured render timestamps. Images buffered per case, encoding after freezing the scene. Main/menu/room arrival remains a fixture; no ordinary full menu/story route, target-device, child, owner, complete visual or cinematic acceptance."},"\t")+"\n")
	file.close()
	main.queue_free()
	await _wait(3)
	quit(1 if failed else 0)
