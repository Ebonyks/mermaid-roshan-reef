extends SceneTree
var m: ReefMain
var game: MelodyGame
var checks: Array[Dictionary] = []
var frames: Array[Dictionary] = []
var out := OS.get_environment("R126_OUT")
var lane := OS.get_environment("R126_LANE")
var width := int(OS.get_environment("R126_WIDTH"))
var height := int(OS.get_environment("R126_HEIGHT"))
var failed := 0
func _init() -> void:
	call_deferred("run")
func check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok})
	if not ok:
		failed += 1
		print("R126|FAIL|", label)
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
	m._save_state = SaveState.new(m, "user://r126_isolated_save.json")
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
	var names: Array[String] = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
	var source_notes_ok := true
	var painted_notes_ok := true
	for i in range(7):
		var note := game.surface().get_node("RainbowNote%d" % i) as Control
		source_notes_ok = source_notes_ok and note != null and note.get_node_or_null("NoteColorGeometry") is Polygon2D
		var card := note.get_node_or_null("PaintedNote") as Sprite2D
		painted_notes_ok = painted_notes_ok and card != null
		if card != null:
			painted_notes_ok = painted_notes_ok and card.texture.resource_path == "res://assets/melody/rainbow_note_" + names[i] + "_painted.png" and card.texture.get_size() == Vector2(256, 256) and card.centered and not card.region_enabled and card.hframes == 1 and card.vframes == 1 and card.position == Vector2.ONE * 42.0 and card.scale.is_equal_approx(Vector2.ONE * 84.0 / 256.0) and card.modulate == Color.WHITE and card.self_modulate == Color.WHITE and card.material == null and card.z_index == 0 and card.z_as_relative and card.get_child_count() == 0 and card.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS and note.get_child_count() == 1 and note.z_index == 35 and note.mouse_filter == Control.MOUSE_FILTER_IGNORE
	check("selected lane exact original geometry or seven complete painted tokens", source_notes_ok if lane == "source" else painted_notes_ok)
	var game_source := FileAccess.get_file_as_string("res://scripts/games/melody.gd")
	var note_source: String = game_source.split("class RainbowNoteCanvas")[1].split("class ProgressPipCanvas")[0]
	check("selected lane original or retired primitive note fallback", note_source.contains("draw_circle(") if lane == "source" else not note_source.contains("draw_circle(") and not note_source.contains("Polygon2D"))
	# A released contact clears the existing entry guard without scoring.
	touch(game.active_note_screen_point(), false)
	await wait_frames(3)
	for note_id in range(7):
		check("ordered active token %d" % note_id, game.active_note_id() == note_id and game.progress_count() == note_id)
		for i in range(360):
			if game.timing_zone_screen_rect().has_point(game.active_note_screen_point()):
				break
			await process_frame
		check("note %d reaches original green window" % note_id, game.timing_zone_screen_rect().has_point(game.active_note_screen_point()))
		await shot("%02d_%s_active" % [note_id + 1, names[note_id]])
		var target: Vector2 = game.active_note_screen_point()
		touch(target, true)
		await wait_frames(2)
		touch(target, false)
		await wait_frames(3)
		if note_id < 6:
			check("intentional note %d scores exactly once" % note_id, m.game == "melody" and game.progress_count() == note_id + 1 and game.active_note_id() == note_id + 1)
		else:
			print("R126_COMPLETION_FACTS|game=", m.game, "|local_friend=", friend, "|route_slot=", m.friends[3], "|trophies=", m.trophies)
			check("seventh intentional note completes original Daddy route", m.game == "" and bool(friend.get("won", false)))
			check("completed token layer synchronously retired", game.active_layer() == null)

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
	var result := {"status": "PASS" if failed == 0 else "FAIL", "lane": lane, "checks": checks, "captures": frames, "formal_QA11": null, "device": null, "child": null, "owner": null, "configured_route_only": true, "source_pin_sha256": OS.get_environment("R126_PIN_SHA256")}
	var file := FileAccess.open(out.path_join("RESULT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t"))
	file.close()
	print("R126|END|", lane, "|checks=", checks.size(), "|bad=", failed)
	quit(0 if failed == 0 else 1)
