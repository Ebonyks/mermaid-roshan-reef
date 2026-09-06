extends SceneTree

## Temporary Mobile/1280x720 visual capture harness for the four active picture
## games. This intentionally calls the same `_mg2d_open`, `pressed.emit`,
## `touch_ui.stick_vec`, and `_tick_mg2d` paths used by probe_mg2d. It does not
## set phases, award rewards, or bypass a transition. The parent agent runs it.

const CAPTURE_DIR := "user://minigame_art_quality_garden_2026-09-05"
const DT := 1.0 / 60.0

var main: ReefMain = null
var capture_index := 0

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	Engine.time_scale = 1.0
	get_root().size = Vector2i(1280, 720)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	if main == null:
		push_error("PICTURE_CAPTURE|FAIL|main scene is not ReefMain")
		quit(1)
		return
	get_root().add_child(main)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(CAPTURE_DIR))
	await process_frame
	await process_frame
	main.day_one_active = false
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		await process_frame
		await process_frame
	if main.intro_active:
		main._skip_intro()
		await process_frame
		await process_frame
	main.set_process(false)
	main.set_physics_process(false)
	var viewport_size: Vector2i = get_root().size
	var renderer := RenderingServer.get_current_rendering_method()
	if viewport_size != Vector2i(1280, 720):
		push_error("PICTURE_CAPTURE|FAIL|viewport=%s expected=1280x720" % viewport_size)
		quit(1)
		return
	if renderer != "mobile":
		push_error("PICTURE_CAPTURE|FAIL|renderer=%s expected=mobile" % renderer)
		quit(1)
		return
	print("PICTURE_CAPTURE|viewport=%s|renderer=%s|output=%s" % [
		viewport_size,
		renderer,
		ProjectSettings.globalize_path(CAPTURE_DIR)])
	await _capture("boot")
	await _capture_garden()
	print("PICTURE_CAPTURE|DONE|count=%d" % capture_index)
	quit()

