class_name DayOneArtStudio
extends Control
## Level One's first art-room job: gather the loose supplies, scrub the
## counters, then wake the painted desk.  The room remains a picture-first
## Canvas2D scene; this node owns only temporary touch targets and effects.

const MATERIALS: Array[Dictionary] = [
	{"id": "brushes", "label": "loose brushes", "center": Vector2(318.0, 390.0),
		"hit_size": Vector2(124.0, 104.0), "color": Color(1.0, 0.72, 0.38)},
	{"id": "pink_paint", "label": "pink paint", "center": Vector2(384.0, 390.0),
		"hit_size": Vector2(92.0, 104.0), "color": Color(1.0, 0.48, 0.70)},
	{"id": "stacked_cups", "label": "stacked paint cups", "center": Vector2(458.0, 390.0),
		"hit_size": Vector2(118.0, 104.0), "color": Color(0.78, 0.65, 1.0)},
	{"id": "blue_paint", "label": "blue paint", "center": Vector2(538.0, 390.0),
		"hit_size": Vector2(92.0, 104.0), "color": Color(0.44, 0.84, 1.0)},
	{"id": "paint_cups", "label": "paint cups", "center": Vector2(608.0, 390.0),
		"hit_size": Vector2(124.0, 104.0), "color": Color(0.73, 0.60, 1.0)},
	{"id": "spare_brushes", "label": "spare brushes", "center": Vector2(666.0, 390.0),
		"hit_size": Vector2(112.0, 104.0), "color": Color(1.0, 0.72, 0.38)},
]
const GRIME: Array[Dictionary] = [
	{"id": "left_counter", "label": "left floor smudge", "center": Vector2(326.0, 440.0),
		"hit_size": Vector2(132.0, 76.0), "radius": Vector2(48.0, 12.0)},
	{"id": "desk_counter", "label": "middle floor smudge", "center": Vector2(470.0, 450.0),
		"hit_size": Vector2(144.0, 72.0), "radius": Vector2(54.0, 11.0)},
	{"id": "right_counter", "label": "right floor smudge", "center": Vector2(654.0, 440.0),
		"hit_size": Vector2(132.0, 76.0), "radius": Vector2(48.0, 12.0)},
]
const DESK_CENTER := Vector2(512.0, 325.0)
const DESK_HIT_SIZE := Vector2(310.0, 158.0)
const RAINBOW_CENTER := Vector2(540.0, 520.0)
const RAINBOW_ART_SIZE := Vector2(190.0, 104.0)
const RAINBOW_HIT_SIZE := Vector2(238.0, 132.0)
const TABLE_OWNERSHIP_RECTS: Array[Rect2] = [
	Rect2(0.0, 316.0, 256.0, 260.0),
	Rect2(720.0, 316.0, 304.0, 260.0),
]
const TABLE_CLEARANCE_MARGIN := 12.0
const SOURCE_CANVAS_SIZE := Vector2(1024.0, 576.0)
const ART_TO_STAGE := 1.25
const ART_BRUSHES := preload("res://assets/castle/day_one_art_studio/loose_brush_bundle.png")
const ART_PAINT_PINK := preload("res://assets/castle/day_one_art_studio/paint_bottle_pink.png")
const ART_PAINT_BLUE := preload("res://assets/castle/day_one_art_studio/paint_bottle_blue.png")
const ART_PAINT_CUPS := preload("res://assets/castle/day_one_art_studio/paint_cups.png")
const ART_GRIME_LEFT := preload("res://assets/castle/day_one_art_studio/grime_left.png")
const ART_GRIME_DESK := preload("res://assets/castle/day_one_art_studio/grime_desk.png")
const ART_GRIME_RIGHT := preload("res://assets/castle/day_one_art_studio/grime_right.png")
const ART_RAINBOW_SPILL := preload("res://assets/castle/day_one_polish_v2/art_rainbow_spill.png")
const ART_MAGIC_BRUSH := preload("res://assets/castle/day_one_art_studio/magic_cleaning_brush.png")
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
var _rainbow_art: Sprite2D = null
var _rainbow_button: Button = null
var _cleaning_tool: Sprite2D = null
var _desk_button: Button = null
var _pointer: Label = null
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
	if m.day_one_castle_dressing != null \
			and is_instance_valid(m.day_one_castle_dressing):
		# The cleanup cards and entry-visible grime own this activity's dirty
		# hierarchy. Keep the generic ambient bunny from covering Roshan or the
		# ordered target, then restore it if the activity is torn down unfinished.
		m.day_one_castle_dressing.set_room_bunny_suppressed(
			"craft_room", true)
	_set_legacy_room_controls_suppressed(true)
	refresh_from_state()
	set_process(true)
	call_deferred("_announce_current_target")


