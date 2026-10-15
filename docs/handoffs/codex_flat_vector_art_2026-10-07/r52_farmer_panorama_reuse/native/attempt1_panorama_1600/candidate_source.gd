extends "res://scripts/opera_world_backdrop_2d.gd"
## R52 NONRUNTIME VISUAL FIT ONLY. Approved source bytes untouched.
var trial_mode := "preserve_lower"
var mapping_rows: Array[Dictionary] = []

func _draw_sky_lagoon_farmer() -> void:
	if trial_mode == "original":
		super._draw_sky_lagoon_farmer()
		return
	if sky_lagoon_tiles.size() != 4:
		return
	var half_width := size.x * 0.5
	var source_y := 448.0 if trial_mode == "centered" else 672.0
	var native_scale := size.x / 2048.0
	mapping_rows.clear()
	for row: int in range(2):
		var global_top := maxf(source_y, float(row) * 1024.0)
		var global_bottom := minf(source_y + 1152.0, float(row + 1) * 1024.0)
		if global_bottom <= global_top:
			continue
		var source := Rect2(0.0, global_top - float(row) * 1024.0,
			1024.0, global_bottom - global_top)
		for column: int in range(2):
			var destination := Rect2(float(column) * half_width,
				(global_top - source_y) * native_scale,
				half_width, source.size.y * native_scale)
			draw_texture_rect_region(sky_lagoon_tiles[row * 2 + column], destination, source)
			mapping_rows.append({"row": row, "column": column, "source": str(source), "destination": str(destination)})
	# Reuse the approved empty shell basket; preserve its source pixels and
	# avoid introducing a pig/corn/barn destination into the strawberry job.
	if farmer_basket_texture != null:
		var bounds := Rect2(983, 560, 114, 120)
		var source_size := farmer_basket_texture.get_size()
		var factor := minf(bounds.size.x / source_size.x, bounds.size.y / source_size.y)
		var drawn := source_size * factor
		# Preserve the existing ground support at bottom-center (1040, 680).
		var destination := Rect2(Vector2(bounds.get_center().x - drawn.x * 0.5,
			bounds.end.y - drawn.y), drawn)
		draw_texture_rect(farmer_basket_texture, destination, false)
