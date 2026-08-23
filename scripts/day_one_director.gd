class_name DayOneDirector
extends RefCounted

## Small, standalone state owner for the castle's Day One onboarding route.
##
## The director has no dependency on scenes or assets. It receives ReefMain as
## its typed state owner; a caller can connect `hook_event` and merge
## `serialize_state()` into its existing save document. Every persisted field
## is additive and namespaced.

signal hook_event(event_name: String, payload: Dictionary)

const ROOM_ORDER: Array[String] = ["bathroom", "pool", "stuffie", "art"]
const ROOM_DEFINITIONS: Dictionary = {
	"bathroom": {
		"index": 0,
		"title": "Bubble Bathroom",
		"kind": "tutorial",
		"activity_id": "bathroom_tutorial",
	},
	"pool": {
		"index": 1,
		"title": "Sparkle Pool",
		"kind": "activity",
		"activity_id": "pool_activity",
	},
	"stuffie": {
		"index": 2,
		"title": "Stuffie Room",
		"kind": "activity",
		"activity_id": "stuffie_activity",
	},
	"art": {
		"index": 3,
		"title": "Art Room",
		"kind": "activity",
		"activity_id": "art_activity",
	},
}

const EVENT_ARRIVAL_PLANE_MEDIA: String = "arrival_plane_media"
const EVENT_DIRTY_CASTLE_DISCOVERY: String = "dirty_castle_discovery"
const EVENT_GROK_VIDEO_2: String = "grok_video_2"
const EVENT_DUST_BUNNY_CLEANUP: String = "dust_bunny_cleanup"
const EVENT_BOSS_DOOR_GLOW: String = "boss_door_glow"
const EVENT_GIANT_DUST_BUNNY_BOSS: String = "giant_dust_bunny_boss"

const SAVE_KEYS: Array[String] = [
	"day_one_active",
	"day_one_current_room",
	"day_one_completed_rooms",
	"day_one_cleaned_rooms",
	"day_one_jobs_locked",
	"day_one_opera_enabled",
	"day_one_arrival_plane_media_seen",
	"day_one_dirty_castle_discovered",
	"day_one_grok_video_2_seen",
	"day_one_boss_door_glow",
	"day_one_giant_dust_bunny_boss_triggered",
	"day_one_bathroom_cleanup_step",
	"day_one_pool_cleanup_step",
	"day_one_pool_rumi_met",
]

var m: ReefMain

# These are typed forwarding properties so existing main-side call sites can
# keep asking the director for policy while the actual mutable state remains on
# ReefMain, the single save/state owner.
var day_one_active: bool:
	get:
		return m.day_one_active
	set(value):
		m.day_one_active = value
var current_room_id: String:
	get:
		return m.day_one_current_room_id
	set(value):
		m.day_one_current_room_id = value
var completed_rooms: Dictionary:
	get:
		return m.day_one_completed_rooms
	set(value):
		m.day_one_completed_rooms = value
var cleaned_rooms: Dictionary:
	get:
		return m.day_one_cleaned_rooms
	set(value):
		m.day_one_cleaned_rooms = value
var arrival_plane_media_seen: bool:
	get:
		return m.day_one_arrival_plane_media_seen
	set(value):
		m.day_one_arrival_plane_media_seen = value
var dirty_castle_discovered: bool:
	get:
		return m.day_one_dirty_castle_discovered
	set(value):
		m.day_one_dirty_castle_discovered = value
var grok_video_2_seen: bool:
	get:
		return m.day_one_grok_video_2_seen
	set(value):
		m.day_one_grok_video_2_seen = value
var boss_door_glow: bool:
	get:
		return m.day_one_boss_door_glow
	set(value):
		m.day_one_boss_door_glow = value
var giant_dust_bunny_boss_triggered: bool:
	get:
		return m.day_one_giant_dust_bunny_boss_triggered
	set(value):
		m.day_one_giant_dust_bunny_boss_triggered = value
var bathroom_cleanup_step: int:
	get:
		return m.day_one_bathroom_cleanup_step
	set(value):
		m.day_one_bathroom_cleanup_step = value
var pool_cleanup_step: int:
	get:
		return m.day_one_pool_cleanup_step
	set(value):
		m.day_one_pool_cleanup_step = value
var pool_rumi_met: bool:
	get:
		return m.day_one_pool_rumi_met
	set(value):
		m.day_one_pool_rumi_met = value
var day_one_event_seen: Dictionary:
	get:
		return m.day_one_event_seen
	set(value):
		m.day_one_event_seen = value
