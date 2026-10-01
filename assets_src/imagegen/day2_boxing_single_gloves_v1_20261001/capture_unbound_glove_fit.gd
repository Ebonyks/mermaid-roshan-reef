extends SceneTree
## Explicit static catalog-phase fixture. Diagnostic subclass changes glove pixels only.
const BASE := "res://assets_src/imagegen/day2_boxing_single_gloves_v1_20261001/"
const OUT := BASE + "native_static_fit_v1/"
const REVIEW_SURFACE := preload(BASE + "unbound_glove_surface.gd")
var main: ReefMain
var records: Array[Dictionary] = []
func _initialize() -> void:
	_run.call_deferred()
func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame
func _candidate(name: String) -> Texture2D:
	var image: Image = Image.load_from_file(BASE + name)
	assert(image != null and image.get_size() == Vector2i(1024,1024))
	return ImageTexture.create_from_image(image)
func _run() -> void:
	Engine.max_fps = 60
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
		var world: OperaCareerWorld2D = OperaCareerWorld2D.new()
		main.add_child(world)
		world.setup(main, config, competition, Callable())
		await _frames(6)
		world.set_process(false)
		var original: OperaBoxingSurface = world.surface as OperaBoxingSurface
		assert(original != null)
		for index: int in range(world.phases.size()):
			var mode_name: String = String(world.phases[index].get("mode",""))
			if mode_name not in ["boxing_jab","boxing_imp"]:
				continue
			for treatment: String in ["procedural","painted"]:
				var active_surface: OperaBoxingSurface = original
				if treatment == "painted":
					var painted: OperaBoxingSurface = REVIEW_SURFACE.new() as OperaBoxingSurface
					painted.name = "UnboundPaintedGloveSurface"
					painted.position = original.position
					painted.size = original.size
					painted.bop_texture = original.bop_texture
					painted.bop_captain_texture = original.bop_captain_texture
					painted.set("review_left",_candidate("left_whole_canvas_1024.png"))
					painted.set("review_right",_candidate("right_whole_canvas_1024.png"))
					painted.gesture.connect(Callable(world,"_on_gesture"))
					world.action_panel.add_child(painted)
					original.visible = false
					original.set_process(false)
					original.mouse_filter = Control.MOUSE_FILTER_IGNORE
					world.surface = painted
					active_surface = painted
				world.phase_index = index
				world.active = true
				world.reveal_t = 0.0
				world.phase_advance_pending = false
				world.phase_gap = 0.0
				world._arm_phase()
				world._open_task()
				await _frames(8)
				await create_timer(0.65).timeout
				active_surface.set_process(false)
				active_surface.demo_active = false
				active_surface._puff_texture = load("res://assets/opera/worlds/props/fx_dust_puff.png") as Texture2D
				for pose: String in ["idle","left_contact","right_contact"]:
					active_surface.glove_positions[0] = active_surface.glove_rest_position(0)
					active_surface.glove_positions[1] = active_surface.glove_rest_position(1)
					active_surface._impact_t = 0.0
					if pose != "idle":
						var hand: int = 0 if pose == "left_contact" else 1
						active_surface.glove_positions[hand] = active_surface.active_target_position()
						active_surface._impact_position = active_surface.active_target_position()
						active_surface._impact_t = 0.42
					active_surface.queue_redraw()
					await _frames(4)
					await RenderingServer.frame_post_draw
					var image: Image = root.get_texture().get_image()
					var name: String = "%d_%s_%s_%s.webp" % [width,mode_name,treatment,pose]
					assert(image.save_webp(OUT+name,true) == OK)
					records.append({"path":name,"sha256":FileAccess.get_sha256(OUT+name),"viewport":[image.get_width(),image.get_height()],"mode":mode_name,"treatment":treatment,"pose":pose,"landed_punches":active_surface.landed_punches,"phase_progress":world.phase_progress,"stars":main.opera_stars,"glove_positions":[[active_surface.glove_positions[0].x,active_surface.glove_positions[0].y],[active_surface.glove_positions[1].x,active_surface.glove_positions[1].y]],"left_source":BASE+"left_whole_canvas_1024.png" if treatment=="painted" else "scripts/opera_boxing_surface.gd::_draw_glove","right_source":BASE+"right_whole_canvas_1024.png" if treatment=="painted" else "scripts/opera_boxing_surface.gd::_draw_glove","qualification":"Static actual career room and inherited production boxing renderer with appearance-only unbound diagnostic subclass. Contact positions/effect are explicitly staged, not played input or chronology. No progression/device/owner acceptance."})
					assert(active_surface.landed_punches == 0 and world.phase_progress == 0.0 and main.opera_stars == saved_stars)
				if treatment == "painted":
					world.surface = original
					active_surface.queue_free()
					original.visible = true
					original.mouse_filter = Control.MOUSE_FILTER_STOP
					await _frames(3)
		world.close()
		world.queue_free()
		await _frames(4)
	assert(records.size() == 24)
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"UNBOUND_24_STATIC_PAIR_CONTACT_COMPARISONS","views":records,"gameplay_progress_unchanged":main.opera_stars==saved_stars},"\t")+"\n")
	file.close()
	main.queue_free()
	await _frames(3)
	print("BOXING_GLOVE_STATIC|PASS|24 complete views|zero hit/phase/star awards")
	quit(0)
