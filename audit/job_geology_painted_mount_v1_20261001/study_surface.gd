extends OperaGeologySurface
## Disposable visual study. Input/progress remain inherited production behavior.
var painted_study := false
var work_texture: Texture2D
var open_left_texture: Texture2D
var open_right_texture: Texture2D

func _draw_work_surface() -> void:
	if not painted_study:
		super._draw_work_surface()
		return
	draw_texture_rect(work_texture, Rect2(330, 130, 860, 560), false)

func _draw_geode() -> void:
	if not painted_study:
		super._draw_geode()
		return
	var center := GEODE_RECT.get_center()
	var fit_size := Vector2(374, 350)
	var left := center - fit_size * 0.5
	if geode_pull <= 0.0:
		draw_texture_rect(geode_texture, Rect2(left, fit_size), false)
		for index: int in range(GEODE_SEAM_SPOTS.size()):
			draw_circle(GEODE_SEAM_SPOTS[index], 15.0,
				Color("#ffe69a") if not geode_seams[index] else Color("#8ce6dd"))
		return
	draw_texture_rect(open_left_texture, Rect2(left, Vector2(187, 350)), false)
	draw_texture_rect(open_right_texture,
		Rect2(center + Vector2(geode_pull, -175), Vector2(187, 350)), false)
	var reward_size := Vector2(96, 130)
	var reward_pos := center + Vector2(geode_pull * 0.5, 0) - reward_size * 0.5
	var clip_left := maxf(reward_pos.x, center.x)
	var clip_right := minf(reward_pos.x + reward_size.x, center.x + geode_pull)
	if clip_right > clip_left:
		var source_size := crystals_texture.get_size()
		var source_left := (clip_left - reward_pos.x) / reward_size.x * source_size.x
		var source_width := (clip_right - clip_left) / reward_size.x * source_size.x
		draw_texture_rect_region(crystals_texture,
			Rect2(clip_left, reward_pos.y, clip_right - clip_left, reward_size.y),
			Rect2(source_left, 0, source_width, source_size.y))
