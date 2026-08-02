extends SceneTree
# Source-asset contract for the Royal Kitchen Sprite3D cards. Historical GLB
# fixtures are intentionally outside the runtime contract.

const ROOM_DIR := "res://assets/flats/castle/rooms/"
const INTERACTION_DIR := "res://assets/flats/castle/interactions/"
const CASTLE_AUDIO_DIR := "res://assets/audio/castle/"
const ASSETS: Array[String] = [
	"room_kitchen_background.png",
	"room_kitchen_front_left.png",
	"room_kitchen_front_right.png",
	"room_kitchen_item_sink.png",
	"room_kitchen_item_pan_1.png",
	"room_kitchen_item_pan_2.png",
	"room_kitchen_item_pan_3.png",
	"room_kitchen_item_pan_4.png",
	"room_kitchen_item_oven.png",
	"room_kitchen_item_fridge.png",
	"background_tiles/room_kitchen_background_r0_c0.png",
	"background_tiles/room_kitchen_background_r0_c1.png",
	"background_tiles/room_kitchen_background_r0_c2.png",
	"background_tiles/room_kitchen_background_r0_c3.png",
	"background_tiles/room_kitchen_background_r1_c0.png",
	"background_tiles/room_kitchen_background_r1_c1.png",
	"background_tiles/room_kitchen_background_r1_c2.png",
	"background_tiles/room_kitchen_background_r1_c3.png",
	"background_tiles/room_kitchen_background_r2_c0.png",
	"background_tiles/room_kitchen_background_r2_c1.png",
	"background_tiles/room_kitchen_background_r2_c2.png",
	"background_tiles/room_kitchen_background_r2_c3.png",
]
const MAX_OPAQUE_COVERAGE := {
	"room_kitchen_front_left.png": 0.72,
	"room_kitchen_front_right.png": 0.50,
	"room_kitchen_item_sink.png": 0.46,
	"room_kitchen_item_pan_1.png": 0.34,
	"room_kitchen_item_pan_2.png": 0.34,
	"room_kitchen_item_pan_3.png": 0.34,
	"room_kitchen_item_pan_4.png": 0.24,
	"room_kitchen_item_oven.png": 0.82,
	"room_kitchen_item_fridge.png": 0.90,
}
const INTERACTION_ATLASES := {
	"kitchen_sink_atlas.png": Vector2i(4, 2),
	"kitchen_pan_1_atlas.png": Vector2i(4, 2),
	"kitchen_pan_2_atlas.png": Vector2i(4, 2),
	"kitchen_pan_3_atlas.png": Vector2i(4, 2),
	"kitchen_pan_4_atlas.png": Vector2i(4, 2),
	"kitchen_oven_atlas.png": Vector2i(4, 2),
	"kitchen_fridge_atlas.png": Vector2i(4, 2),
}
const INTERACTION_AUDIO: Array[String] = [
	"faucet_water.ogg", "pan_clang.ogg", "oven_door.ogg",
	"fridge_door.ogg",
]

func _opaque_coverage(texture: Texture2D) -> float:
	var image: Image = texture.get_image()
	if image == null or image.is_empty():
		return 1.0
	var opaque := 0
	for y in range(image.get_height()):
		for x in range(image.get_width()):
			if image.get_pixel(x, y).a >= 0.5:
				opaque += 1
	return float(opaque) / float(image.get_width() * image.get_height())

func _clear_frame_borders(texture: Texture2D, grid: Vector2i) -> bool:
	var image: Image = texture.get_image()
	if image == null or image.is_empty() \
			or image.get_width() % grid.x != 0 \
			or image.get_height() % grid.y != 0:
		return false
	var cell_width: int = image.get_width() / grid.x
	var cell_height: int = image.get_height() / grid.y
	for frame_index: int in range(8):
		var left: int = (frame_index % grid.x) * cell_width
		var top: int = (frame_index / grid.x) * cell_height
		var right: int = left + cell_width - 1
		var bottom: int = top + cell_height - 1
		for x: int in range(left, right + 1):
			if image.get_pixel(x, top).a > 0.01 \
					or image.get_pixel(x, bottom).a > 0.01:
				return false
		for y: int in range(top, bottom + 1):
			if image.get_pixel(left, y).a > 0.01 \
					or image.get_pixel(right, y).a > 0.01:
				return false
	return true

func _run() -> void:
	var failed := false
	var total_pixels := 0
	for filename: String in ASSETS:
		var path := ROOM_DIR + filename
		if not ResourceLoader.exists(path):
			print("KITCHEN|FAIL|sprite asset unavailable=", path)
			failed = true
			continue
		var texture: Texture2D = load(path) as Texture2D
		if texture == null:
			print("KITCHEN|FAIL|texture load=", path)
			failed = true
			continue
		var size: Vector2 = texture.get_size()
		var size_ok: bool = size.x > 0.0 and size.y > 0.0 \
			and maxf(size.x, size.y) <= 1024.0
		if not size_ok:
			print("KITCHEN|FAIL|texture budget=", size, " path=", path)
			failed = true
		if filename == "room_kitchen_item_fridge.png" \
				and (size.x < 130.0 or size.y < 250.0):
			print("KITCHEN|FAIL|fridge touch silhouette too small=", size)
			failed = true
		if MAX_OPAQUE_COVERAGE.has(filename):
			var opaque_coverage: float = _opaque_coverage(texture)
			var maximum: float = float(MAX_OPAQUE_COVERAGE[filename])
			if opaque_coverage > maximum:
				print("KITCHEN|FAIL|coarse alpha mask=", filename,
					" coverage=", opaque_coverage, " max=", maximum)
				failed = true
		total_pixels += int(size.x * size.y)
		print("KITCHEN|sprite=", filename, " size=", size)
	for filename: String in INTERACTION_ATLASES:
		var path := INTERACTION_DIR + filename
		var grid: Vector2i = INTERACTION_ATLASES[filename]
		var texture: Texture2D = load(path) as Texture2D \
			if ResourceLoader.exists(path) else null
		var atlas_ok: bool = texture != null
		var size := texture.get_size() if texture != null else Vector2.ZERO
		atlas_ok = atlas_ok and size.x > 0.0 and size.y > 0.0 \
			and maxf(size.x, size.y) <= 1024.0 \
			and int(size.x) % grid.x == 0 \
			and int(size.y) % grid.y == 0 \
			and grid.x * grid.y >= 4 and grid.x * grid.y <= 12 \
			and _clear_frame_borders(texture, grid)
		if not atlas_ok:
			print("KITCHEN|FAIL|semantic atlas=", filename,
				" size=", size, " grid=", grid)
			failed = true
		else:
			total_pixels += int(size.x * size.y)
			print("KITCHEN|atlas=", filename, " size=", size,
				" frames=", grid.x * grid.y)
	for filename: String in INTERACTION_AUDIO:
		var path := CASTLE_AUDIO_DIR + filename
		if not ResourceLoader.exists(path):
			print("KITCHEN|FAIL|interaction audio unavailable=", path)
			failed = true
	print("KITCHEN|RESULT=", "FAIL" if failed else "OK",
		" cards=", ASSETS.size() + INTERACTION_ATLASES.size(),
		" pixels=", total_pixels)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
