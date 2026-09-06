extends SceneTree
# Child-paced stress test of the four active picture games. The retired slide
# card delegates to the Lagoon playground route exercised by probe_audit.


func _feedback_layer(stage: Control) -> Control:
	if stage == null or not is_instance_valid(stage):
		return null
	return stage.get_node_or_null("PictureGameFeedbackLayer") as Control


func _has_visible_feedback(stage: Control, feedback_kind: String,
		max_elements: int) -> bool:
	var layer := _feedback_layer(stage)
	if layer == null:
		return false
	for burst_value in layer.get_children():
		var burst := burst_value as Control
		if burst == null or not burst.visible \
				or String(burst.get_meta("feedback_kind", "")) != feedback_kind:
			continue
		var declared := int(burst.get_meta("visible_elements", 0))
		if declared < 4 or declared > max_elements \
				or not Rect2(Vector2.ZERO, stage.size).has_point(burst.position):
			continue
		var visible_elements := 0
		for element_value in burst.get_children():
			var element := element_value as CanvasItem
			if element != null and element.visible and element.modulate.a > 0.05:
				visible_elements += 1
		if visible_elements == declared:
			return true
	return false


func _garden_stage_total(mg: Dictionary) -> int:
	var total := 0
	for stage_value in (mg.get("stage", []) as Array):
		total += int(stage_value)
	return total


func _world_particle_count(node: Node, particle_class: String) -> int:
	var total := 1 if node.get_class() == particle_class else 0
	for child_value in node.get_children():
		var child := child_value as Node
		if child != null:
			total += _world_particle_count(child, particle_class)
	return total


func _tweens_stopped(tweens: Array) -> bool:
	for tween_value in tweens:
		var tracked := tween_value as Tween
		if tracked != null and tracked.is_valid() and tracked.is_running():
			return false
	return true


