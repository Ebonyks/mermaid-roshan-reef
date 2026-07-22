class_name CollectionSystem
extends RefCounted
# Animal-Crossing-inspired Critter Book. All mutable state stays on ReefMain;
# this Phase-7-style satellite owns only catalog, spawn, motion and UI logic.

var m: ReefMain

const TOTAL := 18
const CATCH_RADIUS := 9.0
const CATEGORY_ORDER := ["fish", "insect", "bird"]
const CATEGORY_ICON := {"fish": "🐟", "insect": "🦋", "bird": "🐦"}
const HABITAT_ICON := {"reef": "🌊", "meadow": "🌸", "river": "💧", "alpine": "❄"}
const HABITAT_LABEL := {
	"reef": "Reef Garden",
	"meadow": "Lagoon Meadow",
	"river": "Lagoon River",
	"alpine": "Alpine Ridge",
}

# pos is local to its world. Reef Y is replaced with seabed height; lagoon Y
# is replaced with the analytic terrain height. The authored Y is the hover.
const DEFS := [
	{"id": "coral_clownfish", "name": "Coral Clownfish", "category": "fish", "habitat": "reef", "context": "ocean", "pos": Vector3(-42, 7, -28), "scale": 1.45, "color": Color(0.98, 0.46, 0.46)},
	{"id": "pearl_seahorse", "name": "Pearl Seahorse", "category": "fish", "habitat": "reef", "context": "ocean", "pos": Vector3(36, 9, 22), "scale": 1.85, "color": Color(0.75, 0.60, 0.94)},
	{"id": "rainbow_angelfish", "name": "Rainbow Angelfish", "category": "fish", "habitat": "reef", "context": "ocean", "pos": Vector3(18, 10, -62), "scale": 1.35, "color": Color(0.30, 0.82, 0.88)},
	{"id": "sky_koi", "name": "Sky Koi", "category": "fish", "habitat": "river", "context": "lagoon", "pos": Vector3(-118, 2.2, 66), "scale": 1.35, "color": Color(1.0, 0.58, 0.55)},
	{"id": "cloud_minnow", "name": "Cloud Minnow", "category": "fish", "habitat": "river", "context": "lagoon", "pos": Vector3(126, 2.2, 62), "scale": 1.45, "color": Color(0.48, 0.80, 1.0)},
	{"id": "frostfin", "name": "Frostfin", "category": "fish", "habitat": "alpine", "context": "lagoon", "pos": Vector3(-152, 2.4, -128), "scale": 1.35, "color": Color(0.86, 0.96, 1.0)},
	{"id": "coral_ladybug", "name": "Coral Ladybug", "category": "insect", "habitat": "meadow", "context": "lagoon", "pos": Vector3(-62, 3.0, 126), "scale": 1.75, "color": Color(0.98, 0.43, 0.48)},
	{"id": "blue_dragonfly", "name": "Blue Dragonfly", "category": "insect", "habitat": "river", "context": "lagoon", "pos": Vector3(92, 4.0, 112), "scale": 1.65, "color": Color(0.27, 0.82, 0.91)},
	{"id": "moon_moth", "name": "Moon Moth", "category": "insect", "habitat": "meadow", "context": "lagoon", "pos": Vector3(64, 4.6, 138), "scale": 1.65, "color": Color(0.74, 0.61, 0.95)},
	{"id": "honeybee", "name": "Honeybee", "category": "insect", "habitat": "meadow", "context": "lagoon", "pos": Vector3(-24, 4.0, 76), "scale": 1.85, "color": Color(1.0, 0.82, 0.28)},
	{"id": "snow_beetle", "name": "Snow Beetle", "category": "insect", "habitat": "alpine", "context": "lagoon", "pos": Vector3(-112, 3.0, -186), "scale": 1.75, "color": Color(0.82, 0.95, 1.0)},
	{"id": "crystal_butterfly", "name": "Crystal Butterfly", "category": "insect", "habitat": "alpine", "context": "lagoon", "pos": Vector3(-172, 5.2, -170), "scale": 1.65, "color": Color(0.50, 0.70, 1.0)},
	{"id": "lagoon_bluebird", "name": "Lagoon Bluebird", "category": "bird", "habitat": "meadow", "context": "lagoon", "pos": Vector3(-84, 9.0, 96), "scale": 1.45, "color": Color(0.43, 0.76, 0.97)},
	{"id": "ruby_hummingbird", "name": "Ruby Hummingbird", "category": "bird", "habitat": "meadow", "context": "lagoon", "pos": Vector3(52, 8.0, 94), "scale": 1.35, "color": Color(0.94, 0.40, 0.52)},
	{"id": "river_kingfisher", "name": "River Kingfisher", "category": "bird", "habitat": "river", "context": "lagoon", "pos": Vector3(154, 8.5, 26), "scale": 1.45, "color": Color(0.28, 0.80, 0.86)},
	{"id": "cloud_puffin", "name": "Cloud Puffin", "category": "bird", "habitat": "river", "context": "lagoon", "pos": Vector3(-164, 8.5, 12), "scale": 1.45, "color": Color(0.20, 0.18, 0.42)},
	{"id": "snowy_owl", "name": "Snowy Owl", "category": "bird", "habitat": "alpine", "context": "lagoon", "pos": Vector3(-126, 10.0, -148), "scale": 1.55, "color": Color(0.90, 0.97, 1.0)},
	{"id": "aurora_tern", "name": "Aurora Tern", "category": "bird", "habitat": "alpine", "context": "lagoon", "pos": Vector3(-190, 11.0, -138), "scale": 1.45, "color": Color(0.64, 0.94, 0.88)},
]


