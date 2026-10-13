extends OperaGeologySurface
## Diagnostic only: whole preserved painted closed source; legacy opening shown as a transition control.
func _load_textures() -> void:
	super._load_textures()
	var source_path := OS.get_environment("ROOTPIC_CANDIDATE")
	var image := Image.load_from_file(source_path)
	assert(image != null and not image.is_empty() and image.get_size() == Vector2i(1024,1024),"Exact candidate required; no missing-art fallback")
	geode_texture = ImageTexture.create_from_image(image)

func _draw_geode() -> void:
	if geode_pull > 0.0:
		# Deliberate unchanged production control, not a repaired opening or an adopted fallback.
		super._draw_geode()
		return
	assert(geode_texture != null,"Painted closed source required")
	var center := GEODE_RECT.get_center()
	var box := Rect2(center-Vector2(175,175),Vector2(350,350))
	draw_texture_rect(geode_texture,box,false)
	# Existing visible artwork markers retained as distinct unresolved pieces.
	for index: int in range(GEODE_SEAM_SPOTS.size()):
		var done: bool = geode_seams[index]
		var spot: Vector2 = GEODE_SEAM_SPOTS[index]
		draw_circle(spot,22.0,Color("#ffe69a") if not done else Color("#8ce6dd"))
		if not done:
			draw_arc(spot,32.0,0.0,TAU,24,Color(1.0,0.89,0.42,0.56),5.0,true)
