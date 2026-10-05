class_name DayOneFlow
extends RefCounted

## Day One flow logic extracted verbatim from ReefMain (Phase-7 satellite
## mold): this object owns no state. Every Day One field stays on ReefMain,
## which saves it through DayOneDirector exactly as before. Bodies were moved
## mechanically; ReefMain keeps a same-signature forwarder for every function
## reached from outside this file (other scripts, probes, string dispatch).

const DayOneArtStudioLogic = preload("res://scripts/day_one_art_studio.gd")

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


func _open_day_one_art_studio() -> bool:
	if m.castle_room_stage == null or m.castle_room_id != "craft_room" \
			or not m.day_one_is_active() \
			or m._day_one_ref().is_room_completed("art"):
		return false
	if m._day_one_art_studio != null and is_instance_valid(m._day_one_art_studio):
		m._day_one_art_studio.refresh_from_state()
		return true
	m._day_one_art_studio = DayOneArtStudioLogic.new() as DayOneArtStudio
	m.castle_room_stage.add_child(m._day_one_art_studio)
	m._day_one_art_studio.setup(m)
	return true


func _close_day_one_art_studio() -> void:
	if m._day_one_art_studio != null and is_instance_valid(m._day_one_art_studio):
		m._day_one_art_studio.teardown()
	m._day_one_art_studio = null


func day_one_boss_door_ready() -> bool:
	var director: DayOneDirector = m._day_one_ref()
	return m.day_one_is_active() and director.boss_door_glow \
		and not director.giant_dust_bunny_boss_triggered


func day_one_complete_boss_and_begin_day_two() -> bool:
	var director: DayOneDirector = m._day_one_ref()
	# The real DustBoss win crosses one atomic story boundary. Record and emit
	# the boss defeat first; its synchronous hook starts Chapter 2. Only then
	# emit/present the newer Day Two bridge. Repeated win/end callbacks stop at
	# the idempotent defeat gate and cannot duplicate either event or transition.
	if not director.complete_giant_dust_bunny_boss():
		return false
	director.complete_day_one_after_boss()
	# Persist the unlock before presentation. The normal end-game save follows
	# in the same frame, but this first write protects both the boss boundary
	# and Chapter 2 activation if the platform backgrounds during transition.
	m._write_save()
	m.call_deferred("_show_day_two_transition")
	return true


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
	_close_day_one_art_studio()
	m._castle_rooms_ref().apply_day_one_cleanup("craft_room")
	_day_one_sync_castle_dressing()
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
	_day_one_sync_castle_dressing()
	m._write_save()
	m._show_day_one_room_handoff("playroom", "day_one_new_door")
	return true


func _day_one_discover_dirty_castle() -> void:
	if not m.day_one_is_active():
		return
	m._day_one_ref().discover_dirty_castle()
	_day_one_attach_castle_dressing()
	_day_one_arm_boss_door()


func _day_one_attach_castle_dressing() -> void:
	if not m.day_one_is_active() or m.castle_room_stage == null:
		return
	if m.day_one_castle_dressing == null \
			or not is_instance_valid(m.day_one_castle_dressing):
		m.day_one_castle_dressing = DayOneCastleDressing.create_dressing(
			m.castle_room_stage)
		m.day_one_castle_dressing.name = "DayOneDirtyCastleDressing"
		m.day_one_castle_dressing.z_index = 20
	_day_one_sync_castle_dressing()


func _day_one_sync_castle_dressing() -> void:
	if m.day_one_is_active() and m.castle_room_stage != null:
		var logical_room: String = String(ReefMain.DAY_ONE_CASTLE_ROOM_IDS.get(m.castle_room_id, ""))
		if logical_room != "":
			m._day_one_play_story_clip_for_room(logical_room, m._day_one_ref())
	_sync_day_one_art_studio()
	if m.day_one_castle_dressing == null \
			or not is_instance_valid(m.day_one_castle_dressing):
		return
	var director: DayOneDirector = m._day_one_ref()
	var room_dirty: Dictionary = {}
	var door_unlocked: Dictionary = {}
	for castle_room_value: Variant in ReefMain.DAY_ONE_CASTLE_ROOM_IDS.keys():
		var castle_room: String = String(castle_room_value)
		var logical_room: String = String(ReefMain.DAY_ONE_CASTLE_ROOM_IDS[castle_room])
		room_dirty[castle_room] = not director.is_dust_bunny_cleaned(logical_room)
		door_unlocked[castle_room] = director.can_enter_room(logical_room)
	m.day_one_castle_dressing.update_dressing(0.0, {
		"room_dirty": room_dirty,
		"door_unlocked": door_unlocked,
		"boss_back_door_active": director.boss_door_glow,
		"visible_room_id": m.castle_room_id,
	})
	if m._castle_rooms_25d != null and m._castle_rooms_25d.is_open():
		m._castle_rooms_25d.refresh_door_states()


