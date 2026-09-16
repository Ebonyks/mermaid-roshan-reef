extends RefCounted

const STUDIO := preload("res://scenes/painter_prototype.tscn")
const TEMPLATE := preload("res://scripts/painter/painter_template.gd")
var failures := 0


func check(ok: bool, description: String) -> void:
	print("PAINTER_GUIDED|", "OK|" if ok else "FAIL|", description)
	if not ok:
		failures += 1


func run(tree: SceneTree) -> bool:
	var studio := STUDIO.instantiate() as PainterStudio
	studio.load_saved = false
	studio.save_path = "user://painter_guided_probe_%d.png" % Time.get_ticks_usec()
	tree.root.add_child(studio)
	await tree.process_frame
	var blank := studio.document.image.get_data()
	await tree.create_timer(0.4).timeout
	check(studio.guided and studio.template.complete_count(studio.document.image) == 0
		and studio.document.image.get_data() == blank, "guided is default; idle cannot fill blanks")
	check(studio._buttons.filter(func(button: Button) -> bool:
		return button.visible and String(button.get_meta("action")) in ["brush", "fill", "stamp"]).is_empty(),
		"free-paint tools absent from minigame")
	await _tap(tree, studio, Vector2(679, 645))
	await _hold_region(tree, studio, 1)
	check(studio.document.image.get_data() == blank, "wrong colour kindly cues without progress")
	await _tap(tree, studio, Vector2(427, 645))
	var sun := _region_point(1)
	await _touch(tree, studio, sun, true)
	check((studio._hint.get_child(0) as PainterStudio.ToolIcon).hold_fraction >= 0.0,
		"valid contact immediately shows hold feedback before fill completes")
	await _touch(tree, studio, sun, false)
	await tree.create_timer(0.3).timeout
	check(studio.document.image.get_data() == blank, "short tap does not bypass hold instruction")
	await _touch(tree, studio, sun, true)
	studio.suspend()
	await tree.create_timer(0.3).timeout
	await _touch(tree, studio, sun, false)
	check(studio.document.image.get_data() == blank, "pause cancels held guided action")
	await _tap(tree, studio, Vector2(640, 353))
	for region: int in [1, 0, 2, 3, 4]:
		var index := PainterTemplate.TARGETS[region]
		await _tap(tree, studio, Vector2(301 + index * 126, 645))
		var before := studio.template.complete_count(studio.document.image)
		await _hold_region(tree, studio, region)
		check(studio.template.complete_count(studio.document.image) == before + 1,
			"intentional matching fill completes region %d" % region)
		if region == 1:
			await _capture(tree, "guided-partial")
			var partial := PainterDocument.new()
			check(partial.load_canvas(studio.save_path)
				and studio.template.complete_count(partial.image) == 1, "partial guided work persists")
	check(studio.document.image.get_data() == studio.template.reference.get_data(),
		"finished painting matches coloured reference pixel-for-pixel")
	check(studio.template.accepts_saved(studio.document.image), "completed template validates for reload")
	var complete := studio.document.image.get_data()
	await _hold_region(tree, studio, 4)
	check(studio.document.image.get_data() == complete and studio.document.undo_images.size() == 5,
		"repeating finished region cannot add progress/history")
	await _capture(tree, "guided-complete")
	await _tap(tree, studio, Vector2(1075, 79))
	check(studio.template.complete_count(studio.document.image) == 4, "undo returns one intentional blank")
	await _tap(tree, studio, Vector2(1205, 79))
	check(studio.document.image.get_data() == complete, "redo restores completed layout")
	var path := studio.save_path
	studio.queue_free()
	await tree.process_frame
	var reentered := STUDIO.instantiate() as PainterStudio
	reentered.save_path = path
	tree.root.add_child(reentered)
	await tree.process_frame
	check(reentered.document.image.get_data() == complete
		and reentered.template.complete_count(reentered.document.image) == 5,
		"re-entry retains the exact completed picture")
	reentered.queue_free()
	await tree.process_frame
	for candidate: String in [path, path + ".bak", path + ".tmp.png"]:
		if FileAccess.file_exists(candidate):
			DirAccess.remove_absolute(candidate)
	print("PAINTER_GUIDED|RESULT|", "OK" if failures == 0 else "FAIL", "|failures=", failures)
	return failures == 0


func _region_point(region: int) -> Vector2:
	return PainterStudio.BOARD.position + Vector2(PainterTemplate.SEEDS[region]) * PainterStudio.BOARD.size / Vector2(PainterTemplate.SIZE)


func _hold_region(tree: SceneTree, studio: PainterStudio, region: int) -> void:
	await _touch(tree, studio, _region_point(region), true)
	await tree.create_timer(0.3).timeout
	await _touch(tree, studio, _region_point(region), false)
	var deadline := Time.get_ticks_msec() + 10000
	while studio.document.fill_busy and Time.get_ticks_msec() < deadline:
		await tree.process_frame
	check(not studio.document.fill_busy, "guided worker completes")
	await tree.process_frame


func _touch(tree: SceneTree, studio: PainterStudio, point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.position = tree.root.get_screen_transform() * studio._stage.get_global_transform_with_canvas() * point
	event.index = 0
	event.pressed = pressed
	Input.parse_input_event(event)
	await tree.process_frame


func _tap(tree: SceneTree, studio: PainterStudio, point: Vector2) -> void:
	await _touch(tree, studio, point, true)
	await _touch(tree, studio, point, false)


func _capture(tree: SceneTree, label: String) -> void:
	if "--capture" not in OS.get_cmdline_user_args() or DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	var image := tree.root.get_texture().get_image()
	var path := "res://tmp/painter-prototype/%s-%dx%d.png" % [label, image.get_width(), image.get_height()]
	check(image.save_png(path) == OK, "live diagnostic capture " + path)
