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
	# The crystals are authored inside each half: no detached reward layer.
	var half_height := 320.0
	var left_size := open_left_texture.get_size()
	var right_size := open_right_texture.get_size()
	var left_width := half_height * left_size.x / left_size.y
	var right_width := half_height * right_size.x / right_size.y
	draw_texture_rect(open_left_texture,
		Rect2(center + Vector2(-left_width, -half_height * 0.5),
			Vector2(left_width, half_height)), false)
	draw_texture_rect(open_right_texture,
		Rect2(center + Vector2(geode_pull, -half_height * 0.5),
			Vector2(right_width, half_height)), false)
