class_name LightRig
extends RefCounted
# Phase 8 satellite: the ONE place that decides what colour a painted card is
# multiplied by (LIGHTING_2P5D_AUDIT_2026-08-02 §E2).
#
# Why this exists. Painted 2.5D flats are drawn unshaded — no light touches
# them — so `modulate` is the only per-card lever the engine has. Before this
# module every zone re-invented that lever inline, or skipped it: Sky Lagoon
# grew a real per-species day/night tint, the castle's seven declared depth
# planes all rendered at pure white, and `intensity_class` was set on cards
# that nothing ever read. A card 2 m behind Roshan looked exactly as present
# as the wall she was standing against.
#
# What it does. Multiply-only. A tint can darken and colour-shift a painting
# but never brighten it past what was painted, so it can never clip — which is
# precisely the failure the §E1 grade retune had to undo. Three factors
# compose:
#
#   depth   far cards drift toward the zone's atmospheric colour, near cards
#           settle back — the aerial-perspective cue that makes a stack of
#           flats read as a room instead of as stickers
#   night   the zone's night wash, previously Sky Lagoon-only
#   accent  per-card `intensity_class`, so a quiet background prop can sit
#           back from a focal one without repainting either
#
# What it must NOT touch. Light sources. A sconce, a fire, a glowing pearl is
# the thing the atmosphere is made of; dimming it with distance is backwards.
# Callers skip any card that carries a fixture material or a
# `castle_bloom_emitter` / `light_emitter` meta — see `emits_light()`.
#
# Satellite rules per CLAUDE.md: logic only, `main` by reference, no state.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# far_tint  : multiplied into cards at the far plane (atmospheric haze)
# near_tint : multiplied into cards at the near plane (foreground settles back)
# night_tint: whole-zone wash when m.is_night
# shadow    : contact-shadow colour for the zone, alpha included
#
# Kept deliberately gentle: these are multipliers on finished paintings, and
# the child's phone panel crushes deep blues. Nothing here drops a channel
# below ~0.85 in daylight.
const ZONES := {
	# Castle interiors: the background plate is the reference and stays
	# untouched (far_tint neutral). An interior has almost no real aerial haze,
	# so the honest depth cue is the other end — foreground framing props sit
	# outside the room's light pool and settle back, cooler and a little
	# darker. That is already how room_main_hall_front_left/right are painted;
	# this generalises it to every room's front layer.
	"castle_room": {
		"far_z": 0.0,
		"near_z": 4.0,
		"far_tint": Color(1.0, 1.0, 1.0),
		"near_tint": Color(0.90, 0.87, 0.94),
		"night_tint": Color(0.76, 0.79, 0.96),
		"shadow": Color(0.24, 0.25, 0.48, 0.58),
	},
	"sky_lagoon": {
		"far_z": -12.0,
		"near_z": 2.0,
		"far_tint": Color(0.93, 0.97, 1.02),
		"near_tint": Color(0.92, 0.94, 0.97),
		"night_tint": Color(0.72, 0.78, 0.96),
		"shadow": Color(0.30, 0.38, 0.56, 0.52),
	},
	"opera": {
		"far_z": 0.0,
		"near_z": 4.0,
		"far_tint": Color(0.92, 0.90, 0.98),
		"near_tint": Color(0.91, 0.88, 0.95),
		"night_tint": Color(0.80, 0.82, 0.97),
		"shadow": Color(0.22, 0.22, 0.42, 0.55),
	},
}

# A quiet prop sits back; a focal one keeps its full painted presence. These
# are intentionally shallow — the vocabulary matters more than the amount.
const INTENSITY := {
	"": 1.0,
	"focal": 1.0,
	"quiet": 0.96,
	"ambient": 0.94,
}

const NEUTRAL := Color(1.0, 1.0, 1.0, 1.0)

func has_zone(zone: String) -> bool:
	return ZONES.has(zone)

func emits_light(card: Node) -> bool:
	# Light sources are never atmospherically dimmed — they ARE the light.
	if card == null:
		return false
	return card.has_meta("castle_fixture_material") \
		or bool(card.get_meta("castle_bloom_emitter", false)) \
		or bool(card.get_meta("light_emitter", false))

func depth_ratio(zone: String, depth_z: float) -> float:
	# 0.0 at the zone's far plane, 1.0 at its near plane.
	if not ZONES.has(zone):
		return 0.5
	var data: Dictionary = ZONES[zone]
	var far_z: float = float(data["far_z"])
	var near_z: float = float(data["near_z"])
	if is_equal_approx(near_z, far_z):
		return 0.5
	return clampf((depth_z - far_z) / (near_z - far_z), 0.0, 1.0)

func card_tint(zone: String, depth_z: float,
		intensity_class: String = "") -> Color:
	# The play plane (ratio ~0.5) stays essentially untouched so Roshan and the
	# props she interacts with keep their painted colour; the ramp only bites
	# toward the two extremes.
	if not ZONES.has(zone):
		return NEUTRAL
	var data: Dictionary = ZONES[zone]
	var ratio: float = depth_ratio(zone, depth_z)
	var tint: Color = NEUTRAL
	if ratio < 0.5:
		tint = (data["far_tint"] as Color).lerp(NEUTRAL, ratio * 2.0)
	else:
		tint = NEUTRAL.lerp(data["near_tint"] as Color, (ratio - 0.5) * 2.0)
	if m != null and m.is_night:
		var night: Color = data["night_tint"]
		tint = Color(tint.r * night.r, tint.g * night.g, tint.b * night.b, 1.0)
	var accent: float = float(INTENSITY.get(intensity_class, 1.0))
	return Color(tint.r * accent, tint.g * accent, tint.b * accent, 1.0)

func shadow_tint(zone: String) -> Color:
	if not ZONES.has(zone):
		return Color(0.24, 0.25, 0.48, 0.58)
	var shadow: Color = ZONES[zone]["shadow"]
	if m != null and m.is_night:
		var night: Color = ZONES[zone]["night_tint"]
		return Color(shadow.r * night.r, shadow.g * night.g,
			shadow.b * night.b, shadow.a)
	return shadow

func apply_to_card(card: Sprite3D, zone: String, depth_z: float,
		intensity_class: String = "") -> void:
	# Single entry point for callers. Silently no-ops on light sources and on
	# cards whose alpha is being driven by a tween, so a fade-in is never
	# stomped mid-flight.
	if card == null or not is_instance_valid(card):
		return
	if emits_light(card):
		return
	var tint: Color = card_tint(zone, depth_z, intensity_class)
	card.modulate = Color(tint.r, tint.g, tint.b, card.modulate.a)
	card.set_meta("light_rig_zone", zone)
	card.set_meta("light_rig_depth", depth_z)
