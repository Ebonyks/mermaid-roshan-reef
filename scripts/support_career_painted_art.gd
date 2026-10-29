class_name SupportCareerPaintedArt
extends RefCounted
## Authored pictures only. The existing surface owns all progress/input/timing.
const ROOT := "res://assets/opera/worlds/support_quality_20261019/"
var surface: Control
var textures: Dictionary = {}
var feedback := PaintedFeedbackArt.new()

func bind(owner_surface: Control) -> void:
	surface = owner_surface

func art(name: String) -> Texture2D:
	var path := name if name.begins_with("res://") else ROOT + name + ".png"
	if not textures.has(path):
		textures[path] = load(path) as Texture2D
	assert(textures[path] != null, "Missing painted support-career art: " + path)
	return textures[path] as Texture2D

func value(name: String) -> float:
	return float(surface.get(name))

func complete() -> bool:
	return bool(surface.get("completion_accepted"))

func picture(name: String, at: Vector2, side: float, alpha: float = 1.0) -> void:
	var texture := art(name)
	var extent := texture.get_size() * side / maxf(texture.get_width(), texture.get_height())
	surface.draw_texture_rect(texture, Rect2(at - extent * 0.5, extent), false,
		Color(1.0, 1.0, 1.0, alpha))

func progress_key(progress: float) -> int:
	return 3 if complete() or progress >= 0.999 else (2 if progress >= 0.5 else (1 if progress > 0.01 else 0))

func guide(at: Vector2, pressing: bool) -> void:
	var context := String(surface.get("visual_context"))
	var herd_guide := context == "push_farmer"
	if String(surface.get("visual_context")) == "magic_vanish":
		at = surface.call("_magic_vanish_wand_position", value("widget_fill"))
	if herd_guide:
		var group: Rect2 = surface.call("_long_push_group_rect", value("widget_fill"))
		# Demonstrate a legal belly grip below the three faces.
		at += Vector2(0.0, group.size.y * 0.28)
	if context == "target_farmer":
		var next: int = surface.call("_target_next_unplaced")
		if next >= 0:
			at = surface.call("_target_anchor_point", next)
	var side := 58.0 if pressing else 54.0
	var texture := art("res://assets/opera/worlds/widgets/widget_pipe_guide_hand.png")
	if herd_guide or context == "target_farmer":
		# A rigid side-pointing hand leaves all three faces readable.
		surface.draw_set_transform(at, -PI * 0.5)
		surface.draw_texture_rect(texture, Rect2(-Vector2(0.455, 0.91) * side,
			Vector2.ONE * side), false)
		surface.draw_set_transform(Vector2.ZERO)
		return
	surface.draw_texture_rect(texture, Rect2(at - Vector2(0.455, 0.91) * side,
		Vector2.ONE * side), false)

func pearls(count: int, earned: int, y: float = 0.08) -> void:
	for index in range(count):
		var at := Vector2(surface.size.x * 0.5 + (float(index) - float(count - 1) * 0.5) * 27.0,
			surface.size.y * y)
		feedback.pearl(surface, at, "full" if index < earned else "empty", 23.0)

func patient_rect() -> Rect2:
	var side := minf(surface.size.y * 0.96, surface.size.x * 0.68)
	return Rect2(surface.size * Vector2(0.50, 0.53) - Vector2.ONE * side * 0.5, Vector2.ONE * side)

func patient(bandage: bool, progress: float) -> void:
	var destination := patient_rect()
	var name := "widget_bandage_doctor_" if bandage else "widget_cast_doctor_"
	surface.draw_texture_rect(art(name + str(progress_key(progress))), destination, false)
	pearls(3, progress_key(progress))
	surface.set("last_specialist_subject_route", "doctor_starfish_patient")
	surface.set_meta("support_painted_route", "doctor_bandage" if bandage else "doctor_cast")

func doctor_trace_point(progress: float) -> Vector2:
	var destination := patient_rect()
	# Follow the exposed arm's real diagonal contour; the reward/trace rules stay on the surface.
	var amount := clampf(progress, 0.0, 1.0)
	var uv := Vector2(lerpf(0.79, 0.93, amount), 0.42 + sin(amount * TAU * 3.0) * 0.065)
	return destination.position + destination.size * uv

