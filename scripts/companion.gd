class_name CompanionSystem
extends RefCounted
# THE STUFFED-FRIEND COMPANION WING (Pokemon-style, no fail states).
# Phase-7 satellite: ALL mutable state stays on ReefMain (m.companion_*,
# m.care_points, m.stuffie_wins) — this class owns only roster data, the
# throne gift + picker flow, the overworld follower, fish-token pickups,
# and the sparring-den entrance. The battle itself is scripts/stuffie_battle.gd.
#
# Flow: reach Princess Huluu at the Pearl Castle throne → a gift box appears
# beside the Crown Star → pick a stuffie friend + paint its three colours →
# it follows Roshan through the reef, cheers, guides, and grows through
# Tamagotchi-style CARE (want bubbles → tap → care moment → +1 point). The
# sparkle ring near the shipwreck starts the play-battle ladder, where boss
# stuffies can be befriended and taken home. A second player can steer it by
# holding R1 on a gamepad (battles read every pad natively, so P2 co-op
# there needs no mode at all).

var m: ReefMain

# Data-driven roster — THE core collection loop (owner 2026-07-20): battle a
# boss stuffie, BEFRIEND it, take it HOME to the Stuffie Den, carry it on
# future missions. Fields:
#   kind      → CREATURE_LAYERS/CRAFT_RIGGED key on main (paintable pipeline)
#   model     → direct .glb body instead (photo-scanned toys land this way —
#               Meshy photo→3D, same as the craft creatures were built)
#   locked    → stuffie_wins key that frees it ("" / absent = starter friend);
#               boss rounds set "friend_<id>" on victory (see _end_stuffie_battle)
#   paintable → false hides the palette (a captured toy comes as it is)
const ROSTER := [
	{"id": "eagle", "name": "Baby Eagle", "kind": "bird", "attack": "PECK",
		"body": Color(0.98, 0.72, 0.55), "accent": Color(1.0, 0.85, 0.40), "third": Color(1.0, 0.92, 0.55),
		"hello": "Baby Eagle flies with you now! Peck peck!",
		"pro": "Speedy wings and a quick peck!"},
	{"id": "mewsha", "name": "Mewsha", "kind": "cat", "attack": "CLAW",
		"body": Color(0.95, 0.70, 0.85), "accent": Color(0.60, 0.40, 0.90), "third": Color(0.97, 0.96, 0.93),
		"hello": "Mewsha pads along beside you now! Swish swish!",
		"pro": "Big brave claw swipes!"},
	{"id": "lamma", "name": "Lamb-a'", "kind": "lamb", "attack": "BOUNCE",
		"model": "res://assets/characters/lamb.glb", "model_scale": 2.6,
		"emoji": "🐑", "paintable": false, "locked": "friend_lamma",
		"body": Color(1.0, 0.99, 0.95), "accent": Color(1.0, 0.80, 0.88), "third": Color(0.95, 0.92, 0.97),
		"hello": "Lamb-a' bounces along beside you now! Baa baa!",
		"pro": "Big fluffy bounce attacks!"},
]

const PALETTE := [
	Color(0.98, 0.55, 0.65), Color(1.0, 0.72, 0.42), Color(1.0, 0.9, 0.45),
	Color(0.55, 0.9, 0.6), Color(0.45, 0.82, 0.95), Color(0.62, 0.55, 0.95),
	Color(0.95, 0.7, 0.9), Color(0.97, 0.96, 0.93),
]
const COLOR_SLOTS := ["body", "accent", "third"]
const SLOT_ICON := ["🎨", "✨", "🤍"]

const GIFT_RADIUS := 6.5
const DEN_RADIUS := 9.0
const CARE_RADIUS := 6.5          # how close Roshan must be to tend a want

