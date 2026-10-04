extends SceneTree

func _init() -> void:
	var path := "res://assets/kart/chase/anchors.json"
	var data: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	var valid: bool = data is Dictionary and (data as Dictionary).has("sprites")
	var count := 0
	if valid:
		for key in data["sprites"]:
			var row: Dictionary = data["sprites"][key]
			var texture: Texture2D = load("res://" + String(row["path"]))
			valid = valid and texture != null and texture.get_width() <= 1024 and texture.get_height() <= 1024
			count += 1
	valid = valid and count == 15
	valid = valid and not FileAccess.file_exists("res://assets_src/racer_chase_20261003/kart_native.png")
	valid = valid and not FileAccess.file_exists("res://assets_src/racer_chase_20261003/rejected_empty_halo.png")
	print("RACERPACK|metadata_sha256=", FileAccess.get_sha256(path), "|sprites=", count)
	print("RACERPACK|ALL OK" if valid else "RACERPACK|FAIL")
	quit(0 if valid else 1)
