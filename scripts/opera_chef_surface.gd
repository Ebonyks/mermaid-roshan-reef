class_name OperaChefSurface
extends OperaGestureSurface
## Chapter Two kitchen: separate mixing plinth, cake platform, rack and oven.
## Input, source regions and the wordless demonstration use room coordinates.

const Cake := preload("res://scripts/chapter_two_giant_cake_2d.gd")
const PLATFORM := Vector2(1068, 337)
const MIXING_PLINTH := Vector2(400, 365)
const BOWL_SCALE := 0.20
const CAKE_SCALE := 0.20
const EMPTY_BOWL := "res://assets/chapter2/birthday/chef_empty_shell_bowl_v1.png"
const BATTER_CAVITY: Array[Vector2] = [
	Vector2(99, 449), Vector2(141, 359), Vector2(204, 305), Vector2(332, 266),
	Vector2(481, 252), Vector2(648, 270), Vector2(787, 352), Vector2(879, 449),
	Vector2(890, 530), Vector2(804, 623), Vector2(651, 669), Vector2(444, 698),
	Vector2(275, 665), Vector2(160, 609), Vector2(96, 520),
]
var art_cache: Dictionary = {}


func _art(path: String) -> Texture2D:
	if not art_cache.has(path):
		art_cache[path] = load(path) as Texture2D if ResourceLoader.exists(path) else null
	return art_cache[path] as Texture2D


func _stage_rect(bottom: float, factor: float) -> Rect2:
	var contact := MIXING_PLINTH if mode in ["pourt", "circle"] else PLATFORM
	return Rect2(contact - Vector2(512.0 * factor, bottom * factor),
		Vector2.ONE * 1024.0 * factor)


func _draw_stage(path: String, bottom: float, factor: float) -> void:
	var texture := _art(path)
	if texture != null:
		draw_texture_rect(texture, _stage_rect(bottom, factor), false)


func _draw_transition(before: String, after: String, progress: float,
		bottom: float, factor: float) -> void:
	# Disjoint source regions: no double-painted full cake under the result.
	var destination := _stage_rect(bottom, factor)
	var split := 1024.0 * (1.0 - clampf(progress, 0.0, 1.0))
	for row: Array in [[before, 0.0, split], [after, split, 1024.0 - split]]:
		var texture := _art(String(row[0]))
		var height := float(row[2])
		if texture != null and height > 0.01:
			var source := Rect2(0.0, float(row[1]), 1024.0, height)
			draw_texture_rect_region(texture, Rect2(destination.position
				+ Vector2(0, source.position.y * factor), source.size * factor), source)


func _draw_batter_transition(before: String, after: String, progress: float) -> void:
	var amount := clampf(progress, 0.0, 1.0)
	if amount >= 1.0:
		_draw_stage(after, 909.0, BOWL_SCALE)
		return
	_draw_stage(before, 909.0, BOWL_SCALE)
	var texture := _art(after)
	if texture == null or amount <= 0.0:
		return
	# Only native batter pixels enter the existing cavity. The shell and spoon
	# keep their complete authored contours throughout the pour/stir.
	var top := lerpf(700.0, 250.0, amount)
	var reveal := PackedVector2Array([Vector2(0, top), Vector2(1024, top),
		Vector2(1024, 1024), Vector2(0, 1024)])
	var destination := _stage_rect(909.0, BOWL_SCALE)
	for clipped: PackedVector2Array in Geometry2D.intersect_polygons(PackedVector2Array(BATTER_CAVITY), reveal):
		var vertices := PackedVector2Array()
		var uvs := PackedVector2Array()
		for point: Vector2 in clipped:
			vertices.append(destination.position + point * BOWL_SCALE)
			uvs.append(point / 1024.0)
		draw_polygon(vertices, PackedColorArray([Color.WHITE]), uvs, texture)


