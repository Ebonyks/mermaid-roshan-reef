class_name SkyLagoonPromenade
extends RefCounted
# The Sky Lagoon's three-page 2.5D promenade. The painted PNW flats and
# transparent Codex sprites do the visual work; the real Roshan rig walks in
# one shallow band in front of them. All mutable state remains on ReefMain.

const HALF_W := 72.0
const HALF_D := 2.6
const BACKDROP_TILE_SIZE := Vector2(48.0, 48.0)
const BACKDROP_Z := -18.0
const FRAME_TEX := "res://assets/sprites/sky_lagoon/sky_lagoon_activity_frame_v2.png"
# THE PAINTING IS THE SCREEN. The three lossless tiles reconstruct one 144x48
# world-unit mural, and the lens is sized so the frame lands INSIDE it: the
# camera sits far enough back that the frustum is ~45 units tall where it
# crosses the mural (1.6 units of painted margin top and bottom) and pans only
# as far as SideScrollStage.screen_pan_limit allows. Nothing outside the
# painting can enter frame, so no environment sky is ever visible.
#   Mural: y in [-14.5, 33.5] (centre BACKDROP_CENTER_Y), x in [-72, 72].
#   Lens:  horizontal (look_h == cam_h), so the view centre is CAM_H at every
#          depth — Roshan's 7.8-unit card reads ~24% of frame height with her
#          feet at ~79% down, standing on the painted lawn.
const CAM_DIST := 47.0
const CAM_H := 9.5
const CAM_FOV := 38.0
const BACKDROP_CENTER_Y := CAM_H
# the walk band read off the painted lawn: the touch projection maps this
# window of screen height into the shallow depth band
const BAND_Y := -5.0
const BAND_H := 10.0
# a press has to be held this long on open ground before it becomes follow-the-
# finger travel; below it the press still belongs to the tap router
const HOLD_TRAVEL_S := 0.20
# the activity frames stand on the lawn like easels (they used to hang at
# y 14.5, which put them in the painted sky above the treeline)
const FRAME_STAND_Y := 5.4

var m: ReefMain
var stage: SideScrollStage

func _init(main: ReefMain) -> void:
	m = main
	stage = SideScrollStage.new(main)

