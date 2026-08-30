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
	"res://scripts/medal_system.gd"]
const CHILD_MENU_SYSTEMS := [
	{"id": "intro", "path": "res://scripts/intro_overlay.gd", "token": "adorn_panel"},
	{"id": "pause", "path": "res://scripts/pause_menu.gd", "token": "PauseShell"},
	{"id": "craft", "path": "res://scripts/craft_studio.gd", "token": "adorn_panel"},
	{"id": "castle_logo", "path": "res://scripts/castle_logo_studio.gd", "token": "adorn_panel"},
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
	{"id": "castle_careers", "path": "res://scripts/castle_career_routes.gd", "token": "RoomCareer_"}]

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

func _world_particle_count(node: Node, particle_class: String) -> int:
	var total := 1 if node.get_class() == particle_class else 0
	for child_value in node.get_children():
		var child := child_value as Node
		if child != null:
			total += _world_particle_count(child, particle_class)
	return total

func _wardrobe_feedback_is_visible(wardrobe_layer: CanvasLayer,
		preview: TextureRect) -> bool:
	if wardrobe_layer == null or preview == null:
		return false
	var feedback_layer := _find(wardrobe_layer, "WardrobeFeedbackLayer") as Control
	var burst := _find(wardrobe_layer, "WardrobePreviewFeedbackBurst") as Control
	if feedback_layer == null or burst == null or not burst.visible \
			or feedback_layer.get_child_count() != 1 \
			or int(burst.get_meta("visible_elements", 0)) != 14 \
			or burst.position.distance_to(preview.position + preview.size * 0.5) > 0.1:
		return false
	var visible_elements := 0
	for child_value in burst.get_children():
		var element := child_value as CanvasItem
		if element != null and element.visible and element.modulate.a > 0.05:
			visible_elements += 1
	return visible_elements == 14

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
	_check(wardrobe_source.find("_sparkle_burst") < 0
		and wardrobe_source.find("Vector" + str(3)) < 0,
		"wardrobe try-on feedback stays on its storybook stage")
	_check(kart_source.contains("KartPaintChoice_"),
		"kart garage exposes direct ride and paint choices")
	_check(not pause_source.contains("PauseTouchModeButton")
		and pause_source.contains("func leave_label")
		and pause_source.contains("REEF"),
		"Pause removes the obsolete touch choice and derives its real destination")
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

