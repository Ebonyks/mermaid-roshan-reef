extends SceneTree
## Drives the real start menu with pointer presses. New Game must stay safe
## from a child's quick taps yet be reachable by a grown-up: START NEW is
## hold-gated, names the gesture, fills a bar while held, and completes only
## after a full hold. Uses an isolated save so the real save is never touched.

const PROBE_SAVE_URI := "user://probe_start_menu_new_game_save.json"
const SAVE_SUFFIXES: Array[String] = [
	"", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old",
	".before_new_game", ".before_new_game.tmp", ".before_new_game.old",
]
const SEEDED_GENERATION := 7

var main: ReefMain
var packed: PackedScene
var failures: int = 0
var probe_save_path := ""
var start_presses: int = 0


func _init() -> void:
	probe_save_path = ProjectSettings.globalize_path(PROBE_SAVE_URI)
	_remove_probe_save_artifacts()
	_seed_existing_save()
	packed = load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	main._save_state = SaveState.new(main, probe_save_path)
	get_root().add_child(main)
	await process_frame
	await process_frame
	_check("seeded save counts as an adventure to keep", main.has_saved_game)
	if main.intro_active:
		main._skip_intro()
	await _frames(4)
	main._build_start_menu()
	await _frames(3)
	var menu_layer: Node = main.start_menu_layer
	var new_game := _find_button(menu_layer, "StartMenuNewGameButton")
	var confirm := menu_layer.find_child("StartMenuNewGameConfirmation", true, false) as Control \
		if menu_layer != null else null
	var start := _find_button(menu_layer, "StartMenuConfirmNewGameButton")
	var caption := menu_layer.find_child("StartMenuNewGameHoldCaption", true, false) as Label \
		if menu_layer != null else null
	var fill := menu_layer.find_child("StartMenuNewGameHoldFill", true, false) as Panel \
		if menu_layer != null else null
	_check("start menu, confirm sheet and START NEW exist",
		new_game != null and confirm != null and start != null)
	_check("START NEW names the hold gesture for a grown-up",
		caption != null and caption.text == "PRESS AND HOLD")
	_check("START NEW carries a hold progress bar", fill != null)
	if new_game == null or confirm == null or start == null or caption == null or fill == null:
		_finish()
		return
	start.button_down.connect(func() -> void: start_presses += 1)
	var baseline_generation: int = main.save_generation

	await _click(new_game, 0.08)
	_check("NEW GAME opens the confirm sheet", confirm.is_visible_in_tree())
	_check("hold caption is visible on the confirm sheet", caption.is_visible_in_tree())
	_check("START NEW starts disarmed", start.disabled)
	await _click(start, 0.08)
	_check("a tap on the disarmed START NEW changes nothing",
		confirm.is_visible_in_tree() and main.save_generation == baseline_generation)

	await _wait(StartMenu.NEW_GAME_ARM_DELAY_SECONDS + 0.2)
	_check("START NEW arms after its delay", not start.disabled)
	_press(start, true)
	await _wait(StartMenu.NEW_GAME_HOLD_SECONDS * 0.4)
	var partial_width: float = fill.size.x
	_press(start, false)
	await _wait(StartMenu.NEW_GAME_HOLD_SECONDS + 0.3)
	_check("the pointer press reached START NEW", start_presses >= 1)
	_check("the bar fills while START NEW is held",
		partial_width > 4.0 and partial_width < start.size.x)
	_check("a quick tap never starts a new game",
		confirm.is_visible_in_tree()
		and main.save_generation == baseline_generation
		and not FileAccess.file_exists(probe_save_path + SaveState.NEW_GAME_ARCHIVE_SUFFIX))
	_check("a lifted press empties the bar", is_zero_approx(fill.size.x))
	_check("a lifted press pulses the hold caption",
		int(caption.get_meta("hold_hint_pulses", 0)) == 1)

	_press(start, true)
	await _wait(StartMenu.NEW_GAME_HOLD_SECONDS + 0.3)
	var full_width: float = fill.size.x
	_press(start, false)
	await _frames(2)
	_check("a full hold fills the bar",
		full_width >= start.size.x - StartMenu.NEW_GAME_HOLD_FILL_INSET * 2.0 - 0.5)
	_check("a full hold installs a fresh save",
		main.save_generation > baseline_generation)
	_check("a full hold keeps the old adventure in the grown-up archive",
		_archived_generation() == SEEDED_GENERATION)
	_check("a full hold routes the reload into Day One",
		get_root().has_meta(StartMenu.DAY_ONE_AFTER_RESET_META))
	_check("a completed hold does not pulse the tap hint",
		int(caption.get_meta("hold_hint_pulses", 0)) == 1)
	await _probe_reload_into_day_one(main.save_generation)
	_finish()


