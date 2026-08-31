extends SceneTree
## Focused Main Hall state/seam contract for the Chapter 3 Moonflower route.

var _failures := 0


func _check(label: String, passed: bool, detail: String = "") -> void:
	print("FAIRYROUTE|%s|%s%s" % [
		"OK" if passed else "FAIL",
		label,
		(" (%s)" % detail) if detail != "" else "",
	])
	if not passed:
		_failures += 1


func _count_named(root: Node, node_name: String) -> int:
	if root == null:
		return 0
	var count := 1 if root.name == node_name else 0
	for child: Node in root.get_children():
		count += _count_named(child, node_name)
	return count


func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main := scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame

	# Force a fresh pre-reveal state regardless of the isolated probe save.
	main.opera_done = false
	main.chapter2_story_complete = false
	main.chapter2_candle_taken = false
	main.chapter3_fairy_door_revealed = false
	main.chapter3_fairy_door_opened = false
	main.chapter3_fairy_mission_started = false
	main.galaxy_unlocked = false
	main.bwd_done = false
	main.fairy_skin_unlocked = false
	main.save_data["opera_done"] = false
	main.save_data["galaxy"] = false
	main.save_data["bwdone"] = false
	main.save_data["fairyskin"] = false
	main.save_data["chapter3_fairy_door_revealed"] = false
	main.save_data["chapter3_fairy_door_opened"] = false
	main.save_data["chapter3_fairy_mission_started"] = false
	main._enter_castle_interior_now(false)
	await process_frame
	await process_frame

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var door := main._fairy_conservatory_door_ref() \
		as FairyConservatoryDoor2D
	door.refresh()
	_check("Main Hall route opens", rooms.is_open())
	_check("fresh door is dormant",
		door.visual_state() == "closed")
	_check("dormant relief has no hotspot",
		door.fairy_conservatory_hotspot == null)
	_check("dormant relief has no cue", door.fairy_conservatory_cue == null)
	_check("dormant relief uses closed card",
		door.fairy_conservatory_card != null
		and String(door.fairy_conservatory_card.get_meta(
			"source_asset_path", "")).ends_with("moonflower_door_closed.png"))
	_check("Chapter 3 cannot preempt the birthday candle ending",
		not main._chapter_three_fairy_reveal_authorized())
	main.chapter2_candle_taken = true
	_check("candle take alone is not a completed Chapter 2 story",
		not main._chapter_three_fairy_reveal_authorized())
	main.chapter2_candle_taken = false
	main.chapter2_story_complete = true
	_check("story flag alone cannot bypass the physical candle take",
		not main._chapter_three_fairy_reveal_authorized())
	main.chapter2_story_complete = false
	main.opera_done = true
	_check("grandfathered global Opera completion retains its route",
		main._chapter_three_fairy_reveal_authorized())
	main.opera_done = false
	main.chapter2_story_complete = true
	main.chapter2_candle_taken = true

	# Reveal creates one target and one cue, and repeated refreshes are idempotent.
	_check("completed Chapter 2 candle story reveals the fairy door",
		main._maybe_reveal_fairy_conservatory())
	door.refresh()
	door.refresh()
	await process_frame
	var hotspot_layer: Node = main.castle_room_door_hotspot_layer
	_check("plot reveal transforms into the available Butterfly Gate",
		door.visual_state() == "revealed"
		and String(door.fairy_conservatory_card.get_meta(
			"source_asset_path", "")).ends_with(
				"butterfly_gate_available.png"))
	_check("reveal creates exactly one hotspot",
		_count_named(hotspot_layer, "MoonflowerConservatoryHotspot") == 1)
	_check("reveal creates exactly one pointer cue",
		_count_named(hotspot_layer, "MoonflowerConservatoryPointer") == 1)
	_check("reveal target meets preschool touch floor",
		door.fairy_conservatory_hotspot != null
		and door.fairy_conservatory_hotspot.size.x >= 112.0
		and door.fairy_conservatory_hotspot.size.y >= 112.0)

	# Opening swaps the same card, retains one permanent hotspot, and removes the
	# one-time pointer. Repeated syncs must not duplicate either node.
	main.chapter3_fairy_door_opened = true
	door.refresh()
	door.refresh()
	await process_frame
	_check("entered route retains the available Butterfly Gate",
		door.visual_state() == "open"
		and String(door.fairy_conservatory_card.get_meta(
			"source_asset_path", "")).ends_with(
				"butterfly_gate_available.png"))
	_check("open route keeps exactly one hotspot",
		_count_named(hotspot_layer, "MoonflowerConservatoryHotspot") == 1)
	_check("open route removes the reveal pointer",
		_count_named(hotspot_layer, "MoonflowerConservatoryPointer") == 0
		and door.fairy_conservatory_cue == null)

	# The route suspends, rather than rebuilds, the wide Hall. A plain resume is
	# required so the exact cross-screen camera offset survives.
	rooms.set("_hall_view_left_art", 836.0)
	rooms.suspend()
	rooms.resume()
	door.refresh()
	_check("Hall suspend/resume preserves camera offset",
		is_equal_approx(float(rooms.get("_hall_view_left_art")), 836.0))
	_check("Hall route remains open after resume",
		door.fairy_conservatory_hotspot != null
		and door.fairy_conservatory_hotspot.visible)

	main.queue_free()
	for _frame: int in range(3):
		await process_frame
	print("FAIRYROUTE|RESULT=%s|failures=%d" % [
		"FAIL" if _failures > 0 else "OK", _failures])
	quit(_failures)
