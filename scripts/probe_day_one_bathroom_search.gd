extends SceneTree
## Standalone headless probe for the first Day One bathroom search.

const SEARCH_SCRIPT: Script = preload("res://scripts/day_one_bathroom_search.gd")

var _failures: int = 0
var _progress_events: Array[int] = []
var _completed_events: int = 0
var _activity: DayOneBathroomSearch


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	_activity = SEARCH_SCRIPT.new() as DayOneBathroomSearch
	root.add_child(_activity)
	await process_frame
	_activity.setup(0)
	_activity.progress_changed.connect(_on_progress_changed)
	_activity.completed.connect(_on_completed)
	_activity.start()
	_check_snapshot("initial", 0, false)

	for _frame in range(20):
		await process_frame
	_check_snapshot("passive", 0, false)

	_send_wrong_mouse_tap()
	_check(_activity.audit_snapshot().get("progress_mask", -1) == 0, "wrong area does not progress")
	_check(not bool(_activity.audit_snapshot().get("completed", true)), "wrong area cannot complete")

	_check(_activity.probe_reveal_next(), "probe reveals first supply")
	_check_snapshot("first", 1, false)
	_check(_activity.probe_reveal_next(), "probe reveals second supply")
	_check_snapshot("second", 3, false)
	_check(_activity.probe_reveal_next(), "probe reveals third supply")
	_check_snapshot("complete", 7, true)
	_check(_completed_events == 1, "completed emits once")
	_check(_progress_events.has(1) and _progress_events.has(3) and _progress_events.has(7), "progress emits each mask")
	_check(not _activity.probe_reveal_next(), "completed activity rejects further reveal")

	_activity.stop()
	_activity.setup(5)
	_activity.start()
	_check_snapshot("restored", 5, false)
	_check(_activity.probe_reveal_next(), "restored mask reveals remaining supply")
	_check_snapshot("restored complete", 7, true)
	_check(_completed_events == 2, "restored completion emits once")
	_activity.cancel_touch()
	_check(not bool(_activity.audit_snapshot().get("touch_active", true)), "cancel clears touch ownership")
	_activity.teardown()
	await process_frame
	if _failures == 0:
		print("BATHROOM_SEARCH|RESULT: PASS")
	else:
		print("BATHROOM_SEARCH|RESULT: FAIL|count=%d" % _failures)
	quit(0 if _failures == 0 else 1)


func _send_wrong_mouse_tap() -> void:
	var press: InputEventMouseButton = InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_LEFT
	press.position = Vector2(86.0, 86.0)
	press.pressed = true
	_activity._gui_input(press)
	var release: InputEventMouseButton = InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_LEFT
	release.position = press.position
	release.pressed = false
	_activity._gui_input(release)


func _check_snapshot(label: String, expected_mask: int, expected_completed: bool) -> void:
	var snapshot: Dictionary = _activity.audit_snapshot()
	_check(int(snapshot.get("progress_mask", -1)) == expected_mask, "%s mask" % label)
	_check(bool(snapshot.get("completed", false)) == expected_completed, "%s completion" % label)
	_check(bool(snapshot.get("canvas_only", false)), "%s canvas only" % label)
	_check(bool(snapshot.get("no_fail_state", false)), "%s no fail" % label)
	_check(bool(snapshot.get("no_timer", false)), "%s no timer" % label)
	_check(bool(snapshot.get("one_finger", false)), "%s one finger" % label)
	_check(bool(snapshot.get("revealed_sprites_present", false)), "%s supply sprites" % label)
	print("BATHROOM_SEARCH|SNAPSHOT|%s|mask=%d|completed=%s" % [label, expected_mask, str(expected_completed)])


func _on_progress_changed(mask: int) -> void:
	_progress_events.append(mask)


func _on_completed() -> void:
	_completed_events += 1


func _check(condition: bool, label: String) -> void:
	if condition:
		print("BATHROOM_SEARCH|PASS|%s" % label)
	else:
		_failures += 1
		print("BATHROOM_SEARCH|FAIL|%s" % label)
