extends CanvasLayer
# Developer mode: a live "look lab" for tuning the game on the fly.
# Toggle with F1 or ` (backtick), or via "Developer Mode" in the pause menu.
#
# What it offers:
#   - Camera angles & styles: chase / orbit / top-down / side / front / tripod,
#     plus FOV, chase distance/height and smoothing sliders.
#   - Lighting layers: sun (energy, warmth, angle, shadows), ambient light,
#     day/night, and the accent light layer (pearl + pulse lights).
#   - Rendering layers: fog, glow/bloom, god rays, caustic dapples, plankton,
#     color grade (brightness/contrast/saturation), exposure, render scale, MSAA.
#   - Look presets for quick side-by-side comparisons during playtests.
#   - "Save Look" persists the tuned look across launches (user://look_config.json);
#     "Copy for Feedback" puts the full settings JSON on the clipboard so a tester
#     can paste exactly what they were seeing into a feedback note.
#
# All sliders write straight into the live nodes, so every change is visible
# instantly. The camera override backs off during the slide / fairy-shooter
# minigames and cutscenes, which drive the camera themselves.

const LOOK_PATH := "user://look_config.json"
const SUN_COOL := Color(0.55, 0.80, 0.98)
const SUN_WARM := Color(1.0, 0.72, 0.42)

const LOOK_PRESETS := {
	"Crystal Clear": {"night": false, "fog_on": true, "fog_density": 0.0016, "glow_on": true, "glow_intensity": 0.55, "glow_bloom": 0.08, "grade_on": true, "brightness": 1.05, "contrast": 1.05, "saturation": 1.2, "exposure": 1.2, "sun_on": true, "sun_energy": 0.75, "sun_warm": 0.1, "ambient_energy": 1.1},
	"Deep & Moody": {"night": true, "fog_on": true, "fog_density": 0.009, "glow_on": true, "glow_intensity": 1.2, "glow_bloom": 0.3, "grade_on": true, "brightness": 0.94, "contrast": 1.12, "saturation": 0.95, "exposure": 1.0, "sun_on": true, "sun_energy": 0.35, "sun_warm": 0.0, "ambient_energy": 0.55},
	"Golden Hour": {"night": false, "fog_on": true, "fog_density": 0.0035, "glow_on": true, "glow_intensity": 0.9, "glow_bloom": 0.2, "grade_on": true, "brightness": 1.03, "contrast": 1.08, "saturation": 1.18, "exposure": 1.25, "sun_on": true, "sun_energy": 0.9, "sun_warm": 0.85, "ambient_energy": 0.85},
	"Storybook Soft": {"night": false, "fog_on": true, "fog_density": 0.006, "glow_on": true, "glow_intensity": 1.0, "glow_bloom": 0.35, "grade_on": true, "brightness": 1.08, "contrast": 0.96, "saturation": 1.05, "exposure": 1.1, "sun_on": true, "sun_energy": 0.6, "sun_warm": 0.35, "ambient_energy": 1.0},
}

var main: Node = null
var panel: Panel
var vb: VBoxContainer
var status: Label
var fps_label: Label
var ui := {}            # key -> control, so presets / saves can update the sliders
var mode_btns := {}
var open := false
var defaults := {}      # the look at launch, used by Reset

# ---- camera state (the override runs every frame in _process) ----
var cam_mode := "chase"
var cam_fov := 60.0
var cam_smooth := 6.0
var orbit_speed := 0.4
var orbit_radius := 20.0
var orbit_height := 8.0
var top_height := 44.0
var side_dist := 18.0
var side_height := 4.0
var orbit_angle := 0.0
var tripod_pos := Vector3.ZERO
var tripod_ok := false

# ---- layer toggles that have no single node property to read back ----
var sun_warm := 0.0
var god_rays_on := true
var plankton_on := true
var accent_on := true

func _ready() -> void:
	main = get_parent()
	layer = 20
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	_build_ui()
	_startup.call_deferred()

