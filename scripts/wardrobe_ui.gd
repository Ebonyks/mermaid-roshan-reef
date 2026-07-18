class_name WardrobeUI
extends RefCounted
# Mechanical extraction of the dress-up wardrobe and sticker book overlays
# from main.gd. All state (wardrobe_layer, wd, stickers_layer, skin_id,
# stickers) stays on main (m.*); received by reference, logic only.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ---------------- DRESS-UP WARDROBE (full-skin picker) ----------------
func _open_wardrobe() -> void:
	if m.wardrobe_layer != null:
		return
	m.wardrobe_layer = CanvasLayer.new(); m.wardrobe_layer.layer = 18; m.add_child(m.wardrobe_layer)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT); m.wardrobe_layer.add_child(root)
	var vp: Vector2 = m.get_viewport().get_visible_rect().size
	var bg := ColorRect.new(); bg.color = Color(0.13, 0.09, 0.18, 0.96); bg.set_anchors_preset(Control.PRESET_FULL_RECT); root.add_child(bg)
	var stage := Control.new(); stage.size = Vector2(1280, 720)
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	stage.scale = Vector2(sc, sc); stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	root.add_child(stage)
	m.wd["stage"] = stage
	var title := Label.new(); title.text = "Pick your look!"
	title.add_theme_font_size_override("font_size", 56)
	title.add_theme_color_override("font_color", Color(1.0, 0.92, 0.98))
	title.add_theme_color_override("font_outline_color", Color(0.08, 0.05, 0.15)); title.add_theme_constant_override("outline_size", 10)
	title.position = Vector2(60, 18); stage.add_child(title)
	# ---- preview of the selected skin ----
	var frame := Panel.new(); frame.position = Vector2(110, 110); frame.size = Vector2(470, 560)
	var fsb := StyleBoxFlat.new(); fsb.bg_color = Color(0.22, 0.26, 0.42); fsb.border_color = Color(0.48, 0.86, 0.9, 0.9); fsb.set_border_width_all(3); fsb.set_corner_radius_all(8)
	fsb.set_border_width_all(8); fsb.border_color = Color(0.95, 0.8, 0.45)
	frame.add_theme_stylebox_override("panel", fsb); stage.add_child(frame)
	var preview := TextureRect.new()
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	preview.position = Vector2(125, 125); preview.size = Vector2(440, 530)
	stage.add_child(preview)
	m.wd["preview"] = preview
	# ---- one button per skin (mutually exclusive) ----
	m.wd["btns"] = []
	for si in range(m.SKINS.size()):
		var entry: Dictionary = m.SKINS[si]
		var id: String = String(entry["id"])
		var b := Button.new(); b.add_theme_font_size_override("font_size", 40)
		b.position = Vector2(640, 130.0 + float(si) * 110.0); b.custom_minimum_size = Vector2(450, 92)
		var sb := StyleBoxFlat.new(); sb.set_corner_radius_all(8)
		b.add_theme_stylebox_override("normal", sb); b.add_theme_stylebox_override("hover", sb); b.add_theme_stylebox_override("pressed", sb)
		b.pressed.connect(func(): _wardrobe_pick(id))
		stage.add_child(b)
		(m.wd["btns"] as Array).append({"btn": b, "box": sb, "id": id})
	# ---- Done ----
	var done := Button.new(); done.text = "  Done!  "; done.add_theme_font_size_override("font_size", 46)
	done.position = Vector2(740, 560); done.custom_minimum_size = Vector2(220, 120)
	var dsb := StyleBoxFlat.new(); dsb.bg_color = Color(0.3, 0.8, 0.45); dsb.set_corner_radius_all(8)
	done.add_theme_stylebox_override("normal", dsb); done.add_theme_stylebox_override("hover", dsb); done.add_theme_stylebox_override("pressed", dsb)
	done.pressed.connect(_wardrobe_done); stage.add_child(done)
	_wardrobe_refresh()

func _wardrobe_refresh() -> void:
	if m.wardrobe_layer == null:
		return
	if m.wd.has("preview"):
		(m.wd["preview"] as TextureRect).texture = load(String(m._skin_def(m.skin_id)["preview"]))
	for entry in m.wd.get("btns", []):
		var sel: bool = String(entry["id"]) == m.skin_id
		var eid := String(entry["id"])
		var locked: bool = eid.begins_with("fairy") and not m.fairy_skin_unlocked
		var box: StyleBoxFlat = entry["box"]
		box.bg_color = Color(0.28, 0.28, 0.38) if locked else (Color(0.3, 0.75, 0.42) if sel else Color(0.4, 0.42, 0.6))
		box.set_border_width_all(6 if sel else 0)
		box.border_color = Color(0.2, 1.0, 0.4)
		var bt: Button = entry["btn"]
		bt.text = "🔒 " + String(m._skin_def(eid)["label"]) if locked else ("✔ " if sel else "    ") + String(m._skin_def(eid)["label"])
		bt.modulate = Color(0.75, 0.75, 0.8) if locked else Color.WHITE

