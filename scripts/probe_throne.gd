extends SceneTree
# Royal Hall and Moon Throne triggers, reached the way a four-year-old reaches
# them.
#
# Every castle tap here goes through the viewport, and she WALKS to the Royal
# Hall doorway by
# tapping the floor rather than being teleported there. That distinction is the
# whole point of this historical probe filename: on 2026-08-03 the far-right
# endpoint was reported dead a second time, and the cause was not its art — the
# StorybookUI stage sat on
# top of the Control carrying `_on_room_input` with MOUSE_FILTER_STOP, so every
# tap that missed a hotspot button was swallowed and Roshan could not walk one
# step anywhere in the picture-first castle. Probes that call
# `_position_player_at_foot` directly are blind to that, so this one does not.
#
# 1. Pearl Castle Main Hall: tapping the floor must move her; walking right
#    must bring the mist-sealed Royal Hall entrance on screen. Its locked state,
#    Crown/companion opening, re-offer behavior, and future one-shot event hook
#    are all exercised through the real touch target.
# 2. Butterfly World Star Hall: sitting on the Moon Throne must award the
#    STAR PRINCESS sticker.

# Keep the walking target clear of the omnipresent 136px elevator button at
# x=1116..1252. It remains on the right side of the painted walk lane, so each
# viewport tap still exercises real floor navigation and advances the camera.
const FLOOR_TAP := Vector2(1050.0, 560.0)
const WALK_SETTLE := 90                     # frames for the step + camera pan
const MAX_WALK_TAPS := 8
const ROYAL_HALL_ARRIVAL_SETTLE_MS := 1250
const ROYAL_HALL_RESPONSE_TIMEOUT_MS := 4000

var main: ReefMain
var checks_failed := 0
var royal_hall_event_calls := 0
var royal_hall_rearm_calls := 0
var royal_hall_rearmed_calls := 0

func _init() -> void:
	call_deferred("_run")

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("THRONE|", label, "|", "OK" if ok else "FAIL", "|", detail)

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _touch(at: Vector2) -> void:
	var down := InputEventMouseButton.new()
	down.button_index = MOUSE_BUTTON_LEFT
	down.pressed = true
	down.position = at
	down.global_position = at
	root.push_input(down, true)
	var up := InputEventMouseButton.new()
	up.button_index = MOUSE_BUTTON_LEFT
	up.pressed = false
	up.position = at
	up.global_position = at
	root.push_input(up, true)

func _tap_stage(at: Vector2) -> void:
	_touch(main.castle_room_stage.get_global_transform_with_canvas() * at)

func _tap_button(button: Button) -> bool:
	if button == null or not is_instance_valid(button) \
			or not button.is_visible_in_tree():
		return false
	_touch(button.get_global_transform_with_canvas() * (button.size * 0.5))
	return true

func _wait_ms(milliseconds: int) -> void:
	var deadline_ms: int = Time.get_ticks_msec() + milliseconds
	while Time.get_ticks_msec() < deadline_ms:
		await process_frame

func _foot() -> Vector2:
	return main.castle_room_player_sprite.get_meta(
		"stage_foot", Vector2.ZERO) as Vector2

func _royal_hall_button() -> Button:
	for record: Dictionary in main.castle_room_door_hotspots:
		var data: Dictionary = record.get("data", {})
		if String(data.get("id", "")) == "__royal_hall":
			return record.get("button") as Button
	return null

func _tap_royal_hall() -> void:
	var button: Button = _royal_hall_button()
	if not _tap_button(button):
		return
	# Script-mode headless can run hundreds of near-zero-delta frames before the
	# authored approach tween advances. Wait in monotonic time so the arrival
	# callback always belongs to this tap before the probe changes event state.
	await _wait_ms(ROYAL_HALL_ARRIVAL_SETTLE_MS)

func _tap_royal_hall_now() -> bool:
	return _tap_button(_royal_hall_button())