func basin() -> void:
	var amount := value("widget_fill")
	var washing := bool(surface.get("held")) and not complete()
	var state := "off" if not washing or complete() else ("running" if amount < 0.24 or amount > 0.85 else "foamy")
	var side := minf(surface.size.y * 0.96, surface.size.x * 0.72)
	var center := surface.size * Vector2(0.5, 0.53)
	picture("widget_basin_doctor_" + state, center, side)
	var key := 0 if not washing else (1 if amount < 0.24 or amount > 0.85 else 2 + (int(amount * 12.0) % 2))
	var hands_side := minf(220.0, side * 0.72)
	var palms := center + Vector2(0.0, -side * 0.025)
	var hands_center := palms + Vector2(0.0, hands_side * 0.045)
	picture("widget_hands_doctor_" + str(key), hands_center, hands_side)
	if washing and amount > 0.24:
		picture("res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png",
			palms + Vector2(side * 0.13, -side * 0.07), side * 0.16, 0.70)
	pearls(4, 4 if complete() else mini(3, int(amount * 4.0)))
	surface.set("last_specialist_subject_route", "doctor_basin")
	surface.set_meta("support_painted_route", "doctor_wash")
	surface.set_meta("support_painted_key", key)

func scanner(at: Vector2, radius: float, found: bool) -> void:
	var side := radius * 3.3
	# Lens centre measured on the registered whole scanner, not the handle/canvas centre.
	var center := at - (Vector2(0.5, 0.36) - Vector2.ONE * 0.5) * side
	picture("widget_xray_scanner_" + ("found" if found else "idle"), center, side)

func portal() -> void:
	var progress := value("widget_fill")
	var center: Vector2 = surface.call("_portal_center")
	var radius: float = surface.call("_portal_radius")
	var key := 3 if complete() or progress >= 0.999 else (2 if progress >= 0.5 else (1 if progress > 0.04 else 0))
	picture("widget_portal_magician_ring_" + str(key), center, radius * 3.0)
	# Each complete source has the same fixed rim and a genuinely changing mist aperture.
	surface.set("last_contextual_draw_route", "portal:" + String(surface.get("visual_context")))
	surface.set("last_portal_layer_order", "doorway>aperture")
	if complete() or progress >= 0.999:
		picture("widget_portal_magician_overlay", center + Vector2(radius * 0.20, -radius * 0.12), radius * 0.40)
		surface.set("last_portal_layer_order", "doorway>aperture>glow")
	surface.set_meta("support_painted_route", "magician_portal")

func rope_rect() -> Rect2:
	var width := minf(surface.size.x * 0.86, surface.size.y * 1.9)
	var extent := Vector2(width, width * 0.25)
	return Rect2(surface.size * Vector2(0.5, 0.52) - extent * 0.5, extent)

func rope_point(progress: float) -> Vector2:
	var destination := rope_rect()
	var amount := clampf(progress, 0.0, 1.0)
	return destination.position + destination.size * Vector2(lerpf(0.075, 0.925, amount),
		0.40 + (1.0 - pow(2.0 * amount - 1.0, 2.0)) * 0.34)

func rope() -> void:
	var reference := rope_rect()
	var amount := value("trace_journey")
	var key := 2 if complete() or amount >= 0.999 else (1 if amount >= 0.45 else 0)
	# Common POT canvas pads the exact original rope by256x64; doubled whole
	# destination preserves its original visible body, sockets and input path.
	var destination := Rect2(reference.get_center() - reference.size, reference.size * 2.0)
	surface.draw_texture_rect(art("widget_rope_magician_" + str(key)), destination, false)
	pearls(3, progress_key(amount))
	surface.set_meta("support_painted_route", "magician_rope")
	surface.set_meta("support_painted_key", key)


func garden() -> void:
	var extent := Vector2(surface.size.x * 1.12, surface.size.y * 1.12)
	var texture := art("widget_seed_bed")
	var factor := minf(extent.x / texture.get_width(), extent.y / texture.get_height())
	var bed_size := texture.get_size() * factor
	surface.draw_texture_rect(texture, Rect2(surface.size * Vector2(0.5, 0.47) - bed_size * 0.5, bed_size), false)
	var growth: Array = surface.get("garden_growth")
	var planted := int(surface.get("garden_planted"))
	for index in range(growth.size()):
		var at: Vector2 = surface.call("_garden_hole_point", index)
		var hole_side := minf(surface.size.x, surface.size.y) * 0.21
		if index == planted and planted < growth.size():
			feedback.invitation(surface, at, hole_side * 1.20, int(value("demo_t") * 4.0) % 4)
		picture("widget_soil_hole", at, hole_side)
		var amount := float(growth[index])
		if amount > 0.0:
			var name := "widget_sprout_seed" if amount < 0.20 else ("widget_sprout_sprout" if amount < 0.88 else "widget_sprout_flower_" + str(index))
			var side := minf(surface.size.x, surface.size.y) * (0.12 if amount < 0.20 else 0.29)
			# Socket at bottom centre of the complete padded plant; no stem scaling or tint.
			picture(name, at - Vector2(0.0, side * 0.40), side)
	if planted < growth.size():
		var at: Vector2 = surface.get("garden_seed_pos")
		picture("widget_sprout_seed", at, maxf(50.0, minf(surface.size.x, surface.size.y) * 0.22))
	surface.set_meta("support_painted_route", "farmer_plant")