var day_one_event_history: Array[Dictionary]:
	get:
		return m.day_one_event_history
	set(value):
		m.day_one_event_history = value


func _init(main: ReefMain) -> void:
	m = main
	day_one_event_seen.clear()
	day_one_event_history.clear()
	_normalise_state({})


func room_definitions() -> Dictionary:
	return ROOM_DEFINITIONS.duplicate(true)


func room_ids() -> Array[String]:
	return ROOM_ORDER.duplicate()


func room_status(room_id: String) -> String:
	var id: String = _normalise_room_id(room_id)
	if id == "":
		return "unknown"
	if bool(completed_rooms.get(id, false)):
		return "completed"
	if id == current_room_id:
		return "current"
	return "locked"


func can_enter_room(room_id: String) -> bool:
	var status: String = room_status(room_id)
	return status == "completed" or status == "current"


func unlocked_room_ids() -> Array[String]:
	var unlocked: Array[String] = []
	for room_id: String in ROOM_ORDER:
		if can_enter_room(room_id):
			unlocked.append(room_id)
	return unlocked


func is_room_completed(room_id: String) -> bool:
	var id: String = _normalise_room_id(room_id)
	return id != "" and bool(completed_rooms.get(id, false))


func is_dust_bunny_cleaned(room_id: String) -> bool:
	var id: String = _normalise_room_id(room_id)
	return id != "" and bool(cleaned_rooms.get(id, false))


func jobs_are_globally_locked() -> bool:
	return day_one_active


func is_job_unlocked(_job_id: String) -> bool:
	return not jobs_are_globally_locked()


func can_start_job(job_id: String) -> bool:
	return is_job_unlocked(job_id)


func is_opera_enabled() -> bool:
	return not day_one_active


func can_start_opera() -> bool:
	return is_opera_enabled()


## Placeholder interface for both tutorial and activity rooms. Completion is
## accepted only for the current room; completed rooms remain visitable but do
## not replay their completion hooks.
func complete_activity(room_id: String, activity_id: String = "") -> bool:
	var id: String = _normalise_room_id(room_id)
	if id == "" or not can_enter_room(id) or is_room_completed(id):
		return false
	var definition: Dictionary = ROOM_DEFINITIONS.get(id, {}) as Dictionary
	var expected_activity: String = String(definition.get("activity_id", ""))
	if activity_id != "" and activity_id != expected_activity:
		return false
	return complete_room(id)


func complete_tutorial(room_id: String) -> bool:
	var id: String = _normalise_room_id(room_id)
	if id == "":
		return false
	var definition: Dictionary = ROOM_DEFINITIONS.get(id, {}) as Dictionary
	if String(definition.get("kind", "")) != "tutorial":
		return false
	return complete_activity(id, String(definition.get("activity_id", "")))


func complete_placeholder(room_id: String, activity_id: String = "") -> bool:
	return complete_activity(room_id, activity_id)


func complete_room(room_id: String) -> bool:
	var id: String = _normalise_room_id(room_id)
	if id == "" or id != current_room_id or is_room_completed(id):
		return false
	if id == "bathroom":
		bathroom_cleanup_step = 3
	if id == "pool":
		pool_cleanup_step = 4
		pool_rumi_met = true
	completed_rooms[id] = true
	cleaned_rooms[id] = true
	_emit_once(EVENT_DUST_BUNNY_CLEANUP, {"room_id": id})
	_advance_current_room()
	if _all_rooms_completed():
		boss_door_glow = true
		_emit_once(EVENT_BOSS_DOOR_GLOW, {"room_ids": ROOM_ORDER.duplicate()})
	return true


func trigger_arrival_plane_media() -> bool:
	if arrival_plane_media_seen:
		return false
	arrival_plane_media_seen = true
	_emit_once(EVENT_ARRIVAL_PLANE_MEDIA, {})
	return true


func discover_dirty_castle() -> bool:
	var changed: bool = false
	if not dirty_castle_discovered:
		dirty_castle_discovered = true
		_emit_once(EVENT_DIRTY_CASTLE_DISCOVERY, {})
		changed = true
	# Grok video #2 is the media hook paired with this discovery. It remains a
	# separate event so a UI can show the discovery beat and video independently.
	if not grok_video_2_seen:
		grok_video_2_seen = true
		_emit_once(EVENT_GROK_VIDEO_2, {"video_number": 2})
		changed = true
	return changed


