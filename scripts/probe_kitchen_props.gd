extends SceneTree
# Source-asset contract for the Royal Kitchen Sprite3D cards. Historical GLB
# fixtures are intentionally outside the runtime contract.

const ROOM_DIR := "res://assets/flats/castle/rooms/"
const ASSETS: Array[String] = [
	"room_kitchen_background.png",
	"room_kitchen_front_left.png",
	"room_kitchen_front_right.png",
	"room_kitchen_item_sink.png",
	"room_kitchen_item_soup_pot.png",
	"room_kitchen_item_teapot.png",
]

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
		total_pixels += int(size.x * size.y)
		print("KITCHEN|sprite=", filename, " size=", size)
	print("KITCHEN|RESULT=", "FAIL" if failed else "OK",
		" cards=", ASSETS.size(), " pixels=", total_pixels)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
