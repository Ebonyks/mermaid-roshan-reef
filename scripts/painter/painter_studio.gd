class_name PainterStudio
extends Control
## Single-scene engine review. No story unlocks, currencies or career stars.
## Roshan hosts the child's direct art surface; this is not a remote job action.

signal leave_requested

const TEMPLATE := preload("res://scripts/painter/painter_template.gd")
const GUIDED_VOICE := preload("res://assets/audio/voices/filler_v1/roshan_op_painter_fill.ogg")
const DOCUMENT := preload("res://scripts/painter/painter_document.gd")
const UI := preload("res://scripts/storybook_ui.gd")
const ACTOR := preload("res://scripts/opera_roshan_actor.gd")
const BACKDROP := preload("res://assets/opera/worlds/backdrops/world_painter.png")
const SHELL := preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png")
const VOICE := preload("res://assets/audio/voices/filler_v1/roshan_day1_art_enter.ogg")
const BOARD := Rect2(218, 154, 800, 400)
const COLORS: Array[Color] = TEMPLATE.COLORS
const NONE := -100
const MOUSE := -1

class ToolIcon extends Control:
	var kind := "brush"
	var color := Color.WHITE
	var hold_fraction := -1.0

	func _draw() -> void:
		var ink := Color("514075")
		match kind:
			"guide":
				draw_arc(Vector2(55, 55), 47, 0, TAU, 48, Color("f5c85d"), 6, true)
				draw_circle(Vector2(55, 12), 7, Color("fff6e4"))
				if hold_fraction >= 0.0:
					draw_circle(Vector2(55, 55), 9, Color("f5c85d"))
					draw_arc(Vector2(55, 55), 39, -PI * 0.5,
						-PI * 0.5 + TAU * maxf(0.02, hold_fraction), 40, ink, 5, true)
			"color":
				draw_circle(Vector2(55, 55), 29, color)
				draw_arc(Vector2(55, 55), 29, 0, TAU, 40, ink, 3, true)
			"brush":
				draw_line(Vector2(34, 80), Vector2(71, 29), ink, 15, true)
				draw_line(Vector2(35, 78), Vector2(66, 36), Color("eebc7f"), 9, true)
				draw_circle(Vector2(73, 26), 12, Color("b598dd"))
			"fill":
				draw_colored_polygon(PackedVector2Array([Vector2(28, 42), Vector2(71, 42),
					Vector2(64, 80), Vector2(35, 80)]), Color("b598dd"))
				draw_polyline(PackedVector2Array([Vector2(28, 42), Vector2(71, 42),
					Vector2(64, 80), Vector2(35, 80), Vector2(28, 42)]), ink, 4, true)
				draw_arc(Vector2(50, 40), 18, PI, TAU, 24, ink, 4, true)
				draw_circle(Vector2(83, 77), 9, Color("e97b97"))
			"undo", "redo":
				var direction := 1.0
				if kind == "redo":
					draw_set_transform(Vector2(110, 0), 0.0, Vector2(-1, 1))
				var center := Vector2(55, 55)
				draw_arc(center, 25, -PI * 0.8, PI * 0.6, 32, ink, 7, true)
				draw_line(center + Vector2(-29 * direction, -25),
					center + Vector2(-29 * direction, -2), ink, 7, true)
				draw_line(center + Vector2(-29 * direction, -2),
					center + Vector2(-6 * direction, -7), ink, 7, true)
			"back":
				draw_line(Vector2(79, 55), Vector2(30, 55), ink, 7, true)
				draw_polyline(PackedVector2Array([Vector2(49, 34), Vector2(28, 55),
					Vector2(49, 76)]), ink, 7, true)
			"resume":
				draw_colored_polygon(PackedVector2Array([Vector2(38, 28),
					Vector2(83, 55), Vector2(38, 82)]), ink)

var guided := true
var template: PainterTemplate
var _guided_region := -1
var _hold_seconds := 0.0
var _reference_card: TextureRect
var _progress: Label

