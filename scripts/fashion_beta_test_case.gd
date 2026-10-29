class_name FashionBetaTestCase
extends RefCounted
## Actual input, cancellation, earned unlocks and disk reload for the beta collection.
static func choose(main: ReefMain, slot: String, id: String) -> bool:
	await FashionSkinEngineTestCase._tap(main, main.wardrobe_layer.find_child("FashionSlot_" + slot, true, false) as Control)
	for page: int in range(6):
		var item: Control = main.wardrobe_layer.find_child("FashionOutfit_" + id, true, false) as Control
		if item != null:
			await FashionSkinEngineTestCase._tap(main, item)
			return true
		await FashionSkinEngineTestCase._tap(main, main.wardrobe_layer.find_child("FashionNextPage", true, false) as Control)
	return false

static func run(main: ReefMain, check: Callable) -> void:
	var old_stars: int = main.opera_stars
	var old_unlocked: Dictionary = main.outfits_unlocked.duplicate(true)
	main.opera_stars = 0
	for theme: String in ["candy", "astronaut"]:
		for slot: String in FashionParts.SLOTS:
			main.outfits_unlocked.erase(slot + "_" + theme + "_v1")
	FashionParts.refresh_unlocks(main)
	check.call(not FashionDesigner.owned(main, "body_candy_v1") and not FashionDesigner.owned(main, "body_astronaut_v1"), "Beta earned costumes stay locked without their career")
	var wardrobe := FashionWardrobe.new(main)
	for person: String in FashionParts.PEOPLE:
		wardrobe.open()
		check.call(main.wardrobe_layer.layer == 28 and main.navigation_layer.layer > main.wardrobe_layer.layer, "Fashion surface covers play while global Back stays above it")
		var root: Control = (main.wd["stage"] as Control).get_parent() as Control
		var backdrop: ColorRect = root.get_child(0) as ColorRect
		check.call(backdrop.color.a == 1.0 and backdrop.size == main.get_viewport().get_visible_rect().size, "Wardrobe backing covers the whole viewport")
		await FashionSkinEngineTestCase._tap(main, main.wardrobe_layer.find_child("FashionCharacter_" + person, true, false) as Control)
		var cards: Array[Node] = main.wardrobe_layer.find_children("FashionOutfit_*", "Button", true, false)
		check.call(cards.size() == FashionWardrobe.PAGE_SIZE, "Beta exposes six direct clothing choices: " + person)
		for index: int in range(cards.size()):
			var card: Control = cards[index] as Control
			var bounds := Rect2(card.position, card.size)
			check.call(card.size.x >= 110 and card.size.y >= 110 and Rect2(0, 0, 1280, 720).encloses(bounds), "Beta card remains a full child target: " + String(card.name))
			for other: int in range(index):
				var sibling: Control = cards[other] as Control
				check.call(not bounds.intersects(Rect2(sibling.position, sibling.size)), "Beta cards never overlap")
		for theme: String in ["ballet", "magician"]:
			for slot: String in FashionParts.SLOTS:
				var id: String = slot + "_" + theme + "_v1"
				check.call(await choose(main, slot, id), "New beta piece is reachable through pages: " + person + "/" + id)
				check.call(FashionParts.selected(main, person, slot) == id, "New beta piece equips via real input: " + person + "/" + id)
				var selected: Button = main.wardrobe_layer.find_child("FashionOutfit_" + id, true, false) as Button
				check.call(selected != null and bool(selected.get_meta("selected", false)), "Worn beta card has a visible selection state")
	# The owner cancellation must be neutral; another finger's cancellation is not ownership.
	await FashionSkinEngineTestCase._tap(main, main.wardrobe_layer.find_child("FashionSlot_head", true, false) as Control)
	var target: Control = main.wardrobe_layer.find_child("FashionOutfit_head_royal_v1", true, false) as Control
	var point: Vector2 = target.get_global_transform_with_canvas() * (target.size * 0.5)
	var before: String = FashionParts.selected(main, "daddy_mermaid", "head")
	await FashionSkinEngineTestCase._touch(main, point, 44, true)
	var cancelled := InputEventScreenTouch.new()
	cancelled.position = point
	cancelled.index = 45
	cancelled.pressed = false
	cancelled.canceled = true
	main.get_viewport().push_input(cancelled, true)
	await main.get_tree().process_frame
	check.call(int((main.wd.get("fashion_drag", {}) as Dictionary).get("pointer", -99)) == 44, "Foreign cancellation cannot steal a held costume")
	cancelled.index = 44
	main.get_viewport().push_input(cancelled, true)
	await main.get_tree().process_frame
	await FashionSkinEngineTestCase._touch(main, point, 44, false)
	check.call((main.wd.get("fashion_drag", {}) as Dictionary).is_empty() and FashionParts.selected(main, "daddy_mermaid", "head") == before, "Canceled owner touch and stale release never equip")
	main._wardrobe_ref()._close_wardrobe()
	main.opera_stars = (1 << ChapterTwoDirector.ACT_CANDY_MAKER) | (1 << ChapterTwoDirector.ACT_ASTRONAUT)
	FashionParts.refresh_unlocks(main)
	for theme: String in ["candy", "astronaut"]:
		for slot: String in FashionParts.SLOTS:
			check.call(FashionDesigner.owned(main, slot + "_" + theme + "_v1"), "Existing earned career unlocks each matching slot: " + theme + "/" + slot)
	wardrobe.open()
	for pair: Array in [["head", "head_candy_v1"], ["body", "body_astronaut_v1"], ["tail", "tail_ballet_v1"]]:
		check.call(await choose(main, String(pair[0]), String(pair[1])), "Earned beta piece reachable after unlock")
	main._wardrobe_ref()._close_wardrobe()
	check.call(main._write_save(), "Beta mixed outfit uses the transactional save")
	var raw: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ReefMain.SAVE_PATH)) as Dictionary
	main.character_clothing_parts = {}
	FashionDesigner.restore(main, raw)
	check.call(FashionParts.selected(main, "roshan", "head") == "head_candy_v1" and FashionParts.selected(main, "roshan", "body") == "body_astronaut_v1" and FashionParts.selected(main, "roshan", "tail") == "tail_ballet_v1", "Disk reload retains the earned mixed beta outfit")
	# Real image controls must stay at the intended small pointer size after texture assignment.
	wardrobe.open(true)
	for slot: String in ["body", "head", "tail"]:
		await FashionSkinEngineTestCase._tap(main, main.wardrobe_layer.find_child("FashionSlot_" + slot, true, false) as Control)
		var pointers: Array[Node] = main.wardrobe_layer.find_children("FashionVisualPointer", "TextureRect", true, false)
		check.call(pointers.size() == 1, "Party wardrobe has exactly one actionable guide: " + slot)
		if pointers.size() == 1:
			var hand: TextureRect = pointers[0] as TextureRect
			check.call(hand.size == Vector2(52, 52) and Rect2(0, 0, 1280, 720).encloses(Rect2(hand.position, hand.size)), "Painted pointer stays small and inside the stage")
			check.call(String(hand.get_meta("target")) == ("FashionOutfit_" + FashionDesigner.PARTY_DRESS if slot == "body" else "FashionSlot_body"), "Party guide points to the required live dress target")
	main._wardrobe_ref()._close_wardrobe()
	main.opera_stars = old_stars
	main.outfits_unlocked = old_unlocked
