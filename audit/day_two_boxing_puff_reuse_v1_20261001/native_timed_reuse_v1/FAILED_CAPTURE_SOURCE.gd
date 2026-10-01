extends SceneTree
## Exact production boxing static impact fixture. No glove input or progress.
const OUT := "res://audit/day_two_boxing_puff_reuse_v1_20261001/native_timed_reuse_v1/"
const CLEAN := "res://assets/opera/worlds/props/fx_dust_puff.png"
var main: ReefMain
var records: Array[Dictionary] = []
var timed_actions: Array[Dictionary] = []
var input_records: Array[Dictionary] = []
var frame_images: Array[Image] = []
var frame_states: Array[Dictionary] = []
var surface: OperaBoxingSurface
var world: OperaCareerWorld2D
func _initialize() -> void:
	_run.call_deferred()
func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame
func _run() -> void:
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	main.set_physics_process(false)
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.player != null:
		main.player.visible = false
	var saved_stars: int = main.opera_stars
	var config: Dictionary = {}
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume", "")) == "boxer":
			config = act.duplicate(true)
	assert(not config.is_empty())
	for width: int in [1280,1600]:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		root.size = Vector2i(width,720)
		DisplayServer.window_set_size(root.size)
		await _frames(6)
		var competition: OperaCompetition = OperaCompetition.new()
		competition.configure("boxer")
		world = OperaCareerWorld2D.new()
		main.add_child(world)
		world.setup(main, config, competition, Callable())
		assert(world.root != null)
		await _frames(6)
		world.set_process(false)
		for index: int in range(world.phases.size()):
			var mode: String = String(world.phases[index].get("mode",""))
			if mode not in ["boxing_jab", "boxing_imp"]:
				continue
			world.phase_index = index
			world.active = true
			world.reveal_t = 0.0
			world.phase_advance_pending = false
			world.phase_gap = 0.0
			world._arm_phase()
			world._open_task()
			await _frames(8)
			await create_timer(0.6).timeout
			surface = world.surface as OperaBoxingSurface
			assert(surface != null)
			var original: Texture2D = surface._puff_texture
			assert(original.resource_path == OperaBoxingSurface.PUFF_PATH)
			surface._puff_texture = load(CLEAN) as Texture2D
			# Let the unchanged imp reach its actual open recovery window.
			if mode == "boxing_imp":
				for _wait: int in range(720):
					if surface.imp_is_open():
						break
					await process_frame
				assert(surface.imp_is_open())
			var start_frame: int = frame_states.size()
			var start_us: int = Time.get_ticks_usec()
			await _capture_timed(width,mode,start_us)
			var from: Vector2 = surface.glove_rest_position(0)
			var target: Vector2 = surface.active_target_position()
			_send_touch(from,true,width,mode)
			await _capture_timed(width,mode,start_us)
			for step: int in range(1,9):
				var drag: InputEventScreenDrag = InputEventScreenDrag.new()
				drag.index = 0
				drag.position = surface.get_global_transform_with_canvas()*from.lerp(target,float(step)/8.0)
				root.push_input(drag,true)
				input_records.append({"mode":mode,"width":width,"type":"drag","viewport":[drag.position.x,drag.position.y],"local_fraction":float(step)/8.0,"timestamp_us":Time.get_ticks_usec()})
				await _capture_timed(width,mode,start_us)
			_send_touch(target,false,width,mode)
			for _settle: int in range(45):
				await _capture_timed(width,mode,start_us)
			assert(surface.landed_punches == 1 and world.phase_progress > 0.0)
			assert(surface._impact_t <= 0.0 and main.opera_stars == saved_stars)
			timed_actions.append({"width":width,"mode":mode,"first_frame":start_frame,"last_frame":frame_states.size()-1,"landed_punches":surface.landed_punches,"phase_progress":world.phase_progress,"impact_settled":surface._impact_t<=0.0,"source":CLEAN,"source_sha256":FileAccess.get_sha256(CLEAN),"qualification":"Actual viewport touch/drag/release on unchanged production surface from an explicit catalog phase fixture. Only puff texture overridden. No ordinary HUD route, device or owner pass."})
			surface._puff_texture = original
		world.close()
		world.queue_free()
		await _frames(4)
	assert(timed_actions.size()==4)
	for index: int in range(frame_images.size()):
		var path: String = "frame_%04d.webp" % index
		assert(frame_images[index].save_webp(OUT+path,true)==OK)
		frame_states[index]["path"] = path
		frame_states[index]["sha256"] = FileAccess.get_sha256(OUT+path)
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"UNBOUND_TIMED_REAL_VIEWPORT_REQUESTS","actions":timed_actions,"frames":frame_states,"inputs":input_records,"gameplay_progress_unchanged":main.opera_stars==saved_stars},"\t")+"\n")
	file.close()
	main.queue_free()
	await _frames(3)
	print("BOXING_PUFF_TIMED|PASS|4 local one-punch actions|stars unchanged")
	quit(0)

func _send_touch(local: Vector2,pressed: bool,width: int,mode: String) -> void:
	var touch: InputEventScreenTouch = InputEventScreenTouch.new()
	touch.index = 0
	touch.position = surface.get_global_transform_with_canvas()*local
	touch.pressed = pressed
	root.push_input(touch,true)
	input_records.append({"mode":mode,"width":width,"type":"down" if pressed else "up","viewport":[touch.position.x,touch.position.y],"timestamp_us":Time.get_ticks_usec()})
func _capture_timed(width: int,mode: String,start_us: int) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	frame_images.append(root.get_texture().get_image())
	frame_states.append({"index":frame_states.size(),"width":width,"mode":mode,"seconds":float(Time.get_ticks_usec()-start_us)/1000000.0,"landed_punches":surface.landed_punches,"phase_progress":world.phase_progress,"impact_time":surface._impact_t,"impact_position":[surface._impact_position.x,surface._impact_position.y],"imp_state":surface._imp_state,"touch_owners":surface.touch_owners.duplicate(true),"source":surface._puff_texture.resource_path,"source_sha256":FileAccess.get_sha256(surface._puff_texture.resource_path)})
