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
	print("R147_CAPTURE|", "PASS" if ok else "FAIL", "|", label)
	if not ok:
		failures += 1
func _run() -> void:
	dest = OS.get_environment("R147_CAPTURE_DEST")
	variant = OS.get_environment("R147_CAPTURE_VARIANT")
	width = int(OS.get_environment("R147_CAPTURE_WIDTH"))
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
	seed(147)
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
	check("unchanged floating steering geometry", OperaRacerSurface.STEERING_RECT == Rect2(0,200,580,520) and OperaRacerSurface.STEERING_RANGE == 96.0 and OperaRacerSurface.STICK_RADIUS == 104.0 and OperaRacerSurface.STICK_HOME == Vector2(230,560))
	check("idle stick starts unowned", not surface.held and surface.race_touch_owner == -1)
	await shot("opera-idle-guided", true)
	var event := InputEventScreenTouch.new()
	event.index = 73
	event.pressed = true
	event.position = OperaRacerSurface.STICK_HOME
	surface._notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	surface._gui_input(event)
	surface._publish_controls()
	check("real touch publishes held steering centre", surface.held and surface.race_touch_owner == 73 and bool(surface._engine.controls["stick_held"]))
	await shot("opera-held-center", true)
	var drag := InputEventScreenDrag.new()
	drag.index = 73
	drag.position = OperaRacerSurface.STICK_HOME - Vector2(OperaRacerSurface.STEERING_RANGE,0)
	surface._gui_input(drag)
	surface._publish_controls()
	check("same owned touch reaches left endpoint", surface.race_touch_owner == 73 and surface.race_steer <= -0.99)
	await shot("opera-held-left", true)
	drag.position = OperaRacerSurface.STICK_HOME + Vector2(OperaRacerSurface.STEERING_RANGE,0)
	surface._gui_input(drag)
	surface._publish_controls()
	check("same owned touch reaches right endpoint", surface.race_touch_owner == 73 and surface.race_steer >= 0.99)
	await shot("opera-held-right", true)
	event.pressed = false
	event.position = drag.position
	surface._gui_input(event)
	surface._publish_controls()
	check("real release clears owner and restores home", not surface.held and surface.race_touch_owner == -1 and surface.race_steer == 0.0 and surface._stick_base == OperaRacerSurface.STICK_HOME)
	await shot("opera-released", true)
	event.pressed = true
	event.position = OperaRacerSurface.STICK_HOME
	surface._gui_input(event)
	surface._publish_controls()
	check("second real press owns same steering route", surface.race_touch_owner == 73 and surface.held)
	surface._notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	check("focus cancellation clears steering ownership", not surface.held and surface.race_touch_owner == -1 and not bool(surface._engine.controls["stick_held"]))
	await shot("opera-focus-cancelled", true)
	host.queue_free()
	await process_frame
	surface = null
	quality_context = "fixed_pc_no_quality_selector"
	for count in [1, 2]:
		seed(147)
		var pc := PCScene.instantiate() as PC
		root.add_child(pc)
		pc.set_physics_process(false)
		pc._show_garage(count, -1 if count == 1 else 6)
		if count == 2:
			pc._join(11)
		pc._toggle_ready(0)
		if count == 2:
			pc._toggle_ready(1)
		pc._choose_course(0)
		pc._start_race()
		check("PC touch-control negative branch remains empty " + str(count), pc._race.controls.is_empty())
		await shot("pc-" + str(count) + "-no-touch-steering", false)
		pc.queue_free()
		await process_frame
	var output := FileAccess.open(dest + "/captures.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"variant":variant, "width":width, "records":rows, "failures":failures, "renderer":RenderingServer.get_current_rendering_method(), "version":version, "frame_cap":Engine.max_fps, "source_script_sha256":FileAccess.get_sha256("res://scripts/racer/reef_kart_race.gd"), "limits":"Configured actual surface/PC scenes and production fit helper, not full natural routes or formalQA11/device/child/owner acceptance."}, "\t") + "\n")
	print("R147_CAPTURE|DONE|frames=", rows.size(), "|failures=", failures)
	quit(1 if failures else 0)
func shot(label: String, target_visible: bool) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var picture := root.get_texture().get_image()
	check("native window size " + label, picture.get_size() == Vector2i(width,720))
	var file := dest + "/" + label + ".png"
	var error := picture.save_png(file)
	check("native bytes saved " + label, error == OK)
	var control_state: Dictionary = {}
	if is_instance_valid(surface):
		control_state = {"stick_base":[surface._stick_base.x,surface._stick_base.y], "stick_knob":[surface._engine.controls["stick_knob"].x,surface._engine.controls["stick_knob"].y], "stick_radius":surface.STICK_RADIUS, "steer":surface.race_steer, "held":surface.held, "owner":surface.race_touch_owner, "guide":bool(surface._engine.controls["guide"]), "suspended":surface._application_suspended}
	rows.append({"file":label+".png", "size":[picture.get_width(),picture.get_height()], "sha256":FileAccess.get_sha256(file), "quality_context":quality_context, "target_visible":target_visible, "target_state":control_state, "variant":variant, "renderer":RenderingServer.get_current_rendering_method(), "formal_QA11":false})
