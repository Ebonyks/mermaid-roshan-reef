extends SceneTree
## Pearl Opera House product-route regression.
##
## The sixteen historical bit positions remain readable, but only thirteen
## sparse career slots are playable. This probe enters the ordinary headless
## route without a test-only selector, exercises every live lobby selection,
## and protects passive safety, save-bit identity, completion, replay and
## teardown. Detailed one-finger mechanics remain covered by probe_opera_2d.

var main: ReefMain
var bad := 0


func _init() -> void:
	seed(20260812)
	Engine.time_scale = 8.0
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	main._skip_intro()
	main.opera_progress = 0
	main.opera_stars = 0
	main.opera_done = false
	main.stickers.erase("showtime")
	main.game = "level2"
	main.g["t"] = 0.0
	main._play_music("castle_opera_hall")
	var source_track := main.cur_track
	var source_player_visible := main.player != null and main.player.visible
	var source_touch_visible := main.touch_ui != null and main.touch_ui.visible

	_audit_stable_roster()
	_audit_save_matrix()
	main._start_opera_now()
	await _frames(4)
	var house := main.opera_game as OperaHouse
	_check("a fresh save enters the ordinary Opera route",
		house != null and main.game == "opera"
		and main.cur_track == "opera_lobby"
		and (main.player == null or not main.player.visible)
		and (main.touch_ui == null or not main.touch_ui.visible))
	if house == null:
		_finish()
		return
	_audit_canvas_lobby(house)
	var untouched_children := _direct_child_ids(main)
	await _frames(90)
	_check("idle lobby time cannot award a career",
		house.act == null and main.opera_stars == 0
		and main.opera_progress == 0 and not main.opera_done
		and _direct_child_ids(main) == untouched_children)

	# Tombstones are retained data, never selectable content. The public roster
	# predicate and absence of any card are the durable product boundary; do not
	# manufacture expected engine errors merely to test a private callback.
	for retired_index: int in OperaHouse.RETIRED_ACT_INDICES:
		_check("retired slot %d cannot start" % retired_index,
			not OperaHouse.is_live_act_index(retired_index)
			and not OperaAct.supports_config(OperaHouse.ACTS[retired_index]))
	await _audit_invalid_cancel_ownership()
	await _audit_pause_during_curtain(house)

	# Model a real upgraded save that already contains all three retired bits.
	# Those raw bits survive; effective progress and completion ignore them.
	main.opera_stars = OperaHouse.RETIRED_STAR_MASK
	main.opera_progress = OperaHouse.live_star_count(main.opera_stars)
	house.lobby_2d.refresh(main.opera_stars, 0)
	_check("retired historical bits survive without counting as jobs",
		main.opera_stars == 0x4210 and main.opera_progress == 0
		and not OperaHouse.has_all_live_stars(main.opera_stars)
		and OperaHouse.first_incomplete_floor(main.opera_stars) == 0)
	var curtain_pearls_before := main.pearl_count
	await _win_then_leave_during_curtain(house, int(OperaHouse.LIVE_ACT_INDICES[0]))
	_check("leaving during the curtain call preserves the earned career once",
		main.opera_game == null and main.game == "level2"
		and main.cur_track == source_track
		and (main.player == null or main.player.visible == source_player_visible)
		and (main.touch_ui == null or main.touch_ui.visible == source_touch_visible)
		and main.opera_stars == (OperaHouse.RETIRED_STAR_MASK | 0x0001)
		and main.opera_progress == 1
		and main.pearl_count == curtain_pearls_before + 3
		and int(main.save_data.get("opera_stars", -1)) == main.opera_stars
		and int(main.save_data.get("opera_progress", -1)) == 1)
	main._start_opera_now()
	await _frames(4)
	house = main.opera_game as OperaHouse
	_check("curtain-call leave returns to a clean re-enterable Opera",
		house != null and house.act == null and house.lobby_2d != null)
	if house == null:
		_finish()
		return

	var pearl_baseline: int = main.pearl_count
	for live_index: int in OperaHouse.LIVE_ACT_INDICES:
		if live_index == int(OperaHouse.LIVE_ACT_INDICES[0]):
			continue
		await _complete_lifecycle(house, live_index)
	_check("all thirteen live careers complete across sparse save bits",
		OperaHouse.has_all_live_stars(main.opera_stars)
		and (main.opera_stars & OperaHouse.ACTIVE_STAR_MASK)
			== OperaHouse.ACTIVE_STAR_MASK
		and (main.opera_stars & OperaHouse.RETIRED_STAR_MASK)
			== OperaHouse.RETIRED_STAR_MASK
		and main.opera_progress == OperaHouse.ACTIVE_ACT_COUNT)
	_check("career completion awards the finale reward exactly once",
		main.opera_done and bool(main.stickers.get("showtime", false))
		and main.pearl_count == pearl_baseline
			+ (OperaHouse.ACTIVE_ACT_COUNT - 1) * 3 + 50)
	_check("a complete sparse roster has no incomplete floor",
		OperaHouse.first_incomplete_floor(main.opera_stars) == -1)

	var completed_mask: int = main.opera_stars
	var completed_pearls: int = main.pearl_count
	await _complete_lifecycle(house, int(OperaHouse.LIVE_ACT_INDICES[0]))
	_check("replaying a starred career never duplicates completion rewards",
		main.opera_stars == completed_mask
		and main.opera_progress == OperaHouse.ACTIVE_ACT_COUNT
		and main.pearl_count == completed_pearls + 1
		and main.opera_done)

	house._leave_early()
	await _frames(3)
	_check("leaving closes the Opera and restores the castle",
		main.opera_game == null and main.game == "level2"
		and main.cur_track == source_track
		and (main.player == null or main.player.visible == source_player_visible)
		and (main.touch_ui == null or main.touch_ui.visible == source_touch_visible))
	main._start_opera_now()
	await _frames(4)
	house = main.opera_game as OperaHouse
	_check("re-entry preserves raw bits and effective completion",
		house != null and main.opera_stars == completed_mask
		and OperaHouse.live_star_count(main.opera_stars)
			== OperaHouse.ACTIVE_ACT_COUNT
		and OperaHouse.has_all_live_stars(main.opera_stars))
	if house != null:
		_audit_canvas_lobby(house)
		house._leave_early()
		await _frames(3)
	_finish()