func build(from_castle: bool, from_north: bool, at_ocean_gate_hub: bool) -> void:
	m.g["phase"] = "promenade"
	m.g["ocean_gate_hub"] = at_ocean_gate_hub
	m.g["lagoon_promenade_targets"] = []
	m.g["lagoon_promenade_focus"] = ""
	m.g["lagoon_promenade_focus_t"] = 0.0
	m.lagoon_floor = false
	m.northern_floor = false
	m.arena_center = m.LEVEL2_POS
	m.arena_dome = 92.0
	m.arena_ceil = 34.0
	stage.open({
		"origin": m.LEVEL2_POS,
		"half_w": HALF_W,
		"half_d": HALF_D,
		"hover": 3.0,
		"bob_amp": 0.18,
		"steer_speed": 18.5,
		"arrive_r": 0.85,
		"band_y": BAND_Y,
		"band_h": BAND_H,
		"cam_h": CAM_H,
		"cam_dist": CAM_DIST,
		"look_h": CAM_H,
		"cam_fov": CAM_FOV,
		"cam_follow": 1.0,
		# the mural the lens may never pan off
		"screen_half_w": BACKDROP_TILE_SIZE.x * 1.5,
		"screen_z": BACKDROP_Z,
		# taps belong to the interaction director below, not to raw travel
		"touch_travel": false,
	})
	# Three native-resolution, lossless tiles reconstruct the exact 2172x724
	# master at one depth. Their edges meet without overlap or rescaling.
	_add_backdrop(
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_0.png", -48.0)
	_add_backdrop(
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_1.png", 0.0)
	_add_backdrop(
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_2.png", 48.0)
	_build_ambient_life()
	_build_runway_screen()
	_build_playground_screen()
	_build_castle_screen()
	_build_roshan_card()
	var spawn_x := -48.0
	if from_castle:
		spawn_x = 48.0
	elif from_north:
		spawn_x = 48.0
	_set_spawn(spawn_x)
	if from_castle:
		m.show_msg("Roshan", "Back outside! Tap a picture frame once to light it up, then tap it again to play.")
	else:
		m.show_msg("Roshan", "Our pearl plane landed! Tap the plane or a picture frame to explore.", "intro")

func tick(delta: float) -> void:
	if m.mg_kind != "":
		return
	_tick_hold_travel(delta)
	var old_x: float = m.player.position.x
	stage.walk_tick(delta)
	_sync_roshan_card(m.player.position.x - old_x)
	_tick_ambient_life(delta)
	var focus_id: String = String(m.g.get("lagoon_promenade_focus", ""))
	var focus_t: float = float(m.g.get("lagoon_promenade_focus_t", 0.0)) + delta
	m.g["lagoon_promenade_focus_t"] = focus_t
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var glow: Sprite3D = target.get("highlight") as Sprite3D
		if glow == null or not is_instance_valid(glow):
			continue
		var selected: bool = String(target.get("id", "")) == focus_id
		glow.visible = selected
		if selected:
			var pulse: float = 1.08 + sin(focus_t * 5.2) * 0.035
			glow.scale = Vector3.ONE * pulse

func _tick_hold_travel(delta: float) -> void:
	# The touch grammar, kept honest: a TAP belongs to the tap router
	# (handle_touch, which the touch UI fires on release), a HOLD on open
	# ground is travel. The engine's own hold-to-travel is switched off for
	# this stage (cfg touch_travel false) — while it was on, every press was
	# travel, so pressing a picture frame walked Roshan across the promenade
	# on the way to opening it.
	var vp := m.get_viewport()
	if vp == null:
		return
	if not Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		m.g["lagoon_press_t"] = 0.0
		return
	var held: float = float(m.g.get("lagoon_press_t", 0.0)) + delta
	m.g["lagoon_press_t"] = held
	if held < HOLD_TRAVEL_S:
		return
	var press: Vector2 = vp.get_mouse_position()
	if not _target_at(press).is_empty():
		return
	_set_walk_goal(press)

func handle_touch(screen_pos: Vector2) -> bool:
	var target: Dictionary = _target_at(screen_pos)
	if target.is_empty():
		_clear_focus()
		_set_walk_goal(screen_pos)
		return true
	m.g["ss_walk_goal"] = null
	var target_id: String = String(target.get("id", ""))
	if String(m.g.get("lagoon_promenade_focus", "")) == target_id:
		_activate(target)
		_clear_focus()
	else:
		_focus(target)
	return true

func _build_runway_screen() -> void:
	var plane := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane.png",
		Vector3(-57.0, 6.4, -5.8), 11.2)
	m.g["lagoon_plane_card"] = plane
	m.g["lagoon_plane_base"] = plane.position
	_register_target("plane", plane, "plane", "", 118.0, 1.12)
	var targets: Array = m.g.get("lagoon_promenade_targets", [])
	var plane_target: Dictionary = targets.back() as Dictionary
	m.g["lagoon_plane_highlight"] = plane_target.get("highlight")
	_add_activity_frame("runway_frame", Vector3(-32.0, FRAME_STAND_Y, -4.8),
		"res://assets/book/hall/p_snowman.jpg", "snowman")

func _build_playground_screen() -> void:
	_add_activity_frame("playground_frame", Vector3(-17.5, FRAME_STAND_Y, -4.8),
		"res://assets/book/hall/p_garden.jpg", "garden")
	var slide := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide.png",
		Vector3(-9.0, 8.4, -5.5), 15.5)
	var swing := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_swing.png",
		Vector3(3.0, 8.4, -5.7), 15.0)
	var seesaw := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw.png",
		Vector3(15.0, 5.8, -5.4), 9.2)
	_register_target("slide", slide, "playground", "slide", 100.0, 1.10)
	_register_target("swing", swing, "playground", "swing", 100.0, 1.10)
	_register_target("seesaw", seesaw, "playground", "seesaw", 100.0, 1.12)

