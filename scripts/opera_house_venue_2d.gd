class_name OperaHouseVenue2D
extends Control
## True-2D reconstruction of the July 21 three-floor Pearl Opera House.
##
## The accepted master painting supplies every visible portal. Controls are
## physical portal hit regions. Reused career pictures identify the owner-requested
## four-door waves; the accepted background and Roshan source art are unchanged.

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
# Owner correction 2026-10-17: four foyer jobs, then four balcony jobs.
# The existing Magician remains reachable in the upper gallery after those eight.
const FIRST_WAVE: Array[int] = [6, 0, 3, 10]
const SECOND_WAVE: Array[int] = [2, 13, 11, 1]
const FIRST_WAVE_MASK := 0x0449
const DOOR_X: Array[float] = [382.0, 513.0, 643.0, 773.0]
const FLOOR_Y: Array[float] = [526.0, 352.0, 190.0]
const SAFE_FEET := Vector2(640.0, 704.0)
const FOOT_OFFSET := Vector2(56.0, 124.0)
const WALK_SPEED := 420.0
const FLOOR_AREAS: Array[Rect2] = [
	Rect2(350, 510, 590, 42), Rect2(355, 526, 195, 178),
	Rect2(730, 526, 195, 178), Rect2(170, 690, 910, 20),
]
var m: ReefMain
var launch_career: Callable
var buttons: Array[Button] = []
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
var pending_act := -1
var motion: Tween
var navigation := StageNavigation2D.new()
var feet := SAFE_FEET
var touch_owner := -1
var touch_start := Vector2.ZERO
var touch_dragged := false
var suppress_portal_press := false
var last_guide_act := -1
var last_refresh_mask := -1
var last_refresh_objective := ""
var background_input: Control
var elapsed := 0.0
var practice_book: TextureButton
var tree_book_test: OperaTreeBookTest
var job_playtest_menu: OperaJobPlaytestMenu


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
	_configure_walk_lanes()
	set_meta("historical_layout_commit", HISTORICAL_LAYOUT_COMMIT)
	set_meta("true_2d_venue", true)
	set_meta("historical_floor_count", 3)
	set_meta("historical_portal_count", 12)
	set_meta("active_room_owned_portal_count", active_act_indices.size())
	set_meta("decorative_closed_portal_count",
		12 - active_act_indices.size())
	set_meta("bubble_lift_count", 0)
	set_meta("floating_portal_decoration_count", 0)
	set_meta("chapter2_initial_tutorial_mode", chapter2_tutorial_mode)
	_build_background_tiles()
	_build_input_blocker()
	_build_floor_glow()
	_build_actor()
	_build_portals()
	_build_guide_pointer()
	_build_practice_book()
	_build_playtest_elevator()
	refresh(star_mask)


func open(star_mask: int) -> void:
	m._navigation_push("opera_venue", self, Callable(self, "_go_back"))
	visible = true
	accepting_input = true
	refresh(star_mask)
	guide_current_floor()


func _go_back() -> void:
	close()
	m._castle_rooms_ref().show_room("main_hall", true)


func close() -> void:
	if job_playtest_menu != null:
		job_playtest_menu.shutdown()
	_close_tree_book(false)
	m._navigation_remove("opera_venue")
	_cancel_travel()
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
	return buttons.duplicate()


func refresh(star_mask: int) -> void:
	# sync() runs every frame. Rebuild button/guide state only when its inputs
	# change, so director entry copies and focus selection are not frame work.
	var stamp: int = star_mask | (m.chapter2_party_piece_mask << 18) \
		| (int(m.chapter2_is_active()) << 36) | (int(accepting_input) << 37) \
		| (int(pending_act >= 0) << 38) | (int(m.chapter2_party_started) << 39) \
		| (int(m.chapter2_ember_king_crashed) << 40) \
		| (int(m.day_one_jobs_locked()) << 41) | (int(is_visible_in_tree()) << 42)
	if stamp == last_refresh_mask and m.chapter2_active_objective == last_refresh_objective:
		return
	last_refresh_mask = stamp
	last_refresh_objective = m.chapter2_active_objective
	if practice_book != null:
		practice_book.disabled = not accepting_input
	for button: Button in buttons:
		var act_index := int(button.get_meta("act_index", -1))
		var complete := _portal_is_complete(act_index, star_mask)
		button.disabled = (not accepting_input and pending_act < 0) or not can_enter(act_index)
		button.set_meta("complete", complete)
		var picture := button.get_node_or_null("CareerPicture") as TextureRect
		if picture != null:
			picture.modulate.a = 0.28 if button.disabled and not complete else 1.0
	_update_actor()
	guide_current_floor()
	var next_act := int(guide_button.get_meta("act_index", -1)) if guide_button != null else -1
	if is_visible_in_tree() and accepting_input and m.opera_game == null \
			and next_act >= 0 and next_act != last_guide_act:
		last_guide_act = next_act
		_speak_guide()