func _startup() -> void:
	# capture the launch look for Reset, then re-apply any saved look
	defaults = _collect_look()
	if FileAccess.file_exists(LOOK_PATH):
		var f := FileAccess.open(LOOK_PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if d is Dictionary:
				_apply_look(d)

func _unhandled_key_input(event: InputEvent) -> void:
	var k := event as InputEventKey
	if k != null and k.pressed and not k.echo:
		if k.physical_keycode == KEY_F1 or k.physical_keycode == KEY_QUOTELEFT:
			toggle()

func toggle() -> void:
	open = not open
	visible = open
	if open:
		_sync_ui()
		_status("Changes apply instantly. F1 or ` hides this panel.")

func _env() -> Environment:
	if main != null and main.we_node != null:
		return main.we_node.environment
	return null

# ============================ camera override ============================

func _process(delta: float) -> void:
	if open and fps_label != null:
		fps_label.text = "%d fps" % Engine.get_frames_per_second()
	if main == null or main.player == null or get_tree().paused:
		return
	var p: Node3D = main.player
	var cam: Camera3D = p.cam
	if cam == null or not cam.is_inside_tree():
		return
	if cam.fov != cam_fov:
		cam.fov = cam_fov
	if cam_mode == "chase":
		return
	# these sequences drive the camera themselves - leave them alone
	if main.intro_active or main.l2_cutscene_t >= 0.0:
		return
	if String(main.game) == "slide" or String(main.game) == "fairyshoot":
		return
	var pos: Vector3 = p.position
	var look: Vector3 = pos + Vector3(0, 1.5, 0)
	var target: Vector3 = cam.position
	match cam_mode:
		"orbit":
			orbit_angle += delta * orbit_speed
			target = pos + Vector3(cos(orbit_angle) * orbit_radius, orbit_height, sin(orbit_angle) * orbit_radius)
		"top":
			target = pos + Vector3(0.0, top_height, 0.01)
		"side":
			var right := Vector3(cos(p.yaw), 0.0, -sin(p.yaw))
			target = pos + right * side_dist + Vector3(0, side_height, 0)
		"front":
			var fwd := Vector3(sin(p.yaw), 0.0, cos(p.yaw))
			target = pos + fwd * side_dist + Vector3(0, side_height, 0)
		"tripod":
			if not tripod_ok:
				tripod_pos = cam.position
				tripod_ok = true
			target = tripod_pos
	cam.position = cam.position.lerp(target, 1.0 - pow(0.001, delta * cam_smooth / 6.0))
	if cam.position.distance_to(look) < 0.5:
		return
	if cam_mode == "top":
		cam.look_at(look, Vector3(0, 0, 1))
	else:
		cam.look_at(look)

func _set_cam_mode(id: String) -> void:
	cam_mode = id
	tripod_ok = false
	if id == "orbit" and main != null and main.player != null and main.player.cam != null:
		var p: Node3D = main.player
		orbit_angle = atan2(p.cam.position.z - p.position.z, p.cam.position.x - p.position.x)
	_status("Camera: " + id)

# ============================ collect / apply ============================

func _collect_look() -> Dictionary:
	var d := {
		"cam_mode": cam_mode, "cam_fov": cam_fov, "cam_smooth": cam_smooth,
		"orbit_speed": orbit_speed, "orbit_radius": orbit_radius, "orbit_height": orbit_height,
		"top_height": top_height, "side_dist": side_dist, "side_height": side_height,
		"sun_warm": sun_warm, "god_rays": god_rays_on, "plankton": plankton_on,
		"accent_lights": accent_on,
	}
	if main == null:
		return d
	d["night"] = bool(main.is_night)
	d["caustics"] = bool(main.caustics_enabled)
	var p: Node = main.player
	if p != null:
		d["chase_back"] = float(p.cam_back)
		d["chase_high"] = float(p.cam_high)
	var sun: DirectionalLight3D = main.sun_light
	if sun != null:
		d["sun_on"] = sun.visible
		d["sun_energy"] = sun.light_energy
		d["sun_elev"] = sun.rotation_degrees.x
		d["sun_azim"] = wrapf(sun.rotation_degrees.y, -180.0, 180.0)
		d["shadows"] = sun.shadow_enabled
	var env: Environment = _env()
	if env != null:
		d["ambient_energy"] = env.ambient_light_energy
		d["ambient_sky"] = env.ambient_light_sky_contribution
		d["fog_on"] = env.fog_enabled
		d["fog_density"] = env.fog_density
		d["glow_on"] = env.glow_enabled
		d["glow_intensity"] = env.glow_intensity
		d["glow_bloom"] = env.glow_bloom
		d["grade_on"] = env.adjustment_enabled
		d["brightness"] = env.adjustment_brightness
		d["contrast"] = env.adjustment_contrast
		d["saturation"] = env.adjustment_saturation
		d["exposure"] = env.tonemap_exposure
	var vp := get_viewport()
	if vp != null:
		d["render_scale"] = vp.scaling_3d_scale
		d["msaa"] = vp.msaa_3d != Viewport.MSAA_DISABLED
	return d

func _apply_look(d: Dictionary) -> void:
	if main == null:
		return
	if d.has("night") and bool(d["night"]) != bool(main.is_night):
		main.is_night = bool(d["night"])
		main._apply_time_of_day()
	if d.has("cam_mode"):
		cam_mode = String(d["cam_mode"])
		tripod_ok = false
	if d.has("cam_fov"): cam_fov = float(d["cam_fov"])
	if d.has("cam_smooth"): cam_smooth = float(d["cam_smooth"])
	if d.has("orbit_speed"): orbit_speed = float(d["orbit_speed"])
	if d.has("orbit_radius"): orbit_radius = float(d["orbit_radius"])
	if d.has("orbit_height"): orbit_height = float(d["orbit_height"])
	if d.has("top_height"): top_height = float(d["top_height"])
	if d.has("side_dist"): side_dist = float(d["side_dist"])
	if d.has("side_height"): side_height = float(d["side_height"])
	var p: Node = main.player
	if p != null:
		if d.has("chase_back"): p.cam_back = float(d["chase_back"])
		if d.has("chase_high"): p.cam_high = float(d["chase_high"])
	var sun: DirectionalLight3D = main.sun_light
	if sun != null:
		if d.has("sun_on"): sun.visible = bool(d["sun_on"])
		if d.has("sun_energy"): sun.light_energy = float(d["sun_energy"])
		if d.has("sun_warm"): _set_sun_warm(float(d["sun_warm"]))
		if d.has("sun_elev"): sun.rotation_degrees.x = float(d["sun_elev"])
		if d.has("sun_azim"): sun.rotation_degrees.y = float(d["sun_azim"])
		if d.has("shadows"): sun.shadow_enabled = bool(d["shadows"])
	var env: Environment = _env()
	if env != null:
		if d.has("ambient_energy"): env.ambient_light_energy = float(d["ambient_energy"])
		if d.has("ambient_sky"): env.ambient_light_sky_contribution = float(d["ambient_sky"])
		if d.has("fog_on"): env.fog_enabled = bool(d["fog_on"])
		if d.has("fog_density"): env.fog_density = float(d["fog_density"])
		if d.has("glow_on"): env.glow_enabled = bool(d["glow_on"])
		if d.has("glow_intensity"): env.glow_intensity = float(d["glow_intensity"])
		if d.has("glow_bloom"): env.glow_bloom = float(d["glow_bloom"])
		if d.has("grade_on"): env.adjustment_enabled = bool(d["grade_on"])
		if d.has("brightness"): env.adjustment_brightness = float(d["brightness"])
		if d.has("contrast"): env.adjustment_contrast = float(d["contrast"])
		if d.has("saturation"): env.adjustment_saturation = float(d["saturation"])
		if d.has("exposure"): env.tonemap_exposure = float(d["exposure"])
	if d.has("god_rays"): _set_god_rays(bool(d["god_rays"]))
	if d.has("caustics"): _set_caustics(bool(d["caustics"]))
	if d.has("plankton"): _set_plankton(bool(d["plankton"]))
	if d.has("accent_lights"): _set_accent(bool(d["accent_lights"]))
	var vp := get_viewport()
	if vp != null:
		if d.has("render_scale"): vp.scaling_3d_scale = float(d["render_scale"])
		if d.has("msaa"): vp.msaa_3d = Viewport.MSAA_4X if bool(d["msaa"]) else Viewport.MSAA_DISABLED
	_sync_ui()

# ============================ layer setters ============================

func _set_sun_warm(x: float) -> void:
	sun_warm = x
	if main != null and main.sun_light != null:
		(main.sun_light as DirectionalLight3D).light_color = SUN_COOL.lerp(SUN_WARM, x)

func _set_god_rays(on: bool) -> void:
	god_rays_on = on
	if main == null:
		return
	for gr in main.god_rays:
		var n: MeshInstance3D = gr["node"]
		if is_instance_valid(n):
			n.visible = on

func _set_caustics(on: bool) -> void:
	if main == null:
		return
	main.caustics_enabled = on
	if not on and main.caustics_plane != null and is_instance_valid(main.caustics_plane):
		(main.caustics_plane as MeshInstance3D).visible = false

func _set_plankton(on: bool) -> void:
	plankton_on = on
	if main != null and main.plankton_node != null and is_instance_valid(main.plankton_node):
		(main.plankton_node as GPUParticles3D).visible = on

func _set_accent(on: bool) -> void:
	accent_on = on
	if main == null:
		return
	for l in main.pearl_lights:
		if is_instance_valid(l):
			(l as OmniLight3D).visible = on
	for pl in main.pulse_lights:
		var l2: Light3D = pl["light"]
		if is_instance_valid(l2):
			l2.visible = on

# ============================ save / share ============================

func save_look() -> void:
	var f := FileAccess.open(LOOK_PATH, FileAccess.WRITE)
	if f != null:
		f.store_string(JSON.stringify(_collect_look()))
		_status("Look saved! It loads automatically next launch.")
	else:
		_status("Could not write " + LOOK_PATH)

func copy_feedback() -> void:
	var txt := JSON.stringify(_collect_look(), "  ")
	DisplayServer.clipboard_set(txt)
	print("[dev mode] current look settings:\n", txt)
	_status("Settings copied to clipboard (and printed to the console) - paste them into your feedback.")

func reset_look() -> void:
	if not defaults.is_empty():
		_apply_look(defaults)
	if FileAccess.file_exists(LOOK_PATH):
		DirAccess.remove_absolute(LOOK_PATH)
	_status("Back to the standard look; saved look cleared.")

func _status(txt: String) -> void:
	if status != null:
		status.text = txt

# ============================ UI ============================

func _build_ui() -> void:
	panel = Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.05, 0.08, 0.18, 0.92)
	sb.set_corner_radius_all(18)
	panel.add_theme_stylebox_override("panel", sb)
	panel.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	panel.offset_left = -450
	panel.offset_top = 10
	panel.offset_bottom = -10
	panel.offset_right = -10
	add_child(panel)

	var title := Label.new()
	title.text = "Developer Mode"
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", Color(0.7, 0.95, 1.0))
	title.position = Vector2(20, 12)
	panel.add_child(title)

	fps_label = Label.new()
	fps_label.text = ""
	fps_label.add_theme_font_size_override("font_size", 16)
	fps_label.add_theme_color_override("font_color", Color(0.6, 0.8, 0.6))
	fps_label.position = Vector2(230, 20)
	panel.add_child(fps_label)

	var close := Button.new()
	close.text = "X"
	close.add_theme_font_size_override("font_size", 20)
	close.custom_minimum_size = Vector2(52, 44)
	close.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	close.position = Vector2(-66, 8)
	close.pressed.connect(toggle)
	panel.add_child(close)

	var scroll := ScrollContainer.new()
	scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scroll.offset_top = 58
	scroll.offset_left = 14
	scroll.offset_right = -14
	scroll.offset_bottom = -12
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	panel.add_child(scroll)

	vb = VBoxContainer.new()
	vb.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vb.add_theme_constant_override("separation", 8)
	scroll.add_child(vb)

	status = Label.new()
	status.text = ""
	status.add_theme_font_size_override("font_size", 15)
	status.add_theme_color_override("font_color", Color(1.0, 0.9, 0.6))
	status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	status.custom_minimum_size = Vector2(0, 44)
	vb.add_child(status)

	# ---- look presets ----
	_section("Look Presets")
	var flow := HFlowContainer.new()
	vb.add_child(flow)
	for pname in LOOK_PRESETS.keys():
		var b := Button.new()
		b.text = pname
		b.add_theme_font_size_override("font_size", 15)
		b.custom_minimum_size = Vector2(0, 42)
		b.pressed.connect(func():
			_apply_look(LOOK_PRESETS[pname])
			_status("Preset: " + pname))
		flow.add_child(b)

	# ---- camera ----
	_section("Camera")
	var mflow := HFlowContainer.new()
	vb.add_child(mflow)
	var bg := ButtonGroup.new()
	for md in [["chase", "Chase"], ["orbit", "Orbit"], ["top", "Top-Down"], ["side", "Side"], ["front", "Front"], ["tripod", "Tripod"]]:
		var mb := Button.new()
		mb.text = md[1]
		mb.toggle_mode = true
		mb.button_group = bg
		mb.button_pressed = md[0] == cam_mode
		mb.add_theme_font_size_override("font_size", 15)
		mb.custom_minimum_size = Vector2(0, 42)
		mb.pressed.connect(_set_cam_mode.bind(md[0]))
		mflow.add_child(mb)
		mode_btns[md[0]] = mb
	_slider("fov", "Field of view", 40.0, 110.0, 1.0, cam_fov, func(x: float): cam_fov = x)
	_slider("chase_back", "Chase distance", 6.0, 34.0, 0.5, 16.0, func(x: float):
		if main.player != null: main.player.cam_back = x)
	_slider("chase_high", "Chase height", 1.0, 16.0, 0.5, 6.5, func(x: float):
		if main.player != null: main.player.cam_high = x)
	_slider("smooth", "Follow smoothing", 1.0, 20.0, 0.5, cam_smooth, func(x: float): cam_smooth = x)
	_slider("orbit_speed", "Orbit speed", 0.0, 1.5, 0.05, orbit_speed, func(x: float): orbit_speed = x)
	_slider("orbit_radius", "Orbit radius", 8.0, 50.0, 1.0, orbit_radius, func(x: float): orbit_radius = x)
	_slider("orbit_height", "Orbit height", 2.0, 40.0, 1.0, orbit_height, func(x: float): orbit_height = x)
	_slider("top_height", "Top-down height", 15.0, 90.0, 1.0, top_height, func(x: float): top_height = x)
	_slider("side_dist", "Side/front distance", 8.0, 40.0, 1.0, side_dist, func(x: float): side_dist = x)
	_slider("side_height", "Side/front height", 0.0, 20.0, 0.5, side_height, func(x: float): side_height = x)

	# ---- lighting ----
	_section("Lighting")
	_check("night", "Night time", false, func(on: bool):
		main.is_night = on
		main._apply_time_of_day()
		_sync_ui())
	_check("sun_on", "Sun light", true, func(on: bool):
		if main.sun_light != null: main.sun_light.visible = on)
	_slider("sun_energy", "Sun brightness", 0.0, 2.0, 0.05, 0.55, func(x: float):
		if main.sun_light != null: main.sun_light.light_energy = x)
	_slider("sun_warm", "Sun warmth", 0.0, 1.0, 0.05, 0.0, _set_sun_warm)
	_slider("sun_elev", "Sun angle (elevation)", -85.0, -10.0, 1.0, -55.0, func(x: float):
		if main.sun_light != null: main.sun_light.rotation_degrees.x = x)
	_slider("sun_azim", "Sun direction", -180.0, 180.0, 1.0, 30.0, func(x: float):
		if main.sun_light != null: main.sun_light.rotation_degrees.y = x)
	_check("shadows", "Sun shadows", true, func(on: bool):
		if main.sun_light != null: main.sun_light.shadow_enabled = on)
	_slider("ambient_energy", "Ambient brightness", 0.0, 2.0, 0.05, 0.9, func(x: float):
		var e := _env()
		if e != null: e.ambient_light_energy = x)
	_slider("ambient_sky", "Sky contribution", 0.0, 1.0, 0.05, 0.6, func(x: float):
		var e := _env()
		if e != null: e.ambient_light_sky_contribution = x)
	_check("accent", "Accent lights (pearls & coral)", true, _set_accent)

	# ---- rendering layers ----
	_section("Rendering Layers")
	_check("fog_on", "Fog", true, func(on: bool):
		var e := _env()
		if e != null: e.fog_enabled = on)
	_slider("fog_density", "Fog thickness", 0.0, 0.02, 0.0002, 0.0042, func(x: float):
		var e := _env()
		if e != null: e.fog_density = x)
	_check("glow_on", "Glow", true, func(on: bool):
		var e := _env()
		if e != null: e.glow_enabled = on)
	_slider("glow_intensity", "Glow intensity", 0.0, 2.0, 0.05, 0.75, func(x: float):
		var e := _env()
		if e != null: e.glow_intensity = x)
	_slider("glow_bloom", "Bloom", 0.0, 1.0, 0.02, 0.14, func(x: float):
		var e := _env()
		if e != null: e.glow_bloom = x)
	_check("god_rays", "God rays", true, _set_god_rays)
	_check("caustics", "Caustic dapples", true, _set_caustics)
	_check("plankton", "Plankton particles", true, _set_plankton)

	# ---- picture ----
	_section("Picture")
	_check("grade_on", "Color grade", true, func(on: bool):
		var e := _env()
		if e != null: e.adjustment_enabled = on)
	_slider("brightness", "Brightness", 0.5, 1.5, 0.01, 1.02, func(x: float):
		var e := _env()
		if e != null: e.adjustment_brightness = x)
	_slider("contrast", "Contrast", 0.5, 1.5, 0.01, 1.07, func(x: float):
		var e := _env()
		if e != null: e.adjustment_contrast = x)
	_slider("saturation", "Saturation", 0.0, 2.0, 0.02, 1.12, func(x: float):
		var e := _env()
		if e != null: e.adjustment_saturation = x)
	_slider("exposure", "Exposure", 0.5, 2.0, 0.02, 1.15, func(x: float):
		var e := _env()
		if e != null: e.tonemap_exposure = x)
	_slider("render_scale", "Render scale", 0.5, 1.0, 0.05, 1.0, func(x: float):
		var vp := get_viewport()
		if vp != null: vp.scaling_3d_scale = x)
	_check("msaa", "Smooth edges (MSAA 4x)", false, func(on: bool):
		var vp := get_viewport()
		if vp != null: vp.msaa_3d = Viewport.MSAA_4X if on else Viewport.MSAA_DISABLED)

	# ---- share ----
	_section("Save & Share")
	var save_b := Button.new()
	save_b.text = "Save Look"
	save_b.add_theme_font_size_override("font_size", 17)
	save_b.custom_minimum_size = Vector2(0, 48)
	save_b.pressed.connect(save_look)
	vb.add_child(save_b)
	var copy_b := Button.new()
	copy_b.text = "Copy for Feedback"
	copy_b.add_theme_font_size_override("font_size", 17)
	copy_b.custom_minimum_size = Vector2(0, 48)
	copy_b.pressed.connect(copy_feedback)
	vb.add_child(copy_b)
	var reset_b := Button.new()
	reset_b.text = "Reset Everything"
	reset_b.add_theme_font_size_override("font_size", 17)
	reset_b.custom_minimum_size = Vector2(0, 48)
	reset_b.pressed.connect(reset_look)
	vb.add_child(reset_b)
	var pad := Control.new()
	pad.custom_minimum_size = Vector2(0, 24)
	vb.add_child(pad)

