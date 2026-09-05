extends SceneTree
# The Royal Hall sparring class: walking through its event-ready door opens it,
# each lesson waits for the CHILD's own input (nothing auto-advances), the
# lessons progress tap → combo → charge → wave, a full charge fires itself,
# the diploma persists, and the castle hall comes back afterwards.

const FLOOR_TAP := Vector2(1050.0, 560.0)
const WALK_SETTLE := 90
const MAX_WALK_TAPS := 8

var main: ReefMain
var bad := 0
var capture_dir := ""

func _init() -> void:
	seed(20260801)
	capture_dir = OS.get_environment("TUTORIAL_CAPTURE_DIR")
	if capture_dir != "":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(Vector2i(1280, 720))
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
	else:
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

func _touch(at: Vector2) -> void:
	var down := InputEventMouseButton.new()
	down.button_index = MOUSE_BUTTON_LEFT
	down.pressed = true
	down.position = at
	down.global_position = at
	root.push_input(down, true)
	var up := InputEventMouseButton.new()
	up.button_index = MOUSE_BUTTON_LEFT
	up.pressed = false
	up.position = at
	up.global_position = at
	root.push_input(up, true)

func _tap_button(button: Button) -> bool:
	if button == null or not is_instance_valid(button) \
			or not button.is_visible_in_tree():
		return false
	_touch(button.get_global_transform_with_canvas() * (button.size * 0.5))
	return true

func _capture(name: String) -> void:
	if capture_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(capture_dir)
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	if image != null:
		image.save_png(capture_dir.path_join(name + ".png"))

func _tap_stage(at: Vector2) -> void:
	_touch(main.castle_room_stage.get_global_transform_with_canvas() * at)

func _royal_hall_button() -> Button:
	for record: Dictionary in main.castle_room_door_hotspots:
		var data: Dictionary = record.get("data", {})
		if String(data.get("id", "")) == "__royal_hall":
			return record.get("button") as Button
	return null

func _tap(tut: CombatTutorial, enemy: Dictionary) -> void:
	var pos: Vector2 = tut.cam.unproject_position(tut.he.aim_point(enemy))
	main._on_world_press(pos)
	main._on_world_press_release()