# TAMAGOTCHI CARE (owner 2026-07-20: replaces the sparkle-fish collectible
# model). The stuffie sometimes shows a want bubble; Roshan swims over and
# taps it; a little care moment plays and it grows (+1 care point). GENTLE
# by design: one want at a time, wants wait forever, nothing ever decays,
# gets sick or is lost — an ignored stuffie just keeps asking sweetly.
const WANTS := [
	{"id": "feed", "emoji": "🍎", "ask": "%s is hungry! Tap your stuffie to share a snack!", "done": "Munch munch munch! Yummy!"},
	{"id": "nap", "emoji": "💤", "ask": "%s is sleepy! Tap your stuffie for a little nap!", "done": "Zzz... what a cozy nap!"},
	{"id": "bath", "emoji": "🫧", "ask": "%s wants a bubble bath! Tap your stuffie to scrub-a-dub!", "done": "All clean and extra fluffy!"},
	{"id": "cuddle", "emoji": "❤", "ask": "%s wants a cuddle! Tap your stuffie for a big hug!", "done": "Best. Hug. Ever!"},
	{"id": "play", "emoji": "🎾", "ask": "%s wants to play! Tap your stuffie for zoomies!", "done": "Wheee! That was so fun!"},
]
const WANT_GAP_MIN := 45.0        # quiet time between fulfilled want and the next ask
const WANT_GAP_MAX := 75.0
const LEVEL_EVERY := 4            # care points per level-up celebration

func _init(main: ReefMain) -> void:
	m = main

func def_by_id(id: String) -> Dictionary:
	for d: Dictionary in ROSTER:
		if String(d["id"]) == id:
			return d
	return {}

func unlocked(id: String) -> bool:
	var d := def_by_id(id)
	if d.is_empty():
		return false
	var key := String(d.get("locked", ""))
	return key == "" or bool(m.stuffie_wins.get(key, false))

func unlocked_defs() -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	for d: Dictionary in ROSTER:
		if unlocked(String(d["id"])):
			out.append(d)
	return out

func active_def() -> Dictionary:
	return def_by_id(m.companion_id)

func level() -> int:
	# Tamagotchi track (owner 2026-07-20): every fulfilled want = +1 care
	# point; care is the ONLY way the stuffie grows (replaces fish tokens —
	# old token progress was migrated into care_points on first load)
	return m.care_points

func stage() -> int:
	# the friendly display level: 1 + a star per LEVEL_EVERY care points
	return 1 + int(m.care_points / LEVEL_EVERY)

func tier() -> int:
	# battle ability milestones now ride the care stages too (0..6)
	return clampi(int(m.care_points / LEVEL_EVERY), 0, 6)

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

func creature_for(d: Dictionary, c: Array[Color]) -> Node3D:
	if d.is_empty():
		return null
	# photo-scanned / direct-model toys skip the paint pipeline and load as-is
	if d.has("model"):
		var ps: PackedScene = load(String(d["model"]))
		if ps == null:
			return null
		var wrap := Node3D.new()
		var inst: Node3D = ps.instantiate() as Node3D
		if inst == null:
			return null
		inst.scale = Vector3.ONE * float(d.get("model_scale", 2.6))
		wrap.add_child(inst)
		return wrap
	return m._make_creature_node(String(d["kind"]), c[0], c[1], false, false, c[2])

func make_creature() -> Node3D:
	return creature_for(active_def(), colors())

# ===================== per-frame tick (called from main._process) =====================

# the free-roam worlds where the stuffie tags along (owner 2026-07-19: it
# follows ALL the time) — self-driven modes (kart, slides, battles, 2D
# canvas games…) still hide it so it never photobombs an engine's camera
const FOLLOW_GAMES := ["", "level2", "north"]

func _follow_ctx() -> bool:
	return m.game in FOLLOW_GAMES

func tick(delta: float) -> void:
	if m.player == null or m.intro_active:
		return
	_tick_gift(delta)
	_tick_room(delta)
	if m.companion_id == "":
		return
	# ZONE WATCH (owner 2026-07-20: "sometimes gets lost"): whenever the game
	# context flips (reef ↔ lagoon ↔ castle ↔ north ↔ any engine and back),
	# snap the stuffie straight to Roshan's side — never left behind, never
	# waiting outside a door she came out of somewhere else
	if m.game != m.companion_zone:
		m.companion_zone = m.game
		if _follow_ctx() and m.companion_node != null and is_instance_valid(m.companion_node):
			var zfwd := Vector3(sin(m.player.yaw), 0, cos(m.player.yaw))
			var zright := Vector3(cos(m.player.yaw), 0, -sin(m.player.yaw))
			m.companion_node.position = m.player.position - zfwd * 4.2 - zright * 2.6 + Vector3(0, 1.0, 0)
			m._sparkle_burst(m.companion_node.position + Vector3(0, 1.5, 0), Color(1.0, 0.8, 0.6))
	_tick_follower(delta)
	_tick_care(delta)
	_tick_den(delta)

