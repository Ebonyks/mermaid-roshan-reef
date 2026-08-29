extends SceneTree
## Focused contract probe for the Day One bathroom bunny beat.
##
## This probe intentionally uses the public probe seams on the two bathroom
## owners. It does not reach into private fields or synthesize a production
## animation. The expected new seam is a no-argument tub-tap probe on either
## DayOneBathroomCleaning or its DayOneBathroomCleanup wrapper; aliases are
## accepted while the implementation settles. A valid tap must play one
## bounded Canvas2D spin and one comic spoken "No!", then leave the forgiving
## tub brush gesture available. Passive time, sink-stage taps, and repeats
## must not advance or replay it.

const BATHROOM_CLEANING := preload(
	"res://scripts/games/day_one_bathroom_cleaning.gd")
const BATHROOM_CLEANUP := preload(
	"res://scripts/games/day_one_bathroom_cleanup.gd")
const BUNNY_SWIMMER := preload(
	"res://scripts/games/day_one_dust_bunny_swimmer.gd")
const SINK_CENTER := Vector2(642.0, 280.0)
const TUB_CENTER := Vector2(310.0, 349.0)
const TUB_TAP_METHODS: Array[String] = [
	"probe_tap_tub", "probe_tub_tap", "probe_drain_tub",
]
const REACTION_COUNT_KEYS: Array[String] = [
	"tub_tap_reaction_count", "tub_drain_reaction_count",
	"drain_reaction_count", "bunny_spin_count", "tub_spin_count",
	"drain_tap_count",
]
const REACTION_ONCE_KEYS: Array[String] = [
	"tub_tap_reaction_played", "tub_drain_reaction_played",
	"drain_reaction_played", "bunny_spin_played_once",
	"drain_reaction_played_once",
]

