class_name OperaImpClips
extends RefCounted
## Shared animation state clips for the Pearl Opera scuffle imps.
##
## The costumed scuffle crews ship exactly ONE sprite per career
## (assets/opera/worlds/actors/rival_<costume>.png). Every animation state is
## a transform clip over that same texture, so adding a costume costs one PNG
## and adding a state costs one row in CLIPS — never one file per costume per
## state. At 118 px on a roaming route the motion is what reads; frame art at
## that size is mostly invisible.
##
## Painted state art still wins wherever it exists: the world resolves
## rival_<costume>_bopped.png first and only falls back to a clip, so art can
## land later as a drop-in upgrade with no code change.
##
## The same principle is already used for the imp captain, who is marked by a
## drawn gold ring over the shared costume sprite rather than by his own
## costumed art.
##
## MERGE NOTE 2026-08-03: the painted state art this file was written to make
## unnecessary landed anyway (codex/opera-full-art-regen), and the roaming imps
## are now driven by the imp_ai brain through _apply_imp_pose, which does its
## own squash/tilt/lift/tint per pose. Live from here: state_path (the naming
## convention the world resolves costume art through) and the bopped_* clip the
## shoo-off still plays. The hop_* and hit_* clips are kept but currently
## unused — _apply_imp_pose supersedes them for roaming and for the survived
## hit. Re-point them or delete them, but do not assume they run today.

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