func teardown() -> void:
	set_process(false)
	_customizer_open = false
	if m != null and m.day_one_castle_dressing != null \
			and is_instance_valid(m.day_one_castle_dressing):
		m.day_one_castle_dressing.set_room_bunny_suppressed(
			"craft_room", false)
	_set_legacy_room_controls_suppressed(false)
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
	var rainbow_active: bool = not m.day_one_room_polish_is_complete("art")
	var active_material_id: String = "" if rainbow_active \
		else _next_uncollected_material_id()
	var active_grime_id: String = "" if active_material_id != "" \
		else _next_uncleaned_grime_id()
	if rainbow_active:
		active_grime_id = ""
	if _rainbow_art != null:
		_rainbow_art.visible = rainbow_active
	if _rainbow_button != null:
		_rainbow_button.visible = rainbow_active
		_rainbow_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if rainbow_active else Control.MOUSE_FILTER_IGNORE
	for material_id: String in _material_buttons:
		var material_button: Button = _material_buttons[material_id] as Button
		var collected: bool = bool(m.day_one_art_collected_materials.get(
			material_id, false))
		var material_active: bool = not collected \
			and material_id == active_material_id
		material_button.visible = material_active
		material_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if material_active else Control.MOUSE_FILTER_IGNORE
		var material_card: Sprite2D = _material_art.get(material_id) as Sprite2D
		if material_card != null:
			material_card.visible = not collected
			var material_tint: Color = material_card.get_meta(
				"rest_modulate", Color.WHITE) as Color
			material_tint.a *= 1.0 if material_active else 0.72
			material_card.modulate = material_tint
		var material_shadow: Sprite2D = _material_shadows.get(material_id) as Sprite2D
		if material_shadow != null:
			material_shadow.visible = not collected
			var shadow_tint: Color = material_shadow.get_meta(
				"rest_modulate", material_shadow.modulate) as Color
			shadow_tint.a *= 1.0 if material_active else 0.58
			material_shadow.modulate = shadow_tint
	for grime_id: String in _grime_buttons:
		var grime_button: Button = _grime_buttons[grime_id] as Button
		var cleaned: bool = bool(m.day_one_art_cleaned_grime.get(grime_id, false))
		var grime_active: bool = not cleaned and grime_id == active_grime_id
		grime_button.visible = grime_active
		grime_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if grime_active else Control.MOUSE_FILTER_IGNORE
		var grime_card: Sprite2D = _grime_art.get(grime_id) as Sprite2D
		if grime_card != null:
			# Show the grime from dirty entry. It remains visibly secondary until
			# the ordered supply pickups are done, then one mark at a time brightens
			# and becomes responsive under the pointer.
			grime_card.visible = not cleaned
			var grime_tint: Color = grime_card.get_meta(
				"rest_modulate", grime_card.modulate) as Color
			grime_tint.a *= 1.0 if grime_active else 0.72
			grime_card.modulate = grime_tint
	var ready: bool = bool(m.day_one_art_desk_unlocked)
	if _desk_button != null:
		_desk_button.visible = ready and not _customizer_open
		_desk_button.mouse_filter = Control.MOUSE_FILTER_STOP \
			if _desk_button.visible else Control.MOUSE_FILTER_IGNORE
	_refresh_pointer()


func audit_snapshot() -> Dictionary:
	return {
		"material_count": MATERIALS.size(),
		"grime_count": GRIME.size(),
		"material_button_count": _material_buttons.size(),
		"grime_button_count": _grime_buttons.size(),
		"material_art_count": _material_art.size(),
		"grime_art_count": _grime_art.size(),
		"ordered_interaction_count": 1 + MATERIALS.size() + GRIME.size() + 1,
		"rainbow_owner_count": 1 if _rainbow_art != null else 0,
		"legacy_palette_visual_present": m.castle_room_item_sprites.has("palette"),
		"left_table_visual_owner_count": _table_visual_owner_count("left") \
			+ (1 if m.castle_room_item_sprites.has("palette") else 0),
		"right_table_visual_owner_count": _table_visual_owner_count("right"),
		"table_alpha_cleanup_pass": _table_alpha_cleanup_pass(),
		"target_table_clearance_pass": _target_visual_bounds_clear_tables(),
		"persistent_glow_count": 0,
		"desk_button": _desk_button != null,
		"pointer": _pointer != null,
		"pointer_clear_of_player_face": _pointer_clears_player_face(),
		"one_active_target": _active_target_count() <= 1,
		"active_target_count": _active_target_count(),
		"grime_visible_from_entry": _visible_grime_count() > 0,
		"canvas_only": true,
	}


