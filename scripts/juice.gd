class_name Juice
extends RefCounted
# The impact primitives combat feel is built from (combat wing 2026-08):
# squash, flash, camera micro-shake, haptics. All cosmetic — game logic may
# never gate on these. Allocation-light: transient tweens on existing nodes,
# no new nodes at hit time, nothing measurable on the M11. Hitstop is data
# (enemy["hitstop"], owned by HitEngine, honored by each encounter's tick) —
# never Engine.time_scale, which belongs to the probes.

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
	var base: Vector3 = target.scale
	var mult: float = 1.3 if big else 1.18
	var tw: Tween = target.create_tween()
	tw.tween_property(target, "scale", Vector3(base.x * mult, base.y * (2.0 - mult), base.z * mult), 0.08).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(target, "scale", base, 0.18).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)

# White blink for sprite-card targets (castle bunny cards, cutout enemies).
# Mesh enemies are skipped on purpose: their materials are shared cache
# entries, so tinting one would flash every enemy wearing it — meshes get
# squash + sparkle instead.
static func flash(node: Node3D) -> void:
	var sprite: Sprite3D = node as Sprite3D
	if sprite == null:
		for child in node.get_children():
			if child is Sprite3D:
				sprite = child as Sprite3D
				break
	if sprite == null or not sprite.is_inside_tree():
		return
	var base: Color = sprite.modulate
	var tw: Tween = sprite.create_tween()
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
