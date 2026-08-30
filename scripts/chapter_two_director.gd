class_name ChapterTwoDirector
extends RefCounted

## Additive Chapter 2 progression for Mermaid Roshan's birthday party.
##
## The director owns policy only. Mutable state remains on ReefMain so the
## existing save owner can persist it without replacing any legacy key. Skills
## are granted by the four opening Opera tutorials, but a skill can be used in
## a Castle room only when the exact matching plot objective is active.

signal hook_event(event_name: String, payload: Dictionary)

const ACT_CHEF := 0
const ACT_DETECTIVE := 1
const ACT_BALLERINA := 2
const ACT_CANDY_MAKER := 3
const INITIAL_TUTORIAL_ACTS: Array[int] = [
	ACT_CHEF, ACT_DETECTIVE, ACT_BALLERINA, ACT_CANDY_MAKER,
]
const INITIAL_TUTORIAL_MASK := 0x0F

const SKILL_CHEF := "chef"
const SKILL_DETECTIVE := "detective"
const SKILL_BALLERINA := "ballerina"
const SKILL_CANDY_MAKER := "candy_maker"

const OBJECTIVE_OPERA_TUTORIALS := "opera_tutorials"
const OBJECTIVE_FIND_RAINBOW_CANDLE := "find_rainbow_candle"
const OBJECTIVE_STUFFIE_BALLET := "stuffie_ballet"

const PLOT_CONTEXT_STUFFIE_BALLET := "chapter2_stuffie_ballet"

const ACTION_DETECTIVE_SEARCH := "detective_search"
const ACTION_STUFFIE_BALLET := "stuffie_ballet"

const EVENT_CHAPTER_STARTED := "chapter2_started"
const EVENT_SKILL_LEARNED := "chapter2_skill_learned"
const EVENT_OBJECTIVE_CHANGED := "chapter2_objective_changed"
const EVENT_RAINBOW_CANDLE_FOUND := "chapter2_rainbow_candle_found"
const EVENT_STUFFIE_BALLET_COMPLETED := "chapter2_stuffie_ballet_completed"

var m: ReefMain

var active: bool:
	get:
		return m.chapter2_active
	set(value):
		m.chapter2_active = value
var unlocked_opera_mask: int:
	get:
		return m.chapter2_unlocked_opera_mask
	set(value):
		m.chapter2_unlocked_opera_mask = value
var skill_mask: int:
	get:
		return m.chapter2_skill_mask
	set(value):
		m.chapter2_skill_mask = value
var active_objective: String:
	get:
		return m.chapter2_active_objective
	set(value):
		m.chapter2_active_objective = value
var rainbow_candle_found: bool:
	get:
		return m.chapter2_rainbow_candle_found
	set(value):
		m.chapter2_rainbow_candle_found = value
var stuffie_ballet_done: bool:
	get:
		return m.chapter2_stuffie_ballet_done
	set(value):
		m.chapter2_stuffie_ballet_done = value
var event_seen: Dictionary:
	get:
		return m.chapter2_event_seen
	set(value):
		m.chapter2_event_seen = value
var event_history: Array[Dictionary]:
	get:
		return m.chapter2_event_history
	set(value):
		m.chapter2_event_history = value


func _init(main: ReefMain) -> void:
	m = main
	event_seen.clear()
	event_history.clear()
	_normalise_state({})


func start_after_boss() -> bool:
	if active or not m.day_one_giant_dust_bunny_boss_defeated:
		return false
	active = true
	unlocked_opera_mask = INITIAL_TUTORIAL_MASK
	skill_mask |= m.opera_stars & INITIAL_TUTORIAL_MASK
	_sync_objective()
	_emit_once(EVENT_CHAPTER_STARTED, {
		"objective": active_objective,
		"unlocked_acts": initial_tutorial_act_indices(),
	})
	return true


func initial_tutorial_act_indices() -> Array[int]:
	return INITIAL_TUTORIAL_ACTS.duplicate()


func can_start_opera_tutorial(act_index: int) -> bool:
	return active and INITIAL_TUTORIAL_ACTS.has(act_index) \
		and (unlocked_opera_mask & (1 << act_index)) != 0


func is_opera_priority() -> bool:
	return active and active_objective == OBJECTIVE_OPERA_TUTORIALS


func has_skill(skill_id: String) -> bool:
	var act_index := _act_for_skill(skill_id)
	return act_index >= 0 and (skill_mask & (1 << act_index)) != 0


