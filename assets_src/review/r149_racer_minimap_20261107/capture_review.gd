extends SceneTree
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const PCScene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const World := preload("res://scripts/opera_career_world_2d.gd")
var rows: Array[Dictionary] = []
var failures := 0
var dest := ""
var variant := ""
var width := 1280
var quality_context := "speedy"
var surface: OperaRacerSurface = null
func _initialize() -> void:
	call_deferred("_run")
func check(label: String, ok: bool) -> void:
	print("R149_CAPTURE|", "PASS" if ok else "FAIL", "|", label)
	if not ok:
		failures += 1
func _run() -> void:
	dest = OS.get_environment("R149_CAPTURE_DEST")
	variant = OS.get_environment("R149_CAPTURE_VARIANT")
	width = int(OS.get_environment("R149_CAPTURE_WIDTH"))
	assert(not dest.is_empty() and variant in ["source", "candidate"] and width in [1280, 1600])
	var version: Dictionary = Engine.get_version_info()
	assert(int(version["major"]) == 4 and int(version["minor"]) == 7 and int(version["patch"]) == 2)
	assert(RenderingServer.get_current_rendering_method() == "mobile")
	assert(DisplayServer.get_name() == "Windows")
	Engine.max_fps = 30
	root.size = Vector2i(width, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_EXPAND
	await process_frame
	await process_frame
	seed(149)
	var host := World.new()
	host.set_process(false)
	root.add_child(host)
	host.set_process(false)
	check("incomplete diagnostic host processing stays disabled", not host.is_processing())
	host.root = Control.new()
	host.root.size = Vector2(1280, 720)
	host.add_child(host.root)
	host._sync_root_scale()
	check("production world fit helper owns the fixed1280 canvas", host.root.size == Vector2(1280, 720))
	surface = OperaRacerSurface.new()
	host.root.add_child(surface)
	surface.size = Vector2(1280, 720)
	surface.configure("kart_race", Color.WHITE)
	surface.set_process(false)
	surface.quality = "speedy"
	surface._notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	check("Opera map geometry", surface._engine._minimap_rect == Rect2(1090, 18, 170, 170))
	await shot("opera-grid", [map_snapshot(surface._engine)])
	var engine: ReefKartRace = surface._engine
	surface.race_started = true
	engine.state = "race"
	var initial: Vector2 = engine._pl["pos"]
	var event := InputEventScreenTouch.new()
	event.index = 73
	event.pressed = true
	event.position = OperaRacerSurface.GAS_CENTER
	surface._gui_input(event)
	for index in range(60):
		surface._tick_driving(1.0 / 60.0)
	event.pressed = false
	surface._gui_input(event)
	check("real gas owner and game step move the live map marker", (engine._pl["pos"] as Vector2).distance_to(initial) > 1.0)
	await shot("opera-moving", [map_snapshot(engine)])
	host.queue_free()
	await process_frame
	surface = null
	quality_context = "fixed_pc_no_quality_selector"
	for course in range(4):
		for count in [1, 2]:
			seed(149)
			var pc := PCScene.instantiate() as PC
			root.add_child(pc)
			pc.set_physics_process(false)
			pc._show_garage(count, -1 if count == 1 else 6)
			if count == 2:
				pc._join(11)
			pc._toggle_ready(0)
			if count == 2:
				pc._toggle_ready(1)
			pc._choose_course(course)
			pc._start_race()
			check("PC base map geometry", pc._race._minimap_rect.size == Vector2(86,86) and pc._race._pc_hud)
			var maps: Array[Dictionary] = [map_snapshot(pc._race)]
			if count == 2:
				check("independent second pane map", is_instance_valid(pc._second_view) and pc._second_view._minimap_rect.size == Vector2(86,86))
				maps.append(map_snapshot(pc._second_view))
			await shot("pc-course-%d-panes-%d" % [course, count], maps)
			pc.queue_free()
			await process_frame
	var output := FileAccess.open(dest + "/captures.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"variant":variant, "width":width, "records":rows, "failures":failures, "renderer":RenderingServer.get_current_rendering_method(), "version":version, "frame_cap":Engine.max_fps, "source_script_sha256":FileAccess.get_sha256("res://scripts/racer/reef_kart_race.gd"), "limits":"Configured real Opera and PC surfaces, production views and source-bound map geometry. Physical controls, natural routes, formal QA11, device, child and owner review are separate."}, "\t") + "\n")
	print("R149_CAPTURE|DONE|frames=", rows.size(), "|failures=", failures)
	quit(1 if failures else 0)

func map_snapshot(view: ReefKartRace) -> Dictionary:
	var local: Rect2 = view._minimap_rect.grow(10.0)
	var transform: Transform2D = view._hud.get_global_transform_with_canvas()
	if view._pc_hud:
		var viewport := view.get_viewport() as SubViewport
		var screen := viewport.get_parent() as SubViewportContainer
		transform = screen.get_global_transform_with_canvas() * transform
	var start: Vector2 = transform * local.position
	var end: Vector2 = transform * local.end
	var markers: Array = []
	for kart: Dictionary in view.karts:
		var at: Vector2 = view._minimap_rect.position + (kart["pos"] as Vector2) * view._minimap_rect.size.x / view.track.world_size
		markers.append([at.x,at.y,bool(kart["player"])])
	return {"backing_bounds":[start.x,start.y,end.x,end.y], "route_hash":JSON.stringify(view._minimap).sha256_text(), "markers":markers, "PC":view._pc_hud}

func shot(label: String, maps: Array[Dictionary]) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var picture := root.get_texture().get_image()
	check("native window size " + label, picture.get_size() == Vector2i(width,720))
	var file := dest + "/" + label + ".png"
	var error := picture.save_png(file)
	check("native bytes saved " + label, error == OK)
	rows.append({"file":label+".png","size":[picture.get_width(),picture.get_height()],"sha256":FileAccess.get_sha256(file),"quality_context":quality_context,
		"target_visible":true,"target_state":{"maps":maps},"variant":variant,"renderer":RenderingServer.get_current_rendering_method(),"formal_QA11":false})
