class_name PauseMenu
extends RefCounted
# Child-first pause and universal neutral-exit sheet. All mutable state stays
# on main (m.*); this class receives main by reference and owns only logic.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_pause() -> void:
	m.pause_layer = CanvasLayer.new()
	m.pause_layer.layer = 12
	m.pause_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.pause_layer)
	var gear := Button.new()
	gear.name = "PauseCornerButton"
	StorybookUI.style_icon_button(gear, "Ⅱ", "secondary", Vector2(128, 128), "Pause")
	gear.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	gear.position = Vector2(-146, 18)
	gear.pressed.connect(toggle_pause)
	m.pause_layer.add_child(gear)
	m.pause_layer.set_meta("corner_button", gear)

	# Full-screen root lets the dim and shell scale together while main keeps
	# its historical pause_panel reference and probe surface.
	m.pause_panel = Control.new()
	m.pause_panel.name = "PauseOverlay"
	m.pause_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.pause_panel.visible = false
	m.pause_layer.add_child(m.pause_panel)
	var dim := StorybookUI.add_dim(m.pause_panel)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	var shell := StorybookUI.add_panel(m.pause_panel, Rect2(290, 25, 700, 670), StorybookUI.INK_SOFT, Color(0.86, 0.98, 0.98, 0.99), 62)
	shell.name = "PauseShell"
	var crest := Label.new()
	crest.text = "Ⅱ"
	crest.position = Vector2(570, 38)
	crest.size = Vector2(140, 62)
	crest.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	crest.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_label(crest, 46, StorybookUI.INK)
	m.pause_panel.add_child(crest)

	m.fps_lbl = Label.new()
	StorybookUI.style_label(m.fps_lbl, 18, Color(0.74, 0.82, 0.94), 2)
	m.fps_lbl.position = Vector2(1030, 686)
	m.pause_panel.add_child(m.fps_lbl)
	var resume := _pause_btn("▶   KEEP SWIMMING", Rect2(350, 105, 580, 140), "primary")
	resume.name = "PauseResumeButton"
	resume.pressed.connect(toggle_pause)
	m.pause_resume_btn = resume

	var sticker_btn := _pause_btn("★   STICKERS", Rect2(350, 265, 280, 132), "secondary")
	sticker_btn.name = "PauseStickerButton"
	sticker_btn.pressed.connect(func():
		toggle_pause()
		m._open_stickers())
	m.quality_btn = _pause_btn("✦   SPARKLY", Rect2(650, 265, 280, 132), "secondary")
	m.quality_btn.name = "PauseQualityButton"
	m.quality_btn.pressed.connect(func():
		m._apply_quality("speedy" if m.quality == "sparkly" else "sparkly")
		_sync_labels()
		m._write_save())
	m.music_btn = _pause_btn("♫   MUSIC ON", Rect2(350, 420, 280, 132), "secondary")
	m.music_btn.name = "PauseMusicButton"
	m.music_btn.pressed.connect(func():
		m.music_on = not m.music_on
		m.music.volume_db = -8.0 if m.music_on else -60.0
		_sync_labels()
		m._write_save())
	m.pause_leave_btn = _pause_btn("↩   REEF", Rect2(650, 420, 280, 132), "secondary")
	m.pause_leave_btn.name = "PauseLeaveButton"
	m.pause_leave_btn.set_meta("neutral_exit", true)
	m.pause_leave_btn.visible = false
	m.pause_leave_btn.pressed.connect(_leave_current_activity)

	# Parent/debug affordances deliberately sit outside the child icon grid.
	if m.dev_mode != null:
		var dev_btn := _pause_btn("Parent: Developer Mode", Rect2(500, 586, 280, 66), "secondary")
		dev_btn.name = "PauseDeveloperButton"
		dev_btn.set_meta("parent_only", true)
		dev_btn.pressed.connect(func():
			toggle_pause()
			m.dev_mode.toggle())
	_sync_labels()

func _pause_btn(txt: String, rect: Rect2, kind: String) -> Button:
	var button := Button.new()
	button.text = txt
	button.position = rect.position
	button.custom_minimum_size = rect.size
	button.size = rect.size
	StorybookUI.style_button(button, kind, 30, 34)
	m.pause_panel.add_child(button)
	return button

