extends SceneTree
# Trusted UI contract probe: the dormant storybook prototypes are represented
# by real Controls, every required child target is thumb-sized, overlay exits
# are neutral, and the one-row paint grammar is shared by craft + stuffies.

var failed := false
var main: ReefMain

const GAMEPLAY_HUD_SURFACES := [
	"res://scripts/main.gd",
	"res://scripts/combat_arena.gd",
	"res://scripts/stuffie_battle.gd",
	"res://scripts/dungeon_level.gd",
	"res://scripts/dungeon_puzzle_room.gd",
	"res://scripts/galaxy.gd",
	"res://scripts/ember_fortress.gd",
	"res://scripts/opera_house.gd",
	"res://scripts/opera_act.gd",
	"res://scripts/medal_system.gd"]
const CHILD_MENU_SYSTEMS := [
	{"id": "intro", "path": "res://scripts/intro_overlay.gd", "token": "adorn_panel"},
	{"id": "pause", "path": "res://scripts/pause_menu.gd", "token": "PauseShell"},
	{"id": "craft", "path": "res://scripts/craft_studio.gd", "token": "adorn_panel"},
	{"id": "castle_logo", "path": "res://scripts/castle_logo_studio.gd", "token": "CastleLogoShellCrest"},
	{"id": "wardrobe", "path": "res://scripts/wardrobe_ui.gd", "token": "style_picture_button"},
	{"id": "stickers", "path": "res://scripts/wardrobe_ui.gd", "token": "StickerBook"},
	{"id": "critters", "path": "res://scripts/collection_system.gd", "token": "CritterBook"},
	{"id": "stuffie_care", "path": "res://scripts/companion.gd", "token": "StuffieCare"},
	{"id": "stuffie_picker", "path": "res://scripts/companion.gd", "token": "StuffiePicker"},
	{"id": "castle_rooms", "path": "res://scripts/arena/castle_rooms_25d.gd", "token": "ROOM_ART"},
	{"id": "kitchen", "path": "res://scripts/arena/castle_rooms_25d.gd", "token": "KitchenFridgeMenu"},
	{"id": "picture_games", "path": "res://scripts/games/picture_games.gd", "token": "PictureGameStorybookHeader"},
	{"id": "dance", "path": "res://scripts/games/dance_engine.gd", "token": "StorybookUI.add_panel"},
	{"id": "kart_garage", "path": "res://scripts/kart.gd", "token": "KartRideChoice_"},
	{"id": "opera_lobby", "path": "res://scripts/opera_lobby_2d.gd", "token": "CareerCard"}]

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

func _check_storybook_coverage() -> void:
	for path: String in GAMEPLAY_HUD_SURFACES:
		var source: String = FileAccess.get_file_as_string(path)
		_check(source.contains("StorybookUI.add_hud_panel"), "%s uses a shared Storybook HUD surface" % path.get_file())
	_check(CHILD_MENU_SYSTEMS.size() == 15,
		"menu census covers all 15 child-facing systems")
	var developer_source: String = FileAccess.get_file_as_string(
		"res://scripts/dev_mode.gd")
	_check(developer_source.contains("DeveloperStorybookPanel")
		and developer_source.contains("DeveloperShellCrest")
		and developer_source.contains("_style_parent_controls"),
		"16th interactive system gives parent Developer Mode Storybook styling")
	for row: Dictionary in CHILD_MENU_SYSTEMS:
		var path: String = String(row["path"])
		var menu_source: String = FileAccess.get_file_as_string(path)
		_check(menu_source.contains("StorybookUI")
			and menu_source.contains(String(row["token"])),
			"%s menu uses the audited Storybook contract" % String(row["id"]))
	var picture_source: String = FileAccess.get_file_as_string(
		"res://scripts/games/picture_games.gd")
	var wardrobe_source: String = FileAccess.get_file_as_string(
		"res://scripts/wardrobe_ui.gd")
	var kart_source: String = FileAccess.get_file_as_string("res://scripts/kart.gd")
	var pause_source: String = FileAccess.get_file_as_string(
		"res://scripts/pause_menu.gd")
	var touch_source: String = FileAccess.get_file_as_string("res://scripts/touch_ui.gd")
	_check(picture_source.contains("style_picture_button")
		and wardrobe_source.contains("style_picture_button")
		and kart_source.contains("style_picture_button"),
		"former flat picture choices share physical button states")
	_check(kart_source.contains("KartPaintChoice_"),
		"kart garage exposes direct ride and paint choices")
	_check(not pause_source.contains("PauseTouchModeButton")
		and not pause_source.contains("REEF"),
		"Pause removes the obsolete touch choice and Reef destination")
	_check(touch_source.contains("_stick_hint.visible = false")
		and not touch_source.contains("_stick_hint.visible = wants_touch()"),
		"point-to-interact keeps the movement pad renderer hidden")
	var player_copy: String = ""
	for ui_path: String in [
		"res://scripts/collection_system.gd",
		"res://scripts/companion.gd",
		"res://scripts/games/dance_engine.gd",
		"res://scripts/games/shop.gd",
		"res://scripts/main.gd",
		"res://scripts/opera_house.gd",
		"res://scripts/opera_competition.gd",
		"res://scripts/pause_menu.gd",
		"res://scripts/wardrobe_ui.gd",
	]:
		player_copy += FileAccess.get_file_as_string(ui_path)
	for retired_copy: String in [
		"Back to the reef", "Reef Celebration", "Reef Garden",
		"REEF BAKE-OFF", "Queen of the Reef", "Caribbean reef",
	]:
		_check(not player_copy.contains(retired_copy),
			"retired player-facing Reef copy stays absent: %s" % retired_copy)
	var companion_source: String = FileAccess.get_file_as_string("res://scripts/companion.gd")
	_check(not companion_source.contains("companion_hud_btn")
		and not companion_source.contains("func open_menu()"),
		"legacy duplicate Stuffie launcher and care panel stay removed")

