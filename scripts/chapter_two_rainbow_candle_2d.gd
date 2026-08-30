class_name ChapterTwoRainbowCandle2D
extends Control

## Code-native storybook candle. The ordinary state is intentionally unlit;
## only the explicit Chapter 2 lighting plot enables the rainbow flame.

const RAINBOW_FLAME_BAND_COUNT := 8
const RAINBOW_FLAME_BODY_HEIGHT_RATIO := 0.74

var lit := false
var elapsed := 0.0


func setup(is_lit: bool) -> void:
	name = "ChapterTwoRainbowCandle"
	size = Vector2(150.0, 238.0)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_meta("plot_prop", "rainbow_candle")
	set_meta("ordinary_state", "unlit")
	set_meta("rainbow_flame_band_count", RAINBOW_FLAME_BAND_COUNT)
	set_meta("rainbow_flame_body_height_ratio",
		RAINBOW_FLAME_BODY_HEIGHT_RATIO)
	set_meta("flame_kind", "rainbow" if is_lit else "none")
	set_lit(is_lit)


func set_lit(is_lit: bool) -> void:
	lit = is_lit
	set_meta("lit", lit)
	set_meta("flame_kind", "rainbow" if lit else "none")
	set_process(lit)
	queue_redraw()


func _process(delta: float) -> void:
	if not lit:
		return
	elapsed += delta
	queue_redraw()


func _draw() -> void:
	var ink := Color("#402b58")
	# Soft contact shadow and shell-shaped birthday holder.
	_draw_ellipse_shape(Vector2(75.0, 222.0), Vector2(58.0, 10.0),
		Color(0.14, 0.08, 0.24, 0.24))
	draw_colored_polygon(PackedVector2Array([
		Vector2(18.0, 207.0), Vector2(32.0, 188.0),
		Vector2(118.0, 188.0), Vector2(132.0, 207.0),
		Vector2(112.0, 219.0), Vector2(38.0, 219.0),
	]), ink)
	draw_colored_polygon(PackedVector2Array([
		Vector2(24.0, 204.0), Vector2(36.0, 191.0),
		Vector2(114.0, 191.0), Vector2(126.0, 204.0),
		Vector2(108.0, 213.0), Vector2(42.0, 213.0),
	]), Color("#f5c96d"))
	for ridge_index in range(5):
		var ridge_x := 45.0 + float(ridge_index) * 15.0
		draw_line(Vector2(75.0, 194.0), Vector2(ridge_x, 210.0),
			Color("#fff0b0"), 2.0)

	# Rounded wax body with a thick navy-purple storybook contour.
	draw_rect(Rect2(39.0, 58.0, 72.0, 138.0), ink, true)
	draw_rect(Rect2(45.0, 62.0, 60.0, 130.0), Color("#fff2cb"), true)
	draw_circle(Vector2(75.0, 63.0), 30.0, Color("#fff2cb"))
	draw_arc(Vector2(75.0, 63.0), 33.0, PI, TAU, 30, ink, 6.0)
	# Rainbow wax bands identify the candle even while it is unlit.
	var bands: Array[Color] = [
		Color("#ef6d83"), Color("#f2a85c"), Color("#f2d66c"),
		Color("#72c99a"), Color("#66b8dc"), Color("#9d82d7"),
	]
	for band_index in range(bands.size()):
		draw_rect(Rect2(45.0, 83.0 + float(band_index) * 15.0,
			60.0, 11.0), bands[band_index], true)
	# Wax drips and the clearly dark, unlit wick.
	draw_circle(Vector2(56.0, 73.0), 8.0, Color("#fff2cb"))
	draw_rect(Rect2(51.0, 70.0, 10.0, 20.0), Color("#fff2cb"), true)
	draw_circle(Vector2(94.0, 72.0), 7.0, Color("#fff2cb"))
	draw_rect(Rect2(90.0, 69.0, 8.0, 16.0), Color("#fff2cb"), true)
	draw_line(Vector2(75.0, 57.0), Vector2(75.0, 39.0), ink, 5.0)
	draw_circle(Vector2(75.0, 38.0), 3.0, Color("#241b35"))
	if lit:
		_draw_rainbow_flame()


func _draw_rainbow_flame() -> void:
	var pulse := 1.0 + sin(elapsed * 4.2) * 0.035
	var centre := Vector2(75.0, 11.0)
	# One very large flame silhouette with nested rainbow bands. It is nearly
	# half the candle body's height, so the rainbow reads on a small phone.
	draw_circle(centre, 58.0 * pulse, Color(0.82, 0.68, 1.0, 0.16))
	var colours: Array[Color] = [
		Color("#ef5b72"), Color("#f49a4c"), Color("#f5d85b"),
		Color("#64cf8a"), Color("#4ec6d9"), Color("#5e86e8"),
		Color("#9a69dc"), Color("#fff5c8"),
	]
	var scales: Array[float] = [
		1.62, 1.42, 1.23, 1.05, 0.87, 0.69, 0.51, 0.29,
	]
	for band_index in range(colours.size()):
		var band_centre := centre + Vector2(0.0, float(band_index) * 1.25)
		_draw_flame_drop(band_centre, colours[band_index],
			scales[band_index] * pulse)


func _draw_flame_drop(centre: Vector2, colour: Color, scale_factor: float) -> void:
	var points := PackedVector2Array([
		centre + Vector2(0.0, -36.0) * scale_factor,
		centre + Vector2(20.0, -8.0) * scale_factor,
		centre + Vector2(17.0, 15.0) * scale_factor,
		centre + Vector2(0.0, 27.0) * scale_factor,
		centre + Vector2(-17.0, 15.0) * scale_factor,
		centre + Vector2(-20.0, -8.0) * scale_factor,
	])
	draw_colored_polygon(points, colour)


func _draw_ellipse_shape(centre: Vector2, radii: Vector2,
		colour: Color) -> void:
	var points := PackedVector2Array()
	for index in range(32):
		var angle := TAU * float(index) / 32.0
		points.append(centre + Vector2(
			cos(angle) * radii.x, sin(angle) * radii.y))
	draw_colored_polygon(points, colour)
