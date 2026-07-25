class_name Satchel
extends RefCounted
# S2 of SATCHEL_WORKORDER_2026-07-25: the inventory, built as a HOTBAR.
#
# Minecraft's hotbar is the child-friendly half of its inventory — one visible
# row, pictures not words, one tap to select, and the selected thing is in your
# hands in the world. We take that and refuse the rest (grid, drag-and-drop,
# stack counts, recipes): every one of those is a literacy, dexterity or
# working-memory tax on a 4-year-old with one finger.
#
# NEVER A WALL. A full satchel does not block a pickup. The oldest thing swims
# home to where it was found, with a sparkle. Nothing is ever destroyed and
# there is no state that tells the child "no".
#
# SESSION-ONLY (S2 scope): nothing here is persisted. Placement and the "room"
# save key are S3. Everything picked up returns to the reef when the game is
# reloaded, so the authored world can never degrade.
#
# The pickable pool IS the ReactiveProps registry, filtered to the "bob" kinds
# (loose seafloor things). That is what keeps CarrySystem's two starfish and
# two singing shells out of the satchel for free — they are released from the
# registry on spawn, so they are invisible here and keep their own toss toy.

const SLOTS := 6
const SLOT_PX := 110.0     # the >=110 px tap-target rule, DESIGN_3_0.md
const SLOT_GAP := 8.0
const ROW_BOTTOM := 104.0  # clear of hud_msg below and the action bubble right
const PICK_R := 7.0
const ICON_PX := 128       # POT, well under the 1024 texture ceiling

# Fallback slot art when no rendered icon is available (headless, or a device
# where the render path fails). Colour is the primary differentiator — a
# 4-year-old reads "the pink one" long before any glyph.
const LOOK := {
	"starfish": ["★", Color(1.0, 0.72, 0.42)],
	"spiralshell": ["✿", Color(1.0, 0.78, 0.88)],
	"fanshell": ["❉", Color(0.78, 0.86, 1.0)],
	"smallfanshell": ["❉", Color(0.72, 0.94, 0.90)],
	"sanddollar": ["●", Color(0.98, 0.94, 0.78)],
	"urchin_story": ["✹", Color(0.82, 0.74, 1.0)],
}

var m: ReefMain
var _act_prev := false
var _key_prev := {}
var _pad_prev := false
var _icons := {}       # prop name -> ImageTexture (rendered once, cached)
var _icon_busy := {}
var _btns: Array = []

func _init(main: ReefMain) -> void:
	m = main

# ---------------------------------------------------------------- lifecycle

func stow(hide_row: bool = true) -> void:
	# park everything the satchel owns out of sight. Called whenever the
	# overworld verbs are not live — an overlay is up, or a minigame took the
	# world — so a held prop can never be left hanging in the reef.
	for it in m.satchel:
		var d: Dictionary = it
		var wrap: Node3D = d["wrap"]
		if is_instance_valid(wrap):
			wrap.visible = false
	if hide_row and m.satchel_row != null and is_instance_valid(m.satchel_row):
		m.satchel_row.visible = false

func tick(delta: float, ppos: Vector3) -> void:
	_build_row()
	if CarrySystem.verbs_blocked(m):
		_act_prev = false
		stow()
		return
	if m.satchel_row != null and is_instance_valid(m.satchel_row):
		m.satchel_row.visible = true
	_tick_select()
	# CarrySystem ticks first and gets first refusal on the ACTION edge, so a
	# press that scooped or threw a starfish never also works the satchel.
	var act: bool = Input.is_physical_key_pressed(KEY_SPACE)
	if m.has_method("joy_pressed"):
		act = act or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	if m.touch_ui != null and m.touch_ui.action_down:
		act = true
	if act and not _act_prev and not m._carry_ref().action_used:
		_action(ppos)
	_act_prev = act
	_hold_selected(delta)

