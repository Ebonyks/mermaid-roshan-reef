class_name CraftStudio
extends RefCounted
# Mechanical extraction of the craft studio overlay from main.gd. All state
# (craft_layer, craft_* colours/controls, custom_fish, custom_friends) stays
# on main (m.*); this class receives main by reference and owns only logic.
# _make_creature_node and the rainbow-paint helpers stay on main - they are
# shared with world build (_spawn_crafted_fish), the Sky Lagoon and probes.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _craft_build_preview() -> void:
	if m.craft_fishbox == null:
		return
	for c in m.craft_fishbox.get_children():
		c.queue_free()
	var ln: Array = m.CREATURE_LAYERS.get(m.craft_kind, m.CREATURE_LAYERS["fish"])
	var acca := 1.0
	var order := [String(ln[1]), String(ln[0]), String(ln[2])]
	var roles := ["body", "accent", "line"]
	var cols := [m.craft_body, Color(m.craft_fins.r, m.craft_fins.g, m.craft_fins.b, acca), Color(1, 1, 1)]
	var rbs := [m.craft_body_rb, m.craft_fins_rb, false]
	for i in range(3):
		var tr := TextureRect.new(); tr.texture = load("res://assets/mg/" + order[i] + ".png")
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE; tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.size = m.craft_fishbox.size; tr.modulate = cols[i]; tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		tr.set_meta("role", roles[i]); m.craft_fishbox.add_child(tr)
		if roles[i] != "line":
			m._layer_fx(tr, roles[i], cols[i], rbs[i], m.craft_kind)

