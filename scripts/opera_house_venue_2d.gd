class_name OperaHouseVenue2D
extends Control
## True-2D reconstruction of the July 21 three-floor Pearl Opera House.
##
## The accepted master painting supplies every visible portal. Controls are
## invisible physical portal/lift hit regions; there is no card grid, career
## crest, floating door frame, completion pearl, or all-career menu.

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const TILE_ROOT := \
	"res://assets/flats/castle/opera_house_venue_2d/background_tiles/"
const TILE_LOGICAL_SIZE := Vector2(320.0, 360.0)
const TILE_COLUMNS := 4
const TILE_ROWS := 2
const HISTORICAL_LAYOUT_COMMIT := "90d19190"
const ROSHAN_TEXTURE := \
	"res://assets/characters/roshan_25d/roshan_base.png"
const GHOST_HAND_TEXTURE := "res://assets/castle/training/ghost_hand.png"
const FLOOR_NAMES: Array[String] = [
	"Lagoon Lights Foyer",
	"Starlight Balcony",
	"Grand Gallery",
]
const LEGACY_FLOOR_ACT_INDICES: Array[int] = [2, 8, 13]
const FLOOR_ACTOR_POSITIONS: Array[Vector2] = [
	Vector2(584.0, 548.0),
	Vector2(584.0, 354.0),
	Vector2(584.0, 166.0),
]
const LEGACY_PORTAL_RECTS := {
	2: Rect2(674.0, 408.0, 126.0, 166.0),
	8: Rect2(900.0, 236.0, 126.0, 160.0),
	13: Rect2(830.0, 63.0, 126.0, 156.0),
}
# Four painted foyer doors become the opening Chapter 2 tutorial set. These
# rectangles are measured from the accepted venue painting; no floating cards
# or duplicate door art are added.
const CHAPTER2_PORTAL_RECTS := {
	0: Rect2(382.0, 408.0, 126.0, 166.0),
	1: Rect2(526.0, 408.0, 126.0, 166.0),
	2: Rect2(674.0, 408.0, 126.0, 166.0),
	3: Rect2(817.0, 408.0, 126.0, 166.0),
}
const CHAPTER2_SECOND_WAVE_PORTAL_RECTS := {
	11: Rect2(382.0, 220.0, 126.0, 156.0),
	13: Rect2(817.0, 220.0, 126.0, 156.0),
}
const LIFT_RECTS: Array[Rect2] = [
	Rect2(144.0, 79.0, 126.0, 500.0),
	Rect2(1012.0, 79.0, 126.0, 500.0),
]
const LIFT_ACTOR_X: Array[float] = [164.0, 1024.0]
var m: ReefMain
var launch_career: Callable
var buttons: Array[Button] = []
var lifts: Array[Button] = []
var active_act_indices: Array[int] = []
var portal_rects: Dictionary = {}
var act_floors: Dictionary = {}
var chapter2_tutorial_mode := false
var floor_index := 0
var accepting_input := true
var actor: TextureRect
var floor_glow: ColorRect
var guide_button: Button
var guide_pointer: Sprite2D
var guide_pointer_base := Vector2.ZERO
var motion: Tween
var elapsed := 0.0


func setup(main: ReefMain, star_mask: int, launch_callback: Callable) -> void:
	m = main
	launch_career = launch_callback
	name = "OperaHouseVenue2D"
	visible = false
	accepting_input = false
	position = Vector2.ZERO
	size = CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 42
	_configure_portals()
	set_meta("historical_layout_commit", HISTORICAL_LAYOUT_COMMIT)
	set_meta("true_2d_venue", true)
	set_meta("historical_floor_count", 3)
	set_meta("historical_portal_count", 12)
	set_meta("active_room_owned_portal_count", active_act_indices.size())
	set_meta("decorative_closed_portal_count",
		12 - active_act_indices.size())
	set_meta("bubble_lift_count", 2)
	set_meta("floating_portal_decoration_count", 0)
	set_meta("chapter2_initial_tutorial_mode", chapter2_tutorial_mode)
	_build_background_tiles()
	_build_input_blocker()
	_build_floor_glow()
	_build_actor()
	_build_portals()
	_build_guide_pointer()
	_build_lifts()
	_build_back_button()
	refresh(star_mask)


