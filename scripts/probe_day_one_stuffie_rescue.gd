extends SceneTree
## Focused live probe for Day One's Stuffie Room. The room must use the
## complete bag-free Baby Eagle pose, reject placeholder completion, require
## both pinning bunnies, persist the rescue, and unlock the Art Room.

var main: ReefMain
var failures: int = 0

func _init() -> void:
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _settle(8)
	main._enter_castle_interior_now(false)
	await _settle(8)
	var director: DayOneDirector = main._day_one_ref()
	director.restore_state({
		"day_one_active": true,
		"day_one_completed_rooms": ["bathroom", "pool"],
		"day_one_pool_cleanup_step": 4,
		"day_one_pool_rumi_met": true,
	})
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("playroom", false)
	await _settle(2)
	_check_initial_scene(rooms, director)
	main.day_one_activate_castle_room("playroom")
	_check("placeholder button cannot complete the rescue",
		not director.is_room_completed("stuffie")
		and director.current_room_id == "stuffie")
	var left: Dictionary = main.castle_room_item_sprites.get(
		"eagle_pin_left", {}) as Dictionary
	rooms._position_player_at_foot(
		left.get("contact_foot", Vector2.ZERO) as Vector2, false)
	rooms.tick(0.016)
	await _settle(2)
	_check("first bunny saves but does not unlock the Art Room",
		bool(main.stuffie_wins.get("rescued_eagle_pin_left", false))
		and not director.is_room_completed("stuffie")
		and director.current_room_id == "stuffie")
	var right: Dictionary = main.castle_room_item_sprites.get(
		"eagle_pin_right", {}) as Dictionary
	rooms._position_player_at_foot(
		right.get("contact_foot", Vector2.ZERO) as Vector2, false)
	rooms.tick(0.016)
	await _settle(2)
	_check("second bunny completes Stuffie and unlocks Art",
		bool(main.stuffie_wins.get("rescued_eagle", false))
		and director.is_room_completed("stuffie")
		and director.current_room_id == "art"
		and main.day_one_can_enter_castle_room("craft_room"))
	_check("Day One rescue completion is persisted",
		(main.save_data.get("day_one_completed_rooms", []) as Array).has(
			"stuffie")
		and bool((main.save_data.get("stuffie_wins", {}) as Dictionary).get(
			"rescued_eagle", false)))
	print("DAY_ONE_STUFFIE|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)

func _check_initial_scene(rooms: CastleRooms25D,
		director: DayOneDirector) -> void:
	var eagle_record: Dictionary = main.castle_room_item_sprites.get(
		"baby_eagle_rescue", {}) as Dictionary
	var eagle: Sprite2D = eagle_record.get("sprite") as Sprite2D
	_check("Stuffie is the live Day One room",
		director.current_room_id == "stuffie"
		and main.castle_room_id == "playroom")
	_check("complete bag-free Baby Eagle pose is live",
		eagle != null and eagle.texture != null
		and eagle.texture.resource_path ==
			"res://assets/castle/day_one_stuffie/baby_eagle_pinned.png")
	_check("two separate pinning bunnies are live in front",
		main.castle_room_item_sprites.has("eagle_pin_left")
		and main.castle_room_item_sprites.has("eagle_pin_right")
		and not rooms.playroom_rescue_done())

func _settle(frames: int) -> void:
	for _index: int in range(frames):
		await process_frame

func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_STUFFIE|", label, ": ", "OK" if ok else "FAIL")