func herd() -> void:
	var finish: Vector2 = surface.call("_long_push_end")
	var amount := value("widget_fill")
	var side := minf(surface.size.y * 0.72, surface.size.x * 0.28)
	var group: Rect2 = surface.call("_long_push_group_rect", amount)
	var group_side := maxf(group.size.x, group.size.y) * 1.20
	# Same native hoof/floor baseline at both ends of the original input lane.
	var floor_y := finish.y + group_side * 0.334
	var gate_center := Vector2(finish.x, floor_y - side * 0.386)
	picture("widget_barn_gate_" + ("open" if amount >= 0.98 or complete() else "closed"), gate_center, side)
	var key := "b" if amount > 0.0 and amount < 0.999 and int(amount * 12.0) % 2 == 1 else "a"
	# Two complete authored step poses, with fixed heads and changing hoof support.
	# Their measured opaque footprint stays within the old group rectangle.
	picture("widget_herd_farmer_" + key, group.get_center(), group_side)
	surface.set("last_contextual_draw_route", "push:push_farmer")
	surface.set_meta("support_painted_route", "farmer_herd")
	surface.set_meta("support_painted_key", key)


func picnic() -> void:
	var target: Vector2 = surface.call("_farm_target_center")
	var side := minf(surface.size.y * 0.96, surface.size.x * 0.64)
	var state := "catch"
	if bool(surface.get("farm_complete")) or complete():
		state = "happy"
	elif value("farm_munch_t") > 0.0:
		state = "chew" if value("farm_munch_t") > 0.20 else "happy"
	# Whole group anchored by the central pig's painted open mouth.
	var mouth_uv := Vector2(0.51, 0.31)
	picture("widget_target_farmer_mover_" + state,
		target - (mouth_uv - Vector2.ONE * 0.5) * side, side)
	pearls(4, int(surface.get("farm_landed")))
	surface.set("last_target_subject_route", "target_farmer")
	surface.set("last_specialist_subject_route", "farm_pig_target")
	surface.set_meta("support_painted_route", "farmer_picnic")

func picnic_targets() -> void:
	var pose: Dictionary = surface.call("_target_subject_pose")
	var at: Vector2 = pose.get("centre", surface.size * 0.5)
	var side: float = float(pose.get("extent", surface.size.y * 0.94))
	picture("widget_target_farmer_mover_happy", at, side)
	var placed: Array = surface.get("target_placed")
	var animation: Array = surface.get("target_piece_anim")
	var next: int = surface.call("_target_next_unplaced")
	for index in range(placed.size()):
		var anchor: Vector2 = surface.call("_target_anchor_point", index)
		var bounds: Rect2 = surface.call("_target_piece_rect", index)
		if not placed[index]:
			feedback.invitation(surface, anchor, bounds.size.x * 0.82,
				int(value("demo_t") * 4.0) % 4 if index == next else 0)
			continue
		var settle := clampf(1.0 - float(animation[index]) / 0.42, 0.0, 1.0)
		var texture: Texture2D = surface.call("_target_piece_texture", index)
		assert(texture != null)
		var whole := texture.get_size() * bounds.size.x / maxf(texture.get_width(), texture.get_height())
		var center := anchor - Vector2(0.0, sin(settle * PI) * 4.0)
		surface.draw_texture_rect(texture, Rect2(center - whole * 0.5, whole), false)
	surface.set("last_target_subject_route", "target_farmer")
	surface.set_meta("support_painted_route", "farmer_picnic_targets")

