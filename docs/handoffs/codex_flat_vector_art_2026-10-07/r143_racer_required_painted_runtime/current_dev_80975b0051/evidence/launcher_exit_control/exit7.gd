extends SceneTree
func _init() -> void:
	print("R143_LAUNCHER_CONTROL|engine=" + OS.get_executable_path())
	print("R143_LAUNCHER_CONTROL|intentional_exit=7")
	quit(7)
