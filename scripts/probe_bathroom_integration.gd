extends SceneTree
# Focused live-world audit for the Bubble Bath room. The room is a layered
# Sprite3D stage: tub, sink, and toilet are separate world cards with projected
# touch targets, animations, and sounds. No modeled bathroom may be rebuilt.

var main: ReefMain
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("BATHROOM_WORLD|", label, ": ", ("OK" if ok else "FAIL"),
		(" " + detail if detail != "" else ""))

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _shot() -> void:
	if DisplayServer.get_name() == "headless":
		return
	await _frames(3)
	await RenderingServer.frame_post_draw
	var output_dir := ProjectSettings.globalize_path(
		"res://audit/castle_sprite3d")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var output_path := output_dir.path_join("bubble_bath.png")
	var save_error: Error = root.get_viewport().get_texture().get_image() \
		.save_png(output_path)
	print("BATHROOM_WORLD|shot saved: ", output_path,
		" error=", save_error)

func _run() -> void:
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(16)

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("bubble_bath", false)
	await _frames(3)
	_ck("sprite stage open", rooms.is_open())
	_ck("perspective camera",
		main.castle_room_camera != null
		and main.castle_room_camera.projection
			== Camera3D.PROJECTION_PERSPECTIVE)
	_ck("retired modeled bathroom absent",
		not main.g.has("toilet")
		and main.game_nodes.is_empty()
		and main.arena_solids.is_empty()
		and main.arena_zones.is_empty())
	_ck("three separate touch props",
		main.castle_room_item_sprites.size() == 3
		and main.castle_room_reaction_hotspots.size() == 2
		and main.castle_room_item_hotspot_layer.get_child_count() == 5)

	var props_ok := true
	var depth_ok := true
	var interaction_ok := true
	for prop_id: String in ["bathtub", "sink", "toilet"]:
		var record: Dictionary = main.castle_room_item_sprites.get(prop_id, {})
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		var hotspot: Button = record.get("hotspot") as Button
		props_ok = props_ok and sprite != null and not sprite.shaded \
			and hotspot != null and hotspot.size.x >= 112.0 \
			and hotspot.size.y >= 112.0
		depth_ok = depth_ok and sprite != null \
			and sprite.position.z > main.castle_room_background.position.z \
			and sprite.position.z < CastleRooms25D.FOREGROUND_Z
		if sprite != null:
			rooms._activate_room_item(prop_id)
			await process_frame
			interaction_ok = interaction_ok \
				and bool(sprite.get_meta("busy", false)) \
				and main.castle_room_prop_sfx.stream != null
			await _frames(8)
	_ck("unshaded Sprite3D fixtures", props_ok)
	_ck("fixtures occupy real depth", depth_ok)
	_ck("touch animations and sound", interaction_ok)
	_ck("foreground occluders",
		main.castle_room_front_layer.get_child_count() == 2
		and (main.castle_room_front_layer.get_child(0) as Sprite3D).position.z
			> main.castle_room_player_sprite.position.z)
	_ck("free-roaming controls disabled",
		not main.touch_ui.world_controls_enabled
		and not main.player.visible
		and main.touch_interactables.is_empty())

	await _shot()
	print("BATHROOM_WORLD|RESULT: ", checks_failed,
		(" FAIL" if checks_failed > 0 else " OK"))
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
