extends SceneTree
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const PCScene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const World := preload("res://scripts/opera_career_world_2d.gd")
var rows: Array[Dictionary] = []
var countdown_events: Array[float] = []
var go_events := 0
var restart_events := 0
var failures := 0
var dest := ""
var variant := ""
var width := 1280
var surface: OperaRacerSurface = null
func _initialize() -> void:
	call_deferred("_run")
func check(label: String, ok: bool) -> void:
	print("R151_CAPTURE|", "PASS" if ok else "FAIL", "|", label)
	if not ok:
		failures += 1
func _run() -> void:
	dest = OS.get_environment("R151_CAPTURE_DEST")
	variant = OS.get_environment("R151_CAPTURE_VARIANT")
	width = int(OS.get_environment("R151_CAPTURE_WIDTH"))
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
	seed(151)
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
	engine.race_event.connect(_on_race_event)
	check("pre-touch grid", engine.state == "grid" and not surface.race_started)
	var spawn: Vector2 = engine._pl["pos"]
	await shot("opera-grid", countdown_snapshot(engine, 0, "speedy"))

	var gas := InputEventScreenTouch.new()
	gas.index = 73
	gas.pressed = true
	gas.position = OperaRacerSurface.GAS_CENTER
	surface._gui_input(gas)
	check("deliberate gas touch owns start", surface.race_started and surface.race_gas_held and engine.state == "countdown")
	surface._tick_driving(0.0)
	surface._publish_controls()
	await shot("opera-initial-1", countdown_snapshot(engine, 1, "speedy"))
	step_surface(45)
	await shot("opera-initial-2", countdown_snapshot(engine, 2, "speedy"))
	step_surface(30)
	await shot("opera-initial-3", countdown_snapshot(engine, 3, "speedy"))
	check("kart stays at grid through countdown", engine._pl["pos"] == spawn)
	step_surface(17)
	await shot("opera-initial-go", countdown_snapshot(engine, 0, "speedy"))
	check("original GO and marks run once", engine.state == "race" and engine.go_t > 0.0 and go_events == 1 and countdown_events == [1.0, 2.0, 3.0])
	gas.pressed = false
	surface._gui_input(gas)
	surface._publish_controls()

	engine.state = "imp_beat"
	engine.clock = 0.0
	engine.go_t = 0.0
	surface._tick_driving(0.0)
	check("real restart branch from configured rival-win endpoint", engine.state == "countdown" and restart_events == 1)
	await shot("opera-retry-1", countdown_snapshot(engine, 1, "speedy"))
	step_surface(45)
	await shot("opera-retry-2", countdown_snapshot(engine, 2, "speedy"))
	step_surface(30)
	await shot("opera-retry-3", countdown_snapshot(engine, 3, "speedy"))
	step_surface(17)
	await shot("opera-retry-go", countdown_snapshot(engine, 0, "speedy"))
	check("retry ends once with identical marks", engine.state == "race" and engine.go_t > 0.0 and go_events == 2 and countdown_events == [1.0, 2.0, 3.0, 1.0, 2.0, 3.0])
	host.queue_free()
	await process_frame
	surface = null

	seed(151)
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
	pc._race.state = "countdown"
	pc._race.clock = 0.25
	pc._second_view.state = "countdown"
	pc._second_view.clock = 0.25
	pc._race._hud.queue_redraw()
	pc._second_view._hud.queue_redraw()
	await shot("pc-split-countdown-excluded", countdown_snapshot(pc._race, 0, "fixed_pc_no_quality_selector"))
	pc.queue_free()
	await process_frame
	var output := FileAccess.open(dest + "/captures.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"variant":variant, "width":width, "records":rows, "failures":failures, "renderer":RenderingServer.get_current_rendering_method(), "version":version, "frame_cap":Engine.max_fps, "source_script_sha256":FileAccess.get_sha256("res://scripts/racer/reef_kart_race.gd"), "limits":"Configured production Opera touch and PC split surfaces. Real input starts the timed sequence. Configured rival-win endpoint invokes the actual retry transition. PC exclusion is a sibling negative. Physical controls, natural routes, formal QA11, device, child and owner review are separate."}, "\t") + "\n")
	print("R151_CAPTURE|DONE|frames=", rows.size(), "|failures=", failures)
	quit(1 if failures else 0)

func step_surface(steps: int) -> void:
	for index in range(steps):
		surface._tick_driving(1.0 / 60.0)

func _on_race_event(moment: String, value: float) -> void:
	match moment:
		"countdown":
			countdown_events.append(value)
		"go":
			go_events += 1
		"restart":
			restart_events += 1

func countdown_snapshot(engine: ReefKartRace, expected: int, quality: String) -> Dictionary:
	var active := engine.state == "countdown" and not engine._pc_hud
	var lit := 0
	var boxes: Array = []
	if active:
		var transform := engine._hud.get_global_transform_with_canvas()
		for index in range(3):
			if engine.clock <= ReefKartRace.COUNTDOWN - float(index) * 0.5:
				lit += 1
			var center := Vector2(550.0 + float(index) * 90.0, 200.0)
			var start := transform * (center - Vector2(30.0, 30.0))
			var end := transform * (center + Vector2(30.0, 30.0))
			boxes.append([start.x, start.y, end.x, end.y])
	check("stage has %d lit lenses" % expected, lit == expected)
	return {"visible":active,"quality":quality,"lit":lit,"bounds":boxes,"state":engine.state,"clock":engine.clock,
		"go_time":engine.go_t,"attempt":engine.attempt,"countdown_events":countdown_events.duplicate(),"go_events":go_events}

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
