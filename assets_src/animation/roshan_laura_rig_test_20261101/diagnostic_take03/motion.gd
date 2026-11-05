extends "res://seed.gd"
## Owner-requested source-only Laura phrasing on the unchanged front-view rig.
const LENGTH: float = 11.0
const FPS: int = 30
var phase_label: Label
var note_label: Label


func _ready() -> void:
	build_actor()
	automatic = false
	var bg: ColorRect = ColorRect.new()
	bg.color = Color("dceef0")
	bg.size = Vector2(1280, 720)
	bg.z_index = -20
	add_child(bg)
	var title: Label = Label.new()
	title.text = "ROSHAN  /  LAURA MOVEMENT STUDY"
	title.position = Vector2(42, 27)
	title.add_theme_color_override("font_color", Color("29445a"))
	title.add_theme_font_size_override("font_size", 25)
	add_child(title)
	phase_label = Label.new()
	phase_label.position = Vector2(42, 67)
	phase_label.add_theme_color_override("font_color", Color("3d6174"))
	phase_label.add_theme_font_size_override("font_size", 20)
	add_child(phase_label)
	note_label = Label.new()
	note_label.position = Vector2(42, 647)
	note_label.add_theme_color_override("font_color", Color("3d6174"))
	note_label.add_theme_font_size_override("font_size", 18)
	add_child(note_label)
	actor.scale = Vector2(0.62, 0.62)
	var library: AnimationLibrary = AnimationLibrary.new()
	var sequence: Animation = build_sequence()
	library.add_animation("sequence", sequence)
	player.add_animation_library("laura", library)
	ResourceSaver.save(sequence, "res://sequence.tres")
	set_sequence_time(0.0)


func tail_effort(t: float) -> float:
	# Two definite efforts with recovery/glide; no always-on idle pumping.
	return (pulse(t, 0.30, 0.70, 0.82, 1.35)
		- 0.60 * pulse(t, 1.03, 1.39, 1.46, 1.90)
		+ pulse(t, 1.80, 2.20, 2.32, 2.90)
		- 0.55 * pulse(t, 2.58, 2.98, 3.08, 3.65)
		+ 0.8 * pulse(t, 3.55, 3.97, 4.08, 4.58)
		- 0.65 * pulse(t, 4.20, 4.55, 4.65, 5.25))


func sequence_pose(t: float) -> Dictionary:
	var pose: Dictionary = {}
	for name: String in bones:
		pose[name] = 0.0
	var greeting: float = pulse(t, 5.30, 7.05, 8.20, 9.95)
	var effort: float = tail_effort(t)
	var right_swim: float = pulse(t, 0.25, 1.02, 2.85, 3.72)
	var left_return: float = pulse(t, 3.55, 4.30, 4.75, 5.45)
	var gather: float = pulse(t, 0.0, 0.18, 0.20, 0.53)
	var wave: float = 0.0
	if t >= 7.05 and t <= 8.20:
		var u: float = (t - 7.05) / 1.15
		wave = 6.0 * sin(TAU * 1.25 * u) * pow(sin(PI * u), 2.0)
	# Clockwise pitch sends the head toward rightward travel; opposite on return.
	pose["Root"] = deg_to_rad(28.0 * right_swim - 24.0 * left_return - 3.5 * greeting - 3.0 * gather)
	pose["Torso"] = deg_to_rad(1.8 * effort - 1.5 * greeting + 0.13 * wave)
	# The existing Head weights make this response visible; hair still shares this unit.
	pose["Head"] = deg_to_rad(-1.3 * effort + 1.8 * greeting - 0.10 * wave + 1.3 * gather)
	pose["LeftUpper"] = deg_to_rad(25.0 * greeting + 5.0 * right_swim - 0.22 * wave)
	# Forearm pixels include the hand. LeftHand itself is unweighted in this seed.
	pose["LeftFore"] = deg_to_rad(100.0 * greeting + 5.0 * effort * (1.0 - greeting) + wave)
	pose["LeftHand"] = 0.0
	pose["TailA"] = deg_to_rad(3.0 * effort + 1.3 * greeting - 0.10 * wave)
	pose["TailB"] = deg_to_rad(3.5 * tail_effort(t - 0.07) - 1.0 * greeting)
	pose["TailC"] = deg_to_rad(-3.0 * tail_effort(t - 0.14) + 0.08 * wave)
	pose["TailD"] = deg_to_rad(-2.7 * tail_effort(t - 0.21))
	pose["Fin"] = deg_to_rad(6.5 * tail_effort(t - 0.28) + 0.24 * wave)
	var settle: float = pulse(t, 9.72, 10.04, 10.11, 10.50)
	pose["TailB"] = float(pose["TailB"]) + deg_to_rad(0.8 * settle)
	pose["Fin"] = float(pose["Fin"]) - deg_to_rad(1.5 * settle)
	var travel: float = 410.0 * ease5((t - 0.25) / 3.0)
	travel -= 205.0 * ease5((t - 4.10) / 1.40)
	pose["position"] = Vector2(160.0 + travel, 31.0 - 22.0 * right_swim - 8.0 * left_return)
	pose["eyes"] = "open"
	for blink_start: float in [0.06, 5.52, 10.56]:
		var elapsed: float = t - blink_start
		if elapsed >= 0.0 and elapsed < 0.05:
			pose["eyes"] = "half"
		elif elapsed >= 0.05 and elapsed < 0.13:
			pose["eyes"] = "closed"
		elif elapsed >= 0.13 and elapsed < 0.21:
			pose["eyes"] = "half"
	return pose


