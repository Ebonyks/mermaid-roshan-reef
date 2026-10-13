extends SceneTree
## Independent diagnostic picture-game capture; no production edits.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var fresh_state_ids: Array[String] = []


class PictureTickBridge extends Node:
	var main: ReefMain
	func _process(delta: float) -> void:
		if main != null and is_instance_valid(main) and main.mg_kind != "":
			main._tick_mg2d(delta)

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _wait_frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _set_aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var test: Image = get_root().get_texture().get_image()
		if test != null and test.get_size() == target:
			return true
	return false

func _visible_nodes(node: Node, output: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row: Dictionary = {"path": str(node.get_path()), "class": node.get_class(), "modulate": str(item.modulate), "z_index": item.z_index}
		var control := node as Control
		if control != null:
			row["global_rect"] = str(control.get_global_rect())
		var texture := node as TextureRect
		if texture != null and texture.texture != null:
			row["texture"] = texture.texture.resource_path
		var button := node as Button
		if button != null:
			row["disabled"] = button.disabled
		output.append(row)
	for child: Node in node.get_children():
		_visible_nodes(child, output)

func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}

func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false

func _capture(id: String, input_info: Dictionary = {}, own_medal_expected: bool = false) -> void:
	await RenderingServer.frame_post_draw
	var presentation := _presentation()
	if bool(presentation["boot_splash_present"]) or bool(presentation["start_menu_active"]) or (bool(presentation["medal_present"]) and not own_medal_expected) or float(presentation["fade_alpha"]) > 0.02:
		errors.append("blocking/foreign presentation overlay " + id)
	var frame: Image = get_root().get_texture().get_image()
	var target := get_root().size
	if frame == null or frame.get_size() != target:
		errors.append("image backing mismatch " + id)
		return
	var path := out_dir.path_join(id + ".png")
	if frame.save_png(path) != OK:
		errors.append("save failed " + id)
		return
	var visible: Array[Dictionary] = []
	if m.mg2d_root != null:
		_visible_nodes(m.mg2d_root, visible)
	var image_file := FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "image": {"file": id + ".png", "sha256": FileAccess.get_sha256(path), "bytes": image_file.get_length(), "dimensions": [frame.get_width(),frame.get_height()]}, "presentation": presentation, "own_medal_expected": own_medal_expected, "phase": String(m.mg.get("phase","")), "balls": int(m.mg.get("balls",0)), "face": int(m.mg.get("face",0)), "bites": int(m.mg.get("bites",0)), "bounces": int(m.mg.get("bounces",0)), "placed": int(m.mg.get("placed",0)), "kind": m.mg_kind, "stage": (m.mg.get("stage", []) as Array).duplicate(), "grown": int(m.mg.get("grown",0)), "won": bool(m.mg.get("won",false)), "input": input_info, "visible_nodes": visible, "main_hud_visible": m.hud_layer.visible if m.hud_layer != null else false, "save_path": m._save_state.save_path})
	image_file.close()
	print("ROOTPIC|CAPTURE|" + id)

func _tap_garden(index: int, expected: int) -> Dictionary:
	var buttons: Array = m.mg.get("btns", [])
	var b := buttons[index] as Button
	var where := b.get_global_rect().get_center()
	var press := InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_LEFT
	press.pressed = true
	press.position = where
	press.global_position = where
	get_root().push_input(press, true)
	await process_frame
	var release := InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_LEFT
	release.pressed = false
	release.position = where
	release.global_position = where
	get_root().push_input(release, true)
	await process_frame
	var stage: Array = m.mg.get("stage", [])
	var observed := int(stage[index])
	if observed != expected:
		errors.append("actual pointer did not progress slot%d expected%d got%d" % [index, expected, observed])
	return {"method":"Window.push_input raw mouse press/release", "slot":index, "position":str(where), "expected_stage":expected, "observed_stage":observed, "target_rect":str(b.get_global_rect())}

