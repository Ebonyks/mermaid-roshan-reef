class_name FashionWardrobe
extends RefCounted
## Clothing overlays use the existing wardrobe lifetime and navigation owner.
## Durable state belongs to ReefMain. UI references live in its existing wd.
const PERSON := "fashion_person"
const PAGE := "fashion_page"
const PARTY := "fashion_party"
const PRACTICE := "fashion_practice"
const PAINTED_PANEL: Texture2D = preload("res://assets/fashion/skin_engine_v2/ui/wardrobe_panel.png")
const PAINTED_CARD: Texture2D = preload("res://assets/fashion/skin_engine_v2/ui/wardrobe_card.png")
var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func open(party: bool = false) -> void:
	m._wardrobe_ref()._close_wardrobe()
	m._wardrobe_ref()._open_wardrobe_shell()
	m.wardrobe_layer.set_meta("fashion_fixed_preview", true)
	FashionDesigner.refresh_unlocks(m)
	m.wd[PERSON] = "roshan"
	m.wd[PAGE] = 0
	m.wd[PARTY] = party
	m.wd[PRACTICE] = false
	_build()
	_cue("party_dress" if party else "choose")

func _cue(event: String) -> void:
	m._audio_ref()._stop_active_speech()
	m._say("roshan", "fashion_" + event)

func _button(stage: Control, id: String, rect: Rect2, caption: String,
		callback: Callable, portrait: Texture2D = null) -> Button:
	var button := Button.new()
	button.name = id
	button.position = rect.position
	button.size = rect.size
	button.custom_minimum_size = rect.size
	button.text = caption
	StorybookUI.style_picture_button(button, StorybookUI.PAPER,
		StorybookUI.PURPLE, 30, StorybookUI.ROLE_CHILD_CONTROL, 30)
	for state: String in ["normal", "hover", "pressed", "focus"]:
		var painted := StyleBoxTexture.new()
		painted.texture = PAINTED_CARD
		painted.texture_margin_left = 36
		painted.texture_margin_right = 36
		painted.texture_margin_top = 36
		painted.texture_margin_bottom = 36
		painted.content_margin_left = 12
		painted.content_margin_right = 12
		painted.content_margin_top = 12
		painted.content_margin_bottom = 12
		painted.modulate_color = Color(1.0,0.86,0.64) if state in ["pressed","focus"] else (Color(1.0,0.95,0.83) if state == "hover" else Color.WHITE)
		button.add_theme_stylebox_override(state, painted)
	if portrait != null:
		var art := TextureRect.new()
		art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		art.texture = portrait
		art.position = Vector2(8, 8)
		art.size = rect.size - Vector2(16, 40)
		art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		art.mouse_filter = Control.MOUSE_FILTER_IGNORE
		button.add_child(art)
		button.text = ""
		var label := Label.new()
		label.text = caption
		label.position = Vector2(0, rect.size.y - 40)
		label.size = Vector2(rect.size.x, 35)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		StorybookUI.style_label(label, 30, StorybookUI.INK, 2)
		button.add_child(label)
	button.pressed.connect(callback)
	stage.add_child(button)
	return button