func _probe_reload_into_day_one(fresh_generation: int) -> void:
	# The probe has no current scene, so the menu's deferred reload is inert.
	# Replay what the reload does: boot a fresh main on the same isolated save
	# while the reset marker is still on the root, then let the menu route it.
	main.queue_free()
	await _frames(3)
	main = packed.instantiate() as ReefMain
	main._save_state = SaveState.new(main, probe_save_path)
	get_root().add_child(main)
	await _frames(2)
	if main.intro_active:
		main._skip_intro()
	await _frames(2)
	main._build_start_menu()
	await _frames(4)
	_check("the reloaded game skips the menu and starts Day One",
		main.day_one_is_active() and not main.start_menu_active)
	_check("the reload consumes its one-shot marker",
		not get_root().has_meta(StartMenu.DAY_ONE_AFTER_RESET_META))
	_check("the reloaded game runs on the fresh save",
		main.save_generation == fresh_generation)
	_check("the fresh Day One has no finished rooms",
		main._day_one_ref().completed_rooms.is_empty())


func _seed_existing_save() -> void:
	var file := FileAccess.open(probe_save_path, FileAccess.WRITE)
	file.store_string(JSON.stringify({
		"schema_version": 1,
		"save_generation": SEEDED_GENERATION,
		"day_one_active": true,
		"music": true,
	}))
	file.close()


func _archived_generation() -> int:
	var path := probe_save_path + SaveState.NEW_GAME_ARCHIVE_SUFFIX
	if not FileAccess.file_exists(path):
		return -1
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return -1
	return int((parsed as Dictionary).get("save_generation", -1))


func _find_button(root_node: Node, node_name: String) -> Button:
	if root_node == null:
		return null
	return root_node.find_child(node_name, true, false) as Button


func _click(button: Button, hold_seconds: float) -> void:
	_press(button, true)
	await _wait(hold_seconds)
	_press(button, false)
	await _frames(2)


func _press(button: Button, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	# Headless windows are tiny and stretched, so deliver the press in the
	# root viewport's own canvas coordinates rather than window pixels.
	var point: Vector2 = button.get_global_rect().get_center()
	event.position = point
	event.global_position = point
	get_root().push_input(event, true)


func _wait(seconds: float) -> void:
	await create_timer(seconds).timeout


func _frames(count: int) -> void:
	for _i in range(count):
		await process_frame


func _remove_probe_save_artifacts() -> void:
	for suffix: String in SAVE_SUFFIXES:
		var path := probe_save_path + suffix
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)


func _finish() -> void:
	if get_root().has_meta(StartMenu.DAY_ONE_AFTER_RESET_META):
		get_root().remove_meta(StartMenu.DAY_ONE_AFTER_RESET_META)
	if main != null and is_instance_valid(main):
		main.queue_free()
	await _frames(2)
	_remove_probe_save_artifacts()
	print("START_MENU_NEW_GAME|RESULT: ",
		"PASS" if failures == 0 else "FAIL",
		" failures=", failures)
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("START_MENU_NEW_GAME|", label, ": ", "OK" if ok else "FAIL")