func _run_aspect(target: Vector2i, base_out: String) -> void:
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y])
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	for kind: String in ["snowman"]:
		var scene := load("res://scenes/main.tscn") as PackedScene
		m = scene.instantiate() as ReefMain
		var profile := out_dir.path_join("profiles/" + kind + "/reef_save.json")
		DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
		m._save_state = SaveState.new(m,profile)
		get_root().add_child(m)
		await _wait_frames(3)
		m._apply_quality("speedy")
		m.day_one_active = false
		if m.start_menu_active:
			m._start_menu_ref()._dismiss_menu()
		if m.intro_active:
			m._skip_intro()
		if not await _wait_presentation():
			errors.append("startup presentation did not settle " + kind)
			m.queue_free()
			await _wait_frames(4)
			continue
		m._mg2d_open(kind)
		if m.game == "level2":
			errors.append("tick bridge would duplicate live Lagoon tick")
			return
		var bridge := PictureTickBridge.new()
		bridge.name = "DiagnosticPictureTickBridge"
		bridge.main = m
		m.add_child(bridge)
		await _wait_frames(3)
		await _capture(kind + "_fresh_ready", {"entry":"production _mg2d_open API; fresh Main and isolated save per game; direct route fixture"})
		await _actions(kind)
		m._mg2d_close()
		m.set_process(false)
		m.queue_free()
		await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.root_picture_context/1", "source_revision":OS.get_environment("ROOTPIC_REV"), "capture_method":"same-process viewport", "engine":Engine.get_version_info(), "renderer":RenderingServer.get_current_rendering_method(), "quality":"speedy", "aspect":[target.x,target.y], "states":states, "normal_save_before":normal_before, "normal_save_after":_normal_hashes(), "errors":errors, "scope_limits":"Fresh Main and SaveState per game; direct guarded API entry; bounded actual raw-axis/button events plus sampled states; explicit standalone picture production-tick scheduling fixture, not natural Lagoon route; no natural castle route, save/resume, complete motion, device/child/owner acceptance."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		print("ROOTPIC|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("ROOTPIC|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	await _run_aspect(Vector2i(1280,720),base_out)
	await _run_aspect(Vector2i(1600,720),base_out)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("ROOTPIC|RESULT|" + ("PASS" if errors.is_empty() else "FAIL") + "|" + str(errors))
	quit(0 if errors.is_empty() else 1)


func _raw_button(at: Vector2, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = at
	event.global_position = at
	Input.parse_input_event(event)
	Input.flush_buffered_events()
	await process_frame

func _raw_tap(control: Control) -> Dictionary:
	var at := control.get_global_rect().get_center()
	await _raw_button(at, true)
	await _raw_button(at, false)
	return {"method": "Input.parse_input_event raw mouse press/release", "position": str(at), "target_rect": str(control.get_global_rect())}

func _raw_motion(at: Vector2, relative: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = at
	event.global_position = at
	event.relative = relative
	event.button_mask = MOUSE_BUTTON_MASK_LEFT
	Input.parse_input_event(event)
	Input.flush_buffered_events()
	await process_frame

func _actions(kind: String) -> void:
	match kind:
		"snowman":
			await _snow_actions()
		"trampoline":
			for i: int in range(3):
				var target := m.mg.get("trampoline_target") as Control
				var input_info := await _raw_tap(target)
				if int(m.mg.get("bounces",0)) != i + 1:
					errors.append("trampoline raw tap did not progress")
					return
				await create_timer(0.23).timeout
				await _capture("trampoline_bounce%d_apex" % (i+1), input_info)
				await create_timer(0.36).timeout
				await _capture("trampoline_bounce%d_settle" % (i+1), input_info, i == 2)
		"slide":
			var target := m.mg.get("slide_target") as Control
			var input_info := await _raw_tap(target)
			if String(m.mg.get("phase","")) != "ride":
				errors.append("slide raw tap did not start ride")
				return
			await _capture("slide_ride_entry", input_info)
			await create_timer(1.35).timeout
			await _capture("slide_ride_midpoint", input_info)
			await create_timer(1.78).timeout
			await _capture("slide_ride_payoff", input_info, true)
		"xmas":
			var buttons: Array = m.mg.get("btns",[])
			for i: int in range(5):
				var button := buttons[i] as Button
				var input_info := await _raw_tap(button)
				if int(m.mg.get("placed",0)) != i + 1:
					errors.append("xmas raw tap did not place ornament")
					return
				await _capture("xmas_ornament%d_placed" % (i+1), input_info)
			var flower := m.mg.get("flowerbtn") as Button
			if flower.disabled:
				errors.append("xmas flower did not unlock")
				return
			var input_info := await _raw_tap(flower)
			if not bool(m.mg.get("won",false)):
				errors.append("xmas flower tap did not complete")
			await _capture("xmas_flower_payoff", input_info, true)

func _axis_circle_event(angle: float) -> void:
	for axis: int in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y]:
		var event := InputEventJoypadMotion.new()
		event.device = 99
		event.axis = axis
		event.axis_value = cos(angle) if axis == JOY_AXIS_LEFT_X else sin(angle)
		get_root().push_input(event, true)
	await process_frame

func _axis_release() -> void:
	for axis: int in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y]:
		var event := InputEventJoypadMotion.new()
		event.device = 99
		event.axis = axis
		event.axis_value = 0.0
		get_root().push_input(event, true)
	await process_frame

func _snow_actions() -> void:
	# Explicit synthetic unmapped-controller environment fixture. No controller
	# is physically connected, no progress counters are assigned, and this does
	# not establish the phone touch gesture. Production raw-axis _input and
	# joy_axis fallback consume all simulated events below.
	m.joy_has_unmapped = true
	for index: int in range(3):
		await _axis_circle_event(0.0)
		if absf(m.joy_axis(JOY_AXIS_LEFT_X)) < 0.35:
			errors.append("raw unmapped-axis fixture did not enter production polling")
			await _axis_release()
			return
		var steps := 0
		while int(m.mg.get("balls",0)) == index and steps < 220:
			steps += 1
			await _axis_circle_event(float(steps) * TAU / 48.0)
			if steps == 48:
				await _capture("snow_ball%d_growing" % (index+1), {"method":"Window.push_input raw joypad axis pairs", "fixture":"synthetic unmapped-controller mode joy_has_unmapped=true; no physical controller; diagnostic Node schedules production _tick_mg2d once per actual process frame because direct API fixture bypasses Lagoon scheduler", "steps":steps, "angle_step":TAU/48.0, "observed_rot_acc":float(m.mg.get("rot_acc",0.0)), "motor_assist":bool(m.mg.get("motor_assist",false))})
		await _axis_release()
		if int(m.mg.get("balls",0)) != index + 1:
			errors.append("raw axis circles did not finish ball%d" % (index+1))
			return
		await create_timer(0.6).timeout
		await _capture("snow_ball%d_stacked" % (index+1), {"method":"Window.push_input raw joypad axis pairs", "fixture":"synthetic unmapped-controller mode joy_has_unmapped=true; no physical controller; diagnostic Node schedules production _tick_mg2d once per actual process frame because direct API fixture bypasses Lagoon scheduler", "steps":steps, "motor_assist":bool(m.mg.get("motor_assist",false))})
	if String(m.mg.get("phase","")) != "face":
		errors.append("snow face phase absent")
		return
	var buttons: Array = m.mg.get("btns",[])
	for index: int in range(3):
		var button := buttons[index] as Button
		var input_info := await _raw_tap(button)
		if int(m.mg.get("face",0)) != index + 1:
			errors.append("snow face raw tap did not progress")
			return
		await _capture("snow_face%d_placed" % (index+1), input_info)
	await _capture("snow_chase_entry", {"method":"production transition after three actual face taps", "chase_followthrough":"held raw right axis follows"})
	await _snow_chase_followthrough()

func _snow_chase_followthrough() -> void:
	var right := InputEventJoypadMotion.new()
	right.device = 99
	right.axis = JOY_AXIS_LEFT_X
	right.axis_value = 1.0
	get_root().push_input(right, true)
	var last_bites := 0
	var steps := 0
	while String(m.mg.get("phase","")) in ["chase","carrot"] and steps < 600:
		steps += 1
		await process_frame
		var bites := int(m.mg.get("bites",0))
		if bites > last_bites:
			last_bites = bites
			await _capture("snow_bite%d" % bites, {"method":"raw right-axis event then actual process-frame polling", "fixture":"synthetic unmapped-controller mode and standalone production-tick bridge", "steps":steps}, bool(m.mg.get("won",false)))
	await _axis_release()
	if not bool(m.mg.get("won",false)) or String(m.mg.get("phase","")) != "done":
		errors.append("snow raw-axis chase did not finish within bounded fixture")
		return
	await _capture("snow_carrot_collected_payoff", {"method":"production chase/carrot transition from held raw right axis", "fixture":"synthetic unmapped-controller mode and standalone production-tick bridge", "steps":steps}, true)
