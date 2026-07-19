class_name CompanionSystem
extends RefCounted
# THE STUFFED-FRIEND COMPANION WING (Pokemon-style, no fail states).
# Phase-7 satellite: ALL mutable state stays on ReefMain (m.companion_*,
# m.fish_tokens, m.stuffie_wins) — this class owns only roster data, the
# throne gift + picker flow, the overworld follower, fish-token pickups,
# and the sparring-den entrance. The battle itself is scripts/stuffie_battle.gd.
#
# Flow: reach Princess Huluu at the Pearl Castle throne → a gift box appears
# beside the Crown Star → pick a stuffie friend + paint its three colours →
# it follows Roshan through the reef, cheers, guides, and grabs sparkle fish
# (each fish = +1 level). The sparkle ring near the shipwreck starts the
# play-battle ladder. A second player can steer the stuffie any time by
# holding R1 on a gamepad (battles read every pad natively, so P2 co-op
# there needs no mode at all).

var m: ReefMain

# Data-driven roster: a third stuffed friend is one dictionary away.
# kind → CREATURE_LAYERS/CRAFT_RIGGED key on main (bird = the rigged birdie
# body doubling as the baby eagle; cat = the rigged kitty).
const ROSTER := [
	{"id": "eagle", "name": "Baby Eagle", "kind": "bird", "attack": "PECK",
		"body": Color(0.98, 0.72, 0.55), "accent": Color(1.0, 0.85, 0.40), "third": Color(1.0, 0.92, 0.55),
		"hello": "Baby Eagle flies with you now! Peck peck!",
		"pro": "Speedy wings and a quick peck!"},
	{"id": "mewsha", "name": "Mewsha", "kind": "cat", "attack": "CLAW",
		"body": Color(0.95, 0.70, 0.85), "accent": Color(0.60, 0.40, 0.90), "third": Color(0.97, 0.96, 0.93),
		"hello": "Mewsha pads along beside you now! Swish swish!",
		"pro": "Big brave claw swipes!"},
]

const PALETTE := [
	Color(0.98, 0.55, 0.65), Color(1.0, 0.72, 0.42), Color(1.0, 0.9, 0.45),
	Color(0.55, 0.9, 0.6), Color(0.45, 0.82, 0.95), Color(0.62, 0.55, 0.95),
	Color(0.95, 0.7, 0.9), Color(0.97, 0.96, 0.93),
]
const COLOR_SLOTS := ["body", "accent", "third"]
const SLOT_ICON := ["🎨", "✨", "🤍"]

const TOKEN_TOTAL := 8            # sparkle-fish slots alive in the reef at once
const TOKEN_RESPAWN := 75.0       # seconds until a caught slot refills
const TOKEN_RADIUS := 5.5
const GIFT_RADIUS := 6.5
const DEN_RADIUS := 9.0

func _init(main: ReefMain) -> void:
	m = main

func def_by_id(id: String) -> Dictionary:
	for d: Dictionary in ROSTER:
		if String(d["id"]) == id:
			return d
	return {}

func active_def() -> Dictionary:
	return def_by_id(m.companion_id)

func level() -> int:
	# incremental track: every sparkle fish token = +1 level
	return m.fish_tokens

func tier() -> int:
	# milestone track: real Critter-Book fish catches (0..6) unlock ability tiers
	return m._collection_ref().caught_count("fish")

func colors() -> Array[Color]:
	var d := active_def()
	var out: Array[Color] = []
	var defaults: Array = [d.get("body", Color.WHITE), d.get("accent", Color.WHITE), d.get("third", Color.WHITE)]
	for i in range(3):
		if m.companion_colors.size() > i and typeof(m.companion_colors[i]) == TYPE_STRING:
			out.append(Color.html(String(m.companion_colors[i])))
		else:
			out.append(defaults[i])
	return out