var document: PainterDocument = DOCUMENT.new()
var save_path := PainterDocument.DEFAULT_PATH
var load_saved := true
var selected_tool := "brush"
var selected_color := 0
var owner_id := NONE
var suspended := false
var _stage: Control
var _paper: TextureRect
var _texture: ImageTexture
var _buttons: Array[Button] = []
var _pressed: Button
var _press_point := Vector2.ZERO
var _ui_dragged := false
var _painting := false
var _shell_image: Image
var _voice: AudioStreamPlayer
var _actor: TextureRect
var _actor_player: OperaRoshanActor
var _hint: Control
var _paused: Control
var _resume: Button
var _status: Label
var _save_clock := 0.0
var _hint_clock := 0.0
var _has_painted := false


func _ready() -> void:
	name = "PainterPrototype"
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	if "--free-paint" in OS.get_cmdline_user_args():
		guided = false
	if guided:
		template = TEMPLATE.new()
		if save_path == PainterDocument.DEFAULT_PATH:
			save_path = PainterTemplate.SAVE_PATH
		document.image = template.blank.duplicate()
		selected_tool = "fill"
		selected_color = 1
	if load_saved:
		document.load_canvas(save_path)
		if guided and not template.accepts_saved(document.image):
			document.image = template.blank.duplicate()
	_shell_image = SHELL.get_image()
	_stage = UI.add_stage(self, get_viewport_rect().size)
	resized.connect(_layout_stage)
	_build()
	_layout_stage()
	if get_tree().current_scene == self:
		get_tree().auto_accept_quit = false
	_say()


func _build() -> void:
	_picture(BACKDROP, Rect2(0, 0, 1280, 720), _stage)
	# A quiet paper work surface preserves the background and source pixels.
	var paper_frame := Panel.new()
	paper_frame.position = BOARD.position - Vector2(14, 14)
	paper_frame.size = BOARD.size + Vector2(28, 28)
	paper_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	paper_frame.add_theme_stylebox_override("panel", UI.panel_style(UI.PURPLE, UI.PAPER, 24, 5))
	_stage.add_child(paper_frame)
	_texture = ImageTexture.create_from_image(document.image)
	_paper = _picture(_texture, BOARD, _stage)
	_paper.stretch_mode = TextureRect.STRETCH_SCALE
	_actor = _picture(ACTOR.idle_frame("painter"), Rect2(1020, 300, 240, 240), _stage)
	_actor_player = ACTOR.new()
	add_child(_actor_player)
	_actor_player.setup(_actor, "painter", _actor.texture)
	_actor_player.show_pose("idle", 1)
	var title := Label.new()
	title.text = "Roshan's colour picture" if guided else "Roshan's painting studio"
	title.position = Vector2(214, 44)
	title.size = Vector2(650, 66)
	UI.style_label(title, 38, UI.INK, 4, UI.ROLE_TITLE)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(title)
	_button("back", Vector2(32, 24), "Leave; your painting is kept")
	_button("brush", Vector2(56, 182), "Paint")
	_button("fill", Vector2(56, 316), "Fill a connected colour")
	var stamp_button := _button("stamp", Vector2(56, 450), "Place a shell")
	_picture(SHELL, Rect2(17, 17, 76, 76), stamp_button)
	_button("undo", Vector2(1020, 24), "Undo")
	_button("redo", Vector2(1150, 24), "Redo")
	for index: int in COLORS.size():
		var button := _button("color", Vector2(246 + index * 126, 590), "Paint colour")
		button.set_meta("color_index", index)
		var icon := button.get_node("Icon") as ToolIcon
		icon.color = COLORS[index]
	_hint = Control.new()
	_hint.position = BOARD.position + Vector2(340, 160)
	_hint.size = Vector2(110, 110)
	_hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var hint_icon := ToolIcon.new()
	hint_icon.kind = "brush"
	_hint.add_child(hint_icon)
	_stage.add_child(_hint)
	_status = Label.new()
	_status.position = Vector2(1030, 540)
	_status.size = Vector2(230, 70)
	UI.style_label(_status, 22, UI.INK, 3, UI.ROLE_ADULT_CAPTION)
	_status.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_status)
	_paused = Panel.new()
	_paused.position = Vector2(430, 230)
	_paused.size = Vector2(420, 250)
	(_paused as Panel).add_theme_stylebox_override("panel", UI.panel_style())
	_paused.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_paused)
	_resume = _button("resume", Vector2(155, 68), "Keep painting", _paused)
	_paused.hide()
	_voice = AudioStreamPlayer.new()
	_voice.stream = GUIDED_VOICE if guided else VOICE
	add_child(_voice)
	if guided:
		_build_guidance()
	_refresh_buttons()


