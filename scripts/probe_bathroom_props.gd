extends SceneTree
# Source-asset contract for the Bubble Bath Sprite3D cards. Historical GLB
# fixtures are intentionally outside the runtime contract.

const ROOM_DIR := "res://assets/flats/castle/rooms/"
const INTERACTION_DIR := "res://assets/flats/castle/interactions/"
const CASTLE_AUDIO_DIR := "res://assets/audio/castle/"
const ASSETS: Array[String] = [
	"room_bubble_bath_background.png",
	"room_bubble_bath_front_left.png",
	"room_bubble_bath_front_right.png",
	"room_bubble_bath_item_bathtub.png",
	"room_bubble_bath_item_sink.png",
	"room_bubble_bath_item_toilet.png",
	"room_bubble_bath_item_rubber_duck.png",
]
const INTERACTION_ATLASES := {
	"bubble_bath_bathtub_atlas.png": Vector2i(3, 3),
	"bubble_bath_sink_atlas.png": Vector2i(4, 2),
	"bubble_bath_toilet_atlas.png": Vector2i(4, 2),
	"bubble_bath_rubber_duck_atlas.png": Vector2i(4, 2),
}
const INTERACTION_AUDIO: Array[String] = [
	"bubble_water.ogg", "faucet_water.ogg", "toilet_flush.ogg",
	"duck_squeak.ogg",
]

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
			print("BATHROOM|FAIL|sprite asset unavailable=", path)
			failed = true
			continue
		var texture: Texture2D = load(path) as Texture2D
		if texture == null:
			print("BATHROOM|FAIL|texture load=", path)
			failed = true
			continue
		var size: Vector2 = texture.get_size()
		var size_ok: bool = size.x > 0.0 and size.y > 0.0 \
			and maxf(size.x, size.y) <= 1024.0
		if not size_ok:
			print("BATHROOM|FAIL|texture budget=", size, " path=", path)
			failed = true
		total_pixels += int(size.x * size.y)
		print("BATHROOM|sprite=", filename, " size=", size)
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
			print("BATHROOM|FAIL|semantic atlas=", filename,
				" size=", size, " grid=", grid)
			failed = true
		else:
			total_pixels += int(size.x * size.y)
			print("BATHROOM|atlas=", filename, " size=", size,
				" frames=8")
	for filename: String in INTERACTION_AUDIO:
		var path := CASTLE_AUDIO_DIR + filename
		if not ResourceLoader.exists(path):
			print("BATHROOM|FAIL|interaction audio unavailable=", path)
			failed = true
	print("BATHROOM|RESULT=", "FAIL" if failed else "OK",
		" cards=", ASSETS.size() + INTERACTION_ATLASES.size(),
		" pixels=", total_pixels)
	quit(1 if failed else 0)

func _init() -> void:
	call_deferred("_run")
