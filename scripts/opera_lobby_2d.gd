class_name OperaLobby2D
extends CanvasLayer
## Touch-first Pearl Opera show picker.
##
## Native Controls provide three direct floor tabs, four picture-first career
## cards and one finale card per floor. Approved Roshan cutouts carry
## the identity; the opaque procedural framing stays sharp and inexpensive.

const FLOOR_THEMES := [
	{"name": "LAGOON LIGHTS", "fill": Color(0.20, 0.12, 0.34), "curtain": Color(0.78, 0.24, 0.42), "accent": Color(1.0, 0.76, 0.35)},
	{"name": "STARLIGHT BALCONY", "fill": Color(0.10, 0.16, 0.38), "curtain": Color(0.28, 0.38, 0.72), "accent": Color(0.52, 0.90, 1.0)},
	{"name": "GRAND GALLERY", "fill": Color(0.22, 0.10, 0.36), "curtain": Color(0.52, 0.22, 0.62), "accent": Color(1.0, 0.68, 0.90)},
]
const SHOW_INDICES := [[0, 1, 2, 3], [5, 6, 7, 8], [10, 11, 12, 13]]
const BOSS_INDICES := [4, 9, 14]

var m: ReefMain
var acts: Array
var request_act: Callable
var request_locked_hint: Callable
var request_leave: Callable
var stars := 0
var floor_index := 0
var accepting_input := true
var root: Control
var backdrop: ColorRect
var upper_curtain: ColorRect
var lower_stage: Panel
var floor_title: Label
var progress_label: Label
var floor_tabs: Array[Button] = []
var card_buttons: Array[Button] = []
var card_stars: Array[Label] = []
var boss_button: Button
var boss_marks: Array[Label] = []
var guide_button: Button = null
var elapsed := 0.0


func setup(
		main: ReefMain,
		act_list: Array,
		star_mask: int,
		start_floor: int,
		act_callback: Callable,
		locked_callback: Callable,
		leave_callback: Callable
	) -> void:
	m = main
	acts = act_list
	stars = star_mask
	floor_index = clampi(start_floor, 0, 2)
	request_act = act_callback
	request_locked_hint = locked_callback
	request_leave = leave_callback
	layer = 35
	_build()
	refresh(star_mask, floor_index)


func _build() -> void:
	root = Control.new()
	root.name = "OperaLobby2D"
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	backdrop = ColorRect.new()
	backdrop.name = "ProceduralTheatreBackdrop"
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(backdrop)
	upper_curtain = ColorRect.new()
	upper_curtain.name = "UpperCurtain"
	upper_curtain.size = Vector2(1280, 132)
	upper_curtain.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(upper_curtain)
	var rail := ColorRect.new()
	rail.name = "GoldProsceniumRail"
	rail.position = Vector2(0, 126)
	rail.size = Vector2(1280, 14)
	rail.color = StorybookUI.GOLD
	rail.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(rail)
	lower_stage = StorybookUI.add_panel(root, Rect2(22, 142, 1236, 556), StorybookUI.GOLD, Color(0.96, 0.92, 1.0, 1.0), 42)
	lower_stage.name = "ShowPickerStage"
	progress_label = _top_label("OperaStarProgress", Rect2(28, 20, 250, 92), 32)
	root.add_child(progress_label)
	floor_title = _top_label("FloorTitle", Rect2(286, 143, 638, 42), 26)
	root.add_child(floor_title)
	for i in range(3):
		var tab := Button.new()
		tab.name = "FloorTab%d" % (i + 1)
		tab.position = Vector2(397 + i * 164, 10)
		tab.size = Vector2(150, 112)
		tab.tooltip_text = "Opera floor %d" % (i + 1)
		tab.pressed.connect(_choose_floor.bind(i))
		root.add_child(tab)
		floor_tabs.append(tab)
	var home := Button.new()
	home.name = "OperaBackButton"
	StorybookUI.style_back_button(home, "Save stars and leave")
	home.position = Vector2(1144, 14)
	home.pressed.connect(_leave)
	root.add_child(home)
	var xs := [48.0, 350.0, 652.0, 954.0]
	for slot in range(4):
		var card := Button.new()
		card.name = "CareerCard%d" % slot
		card.position = Vector2(xs[slot], 48)
		card.size = Vector2(278, 336)
		card.clip_contents = true
		card.pressed.connect(_choose_show.bind(slot))
		lower_stage.add_child(card)
		card_buttons.append(card)
		var roshan := _actor_rect("RoshanActor", Rect2(24, 8, 230, 240))
		card.add_child(roshan)
		var star := _card_label("CompletionStar", "", Rect2(209, 0, 64, 70), 29, StorybookUI.GOLD)
		card.add_child(star)
		card_stars.append(star)
	boss_button = Button.new()
	boss_button.name = "FloorFinaleCard"
	boss_button.position = Vector2(326, 394)
	boss_button.size = Vector2(584, 134)
	boss_button.pressed.connect(_choose_boss)
	lower_stage.add_child(boss_button)
	for i in range(4):
		var mark := _card_label("ShowMark%d" % i, "", Rect2(92 + i * 74, 64, 62, 52), 22, StorybookUI.GOLD)
		boss_button.add_child(mark)
		boss_marks.append(mark)


