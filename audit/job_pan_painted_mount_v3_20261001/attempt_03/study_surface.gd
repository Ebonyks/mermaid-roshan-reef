extends OperaGeologySurface
## Disposable visual study. Input/progress remain inherited production behavior.
var painted_study := false
var work_texture: Texture2D
var grain_texture: Texture2D
var open_left_texture: Texture2D
var open_right_texture: Texture2D

func _draw_work_surface() -> void:
	if not painted_study:
		super._draw_work_surface()
		return
	var ratio := work_texture.get_width() / float(work_texture.get_height())
	var fit_size := Vector2(860.0, 860.0 / ratio)
	draw_texture_rect(work_texture, Rect2(WORK_RECT.get_center() - fit_size * 0.5, fit_size), false)

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

func _draw_pan() -> void:
	if not painted_study:
		super._draw_pan()
		return
	var ratio := pan_texture.get_width() / float(pan_texture.get_height())
	var fit_size := Vector2(PAN_RECT.size.x, PAN_RECT.size.x / ratio)
	var rect := Rect2(PAN_RECT.get_center() + Vector2(pan_visual_x, 0.0) - fit_size * 0.5, fit_size)
	draw_texture_rect(pan_texture, rect, false)
	# The authored water basin occupies this normalized region; keep the source
	# and its alpha intact. Only game prop placement changes in this fixture.
	var water_center := rect.position + fit_size * Vector2(0.50, 0.44)
	var grain_count := maxi(3, 20 - floori(pan_wash * 17.0))
	for index: int in range(grain_count):
		var angle := float(index) * 2.399
		var radial := sqrt((float(index) + 0.5) / float(grain_count))
		var grain_pos := water_center + Vector2(cos(angle) * 122.0, sin(angle) * 31.0) * radial
		grain_pos.x += pan_visual_x * 0.12 + sin(float(index) + pan_visual_x * 0.02) * 6.0
		var grain_size := Vector2(15.0 * grain_texture.get_width() / float(grain_texture.get_height()), 15.0)
		draw_texture_rect(grain_texture, Rect2(grain_pos - grain_size * 0.5, grain_size), false)
	for index: int in range(pan_minerals):
		var mineral_size := Vector2(68.0 * crystals_texture.get_width() / float(crystals_texture.get_height()), 68.0)
		var base := water_center + Vector2(-82.0 + float(index) * 82.0, 20.0)
		_draw_ellipse(base + Vector2(0.0, 4.0), Vector2(27.0, 8.0), Color(0.22, 0.60, 0.65, 0.50), Color(0.57, 0.89, 0.88, 0.85), 2.0)
		draw_texture_rect(crystals_texture, Rect2(base - Vector2(mineral_size.x * 0.5, mineral_size.y), mineral_size), false)
