extends SceneTree
## Exact production boxing static impact fixture. No glove input or progress.
const OUT := "res://audit/day_two_boxing_puff_reuse_v1_20261001/native_context_v1/"
const CLEAN := "res://assets/opera/worlds/props/fx_dust_puff.png"
var main: ReefMain
var records: Array[Dictionary] = []
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
		var world: OperaCareerWorld2D = OperaCareerWorld2D.new()
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
			var surface: OperaBoxingSurface = world.surface as OperaBoxingSurface
			assert(surface != null)
			surface.set_process(false)
			var original: Texture2D = surface._puff_texture
			assert(original.resource_path == OperaBoxingSurface.PUFF_PATH)
			for entry: Dictionary in [{"name":"original","texture":original},{"name":"clean_reuse","texture":load(CLEAN)}]:
				surface._puff_texture = entry["texture"] as Texture2D
				surface._impact_t = 0.42
				surface._impact_position = surface.active_target_position()
				surface.demo_active = false
				surface.queue_redraw()
				await _frames(3)
				await RenderingServer.frame_post_draw
				var image: Image = root.get_texture().get_image()
				var name: String = "%d_%s_%s.webp" % [width,mode,entry["name"]]
				assert(image.save_webp(OUT+name,true)==OK)
				records.append({"path":name,"sha256":FileAccess.get_sha256(OUT+name),"viewport":[image.get_width(),image.get_height()],"mode":mode,"source":surface._puff_texture.resource_path,"source_sha256":FileAccess.get_sha256(surface._puff_texture.resource_path),"impact_time":surface._impact_t,"impact_position":[surface._impact_position.x,surface._impact_position.y],"landed_punches":surface.landed_punches,"phase_progress":world.phase_progress,"opera_stars":main.opera_stars,"source_original_restored_after_capture":true,"qualification":"Actual production scene/surface/draw path, static impact fixture at0.42s. One texture overridden for exact reuse comparison. No input, real contact, acted/timed sequence or ordinary navigation claimed."})
				assert(main.opera_stars==saved_stars and surface.landed_punches==0 and world.phase_progress==0.0)
			surface._puff_texture = original
		world.close()
		world.queue_free()
		await _frames(4)
	assert(records.size()==8)
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"EIGHT_UNBOUND_STATIC_IMPACT_VIEWS","views":records,"gameplay_progress_unchanged":main.opera_stars==saved_stars},"\t")+"\n")
	file.close()
	main.queue_free()
	await _frames(3)
	print("BOXING_PUFF_STATIC|PASS|8 views|no progress awards")
	quit(0)
