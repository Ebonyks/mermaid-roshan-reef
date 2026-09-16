class_name PainterTemplate
extends RefCounted
## One data-defined colouring page; no authored Roshan texture is edited.
## Region topology and target colours are separate from the shared paint engine.

const SIZE := PainterDocument.SIZE
const PAPER := PainterDocument.PAPER
const INK := Color("534674")
const TARGETS: Array[int] = [4, 1, 3, 2, 0]
const SEEDS: Array[Vector2i] = [Vector2i(45, 45), Vector2i(160, 64),
	Vector2i(240, 145), Vector2i(100, 228), Vector2i(390, 207)]
const COLORS: Array[Color] = [Color("e97b97"), Color("f5b85d"), Color("6abfab"),
	Color("66aee0"), Color("a187cf"), Color("534674")]
const SAVE_PATH := "user://painter_sunrise_v1.png"

var region_ids := PackedByteArray()
var shell_mask: Image
var blank: Image
var reference: Image


func _init() -> void:
	shell_mask = preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png").get_image()
	shell_mask.resize(106, 94, Image.INTERPOLATE_LANCZOS)
	region_ids.resize(SIZE.x * SIZE.y)
	blank = Image.create(SIZE.x, SIZE.y, false, Image.FORMAT_RGBA8)
	reference = Image.create(SIZE.x, SIZE.y, false, Image.FORMAT_RGBA8)
	for y: int in SIZE.y:
		for x: int in SIZE.x:
			region_ids[y * SIZE.x + x] = _shape_region(Vector2(x, y))
	for y: int in SIZE.y:
		for x: int in SIZE.x:
			var region := int(region_ids[y * SIZE.x + x])
			var boundary := x < 2 or y < 2 or x >= SIZE.x - 2 or y >= SIZE.y - 2
			if not boundary:
				for offset: Vector2i in [Vector2i(-2, 0), Vector2i(2, 0), Vector2i(0, -2), Vector2i(0, 2)]:
					if int(region_ids[(y + offset.y) * SIZE.x + x + offset.x]) != region:
						boundary = true
			blank.set_pixel(x, y, INK if boundary else PAPER)
			reference.set_pixel(x, y, INK if boundary else COLORS[TARGETS[region]])


func _shape_region(point: Vector2) -> int:
	# Reuse the original shell's silhouette in a separate logical region map.
	# The source image is read-only; no new design or PNG is generated.
	var shell_point := Vector2i(point) - Vector2i(337, 156)
	if Rect2i(0, 0, 106, 94).has_point(shell_point) and shell_mask.get_pixelv(shell_point).a > 0.5:
		return 4
	if point.distance_squared_to(Vector2(160, 64)) < 42.0 * 42.0:
		return 1
	if point.y < 106.0 + sin(point.x * TAU / 245.0) * 8.0:
		return 0
	if point.y < 180.0 + sin(point.x * TAU / 270.0 + 0.8) * 10.0:
		return 2
	return 3


func region_at(point: Vector2) -> int:
	var pos := Vector2i(point)
	if not Rect2i(Vector2i.ZERO, SIZE).has_point(pos):
		return -1
	if blank.get_pixelv(pos).is_equal_approx(INK):
		return -1
	return int(region_ids[pos.y * SIZE.x + pos.x])


func complete_count(image: Image) -> int:
	var count := 0
	for region: int in TARGETS.size():
		if is_complete(image, region):
			count += 1
	return count


func is_complete(image: Image, region: int) -> bool:
	return image.get_pixelv(SEEDS[region]).is_equal_approx(COLORS[TARGETS[region]])


func next_region(image: Image) -> int:
	for region: int in [1, 0, 2, 3, 4]:
		if not is_complete(image, region):
			return region
	return -1


func accepts_saved(image: Image) -> bool:
	# All interior pixels must be either blank or their region's target colour;
	# one seed is insufficient to accept an interrupted or foreign document.
	for y: int in SIZE.y:
		for x: int in SIZE.x:
			var pixel := image.get_pixel(x, y)
			var base := blank.get_pixel(x, y)
			if base.is_equal_approx(INK):
				if not pixel.is_equal_approx(INK):
					return false
			else:
				var region := int(region_ids[y * SIZE.x + x])
				var expected := COLORS[TARGETS[region]] if is_complete(image, region) else PAPER
				if not pixel.is_equal_approx(expected):
					return false
	return true