func _check_typography_coverage() -> void:
	var storybook_source: String = FileAccess.get_file_as_string(
		"res://scripts/storybook_ui.gd")
	var roles: Array[StringName] = [
		StorybookUI.ROLE_DISPLAY, StorybookUI.ROLE_TITLE,
		StorybookUI.ROLE_CHILD_CONTROL, StorybookUI.ROLE_BODY,
		StorybookUI.ROLE_ADULT_CAPTION, StorybookUI.ROLE_STATUS,
		StorybookUI.ROLE_NUMERIC, StorybookUI.ROLE_DECORATIVE_GLYPH]
	_check(StorybookUI.TYPOGRAPHY_ROLES.size() == roles.size()
		and storybook_source.contains("TYPOGRAPHY_FONT_AUTHORITY")
		and storybook_source.contains("TYPOGRAPHY_FALLBACK_AUTHORITY"),
		"typography authority and eight named roles are explicit")
	for role: StringName in roles:
		var token: Dictionary = StorybookUI.typography_role(role)
		_check(int(token.get("font_size", 0)) > 0
			and token.has("outline_color") and token.has("outline_size")
			and token.has("focus_color") and token.has("pressed_color")
			and token.has("hover_pressed_color") and token.has("disabled_color")
			and token.has("wrap_mode") and token.has("max_lines")
			and token.has("line_spacing") and token.has("font_authority")
			and token.has("fallback_authority"),
			"typography role token is complete: %s" % String(role))
		# typography_role() must return a defensive copy. Mutating one caller's
		# token may never erase a field from the canonical role or another caller.
		var mutated: Dictionary = StorybookUI.typography_role(role)
		mutated.erase("hover_pressed_color")
		var fresh: Dictionary = StorybookUI.typography_role(role)
		_check(not mutated.has("hover_pressed_color")
			and fresh.has("hover_pressed_color")
			and StorybookUI.TYPOGRAPHY_ROLES[role].has("hover_pressed_color"),
			"typography role mutation stays isolated: %s" % String(role))

	var picture := Button.new()
	StorybookUI.style_picture_button(picture)
	_check(picture.has_theme_color_override("font_color")
		and picture.has_theme_color_override("font_hover_color")
		and picture.has_theme_color_override("font_pressed_color")
		and picture.has_theme_color_override("font_hover_pressed_color")
		and picture.has_theme_color_override("font_focus_color")
		and picture.has_theme_color_override("font_disabled_color")
		and picture.has_theme_stylebox_override("normal")
		and picture.has_theme_stylebox_override("hover")
		and picture.has_theme_stylebox_override("pressed")
		and picture.has_theme_stylebox_override("hover_pressed")
		and picture.has_theme_stylebox_override("focus")
		and picture.has_theme_stylebox_override("disabled")
		and picture.get_theme_font_size("font_size") >= 28
		and picture.get_theme_constant("outline_size") > 0
		and picture.get_theme_stylebox("normal") != null
		and picture.get_theme_stylebox("focus") != null
		and picture.get_theme_stylebox("disabled") != null,
		"picture button has child-size typography, outline, focus, and disabled surfaces")
	_check(picture.has_theme_color_override("font_hover_color")
		and picture.has_theme_color_override("font_focus_color")
		and picture.has_theme_color_override("font_pressed_color")
		and picture.has_theme_color_override("font_hover_pressed_color")
		and picture.has_theme_color_override("font_disabled_color")
		and picture.has_theme_color_override("font_color")
		and picture.get_theme_color("font_hover_color") == StorybookUI.PURPLE_DEEP
		and picture.get_theme_color("font_focus_color") == StorybookUI.PURPLE_DEEP
		and picture.get_theme_color("font_pressed_color") == StorybookUI.PURPLE_DEEP
		and picture.get_theme_color("font_hover_pressed_color") == StorybookUI.PURPLE_DEEP
		and picture.get_theme_color("font_disabled_color") == Color(0.82, 0.84, 0.9),
		"picture button covers hover, focus, pressed, and disabled text colors")
	_check(picture.has_theme_stylebox_override("normal")
		and picture.has_theme_stylebox_override("hover")
		and picture.has_theme_stylebox_override("pressed")
		and picture.has_theme_stylebox_override("hover_pressed")
		and picture.has_theme_stylebox_override("focus")
		and picture.has_theme_stylebox_override("disabled"),
		"picture button owns all six state styleboxes locally")
	var semantic := Button.new()
	StorybookUI.style_button(semantic)
	_check(semantic.has_theme_color_override("font_color")
		and semantic.has_theme_color_override("font_hover_color")
		and semantic.has_theme_color_override("font_pressed_color")
		and semantic.has_theme_color_override("font_hover_pressed_color")
		and semantic.has_theme_color_override("font_focus_color")
		and semantic.has_theme_color_override("font_disabled_color")
		and semantic.has_theme_stylebox_override("normal")
		and semantic.has_theme_stylebox_override("hover")
		and semantic.has_theme_stylebox_override("pressed")
		and semantic.has_theme_stylebox_override("hover_pressed")
		and semantic.has_theme_stylebox_override("focus")
		and semantic.has_theme_stylebox_override("disabled"),
		"text button owns all six state colors and styleboxes locally")
	semantic.free()
	_check(String(picture.get_meta("typography_role", ""))
		== String(StorybookUI.ROLE_CHILD_CONTROL)
		and String(picture.get_meta("typography_font_authority", ""))
		== StorybookUI.TYPOGRAPHY_FONT_AUTHORITY,
		"picture button records its role and font authority")
	picture.free()

	var label := Label.new()
	StorybookUI.style_label(label, 22, StorybookUI.INK_SOFT, 3,
		StorybookUI.ROLE_ADULT_CAPTION)
	_check(label.get_theme_font_size("font_size") == 22
		and label.get_theme_constant("outline_size") == 3
		and label.autowrap_mode == TextServer.AUTOWRAP_WORD_SMART
		and label.max_lines_visible == 3,
		"label helper delegates role wrap and bounded caption typography")
	label.free()

