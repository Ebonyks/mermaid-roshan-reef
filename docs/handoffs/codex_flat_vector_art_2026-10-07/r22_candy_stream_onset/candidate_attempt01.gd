extends OperaGestureSurface
## R22 nonruntime whole painted-stream preview. Candidate quality/acceptance remain open.
var trial_enabled: bool = true
var onset_enabled: bool = false
var floor_columns: Array = []
var contact_rows: Array = []
var contact_image: Image
var stream_texture: Texture2D
var stream_missing: bool = false
const STREAM_START := Vector2(465.0,61)
const STREAM_END := Vector2(437.0,964)

func _pool_contact_data() -> Dictionary:
	var nominal := _pour_landing_point()
	if widget_overlay == null or pour_level <= 0.0:
		return {"valid":false,"nominal":[nominal.x,nominal.y]}
	if contact_rows.is_empty():
		var table: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://.godot/r22_fill_contact_rows.json"))
		contact_rows = table["rows"]
		contact_image = widget_overlay.get_image()
		if contact_image.is_compressed():
			contact_image.decompress()
	var cover := _cover_rect(widget_overlay)
	var tex_size := widget_overlay.get_size()
	var ink := _ink_bounds(widget_overlay)
	var edge := ink.y - (ink.y - ink.x) * clampf(pour_level,0.0,1.0)
	var first_y := clampi(int(ceil(edge * tex_size.y)),0,int(tex_size.y)-1)
	var sx := clampi(int((nominal.x-cover.position.x)/cover.size.x*tex_size.x),0,int(tex_size.x)-1)
	var sy := clampi(int((nominal.y-cover.position.y)/cover.size.y*tex_size.y),0,int(tex_size.y)-1)
	var best := Vector2i(-1,-1)
	var best_score: float = INF
	for y: int in range(first_y,int(tex_size.y)):
		for interval: Array in contact_rows[y]:
			var x := clampi(sx,int(interval[0]),int(interval[1]))
			var pixel_point := cover.position + Vector2(float(x)+0.5,float(y)+0.5)/tex_size*cover.size
			var score := nominal.distance_squared_to(pixel_point)
			if score < best_score and contact_image.get_pixel(x,y).a >= 0.5:
				best = Vector2i(x,y)
				best_score = score
	if best.x < 0:
		return {"valid":false,"nominal":[nominal.x,nominal.y]}
	var point := cover.position + (Vector2(best)+Vector2.ONE*0.5)/tex_size*cover.size
	return {"valid":true,"nominal":[nominal.x,nominal.y],"target":[point.x,point.y],"source_pixel":[best.x,best.y],"source_alpha":contact_image.get_pixel(best.x,best.y).a,"reveal_first_source_y":first_y,"original_endpoint_source_pixel":[sx,sy],"original_endpoint_in_revealed_alpha":sy>=first_y and contact_image.get_pixel(sx,sy).a>=0.5,"distance_from_original":sqrt(best_score)}

func _contact_data() -> Dictionary:
	var data := _pool_contact_data()
	data["contact_kind"] = "revealed_pool" if bool(data.get("valid",false)) else "nominal_unbound"
	if bool(data.get("valid",false)) or not onset_enabled or not _pour_stream_active():
		return data
	if floor_columns.is_empty():
		var table: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://.godot/r22_empty_floor_columns.json"))
		floor_columns = table["columns"]
	var nominal: Array = data["nominal"]
	var cover := _cover_rect(pour_scene_texture)
	var texture_size := pour_scene_texture.get_size()
	var sx := clampi(int((float(nominal[0])-cover.position.x)/cover.size.x*texture_size.x),0,int(texture_size.x)-1)
	var column: Variant = floor_columns[sx]
	if column == null:
		data["floor_lookup_missing"] = true
		return data
	var sy: int = int(column["floor"])
	var point := cover.position+(Vector2(sx,sy)+Vector2.ONE*0.5)/texture_size*cover.size
	data["valid"] = true
	data["contact_kind"] = "empty_cavity_floor_mask"
	data["target"] = [point.x,point.y]
	data["floor_source_pixel"] = [sx,sy]
	data["floor_source_boundary_y"] = int(column["boundary"])
	data["floor_source_inset_pixels"] = 4
	data["floor_lookup_sha256"] = FileAccess.get_sha256("res://.godot/r22_empty_floor_columns.json")
	return data