func _init() -> void:
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	_check_storybook_coverage()

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
	_check(_find(main.intro_layer, "IntroShellCrest") != null,
		"picture intro uses the recovered shell crest")
	main._skip_intro()
	await process_frame

	# The gameplay canvas stays action-first: saved totals remain available to
	# systems, but persistent report-card text is not rendered over the world.
	var status_tray := _find(main.hud_layer, "HudStatusTray") as Control
	var objective_sentence := _find(main.hud_layer, "HudPictureObjective") as Control
	_check(status_tray != null and not status_tray.visible
		and not main.hud_pearls.visible and not main.hud_stars.visible,
		"free roam hides irrelevant persistent totals")
	_check(objective_sentence != null and not objective_sentence.visible,
		"free roam hides the legacy sentence objective")

	# Pause: raised above overlays only while open; resume dominates the icon grid.
	_check_target(main.pause_layer, "PauseCornerButton", "pause corner owns a 128px envelope", Vector2(128, 128))
	_check(_find(main.pause_layer, "PauseCornerShell") != null,
		"pause control uses the recovered shell crest")
	main.toggle_pause()
	_check(main.pause_layer.layer == 29 and main.get_tree().paused, "pause sheet rises above active overlays")
	_check_target(main.pause_panel, "PauseResumeButton", "resume is the dominant 300x140 action", Vector2(300, 140))
	_check_target(main.pause_panel, "PauseStickerButton", "sticker tile is thumb-sized")
	_check_target(main.pause_panel, "PauseMusicButton", "music toggle is thumb-sized")
	_check_target(main.pause_panel, "PauseQualityButton", "quality toggle is thumb-sized")
	_check(_find(main.pause_panel, "PauseShellCrest") != null,
		"pause sheet carries shell-and-pearl adornment")
	_check(_find(main.pause_panel, "PauseTouchModeButton") == null,
		"pause sheet has no movement-mode decision")
	var touch_pad := _find(main.touch_ui, "TouchShellPad") as Control
	_check(touch_pad != null and not touch_pad.visible,
		"movement pad stays off-screen in point-to-interact play")
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
	_check(_find(main.craft_layer, "CraftShellCrest") != null,
		"craft studio carries the shared shell crest")
	for node: Node in main.craft_layer.find_children("CraftSwatch_*", "", true, false):
		_check(_touch_size(node as Control).x >= 110.0 and _touch_size(node as Control).y >= 110.0, "craft swatch is at least 110x110")
	main._close_craft()
	await process_frame

	# Castle logo: six direct paints, eight picture marks, and one large preview.
	main._open_castle_logo()
	await process_frame
	_check_target(main.castle_logo_layer, "CastleLogoBackButton",
		"castle logo has a neutral thumb-sized back")
	_check_target(main.castle_logo_layer, "CastleLogoFinishButton",
		"castle logo finish is a 150px-class primary action", Vector2(150, 150))
	_check(_count_named(main.castle_logo_layer, "CastleLogoColor_*") == 6,
		"castle logo offers five solid paints plus rainbow")
	_check(_count_named(main.castle_logo_layer, "CastleLogoSymbol_*") == 8,
		"castle logo offers eight child-readable picture marks")
	_check(_find(main.castle_logo_layer, "CastleLogoPreview") != null
		and _find(main.castle_logo_layer, "CastleLogoShellCrest") != null,
		"castle logo has a live emblem preview in the shared shell frame")
	for node: Node in main.castle_logo_layer.find_children(
			"CastleLogoColor_*", "", true, false):
		_check(_touch_size(node as Control).x >= 110.0
			and _touch_size(node as Control).y >= 110.0,
			"castle logo paint is at least 110x110")
	main._close_castle_logo()
	await process_frame

	# Wardrobe and books share the same back/finish grammar.
	main._open_wardrobe()
	await process_frame
	_check_target(main.wardrobe_layer, "WardrobeBackButton", "wardrobe back is thumb-sized")
	_check_target(main.wardrobe_layer, "WardrobeFinishButton", "wardrobe finish is thumb-sized")
	_check(_find(main.wardrobe_layer, "WardrobeShellCrest") != null,
		"wardrobe carries the shared shell-and-pearl frame")
	_check(_count_named(main.wardrobe_layer, "WardrobeLookPreview_*") == 3,
		"wardrobe choices are backed by three existing character previews")
	main._close_wardrobe()
	main._open_stickers()
	await process_frame
	_check_target(main.stickers_layer, "StickerBookBackButton", "sticker book back is thumb-sized")
	_check(_find(main.stickers_layer, "StickerBookShellCrest") != null,
		"sticker book carries the shared shell crest")
	main._close_stickers()
	main._collection_ref().open_book()
	await process_frame
	_check_target(main.collection_layer, "CritterBookBackButton", "critter book back is thumb-sized")
	_check(_find(main.collection_layer, "CritterBookShellCrest") != null,
		"critter book carries the shared shell crest")
	main._collection_ref().close_book()

	# Stuffie paint uses the same one-active-part grammar and 110px swatches.
	main._companion_ref().open_picker(false, "mewsha")
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
	_check(launcher != null and launcher.position.x >= 820.0
		and launcher.position.x + launcher.size.x <= 1000.0
		and String(launcher.get_meta("hud_zone", "")) == "upper_right_inset",
		"stuffie care launcher is inset from the far-corner Pause control")
	var critter_button := _find(main, "CritterBookCornerButton") as Control
	var pause_button := _find(main, "PauseCornerButton") as Control
	_check(launcher != null and critter_button != null and pause_button != null
		and launcher.global_position.x + launcher.size.x < critter_button.global_position.x
		and critter_button.global_position.x + critter_button.size.x < pause_button.global_position.x,
		"Stuffie, Critter Book, and Pause keep separate upper-hand hit areas")
	_check(_count_named(main, "StuffieCareMenuButton") == 1, "exactly one Stuffie care launcher exists")
	_check(_find(main.hud_layer, "StuffieWatchShell") != null,
		"Stuffie watch keeps its inset shell treatment")
	main._companion_ref().open_care_menu()
	await process_frame
	_check_target(main.companion_care_layer, "StuffieCareBackButton", "Tamagotchi sheet has a neutral thumb-sized back")
	_check_target(main.companion_care_layer, "StuffieSwitchButton", "Tamagotchi sheet has a thumb-sized friend switch")
	_check(_find(main.companion_care_layer, "StuffieCareShellCrest") != null,
		"Tamagotchi sheet carries the shared shell-and-pearl treatment")
	_check(_find(main.companion_care_layer, "StuffieHeartProgress") != null, "Tamagotchi sheet shows hearts toward the next growth star")
	_check(_count_named(main.companion_care_layer, "StuffieCareAction_*") == 5, "Tamagotchi sheet exposes five picture care actions")
	for node: Node in main.companion_care_layer.find_children("StuffieCareAction_*", "", true, false):
		_check(_touch_size(node as Control).x >= 110.0 and _touch_size(node as Control).y >= 110.0, "Tamagotchi care action is at least 110x110")
	main._companion_ref().close_care_menu()

	# Picture games inherit the neutral exit rather than an alarming X.
	main._mg2d_open("garden")
	await process_frame
	var picture_back := _check_target(main.mg2d_layer, "PictureGameBackButton", "picture-game back is thumb-sized")
	_check(picture_back != null and bool(picture_back.get_meta("neutral_exit", false)), "picture-game exit is neutral")
	_check(_find(main.mg2d_layer, "PictureGameStorybookHeader") != null
		and _find(main.mg2d_layer, "PictureGameShellCrest") != null,
		"picture games carry the shared Storybook shell header")
	main._mg2d_close()

	print("UI_SYSTEM|RESULT|", "FAIL" if failed else "ALL OK")
	quit(1 if failed else 0)
