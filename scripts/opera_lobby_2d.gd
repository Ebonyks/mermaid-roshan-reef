class_name OperaLobby2D
extends CanvasLayer
## Touch-first Pearl Opera show picker.
##
## Native Controls provide three direct floor tabs, four or five picture-first
## career cards and one finale card per floor. Nursery Nurse is job #12 on the
## five-card Grand Gallery while old act-bit indices remain save-compatible.
## Approved Roshan cutouts carry the identity; the opaque procedural framing
## stays sharp and inexpensive.

const FLOOR_THEMES := [
	{"name": "LAGOON LIGHTS", "fill": Color(0.20, 0.12, 0.34), "curtain": Color(0.78, 0.24, 0.42), "accent": Color(1.0, 0.76, 0.35)},
	{"name": "STARLIGHT BALCONY", "fill": Color(0.10, 0.16, 0.38), "curtain": Color(0.28, 0.38, 0.72), "accent": Color(0.52, 0.90, 1.0)},
	{"name": "GRAND GALLERY", "fill": Color(0.22, 0.10, 0.36), "curtain": Color(0.52, 0.22, 0.62), "accent": Color(1.0, 0.68, 0.90)},
]
const SHOW_INDICES := [[0, 1, 2, 3], [5, 6, 7, 8], [10, 11, 12, 15, 13]]
const BOSS_INDICES := [4, 9, 14]
const MAX_CARDS := 5
const CREST_ROOT := "res://assets/opera/worlds/ui/crests/"
const CAREER_CREST_FILES := {
	"chef": "opera_crest_chef.png",
	"detective": "opera_crest_detective.png",
	"ballerina": "opera_crest_ballerina.png",
	"candymaker": "opera_crest_candy.png",
	"doctor": "opera_crest_doctor.png",
	"farmer": "opera_crest_farmer.png",
	"boxer": "opera_crest_boxer.png",
	"magician": "opera_crest_magician.png",
	"painter": "opera_crest_painter.png",
	"astronaut": "opera_crest_engineer.png",
	"racer": "opera_crest_racer.png",
	"popstar": "opera_crest_singer.png",
	"nursery": "goal_nursery.png",
}
const FLOOR_CREST_FILES := [
	"opera_crest_dragon.png",
	"opera_crest_phantom.png",
	"opera_crest_maestro.png",
]
const BOSS_CREST_FILES := FLOOR_CREST_FILES
const HOME_CREST_FILE := "opera_crest_house.png"