func _audit_stable_roster() -> void:
	var exact_live := [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15]
	var exact_retired := [4, 9, 14]
	var exact_floors := [
		[0, 1, 2, 3],
		[5, 6, 7, 8],
		[10, 11, 12, 15, 13],
	]
	_check("Opera keeps sixteen historical save positions",
		OperaHouse.ACTS.size() == 16)
	_check("the thirteen playable positions stay sparse and stable",
		OperaHouse.LIVE_ACT_INDICES == exact_live
		and OperaHouse.ACTIVE_ACT_COUNT == 13
		and OperaHouse.ACTIVE_STAR_MASK == 0xBDEF
		and OperaHouse.ALL_STARS == OperaHouse.ACTIVE_STAR_MASK)
	_check("the three retired boss positions remain inert tombstones",
		OperaHouse.RETIRED_ACT_INDICES == exact_retired
		and OperaHouse.RETIRED_STAR_MASK == 0x4210)
	_check("the three lobby pages map to the real sparse save slots",
		OperaHouse.FLOOR_ACT_INDICES == exact_floors
		and OperaHouse.FLOOR_STAR_MASKS == [0x000F, 0x01E0, 0xBC00])
	var roster_ok := true
	var career_ids: Dictionary = {}
	for slot: int in range(OperaHouse.ACTS.size()):
		var config: Dictionary = OperaHouse.ACTS[slot]
		roster_ok = roster_ok and int(config.get("save_bit", -1)) == slot
		if OperaHouse.is_live_act_index(slot):
			var career_id := String(config.get("costume", ""))
			roster_ok = roster_ok and not bool(config.get("retired", false)) \
				and not career_id.is_empty() and not career_ids.has(career_id)
			career_ids[career_id] = true
		else:
			roster_ok = roster_ok and bool(config.get("retired", false)) \
				and config.size() == 2
	_check("every live career and tombstone owns its original bit", roster_ok)
	_check("all thirteen active careers have unique Canvas identities",
		career_ids.size() == OperaHouse.ACTIVE_ACT_COUNT)


