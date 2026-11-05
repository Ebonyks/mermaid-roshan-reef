extends SceneTree
var m: ReefMain
var game: MelodyGame
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("RINT_OUT")
var lane := OS.get_environment("RINT_LANE")
var width := int(OS.get_environment("RINT_WIDTH"))
var height := int(OS.get_environment("RINT_HEIGHT"))
var failed := 0
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
		print("RINT|FAIL|", label)
func wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame
func shot(label: String) -> void:
	check(label + " has no title-screen occlusion", not m.start_menu_active and m.start_menu_layer == null and m.get_node_or_null("BootSplashHandoff") == null)
	check(label + " painted guidance uses original target/path/pulse", guide_contract())
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var path: String = out.path_join(label + ".png")
	var err: Error = image.save_png(path)
	check(label + " native PNG", err == OK and image.get_size() == Vector2i(width, height))
	frames.append({"path": path, "sha256": FileAccess.get_sha256(path), "width": image.get_width(), "height": image.get_height(), "progress": game.progress_count(), "note": game.active_note_id(), "stage_snapshot": game.audit_snapshot(), "guide": pointer_bindings()})
func touch(point: Vector2, pressed: bool) -> void:
	print("RINT|TOUCH_TRACE|pressed=", pressed, "|frame=", Engine.get_process_frames(), "|progress=", game.progress_count(), "|active_note=", game.active_note_id(), "|focused=", get_root().has_focus(), "|point=", point)
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = point
	event.pressed = pressed
	Input.parse_input_event(event)
