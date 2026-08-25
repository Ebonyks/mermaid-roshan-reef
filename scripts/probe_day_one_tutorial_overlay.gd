extends SceneTree

## Focused contract for the standalone Day One tutorial surface.
## This probe intentionally does not complete a room or write progress: the
## overlay is only allowed to teach, consume, and release its reasoned gate.

const OVERLAY := preload("res://scripts/day_one_tutorial_overlay.gd")
const REASON: String = "day_one_tutorial"

var failures: int = 0
var main: ReefMain = null
var overlay: DayOneTutorialOverlay = null
var skipped: Array[Vector2] = []


func _init() -> void:
	main = ReefMain.new()
	get_root().add_child(main)
	await process_frame
	overlay = OVERLAY.new() as DayOneTutorialOverlay
	main.add_child(overlay)
	var custom: Array[Dictionary] = [
		{"id": "tap_test", "gesture": "tap", "tool": "magnifier",
			"target": Vector2(420, 320), "message": "", "voice": ""},
		{"id": "swipe_test", "gesture": "swipe", "tool": "brush",
			"start": Vector2(300, 340), "end": Vector2(760, 340),
			"target": Vector2(530, 340), "message": "", "voice": ""},
	]
	overlay.tutorial_skipped.connect(_on_skipped)
	overlay.setup(main, "bathroom", custom)
	_check("overlay starts active", bool(overlay.audit_snapshot().get("active", false)))
	_check("overlay owns the reasoned main gate",
		main.touch_control_blocks.has(REASON)
		and not main.touch_ui.world_controls_enabled)
	_check("overlay is Canvas-only and progress-neutral",
		bool(overlay.audit_snapshot().get("canvas_only", false))
		and bool(overlay.audit_snapshot().get("no_progress_owner", false)))
	var first_index: int = int(overlay.audit_snapshot().get("segment_index", -1))
	_inject_press(Vector2(32, 44), 41)
	_check("one press advances exactly one segment",
		int(overlay.audit_snapshot().get("segment_index", -1)) == first_index + 1
		and skipped.size() == 1)
	_check("skip press does not tap through", skipped.size() == 1
		and int(overlay.audit_snapshot().get("segment_index", -1)) == 1
		and bool(overlay.audit_snapshot().get("last_press_consumed", false)))
	await process_frame
	_check("swipe demo animates", float(overlay.audit_snapshot().get(
		"demo_progress", 0.0)) >= 0.0)
	_inject_press(Vector2(1200, 680), 42)
	_check("last segment finishes on one press", not bool(
		overlay.audit_snapshot().get("active", true)))
	_check("finish releases only its gate", not main.touch_control_blocks.has(REASON))
	_check("world controls restore after finish", main.touch_ui.world_controls_enabled)
	var autoplay: Array[Dictionary] = [
		{"id": "autoplay_test", "gesture": "tap", "tool": "rainbow",
			"target": Vector2(640, 360), "message": "", "voice": ""},
	]
	overlay.setup(main, "pool", autoplay)
	overlay._process(DayOneTutorialOverlay.SEGMENT_DURATION)
	await process_frame
	_check("a watched segment advances and finishes without input",
		not bool(overlay.audit_snapshot().get("active", true))
		and not main.touch_control_blocks.has(REASON))
	_check_presets()
	overlay = null
	main.free()
	print("DAY_ONE_TUTORIAL_OVERLAY|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _inject_press(position: Vector2, index: int) -> void:
	var press := InputEventScreenTouch.new()
	press.index = index
	press.position = position
	press.pressed = true
	overlay._gui_input(press)
	var release := InputEventScreenTouch.new()
	release.index = index
	release.position = position
	release.pressed = false
	overlay._gui_input(release)


func _on_skipped(_event_id: String, _segment_index: int) -> void:
	# The actual touch position is checked independently by the overlay's
	# consumed GUI event; this signal only proves one segment was skipped.
	skipped.append(Vector2(float(skipped.size()), 0.0))


func _check_presets() -> void:
	for event_id: String in ["bathroom", "art", "stuffie", "pool", "boss"]:
		var preset: Array[Dictionary] = DayOneTutorialOverlay.preset_segments(event_id)
		_check("%s has configured segments" % event_id, not preset.is_empty())
		for segment: Dictionary in preset:
			_check("%s segment has a gesture" % event_id,
				String(segment.get("gesture", "")) in ["tap", "swipe", "drag"])
			_check("%s segment has a target" % event_id,
				segment.has("target"))


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_TUTORIAL_OVERLAY|", label, ": ", "OK" if ok else "FAIL")