func second_wave_is_open() -> bool:
	var mask := m.chapter2_party_piece_mask if m.chapter2_is_active() else m.opera_stars
	return (mask & FIRST_WAVE_MASK) == FIRST_WAVE_MASK


func can_enter(act_index: int) -> bool:
	if not active_act_indices.has(act_index) or m.day_one_jobs_locked():
		return false
	if SECOND_WAVE.has(act_index) and not second_wave_is_open():
		return false
	if act_index == 8 and (m.chapter2_is_active()
			or (m.opera_stars & ChapterTwoPartyPlan.ALL_PARTY_MASK)
			!= ChapterTwoPartyPlan.ALL_PARTY_MASK):
		return false
	if not m.chapter2_is_active():
		return true
	if act_index == ChapterTwoDirector.ACT_BALLERINA:
		return m._chapter_two_ref().can_start_stuffie_ballet()
	if act_index == ChapterTwoDirector.ACT_DETECTIVE:
		return m._chapter_two_ref().room_plot_action("library") \
			== ChapterTwoDirector.ACTION_DETECTIVE_SEARCH
	return m.chapter2_can_start_opera_act(act_index)


func guide_current_floor() -> bool:
	guide_button = null
	if not visible or not accepting_input:
		return false
	var fallback: Button = null
	for button: Button in buttons:
		if button.disabled:
			continue
		if fallback == null:
			fallback = button
		var act_index := int(button.get_meta("act_index", -1))
		if not _portal_is_complete(act_index, m.opera_stars):
			guide_button = button
			break
	if guide_button == null:
		guide_button = fallback
	if guide_button != null:
		if guide_button.is_inside_tree() and not guide_button.has_focus():
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
	chapter2_tutorial_mode = false
	active_act_indices.assign(FIRST_WAVE + SECOND_WAVE + [8])
	for slot: int in range(active_act_indices.size()):
		var act_index := active_act_indices[slot]
		var floor_id := mini(slot / 4, 2)
		var column := slot % 4
		portal_rects[act_index] = Rect2(DOOR_X[column],
			408.0 if floor_id == 0 else (220.0 if floor_id == 1 else 63.0),
			126.0, 166.0 if floor_id == 0 else 156.0)
		act_floors[act_index] = floor_id


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
	background_input = blocker
	blocker.gui_input.connect(_floor_input)


func _build_floor_glow() -> void:
	floor_glow = ColorRect.new()
	floor_glow.name = "CurrentFloorFootlight"
	floor_glow.position = Vector2(292.0, 708.0)
	floor_glow.size = Vector2(696.0, 5.0)
	floor_glow.color = Color(1.0, 0.84, 0.42, 0.58)
	floor_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	floor_glow.z_index = 2
	add_child(floor_glow)


