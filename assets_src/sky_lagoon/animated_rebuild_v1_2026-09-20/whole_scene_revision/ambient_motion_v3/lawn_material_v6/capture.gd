extends "res://scripts/probe_sky_lagoon_animation_visual.gd"
const STUDY := "res://tmp/sky-lagoon-whole-scene-v2/whole-lawn-four-region-v2/"
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
	_check("lawn_manifest", parser.parse(FileAccess.get_file_as_string(STUDY + "REVIEW.json")) == OK)
	var regions: Array = (parser.data as Dictionary)["regions"] as Array
	var holder: Node2D = main.g["lagoon_base_layer"] as Node2D
	var old_count: int = holder.get_child_count()
	var cards: Array[Dictionary] = []
	for region: Dictionary in regions:
		var old_card: Sprite2D = null
		for value: Variant in main.g.get("lagoon_whole_cards", []) as Array:
			var candidate: Sprite2D = value as Sprite2D
			if str((candidate.get_meta("definition") as Dictionary)["id"]) == str(region["id"]):
				old_card = candidate
		_check("original_owner_" + str(region["id"]), old_card != null)
		if old_card == null:
			continue
		var trial := Sprite2D.new()
		trial.name = "TemporaryWholeLawn_" + str(region["id"])
		trial.centered = false
		var rect: Array = region["rect"] as Array
		trial.position = Vector2(float(rect[0]), float(rect[1]))
		trial.z_index = old_card.z_index
		trial.modulate = old_card.modulate
		trial.material = old_card.material
		trial.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		trial.visible = false
		holder.add_child(trial)
		var textures: Array[Texture2D] = []
		for k: int in range(4):
			var source: Image = Image.load_from_file(STUDY + str(region["id"]) + "/overlay-%d.png" % k)
			_check("overlay_size_" + str(region["id"]), source != null and source.get_size() == Vector2i(int(rect[2]), int(rect[3])))
			source.fix_alpha_edges()
			textures.append(ImageTexture.create_from_image(source))
		cards.append({"old": old_card, "visible": old_card.visible, "trial": trial, "textures": textures})
	_check("four_lawn_owners", cards.size() == 4)
	var pages: int = 3 if main.is_night else 1
	for page: int in range(pages):
		if main.is_night:
			promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
			promenade._apply_view_transform(true)
		var label: String = name + "_p%d" % page
		await snap(label + "_original")
		for row: Dictionary in cards:
			(row["old"] as Sprite2D).visible = false
			(row["trial"] as Sprite2D).visible = true
		for k: int in range(4):
			for row: Dictionary in cards:
				(row["trial"] as Sprite2D).texture = (row["textures"] as Array[Texture2D])[k]
			await snap(label + "_cel%d" % k)
		for row: Dictionary in cards:
			(row["old"] as Sprite2D).visible = bool(row["visible"])
			(row["trial"] as Sprite2D).visible = false
		await snap(label + "_restored")
		if name == "canvas_screen_3_day" or (main.is_night and page == 2):
			await _castle_fragment_review(label)
	for row: Dictionary in cards:
		(row["trial"] as Sprite2D).free()
	_check("temporary_lawns_removed", holder.get_child_count() == old_count)
	promenade.set_master_route_x(route)
	promenade._apply_view_transform(true)
	Engine.time_scale = old_time
	main.set_process(processing)

func _castle_fragment_review(label: String) -> void:
	for ident: String in ["castle_left_verge", "castle_right_verge"]:
		var card: Sprite2D = null
		for value: Variant in main.g.get("lagoon_whole_cards", []) as Array:
			var candidate: Sprite2D = value as Sprite2D
			if str((candidate.get_meta("definition") as Dictionary)["id"]) == ident:
				card = candidate
		_check("castle_fragment_owner_" + ident, card != null)
		if card == null:
			continue
		var saved_frame: int = card.frame
		var saved_visible: bool = card.visible
		card.visible = false
		await snap(label + "_" + ident + "_hidden")
		card.visible = true
		for k: int in range(4):
			card.frame = k
			await snap(label + "_" + ident + "_frame%d" % k)
		card.frame = saved_frame
		card.visible = saved_visible
		await snap(label + "_" + ident + "_restore")
