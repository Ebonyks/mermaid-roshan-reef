extends SceneTree
const SOURCE := "res://assets/characters/roshan_25d/roshan_gesture_b.png"
const REGION := Rect2(527, 819, 28, 35)
func _init() -> void:
	call_deferred("_run")
func _label(text: String, position: Vector2) -> void:
	var label := Label.new()
	label.text = text
	label.position = position
	label.add_theme_font_size_override("font_size", 22)
	root.add_child(label)
func _show(texture: Texture2D, position: Vector2, zoom: float) -> void:
	var sprite := Sprite2D.new()
	sprite.texture = texture
	sprite.region_enabled = true
	sprite.region_rect = REGION
	sprite.region_filter_clip_enabled = true
	sprite.position = position
	sprite.rotation = -PI * 0.5
	sprite.scale = Vector2.ONE * zoom
	root.add_child(sprite)
func _hash(image: Image) -> String:
	var context := HashingContext.new()
	context.start(HashingContext.HASH_SHA256)
	context.update(image.get_data())
	return context.finish().hex_encode()
func _run() -> void:
	var out_dir: String = OS.get_environment("R72_COMPARE_OUT")
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var original: Image = Image.load_from_file(SOURCE)
	var imported: Texture2D = load(SOURCE) as Texture2D
	if original == null or imported == null:
		quit(1)
		return
	original.convert(Image.FORMAT_RGBA8)
	var lossless: ImageTexture = ImageTexture.create_from_image(original)
	var decoded: Image = imported.get_image()
	var compressed_format: int = decoded.get_format()
	if decoded.is_compressed():
		var status: Error = decoded.decompress()
		if status != OK:
			quit(1)
			return
	decoded.convert(Image.FORMAT_RGBA8)
	var count: int = 0
	var error_sum: float = 0.0
	var error_max: float = 0.0
	for y: int in range(819, 854):
		for x: int in range(527, 555):
			var a: Color = original.get_pixel(x, y)
			if a.a < 0.5:
				continue
			var b: Color = decoded.get_pixel(x, y)
			for channel: int in range(3):
				var value: float = absf(a[channel] - b[channel]) * 255.0
				error_sum += value
				error_max = maxf(error_max, value)
				count += 1
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(Vector2i(1280, 720))
	DisplayServer.window_set_position(Vector2i(-2400, 0))
	var background := ColorRect.new()
	background.color = Color(0.10, 0.12, 0.18)
	background.size = Vector2(1280, 720)
	root.add_child(background)
	_label("SOURCE DECODE INSPECTION ONLY - no gameplay/art acceptance", Vector2(20, 15))
	_label("Imported VRAM texture / 4x", Vector2(100, 105))
	_label("Original PNG ImageTexture / 4x", Vector2(660, 105))
	_show(imported, Vector2(300, 260), 4.0)
	_show(lossless, Vector2(900, 260), 4.0)
	_label("Both at actual trial scale49/27", Vector2(390, 465))
	_show(imported, Vector2(300, 560), 49.0 / 27.0)
	_show(lossless, Vector2(900, 560), 49.0 / 27.0)
	for i: int in range(30):
		await process_frame
	await RenderingServer.frame_post_draw
	var frame: Image = root.get_texture().get_image()
	if frame == null or frame.get_size() != Vector2i(1280, 720):
		quit(1)
		return
	var path: String = out_dir.path_join("decode_comparison.png")
	frame.save_png(path)
	var file: FileAccess = FileAccess.open(out_dir.path_join("decode_comparison.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"source": SOURCE, "source_sha256": FileAccess.get_sha256(SOURCE), "source_decoded_rgba_sha256": _hash(original), "imported_decoded_rgba_sha256": _hash(decoded), "source_size": [original.get_width(), original.get_height()], "imported_format_before_decompression": compressed_format, "opaque_region_rgb_sample_count": count, "opaque_region_rgb_mae_8bit": error_sum / float(count), "opaque_region_rgb_max_error_8bit": error_max, "png_sha256": FileAccess.get_sha256(path), "no_source_pixels_modified": true, "scope": "Existing imported versus original PNG lossless decode only; no bitmap editing or new art. Direct source PNG load is not Android export-ready proof."}, "\t", true) + "\n")
	file.close()
	print("R72_DECODE_COMPARISON|OK|", _hash(original))
	quit(0)
