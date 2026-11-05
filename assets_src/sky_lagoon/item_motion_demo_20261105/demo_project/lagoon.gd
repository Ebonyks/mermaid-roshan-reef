extends Node2D

var world := Node2D.new()
var board := Node2D.new()
var clock: float = 0.0
var moving: bool = true
var show_board: bool = false
var entries: Array[Dictionary] = []
var textures: Dictionary = {}
var item_data: Array = []
var hud := Control.new()
var title := Label.new()
var pause_button := Button.new()
var view_button := Button.new()
var capture_mode: bool = false

func _ready() -> void:
	add_child(world)
	add_child(board)
	board.visible = false
	item_data = JSON.parse_string(FileAccess.get_file_as_string("res://items.json"))
	for data: Dictionary in item_data:
		textures[data["id"]] = load("res://" + str(data["atlas"])) as Texture2D
	for row in range(2):
		for column in range(6):
			var sprite := Sprite2D.new()
			sprite.centered = false
			sprite.texture = load("res://background/%d_%d.png" % [row, column]) as Texture2D
			sprite.position = Vector2(column * 320, row * 320)
			sprite.scale = Vector2.ONE * 0.3125
			world.add_child(sprite)
	var placements: Array = JSON.parse_string(FileAccess.get_file_as_string("res://placements.json"))
	for p: Array in placements:
		_add_item(world, str(p[0]), Vector2(float(p[1]), float(p[2])), Vector2(float(p[3]), float(p[4])))
	for index in range(item_data.size()):
		var data: Dictionary = item_data[index]
		var x: float = float(index % 3) * 420.0
		var y: float = float(index / 3) * 195.0
		var label := Label.new()
		label.text = str(data["title"])
		label.position = Vector2(x + 178, y + 83)
		label.add_theme_font_size_override("font_size", 17)
		board.add_child(label)
		_add_item(board, str(data["id"]), Vector2(x - 18, y - 10), Vector2(210, 210))
	add_child(hud)
	title.text = "Sky Lagoon  |  Moving garden"
	title.add_theme_font_size_override("font_size", 26)
	hud.add_child(title)
	pause_button.text = "Show still"
	pause_button.pressed.connect(_toggle_motion)
	hud.add_child(pause_button)
	view_button.text = "See each item"
	view_button.pressed.connect(_toggle_view)
	hud.add_child(view_button)
	get_viewport().size_changed.connect(_fit)
	_fit()
	_update_frames()
	if "--verify" in OS.get_cmdline_user_args():
		set_process(false)
		_verify()
	elif "--capture-fixed" in OS.get_cmdline_user_args():
		capture_mode = true
		set_process(false)
		_capture()

func _add_item(parent: Node2D, id: String, position_value: Vector2, size: Vector2) -> void:
	var sprite := Sprite2D.new()
	sprite.centered = false
	sprite.texture = textures[id] as Texture2D
	sprite.region_enabled = true
	sprite.region_rect = Rect2(0, 0, 256, 256)
	var side: float = minf(size.x, size.y)
	sprite.position = position_value + Vector2((size.x - side) / 2.0, (size.y - side) * 234.0 / 256.0)
	sprite.scale = Vector2.ONE * side / 256.0
	parent.add_child(sprite)
	entries.append({"id": id, "sprite": sprite, "expected_anchor": position_value + size * Vector2(0.5, 234.0 / 256.0)})

func _fit() -> void:
	var view: Vector2 = get_viewport_rect().size
	var scale_value: float = minf(view.x / 1920.0, (view.y - 120.0) / 640.0)
	world.scale = Vector2.ONE * scale_value
	world.position = Vector2((view.x - 1920.0 * scale_value) / 2.0, 70.0 + (view.y - 120.0 - 640.0 * scale_value) / 2.0)
	var board_scale: float = minf(view.x / 1260.0, (view.y - 120.0) / 585.0)
	board.scale = Vector2.ONE * board_scale
	board.position = Vector2((view.x - 1260.0 * board_scale) / 2.0, 83.0)
	title.position = Vector2(24, 16)
	pause_button.position = Vector2(view.x - 320, 12)
	pause_button.size = Vector2(136, 48)
	view_button.position = Vector2(view.x - 174, 12)
	view_button.size = Vector2(158, 48)

func _process(delta: float) -> void:
	if moving:
		clock = fposmod(clock + delta, 4.0)
	_update_frames()

func _update_frames() -> void:
	var index: int = int(clock * 10.0) % 40 if moving else 0
	for entry in entries:
		var sprite: Sprite2D = entry["sprite"] as Sprite2D
		sprite.region_rect = Rect2((index % 8) * 256, (index / 8) * 256, 256, 256)

