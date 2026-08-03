class_name DayOneGuide
extends RefCounted
# The Day One movement-and-interaction guide (owner 2026-08-03).
#
# The four-panel Huluu storybook opener was cut, and with it the only thing in
# the game that ever addressed the child before play started. Nothing in this
# game has ever TAUGHT its three controls — touch-the-world travel, tap-a-thing,
# and two-press activation. They were discoverable only by accident.
#
# This teaches all three in the Sky Lagoon, in the world, with the promenade's
# own playground equipment and animals. It is not a slideshow and not a modal:
# it is a pulsing gold pointer, one voiced line per step, and a step that
# completes the moment she does the thing. She may wander, play, or ignore it
# entirely; the pointer waits. There is no timer, no failure, and no way to get
# it wrong.
#
# Satellite rules (CLAUDE.md): logic only, `main` by reference, every piece of
# mutable state on `main`. Visit state lives on `m.g`, the one persisted bit on
# `m.save_data`.

const POINTER_TEX := "res://assets/mg/star.png"
const SAVE_KEY := "day_one_guide_done"
# She has to actually arrive, not graze the goal — a pointer that clears
# because she happened to drift past teaches nothing.
const WALK_ARRIVE := 3.2
# Breath between a step completing and the next line, so the two voice clips
# never talk over each other.
const STEP_GAP := 1.1
# A step that has been on screen this long re-voices its line once. Four-year-
# olds look away; the pointer alone is not always enough to bring them back.
const RENUDGE_S := 22.0
# How far ahead the "go and find someone" pointer floats while no animal is on
# camera. Far enough to read as a direction, near enough to stay in frame.
const LEAD_AHEAD := 9.0
# The first walk: short enough that a four-year-old completes it on the first
# try, long enough that she has unmistakably travelled.
const FIRST_WALK_STEPS := 9.0

const STEPS: Array[Dictionary] = [
	{
		"id": "walk",
		"line": "Touch the sand, and I will walk there!",
		"done_line": "You did it! Touch anywhere and I will go.",
	},
	{
		# The pearl plane is parked at her feet on Day One, it is a registered
		# two-press target, and it is the thing she just arrived in — a better
		# first "tap a thing" than a toy she cannot see yet.
		"id": "play",
		"line": "Tap our pearl plane once to make it glow. Then tap it again!",
		"done_line": "Two taps! One to look, one to play. That works on everything.",
	},
	{
		# The arrival shore's otter and frog only appear once the plane leaves,
		# so this step deliberately leads her down the promenade — past the
		# slide, the swing and the seesaw — to wherever the live animal is.
		"id": "animal",
		"line": "Somebody is out there! Walk along and tap the little animal.",
		"done_line": "Hello, friend! Now the whole lagoon is yours.",
	},
]

var m: ReefMain
var promenade: SkyLagoonPromenade
var pointer: Sprite3D = null
var step := 0
var step_t := 0.0
var gap_t := 0.0
var renudged := false
var active := false
var walk_goal_x := 0.0

func _init(main: ReefMain, stage_owner: SkyLagoonPromenade) -> void:
	m = main
	promenade = stage_owner

# ---------------------------------------------------------------- lifecycle

static func is_finished(main: ReefMain) -> bool:
	return bool(main.save_data.get(SAVE_KEY, false))

func begin() -> void:
	# Never on top of a minigame, never on a save that has already been taught,
	# and never in a headless probe that did not ask for it by hand.
	if is_finished(m):
		return
	active = true
	step = 0
	step_t = 0.0
	gap_t = 0.6      # let the arrival line land before the first instruction
	renudged = false
	m.g["lagoon_guide_event"] = ""
	m.g["lagoon_guide_step"] = STEPS[0]["id"]

func clear() -> void:
	active = false
	_drop_pointer()
	m.g["lagoon_guide_step"] = ""

func finish() -> void:
	# Only ever written true, never back to false: the guide is progress, and
	# progress in this game is upgrade-only.
	active = false
	_drop_pointer()
	m.g["lagoon_guide_step"] = ""
	m.save_data[SAVE_KEY] = true
	m._write_save()

# ---------------------------------------------------------------- the loop

func tick(delta: float) -> void:
	if not active:
		return
	if gap_t > 0.0:
		gap_t -= delta
		if gap_t <= 0.0:
			_open_step()
		return
	step_t += delta
	_pulse(delta)
	if not renudged and step_t >= RENUDGE_S:
		renudged = true
		m.show_msg("Roshan", String(STEPS[step]["line"]), "talk")
	if _step_satisfied():
		_close_step()

