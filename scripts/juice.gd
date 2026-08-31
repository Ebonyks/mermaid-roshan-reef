class_name Juice
extends RefCounted
# The impact primitives combat feel is built from (combat wing 2026-08):
# squash, flash, camera micro-shake, haptics. All cosmetic — game logic may
# never gate on these. Allocation-light: transient tweens on existing nodes,
# no new nodes at hit time, nothing measurable on the M11. Hitstop is data
# (enemy["hitstop"], owned by HitEngine, honored by each encounter's tick) —
# never Engine.time_scale, which belongs to the probes.
#
# Since the animation-improvement wing (design 06 §20, 2026-08-31) this file
# is also the shared feedback vocabulary for BOTH canvases: new decorative
# tweens reuse these primitives instead of hand-rolling the same pattern per
# site. Everything here is feedback motion under DL-MOT-07 — it never counts
# as authored character animation.

# Wing bounds (checked by tools/audit_animation_polish.py): decorative
# motion shorter than MIN_DUR cannot be read on the target panel, longer
# than MAX_DUR starts feeling like a wait to a four-year-old, and a full
# scale-pulse cycle under MIN_PULSE_PERIOD approaches flicker territory.
const MIN_DUR := 0.06
const MAX_DUR := 1.8
const MIN_PULSE_PERIOD := 0.30

static var haptics_enabled := true   # parent settings toggle lands later

# Impact deform: quick squash, elastic recover. Applies to the art child
# when the encounter animates the root's scale every frame (imp wobble), so
# the two never fight; falls back to the node itself (bunny cards, props).
static func squash(node: Node3D, big: bool = false) -> void:
	if node == null or not node.is_inside_tree():
		return
	var target: Node3D = node
	for child in node.get_children():
		if child is Node3D:
			target = child as Node3D
			break
	# Re-entrancy (alpha audit 2026-08-05): under mash tapping a second squash
	# used to read the FIRST squash's mid-deform scale as its "base" and
	# restore to that — enemies drifted permanently squashed. The true rest
	# scale is remembered once on the node and every squash restores to it;
	# the previous tween is killed so two never fight over the same property.
	var base: Vector3
	if target.has_meta("juice_rest_scale"):
		base = target.get_meta("juice_rest_scale")
	else:
		base = target.scale
		target.set_meta("juice_rest_scale", base)
	if target.has_meta("juice_squash_tw"):
		var old: Tween = target.get_meta("juice_squash_tw")
		if old != null and old.is_valid():
			old.kill()
	var mult: float = 1.3 if big else 1.18
	var tw: Tween = target.create_tween()
	target.set_meta("juice_squash_tw", tw)
	tw.tween_property(target, "scale", Vector3(base.x * mult, base.y * (2.0 - mult), base.z * mult), 0.08).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(target, "scale", base, 0.18).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)

# White blink for sprite-card targets (castle bunny cards, cutout enemies).
# Mesh enemies are skipped on purpose: their materials are shared cache
# entries, so tinting one would flash every enemy wearing it — meshes get
# squash + sparkle instead.
static func flash(node: Node3D) -> void:
	# SpriteBase3D covers Sprite3D AND AnimatedSprite3D — the old Sprite3D
	# check silently skipped every AnimatedSprite3D enemy (alpha audit
	# 2026-08-05), so animated foes never blinked on hit.
	var sprite: SpriteBase3D = node as SpriteBase3D
	if sprite == null:
		for child in node.get_children():
			if child is SpriteBase3D:
				sprite = child as SpriteBase3D
				break
	if sprite == null or not sprite.is_inside_tree():
		return
	# rest-modulate remembered once: interrupting a flash mid-tween must not
	# strand the sprite tinted (same capture rule as squash)
	var base: Color
	if sprite.has_meta("juice_rest_modulate"):
		base = sprite.get_meta("juice_rest_modulate")
	else:
		base = sprite.modulate
		sprite.set_meta("juice_rest_modulate", base)
	if sprite.has_meta("juice_flash_tw"):
		var old: Tween = sprite.get_meta("juice_flash_tw")
		if old != null and old.is_valid():
			old.kill()
	var tw: Tween = sprite.create_tween()
	sprite.set_meta("juice_flash_tw", tw)
	tw.tween_property(sprite, "modulate", Color(1.6, 1.6, 1.5, base.a), 0.06)
	tw.tween_property(sprite, "modulate", base, 0.10)

# One shared micro-shake — SUPER moments only, deliberately small
# (vestibular comfort + M11 overdraw budget both prefer restraint).
static func shake(cam: Camera3D, strength: float = 0.06, dur: float = 0.12) -> void:
	if cam == null or not cam.is_inside_tree():
		return
	var base_h: float = cam.h_offset
	var tw: Tween = cam.create_tween()
	tw.tween_property(cam, "h_offset", base_h + strength, dur * 0.25)
	tw.tween_property(cam, "h_offset", base_h - strength * 0.6, dur * 0.35)
	tw.tween_property(cam, "h_offset", base_h, dur * 0.4)