# ---------- the throne gift (unlock moment) ----------

func _tick_gift(delta: float) -> void:
	# THE OFFER (owner 2026-07-19): meeting Princess Huluu IS the trigger.
	# A breath after her throne greeting she says her line — "I want you to
	# have a new friend!" — and the picker opens right there. The gift box
	# beside the Crown Star remains only as the re-entry if the picker is
	# closed without choosing.
	var in_hall: bool = m.game == "level2" and String(m.g.get("phase", "court")) == "hall"
	if not in_hall or m.companion_id != "":
		if m.companion_gift != null and is_instance_valid(m.companion_gift):
			m._sparkle_burst(m.companion_gift.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.8, 0.9))
			m.companion_gift.queue_free()   # opened! (castle teardown also covers it via game_nodes)
		m.companion_gift = null
		return
	if not bool(m.g.get("huluu_greeted", false)):
		return
	if not bool(m.g.get("companion_offered", false)):
		if m.companion_layer != null:
			return
		# let Huluu's greeting line breathe before her offer
		var wait: float = float(m.g.get("companion_offer_t", 2.8)) - delta
		m.g["companion_offer_t"] = wait
		if wait <= 0.0:
			m.g["companion_offered"] = true
			open_picker(false)
			m.show_msg("Princess Huluu", "I want you to have a new friend! Pick Mewsha or Baby Eagle to come along!", "talk")
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
		m.show_msg("Princess Huluu", "Changed your mind? Your new friend waits in the gift box - tap it any time!", "talk")

func _action_down() -> bool:
	var down := Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	if m.touch_ui != null and bool(m.touch_ui.action_down):
		down = true
	return down

# ---------- the picker + colour studio overlay ----------

func open_picker(say_prompt: bool = true, preselect: String = "") -> void:
	# say_prompt=false when Princess Huluu herself makes the offer — her
	# "I want you to have a new friend!" line owns that moment.
	# preselect: the Stuffie Den shelves open the picker on the tapped friend.
	if m.companion_layer != null:
		return
	if not def_by_id(preselect).is_empty():
		m.companion_pick_id = preselect
	else:
		m.companion_pick_id = String(ROSTER[0]["id"]) if m.companion_id == "" else m.companion_id
	_reset_pick_colors()
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
	if say_prompt:
		m.show_msg("Roshan", "Which stuffie friend comes with me? Tap one, then paint its colors!", "talk")

func _on_picker_dim_input(ev: InputEvent) -> void:
	if ev is InputEventMouseButton and (ev as InputEventMouseButton).pressed:
		close_picker()

func close_picker() -> void:
	if m.companion_layer != null and is_instance_valid(m.companion_layer):
		m.companion_layer.queue_free()
	m.companion_layer = null
	m.companion_stage = null

func _reset_pick_colors() -> void:
	# repainting the CURRENT friend starts from its saved coat, a new friend
	# from its book-art defaults
	m.companion_pick_colors = []
	if m.companion_pick_id == m.companion_id and m.companion_colors.size() == 3:
		m.companion_pick_colors = m.companion_colors.duplicate()
		return
	var d := def_by_id(m.companion_pick_id)
	for slot in COLOR_SLOTS:
		m.companion_pick_colors.append((d[slot] as Color).to_html(false))