var m: ReefMain
var acts: Array
var request_act: Callable
var request_locked_hint: Callable
var request_leave: Callable
var stars := 0
var floor_index := 0
var accepting_input := true
var root: Control
var stage: Control
var backdrop: ColorRect
var upper_curtain: ColorRect
var lower_stage: Panel
var floor_title: Label
var progress_label: Label
var progress_pearl_root: Control
var progress_pearls: Array[Panel] = []
var floor_tabs: Array[Button] = []
var floor_crests: Array[TextureRect] = []
var floor_pearls: Array[Panel] = []
var card_buttons: Array[Button] = []
var card_crests: Array[TextureRect] = []
var card_stars: Array[Panel] = []
var boss_button: Button
var boss_crest: TextureRect
var boss_completion_pearl: Panel
var boss_marks: Array[Panel] = []
var home_button: Button
var active_actor_animator: OperaRoshanActor = null
var highlighted_slot := -1
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
	root.clip_contents = false
	add_child(root)
	var viewport_size := root.size
	if viewport_size.x <= 0.0 or viewport_size.y <= 0.0:
		viewport_size = get_viewport().get_visible_rect().size
	if viewport_size.x <= 0.0 or viewport_size.y <= 0.0:
		viewport_size = StorybookUI.CANVAS_SIZE
	stage = StorybookUI.add_stage(root, viewport_size)
	stage.clip_contents = false
	root.resized.connect(_layout_stage)
	backdrop = ColorRect.new()
	backdrop.name = "ProceduralTheatreBackdrop"
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(backdrop)
	upper_curtain = ColorRect.new()
	upper_curtain.name = "UpperCurtain"
	upper_curtain.size = Vector2(1280, 132)
	upper_curtain.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(upper_curtain)
	var rail := ColorRect.new()
	rail.name = "GoldProsceniumRail"
	rail.position = Vector2(0, 126)
	rail.size = Vector2(1280, 14)
	rail.color = StorybookUI.GOLD
	rail.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(rail)
	lower_stage = StorybookUI.add_panel(stage, Rect2(22, 142, 1236, 556), StorybookUI.GOLD, Color(0.96, 0.92, 1.0, 1.0), 42)
	lower_stage.name = "ShowPickerStage"
	lower_stage.clip_contents = false
	progress_label = _top_label("OperaStarProgress", Rect2(28, 20, 250, 92), 32)
	progress_label.text = ""
	progress_label.visible = false
	stage.add_child(progress_label)
	progress_pearl_root = Control.new()
	progress_pearl_root.name = "OperaPearlProgress"
	progress_pearl_root.position = Vector2(30, 25)
	progress_pearl_root.size = Vector2(246, 82)
	progress_pearl_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(progress_pearl_root)
	for i in range(acts.size()):
		var progress_pearl := _pearl_panel("ProgressPearl%d" % i, Rect2())
		var progress_col: int = i % 8
		var progress_row: int = i / 8
		progress_pearl.position = Vector2(2 + progress_col * 29, 4 + progress_row * 38)
		progress_pearl.size = Vector2(24, 24)
		progress_pearl_root.add_child(progress_pearl)
		progress_pearls.append(progress_pearl)
	floor_title = _top_label("FloorTitle", Rect2(286, 143, 638, 42), 26)
	stage.add_child(floor_title)
	for i in range(3):
		var tab := Button.new()
		tab.name = "FloorTab%d" % (i + 1)
		tab.position = Vector2(397 + i * 164, 10)
		tab.size = Vector2(150, 112)
		tab.custom_minimum_size = StorybookUI.MIN_TOUCH
		tab.clip_contents = false
		tab.focus_mode = Control.FOCUS_ALL
		tab.tooltip_text = "Opera floor %d" % (i + 1)
		tab.pressed.connect(_choose_floor.bind(i))
		stage.add_child(tab)
		floor_tabs.append(tab)
		var floor_crest := _texture_rect("FloorCrest", Rect2(31, 8, 88, 88))
		floor_crest.texture = _crest_texture(String(FLOOR_CREST_FILES[i]))
		tab.add_child(floor_crest)
		floor_crests.append(floor_crest)
		var floor_pearl := _pearl_panel("FloorPearl", Rect2(112, 78, 28, 28))
		tab.add_child(floor_pearl)
		floor_pearls.append(floor_pearl)
	home_button = Button.new()
	home_button.name = "OperaBackButton"
	StorybookUI.style_back_button(home_button, "Save stars and leave")
	home_button.text = ""
	home_button.clip_contents = false
	home_button.position = Vector2(1144, 14)
	home_button.pressed.connect(_leave)
	stage.add_child(home_button)
	var home_crest := _texture_rect("HomeCrest", Rect2(17, 17, 78, 78))
	home_crest.texture = _crest_texture(HOME_CREST_FILE)
	home_button.add_child(home_crest)
	for slot in range(MAX_CARDS):
		var card := Button.new()
		card.name = "CareerCard%d" % slot
		card.position = Vector2.ZERO
		card.size = Vector2(216, 330)
		card.custom_minimum_size = StorybookUI.MIN_TOUCH
		card.clip_contents = false
		card.focus_mode = Control.FOCUS_ALL
		card.pressed.connect(_choose_show.bind(slot))
		card.focus_entered.connect(_set_highlighted_card.bind(slot, false))
		card.mouse_entered.connect(_set_highlighted_card.bind(slot, false))
		lower_stage.add_child(card)
		card_buttons.append(card)
		var roshan := _actor_rect("RoshanActor", Rect2(8, 8, 200, 230))
		card.add_child(roshan)
		var crest := _texture_rect("CareerCrest", Rect2(68, 246, 80, 80))
		card.add_child(crest)
		card_crests.append(crest)
		var star := _pearl_panel("CompletionStar", Rect2(174, 286, 34, 34))
		card.add_child(star)
		card_stars.append(star)
	boss_button = Button.new()
	boss_button.name = "FloorFinaleCard"
	boss_button.position = Vector2(318, 392)
	boss_button.size = Vector2(600, 140)
	boss_button.custom_minimum_size = StorybookUI.MIN_TOUCH
	boss_button.clip_contents = false
	boss_button.focus_mode = Control.FOCUS_ALL
	boss_button.pressed.connect(_choose_boss)
	boss_button.focus_entered.connect(_set_highlighted_card.bind(-1, false))
	boss_button.mouse_entered.connect(_set_highlighted_card.bind(-1, false))
	lower_stage.add_child(boss_button)
	boss_crest = _texture_rect("BossCrest", Rect2(20, 12, 116, 116))
	boss_button.add_child(boss_crest)
	boss_completion_pearl = _pearl_panel("BossCompletionPearl", Rect2(548, 12, 38, 38))
	boss_button.add_child(boss_completion_pearl)
	for i in range(MAX_CARDS):
		var mark := _pearl_panel("ShowMark%d" % i, Rect2())
		boss_button.add_child(mark)
		boss_marks.append(mark)
	active_actor_animator = OperaRoshanActor.new()
	active_actor_animator.name = "ActiveRoshanAnimator"
	stage.add_child(active_actor_animator)
	_layout_stage()


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