func _capture(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var filename := "%03d_%s.png" % [capture_index, label]
	var path := CAPTURE_DIR + "/" + filename
	var error := image.save_png(path)
	print("PICTURE_CAPTURE|file=%s|state=%s|viewport=%s|error=%s" % [
		filename, label, image.get_size(), error])
	capture_index += 1

func _open(kind: String, label: String) -> void:
	if not main.mg_kind.is_empty():
		main._mg2d_close()
		await process_frame
		await process_frame
	main._mg2d_open(kind)
	assert(main.mg_kind == kind and not main.start_menu_active and not main.intro_active)
	await process_frame
	await _capture(label)

func _tick(seconds: float) -> void:
	var frames := maxi(1, int(ceil(seconds / DT)))
	for _i in range(frames):
		main._tick_mg2d(DT)
		await process_frame

func _capture_snowman() -> void:
	await _open("snowman", "snowman_ready")
	var last_balls := int(main.mg.get("balls", 0))
	var elapsed := 0.0
	while main.mg_kind == "snowman" and String(main.mg.get("phase", "")) != "face" \
			and elapsed < 90.0:
		var phase := String(main.mg.get("phase", ""))
		if phase == "roll":
			var angle := float(main.mg.get("t", 0.0)) * 2.4
			main.touch_ui.stick_vec = Vector2(cos(angle), sin(angle))
		elif phase in ["chase", "carrot"]:
			var target := float(main.mg.get("run_x", main.mg.get("chaser_x", 640.0)))
			main.touch_ui.stick_vec = Vector2(signf(target - float(main.mg.get("chaser_x", 640.0))), 0.0)
		else:
			main.touch_ui.stick_vec = Vector2.ZERO
		main._tick_mg2d(DT)
		await process_frame
		elapsed += DT
		var balls := int(main.mg.get("balls", 0))
		if balls > last_balls:
			last_balls = balls
			await _capture("snowman_ball_%d_settle" % balls)
	if String(main.mg.get("phase", "")) == "face":
		main.touch_ui.stick_vec = Vector2.ZERO
		await _capture("snowman_face_ready")
		var face_buttons: Array = main.mg.get("btns", [])
		for i in range(face_buttons.size()):
			var button := face_buttons[i] as Button
			if button != null and button.visible and not button.disabled:
				button.pressed.emit()
				await _capture("snowman_face_%d" % (i + 1))
				await _tick(0.1)
	if String(main.mg.get("phase", "")) == "chase":
		await _capture("snowman_chase_ready")
		var chase_elapsed := 0.0
		while main.mg_kind == "snowman" and String(main.mg.get("phase", "")) == "chase" \
				and chase_elapsed < 20.0:
			var target := float(main.mg.get("run_x", 640.0))
			main.touch_ui.stick_vec = Vector2(signf(target - float(main.mg.get("chaser_x", 640.0))), 0.0)
			main._tick_mg2d(DT)
			await process_frame
			chase_elapsed += DT
		if String(main.mg.get("phase", "")) == "carrot":
			await _capture("snowman_carrot_ready")
			var carrot_elapsed := 0.0
			while main.mg_kind == "snowman" and carrot_elapsed < 6.0:
				var target := float(main.mg.get("run_x", 640.0))
				main.touch_ui.stick_vec = Vector2(signf(target - float(main.mg.get("chaser_x", 640.0))), 0.0)
				main._tick_mg2d(DT)
				await process_frame
				carrot_elapsed += DT
		main.touch_ui.stick_vec = Vector2.ZERO
		await _capture("snowman_final")
	if main.mg_kind != "":
		main._mg2d_close()
		await process_frame
		await process_frame

func _capture_garden() -> void:
	await _open("garden", "garden_ready_all_seeds")
	var buttons: Array = main.mg.get("btns", [])
	for i in range(buttons.size()):
		var button := buttons[i] as Button
		if button == null or not button.visible or button.disabled:
			continue
		await _capture("garden_seed_%d_before" % (i + 1))
		button.pressed.emit()
		await _capture("garden_seed_%d_sprout_or_flower" % (i + 1))
		await _tick(0.65)
		await _capture("garden_seed_%d_settled" % (i + 1))
	for i in range(buttons.size()):
		var button := buttons[i] as Button
		if button != null and button.visible and not button.disabled:
			button.pressed.emit()
			assert(int((main.mg["stage"] as Array)[i]) == 2)
			await _capture("garden_mature_%d" % (i + 1))
			await _tick(0.3)
	assert(int(main.mg.get("grown", 0)) == 5)
	await _capture("garden_all_five_mature")
	if main.mg_kind != "":
		main._mg2d_close()
		await process_frame
		await process_frame

func _capture_trampoline() -> void:
	await _open("trampoline", "trampoline_ready")
	var buttons: Array = main.mg.get("btns", [])
	var jump: Button = null
	if not buttons.is_empty():
		jump = buttons[0] as Button
	if jump != null:
		for i in range(4):
			jump.pressed.emit()
			await _capture("trampoline_bounce_%d" % (i + 1))
			await _tick(0.7)
	await _capture("trampoline_final")
	if main.mg_kind != "":
		main._mg2d_close()
		await process_frame
		await process_frame

func _capture_xmas() -> void:
	await _open("xmas", "xmas_ready_empty_tree")
	var buttons: Array = main.mg.get("btns", [])
	for i in range(buttons.size()):
		var button := buttons[i] as Button
		if button == null or not button.visible or button.disabled:
			continue
		button.pressed.emit()
		await _capture("xmas_ornament_%d_placed" % (i + 1))
		await _tick(0.1)
	print("XMASSTATE|placed=", main.mg.get("placed", -1), "|won=", main.mg.get("won", false))
	var flower_button := main.mg.get("flowerbtn") as Button
	if flower_button != null and flower_button.visible and not flower_button.disabled:
		flower_button.pressed.emit()
		await _capture("xmas_friendship_flower_finale")
	else:
		await _capture("xmas_post_button_sequence")
	if main.mg_kind != "":
		main._mg2d_close()
		await process_frame
		await process_frame