func _check_type_c_layout_contract() -> void:
	const CHILD_FLOOR := 28
	_check(int(StorybookUI.TYPOGRAPHY_ROLES[StorybookUI.ROLE_CHILD_CONTROL]["font_size"])
		>= CHILD_FLOOR
		and int(StorybookUI.TYPOGRAPHY_ROLES[StorybookUI.ROLE_STATUS]["font_size"])
		>= CHILD_FLOOR,
		"child control and status roles keep the 28px minimum")
	# These are source-level guards for the bounded TYPE-C batch. They keep a
	# future edit from silently restoring the audited sub-floor call sites while
	# leaving decorative glyphs and unrelated legacy surfaces out of scope.
	var child_specs: Array[Dictionary] = [
		{"path": "res://scripts/craft_studio.gd",
			"markers": ["style_button(button, \"locked\" if locked else \"secondary\", 24, 28)",
				"style_label(m.craft_status, 21", "known sub-floor child surface"]},
		{"path": "res://scripts/wardrobe_ui.gd",
			"markers": ["ROLE_CHILD_CONTROL, 28)", "b.alignment = HORIZONTAL_ALIGNMENT_RIGHT",
				"bt.alignment = HORIZONTAL_ALIGNMENT_RIGHT"]},
		{"path": "res://scripts/wardrobe_ui.gd",
			"markers": ["font_size\", 20 if earned else 15", "reserves only 72px"]},
		{"path": "res://scripts/collection_system.gd",
			"markers": ["habitat, 28", "ROLE_STATUS", "habitat.max_lines_visible = 2"]},
		{"path": "res://scripts/companion.gd",
			"markers": ["style_button(card, \"selected\" if id == m.companion_pick_id else \"secondary\", 24, 24)",
				"style_label(nm, 26", "style_label(atk, 24", "style_label(asis, 27"]},
		{"path": "res://scripts/games/dance_engine.gd",
			"markers": ["magic_label, 28", "ROLE_STATUS", "magic_label.max_lines_visible = 1"]},
		{"path": "res://scripts/main.gd",
			"markers": ["hint, 24", "hint.mouse_filter = Control.MOUSE_FILTER_IGNORE"]},
	]
	var forbidden_child_sizes: Array[Dictionary] = [
		{"path": "res://scripts/craft_studio.gd", "text": "m.craft_status, 30"},
		{"path": "res://scripts/craft_studio.gd", "text": "else \"secondary\", 30"},
		# The conditional 20/15 sticker-label sizes above are a deliberate,
		# audited exception. Reject only an unconditional sub-floor override.
		{"path": "res://scripts/wardrobe_ui.gd", "text": "font_size\", 20)"},
		{"path": "res://scripts/wardrobe_ui.gd", "text": "font_size\", 15)"},
		{"path": "res://scripts/collection_system.gd", "text": "habitat, 22"},
		{"path": "res://scripts/companion.gd", "text": "card, \"selected\" if id == m.companion_pick_id else \"secondary\", 30"},
		{"path": "res://scripts/companion.gd", "text": "style_label(atk, 28"},
		{"path": "res://scripts/companion.gd", "text": "style_label(nm, 30"},
		{"path": "res://scripts/companion.gd", "text": "style_label(asis, 30"},
		{"path": "res://scripts/games/dance_engine.gd", "text": "magic_label, 24"},
		{"path": "res://scripts/main.gd", "text": "style_hud_label(hint, 28"},
	]
	for spec: Dictionary in child_specs:
		var source: String = FileAccess.get_file_as_string(String(spec["path"]))
		for marker: String in spec["markers"]:
			_check(source.contains(marker), "TYPE-C child layout contract: %s has %s" % [String(spec["path"]), marker])
	for spec: Dictionary in forbidden_child_sizes:
		var source: String = FileAccess.get_file_as_string(String(spec["path"]))
		_check(not source.contains(String(spec["text"])), "TYPE-C rejects sub-floor child call: %s" % String(spec["text"]))
	var adult_specs: Array[Dictionary] = [
		{"path": "res://scripts/intro_overlay.gd", "markers": [
			"ROLE_ADULT_CAPTION", "adult_caption_voice_picture_redundant",
			"m.intro_text.max_lines_visible = 3"]},
		{"path": "res://scripts/start_menu.gd", "markers": [
			"ROLE_STATUS", "This warning protects the child's saved progress",
			"note.max_lines_visible = 3"]},
	]
	for spec: Dictionary in adult_specs:
		var source: String = FileAccess.get_file_as_string(String(spec["path"]))
		for marker: String in spec["markers"]:
			_check(source.contains(marker), "TYPE-C adult-caption exception is explicit: %s" % marker)
		if String(spec["path"]) == "res://scripts/start_menu.gd":
			_check(not source.contains("adult_caption_adult_only_save_safety"),
				"save warning is not misclassified as adult caption")