func _picture(texture: Texture2D, rect: Rect2, parent: Node) -> TextureRect:
	var card := TextureRect.new()
	card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	card.texture = texture
	card.position = rect.position
	card.size = rect.size
	card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(card)
	return card


func _button(action: String, pos: Vector2, hint: String, parent: Node = null) -> Button:
	var button := Button.new()
	button.name = action.capitalize()
	button.position = pos
	button.size = Vector2(110, 110)
	button.custom_minimum_size = button.size
	button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.focus_mode = Control.FOCUS_NONE
	button.tooltip_text = hint
	button.set_meta("action", action)
	UI.style_picture_button(button)
	var icon := ToolIcon.new()
	icon.name = "Icon"
	icon.kind = action
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.add_child(icon)
	(parent if parent != null else _stage).add_child(button)
	_buttons.append(button)
	return button


func _layout_stage() -> void:
	if _stage == null:
		return
	var viewport := get_viewport_rect().size
	var factor := minf(viewport.x / 1280.0, viewport.y / 720.0)
	_stage.scale = Vector2.ONE * factor
	_stage.position = (viewport - Vector2(1280, 720) * factor) * 0.5


func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.canceled:
			if touch.index == owner_id:
				cancel_input()
		elif touch.pressed:
			_press(touch.index, touch.position)
		else:
			_release(touch.index, touch.position)
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_move(drag.index, drag.position)
	elif event is InputEventMouseButton and event.device != InputEvent.DEVICE_ID_EMULATION:
		var mouse := event as InputEventMouseButton
		if mouse.button_index == MOUSE_BUTTON_LEFT:
			if mouse.pressed:
				_press(MOUSE, mouse.position)
			else:
				_release(MOUSE, mouse.position)
	elif event is InputEventMouseMotion and event.device != InputEvent.DEVICE_ID_EMULATION:
		_move(MOUSE, (event as InputEventMouseMotion).position)
	elif event.is_action_pressed("ui_cancel"):
		if suspended:
			_leave()
		else:
			suspend()


func _press(id: int, viewport_point: Vector2) -> void:
	if owner_id != NONE:
		return
	owner_id = id
	var point := _stage.get_global_transform_with_canvas().affine_inverse() * viewport_point
	_press_point = point
	_ui_dragged = false
	for button: Button in _buttons:
		if not button.is_visible_in_tree() or button.disabled:
			continue
		if suspended and button != _resume:
			continue
		if button.get_global_rect().has_point(viewport_point):
			_pressed = button
			button.set_pressed_no_signal(true)
			return
	if suspended or document.fill_busy or not BOARD.has_point(point):
		return
	_painting = true
	var pixel := (point - BOARD.position) * Vector2(PainterDocument.SIZE) / BOARD.size
	if guided:
		var region := template.region_at(pixel)
		if region >= 0 and not template.is_complete(document.image, region):
			if selected_color == PainterTemplate.TARGETS[region]:
				_guided_region = region
				_hold_seconds = 0.0
				# Acknowledge contact immediately; the hold may finish later.
				_hint.position = point - Vector2(55, 55)
				var icon := _hint.get_child(0) as ToolIcon
				icon.hold_fraction = 0.0
				icon.queue_redraw()
				_hint.show()
			else:
				_refresh_guidance(region)
		return
	match selected_tool:
		"brush": document.begin_stroke(pixel, COLORS[selected_color])
		"fill": document.begin_fill(pixel, COLORS[selected_color])
		"stamp": document.stamp(pixel, _shell_image)
	_has_painted = true
	_hint.hide()
	if document.fill_busy:
		(_hint.get_child(0) as ToolIcon).kind = "fill"
		(_hint.get_child(0) as ToolIcon).queue_redraw()
		_hint.position = point - Vector2(55, 55)
		_hint.show()
	_sync_texture()
	_refresh_buttons()