func _top_label(node_name: String, rect: Rect2, font_size: int) -> Label:
	var label := Label.new()
	label.name = node_name
	label.position = rect.position
	label.size = rect.size
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_hud_label(label, font_size, Color.WHITE, 5)
	return label


func _actor_rect(node_name: String, rect: Rect2) -> TextureRect:
	var actor := TextureRect.new()
	actor.name = node_name
	actor.position = rect.position
	actor.size = rect.size
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return actor


func _card_label(node_name: String, text: String, rect: Rect2, font_size: int, colour: Color) -> Label:
	var label := Label.new()
	label.name = node_name
	label.text = text
	label.position = rect.position
	label.size = rect.size
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_hud_label(label, font_size, colour, 4)
	return label


func refresh(star_mask: int, preferred_floor: int = -1) -> void:
	stars = star_mask
	if preferred_floor >= 0:
		floor_index = clampi(preferred_floor, 0, 2)
	if not _floor_unlocked(floor_index):
		floor_index = _highest_unlocked_floor()
	_apply_floor_theme()
	progress_label.text = "STAR %d / 15" % _star_count()
	for i in range(3):
		var unlocked := _floor_unlocked(i)
		var complete := (stars & (1 << BOSS_INDICES[i])) != 0
		var tab := floor_tabs[i]
		tab.text = ("%d  STAR" % (i + 1)) if complete else ("%d" % (i + 1) if unlocked else "%d  LOCK" % (i + 1))
		StorybookUI.style_button(tab, "gold" if i == floor_index else ("secondary" if unlocked else "locked"), 24, 24)
		tab.set_meta("locked", not unlocked)
	var show_indices: Array = SHOW_INDICES[floor_index]
	for slot in range(4):
		var act_index: int = int(show_indices[slot])
		var cfg: Dictionary = acts[act_index]
		var career := String(cfg.get("career", "SHOW"))
		var costume := String(cfg.get("costume", ""))
		var card := card_buttons[slot]
		card.text = "\n\n\n\n\n\n\n\n" + career.to_upper()
		card.tooltip_text = "Play %s" % String(cfg.get("name", career))
		StorybookUI.style_button(card, "gold" if (stars & (1 << act_index)) != 0 else "secondary", 21, 32)
		card.set_meta("act_index", act_index)
		card.set_meta("picture_first", true)
		var roshan := card.get_node("RoshanActor") as TextureRect
		roshan.texture = _actor_texture("roshan", costume)
		card_stars[slot].text = "STAR" if (stars & (1 << act_index)) != 0 else ""
	var boss_index: int = BOSS_INDICES[floor_index]
	var boss_cfg: Dictionary = acts[boss_index]
	var boss_ready := _floor_shows_starred(floor_index)
	var boss_done := (stars & (1 << boss_index)) != 0
	boss_button.text = "FLOOR FINALE\n%s" % String(boss_cfg.get("career", "BIG SHOW")).to_upper()
	boss_button.tooltip_text = "Play %s" % String(boss_cfg.get("name", "floor finale"))
	StorybookUI.style_button(boss_button, "gold" if boss_ready else "locked", 27, 38)
	boss_button.set_meta("locked", not boss_ready)
	boss_button.set_meta("act_index", boss_index)
	for slot in range(4):
		var show_index: int = int(show_indices[slot])
		boss_marks[slot].text = "STAR" if (stars & (1 << show_index)) != 0 else "o"
	boss_button.text += "\nSTAR" if boss_done else ("\nGO!" if boss_ready else "\nWIN THE FOUR SHOWS")
	_update_guide()


