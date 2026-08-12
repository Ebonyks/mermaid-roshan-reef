class_name DollsGame
extends RefCounted
## Faron's sleepy-dolls catcher, presented on one bounded Canvas stage.
##
## The proven Opera nursery surface owns the one-finger catch grammar: press or
## drag the broad cradle beneath a falling baby, keep input live for the catch,
## and let every miss settle safely. Dolls supplies an approved world-tile
## presentation because the Opera widget placeholders are not shippable art.
## State remains on ReefMain so medals, saving, rewards, and callers stay intact.

const GOAL := 3
const PANEL_SIZE := Vector2(1024.0, 608.0)
const PANEL_MARGIN := 24.0
const CONTROL_REASON := "dolls_game"


class DollsNurserySurface extends OperaNurseryCatch:
	## Reuse OperaNurseryCatch's input, bounded faller state, mercy and no-fail
	## rules, while drawing only approved baby art over the accepted nursery
	## world tiles. The three P3/REPLACE widget files are never loaded here.
	const CATCH_RADIUS := 50.0
	const FOCUS_RADIUS := 59.0
	const FOCUS_PULSE := 2.0
	const FOCUS_BOB := 4.0
	const SAFE_BABY_EXTENT := 48.0
	const SAFE_HALO_RADIUS := 22.0
	const SAFE_VISUAL_EXTENT := 50.0
	const SAFE_Y := 0.956

	var safe_mat_style: StyleBoxFlat = null

	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		clip_contents = true
		set_process(false)
		for path: String in BABY_PATHS:
			var texture := load(path) as Texture2D
			if texture != null:
				textures.append(texture)
		backdrop_texture = null
		cradle_texture = null
		pillows_texture = null
		set_meta("no_fail", true)
		set_meta("live_input_gate_seconds", INPUT_MEMORY)
		set_meta("presentation", "approved_world_nursery_tiles")
		set_meta("placeholder_widgets_loaded", false)
		safe_mat_style = StyleBoxFlat.new()
		safe_mat_style.bg_color = Color(0.27, 0.20, 0.49, 0.90)
		safe_mat_style.border_color = Color(0.75, 0.66, 0.92, 0.96)
		safe_mat_style.set_border_width_all(7)
		safe_mat_style.set_corner_radius_all(38)

	func focus_rect_at(at_elapsed: float) -> Rect2:
		var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
		var focus_radius := FOCUS_RADIUS \
			+ sin(at_elapsed * 3.2) * FOCUS_PULSE
		var focus_y := catch_point.y - FOCUS_BOB \
			+ sin(at_elapsed * 4.6) * FOCUS_BOB
		return Rect2(
			Vector2(catch_point.x - focus_radius - 4.0, focus_y - 4.0),
			Vector2((focus_radius + 4.0) * 2.0, focus_radius + 8.0))

	func focus_envelope_rect() -> Rect2:
		var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
		var outer_radius := FOCUS_RADIUS + FOCUS_PULSE + 4.0
		return Rect2(
			Vector2(catch_point.x - outer_radius,
				catch_point.y - FOCUS_BOB * 2.0 - 4.0),
			Vector2(outer_radius * 2.0,
				FOCUS_BOB * 2.0 + 4.0 + outer_radius))

	func bowl_rect() -> Rect2:
		var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
		var outer_radius := minf(CATCH_RADIUS, size.x * 0.15) + 11.0
		return Rect2(catch_point + Vector2(-outer_radius, -11.0),
			Vector2(outer_radius * 2.0, outer_radius + 11.0))

	func safe_mat_rect() -> Rect2:
		return Rect2(
			Vector2(size.x * 0.035, size.y * 0.775),
			Vector2(size.x * 0.93, size.y * 0.225))

	func safe_landing_point(entry: Dictionary) -> Vector2:
		return Vector2(float(entry.get("x", 0.5)) * size.x,
			size.y * SAFE_Y)

	func safe_landing_rect(entry: Dictionary) -> Rect2:
		var center := safe_landing_point(entry)
		return Rect2(center - Vector2.ONE * SAFE_VISUAL_EXTENT * 0.5,
			Vector2.ONE * SAFE_VISUAL_EXTENT)

	func faller_rect(entry: Dictionary) -> Rect2:
		var extent := minf(86.0, size.x * 0.23)
		var center := Vector2(float(entry.get("x", 0.5)) * size.x,
			float(entry.get("y", 0.0)) * size.y)
		return Rect2(center - Vector2.ONE * extent * 0.5,
			Vector2.ONE * extent)

	func _draw() -> void:
		var panel := Rect2(Vector2.ZERO, size)
		draw_rect(panel.grow(-4.0), Color(0.66, 0.90, 0.88), false, 5.0)
		# Three large picture pips stay inside this layer (the legacy text HUD is
		# deliberately below it). Filled picture dots plus the babies resting in the
		# cradle communicate progress without reading.
		for index in range(goal):
			var pip_x := size.x * 0.5 + (float(index) - float(goal - 1) * 0.5) * 48.0
			draw_circle(Vector2(pip_x, 34.0), 18.0,
				Color(0.20, 0.14, 0.34, 0.92))
			draw_circle(Vector2(pip_x, 34.0), 12.0,
				Color(1.0, 0.72, 0.76) if index < caught
				else Color(0.94, 0.90, 1.0, 0.62))

		# A single padded safety mat is the honest code-native fallback for the
		# rejected flat pillow strip. Quilt seams and tufts keep the landing zone
		# legible without adding transparent sprite layers or scene nodes.
		var mat_rect := safe_mat_rect()
		if safe_mat_style != null:
			draw_style_box(safe_mat_style, mat_rect)
		for index in range(7):
			var seam_x := mat_rect.position.x + 28.0 + float(index) * mat_rect.size.x / 7.0
			draw_line(
				Vector2(seam_x, mat_rect.position.y + 14.0),
				Vector2(seam_x + 46.0, mat_rect.end.y - 14.0),
				Color(0.88, 0.80, 1.0, 0.25), 3.0, true)
			draw_circle(
				Vector2(seam_x + 23.0, mat_rect.get_center().y), 4.5,
				Color(1.0, 0.87, 0.66, 0.82))

		# The selected-skin child is explicitly drawn behind this parent. A pulsing
		# U-shaped focus halo belongs to the cradle itself: it bobs without a node
		# or tween and stays below Roshan's visible body instead of covering her.
		var catch_point := Vector2(catcher_x * size.x, size.y * 0.80)
		if input_live_t <= 0.0:
			var focus_radius := FOCUS_RADIUS \
				+ sin(elapsed * 3.2) * FOCUS_PULSE
			var focus_center := catch_point + Vector2(
				0.0, -FOCUS_BOB + sin(elapsed * 4.6) * FOCUS_BOB)
			var focus_alpha := 0.72 + (sin(elapsed * 3.2) + 1.0) * 0.10
			draw_arc(focus_center, focus_radius, 0.0, PI, 36,
				Color(1.0, 0.78, 0.28, focus_alpha), 6.0, true)
			draw_arc(focus_center, focus_radius - 9.0, 0.04, PI - 0.04, 36,
				Color(0.62, 0.95, 0.84, focus_alpha), 3.0, true)

		# Three layered lower semicircles read as one rounded open sling. There is
		# no concave fill or limb-like line work, and babies draw afterward so the
		# target can never paint over them.
		var catch_radius := minf(CATCH_RADIUS, size.x * 0.15)
		draw_arc(catch_point, catch_radius, 0.0, PI, 40,
			Color(0.20, 0.14, 0.34, 0.98), 22.0, true)
		draw_arc(catch_point, catch_radius, 0.0, PI, 40,
			Color(0.96, 0.79, 0.43, 0.98), 14.0, true)
		draw_arc(catch_point, catch_radius, 0.02, PI - 0.02, 40,
			Color(0.69, 0.94, 0.85, 0.98), 7.0, true)

		for landing: Dictionary in safe_landings:
			var landing_point := safe_landing_point(landing)
			var fade := clampf(float(landing.get("time", 0.0)) / 0.35, 0.0, 1.0)
			draw_arc(landing_point, SAFE_HALO_RADIUS, 0.0, TAU, 28,
				Color(0.74, 0.95, 0.93, fade * 0.75), 5.0, true)
			_draw_baby(int(landing.get("texture", 0)), landing_point,
				minf(SAFE_BABY_EXTENT, size.x * 0.21), fade)

		for entry: Dictionary in fallers:
			_draw_baby(
				int(entry.get("texture", 0)),
				Vector2(float(entry.get("x", 0.5)) * size.x,
					float(entry.get("y", 0.0)) * size.y),
				minf(86.0, size.x * 0.23))

		var shown := mini(settled.size(), 3)
		for index in range(shown):
			var spread := float(index) - float(shown - 1) * 0.5
			_draw_baby(settled[index],
				Vector2(catch_point.x + spread * 25.0, size.y * 0.89), 42.0)

