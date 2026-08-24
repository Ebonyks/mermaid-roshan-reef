class_name DayOneArtStudio
extends Control
## Level One's first art-room job: gather the loose supplies, scrub the
## counters, then wake the painted desk.  The room remains a picture-first
## Canvas2D scene; this node owns only temporary touch targets and effects.

const MATERIALS: Array[Dictionary] = [
	{"id": "brushes", "label": "loose brushes", "center": Vector2(215.0, 366.0),
		"hit_size": Vector2(190.0, 142.0), "color": Color(1.0, 0.72, 0.38)},
	{"id": "pink_paint", "label": "pink paint", "center": Vector2(352.0, 270.0),
		"hit_size": Vector2(164.0, 148.0), "color": Color(1.0, 0.48, 0.70)},
	{"id": "blue_paint", "label": "blue paint", "center": Vector2(790.0, 267.0),
		"hit_size": Vector2(172.0, 150.0), "color": Color(0.44, 0.84, 1.0)},
	{"id": "paint_cups", "label": "paint cups", "center": Vector2(928.0, 370.0),
		"hit_size": Vector2(182.0, 156.0), "color": Color(0.73, 0.60, 1.0)},
]
const GRIME: Array[Dictionary] = [
	{"id": "left_counter", "label": "left counter grime", "center": Vector2(170.0, 365.0),
		"hit_size": Vector2(260.0, 130.0), "radius": Vector2(106.0, 36.0)},
	{"id": "desk_counter", "label": "desk counter grime", "center": Vector2(512.0, 315.0),
		"hit_size": Vector2(282.0, 132.0), "radius": Vector2(116.0, 38.0)},
	{"id": "right_counter", "label": "right counter grime", "center": Vector2(854.0, 365.0),
		"hit_size": Vector2(255.0, 130.0), "radius": Vector2(104.0, 36.0)},
]
const DESK_CENTER := Vector2(512.0, 325.0)
const DESK_HIT_SIZE := Vector2(310.0, 158.0)
const SOURCE_CANVAS_SIZE := Vector2(1024.0, 576.0)
const ART_TO_STAGE := 1.25
const SPARKLE_COLORS: Array[Color] = [
	Color(1.0, 0.83, 0.38), Color(0.52, 0.94, 1.0),
	Color(1.0, 0.55, 0.76), Color(0.80, 0.68, 1.0),
]

var m: ReefMain
var _material_buttons: Dictionary = {}
var _grime_buttons: Dictionary = {}
var _desk_button: Button = null
var _pointer: Label = null
var _desk_glow: Label = null
var _pulse_time: float = 0.0
var _announcements_enabled: bool = true
var _customizer_open: bool = false


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	name = "DayOneArtStudio"
	position = Vector2.ZERO
	size = SOURCE_CANVAS_SIZE
	scale = Vector2.ONE * ART_TO_STAGE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 22
	_build_targets()
	_build_pointer()
	refresh_from_state()
	set_process(true)
	call_deferred("_announce_current_target")


func teardown() -> void:
	set_process(false)
	_customizer_open = false
	if is_inside_tree():
		queue_free()
	else:
		free()


func refresh_from_state() -> void:
	if m == null:
		return
	queue_redraw()
	for material_id: String in _material_buttons:
		var material_button: Button = _material_buttons[material_id] as Button
		var collected: bool = bool(m.day_one_art_collected_materials.get(
			material_id, false))
		material_button.visible = not collected
		material_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if not collected else Control.MOUSE_FILTER_IGNORE
	for grime_id: String in _grime_buttons:
		var grime_button: Button = _grime_buttons[grime_id] as Button
		var cleaned: bool = bool(m.day_one_art_cleaned_grime.get(grime_id, false))
		var materials_ready: bool = _all_materials_collected()
		grime_button.visible = materials_ready and not cleaned
		grime_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if not cleaned else Control.MOUSE_FILTER_IGNORE
	var ready: bool = bool(m.day_one_art_desk_unlocked)
	if _desk_button != null:
		_desk_button.visible = ready and not _customizer_open
		_desk_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if _desk_button.visible else Control.MOUSE_FILTER_IGNORE
	if _desk_glow != null:
		_desk_glow.visible = ready
	_refresh_pointer()