func _build_castle_screen() -> void:
	_add_activity_frame("castle_frame", Vector3(31.0, FRAME_STAND_Y, -4.8),
		"res://assets/book/hall/p_trampoline.jpg", "trampoline")
	var gate := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_gate.png",
		Vector3(56.0, 9.1, -5.8), 17.0)
	# The full castle is painted into the panorama. This aligned card is kept
	# hidden until focus so the first tap can still outline the entrance
	# without drawing a second gate over the castle facade.
	gate.visible = false
	_register_target("castle_gate", gate, "castle", "", 128.0, 1.08)

func _build_roshan_card() -> void:
	var card := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_roshan.png",
		Vector3(0.0, 4.0, 0.2), 7.8)
	m.g["lagoon_roshan_card"] = card
	m.player.visible = false

func _sync_roshan_card(delta_x: float = 0.0) -> void:
	var card: Sprite3D = m.g.get("lagoon_roshan_card") as Sprite3D
	var root_node: Node3D = stage.root()
	if card == null or not is_instance_valid(card) or root_node == null:
		return
	var local_player: Vector3 = m.player.position - root_node.position
	card.position = Vector3(local_player.x, local_player.y + 1.0, local_player.z + 0.2)
	if absf(delta_x) > 0.01:
		card.flip_h = delta_x < 0.0

func _build_ambient_life() -> void:
	m.g["lagoon_ambient_t"] = 0.0
	m.g["lagoon_ambient_cards"] = []
	_add_ambient_card("fir",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway.png",
		Vector3(-68.0, 8.0, -7.5), 14.0, 0.0, 0.55, 0.018)
	_add_ambient_card("fir",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway.png",
		Vector3(23.0, 7.4, -8.2), 12.5, 1.8, 0.48, 0.016)
	_add_ambient_card("flower",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		Vector3(-24.0, 3.0, -4.2), 5.2, 0.7, 0.72, 0.030)
	_add_ambient_card("flower",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		Vector3(23.0, 3.0, -4.3), 5.0, 2.4, 0.68, 0.028)
	_add_ambient_card("flower",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		Vector3(68.0, 3.2, -4.1), 5.4, 4.0, 0.64, 0.032)
	_add_ambient_card("cloud",
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_family_drift.png",
		Vector3(-60.0, 26.0, -15.5), 7.0, 1.1, 0.72, 0.0)

func _add_ambient_card(kind: String, path: String, pos: Vector3, height: float,
		phase: float, speed: float, amplitude: float) -> void:
	var card := _add_sprite(path, pos, height)
	card.name = "SkyLagoonAmbient_%s" % kind
	card.set_meta("ambient_kind", kind)
	card.set_meta("ambient_base", pos)
	card.set_meta("ambient_phase", phase)
	card.set_meta("ambient_speed", speed)
	card.set_meta("ambient_amplitude", amplitude)
	var cards: Array = m.g.get("lagoon_ambient_cards", [])
	cards.append(card)
	m.g["lagoon_ambient_cards"] = cards

func _tick_ambient_life(delta: float) -> void:
	var ambient_t: float = float(m.g.get("lagoon_ambient_t", 0.0)) + delta
	m.g["lagoon_ambient_t"] = ambient_t
	for value in (m.g.get("lagoon_ambient_cards", []) as Array):
		var card := value as Sprite3D
		if card == null or not is_instance_valid(card):
			continue
		var base: Vector3 = card.get_meta("ambient_base", card.position) as Vector3
		var phase: float = float(card.get_meta("ambient_phase", 0.0))
		var speed: float = float(card.get_meta("ambient_speed", 0.5))
		var kind: String = String(card.get_meta("ambient_kind", "flower"))
		if kind == "cloud":
			card.position = Vector3(
				wrapf(base.x + ambient_t * speed, -78.0, 78.0),
				base.y + sin(ambient_t * 0.32 + phase) * 0.18,
				base.z)
			continue
		var wave: float = sin(ambient_t * speed + phase)
		var amplitude: float = float(card.get_meta("ambient_amplitude", 0.02))
		card.rotation.z = wave * amplitude
		card.position = Vector3(
			base.x + wave * 0.04,
			base.y + absf(wave) * 0.025,
			base.z)
	var plane: Sprite3D = m.g.get("lagoon_plane_card") as Sprite3D
	if plane != null and is_instance_valid(plane):
		var plane_base: Vector3 = m.g.get("lagoon_plane_base", plane.position) as Vector3
		plane.position = plane_base + Vector3(
			0.0, sin(ambient_t * 1.05) * 0.12, 0.0)
		plane.rotation.z = sin(ambient_t * 0.72) * 0.010
		var plane_glow: Sprite3D = m.g.get("lagoon_plane_highlight") as Sprite3D
		if plane_glow != null and is_instance_valid(plane_glow):
			plane_glow.position = plane.position + Vector3(0.0, 0.0, -0.05)
			plane_glow.rotation.z = plane.rotation.z