func _section(txt: String) -> void:
	var spacer := Control.new()
	spacer.custom_minimum_size = Vector2(0, 6)
	vb.add_child(spacer)
	var l := Label.new()
	l.text = txt
	l.add_theme_font_size_override("font_size", 21)
	l.add_theme_color_override("font_color", Color(0.55, 0.9, 1.0))
	vb.add_child(l)

func _slider(key: String, txt: String, mn: float, mx: float, step: float, val: float, fn: Callable) -> void:
	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 8)
	var l := Label.new()
	l.text = txt
	l.add_theme_font_size_override("font_size", 15)
	l.custom_minimum_size = Vector2(158, 0)
	hb.add_child(l)
	var s := HSlider.new()
	s.min_value = mn
	s.max_value = mx
	s.step = step
	s.value = val
	s.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	s.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	s.custom_minimum_size = Vector2(0, 36)
	hb.add_child(s)
	var v := Label.new()
	v.text = _fmt(val)
	v.add_theme_font_size_override("font_size", 14)
	v.custom_minimum_size = Vector2(52, 0)
	v.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	hb.add_child(v)
	s.value_changed.connect(func(x: float):
		v.text = _fmt(x)
		fn.call(x))
	vb.add_child(hb)
	ui[key] = s
	ui[key + ":v"] = v

