extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
const PREVIOUS := "res://tmp/sky-lagoon-whole-scene-v2/lawn-v6-imported/previous/"
const IDS := ["arrival_lawn", "meadow_upper_left", "meadow_upper_right", "meadow_lower_lawn"]
func snap(label: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	_check(label, root.get_texture().get_image().save_png(OS.get_environment("LIVING_CARD_SHOT_OUT").path_join(label + ".png")) == OK)
func apply_cards(cards: Array[Dictionary], previous: bool, frame: int) -> void:
	for row: Dictionary in cards:
		var card: Sprite2D = row["card"] as Sprite2D
		card.texture = row["old_texture"] as Texture2D if previous else row["texture"] as Texture2D
		card.position = row["old_position"] as Vector2 if previous else row["position"] as Vector2
		card.scale = row["old_scale"] as Vector2 if previous else row["scale"] as Vector2
		card.frame = frame
func _capture(name: String) -> void:
	await super._capture(name)
	if name not in ["canvas_screen_1_day", "canvas_screen_2_day", "canvas_screen_3_day", "canvas_screen_3_night"]:
		return
	var was_processing: bool = main.is_processing()
	var old_time: float = Engine.time_scale
	var route: float = promenade.master_route_x()
	main.set_process(false)
	Engine.time_scale = 0.0
	var old_manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PREVIOUS + "manifest.json")) as Dictionary
	var definitions: Dictionary = {}
	for definition: Dictionary in old_manifest["cards"] as Array:
		definitions[str(definition["id"])] = definition
	var cards: Array[Dictionary] = []
	for value: Variant in main.g["lagoon_whole_cards"] as Array:
		var card: Sprite2D = value as Sprite2D
		var current: Dictionary = card.get_meta("definition") as Dictionary
		var ident: String = str(current["id"])
		if ident not in IDS:
			continue
		_check("imported_four_cel_lawn_" + ident, int(current["frames"]) == 4 and is_equal_approx(float(current["cycle"]), 1.4) and card.texture.resource_path.begins_with("res://assets/"))
		var previous: Dictionary = definitions[ident] as Dictionary
		var source: Image = Image.load_from_file(PREVIOUS + str(previous["file"]))
		source.fix_alpha_edges()
		cards.append({"card": card, "texture": card.texture, "position": card.position, "scale": card.scale, "frame": card.frame, "old_texture": ImageTexture.create_from_image(source), "old_position": Vector2(float(previous["position"][0]), float(previous["position"][1])), "old_scale": Vector2.ONE * float(previous["scale"])})
	_check("four_imported_lawn_owners", cards.size() == 4)
	for page: int in range(3 if main.is_night else 1):
		if main.is_night:
			promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
			promenade._apply_view_transform(true)
		var label: String = name + "_p%d" % page
		apply_cards(cards, true, 0)
		await snap(label + "_previous")
		for k: int in range(4):
			apply_cards(cards, false, k)
			await snap(label + "_lawn%d" % k)
		apply_cards(cards, true, 0)
		await snap(label + "_rollback")
	for row: Dictionary in cards:
		var card: Sprite2D = row["card"] as Sprite2D
		card.texture = row["texture"] as Texture2D
		card.position = row["position"] as Vector2
		card.scale = row["scale"] as Vector2
		card.frame = int(row["frame"])
	promenade.set_master_route_x(route)
	promenade._apply_view_transform(true)
	Engine.time_scale = old_time
	main.set_process(was_processing)
