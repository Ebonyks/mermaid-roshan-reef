extends SceneTree
## Focused input/lifecycle regression; drawn and played acceptance is separate.
var bad: int = 0
var earned: int = 0
var catch: OperaNurseryCatch
var rows: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func check(name: String, condition: bool) -> void:
	rows.append({"check": name, "pass": condition})
	if not condition:
		bad += 1
	print("NURSERY_GEOMETRY|", "OK" if condition else "FAIL", "|", name)

func press(index: int, x: float) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index
	event.pressed = true
	event.position = Vector2(catch.size.x * x, catch.size.y * 0.7)
	catch._gui_input(event)

func _run() -> void:
	catch = OperaNurseryCatch.new()
	root.add_child(catch)
	catch.size = Vector2(472, 358)
	catch.baby_caught.connect(func(_quality: float) -> void: earned += 1)
	await process_frame
	check("three intact baby textures have nonempty measured support anchors",
		catch.textures.size() == 3 and catch.baby_feet.size() == 3
		and catch.baby_feet.all(func(foot: Vector2) -> bool:
			return foot.x > 0.0 and foot.x < 1.0 and foot.y > 0.5 and foot.y <= 1.0))
	catch.start(1)
	catch.set_process(false)
	for _i: int in range(60):
		catch._process(0.1)
	check("passive mercy remains safe without earning a catch", earned == 0
		and catch.caught == 0 and catch.missed > 0 and catch.active)
	catch.start(1)
	catch.set_process(false)
	press(0, 0.3)
	press(1, 0.8)
	check("a second finger cannot steal the first hand position",
		catch.touch_index == 0 and is_equal_approx(catch.catcher_x, 0.3))
	catch._notification(Control.NOTIFICATION_WM_WINDOW_FOCUS_OUT)
	check("focus loss clears ownership and remembered catch intent",
		catch.touch_index == -1 and catch.input_live_t == 0.0)
	catch.start(1)
	catch.set_process(false)
	catch.spawn_t = 99.0
	catch.fallers.append({"base_x": 0.5, "x": 0.5, "y": OperaNurseryCatch.CATCH_Y - 0.005,
		"speed": 0.2, "phase": 0.0, "sway": 0.0, "texture": 1})
	press(0, 0.5)
	catch._process(0.05)
	check("one fresh supported catch earns once and begins its retained transfer",
		earned == 1 and catch.caught == 1 and not catch.active
		and catch.transfers.size() == 1 and catch.settled == [1])
	catch._process(0.1)
	check("final catch still has a visible hold after scoring stops", catch.transfers.size() == 1)
	catch._process(1.0)
	check("final transfer settles without awarding another catch",
		catch.transfers.is_empty() and catch.settled == [1] and earned == 1
		and not catch.is_processing())
	var points: Array[Vector2] = []
	for index: int in range(5):
		points.append(catch.resting_point(index))
	catch.steer_to(0.9)
	check("five distinct resting slots remain fixed when the catcher moves",
		points[0] != points[1] and points[1] != points[2] and points[2] != points[3]
		and points[3] != points[4] and points[2] == catch.resting_point(2))
	catch.start(1)
	catch.set_process(false)
	catch.spawn_t = 99.0
	catch.fallers.append({"base_x": 0.5, "x": 0.5, "y": OperaNurseryCatch.PILLOW_Y,
		"speed": 0.2, "phase": 0.0, "sway": 0.0, "texture": 2})
	press(0, 0.5)
	catch._process(0.05)
	check("a baby already at the floor cannot be scored as a hand catch",
		catch.caught == 0 and catch.missed == 1 and earned == 1)
	catch.transfers.append({"slot": 0, "time": 0.0, "texture": 0, "from_x": 0.5})
	catch.stop()
	check("teardown clears pending transfer and input ownership",
		catch.transfers.is_empty() and catch.touch_index == -1 and catch.input_live_t == 0.0)
	var file := FileAccess.open("res://audit/day2_nursery_contact_20261001/geometry_probe.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks": rows, "failures": bad,
		"godot": Engine.get_version_info(),
		"source_sha256": FileAccess.get_sha256("res://scripts/opera_nursery_catch.gd"),
		"qualification": "Focused deterministic intent/lifecycle fixture; not visual/device/child/owner acceptance."}, "\t") + "\n")
	file.close()
	catch.free()
	print("NURSERY_GEOMETRY|RESULT|", "PASS" if bad == 0 else "FAIL")
	quit(1 if bad else 0)
