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
# ANCHOR THE SET TO THE PAINTING (owner report 2026-07-27). A standee standing
# 12 units in FRONT of the mural parallaxes ~24% faster than the art it stands
# on, so panning the lens slid the whole playground across the painted lawn -
# nothing looked nailed down - and the castle-gate tap target drifted 237 px
# away from the painted door, which is why tapping the door never entered the
# castle. Every world card now shares the mural's depth: still its own sprite,
# still tappable, still animated, but welded to the scene it belongs to and
# with its tap target exactly on the art it represents. Screen sizes and the
# ground line are unchanged - each height and y was rescaled by the depth
# ratio (47 - z_new) / (47 - z_old). Roshan's band is ~18 units in front, so
# she still passes in front of all of it, exactly as she did at z -5.
# The small spread keeps the cards sorting against each other; 0.4 units of
# separation is under 1% of parallax, far below anything the eye reads.
const DRESS_Z := -17.90      # ambient firs, furthest of the anchored cards
const CLOUD_Z := -17.95      # sky, behind the treetops
const LANDMARK_Z := -17.85   # pearl plane, castle gate
const PLAY_Z := -17.80       # playground standees
const FRAME_Z := -17.75      # activity frames
const NEAR_Z := -17.70       # flowering shrubs, nearest of the anchored cards
# the activity frames stand on the lawn like easels (they used to hang at
# y 14.5, which put them in the painted sky above the treeline)
const FRAME_STAND_Y := 4.4

# THE ROUTE THROUGH THE LEVEL (owner request 2026-07-27: "she should have a
# clear routing path through the level as well"). The promenade is a path, not
# an open field: the stone way from the pearl-plane dock, along the shore,
# across the lawn, up the drawbridge, to the castle door. Waypoints are in
# PAINTED coordinates - (mural x, painted ground y) - because that is where
# the way visibly is; _walk_x/_walk_y convert them into the plane Roshan
# actually walks, which is 18 units nearer the lens and therefore does NOT
# share the painting's x scale once the lens pins at a painted edge.
# A touch anywhere still works; it resolves onto this line.
const ROUTE_PAINTED := [
	Vector2(-68.0, -2.6),    # the stepping stones by the pearl plane
	Vector2(-58.0, -3.4),    # the shore path
	Vector2(-40.0, -4.0),    # the path's near edge
	Vector2(-20.0, -3.6),    # onto the lawn
	Vector2(0.0, -3.4),      # the playground lawn
	Vector2(20.0, -3.6),     # the lawn's far side
	Vector2(34.0, -4.0),     # the way to the castle
	Vector2(43.0, -2.6),     # the drawbridge deck
	Vector2(52.5, -2.0),     # the castle doorstep - walking here goes inside
]
const CASTLE_DOOR_X := 52.5      # painted x of the door, shared with the gate card
const DOORSTEP_R := 1.5          # how close counts as arriving at the door
const DOORSTEP_REARM := 8.0      # walk this far back before it can fire again
# Roshan's card hangs 1.0 above her node and stands 7.8 tall, so her feet are
# 2.9 below the node: the offset that turns a painted ground height into hover.
const FOOT_OFFSET := 2.9

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
		# and she may never stroll off the side of the pinned frame
		"keep_on_screen": true,
		"edge_margin": 5.0,
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
	_refresh_route()
	# returning from the castle must not re-trigger the doorstep on frame one
	m.g["lagoon_castle_armed"] = not (from_castle or from_north)
	var spawn_at := -60.0                     # painted: beside the pearl plane
	if from_castle or from_north:
		spawn_at = 34.0                       # painted: the way in front of the castle
	_set_spawn(_walk_x(spawn_at))
	if from_castle:
		m.show_msg("Roshan", "Back outside! Tap a picture frame once to light it up, then tap it again to play.")
	else:
		m.show_msg("Roshan", "Our pearl plane landed! Tap the plane or a picture frame to explore.", "intro")

func tick(delta: float) -> void:
	if m.mg_kind != "":
		return
	_refresh_route()
	_tick_hold_travel(delta)
	var old_x: float = m.player.position.x
	stage.walk_tick(delta)
	_sync_roshan_card(m.player.position.x - old_x)
	_tick_ambient_life(delta)
	_tick_doorstep()
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
		Vector3(-65.0, 5.7, LANDMARK_Z), 13.7)   # the painted dock and water
	m.g["lagoon_plane_card"] = plane
	m.g["lagoon_plane_base"] = plane.position
	_register_target("plane", plane, "plane", "", 118.0, 1.12)
	var targets: Array = m.g.get("lagoon_promenade_targets", [])
	var plane_target: Dictionary = targets.back() as Dictionary
	m.g["lagoon_plane_highlight"] = plane_target.get("highlight")
	_add_activity_frame("runway_frame", Vector3(-34.5, FRAME_STAND_Y, FRAME_Z),
		"res://assets/book/hall/p_snowman.jpg", "snowman")

