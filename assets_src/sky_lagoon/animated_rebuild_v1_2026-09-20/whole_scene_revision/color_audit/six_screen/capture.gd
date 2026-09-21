extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
func _capture(name: String) -> void:
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(1280,720)
	await process_frame
	await super._capture(name)
	var out: String = OS.get_environment("LIVING_CARD_SHOT_OUT")
	await RenderingServer.frame_post_draw
	_check("png_"+name,get_root().get_texture().get_image().save_png(out.path_join(name+".png"))==OK)
	if name != "canvas_screen_3_night":
		return
	var tint: Color = Color(0.62,0.68,0.88)
	for node_name: String in ["SkyLagoonCastleFourTower","SkyLagoonSlide","SkyLagoonPromenadeSwingFrame","SkyLagoonSeesaw","SkyLagoonReefPlane"]:
		var prop: Sprite2D = main.find_child(node_name,true,false) as Sprite2D
		_check("night_grade_"+node_name,prop!=null and prop.modulate==tint)
	var deck: Sprite2D = main.g["lagoon_bridge_patch"] as Sprite2D
	var rail: Sprite2D = main.g["lagoon_bridge_rail"] as Sprite2D
	var chains: Sprite2D = main.g["lagoon_bridge_chains"] as Sprite2D
	_check("bridge_single_tint",deck.modulate==Color.WHITE and rail.modulate==tint and chains.modulate==Color.WHITE)
	for page: int in range(3):
		promenade.set_master_route_x(float(page)*2048.0+1024.0)
		promenade._apply_view_transform(true)
		await process_frame
		await RenderingServer.frame_post_draw
		var shot: Image = get_root().get_texture().get_image()
		_check("night_size_%d"%page,shot.get_size()==Vector2i(1280,720))
		_check("night_page_%d"%page,shot.save_png(out.path_join("night_page_%d.png"%page))==OK)
