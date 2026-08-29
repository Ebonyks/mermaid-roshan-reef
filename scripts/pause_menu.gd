class_name PauseMenu
extends RefCounted
# Child-first pause and universal neutral-exit sheet. All mutable state stays
# on main (m.*); this class receives main by reference and owns only logic.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_pause() -> void:
	# Codex UI handoff 2026-07-19 pause contracts: full-screen cool dim, one
	# unmistakably dominant Resume, secondary actions as an icon-tile grid
	# (>=150x132, 24 px apart), toggles that change silhouette (never color
	# alone), a neutral doorway exit, and dev/FPS kept out of the child menu.
	# The only persistent gameplay control: one upper-left button. It is Back
	# whenever another activity/room is stacked over Sky Lagoon, and becomes
	# Menu only at the Lagoon promenade root. Layer 29 sits over ordinary game
	# surfaces but below the transition fade at 30.
	m.navigation_layer = CanvasLayer.new()
	m.navigation_layer.name = "GlobalNavigationLayer"
	m.navigation_layer.layer = 29
	m.navigation_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.navigation_layer)
	var navigation := Button.new()
	navigation.name = "GlobalNavigationButton"
	StorybookUI.style_icon_button(
		navigation, "↩", "secondary", Vector2(112.0, 112.0), "Back")
	navigation.position = Vector2(18.0, 18.0)
	navigation.button_down.connect(global_navigation_pressed)
	navigation.set_meta("global_navigation_owner", true)
	m.navigation_layer.add_child(navigation)
	m.global_navigation_button = navigation
	# Compatibility for systems that only need to locate the shipped corner
	# control. It no longer means Pause and is never placed in the top-right.
	m.pause_gear_btn = navigation

	m.pause_layer = CanvasLayer.new()
	m.pause_layer.layer = 12
	m.pause_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(m.pause_layer)
	m.pause_dim = ColorRect.new()
	m.pause_dim.color = Color(0.03, 0.06, 0.18, 0.55)
	m.pause_dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.pause_dim.visible = false
	m.pause_layer.add_child(m.pause_dim)
	m.pause_layer.set_meta("corner_button", navigation)

	# Full-screen root lets the dim and shell scale together while main keeps
	# its historical pause_panel reference and probe surface.
	m.pause_panel = Control.new()
	m.pause_panel.name = "PauseOverlay"
	m.pause_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.pause_panel.visible = false
	m.pause_layer.add_child(m.pause_panel)
	var dim := StorybookUI.add_dim(m.pause_panel)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	var shell_rect := Rect2(290, 25, 700, 670)
	var shell := StorybookUI.add_panel(m.pause_panel, shell_rect, StorybookUI.PURPLE, Color(0.90, 0.96, 1.0, 0.99), 62)
	shell.name = "MenuShell"
	StorybookUI.adorn_panel(m.pause_panel, shell_rect, "Menu")

	m.fps_lbl = Label.new()
	StorybookUI.style_label(m.fps_lbl, 18, Color(0.74, 0.82, 0.94), 2)
	m.fps_lbl.position = Vector2(1030, 686)
	m.pause_panel.add_child(m.fps_lbl)
	var resume := _pause_btn("▶   BACK TO PLAY", Rect2(350, 105, 580, 140), "primary")
	resume.name = "PauseResumeButton"
	resume.pressed.connect(toggle_pause)
	m.pause_resume_btn = resume

	var sticker_btn := _pause_btn("★   STICKERS", Rect2(350, 265, 280, 132), "secondary")
	sticker_btn.name = "PauseStickerButton"
	sticker_btn.pressed.connect(func():
		toggle_pause()
		m._open_stickers())
	var critter_btn := _pause_btn("🐟   CRITTERS",
		Rect2(650, 265, 280, 132), "secondary")
	critter_btn.name = "MenuCritterBookButton"
	critter_btn.pressed.connect(func():
		toggle_pause()
		m._collection_ref().open_book())
	var stuffie_btn := _pause_btn("♥   STUFFIE",
		Rect2(350, 420, 280, 132), "secondary")
	stuffie_btn.name = "MenuStuffieButton"
	stuffie_btn.pressed.connect(func():
		toggle_pause()
		if m.companion_id == "":
			m._companion_ref().open_picker()
		else:
			m._companion_ref().open_care_menu())
	m.pause_leave_btn = _pause_btn(leave_label(),
		Rect2(650, 420, 280, 132), "secondary")
	m.pause_leave_btn.name = "PauseLeaveButton"
	m.pause_leave_btn.set_meta("neutral_exit", true)
	m.pause_leave_btn.visible = false
	m.pause_leave_btn.pressed.connect(_leave_current_activity)
	# Point-to-interact is the one child-facing touch vocabulary. The former
	# mode choice advertised an obsolete on-screen movement stick.
	m.touch_mode_btn = null
	m.quality_btn = null
	m.music_btn = null
	m.mic_btn = null
	_sync_labels()
	sync_global_navigation()