func _pick_friend(id: String) -> void:
	m.companion_pick_id = id
	_reset_pick_colors()
	var d := def_by_id(id)
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
	if m.companion_room != null and is_instance_valid(m.companion_room):
		m.companion_room.queue_free()   # rebuilt next tick: heart + coat move shelves
		m.companion_room = null
		m.companion_room_rows = []
	# a swap resets any pending want (care progress itself is shared — it is
	# HER nurturing that grows, whichever friend she carries)
	m.companion_want = ""
	m.companion_care_t = -1.0
	if m.companion_want_bubble != null and is_instance_valid(m.companion_want_bubble):
		m.companion_want_bubble.queue_free()
	m.companion_want_bubble = null
	m.companion_want_cool = 20.0
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
	# friend cards down the left — only friends who already live at home;
	# captured bosses appear here the moment their battle is won
	var picks := unlocked_defs()
	var step: float = minf(250.0, 560.0 / maxf(float(picks.size()), 1.0))
	for i in range(picks.size()):
		var d: Dictionary = picks[i]
		var id := String(d["id"])
		var card := Button.new()
		card.position = Vector2(80, 130 + float(i) * step)
		card.custom_minimum_size = Vector2(330, step - 25.0)
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
		_add_creature_preview(card, d, Vector2(12, 12), Vector2(150, step - 50.0),
			(d["body"] as Color), (d["accent"] as Color))
		var nm := Label.new()
		nm.text = String(d["name"])
		nm.add_theme_font_size_override("font_size", 26)
		nm.add_theme_color_override("font_color", Color(1.0, 0.96, 0.80))
		nm.position = Vector2(172, 24)
		nm.size = Vector2(150, step - 100.0)
		nm.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		card.add_child(nm)
		var atk := Label.new()
		atk.text = ("🐦 " if String(d["kind"]) == "bird" else "🐾 ") + String(d["attack"])
		atk.add_theme_font_size_override("font_size", 24)
		atk.add_theme_color_override("font_color", Color(0.74, 0.96, 0.88))
		atk.position = Vector2(172, step - 82.0)
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
	_add_creature_preview(preview_panel, pick_def, Vector2(14, 14), Vector2(302, 302), pc0, pc1)
	# three colour rows on the right (a captured toy comes exactly as it is)
	if not bool(pick_def.get("paintable", true)):
		var asis := Label.new()
		asis.text = "💕  %s comes just as she is!" % String(pick_def["name"])
		asis.add_theme_font_size_override("font_size", 27)
		asis.add_theme_color_override("font_color", Color(1.0, 0.85, 0.92))
		asis.position = Vector2(830, 240)
		asis.size = Vector2(400, 120)
		asis.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		stage.add_child(asis)
	for slot in range(3 if bool(pick_def.get("paintable", true)) else 0):
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

func _add_creature_preview(parent: Control, d: Dictionary, box_pos: Vector2, box_size: Vector2, body: Color, accent: Color) -> void:
	# layered book-art preview (assets/mg fish/cat/bird sheets), live-tinted —
	# the same sheets the craft creatures use, so the paint matches in-world.
	# The sheets are large illustrations: FIT them into the given box (uniform
	# scale, centered) instead of trusting any fixed scale, and paint in the
	# in-world order — body first, accent OVER it, ink line on top.
	# Model-based toys (captured / photo-scanned) have no paint sheets: show
	# their big friendly emoji instead — the Den shelf carries the real 3D body.
	parent.clip_contents = true
	if d.has("model") or not m.CREATURE_LAYERS.has(String(d.get("kind", ""))):
		var face := Label.new()
		face.text = String(d.get("emoji", "🧸"))
		face.add_theme_font_size_override("font_size", int(minf(box_size.x, box_size.y) * 0.62))
		face.position = box_pos
		face.size = box_size
		face.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		face.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		face.mouse_filter = Control.MOUSE_FILTER_IGNORE
		parent.add_child(face)
		return
	var kind := String(d["kind"])
	var layer_names: Array = m.CREATURE_LAYERS.get(kind, m.CREATURE_LAYERS["fish"])
	var draw_order: Array = [1, 0, 2]   # body, accent, line (matches _make_creature_node)
	var tints: Array[Color] = [body, accent, Color.WHITE]
	var ref_tex: Texture2D = null
	for li in range(3):
		var probe_path := "res://assets/mg/" + String(layer_names[li]) + ".png"
		if ResourceLoader.exists(probe_path):
			ref_tex = load(probe_path)
			break
	if ref_tex == null:
		return
	var ts: Vector2 = ref_tex.get_size()
	var fit: float = minf(box_size.x / maxf(ts.x, 1.0), box_size.y / maxf(ts.y, 1.0))
	var origin: Vector2 = box_pos + (box_size - ts * fit) * 0.5
	parent.clip_contents = true   # nothing ever spills over the card/frame edge
	for i in range(3):
		var tex_path := "res://assets/mg/" + String(layer_names[int(draw_order[i])]) + ".png"
		if not ResourceLoader.exists(tex_path):
			continue
		var tr := TextureRect.new()
		tr.texture = load(tex_path)
		tr.position = origin
		tr.scale = Vector2.ONE * fit
		tr.modulate = tints[i]
		tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		parent.add_child(tr)