func _toggle_motion() -> void:
	moving = not moving
	pause_button.text = "Show still" if moving else "Show breeze"
	_update_frames()

func _toggle_view() -> void:
	show_board = not show_board
	board.visible = show_board
	world.visible = not show_board
	view_button.text = "See the lagoon" if show_board else "See each item"

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and (event as InputEventMouseButton).pressed:
		clock = 0.6
		moving = true
		pause_button.text = "Show still"
	elif event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		clock = 0.6
		moving = true
		pause_button.text = "Show still"

func _draw_frame(t: float) -> Image:
	clock = t
	_update_frames()
	await RenderingServer.frame_post_draw
	return get_viewport().get_texture().get_image()

func _verify() -> void:
	await get_tree().process_frame
	var first: Image = await _draw_frame(0.0)
	var peak: Image = await _draw_frame(1.0)
	var end: Image = await _draw_frame(4.0)
	var bg: Vector2i = Vector2i(world.position + Vector2(400, 50) * world.scale)
	assert(first.get_pixelv(bg) == peak.get_pixelv(bg), "Stationary background changed")
	assert(first.get_data() != peak.get_data(), "Objects did not animate")
	assert(first.get_data() == end.get_data(), "Loop endpoint changed")
	for data: Dictionary in item_data:
		var image: Image = (textures[data["id"]] as Texture2D).get_image()
		assert(image.get_size() == Vector2i(2048, 2048))
		for index in range(40):
			var cel: Image = image.get_region(Rect2i((index % 8) * 256, (index / 8) * 256, 256, 256))
			var context := HashingContext.new()
			context.start(HashingContext.HASH_SHA256)
			var bytes: PackedByteArray = cel.get_data()
			for offset in range(0, bytes.size(), 4):
				if bytes[offset + 3] == 0:
					bytes[offset] = 0
					bytes[offset + 1] = 0
					bytes[offset + 2] = 0
			context.update(bytes)
			var hash_value: String = context.finish().hex_encode()
			if hash_value != str(data["frame_visible_rgba_sha256"][index]):
				cel.save_png("user://import-difference.png")
				printerr("ATLAS_MISMATCH ", data["id"], " frame=", index, " format=", cel.get_format(), " bytes=", bytes.size(), " expected=", data["frame_visible_rgba_sha256"][index], " actual=", hash_value)
				get_tree().quit(1)
				return
	_toggle_view()
	var board_image: Image = await _draw_frame(1.0)
	board_image.save_png("user://item-board.png")
	assert(board.visible and not world.visible)
	_toggle_view()
	_toggle_motion()
	assert(not moving)
	for entry in entries:
		assert((entry["sprite"] as Sprite2D).region_rect == Rect2(0, 0, 256, 256))
	_toggle_motion()
	var touch := InputEventScreenTouch.new()
	touch.pressed = true
	_unhandled_input(touch)
	assert(moving and clock == 0.6)
	for entry in entries:
		var sprite: Sprite2D = entry["sprite"] as Sprite2D
		assert(is_equal_approx(sprite.scale.x, sprite.scale.y), "Source card was stretched")
		var expected_anchor: Vector2 = entry["expected_anchor"]
		assert((sprite.position + sprite.scale * Vector2(128, 234)).is_equal_approx(expected_anchor), "Root anchor moved")
	var receipt: Dictionary = {"result": "PASS", "engine": Engine.get_version_info(), "renderer": RenderingServer.get_current_rendering_method(), "viewport": get_viewport_rect().size, "camera_translation_pixels": 0, "loop_endpoint": "exact", "atlas_cels_checked": 360, "all_item_scales_uniform": true, "source_root_anchors_preserved": true, "still_breeze_item_view_touch_restart": "PASS", "import_hash_scope": "alpha and all nonzero-alpha RGBA exact; fully transparent RGB canonicalized"}
	var file := FileAccess.open("user://item-verification.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t"))
	first.save_png("user://fixed-rest.png")
	peak.save_png("user://fixed-breeze.png")
	print("ITEM_MOTION_VERIFY PASS ", JSON.stringify(receipt))
	get_tree().quit()

func _capture() -> void:
	var output: String = ProjectSettings.globalize_path("res://../captures/engine")
	DirAccess.make_dir_recursive_absolute(output)
	await get_tree().process_frame
	for index in range(40):
		var image: Image = await _draw_frame(float(index) / 10.0)
		image.save_png(output.path_join("%03d.png" % index))
	get_tree().quit()