func _build_playground_screen() -> void:
	_add_activity_frame("playground_frame", Vector3(-17.5, FRAME_STAND_Y, FRAME_Z),
		"res://assets/book/hall/p_garden.jpg", "garden")
	# the open painted lawn runs from about x -22 to +18
	var slide := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide.png",
		Vector3(-9.0, 8.15, PLAY_Z), 19.1)
	var swing := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_swing.png",
		Vector3(3.0, 8.15, PLAY_Z), 18.4)
	var seesaw := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw.png",
		Vector3(15.0, 4.95, PLAY_Z), 11.35)
	_register_target("slide", slide, "playground", "slide", 100.0, 1.10)
	_register_target("swing", swing, "playground", "swing", 100.0, 1.10)
	_register_target("seesaw", seesaw, "playground", "seesaw", 100.0, 1.12)

func _build_castle_screen() -> void:
	_add_activity_frame("castle_frame", Vector3(33.3, FRAME_STAND_Y, FRAME_Z),
		"res://assets/book/hall/p_trampoline.jpg", "trampoline")
	# ON the painted door, not merely near it: the entrance is painted at
	# x 52.5 with its bridge running left to about x 42, and the card is sized
	# to sit over that entrance so the first tap outlines what the child sees.
	var gate := _add_sprite(
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_gate.png",
		Vector3(CASTLE_DOOR_X, 3.3, LANDMARK_Z), 13.9)
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
		Vector3(-57.0, 7.7, DRESS_Z), 16.65, 0.0, 0.55, 0.018)
	_add_ambient_card("fir",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway.png",
		Vector3(23.0, 7.05, DRESS_Z), 14.7, 1.8, 0.48, 0.016)
	_add_ambient_card("flower",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		Vector3(-24.0, 1.3, NEAR_Z), 6.55, 0.7, 0.72, 0.030)
	_add_ambient_card("flower",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		Vector3(23.5, 1.35, NEAR_Z), 6.3, 2.4, 0.68, 0.028)
	_add_ambient_card("flower",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		Vector3(62.0, 1.55, NEAR_Z), 6.8, 4.0, 0.64, 0.032)
	_add_ambient_card("cloud",
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_family_drift.png",
		Vector3(-60.0, 26.6, CLOUD_Z), 7.25, 1.1, 0.72, 0.0)

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
	page.pixel_size = 9.05 / maxf(1.0, float(page.texture.get_height()))
	page.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	page.shaded = false
	page.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	page.position.z = -0.02
	holder.add_child(page)
	var frame := Sprite3D.new()
	frame.texture = load(FRAME_TEX)
	frame.pixel_size = 12.95 / maxf(1.0, float(frame.texture.get_height()))
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

func _depth_ratio() -> float:
	# her plane sits at z 0, the painting at BACKDROP_Z: everything painted is
	# this much further from the lens than she is
	return CAM_DIST / (CAM_DIST - BACKDROP_Z)

func _walk_x(mural_x: float) -> float:
	# Where Roshan must STAND so she appears at a painted spot. While the lens
	# is free to centre her the two agree exactly; once it pins at a painted
	# edge they diverge by the depth ratio, which is why the drawbridge sat out
	# of reach of a straight x = painted_x assumption.
	# the lens is created deferred, so a build that runs on the very first
	# frames (the ocean-kingdom hub path) can reach here before it exists
	var cam: Camera3D = m.player.cam
	if cam == null or not cam.is_inside_tree():
		return mural_x
	var pan: float = stage.screen_pan_limit(m.g.get("ss_cfg", {}), cam)
	if pan < 0.0:
		return mural_x
	var ratio: float = _depth_ratio()
	if mural_x > pan:
		return pan + (mural_x - pan) * ratio
	if mural_x < -pan:
		return -pan + (mural_x + pan) * ratio
	return mural_x

func _walk_y(painted_y: float) -> float:
	# her hover so that her FEET land on a painted ground height
	return CAM_H + (painted_y - CAM_H) * _depth_ratio() + FOOT_OFFSET

func _refresh_route() -> void:
	# the lens pan limit depends on the viewport, so the painted route is
	# reprojected into walk space every tick rather than baked once
	var cfg: Dictionary = m.g.get("ss_cfg", {})
	if cfg.is_empty():
		return
	var route: Array = []
	for value in ROUTE_PAINTED:
		var point: Vector2 = value as Vector2
		route.append(Vector2(_walk_x(point.x), _walk_y(point.y)))
	cfg["route"] = route

func _tick_doorstep() -> void:
	# Walk to the end of the way and you are at the castle door, so the child
	# can simply follow the path in - the two-tap gate stays as the other road.
	# Armed only after she has walked clear of the door, so stepping back out
	# of the castle cannot bounce her straight back inside.
	var root_node: Node3D = stage.root()
	if root_node == null or m.mg_kind != "":
		return
	var door_x: float = _walk_x(CASTLE_DOOR_X)
	var x: float = m.player.position.x - root_node.position.x
	if x < door_x - DOORSTEP_REARM:
		m.g["lagoon_castle_armed"] = true
		return
	if not bool(m.g.get("lagoon_castle_armed", false)):
		return
	if x < door_x - DOORSTEP_R:
		return
	m.g["lagoon_castle_armed"] = false
	m.g["ss_walk_goal"] = null
	_clear_focus()
	m.player.visible = true
	m._enter_castle_interior()

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
	m.player.position = root_node.position + Vector3(
		x, stage.route_y(m.g.get("ss_cfg", {}), x, 3.0), 0.0)
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