func audit_snapshot() -> Dictionary:
	return {
		"material_count": MATERIALS.size(),
		"grime_count": GRIME.size(),
		"material_button_count": _material_buttons.size(),
		"grime_button_count": _grime_buttons.size(),
		"desk_button": _desk_button != null,
		"pointer": _pointer != null,
		"canvas_only": true,
	}


func probe_collect_all() -> bool:
	if m == null:
		return false
	for material: Dictionary in MATERIALS:
		_on_material_pressed(String(material["id"]))
	for grime: Dictionary in GRIME:
		_on_grime_pressed(String(grime["id"]))
	return bool(m.day_one_art_desk_unlocked)


func _process(delta: float) -> void:
	_pulse_time += maxf(delta, 0.0)
	if _pointer != null and is_instance_valid(_pointer) and _pointer.visible:
		_pointer.scale = Vector2.ONE * (1.0 + sin(_pulse_time * 4.2) * 0.10)
		_pointer.rotation = sin(_pulse_time * 2.7) * 0.055
	if _desk_glow != null and is_instance_valid(_desk_glow) and _desk_glow.visible:
		_desk_glow.modulate.a = 0.70 + sin(_pulse_time * 3.2) * 0.20
		queue_redraw()


func _draw() -> void:
	# The room already supplies the desk and counters.  These marks are only
	# temporary, code-native 2D grime/supply accents over that approved painting.
	for material: Dictionary in MATERIALS:
		var material_id: String = String(material["id"])
		if m != null and bool(m.day_one_art_collected_materials.get(material_id, false)):
			continue
		var center: Vector2 = material["center"] as Vector2
		var color: Color = material["color"] as Color
		if material_id == "brushes":
			draw_line(center + Vector2(-46.0, 25.0), center + Vector2(46.0, -26.0),
				Color(0.36, 0.20, 0.16), 15.0, true)
			draw_line(center + Vector2(-42.0, 20.0), center + Vector2(42.0, -31.0),
				color, 7.0, true)
			draw_circle(center + Vector2(49.0, -33.0), 14.0, color)
		else:
			draw_circle(center, 34.0, Color(0.16, 0.12, 0.22, 0.35))
			draw_circle(center, 27.0, color)
			draw_circle(center + Vector2(-9.0, -8.0), 7.0, Color(1.0, 1.0, 1.0, 0.55))
	for grime: Dictionary in GRIME:
		var grime_id: String = String(grime["id"])
		if m != null and bool(m.day_one_art_cleaned_grime.get(grime_id, false)):
			continue
		var center: Vector2 = grime["center"] as Vector2
		var radius: Vector2 = grime["radius"] as Vector2
		_draw_grime_ellipse(center, radius, Color(0.18, 0.13, 0.24, 0.43))
		draw_circle(center + Vector2(-radius.x * 0.45, -4.0), 8.0,
			Color(0.10, 0.08, 0.16, 0.48))
		draw_circle(center + Vector2(radius.x * 0.34, 4.0), 12.0,
			Color(0.10, 0.08, 0.16, 0.38))
	if m != null and bool(m.day_one_art_desk_unlocked):
		var ring_scale: float = 1.0 + sin(_pulse_time * 3.2) * 0.06
		for ring: int in range(3):
			draw_arc(DESK_CENTER, (92.0 + float(ring) * 21.0) * ring_scale,
				0.0, TAU, 40, Color(1.0, 0.84, 0.35, 0.32 - ring * 0.08), 8.0)