func _clear_day_one_bathroom_cleanup() -> void:
	if m._day_one_bathroom_cleanup != null \
			and is_instance_valid(m._day_one_bathroom_cleanup):
		m._day_one_bathroom_cleanup.teardown()
	m._day_one_bathroom_cleanup = null


func _on_day_one_bathroom_cleanup_completed() -> void:
	if not m.day_one_complete_bathroom_scene():
		return
	_clear_day_one_bathroom_cleanup()
	_day_one_sync_castle_dressing()


func _sync_day_one_art_studio() -> void:
	var should_show: bool = m.day_one_is_active() \
		and m.castle_room_stage != null \
		and m.castle_room_id == "craft_room" \
		and not m._day_one_ref().is_room_completed("art")
	if should_show:
		_open_day_one_art_studio()
	else:
		_close_day_one_art_studio()


func _day_one_clear_castle_dressing() -> void:
	_day_one_cancel_story_clips()
	_clear_day_one_bathroom_cleanup()
	_clear_day_one_bathroom_movie_handoff()
	m._day_one_bathroom_movie_handoff_pending = false
	m._day_one_bathroom_entry_movie_checked = false
	m._clear_day_one_pool_route()
	_restore_day_one_bathroom_controls()
	_close_day_one_art_studio()
	if m.day_one_castle_dressing != null \
			and is_instance_valid(m.day_one_castle_dressing):
		m.day_one_castle_dressing.teardown()
	m.day_one_castle_dressing = null


func _clear_day_one_bathroom_movie_handoff() -> void:
	if m._day_one_bathroom_movie_handoff != null \
			and is_instance_valid(m._day_one_bathroom_movie_handoff):
		m._day_one_bathroom_movie_handoff.stop()
		m._day_one_bathroom_movie_handoff.queue_free()
	m._day_one_bathroom_movie_handoff = null
	m._day_one_bathroom_movie_handoff_pending = false


func _show_day_one_pool_route() -> void:
	if not m.day_one_is_active() or m.castle_room_stage == null \
			or not m._day_one_ref().can_enter_room("pool"):
		return
	if m._day_one_bathroom_movie_handoff_pending \
			or _day_one_bathroom_movie_is_playing():
		return
	# Back returns to the hall, where the next unlocked painted door glows.
	_restore_day_one_bathroom_controls()
	if m._day_one_room_handoff_target == "mermaid_pool" \
			and m._day_one_room_handoff_source == m.castle_room_id:
		return
	m._show_day_one_room_handoff("mermaid_pool", "day_one_pool_ready")


func _day_one_bathroom_movie_is_playing() -> bool:
	if m._day_one_bathroom_movie_handoff == null \
			or not is_instance_valid(m._day_one_bathroom_movie_handoff):
		return false
	return bool(m._day_one_bathroom_movie_handoff.audit_snapshot().get(
		"player_active", false))


func _day_one_bathroom_navigation_controls() -> Array[Control]:
	var controls: Array[Control] = []
	var candidates: Array[Node] = [
		m.castle_room_action_button,
		m.castle_room_back_button,
		m.castle_room_menu_panel,
	]
	for candidate: Node in candidates:
		var control: Control = candidate as Control
		if control != null and is_instance_valid(control) \
				and not controls.has(control):
			controls.append(control)
	return controls


func _restore_day_one_bathroom_controls() -> void:
	if not m._day_one_bathroom_controls_suspended:
		return
	for state: Dictionary in m._day_one_bathroom_control_state:
		var control: Control = state.get("control") as Control
		if control == null or not is_instance_valid(control):
			continue
		control.visible = bool(state.get("visible", true))
		control.mouse_filter = int(state.get("mouse_filter",
			Control.MOUSE_FILTER_STOP))
		var button: BaseButton = control as BaseButton
		if button != null:
			button.disabled = bool(state.get("disabled", false))
	m._day_one_bathroom_control_state.clear()
	m._day_one_bathroom_controls_suspended = false
	m.castle_room_menu_open = m._day_one_bathroom_menu_was_open
	m._set_world_controls_enabled(true, "day_one_bathroom_lifecycle")