func probe_collect_all() -> bool:
	if m == null:
		return false
	_on_rainbow_pressed()
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


func _build_targets() -> void:
	_build_item_art()
	_rainbow_button = _make_target_button(
		"ScrubRainbowSpill", RAINBOW_CENTER, RAINBOW_HIT_SIZE,
		_on_rainbow_pressed)
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
	_desk_button.tooltip_text = "Open the ready paint desk"


func _build_item_art() -> void:
	if m.castle_room_world_root == null:
		return
	_world_visual_layer = Node2D.new()
	_world_visual_layer.name = "DayOneArtStudioWorldVisuals"
	m.castle_room_world_root.add_child(_world_visual_layer)
	# All cleanup cards stay in the measured open-floor lane between the two
	# foreground tables. The left depth card is the sole owner of its palette.
	_rainbow_art = _make_world_card("RainbowFloorSpill", ART_RAINBOW_SPILL,
		RAINBOW_CENTER, RAINBOW_ART_SIZE, 245)
	_material_art["brushes"] = _make_world_card("LooseBrushes", ART_BRUSHES,
		Vector2(318.0, 390.0), Vector2(92.0, 62.0), 250)
	_material_art["pink_paint"] = _make_world_card("LoosePinkPaint", ART_PAINT_PINK,
		Vector2(384.0, 390.0), Vector2(42.0, 56.0), 250)
	_material_art["stacked_cups"] = _make_world_card(
		"StackedPaintCups", ART_PAINT_CUPS,
		Vector2(458.0, 390.0), Vector2(84.0, 56.0), 250,
		Color.WHITE, -0.04)
	_material_art["blue_paint"] = _make_world_card("LooseBluePaint", ART_PAINT_BLUE,
		Vector2(538.0, 390.0), Vector2(42.0, 56.0), 250)
	_material_art["paint_cups"] = _make_world_card("LoosePaintCups", ART_PAINT_CUPS,
		Vector2(608.0, 390.0), Vector2(84.0, 56.0), 250)
	_material_art["spare_brushes"] = _make_world_card(
		"SpareBrushes", ART_BRUSHES,
		Vector2(666.0, 390.0), Vector2(76.0, 52.0), 250,
		Color.WHITE, 0.06)
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
	# Existing approved grime is reused as five legible floor-cleaning marks.
	# The three saved ids keep their established schema while their visual owner
	# moves off the foreground tables, eliminating alpha overlap.
	_grime_art["left_counter"] = _make_world_card("GrimeLeft", ART_GRIME_LEFT,
		Vector2(326.0, 440.0), Vector2(82.0, 18.0), 241,
		Color(0.78, 0.72, 0.90, 0.70), -0.025)
	_grime_art["desk_counter"] = _make_world_card("GrimeDesk", ART_GRIME_DESK,
		Vector2(470.0, 450.0), Vector2(96.0, 18.0), 241,
		Color(0.78, 0.72, 0.90, 0.68), 0.01)
	_grime_art["right_counter"] = _make_world_card("GrimeRight", ART_GRIME_RIGHT,
		Vector2(654.0, 440.0), Vector2(82.0, 18.0), 241,
		Color(0.78, 0.72, 0.90, 0.70), 0.025)
	_cleaning_tool = _make_world_card("MagicCleaningBrush", ART_MAGIC_BRUSH,
		Vector2(512.0, 430.0), Vector2(82.0, 82.0), 430)
	_cleaning_tool.visible = false


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
	card.set_meta("rest_modulate", tint)
	card.rotation = rotation_radians
	card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	card.set_meta("source_asset_role", "day_one_cleanup_item")
	card.set_meta("source_art_center", center)
	card.set_meta("source_art_bounds", Rect2(center - art_size * 0.5, art_size))
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
	if m == null or not m.day_one_room_polish_is_complete("art") \
			or bool(m.day_one_art_collected_materials.get(material_id, false)):
		return
	if material_id != _next_uncollected_material_id():
		return
	m._ui_tap()
	_animate_storage_station(material_id)
	_record_cleanup_with_feedback("material", material_id,
		_material_art.get(material_id) as Sprite2D, _material_center(material_id))


