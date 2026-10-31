extends SceneTree
var main: ReefMain
var venue: OperaHouseVenue2D
const OUT := "res://assets_src/review/tree_book_test_20260930/"
func _init() -> void:
	call_deferred("_run")
func shot(name: String) -> void:
	for frame: int in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+name+".png")
func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size = Vector2i(1280,720)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	main._castle_rooms_ref().open("opera_hall")
	main._castle_rooms_ref().show_room("opera_hall", false)
	main._castle_career_routes_ref().open_opera_venue()
	venue = main._castle_career_routes_ref().opera_venue
	await shot("foyer")
	venue.open_tree_book()
	var level: OperaTreeBookTest = venue.tree_book_test
	level.set_process(false)
	for step: int in range(6):
		level.restore_progress({"version":1,"patient":"orange_spots","stage":step})
		if step == 4:
			level._touch(1,true,OperaTreeBookTest.LEAF_RECT.get_center())
			level.advance(0.1)
		await shot("page_%d" % step)
	for viewport_size: Vector2i in [Vector2i(1600,900),Vector2i(1920,900)]:
		main._castle_rooms_ref().close()
		root.size = viewport_size
		await process_frame
		main._castle_rooms_ref().open("opera_hall")
		main._castle_career_routes_ref().open_opera_venue()
		venue = main._castle_career_routes_ref().opera_venue
		venue.open_tree_book()
		venue.tree_book_test.restore_progress({"version":1,"patient":"orange_spots","stage":5})
		await shot("wide_1600x900" if viewport_size.x == 1600 else "phone_1920x900")
	venue.close()
	main.queue_free()
	await process_frame
	quit()
