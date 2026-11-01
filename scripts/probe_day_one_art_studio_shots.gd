extends SceneTree
## Live Craft Room stress and optional Mobile captures. All saves are isolated.
var failures: int = 0
var capture_root: String = ""
var main: ReefMain
var studio: DayOneArtStudio


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(label: String) -> void:
	if capture_root == "":
		return
	await _frames(3)
	await RenderingServer.frame_post_draw
	var pixels: Image = root.get_texture().get_image()
	_check("capture " + label, not pixels.is_empty()
		and pixels.save_png(capture_root.path_join(label + ".png")) == OK)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("ART_STRESS|%s|%s" % ["OK" if ok else "FAIL", label])


func _drive(steps: int) -> void:
	for _index: int in range(steps):
		studio._contact_action._process(0.025)
		studio._process(0.025)


func _tap(point: Vector2) -> void:
	for pressed: bool in [true, false]:
		var event := InputEventScreenTouch.new()
		event.index = 0
		event.pressed = pressed
		event.position = point
		Input.parse_input_event(event)
		await process_frame


func _surface_progress(id: String) -> float:
	var card: Sprite2D = studio._furniture.cards[id] as Sprite2D
	return float((card.material as ShaderMaterial).get_shader_parameter("clean_progress"))


func _run() -> void:
	var save_root: String = OS.get_environment("DAY_ONE_ART_USERDATA_ROOT").replace("\\", "/")
	var actual_save: String = OS.get_user_data_dir().replace("\\", "/")
	_check("explicit isolated save folder", save_root != ""
		and actual_save.begins_with(save_root.simplify_path() + "/"))
	if failures > 0:
		quit(1)
		return
	capture_root = OS.get_environment("DAY_ONE_ART_CAPTURE_OUT")
	if capture_root != "":
		_check("capture requires real Mobile renderer",
			DisplayServer.get_name() != "headless"
			and RenderingServer.get_current_rendering_method() == "mobile")
		DirAccess.make_dir_recursive_absolute(capture_root)
	var view_width: int = maxi(1280, int(OS.get_environment("DAY_ONE_ART_VIEW_WIDTH")))
	root.size = Vector2i(view_width, 720)
	await _frames(4)
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	root.add_child(main)
	await _frames(4)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await _frames(4)
	# This harness tests a saved gameplay checkpoint after its story seams.
	# A still-playing opening clip would hide the room and steal every touch.
	main._day_one_cancel_story_clips()
	main.day_one_story_clips_seen = {
		"d1_opening": true, "d1_castle": true, "d1_bath_arrival": true,
		"d1_bath_clean": true, "d1_pool_arrival": true, "d1_pool_clean": true,
		"d1_eagle_free": true, "d1_art_arrival": true,
	}
	main._day_one_ref().restore_state({
		"day_one_active": true,
		"day_one_current_room": "art",
		"day_one_completed_rooms": ["bathroom", "pool", "stuffie"],
	})
	main.day_one_art_collected_materials = {}
	main.day_one_art_cleaned_grime = {}
	main.day_one_art_desk_unlocked = false
	main.day_one_art_customization_completed = false
	main.pearl_count = 10
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	main._castle_rooms_ref().show_room("craft_room", false)
	await _frames(12)
	main._day_one_cancel_story_clips()
	main._open_day_one_art_studio()
	studio = main._day_one_art_studio
	_check("real room actor and furniture mounted", studio != null
		and studio._contact_action.available() and studio._furniture.cards.size() == 3)
	if studio == null:
		quit(1)
		return
	await _capture("00_dirty_room_with_floor_supplies")
	_drive(160)
	_check("idle does not collect or clean", main.day_one_art_collected_materials.is_empty()
		and main.day_one_art_cleaned_grime.is_empty())
	for id: String in DayOneDirector.ART_GRIME_IDS:
		_check("dirty furniture visible from entry " + id, _surface_progress(id) == 0.0)
		studio._on_grime_pressed(id)
	_check("scrubbing locked until supplies", main.day_one_art_cleaned_grime.is_empty()
		and not studio._contact_action.active)
	var actor: Sprite2D = studio._contact_action.room_actor
	studio._contact_action.room_actor = null
	studio._on_material_pressed("brushes")
	_check("missing actor cannot award remote pickup", studio._pending_id == ""
		and main.day_one_art_collected_materials.is_empty())
	studio._contact_action.room_actor = actor
	# Cancel before arrival, then during storage. Neither may award later.
	studio._on_material_pressed("brushes")
	studio._contact_action.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_drive(240)
	_check("focus cancels pickup without late award", main.day_one_art_collected_materials.is_empty()
		and actor.visible and studio._pending_id == "")
	studio._on_material_pressed("brushes")
	for _index: int in range(240):
		if studio._carrying:
			break
		_drive(1)
	_check("pickup reaches visible carry phase", studio._carrying)
	studio.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	_drive(240)
	_check("interrupted carry restores floor item", main.day_one_art_collected_materials.is_empty()
		and studio._pending_id == "" and actor.visible
		and (studio._material_art["brushes"] as Sprite2D).position.is_equal_approx(
			studio._material_center("brushes") * studio.ART_TO_STAGE))
	for id: String in ["paint_cups", "blue_paint", "pink_paint", "brushes"]:
		var before: int = main.day_one_art_collected_materials.size()
		var button: Button = studio._material_buttons[id] as Button
		await _tap(button.get_global_rect().get_center())
		_check("touch requests pickup before reward " + id,
			main.day_one_art_collected_materials.size() == before
			and studio._pending_id == id)
		for _repeat: int in range(30):
			studio._on_material_pressed(id)
		_drive(300)
		_check("one pickup after travel/storage " + id,
			main.day_one_art_collected_materials.size() == before + 1
			and bool(main.day_one_art_collected_materials.get(id, false)))
	await _capture("01_dirty_furniture_after_supplies")
	studio._on_grime_pressed("left_counter")
	for _index: int in range(240):
		if studio._contact_action.work_time >= 0.4:
			break
		_drive(1)
	_check("partial local brush work changes pixels before progress",
		_surface_progress("left_counter") > 0.0
		and _surface_progress("left_counter") < 1.0
		and main.day_one_art_cleaned_grime.is_empty()
		and studio._contact_action.work_tool.visible)
	await _capture("02_partial_scrub")
	main._pause_ref().toggle_pause()
	await _frames(2)
	_check("gear pause cancels unsaved scrub", studio._pending_id == ""
		and _surface_progress("left_counter") == 0.0)
	main._pause_ref().toggle_pause()
	_drive(240)
	_check("resume never grants canceled scrub", main.day_one_art_cleaned_grime.is_empty())
	studio._on_grime_pressed("left_counter")
	for _index: int in range(300):
		if studio._contact_action.work_time >= 0.30:
			break
		_drive(1)
	studio._contact_action.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_drive(240)
	_check("focus loss during work resets unearned wipe",
		main.day_one_art_cleaned_grime.is_empty() and _surface_progress("left_counter") == 0.0)
	for id: String in ["right_counter", "left_counter", "desk_counter"]:
		var before: int = main.day_one_art_cleaned_grime.size()
		await _tap((studio._grime_buttons[id] as Button).get_global_rect().get_center())
		_check("visible grime touch owns its action " + id, studio._pending_id == id)
		for _repeat: int in range(50):
			studio._on_grime_pressed(id)
			studio._on_grime_pressed("desk_counter")
		_drive(300)
		_check("only requested surface cleans " + id,
			bool(main.day_one_art_cleaned_grime.get(id, false))
			and main.day_one_art_cleaned_grime.size() == before + 1
			and _surface_progress(id) == 1.0)
		await _capture("03_clean_" + id)
	_check("all seven jobs unlock table", main.day_one_art_desk_unlocked
		and not main.day_one_art_customization_completed)
	# Back is cancellation even after selecting a color; reopening remains possible.
	studio._on_desk_pressed()
	main._attack_customizer._on_color_pressed(AttackCustomizer.COLORS[3] as Color)
	main._attack_customizer.close()
	_check("picker Back keeps room incomplete and table reopenable",
		not main.day_one_art_customization_completed and not studio._customizer_open
		and studio._desk_button.visible)
	studio._on_desk_pressed()
	await _capture("04_picker_reopened")
	main._attack_customizer.close()
	# Every saved grime subset restores exact visible dirt with no extra awards.
	var saved_clean: Dictionary = main.day_one_art_cleaned_grime.duplicate()
	for mask: int in range(8):
		var subset: Dictionary = {}
		for bit: int in range(3):
			if mask & (1 << bit):
				subset[DayOneDirector.ART_GRIME_IDS[bit]] = true
		main.day_one_art_cleaned_grime = subset
		_check("save partial surface subset %d" % mask, main._write_save())
		main.day_one_art_cleaned_grime = {}
		main._load_save()
		_check("load partial surface subset %d" % mask,
			main.day_one_art_cleaned_grime == subset)
		main._close_day_one_art_studio()
		await _frames(1)
		main._open_day_one_art_studio()
		studio = main._day_one_art_studio
		studio.refresh_from_state()
		await _frames(3)
		var actor_after_load: Sprite2D = main.castle_room_player_sprite
		_check("reload keeps Roshan opaque %d" % mask, actor_after_load.visible
			and actor_after_load.self_modulate.a > 0.95)
		var ghosts: int = 0
		for child: Node in actor_after_load.get_children():
			if child is SpriteTransition2D:
				ghosts += 1
		_check("reload retains one active smoother %d" % mask, ghosts == 1)
		for bit: int in range(3):
			var id: String = DayOneDirector.ART_GRIME_IDS[bit]
			_check("restore dirty/clean subset %d/%s" % [mask, id],
				_surface_progress(id) == (1.0 if subset.has(id) else 0.0))
	main.day_one_art_cleaned_grime = saved_clean
	studio.refresh_from_state()
	await _capture("05_all_furniture_clean")
	# Exit during a partial action cannot leave cards, hidden originals or callbacks.
	var originals: Array[Dictionary] = studio._furniture.hidden_cards.duplicate()
	main.day_one_art_cleaned_grime = {}
	studio.refresh_from_state()
	studio._on_grime_pressed("left_counter")
	_drive(5)
	main._close_day_one_art_studio()
	await _frames(3)
	var restored: bool = true
	for record: Dictionary in originals:
		var item: CanvasItem = record.get("node") as CanvasItem
		if is_instance_valid(item) and item.visible != bool(record["visible"]):
			restored = false
	_check("teardown restores original room ownership", restored)
	_check("teardown drops unearned scrub", main.day_one_art_cleaned_grime.is_empty())
	main.queue_free()
	await _frames(4)
	print("ART_STRESS|RESULT: %s failures=%d" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(1 if failures > 0 else 0)
