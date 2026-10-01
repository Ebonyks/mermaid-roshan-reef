extends OperaBoxingSurface
## Disposable appearance-only diagnostic subclass; all gameplay methods inherited.
var review_left: Texture2D = null
var review_right: Texture2D = null
func _draw_glove(hand: int) -> void:
	var texture: Texture2D = review_left if hand == 0 else review_right
	assert(texture != null)
	var at: Vector2 = glove_positions[hand]
	var depth: float = _glove_depth(hand)
	var scale_value: float = 0.92 + depth * 0.38
	if _impact_t > 0.0 and at.distance_to(_impact_position) < 130.0:
		scale_value += sin((_impact_t / 0.52) * PI) * 0.10
	var angle: float = (-0.08 if hand == 0 else 0.08) \
		+ clampf((pointer_pos.x - at.x) / maxf(1.0, size.x), -0.08, 0.08)
	# Each independently authored source already has its correct thumb direction.
	draw_set_transform(at, angle, Vector2(scale_value, scale_value))
	draw_texture_rect(texture, Rect2(-82.0,-91.0,164.0,164.0), false)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