func _open_step() -> void:
	if step >= STEPS.size():
		finish()
		return
	step_t = 0.0
	renudged = false
	m.g["lagoon_guide_step"] = STEPS[step]["id"]
	m.g["lagoon_guide_event"] = ""
	_place_pointer()
	m.show_msg("Roshan", String(STEPS[step]["line"]), "intro")

func _close_step() -> void:
	var done_line: String = String(STEPS[step]["done_line"])
	if pointer != null and is_instance_valid(pointer):
		m._sparkle_burst(pointer.global_position, Color(1.0, 0.86, 0.32))
	_drop_pointer()
	m.g["lagoon_guide_event"] = ""
	m.show_msg("Roshan", done_line, "win")
	step += 1
	if step >= STEPS.size():
		finish()
		return
	gap_t = STEP_GAP

func _step_satisfied() -> bool:
	match String(STEPS[step]["id"]):
		"walk":
			return absf(promenade.stage.px() - walk_goal_x) <= WALK_ARRIVE
		"animal":
			return String(m.g.get("lagoon_guide_event", "")) == "animal"
		"play":
			return String(m.g.get("lagoon_guide_event", "")) == "play"
	return true

# ---------------------------------------------------------------- pointer

func _place_pointer() -> void:
	_drop_pointer()
	var anchor: Vector3 = _step_anchor()
	var root_node: Node3D = promenade.stage.root()
	if root_node == null:
		return
	var texture: Texture2D = load(POINTER_TEX) as Texture2D
	if texture == null:
		return
	pointer = Sprite3D.new()
	pointer.name = "DayOneGuidePointer"
	pointer.texture = texture
	# Unshaded, non-billboarded, depth-tested — the same card contract every
	# other Sprite3D in this promenade honours, so it sorts by real depth
	# instead of floating in front of the world as UI.
	pointer.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	pointer.shaded = false
	pointer.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	pointer.pixel_size = 2.6 / maxf(1.0, float(texture.get_height()))
	pointer.modulate = Color(1.0, 0.86, 0.32, 0.95)
	pointer.position = anchor
	pointer.set_meta("source_asset_role", "tutorial_pointer")
	pointer.set_meta("source_object_id", "sky_lagoon:day_one_guide")
	root_node.add_child(pointer)

func _drop_pointer() -> void:
	if pointer != null and is_instance_valid(pointer):
		pointer.queue_free()
	pointer = null

func _pulse(delta: float) -> void:
	if pointer == null or not is_instance_valid(pointer):
		return
	# Hand-driven, not a Tween: a looping Tween on a node the guide frees mid
	# step is how orphaned tweens start writing to freed properties.
	# Re-read the anchor every frame: the animal step follows a moving card, and
	# its no-animal fallback leads ahead of a moving Roshan.
	var anchor: Vector3 = _step_anchor()
	var beat: float = sin(step_t * 4.2)
	pointer.scale = Vector3.ONE * (1.0 + beat * 0.16)
	pointer.position = Vector3(anchor.x, anchor.y + beat * 0.22, anchor.z)
	pointer.rotation.z += delta * 0.9

func _step_anchor() -> Vector3:
	# Every anchor is stage-local: the pointer is a child of the stage root, and
	# so are the plane and animal cards it points at. Mixing in main-space
	# player.position here is how a pointer ends up an origin-width off.
	match String(STEPS[step]["id"]):
		"walk":
			return _over_the_ground(walk_goal_x, 3.4)
		"play":
			var toy: Vector3 = promenade.guide_play_anchor()
			if toy != Vector3.ZERO:
				return toy
		"animal":
			var animal: Vector3 = promenade.guide_animal_anchor()
			if animal != Vector3.ZERO:
				return animal
			# No animal on camera yet: lead her along the promenade instead of
			# hovering over her own head.
			return _over_the_ground(promenade.stage.px() + LEAD_AHEAD, 4.2)
	return _over_the_ground(promenade.stage.px(), 4.2)

func _over_the_ground(x: float, height: float) -> Vector3:
	# BAND_Y is the depth-projection window, NOT a floor height — the walk
	# surface is the stage route. Reading BAND_Y here buries the pointer.
	return Vector3(x, promenade.guide_floor_y(x) + height, -3.0)

# The promenade authors the first walk goal at spawn, in the direction she has
# room to move, so the very first instruction can never point off the painted
# frame's edge.
func set_walk_goal_x(x: float) -> void:
	walk_goal_x = x
