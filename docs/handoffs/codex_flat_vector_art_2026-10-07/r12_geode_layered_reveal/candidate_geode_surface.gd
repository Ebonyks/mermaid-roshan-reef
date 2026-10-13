extends OperaGeologySurface
## Isolated source-preserving layered reveal; original gesture logic unchanged.
var left_shell_texture: Texture2D
var right_shell_texture: Texture2D
var cavity_texture: Texture2D
const CUT_POINTS: Array[Vector2] = [Vector2(600,0), Vector2(584,90), Vector2(550,150), Vector2(539,210), Vector2(529,330), Vector2(530,512), Vector2(530,690), Vector2(518,790), Vector2(516,881), Vector2(504,961), Vector2(504,1024)]
const CLOSED_BOX := Rect2(575,165,350,350)
const CAVITY_TOP := 187.900390625
const CAVITY_HEIGHT := 306.93359375
const CAVITY_WIDTH := 120.5810546875
const GUIDE_SPOTS: Array[Vector2] = [Vector2(763,216),Vector2(756.2,278),Vector2(756.2,340),Vector2(755.8,401),Vector2(751,466)]
func _load_image_texture(path: String, expected: Vector2i) -> Texture2D:
	var image := Image.load_from_file(path)
	assert(image != null and not image.is_empty() and image.get_size()==expected,"Exact source-derived image required; no missing-art fallback")
	return ImageTexture.create_from_image(image)
func _load_textures() -> void:
	super._load_textures()
	geode_texture = _load_image_texture(OS.get_environment("ROOTPIC_CANDIDATE"),Vector2i(1024,1024))
	var base := OS.get_environment("ROOTPIC_LAYERED_DIR")
	left_shell_texture = _load_image_texture(base.path_join("geode_closed_left.png"),Vector2i(1024,1024))
	right_shell_texture = _load_image_texture(base.path_join("geode_closed_right.png"),Vector2i(1024,1024))
	cavity_texture = _load_image_texture(base.path_join("geode_cavity.png"),Vector2i(220,560))
func marker_spot(index: int) -> Vector2:
	return GUIDE_SPOTS[index]
func _cut_x(y: float) -> float:
	for index: int in range(CUT_POINTS.size()-1):
		var a: Vector2 = CUT_POINTS[index]
		var b: Vector2 = CUT_POINTS[index+1]
		if y>=a.y and y<=b.y:
			return floorf(lerpf(a.x,b.x,(y-a.y)/(b.y-a.y))+0.5)
	assert(false,"Missing source crack row")
	return 0.0
func _draw_crystal_gap() -> void:
	# Invisible textured clipping geometry: no colored substitute, no full endpoint swap.
	var ys: Array[float] = [67.0,90.0,150.0,210.0,330.0,512.0,690.0,790.0,881.0,961.0,965.0]
	var points := PackedVector2Array()
	var uv := PackedVector2Array()
	var colors := PackedColorArray()
	for y: float in ys:
		var at := Vector2(CLOSED_BOX.position.x+_cut_x(y)*350.0/1024.0,CLOSED_BOX.position.y+y*350.0/1024.0)
		points.append(at);uv.append(Vector2(0.0,(at.y-CAVITY_TOP)/CAVITY_HEIGHT));colors.append(Color.WHITE)
	for index: int in range(ys.size()-1,-1,-1):
		var y: float = ys[index]
		var at := Vector2(CLOSED_BOX.position.x+_cut_x(y)*350.0/1024.0+geode_pull,CLOSED_BOX.position.y+y*350.0/1024.0)
		points.append(at);uv.append(Vector2(geode_pull/CAVITY_WIDTH,(at.y-CAVITY_TOP)/CAVITY_HEIGHT));colors.append(Color.WHITE)
	draw_polygon(points,colors,uv,cavity_texture)
func _draw_geode() -> void:
	if geode_pull>0.0:
		assert(left_shell_texture != null and right_shell_texture != null and cavity_texture != null)
		_draw_crystal_gap()
		draw_texture_rect(left_shell_texture,CLOSED_BOX,false)
		draw_texture_rect(right_shell_texture,Rect2(CLOSED_BOX.position+Vector2(geode_pull,0),CLOSED_BOX.size),false)
		return
	assert(geode_texture != null)
	draw_texture_rect(geode_texture,CLOSED_BOX,false)
	for index: int in range(GEODE_SEAM_SPOTS.size()):
		var done: bool = geode_seams[index]
		var spot: Vector2 = GUIDE_SPOTS[index]
		draw_circle(spot,22.0,Color("#ffe69a") if not done else Color("#8ce6dd"))
		if not done:
			draw_arc(spot,31.0,0.0,TAU,24,Color(1.0,0.89,0.42,0.56),5.0,true)