# ---------- the Stuffie Den (owner 2026-07-19: a castle room where every
# ---------- stuffed friend sits on the wall shelves, swappable any time) ----------

const ROOM_LOCAL := Vector3(-49.4, 49.6, -44.0)   # west end of the Dreaming
# Floor corridor (Wacky & Chuck's basket holds the east end); CASTLE_POS-relative

func _tick_room(delta: float) -> void:
	var in_hall: bool = m.game == "level2" and String(m.g.get("phase", "court")) == "hall"
	if not in_hall:
		m.companion_room = null   # castle teardown frees the nodes via game_nodes
		m.companion_room_rows = []
		return
	if m.companion_room == null or not is_instance_valid(m.companion_room):
		_build_room()
	if m.companion_room == null:
		return
	var now: float = Time.get_ticks_msec() / 1000.0
	var pointer_node: Label3D = m.companion_room.get_meta("pointer")
	if is_instance_valid(pointer_node):
		pointer_node.position.y = 9.4 + sin(now * 4.0) * 0.4
	# one-time welcome once she wanders into the nook
	if not bool(m.g.get("companion_room_said", false)) \
			and m.companion_room.global_position.distance_to(m.player.position) < 13.0:
		m.g["companion_room_said"] = true
		m.show_msg("Roshan", "The Stuffie Den! All my friends live here - tap one to bring it along!", "talk")
	var best_id := ""
	var best_d := 6.0
	for row_v: Variant in m.companion_room_rows:
		var row: Dictionary = row_v
		var node: Node3D = row["node"]
		if not is_instance_valid(node):
			continue
		var mine: bool = String(row["id"]) == m.companion_id
		var home: bool = bool(row.get("home", true))
		var marker: Label3D = row["marker"]
		var heart: Label3D = row["heart"]
		if is_instance_valid(marker):
			marker.visible = home and not mine
			marker.modulate.a = 0.72 + sin(now * 3.0 + float(row["phase"])) * 0.22
		if is_instance_valid(heart):
			heart.visible = mine
		var dist: float = node.global_position.distance_to(m.player.position)
		if dist < best_d:
			best_d = dist
			best_id = String(row["id"])
	var action: bool = _action_down()
	if best_id != "" and action and not m.companion_room_action_prev and m.companion_layer == null:
		var d := def_by_id(best_id)
		if not unlocked(best_id):
			# an empty mystery shelf: point her at the capture loop, no picker
			m.show_msg("Roshan", "Someone could live on this shelf! Win the toy tournament in the reef and bring a new friend home!", "talk")
		else:
			open_picker(false, best_id)
			if best_id == m.companion_id:
				m.show_msg("Roshan", "New colors for %s? Paint away!" % String(d["name"]), "talk")
			else:
				m.show_msg(String(d["name"]), "Pick me! I'll come along!", "talk")
	m.companion_room_action_prev = action

func _room_colors(id: String) -> Array[Color]:
	# the current friend keeps its painted coat on the shelf; the rest wear
	# their book-art defaults
	if id == m.companion_id:
		return colors()
	var d := def_by_id(id)
	var out: Array[Color] = []
	for slot in COLOR_SLOTS:
		out.append(d[slot] as Color)
	return out

