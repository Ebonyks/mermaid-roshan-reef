extends SceneTree
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const PCScene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const World := preload("res://scripts/opera_career_world_2d.gd")
var rows: Array[Dictionary] = []
var recovery_signals := 0
var failures := 0
var dest := ""
var variant := ""
var width := 1280
var surface: OperaRacerSurface = null
func _initialize() -> void:
	call_deferred("_run")
func check(label: String, ok: bool) -> void:
	print("R150_CAPTURE|", "PASS" if ok else "FAIL", "|", label)
	if not ok:
		failures += 1
func _run() -> void:
	dest = OS.get_environment("R150_CAPTURE_DEST")
	variant = OS.get_environment("R150_CAPTURE_VARIANT")
	width = int(OS.get_environment("R150_CAPTURE_WIDTH"))
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
	seed(150)
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
	var engine: ReefKartRace = surface._engine
	check("Opera uses the production touch HUD at Speedy", not engine._pc_hud and surface.quality == "speedy")
	surface.race_started = true
	engine.state = "race"
	var initial: Vector2 = engine._pl["pos"]
	var gas := InputEventScreenTouch.new()
	gas.index = 73
	gas.pressed = true
	gas.position = OperaRacerSurface.GAS_CENTER
	surface._gui_input(gas)
	for index in range(60):
		surface._tick_driving(1.0 / 60.0)
	gas.pressed = false
	surface._gui_input(gas)
	check("one-finger gas moves the kart", (engine._pl["pos"] as Vector2).distance_to(initial) > 1.0)
	engine.race_event.connect(_on_race_event)
	var course_heading := engine.track.heading_at(float(engine._pl["track_s"]))
	var reference_time := engine._time
	for side: int in [-1, 1]:
		engine._pl["heading"] = course_heading
		engine._player_steer(engine._pl, 0.0, 0.0)
		check("correct heading clears recovery state", not bool(engine._pl["wrong_way"]))
		engine._pl["heading"] = wrapf(course_heading - float(side) * 2.4, -PI, PI)
		var correction := engine._player_steer(engine._pl, 0.0, 0.0)
		check("real heading classifier and steering sign", bool(engine._pl["wrong_way"]) and is_equal_approx(correction, float(side)))
		for phase: int in [0, 1]:
			engine._time = reference_time + float(phase) * PI / 8.0
			engine._hud.queue_redraw()
			var center := Vector2(640.0 + float(side) * (60.0 + sin(engine._time * 8.0) * 10.0), 190.0)
			var transform := engine._hud.get_global_transform_with_canvas()
			var left := -63.0 if side > 0 else -73.0
			var right := 73.0 if side > 0 else 63.0
			var corner := transform * (center + Vector2(left, -53.0))
			var end := transform * (center + Vector2(right, 53.0))
			var tip := transform * (center + Vector2(float(side) * 70.0, 0.0))
			await shot("opera-%s-%d" % ["left" if side < 0 else "right", phase], {
				"visible":true,"side":side,"phase":phase,"heading":engine._pl["heading"],"correction":correction,
				"bounds":[corner.x,corner.y,end.x,end.y],"tip":[tip.x,tip.y],"quality":"speedy","signal_count":recovery_signals})
	check("two distinct wrong-way signals, one per entry", recovery_signals == 2)
	engine._pl["heading"] = course_heading
	engine._player_steer(engine._pl, 0.0, 0.0)
	engine._time = reference_time
	engine._hud.queue_redraw()
	check("cue clears on alignment", not bool(engine._pl["wrong_way"]))
	await shot("opera-recovered", {"visible":false,"heading":engine._pl["heading"],"quality":"speedy","signal_count":recovery_signals})
	host.queue_free()
	await process_frame
	surface = null

	seed(150)
	var pc := PCScene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	pc._show_garage(2, 6)
	pc._join(11)
	pc._toggle_ready(0)
	pc._toggle_ready(1)
	pc._choose_course(0)
	pc._start_race()
	check("both actual PC views use their dedicated HUD", pc._race._pc_hud and is_instance_valid(pc._second_view) and pc._second_view._pc_hud)
	pc._race._pl["wrong_way"] = true
	pc._second_view._pl["wrong_way"] = true
	pc._race._hud.queue_redraw()
	pc._second_view._hud.queue_redraw()
	await shot("pc-split-flag-excluded", {"visible":false,"wrong_way_flags":[true,true],"quality":"fixed_pc_no_quality_selector"})
	pc.queue_free()
	await process_frame
	var output := FileAccess.open(dest + "/captures.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"variant":variant, "width":width, "records":rows, "failures":failures, "renderer":RenderingServer.get_current_rendering_method(), "version":version, "frame_cap":Engine.max_fps, "source_script_sha256":FileAccess.get_sha256("res://scripts/racer/reef_kart_race.gd"), "limits":"Configured production Opera touch and PC split surfaces. Direct heading setup then the real heading classifier, cue draw and steering sign. Exact in-scene diagnostics. Physical controls, natural routes, formal QA11, device, child and owner review are separate."}, "\t") + "\n")
	print("R150_CAPTURE|DONE|frames=", rows.size(), "|failures=", failures)
	quit(1 if failures else 0)

func _on_race_event(moment: String, _value: float) -> void:
	if moment == "wrong_way":
		recovery_signals += 1

func shot(label: String, target: Dictionary) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var picture := root.get_texture().get_image()
	check("native window size " + label, picture.get_size() == Vector2i(width,720))
	var file := dest + "/" + label + ".png"
	var error := picture.save_png(file)
	check("native bytes saved " + label, error == OK)
	rows.append({"file":label+".png","size":[picture.get_width(),picture.get_height()],"sha256":FileAccess.get_sha256(file),"quality_context":target["quality"],
		"target_visible":target["visible"],"target_state":target,"variant":variant,"renderer":RenderingServer.get_current_rendering_method(),"formal_QA11":false})
