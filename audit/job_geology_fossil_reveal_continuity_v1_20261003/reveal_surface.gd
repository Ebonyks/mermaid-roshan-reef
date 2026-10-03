extends "res://audit/job_geology_painted_fracture_trial_v1_20261003/painted_fracture_surface.gd"
## NON_RUNTIME_REVEAL_HOME_STUDY: existing painted fracture material unchanged.
## Broken pieces are under the soil at their actual assembly homes throughout.
## Only home placement/underlying stage0 presentation change; inherited input,
## targets, margins, state format, progress and world completion remain intact.

func fossil_piece_home(index: int) -> Vector2:
	return Vector2(639.0 + float(clampi(index, 0, 2)) * 141.0, 400.0)

func _draw_fossil() -> void:
	if fossil_stage != 0:
		super._draw_fossil()
		return
	for index: int in range(3):
		_draw_fossil_piece(index,
			Rect2(fossil_piece_home(index) - FOSSIL_PIECE_SIZE * 0.5, FOSSIL_PIECE_SIZE))
	var cell_size := Vector2(FOSSIL_RECT.size.x / float(FOSSIL_GRID_COLS),
		FOSSIL_RECT.size.y / float(FOSSIL_GRID_ROWS))
	for row: int in range(FOSSIL_GRID_ROWS):
		for column: int in range(FOSSIL_GRID_COLS):
			var index: int = row * FOSSIL_GRID_COLS + column
			if not fossil_cleared[index] and _fossil_soil_texture != null:
				var source_cell := _fossil_soil_texture.get_size() \
					/ Vector2(FOSSIL_GRID_COLS, FOSSIL_GRID_ROWS)
				draw_texture_rect_region(_fossil_soil_texture,
					Rect2(FOSSIL_RECT.position + Vector2(column, row) * cell_size,
						cell_size), Rect2(Vector2(column, row) * source_cell, source_cell))
	if held:
		_draw_brush(pointer_pos)