func _init(main: ReefMain) -> void:
	m = main


func total_count() -> int:
	return TOTAL


func caught_count(category: String = "") -> int:
	var count := 0
	for d: Dictionary in DEFS:
		if category != "" and String(d["category"]) != category:
			continue
		if bool(m.critter_collection.get(String(d["id"]), false)):
			count += 1
	return count


func has_nearby() -> bool:
	return m.collection_nearby_id != ""


func build() -> void:
	if m.collection_button != null and is_instance_valid(m.collection_button):
		return
	var layer := CanvasLayer.new()
	layer.layer = 11
	m.add_child(layer)
	m.collection_button_layer = layer
	var button := Button.new()
	button.text = "🐾"
	button.tooltip_text = "Critter Book"
	button.add_theme_font_size_override("font_size", 34)
	button.custom_minimum_size = Vector2(76, 76)
	button.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	button.position = Vector2(-208, 18)   # shifted left of the enlarged 100px pause gear
	var normal := StyleBoxFlat.new()
	normal.bg_color = Color(0.18, 0.52, 0.62, 0.82)
	normal.border_color = Color(0.78, 1.0, 0.86, 0.9)
	normal.set_border_width_all(3)
	normal.set_corner_radius_all(38)
	button.add_theme_stylebox_override("normal", normal)
	var pressed := normal.duplicate() as StyleBoxFlat
	pressed.bg_color = Color(0.42, 0.74, 0.58, 0.95)
	button.add_theme_stylebox_override("pressed", pressed)
	button.pressed.connect(open_book)
	layer.add_child(button)
	m.collection_button = button


func _context() -> String:
	if m.game == "":
		return "ocean"
	if m.game == "level2" and String(m.g.get("phase", "court")) == "court":
		return "lagoon"
	return ""