func make_creature() -> Node3D:
	var d := active_def()
	if d.is_empty():
		return null
	var c := colors()
	return m._make_creature_node(String(d["kind"]), c[0], c[1], false, false, c[2])

# ===================== per-frame tick (called from main._process) =====================

func tick(delta: float) -> void:
	if m.player == null or m.intro_active:
		return
	_tick_gift(delta)
	if m.companion_id == "":
		return
	_tick_follower(delta)
	_tick_tokens(delta)
	_tick_den(delta)

# ---------- the throne gift (unlock moment) ----------

func _tick_gift(_delta: float) -> void:
	# Princess Huluu's present: appears beside the Crown Star once she has
	# greeted Roshan, until a stuffie friend has been chosen. Deliberately a
	# walk-up-and-tap object, never an auto-modal — the crown path stays clear.
	var in_hall: bool = m.game == "level2" and String(m.g.get("phase", "court")) == "hall"
	if not in_hall or m.companion_id != "":
		if m.companion_gift != null and is_instance_valid(m.companion_gift):
			m._sparkle_burst(m.companion_gift.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.8, 0.9))
			m.companion_gift.queue_free()   # opened! (castle teardown also covers it via game_nodes)
		m.companion_gift = null
		return
	if not bool(m.g.get("huluu_greeted", false)):
		return
	if m.companion_gift == null or not is_instance_valid(m.companion_gift):
		_build_gift()
	if m.companion_gift == null:
		return
	var t: float = Time.get_ticks_msec() / 1000.0
	var pointer_node: Label3D = m.companion_gift.get_meta("pointer")
	if is_instance_valid(pointer_node):
		pointer_node.position.y = 6.4 + sin(t * 4.0) * 0.5
	m.companion_gift.rotation.y = sin(t * 1.3) * 0.25
	if m.companion_layer != null:
		return
	var gd: float = m.companion_gift.global_position.distance_to(m.player.position)
	var action: bool = _action_down()
	if gd < GIFT_RADIUS and action and not m.companion_action_prev:
		open_picker()
	m.companion_action_prev = action

func _build_gift() -> void:
	if m.l2_stars.is_empty():
		return
	var crown: Node3D = m.l2_stars[0]["node"]
	if not is_instance_valid(crown):
		return
	var root := Node3D.new()
	root.position = crown.position + Vector3(9.0, -1.0, 3.0)
	m.add_child(root)
	m.game_nodes.append(root)
	m.companion_gift = root
	var box := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(3.0, 2.4, 3.0)
	box.mesh = bm
	box.position = Vector3(0, 1.2, 0)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.95, 0.6, 0.78)
	mat.emission_enabled = true
	mat.emission = Color(0.95, 0.6, 0.78)
	mat.emission_energy_multiplier = 0.35
	box.material_override = mat
	root.add_child(box)
	var lid := MeshInstance3D.new()
	var lm := BoxMesh.new()
	lm.size = Vector3(3.4, 0.7, 3.4)
	lid.mesh = lm
	lid.position = Vector3(0, 2.6, 0)
	var lidmat := StandardMaterial3D.new()
	lidmat.albedo_color = Color(0.62, 0.55, 0.95)
	lidmat.emission_enabled = true
	lidmat.emission = Color(0.62, 0.55, 0.95)
	lidmat.emission_energy_multiplier = 0.4
	lid.material_override = lidmat
	root.add_child(lid)
	var bow := Label3D.new()
	bow.text = "🎁"
	bow.font_size = 180
	bow.pixel_size = 0.02
	bow.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	bow.position = Vector3(0, 4.2, 0)
	root.add_child(bow)
	var pointer := Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 150
	pointer.pixel_size = 0.022
	pointer.outline_size = 24
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	pointer.position = Vector3(0, 6.4, 0)
	root.add_child(pointer)
	root.set_meta("pointer", pointer)
	m._sparkle_burst(root.position + Vector3(0, 3.0, 0), Color(1.0, 0.75, 0.9))
	if not bool(m.g.get("companion_gift_said", false)):
		m.g["companion_gift_said"] = true
		m.show_msg("Princess Huluu", "A present for you! Tap the gift box and pick a stuffie friend to carry on your adventure!", "talk")

