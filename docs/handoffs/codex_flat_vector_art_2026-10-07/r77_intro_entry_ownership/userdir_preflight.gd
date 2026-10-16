extends SceneTree
func _init() -> void:
	var before := ProjectSettings.globalize_path("user://reef_save.json")
	ProjectSettings.set_setting("application/config/use_custom_user_dir", true)
	ProjectSettings.set_setting("application/config/custom_user_dir_name", "mermaid-roshan-r77-userdir-preflight-20261016")
	var after := ProjectSettings.globalize_path("user://reef_save.json")
	print("R77_USERDIR_PREFLIGHT|", JSON.stringify({"normal_path": before, "after_path": after, "remapped": before != after, "Main_loaded": false, "save_contents_read": false, "save_files_written": false, "engine": Engine.get_version_info()}))
	quit(0)