func _draw() -> void:
	last_widget_ground_route = "kitchen_station"
	match mode:
		"pourt":
			_draw_batter_transition(EMPTY_BOWL, Cake.BATTER_UNSTIRRED_TEXTURE, pour_level)
			var pitcher := _pour_pitcher_rect()
			draw_set_transform(pitcher.get_center(), _pour_pitcher_rotation())
			if widget_mover != null:
				draw_texture_rect(widget_mover, Rect2(-pitcher.size * 0.5, pitcher.size), false)
			draw_set_transform(Vector2.ZERO)
			if _pour_stream_active() and pour_level < 1.0:
				draw_line(_pour_spout_point(), _pour_landing_point(), Color("#f5cf85"), 6.0, true)
			last_specialist_subject_route = "chef_platform_pour"
		"circle":
			# Continuous feedback comes from the whisk at the finger's angle.
			# The complete authored swirl replaces the ribbons at the earned
			# milestone; a half-ribbon/half-swirl wipe breaks their fluid shape.
			_draw_stage(Cake.BATTER_STIRRED_TEXTURE if completion_accepted
				else Cake.BATTER_UNSTIRRED_TEXTURE, 909.0, BOWL_SCALE)
			var whisk_tip := _circle_pivot() + Vector2(cos(crank_rotation) * 30.0,
				sin(crank_rotation) * 16.0)
			if widget_mover != null:
				# The whisk's wire end stays in the bowl; the entire bowl never spins.
				draw_set_transform(whisk_tip, 0.0, Vector2(-1, 1))
				draw_texture_rect(widget_mover, Rect2(-71, -14, 84, 84), false)
				draw_set_transform(Vector2.ZERO)
			last_contextual_draw_route = "crank:crank_chef"
		"oven":
			_draw_oven(size * 0.5)
			if completion_accepted:
				_draw_baked_rows()
		"tap":
			_draw_stack()
		"swipe":
			_draw_transition(Cake.STACKED_UNFROSTED_TEXTURE, Cake.FROSTED_RAINBOW_TEXTURE,
				trace_journey, 1013.0, CAKE_SCALE)
			var guide := _trace_path_points(1.0)
			draw_polyline(guide, Color(1.0, 0.92, 0.76, 0.48), 4.0, true)
			if held and trace_engaged:
				# Feedback follows this event's finger immediately; earned frosting
				# remains ordered and bounded by actual travel along the cake.
				draw_circle(pointer_pos, 5.0, Color("#fff1bd"))
			last_trace_subject_route = "trace_chef"
	if demo_active:
		_draw_demo_finger()


func _draw_stack() -> void:
	var placed := 0
	for done: bool in target_placed:
		if done:
			placed += 1
	var trays := _art(Cake.BAKED_TIERS_UNSTACKED_TEXTURE)
	for index in range(3):
		if index < target_placed.size() and target_placed[index]:
			continue
		var source := Cake.KITCHEN_TRAY_REGIONS[2 - index]
		var contact := _target_anchor_point(index)
		var bottom := Cake.KITCHEN_TRAY_ALPHA_BOTTOMS[2 - index]
		if trays != null:
			draw_texture_rect_region(trays,
				Rect2(contact - Vector2(512.0, bottom - source.position.y) * 0.14,
					source.size * 0.14), source)
	if placed > 0:
		var texture := _art(Cake.STACKED_UNFROSTED_TEXTURE)
		var destination := _stage_rect(1013.0, CAKE_SCALE)
		# Source rows alone would slice through the next tier. Reuse the complete
		# blue/yellow top from the same baked rounds to cap each earned pair.
		var top: float = [657.0, 415.0, 0.0][clampi(placed - 1, 0, 2)]
		var source := Rect2(0, top, 1024, 1024.0 - top)
		if texture != null:
			draw_texture_rect_region(texture, Rect2(destination.position
				+ Vector2(0, top * CAKE_SCALE), source.size * CAKE_SCALE), source)
		if placed < 3 and trays != null:
			_draw_stack_cap(trays, destination, placed)


func _draw_baked_rows() -> void:
	var texture := _art(Cake.BAKED_TIERS_UNSTACKED_TEXTURE)
	if texture == null:
		return
	for index in range(3):
		var source := Cake.KITCHEN_TRAY_REGIONS[2 - index]
		var bottom := Cake.KITCHEN_TRAY_ALPHA_BOTTOMS[2 - index]
		draw_texture_rect_region(texture,
			Rect2(_target_anchor_point(index) - Vector2(512.0, bottom - source.position.y) * 0.14,
				source.size * 0.14), source)


func _draw_stack_cap(texture: Texture2D, destination: Rect2, placed: int) -> void:
	var source_center := Vector2(315, 695) if placed == 1 else Vector2(309, 426)
	var source_radius := Vector2(123, 51) if placed == 1 else Vector2(94, 43)
	var target_center := Vector2(512, 657) if placed == 1 else Vector2(512, 415)
	var target_radius := Vector2(279, 54) if placed == 1 else Vector2(230, 49)
	var vertices := PackedVector2Array()
	var uvs := PackedVector2Array()
	for sample in range(48):
		var circle := Vector2.from_angle(float(sample) * TAU / 48.0)
		vertices.append(destination.position + (target_center + circle * target_radius) * CAKE_SCALE)
		uvs.append((source_center + circle * source_radius) / 1024.0)
	draw_polygon(vertices, PackedColorArray([Color.WHITE]), uvs, texture)


