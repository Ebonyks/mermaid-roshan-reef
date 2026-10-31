extends SceneTree
var main: ReefMain
const OUT := "res://assets_src/review/fashion_runtime_20261007/"
func _initialize() -> void:
	call_deferred("_run")
func shot(id: String) -> void:
	for index: int in range(4):
		await process_frame
	await RenderingServer.frame_post_draw
	var pixels: Image = root.get_texture().get_image()
	pixels.save_png(OUT + id + ".png")
	print("FASHION_CAPTURE|", id)
func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1280, 720)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.set_process(false)
	main.game = "level2"
	main.g["phase"] = "hall"
	main._castle_rooms_ref().open("bedroom")
	main._castle_rooms_ref().show_room("bedroom", false)
	var wardrobe := FashionWardrobe.new(main)
	wardrobe.open()
	await shot("01-wardrobe-1280x720")
	wardrobe._select_person("rumi")
	await shot("02-rumi-1280x720")
	wardrobe._select_person("roshan")
	wardrobe._page(1)
	await shot("03-locked-source-1280x720")
	main.chapter2_active = true
	main.chapter2_party_piece_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
	main.chapter2_rainbow_candle_found = true
	FashionDesigner.grant(main, FashionDesigner.PARTY_DRESS)
	FashionDesigner.refresh_unlocks(main)
	wardrobe.open(true)
	await shot("04-before-party-1280x720")
	FashionDesigner.equip(main, "roshan", FashionDesigner.PARTY_DRESS, true)
	wardrobe.open(true)
	await shot("05-dress-equipped-1280x720")
	main._wardrobe_ref()._close_wardrobe()
	await shot("06-dress-in-castle-1280x720")
	main.chapter2_story_complete = true
	FashionDesigner.grant(main, "roshan_garden_v1")
	wardrobe.open()
	wardrobe._start_practice()
	await shot("07-disguise-role-1280x720")
	wardrobe._pick("roshan_garden_v1")
	await shot("08-disguise-blend-1280x720")
	wardrobe._pick("roshan_garden_v1")
	await shot("09-disguise-bow-1280x720")
	main._wardrobe_ref()._close_wardrobe()
	root.size = Vector2i(1920, 900)
	await process_frame
	wardrobe.open()
	await shot("10-wide-phone-1920x900")
	main._wardrobe_ref()._close_wardrobe()
	main.queue_free()
	await process_frame
	quit()
