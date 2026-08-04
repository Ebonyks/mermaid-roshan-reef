class_name OperaImpClips
extends RefCounted
## Shared animation state clips for the Pearl Opera scuffle imps.
##
## Every delivered family now has authored state art. The live world resolves
## exact pose -> same-family cousin -> same-family idle. These clips are only
## small supporting envelopes and never authorize a cross-family costume swap.
## `state_path()` owns the family naming convention; the bopped clip owns the
## final bounded squash/spin/fade. The older hop and hit helpers remain only as
## compatible utilities and are not the primary acting path.

const CLIPS := {
	# Roaming hop, keyed to the route's own bob phase: the imp lands wide and
	# short at the bottom of the arc, rises tall and narrow at the top, and
	# leans into her direction of travel through the middle of it.
	"hop": {"squash": 0.10, "tilt": 0.06},
	# The recoil an imp survives (the captain's first bop): a wobble that
	# decays over its own length.
	"hit": {"squash": 0.30, "tilt": 0.20, "len": 0.30},
	# The friendly shoo-off, played while the sprite spins and fades away.
	"bopped": {"squash": 0.26, "spin": 0.6, "len": 0.62,
		"tint": Color(1.0, 0.94, 0.78)},
}

## Optional painted state art. Present -> used; absent -> the clip carries it.
const STATE_DIR := "res://assets/opera/worlds/actors"


static func _value(id: String, key: String, fallback: float = 0.0) -> float:
	var clip: Dictionary = CLIPS.get(id, {})
	return float(clip.get(key, fallback))


static func duration(id: String) -> float:
	return _value(id, "len")


static func state_path(costume: String, state: String) -> String:
	return "%s/rival_%s_%s.png" % [STATE_DIR, costume, state]


## --- roaming hop -----------------------------------------------------------

static func hop_scale(phase: float) -> Vector2:
	# Screen y grows downward, so the route's sin(phase) is +1 at the bottom
	# of the bob: that is the landing, and the landing is the wide pose.
	var k := _value("hop", "squash") * sin(phase)
	return Vector2(1.0 + k, 1.0 - k)


static func hop_tilt(phase: float, facing: float) -> float:
	# cos is a quarter cycle out of phase with the bob, so the lean peaks in
	# mid-arc rather than on the ground.
	return _value("hop", "tilt") * cos(phase) * facing


## --- survived hit ----------------------------------------------------------

static func hit_scale(t: float) -> Vector2:
	var span := duration("hit")
	if t < 0.0 or t >= span or span <= 0.0:
		return Vector2.ONE
	var u := t / span
	var k := _value("hit", "squash") * (1.0 - u) * cos(u * TAU * 1.25)
	return Vector2(1.0 + k, 1.0 - k)


static func hit_tilt(t: float) -> float:
	var span := duration("hit")
	if t < 0.0 or t >= span or span <= 0.0:
		return 0.0
	var u := t / span
	return _value("hit", "tilt") * (1.0 - u) * sin(u * TAU * 1.25)


## --- shoo-off --------------------------------------------------------------

static func bopped_squash() -> Vector2:
	var k := _value("bopped", "squash")
	return Vector2(1.0 + k, 1.0 - k)


static func bopped_stretch() -> Vector2:
	var k := _value("bopped", "squash") * 0.55
	return Vector2(1.0 - k, 1.0 + k)


static func bopped_spin() -> float:
	return _value("bopped", "spin")


static func bopped_tint() -> Color:
	var clip: Dictionary = CLIPS.get("bopped", {})
	return clip.get("tint", Color.WHITE) as Color