func _build_room() -> void:
	var root := Node3D.new()
	root.position = m.CASTLE_POS + ROOM_LOCAL
	m.add_child(root)
	m.game_nodes.append(root)
	m.companion_room = root
	m.companion_room_rows = []
	# cozy dressing: lavender wall band, pastel rug, a soft emissive lamp
	var band := MeshInstance3D.new()
	var band_mesh := BoxMesh.new()
	band_mesh.size = Vector3(0.35, 7.0, 13.5)
	band.mesh = band_mesh
	band.position = Vector3(-3.0, 3.8, 0.0)
	band.material_override = _room_mat(Color(0.78, 0.68, 0.92), 0.12)
	root.add_child(band)
	var rug := MeshInstance3D.new()
	var rug_mesh := BoxMesh.new()
	rug_mesh.size = Vector3(6.4, 0.25, 12.8)
	rug.mesh = rug_mesh
	rug.position = Vector3(0.8, 0.15, 0.0)
	rug.material_override = _room_mat(Color(1.0, 0.82, 0.90))
	root.add_child(rug)
	var lamp := MeshInstance3D.new()
	var lamp_mesh := BoxMesh.new()
	lamp_mesh.size = Vector3(1.1, 1.1, 1.1)
	lamp.mesh = lamp_mesh
	lamp.position = Vector3(-2.4, 7.8, 0.0)
	lamp.material_override = _room_mat(Color(1.0, 0.9, 0.6), 3.0)
	root.add_child(lamp)
	var sign := Label3D.new()
	sign.text = "✨ Stuffie Den ✨"
	sign.font_size = 44
	sign.pixel_size = 0.008
	sign.outline_size = 11
	sign.modulate = Color(1.0, 0.9, 0.95)
	sign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sign.position = Vector3(0, 7.4, 0)
	root.add_child(sign)
	var pointer := Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 140
	pointer.pixel_size = 0.02
	pointer.outline_size = 22
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	pointer.no_depth_test = true
	pointer.position = Vector3(0, 9.4, 0)
	root.add_child(pointer)
	root.set_meta("pointer", pointer)
	# one wall shelf per stuffed friend, each seated and waiting
	for i in range(ROSTER.size()):
		var d: Dictionary = ROSTER[i]
		var id := String(d["id"])
		var shelf_z: float = -3.6 + float(i) * 7.2 - (float(ROSTER.size() - 2) * 3.6)
		var shelf := MeshInstance3D.new()
		var shelf_mesh := BoxMesh.new()
		shelf_mesh.size = Vector3(3.4, 0.5, 3.6)
		shelf.mesh = shelf_mesh
		shelf.position = Vector3(-1.5, 2.4, shelf_z)
		shelf.material_override = _room_mat(Color(0.95, 0.8, 0.35), 0.2)
		root.add_child(shelf)
		var is_home := unlocked(id)
		var creature: Node3D = null
		if is_home:
			creature = creature_for(d, _room_colors(id))
			if creature != null:
				creature.scale = Vector3.ONE * 0.75
				creature.position = Vector3(-1.5, 2.68, shelf_z)
				creature.rotation.y = PI   # gen2 face = -X, so PI looks out at the corridor
				root.add_child(creature)
		else:
			# a friend not yet befriended: an empty shelf with a big mystery mark
			var mystery := Label3D.new()
			mystery.text = "❓"
			mystery.font_size = 160
			mystery.pixel_size = 0.018
			mystery.outline_size = 16
			mystery.modulate = Color(0.75, 0.8, 0.95, 0.9)
			mystery.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			mystery.position = Vector3(-1.5, 4.2, shelf_z)
			root.add_child(mystery)
		var name_sign := Label3D.new()
		name_sign.text = String(d["name"]) if is_home else "❓❓❓"
		name_sign.font_size = 30
		name_sign.pixel_size = 0.008
		name_sign.outline_size = 9
		name_sign.modulate = Color(0.9, 0.95, 1.0)
		name_sign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		name_sign.position = Vector3(-1.2, 4.9, shelf_z)
		root.add_child(name_sign)
		var marker := Label3D.new()
		marker.text = "✦"
		marker.font_size = 120
		marker.pixel_size = 0.018
		marker.outline_size = 18
		marker.modulate = Color(1.0, 0.88, 0.35, 0.9)
		marker.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		marker.no_depth_test = true
		marker.position = Vector3(-1.2, 5.9, shelf_z)
		root.add_child(marker)
		var heart := Label3D.new()
		heart.text = "💗"
		heart.font_size = 100
		heart.pixel_size = 0.018
		heart.outline_size = 14
		heart.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		heart.no_depth_test = true
		heart.position = Vector3(-1.2, 5.9, shelf_z)
		heart.visible = false
		root.add_child(heart)
		m.companion_room_rows.append({"id": id, "node": creature if creature != null else shelf,
			"marker": marker, "heart": heart, "phase": float(i) * 1.7, "home": is_home})

