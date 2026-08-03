extends SceneTree
# Throne triggers — both of them, driven the way a four-year-old drives them.
#
# 1. Pearl Castle Grand Hall: the throne is a painted hotspot two screens to
#    the right of where she spawns. Walking there must bring it on screen, and
#    a REAL touch on it must fire the Crown Star and (owner 2026-07-19) Princess
#    Huluu's stuffie offer. Tapping through the Button's `pressed` signal is not
#    a test — the 2026-08-02 report was about the trigger not firing in the
#    child's hands, so every tap here goes through the viewport.
# 2. Butterfly World Star Hall: sitting on the Moon Throne must award the
#    STAR PRINCESS sticker.

const THRONE_FOOT := Vector2(3090.0, 690.0)

var main: ReefMain
var checks_failed := 0

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

func _throne_button() -> Button:
	for record: Dictionary in main.castle_room_door_hotspots:
		var data: Dictionary = record.get("data", {})
		if String(data.get("id", "")) == "__throne":
			return record.get("button") as Button
	return null

func _tap_throne(rooms: CastleRooms25D) -> void:
	# walk her to the throne end of the hall and touch the painted throne
	rooms._position_player_at_foot(THRONE_FOOT, false)
	await _frames(240)   # the hall camera pans a full screen width
	var button: Button = _throne_button()
	if button == null or not button.visible:
		return
	_touch(button.get_global_transform_with_canvas() * (button.size * 0.5))
	await _frames(120)   # portal walk + its tweened callback

func _run() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	main.pearl_count = main.PEARL_TOTAL
	main.trophies = 5
	main.level2_done_once = true
	main.companion_id = ""
	main.g["crown_won"] = false
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(24)

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	_ck("hall_open", rooms.is_open() and main.castle_room_id == "main_hall",
		main.castle_room_id)
	var button: Button = _throne_button()
	_ck("throne_hotspot_built", button != null)
	if button == null:
		_finish()
		return
	_ck("throne_offscreen_at_spawn", not button.visible,
		"she starts a screen away from it")

	# ---- the walk, then a real touch ----
	rooms._position_player_at_foot(THRONE_FOOT, false)
	await _frames(240)
	button = _throne_button()
	_ck("throne_onscreen_at_the_throne_end", button.visible,
		str(button.get_global_rect()))
	var centre: Vector2 = button.get_global_transform_with_canvas() \
		* (button.size * 0.5)
	_ck("throne_hitbox_is_child_sized",
		button.size.x >= 112.0 and button.size.y >= 112.0, str(button.size))
	_touch(centre)
	await _frames(120)
	_ck("touch_awards_crown_star", bool(main.g.get("crown_won", false)))

	# ---- and Princess Huluu's offer rides the same touch ----
	await _frames(180)
	_ck("throne_offers_a_stuffie_friend", main.companion_layer != null,
		"companion_id=%s" % main.companion_id)
	var companion: CompanionSystem = main._companion_ref()

	# closing without choosing must not burn the moment — the throne re-offers
	companion.close_picker()
	await _frames(10)
	_ck("picker_closed", main.companion_layer == null)
	await _tap_throne(rooms)
	await _frames(180)
	_ck("throne_re_offers_after_a_closed_picker",
		main.companion_layer != null and main.companion_id == "")

	# ---- once she has a friend, the throne is a throne again ----
	companion.close_picker()
	await _frames(10)
	main.companion_id = "birdie"
	await _tap_throne(rooms)
	await _frames(180)
	_ck("no_re_offer_once_she_has_a_friend", main.companion_layer == null,
		"companion_id=%s" % main.companion_id)
	_ck("throne_still_waves", bool(main.g.get("crown_won", false)))

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