func _build_actor() -> void:
	actor = TextureRect.new()
	actor.name = "LobbyRoshanCutout"
	actor.position = SAFE_FEET - FOOT_OFFSET
	actor.size = Vector2(112.0, 132.0)
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	actor.texture = load(FashionOutfitRenderer.path(m, ROSHAN_TEXTURE)) as Texture2D
	actor.z_index = 9
	actor.set_meta("source_asset_role", "character")
	add_child(actor)


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
		button.set_meta("object_id", "opera.foyer.act.%02d" % act_index)
		button.set_meta("approach_point", Vector2(rect.get_center().x, FLOOR_Y[portal_floor]))
		button.set_meta("arrival_radius", 6.0)
		button.set_meta("action", "enter_career")
		button.set_meta("return_target", "opera_hall")
		button.set_meta("presentation",
			"chapter2_initial_tutorial_portal" if chapter2_tutorial_mode \
			else "historical_three_floor_portal")
		button.set_meta("opaque_card", false)
		button.set_meta("painted_door_hit_region", true)
		button.set_meta("floating_decoration", false)
		button.set_meta("screen_hit_size", rect.size)
		_style_portal_button(button)
		button.pressed.connect(_on_portal_pressed.bind(act_index))
		button.gui_input.connect(_portal_input.bind(act_index))
		_build_career_picture(button, act_index)
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
	guide_pointer.visible = true


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
	if (not accepting_input and pending_act < 0) or not can_enter(act_index):
		return
	guide_button = _button_for_act(act_index)
	var target: Vector2 = guide_button.get_meta("approach_point") as Vector2
	_update_guide_pointer()
	_speak_career(act_index)
	travel_to(target, act_index)


func travel_to(target: Vector2, act_index: int = -1) -> void:
	if not accepting_input and pending_act < 0:
		return
	_cancel_travel()
	var destination := _walkable_point(target)
	var lanes: Array[PackedVector2Array] = navigation.branches.duplicate()
	lanes.append(PackedVector2Array([feet, navigation.nearest_point(feet)]))
	lanes.append(PackedVector2Array([destination, navigation.nearest_point(destination)]))
	navigation.configure(lanes)
	var path := navigation.route(feet, destination)
	_configure_walk_lanes()
	if path.is_empty():
		return
	motion = create_tween()
	for index in range(1, path.size()):
		motion.tween_method(_set_feet, path[index - 1], path[index],
			maxf(0.02, path[index - 1].distance_to(path[index]) / WALK_SPEED))
	if act_index >= 0:
		pending_act = act_index
		accepting_input = false
		motion.tween_callback(_launch_selected.bind(act_index))


func _launch_selected(act_index: int) -> void:
	pending_act = -1
	accepting_input = true
	var button := _button_for_act(act_index)
	var arrived := button != null and feet.distance_to(
		button.get_meta("approach_point") as Vector2) <= float(button.get_meta("arrival_radius"))
	if is_visible_in_tree() and arrived and can_enter(act_index) and launch_career.is_valid():
		launch_career.call(act_index)
	refresh(m.opera_stars)


func _cancel_travel() -> void:
	if pending_act >= 0:
		accepting_input = true
	pending_act = -1
	if motion != null and motion.is_valid():
		motion.kill()
	motion = null
	touch_owner = -1


func _set_feet(point: Vector2) -> void:
	feet = _walkable_point(point)
	_update_actor()


func _walkable_point(point: Vector2) -> Vector2:
	for area: Rect2 in FLOOR_AREAS:
		if area.has_point(point):
			return point
	return navigation.nearest_point(point)


func _update_actor() -> void:
	if actor == null:
		return
	floor_index = 0 if feet.y > 410.0 else (1 if feet.y > 260.0 else 2)
	var actor_scale := 1.0 if floor_index == 0 else 0.80
	actor.scale = Vector2.ONE * actor_scale
	actor.position = feet - FOOT_OFFSET * actor_scale


func _configure_walk_lanes() -> void:
	# Floor aisles avoid the three sofas; stair corners follow the painting.
	# The right brass lift connects the upper gallery without crossing a wall.
	var lanes: Array[PackedVector2Array] = [
		PackedVector2Array([Vector2(180, 704), Vector2(1080, 704)]),
		PackedVector2Array([Vector2(350, 526), Vector2(940, 526)]),
		PackedVector2Array([Vector2(450, 704), Vector2(450, 526)]),
		PackedVector2Array([Vector2(830, 704), Vector2(830, 526)]),
		PackedVector2Array([Vector2(350, 526), Vector2(270, 526),
			Vector2(248, 500), Vector2(292, 430), Vector2(350, 352)]),
		PackedVector2Array([Vector2(940, 526), Vector2(1010, 526),
			Vector2(1032, 500), Vector2(988, 430), Vector2(930, 352)]),
		PackedVector2Array([Vector2(350, 352), Vector2(930, 352)]),
		PackedVector2Array([Vector2(1010, 526), Vector2(1090, 526),
			Vector2(1090, 190), Vector2(930, 190), Vector2(350, 190)]),
	]
	navigation.configure(lanes)