func _action(ppos: Vector3) -> void:
	if m.satchel_sel >= 0 and m.satchel_sel < m.satchel.size():
		_put_down(ppos)
		return
	var target: Dictionary = _nearest_pickable(ppos)
	if not target.is_empty():
		_pick_up(target)

# ---------------------------------------------------------------- the verbs

func _nearest_pickable(ppos: Vector3) -> Dictionary:
	var best: Dictionary = {}
	var best_d: float = PICK_R
	for it in m.reactive_props:
		var d: Dictionary = it
		if String(d["kind"]) != "bob":
			continue
		var wrap: Node3D = d["wrap"]
		if not is_instance_valid(wrap) or not wrap.visible:
			continue
		var dist: float = wrap.position.distance_to(ppos)
		if dist < best_d:
			best_d = dist
			best = d
	return best

func _pick_up(entry: Dictionary) -> void:
	var wrap: Node3D = entry["wrap"]
	var pname: String = String(entry["name"])
	var home: Vector3 = wrap.position
	# leaving the registry restores the prop's authored rest pose, so nothing
	# ever freezes mid-squash inside a slot
	m._react_ref().release(wrap)
	wrap.visible = false
	if m.satchel.size() >= SLOTS:
		_swim_home(0)
	m.satchel.append({"name": pname, "wrap": wrap,
		"target": float(entry["target"]), "home": home})
	# NOT auto-selected. If a pickup put the thing straight into her hands, the
	# very next ACTION would drop it again and collecting two things in a row
	# would be impossible. The filling slot, the sparkle and the chime are the
	# feedback; taking something OUT is a separate, deliberate tap on the slot.
	if m.player != null:
		# this press was a scoop, not a jump (main ticks before the player)
		m.player.jump_cool = maxf(float(m.player.jump_cool), 0.5)
		m.player.play_verb("collect")
	m._sparkle_burst(home, Color(1.0, 0.92, 0.72))
	_chime(1.6)
	_build_icon(pname)
	_refresh()

func _put_down(ppos: Vector3) -> void:
	var it: Dictionary = m.satchel[m.satchel_sel]
	var wrap: Node3D = it["wrap"]
	m.satchel.remove_at(m.satchel_sel)
	m.satchel_sel = -1
	if not is_instance_valid(wrap):
		_refresh()
		return
	# seat it on the sand just in front of her, inside the world bounds
	var yaw: float = float(m.player.yaw) if m.player != null else 0.0
	var spot: Vector3 = ppos + Vector3(sin(yaw), 0.0, cos(yaw)) * 4.0
	var dxz: float = Vector2(spot.x, spot.z).length()
	if dxz > ReefMain.WORLD_R:
		spot.x *= ReefMain.WORLD_R / dxz
		spot.z *= ReefMain.WORLD_R / dxz
	spot.y = ReefMain.seabed_y(spot.x, spot.z) + 0.3
	_reseat(wrap, String(it["name"]), float(it["target"]), spot)
	if m.player != null:
		m.player.jump_cool = maxf(float(m.player.jump_cool), 0.5)
	m._sparkle_burst(spot, Color(0.82, 0.96, 1.0))
	_chime(0.9)
	_refresh()

func _swim_home(idx: int) -> void:
	# the satchel is full: the oldest thing goes back exactly where it was
	# found. Never a refusal, never a deletion.
	var it: Dictionary = m.satchel[idx]
	var wrap: Node3D = it["wrap"]
	m.satchel.remove_at(idx)
	if m.satchel_sel >= idx:
		m.satchel_sel -= 1
	if not is_instance_valid(wrap):
		return
	var home: Vector3 = it["home"]
	_reseat(wrap, String(it["name"]), float(it["target"]), home)
	m._sparkle_burst(home, Color(0.86, 0.9, 1.0))
	m._say("roshan", "")

func _reseat(wrap: Node3D, pname: String, target: float, spot: Vector3) -> void:
	wrap.position = spot
	wrap.visible = true
	var inst: Node3D = wrap.get_child(0) if wrap.get_child_count() > 0 else null
	if inst != null:
		m._react_ref().register(wrap, inst, pname, target)

