extends SceneTree
## Lossless gameplay export from the generated driver keys and original chassis.
const SOURCE := "res://assets_src/imagegen/reef_kart_riders_20261107/"
const DEST := "res://assets/racer/riders_v1/"
const CELL := 256
const BASELINE := 220

# Columns are exported rider height, hand/wing contact y, spine x within the
# trimmed image, and a small rise to keep a short driver's silhouette readable.
const RIDERS := [
	[109, 0.53, 0.50, 3], [110, 0.57, 0.48, 0], [103, 0.54, 0.50, 0],
	[96, 0.52, 0.50, 0], [105, 0.55, 0.50, 0], [110, 0.53, 0.50, 0],
	[103, 0.52, 0.50, 0], [110, 0.49, 0.50, 0], [116, 0.57, 0.56, 0],
	[116, 0.58, 0.50, 0], [113, 0.59, 0.55, 0],
	[109, 0.53, 0.50, 3], [109, 0.53, 0.50, 3],
]
# Body width, grip Y and seat/cowling occlusion edge in registered 256px space.
const RIDES := {
	"kart": [196, 97, [[0, 117], [88, 122], [101, 115], [114, 111], [143, 111],
		[158, 115], [169, 123], [255, 117]]],
	"moto": [132, 69, [[0, 84], [95, 84], [108, 80], [120, 78], [137, 78],
		[150, 81], [163, 86], [255, 84]]],
	"truck": [210, 94, [[0, 114], [91, 117], [103, 108], [114, 103], [142, 103],
		[154, 108], [165, 117], [255, 114]]],
}

func _initialize() -> void:
	var eagle := Image.load_from_file(SOURCE + "eagle_native.png")
	var toys := Image.load_from_file(SOURCE + "toy_native.png")
	var family := Image.load_from_file(SOURCE + "family_native.png")
	var keys: Array[Image] = [
		_cell(eagle, 0, 0, 3, 1),
		_trim(family.get_region(Rect2i(0, 0, 654, 567))),
	]
	for i in range(6):
		keys.append(_cell(toys, i % 3, i / 3, 3, 2))
	keys.append(_trim(family.get_region(Rect2i(654, 0, 655, 590))))
	keys.append(_trim(family.get_region(Rect2i(0, 567, 654, 635))))
	keys.append(_trim(family.get_region(Rect2i(654, 590, 655, 612))))
	keys.append(_cell(eagle, 1, 0, 3, 1))
	keys.append(_cell(eagle, 2, 0, 3, 1))
	for ride: String in RIDES:
		var spec: Array = RIDES[ride]
		var original := _trim(Image.load_from_file("res://assets/kart/chase/empty_%s.png" % ride))
		var width := int(spec[0])
		var height := roundi(float(original.get_height() * width) / original.get_width())
		original.resize(width, height, Image.INTERPOLATE_LANCZOS)
		var body := Image.create(CELL, CELL, false, Image.FORMAT_RGBA8)
		body.blit_rect(original, Rect2i(Vector2i.ZERO, original.get_size()),
			Vector2i((CELL - width) / 2, BASELINE - height))
		var atlas := Image.create(1024, 1024, false, Image.FORMAT_RGBA8)
		for i in range(keys.size()):
			var card := _compose(body, keys[i], RIDERS[i], spec[1], spec[2])
			var bounds := card.get_used_rect()
			if bounds.position.y < 12 or bounds.position.x < 12 or bounds.end.x > CELL - 12 					or abs(bounds.end.y - BASELINE) > 2:
				push_error("%s slot %d breached the transparent gutter or ground anchor: %s" % [ride, i, bounds])
				quit(2)
				return
			atlas.blit_rect(card, Rect2i(0, 0, CELL, CELL), Vector2i(i % 4, i / 4) * CELL)
		if atlas.save_png(DEST + ride + ".png") != OK:
			quit(1)
			return
		print("RIDER_ATLAS|", ride, "|poses=", keys.size(), "|body=", width, "x", height)
	quit(0)

func _cell(source: Image, col: int, row: int, columns: int, rows: int) -> Image:
	var size := Vector2i(source.get_width() / columns, source.get_height() / rows)
	return _trim(source.get_region(Rect2i(Vector2i(col, row) * size, size)))

func _trim(source: Image) -> Image:
	source.convert(Image.FORMAT_RGBA8)
	var left := source.get_width()
	var top := source.get_height()
	var right := 0
	var bottom := 0
	for y in range(source.get_height()):
		for x in range(source.get_width()):
			if source.get_pixel(x, y).a >= 32.0 / 255.0:
				left = mini(left, x)
				top = mini(top, y)
				right = maxi(right, x + 1)
				bottom = maxi(bottom, y + 1)
	var bounds := Rect2i(left, top, right - left, bottom - top)
	return source.get_region(bounds.grow(2).intersection(Rect2i(Vector2i.ZERO, source.get_size())))

func _compose(body: Image, source: Image, spec: Array, grip_y: int, seat_edge: Array) -> Image:
	var rider := source.duplicate() as Image
	var height := mini(int(spec[0]), floori(float(grip_y - int(spec[3]) - 14) / float(spec[1])))
	var width := roundi(float(source.get_width() * height) / source.get_height())
	rider.resize(width, height, Image.INTERPOLATE_LANCZOS)
	var contact := Vector2i(roundi(width * float(spec[2])), roundi(height * float(spec[1])))
	var place := Vector2i(CELL / 2, grip_y - int(spec[3])) - contact
	var result := body.duplicate() as Image
	result.blend_rect(rider, Rect2i(Vector2i.ZERO, rider.get_size()), place)
	var segment := 0
	for x in range(CELL):
		while x > int(seat_edge[segment + 1][0]):
			segment += 1
		var a: Array = seat_edge[segment]
		var b: Array = seat_edge[segment + 1]
		var y := roundi(lerpf(float(a[1]), float(b[1]), inverse_lerp(float(a[0]), float(b[0]), float(x))))
		# The original seatback and cowling own the foreground.
		result.blit_rect(body, Rect2i(x, y, 1, CELL - y), Vector2i(x, y))
	return result
