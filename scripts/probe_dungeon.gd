extends SceneTree
# Ten-room adventure regression: mixed combat/puzzles, passive safety,
# checkpoint resume, every room type and final persistent completion.

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
	await _wait_for_room(dungeon, 0)
	_ck("dungeon defines ten rooms", DungeonLevel.ROOMS.size() == 10)
	var combat_count := 0
	var puzzle_count := 0
	for room in DungeonLevel.ROOMS:
		if String(room.get("type", "combat")) == "combat":
			combat_count += 1
		else:
			puzzle_count += 1
	_ck("dungeon mixes four battles with six puzzles", combat_count == 4 and puzzle_count == 6)
	_ck("first room uses shared combat engine", dungeon.arena is CombatArena and dungeon.puzzle == null)
	for i in range(30):
		await process_frame
	_ck("combat room cannot win passively", dungeon.room_index == 0 and dungeon.arena != null)
	var pearls_before_exit: int = main.pearl_count
	dungeon._leave_early()
	await process_frame
	_ck("active combat exit is neutral", main.game == "level2" and main.dungeon_progress == 0 and main.pearl_count == pearls_before_exit)
	main._start_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_room(dungeon, 0)
	dungeon.arena._win()
	dungeon._leave_early()
	await process_frame
	_ck("earned combat celebration checkpoints", main.game == "level2" and main.dungeon_progress == 1 and main.pearl_count == pearls_before_exit + 3)
	main._start_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_room(dungeon, 1)
	_ck("second room uses puzzle engine", dungeon.puzzle is DungeonPuzzleRoom and dungeon.arena == null)
	for i in range(30):
		await process_frame
	_ck("puzzle room cannot win passively", dungeon.room_index == 1 and dungeon.puzzle != null and dungeon.puzzle.state == "play")
	dungeon._leave_early()
	await process_frame
	_ck("active puzzle exit is neutral", main.game == "level2" and main.dungeon_progress == 1 and main.pearl_count == pearls_before_exit + 3)
	main._start_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_room(dungeon, 1)
	dungeon.puzzle.force_solve()
	dungeon._leave_early()
	await process_frame
	_ck("earned puzzle celebration checkpoints", main.game == "level2" and main.dungeon_progress == 2 and main.pearl_count == pearls_before_exit + 6)
	main._start_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_room(dungeon, 2)
	_ck("next visit resumes at room three", dungeon.room_index == 2 and dungeon.puzzle != null)
	for expected in range(2, DungeonLevel.ROOMS.size()):
		await _wait_for_room(dungeon, expected)
		var config: Dictionary = DungeonLevel.ROOMS[expected]
		var expected_type := String(config.get("type", "combat"))
		var correct_engine := dungeon.arena != null if expected_type == "combat" else dungeon.puzzle != null
		_ck("room %d uses %s engine" % [expected + 1, expected_type], correct_engine)
		if expected == DungeonLevel.ROOMS.size() - 1:
			var final_pearls: int = main.pearl_count
			dungeon.arena._win()
			dungeon._leave_early()
			await process_frame
			_ck("final celebration exit keeps all rewards", main.game == "level2" and main.dungeon_progress == 10 and main.dungeon_done and main.pearl_count == final_pearls + 53)
		elif expected_type == "puzzle":
			await _solve_puzzle_room(dungeon, expected)
			await _wait_for_room(dungeon, expected + 1)
		else:
			_clear_room(dungeon)
			await _wait_for_room(dungeon, expected + 1)
	await process_frame
	_ck("all ten checkpoints persist", main.dungeon_progress == 10)
	_ck("final room completes dungeon", main.dungeon_done)
	_ck("completion returns to castle", main.game == "level2" and main.dungeon_game == null)
	var replay_pearls: int = main.pearl_count
	var replay := DungeonLevel.new()
	get_root().add_child(replay)
	replay.start(main, 10, Callable())
	replay._complete_dungeon()
	_ck("completed replay never repeats the fifty-pearl prize", main.pearl_count == replay_pearls)
	replay._finish(true)
	print("DUNGEON|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _clear_room(dungeon: DungeonLevel) -> void:
	if dungeon.arena != null:
		dungeon.arena._win()
		dungeon.arena.win_t = 0.0
	elif dungeon.puzzle != null:
		dungeon.puzzle._finish()

func _solve_puzzle_room(dungeon: DungeonLevel, room_number: int) -> void:
	var puzzle: DungeonPuzzleRoom = dungeon.puzzle
	var controls_clear := true
	for button: Button in puzzle.buttons:
		if button.position.y + button.size.y > 610.0:
			controls_clear = false
	_ck("room %d touch controls clear the progress strip" % (room_number + 1), controls_clear)
	if puzzle.puzzle_kind == "rotate":
		var targets: Array = puzzle.config.get("targets", [1, 0, 3])
		for i in range(targets.size()):
			for _turn in range(int(targets[i])):
				puzzle._puzzle_action(i)
		_ck("rotate puzzle follows the pictured pearl", puzzle.state == "celebrate")
	elif puzzle.puzzle_kind == "pairs":
		_ck("pair controls match the 2x2 cards", puzzle.buttons[0].position.y == puzzle.buttons[1].position.y and puzzle.buttons[2].position.y == puzzle.buttons[3].position.y and puzzle.buttons[2].position.y > puzzle.buttons[0].position.y)
		puzzle._puzzle_action(0)
		puzzle._puzzle_action(1)
		_ck("pair mismatch is gentle and visible", puzzle.state == "play" and puzzle.pair_locked and puzzle.buttons[0].text != "?" and puzzle.buttons[1].text != "?")
		var guard := 0
		while puzzle.pair_locked and guard < 60:
			guard += 1
			await process_frame
		_ck("pair mismatch resets after a viewing pause", not puzzle.pair_locked and puzzle.buttons[0].text == "?" and puzzle.buttons[1].text == "?")
		puzzle._puzzle_action(0)
		puzzle._puzzle_action(2)
		puzzle._puzzle_action(1)
		puzzle._puzzle_action(3)
		_ck("pair puzzle solves through real taps", puzzle.state == "celebrate")
	else:
		var solution: Array = puzzle.config.get("solution", [])
		if not solution.is_empty():
			var wrong: int = (int(solution[0]) + 1) % puzzle.buttons.size()
			puzzle._puzzle_action(wrong)
			_ck("room %d wrong tap has no penalty" % (room_number + 1), puzzle.state == "play" and puzzle.step == 0 and main.dungeon_progress == room_number)
		for choice in solution:
			puzzle._puzzle_action(int(choice))
		_ck("room %d puzzle solves through real taps" % (room_number + 1), puzzle.state == "celebrate")
	await process_frame
	puzzle._finish()

func _wait_for_room(dungeon: DungeonLevel, expected: int) -> void:
	var guard := 0
	while dungeon != null and (dungeon.room_index != expected or (dungeon.arena == null and dungeon.puzzle == null)) and guard < 120:
		guard += 1
		await process_frame

func _ck(label: String, ok: bool) -> void:
	print("DUNGEON|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1
