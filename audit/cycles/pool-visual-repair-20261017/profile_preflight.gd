extends SceneTree
## Review-only probe preflight. No Main, gameplay or save construction.

func _init() -> void:
	var expected: String = OS.get_environment("POOL_REPAIR_PROFILE_ROOT").replace("\\", "/").to_lower().trim_suffix("/")
	var actual: String = OS.get_user_data_dir().replace("\\", "/").to_lower()
	if expected.is_empty() or not actual.begins_with(expected + "/"):
		printerr("POOL_PROFILE_PREFLIGHT|REFUSED|" + actual)
		quit(2)
		return
	print("POOL_PROFILE_PREFLIGHT|ACTUAL_USER_DATA|" + OS.get_user_data_dir())
	quit(0)
