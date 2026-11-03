extends SceneTree
var m: ReefMain
var game: MelodyGame
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("R124_OUT")
var lane := OS.get_environment("R124_LANE")
var width := int(OS.get_environment("R124_WIDTH"))
var height := int(OS.get_environment("R124_HEIGHT"))
var failed := 0
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
		print("R124|FAIL|", label)
func wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame
func shot(label: String) -> void:
	check(label + " has no title-screen occlusion", not m.start_menu_active and m.start_menu_layer == null and m.get_node_or_null("BootSplashHandoff") == null)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var path: String = out.path_join(label + ".png")
	var err: Error = image.save_png(path)
	check(label + " native PNG", err == OK and image.get_size() == Vector2i(width, height))
	frames.append({"path": path, "sha256": FileAccess.get_sha256(path), "width": image.get_width(), "height": image.get_height(), "progress": game.progress_count(), "note": game.active_note_id(), "stage_snapshot": game.audit_snapshot()})
func touch(point: Vector2, pressed: bool) -> void:
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
	m._save_state = SaveState.new(m, "user://r124_isolated_save.json")
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
	check("other original curtain roles remain", frame.get_node("LeftCurtainGeometry") is Polygon2D and frame.get_node("RightCurtainGeometry") is Polygon2D)
	check("original crown and star roles remain", frame.get_node("CrownHeaderGeometry") is Polygon2D and game.surface().get_node("StageStar/StageStarGeometry") is Polygon2D)
	var lights := game.surface().get_node("StageFootlights") as Control
	check("original procedural footlight role remains outside apron scope", lights.get_node("FootlightRailGeometry") is Line2D)
	check("old apron polygon retired", frame.get_node_or_null("StageApronGeometry") == null)
	var fascia := frame.get_node("PaintedStageApronBody") as NinePatchRect
	var rainbow := frame.get_node("PaintedStageApronRainbow") as NinePatchRect
	var frame_size: Vector2 = (frame as Control).size
	var apron_height: float = clampf(frame_size.y * 0.145, 92.0, 106.0)
	var lower_y: float = frame_size.y - apron_height
	var side_width: float = clampf(frame_size.x * 0.15, 176.0, 230.0)
	check("apron body exact whole painted asset", fascia.texture != null and fascia.texture.resource_path == MelodyGame.APRON_BODY_PATH and fascia.texture.get_size() == Vector2(1024, 73))
	check("rainbow inset exact whole seven-color asset", rainbow.texture != null and rainbow.texture.resource_path == MelodyGame.APRON_RAINBOW_PATH and rainbow.texture.get_size() == Vector2(522, 60))
	check("original apron rectangle and height clamp retained", fascia.position.is_equal_approx(Vector2(0.0, lower_y)) and fascia.size.is_equal_approx(Vector2(frame_size.x, apron_height)) and fascia.z_index == -1)
	check("original seven-bar envelope retained", rainbow.position.is_equal_approx(Vector2(side_width * 0.72, lower_y + 11.0)) and rainbow.size.is_equal_approx(Vector2(frame_size.x - side_width * 1.44, 60.0)) and rainbow.z_index == 0)
	check("body end and edge contours preserved", fascia.patch_margin_left == 16 and fascia.patch_margin_right == 16 and fascia.patch_margin_top == 8 and fascia.patch_margin_bottom == 8 and fascia.draw_center)
	check("rainbow whole height and authored ends preserved", rainbow.patch_margin_left == 12 and rainbow.patch_margin_right == 12 and rainbow.patch_margin_top == 0 and rainbow.patch_margin_bottom == 0 and rainbow.draw_center)
	var passive_parts := true
	var untinted_parts := true
	for part: NinePatchRect in [fascia, rainbow]:
		passive_parts = passive_parts and part.mouse_filter == Control.MOUSE_FILTER_IGNORE and part.focus_mode == Control.FOCUS_NONE and part.get_child_count() == 0
		untinted_parts = untinted_parts and part.modulate == Color.WHITE and part.self_modulate == Color.WHITE and part.scale == Vector2.ONE and is_zero_approx(part.rotation) and part.material == null and part.region_rect == Rect2() and part.axis_stretch_horizontal == NinePatchRect.AXIS_STRETCH_MODE_STRETCH
	check("apron parts do not intercept one-finger controls", passive_parts)
	check("apron parts use whole authored pixels without tint or deformation", untinted_parts)
	check("only selected apron parts added to original frame", frame.get_child_count() == 5)

	await shot("01_stage_entry")
	# A released contact clears the existing entry guard without scoring.
	touch(game.active_note_screen_point(), false)
	await wait_frames(3)
	for i in range(360):
		if game.timing_zone_screen_rect().has_point(game.active_note_screen_point()):
			break
		await process_frame
	check("current note reaches green", game.timing_zone_screen_rect().has_point(game.active_note_screen_point()))
	var target: Vector2 = game.active_note_screen_point()
	touch(target, true)
	await wait_frames(2)
	touch(target, false)
	await wait_frames(4)
	check("actual intentional touch scores once", game.progress_count() == 1 and game.active_note_id() == 1)
	await shot("02_one_deliberate_note")
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
	var result := {"status": "PASS" if failed == 0 else "FAIL", "lane": lane, "checks": checks, "captures": frames, "formal_QA11": null, "device": null, "child": null, "owner": null, "configured_route_only": true, "source_pin_sha256": OS.get_environment("R124_PIN_SHA256")}
	var file := FileAccess.open(out.path_join("RESULT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t"))
	file.close()
	print("R124|END|", lane, "|checks=", checks.size(), "|bad=", failed)
	quit(0 if failed == 0 else 1)
