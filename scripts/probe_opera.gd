extends SceneTree

const ROUTE_READY_FRAME_LIMIT := 600
const ROUTE_READY_TIMEOUT_MSEC := 3000
const ROUTE_CARD_MIN_SIZE := Vector2(154.0, 154.0)
const ROUTE_CARD_MIN_GAP := 22.0
const ROUTE_CANVAS_RECT := Rect2(0.0, 0.0, 1280.0, 720.0)
# Current Castle composition: the centered 270 px standee scales down to
# 194.4 px at the shallowest route-room walk depth (foot y=390), beginning at
# y=195.6. This deliberately wider/lower rectangle also reserves the tail and
# contact-shadow area through the front of the walk lane.
const ROUTE_ROSHAN_KEEP_CLEAR := Rect2(360.0, 190.0, 560.0, 490.0)
const ROUTE_WIDE_VIEWPORT := Vector2(1600.0, 720.0)
## MA-OPERA-012 product-route regression.
##
## The Opera is no longer an all-career destination. Each of the thirteen
## sparse historical career slots owns exactly one picture-first Castle-room
## route. This probe touches every shipping card through the real viewport,
## proves cancel/completion return to the same room, and protects passive,
## reward, replay, pause-curtain and sixteen-bit save behavior.

const ROUTE_ROOMS: Array[String] = [
	"kitchen", "opera_hall", "library", "craft_room", "playroom",
	"bubble_bath", "mermaid_pool", "dining_room", "movie_lounge",
]
const EXPECTED_ROOM_ACTS := {
	"kitchen": [0, 3],
	"opera_hall": [2, 13, 8],
	"library": [1],
	"craft_room": [10],
	"playroom": [5, 7],
	"bubble_bath": [15],
	"mermaid_pool": [11],
	"dining_room": [6],
	"movie_lounge": [12],
}

var main: ReefMain
var rooms: CastleRooms25D
var routes: CastleCareerRoutes
var bad := 0


func _init() -> void:
	seed(20260812)
	Engine.time_scale = 8.0
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	main.day_one_active = false
	main._skip_intro()
	main.opera_progress = 0
	main.opera_stars = 0
	main.opera_done = false
	main.stickers.erase("showtime")
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	await _frames(12)
	rooms = main._castle_rooms_ref()
	routes = main._castle_career_routes_ref()
	routes.sync()

	_check("the real Castle picture stage is the only career entry surface",
		rooms.is_open() and main.castle_room_stage != null
		and main.castle_room_layer != null and main.castle_room_layer.visible
		and main.game == "level2" and String(main.g.get("phase", "")) == "hall")
	_check("Castle careers, ambient motion and phone pause stack visibly",
		main.castle_room_layer.layer == 14
		and main.living_layer != null and main.living_layer.visible
		and main.living_layer.layer == 15
		and main.pause_layer != null and main.pause_layer.layer == 16)
	_audit_stable_roster_and_routes()
	_audit_save_matrix()
	await _audit_all_room_cards()
	await _audit_no_hidden_hub()
	await _audit_wrong_and_passive_routes()
	await _audit_cancel_return()
	await _audit_all_career_lifecycles()
	await _audit_replay_curtain()
	await _finish()


