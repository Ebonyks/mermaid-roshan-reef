extends SceneTree
func _initialize() -> void:
	var path := "res://assets/racer/zones_v1/pool_towel_cabinet.png"
	var texture := load(path) as Texture2D
	var picture := texture.get_image()
	var passed := texture.get_size() == Vector2(1024, 1024) and picture.get_mipmap_count() == 10
	var report := {"asset":path, "size":[texture.get_width(),texture.get_height()],
		"mipmaps":picture.get_mipmap_count(), "sha256":FileAccess.get_sha256(path), "pass":passed}
	var file := FileAccess.open("res://assets_src/imagegen/reef_kart_zones_20261105/runtime_verification.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t") + "\n")
	print("ZONE_TEXTURE|", "ALL OK" if passed else "FAIL", "|", JSON.stringify(report))
	quit(0 if passed else 1)
