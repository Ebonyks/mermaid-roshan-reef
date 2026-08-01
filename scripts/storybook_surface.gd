class_name StorybookSurface
extends Control
# Resolution-independent pearl, shell and rainbow trim for shared menu cards.
# The detail is drawn once when a Control is built/resized, so it stays crisp
# without adding texture memory or continuous Mobile-renderer work.

var accent := Color(0.43, 0.30, 0.76, 1.0)
var compact := false
var rainbow_crest := true

func configure(next_accent: Color, next_compact: bool = false,
		next_rainbow_crest: bool = true) -> void:
	accent = next_accent
	compact = next_compact
	rainbow_crest = next_rainbow_crest
	queue_redraw()

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	resized.connect(queue_redraw)

func _draw() -> void:
	if size.x < 36.0 or size.y < 28.0:
		return
	var gold := Color(1.0, 0.78, 0.30, 0.92)
	var pearl := Color(0.82, 0.96, 1.0, 0.90)
	var glow := Color(1.0, 1.0, 1.0, 0.62)
	var inset := Rect2(Vector2(8.0, 7.0), size - Vector2(16.0, 14.0))
	var radius: float = minf(28.0 if compact else 42.0,
		minf(size.x, size.y) * 0.24)
	draw_arc(inset.position + Vector2(radius, radius), radius,
		PI, PI * 1.5, 16, glow, 2.0, true)
	draw_line(Vector2(radius + 8.0, 7.0),
		Vector2(size.x - radius - 8.0, 7.0), glow, 2.0, true)
	# Paired gold/pearl corner studs reproduce the prototype's jewelled rim
	# while keeping the content field quiet and readable.
	var stud_radius: float = 4.0 if compact else 6.0
	var stud_inset: float = 15.0 if compact else 20.0
	for center: Vector2 in [
		Vector2(stud_inset, stud_inset),
		Vector2(size.x - stud_inset, stud_inset),
		Vector2(stud_inset, size.y - stud_inset),
		Vector2(size.x - stud_inset, size.y - stud_inset)]:
		draw_circle(center, stud_radius + 2.0, accent.lerp(gold, 0.55))
		draw_circle(center, stud_radius, pearl)
		draw_circle(center - Vector2.ONE * stud_radius * 0.28,
			maxf(1.2, stud_radius * 0.28), Color.WHITE)
	if compact or not rainbow_crest or size.x < 220.0 or size.y < 90.0:
		return
	# A restrained stained-glass rainbow crown. It occupies only the top rim,
	# never the touch/content area.
	var crest_center := Vector2(size.x * 0.5, 10.0)
	var rainbow := [
		Color(1.0, 0.50, 0.55, 0.88),
		Color(1.0, 0.78, 0.30, 0.90),
		Color(0.52, 0.94, 0.78, 0.90),
		Color(0.50, 0.86, 1.0, 0.90),
		Color(0.78, 0.76, 0.98, 0.92)]
	for band in range(rainbow.size()):
		var band_radius: float = 34.0 - float(band) * 5.0
		draw_arc(crest_center, band_radius, PI, TAU, 24,
			rainbow[band], 5.0, true)
	draw_circle(crest_center, 8.0, accent.lerp(gold, 0.48))
	draw_circle(crest_center, 5.4, pearl)
	draw_circle(crest_center - Vector2(1.7, 1.7), 1.7, Color.WHITE)