func tick(delta: float, ppos: Vector3) -> void:
	var context := _context()
	if m.collection_button_layer != null:
		m.collection_button_layer.visible = context != "" and not m.intro_active and m.collection_layer == null
	if context != m.collection_habitat:
		_spawn_context(context)
	if context == "" or m.collection_layer != null:
		m.collection_nearby_id = ""
		m.collection_action_prev = _action_down()
		return
	if not m.collection_hint_shown and not m.intro_active:
		m.collection_hint_shown = true
		m.show_msg("Roshan", "Look! Little critters! Swim close and tap CATCH to add one to our book!", "")

	var now := Time.get_ticks_msec() / 1000.0
	var best := CATCH_RADIUS
	var best_id := ""
	for row_value: Variant in m.collection_nodes:
		var row: Dictionary = row_value
		var node: Node3D = row["node"]
		if not is_instance_valid(node):
			continue
		var d: Dictionary = row["def"]
		var base: Vector3 = row["base"]
		var phase: float = float(row["phase"])
		var category := String(d["category"])
		var speed: float = 0.55 + fmod(phase, 0.5)
		var angle: float = now * speed + phase
		if category == "fish":
			node.position = base + Vector3(cos(angle) * 3.2, sin(angle * 1.7) * 0.65, sin(angle) * 3.2)
			node.rotation.y = -angle
		elif category == "insect":
			node.position = base + Vector3(cos(angle) * 2.2, 0.6 + sin(angle * 2.3) * 0.8, sin(angle) * 2.2)
			node.rotation.y = -angle + PI * 0.5
			_flap(row, sin(now * 11.0 + phase) * 0.42)
		else:
			node.position = base + Vector3(cos(angle) * 5.0, 1.0 + sin(angle * 1.6) * 1.2, sin(angle) * 5.0)
			node.rotation.y = -angle + PI * 0.5
			_flap(row, sin(now * 7.0 + phase) * 0.24)

		var caught: bool = bool(m.critter_collection.get(String(d["id"]), false))
		var marker: Label3D = row["marker"]
		marker.visible = not caught
		var star: Label3D = row["star"]
		star.visible = caught
		if not caught:
			var dist: float = node.position.distance_to(ppos)
			if dist < best:
				best = dist
				best_id = String(d["id"])
		marker.modulate.a = 0.72 + sin(now * 3.0 + phase) * 0.22
	m.collection_nearby_id = best_id
	var action: bool = _action_down()
	if action and not m.collection_action_prev and best_id != "":
		_catch(best_id)
	m.collection_action_prev = action


func _action_down() -> bool:
	var down := Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	if m.touch_ui != null and bool(m.touch_ui.action_down):
		down = true
	return down


func _spawn_context(context: String) -> void:
	if m.collection_root != null and is_instance_valid(m.collection_root):
		m.collection_root.queue_free()
	m.collection_nodes.clear()
	m.collection_nearby_id = ""
	m.collection_habitat = context
	if context == "":
		m.collection_root = null
		return
	var root_node := Node3D.new()
	root_node.name = "CollectibleCritters"
	m.add_child(root_node)
	m.collection_root = root_node
	var index := 0
	for d: Dictionary in DEFS:
		if String(d["context"]) != context:
			continue
		var path := "res://assets/collectibles/%s.glb" % String(d["id"])
		var scene := load(path) as PackedScene
		if scene == null:
			push_warning("Critter asset missing: " + path)
			continue
		var node := scene.instantiate() as Node3D
		if node == null:
			continue
		node.name = String(d["id"])
		var scale_value: float = float(d["scale"])
		node.scale = Vector3.ONE * scale_value
		var authored: Vector3 = d["pos"]
		var base: Vector3
		if context == "ocean":
			base = Vector3(authored.x, m.seabed_y(authored.x, authored.z) + authored.y, authored.z)
		else:
			base = Vector3(m.LEVEL2_POS.x + authored.x, m.lagoon_h(m.LEVEL2_POS.x + authored.x, m.LEVEL2_POS.z + authored.z) + authored.y, m.LEVEL2_POS.z + authored.z)
		node.position = base
		root_node.add_child(node)

		var marker := Label3D.new()
		marker.text = "✦"
		marker.font_size = 150
		marker.outline_size = 22
		marker.modulate = Color(1.0, 0.88, 0.35, 0.9)
		marker.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		marker.no_depth_test = true
		marker.position = Vector3(0, 3.4 / scale_value, 0)
		node.add_child(marker)
		var star := Label3D.new()
		star.text = "★"
		star.font_size = 100
		star.outline_size = 18
		star.modulate = Color(0.55, 1.0, 0.72, 0.88)
		star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		star.no_depth_test = true
		star.position = Vector3(0, 3.4 / scale_value, 0)
		node.add_child(star)
		var wings: Array[Node3D] = []
		_find_wings(node, wings)
		m.collection_nodes.append({
			"def": d,
			"node": node,
			"base": base,
			"phase": float(index) * 1.731,
			"scale": scale_value,
			"marker": marker,
			"star": star,
			"wings": wings,
		})
		index += 1


func _find_wings(node: Node, out: Array[Node3D]) -> void:
	if node is Node3D and String(node.name).to_lower().begins_with("wing_"):
		out.append(node as Node3D)
	for child: Node in node.get_children():
		_find_wings(child, out)


func _flap(row: Dictionary, amount: float) -> void:
	var wings: Array = row["wings"]
	for i in range(wings.size()):
		var wing_node: Node3D = wings[i]
		if is_instance_valid(wing_node):
			wing_node.rotation.x = amount * (-1.0 if i % 2 == 0 else 1.0)