func _hold_selected(delta: float) -> void:
	# the selected slot IS what she is holding: one concept, not two. Reuses
	# the carry point CarrySystem already tuned so both toys sit identically.
	if m.player == null:
		return
	for i in range(m.satchel.size()):
		var it: Dictionary = m.satchel[i]
		var wrap: Node3D = it["wrap"]
		if not is_instance_valid(wrap):
			continue
		if i != m.satchel_sel:
			wrap.visible = false
			continue
		var yaw: float = float(m.player.yaw)
		var pt: Vector3 = m.player.position \
			+ Vector3(sin(yaw), 0.0, cos(yaw)) * CarrySystem.CARRY_FWD \
			+ Vector3(0.0, CarrySystem.CARRY_UP, 0.0)
		wrap.visible = true
		wrap.position = wrap.position.lerp(pt, 1.0 - pow(0.0005, delta))
		wrap.rotation.y += delta * 1.4

# ---------------------------------------------------------------- selection

func select(i: int) -> void:
	if i < 0 or i >= m.satchel.size():
		return
	var was: int = m.satchel_sel
	m.satchel_sel = -1 if was == i else i
	if was >= 0 and was < m.satchel.size() and was != i:
		var prev: Dictionary = m.satchel[was]
		var pw: Node3D = prev["wrap"]
		if is_instance_valid(pw):
			pw.visible = false
	m._ui_tap()
	_refresh()

func _tick_select() -> void:
	# four input styles, one row: tap the slot (touch/mouse), 1-6 (keyboard,
	# Minecraft's own hotbar keys), shoulder buttons (gamepad).
	for i in range(SLOTS):
		var code: int = KEY_1 + i
		var down: bool = Input.is_physical_key_pressed(code)
		if down and not bool(_key_prev.get(code, false)):
			select(i)
		_key_prev[code] = down
	if not m.has_method("joy_pressed"):
		return
	var nxt: bool = m.joy_pressed(JOY_BUTTON_RIGHT_SHOULDER)
	if nxt and not _pad_prev and not m.satchel.is_empty():
		select((m.satchel_sel + 1) % m.satchel.size())
	_pad_prev = nxt

# ---------------------------------------------------------------- the row

func _build_row() -> void:
	# Parented to the existing hud_layer so it inherits every show/hide the HUD
	# already does for karts, the galaxy, arenas and minigames — no new
	# visibility bookkeeping, and no chance of the row surviving into a mode
	# that hid the rest of the HUD.
	if m.satchel_row != null and is_instance_valid(m.satchel_row):
		return
	if m.hud_layer == null or not is_instance_valid(m.hud_layer):
		return
	var w: float = SLOTS * SLOT_PX + (SLOTS - 1) * SLOT_GAP
	var row := HBoxContainer.new()
	row.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	row.offset_left = -w * 0.5
	row.offset_right = w * 0.5
	row.offset_top = -ROW_BOTTOM - SLOT_PX
	row.offset_bottom = -ROW_BOTTOM
	row.add_theme_constant_override("separation", int(SLOT_GAP))
	m.hud_layer.add_child(row)
	m.satchel_row = row
	_btns.clear()
	for i in range(SLOTS):
		var b := Button.new()
		b.custom_minimum_size = Vector2(SLOT_PX, SLOT_PX)
		b.focus_mode = Control.FOCUS_NONE
		b.pressed.connect(select.bind(i))
		var glyph := Label.new()
		glyph.name = "glyph"
		glyph.add_theme_font_size_override("font_size", 54)
		glyph.add_theme_color_override("font_outline_color", Color(0.16, 0.10, 0.28, 0.9))
		glyph.add_theme_constant_override("outline_size", 10)
		glyph.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		glyph.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		glyph.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		glyph.mouse_filter = Control.MOUSE_FILTER_IGNORE
		b.add_child(glyph)
		var pic := TextureRect.new()
		pic.name = "pic"
		pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		pic.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		pic.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pic.visible = false
		b.add_child(pic)
		row.add_child(b)
		_btns.append(b)
	_refresh()