func sync_global_navigation() -> void:
	m._navigation_ref().sync_button()

func _is_sky_lagoon_root() -> bool:
	return m._navigation_ref().at_sky_lagoon_root()

func _navigation_locked() -> bool:
	if m.start_menu_active or m.intro_active or m.sleep_layer != null \
			or m.hug_layer != null:
		return true
	return m.fade_rect != null and m.fade_rect.visible \
		and (m.fade_rect.color.a * m.fade_rect.modulate.a > 0.01 \
			or m.fade_rect.mouse_filter == Control.MOUSE_FILTER_STOP)

func global_navigation_pressed() -> void:
	m._navigation_ref().press()

func music_label() -> String:
	# State shown by silhouette, not colour: a note when on, a struck note when
	# off. This stays a function because SaveState.load_save() refreshes the
	# button straight from the loaded save - inlining the string here is what
	# broke every probe on run 684.
	return "♫   MUSIC ON" if m.music_on else "♫̸   MUSIC OFF"

func mic_label() -> String:
	# Same reasoning as music_label(): a function, not an inlined string, so a
	# save load can refresh the button straight from the loaded value.
	if m.mic_permission_denied:
		return "🎤̸   SPELLS OFF"
	return "🎤   SAY SPELLS" if m.mic_on else "🎤̸   SPELLS OFF"

func leave_label() -> String:
	# Name the branch the button will actually execute. Local overlays and the
	# castle class close first; only a bare Sky Lagoon/castle state returns to
	# the Reef.
	var local_level2_activity: bool = m.mg_kind != "" \
		or m.wardrobe_layer != null or m.craft_layer != null \
		or m.castle_logo_layer != null or m.stickers_layer != null \
		or m.collection_layer != null or m.companion_layer != null \
		or m.companion_care_layer != null or m.combat_tutorial_game != null
	if m.game == "level2" and not local_level2_activity:
		return "🌊   REEF"
	return "↩   BACK"

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
		m.music_btn.text = music_label()
		m.music_btn.set_meta("toggle_on", m.music_on)
	if m.quality_btn != null:
		m.quality_btn.text = "✦   SPARKLY" if m.quality == "sparkly" else "≋   SPEEDY"
		m.quality_btn.set_meta("toggle_on", m.quality == "sparkly")
	if m.mic_btn != null:
		m.mic_btn.text = mic_label()
		m.mic_btn.set_meta("toggle_on", m.mic_on and not m.mic_permission_denied)
	if m.pause_leave_btn != null:
		m.pause_leave_btn.text = leave_label()

func toggle_pause() -> void:
	var paused: bool = not m.get_tree().paused
	# The corner gear is wired directly to this controller, so it must own the
	# same cancellation contract as ReefMain.toggle_pause().  Clear the active
	# finger before pausing: in Canvas Sky Lagoon this also drops any walk goal
	# and PLAY/ENTER focus, preventing navigation from resuming behind the sheet.
	if paused and m.touch_ui != null:
		m.touch_ui.cancel_all_touches()
	# Melody receives raw screen/key/pad input before the legacy touch router,
	# so TouchUI cannot neutralize every held source on its own.  Notify the
	# controller on both edges before changing SceneTree pause state; it retains
	# a held-source release latch without turning resume into a score.
	if m.game == "melody":
		(m._game_obj("melody", MelodyGame) as MelodyGame).on_pause_changed(paused)
	if m.has_method("_slide_canvas_fish_route_active") \
			and bool(m.call("_slide_canvas_fish_route_active")):
		(m._game_obj("race", SlideRaceGame) as SlideRaceGame).on_pause_changed(paused)
	m.get_tree().paused = paused
	m.pause_panel.visible = paused
	# Activity overlays normally cover the corner button. Start/Escape raises
	# the pause sheet above them, while layer 30 still owns transition fades.
	if paused:
		m.pause_layer.layer = 28
	else:
		m._sync_pause_surface_layer()
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
	return m.mg_kind != "" or m.game != "" or m.wardrobe_layer != null \
		or m.craft_layer != null or m.castle_logo_layer != null \
		or m.stickers_layer != null or m.collection_layer != null \
		or m.companion_layer != null or m.companion_care_layer != null \
		or m.mic_teach_layer != null \
		or (m.dance_engine != null and is_instance_valid(m.dance_engine) \
			and (m.dance_engine as DanceEngine).active)

