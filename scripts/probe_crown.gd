extends SceneTree
# Crown Star probe: touching the crown must CELEBRATE IN PLACE — win recorded,
# Roshan stays in her castle — instead of the old _finish_level2() ocean eject.
# The front-door exit must still return her to the courtyard when SHE chooses.
# Prints OK/FAIL lines (ci.sh convention).

var main: Node
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CROWN|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main.level2_done_once = false
	main._enter_level2()
	await _frames(10)
	main._enter_castle_interior()
	await _frames(20)
	var o: Vector3 = main.CASTLE_POS
	var player: Node3D = main.player
	# swim into the crown star above the throne
	player.position = o + Vector3(0, 24.0, -22.0)
	for i in range(60):
		player.vel = Vector3(0, 0, -10)
		await process_frame
		if bool(main.g.get("crown_won", false)):
			break
	_ck("crown_won_flag", bool(main.g.get("crown_won", false)))
	_ck("win_recorded", main.level2_done_once)
	_ck("still_in_castle", main.game == "level2" and String(main.g.get("phase", "")) == "hall", "game=%s phase=%s" % [main.game, str(main.g.get("phase", ""))])
	var near: bool = (player.position - o).length() < 90.0
	_ck("not_ejected_to_ocean", near, "dist=%.0f" % (player.position - o).length())
	# linger near the throne — no re-trigger, no teleport
	await _frames(60)
	_ck("no_retrigger_teleport", main.game == "level2" and (player.position - o).length() < 90.0)
	# the front door still leaves the castle to the courtyard
	if main.g.has("hall_exit"):
		var hx: Vector3 = main.g["hall_exit"]
		# Exercise the production hall tick at both sides of the threshold. The
		# physics controller can push a teleported player back inside a wall before
		# a headless render frame, which made this transition probe cadence-bound.
		main.g["t"] = 3.0   # beyond the intentional 2.5-second entrance grace
		player.position = hx + Vector3(20.0, 0.0, 0.0)
		player.vel = Vector3.ZERO
		main._tick_castle_hall(1.0 / 60.0, player.position)
		_ck("front_door_arms", bool(main.g.get("hall_exit_armed", false)))
		player.position = hx
		main._tick_castle_hall(1.0 / 60.0, player.position)
		await process_frame
		_ck("front_door_exits", String(main.g.get("phase", "")) != "hall", "phase=%s" % str(main.g.get("phase", "")))
	else:
		_ck("front_door_exits", false, "no hall_exit key")
	print("CROWN|done: ", ("OK" if checks_failed == 0 else "FAIL (%d)" % checks_failed))
	quit()