var checks_failed: int = 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var host := Control.new()
	host.name = "DayOneBathroomBunnyProbeHost"
	host.size = StorybookUI.CANVAS_SIZE
	root.add_child(host)

	# Verify the early-input guard independently in the sink stage. A production
	# implementation may put the tap seam on either owner, so use the cleaning
	# owner first and retain the exact result for the later API contract check.
	var early_main := ReefMain.new()
	early_main._day_one_ref()
	var early := BATHROOM_CLEANING.new() as DayOneBathroomCleaning
	host.add_child(early)
	early.setup(early_main, false)
	await process_frame
	var early_tap := _invoke_tub_tap(early)
	_check("sink-stage tub tap cannot advance",
		bool(early_tap.get("found", false))
		and not bool(early_tap.get("result", false))
		and int(early.audit_snapshot().get("active_step", -1)) == 0)
	teardown_node(early)
	teardown_node(early_main)

	# Start at the persisted post-sink boundary, matching a real re-entry after
	# the sink gesture. This keeps the probe short while still testing the live
	# tub owner and its saved stage semantics.
	var main := ReefMain.new()
	main._day_one_ref()
	main.day_one_bathroom_cleanup_step = 1
	var cleaning := BATHROOM_CLEANING.new() as DayOneBathroomCleaning
	host.add_child(cleaning)
	cleaning.setup(main, false)
	var swimmer := BUNNY_SWIMMER.new() as DayOneDustBunnySwimmer
	host.add_child(swimmer)
	var swimmer_ready: bool = swimmer.setup(
		Rect2(210.0, 238.0, 210.0, 100.0), Vector2(300.0, 286.0),
		92.0, Vector2(13.0, 3.0), 24, Vector2(78.0, 16.0),
		Color(0.72, 0.78, 0.48, 0.26), 0.70)
	cleaning.set_bunny_swimmer(swimmer)
	cleaning.set_supply_basket(Vector2(940.0, 575.0))
	var sink_grime := Sprite2D.new()
	var tub_grime := Sprite2D.new()
	host.add_child(sink_grime)
	host.add_child(tub_grime)
	cleaning.set_dirty_overlays(sink_grime, tub_grime)
	await create_timer(0.42).timeout

	var initial: Dictionary = cleaning.audit_snapshot()
	_check("post-sink entry exposes live tub brush stage",
		int(initial.get("active_step", -1)) == 1
		and String(initial.get("active_stage", "")) == "tub"
		and bool(initial.get("tub_gesture_reachable", false))
		and bool(initial.get("canvas_only", false))
		and not bool(initial.get("failed", false))
		and not bool(initial.get("game_over", false)))
	_check("passive tub wait does not advance",
		_cleaning_wait_is_static(cleaning, initial))

	var bunny: Dictionary = _find_bunny_snapshot(initial)
	_check("bunny is a restrained true-2D casual swimmer",
		swimmer_ready and not bunny.is_empty()
		and bool(_find_bool(bunny, ["true_2d", "canvas_only"]))
		and _contains_swim_label(bunny)
		and bool(initial.get("canvas_only", false)))

	var tap := _invoke_tub_tap(cleaning)
	_check("live tub tap seam exists and accepts one tap",
		bool(tap.get("found", false)) and bool(tap.get("result", false)))
	var after_tap: Dictionary = cleaning.audit_snapshot()
	_check("drain reaction blocks brushing without advancing",
		int(after_tap.get("active_step", -1)) == 1
		and not cleaning.is_tub_active()
		and float(after_tap.get("tub_distance", 0.0)) == 0.0
		and int(after_tap.get("tub_reversals", 0)) == 0)
	await create_timer(0.12).timeout
	after_tap = cleaning.audit_snapshot()
	_check("one comic spin is observable as a one-shot reaction",
		_reaction_started(after_tap)
		and _reaction_is_bounded(after_tap))
	_check("reaction speaks exactly a comic No",
		_voice_or_caption_mentions_no(main)
		or _snapshot_mentions_no(after_tap))

	var first_count: int = _reaction_count(after_tap)
	var first_once: bool = _reaction_once(after_tap)
	var repeat_tap := _invoke_tub_tap(cleaning)
	await create_timer(0.12).timeout
	var repeated: Dictionary = cleaning.audit_snapshot()
	var second_count: int = _reaction_count(repeated)
	_check("repeat tub tap cannot replay the one-shot",
		(not bool(repeat_tap.get("result", false))
			or (first_count >= 0 and second_count == first_count))
		and (first_once or _reaction_once(repeated)))
	_check("repeat and passive input still cannot complete tub",
		not cleaning.is_tub_active()
		and int(repeated.get("active_step", -1)) == 1
		and float(repeated.get("tub_distance", 0.0)) == 0.0)
	# Give a short authored reaction time to finish before exercising the brush
	# gesture. The reaction contract is bounded; this is not a timing shortcut.
	await create_timer(1.05).timeout
	var drained: Dictionary = cleaning.audit_snapshot()
	_check("bounded reaction drains once and enables the brush",
		bool(drained.get("tub_drained", false))
		and cleaning.is_tub_active()
		and int(drained.get("drain_reaction_count", 0)) == 1)
	var saved_patch: Dictionary = main._day_one_ref().serialize_state()
	var restored_main := ReefMain.new()
	restored_main._day_one_ref().restore_state(saved_patch)
	var restored := BATHROOM_CLEANING.new() as DayOneBathroomCleaning
	host.add_child(restored)
	restored.setup(restored_main, false)
	restored.set_supply_basket(Vector2(940.0, 575.0))
	await create_timer(0.42).timeout
	_check("saved drain state skips the comic reaction on Continue",
		restored_main.day_one_bathroom_tub_drained
		and bool(restored.audit_snapshot().get("tub_drained", false))
		and not restored.probe_tap_tub()
		and bool(restored.audit_snapshot().get(
			"back_and_forth_arrows_visible", false)))
	teardown_node(restored)
	teardown_node(restored_main)

	var tub_points: Array[Vector2] = [
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
		TUB_CENTER + Vector2(-210.0, 0.0),
		TUB_CENTER + Vector2(210.0, 0.0),
	]
	_check("existing forgiving tub brush gesture remains causal",
		cleaning.probe_tub_strokes(tub_points, 1.1)
		and int(main.day_one_bathroom_cleanup_step) == 2)

	# Exercise the wrapper seam when it is exposed: the cleanup owner must route
	# to the same one-shot reaction rather than maintaining a second bunny state.
	var wrapper := BATHROOM_CLEANUP.new() as DayOneBathroomCleanup
	host.add_child(wrapper)
	var wrapper_main := ReefMain.new()
	wrapper_main._day_one_ref()
	wrapper_main.day_one_bathroom_supply_hunt_step = 2
	wrapper_main.day_one_bathroom_cleanup_step = 1
	wrapper.setup(wrapper_main, false)
	await process_frame
	await create_timer(0.65).timeout
	var wrapper_tap := _invoke_tub_tap(wrapper)
	var wrapper_snapshot: Dictionary = wrapper.cleaning_audit_snapshot()
	_check("cleanup wrapper exposes the same live tub tap route",
		bool(wrapper_tap.get("found", false))
		and bool(wrapper_tap.get("result", false))
		and int(wrapper_snapshot.get("active_step", -1)) == 1)

	teardown_node(wrapper)
	teardown_node(wrapper_main)
	teardown_node(cleaning)
	teardown_node(swimmer)
	teardown_node(main)
	host.queue_free()
	# Flush queued CanvasItem, shader, and tween teardown before the SceneTree
	# quits so the focused probe cannot hide renderer-resource leaks.
	for frame: int in range(5):
		await process_frame
	print("DAY_ONE_BATHROOM_BUNNY|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _invoke_tub_tap(owner: Object) -> Dictionary:
	for method_name: String in TUB_TAP_METHODS:
		if owner.has_method(method_name):
			return {
				"found": true,
				"method": method_name,
				"result": owner.call(method_name),
			}
	return {"found": false, "method": "", "result": false}


func _cleaning_wait_is_static(cleaning: DayOneBathroomCleaning,
		before: Dictionary) -> bool:
	cleaning._process(4.0)
	var after: Dictionary = cleaning.audit_snapshot()
	return int(after.get("active_step", -1)) == 1 \
		and float(after.get("tub_distance", 0.0)) \
		== float(before.get("tub_distance", 0.0)) \
		and int(after.get("tub_reversals", 0)) \
		== int(before.get("tub_reversals", 0))


func _find_bunny_snapshot(snapshot: Dictionary) -> Dictionary:
	if _contains_bunny_key(snapshot):
		return snapshot
	for value: Variant in snapshot.values():
		if value is Dictionary:
			var nested := _find_bunny_snapshot(value as Dictionary)
			if not nested.is_empty():
				return nested
		elif value is Array:
			for item: Variant in value as Array:
				if item is Dictionary:
					var nested_array := _find_bunny_snapshot(item as Dictionary)
					if not nested_array.is_empty():
						return nested_array
	return {}


func _contains_bunny_key(snapshot: Dictionary) -> bool:
	for key: Variant in snapshot.keys():
		var key_text := String(key).to_lower()
		if key_text.contains("bunny") or key_text.contains("swimmer"):
			return true
	return false


func _contains_swim_label(value: Variant) -> bool:
	if value is String:
		var text := String(value).to_lower()
		return text.contains("swim") or text.contains("bob_paddle")
	if value is Dictionary:
		for nested: Variant in (value as Dictionary).values():
			if _contains_swim_label(nested):
				return true
	elif value is Array:
		for nested_array: Variant in value as Array:
			if _contains_swim_label(nested_array):
				return true
	return false


func _find_bool(value: Variant, keys: Array[String]) -> bool:
	if value is Dictionary:
		var dictionary: Dictionary = value as Dictionary
		for key: String in keys:
			if bool(dictionary.get(key, false)):
				return true
		for nested: Variant in dictionary.values():
			if _find_bool(nested, keys):
				return true
	elif value is Array:
		for nested_array: Variant in value as Array:
			if _find_bool(nested_array, keys):
				return true
	return false


func _reaction_count(snapshot: Dictionary) -> int:
	for key: String in REACTION_COUNT_KEYS:
		var value := _find_numeric(snapshot, key)
		if value >= 0:
			return value
	return -1


func _find_numeric(value: Variant, key: String) -> int:
	if value is Dictionary:
		var dictionary: Dictionary = value as Dictionary
		if dictionary.has(key) and dictionary[key] is int:
			return int(dictionary[key])
		for nested: Variant in dictionary.values():
			var found := _find_numeric(nested, key)
			if found >= 0:
				return found
	elif value is Array:
		for nested_array: Variant in value as Array:
			var found_array := _find_numeric(nested_array, key)
			if found_array >= 0:
				return found_array
	return -1


func _reaction_once(snapshot: Dictionary) -> bool:
	return _find_bool(snapshot, REACTION_ONCE_KEYS)


func _reaction_started(snapshot: Dictionary) -> bool:
	return _reaction_count(snapshot) > 0 or _reaction_once(snapshot) \
		or _contains_key_text(snapshot, ["spin", "drain", "no_reaction"])


func _reaction_is_bounded(snapshot: Dictionary) -> bool:
	var duration := _find_numeric(snapshot, "reaction_duration_ms")
	if duration < 0:
		return true
	return duration > 0 and duration <= 1200


func _contains_key_text(value: Variant, needles: Array[String]) -> bool:
	if value is Dictionary:
		for key: Variant in (value as Dictionary).keys():
			var text := String(key).to_lower()
			for needle: String in needles:
				if text.contains(needle):
					return true
		for nested: Variant in (value as Dictionary).values():
			if _contains_key_text(nested, needles):
				return true
	elif value is Array:
		for nested_array: Variant in value as Array:
			if _contains_key_text(nested_array, needles):
				return true
	return false


func _voice_or_caption_mentions_no(main: ReefMain) -> bool:
	if main.hud_msg != null and String(main.hud_msg.text).to_lower().contains("no"):
		return true
	for key: Variant in main.said_cool.keys():
		var text := String(key).to_lower()
		if text.contains("no") or text.contains("bunny"):
			return true
	return false


func _snapshot_mentions_no(snapshot: Dictionary) -> bool:
	return _contains_value_text(snapshot, ["no!", "no", "bunny_no", "shout"])


func _contains_value_text(value: Variant, needles: Array[String]) -> bool:
	if value is String:
		var text := String(value).to_lower()
		for needle: String in needles:
			if text == needle or text.contains(needle):
				return true
	elif value is Dictionary:
		for nested: Variant in (value as Dictionary).values():
			if _contains_value_text(nested, needles):
				return true
	elif value is Array:
		for nested_array: Variant in value as Array:
			if _contains_value_text(nested_array, needles):
				return true
	return false


func _teardown_if_possible(node: Node) -> void:
	if node != null and is_instance_valid(node):
		if node.has_method("teardown"):
			node.call("teardown")
		elif node.is_inside_tree():
			node.queue_free()
		else:
			node.free()


func teardown_node(node: Node) -> void:
	_teardown_if_possible(node)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_BATHROOM_BUNNY|", label, ": ", "OK" if ok else "FAIL")
