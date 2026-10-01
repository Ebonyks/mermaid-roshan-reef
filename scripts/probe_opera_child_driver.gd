extends RefCounted
## Diagnostic child input. Reads visible control geometry and sends one finger;
## never grants progress, edits scores, completes a phase or bypasses a station.

const Ballet := preload("res://scripts/opera_ballet_surface.gd")
const GeologySurface := preload("res://scripts/opera_geology_surface.gd")
const Teacher := preload("res://scripts/opera_teacher_surface.gd")
var last_phase := -1
var action_t := 0.0
var age := 0.0
var angle := 0.0
var paint_row := 0


static func touch(surface: Control, at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = at
	event.pressed = pressed
	surface._gui_input(event)


static func drag(surface: Control, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = at
	surface._gui_input(event)


static func tap(surface: Control, at: Vector2) -> void:
	touch(surface, at, true)
	touch(surface, at, false)


static func stroke(surface: Control, start: Vector2, finish: Vector2) -> void:
	touch(surface, start, true)
	drag(surface, finish)
	touch(surface, finish, false)


func step(world: OperaCareerWorld2D, delta: float, interval := 1.2) -> void:
	if not world.active or world.phase_advance_pending or world.phase_index >= world.phases.size():
		return
	if last_phase != world.phase_index:
		last_phase = world.phase_index
		action_t = 0.0
		age = 0.0
		angle = 0.0
		paint_row = 0
	if not world.task_open:
		if not world.wander_walking and not world.hotspot_opening and world.armed_station >= 0:
			world._on_hotspot_pressed(world.armed_station)
		return
	if world.contest != null and not world.contest.accepting_input() and world._contest_phase():
		return
	var surface: OperaGestureSurface = world.surface
	var mode := surface.mode
	age += delta
	action_t -= delta
	var act_now := action_t <= 0.0
	if act_now:
		action_t = interval
	if mode == "lens":
		var clue := world._next_unfound_lens_clue()
		if clue >= 0:
			world._move_lens_to(world.lens_pos.move_toward(world.lens_clues[clue], 500.0 * delta), true)
		return
	if surface is OperaRacerSurface and mode == "kart_race":
		var racer := surface as OperaRacerSurface
		var center := OperaRacerSurface.STEERING_RECT.get_center()
		if not racer.held:
			touch(surface, center, true)
		var sway := 22.0 if floori(age / 0.2) % 2 == 0 else -22.0
		drag(surface, center + Vector2(sway, 0.0))
		return
	if surface is OperaBoxingSurface:
		var boxer := surface as OperaBoxingSurface
		var hand := boxer.round_index() % 2
		if mode == "boxing_imp":
			if boxer.touch_owner_snapshot().is_empty():
				touch(surface, boxer.glove_rest(hand), true)
			drag(surface, boxer.guard_target_position(hand) if not boxer.imp_is_open() else boxer.active_target_position())
			if boxer.imp_is_open():
				touch(surface, boxer.active_target_position(), false)
		elif mode == "boxing_guard":
			if boxer.touch_owner_snapshot().is_empty():
				touch(surface, boxer.glove_rest(hand), true)
			drag(surface, boxer.guard_target_position(hand))
		elif act_now:
			var target := boxer.guide_target_position(hand) if mode == "boxing_guide" else boxer.active_target_position()
			stroke(surface, boxer.glove_rest(hand), target)
		return
	if world.nursery_catch != null and mode == "catch":
		var baby_x := world.nursery_catch.lowest_baby_x()
		world.nursery_catch.steer_to(baby_x if baby_x >= 0.0 else 0.5)
		world.nursery_catch._process(delta)
		return
	if surface.get_script() == GeologySurface:
		if act_now:
			_drive_geology_surface(surface)
		return
	if surface.get_script() == Teacher:
		if not act_now:
			return
		var teacher: Variant = surface
		if teacher.lesson_kind() == "add" and not teacher.joined:
			tap(surface, Teacher.JOIN_CENTER)
			return
		for counter in range(teacher.counted.size()):
			if not teacher.counted[counter]:
				tap(surface, teacher.counter_position(counter))
				return
		tap(surface, teacher.choice_rect(teacher.answer_index()).get_center())
		return
	match mode:
		"tap":
			if act_now:
				var next := surface._target_next_unplaced() if surface._uses_anchored_targets() else -1
				tap(surface, surface._target_anchor_point(next) if next >= 0 else surface.size * Vector2(0.42, 0.56))
		"choice":
			if act_now and surface.shuffle_t <= 0.0:
				tap(surface, surface.size * Vector2((float(surface.target_choice) + 0.5) / float(surface.choice_count), 0.5))
		"echo":
			if act_now and surface.echo_listening:
				var verse: Array = [0, 2] if surface.contest_easy_round else OperaGestureSurface.ECHO_VERSES[clampi(surface.echo_verse, 0, OperaGestureSurface.ECHO_VERSES.size() - 1)]
				tap(surface, surface._echo_star_center(int(verse[surface.echo_input_i])))
		"swipe":
			if surface._is_nursery_bedtime_context():
				if act_now:
					var index := surface._nursery_bedtime_next_blanket()
					if index >= 0:
						var start := surface._nursery_bedtime_grab_point(index)
						stroke(surface, start, start + Vector2.DOWN * surface._nursery_bedtime_required_travel())
			elif surface._uses_long_push_context():
				if not surface.long_push_engaged:
					touch(surface, surface._long_push_position(surface.long_push_journey), true)
				drag(surface, surface.pointer_pos + Vector2.RIGHT * 360.0 * delta)
			elif surface._uses_authored_trace_context():
				if not surface.trace_engaged:
					touch(surface, surface._trace_demo_point(surface.trace_journey), true)
				var distance := surface._trace_demo_point(0.0).distance_to(surface._trace_demo_point(1.0))
				var advance := 360.0 * delta / maxf(100.0, distance)
				drag(surface, surface._trace_demo_point(minf(1.0, surface.trace_journey + advance)))
			elif act_now:
				surface.demo_t = 0.0
				var start: Vector2 = surface._demo_finger_pose()["at"]
				surface.demo_t = 1.1
				stroke(surface, start, surface._demo_finger_pose()["at"])
		"ballet_twirl":
			var ballet := surface as OperaBalletSurface
			if ballet.demo_active:
				return
			if not ballet.held:
				touch(surface, ballet.twirl_handle_position(), true)
				angle = (ballet.twirl_handle_position() - ballet.twirl_center()).angle()
			angle += 5.0 * delta
			drag(surface, ballet.twirl_center() + Vector2.from_angle(angle) * ballet.twirl_radius())
		"ballet_pose":
			var ballet := surface as OperaBalletSurface
			if act_now and not ballet.demo_active:
				var index := ballet.pose_option_frames().find(ballet.pose_target_frame())
				tap(surface, ballet.pose_option_rects()[index].get_center())
		"ballet_ribbon":
			var ballet := surface as OperaBalletSurface
			if not ballet.demo_active:
				if not ballet.held:
					touch(surface, ballet.ribbon_point(ballet.ribbon_progress), true)
				drag(surface, ballet.ribbon_point(minf(1.0, ballet.ribbon_progress + delta * 0.30)))
		"hold":
			if not surface.held:
				surface.demo_t = 1.1
				touch(surface, surface._demo_finger_pose()["at"], true)
			drag(surface, surface.pointer_pos)
		"circle":
			var center := surface._circle_pivot()
			var radius := minf(surface.size.x, surface.size.y) * 0.25
			if not surface.held:
				touch(surface, center + Vector2(radius, 0), true)
			angle += 5.0 * delta
			drag(surface, center + Vector2.from_angle(angle) * radius)
		"paint_reveal":
			if act_now:
				var canvas := surface._paint_canvas_rect()
				var y := canvas.position.y + canvas.size.y * (float(paint_row % OperaGestureSurface.PAINT_GRID_ROWS) + 0.5) / float(OperaGestureSurface.PAINT_GRID_ROWS)
				stroke(surface, Vector2(canvas.position.x + 2.0, y), Vector2(canvas.end.x - 2.0, y))
				paint_row += 1
		"farm_lob":
			if act_now and not surface.farm_flying and surface.farm_pause <= 0.0:
				stroke(surface, surface._farm_anchor_point(), surface._farm_demo_pull_point())
		"garden_plant":
			if act_now:
				stroke(surface, surface._garden_seed_home(), surface._garden_hole_point(surface.garden_planted))
		"xray_scan":
			if act_now:
				for index in range(surface.xray_found.size()):
					if not surface.xray_found[index]:
						stroke(surface, surface._xray_home_point(), surface._xray_target_center(index))
						break
		"clue_board":
			if act_now:
				stroke(surface, surface._clue_home_point(), surface._clue_target_rect(surface.clue_index).get_center())
		"candy_sort":
			if act_now:
				stroke(surface, surface.candy_position, surface._candy_bin_rect(surface.candy_type).get_center())
		"pipe":
			if act_now and surface.pipe_pause <= 0.0:
				var routes := [ [["H", 5], ["H", 6]],
					[["SE", 0], ["H", 1], ["SW", 2], ["NE", 6]],
					[["NW", 5], ["SE", 1], ["H", 2], ["NW", 3]] ]
				for pair: Array in routes[clampi(surface.pipe_round, 0, 2)]:
					var cell := int(pair[1])
					if String(surface.pipe_grid[cell]) == String(pair[0]):
						continue
					var slot: int = surface.pipe_tray.find(String(pair[0]))
					if slot >= 0:
						stroke(surface, surface._pipe_tray_rect(slot).get_center(), surface._pipe_cell_rect(cell).get_center())
					break
		"oven":
			if act_now and surface.oven_t >= 0.50:
				tap(surface, surface.size * Vector2(0.42, 0.73))
		"magic_cabinet":
			if act_now:
				var start := surface._cabinet_handle_rect().get_center()
				stroke(surface, start, start + Vector2.DOWN * (surface._cabinet_required_travel() + 2.0))
		"crown_chest":
			if act_now:
				tap(surface, surface._crown_handle_rect().get_center())
		"pourt":
			if not surface.held:
				touch(surface, surface._pour_pitcher_hit_rect().get_center(), true)
			drag(surface, surface.pointer_pos + Vector2(0.0, -10.0))
		_:
			if act_now:
				surface.demo_t = 0.0
				var start: Vector2 = surface._demo_finger_pose()["at"]
				surface.demo_t = 1.1
				stroke(surface, start, surface._demo_finger_pose()["at"])


func _geology_touch(surface: Variant, finger: int, pressed: bool,
		position: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.position = position
	event.pressed = pressed
	surface._gui_input(event)


func _geology_drag(surface: Variant, finger: int,
		position: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = position
	surface._gui_input(event)


func _drive_geology_surface(surface: Variant) -> void:
	match surface.mode:
		"geology_river":
			_geology_touch(surface, 0, true, surface.river_path_point(0))
			for path_index in range(1, GeologySurface.RIVER_PATH.size()):
				_geology_drag(surface, 0, surface.river_path_point(path_index))
			_geology_touch(surface, 0, false,
				surface.river_path_point(GeologySurface.RIVER_PATH.size() - 1))
		"geology_fossil":
			var cell_size := Vector2(
				GeologySurface.FOSSIL_RECT.size.x / GeologySurface.FOSSIL_GRID_COLS,
				GeologySurface.FOSSIL_RECT.size.y / GeologySurface.FOSSIL_GRID_ROWS)
			var first := GeologySurface.FOSSIL_RECT.position + cell_size * 0.5
			_geology_touch(surface, 0, true, first)
			for row in range(GeologySurface.FOSSIL_GRID_ROWS):
				var column := GeologySurface.FOSSIL_GRID_COLS - 1 if row % 2 == 0 else 0
				var at := GeologySurface.FOSSIL_RECT.position \
					+ (Vector2(column, row) + Vector2(0.5, 0.5)) * cell_size
				_geology_drag(surface, 0, at)
			_geology_touch(surface, 0, false, surface.pointer_pos)
			for piece in range(3):
				_geology_touch(surface, 0, true, surface.fossil_piece_home(piece))
				_geology_drag(surface, 0, surface.fossil_piece_target(piece))
				_geology_touch(surface, 0, false, surface.fossil_piece_target(piece))
		"geology_pan":
			var center := GeologySurface.PAN_RECT.get_center()
			_geology_touch(surface, 0, true, center)
			for swing in range(GeologySurface.PAN_REQUIRED_REVERSALS + 1):
				var direction := 1.0 if swing % 2 == 0 else -1.0
				_geology_drag(surface, 0, center + Vector2(direction * 150.0, 0.0))
			_geology_touch(surface, 0, false, surface.pointer_pos)
		"geology_geode":
			for seam in range(GeologySurface.GEODE_SEAM_SPOTS.size()):
				var seam_at: Vector2 = surface.geode_seam_spot(seam)
				_geology_touch(surface, 0, true, seam_at)
				_geology_touch(surface, 0, false, seam_at)
			var half: Vector2 = surface.geode_half_center()
			_geology_touch(surface, 0, true, half)
			_geology_drag(surface, 0,
				half + Vector2(GeologySurface.GEODE_PULL_DISTANCE + 16.0, 0.0))
			_geology_touch(surface, 0, false, surface.pointer_pos)
