extends SceneTree
var m: ReefMain
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("R130_OUT")
var lane := OS.get_environment("R130_LANE")
var width := int(OS.get_environment("R130_WIDTH"))
var height := int(OS.get_environment("R130_HEIGHT"))
var failed := 0
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
		print("R130|FAIL|", label)
func wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame
func shot(label: String) -> void:
	check(label + " title absent", not m.start_menu_active and m.start_menu_layer == null)
	check(label + " live trampoline", m.mg_kind == "trampoline" and m.mg2d_stage != null)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var path: String = out.path_join(label + ".png")
	var err: Error = image.save_png(path)
	check(label + " native PNG", err == OK and image.get_size() == Vector2i(width, height))
	var actor := m.mg.get("roshan") as TextureRect
	var target := m.mg.get("trampoline_target") as Control
	frames.append({"path": path, "sha256": FileAccess.get_sha256(path), "width": width, "height": height, "bounces": m.mg.get("bounces", -1), "actor_rect": str(Rect2(actor.position, actor.size)), "actor_source": actor.texture.resource_path, "target_rect": str(Rect2(target.position, target.size)), "stage_scale": str(m.mg2d_stage.scale), "stage_position": str(m.mg2d_stage.position)})
func touch(point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = point
	event.pressed = pressed
	Input.parse_input_event(event)
func tap_local(point: Vector2) -> void:
	var canvas: Transform2D = m.mg2d_stage.get_global_transform_with_canvas()
	var screen: Vector2 = canvas * point
	touch(screen, true)
	await process_frame
	touch(screen, false)
	await process_frame
func run() -> void:
	seed(20261102)
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(width, height)
	DirAccess.make_dir_recursive_absolute(out)
	var packed := load("res://scenes/main.tscn") as PackedScene
	m = packed.instantiate() as ReefMain
	m._save_state = SaveState.new(m, "user://r130_isolated_save.json")
	get_root().add_child(m)
	await wait_frames(20)
	check("actual display start menu", m.start_menu_active and m.start_menu_layer != null)
	var continue_button := m.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button
	check("real Continue control", continue_button != null)
	if continue_button == null:
		await finish()
		return
	var completed_save: Dictionary = m.save_data.duplicate(true)
	completed_save["day_one_active"] = false
	completed_save["day_one_completed_rooms"] = ["bathroom", "pool", "stuffie", "art"]
	m._day_one_ref().restore_state(completed_save)
	m.save_data.merge(m._day_one_ref().serialize_state(), true)
	m.has_saved_game = true
	continue_button.disabled = false
	continue_button.pressed.emit()
	await wait_frames(20)
	check("Continue closes actual title", not m.start_menu_active and m.start_menu_layer == null and not m.intro_active)
	m._set_touch_mode(m.TOUCH_MODE_HYBRID, false)
	m._apply_quality("speedy")
	m._mg2d_open("trampoline")
	await wait_frames(5)
	check("Mobile renderer", RenderingServer.get_current_rendering_method() == "mobile")
	check("exact viewport", get_root().get_visible_rect().size == Vector2(width, height))
	var target := m.mg.get("trampoline_target") as Control
	var actor := m.mg.get("roshan") as TextureRect
	check("original target400x140", target.position == Vector2(440,430) and target.size == Vector2(400,140))
	check("original actor150x190 at rest430", actor.size == Vector2(150,190) and actor.position == Vector2(565,335))
	check("original star140 square center64090", (m.mg["star"] as TextureRect).position == Vector2(570,20) and (m.mg["star"] as TextureRect).size == Vector2(140,140))
	check("no extra round jump control", (m.mg.get("btns",[]) as Array).is_empty())
	if lane == "candidate":
		var art := m.mg2d_stage.get_node_or_null("TrampolinePainted") as TextureRect
		check("whole painted trampoline exists", art != null)
		if art == null:
			await finish()
			return
		check("one painted texture, no procedural children", art.get_child_count() == 0 and art.texture.resource_path == "res://assets/mg/trampoline_pad_painted.png")
		check("exact runtimePNG hash", FileAccess.get_sha256(art.texture.resource_path) == "5dbe87c969009046242a38564bdb2359a94cb16fd30a10a0f44404e8297acf04")
		check("actual512x163 decoded RGBA alpha", art.texture.get_size() == Vector2(512,163) and art.texture.get_image().detect_alpha() == Image.ALPHA_BLEND)
		check("painted prop ignores input and preserves whole aspect", art.mouse_filter == Control.MOUSE_FILTER_IGNORE and art.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_CENTERED)
		check("registered prop rect, no actor change", art.position == Vector2(438.5,469.5) and art.size == Vector2(403,129) and actor.position == Vector2(565,335))
		check("one texture within450k mip budget", art.texture.get_image().get_data_size() <= 450000)
		for node_value in m.mg2d_stage.get_children():
			var node := node_value as Control
			if node is Panel and node.position == Vector2(440,492):
				check("old flat pad and detached highlight retired", false)

	await shot("01_rest")
	await tap_local(Vector2(1040,590))
	await create_timer(1.0).timeout
	check("wrong touch and passive cannot bounce", int(m.mg.get("bounces",-1)) == 0 and m.mg_kind == "trampoline")
	await shot("02_wrong_passive")
	for bounce in range(1,4):
		await tap_local(Vector2(640,520))
		check("real finger increments exactly " + str(bounce), int(m.mg.get("bounces",-1)) == bounce)
		await create_timer(0.20).timeout
		await shot("0" + str(bounce*2+1) + "_apex_" + str(bounce))
		check("rising actor reaches expected height " + str(bounce), actor.position.y < 335.0 - float(bounce)*60.0)
		await create_timer(0.35).timeout
		check("bounce lands at original rest " + str(bounce), absf(actor.position.y-335.0)<1.0)
		await shot("0" + str(bounce*2+2) + "_landing_" + str(bounce))
	var old_root: WeakRef = weakref(m.mg2d_root)
	m._mg2d_close()
	await wait_frames(3)
	check("close frees stage", old_root.get_ref() == null and m.mg2d_stage == null and m.mg_kind == "")
	m._mg2d_open("trampoline")
	await wait_frames(3)
	check("fresh reentry resets bounce", int(m.mg.get("bounces",-1)) == 0 and m.mg2d_stage != null)
	await shot("09_fresh_reentry")
	m._mg2d_close()
	await wait_frames(3)
	await finish()
func finish() -> void:
	if m != null and is_instance_valid(m):
		m.process_mode = Node.PROCESS_MODE_DISABLED
		m.get_parent().remove_child(m)
		m.free()
	await process_frame
	var result := {"status": "PASS" if failed==0 else "FAIL", "lane":lane, "checks":checks, "captures":frames, "formal_QA11":null, "device":null, "child":null, "owner":null, "configured_route_only":true, "source_pin_sha256":OS.get_environment("R130_PIN_SHA256")}
	var file := FileAccess.open(out.path_join("RESULT.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(result,"\t"))
	file.close()
	print("R130|END|",lane,"|checks=",checks.size(),"|bad=",failed)
	quit(0 if failed==0 else 1)