func _audit_save_matrix() -> void:
	var state := SaveState.new(main)
	var cases: Array[Dictionary] = [
		{"label": "legacy progress 15", "input": {"opera_progress": 15},
			"raw": 0x7FFF, "effective": 12},
		{"label": "legacy progress 16", "input": {"opera_progress": 16},
			"raw": 0xFFFF, "effective": 13},
		{"label": "retired bits only", "input": {"opera_stars": 0x4210},
			"raw": 0x4210, "effective": 0},
		{"label": "floor one live", "input": {"opera_stars": 0x000F},
			"raw": 0x000F, "effective": 4},
		{"label": "floor one plus retired", "input": {"opera_stars": 0x001F},
			"raw": 0x001F, "effective": 4},
		{"label": "first two live floors", "input": {"opera_stars": 0x01EF},
			"raw": 0x01EF, "effective": 8},
		{"label": "first two floors plus retired", "input": {
			"opera_stars": 0x43FF}, "raw": 0x43FF, "effective": 8},
		{"label": "all live careers", "input": {"opera_stars": 0xBDEF},
			"raw": 0xBDEF, "effective": 13},
		{"label": "old all-bits completion", "input": {"opera_stars": 0xFFFF},
			"raw": 0xFFFF, "effective": 13},
	]
	for fixture: Dictionary in cases:
		var normalised: Dictionary = state._normalise_save(
			fixture["input"] as Dictionary)
		var no_reward := not bool(normalised.get("opera_done", true)) \
			and not bool((normalised.get("stickers", {}) as Dictionary).get(
				"showtime", false))
		_check("save migration keeps %s exact" % String(fixture["label"]),
			int(normalised.get("opera_stars", -1)) == int(fixture["raw"])
			and int(normalised.get("opera_progress", -1)) \
				== int(fixture["effective"])
			and no_reward)


func _audit_canvas_lobby(house: OperaHouse) -> void:
	var lobby := house.lobby_2d as OperaLobby2D
	_check("Opera always opens its Canvas lobby",
		house.use_lobby_2d and lobby != null)
	if lobby == null:
		return
	_check("ordinary headless entry builds a Canvas-only presentation subtree",
		_descendants_are_canvas(house))
	_check("the lobby exposes all three direct floor tabs",
		lobby.floor_tabs.size() == 3
		and lobby.floor_tabs.all(func(tab: Button) -> bool:
			return tab.visible and not tab.disabled))
	_check("the retired boss/finale picker is absent",
		lobby.root.find_children("*Boss*", "Node", true, false).is_empty()
		and lobby.root.find_children("*Finale*", "Node", true, false).is_empty())
	_check("thirteen progress pearls map one-to-one to live save slots",
		lobby.progress_pearls.size() == OperaHouse.ACTIVE_ACT_COUNT)
	var expected_counts := [4, 4, 5]
	for floor_index: int in range(3):
		lobby.refresh(main.opera_stars, floor_index)
		var visible_indices: Array[int] = []
		for card: Button in lobby.card_buttons:
			if card.visible:
				visible_indices.append(int(card.get_meta("act_index", -1)))
		_check("floor %d shows its real live career cards" % (floor_index + 1),
			visible_indices == (OperaHouse.FLOOR_ACT_INDICES[floor_index] as Array)
			and visible_indices.size() == int(expected_counts[floor_index]))
	lobby.refresh(main.opera_stars, 0)


func _win_then_leave_during_curtain(house: OperaHouse,
		live_index: int) -> void:
	var floor_index := _floor_for_act(live_index)
	var lobby := house.lobby_2d as OperaLobby2D
	if floor_index < 0 or lobby == null:
		_check("curtain-call fixture has a live lobby card", false)
		return
	_tap_control(lobby.floor_tabs[floor_index], 120 + live_index)
	await _frames(2)
	var career_card: Button = null
	for card: Button in lobby.card_buttons:
		if card.visible and int(card.get_meta("act_index", -1)) == live_index:
			career_card = card
			break
	_check("curtain-call fixture starts through its real picture card",
		career_card != null)
	if career_card == null:
		return
	_tap_control(career_card, 140 + live_index)
	await _frames(3)
	var current_act := house.act as OperaAct
	_check("curtain-call fixture reaches its Canvas career",
		current_act != null and house.act_index == live_index)
	if current_act == null:
		return
	current_act._win()
	_check("curtain-call fixture is won but not yet committed",
		current_act.state == "won"
		and (main.opera_stars & (1 << live_index)) == 0)
	house._leave_early()
	await _frames(4)


