class_name DayOneFlow
extends RefCounted

## Day One flow logic extracted verbatim from ReefMain (Phase-7 satellite
## mold): this object owns no state. Every Day One field stays on ReefMain,
## which saves it through DayOneDirector exactly as before. Bodies were moved
## mechanically; ReefMain keeps a same-signature forwarder for every function
## reached from outside this file (other scripts, probes, string dispatch).

var m: ReefMain


func _init(main: ReefMain) -> void:
	m = main


func day_one_castle_room_for_current() -> String:
	if not m.day_one_is_active():
		return "main_hall"
	var logical_room: String = m._day_one_ref().current_room_id
	# A killed/reloaded adoption picker must return to its owning picture room,
	# not strand the child in the next (art) room with no confirmed companion.
	if logical_room == "art" and m.companion_id == "" \
			and bool(m.stuffie_wins.get("rescued_eagle", false)) \
			and m._day_one_ref().is_room_completed("stuffie"):
		return "playroom"
	for castle_room_value: Variant in ReefMain.DAY_ONE_CASTLE_ROOM_IDS.keys():
		var castle_room: String = String(castle_room_value)
		if String(ReefMain.DAY_ONE_CASTLE_ROOM_IDS[castle_room]) == logical_room:
			return castle_room
	return "main_hall"


func day_one_boss_door_ready() -> bool:
	var director: DayOneDirector = m._day_one_ref()
	return m.day_one_is_active() and director.boss_door_glow \
		and not director.giant_dust_bunny_boss_triggered


func day_one_castle_room_is_clean(castle_room: String) -> bool:
	var logical_room: String = String(ReefMain.DAY_ONE_CASTLE_ROOM_IDS.get(
		castle_room, ""))
	return logical_room != "" \
		and m._day_one_ref().is_dust_bunny_cleaned(logical_room)


func day_one_can_enter_castle_room(castle_room: String) -> bool:
	if not m.day_one_is_active() or castle_room == "main_hall":
		return true
	if ReefMain.DAY_ONE_OPTIONAL_CASTLE_ROOM_IDS.has(castle_room):
		return true
	var logical_room: String = String(ReefMain.DAY_ONE_CASTLE_ROOM_IDS.get(
		castle_room, ""))
	return logical_room != "" and m._day_one_ref().can_enter_room(logical_room)


func day_one_try_enter_castle_room(castle_room: String) -> bool:
	if day_one_can_enter_castle_room(castle_room):
		return true
	m.show_msg("Roshan",
		"That door is napping. Let's clean the next room!",
		"castle_door_resting")
	return false


func day_one_record_bathroom_cleanup_step(step: int) -> void:
	if not m.day_one_is_active():
		return
	m.day_one_bathroom_cleanup_step = clampi(maxi(
		m.day_one_bathroom_cleanup_step, step), 0, 3)
	m._write_save()


func day_one_record_bathroom_supply_step(step: int) -> void:
	if not m.day_one_is_active():
		return
	m.day_one_bathroom_supply_hunt_step = clampi(maxi(
		m.day_one_bathroom_supply_hunt_step, step), 0, 2)
	if m.day_one_bathroom_supply_hunt_step >= 2:
		m.day_one_bathroom_tools_authorized = true
	m._write_save()


func day_one_record_bathroom_toilet_cleaned() -> void:
	if not m.day_one_is_active() or m.day_one_bathroom_cleanup_step < 2:
		return
	m.day_one_bathroom_toilet_cleaned = true
	m._write_save()


func day_one_record_bathroom_tub_drained() -> void:
	if not m.day_one_is_active() or m.day_one_bathroom_tub_drained:
		return
	m.day_one_bathroom_tub_drained = true
	m._write_save()


## The basket is the single authorization point for the two cleaning tools.
## The old hunt-step key is advanced for save compatibility; new callers can
## use this idempotent seam without reviving a cabinet hunt.
func day_one_authorize_bathroom_tools() -> bool:
	if not m.day_one_is_active() \
			or m._day_one_ref().current_room_id != "bathroom" \
			or m._day_one_ref().is_room_completed("bathroom"):
		return false
	if m.day_one_bathroom_tools_authorized:
		return true
	m.day_one_bathroom_tools_authorized = true
	m.day_one_bathroom_supply_hunt_step = 2
	m._write_save()
	return true


func day_one_record_art_cleanup(kind: String, item_id: String) -> bool:
	if not m.day_one_is_active() or m._day_one_ref().current_room_id != "art":
		return false
	var changed: bool = m._day_one_ref().record_art_cleanup(kind, item_id)
	if changed:
		m._write_save()
	return changed


func day_one_complete_art_customization() -> bool:
	if not m.day_one_is_active() or m._day_one_ref().current_room_id != "art":
		return false
	var changed: bool = m._day_one_ref().complete_art_customization()
	if changed:
		m._write_save()
	return changed


func day_one_complete_art_scene() -> bool:
	if not m.day_one_is_active():
		return false
	var director: DayOneDirector = m._day_one_ref()
	if not director.complete_art_studio():
		return false
	m._close_day_one_art_studio()
	m._castle_rooms_ref().apply_day_one_cleanup("craft_room")
	m._day_one_sync_castle_dressing()
	m._write_save()
	m._show_day_one_room_handoff("__royal_hall", "day_one_all_rooms_clean")
	return true


func day_one_record_pool_cleanup_step(step: int) -> void:
	if not m.day_one_is_active():
		return
	m.day_one_pool_cleanup_step = clampi(maxi(
		m.day_one_pool_cleanup_step, step), 0, 4)
	m._write_save()


func day_one_record_pool_activity_progress(
		skimmer_mask: int, waterfall_mask: int, seahorse_tugs: int) -> void:
	if not m.day_one_is_active():
		return
	var next_skimmer: int = m.day_one_pool_skimmer_mask | (skimmer_mask & 0x3F)
	var next_waterfall: int = m.day_one_pool_waterfall_mask | (waterfall_mask & 0x07)
	var next_tugs: int = clampi(maxi(
		m.day_one_pool_seahorse_tugs, seahorse_tugs), 0, 8)
	if next_skimmer == m.day_one_pool_skimmer_mask and next_waterfall == m.day_one_pool_waterfall_mask \
			and next_tugs == m.day_one_pool_seahorse_tugs:
		return
	m.day_one_pool_skimmer_mask = next_skimmer
	m.day_one_pool_waterfall_mask = next_waterfall
	m.day_one_pool_seahorse_tugs = next_tugs
	m._write_save()


func day_one_complete_pool_scene() -> bool:
	if not m.day_one_is_active():
		return false
	var director: DayOneDirector = m._day_one_ref()
	if director.is_room_completed("pool"):
		return false
	m.day_one_pool_cleanup_step = 4
	m.day_one_pool_rumi_met = true
	m.day_one_pool_skimmer_mask = 0x3F
	m.day_one_pool_waterfall_mask = 0x07
	m.day_one_pool_seahorse_tugs = 8
	if not director.complete_activity("pool", "pool_activity"):
		return false
	m._castle_rooms_ref().apply_day_one_cleanup("mermaid_pool")
	m._day_one_sync_castle_dressing()
	m._write_save()
	m._show_day_one_room_handoff("playroom", "day_one_new_door")
	return true
