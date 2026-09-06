class_name DayOneArtStudio
extends Control
## Level One's first art-room job: gather the loose supplies, scrub the
## counters, then wake the painted desk.  The room remains a picture-first
## Canvas2D scene; this node owns only temporary touch targets and effects.

const MATERIALS: Array[Dictionary] = [
	{"id": "brushes", "label": "loose brushes", "center": Vector2(344.0, 390.0),
		"hit_size": Vector2(150.0, 128.0), "color": Color(1.0, 0.72, 0.38)},
	{"id": "pink_paint", "label": "pink paint", "center": Vector2(416.0, 390.0),
		"hit_size": Vector2(128.0, 128.0), "color": Color(1.0, 0.48, 0.70)},
	{"id": "blue_paint", "label": "blue paint", "center": Vector2(608.0, 390.0),
		"hit_size": Vector2(128.0, 128.0), "color": Color(0.44, 0.84, 1.0)},
	{"id": "paint_cups", "label": "paint cups", "center": Vector2(681.0, 390.0),
		"hit_size": Vector2(150.0, 128.0), "color": Color(0.73, 0.60, 1.0)},
]
const GRIME: Array[Dictionary] = [
	{"id": "left_counter", "label": "left counter grime", "center": Vector2(180.0, 385.0),
		"hit_size": Vector2(150.0, 110.0), "radius": Vector2(48.0, 12.0)},
	{"id": "desk_counter", "label": "desk counter grime", "center": Vector2(512.0, 290.0),
		"hit_size": Vector2(150.0, 110.0), "radius": Vector2(54.0, 11.0)},
	{"id": "right_counter", "label": "right counter grime", "center": Vector2(854.0, 385.0),
		"hit_size": Vector2(150.0, 110.0), "radius": Vector2(48.0, 12.0)},
]
const DESK_CENTER := Vector2(512.0, 325.0)
const DESK_HIT_SIZE := Vector2(310.0, 158.0)
const SOURCE_CANVAS_SIZE := Vector2(1024.0, 576.0)
const ART_TO_STAGE := 1.25
const ART_BRUSHES := preload("res://assets/castle/day_one_art_studio/loose_brush_bundle.png")
const ART_PAINT_PINK := preload("res://assets/castle/day_one_art_studio/paint_bottle_pink.png")
const ART_PAINT_BLUE := preload("res://assets/castle/day_one_art_studio/paint_bottle_blue.png")
const ART_PAINT_CUPS := preload("res://assets/castle/day_one_art_studio/paint_cups.png")
const ART_GRIME_LEFT := preload("res://assets/castle/day_one_art_studio/grime_left.png")
const ART_GRIME_DESK := preload("res://assets/castle/day_one_art_studio/grime_desk.png")
const ART_GRIME_RIGHT := preload("res://assets/castle/day_one_art_studio/grime_right.png")
const CONTACT_SHADOW := preload("res://assets/flats/castle/rooms/room_actor_shadow.png")
const SPARKLE_COLORS: Array[Color] = [
	Color(1.0, 0.83, 0.38), Color(0.52, 0.94, 1.0),
	Color(1.0, 0.55, 0.76), Color(0.80, 0.68, 1.0),
]

var m: ReefMain
var _material_buttons: Dictionary = {}
var _grime_buttons: Dictionary = {}
var _material_art: Dictionary = {}
var _material_shadows: Dictionary = {}
var _grime_art: Dictionary = {}
var _world_visual_layer: Node2D = null
var _desk_button: Button = null
var _pointer: Label = null
var _desk_glow: Label = null
var _pulse_time: float = 0.0
var _announcements_enabled: bool = true
var _customizer_open: bool = false
var _voice_session_id: String = "art_visit_0"


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	m._navigation_push("day_one_art_studio", self,
		Callable(m, "_close_day_one_art_studio"))
	_announcements_enabled = announcements_enabled
	var visit_count: int = int(m.g.get("day_one_art_voice_visit_count", 0)) + 1
	m.g["day_one_art_voice_visit_count"] = visit_count
	_voice_session_id = "art_visit_%d" % visit_count
	name = "DayOneArtStudio"
	position = Vector2.ZERO
	size = SOURCE_CANVAS_SIZE
	scale = Vector2.ONE * ART_TO_STAGE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 22
	_build_targets()
	_build_pointer()
	refresh_from_state()
	_say_day_one_context("day1_art_enter",
		"Paint and sparkles! Let's make castle art!")
	set_process(true)
	call_deferred("_announce_current_target")


