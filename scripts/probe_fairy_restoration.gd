extends SceneTree
## Live input, local contact, negative play, interruption and checkpoint proof.
const Prototype := preload("res://scripts/fairy_restoration_prototype.gd")
var stage: FairyRestorationPrototype
var failures := 0
var capture := false
var rows: Array[Dictionary] = []
var game_save_hash := ""

func _init() -> void:
	capture = "--capture" in OS.get_cmdline_user_args()
	call_deferred("_run")

func _check(label: String, condition: bool) -> void:
	print("FAIRYPROBE|", "OK" if condition else "FAIL", "|", label)
	if not condition: failures += 1

func _touch(point: Vector2, pressed: bool, index: int = 0) -> void:
	var event := InputEventScreenTouch.new()
	event.position = stage._world.to_global(point)
	event.index = index
	event.pressed = pressed
	root.push_input(event, true)

func _drag(point: Vector2, index: int = 0) -> void:
	var event := InputEventScreenDrag.new()
	event.position = stage._world.to_global(point)
	event.index = index
	root.push_input(event, true)

func _wait(seconds: float = 1.6) -> void:
	await create_timer(seconds).timeout

func _work_wait(key: String, index: int) -> void:
	# Wait for the actual milestone, not a guessed number of render frames.
	var deadline: int = Time.get_ticks_msec() + 4000
	while (int(stage.progress[key]) & (1 << index)) == 0 and Time.get_ticks_msec() < deadline:
		await process_frame
	_check("local work completes " + key + str(index), (int(stage.progress[key]) & (1 << index)) != 0)

func _tap(point: Vector2) -> void:
	_touch(point, true)
	await process_frame
	_touch(point, false)

func _capture(id: String) -> void:
	if not capture: return
	await process_frame
	await RenderingServer.frame_post_draw
	var directory := "res://tmp/fairy_restoration_review"
	DirAccess.make_dir_recursive_absolute(directory)
	var path: String = directory + "/" + id + ".png"
	var picture: Image = root.get_texture().get_image()
	_check("capture " + id, picture.save_png(path) == OK)
	rows.append({"id": id, "path": path, "phase": stage.phase(), "location": stage.location,
		"progress": stage.progress.duplicate(true), "size": [picture.get_width(), picture.get_height()],
		"sha256": FileAccess.get_sha256(path), "renderer": RenderingServer.get_current_rendering_method(),
		"godot": Engine.get_version_info().string, "script_sha256": FileAccess.get_sha256("res://scripts/fairy_restoration_prototype.gd")})