func _action_down() -> bool:
	var down := Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	if m.touch_ui != null and bool(m.touch_ui.action_down):
		down = true
	return down

# ---------- the picker + colour studio overlay ----------

func open_picker() -> void:
	if m.companion_layer != null:
		return
	m.companion_pick_id = String(ROSTER[0]["id"]) if m.companion_id == "" else m.companion_id
	m.companion_pick_colors = []
	var pick_def := def_by_id(m.companion_pick_id)
	for slot in COLOR_SLOTS:
		m.companion_pick_colors.append((pick_def[slot] as Color).to_html(false))
	m.companion_layer = CanvasLayer.new()
	m.companion_layer.layer = 25
	m.add_child(m.companion_layer)
	var root_control := Control.new()
	root_control.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.companion_layer.add_child(root_control)
	var dim := ColorRect.new()
	dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	dim.color = Color(0.025, 0.06, 0.12, 0.94)
	# tap outside the panel = gently close (also keeps the audit bot un-stuck)
	dim.gui_input.connect(_on_picker_dim_input)
	root_control.add_child(dim)
	var stage := Control.new()
	stage.custom_minimum_size = Vector2(1280, 720)
	stage.size = Vector2(1280, 720)
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	var scale_value: float = minf(viewport_size.x / 1280.0, viewport_size.y / 720.0)
	stage.scale = Vector2.ONE * scale_value
	stage.position = (viewport_size - Vector2(1280, 720) * scale_value) * 0.5
	root_control.add_child(stage)
	m.companion_stage = stage
	if m.player != null:
		m.player.vel = Vector3.ZERO
	_draw_picker()
	m.show_msg("Roshan", "Which stuffie friend comes with me? Tap one, then paint its colors!", "talk")

func _on_picker_dim_input(ev: InputEvent) -> void:
	if ev is InputEventMouseButton and (ev as InputEventMouseButton).pressed:
		close_picker()

func close_picker() -> void:
	if m.companion_layer != null and is_instance_valid(m.companion_layer):
		m.companion_layer.queue_free()
	m.companion_layer = null
	m.companion_stage = null

func _pick_friend(id: String) -> void:
	m.companion_pick_id = id
	m.companion_pick_colors = []
	var d := def_by_id(id)
	for slot in COLOR_SLOTS:
		m.companion_pick_colors.append((d[slot] as Color).to_html(false))
	m._ui_tap()
	m.show_msg("Roshan", String(d["name"]) + "! " + String(d["pro"]), "talk")
	_draw_picker()

func _pick_color(slot: int, col: Color) -> void:
	while m.companion_pick_colors.size() < 3:
		m.companion_pick_colors.append("ffffff")
	m.companion_pick_colors[slot] = col.to_html(false)
	m._ui_tap()
	_draw_picker()

func _confirm_pick() -> void:
	m.companion_id = m.companion_pick_id
	m.companion_colors = m.companion_pick_colors.duplicate()
	var d := active_def()
	close_picker()
	if m.companion_node != null and is_instance_valid(m.companion_node):
		m.companion_node.queue_free()
		m.companion_node = null
	m.companion_greeted = false
	m._write_save()
	m._reward(false)
	if m.player != null:
		m._sparkle_burst(m.player.position + Vector3(0, 2.0, 0), Color(1.0, 0.8, 0.5))
	m.show_msg(String(d["name"]), String(d["hello"]), "win")

