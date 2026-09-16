class_name PainterDocument
extends RefCounted
## One bounded child-authored canvas. Existing artwork is always read-only.
## The standalone prototype owns a separate PNG, never reef_save.json.

const FILL := preload("res://scripts/painter/vendor/painter_flood_fill.gd")
const SIZE := Vector2i(512, 256)
const PAPER := Color("fff6e4")
const HISTORY_LIMIT := 16
const DEFAULT_PATH := "user://painter_prototype.png"

var image: Image
var undo_images: Array[Image] = []
var redo_images: Array[Image] = []
var changed := false
var stroke_active := false
var save_error: Error = OK
var fill_busy := false
var _before: Image
var _last := Vector2.ZERO
var _stroke_color := Color.WHITE
var _thread: Thread
var _discard_fill := false


func _init() -> void:
	image = Image.create(SIZE.x, SIZE.y, false, Image.FORMAT_RGBA8)
	image.fill(PAPER)


func begin_stroke(point: Vector2, color: Color) -> void:
	if fill_busy or stroke_active or not _inside(point):
		return
	_before = image.duplicate()
	stroke_active = true
	_last = point
	_stroke_color = color
	_dab(point)


func move_stroke(point: Vector2) -> void:
	if not stroke_active:
		return
	var end := point.clamp(Vector2.ZERO, Vector2(SIZE - Vector2i.ONE))
	var count := maxi(1, ceili(_last.distance_to(end) / 2.0))
	for step: int in range(1, count + 1):
		_dab(_last.lerp(end, float(step) / float(count)))
	_last = end


func end_stroke() -> void:
	if not stroke_active:
		return
	stroke_active = false
	_commit(_before)
	_before = null


func _dab(point: Vector2) -> void:
	var center := Vector2i(point)
	for y: int in range(maxi(0, center.y - 6), mini(SIZE.y, center.y + 7)):
		for x: int in range(maxi(0, center.x - 6), mini(SIZE.x, center.x + 7)):
			var coverage := clampf(6.0 - Vector2(x, y).distance_to(point), 0.0, 1.0)
			if coverage > 0.0:
				image.set_pixel(x, y, image.get_pixel(x, y).lerp(_stroke_color, coverage))


func stamp(point: Vector2, source: Image) -> void:
	if fill_busy or stroke_active or not _inside(point):
		return
	var before: Image = image.duplicate()
	# Resizing this private copy does not change its original texture or PNG.
	var small: Image = source.duplicate()
	small.convert(Image.FORMAT_RGBA8)
	small.resize(56, 56, Image.INTERPOLATE_LANCZOS)
	image.blend_rect(small, Rect2i(Vector2i.ZERO, small.get_size()),
		Vector2i(point) - Vector2i(28, 28))
	_commit(before)


func begin_fill(point: Vector2, color: Color) -> void:
	if fill_busy or stroke_active or not _inside(point):
		return
	if image.get_pixelv(Vector2i(point)).is_equal_approx(color):
		return
	fill_busy = true
	_discard_fill = false
	_before = image.duplicate()
	_thread = Thread.new()
	var error := _thread.start(_fill_image.bind(image.duplicate(), Vector2i(point), color))
	if error != OK:
		fill_busy = false
		_thread = null
		_before = null


func _fill_image(source: Image, point: Vector2i, color: Color) -> Image:
	var target: Image = source.duplicate()
	var filler: PainterFloodFill = FILL.new()
	filler.flood_fill(point, source, target, func(dest: Image, segments: Array) -> void:
		for segment in segments:
			dest.fill_rect(Rect2i(segment.left_position, segment.y,
				segment.right_position - segment.left_position + 1, 1), color))
	return target


func poll_fill() -> bool:
	if not fill_busy or _thread.is_alive():
		return false
	var result: Image = _thread.wait_to_finish() as Image
	_thread = null
	fill_busy = false
	var applied := not _discard_fill and result != null
	if applied:
		image = result
		_commit(_before)
	_before = null
	return applied


func cancel_input() -> void:
	# Keep only pixels the child already painted; never finish a queued fill.
	end_stroke()
	_discard_fill = true


func shutdown() -> void:
	cancel_input()
	if _thread != null:
		_thread.wait_to_finish()
		_thread = null
	fill_busy = false
	_before = null


func undo() -> bool:
	if fill_busy or stroke_active or undo_images.is_empty():
		return false
	redo_images.append(image)
	image = undo_images.pop_back()
	changed = true
	return true


func redo() -> bool:
	if fill_busy or stroke_active or redo_images.is_empty():
		return false
	undo_images.append(image)
	image = redo_images.pop_back()
	changed = true
	return true


func _commit(before: Image) -> void:
	if before.get_data() == image.get_data():
		return
	undo_images.append(before)
	if undo_images.size() > HISTORY_LIMIT:
		undo_images.pop_front()
	redo_images.clear()
	changed = true


func _inside(point: Vector2) -> bool:
	return Rect2(Vector2.ZERO, Vector2(SIZE)).has_point(point)


func save_canvas(path: String = DEFAULT_PATH) -> Error:
	# Verify a temporary PNG before replacing the primary. A corrupt primary
	# never displaces a known-good backup during recovery.
	var temporary := path + ".tmp.png"
	save_error = image.save_png(temporary)
	if save_error != OK:
		return save_error
	if _read_canvas(temporary) == null:
		save_error = ERR_FILE_CORRUPT
		return save_error
	if _read_canvas(path) != null:
		save_error = DirAccess.copy_absolute(path, path + ".bak")
		if save_error != OK:
			return save_error
	elif _read_canvas(path + ".bak") == null:
		save_error = DirAccess.copy_absolute(temporary, path + ".bak")
		if save_error != OK:
			return save_error
	save_error = DirAccess.rename_absolute(temporary, path)
	if save_error == OK:
		changed = false
	return save_error


func load_canvas(path: String = DEFAULT_PATH) -> bool:
	for candidate: String in [path, path + ".bak"]:
		var restored := _read_canvas(candidate)
		if restored != null:
			image = restored
			undo_images.clear()
			redo_images.clear()
			changed = candidate != path
			return true
	return false


func _read_canvas(path: String) -> Image:
	if not FileAccess.file_exists(path):
		return null
	var bytes := FileAccess.get_file_as_bytes(path)
	# Reject malformed headers/oversized payloads before asking the PNG decoder.
	if bytes.size() < 24 or bytes.size() > 2 * 1024 * 1024:
		return null
	if bytes.slice(0, 8) != PackedByteArray([137, 80, 78, 71, 13, 10, 26, 10]):
		return null
	var width := (int(bytes[16]) << 24) | (int(bytes[17]) << 16) | (int(bytes[18]) << 8) | int(bytes[19])
	var height := (int(bytes[20]) << 24) | (int(bytes[21]) << 16) | (int(bytes[22]) << 8) | int(bytes[23])
	if Vector2i(width, height) != SIZE:
		return null
	var restored := Image.new()
	if restored.load_png_from_buffer(bytes) != OK:
		return null
	restored.convert(Image.FORMAT_RGBA8)
	return restored