func _animate_storage_station(material_id: String) -> void:
	var rooms: Variant = m.call("_castle_rooms_ref")
	if not (rooms is Object) or not (rooms as Object).has_method("_activate_room_item"):
		return
	# Day One needs the authored station motion as causal feedback, but the
	# normal paint-table animation also schedules the Castle Logo activity.
	# Suppress that follow-up here so the room can finish and visibly settle
	# before any later optional activity is opened by a new child tap.
	(rooms as Object).call("_activate_room_item", "paint_table", false)


func _on_grime_pressed(grime_id: String) -> void:
	if m == null or bool(m.day_one_art_cleaned_grime.get(grime_id, false)):
		return
	if grime_id != _next_uncleaned_grime_id() or not _all_materials_collected():
		return
	m._ui_tap()
	_record_cleanup_with_feedback("grime", grime_id,
		_grime_art.get(grime_id) as Sprite2D, _grime_center(grime_id), true)


func _on_rainbow_pressed() -> void:
	if m == null or m.day_one_room_polish_is_complete("art"):
		return
	m._ui_tap()
	if not m.day_one_complete_room_polish("art"):
		return
	_play_cleanup_feedback(_rainbow_art, RAINBOW_CENTER, true)


func _record_cleanup_with_feedback(kind: String, item_id: String,
		card: Sprite2D, center: Vector2, use_brush: bool = false) -> void:
	var result: Variant = m.call("day_one_record_art_cleanup", kind, item_id)
	if result is bool and not bool(result):
		return
	_play_cleanup_feedback(card, center, use_brush)


func _play_cleanup_feedback(card: Sprite2D, center: Vector2,
		use_brush: bool) -> void:
	if _pointer != null:
		_pointer.visible = false
	_spawn_clean_sparkles(center)
	if use_brush and _cleaning_tool != null:
		_cleaning_tool.visible = true
		_cleaning_tool.position = (center + Vector2(-76.0, -42.0)) * ART_TO_STAGE
		_cleaning_tool.rotation = -0.42
		var brush_tween: Tween = _cleaning_tool.create_tween().set_parallel(true)
		brush_tween.tween_property(_cleaning_tool, "position",
			(center + Vector2(76.0, 30.0)) * ART_TO_STAGE, 0.42)
		brush_tween.tween_property(_cleaning_tool, "rotation", 0.36, 0.42)
		brush_tween.chain().tween_callback(_cleaning_tool.hide)
	if card == null or not is_instance_valid(card):
		refresh_from_state()
		_announce_current_target()
		return
	var target_modulate: Color = card.modulate
	target_modulate.a = 0.0
	var feedback: Tween = card.create_tween().set_parallel(true)
	feedback.tween_property(card, "scale", card.scale * 0.72, 0.42) \
		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
	feedback.tween_property(card, "modulate", target_modulate, 0.42)
	feedback.chain().tween_callback(_finish_cleanup_feedback.bind(card))


func _finish_cleanup_feedback(card: Sprite2D) -> void:
	if card != null and is_instance_valid(card):
		card.visible = false
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
	if not m.day_one_room_polish_is_complete("art"):
		target = RAINBOW_CENTER
		found = true
	for material: Dictionary in MATERIALS:
		if found:
			break
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
		var pointer_offset := Vector2(76.0, -78.0)
		if target != RAINBOW_CENTER and target != DESK_CENTER:
			# Keep Roshan's face and silhouette readable while the hand still points
			# straight down to the one responsive floor target.
			pointer_offset = Vector2(0.0, -190.0)
		_pointer.position = target + pointer_offset - _pointer.size * 0.5


func _announce_current_target() -> void:
	if not _announcements_enabled or m == null:
		return
	if not m.day_one_room_polish_is_complete("art"):
		_speak_cue("Tap the big rainbow spill on the open floor!", "talk")
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
		_speak_cue("The magic paint desk is ready! Tap it!", "win")


func _speak_cue(message: String, mood: String) -> void:
	m.show_msg("Roshan", message, mood)
	m._say("roshan", "talk")


func _all_materials_collected() -> bool:
	for material: Dictionary in MATERIALS:
		if not bool(m.day_one_art_collected_materials.get(
				String(material["id"]), false)):
			return false
	return true


