class_name ShellOrnament
extends Control
# Small Godot-native scallop crest shared by the storybook UI. It is drawn at
# runtime so the approved prototype language can scale to every menu without
# flattening a prototype screenshot into the game.

var fill := Color(0.80, 0.76, 1.0, 0.98)
var highlight := Color(0.94, 0.91, 1.0, 0.96)
var outline := Color(0.22, 0.14, 0.52, 1.0)
var pearl := Color(0.70, 0.97, 1.0, 1.0)

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	resized.connect(queue_redraw)

func _draw() -> void:
	if size.x <= 1.0 or size.y <= 1.0:
		return
	var hinge := Vector2(size.x * 0.5, size.y * 0.84)
	var radius := Vector2(size.x * 0.43, size.y * 0.69)
	var fan := PackedVector2Array([hinge])
	const ARC_STEPS := 28
	for step in range(ARC_STEPS + 1):
		var angle: float = lerpf(PI * 1.05, PI * 1.95, float(step) / ARC_STEPS)
		fan.append(hinge + Vector2(cos(angle) * radius.x, sin(angle) * radius.y))
	fan.append(hinge)
	draw_colored_polygon(fan, fill)
	draw_polyline(fan, outline, maxf(3.0, size.x * 0.035), true)
	for rib in range(1, 7):
		var rib_angle: float = lerpf(PI * 1.08, PI * 1.92, float(rib) / 7.0)
		var outer: Vector2 = hinge + Vector2(cos(rib_angle) * radius.x, sin(rib_angle) * radius.y)
		var inner: Vector2 = hinge.lerp(outer, 0.84)
		draw_line(hinge, inner, outline.lightened(0.12), maxf(2.0, size.x * 0.018), true)
	for lobe in range(6):
		var lobe_angle: float = lerpf(PI * 1.10, PI * 1.90, float(lobe) / 5.0)
		var lobe_center: Vector2 = hinge + Vector2(
			cos(lobe_angle) * radius.x * 0.88,
			sin(lobe_angle) * radius.y * 0.88)
		draw_circle(lobe_center, size.x * 0.035, highlight)
		draw_arc(lobe_center, size.x * 0.035, 0.0, TAU, 16, outline, maxf(1.5, size.x * 0.012), true)
	draw_circle(hinge, size.x * 0.105, outline)
	draw_circle(hinge, size.x * 0.072, pearl)
	draw_circle(hinge - Vector2(size.x * 0.021, size.x * 0.021), size.x * 0.018, Color.WHITE)
	# Five stained-glass bands turn the generic crest into the approved
	# shell-and-rainbow crown without relying on a low-resolution texture.
	var rainbow := [
		Color(1.0, 0.50, 0.55, 0.92), Color(1.0, 0.78, 0.30, 0.92),
		Color(0.52, 0.94, 0.78, 0.92), Color(0.50, 0.86, 1.0, 0.92),
		Color(0.78, 0.76, 0.98, 0.94)]
	for band in range(rainbow.size()):
		var band_radius: float = size.x * (0.29 - float(band) * 0.035)
		draw_arc(hinge, band_radius, PI * 1.12, PI * 1.88, 18,
			rainbow[band], maxf(2.0, size.x * 0.028), true)