func _open_craft_studio() -> void:
	if m.craft_layer != null:
		return
	m.craft_kind = "fish"
	m.craft_body = Color(0.4, 0.7, 1.0)
	m.craft_fins = Color(1.0, 0.6, 0.2)
	m.craft_body_rb = false
	m.craft_fins_rb = false
	m.craft_c3 = Color(0, 0, 0, 0)
	m.craft_layer = CanvasLayer.new(); m.craft_layer.layer = 18; m.add_child(m.craft_layer)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT); m.craft_layer.add_child(root)
	var vp: Vector2 = m.get_viewport().get_visible_rect().size
	var bg := ColorRect.new(); bg.color = Color(0.10, 0.13, 0.22, 0.95); bg.set_anchors_preset(Control.PRESET_FULL_RECT); root.add_child(bg)
	var stage := Control.new(); stage.size = Vector2(1280, 720)
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	stage.scale = Vector2(sc, sc); stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	root.add_child(stage)
	var title := Label.new(); title.text = "Color your friend!"
	title.add_theme_font_size_override("font_size", 52)
	title.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); title.add_theme_constant_override("outline_size", 10)
	title.position = Vector2(60, 16); stage.add_child(title)
	title.add_to_group("craft_top")   # hidden when the farewell banner appears
	# creature-type buttons — Kitty and Birdie are one-time rainbow-pearl unlocks
	var kinds := [["fish", "Fishy", 0], ["cat", "Kitty", 5], ["bird", "Birdie", 8]]
	for ki in range(kinds.size()):
		var kk: String = String(kinds[ki][0])
		var knm: String = String(kinds[ki][1])
		var kpr: int = int(kinds[ki][2])
		var locked: bool = kpr > 0 and not bool(m.craft_unlocks.get(kk, false))
		var kb := Button.new(); kb.text = knm; kb.add_theme_font_size_override("font_size", 36)
		kb.position = Vector2(760.0 + float(ki) * 165.0, 14.0); kb.custom_minimum_size = Vector2(155, 64)
		var ksb := StyleBoxFlat.new(); ksb.bg_color = Color(0.32, 0.34, 0.48) if locked else Color(0.4, 0.45, 0.7); ksb.set_corner_radius_all(8)
		kb.add_theme_stylebox_override("normal", ksb); kb.add_theme_stylebox_override("hover", ksb); kb.add_theme_stylebox_override("pressed", ksb)
		kb.set_meta("style", ksb)
		if locked:
			kb.modulate = Color(0.78, 0.78, 0.85)
			var tag := Label.new(); tag.text = "%d pearls" % kpr
			tag.add_theme_font_size_override("font_size", 24)
			tag.add_theme_color_override("font_color", Color(1.0, 0.82, 1.0))
			tag.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); tag.add_theme_constant_override("outline_size", 6)
			tag.position = Vector2(kb.position.x + 28.0, 80.0)
			stage.add_child(tag)
			tag.add_to_group("craft_top")
			kb.set_meta("price_tag", tag)
		kb.pressed.connect(func(): _craft_pick_kind(kk, knm, kpr, kb))
		stage.add_child(kb)
		kb.add_to_group("craft_top")
	# pearl purse + feedback line (the normal HUD sits behind this overlay)
	m.craft_pearl_lbl = Label.new(); m.craft_pearl_lbl.text = "Rainbow pearls: %d" % m.pearl_count
	m.craft_pearl_lbl.add_theme_font_size_override("font_size", 28)
	m.craft_pearl_lbl.add_theme_color_override("font_color", Color(1.0, 0.85, 1.0))
	m.craft_pearl_lbl.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); m.craft_pearl_lbl.add_theme_constant_override("outline_size", 8)
	m.craft_pearl_lbl.position = Vector2(64, 86); stage.add_child(m.craft_pearl_lbl)
	m.craft_status = Label.new()
	m.craft_status.add_theme_font_size_override("font_size", 30)
	m.craft_status.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); m.craft_status.add_theme_constant_override("outline_size", 8)
	m.craft_status.position = Vector2(40, 240); m.craft_status.custom_minimum_size = Vector2(370, 200)
	m.craft_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	stage.add_child(m.craft_status)
	m.craft_fishbox = Control.new(); m.craft_fishbox.size = Vector2(400, 400); m.craft_fishbox.position = Vector2(440, 72); stage.add_child(m.craft_fishbox)
	_craft_build_preview()
	var pal := [Color(0.92, 0.26, 0.3), Color(1, 0.6, 0.2), Color(1, 0.85, 0.25), Color(0.35, 0.8, 0.4), Color(0.3, 0.8, 0.9), Color(0.3, 0.55, 1.0), Color(0.6, 0.4, 0.9), Color(0.95, 0.5, 0.8), Color(0.97, 0.96, 0.93)]
	for row in range(3):
		var part: String = ["body", "accent", "third"][row]
		for ci in range(pal.size()):
			var sw := Button.new(); sw.custom_minimum_size = Vector2(84, 84); sw.size = Vector2(84, 84)
			sw.position = Vector2(300.0 + float(ci) * 94.0, 444.0 + float(row) * 92.0)
			var sb := StyleBoxFlat.new(); sb.bg_color = pal[ci]; sb.set_corner_radius_all(20); sb.set_border_width_all(4); sb.border_color = Color(1, 1, 1, 0.7)
			sw.add_theme_stylebox_override("normal", sb); sw.add_theme_stylebox_override("hover", sb); sw.add_theme_stylebox_override("pressed", sb)
			var col: Color = pal[ci]; var pp: String = part
			sw.pressed.connect(func(): _craft_set(pp, col))
			stage.add_child(sw)
		# RAINBOW swatch (body/accent only; the third zone keeps solid colours)
		if row == 2:
			continue
		var rbw := Button.new(); rbw.custom_minimum_size = Vector2(84, 84); rbw.size = Vector2(84, 84)
		rbw.position = Vector2(300.0 - 94.0, 444.0 + float(row) * 92.0)   # BEFORE the solids
		rbw.flat = true
		var rimg := TextureRect.new(); rimg.texture = load("res://assets/mg/rainbow_swatch.png")
		rimg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE; rimg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		rimg.set_anchors_preset(Control.PRESET_FULL_RECT); rimg.mouse_filter = Control.MOUSE_FILTER_IGNORE
		rbw.add_child(rimg)
		var pp2: String = part
		rbw.pressed.connect(func(): _craft_set(pp2, Color(1, 1, 1), true))
		stage.add_child(rbw)
	var done := Button.new(); done.text = "  Done!  "; done.add_theme_font_size_override("font_size", 46)
	done.position = Vector2(1050, 330); done.custom_minimum_size = Vector2(190, 130)
	var dsb := StyleBoxFlat.new(); dsb.bg_color = Color(0.3, 0.8, 0.4); dsb.set_corner_radius_all(8)
	done.add_theme_stylebox_override("normal", dsb); done.add_theme_stylebox_override("hover", dsb); done.add_theme_stylebox_override("pressed", dsb)
	done.pressed.connect(_craft_done); stage.add_child(done)

