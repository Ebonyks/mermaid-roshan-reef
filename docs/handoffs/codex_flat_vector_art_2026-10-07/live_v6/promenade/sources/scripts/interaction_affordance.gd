class_name InteractionAffordance
extends RefCounted
# One non-reading touch vocabulary for world objects. Color is paired with
# motion so the distinction remains legible without relying on hue alone:
# gold twinkles promise a local animation; deep-blue breaths promise a real
# activity or state change; bright-red beacons mark plot progress.

const ANIMATION := "animation"
const INTERACTION := "interaction"
const PLOT := "plot"

const GOLD_IDLE := Color(1.0, 0.72, 0.20, 0.18)
const GOLD_FOCUS := Color(1.0, 0.84, 0.34, 0.82)
const BLUE_IDLE := Color(0.16, 0.38, 0.82, 0.24)
const BLUE_FOCUS := Color(0.24, 0.56, 1.0, 0.88)
const RED_IDLE := Color(1.0, 0.08, 0.14, 0.42)
const RED_FOCUS := Color(1.0, 0.18, 0.22, 0.98)

static func normalize(kind: String) -> String:
	if kind == ANIMATION or kind == PLOT:
		return kind
	return INTERACTION

static func color(kind: String, focused: bool) -> Color:
	var normalized: String = normalize(kind)
	if normalized == ANIMATION:
		return GOLD_FOCUS if focused else GOLD_IDLE
	if normalized == PLOT:
		return RED_FOCUS if focused else RED_IDLE
	return BLUE_FOCUS if focused else BLUE_IDLE

static func sparkle_color(kind: String) -> Color:
	match normalize(kind):
		ANIMATION:
			return Color(1.0, 0.84, 0.34)
		PLOT:
			return Color(1.0, 0.16, 0.22)
		_:
			return Color(0.34, 0.68, 1.0)

static func pulse_speed(kind: String, focused: bool) -> float:
	var normalized: String = normalize(kind)
	if normalized == ANIMATION:
		return 5.2 if focused else 3.4
	if normalized == PLOT:
		return 6.4 if focused else 4.6
	return 2.8 if focused else 1.7

static func pulse_amount(kind: String, focused: bool) -> float:
	var normalized: String = normalize(kind)
	if normalized == ANIMATION:
		return 0.050 if focused else 0.022
	if normalized == PLOT:
		return 0.180 if focused else 0.120
	return 0.075 if focused else 0.035

static func emission_energy(kind: String, focused: bool) -> float:
	if normalize(kind) == PLOT:
		return 1.65 if focused else 1.05
	return 0.95 if focused else 0.55

static func rotation_speed(kind: String) -> float:
	match normalize(kind):
		ANIMATION:
			return 1.35
		PLOT:
			return 1.05
		_:
			return 0.72

static func opacity_floor(kind: String) -> float:
	return 0.68 if normalize(kind) == PLOT else 0.90

static func make_radial_halo(kind: String, size: Vector2) -> Sprite3D:
	var gradient_texture := GradientTexture2D.new()
	gradient_texture.width = 128
	gradient_texture.height = 128
	gradient_texture.fill = GradientTexture2D.FILL_RADIAL
	gradient_texture.fill_from = Vector2(0.5, 0.5)
	gradient_texture.fill_to = Vector2(0.5, 0.0)
	var gradient := Gradient.new()
	gradient.set_color(0, Color(1.0, 1.0, 1.0, 0.90))
	gradient.set_color(1, Color(1.0, 1.0, 1.0, 0.0))
	gradient_texture.gradient = gradient

	# Castle rooms are intentionally a Sprite3D-only picture stage. This uses
	# the same runtime gradient without introducing model/mesh art or a texture
	# asset. A neutral texture lets one pooled card change category and size.
	var halo := Sprite3D.new()
	halo.texture = gradient_texture
	halo.shaded = false
	halo.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	halo.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	configure_radial_halo(halo, kind, size)
	return halo

static func configure_radial_halo(
		halo: Sprite3D, kind: String, size: Vector2) -> void:
	halo.pixel_size = size.x / 128.0
	halo.scale = Vector3(1.0, size.y / maxf(size.x, 0.001), 1.0)
	halo.modulate = color(kind, false)
	halo.set_meta("affordance_kind", normalize(kind))
	halo.set_meta("affordance_base_scale", halo.scale)


static func make_radial_halo_2d(kind: String, size: Vector2) -> Sprite2D:
	var gradient_texture := GradientTexture2D.new()
	gradient_texture.width = 128
	gradient_texture.height = 128
	gradient_texture.fill = GradientTexture2D.FILL_RADIAL
	gradient_texture.fill_from = Vector2(0.5, 0.5)
	gradient_texture.fill_to = Vector2(0.5, 0.0)
	var gradient := Gradient.new()
	gradient.set_color(0, Color(1.0, 1.0, 1.0, 0.90))
	gradient.set_color(1, Color(1.0, 1.0, 1.0, 0.0))
	gradient_texture.gradient = gradient
	var halo := Sprite2D.new()
	halo.texture = gradient_texture
	configure_radial_halo_2d(halo, kind, size)
	return halo


static func configure_radial_halo_2d(
		halo: Sprite2D, kind: String, size: Vector2) -> void:
	if halo == null:
		return
	halo.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	halo.scale = size / Vector2(128.0, 128.0)
	halo.position = Vector2.ZERO
	halo.modulate = color(kind, false)
	halo.set_meta("affordance_kind", normalize(kind))
	halo.set_meta("affordance_base_scale", halo.scale)