func _audit_stable_roster_and_routes() -> void:
	var exact_live: Array[int] = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15]
	var exact_retired: Array[int] = [4, 9, 14]
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
	_check("the nine owner-approved Castle route sets are exact",
		CastleCareerRoutes.ROOM_ACT_INDICES == EXPECTED_ROOM_ACTS)
	_check("Opera Hall contains exactly Ballerina, Pop Star and Magician",
		CastleCareerRoutes.act_indices_for_room("opera_hall") == [2, 13, 8])
	_check("Movie Lounge is Racer's one canonical Castle home",
		CastleCareerRoutes.room_for_act(12) == "movie_lounge"
		and CastleCareerRoutes.act_indices_for_room("movie_lounge") == [12])
	_check("there is no generic all-career lobby script",
		not ResourceLoader.exists("res://scripts/opera_lobby_2d.gd"))

	var routed: Array[int] = CastleCareerRoutes.routed_act_indices()
	_check("all and only the thirteen live slots have one room route",
		routed == exact_live)
	var roster_ok := true
	var career_ids: Dictionary = {}
	for slot: int in range(OperaHouse.ACTS.size()):
		var config: Dictionary = OperaHouse.ACTS[slot]
		roster_ok = roster_ok and int(config.get("save_bit", -1)) == slot
		if OperaHouse.is_live_act_index(slot):
			var career_id := String(config.get("costume", ""))
			roster_ok = roster_ok and not bool(config.get("retired", false)) \
				and not career_id.is_empty() and not career_ids.has(career_id) \
				and CastleCareerRoutes.room_for_act(slot) != ""
			career_ids[career_id] = true
		else:
			roster_ok = roster_ok and bool(config.get("retired", false)) \
				and config.size() == 2 \
				and CastleCareerRoutes.room_for_act(slot) == ""
	_check("every live career and tombstone retains its original bit", roster_ok)
	_check("all thirteen careers keep unique Canvas identities",
		career_ids.size() == OperaHouse.ACTIVE_ACT_COUNT)


func _audit_save_matrix() -> void:
	var state := SaveState.new(main)
	var cases: Array[Dictionary] = [
		{"label": "legacy progress 0", "input": {"opera_progress": 0},
			"raw": 0x0000, "effective": 0},
		{"label": "legacy progress 15", "input": {"opera_progress": 15},
			"raw": 0x7FFF, "effective": 12},
		{"label": "legacy progress 16", "input": {"opera_progress": 16},
			"raw": 0xFFFF, "effective": 13},
		{"label": "retired bits only", "input": {"opera_stars": 0x4210},
			"raw": 0x4210, "effective": 0},
		{"label": "all live careers", "input": {"opera_stars": 0xBDEF},
			"raw": 0xBDEF, "effective": 13},
		{"label": "old all-bits completion", "input": {"opera_stars": 0xFFFF},
			"raw": 0xFFFF, "effective": 13},
		{"label": "overflow clamps to sixteen bits",
			"input": {"opera_stars": 0x1FFFF},
			"raw": 0xFFFF, "effective": 13},
		{"label": "negative mask clamps safely", "input": {"opera_stars": -9},
			"raw": 0x0000, "effective": 0},
	]
	for fixture: Dictionary in cases:
		var normalised: Dictionary = state._normalise_save(
			fixture["input"] as Dictionary)
		_check("save migration keeps %s exact" % String(fixture["label"]),
			int(normalised.get("opera_stars", -1)) == int(fixture["raw"])
			and int(normalised.get("opera_progress", -1)) \
				== int(fixture["effective"])
			and not bool(normalised.get("opera_done", true)))