static func haptic(ms: int) -> void:
	if haptics_enabled and OS.has_feature("mobile"):
		Input.vibrate_handheld(ms)

# HUD/card entrance on the 2D canvas: grow + fade in to the node's own rest
# state, rest-capture and prior-kill per the squash rules above so a rapid
# replay can never compound. A Control's pivot defaults to its top-left
# corner, which would swing the card away from its asserted rect during the
# grow — the pivot is centered so `position`/`size` stay probe-exact.
static func pop_in(ci: CanvasItem, dur: float = 0.30) -> void:
	if ci == null or not ci.is_inside_tree():
		return
	var ctrl := ci as Control
	var n2 := ci as Node2D
	if ctrl == null and n2 == null:
		return
	if ctrl != null:
		ctrl.pivot_offset = ctrl.size * 0.5
	var rest_scale: Vector2
	if ci.has_meta("juice_rest_scale2d"):
		rest_scale = ci.get_meta("juice_rest_scale2d")
	else:
		rest_scale = ctrl.scale if ctrl != null else n2.scale
		ci.set_meta("juice_rest_scale2d", rest_scale)
	var rest_alpha: float
	if ci.has_meta("juice_rest_alpha"):
		rest_alpha = ci.get_meta("juice_rest_alpha")
	else:
		rest_alpha = ci.modulate.a
		ci.set_meta("juice_rest_alpha", rest_alpha)
	if ci.has_meta("juice_pop_tw"):
		var old: Tween = ci.get_meta("juice_pop_tw")
		if old != null and old.is_valid():
			old.kill()
	var tw: Tween = ci.create_tween()
	ci.set_meta("juice_pop_tw", tw)
	tw.set_parallel(true)
	tw.tween_property(ci, "scale", rest_scale, dur).from(rest_scale * 0.82).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(ci, "modulate:a", rest_alpha, dur * 0.6).from(0.0)

# Attack/QTE telegraph: gentle puffs that always end at the remembered rest
# scale. Canvas-agnostic on purpose: the scale flows through the property
# path as Variant, so one primitive serves today's spatial arenas AND the
# true-2D migration's cards without pinning a spatial type — which would
# also expand the GAME2D 3D-API debt this project only shrinks. Replaces
# the raw `set_loops` pattern whose loop targets froze whatever mid-deform
# scale the build frame happened to see — under a concurrent squash the
# enemy drifted permanently puffed (stuffie QTE, 2026-08-31). Kills the
# squash tween too: both write `scale`, and two writers on one property is
# the drift bug all over again.
static func pulse(node: Node, peak: float = 1.18, times: int = 3, half: float = 0.18) -> void:
	if node == null or not node.is_inside_tree():
		return
	var base: Variant
	if node.has_meta("juice_rest_scale"):
		base = node.get_meta("juice_rest_scale")
	else:
		base = node.get("scale")
		if base == null:
			return   # scale-less node: nothing to pulse
		node.set_meta("juice_rest_scale", base)
	for meta_key: StringName in [&"juice_pulse_tw", &"juice_squash_tw"]:
		if node.has_meta(meta_key):
			var old: Tween = node.get_meta(meta_key)
			if old != null and old.is_valid():
				old.kill()
	var tw: Tween = node.create_tween().set_loops(times)
	node.set_meta("juice_pulse_tw", tw)
	tw.tween_property(node, "scale", base * peak, half).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(node, "scale", base, half).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

# Pickup payoff: a quick pride pop, then shrink out and free. The touched
# thing acknowledges the touch instead of teleporting out of existence
# (DL-MOT-04). Canvas-agnostic like pulse, and for the same two reasons.
# The caller must already have removed the node from every logic list —
# after this call it is display-only and cannot be collected twice; state,
# HUD, and save writes stay exactly where they were.
static func vanish(node: Node, dur: float = 0.22) -> void:
	if node == null:
		return
	if not node.is_inside_tree():
		node.queue_free()   # never strand an off-tree node on the guard path
		return
	for meta_key: StringName in [&"juice_pulse_tw", &"juice_squash_tw"]:
		if node.has_meta(meta_key):
			var old: Tween = node.get_meta(meta_key)
			if old != null and old.is_valid():
				old.kill()
	var base: Variant = node.get_meta("juice_rest_scale") if node.has_meta("juice_rest_scale") else node.get("scale")
	if base == null:
		node.queue_free()   # scale-less node: skip the flourish, never leak
		return
	var tw: Tween = node.create_tween()
	tw.tween_property(node, "scale", base * 1.22, dur * 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(node, "scale", base * 0.04, dur * 0.65).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_callback(node.queue_free)
