extends SceneTree
# Source-asset contract for the Royal Kitchen Sprite3D cards. Historical GLB
# fixtures are intentionally outside the runtime contract.

const ROOM_DIR := "res://assets/flats/castle/rooms/"
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
	print("KITCHEN|RESULT=", "FAIL" if failed else "OK",
		" cards=", ASSETS.size(), " pixels=", total_pixels)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