var m: ReefMain
var layer: CanvasLayer = null
var backdrop: ColorRect = null
var world_backdrop: OperaWorldBackdrop2D = null
var surface: DollsNurserySurface = null
var catcher_card: TextureRect = null
var controls_owned := false


func _init(main: ReefMain) -> void:
	m = main


func build(fr: Dictionary) -> void:
	# A defensive close makes rapid/manual re-entry an exact replacement, never
	# a second live layer. The normal path is a no-op here.
	stage_close()
	m.g["spawned"] = 0
	m.g["caught"] = 0
	m.g["resolved"] = 0
	m.g["missed"] = 0
	m.g["next"] = 0.18
	m.g["dolls"] = []
	m.g["verb_t"] = 0.0
	m.g["timer"] = -1.0
	m._set_world_controls_enabled(false, CONTROL_REASON)
	controls_owned = true

	layer = CanvasLayer.new()
	layer.name = "DollsCatchLayer"
	layer.layer = 7
	m.add_child(layer)

	# One opaque Canvas fill prevents the still-migrating world from contributing
	# pixels through the authored inset's soft translucent edge.
	backdrop = ColorRect.new()
	backdrop.name = "DollsCanvasBacking"
	backdrop.color = Color(0.055, 0.04, 0.12, 1.0)
	backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(backdrop)

	world_backdrop = OperaWorldBackdrop2D.new()
	world_backdrop.name = "DollsApprovedNurseryBackdrop"
	world_backdrop.size = PANEL_SIZE
	world_backdrop.setup("nursery")
	layer.add_child(world_backdrop)

	surface = DollsNurserySurface.new()
	surface.name = "DollsCatchSurface"
	surface.size = PANEL_SIZE
	surface.baby_caught.connect(_on_baby_caught)
	surface.baby_missed.connect(_on_baby_missed)
	layer.add_child(surface)

	# The selected, approved Roshan appearance moves with the cradle. Drawing it
	# behind its parent surface makes the arms, cradle and every baby structurally
	# unable to be occluded by the character art.
	catcher_card = TextureRect.new()
	catcher_card.name = "DollsSelectedSkinCatcher"
	var skin_path: String = m.skin_sprite_path()
	if ResourceLoader.exists(skin_path):
		catcher_card.texture = load(skin_path) as Texture2D
	catcher_card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	catcher_card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	catcher_card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	catcher_card.size = Vector2(200.0, 245.0)
	catcher_card.show_behind_parent = true
	surface.add_child(catcher_card)

	_layout_surface()
	surface.start(GOAL)
	_layout_catcher_card()
	# Accessibility debt is explicit: the available Faron nursery catch clip
	# says five, while this legacy activity's fixed goal is three. Keep the live
	# pointer and generic spoken greeting; do not play a semantically false clip.
	surface.set_meta("objective_recording_gap", "faron_catch_three")
	surface.set_meta("visual_pointer", true)
	m.g["dolls_layer"] = layer
	m.g["dolls_backdrop"] = world_backdrop
	m.g["dolls_surface"] = surface
	m.g["dolls_catcher"] = catcher_card
	_sync_state()
	m.show_msg(fr["fname"], "Catch 3 sleepy dolls in your arms!")