func _move(id: int, viewport_point: Vector2) -> void:
	if id != owner_id:
		return
	var point := _stage.get_global_transform_with_canvas().affine_inverse() * viewport_point
	_ui_dragged = _ui_dragged or point.distance_to(_press_point) > 18.0
	if guided:
		var was_holding := _guided_region >= 0
		if not BOARD.has_point(point):
			_guided_region = -1
		elif _guided_region >= 0:
			var pixel := (point - BOARD.position) * Vector2(PainterDocument.SIZE) / BOARD.size
			if template.region_at(pixel) != _guided_region:
				_guided_region = -1
		if was_holding and _guided_region < 0:
			_refresh_guidance()
		return
	if not _painting or suspended or selected_tool != "brush":
		return
	if not BOARD.has_point(point):
		document.end_stroke()
		return
	var pixel := (point - BOARD.position) * Vector2(PainterDocument.SIZE) / BOARD.size
	if not document.stroke_active:
		document.begin_stroke(pixel, COLORS[selected_color])
	else:
		document.move_stroke(pixel)
	_sync_texture()


func _release(id: int, viewport_point: Vector2) -> void:
	if id != owner_id:
		return
	var chosen := _pressed
	var activate := chosen != null and not _ui_dragged and chosen.get_global_rect().has_point(viewport_point)
	# A normal release completes a fill already intentionally requested; only
	# lifecycle cancellation discards it. Release never starts another action.
	document.end_stroke()
	_clear_touch()
	if activate:
		_activate(chosen)
	_flush()
	_refresh_buttons()


func _activate(button: Button) -> void:
	var action: String = button.get_meta("action")
	match action:
		"back": _leave()
		"resume":
			suspended = false
			_paused.hide()
		"brush", "fill", "stamp": selected_tool = action
		"color": selected_color = int(button.get_meta("color_index"))
		"undo": document.undo()
		"redo": document.redo()
	_sync_texture()
	if guided:
		_refresh_guidance()


func cancel_input() -> void:
	document.cancel_input()
	if _has_painted:
		_hint.hide()
	_clear_touch()
	_flush()
	_refresh_buttons()


func _clear_touch() -> void:
	if _pressed != null:
		_pressed.set_pressed_no_signal(false)
	_pressed = null
	owner_id = NONE
	_painting = false
	_guided_region = -1
	_hold_seconds = 0.0
	if guided and _hint != null:
		var icon := _hint.get_child(0) as ToolIcon
		icon.hold_fraction = -1.0
		icon.queue_redraw()


func suspend() -> void:
	cancel_input()
	suspended = true
	_paused.show()
	_voice.stop()


func _leave() -> void:
	cancel_input()
	if document.changed and document.save_error != OK:
		return
	_voice.stop()
	leave_requested.emit()
	# Standalone review scene closes its window. Embedded callers own navigation.
	if get_tree().current_scene == self:
		get_tree().quit()


func _notification(what: int) -> void:
	if not is_node_ready():
		return
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED:
		suspend()
	elif what == NOTIFICATION_WM_CLOSE_REQUEST:
		_leave()