func _audit_all_room_cards() -> void:
	var seen: Array[int] = []
	for room_id: String in ROUTE_ROOMS:
		rooms.show_room(room_id, false)
		await _frames(3)
		routes.sync()
		if room_id == "opera_hall":
			routes.open_opera_venue()
			await _frames(3)
		var expected: Array[int] = CastleCareerRoutes.act_indices_for_room(room_id)
		var actual: Array[int] = []
		var room_card_rects: Array[Rect2] = []
		var room_card_geometry_ok := true
		var pictures_ok := routes.root != null and routes.root.visible \
			and bool(routes.root.get_meta("room_owned_career_routes", false))
		for button: Button in routes.buttons:
			var act_index := int(button.get_meta("act_index", -1))
			actual.append(act_index)
			seen.append(act_index)
			var presentation := String(button.get_meta("presentation", ""))
			var base_ok := button.visible \
				and button.text.is_empty() and not button.clip_contents \
				and button.size.x >= 110.0 and button.size.y >= 110.0 \
				and String(button.get_meta("castle_room_id", "")) == room_id \
				and (button.get_meta("screen_hit_size", Vector2.ZERO) as Vector2).x \
					>= 110.0 \
				and (button.get_meta("screen_hit_size", Vector2.ZERO) as Vector2).y \
					>= 110.0
			if presentation == "historical_three_floor_portal":
				var portal_focus := button.get_theme_stylebox("focus") \
					as StyleBoxFlat
				pictures_ok = pictures_ok and base_ok \
					and not bool(button.get_meta("opaque_card", true)) \
					and bool(button.get_meta("painted_door_hit_region", false)) \
					and not bool(button.get_meta("floating_decoration", true)) \
					and button.get_child_count() == 0 \
					and portal_focus != null \
					and portal_focus.border_width_left == 0 \
					and is_zero_approx(portal_focus.bg_color.a) \
					and int(button.get_meta("floor_index", -1)) in [0, 1, 2]
			else:
				var crest := button.get_node_or_null("CareerCrest") as TextureRect
				var actor := button.get_node_or_null("RoshanActor") as TextureRect
				var actor_frame := actor.texture as AtlasTexture \
					if actor != null else null
				var card_rect := Rect2(button.position, button.size)
				var screen_hit_size := button.get_meta(
					"screen_hit_size", Vector2.ZERO) as Vector2
				var effective_touch_size := Vector2(
					maxf(button.size.x, button.custom_minimum_size.x),
					maxf(button.size.y, button.custom_minimum_size.y))
				var wide_card_rect := _fit_stage_rect(
					card_rect, ROUTE_WIDE_VIEWPORT)
				var wide_keep_clear := _fit_stage_rect(
					ROUTE_ROSHAN_KEEP_CLEAR, ROUTE_WIDE_VIEWPORT)
				room_card_rects.append(card_rect)
				room_card_geometry_ok = room_card_geometry_ok \
					and ROUTE_CANVAS_RECT.encloses(card_rect) \
					and button.size.x >= ROUTE_CARD_MIN_SIZE.x \
					and button.size.y >= ROUTE_CARD_MIN_SIZE.y \
					and effective_touch_size.x >= ROUTE_CARD_MIN_SIZE.x \
					and effective_touch_size.y >= ROUTE_CARD_MIN_SIZE.y \
					and screen_hit_size.x >= ROUTE_CARD_MIN_SIZE.x \
					and screen_hit_size.y >= ROUTE_CARD_MIN_SIZE.y \
					and not card_rect.intersects(
						ROUTE_ROSHAN_KEEP_CLEAR, true) \
					and Rect2(Vector2.ZERO, ROUTE_WIDE_VIEWPORT).encloses(
						wide_card_rect) \
					and not wide_card_rect.intersects(wide_keep_clear, true)
				pictures_ok = pictures_ok and base_ok \
					and bool(button.get_meta("picture_first", false)) \
					and not button.disabled \
					and actor_frame != null and actor_frame.atlas != null \
					and actor_frame.atlas.resource_path.contains(
						"/actors/animation/roshan_")
		_check("%s exposes its exact room-owned career pictures" % room_id,
			actual == expected and pictures_ok)
		if room_id != "opera_hall":
			for card_index: int in range(1, room_card_rects.size()):
				var previous: Rect2 = room_card_rects[card_index - 1]
				var current: Rect2 = room_card_rects[card_index]
				room_card_geometry_ok = room_card_geometry_ok \
					and is_equal_approx(previous.position.y, current.position.y) \
					and not previous.intersects(current, true) \
					and current.position.x - previous.end.x \
						>= ROUTE_CARD_MIN_GAP
			_check("%s route cards stay full-size, separated and clear Roshan" \
					% room_id,
				room_card_rects.size() == expected.size() \
				and room_card_geometry_ok)
		if room_id == "opera_hall":
			var venue := routes.opera_venue
			var venue_ok := venue != null and venue.is_open() \
				and bool(venue.get_meta("true_2d_venue", false)) \
				and String(venue.get_meta("historical_layout_commit", "")) \
					== "90d19190" \
				and int(venue.get_meta("historical_floor_count", 0)) == 3 \
				and int(venue.get_meta("historical_portal_count", 0)) == 12 \
				and int(venue.get_meta("active_room_owned_portal_count", 0)) == 3 \
				and int(venue.get_meta("decorative_closed_portal_count", 0)) == 9 \
				and int(venue.get_meta("bubble_lift_count", 0)) == 2 \
				and int(venue.get_meta("floating_portal_decoration_count", -1)) == 0 \
				and venue.find_children("CareerCrest", "TextureRect", true, false).is_empty() \
				and venue.find_children("CareerPearl", "Panel", true, false).is_empty() \
				and venue.find_children("VenueTile_*", "TextureRect", true, false).size() == 8 \
				and venue.find_children("BubbleLift*", "Button", true, false).size() == 2 \
				and venue.get_node_or_null("LobbyRoshanCutout") is TextureRect
			_check("Opera Hall opens the recovered three-floor explorable venue",
				venue_ok)
	seen.sort()
	_check("the nine visible room sets contain every career exactly once",
		seen == OperaHouse.LIVE_ACT_INDICES)