func _refresh() -> void:
	for i in range(_btns.size()):
		var b: Button = _btns[i]
		if not is_instance_valid(b):
			continue
		var glyph: Label = b.get_node_or_null("glyph") as Label
		var pic: TextureRect = b.get_node_or_null("pic") as TextureRect
		var filled: bool = i < m.satchel.size()
		var col := Color(1, 1, 1, 0.18)
		var txt := ""
		var tex: Texture2D = null
		if filled:
			var it: Dictionary = m.satchel[i]
			var pname: String = String(it["name"])
			var look: Array = LOOK.get(pname, ["◆", Color(0.9, 0.9, 1.0)])
			txt = String(look[0])
			col = look[1]
			tex = _icons.get(pname, null)
		b.add_theme_stylebox_override("normal", _slot_box(col, filled, i == m.satchel_sel))
		b.add_theme_stylebox_override("hover", _slot_box(col, filled, i == m.satchel_sel))
		b.add_theme_stylebox_override("pressed", _slot_box(col, filled, true))
		if glyph != null:
			glyph.text = txt if tex == null else ""
			glyph.add_theme_color_override("font_color", Color(1, 1, 1, 0.95))
		if pic != null:
			pic.texture = tex
			pic.visible = tex != null

func _slot_box(col: Color, filled: bool, sel: bool) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(col.r, col.g, col.b, 0.42 if filled else 0.14)
	sb.set_corner_radius_all(26)
	sb.set_border_width_all(6 if sel else 3)
	sb.border_color = Color(1.0, 0.86, 0.36, 0.95) if sel else Color(1, 1, 1, 0.28)
	return sb

# ---------------------------------------------------------------- slot icons

func _build_icon(pname: String) -> void:
	# S0 of the workorder, shipped with its fallback wired in: render the prop
	# ONCE into a 128x128 texture and cache it by name. If anything about the
	# path is unavailable — headless probes, a device where SubViewport capture
	# misbehaves — we simply never fill _icons and the coloured glyph slot
	# stands in. The satchel is never blocked on the icon working.
	if _icons.has(pname) or bool(_icon_busy.get(pname, false)):
		return
	if DisplayServer.get_name() == "headless":
		return
	var path := "res://assets/props/gen2/" + pname + ".glb"
	if not ResourceLoader.exists(path):
		return
	_icon_busy[pname] = true
	var ps: PackedScene = load(path)
	if ps == null:
		_icon_busy[pname] = false
		return
	var vp := SubViewport.new()
	vp.size = Vector2i(ICON_PX, ICON_PX)
	vp.transparent_bg = true
	vp.own_world_3d = true
	vp.msaa_3d = Viewport.MSAA_DISABLED
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	m.add_child(vp)
	var inst: Node3D = ps.instantiate()
	var h: float = m._fit_prop(inst, 1.0)
	vp.add_child(inst)
	inst.rotation.y = 0.6
	var cam := Camera3D.new()
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = maxf(1.0, h) * 1.5
	# a default camera already looks down -Z, so framing the prop is just a
	# translation. No look_at: it needs a tree the node is not in yet.
	cam.position = Vector3(0.0, h * 0.5, 3.0)
	vp.add_child(cam)
	var key := DirectionalLight3D.new()
	key.light_energy = 1.4
	key.rotation = Vector3(-0.7, -0.6, 0.0)
	vp.add_child(key)
	await m.get_tree().process_frame
	await m.get_tree().process_frame
	var img: Image = null
	var vt: ViewportTexture = vp.get_texture()
	if vt != null:
		img = vt.get_image()
	vp.queue_free()
	if img != null and img.get_width() > 0:
		_icons[pname] = ImageTexture.create_from_image(img)
		_refresh()

func _chime(pitch: float) -> void:
	if m.chime != null:
		m.chime.pitch_scale = pitch
		m.chime.play()
