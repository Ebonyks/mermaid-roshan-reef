extends SceneTree
var m: ReefMain
var game: MelodyGame
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("R125_OUT")
var lane := OS.get_environment("R125_LANE")
var width := int(OS.get_environment("R125_WIDTH"))
var height := int(OS.get_environment("R125_HEIGHT"))
var failed := 0
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
		print("R125|FAIL|", label)
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
	m._save_state = SaveState.new(m, "user://r125_isolated_save.json")
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
	check("original procedural footlight role remains outside bulb scope", lights.get_node("FootlightRailGeometry") is Line2D)
	check("original apron polygon remains outside bulb scope", frame.get_node_or_null("StageApronGeometry") is Polygon2D)
	var frame_size: Vector2 = (frame as Control).size
	var count: int = maxi(12, int(frame_size.x / 66.0))
	var whole_sources := true
	var exact_centers := true
	var original_diameters := true
	var untinted_parts := true
	var exact_order := true
	var textured_bulb_instances := 0
	var paths: Array[String] = ["res://assets/melody/theatre_bulb_cream_painted.png", "res://assets/melody/theatre_bulb_gold_painted.png"]
	for i in range(count):
		var x: float = 24.0 + float(i) * (frame_size.x - 48.0) / float(maxi(count - 1, 1))
		for row in range(2):
			var node_name: String = ("UpperPaintedBulb%02d" if row == 0 else "LowerPaintedBulb%02d") % i
			var bulb := frame.get_node_or_null(node_name) as Sprite2D
			if bulb == null:
				whole_sources = false
				continue
			textured_bulb_instances += 1
			var y: float = 22.0 if row == 0 else frame_size.y - 19.0
			var diameter: float = 15.0 if row == 0 else 14.0
			whole_sources = whole_sources and bulb.texture != null and bulb.texture.resource_path == paths[row] and bulb.texture.get_size() == Vector2(128, 128) and not bulb.region_enabled and bulb.centered and bulb.offset == Vector2.ZERO and bulb.hframes == 1 and bulb.vframes == 1
			exact_centers = exact_centers and bulb.position.is_equal_approx(Vector2(x, y))
			original_diameters = original_diameters and bulb.scale.is_equal_approx(Vector2.ONE * diameter / 128.0)
			untinted_parts = untinted_parts and bulb.modulate == Color.WHITE and bulb.self_modulate == Color.WHITE and is_zero_approx(bulb.rotation) and bulb.material == null and not bulb.flip_h and not bulb.flip_v
			exact_order = exact_order and bulb.z_index == 0 and bulb.z_as_relative and not bulb.show_behind_parent and bulb.get_parent() == frame and bulb.get_child_count() == 0 and bulb.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	check("two whole authored bulb variants without region fragments", whole_sources)
	check("original width-dependent bulb count in both rows", textured_bulb_instances == count * 2)
	check("original bulb centers and spacing retained", exact_centers)
	check("upper15 lower14 diameters uniform scale retained", original_diameters)
	check("bulb authored light and colors untinted", untinted_parts)
	check("bulb original Canvas draw order and mipmapped filter", exact_order and (frame as Control).z_index == 10)
	check("only painted bulb cards added to four original frame polygons", frame.get_child_count() == 4 + count * 2)
	var game_source := FileAccess.get_file_as_string("res://scripts/games/melody.gd")
	var proscenium_source: String = game_source.split("class ProsceniumCanvas")[1].split("class FootlightsCanvas")[0]
	check("old two-row draw-circle bulb fallback retired", not proscenium_source.contains("draw_circle("))

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
	var result := {"status": "PASS" if failed == 0 else "FAIL", "lane": lane, "checks": checks, "captures": frames, "formal_QA11": null, "device": null, "child": null, "owner": null, "configured_route_only": true, "source_pin_sha256": OS.get_environment("R125_PIN_SHA256")}
	var file := FileAccess.open(out.path_join("RESULT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t"))
	file.close()
	print("R125|END|", lane, "|checks=", checks.size(), "|bad=", failed)
	quit(0 if failed == 0 else 1)