func _check(key: String, txt: String, val: bool, fn: Callable) -> void:
	var c := CheckButton.new()
	c.text = txt
	c.button_pressed = val
	c.add_theme_font_size_override("font_size", 15)
	c.custom_minimum_size = Vector2(0, 42)
	c.toggled.connect(fn)
	vb.add_child(c)
	ui[key] = c

func _fmt(x: float) -> String:
	if absf(x) < 0.05 and x != 0.0:
		return "%.4f" % x
	return "%.2f" % x

func _setv(key: String, val: float) -> void:
	if not ui.has(key):
		return
	(ui[key] as HSlider).set_value_no_signal(val)
	if ui.has(key + ":v"):
		(ui[key + ":v"] as Label).text = _fmt(val)

func _setc(key: String, val: bool) -> void:
	if ui.has(key):
		(ui[key] as CheckButton).set_pressed_no_signal(val)

func _sync_ui() -> void:
	# pull the live values back into the controls (presets, saves, night toggle
	# and the game's own quality switch all change things behind our back)
	if main == null:
		return
	_setv("fov", cam_fov)
	_setv("smooth", cam_smooth)
	_setv("orbit_speed", orbit_speed)
	_setv("orbit_radius", orbit_radius)
	_setv("orbit_height", orbit_height)
	_setv("top_height", top_height)
	_setv("side_dist", side_dist)
	_setv("side_height", side_height)
	if main.player != null:
		_setv("chase_back", float(main.player.cam_back))
		_setv("chase_high", float(main.player.cam_high))
	for mkey in mode_btns.keys():
		(mode_btns[mkey] as Button).set_pressed_no_signal(mkey == cam_mode)
	_setc("night", bool(main.is_night))
	var sun: DirectionalLight3D = main.sun_light
	if sun != null:
		_setc("sun_on", sun.visible)
		_setv("sun_energy", sun.light_energy)
		_setv("sun_warm", sun_warm)
		_setv("sun_elev", sun.rotation_degrees.x)
		_setv("sun_azim", wrapf(sun.rotation_degrees.y, -180.0, 180.0))
		_setc("shadows", sun.shadow_enabled)
	var env: Environment = _env()
	if env != null:
		_setv("ambient_energy", env.ambient_light_energy)
		_setv("ambient_sky", env.ambient_light_sky_contribution)
		_setc("fog_on", env.fog_enabled)
		_setv("fog_density", env.fog_density)
		_setc("glow_on", env.glow_enabled)
		_setv("glow_intensity", env.glow_intensity)
		_setv("glow_bloom", env.glow_bloom)
		_setc("grade_on", env.adjustment_enabled)
		_setv("brightness", env.adjustment_brightness)
		_setv("contrast", env.adjustment_contrast)
		_setv("saturation", env.adjustment_saturation)
		_setv("exposure", env.tonemap_exposure)
	_setc("god_rays", god_rays_on)
	_setc("caustics", bool(main.caustics_enabled))
	_setc("plankton", plankton_on)
	_setc("accent", accent_on)
	var vp := get_viewport()
	if vp != null:
		_setv("render_scale", vp.scaling_3d_scale)
		_setc("msaa", vp.msaa_3d != Viewport.MSAA_DISABLED)