func record_opera_completion(act_index: int,
		plot_context: String = "") -> bool:
	if not active:
		return false
	if plot_context == PLOT_CONTEXT_STUFFIE_BALLET:
		return complete_stuffie_ballet(act_index)
	if plot_context != "" or not INITIAL_TUTORIAL_ACTS.has(act_index):
		return false
	var bit := 1 << act_index
	var learned_now := (skill_mask & bit) == 0
	skill_mask |= bit
	if learned_now:
		_emit_once(EVENT_SKILL_LEARNED, {
			"act_index": act_index,
			"skill_id": _skill_for_act(act_index),
		})
	var previous_objective := active_objective
	_sync_objective()
	_emit_objective_change(previous_objective)
	return learned_now or previous_objective != active_objective


func room_plot_action(room_id: String) -> String:
	if not active:
		return ""
	match active_objective:
		OBJECTIVE_FIND_RAINBOW_CANDLE:
			if room_id == "library" and has_skill(SKILL_DETECTIVE):
				return ACTION_DETECTIVE_SEARCH
		OBJECTIVE_STUFFIE_BALLET:
			if room_id == "playroom" and has_skill(SKILL_BALLERINA):
				return ACTION_STUFFIE_BALLET
	return ""


func complete_detective_search() -> bool:
	if room_plot_action("library") != ACTION_DETECTIVE_SEARCH:
		return false
	rainbow_candle_found = true
	# Chapter 2 only discovers and safeguards the candle. Its dramatic rainbow
	# lighting belongs to a later chapter, so this chapter never mutates lit state.
	var previous_objective := active_objective
	_sync_objective()
	_emit_once(EVENT_RAINBOW_CANDLE_FOUND, {
		"room_id": "library",
		"hiding_place": "magic_storybook",
		"lit": false,
	})
	_emit_objective_change(previous_objective)
	return true


func can_start_stuffie_ballet() -> bool:
	return room_plot_action("playroom") == ACTION_STUFFIE_BALLET


func complete_stuffie_ballet(act_index: int) -> bool:
	if act_index != ACT_BALLERINA or not can_start_stuffie_ballet() \
			or stuffie_ballet_done:
		return false
	stuffie_ballet_done = true
	var previous_objective := active_objective
	_sync_objective()
	_emit_once(EVENT_STUFFIE_BALLET_COMPLETED, {
		"room_id": "playroom",
		"act_index": act_index,
	})
	_emit_objective_change(previous_objective)
	return true


func should_show_candle(room_id: String) -> bool:
	return active and room_id == "library" and rainbow_candle_found


func can_launch_plot_act(room_id: String, act_index: int,
		plot_context: String) -> bool:
	return plot_context == PLOT_CONTEXT_STUFFIE_BALLET \
		and room_id == "playroom" and act_index == ACT_BALLERINA \
		and can_start_stuffie_ballet()


func opera_config_overrides(plot_context: String,
		act_index: int = -1) -> Dictionary:
	if plot_context == "" and can_start_opera_tutorial(act_index):
		return {
			"chapter2_tutorial": true,
			"win_line": "Roshan learned a new party sparkle at the Opera House!",
		}
	if plot_context != PLOT_CONTEXT_STUFFIE_BALLET:
		return {}
	return {
		"chapter2_context": PLOT_CONTEXT_STUFFIE_BALLET,
		"chapter2_scene": "stuffie_room",
		"name": "The Stuffie Birthday Ballet",
		"voice": "Ballerina Roshan! Lead your stuffie friends through their birthday dance!",
		"win_line": "Roshan leads every stuffie through the birthday ballet!",
	}


func serialize_state() -> Dictionary:
	return {
		"chapter2_active": active,
		"chapter2_unlocked_opera_mask": unlocked_opera_mask,
		"chapter2_skill_mask": skill_mask,
		"chapter2_active_objective": active_objective,
		"chapter2_rainbow_candle_found": rainbow_candle_found,
		"chapter2_stuffie_ballet_done": stuffie_ballet_done,
	}


func restore_state(raw: Variant) -> void:
	_normalise_state(raw as Dictionary if raw is Dictionary else {})
	event_seen.clear()
	event_history.clear()


func _normalise_state(source: Dictionary) -> void:
	var normalised := normalise_save_patch(source, m.opera_stars)
	active = bool(normalised.get("chapter2_active", false))
	unlocked_opera_mask = int(normalised.get(
		"chapter2_unlocked_opera_mask", 0))
	skill_mask = int(normalised.get("chapter2_skill_mask", 0))
	active_objective = String(normalised.get(
		"chapter2_active_objective", ""))
	rainbow_candle_found = bool(normalised.get(
		"chapter2_rainbow_candle_found", false))
	stuffie_ballet_done = bool(normalised.get(
		"chapter2_stuffie_ballet_done", false))