func _build_targets() -> void:
	for material: Dictionary in MATERIALS:
		var material_id: String = String(material["id"])
		_material_buttons[material_id] = _make_target_button(
			"Collect_" + material_id, material["center"] as Vector2,
			material["hit_size"] as Vector2, _on_material_pressed.bind(material_id))
	for grime: Dictionary in GRIME:
		var grime_id: String = String(grime["id"])
		_grime_buttons[grime_id] = _make_target_button(
			"Scrub_" + grime_id, grime["center"] as Vector2,
			grime["hit_size"] as Vector2, _on_grime_pressed.bind(grime_id))
	_desk_button = _make_target_button("OpenPaintDesk", DESK_CENTER, DESK_HIT_SIZE,
		_on_desk_pressed)
	_desk_button.z_index = 18
	_desk_button.tooltip_text = "Open the glowing paint desk"
	_desk_glow = Label.new()
	_desk_glow.name = "PaintDeskGlow"
	_desk_glow.text = "✦"
	_desk_glow.position = DESK_CENTER - Vector2(62.0, 62.0)
	_desk_glow.size = Vector2(124.0, 124.0)
	_desk_glow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_desk_glow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_desk_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_desk_glow.z_index = 16
	StorybookUI.style_label(_desk_glow, 76, Color(1.0, 0.84, 0.34), 5)
	add_child(_desk_glow)
	move_child(_desk_glow, 0)


func _make_target_button(button_name: String, center: Vector2, hit_size: Vector2,
		handler: Callable) -> Button:
	var target := Button.new()
	target.name = button_name
	target.position = center - hit_size * 0.5
	target.size = hit_size
	target.flat = true
	target.focus_mode = Control.FOCUS_NONE
	target.mouse_filter = Control.MOUSE_FILTER_STOP
	target.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
	target.z_index = 14
	target.pressed.connect(handler)
	add_child(target)
	return target


func _build_pointer() -> void:
	_pointer = Label.new()
	_pointer.name = "ArtStudioPointer"
	_pointer.text = "👇"
	_pointer.size = Vector2(96.0, 96.0)
	_pointer.pivot_offset = _pointer.size * 0.5
	_pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pointer.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pointer.z_index = 30
	StorybookUI.style_label(_pointer, 64, Color(1.0, 0.88, 0.35), 6)
	add_child(_pointer)


func _on_material_pressed(material_id: String) -> void:
	if m == null or bool(m.day_one_art_collected_materials.get(material_id, false)):
		return
	m._ui_tap()
	_spawn_clean_sparkles(_material_center(material_id))
	_record_cleanup("material", material_id)


func _on_grime_pressed(grime_id: String) -> void:
	if m == null or bool(m.day_one_art_cleaned_grime.get(grime_id, false)):
		return
	m._ui_tap()
	_spawn_clean_sparkles(_grime_center(grime_id))
	_record_cleanup("grime", grime_id)


func _record_cleanup(kind: String, item_id: String) -> void:
	var result: Variant = m.call("day_one_record_art_cleanup", kind, item_id)
	if result is bool and not bool(result):
		return
	refresh_from_state()
	_announce_current_target()


func _on_desk_pressed() -> void:
	if m == null or not bool(m.day_one_art_desk_unlocked) or _customizer_open:
		return
	_customizer_open = true
	m._ui_tap()
	refresh_from_state()
	m._open_attack_customizer(Callable(self, "_on_customization_confirmed"))


func _on_customization_confirmed(_result: Variant = null) -> void:
	if m == null:
		return
	_customizer_open = false
	var customization_result: Variant = m.call("day_one_complete_art_customization")
	if customization_result is bool and not bool(customization_result) \
			and not bool(m.day_one_art_customization_completed):
		refresh_from_state()
		return
	var result: Variant = m.call("day_one_complete_art_scene")
	if result is bool and not bool(result):
		# A repeated confirmation is harmless, but the visual state should still
		# follow the saved customization flag supplied by the main state owner.
		refresh_from_state()
		return
	m.call("_day_one_sync_castle_dressing")
	m.call("_write_save")
	# Completion makes the art room a normal, replayable castle room. Ask the
	# castle satellite to remove this temporary overlay before returning to its
	# regular Craft Room interactions.
	var rooms: Variant = m.call("_castle_rooms_ref")
	if rooms is Object and (rooms as Object).has_method("_clear_day_one_art_studio"):
		(rooms as Object).call("_clear_day_one_art_studio")
	else:
		refresh_from_state()