func _texture_rect(node_name: String, rect: Rect2) -> TextureRect:
	var picture := TextureRect.new()
	picture.name = node_name
	picture.position = rect.position
	picture.size = rect.size
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return picture


func _pearl_panel(node_name: String, rect: Rect2) -> Panel:
	var pearl := Panel.new()
	pearl.name = node_name
	pearl.position = rect.position
	pearl.size = rect.size
	pearl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	pearl.set_meta("complete", false)
	return pearl


func _style_pearl(pearl: Panel, complete: bool) -> void:
	var pearl_style := StyleBoxFlat.new()
	pearl_style.bg_color = StorybookUI.PEARL_BLUE if complete else Color(0.28, 0.26, 0.50, 0.82)
	pearl_style.border_color = StorybookUI.GOLD if complete else Color(0.62, 0.59, 0.78, 0.92)
	pearl_style.set_border_width_all(3)
	var radius: int = maxi(4, int(minf(pearl.size.x, pearl.size.y) * 0.5))
	pearl_style.set_corner_radius_all(radius)
	pearl_style.shadow_color = Color(0.50, 0.96, 1.0, 0.72) if complete else Color(0.08, 0.05, 0.20, 0.30)
	pearl_style.shadow_size = 8 if complete else 2
	pearl_style.shadow_offset = Vector2.ZERO
	pearl.add_theme_stylebox_override("panel", pearl_style)
	pearl.set_meta("complete", complete)


func _crest_texture(file_name: String) -> Texture2D:
	var path := CREST_ROOT + file_name
	if ResourceLoader.exists(path):
		return ResourceLoader.load(path) as Texture2D
	return null


func _layout_stage() -> void:
	if root == null or stage == null:
		return
	var viewport_size := root.size
	if viewport_size.x <= 0.0 or viewport_size.y <= 0.0:
		viewport_size = get_viewport().get_visible_rect().size
	if viewport_size.x <= 0.0 or viewport_size.y <= 0.0:
		viewport_size = StorybookUI.CANVAS_SIZE
	var scale_value: float = minf(
		viewport_size.x / StorybookUI.CANVAS_SIZE.x,
		viewport_size.y / StorybookUI.CANVAS_SIZE.y)
	stage.size = StorybookUI.CANVAS_SIZE
	stage.scale = Vector2.ONE * scale_value
	stage.position = (viewport_size - StorybookUI.CANVAS_SIZE * scale_value) * 0.5
	stage.set_meta("uniform_scale", scale_value)