func _audit_no_hidden_hub() -> void:
	rooms.show_room("opera_hall", false)
	await _frames(3)
	routes.sync()
	var stars_before := main.opera_stars
	var pearls_before := main.pearl_count
	main._start_opera()
	await _frames(3)
	var venue := routes.opera_venue
	_check("the Opera stage star opens the recovered three-floor venue",
		main.opera_game == null and main.opera_pending_act_index == -1
		and routes.root != null and routes.root.visible
		and venue != null and venue.is_open()
		and int(venue.get_meta("historical_floor_count", 0)) == 3
		and int(venue.get_meta("historical_portal_count", 0)) == 12
		and main.opera_stars == stars_before and main.pearl_count == pearls_before)
	_check("the recovered venue is not an all-career picker",
		main.find_children("*OperaLobby*", "Node", true, false).is_empty()
		and main.find_children("*FloorTab*", "Node", true, false).is_empty()
		and venue.career_buttons().size() == 3)


func _audit_wrong_and_passive_routes() -> void:
	rooms.show_room("library", false)
	await _frames(3)
	routes.sync()
	var stars_before := main.opera_stars
	var progress_before := main.opera_progress
	var pearls_before := main.pearl_count
	var children_before := _direct_child_ids(main)
	await _frames(90)
	_check("idle room pictures cannot award or launch a career",
		main.opera_game == null and main.opera_stars == stars_before
		and main.opera_progress == progress_before and main.pearl_count == pearls_before
		and _direct_child_ids(main) == children_before)
	# This calls the real route guard with a current room but an act owned by a
	# different room. It must be a quiet no-op, not a hidden direct launcher.
	routes._launch("library", 0)
	await _frames(3)
	_check("a career picture cannot launch from the wrong room",
		main.opera_game == null and main.opera_pending_act_index == -1
		and main.castle_room_id == "library" and main.castle_room_layer.visible
		and main.opera_stars == stars_before and main.pearl_count == pearls_before)
	# A valid room/index pair is still rejected when that room is not the live
	# Castle owner. This closes a programmatic route around the visible cards.
	main._start_opera_from_room(0, "kitchen")
	await _frames(3)
	_check("a valid career tuple cannot launch outside its current Castle room",
		main.opera_game == null and main.opera_pending_act_index == -1
		and main.opera_return_room == "" and main.castle_room_id == "library"
		and main.castle_room_layer.visible and main.opera_stars == stars_before
		and main.pearl_count == pearls_before)
	for retired_index: int in OperaHouse.RETIRED_ACT_INDICES:
		_check("retired slot %d has no route or playable config" % retired_index,
			CastleCareerRoutes.room_for_act(retired_index) == ""
			and not OperaHouse.is_live_act_index(retired_index)
			and not OperaAct.supports_config(OperaHouse.ACTS[retired_index]))