func _next_uncollected_material_id() -> String:
	for material: Dictionary in MATERIALS:
		var material_id: String = String(material["id"])
		if not bool(m.day_one_art_collected_materials.get(material_id, false)):
			return material_id
	return ""


func _next_uncleaned_grime_id() -> String:
	for grime: Dictionary in GRIME:
		var grime_id: String = String(grime["id"])
		if not bool(m.day_one_art_cleaned_grime.get(grime_id, false)):
			return grime_id
	return ""


func _active_target_count() -> int:
	var count := 0
	if _rainbow_button != null and _rainbow_button.visible \
			and _rainbow_button.mouse_filter == Control.MOUSE_FILTER_STOP:
		count += 1
	for button_value: Variant in _material_buttons.values():
		var material_button: Button = button_value as Button
		if material_button != null and material_button.visible \
				and material_button.mouse_filter == Control.MOUSE_FILTER_STOP:
			count += 1
	for button_value: Variant in _grime_buttons.values():
		var grime_button: Button = button_value as Button
		if grime_button != null and grime_button.visible \
				and grime_button.mouse_filter == Control.MOUSE_FILTER_STOP:
			count += 1
	if _desk_button != null and _desk_button.visible \
			and _desk_button.mouse_filter == Control.MOUSE_FILTER_STOP:
		count += 1
	return count


func _visible_grime_count() -> int:
	var count := 0
	for card_value: Variant in _grime_art.values():
		var card: Sprite2D = card_value as Sprite2D
		if card != null and card.visible:
			count += 1
	return count


func _target_visual_bounds_clear_tables() -> bool:
	var cards: Array[Sprite2D] = []
	if _rainbow_art != null:
		cards.append(_rainbow_art)
	for card_value: Variant in _material_art.values():
		var material_card: Sprite2D = card_value as Sprite2D
		if material_card != null:
			cards.append(material_card)
	for card_value: Variant in _grime_art.values():
		var grime_card: Sprite2D = card_value as Sprite2D
		if grime_card != null:
			cards.append(grime_card)
	for card: Sprite2D in cards:
		var bounds: Rect2 = card.get_meta(
			"source_art_bounds", Rect2()) as Rect2
		for table_rect: Rect2 in TABLE_OWNERSHIP_RECTS:
			if bounds.grow(TABLE_CLEARANCE_MARGIN).intersects(table_rect):
				return false
	return true


func _table_visual_owner_count(side: String) -> int:
	if m == null or m.castle_room_front_layer == null:
		return 0
	var count := 0
	for child: Node in m.castle_room_front_layer.get_children():
		if child is CanvasItem and (child as CanvasItem).visible \
				and String(child.get_meta("table_owner_side", "")) == side:
			count += 1
	return count


func _table_alpha_cleanup_pass() -> bool:
	if m == null or m.castle_room_front_layer == null:
		return false
	for side: String in ["left", "right"]:
		var found: bool = false
		for child: Node in m.castle_room_front_layer.get_children():
			if String(child.get_meta("table_owner_side", "")) != side:
				continue
			found = true
			if String(child.get_meta("alpha_cleanup_method", "")) \
					!= "approved_rgb_plus_reviewed_body_polygons_v2":
				return false
		if not found:
			return false
	return true


func _pointer_clears_player_face() -> bool:
	if _pointer == null or not _pointer.visible or m == null \
			or m.castle_room_player_sprite == null:
		return true
	# The player card uses a transparent multi-pose atlas, so its raw texture
	# bounds are much larger than Roshan's visible face. Audit the authored face
	# pocket relative to the stage-foot anchor instead.
	var stage_foot: Vector2 = m.castle_room_player_sprite.get_meta(
		"stage_foot", Vector2(640.0, 640.0)) as Vector2
	var face_rect := Rect2(stage_foot + Vector2(-62.0, -250.0),
		Vector2(124.0, 140.0))
	var pointer_rect := Rect2(
		_pointer.position * ART_TO_STAGE,
		_pointer.size * ART_TO_STAGE)
	return not pointer_rect.intersects(face_rect)


func _set_legacy_room_controls_suppressed(suppressed: bool) -> void:
	if m == null:
		return
	for record_value: Variant in m.castle_room_item_sprites.values():
		var record: Dictionary = record_value as Dictionary
		var hotspot: Button = record.get("hotspot") as Button
		if hotspot != null and is_instance_valid(hotspot):
			hotspot.set_meta("day_one_art_suppressed", suppressed)
			hotspot.disabled = suppressed
			hotspot.visible = not suppressed


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
