extends SceneTree
## Fail-closed WP-D3 probe. It builds the shared arrow in isolation and checks
## the same-frame visual/voice contract without booting the heavyweight world.

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
	main.day_one_cleaned_rooms.assign({"bathroom": true, "pool": true, "stuffie": true, "art": true})
	main.global_navigation_button = Button.new()
	main.add_child(main.global_navigation_button)
	main._navigation_ref().position_button(main.global_navigation_button)
	main._navigation_push("pearl_castle_room", main, func() -> void: pass)
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
		var shown: bool = main._show_day_one_room_handoff(
			String(handoff["target"]), String(handoff["voice"]))
		var arrow: Button = main.global_navigation_button
		var pointer: CanvasItem = arrow.get_node_or_null("DayOneRouteGhostHand") as CanvasItem
		var glow: CanvasItem = arrow.get_node_or_null("DayOneArrowGlow") as CanvasItem
		_check("%s handoff builds" % handoff["target"], shown)
		_check("%s uses only the shared arrow" % handoff["target"],
			main._day_one_pool_route_button == arrow
			and stage.get_node_or_null("DayOneRouteCard") == null
			and arrow.get_node_or_null("ApprovedRoomPreview") == null)
		_check("arrow is anchored upper right with a generous target",
			arrow.anchor_right == 1.0 and arrow.offset_right == -18.0
			and arrow.size == Vector2(112.0, 112.0) and arrow.visible and not arrow.disabled)
		_check("correct next room is bound", String(arrow.get_meta(
			"day_one_route_target", "")) == String(handoff["target"]))
		_check("pointer accompanies existing completion speech",
			pointer != null and pointer.visible and main.hud_msg.text != ""
			and String(arrow.get_meta("semantic_voice_key", "")) in [
				"day_one_room_clean", "day_one_pool_ready"])
		var save_before: Dictionary = main._day_one_ref().serialize_state().duplicate(true)
		main._navigation_ref().tick_attention(7.0)
		main._sync_day_one_bathroom_cleanup()
		main._navigation_ref().tick_attention(7.9)
		_check("no early flashing", glow != null and glow.modulate.a == 0.0
			and arrow.self_modulate == Color.WHITE)
		main._navigation_ref().tick_attention(0.1)
		_check("red glow starts at fifteen seconds", glow != null and glow.modulate.a > 0.0
			and arrow.self_modulate != Color.WHITE)
		var initial_alpha: float = glow.modulate.a
		main._navigation_ref().tick_attention(1.0)
		_check("glow pulses gently", glow.modulate.a > initial_alpha)
		_check("idle never advances or pays progress",
			main._day_one_ref().serialize_state() == save_before
			and main.castle_room_id == String(handoff["source"]))
		var tap := InputEventScreenTouch.new()
		tap.pressed = true
		main._input(tap)
		_check("touch resets glow immediately", main.navigation_idle_seconds == 0.0
			and glow.modulate.a == 0.0 and arrow.self_modulate == Color.WHITE)
		main._navigation_ref().tick_attention(20.0)
		_check("held touch does not trigger inactivity", main.navigation_idle_seconds == 0.0)
		tap.pressed = false
		main._input(tap)
		main.navigation_attention_blocks = 1
		main._navigation_ref().tick_attention(20.0)
		_check("focus loss suppresses attention", main.navigation_idle_seconds == 0.0
			and not pointer.visible)
		main.navigation_attention_blocks = 0
		main.pause_panel = Control.new()
		main.add_child(main.pause_panel)
		main.pause_panel.visible = false
		main._navigation_ref().tick_attention(16.0)
		main._pause_ref().toggle_pause()
		_check("pause immediately clears attention without a process tick",
			main.navigation_idle_seconds == 0.0 and glow.modulate.a == 0.0
			and not pointer.visible)
		main._pause_ref().toggle_pause()
		main.pause_panel.free()
		main.pause_panel = null
		main._navigation_push("test_overlay", main, func() -> void: pass)
		main._navigation_ref().tick_attention(20.0)
		_check("another overlay owns Back", not main._navigation_ref().handoff_actionable()
			and main.navigation_idle_seconds == 0.0)
		main._navigation_ref().press()
		_check("overlay Back preserves next-room handoff",
			main._day_one_room_handoff_target == String(handoff["target"])
			and main._navigation_ref().top_id() == "pearl_castle_room")
		main._clear_day_one_pool_route()
		_check("teardown keeps arrow and removes attention", is_instance_valid(arrow)
			and arrow.get_node_or_null("DayOneArrowGlow") == null
			and arrow.self_modulate == Color.WHITE)
	main.queue_free()
	print("DAY_ONE_HANDOFFS|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_HANDOFFS|", label, ": ", "OK" if ok else "FAIL")