func _tap_elevator() -> bool:
	if main.castle_room_stage == null:
		return false
	return _tap_button(main.castle_room_stage.get_node_or_null(
		"ElevatorButton") as Button)

func _tap_elevator_close() -> bool:
	if main.castle_room_menu_panel == null:
		return false
	return _tap_button(main.castle_room_menu_panel.get_node_or_null(
		"ElevatorMenuClose") as Button)

func _tap_elevator_room(room_id: String) -> bool:
	return _tap_button(main.castle_room_menu_buttons.get(room_id) as Button)

func _wait_for_royal_hall_offer() -> void:
	# Headless frames can advance with a much smaller delta than a rendered
	# 60 Hz frame. Wait on the authored outcomes (arrival callback plus Huluu's
	# deliberate 1.6 s story beat), bounded by real monotonic time.
	var deadline_ms: int = Time.get_ticks_msec() \
		+ ROYAL_HALL_RESPONSE_TIMEOUT_MS
	while Time.get_ticks_msec() < deadline_ms:
		if bool(main.g.get("crown_won", false)) \
				and main.companion_layer != null:
			return
		await process_frame

func _visible_royal_hall_mist() -> int:
	var visible_count := 0
	for mist: Sprite3D in main.castle_royal_hall_mist_cards:
		if mist != null and mist.visible and mist.modulate.a > 0.012:
			visible_count += 1
	return visible_count

func _mist_transforms() -> Array[Transform3D]:
	var values: Array[Transform3D] = []
	for mist: Sprite3D in main.castle_royal_hall_mist_cards:
		if mist != null and is_instance_valid(mist):
			values.append(mist.transform)
	return values

func _mist_transform_changed(before: Array[Transform3D],
		after: Array[Transform3D]) -> bool:
	if before.size() != after.size():
		return false
	for index: int in range(before.size()):
		if before[index].origin.distance_to(after[index].origin) > 0.00001 \
				or before[index].basis.get_scale().distance_to(
					after[index].basis.get_scale()) > 0.00001:
			return true
	return false

func _wait_for_locked_royal_hall_feedback() -> bool:
	var deadline_ms: int = Time.get_ticks_msec() \
		+ ROYAL_HALL_ARRIVAL_SETTLE_MS
	while Time.get_ticks_msec() < deadline_ms:
		if main.castle_royal_hall_mist_flutter_time > 0.0 \
				and main.hud_msg != null \
				and "royal mist" in main.hud_msg.text.to_lower():
			return true
		await process_frame
	return false

func _latest_voice_player() -> AudioStreamPlayer:
	if main.voice_i <= 0 or main.voice_pool.is_empty():
		return null
	var index: int = posmod(main.voice_i - 1, main.voice_pool.size())
	return main.voice_pool[index] as AudioStreamPlayer

func _event_matches(rooms: CastleRooms25D, event_id: String,
		token: int) -> bool:
	return main.castle_royal_hall_event_id == event_id \
		and main.castle_royal_hall_event_entry.is_valid() \
		and rooms.royal_hall_event_token(event_id) == token

func _on_probe_royal_hall_event() -> void:
	royal_hall_event_calls += 1

func _on_probe_royal_hall_rearm() -> void:
	royal_hall_rearm_calls += 1
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.arm_royal_hall_event("probe_double_next",
		Callable(self, "_on_probe_royal_hall_rearmed"))

func _on_probe_royal_hall_rearmed() -> void:
	royal_hall_rearmed_calls += 1

