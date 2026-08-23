extends SceneTree

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const DoorCue := preload("res://scripts/castle_door_cue.gd")

var failures := 0


func _init() -> void:
	_check("first arrival royal hall is plot",
		_state(DoorLanguage.ROYAL_HALL_ID, false, true, true)
			== DoorLanguage.PLOT)
	_check("first arrival playroom is bonus",
		_state("playroom", false, true, true) == DoorLanguage.BONUS)
	_check("first arrival kitchen is quiet open",
		_state("kitchen", false, true, true) == DoorLanguage.OPEN)
	_check("first arrival library is quiet open",
		_state("library", false, true, true) == DoorLanguage.OPEN)
	for room_id: String in [
			"family_gallery", "opera_hall", "craft_room", "mermaid_pool",
			"bubble_bath", "dining_room", "royal_bedroom",
			"sleepover_bedroom", "movie_lounge"]:
		_check("first arrival seals " + room_id,
			_state(room_id, false, true, true) == DoorLanguage.BLOCKED)
	_check("Crown opens an ordinary sealed room",
		_state("opera_hall", true, true, true) == DoorLanguage.OPEN)
	_check("Playroom stays blue until its saved bonus is collected",
		_state("playroom", true, true, true) == DoorLanguage.BONUS)
	_check("Collected Playroom bonus becomes quiet open",
		_state("playroom", true, false, true) == DoorLanguage.OPEN)
	_check("Royal Hall rests behind mist with no plot",
		_state(DoorLanguage.ROYAL_HALL_ID, true, false, false)
			== DoorLanguage.BLOCKED)
	_check("Unknown direct routes fail closed",
		_state("retired_backdoor", true, false, false)
			== DoorLanguage.BLOCKED)
	_check("Blocked state cannot travel",
		not DoorLanguage.allows_travel(DoorLanguage.BLOCKED))
	_check("All three visitable states can travel",
		DoorLanguage.allows_travel(DoorLanguage.OPEN)
		and DoorLanguage.allows_travel(DoorLanguage.BONUS)
		and DoorLanguage.allows_travel(DoorLanguage.PLOT))
	var cue := DoorCue.new()
	root.add_child(cue)
	cue.size = Vector2(180.0, 300.0)
	cue.set_door_state(DoorLanguage.BLOCKED)
	_check("Cue is input-transparent", cue.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	_check("Blocked cue is visible", cue.visible)
	cue.set_door_state(DoorLanguage.OPEN)
	_check("Ordinary open has no highlight", not cue.visible)
	cue.queue_free()
	if failures == 0:
		print("DOORLANGUAGE|ALL OK")
		quit(0)
	else:
		print("DOORLANGUAGE|FAIL|%d" % failures)
		quit(1)


func _state(room_id: String, crown: bool, bonus: bool, plot: bool) -> String:
	return DoorLanguage.resolve(room_id, crown, bonus, plot)


func _check(label: String, passed: bool) -> void:
	if passed:
		print("DOORLANGUAGE|OK|" + label)
	else:
		failures += 1
		print("DOORLANGUAGE|FAIL|" + label)