func run() -> void:
	seed(20261101)
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(width, height)
	DirAccess.make_dir_recursive_absolute(out)
	var packed := load("res://scenes/main.tscn") as PackedScene
	m = packed.instantiate() as ReefMain
	m._save_state = SaveState.new(m, "user://recent_updates_isolated_save.json")
	get_root().add_child(m)
	await wait_frames(20)
	check("actual display start menu is present", m.start_menu_active and m.start_menu_layer != null)
	var continue_button := m.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button
	check("real Continue control found", continue_button != null)
	if continue_button == null:
		await finish()
		return
	# Match the existing display-boot probe's isolated resumable-save fixture.
	var completed_save: Dictionary = m.save_data.duplicate(true)
	completed_save["day_one_active"] = false
	completed_save["day_one_completed_rooms"] = ["bathroom", "pool", "stuffie", "art"]
	m._day_one_ref().restore_state(completed_save)
	m.save_data.merge(m._day_one_ref().serialize_state(), true)
	m.has_saved_game = true
	continue_button.disabled = false
	continue_button.pressed.emit()
	await wait_frames(20)
	check("Continue removes title menu before Melody", not m.start_menu_active and m.start_menu_layer == null and not m.intro_active)
	m._set_touch_mode(m.TOUCH_MODE_HYBRID, false)
	m._apply_quality("speedy")
	get_root().grab_focus()
	await wait_frames(4)
	check("owned context window focused for real touch", get_root().has_focus())
	var friend: Dictionary = {}
	var routes := 0
	for item: Dictionary in m.friends:
		if String(item.get("game", "")) == "melody":
			friend = item
			routes += 1
	check("single Daddy route", routes == 1 and String(friend.get("fname", "")) == "Daddy Mermaid")
	if friend.is_empty():
		await finish()
		return
	if m.touch_ui != null:
		m.touch_ui.consume_action()
	m._start_game(friend)
	game = m._game_obj("melody", MelodyGame) as MelodyGame
	for i in range(240):
		if m.game == "melody" and m.fade_rect.modulate.a < 0.02:
			break
		await process_frame
	check("production Melody entry and reveal", m.game == "melody" and game != null and m.fade_rect.modulate.a < 0.02)
	check("Mobile renderer", RenderingServer.get_current_rendering_method() == "mobile")
	check("actual expanded viewport", get_root().get_visible_rect().size == Vector2(width, height))
	check("initial progress zero", game.progress_count() == 0 and game.active_note_id() == 0)
	await wait_frames(12)
	check("passive cannot score", game.progress_count() == 0)
	var frame: Node = game.surface().get_node("OperaProscenium")
	check("stage parent and ignore mouse", frame is Control and (frame as Control).mouse_filter == Control.MOUSE_FILTER_IGNORE)
	check("Daddy original texture", (game.surface().get_node("DaddyGuide") as Sprite2D).texture.resource_path == MelodyGame.DADDY_PATH)
	check("Roshan original texture", (game.surface().get_node("PopstarRoshan") as Sprite2D).texture.resource_path == MelodyGame.ROSHAN_PATH)
	check("original goal seven", game.note_count() == 7)
	check("original hit target120", game.active_note_hit_rect().size == Vector2.ONE * 120.0)
	check("both whole painted curtain roles remain",
		frame.get_node_or_null("LeftPaintedCurtain/PaintedCloth") is TextureRect \
		and frame.get_node_or_null("RightPaintedCurtain/PaintedCloth") is TextureRect)
	check("painted crown/star replace retired geometry",
		frame.get_node_or_null("PaintedCrownHeader") is TextureRect \
		and game.surface().get_node_or_null("StageStar/StageStarPaintedCard") is TextureRect \
		and frame.get_node_or_null("CrownHeaderGeometry") == null)
	var lights := game.surface().get_node("StageFootlights") as Control
	check("whole painted footlight rail and13 globes",
		lights.get_child_count() == 14 and lights.get_node_or_null("PaintedFootlightRail") is NinePatchRect \
		and lights.get_node_or_null("FootlightRailGeometry") == null)
	check("whole painted apron pair and retired polygon absent",
		frame.get_node_or_null("PaintedStageApronBody") is NinePatchRect \
		and frame.get_node_or_null("PaintedStageApronRainbow") is NinePatchRect \
		and frame.get_node_or_null("StageApronGeometry") == null)
	check("painted timing pair replaces old geometry",
		game.surface().get_node("TimingZone").get_child_count() == 2 \
		and game.surface().get_node_or_null("TimingZone/GreenWindowGeometry") == null)
	var pointer := game.surface().get_node("VisualPointer") as Control
	check("three sole painted guide children and no retired primitive", pointer.get_child_count() == 3 and pointer.get_node_or_null("PointerArrowPainted") is Sprite2D and pointer.get_node_or_null("PointerBeamPainted") is Sprite2D and pointer.get_node_or_null("PointerRingPainted") is Sprite2D and pointer.get_node_or_null("PointerTargetGeometry") == null and pointer.get_node_or_null("PointerLineGeometry") == null)
	check("guide shares original active note and ignores input", pointer.z_index == 32 and pointer.mouse_filter == Control.MOUSE_FILTER_IGNORE and int(pointer.get("target_id")) == game.active_note_id())
	var fractions: Array[float] = [0.08, 0.30, 0.55, 0.75, 0.93]
	var labels: Array[String] = ["01_left_08", "02_approach_30", "03_mid_55", "04_window_75", "05_right_93"]
	for index in range(fractions.size()):
		var found := false
		for wait_index in range(600):
			var start: Vector2 = game.get("_track_start")
			var end: Vector2 = game.get("_track_end")
			var fraction: float = (game.active_note_screen_point().x - start.x) / (end.x - start.x)
			if fraction >= fractions[index] and fraction <= fractions[index] + 0.04:
				found = true
				break
			await process_frame
		check(labels[index] + " actual passive travel position reached", found)
		check(labels[index] + " original target equals note", (pointer.get("target") as Vector2).is_equal_approx(game.active_note_screen_point()) and int(pointer.get("target_id")) == 0 and game.progress_count() == 0)
		await shot(labels[index])
	check("full selected guide travel remains passive and cannot win", game.progress_count() == 0 and game.active_note_id() == 0 and m.game == "melody" and not bool(friend.get("won", false)))
	for note_id in range(1, 7):
		for wait_index in range(360):
			if bool(game.call("_note_is_in_green")):
				break
			await process_frame
		get_root().grab_focus()
		await wait_frames(4)
		check("owned window remains focused before one-finger press " + str(note_id), get_root().has_focus())
		var center: Vector2 = game.active_note_screen_point()
		touch(center, true)
		await wait_frames(4)
		touch(center, false)
		await wait_frames(4)
		check("one-finger progression " + str(note_id), game.progress_count() == note_id and game.active_note_id() == note_id)
		if game.progress_count() != note_id or game.active_note_id() != note_id:
			await finish()
			return
		for wait_index in range(360):
			if bool(game.call("_note_is_in_green")):
				break
			await process_frame
		await shot("0" + str(5 + note_id) + "_note_" + str(note_id) + "_green" if note_id < 5 else str(5 + note_id) + "_note_" + str(note_id) + "_green")
	await finish()

