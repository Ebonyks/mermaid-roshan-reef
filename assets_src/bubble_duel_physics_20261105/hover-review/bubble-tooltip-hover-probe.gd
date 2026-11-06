extends "res://scripts/probe_bubble_duel_capture.gd"
func _capture(key: String, role: String) -> void:
	if key != "01-elevator" and venue != null and venue.bubble_duel != null:
		for button: Button in venue.buttons: button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	await super._capture(key, role)