func _process(delta: float) -> void:
	if guided and not suspended and _guided_region >= 0 and owner_id != NONE:
		_hold_seconds += delta
		var icon := _hint.get_child(0) as ToolIcon
		icon.hold_fraction = minf(1.0, _hold_seconds / 0.22)
		icon.queue_redraw()
		if _hold_seconds >= 0.22:
			document.begin_fill(Vector2(PainterTemplate.SEEDS[_guided_region]), COLORS[selected_color])
			_guided_region = -1
	var was_busy := document.fill_busy
	if document.poll_fill():
		_sync_texture()
		_flush()
		_refresh_buttons()
	if was_busy and not document.fill_busy:
		_hint.hide()
		_refresh_buttons()
		if guided:
			_refresh_guidance()
	_save_clock += delta
	if _save_clock >= 1.0:
		_save_clock = 0.0
		if document.stroke_active:
			document.changed = true
		_flush()
	if guided and _hint.visible and not suspended:
		_hint_clock += delta
		_hint.modulate.a = 0.75 + sin(_hint_clock * 3.0) * 0.25
	if not guided and not _has_painted and not suspended:
		_hint_clock += delta
		_hint.position.x = BOARD.position.x + 340.0 + sin(_hint_clock * 1.8) * 28.0


func _sync_texture() -> void:
	_texture.update(document.image)


func _flush() -> void:
	if not document.changed:
		return
	var error := document.save_canvas(save_path)
	_status.text = "" if error == OK else "Painting kept here.\nSave needs attention."


func _refresh_buttons() -> void:
	for button: Button in _buttons:
		var action: String = button.get_meta("action")
		if guided:
			button.visible = action not in ["brush", "fill", "stamp"] and not (action == "color" and int(button.get_meta("color_index")) == 5)
		button.disabled = (action == "undo" and (document.undo_images.is_empty() or document.fill_busy)) \
			or (action == "redo" and (document.redo_images.is_empty() or document.fill_busy))
		var selected := action == selected_tool
		if action == "color":
			selected = int(button.get_meta("color_index")) == selected_color
		UI.set_selected(button, selected)


func _say() -> void:
	# Existing cues: guided hold-to-fill; free-paint invitation. No new audio.
	_voice.play()


func _exit_tree() -> void:
	if is_instance_valid(_voice):
		_voice.stop()
		_voice.stream = null
	document.shutdown()
	if document.changed:
		document.save_canvas(save_path)


func _build_guidance() -> void:
	var frame := Panel.new()
	frame.position = Vector2(16, 180)
	frame.size = Vector2(182, 140)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	frame.add_theme_stylebox_override("panel", UI.panel_style(UI.GOLD, UI.PAPER, 20, 4))
	_stage.add_child(frame)
	_reference_card = _picture(ImageTexture.create_from_image(template.reference),
		Rect2(9, 22, 164, 82), frame)
	_progress = Label.new()
	_progress.position = Vector2(25, 340)
	_progress.size = Vector2(170, 100)
	UI.style_label(_progress, 34, UI.INK, 3, UI.ROLE_STATUS)
	_progress.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_progress)
	_refresh_guidance()


func _refresh_guidance(region: int = -1) -> void:
	var completed := template.complete_count(document.image)
	_progress.text = "●".repeat(completed) + "○".repeat(5 - completed)
	if completed == 5:
		_hint.hide()
		_actor_player.show_pose("cheer", 3)
		return
	_actor_player.show_pose("idle", 1)
	if region < 0:
		region = template.next_region(document.image)
	var color_index := PainterTemplate.TARGETS[region]
	var hint_icon := _hint.get_child(0) as ToolIcon
	hint_icon.kind = "guide"
	hint_icon.hold_fraction = -1.0
	hint_icon.queue_redraw()
	if selected_color == color_index:
		_hint.position = BOARD.position + Vector2(PainterTemplate.SEEDS[region]) * BOARD.size / Vector2(PainterDocument.SIZE) - Vector2(55, 55)
	else:
		_hint.position = Vector2(246 + color_index * 126, 590)
	_hint.show()
