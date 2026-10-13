extends OperaGestureSurface
## R20 isolated contact/occlusion study. Original flat material remains open.
var trial_enabled: bool = false
var contact_rows: Array = []
var contact_image: Image

func _contact_data() -> Dictionary:
	var nominal := _pour_landing_point()
	if widget_overlay == null or pour_level <= 0.0:
		return {"valid":false,"nominal":[nominal.x,nominal.y]}
	if contact_rows.is_empty():
		var table: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://.godot/r20_fill_contact_rows.json"))
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

func stream_contract() -> Dictionary:
	var data := _contact_data()
	data["trial_enabled"] = trial_enabled
	data["stream_active"] = _pour_stream_active() and pour_level < 1.0
	data["pour_level"] = pour_level
	data["spout"] = str(_pour_spout_point())
	data["draw_order"] = "background/stream/painted_fill/ladle" if trial_enabled else "background/painted_fill/stream/ladle"
	data["material"] = "Original three uniform polylines; no art-removal claim"
	data["lookup_sha256"] = FileAccess.get_sha256("res://.godot/r20_fill_contact_rows.json")
	data["prototype_sha256"] = FileAccess.get_sha256("res://.godot/r20_candy_stream_surface.gd")
	return data

func _draw_candymaker_pour_stream() -> void:
	if not trial_enabled:
		super._draw_candymaker_pour_stream()
		return
	if not _pour_stream_active() or pour_level >= 1.0:
		return
	var data := _contact_data()
	if not bool(data.get("valid",false)):
		super._draw_candymaker_pour_stream()
		return
	var target: Array = data["target"]
	var landing := Vector2(float(target[0]),float(target[1]))
	var spout := _pour_spout_point()
	var reserve_scale := clampf(pour_reserve/0.18,0.38,1.0)
	var thickness := (5.0+9.0*(pour_tilt-0.36)/0.64)*reserve_scale
	var control := Vector2(spout.x+5.0,landing.y-8.0)
	var rope := PackedVector2Array()
	for sample: int in range(9):
		var t := float(sample)/8.0
		var one_minus_t := 1.0-t
		rope.append(spout*one_minus_t*one_minus_t+control*2.0*one_minus_t*t+landing*t*t)
	draw_polyline(rope,Color("#75432f"),thickness+3.0,true)
	draw_polyline(rope,Color("#f2b94f"),thickness,true)
	var highlight := PackedVector2Array()
	for point: Vector2 in rope:
		highlight.append(point+Vector2(-1.2,-0.6))
	draw_polyline(highlight,Color(1.0,0.89,0.55,0.82),maxf(1.2,thickness*0.22),true)

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