func _class_case() -> void:
	main.level2_done_once = true
	main.companion_id = "eagle"
	main.combat_tutorial_done = false
	main.pearl_count = main.PEARL_TOTAL
	main.trophies = 5
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(24)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	_ck("the first class readies the Royal Hall gate",
		rooms._royal_hall_event_id() == "combat_tutorial")
	if capture_dir != "":
		# Rendering capture runs use a real window where synthetic castle-floor
		# navigation is platform-focus dependent. Enter the same activity through
		# its production room helper; the default probe still gates the real door.
		rooms._start_combat_tutorial()
	else:
		var royal_hall_button: Button = _royal_hall_button()
		var walk_taps := 0
		while royal_hall_button != null and not royal_hall_button.visible \
				and walk_taps < MAX_WALK_TAPS:
			_tap_stage(FLOOR_TAP)
			await _frames(WALK_SETTLE)
			walk_taps += 1
			royal_hall_button = _royal_hall_button()
		_ck("the class gate is reached through real floor navigation",
			royal_hall_button != null and royal_hall_button.visible)
		var touched_gate := _tap_button(royal_hall_button)
		_ck("the sparring class starts from the real Royal Hall touch target",
			touched_gate)
	var arrival_deadline_msec: int = Time.get_ticks_msec() + 3000
	while main.combat_tutorial_game == null \
			and Time.get_ticks_msec() < arrival_deadline_msec:
		await process_frame
	var tut: CombatTutorial = main.combat_tutorial_game
	_ck("the Royal Hall door opens the sparring class",
		tut != null and main.hit_engines.has(tut.he))
	if tut == null:
		rooms.close()
		return
	_ck("the grotto is a true Canvas backdrop", tut.backdrop_layer != null
		and tut.backdrop_layer.get_child_count() >= 1
		and tut.backdrop_layer.get_child(0) is TextureRect
		and main.we_node.environment.background_mode == 3
		and main.we_node.environment.background_canvas_max_layer == -10)
	_ck("the reusable guide loads approved TAP and HOLD pictures",
		tut.demo is EncounterGestureGuide2D and tut.demo.tap_chip != null
		and tut.demo.hold_chip != null and tut.demo.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	_ck("class begins at the TAP lesson", tut.lesson == "tap")
	_ck("Roshan and the live imp remain in front of the Canvas grotto",
		tut.avatar.visible and bool(tut.enemies[0]["node"].visible))
	print("TUTORIAL|caption_geometry|", main.hud_msg.position, "|", main.hud_msg.size)
	_ck("the tutorial uses the compact scoped caption strip",
		main.hud_msg.position == Vector2(320.0, 626.0)
		and main.hud_msg.size == Vector2(640.0, 82.0))
	_ck("tutorial suppresses the unrelated JUMP medallion",
		main.touch_ui._act_button == null or not main.touch_ui._act_button.visible)
	await _capture("01_tap")
	await _frames(30)
	var first: Dictionary = tut.enemies[0]
	_ck("nothing advances without her input",
		tut.lesson == "tap" and int(first["hp"]) == 3)
	_tap(tut, first)
	await _frames(1)
	_ck("her first bop advances to COMBO",
		tut.lesson == "combo" and int(first["hp"]) == 2)
	await _capture("02_combo")
	_tap(tut, first)
	_tap(tut, first)
	await _frames(2)
	_ck("the 1-2-3 combo pops the imp into the CHARGE lesson",
		tut.lesson == "charge")
	await _frames(25)   # let the combo window lapse so the hold is a clean read
	var second: Dictionary = tut._lesson_target()
	_ck("a fresh sparring imp waits", not second.is_empty() and int(second["hp"]) == 3)
	_ck("the prior combo does not hide the new hold demonstration", tut.demo.visible)
	await _capture("03_hold")
	var pos: Vector2 = tut.cam.unproject_position(tut.he.aim_point(second))
	main._on_world_press(pos)   # press-fire tap, then HOLD — no release
	await _frames(20)           # past the engine's live 1.75 s full-charge time
	_ck("a full charge fells the imp and readies partner power",
		tut.lesson == "partner" and String(second["state"]) != "active")
	await _frames(2)
	_ck("the companion lesson shows its picture bubble",
		tut.pa != null and tut.pa.bubble != null)
	_ck("the teaching hand stays above the partner portrait",
		tut.pa != null and tut.pa.layer != null and tut.demo_layer.layer > tut.pa.layer.layer)
	await _capture("04_partner")
	if tut.pa != null and tut.pa.bubble != null:
		tut.pa.bubble.pressed.emit()
	await _frames(2)
	_ck("partner power opens the graduation wave",
		tut.lesson == "wave" and tut.enemies.size() >= 4)
	await _capture("05_wave")
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
	_ck("the global caption layout is restored",
		main.hud_msg.position == Vector2(230.0, 590.0)
		and main.hud_msg.size == Vector2(820.0, 112.0))
	_ck("the castle hall comes back",
		rooms.is_open() and main.castle_room_layer.visible)
	rooms._tick_royal_hall_mist(1.0)
	var royal_hall_mist_restored := \
		main.castle_royal_hall_mist_cards.size() == 5
	for mist: Sprite2D in main.castle_royal_hall_mist_cards:
		var rest_alpha: float = float(mist.get_meta("mist_rest_alpha", 0.0))
		royal_hall_mist_restored = royal_hall_mist_restored \
			and mist.modulate.a >= rest_alpha * 0.90
	_ck("the Royal Hall reseals after graduation",
		rooms._royal_hall_event_id().is_empty()
		and royal_hall_mist_restored)
	rooms.close()
	await process_frame
