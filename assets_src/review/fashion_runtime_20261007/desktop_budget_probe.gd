extends SceneTree
var main: ReefMain
var results: Array[Dictionary] = []
func _initialize() -> void:
	call_deferred("_run")
func sample(label: String, operation_us: int = 0) -> void:
	for frame: int in range(8):
		await process_frame
	await RenderingServer.frame_post_draw
	results.append({"phase": label, "texture_bytes": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TEXTURE_MEM_USED),
		"raw_visible_draw_calls_counter": RenderingServer.viewport_get_render_info(root.get_viewport_rid(), RenderingServer.VIEWPORT_RENDER_INFO_TYPE_VISIBLE, RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME),
		"global_draw_calls_in_frame": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME),
		"operation_wall_microseconds": operation_us})
func _run() -> void:
	AudioServer.set_bus_mute(0, true)
	root.size = Vector2i(1280, 720)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.day_one_active = false
	main.set_process(false)
	main._apply_quality("speedy")
	main.game = "level2"
	main.g["phase"] = "hall"
	main._castle_rooms_ref().open("bedroom")
	main.chapter2_active = true
	main.chapter2_party_piece_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
	main.chapter2_rainbow_candle_found = true
	main.chapter2_farmer_strawberries_ready = true
	FashionDesigner.refresh_unlocks(main)
	await sample("castle_before_wardrobe")
	var wardrobe := FashionWardrobe.new(main)
	var started: int = Time.get_ticks_usec()
	wardrobe.open()
	await sample("wardrobe_first_page", Time.get_ticks_usec() - started)
	started = Time.get_ticks_usec()
	wardrobe._pick(FashionDesigner.PARTY_DRESS)
	await sample("special_dress_equipped", Time.get_ticks_usec() - started)
	started = Time.get_ticks_usec()
	wardrobe._page(1)
	await sample("second_outfit_page", Time.get_ticks_usec() - started)
	for id: String in ["rumi", "baby_eagle", "daddy_mermaid", "rainbow_dust_bunny"]:
		started = Time.get_ticks_usec()
		wardrobe._select_person(id)
		wardrobe._pick(id + "_ribbon_v1")
		await sample(id + "_equipped", Time.get_ticks_usec() - started)
	main._wardrobe_ref()._close_wardrobe()
	await sample("wardrobe_closed")
	var record: Dictionary = {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"gpu": RenderingServer.get_video_adapter_name(), "quality_tier": main.quality,
		"profile": "1280x720 desktop Mobile; isolated synthetic save; main game tick paused for repeatable UI/texture measurements. Not FPS, touchscreen, target-device or child acceptance.", "measurements": results}
	var file := FileAccess.open("res://assets_src/review/fashion_runtime_20261007/desktop_budget.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(record, "\t") + "\n")
	file.close()
	print("FASHION_DESKTOP_BUDGET|", JSON.stringify(record))
	main.queue_free()
	await process_frame
	quit()