func open(star_mask: int) -> void:
	visible = true
	accepting_input = true
	refresh(star_mask)
	guide_current_floor()


func close() -> void:
	accepting_input = false
	guide_button = null
	if guide_pointer != null:
		guide_pointer.visible = false
	if motion != null and motion.is_valid():
		motion.kill()
	motion = null
	visible = false


func is_open() -> bool:
	return visible


func is_chapter2_tutorial_mode() -> bool:
	return chapter2_tutorial_mode


func career_buttons() -> Array[Button]:
	# Keep the established room-route order stable even though the physical
	# venue is built from ground floor upward.
	var ordered: Array[Button] = []
	var requested_order: Array[int] = active_act_indices.duplicate()
	if not chapter2_tutorial_mode and not (m != null and m.chapter2_is_active()):
		requested_order = [2, 13, 8]
	for act_index: int in requested_order:
		for button: Button in buttons:
			if int(button.get_meta("act_index", -1)) == act_index:
				ordered.append(button)
				break
	return ordered


func refresh(star_mask: int) -> void:
	for button: Button in buttons:
		var act_index := int(button.get_meta("act_index", -1))
		var portal_floor := int(button.get_meta("floor_index", -1))
		var on_floor := portal_floor == floor_index
		var complete := _portal_is_complete(act_index, star_mask)
		var chapter2_complete := chapter2_tutorial_mode \
			or (m != null and m.chapter2_is_active())
		button.disabled = not on_floor or not accepting_input \
			or not m.chapter2_can_start_opera_act(act_index) \
			or (chapter2_complete and complete)
		button.set_meta("complete", complete)
		button.set_meta("chapter2_skill_complete",
			chapter2_tutorial_mode and complete)
		button.set_meta("chapter2_party_complete",
			m != null and m.chapter2_is_active() and not chapter2_tutorial_mode \
			and complete)
	if actor != null:
		actor.position = FLOOR_ACTOR_POSITIONS[floor_index]
	if floor_glow != null:
		floor_glow.position.y = FLOOR_ACTOR_POSITIONS[floor_index].y + 118.0
	guide_current_floor()


func guide_current_floor() -> bool:
	guide_button = null
	if not visible or not accepting_input:
		return false
	var candidates: Array[Button] = []
	for button: Button in buttons:
		if int(button.get_meta("floor_index", -1)) == floor_index \
				and not button.disabled:
			candidates.append(button)
	for button: Button in candidates:
		var act_index := int(button.get_meta("act_index", -1))
		if not _portal_is_complete(act_index, m.opera_stars):
			guide_button = button
			if button.is_inside_tree():
				button.grab_focus()
			_update_guide_pointer()
			return true
	if not candidates.is_empty():
		guide_button = candidates[0]
		if guide_button.is_inside_tree():
			guide_button.grab_focus()
		_update_guide_pointer()
		return true
	if guide_pointer != null:
		guide_pointer.visible = false
	return false


func _portal_is_complete(act_index: int, star_mask: int) -> bool:
	if act_index < 0:
		return false
	var bit := 1 << act_index
	if chapter2_tutorial_mode:
		# Opening lessons are deliberately non-star runs. Their door state and
		# guide progression come from the director's learned-skill mask only.
		return m != null and (int(m._chapter_two_ref().skill_mask) & bit) != 0
	if m != null and m.chapter2_is_active():
		# A plot-only Stuffie Ballet makes act 2 a completed party contribution;
		# keep its historical Opera Hall portal visible but unavailable. Legacy
		# Opera stars do not count as birthday prep: a returning save must still
		# be able to make the Magician and Pop Star party contributions.
		return (int(m._chapter_two_ref().party_piece_mask) & bit) != 0
	return (star_mask & bit) != 0