func trigger_grok_video_2() -> bool:
	if grok_video_2_seen:
		return false
	grok_video_2_seen = true
	_emit_once(EVENT_GROK_VIDEO_2, {"video_number": 2})
	return true


func trigger_giant_dust_bunny_boss() -> bool:
	if not boss_door_glow or not _all_rooms_completed():
		return false
	if giant_dust_bunny_boss_triggered:
		return false
	giant_dust_bunny_boss_triggered = true
	_emit_once(EVENT_GIANT_DUST_BUNNY_BOSS, {"room_id": "art"})
	return true


func event_history() -> Array[Dictionary]:
	return day_one_event_history.duplicate(true)


func drain_events() -> Array[Dictionary]:
	var pending: Array[Dictionary] = day_one_event_history.duplicate(true)
	day_one_event_history.clear()
	return pending


## Returns only additive Day One fields. The caller may merge this dictionary
## into an existing save without changing any legacy key or schema version.
func serialize_state() -> Dictionary:
	return {
		"day_one_active": day_one_active,
		"day_one_current_room": current_room_id,
		"day_one_completed_rooms": _room_map_to_array(completed_rooms),
		"day_one_cleaned_rooms": _room_map_to_array(cleaned_rooms),
		"day_one_jobs_locked": jobs_are_globally_locked(),
		"day_one_opera_enabled": is_opera_enabled(),
		"day_one_arrival_plane_media_seen": arrival_plane_media_seen,
		"day_one_dirty_castle_discovered": dirty_castle_discovered,
		"day_one_grok_video_2_seen": grok_video_2_seen,
		"day_one_boss_door_glow": boss_door_glow,
		"day_one_giant_dust_bunny_boss_triggered": \
			giant_dust_bunny_boss_triggered,
		"day_one_bathroom_cleanup_step": bathroom_cleanup_step,
		"day_one_pool_cleanup_step": pool_cleanup_step,
		"day_one_pool_rumi_met": pool_rumi_met,
	}


func restore_state(raw: Variant) -> void:
	_normalise_state(raw as Dictionary if raw is Dictionary else {})
	day_one_event_seen.clear()
	day_one_event_history.clear()


func _normalise_state(source: Dictionary) -> void:
	var normalised: Dictionary = normalise_save_patch(source)
	day_one_active = bool(normalised.get("day_one_active", true))
	current_room_id = String(normalised.get("day_one_current_room", ""))
	completed_rooms = _room_membership(normalised.get(
		"day_one_completed_rooms", []))
	cleaned_rooms = _room_membership(normalised.get("day_one_cleaned_rooms", []))
	arrival_plane_media_seen = bool(normalised.get(
		"day_one_arrival_plane_media_seen", false))
	dirty_castle_discovered = bool(normalised.get(
		"day_one_dirty_castle_discovered", false))
	grok_video_2_seen = bool(normalised.get("day_one_grok_video_2_seen", false))
	boss_door_glow = bool(normalised.get("day_one_boss_door_glow", false))
	giant_dust_bunny_boss_triggered = bool(normalised.get(
		"day_one_giant_dust_bunny_boss_triggered", false))
	bathroom_cleanup_step = int(normalised.get(
		"day_one_bathroom_cleanup_step", 0))
	pool_cleanup_step = int(normalised.get("day_one_pool_cleanup_step", 0))
	pool_rumi_met = bool(normalised.get("day_one_pool_rumi_met", false))


