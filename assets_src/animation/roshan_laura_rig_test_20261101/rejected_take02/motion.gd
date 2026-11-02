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
	return (pulse(t, 0.70, 1.12, 1.22, 1.85)
		- 0.55 * pulse(t, 1.42, 1.92, 2.03, 2.38)
		+ pulse(t, 2.35, 2.77, 2.87, 3.50)
		- 0.45 * pulse(t, 3.12, 3.62, 3.73, 4.15)
		+ 0.65 * pulse(t, 4.30, 4.68, 4.78, 5.45)
		- 0.30 * pulse(t, 5.10, 5.50, 5.57, 6.05))


func sequence_pose(t: float) -> Dictionary:
	var pose: Dictionary = {}
	for name: String in bones:
		pose[name] = 0.0
	var greeting: float = pulse(t, 5.95, 7.70, 8.45, 10.20)
	var bank: float = (-6.0 * pulse(t, 0.65, 1.45, 3.10, 3.92)
		+ 5.0 * pulse(t, 3.65, 4.35, 5.20, 5.95))
	pose["Root"] = deg_to_rad(bank)
	pose["Torso"] = deg_to_rad(-0.7 * tail_effort(t) - 2.0 * greeting)
	# Preserve the source's rigid head/hair unit. Missing gaze/hair poses are reported.
	pose["Head"] = 0.0
	pose["LeftUpper"] = deg_to_rad(25.0 * greeting)
	pose["LeftFore"] = deg_to_rad(100.0 * greeting)
	var wave: float = 0.0
	if t >= 7.70 and t <= 8.45:
		var u: float = (t - 7.70) / 0.75
		wave = 6.0 * sin(TAU * u) * sin(PI * u)
	pose["LeftHand"] = deg_to_rad(wave)
	pose["TailA"] = deg_to_rad(2.7 * tail_effort(t) + 1.0 * greeting)
	pose["TailB"] = deg_to_rad(4.5 * tail_effort(t - 0.06) - 1.0 * greeting)
	pose["TailC"] = deg_to_rad(-3.6 * tail_effort(t - 0.12))
	pose["TailD"] = deg_to_rad(-2.7 * tail_effort(t - 0.18))
	pose["Fin"] = deg_to_rad(1.8 * tail_effort(t - 0.24))
	var settle: float = pulse(t, 9.8, 10.23, 10.30, 10.65)
	pose["TailB"] = float(pose["TailB"]) + deg_to_rad(0.6 * settle)
	pose["TailC"] = float(pose["TailC"]) - deg_to_rad(0.5 * settle)
	var travel: float = 360.0 * ease5((t - 0.65) / 3.0)
	travel -= 155.0 * ease5((t - 4.35) / 1.60)
	pose["position"] = Vector2(160.0 + travel, 31.0 - 12.0 * pulse(t, 0.8, 2.3, 3.1, 4.1))
	pose["eyes"] = "open"
	for blink_start: float in [0.28, 5.70, 10.55]:
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
	if t < 0.65:
		phase_label.text = "01  Notice and prepare"
	elif t < 3.65:
		phase_label.text = "02  Soft tail effort, then glide"
	elif t < 5.95:
		phase_label.text = "03  Bank and reverse the route"
	elif t < 10.20:
		phase_label.text = "04  Arrive, greet once, lower the hand"
	else:
		phase_label.text = "05  Resolve the tail and return to quiet"
	note_label.text = "Current front-view rig / source test / no new artwork"
	if t >= 3.65 and t < 5.95:
		note_label.text = "TURN GAP: profile and quarter-view surfaces are missing; this is a route reversal."
	elif t >= 6.0 and t < 10.2:
		note_label.text = "WAVE GAP: existing hand and rigid head/hair; new palm and follow-through poses needed."


func _process(delta: float) -> void:
	if automatic:
		time_seconds = minf(time_seconds + delta, LENGTH)
		set_sequence_time(time_seconds)
