class_name PauseMenu
extends RefCounted
# Mechanical extraction of the pause menu overlay from main.gd. All state
# (pause_layer, pause_panel, the button refs) stays on main (m.*); this
# class receives main by reference and owns only the logic.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_pause() -> void:
	# Codex UI handoff 2026-07-19 pause contracts: full-screen cool dim, one
	# unmistakably dominant Resume, secondary actions as an icon-tile grid
	# (>=150x132, 24 px apart), toggles that change silhouette (never color
	# alone), a neutral doorway exit, and dev/FPS kept out of the child menu.
	m.pause_layer = CanvasLayer.new()
	m.pause_layer.layer = 12
	m.pause_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.pause_layer)
	m.pause_dim = ColorRect.new()
	m.pause_dim.color = Color(0.03, 0.06, 0.18, 0.55)
	m.pause_dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.pause_dim.visible = false
	m.pause_layer.add_child(m.pause_dim)
	# 112 px visual pause circle centered in a 128 px hit envelope, inset from
	# the top-right safe edge (frustrated fingers mash here)
	var gear := Button.new()
	gear.flat = true
	gear.focus_mode = Control.FOCUS_NONE   # pad focus stays inside the panel
	gear.custom_minimum_size = Vector2(128, 128)
	var gempty := StyleBoxEmpty.new()
	for st in ["normal", "hover", "pressed", "focus"]:
		gear.add_theme_stylebox_override(st, gempty)
	gear.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	gear.position = Vector2(-148, 12)
	gear.size = Vector2(128, 128)
	gear.pressed.connect(toggle_pause)
	m.pause_layer.add_child(gear)
	m.pause_gear_btn = gear
	var gvis := Panel.new()
	var gsb := StyleBoxFlat.new()
	gsb.bg_color = Color(0.1, 0.15, 0.3, 0.6)
	gsb.border_color = Color(0.5, 0.9, 0.95, 0.9)
	gsb.set_border_width_all(4)
	gsb.set_corner_radius_all(56)
	gvis.add_theme_stylebox_override("panel", gsb)
	gvis.position = Vector2(8, 8)
	gvis.size = Vector2(112, 112)
	gvis.mouse_filter = Control.MOUSE_FILTER_IGNORE
	gear.add_child(gvis)
	var glbl := Label.new()
	glbl.text = "| |"
	glbl.add_theme_font_size_override("font_size", 34)
	glbl.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	glbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	glbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	glbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	gvis.add_child(glbl)
	m.pause_panel = Panel.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.07, 0.1, 0.24, 0.93)
	psb.border_color = Color(0.48, 0.86, 0.9, 0.9)
	psb.set_border_width_all(3)
	psb.set_corner_radius_all(24)
	m.pause_panel.add_theme_stylebox_override("panel", psb)
	m.pause_panel.custom_minimum_size = Vector2(880, 600)
	m.pause_panel.set_anchors_preset(Control.PRESET_CENTER)
	m.pause_panel.position = Vector2(-440, -300)
	m.pause_panel.size = Vector2(880, 600)
	m.pause_panel.visible = false
	m.pause_layer.add_child(m.pause_panel)
	var vb := VBoxContainer.new()
	vb.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vb.offset_left = 28
	vb.offset_right = -28
	vb.offset_top = 22
	vb.offset_bottom = -22
	vb.add_theme_constant_override("separation", 16)
	m.pause_panel.add_child(vb)
	if m.dev_mode != null:
		# dev-mode-only readout, outside the child-facing controls
		m.fps_lbl = Label.new()
		m.fps_lbl.add_theme_font_size_override("font_size", 20)
		m.fps_lbl.add_theme_color_override("font_color", Color(0.7, 0.85, 1.0))
		m.fps_lbl.position = Vector2(16, 570)
		m.pause_panel.add_child(m.fps_lbl)
	var resume := Button.new()
	resume.text = "▶   Keep Swimming!"
	resume.add_theme_font_size_override("font_size", 40)
	resume.custom_minimum_size = Vector2(320, 150)
	resume.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var rsb := StyleBoxFlat.new()
	rsb.bg_color = Color(0.55, 0.92, 0.78)
	rsb.set_corner_radius_all(26)
	var rsb_press: StyleBoxFlat = rsb.duplicate() as StyleBoxFlat
	rsb_press.bg_color = Color(0.42, 0.78, 0.64)
	var rsb_focus: StyleBoxFlat = rsb.duplicate() as StyleBoxFlat
	rsb_focus.border_color = Color(1.0, 0.85, 0.4)
	rsb_focus.set_border_width_all(6)
	resume.add_theme_stylebox_override("normal", rsb)
	resume.add_theme_stylebox_override("hover", rsb)
	resume.add_theme_stylebox_override("pressed", rsb_press)
	resume.add_theme_stylebox_override("focus", rsb_focus)
	for cn in ["font_color", "font_hover_color", "font_pressed_color", "font_focus_color"]:
		resume.add_theme_color_override(cn, Color(0.05, 0.16, 0.2))
	vb.add_child(resume)
	resume.pressed.connect(toggle_pause)
	m.pause_resume_btn = resume
	m.pause_grid = GridContainer.new()
	m.pause_grid.columns = 2
	m.pause_grid.add_theme_constant_override("h_separation", 24)
	m.pause_grid.add_theme_constant_override("v_separation", 24)
	vb.add_child(m.pause_grid)
	var stick_btn := _pause_tile("⭐\nSticker Book")
	stick_btn.pressed.connect(func():
		toggle_pause()
		m._open_stickers())
	m.pause_leave_btn = _pause_tile("🏠\nBack to the Reef")
	m.pause_leave_btn.visible = false
	m.pause_leave_btn.pressed.connect(_leave_current_activity)
	m.music_btn = _pause_tile(music_label())
	m.music_btn.pressed.connect(func():
		m.music_on = not m.music_on
		m.music.volume_db = -8.0 if m.music_on else -60.0
		m.music_btn.text = music_label()
		m._write_save())
	m.quality_btn = _pause_tile("✨\nSparkly")
	m.quality_btn.pressed.connect(func():
		m._apply_quality("speedy" if m.quality == "sparkly" else "sparkly")
		m._write_save())
	if m.dev_mode != null:
		var dev_btn := Button.new()
		dev_btn.text = "Developer Mode"
		dev_btn.add_theme_font_size_override("font_size", 22)
		dev_btn.custom_minimum_size = Vector2(0, 48)
		vb.add_child(dev_btn)
		dev_btn.pressed.connect(func():
			toggle_pause()
			m.dev_mode.toggle())