func _add_backdrop(path: String, x: float) -> void:
	var root_node: Node3D = stage.root()
	if root_node == null:
		return
	var backdrop := Sprite3D.new()
	backdrop.name = "SkyLagoonBackdrop_%d" % roundi(x)
	backdrop.texture = load(path)
	backdrop.pixel_size = BACKDROP_TILE_SIZE.x / maxf(
		1.0, float(backdrop.texture.get_width()))
	# NEVER billboard the mural. A billboarded card swings about its OWN centre
	# to face the lens, so the moment the camera was not dead in front of a
	# tile the three cards stopped being coplanar, their painted edges pulled
	# apart, and the environment sky showed through the wedges between them as
	# vertical blue seams. The mural is one flat wall facing +Z (where the
	# side-on camera lives); its tiles then meet exactly, as the resolution
	# audit specifies.
	backdrop.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	# opaque pass + depth write: the wall sorts against the standees in front
	# of it by real depth instead of by transparent-queue distance
	backdrop.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	backdrop.shaded = false
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	backdrop.position = Vector3(x, BACKDROP_CENTER_Y, BACKDROP_Z)
	root_node.add_child(backdrop)

func _add_sprite(path: String, pos: Vector3, height: float) -> Sprite3D:
	var root_node: Node3D = stage.root()
	var sprite := Sprite3D.new()
	sprite.texture = load(path)
	sprite.pixel_size = height / maxf(1.0, float(sprite.texture.get_height()))
	# Standees are cutouts standing IN the diorama, not billboards: they stay
	# parallel to the mural so that panning the side-on lens slides them past
	# the painting instead of swivelling each one out of its painted setting.
	sprite.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	sprite.shaded = false
	sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	sprite.position = pos
	root_node.add_child(sprite)
	return sprite

func _add_activity_frame(id: String, pos: Vector3, page_path: String, minigame: String) -> void:
	var root_node: Node3D = stage.root()
	if root_node == null:
		return
	var holder := Node3D.new()
	holder.position = pos
	root_node.add_child(holder)
	var page := Sprite3D.new()
	page.texture = load(page_path)
	page.pixel_size = 7.25 / maxf(1.0, float(page.texture.get_height()))
	page.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	page.shaded = false
	page.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	page.position.z = -0.02
	holder.add_child(page)
	var frame := Sprite3D.new()
	frame.texture = load(FRAME_TEX)
	frame.pixel_size = 10.4 / maxf(1.0, float(frame.texture.get_height()))
	frame.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	frame.shaded = false
	frame.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	holder.add_child(frame)
	_register_target(id, holder, "frame", minigame, 92.0, 1.08, frame)

func _register_target(id: String, node: Node3D, kind: String, payload: String,
		radius_px: float, highlight_scale: float, outline_source: Sprite3D = null) -> void:
	var glow: Sprite3D
	if outline_source != null:
		glow = Sprite3D.new()
		glow.texture = outline_source.texture
		glow.pixel_size = outline_source.pixel_size
		glow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
		glow.shaded = false
		glow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		glow.modulate = Color(1.0, 0.80, 0.20, 0.82)
		glow.position.z = -0.04
		node.add_child(glow)
	else:
		glow = Sprite3D.new()
		if node is Sprite3D:
			var source := node as Sprite3D
			glow.texture = source.texture
			glow.pixel_size = source.pixel_size
			glow.billboard = BaseMaterial3D.BILLBOARD_DISABLED
			glow.shaded = false
			glow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			glow.modulate = Color(1.0, 0.82, 0.25, 0.72)
			glow.position = source.position + Vector3(0, 0, -0.05)
			var root_node: Node3D = stage.root()
			root_node.add_child(glow)
	glow.scale = Vector3.ONE * highlight_scale
	glow.visible = false
	var targets: Array = m.g.get("lagoon_promenade_targets", [])
	targets.append({
		"id": id,
		"node": node,
		"kind": kind,
		"payload": payload,
		"radius_px": radius_px,
		"highlight": glow,
		"highlight_scale": highlight_scale,
	})
	m.g["lagoon_promenade_targets"] = targets