func _floor_input(event: InputEvent) -> void:
	if not visible or (not accepting_input and pending_act < 0):
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed and touch_owner == -1:
			_cancel_travel()
			touch_owner = touch.index
			touch_start = touch.position
			touch_dragged = false
		elif not touch.pressed and touch.index == touch_owner:
			touch_owner = -1
			if touch.canceled:
				_cancel_travel()
			else:
				_commit_floor_release(touch.position)
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == touch_owner:
			touch_dragged = touch_start.distance_to(drag.position) > 16.0
	elif event is InputEventMouseButton:
		var mouse := event as InputEventMouseButton
		if mouse.button_index == MOUSE_BUTTON_LEFT:
			if mouse.pressed and touch_owner == -1:
				_cancel_travel()
				touch_owner = -2
			elif not mouse.pressed and touch_owner == -2:
				touch_owner = -1
				_commit_floor_release(mouse.position)
	background_input.accept_event()


func _commit_floor_release(point: Vector2) -> void:
	for button: Button in buttons:
		if not button.disabled and Rect2(button.position, button.size).has_point(point):
			touch_dragged = false
			_choose_career(int(button.get_meta("act_index")))
			return
	travel_to(point)


func _on_portal_pressed(act_index: int) -> void:
	# Screen touches are committed below by their owning finger. This signal
	# retains ordinary mouse, keyboard and accessibility button activation.
	if not suppress_portal_press and touch_owner == -1:
		_choose_career(act_index)


func _clear_portal_suppression() -> void:
	suppress_portal_press = false


func _portal_input(event: InputEvent, act_index: int) -> void:
	if event is InputEventScreenTouch:
		suppress_portal_press = true
		call_deferred("_clear_portal_suppression")
		var touch := event as InputEventScreenTouch
		var button := _button_for_act(act_index)
		if touch.pressed and touch_owner == -1:
			_cancel_travel()
			touch_owner = touch.index
			touch_start = touch.position + button.position
			touch_dragged = false
		elif not touch.pressed and touch.index == touch_owner:
			touch_owner = -1
			if touch.canceled:
				_cancel_travel()
			else:
				_commit_floor_release(touch.position + button.position)
	elif event is InputEventMouseButton:
		var mouse := event as InputEventMouseButton
		if mouse.button_index != MOUSE_BUTTON_LEFT:
			return
		suppress_portal_press = true
		call_deferred("_clear_portal_suppression")
		if mouse.pressed and touch_owner == -1:
			_cancel_travel()
			touch_owner = -2
		elif not mouse.pressed and touch_owner == -2:
			touch_owner = -1
			var button := _button_for_act(act_index)
			_commit_floor_release(mouse.position + button.position)
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == touch_owner:
			touch_dragged = true


func _notification(what: int) -> void:
	if what in [NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_APPLICATION_PAUSED, NOTIFICATION_PAUSED]:
		_cancel_travel()
		accepting_input = visible and tree_book_test == null \
			and (job_playtest_menu == null or not job_playtest_menu.session_open)


func _button_for_act(act_index: int) -> Button:
	for button: Button in buttons:
		if int(button.get_meta("act_index", -1)) == act_index:
			return button
	return null


func _speak_guide() -> void:
	if guide_button != null:
		_speak_career(int(guide_button.get_meta("act_index")))


func _speak_career(act_index: int) -> void:
	m._audio_ref().chapter_two_prompt("op_" + String(
		(OperaHouse.ACTS[act_index] as Dictionary).get("costume", "")) + "_work")