func _day_one_arm_boss_door() -> void:
	var director: DayOneDirector = m._day_one_ref()
	if not m.day_one_is_active() or not director.boss_door_glow \
			or director.giant_dust_bunny_boss_triggered:
		return
	m._castle_rooms_ref().arm_royal_hall_event(
		"day_one_giant_dust_bunny", _day_one_trigger_boss)


func _day_one_trigger_boss() -> void:
	m._day_one_ref().trigger_giant_dust_bunny_boss()


func _day_one_drain_story_clips() -> void:
	if not m.is_inside_tree() or m.is_queued_for_deletion() \
			or (m._day_one_story_clip != null and is_instance_valid(m._day_one_story_clip)):
		return
	if m.touch_ui != null:
		m.touch_ui.consume_action()
	while not m._day_one_story_clip_queue.is_empty():
		var next_id: String = m._day_one_story_clip_queue.pop_front()
		if m._day_one_play_story_clip(next_id):
			return
	if m._day_one_story_boss_start_pending:
		m._day_one_story_boss_start_pending = false
		if m.day_one_is_active() and m._day_one_ref().giant_dust_bunny_boss_triggered:
			m._start_game(m.dust_boss_fr)
	if m._day_one_story_boss_transition_pending:
		m._day_one_story_boss_transition_pending = false
		m._show_day_two_transition()
	if m.castle_room_id == "bubble_bath" and m.castle_room_stage != null:
		m._sync_day_one_bathroom_cleanup()


func _day_one_cancel_story_clips() -> void:
	m._day_one_story_clip_queue.clear()
	if m._day_one_story_boss_start_pending and m.day_one_is_active():
		# A room teardown during C11 must leave the boss door re-triggerable,
		# never a triggered checkpoint with no active encounter behind it.
		m._day_one_ref().giant_dust_bunny_boss_triggered = false
		m.day_one_event_seen.erase(DayOneDirector.EVENT_GIANT_DUST_BUNNY_BOSS)
		m._queue_save()
	m._day_one_story_boss_start_pending = false
	m._day_one_story_boss_transition_pending = false
	var previous: DayOneStoryClips = m._day_one_story_clip
	m._day_one_story_clip = null
	if previous != null and is_instance_valid(previous):
		# Release its pause synchronously before another scene acquires it. The
		# detached callback cannot advance an abandoned room or boss route.
		previous.skip()


func _day_one_suspend_boss_for_lifecycle() -> void:
	# Interruptions keep the live fight paused; only deliberate Leave tears it down.
	if m._day_one_story_boss_start_pending:
		_day_one_cancel_story_clips()
		m._day_one_ref().giant_dust_bunny_boss_triggered = false
		_return_day_one_boss_to_castle()
		return
	if m.game != "dustboss" or not m.day_one_is_active() \
			or m._day_one_ref().giant_dust_bunny_boss_defeated:
		return
	if not m.get_tree().paused:
		m._pause_ref().toggle_pause()
	m._write_save()


func _return_day_one_boss_to_castle() -> void:
	if not m.day_one_is_active() \
			or m._day_one_ref().giant_dust_bunny_boss_defeated:
		return
	# _enter_level2 establishes the Canvas world before the hall seam opens it.
	# Keep this post-clear: rebuilding while the arena still owns g leaves stale
	# DustBoss nodes and can make the first returned tap hit the old encounter.
	m._enter_level2(true)
	m._enter_castle_interior(true)
	_day_one_arm_boss_door()
	m._write_save()


func _day_one_reorient_after_exit_now() -> void:
	if not m.day_one_is_active():
		return
	var resume_room: String = day_one_castle_room_for_current()
	if m.game == "":
		# No world owns the castle, so resuming the room alone would leave the
		# watchdog firing every frame. Rebuild the Canvas world once instead.
		m._enter_level2_now(true)
		m._enter_castle_interior_now()
		if m._castle_rooms_ref().is_open():
			m._castle_rooms_ref().show_room(resume_room, false)
		return
	if m._castle_rooms_ref().is_open():
		m._castle_rooms_ref().resume(resume_room)
	else:
		m._enter_castle_interior_now()
		if m._castle_rooms_ref().is_open():
			m._castle_rooms_ref().show_room(resume_room, false)