func _leave_current_activity() -> void:
	# This is a voluntary, neutral exit -- never a loss and never a free win.
	m.get_tree().paused = false
	m.pause_panel.visible = false
	m._sync_pause_surface_layer()
	if m.dance_engine != null and is_instance_valid(m.dance_engine) \
			and (m.dance_engine as DanceEngine).active:
		(m.dance_engine as DanceEngine).close_demo()
		return
	if m._attack_customizer != null \
			and is_instance_valid(m._attack_customizer) \
			and m._attack_customizer.is_open:
		m._attack_customizer.close()
		return
	if m._day_one_art_studio != null \
			and is_instance_valid(m._day_one_art_studio):
		m._close_day_one_art_studio()
		return
	if m._castle_career_routes != null \
			and m._castle_career_routes.opera_venue != null \
			and is_instance_valid(m._castle_career_routes.opera_venue) \
			and m._castle_career_routes.opera_venue.is_open():
		m._castle_career_routes.close_opera_venue()
		return
	if m._castle_rooms_25d != null \
			and m._castle_rooms_25d.kitchen_menu_layer != null:
		m._castle_rooms_25d._close_kitchen_menu()
		return
	if m.mic_teach_layer != null:
		m._mic_ref().close_teach()
		return
	if m.stickers_layer != null:
		m._close_stickers()
		return
	if m.collection_layer != null:
		m._collection_ref().close_book()
		return
	if m.companion_layer != null:
		m._companion_ref().close_picker()
		return
	if m.companion_care_layer != null:
		m._companion_ref().close_care_menu()
		return
	if m.mg_kind != "":
		m._mg2d_close()
		return
	if m.wardrobe_layer != null:
		m._close_wardrobe()
		return
	if m.castle_logo_layer != null:
		m._close_castle_logo()
		return
	if m.craft_layer != null:
		m._close_craft()
		return
	if m.combat_tutorial_game != null:
		# the sparring class is a castle cutaway (m.game stays "level2"):
		# leaving must put the CLASS away first — cancel resumes the hall via
		# its finish callback; the next leave-press then exits the castle.
		# Without this the tutorial haunted the session: ghost finger stuck on
		# screen, its hit engine stealing every ocean tap (alpha audit
		# 2026-08-05).
		m.combat_tutorial_game.cancel()
		return
	# Child activities can suspend the castle room layer while leaving its state
	# alive. They must unwind before the castle itself sees Back.
	if m.game == "kitchen_cooking":
		m._castle_rooms_ref().cancel_kitchen_recipe()
		return
	if m.game == "opera" and m.opera_game != null:
		(m.opera_game as OperaHouse)._leave_early()
		return
	if m.game == "kart" and m.kart_game != null:
		m.kart_game.call("_quit_race")
		return
	if (m.game == "dungeon" or m.game == "emberdun") and m.dungeon_game != null:
		m.dungeon_game._leave_early()
		return
	if m._castle_rooms_25d != null and m._castle_rooms_25d.is_open() \
			and m.castle_room_layer != null and m.castle_room_layer.visible:
		m._castle_rooms_25d._go_back()
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
	if m.game == "combat" and m.combat_game != null:
		m.combat_game.cancel()
		return
	if m.game == "stuffie" and m.stuffie_game != null:
		m.stuffie_game.cancel()
		return
	if m.game == "":
		return
	var leaving_game: String = m.game
	var leaving_slide_canvas: bool = m.has_method("_slide_canvas_fish_route_active") \
		and bool(m.call("_slide_canvas_fish_route_active"))
	var friend_state: Dictionary = m.g.get("fr", {})
	var leaving_name: String = String(friend_state.get("fname", ""))
	m._leave_arena()
	# Back to free swim at return_pos: shed any banking/pitch tilt frozen by
	# a spatial arena so she does not reappear mid-lean in the reef. The opaque
	# fish Canvas never changed that return pose, so preserve it exactly.
	if not leaving_slide_canvas:
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
		m.show_msg("Roshan", "Back to the castle! Pick anything you want to play.")