func stream_contract() -> Dictionary:
	var data := _contact_data()
	data["trial_enabled"] = trial_enabled
	data["onset_enabled"] = onset_enabled
	data["stream_active"] = _pour_stream_active() and pour_level < 1.0
	data["pour_level"] = pour_level
	data["spout"] = str(_pour_spout_point())
	data["draw_order"] = "background/stream/painted_fill/ladle" if trial_enabled else "background/painted_fill/stream/ladle"
	data["material"] = "R21 whole painted image unchanged; strong S contour/action remain failed; broad hidden-RGB glow alpha0" if trial_enabled else "Original three uniform polylines"
	data["whole_unit_transform"] = "Rigid rotation and uniform scaling only; no part/UV deformation"
	data["stream_missing"] = stream_missing
	data["candidate_sha256"] = FileAccess.get_sha256("res://assets_src/flat_vector_candy_stream_20261013/stream_1024.png")
	data["lookup_sha256"] = FileAccess.get_sha256("res://.godot/r22_fill_contact_rows.json")
	data["prototype_sha256"] = FileAccess.get_sha256("res://.godot/r22_candy_stream_surface.gd")
	return data

func _draw_candymaker_pour_stream() -> void:
	if not trial_enabled or stream_missing:
		super._draw_candymaker_pour_stream()
		return
	if not _pour_stream_active() or pour_level >= 1.0:
		return
	if stream_texture == null:
		var image := Image.load_from_file("res://assets_src/flat_vector_candy_stream_20261013/stream_1024.png")
		if image == null or image.is_empty():
			super._draw_candymaker_pour_stream()
			return
		stream_texture = ImageTexture.create_from_image(image)
	var data := _contact_data()
	var endpoint: Array = data["target"] if bool(data.get("valid",false)) else data["nominal"]
	var landing := Vector2(float(endpoint[0]),float(endpoint[1]))
	var spout := _pour_spout_point()
	var delta := landing-spout
	var axis := STREAM_END-STREAM_START
	var scale := delta.length()/axis.length()
	draw_set_transform(spout,delta.angle()-axis.angle(),Vector2.ONE*scale)
	draw_texture_rect(stream_texture,Rect2(-STREAM_START,stream_texture.get_size()),false)
	draw_set_transform(Vector2.ZERO)

func _draw_pour_scene(center: Vector2) -> void:
	if not trial_enabled or not _is_candymaker_pour() or pour_scene_texture == null or widget_overlay == null or pour_empty_mover_texture == null or widget_mover == null:
		super._draw_pour_scene(center)
		return
	draw_texture_rect(pour_scene_texture,_cover_rect(pour_scene_texture),false)
	_draw_candymaker_pour_stream()
	_draw_progress_overlay(widget_overlay,pour_level,false)
	last_specialist_subject_route = "candy_molds"
	var pitcher := _pour_pitcher_rect()
	draw_set_transform(pitcher.get_center(),_pour_pitcher_rotation())
	draw_texture_rect(pour_empty_mover_texture,Rect2(-pitcher.size*0.5,pitcher.size),false)
	if _candymaker_full_ladle_alpha() > 0.0:
		draw_texture_rect(widget_mover,Rect2(-pitcher.size*0.5,pitcher.size),false,Color(1.0,1.0,1.0,_candymaker_full_ladle_alpha()))
	draw_set_transform(Vector2.ZERO)