func lanes() -> void:
	var count := int(surface.get("choice_count"))
	var target := int(surface.get("target_choice"))
	var magician := String(surface.get("visual_context")) == "lanes_magician"
	var doctor := String(surface.get("visual_context")) == "lanes_doctor"
	var from := int(surface.get("shuffle_from"))
	var shuffle := value("shuffle_t") > 0.0 and from >= 0 and magician
	var side := minf(surface.size.x / float(count + 1), surface.size.y * 0.58)
	for index in range(count):
		var at: Vector2 = surface.call("_lane_center", index)
		if shuffle and index in [target, from]:
			continue
		if index == target and (value("choice_flash") > 0.0 or bool(surface.get("demo_active")) or complete()):
			feedback.invitation(surface, at, side * 1.18, int(value("demo_t") * 4.0) % 4)
		if doctor:
			var states := ["concerned", "sleepy", "happy_cap"]
			picture("widget_find_doctor_" + String(states[index % 3]), at, side)
		elif magician:
			picture("widget_hat_magician_" + str(index % 3), at, side)
		else:
			var texture: Texture2D = surface.get("widget_mover")
			var banner := texture != null and texture.resource_path.ends_with("castle_banner_rainbow.png")
			picture("res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png" if banner else
				"res://assets/opera/worlds/props/goal_painter.png", at, side)
	if shuffle:
		var amount := clampf(1.0 - value("shuffle_t") / 1.5, 0.0, 1.0)
		var eased := amount * amount * (3.0 - 2.0 * amount)
		var start: Vector2 = surface.call("_lane_center", from)
		var finish: Vector2 = surface.call("_lane_center", target)
		var main := start.lerp(finish, eased) - Vector2(0.0, sin(eased * PI) * 64.0)
		var decoy := finish.lerp(start, eased) + Vector2(0.0, sin(eased * PI) * 40.0)
		picture("widget_hat_magician_" + str(from % 3), decoy, side)
		picture("widget_hat_magician_" + str(target % 3), main, side)
		feedback.invitation(surface, main, side * 1.15, int(value("demo_t") * 4.0) % 4)
	surface.set_meta("support_painted_route", "magician_hats" if magician else ("doctor_find" if doctor else "painter_gallery"))

func painting_rect() -> Rect2:
	var texture: Texture2D = surface.get("paint_reveal_texture")
	var side := minf(surface.size.x * 0.66, surface.size.y * 0.96)
	var extent := Vector2.ONE * side
	if texture != null:
		extent = texture.get_size() * side / maxf(texture.get_width(), texture.get_height())
	return Rect2(surface.size * 0.5 - extent * 0.5, extent)

func paint_window() -> Rect2:
	var destination := painting_rect()
	var texture: Texture2D = surface.get("paint_reveal_texture")
	if texture != null and texture.resource_path.ends_with("goal_painter.png"):
		return Rect2(destination.position + destination.size * Vector2(105.0, 106.0) / 512.0,
			destination.size * Vector2(301.0, 315.0) / 512.0)
	return destination

func clipped_cloud(texture: Texture2D, destination: Rect2, window: Rect2, alpha: float = 1.0) -> void:
	var clipped := destination.intersection(window)
	if not clipped.has_area():
		return
	var uv := Rect2((clipped.position - destination.position) / destination.size * texture.get_size(),
		clipped.size / destination.size * texture.get_size())
	# Native full cloud is occluded by the authored canvas/frame boundary, never deformed.
	surface.draw_texture_rect_region(texture, clipped, uv, Color(1.0, 1.0, 1.0, alpha))

func paint() -> void:
	var texture: Texture2D = surface.get("paint_reveal_texture")
	assert(texture != null)
	surface.draw_texture_rect(texture, painting_rect(), false)
	var window := paint_window()
	var cells: Array = surface.get("paint_cells")
	var positions: Array[Vector2] = [Vector2(0.18,0.16), Vector2(0.76,0.14),
		Vector2(0.47,0.43), Vector2(0.08,0.78), Vector2(0.88,0.72), Vector2(0.47,0.92)]
	var totals: Array[int] = [0,0,0,0,0,0]
	var cleared: Array[int] = [0,0,0,0,0,0]
	# Existing60touch cells still own all earning. Their spatial regions fade
	# six whole irregular puffs, rather than repeating a puff sixty times.
	for row in range(6):
		for col in range(10):
			var normalized := Vector2((float(col)+0.5)/10.0,(float(row)+0.5)/6.0)
			var nearest := 0
			var distance := INF
			for index in range(positions.size()):
				var candidate := normalized.distance_squared_to(positions[index])
				if candidate < distance:
					distance = candidate
					nearest = index
			totals[nearest] += 1
			if cells[row * 10 + col]:
				cleared[nearest] += 1
	if not bool(surface.get("paint_complete")):
		var scales: Array[float] = [1.05,0.94,1.12,1.00,1.12,1.07]
		for index in range(positions.size()):
			var alpha := 1.0 - float(cleared[index]) / maxf(1.0,float(totals[index]))
			if alpha <= 0.001:
				continue
			var side := maxf(window.size.x,window.size.y) * scales[index]
			var center := window.position + window.size * positions[index]
			clipped_cloud(art("widget_paint_cloud_" + str(index)),
				Rect2(center - Vector2.ONE * side * 0.5,Vector2.ONE * side),window,alpha)
	var required: int = surface.call("_paint_required_cells")
	pearls(8,mini(8,int(8.0 * value("paint_covered") / maxf(1,required))),0.94)
	surface.set_meta("support_painted_route", "painter_cloud_reveal")


