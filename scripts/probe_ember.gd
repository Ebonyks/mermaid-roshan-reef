extends SceneTree
# Ember Fortress regression: later-world gating (open in dev mode, discovered
# after the Butterfly World in normal play), the rainbow-junction routing that
# dives the float race DOWN into the fortress, the five-lantern objective, the
# six-room fortress dungeon (own ember_progress/ember_done checkpoints, castle
# dungeon untouched) and the safe home-ring return.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260721)
	Engine.time_scale = 8.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	# ---- gating: a later world in normal play, always open in dev mode ----
	var dev_stash: Node = main.dev_mode
	main.dev_mode = null
	main.bwd_done = false
	main.ember_found = false
	main.ember_done = false
	_ck("fresh save keeps the fortress hidden in normal play", not main._ember_open())
	main.bwd_done = true
	_ck("saving the Butterfly World reveals the fortress", main._ember_open())
	main.bwd_done = false
	main.ember_found = true
	_ck("a visited fortress stays discovered", main._ember_open())
	main.ember_found = false
	main.dev_mode = dev_stash
	if dev_stash != null:
		_ck("dev mode keeps the fortress open", main._ember_open())
	# ---- the rainbow junction gate in the Sky Lagoon ----
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main.dev_mode = null   # normal-play build of the lagoon first
	main._enter_level2()
	await process_frame
	_ck("hidden fortress builds no junction gate", main.ember_portal_pos == Vector3.ZERO)
	main.bwd_done = true
	main._enter_level2()
	await process_frame
	_ck("discovered fortress smoulders at the rainbow junction", main.ember_portal_pos != Vector3.ZERO)
	main.dev_mode = dev_stash
	# ---- junction routing: the float race dives DOWN to the fortress ----
	main.game = "kart"
	main.kart_from = "level2"
	main.kart_ground = "float"
	main.kart_completion_committed = false
	main.kart_float_dest = "ember"
	main._end_kart_game(2)
	for i in range(4):
		await process_frame
	_ck("finished ember-bound float race lands in the fortress", main.game == "ember" and main.ember_game != null)
	_ck("junction destination resets after landing", main.kart_float_dest == "galaxy")
	_ck("first landing marks the fortress discovered", main.ember_found)
	var ember: EmberFortressLevel = main.ember_game as EmberFortressLevel
	var env: Environment = main.we_node.environment
	_ck("fortress wears its own dark scene grade", env != null and String(env.get_meta("scene_grade_profile", "")) == "ember")
	_ck("ambient stays capped for the dark look", env != null and env.ambient_light_energy <= 0.551)
	_ck("five ember lanterns await", ember._lanterns.size() == 5 and ember._lit == 0)
	_ck("the Great Gate starts shut", not ember._gate_open)
	# ---- passive safety: nothing lights or opens by itself ----
	for i in range(30):
		await process_frame
	_ck("no lantern lights without Roshan", ember._lit == 0 and not ember._gate_open and main.dungeon_game == null)
	# ---- the five-lantern objective (deterministic single entry point) ----
	for i in range(5):
		ember._light_lantern(i)
	_ck("all five lanterns burn", ember._lit == 5)
	_ck("lantern checkpoints persist as hidden sticker keys", bool(main.stickers.get("_ember_lantern_0", false)) and bool(main.stickers.get("_ember_lantern_4", false)))
	_ck("five lanterns open the Great Gate", ember._gate_open)
	# ---- the six-room fortress dungeon ----
	_ck("fortress dungeon defines six rooms", EmberFortressLevel.ROOMS.size() == 6)
	var combat_count := 0
	var puzzle_count := 0
	for room: Dictionary in EmberFortressLevel.ROOMS:
		if String(room.get("type", "combat")) == "combat":
			combat_count += 1
		else:
			puzzle_count += 1
	_ck("fortress mixes three battles with three puzzles", combat_count == 3 and puzzle_count == 3)
	main._start_ember_dungeon()
	var dungeon: DungeonLevel = main.dungeon_game
	_ck("open gate admits the dungeon", dungeon != null and main.game == "emberdun")
	_ck("fortress level pauses underneath", not ember.visible and ember.process_mode == Node.PROCESS_MODE_DISABLED)
	await _wait_for_room(dungeon, 0)
	_ck("sequencer runs the fortress room table", dungeon.rooms.size() == 6 and String((dungeon.rooms[0] as Dictionary)["name"]) == "Cinder Gate Imps")
	for i in range(30):
		await process_frame
	_ck("fortress combat cannot win passively", dungeon.room_index == 0 and dungeon.arena != null)
	_clear_combat(dungeon)
	await _wait_for_room(dungeon, 1)
	_exercise_puzzle(dungeon.puzzle, EmberFortressLevel.ROOMS[1])
	await _wait_for_room(dungeon, 2)
	_ck("fortress checkpoints land in ember_progress", main.ember_progress == 2)
	_ck("castle dungeon progress stays untouched", main.dungeon_progress == 0 and not main.dungeon_done)
	# leave early: a neutral exit back to the fortress planet, checkpoint kept
	dungeon._leave_early()
	await process_frame
	_ck("home icon returns to the fortress planet", main.game == "ember" and main.dungeon_game == null and ember.visible)
	main._start_ember_dungeon()
	dungeon = main.dungeon_game
	await _wait_for_room(dungeon, 2)
	_ck("next visit resumes at fortress room three", dungeon != null and dungeon.room_index == 2)
	for expected in range(2, EmberFortressLevel.ROOMS.size()):
		await _wait_for_room(dungeon, expected)
		var config: Dictionary = EmberFortressLevel.ROOMS[expected]
		var expected_type := String(config.get("type", "combat"))
		_ck("fortress room %d uses %s engine" % [expected + 1, expected_type], dungeon.arena != null if expected_type == "combat" else dungeon.puzzle != null)
		if dungeon.puzzle != null:
			_exercise_puzzle(dungeon.puzzle, config)
		elif expected == EmberFortressLevel.ROOMS.size() - 1:
			_exercise_finale(dungeon.arena)
		else:
			_clear_combat(dungeon)
		if expected < EmberFortressLevel.ROOMS.size() - 1:
			await _wait_for_room(dungeon, expected + 1)
	await process_frame
	_ck("all six fortress checkpoints persist", main.ember_progress == 6)
	_ck("final room completes the fortress", main.ember_done)
	dungeon._finish(true)
	await process_frame
	_ck("completion returns outside the Great Gate", main.game == "ember" and main.dungeon_game == null and ember.visible)
	_ck("the Fortress Hero sticker is awarded", bool(main.stickers.get("volcano", false)))
	_ck("the save carries the fortress keys", bool(main.save_data.get("ember_done", false)) and int(main.save_data.get("ember_progress", 0)) == 6)
	_ck("castle dungeon still untouched after the finale", main.dungeon_progress == 0 and not main.dungeon_done)
	# ---- the rainbow home ring: a neutral exit, never a loss ----
	ember._teardown(false)
	for i in range(4):
		await process_frame
	_ck("home ring returns to the lagoon", main.game == "level2" and main.ember_game == null)
	print("EMBER|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _exercise_puzzle(puzzle: DungeonPuzzleRoom, config: Dictionary) -> void:
	var solution: Array = config.get("solution", [])
	for choice in solution:
		_activate(puzzle, int(choice))
	_ck("puzzle solution physically opens door", puzzle.state == "exit" and puzzle.door != null)
	puzzle._finish()

func _activate(puzzle: DungeonPuzzleRoom, choice: int) -> void:
	for entry: Dictionary in puzzle.interactives:
		if int(entry["index"]) == choice:
			puzzle.player_pos = entry["pos"] as Vector3
			puzzle._puzzle_action(choice)
			return
	_ck("choice %d has a physical prop" % choice, false)

func _exercise_finale(arena: CombatArena) -> void:
	_ck("the Molten Throne opens with the ice shell phase", arena.kind == "dual" and arena.action_label() == "ICE")
	var hp: int = int(arena.boss["hp"])
	for cycle in range(hp):
		arena._hit_boss("ice")
		arena._hit_boss("fire")
	_ck("dual-element throne resolves", arena.state == "won")
	arena.win_t = 0.0

func _clear_combat(dungeon: DungeonLevel) -> void:
	if dungeon.arena == null:
		return
	dungeon.arena._win()
	dungeon.arena.win_t = 0.0

func _wait_for_room(dungeon: DungeonLevel, expected: int) -> void:
	var guard := 0
	while dungeon != null and is_instance_valid(dungeon) and (dungeon.room_index != expected or (dungeon.arena == null and dungeon.puzzle == null)) and guard < 180:
		guard += 1
		await process_frame

func _ck(label: String, ok: bool) -> void:
	print("EMBER|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1
