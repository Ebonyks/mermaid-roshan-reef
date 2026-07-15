extends SceneTree
# Ten-room dungeon regression: engine reuse, passive safety, checkpoint resume,
# every configured room and final persistent completion.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260715)
	Engine.time_scale = 8.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.combat_ice_done = true
	main.combat_fire_done = true
	main.dungeon_progress = 0
	main.dungeon_done = false
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_dungeon()
	var dungeon: DungeonLevel = main.dungeon_game
	await _wait_for_arena(dungeon)
	_ck("dungeon defines ten rooms", DungeonLevel.ROOMS.size() == 10)
	_ck("first room uses shared combat engine", dungeon.arena is CombatArena and dungeon.room_index == 0)
	for i in range(30):
		await process_frame
	_ck("first room cannot win passively", dungeon.arena != null and dungeon.arena.state == "play")
	_clear_room(dungeon)
	await _wait_for_room(dungeon, 1)
	_ck("room clear saves checkpoint", main.dungeon_progress == 1)
	dungeon._leave_early()
	await process_frame
	_ck("home icon returns safely", main.game == "level2" and main.dungeon_game == null)
	main._start_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_arena(dungeon)
	_ck("next visit resumes at room two", dungeon.room_index == 1)
	for expected in range(1, DungeonLevel.ROOMS.size()):
		await _wait_for_room(dungeon, expected)
		var config: Dictionary = DungeonLevel.ROOMS[expected]
		_ck("room %d kind configured" % (expected + 1), dungeon.arena != null and dungeon.arena.kind == String(config["kind"]))
		_clear_room(dungeon)
		if expected < DungeonLevel.ROOMS.size() - 1:
			await _wait_for_room(dungeon, expected + 1)
	await process_frame
	_ck("all ten checkpoints persist", main.dungeon_progress == 10)
	_ck("final room completes dungeon", main.dungeon_done)
	dungeon._finish(true)
	await process_frame
	_ck("completion returns to castle", main.game == "level2" and main.dungeon_game == null)
	print("DUNGEON|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _clear_room(dungeon: DungeonLevel) -> void:
	if dungeon.arena == null:
		return
	dungeon.arena._win()
	dungeon.arena.win_t = 0.0

func _wait_for_arena(dungeon: DungeonLevel) -> void:
	var guard := 0
	while dungeon != null and dungeon.arena == null and guard < 60:
		guard += 1
		await process_frame

func _wait_for_room(dungeon: DungeonLevel, expected: int) -> void:
	var guard := 0
	while dungeon != null and (dungeon.room_index != expected or dungeon.arena == null) and guard < 120:
		guard += 1
		await process_frame

func _ck(label: String, ok: bool) -> void:
	print("DUNGEON|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1
