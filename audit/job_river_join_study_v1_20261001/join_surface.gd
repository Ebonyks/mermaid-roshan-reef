extends OperaGeologySurface
## Non-runtime source join study. Input, saves and flow stay on the actual parent.
const SOURCE := "res://assets_src/imagegen/geologist_river_components_v1_20261001/"
var dry_node: Texture2D
var wet_node: Texture2D
var dry_channel: Texture2D
var wet_channel: Texture2D

func _load_textures() -> void:
	super._load_textures()
	dry_node = _native_region("attempt_01/whole_canvas_1024.png", Rect2(44,167,560,547))
	wet_node = _native_region("attempt_01/whole_canvas_1024.png", Rect2(655,167,560,547))
	dry_channel = _native_region("attempt_02/whole_canvas_1024.png", Rect2(38,310,1180,300))
	wet_channel = _native_region("attempt_02/whole_canvas_1024.png", Rect2(37,734,1181,302))

func _native_region(path: String, native_rect: Rect2) -> Texture2D:
	var source := Image.load_from_file(SOURCE + path)
	assert(source != null and source.get_size() == Vector2i(1024,1024))
	var atlas := AtlasTexture.new()
	atlas.atlas = ImageTexture.create_from_image(source)
	atlas.region = Rect2(native_rect.position * 1024.0 / 1254.0,
		native_rect.size * 1024.0 / 1254.0)
	return atlas

func _draw_node(texture: Texture2D, center: Vector2, art_width: float) -> void:
	var art_size := Vector2(art_width, art_width * texture.get_height() / float(texture.get_width()))
	draw_texture_rect(texture, Rect2(center - art_size * 0.5, art_size), false)

func _draw_channel(texture: Texture2D, start: Vector2, finish: Vector2) -> void:
	var length_now := start.distance_to(finish)
	var height_now := length_now * texture.get_height() / float(texture.get_width())
	draw_set_transform((start + finish) * 0.5, (finish - start).angle())
	draw_texture_rect(texture, Rect2(Vector2(-length_now,-height_now) * 0.5,
		Vector2(length_now,height_now)), false)
	draw_set_transform(Vector2.ZERO)

func _draw_river() -> void:
	var flowing := _river_flow_indices()
	# Nodes first and complete open strips afterward: the study audits these joins.
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS, index / RIVER_COLS)
		_draw_node(wet_node if flowing.has(index) else dry_node,
			river_path_cell_center(cell), 60.0)
	_draw_node(wet_node,river_path_point(0),86.0)
	_draw_node(wet_node if _river_connected() else dry_node,
		river_path_point(RIVER_PATH.size()-1),94.0)
	for index: int in range(RIVER_COLS * RIVER_ROWS):
		if not river_wet[index]:
			continue
		var cell := Vector2i(index % RIVER_COLS, index / RIVER_COLS)
		for step: Vector2i in [Vector2i.RIGHT,Vector2i.DOWN]:
			var next := cell + step
			if next.x < RIVER_COLS and next.y < RIVER_ROWS \
					and river_wet[next.y * RIVER_COLS + next.x]:
				_draw_channel(wet_channel if flowing.has(index) else dry_channel,
					river_path_cell_center(cell),river_path_cell_center(next))
	if held:
		_draw_brush(pointer_pos)