func _audit_pause_during_curtain(house: OperaHouse) -> void:
	var live_index := int(OperaHouse.LIVE_ACT_INDICES[1])
	var floor_index := _floor_for_act(live_index)
	var lobby := house.lobby_2d as OperaLobby2D
	var stars_before := main.opera_stars
	var pearls_before := main.pearl_count
	if floor_index < 0 or lobby == null:
		_check("pause-during-curtain fixture has a live lobby card", false)
		return
	_tap_control(lobby.floor_tabs[floor_index], 180 + live_index)
	await _frames(2)
	var career_card: Button = null
	for card: Button in lobby.card_buttons:
		if card.visible and int(card.get_meta("act_index", -1)) == live_index:
			career_card = card
			break
	_check("pause-during-curtain fixture starts through its real picture card",
		career_card != null)
	if career_card == null:
		return
	_tap_control(career_card, 200 + live_index)
	await _frames(3)
	var current_act := house.act as OperaAct
	if current_act == null:
		_check("pause-during-curtain fixture reaches its Canvas career", false)
		return
	current_act._win()
	current_act.notification(NOTIFICATION_APPLICATION_PAUSED)
	await _frames(3)
	var expected_mask: int = stars_before | (1 << live_index)
	_check("application pause commits an earned curtain-call result once",
		house.act == null and main.opera_stars == expected_mask
		and main.opera_progress == OperaHouse.live_star_count(expected_mask)
		and main.pearl_count == pearls_before + 3
		and int(main.save_data.get("opera_stars", -1)) == expected_mask
		and main.cur_track == "opera_lobby")
	await _frames(30)
	_check("later frames cannot duplicate a pause-committed curtain call",
		main.opera_stars == expected_mask and main.pearl_count == pearls_before + 3)


func _audit_invalid_cancel_ownership() -> void:
	var touch_before := main.touch_ui != null and main.touch_ui.visible
	var player_before := main.player != null and main.player.visible
	var track_before := main.cur_track
	if main.touch_ui != null:
		main.touch_ui.visible = false
	if main.player != null:
		main.player.visible = false
	var invalid := OperaAct.new()
	invalid.m = main
	invalid.state = "invalid"
	var callback_count := 0
	invalid.finish_cb = func() -> void: callback_count += 1
	get_root().add_child(invalid)
	invalid.cancel()
	await _frames(2)
	_check("invalid cancellation cannot claim caller-owned state",
		not is_instance_valid(invalid) and callback_count == 0
		and main.cur_track == track_before
		and (main.touch_ui == null or not main.touch_ui.visible)
		and (main.player == null or not main.player.visible))
	if main.touch_ui != null:
		main.touch_ui.visible = touch_before
	if main.player != null:
		main.player.visible = player_before


func _complete_lifecycle(house: OperaHouse, live_index: int) -> void:
	var config: Dictionary = OperaHouse.ACTS[live_index]
	var stars_before: int = main.opera_stars
	var progress_before: int = main.opera_progress
	var floor_index := _floor_for_act(live_index)
	var lobby := house.lobby_2d as OperaLobby2D
	_check("live slot %d has a real lobby page" % live_index,
		floor_index >= 0 and lobby != null)
	if floor_index < 0 or lobby == null:
		return
	_tap_control(lobby.floor_tabs[floor_index], 20 + live_index)
	await _frames(2)
	_check("live slot %d page opens through viewport touch" % live_index,
		lobby.floor_index == floor_index)
	var career_card: Button = null
	for card: Button in lobby.card_buttons:
		if card.visible and int(card.get_meta("act_index", -1)) == live_index:
			career_card = card
			break
	_check("live slot %d exposes its stable picture card" % live_index,
		career_card != null)
	if career_card == null:
		return
	_tap_control(career_card, 40 + live_index)
	await _frames(3)
	var act := house.act as OperaAct
	var career_id := String(config.get("costume", "career"))
	_check("%s starts from raw viewport input on its stable lobby slot" % career_id,
		act != null and house.act_index == live_index
		and int(act.config.get("save_bit", -1)) == live_index
		and main.cur_track == String(config.get("music", ""))
		and (main.player == null or not main.player.visible)
		and main.kart_game == null)
	if act == null:
		return
	_check("%s uses only its Canvas career world" % career_id,
		act.use_career_world_2d and act.career_world_2d != null
		and _descendants_are_canvas(act))
	await _frames(45)
	var idle_safe := act.state == "play" and main.opera_stars == stars_before \
		and main.opera_progress == progress_before
	if not idle_safe:
		print("OPERA|idle_detail: career=%s state=%s stars=%04X/%04X progress=%d/%d" % [
			career_id, act.state, main.opera_stars, stars_before,
			main.opera_progress, progress_before,
		])
	_check("%s cannot award itself while idle" % career_id, idle_safe)
	if career_id == "racer":
		_check("Racer never launches an external Kart child",
			main.kart_game == null
			and main.find_children("*", "KartGame", true, false).is_empty()
			and act.career_world_2d.surface.mode == "circle")
		await _complete_racer_with_viewport(act, act.career_world_2d)
	else:
		act._win()
	act.win_t = 0.0
	act._process(0.1)
	await _frames(3)
	_check("%s returns to the lobby with exactly its bit" % career_id,
		house.act == null and (main.opera_stars & (1 << live_index)) != 0
		and main.opera_progress == OperaHouse.live_star_count(main.opera_stars)
		and house.lobby_2d != null and house.lobby_2d.visible
		and main.cur_track == "opera_lobby"
		and (main.player == null or not main.player.visible)
		and (main.touch_ui == null or not main.touch_ui.visible))


