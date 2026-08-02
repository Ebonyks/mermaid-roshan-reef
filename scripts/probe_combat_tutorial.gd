extends SceneTree
# The throne sparring class: touching the Royal throne opens the tutorial,
# each lesson waits for the CHILD's own input (nothing auto-advances), the
# lessons progress tap → combo → charge → wave, a full charge fires itself,
# the diploma persists, and the castle hall comes back afterwards.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260801)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _class_case()
	print("TUTORIAL|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	get_root().remove_child(main)
	main.free()
	await process_frame
	quit()

func _ck(label: String, ok: bool) -> void:
	print("TUTORIAL|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _tap(tut: CombatTutorial, enemy: Dictionary) -> void:
	var pos: Vector2 = tut.cam.unproject_position(tut.he.aim_point(enemy))
	main._on_world_press(pos)
	main._on_world_press_release()

func _class_case() -> void:
	main.companion_id = ""
	main.game = "level2"
	main.g["t"] = 0.0
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.open("main_hall")
	await _frames(2)
	rooms._start_combat_tutorial()
	await _frames(2)
	var tut: CombatTutorial = main.combat_tutorial_game
	_ck("the throne opens the sparring class",
		tut != null and main.hit_engines.has(tut.he))
	_ck("class begins at the TAP lesson", tut.lesson == "tap")
	await _frames(30)
	var first: Dictionary = tut.enemies[0]
	_ck("nothing advances without her input",
		tut.lesson == "tap" and int(first["hp"]) == 3)
	_tap(tut, first)
	await _frames(1)
	_ck("her first bop advances to COMBO",
		tut.lesson == "combo" and int(first["hp"]) == 2)
	_tap(tut, first)
	_tap(tut, first)
	await _frames(2)
	_ck("the 1-2-3 combo pops the imp into the CHARGE lesson",
		tut.lesson == "charge")
	await _frames(25)   # let the combo window lapse so the hold is a clean read
	var second: Dictionary = tut._lesson_target()
	_ck("a fresh sparring imp waits", not second.is_empty() and int(second["hp"]) == 3)
	var pos: Vector2 = tut.cam.unproject_position(tut.he.aim_point(second))
	main._on_world_press(pos)   # press-fire tap, then HOLD — no release
	await _frames(16)           # past 1.45 s: stage 3 fires itself
	_ck("a full charge fells the imp and graduates",
		tut.lesson == "wave" and String(second["state"]) != "active")
	_ck("the graduation wave arrives", tut.enemies.size() >= 4)
	for _round in range(8):
		var target: Dictionary = tut._lesson_target()
		if target.is_empty():
			break
		_tap(tut, target)
		await _frames(1)
	await _frames(2)
	_ck("clearing the wave ends the class", tut.state == "won")
	tut.win_t = 0.0
	await _frames(3)
	_ck("the diploma persists",
		main.combat_tutorial_done and main.combat_tutorial_game == null)
	_ck("the castle hall comes back",
		rooms.is_open() and main.castle_room_layer.visible)
	rooms.close()
	await process_frame
