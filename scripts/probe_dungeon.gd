extends SceneTree
# Ten-room adventure regression: physical puzzle interaction, mixed combat,
# touch-safe HUD, gentle feedback, checkpoint resume and dual-element finale.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260716)
	Engine.time_scale = 8.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	# A brand-new save must be able to enter. These abilities are introduced by
	# the dungeon rooms and must never be prerequisites for the entrance.
	main.combat_ice_done = false
	main.combat_fire_done = false
	main.dungeon_progress = 0
	main.dungeon_done = false
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_dungeon()
	var dungeon: DungeonLevel = main.dungeon_game
	_ck("fresh save can enter before finding elemental encounters", dungeon != null)
	await _wait_for_room(dungeon, 0)
	_ck("dungeon defines ten rooms", DungeonLevel.ROOMS.size() == 10)
	var combat_count := 0
	var puzzle_count := 0
	for room: Dictionary in DungeonLevel.ROOMS:
		if String(room.get("type", "combat")) == "combat": combat_count += 1
		else: puzzle_count += 1
	_ck("dungeon mixes four battles with six puzzles", combat_count == 4 and puzzle_count == 6)
	_ck("progress HUD never blocks touch", dungeon.progress_label.mouse_filter == Control.MOUSE_FILTER_IGNORE and dungeon.room_label.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	_ck("first room uses bounded combat scene", dungeon.arena is CombatArena and _descendants(dungeon.arena) < 100)
	for i in range(30): await process_frame
	_ck("combat room cannot win passively", dungeon.room_index == 0 and dungeon.arena != null)
	_clear_combat(dungeon)
	await _wait_for_room(dungeon, 1)
	_ck("puzzle gives Roshan spatial controls", dungeon.puzzle.avatar != null and dungeon.puzzle.interactives.size() == 3)
	_ck("puzzle room stays inside mobile node budget", _descendants(dungeon.puzzle) < 90)
	for i in range(30): await process_frame
	_ck("puzzle cannot win passively", dungeon.puzzle.state == "play")
	_exercise_puzzle(dungeon.puzzle, DungeonLevel.ROOMS[1])
	await _wait_for_room(dungeon, 2)
	_ck("real puzzle clear saves checkpoint", main.dungeon_progress == 2)
	dungeon._leave_early()
	await process_frame
	_ck("home icon returns safely", main.game == "level2" and main.dungeon_game == null)
	main._start_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_room(dungeon, 2)
	_ck("next visit resumes at room three", dungeon.room_index == 2 and dungeon.puzzle != null)
	for expected in range(2, DungeonLevel.ROOMS.size()):
		await _wait_for_room(dungeon, expected)
		var config: Dictionary = DungeonLevel.ROOMS[expected]
		var expected_type := String(config.get("type", "combat"))
		_ck("room %d uses %s engine" % [expected + 1, expected_type], dungeon.arena != null if expected_type == "combat" else dungeon.puzzle != null)
		if dungeon.puzzle != null:
			_exercise_puzzle(dungeon.puzzle, config)
		else:
			if expected == 9:
				_exercise_finale(dungeon.arena)
			else:
				_clear_combat(dungeon)
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

func _exercise_puzzle(puzzle: DungeonPuzzleRoom, config: Dictionary) -> void:
	var kind := String(config["puzzle"])
	if kind == "pairs":
		_activate(puzzle, 0)
		_activate(puzzle, 1)
		_ck("mismatched runes remain visible", puzzle.pair_hide_t > 0.0 and puzzle.card_labels[0].text != "?" and puzzle.card_labels[1].text != "?")
		puzzle._process(1.2)
		_activate(puzzle, 0)
		_activate(puzzle, 2)
		_activate(puzzle, 1)
		_activate(puzzle, 3)
	elif kind == "rotate":
		var targets: Array = config["targets"]
		_ck("shell targets face the central pearl", targets == [1, 0, 3])
		for i in range(targets.size()):
			for turn in range(int(targets[i])):
				_activate(puzzle, i)
	else:
		var solution: Array = config["solution"]
		for choice in solution:
			_activate(puzzle, int(choice))
	_ck("puzzle solution physically opens door", puzzle.state == "exit" and puzzle.door != null)
	puzzle._finish()

func _activate(puzzle: DungeonPuzzleRoom, choice: int) -> void:
	for entry: Dictionary in puzzle.interactives:
		if int(entry["index"]) == choice:
			puzzle.player_pos = entry["pos"] as Vector3
			_ck("choice %d reachable by proximity" % choice, puzzle._nearest_interactive() >= 0)
			puzzle._puzzle_action(choice)
			return
	_ck("choice %d has a physical prop" % choice, false)

func _exercise_finale(arena: CombatArena) -> void:
	_ck("final boss starts with ice shell phase", arena.kind == "dual" and arena.action_label() == "ICE")
	var hp: int = int(arena.boss["hp"])
	arena._hit_boss("fire")
	_ck("fire cannot skip frozen-shell lesson", int(arena.boss["hp"]) == hp and String(arena.boss["phase"]) == "shell")
	for cycle in range(hp):
		arena._hit_boss("ice")
		_ck("cycle %d changes action to fire" % (cycle + 1), arena.action_label() == "FIRE")
		arena._hit_boss("fire")
		if cycle < hp - 1:
			_ck("cycle %d returns to ice shell" % (cycle + 1), arena.action_label() == "ICE")
	_ck("dual-element finale resolves", arena.state == "won")
	_ck("combat materials are reused", arena._mat(Color.WHITE) == arena._mat(Color.WHITE))
	arena.win_t = 0.0

func _clear_combat(dungeon: DungeonLevel) -> void:
	if dungeon.arena == null: return
	dungeon.arena._win()
	dungeon.arena.win_t = 0.0

func _wait_for_room(dungeon: DungeonLevel, expected: int) -> void:
	var guard := 0
	while dungeon != null and (dungeon.room_index != expected or (dungeon.arena == null and dungeon.puzzle == null)) and guard < 180:
		guard += 1
		await process_frame

func _descendants(node: Node) -> int:
	var total := 0
	for child in node.get_children():
		total += 1 + _descendants(child)
	return total

func _ck(label: String, ok: bool) -> void:
	print("DUNGEON|", label, ": ", "OK" if ok else "FAIL")
	if not ok: bad += 1
