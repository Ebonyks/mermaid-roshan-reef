extends SceneTree
## Fail-closed Day One handoff probe. Completion may cue the route, but it must
## never repurpose the sole global Back button as a forward transport control.

var failures: int = 0
const TARGETS: Array[Dictionary] = [
	{"source": "bubble_bath", "target": "mermaid_pool", "voice": "day_one_pool_ready"},
	{"source": "mermaid_pool", "target": "playroom", "voice": "day_one_new_door"},
	{"source": "playroom", "target": "craft_room", "voice": "day_one_new_door"},
	{"source": "craft_room", "target": "__royal_hall", "voice": "day_one_all_rooms_clean"},
]


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var main := ReefMain.new()
	get_root().add_child(main)
	main.set_process(false)
	main.start_menu_active = false
	main.intro_active = false
	main.day_one_active = true
	main.day_one_cleaned_rooms.assign({
		"bathroom": true, "pool": true, "stuffie": true, "art": true})
	main.global_navigation_button = Button.new()
	main.global_navigation_button.name = "GlobalNavigationButton"
	main.add_child(main.global_navigation_button)
	main._navigation_ref().position_button(main.global_navigation_button)
	main.castle_room_stage = Control.new()
	main.castle_room_stage.size = StorybookUI.CANVAS_SIZE
	main.add_child(main.castle_room_stage)
	main.hud_msg = Label.new()
	main.add_child(main.hud_msg)
	main.voice = AudioStreamPlayer.new()
	main.add_child(main.voice)
	var voice_player := AudioStreamPlayer.new()
	main.add_child(voice_player)
	main.voice_pool.append(voice_player)
	var stage: Control = main.castle_room_stage
	for handoff: Dictionary in TARGETS:
		main.castle_room_id = String(handoff["source"])
		main._navigation_push("pearl_castle_room", main, func() -> void:
			main.castle_room_id = "main_hall")
		var shown: bool = main._show_day_one_room_handoff(
			String(handoff["target"]), String(handoff["voice"]))
		var back: Button = main.global_navigation_button
		_check("%s route cue builds" % handoff["target"], shown)
		_check("%s completion creates no forward overlay" % handoff["target"],
			stage.find_children("*", "Button", true, false).is_empty()
			and stage.get_node_or_null("DayOneRouteCard") == null
			and back.get_node_or_null("DayOneRouteGhostHand") == null
			and back.get_node_or_null("DayOneArrowGlow") == null)
		_check("global Back stays upper left with a generous target",
			back.anchor_left == 0.0 and back.anchor_right == 0.0
			and back.offset_left == 18.0 and back.offset_right == 130.0
			and back.size == Vector2(112.0, 112.0)
			and String(back.get_meta("global_navigation_mode", "")) == "back")
		_check("route target remains internal, not button metadata",
			main._day_one_room_handoff_target == String(handoff["target"])
			and not back.has_meta("day_one_route_target")
			and not back.has_meta("day_one_route_handoff"))
		_check("completion supplies a short hall-and-door cue",
			main.hud_msg.text.contains("hall")
			and main.hud_msg.text.contains("glowing door"))
		var save_before: Dictionary = \
			main._day_one_ref().serialize_state().duplicate(true)
		main._navigation_ref().press()
		_check("Back returns to the hall instead of advancing",
			main.castle_room_id == "main_hall"
			and main._day_one_room_handoff_target == String(handoff["target"])
			and main._day_one_ref().serialize_state() == save_before)
		main._clear_day_one_pool_route()
		_check("cue teardown preserves the sole global control",
			is_instance_valid(back)
			and main._day_one_room_handoff_target.is_empty()
			and back.get_child_count() == 0)
	main.queue_free()
	print("DAY_ONE_HANDOFFS|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_HANDOFFS|", label, ": ", "OK" if ok else "FAIL")
