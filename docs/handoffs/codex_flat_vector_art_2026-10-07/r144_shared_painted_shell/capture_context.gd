extends SceneTree
var main: ReefMain
var dest: String
var records: Array[Dictionary] = []
func _initialize() -> void:
	call_deferred("_run")
func _run() -> void:
	dest = OS.get_environment("R144_CAPTURE_OUT")
	assert(not dest.is_empty() and not DirAccess.dir_exists_absolute(dest))
	DirAccess.make_dir_recursive_absolute(dest)
	assert(str(Engine.get_version_info().get("hash")) == "ed1daf0bf001b61586d9930840f2f1394092c079")
	assert(RenderingServer.get_current_rendering_method() == "mobile" and DisplayServer.get_name() == "Windows")
	Engine.max_fps = 30
	DisplayServer.window_set_position(Vector2i(-2400, 0))
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_EXPAND
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	seed(20261106)
	main = load("res://scenes/main.tscn").instantiate() as ReefMain
	root.add_child(main)
	await create_timer(3.0).timeout
	main.set_process(false)
	main.set_physics_process(false)
	main._apply_quality("speedy")
	assert(main.quality == "speedy")
	await shot("start-menu")
	main._start_menu_ref()._toggle_options()
	await shot("start-options")
	main._start_menu_ref()._close_options()
	# In-memory fixture only: expose the existing save-protection sheet without
	# loading or deleting a child save. Never press or release its reset action.
	main.has_saved_game = true
	main._start_menu_ref()._request_new_game()
	await shot("start-keep-game")
	main._start_menu_ref()._cancel_new_game()
	main._start_menu_ref()._dismiss_menu()
	await process_frame
	main.day_one_active = false
	main._build_intro()
	await shot("legacy-intro")
	main.intro_layer.queue_free()
	main.intro_layer = null
	main.intro_active = false
	await process_frame
	main.pause_panel.visible = true
	await shot("pause")
	main.pause_panel.visible = false
	main._open_craft_studio()
	await shot("craft")
	main._close_craft()
	main._open_castle_logo()
	await shot("castle-logo")
	main._close_castle_logo()
	main._open_wardrobe()
	await shot("wardrobe")
	main._close_wardrobe()
	main._open_stickers()
	await shot("stickers")
	main._close_stickers()
	main.companion_id = "mewsha"
	main._companion_ref().open_care_menu()
	await shot("stuffie-care")
	main._companion_ref().close_care_menu()
	# Build the actual microphone sheet without arming capture or enrollment.
	main._mic_ref()._build_teach_layer()
	await shot("mic-teach-sheet-unarmed")
	main.mic_teach_layer.queue_free()
	main.mic_teach_layer = null
	main._mg2d_open("garden")
	await shot("picture-garden")
	main._mg2d_close()
	var developer := load("res://scripts/dev_mode.gd").new() as CanvasLayer
	main.add_child(developer)
	developer.visible = true
	await shot("developer-parent-panel")
	developer.queue_free()
	# The old touch hint is deliberately hidden in production. Census it as
	# hidden; never show it to manufacture an art-removal claim.
	var hint := main.touch_ui.get("_stick_hint") as Control
	assert(hint != null and not hint.visible)
	records.append({"id":"retired-touch-pad", "capture":false, "visible":false, "classification":"hidden compatibility UI; no accepted removal"})
	# Same real menu at an expand/aspect edge, no synthetic ornament gallery.
	main._build_start_menu()
	root.size = Vector2i(1280, 800)
	await shot("start-menu-16x10")
	root.size = Vector2i(1600, 900)
	await shot("start-menu-1600x900")
	var file := FileAccess.open(dest.path_join("captures.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(records, "\t") + "\n")
	print("R144_CAPTURE|DONE|", records.size())
	quit()
func shot(id: String) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var name := id + ".png"
	var error := image.save_png(dest.path_join(name))
	assert(error == OK)
	var shells: Array[Dictionary] = []
	for node: Node in main.find_children("*", "Control", true, false):
		if not node is ShellOrnament:
			continue
		var crest := node as Control
		shells.append({"name":str(crest.name), "visible":crest.is_visible_in_tree(),
			"rect":str(crest.get_global_rect()),"size":str(crest.size),
			"mouse_filter":crest.mouse_filter,"z_index":crest.z_index})
	records.append({"id":id,"file":name,"sha256":FileAccess.get_sha256(dest.path_join(name)),
		"source_sha256":OS.get_environment("R144_SOURCE_SHA256"),"width":image.get_width(),"height":image.get_height(),
		"shells":shells,"profile":{"version":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),
		"quality":main.quality,"stretch":"canvas_items/expand","display":DisplayServer.get_name()},
		"formal_QA11":null,"device":null,"child":null,"owner":null})
	print("R144_CAPTURE|",id,"|",shells.size())
