extends OperaGeologySurface
## Isolated atlas field study. Actual parent input, grid, flow and saves unchanged.
const PARTS := "res://assets_src/imagegen/geologist_river_components_v1_20261001/"
const JUNCTIONS := "res://assets_src/imagegen/geologist_river_junctions_v1_20261001/"
const NATIVE_TO_RUNTIME := 1024.0 / 1254.0
var source_textures: Dictionary = {}
var dry_circle: Texture2D
var wet_circle: Texture2D
var wide_earth: Texture2D

func _source_texture(path: String) -> Texture2D:
	if not source_textures.has(path):
		var image := Image.load_from_file(path)
		assert(image != null and image.get_size() == Vector2i(1024,1024))
		source_textures[path] = ImageTexture.create_from_image(image)
	return source_textures[path] as Texture2D

func _region(path: String, native_rect: Rect2) -> Texture2D:
	var atlas := AtlasTexture.new()
	atlas.atlas = _source_texture(path)
	atlas.region = Rect2(native_rect.position * NATIVE_TO_RUNTIME,
		native_rect.size * NATIVE_TO_RUNTIME)
	assert(Rect2(Vector2.ZERO,Vector2(1024,1024)).encloses(atlas.region))
	return atlas

func _load_textures() -> void:
	super._load_textures()
	var soil_image := Image.load_from_file("res://assets_src/imagegen/geologist_river_bed_v1_20261002/attempt_01/whole_canvas_1024x512.png")
	assert(soil_image != null and soil_image.get_size() == Vector2i(1024,512))
	wide_earth = ImageTexture.create_from_image(soil_image)
	dry_circle = _region(PARTS + "attempt_01/whole_canvas_1024.png",Rect2(44,167,560,547))
	wet_circle = _region(PARTS + "attempt_01/whole_canvas_1024.png",Rect2(655,167,560,547))

func _draw_circle_art(center: Vector2, wet: bool, width_now: float) -> void:
	var art := wet_circle if wet else dry_circle
	var size_now := Vector2(width_now,width_now * art.get_height() / float(art.get_width()))
	draw_texture_rect(art,Rect2(center-size_now*0.5,size_now),false)

func _draw_work_surface() -> void:
	# Source-transparent full canvas, authored2:1 aspect, no flat panel below it.
	draw_texture_rect(wide_earth,Rect2(Vector2(248.0,114.0),Vector2(1024.0,512.0)),false)

func _mask(cell: Vector2i) -> int:
	var result := 0
	var steps: Array[Vector2i] = [Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP]
	for bit: int in range(4):
		var next := cell + steps[bit]
		if next.x >= 0 and next.x < RIVER_COLS and next.y >= 0 and next.y < RIVER_ROWS \
				and river_wet[next.y * RIVER_COLS + next.x]:
			result |= 1 << bit
	return result

func _draw_field(center: Vector2, kind: String, angle: float, wet: bool) -> void:
	var source_path := JUNCTIONS + ("wet_attempt_01/" if wet else "dry_attempt_01/") \
		+ "whole_canvas_1024.png"
	var anchor := Vector2(941.0,915.5)
	var pixel_scale := 0.18
	if kind == "elbow":
		anchor = Vector2(889.0,407.0)
	elif kind == "tee":
		anchor = Vector2(317.0,963.0)
	var turned := not is_zero_approx(sin(angle))
	var extent := Vector2(76.0,88.0) if turned else Vector2(88.0,76.0)
	var region_now := Rect2(anchor - extent * 0.5 / pixel_scale,extent / pixel_scale)
	if kind == "endcap":
		anchor = Vector2(345.5555556,345.0)
		pixel_scale = 0.18
		# Keep the complete closed bowl; only its open right stub ends on its port plane.
		region_now = Rect2(53.0,119.0,anchor.x + extent.x * 0.5 / pixel_scale - 53.0,423.0)
	elif kind == "straight":
		source_path = PARTS + "attempt_02/whole_canvas_1024.png"
		var height_now := 302.0 if wet else 300.0
		var source_y := 734.0 if wet else 310.0
		pixel_scale = extent.x / 586.0
		region_now = Rect2(334.5,source_y,586.0,height_now)
		anchor = region_now.get_center()
	var art := _region(source_path,region_now)
	draw_set_transform(center,angle)
	draw_texture_rect(art,Rect2((region_now.position-anchor)*pixel_scale,
		region_now.size*pixel_scale),false)
	draw_set_transform(Vector2.ZERO)

func _draw_river() -> void:
	var flowing := _river_flow_indices()
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS,index / RIVER_COLS)
		var center := river_path_cell_center(cell)
		var mask := _mask(cell)
		var wet := flowing.has(index)
		if mask == 0:
			_draw_circle_art(center,wet,60.0)
		elif mask in [1,2,4,8]:
			var angle := 0.0 if mask == 1 else PI*0.5 if mask == 2 else PI if mask == 4 else -PI*0.5
			_draw_field(center,"endcap",angle,wet)
		elif mask in [5,10]:
			_draw_field(center,"straight",0.0 if mask == 5 else PI*0.5,wet)
		elif mask in [9,3,6,12]:
			var angle := 0.0 if mask == 9 else PI*0.5 if mask == 3 else PI if mask == 6 else -PI*0.5
			_draw_field(center,"elbow",angle,wet)
		elif mask in [13,11,7,14]:
			var angle := 0.0 if mask == 13 else PI*0.5 if mask == 11 else PI if mask == 7 else -PI*0.5
			_draw_field(center,"tee",angle,wet)
		else:
			assert(mask == 15)
			_draw_field(center,"cross",0.0,wet)
	if not river_wet[RIVER_PATH[0].y * RIVER_COLS + RIVER_PATH[0].x]:
		_draw_circle_art(river_path_point(0),true,86.0)
	if not river_wet[RIVER_PATH[-1].y * RIVER_COLS + RIVER_PATH[-1].x]:
		_draw_circle_art(river_path_point(RIVER_PATH.size()-1),false,94.0)
	if held:
		_draw_brush(pointer_pos)