func teardown() -> void:
	m._navigation_remove("day_one_art_studio")
	set_process(false)
	_customizer_open = false
	if _world_visual_layer != null and is_instance_valid(_world_visual_layer):
		_world_visual_layer.queue_free()
	_world_visual_layer = null
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
		var material_card: Sprite2D = _material_art.get(material_id) as Sprite2D
		if material_card != null:
			material_card.visible = not collected
		var material_shadow: Sprite2D = _material_shadows.get(material_id) as Sprite2D
		if material_shadow != null:
			material_shadow.visible = not collected
	for grime_id: String in _grime_buttons:
		var grime_button: Button = _grime_buttons[grime_id] as Button
		var cleaned: bool = bool(m.day_one_art_cleaned_grime.get(grime_id, false))
		var materials_ready: bool = _all_materials_collected()
		grime_button.visible = materials_ready and not cleaned
		grime_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if not cleaned else Control.MOUSE_FILTER_IGNORE
		var grime_card: Sprite2D = _grime_art.get(grime_id) as Sprite2D
		if grime_card != null:
			grime_card.visible = materials_ready and not cleaned
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
		"material_art_count": _material_art.size(),
		"grime_art_count": _grime_art.size(),
		"desk_button": _desk_button != null,
		"pointer": _pointer != null,
		"expected_tap_count": MATERIALS.size() + GRIME.size(),
		"child_sized_hit_targets": _child_sized_hit_targets(),
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
	# Representational supplies and grime are texture-backed cards.  Only the
	# transient desk invitation remains code-native.
	if m != null and bool(m.day_one_art_desk_unlocked):
		var ring_scale: float = 1.0 + sin(_pulse_time * 3.2) * 0.06
		for ring: int in range(3):
			draw_arc(DESK_CENTER, (92.0 + float(ring) * 21.0) * ring_scale,
				0.0, TAU, 40, Color(1.0, 0.84, 0.35, 0.32 - ring * 0.08), 8.0)


func _build_targets() -> void:
	_build_item_art()
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


func _build_item_art() -> void:
	if m.castle_room_world_root == null:
		return
	_world_visual_layer = Node2D.new()
	_world_visual_layer.name = "DayOneArtStudioWorldVisuals"
	m.castle_room_world_root.add_child(_world_visual_layer)
	# These are the only new loose supplies. Existing stored brushes, bottles,
	# cups, palette and paint table remain owned by the accepted room cards.
	_material_art["brushes"] = _make_world_card("LooseBrushes", ART_BRUSHES,
		Vector2(344.0, 390.0), Vector2(92.0, 62.0), 250)
	_material_art["pink_paint"] = _make_world_card("LoosePinkPaint", ART_PAINT_PINK,
		Vector2(416.0, 390.0), Vector2(42.0, 56.0), 250)
	_material_art["blue_paint"] = _make_world_card("LooseBluePaint", ART_PAINT_BLUE,
		Vector2(608.0, 390.0), Vector2(42.0, 56.0), 250)
	_material_art["paint_cups"] = _make_world_card("LoosePaintCups", ART_PAINT_CUPS,
		Vector2(681.0, 390.0), Vector2(92.0, 62.0), 250)
	for material: Dictionary in MATERIALS:
		var material_id: String = String(material["id"])
		var center: Vector2 = material["center"] as Vector2
		var shadow_size := Vector2(76.0, 18.0)
		if material_id in ["pink_paint", "blue_paint"]:
			shadow_size = Vector2(38.0, 13.0)
		_material_shadows[material_id] = _make_world_card(
			"Shadow_" + material_id, CONTACT_SHADOW,
			center + Vector2(0.0, 27.0), shadow_size, 249,
			Color(0.22, 0.18, 0.40, 0.34))
	# Surface marks share the room's own world depth rather than the stage UI.
	_grime_art["left_counter"] = _make_world_card("GrimeLeft", ART_GRIME_LEFT,
		Vector2(180.0, 385.0), Vector2(82.0, 18.0), 401,
		Color(0.78, 0.72, 0.90, 0.70), -0.025)
	_grime_art["desk_counter"] = _make_world_card("GrimeDesk", ART_GRIME_DESK,
		Vector2(512.0, 290.0), Vector2(96.0, 18.0), 201,
		Color(0.78, 0.72, 0.90, 0.68), 0.01)
	_grime_art["right_counter"] = _make_world_card("GrimeRight", ART_GRIME_RIGHT,
		Vector2(854.0, 385.0), Vector2(82.0, 18.0), 401,
		Color(0.78, 0.72, 0.90, 0.70), 0.025)


func _make_world_card(card_name: String, texture: Texture2D, center: Vector2,
		art_size: Vector2, card_z_index: int, tint: Color = Color.WHITE,
		rotation_radians: float = 0.0) -> Sprite2D:
	var card := Sprite2D.new()
	card.name = card_name
	card.texture = texture
	card.position = center * ART_TO_STAGE
	card.scale = art_size * ART_TO_STAGE / texture.get_size()
	card.z_index = card_z_index
	card.modulate = tint
	card.rotation = rotation_radians
	card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	card.set_meta("source_asset_role", "day_one_cleanup_item")
	card.set_meta("source_art_center", center)
	_world_visual_layer.add_child(card)
	return card


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
	_animate_storage_station(material_id)
	if not _record_cleanup("material", material_id):
		return
	_say_day_one_context(_material_context_key(material_id),
		_material_context_caption(material_id))
	if _all_materials_collected():
		_say_day_one_context("day1_art_materials_complete",
			"All the art supplies are ready!", 0)