func _def_by_id(id: String) -> Dictionary:
	for d: Dictionary in DEFS:
		if String(d["id"]) == id:
			return d
	return {}


func _row_by_id(id: String) -> Dictionary:
	for row_value: Variant in m.collection_nodes:
		var row: Dictionary = row_value
		var d: Dictionary = row["def"]
		if String(d["id"]) == id:
			return row
	return {}


func _catch(id: String) -> void:
	if bool(m.critter_collection.get(id, false)):
		return
	var d := _def_by_id(id)
	var row := _row_by_id(id)
	if d.is_empty() or row.is_empty():
		return
	m.critter_collection[id] = true
	m.collection_nearby_id = ""
	var node: Node3D = row["node"]
	if is_instance_valid(node):
		m._sparkle_burst(node.position + Vector3(0, 1.0, 0), d["color"])
		var base_scale: float = float(row["scale"])
		var tween := node.create_tween()
		tween.tween_property(node, "scale", Vector3.ONE * base_scale * 1.35, 0.18).set_trans(Tween.TRANS_BACK)
		tween.tween_property(node, "scale", Vector3.ONE * base_scale, 0.24).set_trans(Tween.TRANS_BOUNCE)
	_sweep_net()
	if m.player != null:
		m.player.play_verb("cheer")
	if m.chime != null:
		m.chime.pitch_scale = 1.2
		m.chime.play()
	var habitat := String(HABITAT_LABEL.get(String(d["habitat"]), "the reef"))
	m.show_msg("Roshan", "I found a %s! It lives in %s. Into our Critter Book!" % [String(d["name"]), habitat], "")
	m._update_hud()
	m._write_save()


func _sweep_net() -> void:
	if m.player == null:
		return
	var scene := load("res://assets/collectibles/catch_net.glb") as PackedScene
	if scene == null:
		return
	var net := scene.instantiate() as Node3D
	if net == null:
		return
	net.position = m.player.position + Vector3(0, 2.0, 0)
	net.rotation_degrees = Vector3(15, m.player.rotation_degrees.y, -55)
	net.scale = Vector3.ONE * 1.5
	m.add_child(net)
	var tween := net.create_tween()
	tween.tween_property(net, "rotation_degrees:z", 58.0, 0.36).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.parallel().tween_property(net, "position:y", net.position.y + 1.4, 0.36)
	tween.tween_property(net, "scale", Vector3.ONE * 0.15, 0.20)
	tween.tween_callback(net.queue_free)


func open_book() -> void:
	if m.collection_layer != null:
		return
	m.collection_layer = CanvasLayer.new()
	m.collection_layer.layer = 25
	m.add_child(m.collection_layer)
	var root_control := Control.new()
	root_control.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.collection_layer.add_child(root_control)
	var dim := ColorRect.new()
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.color = Color(0.025, 0.06, 0.12, 0.94)
	root_control.add_child(dim)
	var stage := Control.new()
	stage.custom_minimum_size = Vector2(1280, 720)
	stage.size = Vector2(1280, 720)
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	var scale_value: float = minf(viewport_size.x / 1280.0, viewport_size.y / 720.0)
	stage.scale = Vector2.ONE * scale_value
	stage.position = (viewport_size - Vector2(1280, 720) * scale_value) * 0.5
	root_control.add_child(stage)
	m.collection_stage = stage
	if m.player != null:
		m.player.vel = Vector3.ZERO
	m.collection_category = "fish"
	_draw_book()
	m._say("roshan", "")


func close_book() -> void:
	if m.collection_layer != null and is_instance_valid(m.collection_layer):
		m.collection_layer.queue_free()
	m.collection_layer = null
	m.collection_stage = null


func _switch_category(category: String) -> void:
	m.collection_category = category
	_draw_book()