func _complete_racer_with_viewport(act: OperaAct,
		world: OperaCareerWorld2D) -> void:
	world.phase_index = world._finale_start()
	world._show_phase()
	await _frames(2)
	var surface := world.surface as OperaGestureSurface
	_check("Racer's real final activity is ready for routed input",
		world.task_open and surface != null and surface.mode == "circle"
		and is_equal_approx(world.phase_progress, 0.0))
	if surface == null:
		return
	var center := surface.size * 0.5
	var radius := minf(surface.size.x, surface.size.y) * 0.32
	var local_position := center + Vector2(radius, 0.0)
	var screen_position := _control_screen_point(surface, local_position)
	var press := InputEventScreenTouch.new()
	press.index = 77
	press.position = screen_position
	press.pressed = true
	surface.get_viewport().push_input(press, false)
	var prior_screen := screen_position
	for sample: int in range(1, 49):
		var angle := TAU * float(sample) / 24.0
		local_position = center + Vector2.from_angle(angle) * radius
		screen_position = _control_screen_point(surface, local_position)
		var drag := InputEventScreenDrag.new()
		drag.index = 77
		drag.position = screen_position
		drag.relative = screen_position - prior_screen
		prior_screen = screen_position
		surface.get_viewport().push_input(drag, false)
	var release := InputEventScreenTouch.new()
	release.index = 77
	release.position = screen_position
	release.pressed = false
	surface.get_viewport().push_input(release, false)
	await _frames(2)
	world._process(2.3)
	await _frames(2)
	_check("one routed one-finger loop completes Racer without a shortcut",
		surface.input_started and not surface.demo_active
		and surface.completion_accepted and act.state == "won")


func _floor_for_act(live_index: int) -> int:
	for floor_index: int in range(OperaHouse.FLOOR_ACT_INDICES.size()):
		if (OperaHouse.FLOOR_ACT_INDICES[floor_index] as Array).has(live_index):
			return floor_index
	return -1


func _tap_control(control: Control, touch_index: int) -> void:
	var screen_position := _control_screen_point(control, control.size * 0.5)
	var press := InputEventScreenTouch.new()
	press.index = touch_index
	press.position = screen_position
	press.pressed = true
	control.get_viewport().push_input(press, false)
	var release := InputEventScreenTouch.new()
	release.index = touch_index
	release.position = screen_position
	release.pressed = false
	control.get_viewport().push_input(release, false)


func _control_screen_point(control: Control, local_position: Vector2) -> Vector2:
	var viewport := control.get_viewport()
	return viewport.get_screen_transform() \
		* (control.get_screen_transform() * local_position)


func _direct_child_ids(node: Node) -> Array[int]:
	var ids: Array[int] = []
	for child: Node in node.get_children():
		ids.append(int(child.get_instance_id()))
	ids.sort()
	return ids


func _descendants_are_canvas(node: Node) -> bool:
	for child: Node in node.get_children():
		# Plain Node children are nonvisual lifecycle/animation controllers. Any
		# presentation-bearing descendant must belong to the Canvas hierarchy.
		if not (child is CanvasItem or child is CanvasLayer \
				or child is AudioStreamPlayer or child.get_class() == "Node"):
			print("OPERA|non_canvas_descendant: path=%s class=%s" % [
				String(child.get_path()), child.get_class(),
			])
			return false
		if not _descendants_are_canvas(child):
			return false
	return true


func _frames(count: int) -> void:
	for _frame: int in range(count):
		await process_frame


func _check(label: String, condition: bool) -> void:
	print("OPERA|%s: %s" % [label, "OK" if condition else "FAIL"])
	if not condition:
		bad += 1


func _finish() -> void:
	print("OPERA|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit(0 if bad == 0 else 1)
