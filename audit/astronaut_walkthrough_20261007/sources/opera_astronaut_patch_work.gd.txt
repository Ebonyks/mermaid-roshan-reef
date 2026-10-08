extends "res://scripts/opera_astronaut_pipe_work.gd"
## Intact wrench work for one genuinely requested leak; world owns repair.


func _init(owner: OperaCareerWorld2D) -> void:
	super(owner)


func _target_viewport() -> Vector2:
	return world.surface.get_global_transform_with_canvas() \
		* world.surface._target_anchor_point(cell)


func _live() -> bool:
	return is_instance_valid(world) and is_instance_valid(world.surface) \
		and is_instance_valid(world.player_actor) and world.active and world.task_open \
		and world.phase_index == phase_index and phase_index >= 0 \
		and phase_index < world.phases.size() \
		and String((world.phases[phase_index] as Dictionary).get("mode", "")) == "tap" \
		and not (world.surface as OperaAstronautSurface).input_suspended() \
		and (world.surface as OperaAstronautSurface).patch_generation == request_id


func _abort() -> void:
	if is_instance_valid(world) and is_instance_valid(world.surface):
		var surface := world.surface as OperaAstronautSurface
		if surface.patch_generation == request_id:
			surface.cancel_input()
	cancel()


func contact_eligible(next_id: int, next_phase: int, next_cell: int) -> bool:
	return super.contact_eligible(next_id, next_phase, next_cell) \
		and world.player_actor.flip_h == work_flip


func tick(delta: float) -> void:
	if not is_instance_valid(world) or not is_instance_valid(world.surface):
		cancel(false)
		return
	var surface := world.surface as OperaAstronautSurface
	if not busy():
		if world.active and world.task_open and not world.phase_advance_pending \
				and surface.mode == "tap" and not surface.input_suspended() \
				and not surface.patch_targets.is_empty():
			super.request(surface.patch_generation, surface.patch_targets[0])
		return
	if not _live():
		_abort()
		return
	if state not in ["release", "return"] and (surface.patch_targets.is_empty() \
			or surface.patch_targets[0] != cell):
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
				_pose("contact_a", 0)
		"contact_a":
			if state_t >= 0.16:
				_pose("contact_b", 1)
		"contact_b":
			if state_t >= 0.18:
				var jaw := actor.get_global_transform_with_canvas() * _jaw_local(JAW_B)
				var target := _target_viewport()
				var atlas := actor.texture as AtlasTexture
				if not world._commit_astronaut_patch_work(request_id, phase_index, cell):
					_abort()
					return
				last_contact = {"generation": request_id, "phase_index": phase_index,
					"target_index": cell, "jaw": jaw, "target": target,
					"distance": jaw.distance_to(target), "scale": actor.scale,
					"atlas_region": atlas.region, "time_msec": Time.get_ticks_msec()}
				_pose("release", 2)
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