func _configure_portals() -> void:
	# The four-door surface lasts only while the Chapter 2 director is asking
	# for Opera skill lessons. Candle/ballet plot beats and post-onboarding
	# free play use the historical room-distributed Opera routes again.
	chapter2_tutorial_mode = m != null and m.chapter2_is_active() \
		and m._chapter_two_ref().is_opera_priority()
	active_act_indices.clear()
	portal_rects.clear()
	act_floors.clear()
	if chapter2_tutorial_mode:
		active_act_indices = m.chapter2_initial_tutorial_act_indices()
		for act_index: int in active_act_indices:
			portal_rects[act_index] = CHAPTER2_PORTAL_RECTS[act_index]
			act_floors[act_index] = 0
		return
	if m != null and m.chapter2_is_active():
		# The venue shows only the eight-career birthday roster. Ballerina and
		# Detective remain room-owned plot actions; their normal doors are not
		# duplicated here. The first wave is supplied by the director mask, and
		# the second wave appears after Painter completes.
		for act_index: int in ChapterTwoPartyPlan.GUIDE_ORDER:
			if act_index in [ChapterTwoDirector.ACT_BALLERINA,
					ChapterTwoDirector.ACT_DETECTIVE]:
				continue
			if (int(m._chapter_two_ref().unlocked_opera_mask) & (1 << act_index)) == 0:
				continue
			active_act_indices.append(act_index)
			var rect: Rect2 = CHAPTER2_PORTAL_RECTS.get(
				active_act_indices.size() - 1,
				CHAPTER2_SECOND_WAVE_PORTAL_RECTS.get(act_index,
					Rect2(0.0, 0.0, 126.0, 156.0)))
			if active_act_indices.size() > CHAPTER2_PORTAL_RECTS.size():
				rect = CHAPTER2_SECOND_WAVE_PORTAL_RECTS.get(act_index, rect)
			portal_rects[act_index] = rect
			act_floors[act_index] = 0
		return
	active_act_indices = LEGACY_FLOOR_ACT_INDICES.duplicate()
	for legacy_floor in range(active_act_indices.size()):
		var act_index := active_act_indices[legacy_floor]
		portal_rects[act_index] = LEGACY_PORTAL_RECTS[act_index]
		act_floors[act_index] = legacy_floor


func _build_background_tiles() -> void:
	var tile_root := Control.new()
	tile_root.name = "AcceptedThreeFloorVenueTiles"
	tile_root.position = Vector2.ZERO
	tile_root.size = CANVAS_SIZE
	tile_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tile_root.z_index = 0
	add_child(tile_root)
	for row in range(TILE_ROWS):
		for column in range(TILE_COLUMNS):
			var path := TILE_ROOT \
				+ "room_opera_house_venue_background_r%d_c%d.png" % [
					row, column]
			var tile := TextureRect.new()
			tile.name = "VenueTile_r%d_c%d" % [row, column]
			tile.position = Vector2(
				float(column) * TILE_LOGICAL_SIZE.x,
				float(row) * TILE_LOGICAL_SIZE.y)
			tile.size = TILE_LOGICAL_SIZE
			tile.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			tile.stretch_mode = TextureRect.STRETCH_SCALE
			tile.mouse_filter = Control.MOUSE_FILTER_IGNORE
			tile.texture = load(path) as Texture2D
			tile.set_meta("source_asset_role", "clean_background_tile")
			tile.set_meta("source_master_grid", "2x4_3640x2048")
			tile_root.add_child(tile)


func _build_input_blocker() -> void:
	var blocker := Control.new()
	blocker.name = "VenueWorldInputBlocker"
	blocker.position = Vector2.ZERO
	blocker.size = CANVAS_SIZE
	blocker.mouse_filter = Control.MOUSE_FILTER_STOP
	blocker.z_index = 1
	add_child(blocker)


func _build_floor_glow() -> void:
	floor_glow = ColorRect.new()
	floor_glow.name = "CurrentFloorFootlight"
	floor_glow.position = Vector2(292.0, 666.0)
	floor_glow.size = Vector2(696.0, 5.0)
	floor_glow.color = Color(1.0, 0.84, 0.42, 0.58)
	floor_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	floor_glow.z_index = 2
	add_child(floor_glow)


