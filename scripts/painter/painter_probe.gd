extends RefCounted
## Invoked by both probe_painter and the existing trusted MG2D roster entry.

const DOC := preload("res://scripts/painter/painter_document.gd")
const STUDIO := preload("res://scenes/painter_prototype.tscn")
const FILL := preload("res://scripts/painter/vendor/painter_flood_fill.gd")
var failures := 0


func check(ok: bool, description: String) -> void:
	print("PAINTER|", "OK|" if ok else "FAIL|", description)
	if not ok:
		failures += 1


func run(tree: SceneTree) -> bool:
	var document: PainterDocument = DOC.new()
	var blank := document.image.get_data()
	document.begin_stroke(Vector2(40, 40), Color.NAVY_BLUE)
	for point: Vector2 in [Vector2(170, 40), Vector2(170, 170), Vector2(40, 170), Vector2(40, 40)]:
		document.move_stroke(point)
	document.end_stroke()
	var outlined := document.image.get_data()
	var start := Time.get_ticks_usec()
	document.begin_fill(Vector2(90, 90), Color.CORAL)
	await _wait_fill(tree, document)
	print("PAINTER|fill_elapsed_ms|", (Time.get_ticks_usec() - start) / 1000.0)
	check(document.image.get_pixel(90, 90).is_equal_approx(Color.CORAL)
		and document.image.get_pixel(200, 90).is_equal_approx(DOC.PAPER), "closed region fills without crossing brush boundary")
	var filled := document.image.get_data()
	check(document.undo() and document.image.get_data() == outlined, "fill undo is exact")
	check(document.redo() and document.image.get_data() == filled, "fill redo is exact")
	document.undo()
	document.undo()
	check(document.image.get_data() == blank, "stroke undo restores blank")
	document.begin_fill(Vector2(0, 0), Color.BLUE)
	document.cancel_input()
	await _wait_fill(tree, document)
	check(document.image.get_data() == blank, "cancelled background fill never applies")
	document.begin_fill(Vector2(-1, 0), Color.RED)
	check(not document.fill_busy, "out of bounds seed rejected")
	for i: int in range(20):
		document.begin_stroke(Vector2(10 + i * 20, 20), Color.BLUE)
		document.end_stroke()
	check(document.undo_images.size() == 16, "history bounded at 16 half-megabyte canvases")
	_compare_fill_reference()
	var save_path := "user://painter_probe_%d.png" % Time.get_ticks_usec()
	check(document.save_canvas(save_path) == OK, "atomic save")
	var saved := document.image.get_data()
	document.begin_stroke(Vector2(20, 70), Color.RED)
	document.end_stroke()
	check(document.save_canvas(save_path) == OK, "second save keeps previous backup")
	var restored: PainterDocument = DOC.new()
	check(restored.load_canvas(save_path) and restored.image.get_data() == document.image.get_data(), "reload exact latest pixels")
	var corrupt := FileAccess.open(save_path, FileAccess.WRITE)
	corrupt.store_string("incomplete save")
	corrupt.close()
	check(restored.load_canvas(save_path) and restored.image.get_data() == saved, "corrupt primary recovers previous valid canvas")
	check(restored.save_canvas(save_path) == OK, "recovered document repairs primary safely")
	document.shutdown()
	var studio := STUDIO.instantiate() as PainterStudio
	studio.guided = false
	studio.load_saved = false
	studio.save_path = save_path
	tree.root.add_child(studio)
	await tree.process_frame
	await tree.process_frame
	blank = studio.document.image.get_data()
	for frame: int in range(12):
		await tree.process_frame
	check(studio.document.image.get_data() == blank and studio.document.undo_images.is_empty(), "passive scene makes no marks or awards")
	await _touch(tree, studio, Vector2(310, 250), true, 0)
	await _touch(tree, studio, Vector2(60, 60), true, 1)
	check(studio.owner_id == 0, "second finger cannot steal canvas")
	await _drag(tree, studio, Vector2(900, 430), 0)
	await _touch(tree, studio, Vector2(900, 430), false, 0)
	await _touch(tree, studio, Vector2(60, 60), false, 1)
	check(studio.document.image.get_data() != blank, "real ScreenTouch and drag paint")
	var snapshot := studio.document.image.get_data()
	await _touch(tree, studio, Vector2(380, 340), true, 0)
	studio.suspend()
	var paused := studio.document.image.get_data()
	await _drag(tree, studio, Vector2(780, 250), 0)
	await _touch(tree, studio, Vector2(780, 250), false, 0)
	check(studio.owner_id == PainterStudio.NONE and studio.document.image.get_data() == paused, "pause cancels held input and stale release")
	await _tap(tree, studio, Vector2(640, 353))
	check(not studio.suspended, "picture resume works")
	await _tap(tree, studio, Vector2(1075, 79))
	check(studio.document.image.get_data() == snapshot, "real undo control")
	await _tap(tree, studio, Vector2(1205, 79))
	check(studio.document.image.get_data() == paused, "real redo control")
	await _tap(tree, studio, Vector2(111, 505))
	await _tap(tree, studio, Vector2(630, 330))
	check(studio.selected_tool == "stamp" and studio.document.image.get_data() != paused, "existing shell stamp via touch")
	await _tap(tree, studio, Vector2(111, 237))
	var before_outside := studio.document.image.get_data()
	await _touch(tree, studio, Vector2(1075, 79), true, 0)
	await _drag(tree, studio, Vector2(700, 250), 0)
	await _touch(tree, studio, Vector2(700, 250), false, 0)
	check(studio.document.image.get_data() == before_outside, "tool press cannot turn into canvas stroke")
	await _tap(tree, studio, Vector2(111, 371))
	await _tap(tree, studio, Vector2(679, 645))
	await _tap(tree, studio, Vector2(270, 520))
	await _wait_studio_fill(tree, studio)
	await tree.process_frame
	check(studio.document.image.get_pixel(33, 234).is_equal_approx(PainterStudio.COLORS[3]), "bucket and colour controls fill through real touch")
	await _tap(tree, studio, Vector2(1075, 79))
	check(studio.document.image.get_data() == before_outside, "touch bucket undo preserves prior picture")
	if "--capture" in OS.get_cmdline_user_args() and DisplayServer.get_name() != "headless":
		# Illustrative marks are produced with the same touch route, never
		# pasted into a screenshot or saved over source artwork.
		while not studio.document.undo_images.is_empty():
			await _tap(tree, studio, Vector2(1075, 79))
		await _tap(tree, studio, Vector2(111, 237))
		await _tap(tree, studio, Vector2(427, 645))
		await _touch(tree, studio, Vector2(600, 260), true, 0)
		for step: int in range(1, 49):
			var angle := float(step) * TAU / 48.0
			await _drag(tree, studio, Vector2(530, 260) + Vector2(cos(angle), sin(angle)) * 70, 0)
		await _touch(tree, studio, Vector2(600, 260), false, 0)
		await _tap(tree, studio, Vector2(111, 371))
		await _tap(tree, studio, Vector2(530, 260))
		await _wait_studio_fill(tree, studio)
		await _tap(tree, studio, Vector2(111, 237))
		await _tap(tree, studio, Vector2(679, 645))
		for row: int in range(2):
			await _touch(tree, studio, Vector2(290, 400 + row * 60), true, 0)
			for step: int in range(1, 49):
				await _drag(tree, studio, Vector2(290 + step * 13,
					400 + row * 60 + sin(float(step) * TAU / 16.0) * 15.0), 0)
			await _touch(tree, studio, Vector2(914, 400 + row * 60), false, 0)
		await _tap(tree, studio, Vector2(111, 505))
		await _tap(tree, studio, Vector2(780, 275))
		await RenderingServer.frame_post_draw
		var capture := tree.root.get_texture().get_image()
		var capture_path := "res://tmp/painter-prototype/free-studio-%dx%d.png" % [capture.get_width(), capture.get_height()]
		check(capture.save_png(capture_path) == OK, "desktop diagnostic capture " + capture_path)
	var exit_count := [0]
	studio.leave_requested.connect(func() -> void: exit_count[0] += 1)
	await _tap(tree, studio, Vector2(87, 79))
	check(exit_count[0] == 1 and studio.owner_id == PainterStudio.NONE, "neutral exit emits once and releases touch")
	studio.queue_free()
	await tree.process_frame
	for path: String in [save_path, save_path + ".bak", save_path + ".tmp.png"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("PAINTER|RESULT|", "OK" if failures == 0 else "FAIL", "|failures=", failures)
	var guided_probe := preload("res://scripts/painter/painter_guided_probe.gd").new()
	var guided_pass: bool = await guided_probe.run(tree)
	return failures == 0 and guided_pass


func _wait_fill(tree: SceneTree, document: PainterDocument) -> void:
	var deadline := Time.get_ticks_msec() + 10000
	while document.fill_busy and Time.get_ticks_msec() < deadline:
		document.poll_fill()
		await tree.process_frame
	check(not document.fill_busy, "fill task finishes within timeout")
	if document.fill_busy:
		document.shutdown()


func _compare_fill_reference() -> void:
	# Differential test against an independent four-neighbour BFS: narrow
	# bridges, disconnected islands and segment revisits must match exactly.
	var rng := RandomNumberGenerator.new()
	rng.seed = 9216
	var all_equal := true
	for trial: int in range(32):
		var source := Image.create(23, 17, false, Image.FORMAT_RGBA8)
		for y: int in 17:
			for x: int in 23:
				source.set_pixel(x, y, Color.WHITE if rng.randf() > 0.30 else Color.BLACK)
		var seed := Vector2i(rng.randi_range(0, 22), rng.randi_range(0, 16))
		var expected: Image = source.duplicate()
		var actual: Image = source.duplicate()
		var target := source.get_pixelv(seed)
		var queue: Array[Vector2i] = [seed]
		expected.set_pixelv(seed, Color.RED)
		while not queue.is_empty():
			var point: Vector2i = queue.pop_back()
			for offset: Vector2i in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
				var next := point + offset
				if Rect2i(0, 0, 23, 17).has_point(next) and expected.get_pixelv(next) == target:
					expected.set_pixelv(next, Color.RED)
					queue.append(next)
		var fill: PainterFloodFill = FILL.new()
		fill.flood_fill(seed, source, actual, func(dest: Image, segments: Array) -> void:
			for segment in segments:
				dest.fill_rect(Rect2i(segment.left_position, segment.y,
					segment.right_position - segment.left_position + 1, 1), Color.RED))
		all_equal = all_equal and expected.get_data() == actual.get_data()
	check(all_equal, "imported scanline fill matches independent BFS on 32 seeded maps")


func _touch(tree: SceneTree, studio: PainterStudio, point: Vector2, pressed: bool, id: int) -> void:
	var event := InputEventScreenTouch.new()
	event.position = tree.root.get_screen_transform() * studio._stage.get_global_transform_with_canvas() * point
	event.index = id
	event.pressed = pressed
	Input.parse_input_event(event)
	await tree.process_frame


func _drag(tree: SceneTree, studio: PainterStudio, point: Vector2, id: int) -> void:
	var event := InputEventScreenDrag.new()
	event.position = tree.root.get_screen_transform() * studio._stage.get_global_transform_with_canvas() * point
	event.index = id
	Input.parse_input_event(event)
	await tree.process_frame


func _tap(tree: SceneTree, studio: PainterStudio, point: Vector2) -> void:
	await _touch(tree, studio, point, true, 0)
	await _touch(tree, studio, point, false, 0)



func _wait_studio_fill(tree: SceneTree, studio: PainterStudio) -> void:
	var deadline := Time.get_ticks_msec() + 10000
	while studio.document.fill_busy and Time.get_ticks_msec() < deadline:
		await tree.process_frame
	check(not studio.document.fill_busy, "studio applies worker result through live process")
