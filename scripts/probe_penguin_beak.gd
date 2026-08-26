extends SceneTree
# BEAK PROBE — verifies the approved 2D penguin art source remains available.

const PENGUIN_ART := "res://assets/aquatic2/Penguin_Image_0.jpg"

func _init() -> void:
	var image := Image.new()
	var error: int = image.load(ProjectSettings.globalize_path(PENGUIN_ART))
	var ok := error == OK and not image.is_empty()
	print("BEAK|2d_art=", PENGUIN_ART, " size=", image.get_size(), " error=", error)
	print("BEAK|RESULT=", "OK" if ok else "FAIL")
	quit(0 if ok else 1)