func _layout_surface() -> void:
	if surface == null or not is_instance_valid(surface):
		return
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	var available := Vector2(
		maxf(1.0, viewport_size.x - PANEL_MARGIN * 2.0),
		maxf(1.0, viewport_size.y - PANEL_MARGIN * 2.0))
	var panel_scale := minf(1.0, minf(
		available.x / PANEL_SIZE.x, available.y / PANEL_SIZE.y))
	panel_scale = maxf(0.1, panel_scale)
	surface.scale = Vector2.ONE * panel_scale
	surface.position = (viewport_size - PANEL_SIZE * panel_scale) * 0.5
	if world_backdrop != null and is_instance_valid(world_backdrop):
		world_backdrop.scale = surface.scale
		world_backdrop.position = surface.position
	if backdrop != null and is_instance_valid(backdrop):
		backdrop.position = Vector2.ZERO
		backdrop.size = viewport_size
	_layout_catcher_card()


func _layout_catcher_card() -> void:
	if surface == null or not is_instance_valid(surface) \
			or catcher_card == null or not is_instance_valid(catcher_card):
		return
	catcher_card.position = Vector2(
		surface.catcher_x * PANEL_SIZE.x - catcher_card.size.x * 0.5,
		PANEL_SIZE.y * 0.36)


func _sync_state() -> void:
	if surface == null or not is_instance_valid(surface):
		return
	m.g["spawned"] = surface.spawned
	m.g["caught"] = surface.caught
	m.g["resolved"] = surface.caught + surface.missed
	m.g["missed"] = surface.missed
	m.g["next"] = surface.spawn_t
	m.g["verb_t"] = surface.input_live_t
	m.g["dolls"] = surface.fallers


func _on_baby_caught(_quality: float) -> void:
	_sync_state()
	if m.voice != null:
		m.voice.pitch_scale = 1.0 + randf() * 0.25
		m.voice.play()


func _on_baby_missed() -> void:
	_sync_state()
	# The exact recorded Faron miss stays rate-limited so close landings never
	# talk over one another.
	m._say("faron", "miss", 3.0)


func _tick_dolls(_delta: float, fr: Dictionary) -> void:
	if surface == null or not is_instance_valid(surface) \
			or not surface.is_inside_tree():
		return
	_sync_state()
	_layout_catcher_card()
	m.hud_game.text = "Sleepy dolls  " + m._pips(surface.caught, GOAL, "🎎")
	if surface.caught >= GOAL:
		m._end_game(true, fr,
			"You tucked in %d dolls! All cozy now." % surface.caught)


func stage_close() -> void:
	if surface != null and is_instance_valid(surface):
		surface.stop()
	var old_layer: CanvasLayer = layer
	if old_layer != null and is_instance_valid(old_layer):
		if old_layer.get_parent() != null:
			old_layer.get_parent().remove_child(old_layer)
		old_layer.queue_free()
	catcher_card = null
	surface = null
	world_backdrop = null
	backdrop = null
	layer = null
	if m != null and controls_owned:
		m._set_world_controls_enabled(true, CONTROL_REASON)
	controls_owned = false