func _build_actor() -> void:
	actor = TextureRect.new()
	actor.name = "LobbyRoshanCutout"
	actor.position = FLOOR_ACTOR_POSITIONS[0]
	actor.size = Vector2(112.0, 132.0)
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	actor.texture = load(ROSHAN_TEXTURE) as Texture2D
	actor.z_index = 5
	actor.set_meta("source_asset_role", "character")
	add_child(actor)
	var idle := actor.create_tween().set_loops()
	idle.tween_property(actor, "rotation", -0.018, 0.75) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	idle.tween_property(actor, "rotation", 0.018, 0.75) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


func _build_portals() -> void:
	for act_index: int in active_act_indices:
		var portal_floor := int(act_floors.get(act_index, 0))
		var rect: Rect2 = portal_rects[act_index]
		var button := Button.new()
		button.name = "OperaVenuePortal_%02d" % act_index
		button.position = rect.position
		button.size = rect.size
		button.custom_minimum_size = StorybookUI.MIN_TOUCH
		button.text = ""
		button.tooltip_text = "Enter %s" % String(
			(OperaHouse.ACTS[act_index] as Dictionary).get("career", "show"))
		button.focus_mode = Control.FOCUS_ALL
		button.clip_contents = false
		button.z_index = 8
		button.set_meta("act_index", act_index)
		button.set_meta("castle_room_id", "opera_hall")
		button.set_meta("floor_index", portal_floor)
		button.set_meta("presentation",
			"chapter2_initial_tutorial_portal" if chapter2_tutorial_mode \
			else "historical_three_floor_portal")
		button.set_meta("opaque_card", false)
		button.set_meta("painted_door_hit_region", true)
		button.set_meta("floating_decoration", false)
		button.set_meta("screen_hit_size", rect.size)
		_style_portal_button(button)
		button.pressed.connect(_choose_career.bind(act_index))
		add_child(button)
		buttons.append(button)


func _build_guide_pointer() -> void:
	guide_pointer = Sprite2D.new()
	guide_pointer.name = "ChapterTwoOperaDoorPointer"
	guide_pointer.texture = load(GHOST_HAND_TEXTURE) as Texture2D
	guide_pointer.scale = Vector2.ONE * 0.13
	guide_pointer.visible = false
	guide_pointer.z_index = 12
	guide_pointer.set_meta("visual_pointer", true)
	guide_pointer.set_meta("replacement_door_art", false)
	add_child(guide_pointer)


func _update_guide_pointer() -> void:
	if guide_pointer == null or guide_button == null:
		return
	guide_pointer_base = guide_button.position + Vector2(
		guide_button.size.x * 0.5, -10.0)
	guide_pointer.position = guide_pointer_base
	guide_pointer.visible = chapter2_tutorial_mode


func _build_lifts() -> void:
	for lift_index in range(LIFT_RECTS.size()):
		var rect := LIFT_RECTS[lift_index]
		var lift := Button.new()
		lift.name = "BubbleLift%d" % (lift_index + 1)
		lift.position = rect.position
		lift.size = rect.size
		lift.custom_minimum_size = StorybookUI.MIN_TOUCH
		lift.text = ""
		lift.tooltip_text = "Ride the bubble lift"
		lift.focus_mode = Control.FOCUS_ALL
		lift.z_index = 7
		lift.set_meta("physical_floor_cycle", [0, 1, 2])
		lift.set_meta("transparent_diegetic_hit_region", true)
		lift.visible = not chapter2_tutorial_mode
		lift.disabled = chapter2_tutorial_mode
		_style_lift_button(lift)
		lift.pressed.connect(_ride_lift.bind(lift_index))
		add_child(lift)
		lifts.append(lift)


func _build_back_button() -> void:
	var back := Button.new()
	back.name = "OperaVenueBack"
	StorybookUI.style_back_button(back, "Back to the Opera Hall")
	back.position = Vector2(18.0, 18.0)
	back.z_index = 12
	back.pressed.connect(close)
	add_child(back)


