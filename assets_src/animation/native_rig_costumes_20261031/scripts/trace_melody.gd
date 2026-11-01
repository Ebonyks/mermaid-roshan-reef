extends "res://scripts/probe_melody.gd"
## Read-only input diagnostic: inherited assertions and timing remain unchanged.

func _push_touch(position: Vector2, pressed: bool, index: int,
		device: int = 0, canceled: bool = false) -> void:
	if index in [TOUCH_INDEX + 10, TOUCH_INDEX + 70, TOUCH_INDEX + 71, TOUCH_INDEX + 72]:
		_trace_input("before", position, pressed, index, device, canceled)
	super._push_touch(position, pressed, index, device, canceled)
	if index in [TOUCH_INDEX + 10, TOUCH_INDEX + 70, TOUCH_INDEX + 71, TOUCH_INDEX + 72]:
		_trace_input("after", position, pressed, index, device, canceled)


func _trace_input(stage: String, position: Vector2, pressed: bool,
		index: int, device: int, canceled: bool) -> void:
	var snapshot: Dictionary = melody.audit_snapshot()
	var point: Vector2 = melody.active_note_screen_point()
	var hit: Rect2 = melody.active_note_hit_rect()
	print("MELODY_DIAGNOSTIC|", JSON.stringify({
		"stage":stage,"position":[position.x,position.y],"pressed":pressed,
		"index":index,"device":device,"canceled":canceled,
		"progress":melody.progress_count(),"note_point":[point.x,point.y],
		"hits_current_note":hit.has_point(position),
		"green":melody.timing_zone_screen_rect().has_point(point),
		"snapshot":snapshot
	}))