func _run() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	main.pearl_count = main.PEARL_TOTAL
	main.trophies = 5
	main.level2_done_once = true
	main.companion_id = "eagle"
	main.combat_tutorial_done = true
	main.g["crown_won"] = false
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(24)

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	_ck("hall_open", rooms.is_open() and main.castle_room_id == "main_hall",
		main.castle_room_id)
	var button: Button = _royal_hall_button()
	_ck("royal_hall_hotspot_built", button != null)
	if button == null:
		_finish()
		return
	_ck("royal_hall_offscreen_at_spawn", not button.visible,
		"she starts two screens away from it")

	# ---- she must be able to WALK: the tap that misses every hotspot ----
	var spawn_foot: Vector2 = _foot()
	_tap_stage(FLOOR_TAP)
	await _frames(WALK_SETTLE)
	_ck("floor_tap_walks_her", _foot().x > spawn_foot.x + 200.0,
		"foot %.0f -> %.0f" % [spawn_foot.x, _foot().x])

	# ---- and walking right must bring the Royal Hall on screen ----
	var taps := 1
	while taps < MAX_WALK_TAPS and not _royal_hall_button().visible:
		_tap_stage(FLOOR_TAP)
		await _frames(WALK_SETTLE)
		taps += 1
	button = _royal_hall_button()
	_ck("walking_brings_royal_hall_on_screen", button.visible,
		"%d floor taps, foot=%.0f" % [taps, _foot().x])
	if not button.visible:
		_finish()
		return
	_ck("royal_hall_hitbox_is_child_sized",
		button.size.x >= 112.0 and button.size.y >= 112.0, str(button.size))

	# ---- ordinary free-roam: the mist seals the gate kindly ----
	_ck("locked_royal_hall_has_five_mist_cards",
		main.castle_royal_hall_mist_cards.size() == 5
		and _visible_royal_hall_mist() == 5)
	var locked_mist_before: Array[Transform3D] = _mist_transforms()
	var voice_i_before: int = main.voice_i
	_ck("locked_royal_hall_tap_reaches_real_button",
		_tap_royal_hall_now())
	var locked_feedback_seen: bool = \
		await _wait_for_locked_royal_hall_feedback()
	var flutter_seen: bool = main.castle_royal_hall_mist_flutter_time > 0.0
	# Advance the authored flutter deterministically; uncapped headless frames can
	# carry near-zero delta even while the arrival tween uses real elapsed time.
	rooms._tick_royal_hall_mist(0.08)
	var locked_mist_after: Array[Transform3D] = _mist_transforms()
	var locked_voice: AudioStreamPlayer = _latest_voice_player()
	var locked_voice_stream: AudioStream = locked_voice.stream \
		if locked_voice != null else null
	var locked_feedback_stream: AudioStream = main.castle_room_prop_sfx.stream \
		if main.castle_room_prop_sfx != null else null
	_ck("locked_mist_visibly_flutters",
		locked_feedback_seen and flutter_seen
		and _mist_transform_changed(locked_mist_before, locked_mist_after)
		and _visible_royal_hall_mist() == 5,
		"feedback=%s flutter=%.2f moved=%s mist=%d" % [
			locked_feedback_seen, main.castle_royal_hall_mist_flutter_time,
			_mist_transform_changed(locked_mist_before, locked_mist_after),
			_visible_royal_hall_mist()])
	_ck("locked_gate_has_spoken_feedback",
		main.voice_i == voice_i_before + 1
		and locked_voice_stream != null
		and locked_voice_stream.resource_path.ends_with(
			"voices/roshan_talk.ogg")
		and main.hud_msg != null
		and "royal mist" in main.hud_msg.text.to_lower(),
		"voice_i=%d->%d stream=%s caption=%s" % [
			voice_i_before, main.voice_i,
			locked_voice_stream.resource_path \
				if locked_voice_stream != null else "missing",
			main.hud_msg.text if main.hud_msg != null else "missing"])
	_ck("locked_gate_does_not_award_or_open_picker",
		not bool(main.g.get("crown_won", false))
		and main.companion_layer == null
		and _visible_royal_hall_mist() == 5
		and locked_feedback_stream != null
		and locked_feedback_stream.resource_path.ends_with(
			"castle/curtain_swish.ogg"),
		"crown=%s picker=%s mist=%d sfx=%s" % [
			main.g.get("crown_won", false), main.companion_layer != null,
			_visible_royal_hall_mist(),
			locked_feedback_stream.resource_path \
				if locked_feedback_stream != null else "missing"])

	# ---- invalid owners cannot erase or replace a valid incumbent ----
	var incumbent_entry := Callable(self, "_on_probe_royal_hall_event")
	_ck("generation_contract_incumbent_arms",
		rooms.arm_royal_hall_event("probe_same_id", incumbent_entry))
	var incumbent_token: int = rooms.royal_hall_event_token("probe_same_id")
	var invalid_empty_id: bool = rooms.arm_royal_hall_event(
		"", incumbent_entry)
	var invalid_callable: bool = rooms.arm_royal_hall_event(
		"probe_invalid", Callable())
	var reserved_crown_id: bool = rooms.arm_royal_hall_event(
		"crown_welcome", incumbent_entry)
	var reserved_companion_id: bool = rooms.arm_royal_hall_event(
		"companion_welcome", incumbent_entry)
	var reserved_tutorial_id: bool = rooms.arm_royal_hall_event(
		"combat_tutorial", incumbent_entry)
	_ck("invalid_arm_preserves_incumbent",
		not invalid_empty_id and not invalid_callable
		and not reserved_crown_id and not reserved_companion_id
		and not reserved_tutorial_id
		and _event_matches(rooms, "probe_same_id", incumbent_token)
		and main.castle_royal_hall_event_entry == incumbent_entry,
		"token=%d current=%d id=%s" % [incumbent_token,
			rooms.royal_hall_event_token("probe_same_id"),
			main.castle_royal_hall_event_id])

	# Reusing the same semantic id creates a new ownership generation. A stale
	# teardown must not clear it, while the current owner still can.
	_ck("same_id_event_rearms",
		rooms.arm_royal_hall_event("probe_same_id", incumbent_entry))
	var current_token: int = rooms.royal_hall_event_token("probe_same_id")
	var stale_clear_result: bool = rooms.clear_royal_hall_event(
		"probe_same_id", incumbent_token)
	_ck("stale_same_id_clear_fails",
		not stale_clear_result and current_token > incumbent_token
		and _event_matches(rooms, "probe_same_id", current_token),
		"stale=%d current=%d" % [incumbent_token, current_token])
	_ck("current_generation_clear_works",
		rooms.clear_royal_hall_event("probe_same_id", current_token)
		and main.castle_royal_hall_event_id == ""
		and not main.castle_royal_hall_event_entry.is_valid())

	# ---- an eligible Crown welcome clears the veil and opens on arrival ----
	main.combat_tutorial_done = false
	main.level2_done_once = false
	main.companion_id = ""
	# Complete the authored fade deterministically. Script-mode headless frames
	# can carry near-zero deltas and are not a reliable wall-clock sampler.
	rooms._tick_royal_hall_mist(1.0)
	_ck("crown_event_clears_royal_hall_mist",
		rooms._royal_hall_event_id() == "crown_welcome"
		and _visible_royal_hall_mist() == 0,
		"event=%s mist=%d" % [rooms._royal_hall_event_id(),
			_visible_royal_hall_mist()])
	await _tap_royal_hall()
	await _wait_for_royal_hall_offer()
	_ck("touch_awards_crown_star", bool(main.g.get("crown_won", false)))
	_ck("royal_hall_offers_a_stuffie_friend", main.companion_layer != null,
		"companion_id=%s" % main.companion_id)
	var companion: CompanionSystem = main._companion_ref()

	# Closing without choosing must not burn the moment: the gate re-opens.
	companion.close_picker()
	await _frames(10)
	_ck("picker_closed", main.companion_layer == null)
	await _tap_royal_hall()
	await _wait_for_royal_hall_offer()
	_ck("royal_hall_re_offers_after_a_closed_picker",
		main.companion_layer != null and main.companion_id == "")

	# ---- after both welcomes, the first combat class is the next event ----
	companion.close_picker()
	await _frames(10)
	main.companion_id = "eagle"
	await _frames(40)
	_ck("combat_tutorial_follows_crown_and_companion",
		rooms._royal_hall_event_id() == "combat_tutorial"
		and _visible_royal_hall_mist() == 0)
	# The dedicated tutorial probe enters and graduates through the real gate.
	# Here, mark that separate saved beat complete so the remaining locked-state
	# and custom-owner checks stay focused on Royal Hall routing.
	main.combat_tutorial_done = true
	rooms._tick_royal_hall_mist(1.0)
	_ck("mist_returns_after_first_combat_class",
		rooms._royal_hall_event_id().is_empty()
		and _visible_royal_hall_mist() == 5)
	await _tap_royal_hall()
	await _frames(60)
	_ck("no_re_offer_once_she_has_a_friend", main.companion_layer == null,
		"companion_id=%s" % main.companion_id)
	_ck("crown_progress_remains_recorded", bool(main.g.get("crown_won", false)))

	# ---- a double tap cannot consume an event armed by its own callback ----
	royal_hall_rearm_calls = 0
	royal_hall_rearmed_calls = 0
	_ck("rapid_double_event_arms",
		rooms.arm_royal_hall_event("probe_double_first",
			Callable(self, "_on_probe_royal_hall_rearm")))
	var first_rapid_tap: bool = _tap_royal_hall_now()
	var second_rapid_tap: bool = _tap_royal_hall_now()
	await _wait_ms(ROYAL_HALL_ARRIVAL_SETTLE_MS)
	var rearmed_token: int = rooms.royal_hall_event_token(
		"probe_double_next")
	_ck("rapid_double_tap_preserves_callback_rearm",
		first_rapid_tap and second_rapid_tap
		and royal_hall_rearm_calls == 1
		and royal_hall_rearmed_calls == 0
		and rearmed_token >= 0
		and _event_matches(rooms, "probe_double_next", rearmed_token),
		"first=%d next=%d token=%d pending=%s" % [
			royal_hall_rearm_calls, royal_hall_rearmed_calls,
			rearmed_token, main.castle_royal_hall_arrival_pending])
	_ck("rapid_double_rearm_can_be_cleared_by_owner",
		rooms.clear_royal_hall_event("probe_double_next", rearmed_token))

	# ---- opening the real elevator cancels approach, not event ownership ----
	royal_hall_event_calls = 0
	_ck("menu_cancel_event_arms",
		rooms.arm_royal_hall_event("probe_menu_cancel",
			Callable(self, "_on_probe_royal_hall_event")))
	var menu_cancel_token: int = rooms.royal_hall_event_token(
		"probe_menu_cancel")
	var menu_approach_tap: bool = _tap_royal_hall_now()
	var menu_open_tap: bool = _tap_elevator()
	await _frames(2)
	var menu_opened_during_approach: bool = main.castle_room_menu_open
	await _wait_ms(ROYAL_HALL_ARRIVAL_SETTLE_MS)
	_ck("opening_elevator_cancels_arrival_and_preserves_event",
		menu_approach_tap and menu_open_tap and menu_opened_during_approach
		and royal_hall_event_calls == 0
		and not main.castle_royal_hall_arrival_pending
		and _event_matches(rooms, "probe_menu_cancel", menu_cancel_token),
		"menu=%s calls=%d pending=%s token=%d" % [
			menu_opened_during_approach, royal_hall_event_calls,
			main.castle_royal_hall_arrival_pending, menu_cancel_token])
	_ck("real_elevator_close_tap_works", _tap_elevator_close())
	await _frames(2)
	_ck("menu_cancel_owner_clears_event",
		rooms.clear_royal_hall_event(
			"probe_menu_cancel", menu_cancel_token))

	# ---- choosing a real room during approach also preserves the event ----
	royal_hall_event_calls = 0
	_ck("navigation_cancel_event_arms",
		rooms.arm_royal_hall_event("probe_navigation_cancel",
			Callable(self, "_on_probe_royal_hall_event")))
	var navigation_cancel_token: int = rooms.royal_hall_event_token(
		"probe_navigation_cancel")
	var navigation_approach_tap: bool = _tap_royal_hall_now()
	var navigation_menu_tap: bool = _tap_elevator()
	await _frames(2)
	var navigation_room_tap: bool = _tap_elevator_room("library")
	await _frames(4)
	await _wait_ms(ROYAL_HALL_ARRIVAL_SETTLE_MS)
	_ck("navigating_away_cancels_arrival_and_preserves_event",
		navigation_approach_tap and navigation_menu_tap
		and navigation_room_tap and main.castle_room_id == "library"
		and royal_hall_event_calls == 0
		and not main.castle_royal_hall_arrival_pending
		and _event_matches(rooms, "probe_navigation_cancel",
			navigation_cancel_token),
		"room=%s calls=%d pending=%s" % [main.castle_room_id,
			royal_hall_event_calls, main.castle_royal_hall_arrival_pending])
	_ck("real_room_back_tap_returns_to_hall",
		_tap_button(main.castle_room_back_button))
	await _frames(12)
	_ck("room_back_returns_to_main_hall", main.castle_room_id == "main_hall",
		main.castle_room_id)
	_ck("navigation_cancel_owner_clears_event",
		rooms.clear_royal_hall_event(
			"probe_navigation_cancel", navigation_cancel_token))

	# ---- a full close/reopen preserves an armed future Royal Hall event ----
	royal_hall_event_calls = 0
	_ck("reopen_event_arms",
		rooms.arm_royal_hall_event("probe_reopen",
			Callable(self, "_on_probe_royal_hall_event")))
	var reopen_token: int = rooms.royal_hall_event_token("probe_reopen")
	var real_back_closed_hall: bool = _tap_button(main.castle_room_back_button)
	await _frames(10)
	_ck("real_back_closes_hall_but_preserves_event",
		real_back_closed_hall and not rooms.is_open()
		and _event_matches(rooms, "probe_reopen", reopen_token),
		"open=%s token=%d" % [rooms.is_open(), reopen_token])
	rooms.open("main_hall")
	await _frames(24)
	_ck("reopen_preserves_armed_event",
		rooms.is_open() and main.castle_room_id == "main_hall"
		and _event_matches(rooms, "probe_reopen", reopen_token),
		"room=%s token=%d" % [main.castle_room_id,
			rooms.royal_hall_event_token("probe_reopen")])
	_ck("reopened_event_can_be_cleared_by_same_owner",
		rooms.clear_royal_hall_event("probe_reopen", reopen_token))

	# ---- the same swallowed-tap bug froze every other room too ----
	rooms.show_room("library", false)
	await _frames(10)
	var library_foot: Vector2 = _foot()
	_tap_stage(Vector2(300.0, 560.0))
	await _frames(WALK_SETTLE)
	_ck("floor_tap_walks_her_in_a_room_too",
		absf(_foot().x - library_foot.x) > 80.0,
		"foot %.0f -> %.0f" % [library_foot.x, _foot().x])
	rooms.show_room("main_hall", false)
	await _frames(10)

	# ---- Butterfly World: the Moon Throne ----
	rooms.close()
	await _frames(6)
	main.stickers.erase("throne")
	main.galaxy_unlocked = true
	main._start_galaxy()
	await _frames(40)
	var galaxy: GalaxyLevel = main.galaxy_game as GalaxyLevel
	_ck("galaxy_running", galaxy != null, "game=" + main.game)
	if galaxy != null:
		galaxy._enter_hall()
		await _frames(20)
		galaxy.set("_cpos", Vector3(0.0, 0.0, -20.0))
		galaxy.set("_throne_cool", 0.0)
		await _frames(40)
		_ck("moon_throne_crowns_the_star_princess",
			main.stickers.has("throne"))
	_finish()

func _finish() -> void:
	print("THRONE|done: ",
		("ALL OK" if checks_failed == 0 else "FAILED (%d)" % checks_failed))
	quit()
