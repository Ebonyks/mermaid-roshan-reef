extends SceneTree
## Focused state/input probe for the standalone Day One Stuffie Room lesson.

const ACTIVITY := preload("res://scripts/day_one_stuffie_cleanup.gd")

var failures := 0


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var host := Control.new()
	host.name = "DayOneStuffieCleanupProbeHost"
	host.size = Vector2(1280.0, 720.0)
	get_root().add_child(host)
	var activity := ACTIVITY.new() as DayOneStuffieCleanup
	host.add_child(activity)
	activity.size = host.size
	activity.setup()
	var initial: Dictionary = activity.audit_snapshot()
	_check("two Canvas bunny targets", int(initial.get("target_count", 0)) == 2
		and int(initial.get("bunny_count", 0)) == 2
		and bool(initial.get("canvas_only", false)))
	_check("target and swipe geometry are generous",
		(activity.TARGET_SIZES[0] as Vector2).x >= 110.0
		and float(initial.get("swipe_band", 0.0)) >= 110.0
		and float(initial.get("swipe_min_length", 0.0)) >= 90.0)
	var centers: Array = initial.get("target_centers", []) as Array
	_check("targets align to authored playroom pins", centers.size() == 2
		and centers[0] == Vector2(556.0, 456.0)
		and centers[1] == Vector2(724.0, 456.0))
	_check("approved bunny cards and magic brush load",
		bool(initial.get("brush_present", false)))
	_check("no fail, timer, or text dependency",
		bool(initial.get("no_fail_state", false))
		and bool(initial.get("no_timer", false))
		and bool(initial.get("text_free", false)))
	activity.start()
	var passive_before := activity.audit_snapshot()
	await process_frame
	await process_frame
	var passive_after := activity.audit_snapshot()
	_check("passive demo never advances",
		int(passive_before.get("progress_mask", -1)) == 0
		and int(passive_after.get("progress_mask", -1)) == 0)
	_check("wrong swipe cannot advance",
		not activity._accept_swipe(0, Vector2(20.0, 20.0), Vector2(220.0, 20.0))
		and int(activity.audit_snapshot().get("progress_mask", -1)) == 0)
	_check("wake is a separate first step", activity.probe_wake_next()
		and int(activity.audit_snapshot().get("woken_count", 0)) == 1
		and int(activity.audit_snapshot().get("cleaned_count", 0)) == 0)
	_check("wake alone does not clean",
		not bool(activity.audit_snapshot().get("completed", true))
		and int(activity.audit_snapshot().get("cleaned_count", 0)) == 0)
	_check("first valid crossed swipe cleans one",
		activity.probe_swipe_next()
		and int(activity.audit_snapshot().get("cleaned_count", 0)) == 1
		and int(activity.audit_snapshot().get("progress_mask", -1)) == 1)
	_check("second target also requires wake then swipe",
		activity.probe_complete_current()
		and int(activity.audit_snapshot().get("cleaned_count", 0)) == 2
		and bool(activity.audit_snapshot().get("completed", false)))
	var restored := ACTIVITY.new() as DayOneStuffieCleanup
	host.add_child(restored)
	restored.size = host.size
	restored.setup(1)
	_check("restored two-bit mask preserves clean state",
		int(restored.audit_snapshot().get("woken_count", 0)) == 0
		and int(restored.audit_snapshot().get("cleaned_count", 0)) == 1
		and int(restored.audit_snapshot().get("progress_mask", -1)) == 1)
	restored.cancel_touch()
	_check("touch cancellation clears ownership",
		not bool(restored.audit_snapshot().get("touch_active", true)))
	activity.teardown()
	restored.teardown()
	host.queue_free()
	await process_frame
	print("DAY_ONE_STUFFIE_CLEANUP|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_STUFFIE_CLEANUP|", label, ": ", "OK" if ok else "FAIL")
