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
const FLOOR_NAMES: Array[String] = [
	"Lagoon Lights Foyer",
	"Starlight Balcony",
	"Grand Gallery",
]
const FLOOR_ACT_INDICES: Array[int] = [2, 8, 13]
const FLOOR_ACTOR_POSITIONS: Array[Vector2] = [
	Vector2(584.0, 548.0),
	Vector2(584.0, 354.0),
	Vector2(584.0, 166.0),
]
const PORTAL_RECTS := {
	2: Rect2(674.0, 408.0, 126.0, 166.0),
	8: Rect2(900.0, 236.0, 126.0, 160.0),
	13: Rect2(830.0, 63.0, 126.0, 156.0),
}
const LIFT_RECTS: Array[Rect2] = [
	Rect2(144.0, 79.0, 126.0, 500.0),
	Rect2(1012.0, 79.0, 126.0, 500.0),
]
const LIFT_ACTOR_X: Array[float] = [164.0, 1024.0]
var m: ReefMain
var launch_career: Callable
var buttons: Array[Button] = []
var floor_index := 0
var accepting_input := true
var actor: TextureRect
var floor_glow: ColorRect
var guide_button: Button
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
	set_meta("historical_layout_commit", HISTORICAL_LAYOUT_COMMIT)
	set_meta("true_2d_venue", true)
	set_meta("historical_floor_count", 3)
	set_meta("historical_portal_count", 12)
	set_meta("active_room_owned_portal_count", 3)
	set_meta("decorative_closed_portal_count", 9)
	set_meta("bubble_lift_count", 2)
	set_meta("floating_portal_decoration_count", 0)
	_build_background_tiles()
	_build_input_blocker()
	_build_floor_glow()
	_build_actor()
	_build_portals()
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
	if motion != null and motion.is_valid():
		motion.kill()
	motion = null
	visible = false


func is_open() -> bool:
	return visible


func career_buttons() -> Array[Button]:
	# Keep the established room-route order stable even though the physical
	# venue is built from ground floor upward.
	var ordered: Array[Button] = []
	for act_index: int in [2, 13, 8]:
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
		button.disabled = not on_floor or not accepting_input
		button.set_meta("complete", (star_mask & (1 << act_index)) != 0)
	if actor != null:
		actor.position = FLOOR_ACTOR_POSITIONS[floor_index]
	if floor_glow != null:
		floor_glow.position.y = FLOOR_ACTOR_POSITIONS[floor_index].y + 118.0
	guide_current_floor()


func guide_current_floor() -> bool:
	guide_button = null
	if not visible or not accepting_input or not is_inside_tree():
		return false
	var act_index := FLOOR_ACT_INDICES[floor_index]
	for button: Button in buttons:
		if int(button.get_meta("act_index", -1)) == act_index:
			guide_button = button
			button.grab_focus()
			return true
	return false


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
	for portal_floor in range(FLOOR_ACT_INDICES.size()):
		var act_index := FLOOR_ACT_INDICES[portal_floor]
		var rect: Rect2 = PORTAL_RECTS[act_index]
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
		button.set_meta("presentation", "historical_three_floor_portal")
		button.set_meta("opaque_card", false)
		button.set_meta("painted_door_hit_region", true)
		button.set_meta("floating_decoration", false)
		button.set_meta("screen_hit_size", rect.size)
		_style_portal_button(button)
		button.pressed.connect(_choose_career.bind(act_index))
		add_child(button)
		buttons.append(button)
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
		_style_lift_button(lift)
		lift.pressed.connect(_ride_lift.bind(lift_index))
		add_child(lift)


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
	if not accepting_input or FLOOR_ACT_INDICES[floor_index] != act_index:
		return
	accepting_input = false
	refresh(m.opera_stars)
	var rect: Rect2 = PORTAL_RECTS[act_index]
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
	if not accepting_input:
		return
	accepting_input = false
	refresh(m.opera_stars)
	var next_floor := (floor_index + 1) % FLOOR_ACT_INDICES.size()
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
	if floor_glow != null:
		floor_glow.modulate.a = 0.72 + sin(elapsed * 2.6) * 0.20