func _craft_pick_kind(kk: String, knm: String, price: int, kb: Button) -> void:
	if price > 0 and not bool(m.craft_unlocks.get(kk, false)):
		if m.pearl_count < price:
			if m.craft_status != null and is_instance_valid(m.craft_status):
				m.craft_status.text = "%s costs %d rainbow pearls. You have %d - the reef is full of them!" % [knm, price, m.pearl_count]
			if m.chime != null:
				m.chime.pitch_scale = 0.7
				m.chime.play()
			return
		m.pearl_count -= price
		m.craft_unlocks[kk] = true
		m._write_save()
		m._update_hud()
		if m.chime != null:
			m.chime.pitch_scale = 1.5
			m.chime.play()
		kb.modulate = Color(1, 1, 1)
		var sb: StyleBoxFlat = kb.get_meta("style", null)
		if sb != null:
			sb.bg_color = Color(0.4, 0.45, 0.7)
		var tag: Label = kb.get_meta("price_tag", null)
		if tag != null and is_instance_valid(tag):
			tag.queue_free()
		if m.craft_pearl_lbl != null and is_instance_valid(m.craft_pearl_lbl):
			m.craft_pearl_lbl.text = "Rainbow pearls: %d" % m.pearl_count
		if m.craft_status != null and is_instance_valid(m.craft_status):
			m.craft_status.text = "%s unlocked forever! Yay!" % knm
	m.craft_kind = kk
	_craft_build_preview()

func _craft_set(part: String, col: Color, rb: bool = false) -> void:
	if part == "body":
		m.craft_body = col
		m.craft_body_rb = rb
	elif part == "third":
		m.craft_c3 = col
	else:
		m.craft_fins = col
		m.craft_fins_rb = rb
	if m.craft_fishbox != null:
		for c in m.craft_fishbox.get_children():
			if c is TextureRect:
				var role: String = (c as TextureRect).get_meta("role", "")
				if part == "body" and role == "body": (c as TextureRect).modulate = col
				if part == "accent" and role == "accent":
					(c as TextureRect).modulate = Color(col.r, col.g, col.b, 1.0)

func _craft_done() -> void:
	if m.craft_layer == null or bool(m.get_meta("craft_closing", false)):
		return   # reentry guard: double-click / double-A must not craft twice
	m.set_meta("craft_closing", true)
	m.stickers["_c_" + m.craft_kind] = true   # hidden progress toward Little Artist
	if bool(m.stickers.get("_c_fish", false)) and bool(m.stickers.get("_c_cat", false)) and bool(m.stickers.get("_c_bird", false)):
		m.award_sticker("artist")
	var fishy: bool = m.craft_kind == "fish"
	var msgtxt: String
	if fishy:
		m.custom_fish.append([m.craft_body.r, m.craft_body.g, m.craft_body.b, m.craft_fins.r, m.craft_fins.g, m.craft_fins.b, 1 if m.craft_body_rb else 0, 1 if m.craft_fins_rb else 0])
		m._spawn_crafted_fish()   # same spawn path as build/load keeps the counter honest
		msgtxt = "Swim away, little fish! Find me in the ocean!"
	else:
		var c3: Color = m.craft_c3
		if c3.a <= 0.0 and m.CRAFT_RIGGED.has(m.craft_kind):
			c3 = (m.CRAFT_RIGGED[m.craft_kind] as Array)[2]
		m.custom_friends.append([m.craft_kind, m.craft_body.r, m.craft_body.g, m.craft_body.b, m.craft_fins.r, m.craft_fins.g, m.craft_fins.b, 1 if m.craft_body_rb else 0, 1 if m.craft_fins_rb else 0, c3.r, c3.g, c3.b])
		msgtxt = "Off to the courtyard! Find me when you visit!"
	m._write_save()
	if m.chime != null:
		m.chime.pitch_scale = 1.3; m.chime.play()
	m._say("roshan", "win", 0.5)   # a real cheer beside the chime when a craft finishes
	for tn in m.get_tree().get_nodes_in_group("craft_top"):
		if tn is CanvasItem:
			(tn as CanvasItem).visible = false   # audit: banner overlapped title/buttons
	if m.craft_fishbox != null:
		var box := m.craft_fishbox
		var msg := Label.new(); msg.text = msgtxt
		msg.add_theme_font_size_override("font_size", 46); msg.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); msg.add_theme_constant_override("outline_size", 10)
		msg.position = Vector2(180, 18); box.get_parent().add_child(msg)
		box.pivot_offset = box.size * 0.5
		var tw := box.create_tween()
		tw.tween_property(box, "scale", Vector2(1.25, 1.25), 0.4).set_trans(Tween.TRANS_BACK)
		tw.tween_interval(0.5)
		tw.parallel().tween_property(box, "position:x", 1500.0, 1.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.parallel().tween_property(box, "scale", Vector2(0.5, 0.5), 1.0)
	m.get_tree().create_timer(2.6).timeout.connect(_close_craft)

func _close_craft() -> void:
	m.set_meta("craft_closing", false)
	if m.craft_layer != null and is_instance_valid(m.craft_layer):
		m.craft_layer.queue_free()
	m.craft_status = null
	m.craft_pearl_lbl = null
	m.craft_layer = null
	m.craft_fishbox = null
	m.mg_cool = 10.0