func _audit_cancel_return() -> void:
	var act_index := 1
	var room_id := CastleCareerRoutes.room_for_act(act_index)
	var expected_room_track := main._castle_room_music_track(room_id)
	var stars_before := main.opera_stars
	var progress_before := main.opera_progress
	var pearls_before := main.pearl_count
	var house := await _start_via_room_touch(room_id, act_index)
	if house == null:
		return
	_check("Detective owns its career cue while Library remains its return music",
		house.act != null and main.cur_track == "opera_detective"
		and house.act.prior_music == expected_room_track)
	await _frames(90)
	_check("an idle Detective act cannot advance or award itself",
		house.act != null and house.act.state == "play"
		and main.opera_stars == stars_before
		and main.opera_progress == progress_before
		and main.pearl_count == pearls_before)
	house._leave_early()
	await _frames(4)
	_check("cancel returns to the exact Library with no reward",
		_route_returned(room_id) and main.opera_stars == stars_before
		and main.opera_progress == progress_before and main.pearl_count == pearls_before
		and main.cur_track == expected_room_track)


func _audit_all_career_lifecycles() -> void:
	var pearl_baseline := main.pearl_count
	for act_index: int in OperaHouse.LIVE_ACT_INDICES:
		var room_id := CastleCareerRoutes.room_for_act(act_index)
		var stars_before := main.opera_stars
		var progress_before := main.opera_progress
		var house := await _start_via_room_touch(room_id, act_index)
		if house == null:
			continue
		var act := house.act as OperaAct
		var career_id := String((OperaHouse.ACTS[act_index] as Dictionary).get(
			"costume", "career"))
		_check("%s starts only its stable Canvas career" % career_id,
			act != null and house.act_index == act_index
			and int(act.config.get("save_bit", -1)) == act_index
			and act.use_career_world_2d and act.career_world_2d != null
			and act.career_world_2d.layer == 10
			and main.living_layer != null and main.living_layer.layer == 11
			and main.hud_layer != null and main.hud_layer.visible
			and main.hud_layer.layer == 12
			and main.pause_layer != null and main.pause_layer.layer == 13
			and _descendants_are_canvas(act)
			and (main.player == null or not main.player.visible)
			and main.kart_game == null)
		if act == null:
			continue
		if act_index == 12:
			var racer_voice_path := ""
			if main.voice_i > 0 and not main.voice_pool.is_empty():
				var voice_index := posmod(main.voice_i - 1, main.voice_pool.size())
				var racer_voice := main.voice_pool[voice_index] as AudioStreamPlayer
				if racer_voice != null and racer_voice.stream != null:
					racer_voice_path = racer_voice.stream.resource_path
			_check("Racer exact objective voice replaces its caption fallback",
				racer_voice_path == "res://assets/audio/voices/filler_v1/roshan_op_racer_tune_up_stage.ogg"
				and not main.hud_msg.visible and main.hud_msg.text.is_empty()
				and main.hud_layer.layer > act.career_world_2d.layer)
			main._pause_ref().toggle_pause()
			_check("pause sheet rises above the room-started Opera career",
				main.get_tree().paused and main.pause_panel.visible
				and main.pause_layer.layer == 29
				and main.pause_layer.layer > main.hud_layer.layer)
			main._pause_ref().toggle_pause()
			_check("resume restores the nonblocking pause layer",
				not main.get_tree().paused and not main.pause_panel.visible
				and main.pause_layer.layer == 13)
		await _frames(45)
		_check("%s cannot award itself while idle" % career_id,
			act.state == "play" and main.opera_stars == stars_before
			and main.opera_progress == progress_before)
		act._win()
		if act_index == 0:
			act.notification(NOTIFICATION_APPLICATION_PAUSED)
		else:
			act.win_t = 0.0
			act._process(0.1)
		await _frames(4)
		var expected_mask := stars_before | (1 << act_index)
		_check("%s saves once and returns to %s" % [career_id, room_id],
			_route_returned(room_id) and main.opera_stars == expected_mask
			and main.opera_progress == OperaHouse.live_star_count(expected_mask)
			and main.pearl_count == pearl_baseline
				+ OperaHouse.live_star_count(expected_mask) * 3
				+ (50 if OperaHouse.has_all_live_stars(expected_mask) else 0)
			and int(main.save_data.get("opera_stars", -1)) == expected_mask
			and int(main.save_data.get("opera_progress", -1)) \
				== OperaHouse.live_star_count(expected_mask))

	_check("all thirteen sparse careers complete through their nine rooms",
		OperaHouse.has_all_live_stars(main.opera_stars)
		and main.opera_stars == OperaHouse.ACTIVE_STAR_MASK
		and main.opera_progress == OperaHouse.ACTIVE_ACT_COUNT)
	_check("the finale reward and sticker are awarded exactly once",
		main.opera_done and bool(main.stickers.get("showtime", false))
		and main.pearl_count == pearl_baseline
			+ OperaHouse.ACTIVE_ACT_COUNT * 3 + 50)