func _init() -> void:
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	_check_storybook_coverage()
	_check_typography_coverage()
	_check_type_c_layout_contract()

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
	main.game = "level2"
	main._pause_ref()._sync_labels()
	_check(leave != null and leave.text.contains("REEF"),
		"bare Sky Lagoon Pause fallback names its Reef destination")
	main.mg_kind = "snowman"
	main._pause_ref()._sync_labels()
	_check(leave != null and leave.text.contains("BACK"),
		"Sky Lagoon local activity Pause closes locally before leaving")
	main.mg_kind = ""
	main.game = ""
	main._pause_ref()._sync_labels()
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
	var original_skin: String = main.skin_id
	var first_skin := "classic" if original_skin != "classic" else "huluu"
	var first_button := _find(main.wardrobe_layer,
		"WardrobeLook_" + first_skin) as Button
	var preview := main.wd.get("preview") as TextureRect
	var particle_class := "CPU" + "Particles" + str(3) + "D"
	var particle_baseline := _world_particle_count(main, particle_class)
	if first_button != null:
		first_button.pressed.emit()
	var first_burst := _find(main.wardrobe_layer,
		"WardrobePreviewFeedbackBurst") as Control
	var first_burst_ref: WeakRef = weakref(first_burst)
	var first_tween := main.wd.get("feedback_tween") as Tween
	var expected_preview: String = String(main._skin_def(first_skin)["preview"])
	_check(first_button != null and main.skin_id == first_skin
		and preview != null and preview.texture != null
		and preview.texture.resource_path == expected_preview
		and bool(first_button.get_meta("selected", false))
		and String(main.player.verb) == "twirl",
		"real look pick refreshes the preview, selection, skin, and twirl")
	_check(_wardrobe_feedback_is_visible(main.wardrobe_layer, preview),
		"look pick shows one 14-element burst centred on the preview")
	_check(_world_particle_count(main, particle_class) == particle_baseline,
		"look pick adds no off-overlay particle request")
	var second_skin := "huluu" if first_skin == "classic" else "classic"
	var second_button := _find(main.wardrobe_layer,
		"WardrobeLook_" + second_skin) as Button
	if second_button != null:
		second_button.pressed.emit()
	var active_burst := _find(main.wardrobe_layer,
		"WardrobePreviewFeedbackBurst") as Control
	var active_burst_ref: WeakRef = weakref(active_burst)
	var active_tween := main.wd.get("feedback_tween") as Tween
	_check(second_button != null and main.skin_id == second_skin
		and _wardrobe_feedback_is_visible(main.wardrobe_layer, preview)
		and (first_tween == null or not first_tween.is_valid()
			or not first_tween.is_running()),
		"rapid look pick replaces the prior burst without overdraw growth")
	var wardrobe_ref: WeakRef = weakref(main.wardrobe_layer)
	var feedback_layer_ref: WeakRef = weakref(
		_find(main.wardrobe_layer, "WardrobeFeedbackLayer"))
	main._close_wardrobe()
	await process_frame
	await process_frame
	_check(main.wardrobe_layer == null and wardrobe_ref.get_ref() == null
		and feedback_layer_ref.get_ref() == null
		and first_burst_ref.get_ref() == null
		and active_burst_ref.get_ref() == null
		and (active_tween == null or not active_tween.is_valid()
			or not active_tween.is_running()),
		"wardrobe close frees feedback nodes and stops its tween")
	main.skin_id = original_skin
	main._apply_skin()
	main._open_wardrobe()
	await process_frame
	var fresh_feedback := _find(main.wardrobe_layer,
		"WardrobeFeedbackLayer") as Control
	_check(fresh_feedback != null and fresh_feedback.get_child_count() == 0
		and not main.wd.has("feedback_tween"),
		"wardrobe re-entry starts with a clean feedback layer")
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