func show_lobby(preferred_floor: int, star_mask: int) -> void:
	accepting_input = true
	root.visible = true
	refresh(star_mask, preferred_floor)


func hide_lobby() -> void:
	accepting_input = false
	root.visible = false


func close() -> void:
	accepting_input = false
	queue_free()


func _actor_texture(side: String, costume: String) -> Texture2D:
	var path := "res://assets/opera/worlds/actors/%s_%s.png" % [side, costume]
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	return null


func _apply_floor_theme() -> void:
	var theme: Dictionary = FLOOR_THEMES[floor_index]
	backdrop.color = Color(theme["fill"])
	upper_curtain.color = Color(theme["curtain"])
	floor_title.text = "%d  %s" % [floor_index + 1, String(theme["name"])]
	lower_stage.add_theme_stylebox_override("panel", StorybookUI.panel_style(Color(theme["accent"]), Color(0.96, 0.92, 1.0, 1.0), 42, 6))


func _choose_floor(which: int) -> void:
	if not accepting_input:
		return
	if not _floor_unlocked(which):
		if request_locked_hint.is_valid():
			request_locked_hint.call(which + 1)
		return
	floor_index = which
	refresh(stars, which)
	if m != null:
		m.show_msg("Roshan", "Floor %d! Pick any picture for our next show!" % (which + 1), "hint")


func _choose_show(slot: int) -> void:
	if accepting_input:
		_start_requested_act(int(SHOW_INDICES[floor_index][slot]))


func _choose_boss() -> void:
	if not accepting_input:
		return
	if not _floor_shows_starred(floor_index):
		if request_locked_hint.is_valid():
			request_locked_hint.call(floor_index + 1)
		return
	_start_requested_act(BOSS_INDICES[floor_index])


func _start_requested_act(act_index: int) -> void:
	accepting_input = false
	if request_act.is_valid():
		request_act.call(act_index)


func _leave() -> void:
	if accepting_input and request_leave.is_valid():
		accepting_input = false
		request_leave.call()


func _floor_unlocked(which: int) -> bool:
	return which <= 0 or (stars & (1 << BOSS_INDICES[which - 1])) != 0


func _floor_shows_starred(which: int) -> bool:
	for act_index in SHOW_INDICES[which]:
		if (stars & (1 << int(act_index))) == 0:
			return false
	return true


func _highest_unlocked_floor() -> int:
	for i in range(2, -1, -1):
		if _floor_unlocked(i):
			return i
	return 0


func _star_count() -> int:
	var total := 0
	for i in range(15):
		if (stars & (1 << i)) != 0:
			total += 1
	return total


func _update_guide() -> void:
	guide_button = null
	var show_indices: Array = SHOW_INDICES[floor_index]
	for slot in range(4):
		if (stars & (1 << int(show_indices[slot]))) == 0:
			guide_button = card_buttons[slot]
			return
	var boss_index: int = BOSS_INDICES[floor_index]
	if (stars & (1 << boss_index)) == 0:
		guide_button = boss_button


func _process(delta: float) -> void:
	if not accepting_input or guide_button == null or not is_instance_valid(guide_button):
		return
	elapsed += delta
	var pulse := 0.88 + sin(elapsed * 3.0) * 0.12
	guide_button.modulate = Color(1.0, 1.0, pulse, 1.0)