## SaveState can call this static helper without constructing a director (and
## therefore without manufacturing a ReefMain). It accepts only the additive
## Day One namespace and returns a complete, normalized Day One patch.
static func normalise_save_patch(raw: Variant) -> Dictionary:
	var source: Dictionary = raw as Dictionary if raw is Dictionary else {}
	var candidates: Dictionary = _room_membership_static(source.get(
		"day_one_completed_rooms", []))
	var completed: Array[String] = []
	for room_id: String in ROOM_ORDER:
		if not bool(candidates.get(room_id, false)):
			break
		completed.append(room_id)
	var cleaned: Array[String] = completed.duplicate()
	var current: String = ""
	if completed.size() < ROOM_ORDER.size():
		current = ROOM_ORDER[completed.size()]
	var grok_seen: bool = _as_bool_static(source.get(
		"day_one_grok_video_2_seen", false), false)
	var all_done: bool = completed.size() == ROOM_ORDER.size()
	var bathroom_done: bool = completed.has("bathroom")
	var pool_done: bool = completed.has("pool")
	var saved_bathroom_step: int = clampi(int(source.get(
		"day_one_bathroom_cleanup_step", 3 if bathroom_done else 0)), 0, 3)
	if bathroom_done:
		saved_bathroom_step = 3
	var saved_pool_step: int = clampi(int(source.get(
		"day_one_pool_cleanup_step", 4 if pool_done else 0)), 0, 4)
	if pool_done:
		saved_pool_step = 4
	return {
		"day_one_active": _as_bool_static(source.get(
			"day_one_active", true), true),
		"day_one_current_room": current,
		"day_one_completed_rooms": completed,
		"day_one_cleaned_rooms": cleaned,
		"day_one_jobs_locked": _as_bool_static(source.get(
			"day_one_active", true), true),
		"day_one_opera_enabled": not _as_bool_static(source.get(
			"day_one_active", true), true),
		"day_one_arrival_plane_media_seen": _as_bool_static(source.get(
			"day_one_arrival_plane_media_seen", false), false),
		"day_one_dirty_castle_discovered": _as_bool_static(source.get(
			"day_one_dirty_castle_discovered", false), false) or grok_seen,
		"day_one_grok_video_2_seen": grok_seen,
		"day_one_boss_door_glow": all_done,
		"day_one_giant_dust_bunny_boss_triggered": all_done and _as_bool_static(
			source.get("day_one_giant_dust_bunny_boss_triggered", false), false),
		"day_one_bathroom_cleanup_step": saved_bathroom_step,
		"day_one_pool_cleanup_step": saved_pool_step,
		"day_one_pool_rumi_met": pool_done or _as_bool_static(
			source.get("day_one_pool_rumi_met", false), false),
	}


func _advance_current_room() -> void:
	current_room_id = _first_incomplete_room()


func _first_incomplete_room() -> String:
	for room_id: String in ROOM_ORDER:
		if not bool(completed_rooms.get(room_id, false)):
			return room_id
	return ""


func _all_rooms_completed() -> bool:
	return completed_rooms.size() == ROOM_ORDER.size()


func _normalise_room_id(value: String) -> String:
	var id: String = value.strip_edges().to_lower()
	return id if ROOM_DEFINITIONS.has(id) else ""


func _room_membership(value: Variant) -> Dictionary:
	var result: Dictionary = {}
	if value is Dictionary:
		for key: Variant in (value as Dictionary).keys():
			var id: String = _normalise_room_id(String(key))
			if id != "" and _as_bool((value as Dictionary).get(key, false), false):
				result[id] = true
	elif value is Array:
		for entry: Variant in value as Array:
			var id_from_entry: String = _normalise_room_id(String(entry))
			if id_from_entry != "":
				result[id_from_entry] = true
	return result


static func _room_membership_static(value: Variant) -> Dictionary:
	var result: Dictionary = {}
	if value is Dictionary:
		var source: Dictionary = value as Dictionary
		for key: Variant in source.keys():
			var id: String = _normalise_room_id_static(String(key))
			if id != "" and _as_bool_static(source.get(key, false), false):
				result[id] = true
	elif value is Array:
		for entry: Variant in value as Array:
			var id_from_entry: String = _normalise_room_id_static(String(entry))
			if id_from_entry != "":
				result[id_from_entry] = true
	return result


func _room_map_to_array(value: Dictionary) -> Array[String]:
	var result: Array[String] = []
	for room_id: String in ROOM_ORDER:
		if bool(value.get(room_id, false)):
			result.append(room_id)
	return result


func _as_bool(value: Variant, fallback: bool) -> bool:
	return _as_bool_static(value, fallback)


static func _as_bool_static(value: Variant, fallback: bool) -> bool:
	if value is bool:
		return bool(value)
	if value is int or value is float:
		return float(value) != 0.0
	if value is String:
		var text: String = String(value).strip_edges().to_lower()
		if text in ["true", "yes", "on", "1"]:
			return true
		if text in ["false", "no", "off", "0", ""]:
			return false
	return fallback


static func _normalise_room_id_static(value: String) -> String:
	var id: String = value.strip_edges().to_lower()
	return id if ROOM_DEFINITIONS.has(id) else ""


func _emit_once(event_name: String, payload: Dictionary) -> void:
	if bool(day_one_event_seen.get(event_name, false)):
		return
	day_one_event_seen[event_name] = true
	var record: Dictionary = {
		"event": event_name,
		"payload": payload.duplicate(true),
	}
	day_one_event_history.append(record)
	hook_event.emit(event_name, payload.duplicate(true))