func _wardrobe_pick(id: String) -> void:
	if id.begins_with("fairy") and not m.fairy_skin_unlocked:
		# the Butterfly World prize — tease it, don't grant it
		if m.chime != null:
			m.chime.pitch_scale = 0.5
			m.chime.play()
		_wardrobe_toast("🦋 Save the Butterfly World to unlock Fairy Roshan!")
		return
	m.skin_id = id
	m._apply_skin()
	_wardrobe_refresh()
	if m.chime != null:
		m.chime.pitch_scale = 1.3; m.chime.play()
	# magic-moment: trying on a look showers Roshan in a sparkle swirl + twirl
	m._sparkle_burst(m.player.position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 1.0))
	m._sparkle_burst(m.player.position + Vector3(0, 0.5, 0), Color(0.7, 0.95, 1.0))
	m.player.play_verb("twirl")   # R2-C: she shows off the new look

func _open_stickers() -> void:
	if m.stickers_layer != null:
		return
	m.stickers_layer = CanvasLayer.new(); m.stickers_layer.layer = 18; m.add_child(m.stickers_layer)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT); m.stickers_layer.add_child(root)
	var vp: Vector2 = m.get_viewport().get_visible_rect().size
	var bg := ColorRect.new(); bg.color = Color(0.10, 0.07, 0.17, 0.96); bg.set_anchors_preset(Control.PRESET_FULL_RECT); root.add_child(bg)
	var stage := Control.new(); stage.size = Vector2(1280, 720)
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	stage.scale = Vector2(sc, sc); stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	root.add_child(stage)
	var got := 0
	for d in m.STICKER_DEFS:
		if bool(m.stickers.get(String(d["id"]), false)):
			got += 1
	var title := Label.new(); title.text = "⭐ My Sticker Book!   %d / %d" % [got, m.STICKER_DEFS.size()]
	title.add_theme_font_size_override("font_size", 52)
	title.add_theme_color_override("font_color", Color(1.0, 0.93, 0.6))
	title.add_theme_color_override("font_outline_color", Color(0.08, 0.05, 0.15)); title.add_theme_constant_override("outline_size", 10)
	title.position = Vector2(60, 16); stage.add_child(title)
	for si in range(m.STICKER_DEFS.size()):
		var d2: Dictionary = m.STICKER_DEFS[si]
		var earned: bool = bool(m.stickers.get(String(d2["id"]), false))
		var cell := Panel.new()
		cell.position = Vector2(46.0 + float(si % 6) * 199.0, 104.0 + float(si / 6) * 194.0)
		cell.size = Vector2(184, 178)
		var csb := StyleBoxFlat.new()
		csb.bg_color = Color(0.32, 0.28, 0.5, 0.95) if earned else Color(0.2, 0.19, 0.28, 0.9)
		csb.set_corner_radius_all(8)
		csb.set_border_width_all(4)
		csb.border_color = Color(1.0, 0.85, 0.4) if earned else Color(0.35, 0.35, 0.45)
		cell.add_theme_stylebox_override("panel", csb)
		stage.add_child(cell)
		var em := Label.new()
		em.text = String(d2["emoji"]) if earned else "?"
		em.add_theme_font_size_override("font_size", 64)
		em.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
		em.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		em.offset_top = 8.0
		em.modulate = Color.WHITE if earned else Color(0.55, 0.55, 0.65)
		cell.add_child(em)
		var nm := Label.new()
		nm.text = String(d2["label"]) if earned else String(d2["hint"])
		nm.add_theme_font_size_override("font_size", 20 if earned else 15)
		nm.add_theme_color_override("font_color", Color(1.0, 0.95, 0.8) if earned else Color(0.7, 0.7, 0.78))
		nm.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		nm.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		nm.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		nm.offset_top = -72.0
		nm.offset_left = 8.0
		nm.offset_right = -8.0
		cell.add_child(nm)
	var xb := Button.new(); xb.text = "✕"
	xb.add_theme_font_size_override("font_size", 42)
	xb.position = Vector2(1186, 14); xb.custom_minimum_size = Vector2(76, 76)
	xb.pressed.connect(_close_stickers)
	stage.add_child(xb)

func _close_stickers() -> void:
	if m.stickers_layer != null and is_instance_valid(m.stickers_layer):
		m.stickers_layer.queue_free()
	m.stickers_layer = null

func _wardrobe_toast(txt: String) -> void:
	if not m.wd.has("stage"):
		return
	var t := Label.new()
	t.text = txt
	t.add_theme_font_size_override("font_size", 34)
	t.add_theme_color_override("font_color", Color(1.0, 0.85, 0.5))
	t.add_theme_color_override("font_outline_color", Color(0.08, 0.05, 0.15))
	t.add_theme_constant_override("outline_size", 10)
	t.position = Vector2(110, 682)
	(m.wd["stage"] as Control).add_child(t)
	var tw := t.create_tween()
	tw.tween_interval(2.2)
	tw.tween_property(t, "modulate:a", 0.0, 0.6)
	tw.tween_callback(t.queue_free)

func _wardrobe_done() -> void:
	m._write_save()
	if m.voice != null:
		m.voice.pitch_scale = 1.15; m.voice.play()
	_close_wardrobe()

func _close_wardrobe() -> void:
	if m.wardrobe_layer != null and is_instance_valid(m.wardrobe_layer):
		m.wardrobe_layer.queue_free()
	m.wardrobe_layer = null
	m.wd = {}
	m.mg_cool = 8.0