func _uses_anchored_targets() -> bool:
	return mode == "tap"


func _target_anchor_count() -> int:
	return 3


func _target_anchor_point(index: int) -> Vector2:
	return Vector2(802.0, [352.0, 309.0, 264.0][clampi(index, 0, 2)])


func _target_press(at: Vector2) -> void:
	var next := _target_next_unplaced()
	if next < 0:
		return
	var nearest := 0
	var nearest_distance := INF
	for index in range(3):
		var distance := at.distance_to(_target_anchor_point(index) - Vector2(0, 17))
		if distance < nearest_distance:
			nearest = index
			nearest_distance = distance
	if nearest != next or nearest_distance > 62.0:
		_target_rehint(at)
		return
	target_placed[next] = true
	feedback_positive = true
	feedback_t = 0.30
	feedback_anchor = at
	gesture.emit("tap", 1.0, 1.0)


func _circle_pivot() -> Vector2:
	return Vector2(400, 278)


func _circle_min_radius() -> float:
	return 12.0


func _crank_action_rect() -> Rect2:
	return Rect2(315, 234, 170, 88)


func _pour_bowl_rect() -> Rect2:
	return Rect2(320, 255, 160, 68)


func _pour_home_x() -> float:
	return 480.0


func _pour_x_bounds() -> Vector2:
	return Vector2(468, 492)


func _pour_pitcher_rect() -> Rect2:
	return Rect2(pour_x - 60.0, 180.0, 120.0, 110.0)


func _pour_pitcher_hit_rect() -> Rect2:
	return _pour_pitcher_rect().grow(12.0)


func _pour_pitcher_rotation() -> float:
	return -pour_tilt * 1.05


func _pour_spout_point() -> Vector2:
	var pitcher := _pour_pitcher_rect()
	var lip := (Vector2(0.086, 0.312) - Vector2.ONE * 0.5) * pitcher.size
	return pitcher.get_center() + lip.rotated(_pour_pitcher_rotation())


func _pour_landing_point() -> Vector2:
	return Vector2(_pour_spout_point().x - 5.0, 300.0)


func _pour_fill_delta(tilt_flow: float, delta: float) -> float:
	# One deliberate short hold; the fading jug reserve never slows the last drop.
	return tilt_flow * delta / 3.5


func _oven_handle_rect() -> Rect2:
	return Rect2(590, 319, 100, 44)


func _oven_meter_rect() -> Rect2:
	return Rect2(592, 391, 98, 8)


func _draw_oven(_center: Vector2) -> void:
	# The actual painted hearth remains the sole oven. A small warm gauge and
	# door-local glow tell the child when to tap it, without a second oven card.
	var meter := _oven_meter_rect()
	draw_line(meter.position, meter.position + Vector2(meter.size.x, 0), Color("#59415f"), 8.0, true)
	draw_line(meter.position, meter.position + Vector2(meter.size.x * clampf(oven_t, 0, 1), 0), Color("#ffd77c"), 5.0, true)
	if oven_t >= 0.45:
		draw_arc(_oven_handle_rect().get_center(), 24.0, 0, TAU, 32, Color(1.0, 0.87, 0.56, 0.65), 3.0, true)
	last_specialist_subject_route = "chef_room_hearth"


func _trace_demo_point(progress: float) -> Vector2:
	var amount := clampf(progress, 0.0, 1.0)
	return Vector2(1068.0 + sin(amount * TAU * 1.5 - PI * 0.5) * 45.0,
		lerpf(181.0, 296.0, amount))


func _trace_progress_for_point(point: Vector2) -> float:
	return clampf(inverse_lerp(181.0, 296.0, point.y), 0, 1)


func _trace_start_hit_rect() -> Rect2:
	return Rect2(_trace_demo_point(trace_journey) - Vector2.ONE * 55.0, Vector2.ONE * 110.0)


func _trace_corridor_contains(point: Vector2) -> bool:
	var amount := _trace_progress_for_point(point)
	return point.y >= 173.0 and point.y <= 304.0 \
		and absf(point.x - _trace_demo_point(amount).x) <= 28.0


func _demo_finger_pose() -> Dictionary:
	if mode == "circle":
		var angle := -2.7 + fmod(demo_t, 3.0) * 2.0
		return {"at": _circle_pivot() + Vector2(cos(angle) * 42.0,
			sin(angle) * 24.0), "pressing": true}
	return super._demo_finger_pose()


func _load_widget_set() -> void:
	super._load_widget_set()
	# None of the copied family fills, stamps or success cards is rendered here.
	widget_overlay = null
	widget_stamp = null
	widget_shared = null
	if mode not in ["pourt", "circle"]:
		widget_mover = null