func _draw_book() -> void:
	var stage: Control = m.collection_stage
	if stage == null or not is_instance_valid(stage):
		return
	for child: Node in stage.get_children():
		child.queue_free()
	var panel := Panel.new()
	panel.position = Vector2(34, 24)
	panel.size = Vector2(1212, 672)
	var panel_style := StyleBoxFlat.new()
	panel_style.bg_color = Color(0.10, 0.17, 0.30, 0.98)
	panel_style.border_color = Color(0.48, 0.92, 0.80)
	panel_style.set_border_width_all(5)
	panel_style.set_corner_radius_all(28)
	panel.add_theme_stylebox_override("panel", panel_style)
	stage.add_child(panel)

	var title := Label.new()
	title.text = "🐚  My Critter Book   %d / %d" % [caught_count(), TOTAL]
	title.add_theme_font_size_override("font_size", 46)
	title.add_theme_color_override("font_color", Color(1.0, 0.94, 0.66))
	title.add_theme_color_override("font_outline_color", Color(0.05, 0.07, 0.16))
	title.add_theme_constant_override("outline_size", 9)
	title.position = Vector2(70, 34)
	stage.add_child(title)

	var close := Button.new()
	close.text = "✕"
	close.add_theme_font_size_override("font_size", 44)
	close.position = Vector2(1122, 34)   # 100px: frustrated fingers mash here
	close.custom_minimum_size = Vector2(100, 100)
	close.pressed.connect(close_book)
	stage.add_child(close)

	for i in range(CATEGORY_ORDER.size()):
		var category: String = CATEGORY_ORDER[i]
		var tab := Button.new()
		tab.text = "%s  %d / 6" % [String(CATEGORY_ICON[category]), caught_count(category)]
		tab.add_theme_font_size_override("font_size", 30)
		tab.position = Vector2(88 + float(i) * 270.0, 100)   # up 5px so the taller tab clears the cards at y=198
		tab.custom_minimum_size = Vector2(242, 90)
		if category == m.collection_category:
			var active_style := StyleBoxFlat.new()
			active_style.bg_color = Color(0.32, 0.70, 0.62, 0.95)
			active_style.set_corner_radius_all(22)
			tab.add_theme_stylebox_override("normal", active_style)
		tab.pressed.connect(_switch_category.bind(category))
		stage.add_child(tab)

	var visible_defs: Array[Dictionary] = []
	for d: Dictionary in DEFS:
		if String(d["category"]) == m.collection_category:
			visible_defs.append(d)
	for i in range(visible_defs.size()):
		var d: Dictionary = visible_defs[i]
		var caught: bool = bool(m.critter_collection.get(String(d["id"]), false))
		var card := Panel.new()
		card.position = Vector2(82 + float(i % 3) * 388.0, 198 + float(i / 3) * 218.0)
		card.size = Vector2(356, 192)
		var card_style := StyleBoxFlat.new()
		var card_color: Color = d["color"]
		card_style.bg_color = card_color.darkened(0.48) if caught else Color(0.13, 0.15, 0.23, 0.96)
		card_style.border_color = card_color if caught else Color(0.30, 0.34, 0.42)
		card_style.set_border_width_all(4)
		card_style.set_corner_radius_all(24)
		card.add_theme_stylebox_override("panel", card_style)
		stage.add_child(card)
		var icon := Label.new()
		icon.text = String(CATEGORY_ICON[m.collection_category]) if caught else "?"
		icon.add_theme_font_size_override("font_size", 68)
		icon.position = Vector2(22, 23)
		icon.size = Vector2(96, 96)
		icon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		card.add_child(icon)
		var name_label := Label.new()
		name_label.text = String(d["name"]) if caught else "Mystery Friend"
		name_label.add_theme_font_size_override("font_size", 29 if caught else 25)
		name_label.add_theme_color_override("font_color", Color(1.0, 0.96, 0.80) if caught else Color(0.67, 0.72, 0.80))
		name_label.position = Vector2(122, 30)
		name_label.size = Vector2(220, 74)
		name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		card.add_child(name_label)
		var habitat := Label.new()
		var habitat_id := String(d["habitat"])
		habitat.text = "%s  %s" % [String(HABITAT_ICON[habitat_id]), String(HABITAT_LABEL[habitat_id])]
		habitat.add_theme_font_size_override("font_size", 22)
		habitat.add_theme_color_override("font_color", Color(0.74, 0.96, 0.88))
		habitat.position = Vector2(28, 134)
		card.add_child(habitat)

	var help := Label.new()
	help.text = "✦  Swim close to a sparkling critter, then tap CATCH!  ✦"
	help.add_theme_font_size_override("font_size", 25)
	help.add_theme_color_override("font_color", Color(0.78, 0.92, 1.0))
	help.position = Vector2(230, 638)
	stage.add_child(help)