func finish() -> void:
	if m != null and is_instance_valid(m):
		m.process_mode = Node.PROCESS_MODE_DISABLED
		if game != null:
			game.stage_close()
			check("configured stage close clears layer", game.active_layer() == null)
		m.get_parent().remove_child(m)
		m.free()
	await process_frame
	var result := {"status": "PASS" if failed == 0 else "FAIL", "lane": lane, "checks": checks, "captures": frames, "formal_QA11": null, "device": null, "child": null, "owner": null, "configured_route_only": true, "source_pin_sha256": OS.get_environment("RINT_PIN_SHA256")}
	var file := FileAccess.open(out.path_join("RESULT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t"))
	file.close()
	print("RINT|END|", lane, "|checks=", checks.size(), "|bad=", failed)
	quit(0 if failed == 0 else 1)

func pointer_bindings() -> Dictionary:
	var pointer := game.surface().get_node("VisualPointer") as Control
	var target: Vector2 = pointer.get("target")
	var zone_center: Vector2 = pointer.get("zone_center")
	var pulse: float = float(pointer.get("pulse"))
	var head := pointer.get_node("PointerArrowPainted") as Sprite2D
	var beam := pointer.get_node("PointerBeamPainted") as Sprite2D
	var ring := pointer.get_node("PointerRingPainted") as Sprite2D
	return {"target": str(target), "zone_center": str(zone_center), "pulse": pulse, "ring_radius": 34.0 + sin(pulse * 6.0) * 5.0, "head_transform": str(head.transform), "head_texture": head.texture.resource_path, "beam_transform": str(beam.transform), "beam_visible": beam.visible, "beam_texture": beam.texture.resource_path, "ring_transform": str(ring.transform), "ring_texture": ring.texture.resource_path, "target_id": pointer.get("target_id"), "z_index": pointer.z_index}


func guide_contract() -> bool:
	var p := game.surface().get_node("VisualPointer") as Control
	var head := p.get_node("PointerArrowPainted") as Sprite2D
	var beam := p.get_node("PointerBeamPainted") as Sprite2D
	var ring := p.get_node("PointerRingPainted") as Sprite2D
	var target: Vector2 = game.active_note_screen_point()
	var zone: Vector2 = p.get("zone_center")
	var direction: Vector2 = target - zone
	direction = Vector2.RIGHT if direction.length_squared() <= 0.001 else direction.normalized()
	var a: Vector2 = zone + direction * 82.0
	var b: Vector2 = target - direction * 38.0
	var pulse: float = float(p.get("pulse"))
	var radius: float = 34.0 + sin(pulse * 6.0) * 5.0
	return head.visible and ring.visible and head.position.distance_to(target) < 0.01 \
		and int(p.get("target_id")) == game.active_note_id() \
		and absf(angle_difference(head.rotation, direction.angle())) < 0.001 \
		and (beam.get_global_transform_with_canvas() * Vector2(-64, 0)).distance_to(a) < 0.01 \
		and (beam.get_global_transform_with_canvas() * Vector2(64, 0)).distance_to(b) < 0.01 \
		and is_equal_approx(beam.scale.y * 36.0, 9.0) \
		and beam.visible == (a.distance_to(b) > 14.0) \
		and ring.position.distance_to(target) < 0.01 \
		and ring.scale.is_equal_approx(Vector2.ONE * ((radius + 8.0) * 2.0 + 5.0) / 253.0)
