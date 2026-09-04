extends SceneTree
## Fail-closed WP-D3 probe. It builds the route card in isolation and checks
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
	main.day_one_active = true
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
		var card: Control = stage.get_node_or_null("DayOneRouteCard") as Control
		var pointer: Node = card.get_node_or_null("DayOneRouteGhostHand") \
			if card != null else null
		var card_rect := card.get_rect() if card != null else Rect2()
		var view_rect := Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
		_check("%s handoff builds" % handoff["target"], shown)
		_check("%s card visible and opaque" % handoff["target"],
			card != null and card.visible and card.modulate.a > 0.0)
		_check("%s target intersects view" % handoff["target"],
			card != null and card_rect.intersects(view_rect))
		_check("%s target is actionable and unobscured" % handoff["target"],
			card != null and card.mouse_filter == Control.MOUSE_FILTER_STOP
			and bool(card.get_meta("actionable_target", false))
			and bool(card.get_meta("target_unobscured", false)))
		_check("%s pointer is visible and nonzero alpha" % handoff["target"],
			pointer != null and pointer.visible \
			and (pointer as CanvasItem).modulate.a > 0.0
			and bool(pointer.get_meta("visual_pointer", false)))
		_check("%s exact voice is same-frame" % handoff["target"],
			main.hud_msg.text != ""
			and String(card.get_meta("semantic_voice_key", ""))
			== String(handoff["voice"]))
		main._clear_day_one_pool_route()
	main.queue_free()
	print("DAY_ONE_HANDOFFS|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_HANDOFFS|", label, ": ", "OK" if ok else "FAIL")
