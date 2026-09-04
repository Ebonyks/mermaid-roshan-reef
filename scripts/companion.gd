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
# boss stuffie, BEFRIEND it, take it HOME to the Stuffie Studio, carry it on
# future missions. Fields:
#   kind      → CREATURE_LAYERS key on main (paintable 2D layer pipeline)
#   sprite    → direct 2D cutout for a non-paintable captured friend
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
		"hello": "I'm coming along beside you now! Swish swish!",
		"pro": "Big brave claw swipes!"},
	{"id": "lamma", "name": "Lamb-a'", "kind": "lamb", "attack": "BOUNCE",
		"sprite": "res://assets/sprites/stuffie_studio/lamma.png",
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
# Post-battle care is an invitation, never a countdown. A gentle reminder may
# repeat while boo-boos remain, but waiting can never remove the friend, block
# play, erase progress, or add emotional pressure.
const CARE_REMINDER_GAP := 60.0

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
	return _stuffie_cutout(d, c, 3.8)

func make_creature() -> Node3D:
	return creature_for(active_def(), colors())

func _stuffie_cutout(d: Dictionary, c: Array[Color], target_height: float) -> Node3D:
	# Stuffies are deliberately flat storybook cutouts. This replaces the
	# retired GLB path for the follower, battle copy, and Studio display.
	var root := Node3D.new()
	root.name = "StuffieCutout_" + String(d.get("id", "friend"))
	var anim := Node3D.new()
	anim.name = "StorybookBob"
	root.add_child(anim)
	if d.has("sprite"):
		var direct_tex: Texture2D = load(String(d["sprite"]))
		if direct_tex == null:
			return null
		var direct := Sprite3D.new()
		direct.name = "StorybookSprite"
		direct.texture = direct_tex
		direct.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		direct.pixel_size = target_height / maxf(float(direct_tex.get_height()), 1.0)
		direct.render_priority = 2
		anim.add_child(direct)
	else:
		var kind := String(d.get("kind", ""))
		if not m.CREATURE_LAYERS.has(kind):
			return null
		var layer_names: Array = m.CREATURE_LAYERS[kind]
		var body_tex: Texture2D = load("res://assets/mg/" + String(layer_names[1]) + ".png")
		if body_tex == null:
			return null
		var pixel: float = target_height / maxf(float(body_tex.get_height()), 1.0)
		var draw_order: Array = [1, 0, 2]
		var tints: Array[Color] = [c[0], c[1], Color.WHITE]
		for i in range(draw_order.size()):
			var layer_index: int = int(draw_order[i])
			var tex: Texture2D = load("res://assets/mg/" + String(layer_names[layer_index]) + ".png")
			if tex == null:
				continue
			var layer := Sprite3D.new()
			layer.name = "StorybookLayer_%d" % i
			layer.texture = tex
			layer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			layer.pixel_size = pixel
			layer.render_priority = i
			layer.modulate = tints[i]
			anim.add_child(layer)
	root.set_meta("storybook_sprite", true)
	return root

# ===================== per-frame tick (called from main._process) =====================

# The stuffie follows EVERYWHERE (owner 2026-07-19/21: all of the time —
# it kept vanishing in levels an allow-list never heard of). Inverted to a
# HIDE-list mirroring player.gd's self-driven modes: only engines that own
# the player/camera themselves (racers, stages, battles, room sequencers)
# park the stuffie, so every new explorable level follows by default.
const HIDE_GAMES := ["kart", "galaxy", "combat", "stuffie", "dungeon", "emberdun",
	"opera", "dolls", "slide", "fairyshoot", "brawl"]

func _follow_ctx() -> bool:
	if m.game == "level2" \
			and String(m.g.get("phase", "court")) == "hall":
		return false
	return m.game not in HIDE_GAMES

func tick(delta: float) -> void:
	_ensure_menu_button()
	_sync_menu_button()
	if m.player == null or m.intro_active:
		return
	# The retired free-roaming castle used modeled gift/Stuffie Den builders
	# here. The picture-first castle exposes the picker from its Playroom
	# action instead, so no companion world geometry is built in the hall phase.
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

# ---------- the inset HUD launcher + Tamagotchi care sheet ----------

func _ensure_menu_button() -> void:
	if m.companion_menu_button != null and is_instance_valid(m.companion_menu_button):
		return
	if m.hud_layer == null:
		return
	var button := Button.new()
	button.name = "StuffieCareMenuButton"
	# Upper-right hand area, intentionally left of both the Critter Book and the
	# pause-owned far corner; all three targets keep a visible finger-width gap.
	button.position = Vector2(858, 22)
	StorybookUI.style_icon_button(button, "🧸", "secondary", Vector2(128, 128), "Care for your stuffie")
	StorybookUI.add_shell_crest(button, Rect2(34, 72, 60, 45), "StuffieWatchShell")
	button.set_meta("hud_zone", "upper_right_inset")
	button.pressed.connect(open_care_menu)
	m.hud_layer.add_child(button)
	m.companion_menu_button = button

func _sync_menu_button() -> void:
	var button: Button = m.companion_menu_button
	if button == null or not is_instance_valid(button):
		return
	button.visible = m.companion_id != "" and _follow_ctx() and not m.intro_active \
		and m.companion_care_layer == null and m.companion_layer == null
	if not button.visible:
		return
	var icon := "🧸"
	var kind := "secondary"
	if m.companion_bruises > 0:
		icon = "🩹"
		kind = "action"
	elif m.companion_want != "":
		var want := want_def(m.companion_want)
		icon = String(want.get("emoji", "♥"))
		kind = "gold"
	if button.text != icon or String(button.get_meta("storybook_kind", "")) != kind:
		StorybookUI.style_icon_button(button, icon, kind, Vector2(128, 128), "Care for your stuffie")
	button.pivot_offset = button.size * 0.5
	if kind != "secondary":
		var now: float = Time.get_ticks_msec() / 1000.0
		button.scale = Vector2.ONE * (1.0 + sin(now * 4.0) * 0.08)
	else:
		button.scale = Vector2.ONE


func open_care_menu() -> void:
	if m.companion_id == "" or m.companion_care_layer != null or m.companion_layer != null:
		return
	if not _follow_ctx() or m.intro_active:
		return
	m.companion_care_layer = CanvasLayer.new()
	m.companion_care_layer.layer = 25
	m.add_child(m.companion_care_layer)
	var root_control := Control.new()
	root_control.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.companion_care_layer.add_child(root_control)
	var dim := StorybookUI.add_dim(root_control)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	dim.gui_input.connect(_on_care_dim_input)
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	m.companion_care_stage = StorybookUI.add_stage(root_control, viewport_size)
	if m.player != null:
		m.player.vel = Vector3.ZERO
	_draw_care_menu()
	var d := active_def()
	if m.companion_want != "":
		var w := want_def(m.companion_want)
		m.show_msg(String(d["name"]), String(w.get("ask", "Tap what I need!")) % String(d["name"]), "talk")
	elif not m.companion_want_queue.is_empty():
		var queued := want_def(String(m.companion_want_queue[0]))
		m.show_msg(String(d["name"]), String(queued.get("ask", "Tap the glowing care picture!")) % String(d["name"]), "talk")
	else:
		m.show_msg(String(d["name"]), "Care and happy play fill my next upgrade star! What should we do together?", "talk")

func _on_care_dim_input(ev: InputEvent) -> void:
	if ev is InputEventMouseButton and (ev as InputEventMouseButton).pressed:
		close_care_menu()

func close_care_menu() -> void:
	if m.companion_care_layer != null and is_instance_valid(m.companion_care_layer):
		m.companion_care_layer.queue_free()
	m.companion_care_layer = null
	m.companion_care_stage = null

func _draw_care_menu() -> void:
	var stage_control: Control = m.companion_care_stage
	if stage_control == null or not is_instance_valid(stage_control):
		return
	for child: Node in stage_control.get_children():
		child.queue_free()
	var d := active_def()
	var care_rect := Rect2(38, 24, 1204, 672)
	var panel := StorybookUI.add_panel(stage_control, care_rect, StorybookUI.PURPLE, Color(0.91, 0.97, 1.0, 0.99), 48)
	panel.name = "StuffieCareShell"
	StorybookUI.adorn_panel(stage_control, care_rect, "StuffieCare")
	var title := Label.new()
	title.text = "♥  ⭐  %s" % String(d["name"])
	title.position = Vector2(72, 42)
	title.size = Vector2(720, 70)
	StorybookUI.style_label(title, 44, StorybookUI.INK, 4)
	stage_control.add_child(title)
	var close := Button.new()
	close.name = "StuffieCareBackButton"
	StorybookUI.style_back_button(close, "Back to swimming")
	close.position = Vector2(1100, 38)
	close.pressed.connect(close_care_menu)
	stage_control.add_child(close)

	var preview := StorybookUI.add_panel(stage_control, Rect2(72, 138, 350, 360), StorybookUI.MINT, Color(0.96, 0.99, 1.0, 0.98), 38)
	var current_colors: Array[Color] = colors()
	_add_creature_preview(preview, d, Vector2(16, 16), Vector2(318, 328), current_colors[0], current_colors[1])
	var growth := Label.new()
	growth.name = "StuffieGrowthPips"
	growth.text = _star_pips()
	growth.position = Vector2(72, 496)
	growth.size = Vector2(350, 42)
	growth.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(growth, 36, StorybookUI.GOLD, 4)
	stage_control.add_child(growth)
	var heart_text := ""
	for i in range(LEVEL_EVERY):
		heart_text += "💗" if i < (m.care_points % LEVEL_EVERY) else "🤍"
	var hearts := Label.new()
	hearts.name = "StuffieHeartProgress"
	hearts.text = heart_text + "  →  ⭐"
	hearts.position = Vector2(72, 536)
	hearts.size = Vector2(350, 40)
	hearts.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(hearts, 31, StorybookUI.INK_SOFT, 3)
	stage_control.add_child(hearts)
	var paint := Button.new()
	paint.name = "StuffieSwitchButton" # stable probe/controller focus contract
	paint.text = "🎨  CHANGE"
	paint.position = Vector2(92, 576)
	paint.custom_minimum_size = Vector2(310, 112)
	paint.size = Vector2(310, 112)
	StorybookUI.style_button(paint, "secondary", 28, 30)
	paint.disabled = m.companion_care_t > 0.0 \
		or not bool(d.get("paintable", true))
	paint.pressed.connect(_care_open_studio)
	stage_control.add_child(paint)

	var asked := m.companion_want
	if asked == "" and not m.companion_want_queue.is_empty():
		asked = String(m.companion_want_queue[0])
	var need_panel := StorybookUI.add_panel(stage_control, Rect2(466, 138, 698, 176), StorybookUI.GOLD, Color(1.0, 0.97, 0.86, 0.99), 36)
	var need := Label.new()
	need.name = "StuffieCurrentNeed"
	need.position = Vector2(20, 12)
	need.size = Vector2(658, 152)
	need.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	need.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	need.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	var need_icon := "♥"
	var need_text := "Pick something happy to do together!"
	if m.companion_care_t > 0.0:
		need_icon = "✨"
		need_text = "A happy care moment is happening!"
	elif m.companion_bruises > 0:
		need_icon = "🩹"
		need_text = "A hug and bubbles make boo-boos better"
	elif m.companion_want != "":
		var current := want_def(m.companion_want)
		need_icon = String(current.get("emoji", "♥"))
		need_text = "This is what I need!"
	elif asked != "":
		need_icon = String(want_def(asked).get("emoji", ""))
		need_text = "This happy care is waiting!"
	need.text = "%s\n%s" % [need_icon, need_text]
	StorybookUI.style_label(need, 31, StorybookUI.INK, 4)
	need_panel.add_child(need)

	for i in range(WANTS.size()):
		var want: Dictionary = WANTS[i]
		var care := Button.new()
		care.name = "StuffieCareAction_%s" % String(want["id"])
		care.position = Vector2(466.0 + float(i) * 140.0, 344)
		StorybookUI.style_icon_button(care, String(want["emoji"]),
			"primary" if String(want["id"]) == asked else "secondary",
			Vector2(126, 132), String(want["id"]))
		care.disabled = m.companion_care_t > 0.0
		care.pressed.connect(_choose_menu_care.bind(String(want["id"])))
		stage_control.add_child(care)
	var hint := Label.new()
	hint.text = "🍎   💤   🫧   ❤   🎾"
	hint.position = Vector2(466, 500)
	hint.size = Vector2(698, 66)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(hint, 34, StorybookUI.INK_SOFT, 3)
	stage_control.add_child(hint)
	var safety := Label.new()
	safety.text = "♥  Wants wait patiently. Nothing is ever lost."
	safety.position = Vector2(466, 584)
	safety.size = Vector2(698, 70)
	safety.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	safety.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_label(safety, 25, StorybookUI.MUTED, 3)
	stage_control.add_child(safety)
	m._hook_button_taps(stage_control)

func _choose_menu_care(id: String) -> void:
	if m.companion_care_t > 0.0 or want_def(id).is_empty():
		return
	close_care_menu()
	var d := active_def()
	if not _follow_ctx():
		m.show_msg(String(d["name"]), "I'll come out to play after this game!", "talk")
		return
	if m.companion_node == null or not is_instance_valid(m.companion_node):
		_tick_follower(0.0)
	if m.companion_node == null or not is_instance_valid(m.companion_node):
		return
	# Menu care is the same persisted care loop as the in-world thought bubble.
	# A queued or active requested care grows the stuffie; every other choice is
	# welcome affection with hearts and no point, failure, or scolding.
	var fwd := Vector3(sin(m.player.yaw), 0, cos(m.player.yaw))
	var right := Vector3(cos(m.player.yaw), 0, -sin(m.player.yaw))
	m.companion_node.position = m.player.position + fwd * 3.5 - right * 1.5 + Vector3(0, 1.0, 0)
	if m.companion_want == "" and m.companion_want_queue.has(id):
		m.companion_want_queue.erase(id)
		m.companion_want = id
	if m.companion_want == id:
		_start_care()
		return
	_pal_bounce(1.15)
	m._greet_heart(m.companion_node.position + Vector3(0, 2.6, 0))
	if m.companion_want != "":
		m.show_msg(String(d["name"]), "Thank you! I would also love %s!" % String(want_def(m.companion_want).get("emoji", "")), "talk")
	else:
		m.show_msg(String(d["name"]), "I love that! You're the best!", "talk")

func _care_open_studio() -> void:
	if m.companion_care_t > 0.0:
		return
	close_care_menu()
	open_picker(true, m.companion_id, "studio")

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
		if m.companion_layer != null or m.companion_care_layer != null:
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
	var action: bool = _action_down()
	var tapped: bool = action and not m.companion_action_prev
	m.companion_action_prev = action   # refresh every frame, even with the picker open
	if m.companion_layer != null:
		return
	var gd: float = m.companion_gift.global_position.distance_to(m.player.position)
	if gd < GIFT_RADIUS and tapped:
		open_picker()

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

func open_picker(say_prompt: bool = true, preselect: String = "", mode: String = "adopt") -> void:
	# say_prompt=false when Princess Huluu herself makes the offer — her
	# "I want you to have a new friend!" line owns that moment.
	# The toy chest uses swap mode; the worktable uses studio mode.
	if m.companion_layer != null:
		return
	m.companion_pick_mode = mode if mode in ["adopt", "swap", "studio"] else "adopt"
	var resume_rescue_draft: bool = bool(m.g.get("stuffie_rescue_tutorial", false)) \
			and m.companion_pick_mode == "adopt" \
			and m.companion_pick_id != ""
	if resume_rescue_draft:
		# The child-facing Back/dim/B paths are reversible. Keep the current
		# friend/coat draft so a return to the picker feels like a resume.
		_reset_pick_colors()
	elif m.companion_pick_mode == "studio" and m.companion_id != "":
		m.companion_pick_id = m.companion_id
		_reset_pick_colors()
	elif not def_by_id(preselect).is_empty():
		m.companion_pick_id = preselect
		_reset_pick_colors()
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
	dim.color = StorybookUI.DIM
	# tap outside the panel = gently close (also keeps the audit bot un-stuck)
	dim.gui_input.connect(_on_picker_dim_input)
	root_control.add_child(dim)
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	var stage := StorybookUI.add_stage(root_control, viewport_size)
	m.companion_stage = stage
	if m.player != null:
		m.player.vel = Vector3.ZERO
	_draw_picker()
	if say_prompt:
		if m.companion_pick_mode == "studio":
			m.show_msg("Roshan", "Makeover time! Tap a color, then the big heart to save it!", "talk")
		elif m.companion_pick_mode == "swap":
			m.show_msg("Roshan", "Which stuffie comes with me? Tap a friend, then the big heart!", "talk")
		else:
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
	if bool(m.g.get("stuffie_rescue_tutorial", false)) \
			and m.companion_pick_colors.size() == 3:
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
	if bool(m.g.get("stuffie_rescue_tutorial", false)):
		m.g["stuffie_rescue_tutorial_step"] = 2
		m.show_msg("Roshan",
			"Beautiful! Tap the big heart to take Baby Eagle along!",
			"talk")
	_draw_picker()

func _pick_color_slot(slot: int) -> void:
	m.companion_pick_slot = clampi(slot, 0, 2)
	m._ui_tap()
	if bool(m.g.get("stuffie_rescue_tutorial", false)):
		m.g["stuffie_rescue_tutorial_step"] = 1
		m.show_msg("Roshan", "Now tap any big color!", "talk")
	_draw_picker()

func _confirm_pick() -> void:
	var studio_change: bool = m.companion_pick_mode == "studio" \
		and m.companion_pick_id == m.companion_id
	m.g.erase("stuffie_rescue_tutorial")
	m.g.erase("stuffie_rescue_tutorial_step")
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
	if not studio_change:
		# A chest swap resets pending wants (care progress itself is shared —
		# Roshan's nurturing grows whichever friend she carries).
		m.companion_want = ""
		m.companion_care_t = -1.0
		if m.companion_want_bubble != null and is_instance_valid(m.companion_want_bubble):
			m.companion_want_bubble.queue_free()
		m.companion_want_bubble = null
		m.companion_want_cool = 20.0
		m.companion_want_queue = []
		m.companion_bruises = 0
		m.companion_rest_timer = -1.0
		m.companion_resting = false
		m.companion_greeted = false
	m._write_save()
	# Adoption is durable before the picker is removed. The castle owns one
	# reusable Canvas card; confirmation refreshes/repositions that card rather
	# than creating a follower or a tween callback instance.
	if m.castle_room_layer != null and is_instance_valid(m.castle_room_layer):
		m._castle_rooms_ref().sync_castle_companion_card()
	m._reward(false)
	if m.player != null:
		m._sparkle_burst(m.player.position + Vector3(0, 2.0, 0), Color(1.0, 0.8, 0.5))
	if studio_change:
		m.show_msg(String(d["name"]), "My new colors are beautiful! Thank you!", "win")
	else:
		m.show_msg(String(d["name"]), String(d["hello"]), "win")

func _draw_picker() -> void:
	var stage: Control = m.companion_stage
	if stage == null or not is_instance_valid(stage):
		return
	for child: Node in stage.get_children():
		stage.remove_child(child)
		child.queue_free()
	var panel := Panel.new()
	panel.position = Vector2(34, 24)
	panel.size = Vector2(1212, 672)
	var panel_style := StorybookUI.panel_style(Color(0.95, 0.70, 0.90), Color(0.91, 0.97, 1.0, 0.99), 48, 5)
	panel.add_theme_stylebox_override("panel", panel_style)
	stage.add_child(panel)
	var title := Label.new()
	title.text = "🎨  Stuffie Makeover!" if m.companion_pick_mode == "studio" \
		else "🧸  Choose a stuffie friend!"
	StorybookUI.style_label(title, 42, StorybookUI.INK, 4)
	title.position = Vector2(70, 34)
	stage.add_child(title)
	var close := Button.new()
	close.name = "StuffiePickerBackButton"
	StorybookUI.style_back_button(close, "Back to the castle")
	close.position = Vector2(1110, 32)
	close.pressed.connect(close_picker)
	stage.add_child(close)
	# The chest lists every friend who lives at home. The worktable deliberately
	# locks this column to the active friend so choosing and changing are distinct.
	var picks: Array[Dictionary] = unlocked_defs()
	if bool(m.g.get("stuffie_rescue_tutorial", false)) \
			and m.companion_pick_mode == "adopt":
		var eagle: Dictionary = def_by_id("eagle")
		if not eagle.is_empty():
			picks = [eagle]
	if m.companion_pick_mode == "studio":
		picks = [active_def()]
	var step: float = minf(250.0, 560.0 / maxf(float(picks.size()), 1.0))
	for i in range(picks.size()):
		var d: Dictionary = picks[i]
		var id := String(d["id"])
		var card := Button.new()
		card.name = "StuffieCard_" + id
		card.set_meta("touch_target", true)
		card.position = Vector2(80, 130 + float(i) * step)
		card.custom_minimum_size = Vector2(330, step - 25.0)
		StorybookUI.style_button(card, "selected" if id == m.companion_pick_id else "secondary", 24, 24)
		card.pressed.connect(_pick_friend.bind(id))
		stage.add_child(card)
		_add_creature_preview(card, d, Vector2(12, 12), Vector2(150, step - 50.0),
			(d["body"] as Color), (d["accent"] as Color))
		var nm := Label.new()
		nm.text = String(d["name"])
		StorybookUI.style_label(nm, 26, StorybookUI.INK, 3)
		nm.position = Vector2(172, 24)
		nm.size = Vector2(150, step - 100.0)
		nm.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		card.add_child(nm)
		var atk := Label.new()
		atk.text = ("🐦 " if String(d["kind"]) == "bird" else "🐾 ") + String(d["attack"])
		StorybookUI.style_label(atk, 24, StorybookUI.INK_SOFT, 2)
		atk.position = Vector2(172, step - 82.0)
		card.add_child(atk)
	# big live preview, painted with the picked colours
	var pick_def := def_by_id(m.companion_pick_id)
	var pc0 := Color.html(String(m.companion_pick_colors[0]))
	var pc1 := Color.html(String(m.companion_pick_colors[1]))
	var preview_panel := StorybookUI.add_panel(stage, Rect2(460, 130, 330, 330), StorybookUI.LAVENDER, Color(0.94, 0.97, 1.0, 0.98), 34)
	preview_panel.name = "StuffiePreviewCard"
	_add_creature_preview(preview_panel, pick_def, Vector2(14, 14), Vector2(302, 302), pc0, pc1)
	# Three large part selectors, but only one large palette at a time.
	var show_palette: bool = m.companion_pick_mode != "swap" \
		and bool(pick_def.get("paintable", true))
	if m.companion_pick_mode == "swap":
		var take_hint := Label.new()
		take_hint.text = "🐾   💗   🧜‍♀️"
		StorybookUI.style_label(take_hint, 54, StorybookUI.INK, 4)
		take_hint.position = Vector2(820, 220)
		take_hint.size = Vector2(370, 150)
		take_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		stage.add_child(take_hint)
	elif not bool(pick_def.get("paintable", true)):
		var asis := Label.new()
		asis.text = "💕  %s comes just as she is!" % String(pick_def["name"])
		StorybookUI.style_label(asis, 27, StorybookUI.INK, 3)
		asis.position = Vector2(830, 240)
		asis.size = Vector2(400, 120)
		asis.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		stage.add_child(asis)
	for slot in range(3 if show_palette else 0):
		var icon := Button.new()
		icon.name = "StuffiePart_%d" % slot
		icon.text = SLOT_ICON[slot]
		icon.position = Vector2(800.0 + float(slot) * 130.0, 130)
		icon.custom_minimum_size = Vector2(116, 116)
		icon.size = Vector2(116, 116)
		StorybookUI.style_button(icon, "selected" if slot == m.companion_pick_slot else "secondary", 42, 30)
		icon.pressed.connect(_pick_color_slot.bind(slot))
		stage.add_child(icon)
		if slot != m.companion_pick_slot:
			continue
		for ci in range(PALETTE.size()):
			var col: Color = PALETTE[ci]
			var swatch := Button.new()
			swatch.name = "StuffieSwatch_%d" % ci
			swatch.set_meta("touch_target", true)
			swatch.position = Vector2(800.0 + float(ci % 4) * 112.0, 270.0 + float(ci / 4) * 116.0)
			swatch.custom_minimum_size = Vector2(110, 110)
			swatch.size = Vector2(110, 110)
			var sw_style := StyleBoxFlat.new()
			sw_style.bg_color = col
			var chosen: bool = col.to_html(false) == String(m.companion_pick_colors[slot])
			sw_style.border_color = Color(1.0, 1.0, 1.0) if chosen else Color(0.1, 0.12, 0.2)
			sw_style.set_border_width_all(5 if chosen else 2)
			sw_style.set_corner_radius_all(30)
			swatch.add_theme_stylebox_override("normal", sw_style)
			swatch.add_theme_stylebox_override("hover", sw_style)
			swatch.add_theme_stylebox_override("pressed", sw_style)
			swatch.pressed.connect(_pick_color.bind(slot, col))
			stage.add_child(swatch)
	var go := Button.new()
	go.name = "StuffieConfirmButton"
	go.text = "🎨  SAVE COLORS!" if m.companion_pick_mode == "studio" \
		else "♥  TAKE ALONG!"
	go.position = Vector2(460, 500)
	go.custom_minimum_size = Vector2(330, 150)
	StorybookUI.style_button(go, "primary", 38, 38)
	go.pressed.connect(_confirm_pick)
	stage.add_child(go)
	_add_rescue_tutorial_focus(stage)
	m._hook_button_taps(stage)

func _add_rescue_tutorial_focus(stage: Control) -> void:
	if not bool(m.g.get("stuffie_rescue_tutorial", false)):
		return
	var step: int = clampi(int(m.g.get(
		"stuffie_rescue_tutorial_step", 0)), 0, 2)
	var focus_rects: Array[Rect2] = [
		Rect2(785.0, 114.0, 420.0, 142.0),
		Rect2(785.0, 254.0, 465.0, 252.0),
		Rect2(444.0, 484.0, 362.0, 182.0),
	]
	var focus_rect: Rect2 = focus_rects[step]
	var focus := Panel.new()
	focus.name = "StuffieRescueTutorialFocus"
	focus.position = focus_rect.position
	focus.size = focus_rect.size
	focus.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var focus_style := StyleBoxFlat.new()
	focus_style.bg_color = Color(1.0, 0.88, 0.32, 0.05)
	focus_style.border_color = StorybookUI.GOLD
	focus_style.set_border_width_all(8)
	focus_style.set_corner_radius_all(34)
	focus.add_theme_stylebox_override("panel", focus_style)
	stage.add_child(focus)
	var pointer := Label.new()
	pointer.name = "StuffieRescueTutorialPointer"
	pointer.text = "▼"
	pointer.position = Vector2(
		focus_rect.position.x + focus_rect.size.x * 0.5 - 34.0,
		focus_rect.position.y - 58.0)
	pointer.size = Vector2(68.0, 62.0)
	pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(pointer, 52, StorybookUI.GOLD, 5)
	stage.add_child(pointer)
	var pulse: Tween = focus.create_tween().set_loops()
	pulse.tween_property(focus, "modulate:a", 0.50,
		0.42).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	pulse.parallel().tween_property(pointer, "position:y",
		pointer.position.y + 10.0, 0.42).set_trans(Tween.TRANS_SINE)
	pulse.tween_property(focus, "modulate:a", 1.0,
		0.42).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	pulse.parallel().tween_property(pointer, "position:y",
		pointer.position.y, 0.42).set_trans(Tween.TRANS_SINE)

func _add_creature_preview(parent: Control, d: Dictionary, box_pos: Vector2, box_size: Vector2, body: Color, accent: Color) -> void:
	# layered book-art preview (assets/mg fish/cat/bird sheets), live-tinted —
	# the same sheets the craft creatures use, so the paint matches in-world.
	# The sheets are large illustrations: FIT them into the given box (uniform
	# scale, centered) instead of trusting any fixed scale, and paint in the
	# in-world order — body first, accent OVER it, ink line on top.
	parent.clip_contents = true
	if d.has("sprite"):
		var direct := TextureRect.new()
		direct.texture = load(String(d["sprite"]))
		direct.position = box_pos
		direct.size = box_size
		direct.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		direct.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		direct.mouse_filter = Control.MOUSE_FILTER_IGNORE
		parent.add_child(direct)
		return
	if not m.CREATURE_LAYERS.has(String(d.get("kind", ""))):
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

# ---------- the Stuffie Studio: six display cubbies, a care/upgrade table,
# ---------- and a separate toy chest for choosing the active friend ----------

const ROOM_LOCAL := Vector3(-49.4, 49.6, -44.0)   # west end of the Dreaming
const ROOM_SLOT_COUNT := 6
const ROOM_INTERACT_RADIUS := 6.0
const ROOM_SHELF_TEXTURE := "res://assets/sprites/stuffie_studio/display_shelf.png"
const ROOM_TABLE_TEXTURE := "res://assets/sprites/stuffie_studio/worktable.png"
const ROOM_CHEST_TEXTURE := "res://assets/sprites/stuffie_studio/toy_chest.png"
# Floor corridor (Wacky & Chuck's basket holds the east end); CASTLE_POS-relative

func _tick_room(_delta: float) -> void:
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
	var pointers_v: Variant = m.companion_room.get_meta("pointers", [])
	if pointers_v is Array:
		for i in range((pointers_v as Array).size()):
			var pointer_node: Label3D = (pointers_v as Array)[i] as Label3D
			if is_instance_valid(pointer_node):
				pointer_node.position.y = float(pointer_node.get_meta("base_y", pointer_node.position.y)) \
					+ sin(now * 4.0 + float(i) * 1.7) * 0.28
	# Voice and a three-icon tour make the room understandable without reading.
	if not bool(m.g.get("companion_room_said", false)) \
			and m.companion_room.global_position.distance_to(m.player.position) < 16.0:
		m.g["companion_room_said"] = true
		m.show_msg("Roshan", "The Stuffie Studio! Friends sit on the shelves. The table cares for and changes them. The toy chest chooses who comes with me!", "talk")
	var best_kind := ""
	var best_id := ""
	var best_d := ROOM_INTERACT_RADIUS
	for row_v: Variant in m.companion_room_rows:
		var row: Dictionary = row_v
		var node: Node3D = row["node"]
		if not is_instance_valid(node):
			continue
		var mine: bool = String(row["id"]) != "" and String(row["id"]) == m.companion_id
		var home: bool = bool(row.get("home", false))
		var marker: Label3D = row["marker"]
		var heart: Label3D = row["heart"]
		var visual: Node3D = row.get("visual") as Node3D
		if is_instance_valid(visual):
			visual.position.y = float(row["base_y"]) \
				+ sin(now * 2.2 + float(row["phase"])) * 0.1
		if is_instance_valid(marker):
			marker.visible = home and not mine
			marker.modulate.a = 0.72 + sin(now * 3.0 + float(row["phase"])) * 0.22
		if is_instance_valid(heart):
			heart.visible = mine
			heart.text = "💗"
		var dist: float = node.global_position.distance_to(m.player.position)
		if dist < best_d:
			best_d = dist
			best_kind = "shelf"
			best_id = String(row["id"])
	var table_anchor: Node3D = m.companion_room.get_meta("table_anchor") as Node3D
	if is_instance_valid(table_anchor):
		var table_d: float = table_anchor.global_position.distance_to(m.player.position)
		if table_d < best_d:
			best_d = table_d
			best_kind = "table"
	var chest_anchor: Node3D = m.companion_room.get_meta("chest_anchor") as Node3D
	if is_instance_valid(chest_anchor):
		var chest_d: float = chest_anchor.global_position.distance_to(m.player.position)
		if chest_d < best_d:
			best_d = chest_d
			best_kind = "chest"
	var action: bool = _action_down()
	var overlay_open: bool = m.companion_layer != null or m.companion_care_layer != null
	if best_kind != "" and action and not m.companion_room_action_prev and not overlay_open:
		match best_kind:
			"shelf":
				if best_id == "":
					m.show_msg("Roshan", "An empty cubby! A new stuffie friend can live here someday.", "talk")
				elif not unlocked(best_id):
					m.show_msg("Roshan", "A mystery friend belongs here! We can befriend them at the castle toy tournament.", "talk")
				else:
					var shelf_def := def_by_id(best_id)
					var shelf_line := "I'm waiting on my cozy shelf!"
					if best_id == m.companion_id:
						shelf_line = "That's me! My heart shows I'm the active stuffie."
					m.show_msg(String(shelf_def["name"]), shelf_line, "talk")
			"table":
				if m.companion_id == "":
					m.show_msg("Roshan", "This table changes and upgrades a stuffie. First choose a friend from the toy chest!", "talk")
				else:
					open_care_menu()
			"chest":
				var preselect: String = m.companion_id
				if preselect == "":
					preselect = String(ROSTER[0]["id"])
				open_picker(false, preselect, "swap")
				m.show_msg("Roshan", "Toy chest time! Tap the stuffie who comes on the adventure, then tap the big heart!", "talk")
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
	root.name = "StuffieStudioRoom"
	root.position = m.CASTLE_POS + ROOM_LOCAL
	m.add_child(root)
	m.game_nodes.append(root)
	m.companion_room = root
	m.companion_room_rows = []
	var shelf_art: Sprite3D = _room_sprite(ROOM_SHELF_TEXTURE, Vector3(-2.8, 6.4, 0.0), 13.2, 0)
	shelf_art.name = "StuffieSixCubbyDisplay"
	root.add_child(shelf_art)
	var table_art: Sprite3D = _room_sprite(ROOM_TABLE_TEXTURE, Vector3(-0.4, 2.75, -9.0), 5.3, 0)
	table_art.name = "StuffieUpgradeTable"
	root.add_child(table_art)
	var chest_art: Sprite3D = _room_sprite(ROOM_CHEST_TEXTURE, Vector3(-0.4, 2.9, 9.0), 5.8, 0)
	chest_art.name = "StuffieActiveToyChest"
	root.add_child(chest_art)
	var sign := Label3D.new()
	sign.text = "🧸  STUFFIE STUDIO  ✨"
	sign.font_size = 44
	sign.pixel_size = 0.008
	sign.outline_size = 11
	sign.modulate = Color(1.0, 0.9, 0.95)
	sign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sign.position = Vector3(-2.4, 13.1, 0)
	root.add_child(sign)
	var table_anchor := Node3D.new()
	table_anchor.name = "StuffieTableAnchor"
	table_anchor.position = Vector3(1.0, 2.0, -9.0)
	root.add_child(table_anchor)
	root.set_meta("table_anchor", table_anchor)
	var chest_anchor := Node3D.new()
	chest_anchor.name = "StuffieChestAnchor"
	chest_anchor.position = Vector3(1.0, 2.0, 9.0)
	root.add_child(chest_anchor)
	root.set_meta("chest_anchor", chest_anchor)
	var pointers: Array[Label3D] = []
	var table_pointer: Label3D = _room_pointer("♥  ⭐  🎨", Vector3(0.4, 6.4, -9.0))
	table_pointer.name = "StuffieTablePointer"
	root.add_child(table_pointer)
	pointers.append(table_pointer)
	var chest_pointer: Label3D = _room_pointer("🧸  ↔  🧜‍♀️", Vector3(0.4, 6.6, 9.0))
	chest_pointer.name = "StuffieChestPointer"
	root.add_child(chest_pointer)
	pointers.append(chest_pointer)
	root.set_meta("pointers", pointers)
	# The card itself has a 3x2 grid. Runtime friends sit directly inside those
	# six painted cubbies; future roster slots remain inviting mystery spaces.
	for i in range(ROOM_SLOT_COUNT):
		var column: int = i % 3
		var row_index: int = int(i / 3)
		var slot_pos := Vector3(-2.45, 6.95 - float(row_index) * 3.35,
			-3.2 + float(column) * 3.2)
		var anchor := Node3D.new()
		anchor.name = "StuffieShelfSlot%d" % (i + 1)
		anchor.position = slot_pos
		root.add_child(anchor)
		var d: Dictionary = ROSTER[i] if i < ROSTER.size() else {}
		var id := String(d.get("id", ""))
		var is_home: bool = id != "" and unlocked(id)
		var display_creature: Node3D = null
		if is_home:
			display_creature = _stuffie_cutout(d, _room_colors(id), 2.4)
			if display_creature != null:
				display_creature.position = slot_pos + Vector3(0.12, -0.05, 0)
				root.add_child(display_creature)
			var name_sign := Label3D.new()
			name_sign.text = String(d["name"])
			name_sign.font_size = 24
			name_sign.pixel_size = 0.007
			name_sign.outline_size = 8
			name_sign.modulate = Color(0.96, 0.98, 1.0)
			name_sign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			name_sign.position = slot_pos + Vector3(0.2, -1.25, 0)
			root.add_child(name_sign)
		else:
			var mystery := Label3D.new()
			mystery.text = "❔"
			mystery.font_size = 112
			mystery.pixel_size = 0.014
			mystery.outline_size = 14
			mystery.modulate = Color(0.82, 0.86, 1.0, 0.92)
			mystery.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			mystery.position = slot_pos
			root.add_child(mystery)
		var marker := Label3D.new()
		marker.text = "✨"
		marker.font_size = 78
		marker.pixel_size = 0.013
		marker.outline_size = 13
		marker.modulate = Color(1.0, 0.88, 0.35, 0.9)
		marker.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		marker.no_depth_test = true
		marker.position = slot_pos + Vector3(0.25, 1.18, 0)
		root.add_child(marker)
		var heart := Label3D.new()
		heart.text = "💗"
		heart.font_size = 78
		heart.pixel_size = 0.013
		heart.outline_size = 13
		heart.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		heart.no_depth_test = true
		heart.position = slot_pos + Vector3(0.25, 1.18, 0)
		heart.visible = false
		root.add_child(heart)
		m.companion_room_rows.append({"id": id, "node": anchor,
			"marker": marker, "heart": heart, "visual": display_creature,
			"base_y": slot_pos.y - 0.05, "phase": float(i) * 1.7, "home": is_home})

func _room_sprite(path: String, pos: Vector3, target_height: float, priority: int) -> Sprite3D:
	var sprite := Sprite3D.new()
	var tex: Texture2D = load(path)
	sprite.texture = tex
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.pixel_size = target_height / maxf(float(tex.get_height()), 1.0) if tex != null else 0.01
	sprite.render_priority = priority
	sprite.position = pos
	return sprite

func _room_pointer(icon: String, pos: Vector3) -> Label3D:
	var pointer := Label3D.new()
	pointer.text = icon
	pointer.font_size = 72
	pointer.pixel_size = 0.012
	pointer.outline_size = 14
	pointer.modulate = Color(1.0, 0.94, 0.45)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	pointer.no_depth_test = true
	pointer.position = pos
	pointer.set_meta("base_y", pos.y)
	return pointer

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

func after_battle(announce: bool = true) -> void:
	# Every big battle earns a hug + bubble bath. Boo-boos wait patiently until
	# the child chooses care; the timer below only schedules gentle reminders.
	if m.companion_id == "":
		return
	m.companion_want = ""
	if m.companion_want_bubble != null and is_instance_valid(m.companion_want_bubble):
		m.companion_want_bubble.queue_free()
	m.companion_want_bubble = null
	m.companion_care_t = -1.0
	m.companion_want_queue = ["cuddle", "bath"]
	m.companion_want_cool = 1.5
	if m.companion_bruises > 0:
		m.companion_rest_timer = CARE_REMINDER_GAP
		if announce:
			var d := active_def()
			m.show_msg(String(d["name"]), "What a big battle! I have boo-boos... I need a hug and a bubble bath!", "talk")
	elif announce:
		var d2 := active_def()
		m.show_msg(String(d2["name"]), "What a big battle! Can I have a hug and a bubble bath?", "talk")

func _tick_care(delta: float) -> void:
	if not _follow_ctx() or m.companion_node == null or not is_instance_valid(m.companion_node):
		return
	# edge-detect THE button up front, every frame this tick runs — updating
	# the prev flag only inside one branch left it stale and ate real taps
	# (caught by probe_stuffie: the post-battle bath never got tended)
	var action: bool = _action_down()
	var tapped: bool = action and not m.companion_care_action_prev
	m.companion_care_action_prev = action
	# Opening the care sheet is already an attempt to help. Freeze asks and the
	# reminder clock until a choice is made or the sheet is closed.
	if m.companion_care_layer != null:
		return
	# reloaded mid-injury (or came back before the queue ran): re-ask kindly
	if m.companion_bruises > 0 and m.companion_want_queue.is_empty() \
			and m.companion_want == "" and m.companion_rest_timer < 0.0:
		after_battle(false)
	# A reminder clock only ticks while she can actually help. It loops forever;
	# it never changes availability, progress, bruises, or companion presence.
	if m.companion_bruises > 0 and m.companion_rest_timer > 0.0 and m.companion_care_t <= 0.0:
		m.companion_rest_timer -= delta
		if m.companion_rest_timer <= 0.0:
			m.companion_rest_timer = CARE_REMINDER_GAP
			var d := active_def()
			m.show_msg(String(d["name"]), "Whenever you're ready, tap me for a hug and bubble bath!", "talk")
	# a care moment in progress owns the stuffie for a beat
	if m.companion_care_t > 0.0:
		m.companion_care_t -= delta
		if m.companion_care_t <= 0.0:
			_finish_care()
		return
	if m.companion_want == "":
		if m.companion_layer != null or m.companion_care_layer != null:
			return
		m.companion_want_cool -= delta
		if m.companion_want_cool <= 0.0:
			# queued post-battle care first, then the ordinary gentle asks
			if not m.companion_want_queue.is_empty():
				_begin_want(String(m.companion_want_queue.pop_front()))
			else:
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
	if tapped and m.companion_node.position.distance_to(m.player.position) < CARE_RADIUS \
			and m.companion_layer == null and m.companion_care_layer == null:
		_start_care()

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
	if not m.companion_want_queue.is_empty():
		m.companion_want_cool = 1.2   # the post-battle bath follows the hug right away
	m.care_points += 1
	# tending BOTH post-battle wants heals every boo-boo — all better!
	if m.companion_bruises > 0 and m.companion_want_queue.is_empty():
		m.companion_bruises = 0
		m.companion_rest_timer = -1.0
		if m.companion_node != null and is_instance_valid(m.companion_node):
			for i in range(6):
				var a: float = TAU * float(i) / 6.0
				m._sparkle_burst(m.companion_node.position + Vector3(cos(a) * 1.8, 1.5, sin(a) * 1.8), Color(0.6, 1.0, 0.75))
		m.show_msg(String(d["name"]), "All better! My boo-boos are gone! You take such good care of me!", "win")
		m._write_save()
		if m.chime != null:
			m.chime.pitch_scale = 1.4
			m.chime.play()
		return
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
	# Hybrid contract: proximity may advertise, it never starts a game. The
	# den is a registered tap target there ("reef:den"); walking into the ring
	# only auto-starts the battle on the Classic path.
	if m.touch_uses_explicit_interactions():
		return
	if m.stuffie_cool <= 0.0 and m.companion_den.position.distance_to(m.player.position) < DEN_RADIUS:
		m.stuffie_cool = 14.0
		m._start_stuffie_battle()

func _build_den() -> void:
	# The den keeps its historical spot (the old wreck at heading 2.4 / r150
	# plus the 34,20 offset). The 3D wreck itself was deleted 2026-07-28, so
	# this no longer derives from m.wreck_pos (which now stays ZERO).
	var x: float = cos(2.4) * 150.0 + 34.0
	var z: float = sin(2.4) * 150.0 + 20.0
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
		var d: Dictionary = active_def()
		if not d.is_empty():
			m.show_msg(String(d.get("name", "Stuffie Friend")),
				"Look, a sparkle ring! Let's play-battle with the mischief imps!",
				"talk")