func _layout_cards(show_count: int) -> void:
	var count := clampi(show_count, 1, MAX_CARDS)
	var card_width := 270.0 if count <= 4 else 216.0
	var gap := 20.0
	var total_width: float = float(count) * card_width + float(count - 1) * gap
	var left: float = (lower_stage.size.x - total_width) * 0.5
	for slot in range(card_buttons.size()):
		var card: Button = card_buttons[slot]
		var visible_slot: bool = slot < count
		card.visible = visible_slot
		card.disabled = not visible_slot
		if not visible_slot:
			card.set_meta("animator_active", false)
			continue
		card.position = Vector2(left + float(slot) * (card_width + gap), 45)
		card.size = Vector2(card_width, 330)
		var roshan := card.get_node("RoshanActor") as TextureRect
		roshan.position = Vector2(8, 8)
		roshan.size = Vector2(card_width - 16.0, 230)
		var crest: TextureRect = card_crests[slot]
		crest.position = Vector2((card_width - 80.0) * 0.5, 246)
		crest.size = Vector2(80, 80)
		var star: Panel = card_stars[slot]
		star.position = Vector2(card_width - 42.0, 288)
		star.size = Vector2(32, 32)
	var mark_width := 42.0
	var mark_gap := 18.0
	var marks_total: float = float(count) * mark_width + float(count - 1) * mark_gap
	var mark_start: float = 156.0 + (boss_button.size.x - 166.0 - marks_total) * 0.5
	for slot in range(boss_marks.size()):
		var mark: Panel = boss_marks[slot]
		mark.visible = slot < count
		mark.position = Vector2(mark_start + float(slot) * (mark_width + mark_gap), 72)
		mark.size = Vector2(mark_width, mark_width)


func refresh(star_mask: int, preferred_floor: int = -1) -> void:
	stars = star_mask
	if preferred_floor >= 0:
		floor_index = clampi(preferred_floor, 0, 2)
	if not _floor_unlocked(floor_index):
		floor_index = _highest_unlocked_floor()
	_set_highlighted_card(-1, true)
	_apply_floor_theme()
	progress_label.text = ""
	for i in range(progress_pearls.size()):
		_style_pearl(progress_pearls[i], (stars & (1 << i)) != 0)
	for i in range(3):
		var unlocked: bool = _floor_unlocked(i)
		var complete: bool = (stars & (1 << int(BOSS_INDICES[i]))) != 0
		var tab: Button = floor_tabs[i]
		tab.text = ""
		tab.tooltip_text = "Opera floor %d%s" % [i + 1, " complete" if complete else ("" if unlocked else " locked")]
		StorybookUI.style_button(tab, "gold" if i == floor_index else ("secondary" if unlocked else "locked"), 24, 24)
		tab.set_meta("locked", not unlocked)
		floor_crests[i].modulate = Color.WHITE if unlocked else Color(0.56, 0.58, 0.70, 0.72)
		_style_pearl(floor_pearls[i], complete)
	var show_indices: Array = SHOW_INDICES[floor_index]
	_layout_cards(show_indices.size())
	for slot in range(show_indices.size()):
		var act_index: int = int(show_indices[slot])
		var cfg: Dictionary = acts[act_index]
		var career: String = String(cfg.get("career", "SHOW"))
		var costume: String = String(cfg.get("costume", ""))
		var card: Button = card_buttons[slot]
		var complete: bool = (stars & (1 << act_index)) != 0
		card.text = ""
		card.tooltip_text = "Play %s" % String(cfg.get("name", career))
		StorybookUI.style_picture_button(card, Color(0.91, 0.93, 1.0, 0.98), StorybookUI.GOLD if complete else StorybookUI.PURPLE, 32)
		card.set_meta("act_index", act_index)
		card.set_meta("picture_first", true)
		card.set_meta("costume", costume)
		card.set_meta("animator_active", false)
		var roshan := card.get_node("RoshanActor") as TextureRect
		var static_fallback: Texture2D = _actor_texture("roshan", costume)
		roshan.texture = OperaRoshanActor.idle_frame(costume, static_fallback)
		card_crests[slot].texture = _crest_texture(String(CAREER_CREST_FILES.get(costume, "")))
		card_crests[slot].set_meta("crest_key", costume)
		_style_pearl(card_stars[slot], complete)
	var boss_index: int = BOSS_INDICES[floor_index]
	var boss_cfg: Dictionary = acts[boss_index]
	var boss_ready: bool = _floor_shows_starred(floor_index)
	var boss_done: bool = (stars & (1 << boss_index)) != 0
	boss_button.text = ""
	boss_button.tooltip_text = "Play %s" % String(boss_cfg.get("name", "floor finale"))
	StorybookUI.style_picture_button(boss_button, Color(0.93, 0.91, 1.0, 0.98) if boss_ready else Color(0.72, 0.73, 0.82, 0.96), StorybookUI.GOLD if boss_ready else StorybookUI.MUTED, 38)
	boss_button.set_meta("locked", not boss_ready)
	boss_button.set_meta("act_index", boss_index)
	boss_crest.texture = _crest_texture(String(BOSS_CREST_FILES[floor_index]))
	boss_crest.set_meta("crest_key", String(BOSS_CREST_FILES[floor_index]))
	boss_crest.modulate = Color.WHITE if boss_ready else Color(0.62, 0.62, 0.72, 0.76)
	_style_pearl(boss_completion_pearl, boss_done)
	for slot in range(show_indices.size()):
		var show_index: int = int(show_indices[slot])
		_style_pearl(boss_marks[slot], (stars & (1 << show_index)) != 0)
	_update_guide()
	var guide_slot: int = card_buttons.find(guide_button)
	_set_highlighted_card(guide_slot, true)