static func normalise_save_patch(raw: Variant, opera_star_mask: int) -> Dictionary:
	var source: Dictionary = raw as Dictionary if raw is Dictionary else {}
	var boss_defeated := _bool_static(
		source, "day_one_giant_dust_bunny_boss_defeated", false)
	# Chapter 2 currently has no completed/inactive state. Heal a save written
	# between boss defeat and the chapter-start event instead of skipping it.
	var chapter_active := boss_defeated
	var unlocked_mask := _nonnegative_int_static(source,
		"chapter2_unlocked_opera_mask",
		INITIAL_TUTORIAL_MASK if chapter_active else 0) \
		& INITIAL_TUTORIAL_MASK
	if chapter_active:
		unlocked_mask |= INITIAL_TUTORIAL_MASK
	var learned_mask := _nonnegative_int_static(
		source, "chapter2_skill_mask", 0) \
		& INITIAL_TUTORIAL_MASK
	if chapter_active:
		learned_mask |= opera_star_mask & INITIAL_TUTORIAL_MASK
	var all_tutorials_done := chapter_active \
		and (learned_mask & INITIAL_TUTORIAL_MASK) == INITIAL_TUTORIAL_MASK
	var candle_found := all_tutorials_done and _bool_static(
		source, "chapter2_rainbow_candle_found", false)
	var ballet_done := candle_found and _bool_static(
		source, "chapter2_stuffie_ballet_done", false)
	var objective := _derived_objective_static(
		chapter_active, all_tutorials_done, candle_found, ballet_done)
	return {
		"chapter2_active": chapter_active,
		"chapter2_unlocked_opera_mask": unlocked_mask,
		"chapter2_skill_mask": learned_mask,
		"chapter2_active_objective": objective,
		"chapter2_rainbow_candle_found": candle_found,
		"chapter2_stuffie_ballet_done": ballet_done,
	}


static func _bool_static(source: Dictionary, key: String,
		default_value: bool) -> bool:
	var value: Variant = source.get(key, default_value)
	return bool(value) if typeof(value) == TYPE_BOOL else default_value


static func _nonnegative_int_static(source: Dictionary, key: String,
		default_value: int) -> int:
	var value: Variant = source.get(key, default_value)
	if typeof(value) == TYPE_INT:
		return int(value) if int(value) >= 0 else default_value
	if typeof(value) == TYPE_FLOAT:
		var number := float(value)
		if is_finite(number) and number >= 0.0 and number == floorf(number):
			return int(number)
	return default_value


static func _derived_objective_static(chapter_active: bool,
		all_tutorials_done: bool, candle_found: bool,
		ballet_done: bool) -> String:
	if not chapter_active:
		return ""
	if not all_tutorials_done:
		return OBJECTIVE_OPERA_TUTORIALS
	if not candle_found:
		return OBJECTIVE_FIND_RAINBOW_CANDLE
	if not ballet_done:
		return OBJECTIVE_STUFFIE_BALLET
	return ""


func _sync_objective() -> void:
	skill_mask |= m.opera_stars & INITIAL_TUTORIAL_MASK
	active_objective = _derived_objective_static(
		active,
		(skill_mask & INITIAL_TUTORIAL_MASK) == INITIAL_TUTORIAL_MASK,
		rainbow_candle_found,
		stuffie_ballet_done)


func _emit_objective_change(previous_objective: String) -> void:
	if previous_objective == active_objective:
		return
	_emit_once(EVENT_OBJECTIVE_CHANGED, {
		"from": previous_objective,
		"objective": active_objective,
	})


func _skill_for_act(act_index: int) -> String:
	match act_index:
		ACT_CHEF:
			return SKILL_CHEF
		ACT_DETECTIVE:
			return SKILL_DETECTIVE
		ACT_BALLERINA:
			return SKILL_BALLERINA
		ACT_CANDY_MAKER:
			return SKILL_CANDY_MAKER
	return ""


func _act_for_skill(skill_id: String) -> int:
	match skill_id:
		SKILL_CHEF:
			return ACT_CHEF
		SKILL_DETECTIVE:
			return ACT_DETECTIVE
		SKILL_BALLERINA:
			return ACT_BALLERINA
		SKILL_CANDY_MAKER:
			return ACT_CANDY_MAKER
	return -1


func _emit_once(event_name: String, payload: Dictionary) -> void:
	var discriminator := String(payload.get(
		"skill_id", payload.get("objective", payload.get("flame", ""))))
	var event_id := "%s:%s" % [event_name, discriminator]
	if bool(event_seen.get(event_id, false)):
		return
	event_seen[event_id] = true
	var record := {
		"event": event_name,
		"payload": payload.duplicate(true),
	}
	event_history.append(record)
	hook_event.emit(event_name, payload.duplicate(true))