func _draw_picker() -> void:
	var stage: Control = m.companion_stage
	if stage == null or not is_instance_valid(stage):
		return
	for child: Node in stage.get_children():
		child.queue_free()
	var panel := Panel.new()
	panel.position = Vector2(34, 24)
	panel.size = Vector2(1212, 672)
	var panel_style := StyleBoxFlat.new()
	panel_style.bg_color = Color(0.10, 0.17, 0.30, 0.98)
	panel_style.border_color = Color(0.95, 0.7, 0.9)
	panel_style.set_border_width_all(5)
	panel_style.set_corner_radius_all(28)
	panel.add_theme_stylebox_override("panel", panel_style)
	stage.add_child(panel)
	var title := Label.new()
	title.text = "🧸  Pick your stuffie friend!"
	title.add_theme_font_size_override("font_size", 44)
	title.add_theme_color_override("font_color", Color(1.0, 0.94, 0.66))
	title.add_theme_color_override("font_outline_color", Color(0.05, 0.07, 0.16))
	title.add_theme_constant_override("outline_size", 9)
	title.position = Vector2(70, 34)
	stage.add_child(title)
	var close := Button.new()
	close.text = "✕"
	close.add_theme_font_size_override("font_size", 38)
	close.position = Vector2(1145, 40)
	close.custom_minimum_size = Vector2(72, 72)
	close.pressed.connect(close_picker)
	stage.add_child(close)
	# friend cards down the left
	for i in range(ROSTER.size()):
		var d: Dictionary = ROSTER[i]
		var id := String(d["id"])
		var card := Button.new()
		card.position = Vector2(80, 130 + float(i) * 250.0)
		card.custom_minimum_size = Vector2(330, 225)
		var card_style := StyleBoxFlat.new()
		card_style.bg_color = Color(0.32, 0.55, 0.62, 0.95) if id == m.companion_pick_id else Color(0.13, 0.15, 0.23, 0.96)
		card_style.border_color = Color(1.0, 0.9, 0.4) if id == m.companion_pick_id else Color(0.30, 0.34, 0.42)
		card_style.set_border_width_all(5)
		card_style.set_corner_radius_all(24)
		card.add_theme_stylebox_override("normal", card_style)
		card.add_theme_stylebox_override("hover", card_style)
		card.add_theme_stylebox_override("pressed", card_style)
		card.pressed.connect(_pick_friend.bind(id))
		stage.add_child(card)
		_add_creature_preview(card, String(d["kind"]), Vector2(28, 24), 0.62,
			(d["body"] as Color), (d["accent"] as Color))
		var nm := Label.new()
		nm.text = String(d["name"])
		nm.add_theme_font_size_override("font_size", 26)
		nm.add_theme_color_override("font_color", Color(1.0, 0.96, 0.80))
		nm.position = Vector2(160, 40)
		nm.size = Vector2(160, 120)
		nm.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		card.add_child(nm)
		var atk := Label.new()
		atk.text = ("🐦 " if String(d["kind"]) == "bird" else "🐾 ") + String(d["attack"])
		atk.add_theme_font_size_override("font_size", 24)
		atk.add_theme_color_override("font_color", Color(0.74, 0.96, 0.88))
		atk.position = Vector2(160, 165)
		card.add_child(atk)
	# big live preview, painted with the picked colours
	var pick_def := def_by_id(m.companion_pick_id)
	var pc0 := Color.html(String(m.companion_pick_colors[0]))
	var pc1 := Color.html(String(m.companion_pick_colors[1]))
	var preview_panel := Panel.new()
	preview_panel.position = Vector2(460, 130)
	preview_panel.size = Vector2(330, 330)
	var pv_style := StyleBoxFlat.new()
	pv_style.bg_color = Color(0.16, 0.24, 0.38, 0.96)
	pv_style.set_corner_radius_all(26)
	preview_panel.add_theme_stylebox_override("panel", pv_style)
	stage.add_child(preview_panel)
	_add_creature_preview(preview_panel, String(pick_def["kind"]), Vector2(35, 35), 1.3, pc0, pc1)
	# three colour rows on the right
	for slot in range(3):
		var row_y := 130.0 + float(slot) * 120.0
		var icon := Label.new()
		icon.text = SLOT_ICON[slot]
		icon.add_theme_font_size_override("font_size", 46)
		icon.position = Vector2(830, row_y + 18.0)
		stage.add_child(icon)
		for ci in range(PALETTE.size()):
			var col: Color = PALETTE[ci]
			var swatch := Button.new()
			swatch.position = Vector2(900 + float(ci % 4) * 78.0, row_y + float(ci / 4) * 52.0)
			swatch.custom_minimum_size = Vector2(64, 44)
			var sw_style := StyleBoxFlat.new()
			sw_style.bg_color = col
			var chosen: bool = col.to_html(false) == String(m.companion_pick_colors[slot])
			sw_style.border_color = Color(1.0, 1.0, 1.0) if chosen else Color(0.1, 0.12, 0.2)
			sw_style.set_border_width_all(5 if chosen else 2)
			sw_style.set_corner_radius_all(16)
			swatch.add_theme_stylebox_override("normal", sw_style)
			swatch.add_theme_stylebox_override("hover", sw_style)
			swatch.add_theme_stylebox_override("pressed", sw_style)
			swatch.pressed.connect(_pick_color.bind(slot, col))
			stage.add_child(swatch)
	var go := Button.new()
	go.text = "✔  LET'S GO!"
	go.add_theme_font_size_override("font_size", 40)
	go.position = Vector2(460, 520)
	go.custom_minimum_size = Vector2(640, 110)
	var go_style := StyleBoxFlat.new()
	go_style.bg_color = Color(0.35, 0.75, 0.5, 0.97)
	go_style.border_color = Color(0.85, 1.0, 0.9)
	go_style.set_border_width_all(4)
	go_style.set_corner_radius_all(30)
	go.add_theme_stylebox_override("normal", go_style)
	go.pressed.connect(_confirm_pick)
	stage.add_child(go)
	m._hook_button_taps(stage)

