extends "res://scripts/probe_opera_art.gd"

func snap(label: String) -> void:
	await _settle(3)
	await RenderingServer.frame_post_draw
	get_root().get_texture().get_image().save_png("res://tmp/art-quality/" + label + ".png")
	print("GEOLOGYSHOT|", label)

func _run() -> void:
	await _set_aspect(Vector2i(1280, 720))
	if not await _start_runtime():
		quit(1)
		return
	main.save_data["opera_geology_checkpoint"] = {}
	var room_id := CastleCareerRoutes.room_for_act(16)
	if not await _prepare_career_route(room_id, 16):
		quit(2)
		return
	routes._launch(room_id, 16)
	if not await _wait_career_ready(16, room_id):
		quit(3)
		return
	var act: OperaAct = main.opera_game.act
	var world: OperaCareerWorld2D = act.career_world_2d
	act.set_process(false)
	world.set_process(false)
	for phase in range(4):
		main.save_data["opera_geology_checkpoint"] = {}
		world.phase_index = phase
		world._show_phase()
		world._process(3.0)
		var geo := world.surface as OperaGeologySurface
		geo.set_process(false)
		await snap("phase-%d-ready" % phase)
		match phase:
			0:
				geo._press(geo.river_path_point(0) - Vector2(20, 0))
				for index in range(6):
					geo._drag(geo.river_path_point(index))
				geo._release(geo.river_path_point(5))
			1:
				geo._press(Vector2(720, 310))
				await snap("phase-1-brush-contact")
				geo._drag(Vector2(520, 200))
				for row in range(4):
					geo._drag(Vector2(520, 195 + row * 60))
					geo._drag(Vector2(1040, 195 + row * 60))
				geo._release(Vector2(1040, 375))
			2:
				geo._press(Vector2(650, 380))
				for index in range(7):
					geo._drag(Vector2(650 if index % 2 else 950, 380))
				geo._release(Vector2(650, 380))
			3:
				for index in range(5):
					geo._press(geo.geode_seam_spot(index))
					geo._release(geo.geode_seam_spot(index))
				geo._press(geo.geode_half_center())
				geo._drag(geo.geode_half_center() + Vector2(110, 0))
				geo._release(geo.geode_half_center())
		await snap("phase-%d-progress" % phase)
		await _set_aspect(Vector2i(1600, 720))
		await snap("phase-%d-wide" % phase)
		await _set_aspect(Vector2i(1280, 720))
	print("GEOLOGYSHOT|DONE")
	quit(0)
