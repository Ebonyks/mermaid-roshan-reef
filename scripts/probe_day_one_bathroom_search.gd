extends SceneTree
## Standalone no-fail/touch/save probe for the Day One Bathroom search.

const SEARCH_SCRIPT: Script = preload("res://scripts/day_one_bathroom_search.gd")

var failures: int = 0
var progress_events: Array[int] = []
var completed_events: int = 0
var activity: Control


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	activity = SEARCH_SCRIPT.new() as Control
	root.add_child(activity)
	await process_frame
	activity.call("setup", 0)
	activity.connect("progress_changed", _on_progress_changed)
	activity.connect("completed", _on_completed)
	activity.call("start")
	_check_snapshot("initial", 0, false)
	for _frame: int in range(20):
		await process_frame
	_check_snapshot("passive", 0, false)
	_check(bool(activity.call("probe_reveal_next")), "first reveal")
	_check(bool(activity.call("probe_reveal_next")), "second reveal")
	_check(bool(activity.call("probe_reveal_next")), "third reveal")
	_check_snapshot("complete", 7, true)
	_check(completed_events == 1, "completion emits once")
	_check(progress_events.has(1) and progress_events.has(3) \
		and progress_events.has(7), "progress is monotonic")
	activity.call("stop")
	activity.call("setup", 5)
	activity.call("start")
	_check(bool(activity.call("probe_reveal_next")),
		"restored mask reveals remaining supply")
	_check_snapshot("restored complete", 7, true)
	activity.call("teardown")
	await process_frame
	print("BATHROOM_SEARCH|RESULT: ", "PASS" if failures == 0 else "FAIL",
		" failures=", failures)
	quit(1 if failures > 0 else 0)


func _check_snapshot(label: String, mask: int, completed_state: bool) -> void:
	var snapshot: Dictionary = activity.call("audit_snapshot") as Dictionary
	_check(int(snapshot.get("progress_mask", -1)) == mask, label + " mask")
	_check(bool(snapshot.get("completed", false)) == completed_state,
		label + " completion")
	_check(bool(snapshot.get("canvas_only", false)), label + " Canvas only")
	_check(bool(snapshot.get("one_finger", false)), label + " one finger")
	_check(bool(snapshot.get("no_fail_state", false)), label + " no fail")
	_check(bool(snapshot.get("no_timer", false)), label + " no timer")


func _check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("BATHROOM_SEARCH|", label, ": ", "OK" if ok else "FAIL")


func _on_progress_changed(mask: int) -> void:
	progress_events.append(mask)


func _on_completed() -> void:
	completed_events += 1