func _sync_labels() -> void:
	if m.music_btn != null:
		m.music_btn.text = "♫   MUSIC ON" if m.music_on else "♫̸   MUSIC OFF"
		m.music_btn.set_meta("toggle_on", m.music_on)
	if m.quality_btn != null:
		m.quality_btn.text = "✦   SPARKLY" if m.quality == "sparkly" else "≋   SPEEDY"
		m.quality_btn.set_meta("toggle_on", m.quality == "sparkly")

func toggle_pause() -> void:
	var paused: bool = not m.get_tree().paused
	m.get_tree().paused = paused
	m.pause_panel.visible = paused
	# Activity overlays normally cover the corner button. Start/Escape raises
	# the pause sheet above them, while layer 30 still owns transition fades.
	m.pause_layer.layer = 29 if paused else 12
	_sync_labels()
	if m.pause_leave_btn != null:
		m.pause_leave_btn.visible = paused and _has_leave_context()
	if paused and m.pause_resume_btn != null:
		m.pause_resume_btn.grab_focus()
	elif not paused:
		if m.touch_ui != null and m.touch_ui.has_method("_clear_touch_state"):
			m.touch_ui._clear_touch_state()
		if m.game == "shop":
			# A/Enter may be the button that resumed the menu. Require a release
			# before it can become a purchase confirmation near the counter.
			m.g["shop_wait_release"] = true
		elif m.game == "fairyshoot":
			m.g["fairy_wait_release"] = true
		var focus_owner := m.get_viewport().gui_get_focus_owner()
		if focus_owner != null:
			focus_owner.release_focus()

func _has_leave_context() -> bool:
	return m.mg_kind != "" or m.game != "" or m.wardrobe_layer != null or m.craft_layer != null or m.stickers_layer != null or m.collection_layer != null or m.companion_layer != null

func _leave_current_activity() -> void:
	# This is a voluntary, neutral exit -- never a loss and never a free win.
	m.get_tree().paused = false
	m.pause_panel.visible = false
	m.pause_layer.layer = 12
	if m.stickers_layer != null:
		m._close_stickers()
		return
	if m.collection_layer != null:
		m._collection_ref().close_book()
		return
	if m.companion_layer != null:
		m._companion_ref().close_picker()
		return
	if m.mg_kind != "":
		m._mg2d_close()
		return
	if m.wardrobe_layer != null:
		m._close_wardrobe()
		return
	if m.craft_layer != null:
		m._close_craft()
		return
	if m.game == "level2":
		m._exit_level2()
		return
	if m.game == "galaxy" and m.galaxy_game != null:
		(m.galaxy_game as GalaxyLevel)._teardown(false)
		return
	if m.game == "ember" and m.ember_game != null:
		(m.ember_game as EmberFortressLevel)._teardown(false)
		return
	if m.game == "kart" and m.kart_game != null:
		m.kart_game.call("_quit_race")
		return
	if m.game == "combat" and m.combat_game != null:
		m.combat_game.cancel()
		return
	if m.game == "stuffie" and m.stuffie_game != null:
		m.stuffie_game.cancel()
		return
	if (m.game == "dungeon" or m.game == "emberdun") and m.dungeon_game != null:
		m.dungeon_game._leave_early()
		return
	if m.game == "":
		return
	var leaving_game: String = m.game
	var friend_state: Dictionary = m.g.get("fr", {})
	var leaving_name: String = String(friend_state.get("fname", ""))
	m._leave_arena()
	# Back to free swim at return_pos: shed any banking/pitch tilt frozen by
	# the arena so she does not reappear mid-lean in the reef.
	m.player.rotation.x = 0.0
	m.player.rotation.z = 0.0
	if not friend_state.is_empty():
		friend_state["cool"] = 8.0
	if leaving_game == "fairyshoot":
		m._apply_skin()
	if leaving_name == "Pearl Shop":
		m.shop_cool = 16.0
	elif leaving_name == "Secret Cave":
		m.treasure_cool = 14.0
	elif leaving_name == "Penguin Slide":
		m.slide_cool = 14.0
	elif leaving_name == "Toy Castle":
		m.brawl_cool = 14.0
	m._clear_game()
	m._write_save()
	if leaving_game == "fairyshoot" and m.fairy_from_galaxy:
		m.fairy_from_galaxy = false
		m.call_deferred("_start_galaxy")
	elif leaving_game == "fairyshoot" or leaving_name == "Rainbow Slide":
		m.call_deferred("_enter_level2", m.l2_open)
	else:
		m.show_msg("Roshan", "Back to the reef! Pick anything you want to play.")
