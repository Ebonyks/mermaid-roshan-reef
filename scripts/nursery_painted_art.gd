class_name NurseryPaintedArt
extends RefCounted
## Drawing/cache only. Existing surfaces and world own every input/progress/save.

const ROOT := "res://assets/opera/worlds/nursery_quality_20261019/"
const BOTTLE_NIPPLE_UV := Vector2(0.5, 25.0 / 256.0)
const BOTTLE_LABEL := [Vector2(139, 142), Vector2(152, 144), Vector2(163, 151),
	Vector2(170, 162), Vector2(171, 176), Vector2(167, 190), Vector2(157, 200),
	Vector2(144, 204), Vector2(130, 201), Vector2(118, 194), Vector2(110, 181),
	Vector2(109, 167), Vector2(113, 155), Vector2(124, 146)]
var surface: Control
var textures: Dictionary = {}

func bind(owner_surface: Control) -> void:
	surface = owner_surface

func art(name: String) -> Texture2D:
	if not textures.has(name):
		textures[name] = load(ROOT + name + ".png") as Texture2D
	return textures[name] as Texture2D

func picture(name: String, destination: Rect2) -> void:
	var texture := art(name)
	if texture != null:
		surface.draw_texture_rect(texture, destination, false)

func wash_rect() -> Rect2:
	var side := minf(surface.size.y, surface.size.x * 0.70)
	return Rect2((surface.size - Vector2.ONE * side) * 0.5, Vector2.ONE * side)

func draw_wash() -> void:
	surface.set_meta("nursery_painted_draw_route", "whole_connected_wash")
	var fill := clampf(float(surface.get("widget_fill")), 0.0, 1.0)
	var states := ["ready", "wet", "rub_palm", "rub_palm02", "rub_back", "rinse", "clean"]
	var index := clampi(floori(fill * 6.0), 0, 6)
	picture("wash_" + String(states[index]), wash_rect())

func crib_rect(index: int) -> Rect2:
	var center: Vector2 = surface.call("_nursery_baby_center", index)
	var side := minf(surface.size.x * 0.255, surface.size.y * 0.45)
	return Rect2(center - Vector2(side * 0.5, side * 0.47), Vector2.ONE * side)

func crib_front(destination: Rect2) -> void:
	# Same exact authored front rail/legs, never a second unrelated sticker.
	var source := Rect2(0, 330, 512, 182)
	surface.draw_texture_rect_region(art("crib"),
		Rect2(destination.position + Vector2(0, 330.0 / 512.0 * destination.size.y),
			Vector2(destination.size.x, 182.0 / 512.0 * destination.size.y)), source)

func draw_feed() -> void:
	surface.set_meta("nursery_painted_draw_route", "registered_bottle_and_crib")
	for index in range(3):
		var center: Vector2 = surface.call("_nursery_baby_center", index)
		var crib := crib_rect(index)
		picture("crib", crib)
		surface.call("_draw_nursery_baby", index, center,
			minf(surface.size.x, surface.size.y) * 0.29)
		crib_front(crib)
	var active := bool(surface.get("held")) or bool(surface.get("completion_accepted"))
	var pose: Dictionary = surface.call("_nursery_feed_bottle_pose", active)
	var side := minf(surface.size.x, surface.size.y) * 0.34
	var tip: Vector2 = pose["position"]
	surface.draw_set_transform(tip, float(pose["rotation"]))
	var destination := Rect2(-BOTTLE_NIPPLE_UV * side, Vector2.ONE * side)
	var full: Texture2D = surface.get("nursery_bottle_texture")
	if full != null:
		_draw_bottle(full, destination, float(pose["remaining"]))
	surface.draw_set_transform(Vector2.ZERO)

func _bottle_region(texture: Texture2D, source: Rect2, destination: Rect2) -> void:
	if source.size.x <= 0.0 or source.size.y <= 0.0:
		return
	surface.draw_texture_rect_region(texture,
		Rect2(destination.position + source.position / 256.0 * destination.size,
			source.size / 256.0 * destination.size), source)

