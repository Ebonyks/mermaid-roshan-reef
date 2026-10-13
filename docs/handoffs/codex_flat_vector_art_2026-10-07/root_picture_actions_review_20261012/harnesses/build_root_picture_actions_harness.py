from pathlib import Path

b = Path(__file__).resolve().parent
s = (b / 'root_capture_picture_context_guarded_20261012.gd').read_text(encoding='utf-8')
s = s.replace('func _capture(id: String, input_info: Dictionary = {}) -> void:', 'func _capture(id: String, input_info: Dictionary = {}, own_medal_expected: bool = false) -> void:')
s = s.replace('or bool(presentation["medal_present"]) or float', 'or (bool(presentation["medal_present"]) and not own_medal_expected) or float')
s = s.replace('"kind": m.mg_kind, "stage":', '"own_medal_expected": own_medal_expected, "phase": String(m.mg.get("phase","")), "balls": int(m.mg.get("balls",0)), "face": int(m.mg.get("face",0)), "bites": int(m.mg.get("bites",0)), "bounces": int(m.mg.get("bounces",0)), "placed": int(m.mg.get("placed",0)), "kind": m.mg_kind, "stage":')
s = s.replace('for kind: String in ["garden", "snowman", "trampoline", "xmas"]:', 'for kind: String in ["snowman", "trampoline", "xmas"]:')
s = s.replace('\t\tm._mg2d_close()\n\t\tm.set_process(false)', '\t\tawait _actions(kind)\n\t\tm._mg2d_close()\n\t\tm.set_process(false)')
s = s.replace('ready stills only, no natural castle route, action/save/motion/device/child/owner acceptance.', 'bounded actual raw-input actions plus sampled states; no natural castle route, save/resume, complete motion, device/child/owner acceptance.')
s += '''

func _raw_button(at: Vector2, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = at
	event.global_position = at
	Input.parse_input_event(event)
	Input.flush_buffered_events()
	await process_frame

func _raw_tap(control: Control) -> Dictionary:
	var at := control.get_global_rect().get_center()
	await _raw_button(at, true)
	await _raw_button(at, false)
	return {"method": "Input.parse_input_event raw mouse press/release", "position": str(at), "target_rect": str(control.get_global_rect())}

func _raw_motion(at: Vector2, relative: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = at
	event.global_position = at
	event.relative = relative
	event.button_mask = MOUSE_BUTTON_MASK_LEFT
	Input.parse_input_event(event)
	Input.flush_buffered_events()
	await process_frame

func _actions(kind: String) -> void:
	match kind:
		"snowman":
			await _snow_actions()
		"trampoline":
			for i: int in range(3):
				var target := m.mg.get("trampoline_target") as Control
				var input_info := await _raw_tap(target)
				if int(m.mg.get("bounces",0)) != i + 1:
					errors.append("trampoline raw tap did not progress")
					return
				await create_timer(0.23).timeout
				await _capture("trampoline_bounce%d_apex" % (i+1), input_info)
				await create_timer(0.36).timeout
				await _capture("trampoline_bounce%d_settle" % (i+1), input_info, i == 2)
		"slide":
			var target := m.mg.get("slide_target") as Control
			var input_info := await _raw_tap(target)
			if String(m.mg.get("phase","")) != "ride":
				errors.append("slide raw tap did not start ride")
				return
			await _capture("slide_ride_entry", input_info)
			await create_timer(1.35).timeout
			await _capture("slide_ride_midpoint", input_info)
			await create_timer(1.78).timeout
			await _capture("slide_ride_payoff", input_info, true)
		"xmas":
			var buttons: Array = m.mg.get("btns",[])
			for i: int in range(5):
				var button := buttons[i] as Button
				var input_info := await _raw_tap(button)
				if int(m.mg.get("placed",0)) != i + 1:
					errors.append("xmas raw tap did not place ornament")
					return
				await _capture("xmas_ornament%d_placed" % (i+1), input_info)
			var flower := m.mg.get("flowerbtn") as Button
			if flower.disabled:
				errors.append("xmas flower did not unlock")
				return
			var input_info := await _raw_tap(flower)
			if not bool(m.mg.get("won",false)):
				errors.append("xmas flower tap did not complete")
			await _capture("xmas_flower_payoff", input_info, true)

func _snow_actions() -> void:
	for index: int in range(3):
		var center := m.mg2d_stage.get_global_transform_with_canvas() * m.SNOW_ROLL_C
		var previous := center + Vector2(150,0)
		await _raw_button(previous,true)
		if not Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
			errors.append("snow raw mouse button did not enter polled state")
			await _raw_button(previous,false)
			return
		var steps := 0
		while int(m.mg.get("balls",0)) == index and steps < 220:
			steps += 1
			var angle := float(steps) * TAU / 48.0
			var at := center + Vector2(cos(angle),sin(angle)) * 150.0
			await _raw_motion(at,at-previous)
			previous = at
			if steps == 48:
				await _capture("snow_ball%d_growing" % (index+1), {"method":"raw mouse circle gesture", "steps":steps, "angle_step":TAU/48.0, "observed_rot_acc":float(m.mg.get("rot_acc",0.0))})
		await _raw_button(previous,false)
		if int(m.mg.get("balls",0)) != index + 1:
			errors.append("snow raw circle did not finish ball%d" % (index+1))
			return
		await create_timer(0.6).timeout
		await _capture("snow_ball%d_stacked" % (index+1), {"method":"raw mouse circle gesture", "steps":steps})
	if String(m.mg.get("phase","")) != "face":
		errors.append("snow face phase absent")
		return
	var buttons: Array = m.mg.get("btns",[])
	for index: int in range(3):
		var button := buttons[index] as Button
		var input_info := await _raw_tap(button)
		if int(m.mg.get("face",0)) != index + 1:
			errors.append("snow face raw tap did not progress")
			return
		await _capture("snow_face%d_placed" % (index+1), input_info)
	# Deliberately stop at chase entry. A still does not establish the full chase,
	# eaten-body/contact/carrot finish, assistance or save/exit lifecycle.
	await _capture("snow_chase_entry", {"method":"production transition after three actual face taps", "chase_followthrough":"not exercised"})
'''
(b / 'root_capture_picture_actions_20261012.gd').write_text(s, encoding='utf-8', newline='\n')
print('Created separate action harness; original guarded-ready harness preserved.')
