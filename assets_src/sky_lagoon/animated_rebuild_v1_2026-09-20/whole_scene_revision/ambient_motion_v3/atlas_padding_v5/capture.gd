extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
const STUDY := "res://tmp/sky-lagoon-whole-scene-v2/atlas-padding-audit/"
func snap(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(label, root.get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(label + ".png")) == OK)
func _capture(name: String) -> void:
	await super._capture(name)
	if name not in ["canvas_screen_1_day", "canvas_screen_2_day", "canvas_screen_3_day", "canvas_screen_3_night"]:
		return
	var processing: bool = main.is_processing()
	var old_time: float = Engine.time_scale
	var route: float = promenade.master_route_x()
	main.set_process(false)
	Engine.time_scale = 0.0
	var parser := JSON.new()
	_check("candidate_manifest", parser.parse(FileAccess.get_file_as_string(STUDY + "CANDIDATES.json")) == OK)
	var candidates: Dictionary = {}
	for value: Variant in (parser.data as Dictionary)["cards"] as Array:
		var row: Dictionary = value as Dictionary
		candidates[str(row["id"])] = row
	var saved: Array[Dictionary] = []
	for value: Variant in main.g["lagoon_whole_cards"] as Array:
		var card: Sprite2D = value as Sprite2D
		var definition: Dictionary = card.get_meta("definition") as Dictionary
		if not candidates.has(str(definition["id"])):
			continue
		var row: Dictionary = candidates[str(definition["id"])] as Dictionary
		var source: Image = Image.load_from_file(STUDY + "candidate/" + str(row["file"]))
		source.fix_alpha_edges()
		saved.append({"card": card, "texture": card.texture, "position": card.position, "frame": card.frame, "count": int(definition["frames"]), "candidate": ImageTexture.create_from_image(source), "offset": Vector2(float(row["position_offset_master"][0]), float(row["position_offset_master"][1]))})
	_check("twenty_seven_candidates", saved.size() == 27)
	var pages: int = 3 if main.is_night else 1
	for page: int in range(pages):
		if main.is_night:
			promenade.set_master_route_x(float(page)*2048.0+1024.0)
			promenade._apply_view_transform(true)
		for k: int in range(12):
			for row: Dictionary in saved:
				var card: Sprite2D = row["card"] as Sprite2D
				card.texture = row["texture"] as Texture2D
				card.position = row["position"] as Vector2
				card.frame = k % int(row["count"])
			await snap(name + "_p%d_k%02d_original" % [page,k])
			for row: Dictionary in saved:
				var card: Sprite2D = row["card"] as Sprite2D
				card.texture = row["candidate"] as Texture2D
				card.position = (row["position"] as Vector2) + (row["offset"] as Vector2)
			await snap(name + "_p%d_k%02d_cropped" % [page,k])
	for row: Dictionary in saved:
		var card: Sprite2D = row["card"] as Sprite2D
		card.texture = row["texture"] as Texture2D
		card.position = row["position"] as Vector2
		card.frame = int(row["frame"])
	promenade.set_master_route_x(route)
	promenade._apply_view_transform(true)
	Engine.time_scale = old_time
	main.set_process(processing)
