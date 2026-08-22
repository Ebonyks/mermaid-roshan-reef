class_name MasterMode
extends CanvasLayer
## One-screen debug launcher opened by the enchanted painting in Pearl Castle.
## It deliberately reuses each activity's shipping entry/exit path; the only
## extra state is the Castle room to rebuild after a directly launched Canvas
## game finishes or is left early.

const CANVAS_GAMES: Array[Dictionary] = [
	{"id": "harper_slide", "icon": "🌈", "label": "Harper + Fiona\nRainbow Slide",
		"config": {"fname": "Harper and Fiona", "game": "slide",
			"theme": "rainbow", "mode": "fish", "won": true, "cool": 0.0}},
	{"id": "melody", "icon": "🎵", "label": "Daddy Mermaid\nRainbow Melody",
		"config": {"fname": "Daddy Mermaid", "game": "melody",
			"won": true, "cool": 0.0}},
	{"id": "dolls", "icon": "🧸", "label": "Faron\nSleepy Dolls",
		"config": {"fname": "Faron", "game": "dolls",
			"won": true, "cool": 0.0}},
	{"id": "seek", "icon": "🔎", "label": "Evie + Lamb-a'\nHide and Seek",
		"config": {"fname": "Evie and Lamb-a'", "game": "seek",
			"won": true, "cool": 0.0}},
]
const PICTURE_GAMES: Array[Dictionary] = [
	{"id": "snowman", "icon": "⛄", "label": "Snowman", "kind": "snowman"},
	{"id": "garden", "icon": "🌻", "label": "Flower Garden", "kind": "garden"},
	{"id": "trampoline", "icon": "⭐", "label": "Trampoline", "kind": "trampoline"},
	{"id": "xmas", "icon": "🎄", "label": "Christmas", "kind": "xmas"},
]
const FEATURE_SHORTCUTS: Array[Dictionary] = [
	{"id": "castle_logo", "icon": "♛", "label": "Castle Logo"},
	{"id": "craft", "icon": "🎨", "label": "Color a Friend"},
	{"id": "wardrobe", "icon": "👗", "label": "Wardrobe"},
	{"id": "stickers", "icon": "⭐", "label": "Sticker Book"},
	{"id": "collection", "icon": "🐠", "label": "Critter Book"},
]

var m: ReefMain
var root: Control = null
var stage: Control = null
var open_state := false
var pending_standard_activity := false
var return_room := "main_hall"


func _init(main: ReefMain) -> void:
	m = main
	layer = 16
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false


func is_open() -> bool:
	return open_state and root != null and is_instance_valid(root) and visible


