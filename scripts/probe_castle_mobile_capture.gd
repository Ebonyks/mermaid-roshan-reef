extends SceneTree

# Non-headless Mobile-renderer evidence for the true-2D castle. This probe is
# deliberately visual: it captures every composed room, both ends of the wide
# hall, the fastest hall traversal, the sconce lighting states, and active
# fixture water. Output is review evidence under an explicit environment path,
# never runtime art.

const ROOM_IDS: Array[String] = [
	"main_hall",
	"opera_hall",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
	"kitchen",
	"family_gallery",
	"dining_room",
	"royal_bedroom",
	"sleepover_bedroom",
	"movie_lounge",
]

var failures := 0
var capture_root := ""


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("CASTLE_MOBILE|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		(" (%s)" % detail) if detail != "" else ""])


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(name: String) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var path := capture_root.path_join(name + ".png")
	var save_error: Error = image.save_png(path)
	_check("capture %s" % name,
		not image.is_empty() and save_error == OK,
		"size=%s error=%s path=%s" % [image.get_size(), save_error, path])


func _hall_source_crops_are_exact_and_non_overlapping(main: Node) -> bool:
	var tiles: Array = main.get("castle_room_background_tiles") as Array
	if tiles.size() != 16:
		return false
	for index: int in range(tiles.size()):
		var value: Variant = tiles[index]
		var tile: Sprite2D = value as Sprite2D
		if tile == null:
			return false
		var row: int = index / 8
		var column: int = index % 8
		var expected_master_x := float(column) * 910.0
		var source_rect: Rect2 = tile.get_meta(
			"source_art_rect", Rect2()) as Rect2
		var master_rect: Rect2 = tile.get_meta(
			"source_master_rect", Rect2()) as Rect2
		var native_size: Vector2 = tile.get_meta(
			"native_texture_size", Vector2.ZERO) as Vector2
		var native_to_logical: Vector2 = tile.get_meta(
			"native_to_logical_scale", Vector2.ZERO) as Vector2
		if not source_rect.has_area() or not master_rect.has_area() \
			or native_size != Vector2(910.0, 1024.0) \
				or master_rect.position != Vector2(expected_master_x,
					float(row) * 1024.0) \
				or master_rect.size != native_size \
				or source_rect.position != Vector2(
					expected_master_x * native_to_logical.x,
					float(row) * 1024.0 * native_to_logical.y) \
				or source_rect.size != native_size * native_to_logical \
				or tile.get_meta("runtime_seam_bleed_pixels", Vector2i(-1, -1)) \
						!= Vector2i.ZERO:
			return false
	return true


func _hall_has_no_legacy_front_cards(main: Node) -> bool:
	var front_layer: Node2D = main.get("castle_room_front_layer") as Node2D
	if front_layer == null:
		return false
	for child: Node in front_layer.get_children():
		if child is Sprite2D and String(child.get_meta("source_texture", "")) \
				in ["room_main_hall_front_left.png", "room_main_hall_front_right.png"]:
			return false
	return front_layer.get_child_count() == 0


func _hall_tiles_have_unmodified_canvas_state(main: Node) -> bool:
	var tiles: Array = main.get("castle_room_background_tiles") as Array
	if tiles.size() != 16:
		return false
	for value: Variant in tiles:
		var tile: Sprite2D = value as Sprite2D
		if tile == null or tile.texture == null \
		or Vector2i(tile.texture.get_size()) != Vector2i(910, 1024) \
				or tile.modulate != Color.WHITE \
				or tile.self_modulate != Color.WHITE \
				or tile.material != null \
				or tile.texture_filter != 0:
			return false
	return true


func _run() -> void:
	_check("real Mobile viewport is available",
		DisplayServer.get_name() != "headless", DisplayServer.get_name())
	if failures > 0:
		quit(1)
		return
	capture_root = OS.get_environment("CASTLE_CAPTURE_OUT")
	if capture_root == "":
		capture_root = ProjectSettings.globalize_path(
			"user://castle_mobile_capture")
	var dir_error: Error = DirAccess.make_dir_recursive_absolute(capture_root)
	_check("capture directory is ready", dir_error == OK, capture_root)

	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: Node = scene.instantiate()
	root.add_child(main)
	await _frames(2)
	if main.has_method("_skip_intro"):
		main.call("_skip_intro")
	await _frames(2)
	main.set("pearl_count", 10)
	for friend_value: Variant in main.get("friends") as Array:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.set("trophies", 5)
	main.set("level2_done_once", true)
	main.call("_enter_level2_now", true, false, false)
	await _frames(12)
	main.call("_enter_castle_interior_now", false)
	await _frames(18)
	var rooms: RefCounted = main.call("_castle_rooms_ref") as RefCounted
	_check("castle room controller opened", rooms != null)
	if rooms == null:
		quit(1)
		return
	_check("main hall source crops stay exact and non-overlapping",
		_hall_source_crops_are_exact_and_non_overlapping(main))
	rooms.call("show_room", "main_hall", false)
	await _frames(8)
	_check("main hall does not compose legacy front cards",
		_hall_has_no_legacy_front_cards(main))
	_check("main hall tiles have unmodified Canvas state",
		_hall_tiles_have_unmodified_canvas_state(main))
	for room_id: String in ROOM_IDS:
		rooms.call("show_room", room_id, false)
		await _frames(8)
		await _capture("rest_" + room_id)

	# Capture a live authored V4 sconce at stable action/rest states rather than
	# the retired Main Hall V2 sconces now baked into that panorama. This exposes
	# Canvas bloom washout and frame readability on an actual runtime fixture.
	rooms.call("show_room", "opera_hall", false)
	await _frames(8)
	var opera_items: Dictionary = main.get(
		"castle_room_item_sprites") as Dictionary
	var sconce_record: Dictionary = opera_items.get(
		"pearl_sconce_left", {}) as Dictionary
	var sconce_sprite: Sprite2D = sconce_record.get("sprite") as Sprite2D
	_check("sconce capture target is registered",
		sconce_sprite != null and is_instance_valid(sconce_sprite),
		"keys=%s" % [opera_items.keys()])
	await _capture("opera_hall_sconce_rest")
	rooms.call("_activate_room_item", "pearl_sconce_left")
	await _frames(4)
	await _capture("opera_hall_sconce_active")
	await _frames(70)
	await _capture("opera_hall_sconce_restored")

	# Move at the controller's maximum child-friendly duration. Four samples plus
	# the two end states make panorama culling/draw-in review reproducible.
	rooms.call("show_room", "main_hall", false)
	await _frames(8)
	rooms.call("_position_hall_player_at_foot", Vector2(380.0, 835.0), false)
	await _frames(24)
	await _capture("hall_traverse_00_left")
	rooms.call("_position_hall_player_at_foot", Vector2(2960.0, 835.0), true)
	for sample_index: int in range(1, 5):
		await _frames(16)
		await _capture("hall_traverse_%02d" % sample_index)
	await _frames(24)
	await _capture("hall_traverse_05_right")

	# The bathtub combines an authored atlas action, analytic spring motion, and
	# bounded Canvas water, so one mid-action frame covers the highest-risk
	# shader/animation integration without manufacturing test-only visuals.
	rooms.call("show_room", "bubble_bath", false)
	await _frames(8)
	var bath_items: Dictionary = main.get("castle_room_item_sprites") as Dictionary
	var bath_record: Dictionary = bath_items.get("bathtub", {}) as Dictionary
	var bath_rig: Dictionary = bath_record.get("fixture_rig", {}) as Dictionary
	var bath_water: Array = bath_rig.get("water", []) as Array
	var bath_roles := PackedStringArray()
	var bath_alpha := 1.0
	for water_value: Variant in bath_water:
		var water_record: Dictionary = water_value as Dictionary
		bath_roles.append(String(water_record.get("role", "")))
		if String(water_record.get("role", "")) == "fill":
			var bath_material: ShaderMaterial = water_record.get(
				"material") as ShaderMaterial
			if bath_material != null:
				bath_alpha = float(bath_material.get_shader_parameter("alpha_base"))
	_check("bathtub water remains one soft basin layer before action",
		bath_water.size() == 1 and bath_roles.has("fill")
		and not bath_roles.has("stream") and bath_alpha <= 0.24,
		"roles=%s alpha=%.3f" % [bath_roles, bath_alpha])
	rooms.call("_activate_room_item", "bathtub")
	await _frames(18)
	await _capture("bubble_bath_bathtub_active_early")
	await _frames(18)
	await _capture("bubble_bath_bathtub_active_late")

	main.queue_free()
	await _frames(5)
	print("CASTLE_MOBILE|done failures=%d output=%s" % [
		failures, capture_root])
	quit(1 if failures > 0 else 0)


func _init() -> void:
	call_deferred("_run")
