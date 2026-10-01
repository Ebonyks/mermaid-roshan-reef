extends SceneTree
## Unbound diagnostic pose/hand/tool fits, not production action captures.
## Approved complete atlas cells remain unchanged. No gameplay progress awarded.

var output: String
var rows: Array[Dictionary] = []
const CANDIDATES := [
	{"sheet": "play_a", "index": 8, "hand": Vector2(179, 140), "rotation": 0.35},
	{"sheet": "play_a", "index": 9, "hand": Vector2(192, 128), "rotation": 0.31},
]

func _initialize() -> void:
	_run.call_deferred()

func _run() -> void:
	output = OS.get_environment("POOL_REUSE_CAPTURE_OUT")
	assert(output != "")
	assert(DirAccess.make_dir_recursive_absolute(output) == OK)
	var main: ReefMain = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
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
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	root.size = Vector2i(1280, 720)
	DisplayServer.window_set_size(root.size)
	await _frames(6)
	main._day_one_ref().restore_state({"day_one_active": true,
		"day_one_completed_rooms": ["bathroom"], "day_one_pool_cleanup_step": 0,
		"day_one_pool_skimmer_mask": 0, "day_one_pool_waterfall_mask": 0,
		"day_one_pool_seahorse_tugs": 0})
	main.skin_id = "classic"
	main._apply_skin()
	main.pearl_count = 10
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)
	main._castle_rooms_ref().show_room("mermaid_pool", false)
	await _frames(12)
	var cleanup: DayOnePoolCleanup = main._castle_rooms_ref().day_one_pool_cleanup
	assert(is_instance_valid(cleanup))
	var skimmer: PoolSkimmerActivity = cleanup.skimmer_activity
	skimmer.set_process(false)
	skimmer._running = false
	skimmer._fit_sprite(skimmer._skimmer, Vector2(150, 150))
	skimmer._demo_pointer.hide()
	main.castle_voice_caption.text = "Approved pose study: tool fit only; no game action or progress"
	for candidate: Dictionary in CANDIDATES:
		var source: String = "res://assets/characters/roshan_25d/roshan_%s.png" % candidate["sheet"]
		var atlas: AtlasTexture = AtlasTexture.new()
		atlas.atlas = load(source) as Texture2D
		var index: int = int(candidate["index"])
		atlas.region = Rect2(float(index % 4) * 256.0, float(index / 4) * 256.0, 256.0, 256.0)
		skimmer._roshan.texture = atlas
		skimmer._roshan.flip_h = true
		skimmer._roshan.z_index = 1
		skimmer._skimmer.z_index = 0
		skimmer._skimmer.rotation = float(candidate["rotation"])
		var hand: Vector2 = candidate["hand"] as Vector2
		skimmer._hand_offset = (hand - Vector2(128, 128)) * skimmer._roshan.scale
		skimmer._skimmer.position = skimmer._hand_offset - (
			PoolSkimmerActivity.HANDLE_PIXEL - skimmer._skimmer.texture.get_size() * 0.5
			).rotated(skimmer._skimmer.rotation) * skimmer._skimmer.scale
		skimmer._cleaner.position = Vector2(230, 435)
		skimmer._cleaner.rotation = 0.0
		skimmer._sync_net_position()
		await _frames(3)
		await _capture(candidate, "idle_clear", source, skimmer, main)
		var target: Vector2 = skimmer._trash_contact_position(0)
		skimmer._cleaner.position += target - skimmer._skimmer_position
		skimmer._sync_net_position()
		await _frames(3)
		await _capture(candidate, "contact_wrapper_fixture", source, skimmer, main)
		assert(main.day_one_pool_skimmer_mask == 0)
	var harness: String = (get_script() as Script).resource_path
	var receipt: Dictionary = {"status": "STATIC_DIAGNOSTIC_CAPTURE_NOT_ACTION_PASS",
		"engine": Engine.get_version_info(), "dimensions": [1280, 720],
		"harness": harness, "harness_sha256": FileAccess.get_sha256(harness), "views": rows,
		"qualification": "Explicit unbound fixture: complete approved pose cell horizontally flipped, declared sockets, existing whole skimmer rotated and positioned, tool behind complete actor card, tool uniformly fit150x150, initial anchor230435, wrapper contact positioned without an input or award. Actual pool source context otherwise reused. No production file, source art or protected original changed. No timed/wardrobe/ordinary-route/device/child/owner acceptance."}
	var file: FileAccess = FileAccess.open(output.path_join("CAPTURE_RECEIPT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(receipt, "\t") + "\n")
	file.close()
	main.queue_free()
	await _frames(4)
	print("POOL_ACTOR_REUSE|PASS|4 unbound shorter-tool views|no awards")
	quit(0)

func _capture(candidate: Dictionary, phase: String, source: String,
		skimmer: PoolSkimmerActivity, main: ReefMain) -> void:
	await RenderingServer.frame_post_draw
	var name: String = "%s_%02d_%s.webp" % [candidate["sheet"], int(candidate["index"]), phase]
	var path: String = output.path_join(name)
	assert(root.get_texture().get_image().save_webp(path, true, 1.0) == OK)
	var bounds: Rect2 = skimmer._roshan.get_global_transform_with_canvas() * skimmer._roshan.get_rect()
	assert(Rect2(Vector2.ZERO, Vector2(1280, 720)).encloses(bounds))
	rows.append({"actor_full_card_bounds": [bounds.position.x, bounds.position.y, bounds.size.x, bounds.size.y],
		"actor_full_card_inside_viewport": true, "path": name, "sha256": FileAccess.get_sha256(path), "phase": phase,
		"source": source, "source_sha256": FileAccess.get_sha256(source),
		"source_cell": int(candidate["index"]), "flip_h": true,
		"hand_canvas": [skimmer._hand_offset.x, skimmer._hand_offset.y],
		"tool_rotation": skimmer._skimmer.rotation, "socket_distance": skimmer._hand_grip_error(),
		"actor_position": [skimmer._cleaner.position.x, skimmer._cleaner.position.y],
		"progress_mask": main.day_one_pool_skimmer_mask})

func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame
