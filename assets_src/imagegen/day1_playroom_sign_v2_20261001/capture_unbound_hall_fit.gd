extends SceneTree
## Unbound static navigation-art fit; actual production hall, isolated save.
## Candidate replaces only this diagnostic Sprite2D texture, never runtime source.
var main: ReefMain
var records: Array[Dictionary] = []
const OUT := "res://assets_src/imagegen/day1_playroom_sign_v2_20261001/native_hall_fit_v1/"
const ORIGINAL := "res://assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_playroom.png"
const CANDIDATE := "res://assets_src/imagegen/day1_playroom_sign_v2_20261001/attempt_02_whole_canvas_256.png"
func _initialize() -> void:
	_run.call_deferred()
func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame
func _run() -> void:
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _frames(3)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await _frames(3)
	for movie_id: String in DayOneStoryClips.clip_ids():
		main.day_one_story_clips_seen[movie_id] = true
	main._day_one_cancel_story_clips()
	main.pearl_count = 10
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("main_hall", false)
	await _frames(12)
	main.set_process(false)
	rooms._cancel_player_motion()
	rooms._position_hall_player_at_foot(Vector2(2015, 620), false)
	rooms._hall_view_left_art = 735.0
	main.castle_room_world_root.position = Vector2(-735.0 * CastleRooms25D.HALL_STAGE_SCALE, 0.0)
	rooms._sync_hall_horizontal_culling()
	var sign: Sprite2D = main.castle_room_mid_layer.get_node("HallDoorSign_playroom") as Sprite2D
	assert(sign != null and sign.texture.resource_path == ORIGINAL)
	var original: Texture2D = sign.texture
	var candidate: Texture2D = ImageTexture.create_from_image(Image.load_from_file(CANDIDATE))
	assert(candidate.get_size() == original.get_size())
	for width: int in [1280,1600]:
		root.size = Vector2i(width,720)
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(root.size)
		await _frames(8)
		for entry: Dictionary in [{"name":"original","texture":original,"source":ORIGINAL},{"name":"candidate","texture":candidate,"source":CANDIDATE}]:
			sign.texture = entry["texture"] as Texture2D
			await _frames(3)
			await RenderingServer.frame_post_draw
			var image: Image = root.get_texture().get_image()
			var name: String = "%d_%s.webp" % [width, entry["name"]]
			assert(image.save_webp(OUT+name, true) == OK)
			var bounds: Rect2 = sign.get_global_transform_with_canvas()*sign.get_rect()
			records.append({"path":name,"sha256":FileAccess.get_sha256(OUT+name),"viewport":[image.get_width(),image.get_height()],"source":entry["source"],"source_sha256":FileAccess.get_sha256(entry["source"]),"sign_canvas_bounds":[bounds.position.x,bounds.position.y,bounds.size.x,bounds.size.y],"z_index":sign.z_index,"sign_visible":sign.is_visible_in_tree(),"qualification":"Exact production sign node/scale/parent/depth; direct centered-hall fixture, only candidate texture overridden. No route, interaction, owner or device acceptance."})
	sign.texture = original
	var file: FileAccess = FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"FOUR_UNBOUND_STATIC_HALL_VIEWS","views":records,"original_restored":sign.texture.resource_path==ORIGINAL},"\t")+"\n")
	file.close()
	print("PLAYROOM_SIGN_NATIVE_FIT|PASS four retained original/candidate full-canvas views")
	main.queue_free()
	await _frames(3)
	quit(0)