func show_lobby(preferred_floor: int, star_mask: int) -> void:
	accepting_input = true
	root.visible = true
	refresh(star_mask, preferred_floor)


func hide_lobby() -> void:
	accepting_input = false
	_set_highlighted_card(-1, true)
	root.visible = false


func close() -> void:
	accepting_input = false
	_set_highlighted_card(-1, true)
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
	floor_title.text = String(theme["name"])
	lower_stage.add_theme_stylebox_override("panel", StorybookUI.panel_style(Color(theme["accent"]), Color(0.96, 0.92, 1.0, 1.0), 42, 6))


func _set_highlighted_card(slot: int, force: bool = false) -> void:
	if not force and slot == highlighted_slot:
		return
	if active_actor_animator != null and is_instance_valid(active_actor_animator):
		active_actor_animator.stop()
		active_actor_animator.setup(null, "", null)
	for card in card_buttons:
		card.set_meta("animator_active", false)
	highlighted_slot = -1
	if slot < 0 or slot >= card_buttons.size():
		return
	var card: Button = card_buttons[slot]
	if not card.visible or card.disabled:
		return
	var costume: String = String(card.get_meta("costume", ""))
	var roshan := card.get_node_or_null("RoshanActor") as TextureRect
	if roshan == null:
		return
	var fallback: Texture2D = roshan.texture
	highlighted_slot = slot
	card.set_meta("animator_active", true)
	active_actor_animator.setup(roshan, costume, fallback)


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
	if not accepting_input:
		return
	var show_indices: Array = SHOW_INDICES[floor_index]
	if slot < 0 or slot >= show_indices.size():
		return
	_start_requested_act(int(show_indices[slot]))


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
	for i in range(acts.size()):
		if (stars & (1 << i)) != 0:
			total += 1
	return total


func _update_guide() -> void:
	for card in card_buttons:
		card.modulate = Color.WHITE
	boss_button.modulate = Color.WHITE
	for tab in floor_tabs:
		tab.modulate = Color.WHITE
	guide_button = null
	elapsed = 0.0
	var show_indices: Array = SHOW_INDICES[floor_index]
	for slot in range(show_indices.size()):
		if (stars & (1 << int(show_indices[slot]))) == 0:
			guide_button = card_buttons[slot]
			break
	var boss_index: int = BOSS_INDICES[floor_index]
	if guide_button == null and (stars & (1 << boss_index)) == 0:
		guide_button = boss_button


func _process(delta: float) -> void:
	if not accepting_input or guide_button == null or not is_instance_valid(guide_button):
		return
	elapsed += delta
	var pulse := 0.88 + sin(elapsed * 3.0) * 0.12
	guide_button.modulate = Color(1.0, 1.0, pulse, 1.0)
