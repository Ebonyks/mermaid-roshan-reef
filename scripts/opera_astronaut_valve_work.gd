extends "res://scripts/opera_astronaut_pipe_work.gd"
## Reuse intact-figure approach/socket geometry; world owns valve awards.

var contact_age := 0.0
var applied_arc := 0.0


func _init(owner: OperaCareerWorld2D) -> void:
	super(owner)


func _target_viewport() -> Vector2:
	var surface := world.surface as OperaAstronautSurface
	return surface.get_global_transform_with_canvas() * surface._circle_pivot()


func _live() -> bool:
	return is_instance_valid(world) and is_instance_valid(world.surface) \
		and is_instance_valid(world.player_actor) and world.active and world.task_open \
		and world.phase_index == phase_index and phase_index >= 0 \
		and phase_index < world.phases.size() \
		and String((world.phases[phase_index] as Dictionary).get("mode", "")) == "circle" \
		and not (world.surface as OperaAstronautSurface).input_suspended() \
		and (world.surface as OperaAstronautSurface).valve_input_generation == request_id


func _abort() -> void:
	if is_instance_valid(world) and is_instance_valid(world.surface):
		var surface := world.surface as OperaAstronautSurface
		if surface.valve_input_generation == request_id:
			surface.cancel_input()
	cancel()


func contact_eligible(next_id: int, next_phase: int, _next_cell: int) -> bool:
	if state != "contact" or contact_age < 0.18 or not _live() \
			or next_id != request_id or next_phase != phase_index:
		return false
	var actor := world.player_actor
	var frame := world.player_animator.current_frame
	var atlas := actor.texture as AtlasTexture
	var point := JAW_A if frame == 0 else JAW_B
	var jaw := actor.get_global_transform_with_canvas() * _jaw_local(point)
	return frame in [0, 1] and world.player_animator.current_animation == "work" \
		and atlas != null and atlas.region == Rect2(frame * 256, 512, 256, 256) \
		and actor.scale.is_equal_approx(entry_scale) and actor.flip_h == work_flip \
		and jaw.distance_to(_target_viewport()) <= CONTACT_RADIUS


func tick(delta: float) -> void:
	if not is_instance_valid(world) or not is_instance_valid(world.surface):
		cancel(false)
		return
	var surface := world.surface as OperaAstronautSurface
	if not busy():
		if world.active and world.task_open and not world.phase_advance_pending \
				and surface.mode == "circle" and not surface.input_suspended():
			super.request(surface.valve_input_generation, -1)
			contact_age = 0.0
			applied_arc = 0.0
		return
	if not _live():
		_abort()
		return
	state_t += delta
	var actor := world.player_actor
	match state:
		"wait_reveal":
			if world.action_panel.scale.is_equal_approx(Vector2.ONE):
				if not _begin_approach():
					_abort()
			elif state_t > 0.50:
				_abort()
		"approach":
			var progress := clampf(state_t / travel_seconds, 0.0, 1.0)
			actor.position = travel_start.lerp(work_position, smoothstep(0.0, 1.0, progress))
			if progress >= 1.0:
				actor.flip_h = work_flip
				_pose("anticipation", 2)
		"anticipation":
			if state_t >= 0.12:
				_pose("contact", 0)
		"contact":
			contact_age += delta
			if world.phase_advance_pending:
				_pose("release", 2)
			elif not surface.valve_arcs.is_empty() and contact_age >= 0.18:
				if not contact_eligible(request_id, phase_index, -1):
					_abort()
					return
				var frame := world.player_animator.current_frame
				var point := JAW_A if frame == 0 else JAW_B
				var jaw := actor.get_global_transform_with_canvas() * _jaw_local(point)
				var target := _target_viewport()
				var arc := world._commit_astronaut_valve_motion(request_id, phase_index, delta * 4.0)
				if is_zero_approx(arc):
					_abort()
					return
				last_contact = {"generation": request_id, "phase_index": phase_index,
					"jaw": jaw, "target": target, "distance": jaw.distance_to(target),
					"scale": actor.scale, "frame": frame, "signed_radians": arc,
					"time_msec": Time.get_ticks_msec()}
				applied_arc += absf(arc)
				if not world.phase_advance_pending:
					world.player_animator.show_pose("work", int(floor(applied_arc / 0.35)) % 2)
		"release":
			if state_t >= 0.16:
				state = "return"
				state_t = 0.0
				travel_start = actor.position
				travel_seconds = clampf(travel_start.distance_to(entry_position) / 700.0, 0.18, 0.60)
				actor.flip_h = entry_position.x > travel_start.x
				world.player_animator.play("travel")
		"return":
			var progress := clampf(state_t / travel_seconds, 0.0, 1.0)
			actor.position = travel_start.lerp(entry_position, smoothstep(0.0, 1.0, progress))
			if progress >= 1.0:
				cancel()