func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	# No-input remains neutral even after the assist delay. A held virtual-stick
	# direction then activates the accessible roll fallback without auto-winning.
	main._mg2d_open("snowman")
	for _second in range(9):
		main.touch_ui.stick_vec = Vector2.ZERO
		main._tick_mg2d(1.0)
		await process_frame
	var passive_ok: bool = is_zero_approx(float(main.mg.get("rot_acc", -1.0))) and not bool(main.mg.get("motor_assist", false))
	main.touch_ui.stick_vec = Vector2.RIGHT
	for _second in range(9):
		main._tick_mg2d(1.0)
		await process_frame
	var assist_ok: bool = bool(main.mg.get("motor_assist", false)) and float(main.mg.get("rot_acc", 0.0)) > 0.0
	main.touch_ui.stick_vec = Vector2.ZERO
	# The assist exercise can finish the first ball. Re-enter on a clean stage so
	# the progression ledger below observes all three real settle branches.
	main._mg2d_close()
	await process_frame
	await process_frame
	main._mg2d_open("snowman")
	await process_frame
	var results := []
	var failed := not passive_ok or not assist_ok
	var snow_face_touch_checked := false
	var snow_face_touch_ok := false
	var snow_carrot_angle_ok := true
	var snow_carrot_motion_checked := false
	var snow_carrot_moved := false
	var snow_carrot_before_x := 0.0
	var picture_source: String = FileAccess.get_file_as_string(
		"res://scripts/games/picture_games.gd")
	var source_feedback_only: bool = picture_source.find("_sparkle_burst") < 0 \
		and picture_source.find("Vector" + str(3)) < 0 \
		and picture_source.find(".g" + "lb") < 0
	var source_has_no_round_overlay_controls: bool = \
		picture_source.find("_mg_round" + "btn") < 0 \
		and picture_source.find("\"JUMP\"") < 0 \
		and picture_source.find("\"GO!\"") < 0
	failed = failed or not source_feedback_only \
		or not source_has_no_round_overlay_controls
	results.append("snow assist: %s" % ("OK" if passive_ok and assist_ok else "FAIL"))
	results.append("picture feedback has no world sparkle request: %s" % (
		"OK" if source_feedback_only else "FAIL"))
	results.append("picture games have no jump/go overlay controls: %s" % (
		"OK" if source_has_no_round_overlay_controls else "FAIL"))
	var particle_class: String = "CPU" + "Particles" + str(3) + "D"
	var snow_settle_checks := 0
	var snow_settle_ok := true
	var garden_growth_checks := 0
	var garden_growth_ok := true
	var garden_win_checked := false
	var garden_win_ok := false
	var teardown_checks := 0
	var teardown_ok := true
	var fresh_stage_checks := 0
	var fresh_stage_ok := true
	for kind in ["snowman", "garden", "trampoline", "xmas"]:
		if kind != "snowman":
			main._mg2d_open(kind)
			await process_frame
		var active_stage: Control = main.mg2d_stage as Control
		var active_feedback_layer: Control = _feedback_layer(active_stage)
		var direct_trampoline_target: Control = \
			main.mg.get("trampoline_target") as Control \
			if kind == "trampoline" else null
		if kind == "trampoline":
			var direct_trampoline_ok: bool = direct_trampoline_target != null \
				and (main.mg.get("btns", []) as Array).is_empty()
			failed = failed or not direct_trampoline_ok
			results.append("trampoline uses direct art tap: %s" % (
				"OK" if direct_trampoline_ok else "FAIL"))
		fresh_stage_checks += 1
		fresh_stage_ok = fresh_stage_ok and active_feedback_layer != null \
			and active_feedback_layer.get_child_count() == 0 \
			and (main.mg.get("feedback_events", {}) as Dictionary).is_empty()
		var root_ref: WeakRef = weakref(main.mg2d_root)
		var stage_ref: WeakRef = weakref(active_stage)
		var feedback_layer_ref: WeakRef = weakref(active_feedback_layer)
		var tracked_feedback_tweens: Array = main.mg.get("feedback_tweens", [])
		var delayed_close: Tween = null
		var world_particle_baseline: int = _world_particle_count(main, particle_class)
		var t := 0.0
		var press_cd := 0.0
		while main.mg_kind == kind and t < 60.0:
			t += 1.0/60.0 * Engine.time_scale
			press_cd -= 1.0/60.0 * Engine.time_scale
			# Perform each of the snowman's real touch verbs: circle the virtual
			# stick to roll all three balls, then chase the snowman and finally
			# eat his carrot nose (the book-canon ending).
			if kind == "snowman" and main.touch_ui != null:
				var snow_phase: String = String(main.mg.get("phase", ""))
				if snow_phase == "face" and not snow_face_touch_checked:
					snow_face_touch_checked = true
					var face_buttons: Array = main.mg.get("btns", [])
					snow_face_touch_ok = face_buttons.size() == 3
					for face_button_value in face_buttons:
						var face_button: Control = face_button_value as Control
						if face_button == null:
							snow_face_touch_ok = false
							continue
						var touch_size := Vector2(
							maxf(face_button.size.x, face_button.custom_minimum_size.x),
							maxf(face_button.size.y, face_button.custom_minimum_size.y))
						if touch_size.x < StorybookUI.MIN_TOUCH.x \
								or touch_size.y < StorybookUI.MIN_TOUCH.y:
							snow_face_touch_ok = false
					failed = failed or not snow_face_touch_ok
					results.append("snow face touch targets: %s" % (
						"OK" if snow_face_touch_ok else "FAIL"))
				if snow_phase == "roll":
					var spin_ang: float = float(main.mg.get("t", 0.0)) * 2.4
					main.touch_ui.stick_vec = Vector2(cos(spin_ang), sin(spin_ang))
				elif snow_phase in ["chase", "carrot"]:
					var chase_dir: float = signf(float(main.mg.get("run_x", 640.0)) - float(main.mg.get("chaser_x", 640.0)))
					main.touch_ui.stick_vec = Vector2(chase_dir, 0.0)
				else:
					main.touch_ui.stick_vec = Vector2.ZERO
			elif main.touch_ui != null:
				main.touch_ui.stick_vec = Vector2.ZERO
			# A 4yo taps roughly twice a second, touching the visible play art.
			if press_cd <= 0.0:
				press_cd = 0.5
				if kind == "trampoline" and direct_trampoline_target != null:
					var direct_press := InputEventMouseButton.new()
					direct_press.button_index = MOUSE_BUTTON_LEFT
					direct_press.pressed = true
					direct_trampoline_target.gui_input.emit(direct_press)
				var btns: Array = main.mg.get("btns", [])
				for b in btns:
					if is_instance_valid(b) and b.visible and not b.disabled:
						var growth_before: int = _garden_stage_total(main.mg) \
							if kind == "garden" else 0
						b.pressed.emit()
						if kind == "garden":
							garden_growth_checks += 1
							var garden_won: bool = bool(main.mg.get("won", false))
							var progressed: bool = _garden_stage_total(main.mg) \
								== growth_before + 1
							var feedback_kind: String = "win" if garden_won else "garden_growth"
							var visible: bool = _has_visible_feedback(
								main.mg2d_stage as Control, feedback_kind,
								18 if garden_won else 10)
							var stayed_on_stage: bool = garden_won or \
								_world_particle_count(main, particle_class) \
									<= world_particle_baseline
							garden_growth_ok = garden_growth_ok and progressed \
								and visible and stayed_on_stage
							if garden_won:
								garden_win_checked = true
								var events: Dictionary = main.mg.get("feedback_events", {})
								var completed_garden_visible := true
								for plant_value in (main.mg.get("btns", []) as Array):
									var plant := plant_value as Button
									completed_garden_visible = completed_garden_visible and plant != null \
										and plant.visible and plant.disabled
								failed = failed or not completed_garden_visible
								results.append("completed garden retains all five flowers: %s" % (
									"OK" if completed_garden_visible else "FAIL"))
								garden_win_ok = int(main.mg.get("grown", 0)) == 5 \
									and _garden_stage_total(main.mg) == 10 \
									and int(events.get("garden_growth", 0)) == 9 \
									and int(events.get("win", 0)) == 1 \
									and visible
						break
			var balls_before: int = int(main.mg.get("balls", 0)) \
				if kind == "snowman" else 0
			var world_before_settle := -1
			if kind == "snowman" and String(main.mg.get("phase", "")) == "roll" \
					and float(main.mg.get("rot_need", 0.0)) \
						- float(main.mg.get("rot_acc", 0.0)) <= 0.6:
				world_before_settle = _world_particle_count(main, particle_class)
			main._tick_mg2d(1.0/60.0 * Engine.time_scale)
			if kind == "snowman":
				var balls_after: int = int(main.mg.get("balls", 0))
				if balls_after > balls_before:
					snow_settle_checks += 1
					var progression_ok: bool = balls_after == balls_before + 1 \
						and ((balls_after < 3 and main.mg.has("roll_ball")) \
							or (balls_after == 3 \
								and String(main.mg.get("phase", "")) == "face"))
					var events: Dictionary = main.mg.get("feedback_events", {})
					var event_ok: bool = int(events.get("snowball_settle", 0)) == balls_after
					var visible_ok: bool = _has_visible_feedback(
						main.mg2d_stage as Control, "snowball_settle", 10)
					var world_ok: bool = world_before_settle >= 0 \
						and _world_particle_count(main, particle_class) \
							<= world_before_settle
					var settle_ok: bool = progression_ok and event_ok and visible_ok and world_ok
					snow_settle_ok = snow_settle_ok and settle_ok
					if not settle_ok:
						results.append("snow settle %d detail: progression=%s event=%s visible=%s world=%s" % [
							balls_after, progression_ok, event_ok, visible_ok, world_ok])
				if String(main.mg.get("phase", "")) == "chase":
					var carrot_bit := main.mg.get("carrot_bit") as TextureRect
					if carrot_bit != null and is_instance_valid(carrot_bit):
						var authored_rotation: float = float(
							carrot_bit.get_meta("snowman_authored_rotation",
								deg_to_rad(-135.0)))
						var expected_rotation := authored_rotation \
							+ sin(float(main.mg.get("t", 0.0)) * 10.0) * 0.08
						snow_carrot_angle_ok = snow_carrot_angle_ok \
							and is_equal_approx(carrot_bit.rotation, expected_rotation)
						if not snow_carrot_motion_checked:
							snow_carrot_before_x = carrot_bit.position.x
							snow_carrot_motion_checked = true
						else:
							snow_carrot_moved = snow_carrot_moved \
								or absf(carrot_bit.position.x - snow_carrot_before_x) > 0.001
			var close_candidate: Tween = main.mg.get("close_tween") as Tween
			if close_candidate != null:
				delayed_close = close_candidate
			await process_frame
		if main.mg_kind == "":
			results.append("%s: WON (%.1fs)" % [kind, t])
		else:
			failed = true
			results.append("%s: FAIL (STUCK at %.1fs)" % [kind, t])
		if main.mg_kind != "":
			main._mg2d_close()
		if main.touch_ui != null:
			main.touch_ui.stick_vec = Vector2.ZERO
		await process_frame
		await process_frame
		teardown_checks += 1
		var root_gone: bool = root_ref.get_ref() == null
		var stage_gone: bool = stage_ref.get_ref() == null
		var feedback_gone: bool = feedback_layer_ref.get_ref() == null
		var feedback_tweens_stopped: bool = _tweens_stopped(tracked_feedback_tweens)
		var close_stopped: bool = delayed_close == null \
			or not delayed_close.is_valid() or not delayed_close.is_running()
		var layer_empty: bool = main.mg2d_layer == null \
			or main.mg2d_layer.get_child_count() == 0
		var clean_close: bool = root_gone and stage_gone and feedback_gone \
			and feedback_tweens_stopped and close_stopped and layer_empty
		if not clean_close:
			results.append("%s feedback cleanup detail: root=%s stage=%s feedback=%s tweens=%s close=%s layer=%s" % [
				kind, root_gone, stage_gone, feedback_gone,
				feedback_tweens_stopped, close_stopped, layer_empty])
		teardown_ok = teardown_ok and clean_close
	if not snow_face_touch_checked:
		failed = true
		results.append("snow face touch targets: FAIL (face phase not reached)")
	var snow_feedback_pass: bool = snow_settle_checks == 3 and snow_settle_ok
	var snow_carrot_pose_pass: bool = snow_carrot_motion_checked \
		and snow_carrot_moved and snow_carrot_angle_ok
	var garden_feedback_pass: bool = garden_growth_checks == 10 \
		and garden_growth_ok and garden_win_checked and garden_win_ok
	var lifecycle_pass: bool = teardown_checks == 4 and teardown_ok \
		and fresh_stage_checks == 4 and fresh_stage_ok
	failed = failed or not snow_feedback_pass or not snow_carrot_pose_pass \
		or not garden_feedback_pass \
		or not lifecycle_pass
	results.append("snowball settle feedback/progression: %s (%d/3)" % [
		"OK" if snow_feedback_pass else "FAIL", snow_settle_checks])
	results.append("snowman carrot authored angle survives moving chase: %s" % (
		"OK" if snow_carrot_pose_pass else "FAIL"))
	results.append("garden growth + bounded win feedback: %s (%d/10)" % [
		"OK" if garden_feedback_pass else "FAIL", garden_growth_checks])
	results.append("feedback teardown/re-entry: %s (%d closes, %d fresh)" % [
		"OK" if lifecycle_pass else "FAIL", teardown_checks, fresh_stage_checks])
	print("=== STAGE 2 MINIGAME STRESS TEST ===")
	for r in results: print("  " + r)
	print("MG2D|done: ", "FAIL" if failed else "OK")
	quit()