func build_sequence() -> Animation:
	var animation: Animation = Animation.new()
	animation.length = LENGTH
	animation.loop_mode = Animation.LOOP_NONE
	var tracks: Dictionary = {}
	for name: String in bones:
		var track: int = animation.add_track(Animation.TYPE_VALUE)
		animation.track_set_path(track, NodePath(str(actor.get_path_to(bones[name])) + ":rotation"))
		animation.track_set_interpolation_type(track, Animation.INTERPOLATION_LINEAR)
		tracks[name] = track
	var position_track: int = animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(position_track, NodePath(".:position"))
	for state: String in ["half", "closed"]:
		var track: int = animation.add_track(Animation.TYPE_VALUE)
		var eye: Sprite2D = eye_half if state == "half" else eye_closed
		animation.track_set_path(track, NodePath(str(actor.get_path_to(eye)) + ":visible"))
		animation.value_track_set_update_mode(track, Animation.UPDATE_DISCRETE)
		tracks["eyes_" + state] = track
	for frame: int in range(1321):
		var t: float = frame / 120.0
		var pose: Dictionary = sequence_pose(t)
		for name: String in bones:
			var bone: Bone2D = bones[name]
			animation.track_insert_key(tracks[name], t, bone.rest.get_rotation() + float(pose[name]))
		animation.track_insert_key(position_track, t, pose["position"])
		for state: String in ["half", "closed"]:
			animation.track_insert_key(tracks["eyes_" + state], t, pose["eyes"] == state)
	return animation


func set_sequence_time(t: float) -> void:
	player.play("laura/sequence")
	player.seek(clampf(t, 0.0, LENGTH), true)
	if t < 0.25:
		phase_label.text = "01  Notice and prepare"
	elif t < 3.55:
		phase_label.text = "02  Push, recover, then glide"
	elif t < 5.50:
		phase_label.text = "03  Bank and reverse the route"
	elif t < 9.95:
		phase_label.text = "04  Arrive, greet once, lower the hand"
	else:
		phase_label.text = "05  Resolve the tail and return to quiet"
	note_label.text = "Current front-view rig / source test / no new artwork"
	if t >= 3.55 and t < 5.50:
		note_label.text = "TURN GAP: profile and quarter-view surfaces are missing; this is a route reversal."
	elif t >= 5.5 and t < 9.95:
		note_label.text = "WAVE GAP: existing fingers; independent palm, gaze and ponytail views still needed."


func _process(delta: float) -> void:
	if automatic:
		time_seconds = minf(time_seconds + delta, LENGTH)
		set_sequence_time(time_seconds)