func _build() -> void:
	var stage: Control = m.wd.get("stage") as Control
	if stage == null:
		return
	var previous: Tween = m.wd.get("feedback_tween") as Tween
	if previous != null and previous.is_valid():
		previous.kill()
	for child: Node in stage.get_children():
		stage.remove_child(child)
		child.queue_free()
	var panel := TextureRect.new()
	panel.texture = PAINTED_PANEL
	panel.position = Vector2(28,18)
	panel.size = Vector2(1224,684)
	panel.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	panel.stretch_mode = TextureRect.STRETCH_SCALE
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(panel)
	var party: bool = bool(m.wd[PARTY])
	var practice: bool = bool(m.wd[PRACTICE])
	var person: String = String(m.wd[PERSON])
	var phase: int = FashionDesigner.next_disguise_phase(m)
	var title := Label.new()
	title.text = "Party dress" if party else ("Disguise play" if practice else ("Dress up: " + String(FashionDesigner.character(person).get("name", "")) if person in ["roshan","rumi","daddy_mermaid"] else "Our clothes"))
	title.position = Vector2(165, 22)
	title.size = Vector2(800, 64)
	StorybookUI.style_label(title, 42, StorybookUI.INK, 4)
	stage.add_child(title)
	if not party and not practice:
		for index: int in range(FashionDesigner.CHARACTERS.size()):
			var entry: Dictionary = FashionDesigner.CHARACTERS[index]
			var id: String = String(entry["id"])
			var pick := _button(stage, "FashionCharacter_" + id,
				Rect2(45 + index * 126, 140, 116, 120), "",
				_select_person.bind(id), FashionOutfitRenderer.portrait(m, id))
			pick.set_meta("selected", person == id)
			if person == id:
				pick.modulate = Color(1.0, 0.88, 0.64)
	var preview := TextureRect.new()
	preview.name = "FashionCurrentLook"
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.texture = FashionOutfitRenderer.portrait(m, person)
	preview.position = Vector2(70, 270)
	preview.size = Vector2(425, 300)
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	preview.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(preview)
	m.wd["preview"] = preview
	m.wd["fashion_fit_rect"] = FashionSkinEngine.fit_rect(person,preview)
	var dressing: FashionDressingInput = null
	if not practice and person in ["roshan","rumi","daddy_mermaid"]:
		dressing = FashionDressingInput.new()
		stage.add_child(dressing)
		dressing.setup(m,self)
		m.wd["dressing_input"] = dressing
	var feedback := Control.new()
	feedback.name = "WardrobeFeedbackLayer"
	feedback.mouse_filter = Control.MOUSE_FILTER_IGNORE
	feedback.z_index = 20
	stage.add_child(feedback)
	m.wd["feedback_layer"] = feedback
	var entries: Array[Dictionary] = FashionDesigner.outfits(person)
	if party:
		entries = [FashionDesigner.outfit(FashionDesigner.PARTY_DRESS)]
	elif practice:
		if phase >= 3:
			m.wd[PRACTICE] = false
			_build()
			_cue("done")
			return
		var sample := TextureRect.new()
		sample.name = "FashionGoalPicture"
		sample.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		sample.texture = FashionOutfitRenderer.portrait(m, "rumi" if phase == 1 else "roshan", "rumi_garden_v1" if phase == 1 else "roshan_garden_v1")
		sample.position = Vector2(730, 80)
		sample.size = Vector2(150, 158)
		sample.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		sample.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		sample.mouse_filter = Control.MOUSE_FILTER_IGNORE
		stage.add_child(sample)
		entries = [FashionDesigner.outfit("roshan_ribbon_v1"),
			FashionDesigner.outfit(FashionDesigner.PARTY_DRESS),
			FashionDesigner.outfit("roshan_garden_v1")]
		if phase == 2:
			entries = [{"id": "finish_bow", "kind": "disguise", "label": "Bow"}]
	var start: int = 0 if party or practice else int(m.wd[PAGE]) * 3
	for index: int in range(start, mini(start + 3, entries.size())):
		var entry: Dictionary = entries[index]
		var id: String = String(entry["id"])
		var locked: bool = id != "finish_bow" and not FashionDesigner.owned(m, id)
		var source_id: String = "roshan_garden_disguise_v1" if id == "finish_bow" else id
		var clothing: Texture2D = FashionSkinEngine.garment(source_id) if not practice else null
		var card := _button(stage, "FashionOutfit_" + id,
			Rect2(575 + (index - start) * 212, 258, 196, 306),
			"🔒" if locked else ("✔" if FashionDesigner.selected(m, person) == id else ""),
			_pick.bind(id), clothing if clothing != null else FashionOutfitRenderer.portrait(m, person, source_id))
		if dressing != null and not locked and clothing != null:
			card.gui_input.connect(dressing.card_input.bind(id,card))
		card.set_meta("locked", locked)
		if locked:
			var unlock_picture := TextureRect.new()
			unlock_picture.name = "FashionUnlockSourcePicture"
			unlock_picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			unlock_picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			var source: String = ChapterTwoGiantCake2D.FINAL_CAKE_TEXTURE if String(entry["kind"]) == "party" else (
				"res://assets/fashion/party_dress_garment.png" if String(entry["kind"]) == "disguise" else "res://assets/chapter2/birthday/sky_lagoon_strawberry_single.png")
			unlock_picture.texture = load(source) as Texture2D
			unlock_picture.position = Vector2(132, 244)
			unlock_picture.size = Vector2(54, 54)
			unlock_picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
			card.add_child(unlock_picture)
		if party or practice:
			var pointer := Label.new()
			pointer.name = "FashionVisualPointer"
			pointer.text = "👇"
			pointer.position = Vector2(card.position.x + 60, 205)
			StorybookUI.style_label(pointer, 45, StorybookUI.GOLD, 3)
			stage.add_child(pointer)
	if not party and not practice:
		_button(stage, "FashionPreviousPage", Rect2(590, 577, 132, 110), "◀",
			_page.bind(-1))
		_button(stage, "FashionNextPage", Rect2(738, 577, 132, 110), "▶",
			_page.bind(1))
		if FashionDesigner.practice_available(m):
			_button(stage, "FashionDisguisePlay", Rect2(55, 577, 180, 110), "🎭",
				_start_practice)
	_button(stage, "FashionHelp", Rect2(888, 577, 132, 110), "?", _help)
	_button(stage, "FashionFinish", Rect2(1040, 577, 165, 110), "✔",
		m._wardrobe_ref()._close_wardrobe)

func _select_person(id: String) -> void:
	m.wd[PERSON] = id
	m.wd[PAGE] = 0
	_build()
	_cue("choose")

func _page(direction: int) -> void:
	var count: int = FashionDesigner.outfits(String(m.wd[PERSON])).size()
	m.wd[PAGE] = posmod(int(m.wd[PAGE]) + direction, ceili(count / 3.0))
	_build()

func _help() -> void:
	if bool(m.wd[PARTY]):
		_cue("party_dress")
	elif bool(m.wd[PRACTICE]):
		_cue(["role_pick", "blend_pick", "finish_piece"][FashionDesigner.next_disguise_phase(m)])
	else:
		_cue("choose")

func _start_practice() -> void:
	m.wd[PRACTICE] = true
	m.wd[PERSON] = "roshan"
	_build()
	_help()

func _pick(id: String) -> void:
	if not (m.wd.get("fashion_drag", {}) as Dictionary).is_empty():
		return
	if bool(m.wd[PRACTICE]):
		var phase: int = FashionDesigner.next_disguise_phase(m)
		if not FashionDesigner.complete_disguise_phase(m, phase, id, true):
			_cue("help")
			return
		_build()
		if FashionDesigner.next_disguise_phase(m) < 3:
			_help()
		return
	if not FashionDesigner.owned(m, id):
		var kind: String = String(FashionDesigner.outfit(id).get("kind", ""))
		_cue("locked_party" if kind == "party" else ("locked_disguise" if kind == "disguise" else "locked_garden"))
		return
	FashionDesigner.equip(m, String(m.wd[PERSON]), id, true)
	if bool(m.wd[PARTY]) and FashionDesigner.party_dressed(m):
		m._wardrobe_ref()._close_wardrobe()
		m.call_deferred("_start_chapter2_lawn")
		return
	_build()
	m._wardrobe_ref()._wardrobe_feedback_burst()
	_cue("changed")