func _animate_storage_station(material_id: String) -> void:
	var rooms: Variant = m.call("_castle_rooms_ref")
	if not (rooms is Object) or not (rooms as Object).has_method(
			"play_day_one_art_station"):
		return
	var station_id := "paint_table" if material_id in ["brushes", "blue_paint"] \
		else "palette"
	# The craft-room cards are shared with the post-Day-One logo studio. This
	# narrow route plays their authored fixture animation without inheriting the
	# room card's launch_activity, so a supply tap can never hijack into the logo.
	(rooms as Object).call("play_day_one_art_station", station_id)


func _on_grime_pressed(grime_id: String) -> void:
	if m == null or bool(m.day_one_art_cleaned_grime.get(grime_id, false)):
		return
	m._ui_tap()
	_spawn_clean_sparkles(_grime_center(grime_id))
	if not _record_cleanup("grime", grime_id):
		return
	_say_day_one_context(_grime_context_key(grime_id),
		_grime_context_caption(grime_id))
	if _all_grime_cleaned():
		_say_day_one_context("day1_art_desk_unlock",
			"The paint table is glowing! Let's make something!", 0)


func _record_cleanup(kind: String, item_id: String) -> bool:
	var result: Variant = m.call("day_one_record_art_cleanup", kind, item_id)
	if result is bool and not bool(result):
		return false
	refresh_from_state()
	return true


func _on_desk_pressed() -> void:
	if m == null or not bool(m.day_one_art_desk_unlocked) or _customizer_open:
		return
	_customizer_open = true
	m._ui_tap()
	refresh_from_state()
	_say_day_one_context("day1_art_desk_open",
		"The paint desk is open!", 0)
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
	_say_day_one_context("day1_art_customization_confirmed",
		"Our colors are ready!", 0)
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
		_say_day_one_context("day1_art_complete",
			"All clean! The floor is twinkling!", 0)
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
			var material_id := String(material["id"])
			_say_day_one_context(_material_context_hint_key(material_id),
				"Tap the %s!" % String(material["label"]))
			return
	for grime: Dictionary in GRIME:
		if not bool(m.day_one_art_cleaned_grime.get(String(grime["id"]), false)):
			var grime_id := String(grime["id"])
			_say_day_one_context(_grime_context_hint_key(grime_id),
				"Now scrub the %s!" % String(grime["label"]))
			return
	if bool(m.day_one_art_desk_unlocked) and not _customizer_open:
		_say_day_one_context("day1_art_desk_hint",
			"The magic paint desk is glowing! Tap it!")


func _say_day_one_context(cue_id: String, caption: String,
		variant: int = 0) -> void:
	if m == null:
		return
	m.say_day_one_context(cue_id, caption, "art", _voice_session_id,
		variant, false)


func _material_context_key(material_id: String) -> String:
	match material_id:
		"brushes": return "day1_art_material_brushes_found"
		"pink_paint": return "day1_art_material_pink_paint_found"
		"blue_paint": return "day1_art_material_blue_paint_found"
		"paint_cups": return "day1_art_material_cups_found"
	return "day1_art_material_brushes_found"


func _material_context_hint_key(material_id: String) -> String:
	return _material_context_key(material_id).trim_suffix("_found") + "_hint"


func _material_context_caption(material_id: String) -> String:
	match material_id:
		"brushes": return "I found the brushes!"
		"pink_paint": return "Pink paint! My favorite!"
		"blue_paint": return "Blue paint is ready!"
		"paint_cups": return "I found the little paint cups!"
	return "I found an art supply!"


func _grime_context_key(grime_id: String) -> String:
	match grime_id:
		"left_counter": return "day1_art_scrub_left_clean"
		"desk_counter": return "day1_art_scrub_desk_clean"
		"right_counter": return "day1_art_scrub_right_clean"
	return "day1_art_scrub_left_clean"


func _grime_context_hint_key(grime_id: String) -> String:
	return _grime_context_key(grime_id).trim_suffix("_clean") + "_hint"


func _grime_context_caption(grime_id: String) -> String:
	match grime_id:
		"left_counter": return "Scrub this painty counter!"
		"desk_counter": return "The desk needs a good scrub!"
		"right_counter": return "One more counter to sparkle!"
	return "Scrub this spot until it sparkles!"


func _all_materials_collected() -> bool:
	for material: Dictionary in MATERIALS:
		if not bool(m.day_one_art_collected_materials.get(
				String(material["id"]), false)):
			return false
	return true


func _all_grime_cleaned() -> bool:
	for grime: Dictionary in GRIME:
		if not bool(m.day_one_art_cleaned_grime.get(String(grime["id"]), false)):
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


func _child_sized_hit_targets() -> bool:
	for material: Dictionary in MATERIALS:
		var hit_size: Vector2 = material["hit_size"] as Vector2
		if hit_size.x < 128.0 or hit_size.y < 128.0:
			return false
	for grime: Dictionary in GRIME:
		var grime_size: Vector2 = grime["hit_size"] as Vector2
		if grime_size.x < 150.0 or grime_size.y < 110.0:
			return false
	return true


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