func _target_at(screen_pos: Vector2) -> Dictionary:
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return {}
	var best: Dictionary = {}
	var best_dist := INF
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var node: Node3D = target.get("node") as Node3D
		if node == null or not is_instance_valid(node):
			continue
		var dist: float = cam.unproject_position(node.global_position).distance_to(screen_pos)
		if dist <= float(target.get("radius_px", 92.0)) and dist < best_dist:
			best = target
			best_dist = dist
	return best

func _focus(target: Dictionary) -> void:
	var target_id: String = String(target.get("id", ""))
	m.g["lagoon_promenade_focus"] = target_id
	m.g["lagoon_promenade_focus_t"] = 0.0
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var item: Dictionary = value as Dictionary
		var glow: Sprite3D = item.get("highlight") as Sprite3D
		if glow != null and is_instance_valid(glow):
			glow.visible = String(item.get("id", "")) == target_id
	var node: Node3D = target.get("node") as Node3D
	if node != null and is_instance_valid(node):
		m._sparkle_burst(node.global_position, Color(1.0, 0.84, 0.30))

func _clear_focus() -> void:
	m.g["lagoon_promenade_focus"] = ""
	for value in (m.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		var glow: Sprite3D = target.get("highlight") as Sprite3D
		if glow != null and is_instance_valid(glow):
			glow.visible = false

func _activate(target: Dictionary) -> void:
	var node: Node3D = target.get("node") as Node3D
	match String(target.get("kind", "")):
		"frame":
			m._mg2d_open(String(target.get("payload", "")))
		"plane":
			_bounce(node, 0.20)
			m._sparkle_burst(node.global_position, Color(0.65, 0.94, 1.0))
			m.show_msg("Roshan", "The pearl plane is ready for another sky adventure!")
		"playground":
			_bounce(node, 0.12)
			m.player.play_verb("giggle")
			m._sparkle_burst(node.global_position, Color(1.0, 0.65, 0.88))
		"castle":
			m.player.visible = true
			m._enter_castle_interior()

func _bounce(node: Node3D, tilt: float) -> void:
	if node == null or not is_instance_valid(node):
		return
	var tween: Tween = m.create_tween()
	tween.tween_property(node, "rotation:z", tilt, 0.16).set_trans(Tween.TRANS_BACK)
	tween.tween_property(node, "rotation:z", -tilt * 0.45, 0.18)
	tween.tween_property(node, "rotation:z", 0.0, 0.16)

func _set_walk_goal(screen_pos: Vector2) -> void:
	# one projection for the whole engine: the stage owns the band window, so
	# a tap here and a hold in walk_tick land on exactly the same spot
	var goal: Variant = stage.plane_goal(screen_pos)
	if goal is Vector2:
		m.g["ss_walk_goal"] = goal

func _set_spawn(x: float) -> void:
	var root_node: Node3D = stage.root()
	if root_node == null:
		return
	m.player.position = root_node.position + Vector3(x, 3.0, 0.0)
	m.player.vel = Vector3.ZERO
	m.player.rotation.y = PI
	var cam: Camera3D = m.player.cam
	if cam != null and cam.is_inside_tree():
		cam.fov = CAM_FOV
		# spawn straight onto the framing the glide would settle into — the
		# lens starts inside the mural instead of gliding in from off the edge
		var pan: float = stage.screen_pan_limit(m.g.get("ss_cfg", {}), cam)
		var cam_x: float = x if pan < 0.0 else clampf(x, -pan, pan)
		cam.position = root_node.position + Vector3(cam_x, CAM_H, CAM_DIST)
		cam.look_at(root_node.position + Vector3(cam_x, CAM_H, 0.0))
	_sync_roshan_card()
