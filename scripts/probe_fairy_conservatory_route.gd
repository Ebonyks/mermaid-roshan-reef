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
	main.chapter3_fairy_door_revealed = false
	main.chapter3_fairy_door_opened = false
	main.chapter3_fairy_mission_started = false
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
	_check("Main Hall route opens", rooms.is_open())
	_check("fresh door is dormant",
		rooms._fairy_conservatory_visual_state() == "closed")
	_check("dormant relief has no hotspot",
		rooms.fairy_conservatory_hotspot == null)
	_check("dormant relief has no cue", rooms.fairy_conservatory_cue == null)
	_check("dormant relief uses closed card",
		rooms.fairy_conservatory_card != null
		and String(rooms.fairy_conservatory_card.get_meta(
			"source_asset_path", "")).ends_with("moonflower_door_closed.png"))

	# Reveal creates one target and one cue, and repeated refreshes are idempotent.
	main.chapter3_fairy_door_revealed = true
	rooms.refresh_fairy_conservatory_state()
	rooms.refresh_fairy_conservatory_state()
	await process_frame
	var hotspot_layer: Node = main.castle_room_door_hotspot_layer
	_check("revealed door retains closed relief",
		rooms._fairy_conservatory_visual_state() == "revealed"
		and String(rooms.fairy_conservatory_card.get_meta(
			"source_asset_path", "")).ends_with("moonflower_door_closed.png"))
	_check("reveal creates exactly one hotspot",
		_count_named(hotspot_layer, "MoonflowerConservatoryHotspot") == 1)
	_check("reveal creates exactly one pointer cue",
		_count_named(hotspot_layer, "MoonflowerConservatoryPointer") == 1)
	_check("reveal target meets preschool touch floor",
		rooms.fairy_conservatory_hotspot != null
		and rooms.fairy_conservatory_hotspot.size.x >= 112.0
		and rooms.fairy_conservatory_hotspot.size.y >= 112.0)

	# Opening swaps the same card, retains one permanent hotspot, and removes the
	# one-time pointer. Repeated syncs must not duplicate either node.
	main.chapter3_fairy_door_opened = true
	rooms.refresh_fairy_conservatory_state()
	rooms.refresh_fairy_conservatory_state()
	await process_frame
	_check("opened route uses open card",
		rooms._fairy_conservatory_visual_state() == "open"
		and String(rooms.fairy_conservatory_card.get_meta(
			"source_asset_path", "")).ends_with("moonflower_door_open.png"))
	_check("open route keeps exactly one hotspot",
		_count_named(hotspot_layer, "MoonflowerConservatoryHotspot") == 1)
	_check("open route removes the reveal pointer",
		_count_named(hotspot_layer, "MoonflowerConservatoryPointer") == 0
		and rooms.fairy_conservatory_cue == null)

	# The route suspends, rather than rebuilds, the wide Hall. A plain resume is
	# required so the exact cross-screen camera offset survives.
	rooms.set("_hall_view_left_art", 836.0)
	rooms.suspend()
	rooms.resume()
	_check("Hall suspend/resume preserves camera offset",
		is_equal_approx(float(rooms.get("_hall_view_left_art")), 836.0))
	_check("Hall route remains open after resume",
		rooms.fairy_conservatory_hotspot != null
		and rooms.fairy_conservatory_hotspot.visible)

	main.queue_free()
	for _frame: int in range(3):
		await process_frame
	print("FAIRYROUTE|RESULT=%s|failures=%d" % [
		"FAIL" if _failures > 0 else "OK", _failures])
	quit(_failures)
