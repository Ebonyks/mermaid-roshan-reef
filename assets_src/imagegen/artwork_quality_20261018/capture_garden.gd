extends SceneTree
## Configured scene fixture using real GUI touch events. Not a natural-route,
## device, child, owner or canonical QA11 visual-contract acceptance claim.
const OUT := "res://assets_src/imagegen/artwork_quality_20261018/review/"
var m: ReefMain
var records: Array[Dictionary] = []
func _initialize() -> void:
	call_deferred("_run")
func _shot(id: String) -> void:
	await create_timer(0.35).timeout
	await RenderingServer.frame_post_draw
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id": id, "path": path.trim_prefix("res://"),
		"renderer": RenderingServer.get_current_rendering_method(),
		"viewport": [root.size.x, root.size.y], "hud": true,
		"runtime": true, "fixture": "configured garden with real GUI touch input"})
func _tap(button: Button) -> void:
	var point := button.get_global_transform_with_canvas() * (button.size * 0.5)
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = point
	event.pressed = true
	root.push_input(event)
	await process_frame
	event = InputEventScreenTouch.new()
	event.index = 0
	event.position = point
	event.pressed = false
	root.push_input(event)
	await process_frame
func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	for id: String in ["wateringcan", "k_sprout", "k_flower1", "flower", "flower2", "k_flower2", "flower3", "pot"]:
		var texture: Texture2D = load(PictureGames.GARDEN_ART_ROOT + id + ".png") as Texture2D
		if texture == null or texture.get_size() != Vector2(512, 512):
			push_error("ARTWORK_CAPTURE missing or invalid imported texture: " + id)
			quit(1)
			return
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(3.0).timeout
	m._start_menu_ref()._dismiss_menu()
	m._skip_intro()
	m.day_one_active = false
	for width: int in [1280, 1600]:
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(root.size)
		await process_frame
		m._mg2d_open("garden")
		await _shot("garden-seeds-%d" % width)
		var buttons: Array[Button] = []
		for node: Node in m.mg2d_stage.get_children():
			if node is Button and node.has_meta("hx"):
				buttons.append(node as Button)
		assert(buttons.size() == 5)
		for button: Button in buttons:
			await _tap(button)
		assert(m.mg["stage"] == [1, 1, 1, 1, 1])
		await _shot("garden-sprouts-%d" % width)
		for index: int in range(4):
			await _tap(buttons[index])
		await _shot("garden-four-flowers-%d" % width)
		await _tap(buttons[4])
		assert(int(m.mg["grown"]) == 5)
		await _shot("garden-complete-%d" % width)
		m._mg2d_close()
		# Each aspect is a separate configured fixture; retire the first
		# fixture's global reward before opening the next one.
		m._medal_ref()._retire_celebration()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT + "capture.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures": records,
		"scope": "Current Mobile scene fixture; no natural-route or external acceptance"}, "\t"))
	file.close()
	print("ARTWORK_CAPTURE|PASS|8 real Mobile/HUD frames, 20 GUI taps, both aspects")
	quit()
