extends SceneTree
# HitEngine probe: taps on enemies route through the shared hit pipeline into
# the dying animation, picking is honest (far taps miss), nothing dies without
# input, boss phase rules survive the engine, and the generic hp path works
# for future clients.

var main: ReefMain
var bad := 0
var defeated := 0

func _init() -> void:
	seed(20260728)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _tap_ice_case()
	await _tap_boss_case()
	await _generic_engine_case()
	print("HIT|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	# tear the scene down before quitting: the Windows 4.7-dev2 binary can
	# crash inside exit-time Dictionary teardown when the full game tree is
	# reaped by quit() itself
	get_root().remove_child(main)
	main.free()
	await process_frame
	quit()

func _ck(label: String, ok: bool) -> void:
	print("HIT|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _screen_pos_of(arena: CombatArena, enemy: Dictionary) -> Vector2:
	return arena.cam.unproject_position(arena.he.aim_point(enemy))

func _tap_ice_case() -> void:
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("arena builds its hit engine", arena != null and arena.he != null)
	_ck("router finds the live arena", main._combat_arena_ref() == arena)
	_ck("engine borrows the imp dicts", arena.he.targets.size() == 8)
	# agency: idle frames defeat nobody
	for i in range(20):
		await process_frame
	var active := 0
	for enemy: Dictionary in arena.enemies:
		if String(enemy["state"]) == "active":
			active += 1
	_ck("no imp dies without input", active == 8)
	# a tap in the far corner picks nothing
	_ck("far tap misses every imp", arena.he.tap_pick(Vector2(4.0, 4.0)).is_empty())
	_ck("missed tap deals no hit", not arena.he.tap(Vector2(4.0, 4.0)))
	# a tap on an imp picks that imp and freezes it into the dying sequence
	var target: Dictionary = arena.enemies[0]
	var tap_pos: Vector2 = _screen_pos_of(arena, target)
	_ck("tap picks the imp under the finger", is_same(arena.he.tap_pick(tap_pos), target))
	main._on_touch_world(tap_pos)
	_ck("routed tap freezes the imp", String(target["state"]) == "frozen")
	target["timer"] = 0.0
	await process_frame
	await process_frame
	_ck("frozen imp pops into the dying animation", String(target["state"]) == "popped")
	_ck("popped imp leaves the stage", not (target["node"] as Node3D).visible)
	_ck("popped imp is no longer hittable", not arena.he.hit(target, 1, "tap"))
	# pop the rest by tapping each one; the arena win flow is untouched
	for enemy: Dictionary in arena.enemies:
		if String(enemy["state"]) == "active":
			main._on_touch_world(_screen_pos_of(arena, enemy))
			enemy["timer"] = 0.0
	await process_frame
	await process_frame
	_ck("tapping every imp wins the arena", arena.state == "won")
	arena.win_t = 0.0
	await process_frame
	await process_frame
	_ck("tap-won battle saves and returns", main.combat_ice_done and main.combat_game == null)

func _tap_boss_case() -> void:
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_combat("fire")
	await process_frame
	var arena: CombatArena = main.combat_game
	var boss: Dictionary = arena.boss
	_ck("boss registers with the engine", arena.he.targets.size() == 1 and is_same(arena.he.targets[0], boss))
	var hp_before: int = int(boss["hp"])
	boss["phase"] = "shell"
	main._on_touch_world(_screen_pos_of(arena, boss))
	_ck("shell phase still blocks a tap", int(boss["hp"]) == hp_before)
	boss["phase"] = "peek"
	main._on_touch_world(_screen_pos_of(arena, boss))
	_ck("peeking boss takes tap damage", int(boss["hp"]) == hp_before - 1)
	arena.cancel(true)
	await process_frame

func _generic_engine_case() -> void:
	# the open interface future encounters use: default hp pipeline + a
	# named dying animation, no arena involved. Park main in the neutral
	# blank state so no world tick runs against an unbuilt level.
	main.game = ""
	var eng := HitEngine.new(main)
	eng.on_defeated = func(_enemy: Dictionary) -> void: defeated += 1
	var dummy := Node3D.new()
	main.add_child(dummy)
	var rec: Dictionary = {"node": dummy, "state": "active", "hp": 2, "death": "flop"}
	eng.targets = [rec]
	_ck("generic hit lands from any source", eng.hit(rec, 1, "future_verb"))
	_ck("survivor keeps reduced hp", int(rec["hp"]) == 1 and String(rec["state"]) == "active")
	_ck("lethal hit starts the dying animation", eng.hit(rec, 1, "future_verb") and String(rec["state"]) == "popped")
	_ck("defeat callback fired once", defeated == 1)
	for i in range(60):
		await process_frame
	_ck("flop death disposes the node", not is_instance_valid(dummy))
	_ck("dead record refuses further hits", not eng.hit(rec, 1, "tap"))
