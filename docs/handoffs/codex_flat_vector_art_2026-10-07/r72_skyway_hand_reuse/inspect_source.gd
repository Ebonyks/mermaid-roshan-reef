extends SceneTree
# SOURCE_INSPECTION_ONLY. Original pixels rendered through Sprite2D regions; no asset export/edit.
var out_dir := ""
func _init() -> void:
	call_deferred("_run")
func _label(text: String, position: Vector2) -> void:
	var label := Label.new()
	label.text = text
	label.position = position
	label.add_theme_font_size_override("font_size", 20)
	root.add_child(label)
func _sprite(path: String, rect: Rect2, position: Vector2, angle: float, zoom: float) -> void:
	var sprite := Sprite2D.new()
	sprite.texture = load(path) as Texture2D
	sprite.region_enabled = true
	sprite.region_rect = rect
	sprite.region_filter_clip_enabled = true
	sprite.position = position
	sprite.rotation = angle
	sprite.scale = Vector2.ONE * zoom
	root.add_child(sprite)
func _run() -> void:
	out_dir = OS.get_environment("R72_INSPECT_OUT")
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(Vector2i(1280, 720))
	DisplayServer.window_set_position(Vector2i(-2400, 0))
	var backdrop := ColorRect.new()
	backdrop.color = Color(0.10, 0.12, 0.18)
	backdrop.size = Vector2(1280, 720)
	root.add_child(backdrop)
	_label("SOURCE INSPECTION ONLY - literal regions, no edited asset, no gameplay/acceptance", Vector2(20, 10))
	_sprite("res://assets/characters/roshan_25d/roshan_gesture_b.png", Rect2(512, 768, 256, 256), Vector2(150, 210), 0.0, 1.2)
	_label("Current atlas frame14", Vector2(20, 380))
	var sizes: Array[int] = [40, 32, 28, 25]
	for i: int in range(sizes.size()):
		var x: float = 430.0 + float(i) * 220.0
		_sprite("res://assets/characters/roshan_25d/roshan_gesture_b.png", Rect2(527, 819, sizes[i], 35), Vector2(x, 190), -PI * 0.5, 4.0)
		_label("Width " + str(sizes[i]) + " / 4x", Vector2(x - 70, 300))
		_sprite("res://assets/characters/roshan_25d/roshan_gesture_b.png", Rect2(527, 819, sizes[i], 35), Vector2(x, 440), -PI * 0.5, 1.25)
		_label("Same region / 1.25x", Vector2(x - 85, 490))
	_sprite("res://assets/characters/roshan_25d/roshan_gestures.png", Rect2(773, 331, 29, 27), Vector2(150, 540), -PI * 0.5, 4.0)
	_label("Original reference / 4x", Vector2(20, 640))
	for i: int in range(30):
		await process_frame
	await RenderingServer.frame_post_draw
	var frame: Image = root.get_texture().get_image()
	if frame == null or frame.get_size() != Vector2i(1280, 720):
		quit(1)
		return
	var path: String = out_dir.path_join("source_inspection.png")
	var status: Error = frame.save_png(path)
	print("R72_SOURCE_INSPECTION|", status, "|", FileAccess.get_sha256(path))
	quit(0 if status == OK else 1)