func music_label() -> String:
	# state shown by silhouette, not color: a note when on, a muted bell when off
	return "🎵\nMusic On" if m.music_on else "🔕\nMusic Off"

func _pause_tile(txt: String) -> Button:
	var b := Button.new()
	b.text = txt
	b.add_theme_font_size_override("font_size", 30)
	b.custom_minimum_size = Vector2(388, 150)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.12, 0.18, 0.38, 0.95)
	sb.border_color = Color(0.48, 0.86, 0.9, 0.7)
	sb.set_border_width_all(3)
	sb.set_corner_radius_all(22)
	var sb_press: StyleBoxFlat = sb.duplicate() as StyleBoxFlat
	sb_press.bg_color = Color(0.18, 0.26, 0.5, 0.95)
	var sb_focus: StyleBoxFlat = sb.duplicate() as StyleBoxFlat
	sb_focus.border_color = Color(1.0, 0.85, 0.4)
	sb_focus.set_border_width_all(6)
	b.add_theme_stylebox_override("normal", sb)
	b.add_theme_stylebox_override("hover", sb)
	b.add_theme_stylebox_override("pressed", sb_press)
	b.add_theme_stylebox_override("focus", sb_focus)
	m.pause_grid.add_child(b)
	return b

func toggle_pause() -> void:
	var p: bool = not m.get_tree().paused
	m.get_tree().paused = p
	m.pause_panel.visible = p
	if m.pause_dim != null:
		m.pause_dim.visible = p
	if m.pause_leave_btn != null:
		m.pause_leave_btn.visible = p and _has_leave_context()
	# gamepad menu navigation: focus the first button so D-pad + A work
	if p and m.pause_resume_btn != null:
		m.pause_resume_btn.grab_focus()
	elif not p:
		if m.touch_ui != null and m.touch_ui.has_method("_clear_touch_state"):
			m.touch_ui._clear_touch_state()
		if m.game == "shop":
			# A/Enter may be the button that resumed the menu. Require a release
			# before it can become a purchase confirmation near the counter.
			m.g["shop_wait_release"] = true
		elif m.game == "fairyshoot":
			m.g["fairy_wait_release"] = true
		var fo := m.get_viewport().gui_get_focus_owner()
		if fo != null:
			fo.release_focus()

func _has_leave_context() -> bool:
	return m.mg_kind != "" or m.game != "" or m.wardrobe_layer != null or m.craft_layer != null

func _leave_current_activity() -> void:
	# This is a voluntary, neutral exit -- never a loss and never a free win.
	m.get_tree().paused = false
	m.pause_panel.visible = false
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
	var fr: Dictionary = m.g.get("fr", {})
	var leaving_name: String = String(fr.get("fname", ""))
	m._leave_arena()
	# back to free swim at return_pos: shed any banking/pitch tilt frozen by
	# the arena so she doesn't reappear mid-lean in the reef
	m.player.rotation.x = 0.0
	m.player.rotation.z = 0.0
	if not fr.is_empty():
		fr["cool"] = 8.0
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