func _refresh_pointer() -> void:
	if _pointer == null:
		return
	var target: Vector2 = Vector2.ZERO
	var found: bool = false
	for material: Dictionary in MATERIALS:
		if not bool(m.day_one_art_collected_materials.get(String(material["id"]), false)):
			target = material["center"] as Vector2
			found = true
			break
	if not found:
		for grime: Dictionary in GRIME:
			if not bool(m.day_one_art_cleaned_grime.get(String(grime["id"]), false)):
				target = grime["center"] as Vector2
				found = true
				break
	if not found and bool(m.day_one_art_desk_unlocked) and not _customizer_open:
		target = DESK_CENTER
		found = true
	_pointer.visible = found
	if found:
		_pointer.position = target + Vector2(76.0, -78.0) - _pointer.size * 0.5


func _announce_current_target() -> void:
	if not _announcements_enabled or m == null:
		return
	for material: Dictionary in MATERIALS:
		if not bool(m.day_one_art_collected_materials.get(String(material["id"]), false)):
			_speak_cue("Tap the loose %s!" % String(material["label"]), "talk")
			return
	for grime: Dictionary in GRIME:
		if not bool(m.day_one_art_cleaned_grime.get(String(grime["id"]), false)):
			_speak_cue("Now scrub the %s!" % String(grime["label"]), "talk")
			return
	if bool(m.day_one_art_desk_unlocked) and not _customizer_open:
		_speak_cue("The magic paint desk is glowing! Tap it!", "win")


func _speak_cue(message: String, mood: String) -> void:
	m.show_msg("Roshan", message, mood)
	m._say("roshan", "talk")


func _all_materials_collected() -> bool:
	for material: Dictionary in MATERIALS:
		if not bool(m.day_one_art_collected_materials.get(
				String(material["id"]), false)):
			return false
	return true


func _material_center(material_id: String) -> Vector2:
	for material: Dictionary in MATERIALS:
		if String(material["id"]) == material_id:
			return material["center"] as Vector2
	return DESK_CENTER


func _grime_center(grime_id: String) -> Vector2:
	for grime: Dictionary in GRIME:
		if String(grime["id"]) == grime_id:
			return grime["center"] as Vector2
	return DESK_CENTER


func _spawn_clean_sparkles(center: Vector2) -> void:
	for index: int in range(7):
		var sparkle := Label.new()
		sparkle.text = "✦"
		sparkle.size = Vector2(42.0, 42.0)
		sparkle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sparkle.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		sparkle.mouse_filter = Control.MOUSE_FILTER_IGNORE
		sparkle.z_index = 40
		var angle: float = TAU * float(index) / 7.0
		var start_offset := Vector2(cos(angle), sin(angle)) * 16.0
		var end_offset := Vector2(cos(angle), sin(angle)) * (58.0 + index * 4.0)
		sparkle.position = center + start_offset - sparkle.size * 0.5
		StorybookUI.style_label(sparkle, 30,
			SPARKLE_COLORS[index % SPARKLE_COLORS.size()], 3)
		add_child(sparkle)
		var tween: Tween = sparkle.create_tween().set_parallel(true)
		tween.tween_property(sparkle, "position",
			center + end_offset - sparkle.size * 0.5, 0.42)
		tween.tween_property(sparkle, "modulate:a", 0.0, 0.42)
		tween.chain().tween_callback(sparkle.queue_free)


func _draw_grime_ellipse(center: Vector2, radius: Vector2, color: Color) -> void:
	var points := PackedVector2Array()
	for index: int in range(25):
		var angle: float = TAU * float(index) / 24.0
		points.append(center + Vector2(cos(angle) * radius.x, sin(angle) * radius.y))
	draw_colored_polygon(points, color)
