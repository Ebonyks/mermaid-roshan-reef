extends SceneTree

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const DoorCue := preload("res://scripts/castle_door_cue.gd")

var failures := 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var completed: Array[String] = []
	for current_id: String in DoorLanguage.ACT_ONE_DESTINATIONS:
		var states: Dictionary = _act_one_states(current_id, completed, false)
		_check("one highlight while " + current_id + " is current",
			_highlight_count(states) == 1)
		_check(current_id + " is the sole rainbow plot door",
			String(states[current_id]) == DoorLanguage.PLOT
			and _highlight_id(states) == current_id)
		for completed_id: String in completed:
			_check(completed_id + " stays quiet open",
				String(states[completed_id]) == DoorLanguage.OPEN)
		var current_index: int = DoorLanguage.ACT_ONE_DESTINATIONS.find(
			current_id)
		for future_index: int in range(current_index + 1,
				DoorLanguage.ACT_ONE_DESTINATIONS.size()):
			var future_id: String = DoorLanguage.ACT_ONE_DESTINATIONS[
				future_index]
			_check(future_id + " stays fog blocked",
				String(states[future_id]) == DoorLanguage.BLOCKED)
		completed.append(current_id)

	var baby_eagle_states: Dictionary = _act_one_states(
		"playroom", ["bubble_bath", "mermaid_pool"], false)
	_check("Baby Eagle rescue is plot, never bonus",
		String(baby_eagle_states["playroom"]) == DoorLanguage.PLOT)
	_check("unrelated early rooms stay blocked",
		String(baby_eagle_states["kitchen"]) == DoorLanguage.BLOCKED
		and String(baby_eagle_states["library"]) == DoorLanguage.BLOCKED
		and String(baby_eagle_states["opera_hall"])
			== DoorLanguage.BLOCKED)

	var boss_states: Dictionary = _act_one_states("", completed, true)
	_check("boss handoff has one highlight",
		_highlight_count(boss_states) == 1)
	_check("Royal Hall becomes the sole plot door after four rooms",
		_highlight_id(boss_states) == DoorLanguage.ROYAL_HALL_ID
		and String(boss_states[DoorLanguage.ROYAL_HALL_ID])
			== DoorLanguage.PLOT)
	for completed_id: String in completed:
		_check(completed_id + " remains open at boss handoff",
			String(boss_states[completed_id]) == DoorLanguage.OPEN)

	var bonus_states: Dictionary = {}
	for destination_id: String in DoorLanguage.CASTLE_DESTINATIONS:
		bonus_states[destination_id] = DoorLanguage.resolve_act_one(
			destination_id, "mermaid_pool", ["bubble_bath"], false,
			DoorLanguage.BONUS)
	_check("optional arbitration still permits only one red highlight",
		_highlight_count(bonus_states) == 1
		and _highlight_id(bonus_states) == "mermaid_pool"
		and String(bonus_states["mermaid_pool"]) == DoorLanguage.BONUS)
	_check("bonus cue retains its slow red glow",
		DoorCue.BONUS_GLOW_COLOR.r > DoorCue.BONUS_GLOW_COLOR.g
		and DoorCue.BONUS_GLOW_COLOR.r > DoorCue.BONUS_GLOW_COLOR.b
		and DoorCue.BONUS_PERIOD_SECONDS >= 4.0)
	_check("plot cue retains its restrained gold glow",
		DoorCue.PLOT_GLOW_COLOR.r > DoorCue.PLOT_GLOW_COLOR.b
		and DoorCue.PLOT_GLOW_COLOR.g > DoorCue.PLOT_GLOW_COLOR.b
		and DoorCue.PLOT_PERIOD_SECONDS >= 3.0)

	_check("unknown direct routes fail closed",
		DoorLanguage.resolve_act_one("retired_backdoor", "bubble_bath", [],
			false) == DoorLanguage.BLOCKED)
	_check("blocked state cannot travel",
		not DoorLanguage.allows_travel(DoorLanguage.BLOCKED))
	_check("open and highlighted states can travel",
		DoorLanguage.allows_travel(DoorLanguage.OPEN)
		and DoorLanguage.allows_travel(DoorLanguage.BONUS)
		and DoorLanguage.allows_travel(DoorLanguage.PLOT))

	var cue: Control = DoorCue.new() as Control
	root.add_child(cue)
	cue.size = Vector2(180.0, 300.0)
	cue.call("set_door_state", DoorLanguage.PLOT)
	_check("plot glow remains visible and input-transparent",
		cue.visible and cue.is_processing()
		and cue.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	cue.call("set_door_state", DoorLanguage.BONUS)
	_check("bonus glow remains visible and input-transparent",
		cue.visible and cue.is_processing())
	_check("mismatched frame-tracing geometry is removed",
		not cue.has_method("_arch_points")
		and not cue.has_method("_draw_bonus")
		and not cue.has_method("_draw_plot"))
	_check("unified cue has no legacy keyhole child",
		cue.find_child("*Keyhole*", true, false) == null
		and cue.find_child("*LockIcon*", true, false) == null)
	cue.call("set_door_state", DoorLanguage.BLOCKED)
	cue.call("pulse_blocked_feedback")
	_check("blocked fog cue owns local feedback",
		cue.visible and float(cue.get("feedback_time")) > 0.0)
	cue.call("set_door_state", DoorLanguage.OPEN)
	_check("ordinary open has no cue", not cue.visible)
	cue.queue_free()

	if failures == 0:
		print("DOORLANGUAGE|ALL OK")
		quit(0)
	else:
		print("DOORLANGUAGE|FAIL|%d" % failures)
		quit(1)


func _act_one_states(current_id: String, completed: Array[String],
		boss_ready: bool) -> Dictionary:
	var states: Dictionary = {}
	for destination_id: String in DoorLanguage.CASTLE_DESTINATIONS:
		states[destination_id] = DoorLanguage.resolve_act_one(
			destination_id, current_id, completed, boss_ready)
	return states


func _highlight_count(states: Dictionary) -> int:
	var count := 0
	for state_value: Variant in states.values():
		if DoorLanguage.is_highlighted(String(state_value)):
			count += 1
	return count


func _highlight_id(states: Dictionary) -> String:
	for destination_value: Variant in states.keys():
		var destination_id: String = String(destination_value)
		if DoorLanguage.is_highlighted(String(states[destination_id])):
			return destination_id
	return ""


func _check(label: String, passed: bool) -> void:
	if passed:
		print("DOORLANGUAGE|OK|" + label)
	else:
		failures += 1
		print("DOORLANGUAGE|FAIL|" + label)