func _style_portal_button(button: Button) -> void:
	button.add_theme_stylebox_override("normal", _outline_style(
		Color.TRANSPARENT, Color.TRANSPARENT, 0, 54))
	button.add_theme_stylebox_override("hover", _outline_style(
		Color.TRANSPARENT, Color.TRANSPARENT, 0, 54))
	button.add_theme_stylebox_override("pressed", _outline_style(
		Color.TRANSPARENT, Color.TRANSPARENT, 0, 54))
	button.add_theme_stylebox_override("focus", _outline_style(
		Color.TRANSPARENT, Color.TRANSPARENT, 0, 54))
	button.add_theme_stylebox_override("disabled", _outline_style(
		Color.TRANSPARENT, Color.TRANSPARENT, 0, 54))


func _style_lift_button(button: Button) -> void:
	button.add_theme_stylebox_override("normal", _outline_style(
		Color.TRANSPARENT, Color.TRANSPARENT, 0, 52))
	button.add_theme_stylebox_override("hover", _outline_style(
		Color(0.66, 0.94, 1.0, 0.92), Color(0.48, 0.88, 1.0, 0.08), 4, 52))
	button.add_theme_stylebox_override("pressed", _outline_style(
		Color.WHITE, Color(0.55, 0.92, 1.0, 0.13), 5, 52))
	button.add_theme_stylebox_override("focus", _outline_style(
		Color(0.76, 0.96, 1.0, 1.0), Color(0.55, 0.92, 1.0, 0.10), 5, 52))


func _outline_style(border: Color, fill: Color, width: int,
		radius: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.set_border_width_all(width)
	style.set_corner_radius_all(radius)
	style.shadow_color = Color(0.18, 0.08, 0.26, 0.24) \
		if width > 0 else Color.TRANSPARENT
	style.shadow_size = 8 if width > 0 else 0
	style.shadow_offset = Vector2.ZERO
	return style


func _choose_career(act_index: int) -> void:
	if not accepting_input or int(act_floors.get(act_index, -1)) != floor_index \
			or not m.chapter2_can_start_opera_act(act_index):
		return
	accepting_input = false
	refresh(m.opera_stars)
	var rect: Rect2 = portal_rects[act_index]
	var target := Vector2(
		rect.get_center().x - actor.size.x * 0.5,
		FLOOR_ACTOR_POSITIONS[floor_index].y)
	_start_motion()
	motion.tween_property(actor, "position", target, 0.55) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	motion.tween_callback(_launch_selected.bind(act_index))


func _launch_selected(act_index: int) -> void:
	accepting_input = true
	if launch_career.is_valid():
		launch_career.call(act_index)


func _ride_lift(lift_index: int) -> void:
	if not accepting_input or chapter2_tutorial_mode:
		return
	accepting_input = false
	refresh(m.opera_stars)
	var next_floor := (floor_index + 1) % FLOOR_NAMES.size()
	var lift_position := Vector2(
		LIFT_ACTOR_X[lift_index], actor.position.y)
	var lifted_position := Vector2(
		LIFT_ACTOR_X[lift_index], FLOOR_ACTOR_POSITIONS[next_floor].y)
	_start_motion()
	motion.tween_property(actor, "position", lift_position, 0.38) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	motion.tween_property(actor, "position", lifted_position, 0.62) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	motion.tween_callback(_finish_lift.bind(next_floor))


func _finish_lift(next_floor: int) -> void:
	floor_index = next_floor
	accepting_input = true
	refresh(m.opera_stars)
	if m != null:
		m.show_msg("Pearl Opera House", FLOOR_NAMES[floor_index], "home")


func _start_motion() -> void:
	if motion != null and motion.is_valid():
		motion.kill()
	motion = create_tween()


func _process(delta: float) -> void:
	if not visible or guide_button == null or not is_instance_valid(guide_button):
		return
	elapsed += delta
	var glow := 0.88 + sin(elapsed * 3.2) * 0.12
	guide_button.modulate = Color(1.0, 1.0, glow, 1.0)
	if guide_pointer != null and guide_pointer.visible:
		guide_pointer.position.y = guide_pointer_base.y \
			+ sin(elapsed * 4.0) * 10.0
	if floor_glow != null:
		floor_glow.modulate.a = 0.72 + sin(elapsed * 2.6) * 0.20