func _run() -> void:
	# Disk fixtures are permitted only in this task's explicitly isolated profile.
	if not OS.get_user_data_dir().contains("fairy_restoration_review"):
		_check("isolated APPDATA profile required for disk fixtures", false)
		quit(1)
		return
	var game_save := FileAccess.open("user://reef_save.json", FileAccess.WRITE)
	game_save.store_string('{"chapter2_candle_taken":true,"opera_stars":31,"future_key":"preserve"}')
	game_save.close()
	game_save_hash = FileAccess.get_sha256("user://reef_save.json")
	if capture:
		root.mode = Window.MODE_WINDOWED
		root.size = Vector2i(1280, 720)
		root.content_scale_size = Vector2i(1280, 720)
		await process_frame
	stage = Prototype.new()
	stage.persist = false
	root.add_child(stage)
	await process_frame
	await _capture("01_castle_entry")
	_check("starts in castle", stage.location == "castle" and stage.phase() == "arborist")
	await _wait(0.5)
	_check("passive castle does not enter", stage.location == "castle")
	await _tap(Vector2(635, 355))
	await _wait(0.5)
	_check("visible doorway enters garden through live touch", stage.location == "garden")
	if stage.location != "garden":
		quit(1)
		return
	var before: Dictionary = stage.progress.duplicate(true)
	await _wait()
	await _tap(Vector2(80, 590))
	await _wait(0.5)
	_check("passive and wrong taps do not earn work", stage.progress == before)
	await _capture("02_sick_tree")
	await _tap(stage.TREE_POINTS[0])
	await _tap(Vector2(75, 62))
	await _wait(1.1)
	_check("Back cancels travel before any repair reward", stage.location == "castle" and int(stage.progress.cleared) == 0)
	await _tap(Vector2(635, 355))
	_touch(stage.TREE_POINTS[0], true)
	await process_frame
	_check("far selection awards nothing before arrival", int(stage.progress.cleared) == 0 and not stage._arrived)
	_touch(stage.TREE_POINTS[1], true, 1)
	_drag(stage.TREE_POINTS[1], 1)
	_check("second finger cannot redirect local work", stage._index == 0 and stage._owner == 0)
	_touch(stage.TREE_POINTS[0], false)
	var arrival_deadline: int = Time.get_ticks_msec() + 4000
	while not stage._arrived and Time.get_ticks_msec() < arrival_deadline:
		await process_frame
	await _capture("02b_arborist_contact")
	await _work_wait("cleared", 0)
	_check("intentional tap performs one local repair", int(stage.progress.cleared) == 1)
	await _tap(stage.TREE_POINTS[0])
	await _wait(0.5)
	_check("repeat repaired branch earns nothing", int(stage.progress.cleared) == 1)
	for index: int in [1, 2]:
		await _tap(stage.TREE_POINTS[index])
		await _work_wait("cleared", index)
	_check("tree untangling unlocks water only", stage.phase() == "water" and int(stage.progress.picked) == 0)
	await _capture("03_water_roots")
	await _tap(stage.ROOT_POINT)
	await _wait()
	_check("tap and arrival cannot water tree", float(stage.progress.water) == 0.0)
	_touch(stage.ROOT_POINT + Vector2(-35, 0), true)
	await _wait(1.2)
	_drag(Vector2(1000, 600))
	_check("off-target water motion earns nothing", float(stage.progress.water) == 0.0)
	_drag(stage.ROOT_POINT + Vector2(-35, 0))
	_drag(stage.ROOT_POINT + Vector2(35, 0))
	await process_frame
	_check("local water stroke advances partial checkpoint", float(stage.progress.water) > 0.0 and float(stage.progress.water) < 1.0)
	stage.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	var partial: float = float(stage.progress.water)
	await _wait(0.3)
	_drag(stage.ROOT_POINT + Vector2(-35, 0))
	_check("focus loss cancels owned gesture", stage._owner == -2 and float(stage.progress.water) == partial)
	stage.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_touch(stage.ROOT_POINT, false)
	await _tap(Vector2(75, 62))
	await _tap(Vector2(635, 355))
	_check("Back and re-entry preserve partial water", float(stage.progress.water) == partial)
	_touch(stage.ROOT_POINT + Vector2(-35, 0), true)
	await _wait(1.2)
	for step: int in range(10):
		_drag(stage.ROOT_POINT + Vector2(35 if step % 2 == 0 else -35, 0))
		await process_frame
	_touch(stage.ROOT_POINT, false)
	_check("intentional watering grows fruit", stage.phase() == "harvest")
	await _capture("04_healthy_fruit_tree")
	for index: int in range(3):
		await _tap(stage.FRUIT_POINTS[index])
		await _work_wait("picked", index)
	_check("harvest supplies three apples to chef", stage.phase() == "chef" and int(stage.progress.picked) == 7)
	await _capture("05_chef_whole_apples")
	await _tap(stage.CHEF_POINTS[0])
	await _wait()
	_check("chef tapping cannot cut food", int(stage.progress.cut) == 0)
	for index: int in range(3):
		_touch(stage.CHEF_POINTS[index] + Vector2(-55, 0), true)
		await _wait(1.2)
		if index == 0: await _capture("05b_chef_contact")
		_drag(stage.CHEF_POINTS[index] + Vector2(55, 0))
		await process_frame
		_touch(stage.CHEF_POINTS[index], false)
	_check("local cross-fruit swipes prepare all snacks", stage.phase() == "picnic")
	await _capture("06_prepared_snacks")
	for index: int in range(3):
		await _tap(stage.FRIEND_POINTS[index])
		await _work_wait("fed", index)
	_check("feeding friends opens flower flight", stage.phase() == "shooter")
	await _capture("07_flower_flight")
	await _wait()
	_check("shooter never fires from passive play", int(stage.progress.bloom) == 0)
	_touch(Vector2(470, 530), true)
	await _wait(1.0)
	_touch(Vector2(470, 530), false)
	_check("wrong lane does not bloom a flower", int(stage.progress.bloom) == 0)
	_touch(Vector2(300, 530), true)
	await _wait(1.0)
	_check("holding in correct lane blooms first flower", int(stage.progress.bloom) == 1)
	_drag(Vector2(640, 530))
	await _wait(1.0)
	_drag(Vector2(980, 530))
	await _wait(1.0)
	_touch(Vector2(980, 530), false)
	_check("one held finger can glide across all flower lanes", stage.phase() == "complete" and not bool(stage.progress.returned))
	await _capture("08_fountain_restored")
	await _tap(Vector2(640, 525))
	_check("intentional carry-home restores faerie half only", stage.location == "castle" and bool(stage.progress.returned))
	await _capture("09_castle_faerie_magic")
	var completed: Dictionary = stage.progress.duplicate(true)
	await _tap(Vector2(635, 355))
	await _tap(Vector2(640, 525))
	_check("replay cannot duplicate or erase milestones", stage.progress == completed)
	_check("every phase has an exact cue and OGG", stage.cue_history.size() >= 9)
	for key: String in ["enter", "returned", "arborist", "water", "harvest", "chef", "picnic", "shooter", "complete"]:
		_check("voice cue " + key, ResourceLoader.exists("res://assets/prototypes/fairy_restoration/voices/" + key + ".ogg"))
	# Actual disk round-trip/backup recovery uses a task-isolated APPDATA profile.
	stage.persist = true
	stage.progress["future_key"] = "retained"
	stage.save_checkpoint()
	stage.save_checkpoint()
	var fresh := Prototype.new()
	fresh.load_checkpoint()
	_check("checkpoint round-trip preserves progress and future keys", fresh.progress == stage.progress)
	var broken := FileAccess.open(stage.SAVE_PATH, FileAccess.WRITE)
	broken.store_string("{broken")
	broken.close()
	fresh.progress = {"cleared": 0, "water": 0.0, "picked": 0, "cut": 0, "fed": 0, "bloom": 0, "returned": false}
	fresh.load_checkpoint()
	_check("corrupt main checkpoint recovers backup", fresh.progress == stage.progress)
	_check("production save canary remains byte-identical", FileAccess.get_sha256("user://reef_save.json") == game_save_hash)
	fresh.free()
	if capture:
		var manifest := FileAccess.open("res://tmp/fairy_restoration_review/CAPTURE_MANIFEST.json", FileAccess.WRITE)
		manifest.store_string(JSON.stringify({"baseline": "285355eb9e09a29aa4ac53d36874e31419d4674e", "frames": rows}, "\t"))
		manifest.close()
	stage.queue_free()
	await process_frame
	await process_frame
	# The dummy audio driver releases stopped OGG playback on its own thread.
	# Uncapped headless frames can otherwise quit before that release finishes.
	await create_timer(0.25).timeout
	print("FAIRYPROBE|RESULT|", "ALL OK" if failures == 0 else "FAIL", "|failures=", failures)
	quit(0 if failures == 0 else 1)
