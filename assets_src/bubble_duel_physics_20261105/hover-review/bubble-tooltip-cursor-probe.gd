extends "res://scripts/probe_bubble_duel_capture.gd"
func _capture(key: String, role: String) -> void:
	if key == "02-hub":
		for method: Dictionary in root.get_method_list():
			if "tooltip" in String(method.name) or "cursor" in String(method.name): print("API|", method.name)
		print("HOVER_BEFORE|", root.gui_get_hovered_control())
		if root.has_method("update_mouse_cursor_state"): root.call("update_mouse_cursor_state")
		print("HOVER_AFTER|", root.gui_get_hovered_control())
	await super._capture(key, role)
