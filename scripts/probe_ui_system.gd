extends SceneTree
# Trusted UI contract probe: the dormant storybook prototypes are represented
# by real Controls, every required child target is thumb-sized, overlay exits
# are neutral, and the one-row paint grammar is shared by craft + stuffies.

var failed := false
var main: ReefMain

func _check(ok: bool, label: String) -> void:
	if ok:
		print("UI_SYSTEM|OK|", label)
	else:
		failed = true
		print("FAIL UI_SYSTEM|", label)

func _find(from: Node, pattern: String) -> Node:
	return from.find_child(pattern, true, false)

func _touch_size(control: Control) -> Vector2:
	return Vector2(maxf(control.size.x, control.custom_minimum_size.x), maxf(control.size.y, control.custom_minimum_size.y))

func _check_target(from: Node, pattern: String, label: String, minimum: Vector2 = StorybookUI.MIN_TOUCH) -> Control:
	var node := _find(from, pattern)
	var control := node as Control
	_check(control != null and _touch_size(control).x >= minimum.x and _touch_size(control).y >= minimum.y, label)
	return control

func _count_named(from: Node, pattern: String) -> int:
	var count := 0
	for node: Node in from.find_children(pattern, "", true, false):
		if node is Control:
			count += 1
	return count

func _init() -> void:
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame

	# Intro: four shape pips, repeat voice, explicit next, and deliberate hold-skip.
	if not main.intro_active:
		main._build_intro()
	await process_frame
	_check(_count_named(main.intro_layer, "IntroNextButton") == 1, "picture intro has one obvious next action")
	_check_target(main.intro_layer, "IntroNextButton", "intro next is a 150px-class target", Vector2(150, 150))
	_check_target(main.intro_layer, "IntroRepeatVoiceButton", "intro narration repeat is thumb-sized")
	var skip := _check_target(main.intro_layer, "IntroHoldToSkipButton", "intro skip is thumb-sized")
	_check(skip != null and float(skip.get_meta("hold_seconds", 0.0)) >= 1.2, "intro skip requires a deliberate hold")
	var intro_pips: Array = main.intro_layer.get_meta("page_pips", [])
	_check(intro_pips.size() == 4, "intro has four non-reading page pips")
	main._skip_intro()
	await process_frame

	# Pause: raised above overlays only while open; resume dominates the icon grid.
	_check_target(main.pause_layer, "PauseCornerButton", "pause corner owns a 128px envelope", Vector2(128, 128))
	main.toggle_pause()
	_check(main.pause_layer.layer == 29 and main.get_tree().paused, "pause sheet rises above active overlays")
	_check_target(main.pause_panel, "PauseResumeButton", "resume is the dominant 300x140 action", Vector2(300, 140))
	_check_target(main.pause_panel, "PauseStickerButton", "sticker tile is thumb-sized")
	_check_target(main.pause_panel, "PauseMusicButton", "music toggle is thumb-sized")
	_check_target(main.pause_panel, "PauseQualityButton", "quality toggle is thumb-sized")
	var leave := _find(main.pause_panel, "PauseLeaveButton") as Button
	_check(leave != null and bool(leave.get_meta("neutral_exit", false)), "activity exit uses neutral-back semantics")
	main.toggle_pause()
	_check(main.pause_layer.layer == 12 and not main.get_tree().paused, "resume restores normal overlay order")

	# Craft: large preview, three part selectors, exactly one large palette row.
	main._open_craft_studio()
	await process_frame
	_check_target(main.craft_layer, "CraftBackButton", "craft has a neutral thumb-sized back")
	_check_target(main.craft_layer, "CraftFinishButton", "craft finish is a 150px-class primary action", Vector2(150, 150))
	_check(_count_named(main.craft_layer, "CraftPart_*") == 3, "craft exposes three picture part selectors")
	_check(_count_named(main.craft_layer, "CraftSwatch_*") == 8 and _count_named(main.craft_layer, "CraftRainbowSwatch") == 1, "craft shows one nine-choice palette row")
	for node: Node in main.craft_layer.find_children("CraftSwatch_*", "", true, false):
		_check(_touch_size(node as Control).x >= 110.0 and _touch_size(node as Control).y >= 110.0, "craft swatch is at least 110x110")
	main._close_craft()
	await process_frame

	# Wardrobe and books share the same back/finish grammar.
	main._open_wardrobe()
	await process_frame
	_check_target(main.wardrobe_layer, "WardrobeBackButton", "wardrobe back is thumb-sized")
	_check_target(main.wardrobe_layer, "WardrobeFinishButton", "wardrobe finish is thumb-sized")
	main._close_wardrobe()
	main._open_stickers()
	await process_frame
	_check_target(main.stickers_layer, "StickerBookBackButton", "sticker book back is thumb-sized")
	main._close_stickers()
	main._collection_ref().open_book()
	await process_frame
	_check_target(main.collection_layer, "CritterBookBackButton", "critter book back is thumb-sized")
	main._collection_ref().close_book()

	# Stuffie paint uses the same one-active-part grammar and 110px swatches.
	main._companion_ref().open_picker(false)
	await process_frame
	_check_target(main.companion_layer, "StuffiePickerBackButton", "stuffie picker back is thumb-sized")
	_check(_count_named(main.companion_layer, "StuffiePart_*") == 3, "stuffie picker has three picture part selectors")
	_check(_count_named(main.companion_layer, "StuffieSwatch_*") == 8, "stuffie picker shows one palette at a time")
	for node: Node in main.companion_layer.find_children("StuffieSwatch_*", "", true, false):
		_check(_touch_size(node as Control).x >= 110.0 and _touch_size(node as Control).y >= 110.0, "stuffie swatch is at least 110x110")
	main._companion_ref().close_picker()

	# Tamagotchi care owns an inset upper-right launcher, never the Pause corner,
	# and exposes all five persisted care verbs through the same storybook sheet.
	main.companion_id = "mewsha"
	main._companion_ref().tick(0.0)
	var launcher := _check_target(main.hud_layer, "StuffieCareMenuButton", "stuffie care launcher is a 128px target", Vector2(128, 128))
	_check(launcher != null and launcher.position.x >= 900.0
		and launcher.position.x + launcher.size.x <= 1130.0
		and String(launcher.get_meta("hud_zone", "")) == "upper_right_inset",
		"stuffie care launcher is inset from the far-corner Pause control")
	main._companion_ref().open_care_menu()
	await process_frame
	_check_target(main.companion_care_layer, "StuffieCareBackButton", "Tamagotchi sheet has a neutral thumb-sized back")
	_check_target(main.companion_care_layer, "StuffieSwitchButton", "Tamagotchi sheet has a thumb-sized friend switch")
	_check(_count_named(main.companion_care_layer, "StuffieCareAction_*") == 5, "Tamagotchi sheet exposes five picture care actions")
	for node: Node in main.companion_care_layer.find_children("StuffieCareAction_*", "", true, false):
		_check(_touch_size(node as Control).x >= 110.0 and _touch_size(node as Control).y >= 110.0, "Tamagotchi care action is at least 110x110")
	main._companion_ref().close_care_menu()

	# Picture games inherit the neutral exit rather than an alarming X.
	main._mg2d_open("garden")
	await process_frame
	var picture_back := _check_target(main.mg2d_layer, "PictureGameBackButton", "picture-game back is thumb-sized")
	_check(picture_back != null and bool(picture_back.get_meta("neutral_exit", false)), "picture-game exit is neutral")
	main._mg2d_close()

	# ---- contracts inherited from the retired probe_ui ----------------------
	# The gold-slice probe asserted geometry StorybookUI replaced, but three of
	# its checks are CLAUDE.md hard rules rather than layout details, so they
	# move here instead of being dropped with it.
	main._skip_intro()
	await process_frame
	# 1. the status tray stays icons, pips and digits - a non-reader must never
	#    be asked to read a word to know their progress
	var prose := ""
	for tray_text: String in [String(main.hud_pearls.text), String(main.hud_stars.text)]:
		for index in range(tray_text.length()):
			var code: int = tray_text.unicode_at(index)
			if (code >= 65 and code <= 90) or (code >= 97 and code <= 122):
				prose = tray_text
				break
	_check(prose == "", "status tray carries no prose (saw '%s')" % prose)
	# 2. an objective is always a picture, never text alone
	main._set_objective("probe", null, "*")
	await process_frame
	_check(main.obj_card != null and (main.obj_card as Panel).visible, "objective card appears when an objective is set")
	_check(main.obj_icon_lbl != null and (main.obj_icon_lbl as Label).visible
		and String((main.obj_icon_lbl as Label).text) != "", "objective card carries a pictogram")
	main._set_objective("", null, "")
	await process_frame
	# 3. the stick explains itself before the first drag: a visible resting
	#    affordance at a thumb-readable size
	var stick_touch: Node = main.touch_ui
	if stick_touch != null and bool(stick_touch.wants_touch()):
		var hint: Panel = stick_touch._stick_hint as Panel
		var stick_base: Panel = stick_touch._base as Panel
		var resting: Panel = hint if hint != null else stick_base
		_check(resting != null and resting.visible, "the stick shows a resting affordance before the first drag")
		_check(resting != null and _touch_size(resting).x >= 176.0,
			"the resting stick is at least 176px across (saw %s)" % [resting.size if resting != null else Vector2.ZERO])
		_check(stick_touch._act_vis != null and _touch_size(stick_touch._act_vis as Panel).x >= 128.0,
			"the action bubble is thumb-sized")

	print("UI_SYSTEM|RESULT|", "FAIL" if failed else "ALL OK")
	quit(1 if failed else 0)
