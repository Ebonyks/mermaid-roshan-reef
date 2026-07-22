extends SceneTree
# Deterministic UI-contract probe for the Codex handoff gold slice
# (gen2/UI_PROTOTYPE_REVISIONS_2026-07-19.md: exploration HUD -> pause -> resume).
# Geometry/state checks only — no rendering needed. Run with `-- --touch`.
#   * pause button: >=110 px visual circle inside a >=128 px hit envelope, top-right
#   * corner ownership: status tray, objective card and captions stay out of the
#     joystick, action-bubble and pause corner zones
#   * status tray is icons/pips/digits only — no prose a child would need to read
#   * objective card is picture-first (pictogram present, text never required)
#   * pause overlay: dominant Resume >=300x140 that takes first focus; icon
#     tiles >=150x132 with >=24 px separation; cool full-screen dim
#   * resume: unpauses, clears touch state, and the pause round-trip wins nothing

var fails := 0

func _bad(msg: String) -> void:
	fails += 1
	print("UI FAIL: ", msg)

func _overlaps(r: Rect2, zone: Rect2, what: String, zname: String) -> void:
	if r.intersects(zone):
		_bad("%s enters the %s corner zone (%s vs %s)" % [what, zname, r, zone])

func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(10):
		await process_frame
	var touch: CanvasLayer = main.touch_ui
	if touch == null or not touch.wants_touch():
		print("UI FAIL: touch_ui missing or wants_touch() false — run with -- --touch")
		quit()
		return

	# ---- pause button geometry: 128 hit envelope, 112 visual, top-right
	var gear: Button = main.pause_gear_btn
	if gear == null:
		_bad("pause_gear_btn missing")
	else:
		if gear.size.x < 128.0 or gear.size.y < 128.0:
			_bad("pause hit envelope %s under 128x128" % gear.size)
		var gvis: Control = null
		for c in gear.get_children():
			if c is Panel:
				gvis = c
		if gvis == null or gvis.size.x < 110.0 or gvis.size.y < 110.0:
			_bad("pause visual target under 110x110")
		var gr: Rect2 = gear.get_global_rect()
		if gr.position.x < 1280.0 - 260.0 or gr.position.y > 200.0:
			_bad("pause button not in the top-right corner (%s)" % gr)

	# ---- joystick affordance: visible at rest, >=176 px visual, action bubble >=148
	var base: Panel = touch._base
	if base == null or not base.visible:
		_bad("joystick has no resting affordance (base hidden while idle)")
	elif base.size.x < 176.0:
		_bad("joystick visual %s under the ~180 px contract" % base.size)
	if touch._act_vis == null:
		_bad("action bubble missing under --touch")
	elif (touch._act_vis as Panel).size.x < 148.0:
		_bad("action bubble under 148 px")

	# ---- status tray: icons, pips and digits only — no prose
	for t in [String(main.hud_pearls.text), String(main.hud_stars.text)]:
		for k in range(t.length()):
			var code: int = t.unicode_at(k)
			if (code >= 65 and code <= 90) or (code >= 97 and code <= 122):
				_bad("status tray contains prose: '%s'" % t)
				break

	# ---- objective card mechanics: picture-first, pulses in, never text-only
	main._set_objective("probe", null, "⭐")
	await process_frame
	if not (main.obj_card as Panel).visible:
		_bad("objective card did not appear")
	if not ((main.obj_icon_lbl as Label).visible and String((main.obj_icon_lbl as Label).text) != ""):
		_bad("objective card shows no pictogram")
	main._set_objective("", null, "")
	# and the live wayfinder path: whenever the card is up it must carry a picture
	main._wayfind_t = 0.0
	await process_frame
	await process_frame
	if (main.obj_card as Panel).visible:
		var has_tex: bool = (main.obj_icon as TextureRect).visible and (main.obj_icon as TextureRect).texture != null
		var has_emj: bool = (main.obj_icon_lbl as Label).visible and String((main.obj_icon_lbl as Label).text) != ""
		if not has_tex and not has_emj:
			_bad("wayfinder objective card visible without a pictogram")

	# ---- corner ownership: HUD cards stay out of the three touch corners
	var bl: Rect2 = touch.rest_zone()
	var br: Rect2 = touch.action_zone()
	var tr: Rect2 = (gear.get_global_rect().grow(8.0)) if gear != null else Rect2(1080, 0, 200, 200)
	_overlaps((main.hud_tray as Panel).get_global_rect(), bl, "status tray", "joystick")
	_overlaps((main.hud_tray as Panel).get_global_rect(), tr, "status tray", "pause")
	_overlaps((main.obj_card as Panel).get_global_rect(), tr, "objective card", "pause")
	var msg_rect := Rect2((main.hud_msg as Label).position, (main.hud_msg as Label).size)
	_overlaps(msg_rect, bl, "caption line", "joystick")
	_overlaps(msg_rect, br, "caption line", "action")

	# ---- pause overlay: dim, dominant resume, first focus, tile grid
	var pearls_before: int = main.pearl_count
	var trophies_before: int = main.trophies
	main.toggle_pause()
	await process_frame
	await process_frame
	if not main.get_tree().paused:
		_bad("toggle_pause did not pause the tree")
	if main.pause_dim == null or not (main.pause_dim as ColorRect).visible:
		_bad("pause dim not shown")
	var resume: Button = main.pause_resume_btn
	if resume == null or not resume.visible:
		_bad("resume button missing while paused")
	else:
		if resume.custom_minimum_size.x < 300.0 or resume.custom_minimum_size.y < 140.0:
			_bad("resume under the 300x140 contract (%s)" % resume.custom_minimum_size)
		if main.get_viewport().gui_get_focus_owner() != resume:
			_bad("first focus is not the resume button")
	var grid: GridContainer = main.pause_grid
	if grid == null:
		_bad("pause tile grid missing")
	else:
		if grid.get_theme_constant("h_separation") < 24 or grid.get_theme_constant("v_separation") < 24:
			_bad("pause tiles closer than 24 px")
		var shown := 0
		for c in grid.get_children():
			var b := c as Button
			if b == null or not b.visible:
				continue
			shown += 1
			var w: float = maxf(b.size.x, b.custom_minimum_size.x)
			var h: float = maxf(b.size.y, b.custom_minimum_size.y)
			if w < 150.0 or h < 132.0:
				_bad("pause tile '%s' under 150x132 (%0.0f x %0.0f)" % [b.text.replace("\n", " "), w, h])
		if shown < 3:
			_bad("expected at least 3 pause tiles, saw %d" % shown)
	if main.pause_leave_btn != null and (main.pause_leave_btn as Button).visible:
		_bad("leave-activity tile visible in free swim (no activity context)")

	# ---- resume: unpause, touch state cleared, nothing won or lost
	main.toggle_pause()
	await process_frame
	if main.get_tree().paused:
		_bad("resume did not unpause")
	if (main.pause_dim as ColorRect).visible:
		_bad("pause dim stayed up after resume")
	if touch.stick_vec != Vector2.ZERO or touch.action_down:
		_bad("touch state not cleared on resume")
	if main.pearl_count != pearls_before or main.trophies != trophies_before:
		_bad("pause round-trip changed progress (pearls %d->%d trophies %d->%d)" % [pearls_before, main.pearl_count, trophies_before, main.trophies])

	if fails == 0:
		print("UI ALL OK — gold-slice contracts hold")
	else:
		print("UI RESULT: %d contract check(s) failed" % fails)
	quit()
