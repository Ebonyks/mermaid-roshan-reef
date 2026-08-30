extends SceneTree
## Exact-4.7.2 Mobile evidence for the new Stuffie tidy beat and staged rescue.

var failures := 0
var capture_root := ""


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("STUFFIE_TRANSITION_V2|%s: %s%s" % [label,
		"OK" if ok else "FAIL", (" (%s)" % detail) if detail != "" else ""])


func _capture(name: String) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path: String = capture_root.path_join(name + ".png")
	var error: Error = image.save_png(path)
	_check("capture " + name, not image.is_empty()
		and image.get_size() == Vector2i(1280, 720) and error == OK, path)


func _run() -> void:
	root.size = Vector2i(1280, 720)
	await _frames(4)
	capture_root = OS.get_environment("DAY_ONE_STUFFIE_V2_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path("user://stuffie_transition_v2")
	_check("capture directory",
		DirAccess.make_dir_recursive_absolute(capture_root) == OK, capture_root)
	_check("Mobile renderer", RenderingServer.get_current_rendering_method()
		== "mobile", RenderingServer.get_current_rendering_method())
	_check("non-headless capture", DisplayServer.get_name() != "headless",
		DisplayServer.get_name())

	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	root.add_child(main)
	await _frames(3)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await _frames(3)
	main._day_one_ref().restore_state({
		"day_one_active": true,
		"day_one_completed_rooms": ["bathroom", "pool"],
		"day_one_room_polish_completed": {},
	})
	main.stuffie_wins = {}
	main.save_data["stuffie_wins"] = {}
	main.g.erase("castle_dust_bunnies_cleared")
	main.companion_id = ""
	main.pearl_count = 10
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("playroom", false)
	await _frames(12)

	var polish: DayOneRoomPolish = main._day_one_room_polish
	var polish_snapshot: Dictionary = polish.audit_snapshot() if polish != null else {}
	var polish_hit_size: Vector2 = polish_snapshot.get(
		"target_hit_size", Vector2.ZERO) as Vector2
	_check("purpose-built loose stuffing is the only first target",
		polish != null and String(polish_snapshot.get("task_id", ""))
		== "loose_stuffing" and bool(polish_snapshot.get("pointer_visible", false))
		and polish_hit_size == Vector2(290.0, 175.0))
	var dirty_display: Control = main.castle_logo_room_display
	var dirty_banner_nodes: Array = dirty_display.get_meta(
		"banner_nodes", []) as Array if dirty_display != null else []
	var dirty_cover_nodes: Array = dirty_display.get_meta(
		"dirty_cover_nodes", []) as Array if dirty_display != null else []
	_check("dirty Stuffie hides both room banners behind authored wall patches",
		dirty_display != null and dirty_banner_nodes.is_empty()
		and dirty_cover_nodes.size() == 2
		and String(dirty_display.get_meta("banner_visibility_state", ""))
		== "hidden_until_settled_clean")
	await _capture("00_dirty_no_banners_hanging_bunny_pending")
	_check("one tap saves the new tidy beat", polish != null
		and polish.probe_complete())
	await create_timer(1.35).timeout
	_check("tidy beat is immediately durable",
		main.day_one_room_polish_is_complete("stuffie")
		and bool((main.save_data.get("day_one_room_polish_completed", {})
			as Dictionary).get("stuffie", false)))

	var left_record: Dictionary = main.castle_room_item_sprites.get(
		"eagle_pin_left", {}) as Dictionary
	var right_record: Dictionary = main.castle_room_item_sprites.get(
		"eagle_pin_right", {}) as Dictionary
	var ceiling_record: Dictionary = main.castle_room_item_sprites.get(
		"ceiling_bunny", {}) as Dictionary
	var eagle_record: Dictionary = main.castle_room_item_sprites.get(
		"baby_eagle_rescue", {}) as Dictionary
	var left: Sprite2D = left_record.get("sprite") as Sprite2D
	var right: Sprite2D = right_record.get("sprite") as Sprite2D
	var ceiling: Sprite2D = ceiling_record.get("sprite") as Sprite2D
	var eagle: Sprite2D = eagle_record.get("sprite") as Sprite2D
	var pointer: Sprite2D = main.castle_room_item_effect_layer.get_node_or_null(
		"BabyEagleRescuePointer") as Sprite2D
	var entry_foot: Vector2 = main.castle_room_player_sprite.get_meta(
		"stage_foot", Vector2.ZERO) as Vector2
	_check("purpose-built pinned Eagle is live",
		eagle != null and eagle.texture != null and eagle.texture.resource_path
		== "res://assets/castle/day_one_stuffie/baby_eagle_pinned.png")
	_check("Roshan is clear left and hanging bunny owns the first pointer",
		entry_foot.x <= 360.0 and left != null and right != null
		and ceiling != null
		and pointer != null and pointer.visible
		and String(pointer.get_meta("active_target_id", "")) == "ceiling_bunny"
		and bool(ceiling.get_meta("playroom_rescue_active_target", false))
		and not bool(left.get_meta("playroom_rescue_active_target", true))
		and not bool(right.get_meta("playroom_rescue_active_target", true)))
	_check("hanging bunny uses approved art and a 2D cord",
		ceiling.texture != null and ceiling.texture.resource_path
		== "res://assets/castle/dirty_cleanup_2d/critters/"
		+ "dust_bunnies/dust_bunny_hop.png"
		and ceiling_record.get("hanging_cord") is Line2D)
	_check("entry voice and pointer identify the high target",
		String(pointer.get_meta("announced_target_id", "")) == "ceiling_bunny")
	await _capture("01_dirty_hanging_bunny_target")

	rooms._explode_dust_bunny("eagle_pin_left")
	_check("inactive pin cannot skip the ceiling target",
		main.castle_room_item_sprites.has("eagle_pin_left")
		and not bool(main.stuffie_wins.get("rescued_eagle_pin_left", false)))
	rooms._activate_room_item("ceiling_bunny")
	await _frames(3)
	pointer = main.castle_room_item_effect_layer.get_node_or_null(
		"BabyEagleRescuePointer") as Sprite2D
	_check("ceiling bunny saves immediately and advances to left pin",
		bool(main.stuffie_wins.get("rescued_ceiling_bunny", false))
		and bool((main.save_data.get("stuffie_wins", {}) as Dictionary).get(
			"rescued_ceiling_bunny", false))
		and pointer != null and String(pointer.get_meta(
			"active_target_id", "")) == "eagle_pin_left")
	await _capture("02_hanging_bunny_resolved")
	rooms._walk_cutout_to(left.position)
	await _frames(12)
	pointer = main.castle_room_item_effect_layer.get_node_or_null(
		"BabyEagleRescuePointer") as Sprite2D
	_check("first beat saves and advances pointer",
		bool(main.stuffie_wins.get("rescued_eagle_pin_left", false))
		and not bool(main.stuffie_wins.get("rescued_eagle", false))
		and pointer != null and String(pointer.get_meta(
			"active_target_id", "")) == "eagle_pin_right")
	_check("Eagle visibly responds after first beat", eagle.position.y
		< (eagle.get_meta("playroom_rescue_rest_position", eagle.position)
			as Vector2).y)
	await _capture("03_first_pin_response")

	rooms._walk_cutout_to(right.position)
	await _frames(34)
	_check("second beat saves rescue monotonically",
		bool(main.stuffie_wins.get("rescued_eagle", false))
		and bool((main.save_data.get("stuffie_wins", {}) as Dictionary).get(
			"rescued_eagle", false)))
	_check("standing sprite is used for the payoff", eagle != null
		and String(eagle.get_meta("rescue_pose", "")) == "standing_idle"
		and eagle.texture != null and eagle.texture.resource_path
		== "res://assets/castle/day_one_stuffie/baby_eagle_standing_idle.png")
	await _capture("04_purpose_built_eagle_rescue")
	await create_timer(0.84).timeout
	var dressing_snapshot: Dictionary = main.day_one_castle_dressing.audit_snapshot()
	_check("playroom settles into a bright clean environment before adoption",
		float(dressing_snapshot.get("visible_dirty_strength", 1.0)) <= 0.05)
	var clean_display: Control = main.castle_logo_room_display
	var clean_banner_nodes: Array = clean_display.get_meta(
		"banner_nodes", []) as Array if clean_display != null else []
	var clean_cover_nodes: Array = clean_display.get_meta(
		"dirty_cover_nodes", []) as Array if clean_display != null else []
	_check("settled clean restores both banners exactly once",
		clean_display != null and clean_banner_nodes.size() == 2
		and clean_cover_nodes.is_empty()
		and String(clean_display.get_meta("banner_visibility_state", ""))
		== "settled_clean")
	await _capture("05_settled_clean_banners_restored")
	await create_timer(0.60).timeout
	_check("focused adoption tutorial follows rescue",
		main.companion_layer != null and main.companion_pick_id == "eagle"
		and main.companion_stage.find_children(
			"StuffieCard_*", "Button", true, false).size() == 1)
	var rescue_previews: Array[Node] = main.companion_stage.find_children(
		"RescueEaglePreview", "Sprite2D", true, false)
	_check("adoption preview preserves the rescued Eagle identity",
		rescue_previews.size() == 2)
	for preview_node: Node in rescue_previews:
		var preview := preview_node as Sprite2D
		var preview_box: Vector2 = preview.get_meta(
			"preview_box_size", Vector2.ZERO) as Vector2
		var visible_size: Vector2 = preview.texture.get_size() \
			* preview.scale.abs() if preview.texture != null else Vector2.ZERO
		_check("rescue Eagle preview uses exact standing texture",
			preview.texture != null and preview.texture.resource_path
			== "res://assets/castle/day_one_stuffie/"
			+ "baby_eagle_standing_idle.png")
		_check("full rescue Eagle silhouette contain-fits its preview box",
			bool(preview.get_meta("contain_fit", false))
			and visible_size.x <= preview_box.x + 0.5
			and visible_size.y <= preview_box.y + 0.5
			and visible_size.x >= preview_box.x * 0.34
			and visible_size.y >= preview_box.y * 0.74,
			"visible=%s box=%s" % [visible_size, preview_box])
	_check("rescue adoption focuses the one take-along action",
		int(main.g.get("stuffie_rescue_tutorial_step", -1)) == 2
		and main.companion_stage.find_children(
			"StuffieSwatch_*", "Button", true, false).is_empty())
	await _capture("06_focused_adoption_tutorial")

	main.queue_free()
	await _frames(4)
	print("STUFFIE_TRANSITION_V2|RESULT: %s failures=%d output=%s" % [
		"PASS" if failures == 0 else "FAIL", failures, capture_root])
	quit(1 if failures > 0 else 0)