func _add_creature_preview(parent: Control, kind: String, pos: Vector2, scale_value: float, body: Color, accent: Color) -> void:
	# layered book-art preview (assets/mg fish/cat/bird sheets), live-tinted —
	# the same sheets the craft creatures use, so the paint matches in-world
	var layer_names: Array = m.CREATURE_LAYERS.get(kind, m.CREATURE_LAYERS["fish"])
	var tints: Array[Color] = [accent, body, Color.WHITE]   # [accent, body, line] draw order
	for li in range(3):
		var tex_path := "res://assets/mg/" + String(layer_names[li]) + ".png"
		if not ResourceLoader.exists(tex_path):
			continue
		var tr := TextureRect.new()
		tr.texture = load(tex_path)
		tr.position = pos
		tr.scale = Vector2.ONE * scale_value
		tr.modulate = tints[li] if li < 2 else Color.WHITE
		tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		parent.add_child(tr)

# ---------- the overworld follower ----------

func _tick_follower(delta: float) -> void:
	if m.companion_node == null or not is_instance_valid(m.companion_node):
		if m.game != "":
			return   # spawn only in the open reef, never mid-arena
		var fwd0 := Vector3(sin(m.player.yaw), 0, cos(m.player.yaw))
		var node := make_creature()
		if node == null:
			return
		m.add_child(node)
		node.position = m.player.position - fwd0 * 5.0 + Vector3(-1.8, 1.0, 0)
		m.companion_node = node
		m._sparkle_burst(node.position + Vector3(0, 1.5, 0), Color(1.0, 0.8, 0.6))
		if not m.companion_greeted:
			m.companion_greeted = true
			var d := active_def()
			m.show_msg(String(d["name"]), "Here I am! Let's explore together!", "talk")
	# hide during minigames/castle so it never photobombs an arena (the battle
	# builds its own painted copy of the creature)
	m.companion_node.visible = m.game == ""
	if m.game != "":
		return
	var t: float = Time.get_ticks_msec() / 1000.0
	var fwd := Vector3(sin(m.player.yaw), 0, cos(m.player.yaw))
	var right := Vector3(cos(m.player.yaw), 0, -sin(m.player.yaw))
	# P2 casual co-op: while a pad holds R1, its left stick steers the stuffie
	# (player.gd mutes its own pad-move contribution while companion_p2 is on)
	m.companion_p2 = m.joy_pressed(JOY_BUTTON_RIGHT_SHOULDER)
	if m.companion_p2:
		var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
		var jy: float = m.joy_axis(JOY_AXIS_LEFT_Y)
		var drive := Vector3(jx, 0, jy)
		if drive.length() > 0.2:
			var vel: Vector3 = (fwd * -drive.z + right * drive.x).limit_length(1.0) * 17.0
			m.companion_node.position += vel * delta
			m.companion_node.rotation.y = lerp_angle(m.companion_node.rotation.y, atan2(vel.z, -vel.x), 1.0 - pow(0.02, delta))
		# rubber-band leash so P2 can never lose the stuffie off-screen
		var leash: Vector3 = m.companion_node.position - m.player.position
		if leash.length() > 45.0:
			m.companion_node.position = m.player.position + leash.limit_length(45.0)
	else:
		var want: Vector3 = m.player.position - fwd * 4.2 - right * 2.6 + Vector3(0, 1.0, 0)
		want += Vector3(sin(t * 0.8) * 0.7, sin(t * 1.3) * 0.5, cos(t * 1.0) * 0.7)
		var to_want: Vector3 = want - m.companion_node.position
		var d2: float = to_want.length()
		if d2 > 70.0:
			m.companion_node.position = want
		elif d2 > 0.05:
			var spd: float = clampf(d2 * 1.8, 2.5, 22.0)
			m.companion_node.position += to_want.limit_length(spd * delta)
		var face: Vector3 = to_want if d2 > 1.6 else (m.player.position - m.companion_node.position)
		if Vector2(face.x, face.z).length() > 0.3:
			m.companion_node.rotation.y = lerp_angle(m.companion_node.rotation.y, atan2(face.z, -face.x), 1.0 - pow(0.03, delta))
	m.companion_node.position.y = maxf(m.companion_node.position.y, ReefMain.seabed_y(m.companion_node.position.x, m.companion_node.position.z) + 1.4)
	_drive_gait(m.companion_node, m.companion_node.position.distance_to(m.player.position))
	# helper beats: cheer beside a resting Roshan; every so often dash toward
	# the nearest unfound friend so the stuffie SHOWS the way (visual pointer)
	m.companion_cool -= delta
	m.companion_cheer_t -= delta
	var pd: float = m.companion_node.position.distance_to(m.player.position)
	if m.companion_cool <= 0.0 and pd < 6.5 and m.player.vel.length() < 3.0:
		m.companion_cool = 14.0
		m.companion_cheer_t = 1.4
		m._greet_heart(m.companion_node.position + Vector3(0, 2.4, 0))
	m.companion_guide_cool -= delta
	if m.companion_guide_cool <= 0.0 and not m.companion_p2:
		m.companion_guide_cool = 22.0
		var target := _nearest_unfound_friend()
		if target != Vector3.ZERO and target.distance_to(m.player.position) < 120.0:
			var dir: Vector3 = (target - m.companion_node.position).normalized()
			var dash_to: Vector3 = m.companion_node.position + dir * 9.0
			var tw: Tween = m.companion_node.create_tween()
			tw.tween_property(m.companion_node, "position", dash_to, 0.9).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			m._sparkle_burst(dash_to, Color(1.0, 0.94, 0.4))
			var d := active_def()
			m.show_msg(String(d["name"]), "This way! I can feel a friend sparkling over here!", "talk")