func _draw_bottle(full: Texture2D, destination: Rect2, remaining: float) -> void:
	# Disjoint source regions: translucent empty glass must REPLACE milk pixels,
	# never alpha-blend on top of them. The original exterior/nipple stays exact.
	for fixed: Rect2 in [Rect2(0, 0, 256, 112), Rect2(0, 112, 83, 114),
			Rect2(173, 112, 83, 114), Rect2(0, 226, 256, 30)]:
		_bottle_region(full, fixed, destination)
	var split := lerpf(112.0, 226.0, 1.0 - clampf(remaining, 0.0, 1.0))
	_bottle_region(art("bottle_empty"), Rect2(83, 112, 90, split - 112.0), destination)
	_bottle_region(full, Rect2(83, split, 90, 226.0 - split), destination)
	# Only the source-painted medallion is overlaid; the rectangular corners
	# around it must not carry the old milk through the empty state.
	var vertices := PackedVector2Array()
	var uvs := PackedVector2Array()
	for point: Vector2 in BOTTLE_LABEL:
		vertices.append(destination.position + point / 256.0 * destination.size)
		uvs.append(point / 256.0)
	surface.draw_polygon(vertices, PackedColorArray([Color.WHITE]), uvs, full)

func draw_bedtime() -> void:
	surface.set_meta("nursery_painted_draw_route", "three_whole_quilt_keys")
	for index in range(3):
		var center: Vector2 = surface.call("_nursery_baby_center", index)
		var crib := crib_rect(index)
		picture("crib", crib)
		surface.call("_draw_nursery_baby", index, center - Vector2(0, surface.size.y * 0.04),
			minf(surface.size.x, surface.size.y) * 0.27)
		crib_front(crib)
		var progress: Array = surface.get("nursery_blanket_progress")
		var tucked: Array = surface.get("nursery_blankets_tucked")
		var amount := float(progress[index])
		var state := "tucked" if bool(tucked[index]) else ("half" if amount >= 0.35 else "folded")
		var width := crib.size.x * 0.54
		var top := float(surface.call("_nursery_blanket_top", index))
		picture("quilt_" + state,
			Rect2(Vector2(center.x - width * 0.5, top), Vector2.ONE * width))

func draw_burp() -> void:
	surface.set_meta("nursery_painted_draw_route", "painted_hand_on_swaddle")
	var timer := float(surface.get("nursery_burp_pat_t"))
	var amount := sin(clampf(1.0 - timer / 0.42, 0.0, 1.0) * PI) if timer > 0.0 else 0.0
	var center: Vector2 = surface.call("_nursery_baby_center", 1)
	# Source contour remains whole; a rigid response never squashes the baby.
	surface.draw_set_transform(center + Vector2(0, amount * 3.0), -0.025 * amount)
	surface.call("_draw_nursery_baby", 1, Vector2.ZERO,
		minf(surface.size.x, surface.size.y) * 0.52)
	surface.draw_set_transform(Vector2.ZERO)
	var contact: Vector2 = surface.call("_nursery_burp_hand_point", amount)
	var side := minf(surface.size.x, surface.size.y) * 0.38
	picture("pat_hand", Rect2(contact - Vector2(0.02, 0.37) * side, Vector2.ONE * side))

func draw_guide(at: Vector2, pressing: bool) -> void:
	var side := 58.0 if pressing else 54.0
	var rotation := 0.0
	if surface.has_method("_is_nursery_feed_context"):
		var context := String(surface.get("visual_context"))
		if context in ["nursery_bedtime", "push_nursery", "nursery_burp"]:
			# Point from below the cloth/back so the palm never covers a face.
			rotation = PI
		elif context in ["nursery_feed", "pour_nursery"]:
			rotation = PI * 0.5
	else:
		side = 45.0
		rotation = -PI * 0.5 if at.x > surface.size.x * 0.65 else PI * 0.5
	surface.draw_set_transform(at, rotation)
	picture("guide_hand", Rect2(-Vector2(0.436523, 0.986328) * side, Vector2.ONE * side))
	surface.draw_set_transform(Vector2.ZERO)