func _build_career_picture(button: Button, act_index: int) -> void:
	var crest_file := String(CastleCareerRoutes.CAREER_CREST_FILES.get(
		String((OperaHouse.ACTS[act_index] as Dictionary).get("costume", "")), ""))
	if crest_file.is_empty():
		return
	var picture := TextureRect.new()
	picture.name = "CareerPicture"
	picture.position = Vector2(31, 48)
	picture.size = Vector2(64, 64)
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	picture.texture = load(CastleCareerRoutes.CREST_ROOT + crest_file) as Texture2D
	button.add_child(picture)


func _process(delta: float) -> void:
	if is_visible_in_tree() and (accepting_input or pending_act >= 0):
		var axis := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
		axis += Vector2(float(Input.is_physical_key_pressed(KEY_D)) - float(Input.is_physical_key_pressed(KEY_A)),
			float(Input.is_physical_key_pressed(KEY_S)) - float(Input.is_physical_key_pressed(KEY_W)))
		axis = axis.limit_length()
		if axis.length_squared() > 0.01:
			_cancel_travel()
			_set_feet(feet + axis * WALK_SPEED * delta)
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

func _build_practice_book() -> void:
	practice_book = TextureButton.new()
	practice_book.name = "TreeBookPractice"
	practice_book.z_index = 8
	practice_book.position = Vector2(1032, 552)
	practice_book.size = Vector2(174, 131)
	practice_book.texture_normal = load("res://assets/opera/tree_book_test/book.png") as Texture2D
	practice_book.ignore_texture_size = true
	practice_book.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	practice_book.tooltip_text = "Tree Book practice"
	practice_book.pressed.connect(open_tree_book)
	add_child(practice_book)
	var tree := TextureRect.new()
	tree.position = Vector2(58, 33)
	tree.size = Vector2(66, 64)
	var atlas := AtlasTexture.new()
	atlas.atlas = load("res://assets/opera/tree_book_test/patient.png") as Texture2D
	atlas.region = Rect2(0, 0, 512, 512)
	tree.texture = atlas
	tree.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tree.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	tree.mouse_filter = Control.MOUSE_FILTER_IGNORE
	practice_book.add_child(tree)


func _build_playtest_elevator() -> void:
	if not OperaJobPlaytestMenu.ENABLED:
		return
	job_playtest_menu = OperaJobPlaytestMenu.new()
	job_playtest_menu.setup(m, self)
	add_child(job_playtest_menu)
	var elevator := Button.new()
	elevator.name = "OperaLeftElevatorPlaytest"
	# The accepted painting's left brass elevator gate at base-canvas scale.
	elevator.position = Vector2(178.0, 390.0)
	elevator.size = Vector2(136.0, 134.0)
	elevator.text = ""
	elevator.tooltip_text = "Open job playtesting"
	elevator.z_index = 8
	elevator.set_meta("painted_elevator_hit_region", true)
	_style_portal_button(elevator)
	elevator.pressed.connect(job_playtest_menu.open)
	add_child(elevator)


func open_tree_book() -> void:
	if not visible or not accepting_input or tree_book_test != null or touch_owner >= 0:
		return
	_cancel_travel()
	accepting_input = false
	m._set_world_controls_enabled(false, "tree_book_practice")
	refresh(m.opera_stars)
	if guide_pointer != null:
		guide_pointer.hide()
	tree_book_test = OperaTreeBookTest.new()
	tree_book_test.setup(m, m.save_data.get(OperaTreeBookTest.SAVE_KEY, {}))
	tree_book_test.checkpoint_changed.connect(_save_tree_book)
	tree_book_test.close_requested.connect(_close_tree_book)
	add_child(tree_book_test)
	m._navigation_push("arborist_tree_book_test", tree_book_test, Callable(self, "_close_tree_book"))


func _save_tree_book(checkpoint: Dictionary) -> void:
	m.save_data[OperaTreeBookTest.SAVE_KEY] = checkpoint
	m._queue_save()


func _close_tree_book(restore_venue: bool = true) -> void:
	if tree_book_test == null:
		return
	tree_book_test.shutdown()
	tree_book_test.queue_free()
	tree_book_test = null
	m._navigation_remove("arborist_tree_book_test")
	m._set_world_controls_enabled(true, "tree_book_practice")
	m._write_save()
	if restore_venue and visible:
		accepting_input = true
		refresh(m.opera_stars)