func _drive_gait(node: Node3D, dist: float) -> void:
	# rigged craft creatures carry their AnimationPlayer in meta "ap"
	# (idle/walk/run/happy clips); billboard fallbacks animate themselves
	var ap_v: Variant = node.get_meta("ap") if node.has_meta("ap") else null
	if ap_v == null or not (ap_v is AnimationPlayer):
		return
	var ap := ap_v as AnimationPlayer
	var clip := "idle"
	if m.companion_cheer_t > 0.0:
		clip = "happy"
	elif dist > 9.0:
		clip = "run"
	elif dist > 4.5:
		clip = "walk"
	if ap.has_animation(clip) and ap.current_animation != clip:
		ap.play(clip, 0.25)

func _nearest_unfound_friend() -> Vector3:
	var best := Vector3.ZERO
	var best_d := INF
	for f in m.friends:
		if bool(f["found"]):
			continue
		var node: Sprite3D = f["node"]
		if not is_instance_valid(node):
			continue
		var dd: float = node.position.distance_to(m.player.position)
		if dd < best_d:
			best_d = dd
			best = node.position
	return best

# ---------- sparkle-fish tokens (incremental upgrades) ----------

func _tick_tokens(delta: float) -> void:
	if m.game != "":
		return
	if m.companion_tokens.is_empty():
		_build_tokens()
	var now: float = Time.get_ticks_msec() / 1000.0
	for row_v: Variant in m.companion_tokens:
		var row: Dictionary = row_v
		if row["node"] == null:
			row["timer"] = float(row["timer"]) - delta
			if float(row["timer"]) <= 0.0:
				_spawn_token(row)
			continue
		var node: Node3D = row["node"]
		if not is_instance_valid(node):
			row["node"] = null
			row["timer"] = TOKEN_RESPAWN
			continue
		var base: Vector3 = row["base"]
		node.position = base + Vector3(0, sin(now * 2.0 + float(row["phase"])) * 0.6, 0)
		node.rotation.y += delta * 1.5
		var near_player: bool = node.position.distance_to(m.player.position) < TOKEN_RADIUS
		var near_pal: bool = m.companion_node != null and is_instance_valid(m.companion_node) \
			and node.position.distance_to(m.companion_node.position) < TOKEN_RADIUS
		if near_player or near_pal:
			_collect_token(row, near_pal and not near_player)

