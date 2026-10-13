extends OperaGeologySurface
## Nonruntime R15 whole-source cue study. All inherited input/state/save functions unchanged.
const CUE_PATH := "res://assets/mg/star.png"
var cue_texture: Texture2D = load(CUE_PATH) as Texture2D

func _draw_geode() -> void:
	var center := GEODE_RECT.get_center()
	var seam_x := center.x
	var opened := geode_pull > 0.0
	if opened:
		_draw_ellipse(center + Vector2(geode_pull * 0.5, 0.0),
			Vector2(36.0 + geode_pull * 0.32, 122.0), Color("#291f48"),
			Color("#392958"), 8.0)
		if crystals_texture != null:
			draw_texture_rect(crystals_texture,
				Rect2(center + Vector2(geode_pull * 0.5 - 78.0, -84.0),
					Vector2(156.0, 168.0)), false)
		else:
			_draw_crystal_gallery(center + Vector2(geode_pull * 0.5, 18.0))
	var left_half := _geode_half_points(seam_x, center.y, -1.0, 0.0)
	var right_half := _geode_half_points(seam_x + geode_pull, center.y, 1.0, 0.0)
	draw_colored_polygon(left_half, Color("#65506e"))
	draw_colored_polygon(right_half, Color("#755c7d"))
	var left_outline := left_half.duplicate()
	left_outline.append(left_half[0])
	draw_polyline(left_outline, Color("#392958"), 12.0, true)
	var right_outline := right_half.duplicate()
	right_outline.append(right_half[0])
	draw_polyline(right_outline, Color("#392958"), 12.0, true)
	if not opened:
		draw_line(Vector2(seam_x, center.y - 130.0),
			Vector2(seam_x, center.y + 130.0), Color("#392958"), 9.0, true)
	if not opened:
		assert(cue_texture != null, "R15 source must load; no circle/halo artwork fallback")
		for index in range(GEODE_SEAM_SPOTS.size()):
			var spot: Vector2 = GEODE_SEAM_SPOTS[index]
			var alpha: float = 0.32 if geode_seams[index] else 1.0
			draw_texture_rect(cue_texture, Rect2(spot - Vector2(32, 32), Vector2(64, 64)),
				false, Color(1, 1, 1, alpha))

func marker_spot(index: int) -> Vector2:
	return GEODE_SEAM_SPOTS[index]
