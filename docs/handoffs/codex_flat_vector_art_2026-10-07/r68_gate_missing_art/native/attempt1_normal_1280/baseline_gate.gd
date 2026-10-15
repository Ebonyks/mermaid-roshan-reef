extends "res://scripts/arena/sky_lagoon_promenade.gd"
## R67 nonproduction source-reuse candidate. All other targets use exact source.
const PAINTED_CUE: String = "res://assets/opera/worlds/props/fx_stolen_sparkle.png"
const CUE_MASTER_HEIGHT: float = 196.0

func _init(main: ReefMain) -> void:
	super(main)

func _register_target(id: String, node: Node2D, kind: String, payload: String,
		radius_px: float, highlight_scale: float, highlight_path: String = "",
		highlight_height: float = 0.0) -> void:
	if id != "castle_gate":
		super(id, node, kind, payload, radius_px, highlight_scale, highlight_path, highlight_height)
		return
	# Retire the white-mask constructor for this role. No flat fallback.
	var texture: Texture2D = _gate_cue_texture()
	if texture == null:
		push_error("R67 painted gate cue missing; no flat fallback permitted")
		return
	var affordance_kind: String = Affordance.PLOT
	var glow := Sprite2D.new()
	glow.name = "SkyLagoonFocus_%s" % id
	glow.texture = texture
	glow.scale = Vector2.ONE * (CUE_MASTER_HEIGHT / float(texture.get_height()))
	glow.position = node.position
	var idle_tint: Color = Affordance.color(affordance_kind, false)
	idle_tint.r = 1.0
	idle_tint.g = 1.0
	idle_tint.b = 1.0
	# A complete duplicate object is never the affordance. Idle animation targets
	# use a nearly invisible shimmer; selection raises the same pixels briefly.
	idle_tint.a = minf(idle_tint.a,
		0.055 if kind == "playground" else 0.10)
	glow.modulate = idle_tint
	glow.visible = true
	glow.z_index = node.z_index + 4
	glow.set_meta("canvas_layer_role", "interaction_affordance")
	glow.set_meta("interaction_id", id)
	glow.set_meta("affordance_base_scale", glow.scale)
	(m.g.get("lagoon_interactive_layer") as Node2D).add_child(glow)
	node.set_meta("interaction_id", id)
	node.set_meta("touch_footprint_px", radius_px * 2.0)
	node.set_meta("canvas_layer_role", "interactive")
	var targets: Array = m.g.get("lagoon_promenade_targets", []) as Array
	targets.append({
		"id": id, "node": node, "kind": kind, "payload": payload,
		"radius_px": radius_px, "affordance_kind": affordance_kind,
		"highlight": glow, "highlight_scale": highlight_scale,
	})
	m.g["lagoon_promenade_targets"] = targets


func _tick_target_affordances(focus_id: String, focus_t: float) -> void:
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		var glow: Sprite2D = target.get("highlight") as Sprite2D
		if glow == null or not is_instance_valid(glow):
			continue
		var selected: bool = String(target.get("id", "")) == focus_id
		glow.visible = true
		var kind: String = String(target.get("affordance_kind", Affordance.INTERACTION))
		var wave: float = sin(focus_t * Affordance.pulse_speed(kind, selected))
		var tint: Color = Affordance.color(kind, selected)
		if selected:
			tint.a = lerpf(0.82, 1.0, wave * 0.5 + 0.5)
		else:
			# Day One's castle gate is the route anchor. It must remain a readable
			# idle cue after focus is cleared; the generic promenade cap would make
			# the only safe destination effectively disappear.
			if m.day_one_is_active() and String(target.get("id", "")) == "castle_gate":
				tint.a = maxf(tint.a, 0.45)
			else:
				tint.a = minf(tint.a, 0.055)
		if str(target.get("id", "")) == "castle_gate":
			# Preserve source alpha/pulse, retain authored gold/violet RGB.
			tint.r = 1.0
			tint.g = 1.0
			tint.b = 1.0
		glow.modulate = tint
		var pulse: float = 1.0 + wave * Affordance.pulse_amount(kind, selected)
		var base_scale: float = float(target.get("highlight_scale", 1.0))
		if String(glow.get_meta("focus_cue_role", "")) \
				== "procedural_ring_pointer":
			glow.scale = Vector2.ONE * base_scale * pulse
		elif String(target.get("id", "")) != "castle_gate":
			var node: Node2D = target.get("node") as Node2D
			if node is Sprite2D:
				glow.scale = (node as Sprite2D).scale * base_scale * pulse


func _gate_cue_texture() -> Texture2D:
	return null
