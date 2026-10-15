extends SceneTree
func _init() -> void:
	var rows: Array = []
	for item: Dictionary in ClassDB.class_get_property_list("StyleBoxTexture", true):
		rows.append(str(item.get("name", "")))
	print(JSON.stringify({"engine": Engine.get_version_info(), "StyleBoxTexture_properties": rows}))
	quit()