func _audit_replay_curtain() -> void:
	var act_index := 0
	var room_id := CastleCareerRoutes.room_for_act(act_index)
	var completed_mask := main.opera_stars
	var completed_progress := main.opera_progress
	var pearls_before := main.pearl_count
	var house := await _start_via_room_touch(room_id, act_index)
	if house == null or house.act == null:
		return
	house.act._win()
	_check("replay curtain has earned but not yet duplicated the saved bit",
		house.act.state == "won" and main.opera_stars == completed_mask
		and main.pearl_count == pearls_before)
	house._leave_early()
	await _frames(4)
	_check("leaving during a replay curtain commits only the replay pearl",
		_route_returned(room_id) and main.opera_stars == completed_mask
		and main.opera_progress == completed_progress
		and main.pearl_count == pearls_before + 1 and main.opera_done
		and bool(main.stickers.get("showtime", false)))
	# Exercise the actual pause-sheet exit too: a neutral leave while play is
	# live must return to the same room without a star or pearl.
	house = await _start_via_room_touch(room_id, act_index)
	if house != null:
		main.toggle_pause()
		main._pause_ref()._leave_current_activity()
		await _frames(4)
		_check("neutral pause leave returns to the exact room without reward",
			_route_returned(room_id) and not main.get_tree().paused
			and main.opera_stars == completed_mask
			and main.opera_progress == completed_progress
			and main.pearl_count == pearls_before + 1)
	await _frames(60)
	_check("later frames cannot duplicate the curtain reward",
		main.opera_stars == completed_mask and main.pearl_count == pearls_before + 1
		and main.opera_game == null)


func _start_via_room_touch(room_id: String, act_index: int) -> OperaHouse:
	rooms.show_room(room_id, false)
	await _frames(3)
	routes.sync()
	if room_id == "opera_hall":
		_check("Opera Hall touch route enters the recovered foyer",
			routes.open_opera_venue())
		await _frames(2)
	var button := routes.button_for_act(act_index)
	if room_id == "opera_hall" and button != null:
		var venue := routes.opera_venue
		var target_floor := int(button.get_meta("floor_index", -1))
		var lift_attempts := 0
		while venue != null and venue.floor_index != target_floor \
				and lift_attempts < 4:
			var lift := venue.get_node_or_null("BubbleLift1") as Button
			if lift == null:
				break
			lift_attempts += 1
			var old_floor := venue.floor_index
			_tap_control(lift, 140 + act_index + venue.floor_index)
			var lift_deadline := Time.get_ticks_msec() + 2500
			for _wait_frame: int in range(ROUTE_READY_FRAME_LIMIT):
				await process_frame
				if venue.floor_index != old_floor:
					break
				if Time.get_ticks_msec() >= lift_deadline:
					break
		_check("slot %d reaches its Opera Hall venue floor" % act_index,
			venue != null and venue.floor_index == target_floor)
	_check("slot %d exposes its real %s picture" % [act_index, room_id],
		button != null and button.is_visible_in_tree() and not button.disabled
		and int(button.get_meta("act_index", -1)) == act_index)
	if button == null:
		return null
	_tap_control(button, 40 + act_index)
	var route_ready := await _await_route_ready(act_index)
	_check("slot %d reaches its routed career after the reveal" % act_index,
		route_ready)
	var house := main.opera_game as OperaHouse
	_check("slot %d launches through raw viewport touch" % act_index,
		house != null and main.game == "opera"
		and main.opera_active_act_index == act_index
		and main.opera_return_room == room_id
		and main.castle_room_id == room_id
		and main.castle_room_layer != null and not main.castle_room_layer.visible)
	return house