func _room_mat(col: Color, emission: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.6
	if emission > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = emission
	return mat

# ---------- the overworld follower ----------

func _tick_follower(delta: float) -> void:
	# a node that something reclaimed (arena teardown, freed parent) counts as
	# lost — drop the handle so the respawn below brings the stuffie back
	if m.companion_node != null and (not is_instance_valid(m.companion_node) or not m.companion_node.is_inside_tree()):
		m.companion_node = null
	if m.companion_node == null:
		if not _follow_ctx():
			return   # spawn in a free-roam world, never mid-engine
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
	# tag along everywhere free-roam; hide only inside self-driven engines
	# (the battle builds its own painted copy of the creature)
	m.companion_node.visible = _follow_ctx()
	if not _follow_ctx():
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
	# per-world floor: reef seabed / lagoon terrain; castle + northern floors
	# are architectural, so there it simply keeps to Roshan's height band
	if m.game == "":
		m.companion_node.position.y = maxf(m.companion_node.position.y, ReefMain.seabed_y(m.companion_node.position.x, m.companion_node.position.z) + 1.4)
	elif m.game == "level2" and String(m.g.get("phase", "court")) == "court":
		m.companion_node.position.y = maxf(m.companion_node.position.y, m.lagoon_h(m.companion_node.position.x, m.companion_node.position.z) + 1.2)
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

# ---------- Tamagotchi care (the leveling system) ----------

func want_def(id: String) -> Dictionary:
	for w: Dictionary in WANTS:
		if String(w["id"]) == id:
			return w
	return {}

func _tick_care(delta: float) -> void:
	if not _follow_ctx() or m.companion_node == null or not is_instance_valid(m.companion_node):
		return
	# a care moment in progress owns the stuffie for a beat
	if m.companion_care_t > 0.0:
		m.companion_care_t -= delta
		if m.companion_care_t <= 0.0:
			_finish_care()
		return
	if m.companion_want == "":
		# quiet time, then the next gentle ask (never during the picker)
		if m.companion_layer != null:
			return
		m.companion_want_cool -= delta
		if m.companion_want_cool <= 0.0:
			_begin_want(String(WANTS[randi() % WANTS.size()]["id"]))
		return
	# a want is showing: keep the bubble riding above the stuffie
	var bubble: Label3D = m.companion_want_bubble
	if bubble == null or not is_instance_valid(bubble):
		_make_want_bubble()
		bubble = m.companion_want_bubble
	if bubble != null and is_instance_valid(bubble):
		var now: float = Time.get_ticks_msec() / 1000.0
		bubble.position = m.companion_node.position + Vector3(0, 4.6 + sin(now * 3.0) * 0.35, 0)
		bubble.scale = Vector3.ONE * (1.0 + sin(now * 5.0) * 0.08)
	# tend it: swim close and tap THE button
	var action: bool = _action_down()
	if action and not m.companion_care_action_prev \
			and m.companion_node.position.distance_to(m.player.position) < CARE_RADIUS \
			and m.companion_layer == null:
		_start_care()
	m.companion_care_action_prev = action

func _begin_want(id: String) -> void:
	var w := want_def(id)
	if w.is_empty():
		return
	m.companion_want = id
	_make_want_bubble()
	var d := active_def()
	m.show_msg(String(d["name"]), String(w["ask"]) % String(d["name"]), "talk")

func _make_want_bubble() -> void:
	if m.companion_want_bubble != null and is_instance_valid(m.companion_want_bubble):
		m.companion_want_bubble.queue_free()
	var w := want_def(m.companion_want)
	if w.is_empty() or m.companion_node == null or not is_instance_valid(m.companion_node):
		return
	var bubble := Label3D.new()
	bubble.text = String(w["emoji"])
	bubble.font_size = 150
	bubble.pixel_size = 0.02
	bubble.outline_size = 22
	bubble.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	bubble.no_depth_test = true
	m.add_child(bubble)
	m.companion_want_bubble = bubble

func _start_care() -> void:
	# the care moment: a short, readable animation per want, all analytic
	m.companion_care_t = 2.0
	if m.companion_want_bubble != null and is_instance_valid(m.companion_want_bubble):
		m.companion_want_bubble.queue_free()
		m.companion_want_bubble = null
	var pal: Node3D = m.companion_node
	var pos: Vector3 = pal.position
	match m.companion_want:
		"feed":
			var snack := Label3D.new()
			snack.text = "🍎"
			snack.font_size = 110
			snack.pixel_size = 0.02
			snack.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			snack.position = m.player.position + Vector3(0, 2.0, 0)
			m.add_child(snack)
			var tw: Tween = snack.create_tween()
			tw.tween_property(snack, "position", pos + Vector3(0, 2.2, 0), 0.7).set_trans(Tween.TRANS_QUAD)
			tw.tween_property(snack, "scale", Vector3.ZERO, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
			tw.tween_callback(snack.queue_free)
			_pal_bounce(1.15)
		"nap":
			var zzz := Label3D.new()
			zzz.text = "💤"
			zzz.font_size = 120
			zzz.pixel_size = 0.02
			zzz.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			zzz.position = pos + Vector3(0.8, 3.6, 0)
			m.add_child(zzz)
			var tz: Tween = zzz.create_tween()
			tz.tween_property(zzz, "position:y", pos.y + 6.0, 1.9)
			tz.parallel().tween_property(zzz, "modulate:a", 0.0, 1.9)
			tz.tween_callback(zzz.queue_free)
			_pal_bounce(0.9)
		"bath":
			for i in range(3):
				m._sparkle_burst(pos + Vector3(randf_range(-1.2, 1.2), 1.5 + float(i), randf_range(-1.2, 1.2)), Color(0.75, 0.92, 1.0))
			_pal_bounce(1.1)
		"cuddle":
			m._greet_heart(pos + Vector3(0, 2.6, 0))
			if m.player != null and m.player.has_method("play_verb"):
				m.player.play_verb("cheer")
			_pal_bounce(1.2)
		_:
			# play: happy zoomies — a quick circle dash with a sparkle trail
			var tw2: Tween = pal.create_tween()
			for i in range(4):
				var a: float = TAU * float(i + 1) / 4.0
				tw2.tween_property(pal, "position", pos + Vector3(cos(a) * 3.0, 0.6, sin(a) * 3.0), 0.35).set_trans(Tween.TRANS_SINE)
			m._sparkle_burst(pos + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.5))
	m.companion_cheer_t = 2.0   # rigged bodies play their "happy" clip

func _pal_bounce(peak: float) -> void:
	var pal: Node3D = m.companion_node
	if pal == null or not is_instance_valid(pal):
		return
	var base: Vector3 = pal.scale
	var tw: Tween = pal.create_tween()
	tw.tween_property(pal, "scale", base * peak, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(pal, "scale", base, 0.45).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)

func _finish_care() -> void:
	var w := want_def(m.companion_want)
	var d := active_def()
	m.companion_want = ""
	m.companion_want_cool = randf_range(WANT_GAP_MIN, WANT_GAP_MAX)
	m.care_points += 1
	if m.chime != null:
		m.chime.pitch_scale = 1.3
		m.chime.play()
	if m.companion_node != null and is_instance_valid(m.companion_node):
		m._greet_heart(m.companion_node.position + Vector3(0, 2.8, 0))
	if m.care_points % LEVEL_EVERY == 0:
		# LEVEL UP — a proper celebration: fanfare, sparkle ring, star pips
		m._reward(false)
		if m.companion_node != null and is_instance_valid(m.companion_node):
			for i in range(8):
				var a: float = TAU * float(i) / 8.0
				m._sparkle_burst(m.companion_node.position + Vector3(cos(a) * 2.2, 1.2, sin(a) * 2.2), Color.from_hsv(float(i) / 8.0, 0.5, 1.0))
		m.show_msg(String(d["name"]), "I grew SO big and strong! %s" % _star_pips(), "win")
	elif not w.is_empty():
		m.show_msg(String(d["name"]), String(w["done"]), "talk")
	m._write_save()

func _star_pips() -> String:
	# non-reader level display: stars, never numerals
	var stars := ""
	for i in range(mini(stage(), 8)):
		stars += "⭐"
	return stars

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