func open() -> void:
	if is_open() or pending_standard_activity:
		return
	var castle_visible: bool = m.castle_room_layer != null \
		and is_instance_valid(m.castle_room_layer) \
		and m.castle_room_layer.visible
	if m.game != "level2" or String(m.g.get("phase", "")) != "hall" \
			or not castle_visible:
		return
	if root == null or not is_instance_valid(root):
		_build_ui()
	open_state = true
	visible = true
	m._set_world_controls_enabled(false, "master_mode")
	var book: Panel = stage.get_node_or_null("MasterModeBook") as Panel
	if book != null:
		book.pivot_offset = book.size * 0.5
		book.scale = Vector2(0.90, 0.90)
		var pop: Tween = create_tween()
		pop.tween_property(book, "scale", Vector2.ONE, 0.18).set_trans(
			Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func close() -> void:
	if not open_state:
		return
	open_state = false
	visible = false
	m._set_world_controls_enabled(true, "master_mode")


func _build_ui() -> void:
	root = Control.new()
	root.name = "MasterModeRoot"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(root)

	var dim := ColorRect.new()
	dim.color = Color(0.035, 0.025, 0.12, 0.92)
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	root.add_child(dim)
	stage = StorybookUI.add_stage(root, m.get_viewport().get_visible_rect().size)

	var book: Panel = StorybookUI.add_panel(stage,
		Rect2(24.0, 18.0, 1232.0, 684.0), StorybookUI.PURPLE_DEEP,
		Color(0.94, 0.97, 1.0, 0.995), 48)
	book.name = "MasterModeBook"
	book.mouse_filter = Control.MOUSE_FILTER_STOP
	StorybookUI.add_shell_crest(book,
		Rect2(576.0, 10.0, 80.0, 56.0), "MasterModeShellCrest")

	var title := Label.new()
	title.name = "MasterModeTitle"
	title.text = "MASTER MODE  •  ALL 2D GAMES"
	title.position = Vector2(52.0, 28.0)
	title.size = Vector2(1000.0, 64.0)
	StorybookUI.style_label(title, 42, StorybookUI.INK, 5)
	book.add_child(title)

	var back := Button.new()
	back.name = "MasterModeBackButton"
	back.position = Vector2(1092.0, 20.0)
	StorybookUI.style_back_button(back, "Back to the Main Hall")
	back.pressed.connect(close)
	book.add_child(back)

	var scroll := ScrollContainer.new()
	scroll.name = "MasterModeGameScroll"
	scroll.position = Vector2(40.0, 104.0)
	scroll.size = Vector2(1152.0, 548.0)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	book.add_child(scroll)

	var sections := VBoxContainer.new()
	sections.name = "MasterModeSections"
	sections.custom_minimum_size = Vector2(1110.0, 0.0)
	sections.add_theme_constant_override("separation", 18)
	scroll.add_child(sections)

	_add_section(sections, "NEW CANVAS GAMES", CANVAS_GAMES, "canvas")
	_add_section(sections, "PICTURE GAMES", PICTURE_GAMES, "picture")
	_add_section(sections, "OPERA CAREER WORLDS", _opera_items(), "opera")
	_add_section(sections, "MAJOR TOOLS", FEATURE_SHORTCUTS, "feature")


func _opera_items() -> Array[Dictionary]:
	var items: Array[Dictionary] = []
	for act_index: int in OperaHouse.LIVE_ACT_INDICES:
		var config: Dictionary = OperaHouse.ACTS[act_index] as Dictionary
		items.append({
			"id": "opera_%02d" % act_index,
			"icon": String(config.get("emoji", "★")),
			"label": String(config.get("career", "Opera Career")),
			"act_index": act_index,
		})
	return items


func _add_section(parent: VBoxContainer, heading: String,
		items: Array[Dictionary], launch_kind: String) -> void:
	var label := Label.new()
	label.text = heading
	label.custom_minimum_size = Vector2(1080.0, 44.0)
	StorybookUI.style_label(label, 28, StorybookUI.PURPLE, 3)
	parent.add_child(label)

	var grid := GridContainer.new()
	grid.name = "MasterModeGrid_" + launch_kind
	grid.columns = 5
	grid.add_theme_constant_override("h_separation", 14)
	grid.add_theme_constant_override("v_separation", 14)
	parent.add_child(grid)
	for item: Dictionary in items:
		var button := Button.new()
		var item_id := String(item["id"])
		button.name = "MasterModeGame_" + item_id
		button.text = "%s\n%s" % [
			String(item.get("icon", "★")), String(item["label"])]
		button.custom_minimum_size = Vector2(210.0, 112.0)
		button.size = button.custom_minimum_size
		button.focus_mode = Control.FOCUS_ALL
		button.set_meta("master_mode_kind", launch_kind)
		button.set_meta("master_mode_id", item_id)
		StorybookUI.style_button(button, "secondary", 22, 28)
		button.pressed.connect(_launch.bind(launch_kind, item))
		grid.add_child(button)


func _launch(launch_kind: String, item: Dictionary) -> void:
	m._ui_tap()
	match launch_kind:
		"picture":
			close()
			m._mg2d_open(String(item["kind"]))
		"opera":
			var act_index := int(item["act_index"])
			var room_id := CastleCareerRoutes.room_for_act(act_index)
			if room_id == "":
				return
			close()
			m._castle_rooms_ref().show_room(room_id, false)
			m.call_deferred("_start_opera_from_room", act_index, room_id)
		"canvas":
			_launch_standard_activity(
				(item["config"] as Dictionary).duplicate(true))
		"feature":
			close()
			match String(item["id"]):
				"castle_logo":
					m._open_castle_logo()
				"craft":
					m._open_craft_studio()
				"wardrobe":
					m._open_wardrobe()
				"stickers":
					m._open_stickers()
				"collection":
					m._collection_ref().open_book()


func _launch_standard_activity(config: Dictionary) -> void:
	if pending_standard_activity or config.is_empty():
		return
	return_room = m.castle_room_id
	pending_standard_activity = true
	close()
	m._castle_rooms_ref().suspend()
	m._start_game(config)


func restore_after_standard_activity() -> bool:
	if not pending_standard_activity:
		return false
	pending_standard_activity = false
	# Standard minigame cleanup frees the prior level's game_nodes. Rebuild the
	# full Lagoon context, then immediately enter the Castle under the already
	# opaque transition cover. Merely showing the old Castle layer would leave
	# its courtyard and return routes deleted. Close that suspended layer first:
	# its transient affordance and room keys belonged to the cleared game state.
	m._castle_rooms_ref().close()
	m._enter_level2_now(true, false, false)
	m._enter_castle_interior_now(true)
	if return_room != "main_hall":
		m._castle_rooms_ref().show_room(return_room, false)
	return_room = "main_hall"
	return true