func _build_tokens() -> void:
	for i in range(TOKEN_TOTAL):
		var x: float = ReefMain.hash2(float(i) * 3.7, 21.0) * 190.0 - 95.0
		var z: float = ReefMain.hash2(float(i) * 5.3, 47.0) * 190.0 - 95.0
		var base := Vector3(x, ReefMain.seabed_y(x, z) + 3.5 + ReefMain.hash2(float(i), 9.0) * 4.0, z)
		var row := {"base": base, "node": null, "timer": 0.0, "phase": float(i) * 1.7}
		_spawn_token(row)
		m.companion_tokens.append(row)

func _spawn_token(row: Dictionary) -> void:
	var node := m._make_creature_node("fish", Color(1.0, 0.85, 0.35), Color(1.0, 0.95, 0.7))
	if node == null:
		return
	m.add_child(node)
	node.scale = Vector3.ONE * 0.55
	node.position = row["base"]
	var halo := Label3D.new()
	halo.text = "✦"
	halo.font_size = 130
	halo.pixel_size = 0.02
	halo.outline_size = 20
	halo.modulate = Color(1.0, 0.9, 0.4, 0.9)
	halo.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	halo.no_depth_test = true
	halo.position = Vector3(0, 4.5, 0)
	node.add_child(halo)
	row["node"] = node
	row["timer"] = 0.0

