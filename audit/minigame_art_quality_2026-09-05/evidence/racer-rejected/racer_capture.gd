extends "res://scripts/probe_opera_art.gd"

func snap(label: String) -> void:
	var race := main.opera_game.act.career_world_2d.surface as OperaRacerSurface
	if race != null:
		race.queue_redraw()
		print("RACERSTATE|", label, "|steer=", race.race_steer, "|held=", race.held)
	await _settle(3)
	await RenderingServer.frame_post_draw
	get_root().get_texture().get_image().save_png("res://tmp/art-quality/racer/" + label + ".png")
	print("RACERSHOT|", label)

func _run() -> void:
	await _set_aspect(Vector2i(1280,720))
	if not await _start_runtime():
		quit(1)
		return
	var room_id := CastleCareerRoutes.room_for_act(12)
	if not await _prepare_career_route(room_id, 12):
		quit(2)
		return
	routes._launch(room_id, 12)
	if not await _wait_career_ready(12, room_id):
		quit(3)
		return
	var act: OperaAct = main.opera_game.act
	var world: OperaCareerWorld2D = act.career_world_2d
	act.set_process(false)
	world.set_process(false)
	world.surface.set_process(false)
	world._show_phase()
	world._process(3.0)
	await snap("01-pit-stop")
	world.phase_index = world._finale_start()
	world._show_phase()
	world._process(3.0)
	await snap("02-race-ready")
	await _set_aspect(Vector2i(1600,720))
	await snap("02-race-ready-wide")
	await _set_aspect(Vector2i(1280,720))
	var surface := world.surface as OperaRacerSurface
	surface._press(surface.STEERING_RECT.get_center())
	surface._drag(surface.STEERING_RECT.get_center() + Vector2(-290,0))
	await snap("02-steer-left")
	surface._drag(surface.STEERING_RECT.get_center() + Vector2(290,0))
	await snap("02-steer-right")
	surface._drag(surface.STEERING_RECT.get_center())
	for frame in range(720):
		surface._process(1.0/60.0)
	await snap("03-race-far-bend")
	for frame in range(1500):
		surface._process(1.0/60.0)
	await snap("04-second-lap")
	for frame in range(1600):
		surface._process(1.0/60.0)
	act._process(0.05)
	world._process(2.21)
	await snap("05-finish")
	print("RACERSHOT|distance=",surface.kart.s," state=",act.state)
	quit(0)
