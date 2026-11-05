extends SceneTree
const IDS := ["item_capsule", "kelp_trap", "turn_marker", "play_blocks", "play_tent", "kitchen_teapot", "pool_seahorse"]
func valid(texture: Texture2D) -> bool:
	if texture == null:
		return false
	var image := texture.get_image()
	return image != null and image.get_size() == Vector2i(1024, 1024) and image.has_mipmaps() and image.get_mipmap_count() == 10
func _initialize() -> void:
	var failures := 0
	var no_mips := ImageTexture.create_from_image(Image.create(1024, 1024, false, Image.FORMAT_RGBA8))
	var wrong_size := ImageTexture.create_from_image(Image.create(512, 512, true, Image.FORMAT_RGBA8))
	var controls_ok := not valid(no_mips) and not valid(wrong_size) and not valid(null)
	print("RACER_RUNTIME_TEXTURE|", "PASS" if controls_ok else "FAIL", "|negative controls: missing mipmaps, wrong size, missing texture")
	failures += int(not controls_ok)
	for id: String in IDS:
		var texture := load("res://assets/racer/context_v2/" + id + ".png") as Texture2D
		var ok := valid(texture)
		print("RACER_RUNTIME_TEXTURE|", "PASS" if ok else "FAIL", "|", id,
			"|size=", texture.get_size() if texture != null else Vector2.ZERO,
			"|mips=", texture.get_image().get_mipmap_count() if texture != null else -1)
		failures += int(not ok)
	print("RACER_RUNTIME_TEXTURE|DONE|failures=", failures)
	quit(1 if failures else 0)
