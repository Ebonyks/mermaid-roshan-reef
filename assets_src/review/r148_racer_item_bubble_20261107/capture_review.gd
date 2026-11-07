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
	print("R148_CAPTURE|", "PASS" if ok else "FAIL", "|", label)
	if not ok:
		failures += 1
func _run() -> void:
	dest = OS.get_environment("R148_CAPTURE_DEST")
	variant = OS.get_environment("R148_CAPTURE_VARIANT")
	width = int(OS.get_environment("R148_CAPTURE_WIDTH"))
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
	check("item touch geometry", OperaRacerSurface.TURBO_CENTER == Vector2(1010,505) and OperaRacerSurface.TURBO_RADIUS == 70.0 and OperaRacerSurface.HIT_MARGIN == 16.0)
	var engine: ReefKartRace = surface._engine
	surface.race_started = true
	engine.state = "race"
	for kind: String in ReefKartRace.ITEM_KINDS:
		check("existing item art resolves " + kind, engine._tex.get("icon_" + kind) is Texture2D)
	pose_item("", 0.0, 0.25)
	await shot("opera-empty", true)
	for index in range(ReefKartRace.ITEM_KINDS.size()):
		var kind: String = ReefKartRace.ITEM_KINDS[index]
		pose_item("", 0.45, (float(index) + 0.1) / 12.0)
		await shot("opera-rolling-" + kind, true)
	for kind: String in ReefKartRace.ITEM_KINDS:
		pose_item(kind, 0.0, 0.32)
		await shot("opera-ready-" + kind, true)
	pose_item("zoom", 0.0, 0.32)
	var event := InputEventScreenTouch.new()
	event.index = 73
	event.pressed = true
	event.position = OperaRacerSurface.TURBO_CENTER
	surface._gui_input(event)
	surface._publish_controls()
	check("touch owns existing item route", surface.race_turbo_owner == 73 and surface.race_turbo_held and surface._turbo_queued and bool(engine.controls["bubble_held"]))
	await shot("opera-held", true)
	event.pressed = false
	surface._gui_input(event)
	check("release clears existing item owner", surface.race_turbo_owner == -1 and not surface.race_turbo_held and not bool(engine.controls["bubble_held"]))
	await shot("opera-released", true)
	event.pressed = true
	surface._gui_input(event)
	surface._notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	check("focus loss drops the queued activation and retains the item", not surface._turbo_queued and surface.race_turbo_owner == -1 and not bool(engine.controls["bubble_held"]) and String(engine._pl["item"]) == "zoom")
	await shot("opera-focus-cancelled", true)
	surface._notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	surface._gui_input(event)
	surface._tick_driving(1.0 / 30.0)
	check("real item activation spends zoom", String(engine._pl["item"]).is_empty() and engine.turbo_count == 1)
	event.pressed = false
	surface._gui_input(event)
	pose_item("", 0.0, 0.32)
	await shot("opera-spent", true)
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
		check("PC touch-item negative branch remains empty " + str(count), pc._race.controls.is_empty())
		await shot("pc-" + str(count) + "-no-touch-item-frame", false)
		pc.queue_free()
		await process_frame
	var output := FileAccess.open(dest + "/captures.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"variant":variant, "width":width, "records":rows, "failures":failures, "renderer":RenderingServer.get_current_rendering_method(), "version":version, "frame_cap":Engine.max_fps, "source_script_sha256":FileAccess.get_sha256("res://scripts/racer/reef_kart_race.gd"), "limits":"Configured real surface and production fit helper. Inventory and roulette states are posed; item press/release/cancel and spend use the surface handlers. PC negatives are configured. Formal QA11 and natural/device/child/owner remain open."}, "\t") + "\n")
	print("R148_CAPTURE|DONE|frames=", rows.size(), "|failures=", failures)
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
		control_state = {"center":[1010,505], "radius":70.0, "held":surface.race_turbo_held, "owner":surface.race_turbo_owner, "item":String(surface._engine._pl["item"]), "roulette":float(surface._engine._pl["roulette_t"]), "clock":surface._engine._time, "queued":surface._turbo_queued, "suspended":surface._application_suspended}
	rows.append({"file":label+".png", "size":[picture.get_width(),picture.get_height()], "sha256":FileAccess.get_sha256(file), "quality_context":quality_context, "target_visible":target_visible, "target_state":control_state, "variant":variant, "renderer":RenderingServer.get_current_rendering_method(), "formal_QA11":false})
func pose_item(kind: String, roulette: float, time: float) -> void:
	surface._engine._pl["item"] = kind
	surface._engine._pl["roulette_t"] = roulette
	surface._engine._time = time
	surface._publish_controls()
