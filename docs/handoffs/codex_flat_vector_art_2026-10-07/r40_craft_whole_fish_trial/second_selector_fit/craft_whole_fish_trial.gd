extends "res://scripts/craft_studio.gd"
## Isolated complete-source trial. All gameplay state remains on inherited main.
## Selector texture is invisible functional colour geometry, never a drawn part or appearance source.
const ROOT_PATH := "res://docs/handoffs/codex_flat_vector_art_2026-10-07/r40_craft_whole_fish_trial/"
const ART_PATH := "res://assets_src/flat_vector_craft_fish_20261014/"
func _init(main: ReefMain) -> void:
	super(main)

func _ensure_resources() -> void:
	if m.has_meta("r40_whole_texture"):
		return
	var source: Image=Image.load_from_file(ART_PATH+"whole_fish_1024.png")
	assert(source!=null and source.get_size()==Vector2i(1024,1024))
	var whole: ImageTexture=ImageTexture.create_from_image(source)
	m.set_meta("r40_whole_texture",whole)
	var geometry: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(ROOT_PATH+"PALETTE_GEOMETRY.json")) as Dictionary
	var mask: Image=Image.create(1024,1024,false,Image.FORMAT_RGBA8)
	mask.fill(Color.BLACK)
	for region: Dictionary in geometry["regions"]:
		var polygon: PackedVector2Array=[]
		for point: Array in region["points_uv"]:
			polygon.append(Vector2(float(point[0])*1024.0,float(point[1])*1024.0))
		var expanded_polygons: Array[PackedVector2Array]=Geometry2D.offset_polygon(polygon,12.0)
		var expanded: PackedVector2Array=expanded_polygons[0] if not expanded_polygons.is_empty() else polygon
		var bounds: Rect2=Rect2(expanded[0],Vector2.ZERO)
		for point: Vector2 in expanded:
			bounds=bounds.expand(point)
		for y: int in range(maxi(0,int(bounds.position.y)),mini(1024,int(ceilf(bounds.end.y))+1)):
			for x: int in range(maxi(0,int(bounds.position.x)),mini(1024,int(ceilf(bounds.end.x))+1)):
				var where: Vector2=Vector2(x+0.5,y+0.5)
				var pigment: Color=source.get_pixel(x,y)
				var original_region: bool=Geometry2D.is_point_in_polygon(where,polygon)
				var fin_pigment: bool=pigment.h>=0.68 and pigment.s>=0.25 and pigment.v>=0.50
				if original_region or (fin_pigment and Geometry2D.is_point_in_polygon(where,expanded)):
					mask.set_pixel(x,y,Color.RED)
	for protected_region: Dictionary in geometry["protected_identity_geometry"]:
		var center: Vector2=Vector2(float(protected_region["center_uv"][0]),float(protected_region["center_uv"][1]))*1024.0
		var radius: float=float(protected_region["radius_uv"])*1024.0
		for y: int in range(maxi(0,int(center.y-radius)),mini(1024,int(ceilf(center.y+radius))+1)):
			for x: int in range(maxi(0,int(center.x-radius)),mini(1024,int(ceilf(center.x+radius))+1)):
				if Vector2(x+0.5,y+0.5).distance_to(center)<=radius:
					var pigment: Color=source.get_pixel(x,y)
					var warm: float=1.0-smoothstep(0.20,0.32,pigment.h)
					var amount: float=warm*smoothstep(0.08,0.25,pigment.s)
					var existing: Color=mask.get_pixel(x,y)
					mask.set_pixel(x,y,Color(existing.r,0.0,amount,1.0))
	var output: String=OS.get_environment("R40_SELECTOR_OUT")
	if not output.is_empty():
		assert(mask.save_png(output)==OK)
	m.set_meta("r40_selector",ImageTexture.create_from_image(mask))
	m.set_meta("r40_geometry",geometry)

func _craft_build_preview() -> void:
	if m.craft_kind!="fish":
		super()
		return
	if m.craft_fishbox==null:
		return
	_ensure_resources()
	for child: Node in m.craft_fishbox.get_children():
		child.queue_free()
	var whole: ImageTexture=m.get_meta("r40_whole_texture") as ImageTexture
	var geometry: Dictionary=m.get_meta("r40_geometry") as Dictionary
	var region_data: Array=geometry["visible_alpha_roi"]
	var atlas: AtlasTexture=AtlasTexture.new()
	atlas.atlas=whole
	atlas.region=Rect2(float(region_data[0]),float(region_data[1]),float(region_data[2]),float(region_data[3]))
	var tr: TextureRect=TextureRect.new()
	tr.name="R40WholePaintedFish"
	tr.texture=atlas
	tr.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
	tr.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	tr.position=Vector2(0.0,80.0)
	tr.size=Vector2(m.craft_fishbox.size.x,240.0)
	tr.mouse_filter=Control.MOUSE_FILTER_IGNORE
	tr.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	tr.modulate=Color.WHITE
	tr.set_meta("role","complete_whole_fish")
	tr.set_meta("whole_source_path",ART_PATH+"whole_fish_1024.png")
	tr.set_meta("functional_selector_only",true)
	tr.set_meta("whole_source_art_layers",1)
	var material: ShaderMaterial=ShaderMaterial.new()
	material.shader=load(ROOT_PATH+"whole_fish_palette.gdshader") as Shader
	material.set_shader_parameter("palette_selector",m.get_meta("r40_selector"))
	material.set_shader_parameter("body_choice",m.craft_body)
	material.set_shader_parameter("fin_choice",Color(m.craft_fins.r,m.craft_fins.g,m.craft_fins.b,1.0))
	material.set_shader_parameter("body_rainbow",m.craft_body_rb)
	material.set_shader_parameter("fin_rainbow",m.craft_fins_rb)
	tr.material=material
	m.craft_fishbox.add_child(tr)