func _await_route_ready(act_index: int) -> bool:
	# A routed touch starts the career synchronously under the fade cover, but
	# LivingWorld intentionally waits for the 0.25 s reveal to clear before it
	# changes from Castle layer 15 to the career's layer 11. Frame duration is
	# runner-dependent, so sample the production-ready state instead of assuming
	# that four frames always outlive the tween.
	var expected_stage := "opera.act.%02d" % act_index
	var deadline_msec := Time.get_ticks_msec() + ROUTE_READY_TIMEOUT_MSEC
	for _frame: int in range(ROUTE_READY_FRAME_LIMIT):
		var fade_ready := main.fade_rect == null \
			or (main.fade_rect.modulate.a <= 0.02 \
				and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)
		if main.opera_game != null and fade_ready \
				and main.living_stage_id == expected_stage \
				and main.living_layer != null and main.living_layer.layer == 11:
			return true
		if Time.get_ticks_msec() >= deadline_msec:
			break
		await process_frame
	print("OPERA|route readiness evidence: act=%d stage=%s layer=%s fade=%s" % [
		act_index,
		main.living_stage_id,
		str(main.living_layer.layer if main.living_layer != null else -1),
		str(main.fade_rect.modulate.a if main.fade_rect != null else 0.0),
	])
	return false


func _route_returned(room_id: String) -> bool:
	routes.sync()
	return main.opera_game == null and main.opera_pending_act_index == -1 \
		and main.opera_active_act_index == -1 and main.opera_return_room == "" \
		and main.game == "level2" and main.castle_room_id == room_id \
		and main.castle_room_layer != null and main.castle_room_layer.visible \
		and routes.root != null and routes.root.visible


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


func _fit_stage_rect(stage_rect: Rect2, viewport_size: Vector2) -> Rect2:
	var fit_scale := minf(
		viewport_size.x / StorybookUI.CANVAS_SIZE.x,
		viewport_size.y / StorybookUI.CANVAS_SIZE.y)
	var fit_offset := (
		viewport_size - StorybookUI.CANVAS_SIZE * fit_scale) * 0.5
	return Rect2(
		fit_offset + stage_rect.position * fit_scale,
		stage_rect.size * fit_scale)


func _direct_child_ids(node: Node) -> Array[int]:
	var ids: Array[int] = []
	for child: Node in node.get_children():
		ids.append(int(child.get_instance_id()))
	ids.sort()
	return ids


func _descendants_are_canvas(node: Node) -> bool:
	for child: Node in node.get_children():
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
	var exit_code := 0 if bad == 0 else 1
	# Let the product owners tear down before SceneTree exits so leaked nodes or
	# resources cannot hide behind an assertion-green result.
	if main != null and is_instance_valid(main):
		if main.opera_game != null and is_instance_valid(main.opera_game):
			(main.opera_game as OperaHouse)._leave_early()
		if main._castle_rooms_ref().is_open():
			main._castle_rooms_ref().close()
		main.queue_free()
	# These RefCounted helpers own back-references to Main. Release the probe's
	# handles before shutdown so queued scene deletion can complete cleanly.
	routes = null
	rooms = null
	main = null
	for _frame: int in range(4):
		await process_frame
	quit(exit_code)
