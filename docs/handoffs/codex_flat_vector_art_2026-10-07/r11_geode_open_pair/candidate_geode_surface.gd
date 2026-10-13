extends OperaGeologySurface
var opened_pair_texture: Texture2D
const OPENED_BOX := Rect2(Vector2(534.960761543,107.710532798),Vector2(471.921921922,471.921921922))
## R10 diagnostic marker/source alignment only: whole preserved painted closed source; legacy opening shown as a transition control.
func _load_textures() -> void:
	super._load_textures()
	var source_path := OS.get_environment("ROOTPIC_CANDIDATE")
	var image := Image.load_from_file(source_path)
	assert(image != null and not image.is_empty() and image.get_size() == Vector2i(1024,1024),"Exact candidate required; no missing-art fallback")
	geode_texture = ImageTexture.create_from_image(image)
	var opened_image := Image.load_from_file(OS.get_environment("ROOTPIC_OPEN_CANDIDATE"))
	assert(opened_image != null and not opened_image.is_empty() and opened_image.get_size() == Vector2i(1024,1024), "Exact opened pair required; no fallback")
	opened_pair_texture = ImageTexture.create_from_image(opened_image)

const GUIDE_SPOTS: Array[Vector2] = [Vector2(763,216), Vector2(756.2,278), Vector2(756.2,340), Vector2(755.8,401), Vector2(751,466)]

func marker_spot(index: int) -> Vector2:
	return GUIDE_SPOTS[index]

func _draw_geode() -> void:
	if geode_pull > 0.0:
		# Direct endpoint-only mount trial. Constant endpoint is intentionally evaluated for transition failure.
		assert(opened_pair_texture != null, "Opened candidate required")
		draw_texture_rect(opened_pair_texture,OPENED_BOX,false)
		return
	assert(geode_texture != null,"Painted closed source required")
	var center := GEODE_RECT.get_center()
	var box := Rect2(center-Vector2(195,175),Vector2(350,350))
	draw_texture_rect(geode_texture,box,false)
	# Guide circles remain unresolved vector artwork; their centers follow the painted crack.
	# Outer halo33.5 plus maximum center offset21.8 remains inside original56px touch envelope.
	for index: int in range(GEODE_SEAM_SPOTS.size()):
		var done: bool = geode_seams[index]
		var spot: Vector2 = GUIDE_SPOTS[index]
		draw_circle(spot,22.0,Color("#ffe69a") if not done else Color("#8ce6dd"))
		if not done:
			draw_arc(spot,31.0,0.0,TAU,24,Color(1.0,0.89,0.42,0.56),5.0,true)