func _collect_token(row: Dictionary, by_pal: bool) -> void:
	var node: Node3D = row["node"]
	row["node"] = null
	row["timer"] = TOKEN_RESPAWN
	m.fish_tokens += 1
	if is_instance_valid(node):
		m._sparkle_burst(node.position + Vector3(0, 1.0, 0), Color(1.0, 0.9, 0.4))
		node.queue_free()
	if m.chime != null:
		m.chime.pitch_scale = 1.3
		m.chime.play()
	var d := active_def()
	if by_pal:
		m.show_msg(String(d["name"]), "Yum, a sparkle fish! I feel stronger! Level %d!" % level(), "talk")
		if m.companion_node != null and is_instance_valid(m.companion_node):
			m.companion_cheer_t = 1.2
			m._greet_heart(m.companion_node.position + Vector3(0, 2.4, 0))
	else:
		m.show_msg("Roshan", "A sparkle fish for %s! Level %d!" % [String(d["name"]), level()], "talk")
	m._write_save()

# ---------- the sparring den (battle entrance) ----------

func _tick_den(delta: float) -> void:
	if m.game != "":
		return
	if m.companion_den == null or not is_instance_valid(m.companion_den):
		_build_den()
	if m.companion_den == null:
		return
	var t: float = Time.get_ticks_msec() / 1000.0
	var pointer_node: Label3D = m.companion_den.get_meta("pointer")
	if is_instance_valid(pointer_node):
		pointer_node.position.y = 11.0 + sin(t * 4.0) * 0.6
	m.stuffie_cool = maxf(0.0, m.stuffie_cool - delta)
	if m.stuffie_cool <= 0.0 and m.companion_den.position.distance_to(m.player.position) < DEN_RADIUS:
		m.stuffie_cool = 14.0
		m._start_stuffie_battle()

func _build_den() -> void:
	if m.wreck_pos == Vector3.ZERO:
		return
	var x: float = m.wreck_pos.x + 34.0
	var z: float = m.wreck_pos.z + 20.0
	var root := Node3D.new()
	root.position = Vector3(x, ReefMain.seabed_y(x, z) + 1.0, z)
	m.add_child(root)
	m.companion_den = root
	# pastel star-post ring — the "toy tournament" mat
	for i in range(6):
		var a: float = float(i) * TAU / 6.0
		var post := MeshInstance3D.new()
		var cm := CylinderMesh.new()
		cm.top_radius = 0.45
		cm.bottom_radius = 0.6
		cm.height = 4.0
		cm.radial_segments = 10
		post.mesh = cm
		post.position = Vector3(cos(a) * 7.5, 2.0, sin(a) * 7.5)
		var pm := StandardMaterial3D.new()
		pm.albedo_color = Color.from_hsv(float(i) / 6.0, 0.35, 1.0)
		pm.emission_enabled = true
		pm.emission = pm.albedo_color
		pm.emission_energy_multiplier = 0.3
		post.material_override = pm
		root.add_child(post)
		var star := Label3D.new()
		star.text = "⭐"
		star.font_size = 110
		star.pixel_size = 0.02
		star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		star.position = post.position + Vector3(0, 3.0, 0)
		root.add_child(star)
	var mat_disc := MeshInstance3D.new()
	var dm := CylinderMesh.new()
	dm.top_radius = 8.0
	dm.bottom_radius = 8.0
	dm.height = 0.4
	dm.radial_segments = 24
	mat_disc.mesh = dm
	mat_disc.position = Vector3(0, 0.2, 0)
	var dmat := StandardMaterial3D.new()
	dmat.albedo_color = Color(0.75, 0.62, 0.92)
	mat_disc.material_override = dmat
	root.add_child(mat_disc)
	var pointer := Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 150
	pointer.pixel_size = 0.022
	pointer.outline_size = 24
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	pointer.no_depth_test = true
	pointer.position = Vector3(0, 11.0, 0)
	root.add_child(pointer)
	root.set_meta("pointer", pointer)
	if not m.companion_den_said:
		m.companion_den_said = true
		var d := active_def()
		m.show_msg(String(d["name"]), "Look, a sparkle ring! Let's play-battle with the mischief imps!", "talk")
