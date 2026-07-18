class_name PauseMenu
extends RefCounted
# Mechanical extraction of the pause menu overlay from main.gd. All state
# (pause_layer, pause_panel, the button refs) stays on main (m.*); this
# class receives main by reference and owns only the logic.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_pause() -> void:
	m.pause_layer = CanvasLayer.new()
	m.pause_layer.layer = 12
	m.pause_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.pause_layer)
	var gear := Button.new()
	gear.text = "| |"
	gear.add_theme_font_size_override("font_size", 26)
	gear.custom_minimum_size = Vector2(76, 76)
	var gsb := StyleBoxFlat.new()
	gsb.bg_color = Color(0.1, 0.15, 0.3, 0.55)
	gsb.set_corner_radius_all(38)
	gear.add_theme_stylebox_override("normal", gsb)
	gear.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	gear.position = Vector2(-96, 18)
	gear.pressed.connect(toggle_pause)
	m.pause_layer.add_child(gear)
	m.pause_panel = Panel.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.07, 0.1, 0.24, 0.93)
	psb.border_color = Color(0.48, 0.86, 0.9, 0.9)
	psb.set_border_width_all(3)
	psb.set_corner_radius_all(8)
	m.pause_panel.add_theme_stylebox_override("panel", psb)
	m.pause_panel.custom_minimum_size = Vector2(500, 680)
	m.pause_panel.set_anchors_preset(Control.PRESET_CENTER)
	m.pause_panel.position = Vector2(-250, -340)
	m.pause_panel.size = Vector2(500, 680)
	m.pause_panel.visible = false
	m.pause_layer.add_child(m.pause_panel)
	var vb := VBoxContainer.new()
	vb.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vb.offset_left = 28
	vb.offset_right = -28
	vb.offset_top = 20
	vb.offset_bottom = -20
	vb.add_theme_constant_override("separation", 8)
	m.pause_panel.add_child(vb)
	m.fps_lbl = Label.new()
	m.fps_lbl.add_theme_font_size_override("font_size", 20)
	m.fps_lbl.add_theme_color_override("font_color", Color(0.7, 0.85, 1.0))
	m.fps_lbl.position = Vector2(16, 650)
	m.pause_panel.add_child(m.fps_lbl)
	var resume := _pause_btn(vb, "Keep Swimming!")
	m.pause_leave_btn = _pause_btn(vb, "🏠 Leave Activity")
	m.pause_leave_btn.visible = false
	m.pause_leave_btn.pressed.connect(_leave_current_activity)
	var stick_btn := _pause_btn(vb, "⭐ Sticker Book")
	stick_btn.pressed.connect(func():
		toggle_pause()
		m._open_stickers())
	resume.pressed.connect(toggle_pause)
	m.pause_resume_btn = resume
	m.quality_btn = _pause_btn(vb, "Graphics: Sparkly")
	m.quality_btn.pressed.connect(func():
		m._apply_quality("speedy" if m.quality == "sparkly" else "sparkly")
		m._write_save())
	m.music_btn = _pause_btn(vb, "Music: On")
	m.music_btn.pressed.connect(func():
		m.music_on = not m.music_on
		m.music.volume_db = -8.0 if m.music_on else -60.0
		m.music_btn.text = "Music: On" if m.music_on else "Music: Off"
		m._write_save())
	if m.dev_mode != null:
		var dev_btn := _pause_btn(vb, "Developer Mode")
		dev_btn.pressed.connect(func():
			toggle_pause()
			m.dev_mode.toggle())

func _pause_btn(vb: VBoxContainer, txt: String) -> Button:
	var b := Button.new()
	b.text = txt
	b.add_theme_font_size_override("font_size", 30)
	b.custom_minimum_size = Vector2(0, 96)
	vb.add_child(b)
	return b

func toggle_pause() -> void:
	var p: bool = not m.get_tree().paused
	m.get_tree().paused = p
	m.pause_panel.visible = p
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
	if m.game == "kart" and m.kart_game != null:
		m.kart_game.call("_quit_race")
		return
	if m.game == "combat" and m.combat_game != null:
		m.combat_game.cancel()
		return
	if m.game == "stuffie" and m.stuffie_game != null:
		m.stuffie_game.cancel()
		return
	if m.game == "dungeon" and m.dungeon_game != null:
		m.dungeon_game._leave_early()
		return
	if m.game == "":
		return
	var leaving_game: String = m.game
	var fr: Dictionary = m.g.get("fr", {})
	var leaving_name: String = String(fr.get("fname", ""))
	m._leave_arena()
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
	m._clear_game()
	m._write_save()
	if leaving_game == "fairyshoot" and m.fairy_from_galaxy:
		m.fairy_from_galaxy = false
		m.call_deferred("_start_galaxy")
	elif leaving_game == "fairyshoot" or leaving_name == "Rainbow Slide":
		m.call_deferred("_enter_level2", m.l2_open)
	else:
		m.show_msg("Roshan", "Back to the reef! Pick anything you want to play.")
