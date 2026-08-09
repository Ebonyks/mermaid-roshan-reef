extends SceneTree
## Focused contract for the shared Opera gesture surface: the wordless hand
## follows the real control geometry, and a stationary tap cannot impersonate
## a hold, swipe, or circle. This probe deliberately owns no career state.

var checks := 0
var failed := 0
var events: Array[Dictionary] = []


func _ck(name: String, ok: bool) -> void:
	checks += 1
	if not ok:
		failed += 1
		print("GESTURE_QUALITY|FAIL|%s" % name)


func _record_gesture(kind: String, amount: float, quality: float) -> void:
	events.append({"kind": kind, "amount": amount, "quality": quality})


func _paid(kind: String) -> bool:
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind and float(event.get("amount", 0.0)) > 0.0:
			return true
	return false


func _paid_count(kind: String) -> int:
	var count := 0
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind and float(event.get("amount", 0.0)) > 0.0:
			count += 1
	return count


func _pose_at(surface: OperaGestureSurface, time: float) -> Dictionary:
	surface.demo_t = time
	return surface._demo_finger_pose()


func _pose_point(pose: Dictionary) -> Vector2:
	return pose.get("at", Vector2.ZERO)


func _rect_inside(bounds: Rect2, rect: Rect2) -> bool:
	return rect.position.x >= bounds.position.x and rect.position.y >= bounds.position.y \
		and rect.end.x <= bounds.end.x and rect.end.y <= bounds.end.y


func _finish_after_render(surface: OperaGestureSurface) -> void:
	# Let CanvasItem execute each custom draw path once. Analyzer-only tests do
	# not catch invalid draw geometry or texture-region calls.
	for specialist_mode: String in [
		"xray_scan", "dance_sequence", "candy_sort", "paint_reveal", "farm_lob",
		"boxer_rhythm",
	]:
		surface.configure(specialist_mode, Color.WHITE)
		surface.queue_redraw()
		await process_frame
	_ck("all six specialist draw paths render a frame", true)
	print("GESTURE_QUALITY|result: %s (%d checks)" % [
		"ALL OK" if failed == 0 else "%d FAIL" % failed,
		checks,
	])
	quit(0 if failed == 0 else 1)


func _init() -> void:
	var surface := OperaGestureSurface.new()
	surface.size = Vector2(852, 560)
	get_root().add_child(surface)
	surface.set_process(false)
	surface.gesture.connect(_record_gesture)

	# Directional demos use the same vector as the input gate.
	surface.configure("swipe", Color.WHITE)
	surface.swipe_dir = Vector2.DOWN
	var down_start := _pose_point(_pose_at(surface, 0.0))
	var down_end := _pose_point(_pose_at(surface, 1.85))
	_ck("down-swipe hand travels down, not sideways",
		down_end.y > down_start.y + 250.0 and absf(down_end.x - down_start.x) < 1.0)

	# Specialist demos point at their actual visible controls.
	surface.configure("pourt", Color.WHITE)
	var pour_pose := _pose_at(surface, 1.2)
	_ck("pour hand grabs the real pitcher",
		_pose_point(pour_pose).distance_to(surface._pour_pitcher_rect().get_center()) < 16.0
		and bool(pour_pose.get("pressing", false)))

	surface.configure("oven", Color.WHITE)
	surface.oven_t = 0.2
	var oven_watch := _pose_at(surface, 0.4)
	_ck("cold oven hand watches the thermometer without tapping",
		surface._oven_meter_rect().grow(12.0).has_point(_pose_point(oven_watch))
		and not bool(oven_watch.get("pressing", true)))
	surface.oven_t = 0.55
	var oven_take := _pose_at(surface, 1.2)
	_ck("golden oven hand taps the mitt handle",
		_pose_point(oven_take).distance_to(surface._oven_handle_rect().get_center()) < 1.0
		and bool(oven_take.get("pressing", false)))

	surface.size = Vector2(712, 560)
	surface.configure("pipe", Color.WHITE)
	var pipe_start := _pose_point(_pose_at(surface, 0.0))
	var pipe_end := _pose_point(_pose_at(surface, 1.75))
	_ck("pipe hand carries the first tray tile to the first useful gap",
		pipe_start.distance_to(surface._pipe_tray_rect(0).get_center()) < 1.0
		and pipe_end.distance_to(surface._pipe_cell_rect(5).get_center()) < 1.0)
	var pipe_bounds := Rect2(Vector2.ZERO, surface.size)
	var pipe_geometry_inside := true
	for cell in range(OperaGestureSurface.PIPE_COLS * OperaGestureSurface.PIPE_ROWS):
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_cell_rect(cell))
	for slot in range(6):
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_tray_rect(slot))
	for round_data: Dictionary in OperaGestureSurface.PIPE_ROUNDS:
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_tank_rect(round_data))
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_intake_rect(round_data))
	_ck("all pipe cells, six tray pieces, tank, and every intake fit the surface",
		pipe_geometry_inside)
	var stage_bounds := Rect2(Vector2.ZERO, Vector2(1280, 720))
	var both_panel_docks_inside := true
	for panel_position: Vector2 in [Vector2(24, 36), Vector2(496, 36)]:
		both_panel_docks_inside = both_panel_docks_inside and _rect_inside(
			stage_bounds, Rect2(panel_position, Vector2(760, 648)))
		var surface_origin := panel_position + Vector2(24, 24)
		for round_data: Dictionary in OperaGestureSurface.PIPE_ROUNDS:
			var global_intake := surface._pipe_intake_rect(round_data)
			global_intake.position += surface_origin
			both_panel_docks_inside = both_panel_docks_inside and _rect_inside(
				stage_bounds, global_intake)
	_ck("pipe endpoint art fits 1280x720 at either authored panel dock",
		both_panel_docks_inside)
	surface.size = Vector2(852, 560)

	surface.configure("echo", Color.WHITE)
	surface.echo_listening = true
	surface.echo_input_i = 0
	var echo_pose := _pose_at(surface, 1.2)
	_ck("echo hand taps the next sung star on Roshan's turn",
		_pose_point(echo_pose).distance_to(surface._echo_star_center(0)) < 1.0
		and bool(echo_pose.get("pressing", false)))

	# Doctor uses the approved X-ray-machine card and a square scanner sweep,
	# not Detective's stage-wide magnifying glass. Only crossing a new sore spot
	# changes state; taps and unrelated motion are harmless.
	events.clear()
	surface.size = Vector2(392, 232)
	surface.configure("xray_scan", Color.WHITE)
	_ck("X-ray scan binds the approved Doctor machine card",
		surface.visual_context == "target_doctor" and surface.widget_backdrop != null
		and surface.widget_backdrop.resource_path.ends_with("widget_target_doctor.png"))
	var first_xray_target := surface._xray_target_center(0)
	var first_xray_demo := _pose_at(surface, 1.65)
	_ck("X-ray rehint sweeps to the current real sore spot",
		_pose_point(first_xray_demo).distance_to(first_xray_target) < 1.0
		and bool(first_xray_demo.get("pressing", false)))
	surface._press(first_xray_target)
	surface._release(first_xray_target)
	_ck("stationary scanner tap cannot diagnose",
		surface.xray_found_count == 0 and not _paid("xray_scan"))
	var wrong_scan_start := Vector2(24, surface.size.y - 18.0)
	var wrong_scan_end := Vector2(76, surface.size.y - 18.0)
	surface._press(wrong_scan_start)
	surface._drag(wrong_scan_end)
	surface._release(wrong_scan_end)
	_ck("unrelated scanner sweep is safe and pays zero",
		surface.xray_found_count == 0 and not _paid("xray_scan") and surface.demo_active)
	var scan_home := surface._xray_home_point()
	surface._press(scan_home)
	surface._drag(first_xray_target)
	surface._release(first_xray_target)
	_ck("first valid scan banks exactly one diagnosis",
		surface.xray_found_count == 1 and _paid_count("xray_scan") == 1
		and not surface.xray_complete)
	var second_xray_target := surface._xray_target_center(1)
	var second_xray_demo := _pose_at(surface, 1.65)
	_ck("scanner rehint advances to the second deterministic spot",
		_pose_point(second_xray_demo).distance_to(second_xray_target) < 1.0)
	surface._press(scan_home)
	surface._drag(second_xray_target)
	surface._release(second_xray_target)
	_ck("two valid scan transitions complete with exactly two payouts",
		surface.xray_complete and surface.xray_found_count == OperaGestureSurface.XRAY_SPOTS.size()
		and _paid_count("xray_scan") == OperaGestureSurface.XRAY_SPOTS.size())
	surface.size = Vector2(852, 560)

	# A stationary press supplies state/feedback only. Progress comes from a
	# sustained hold in the owner or qualifying movement in _drag().
	var center := surface.size * 0.5
	for stationary_mode: String in ["hold", "swipe", "circle"]:
		events.clear()
		surface.configure(stationary_mode, Color.WHITE)
		surface._press(center)
		_ck("stationary %s press pays no progress" % stationary_mode,
			not _paid(stationary_mode))
		if stationary_mode == "hold":
			_ck("hold press still arms sustained input", surface.held)
		surface._release(center)

	events.clear()
	surface.configure("swipe", Color.WHITE)
	surface._press(center)
	surface._drag(center + Vector2(100.0, 0.0))
	_ck("real swipe motion still advances", _paid("swipe"))
	surface._release(center + Vector2(100.0, 0.0))

	events.clear()
	surface.configure("circle", Color.WHITE)
	var radius := 90.0
	surface._press(center + Vector2.RIGHT * radius)
	surface._drag(center + Vector2.from_angle(0.28) * radius)
	surface._drag(center + Vector2.from_angle(0.56) * radius)
	_ck("real circular motion still advances", _paid("circle"))
	surface._release(center + Vector2.from_angle(0.56) * radius)

	# Four-pad dance is a true call-and-response state machine. A wrong tap
	# replays the phrase and cannot bank any of its earlier correct prefix.
	events.clear()
	surface.configure("dance_sequence", Color.WHITE)
	_ck("dance defaults to the approved ballerina context",
		surface.visual_context == "lanes_ballerina" and surface.widget_backdrop != null)
	for tick in range(28):
		surface._dance_tick(0.15)
	_ck("dance demonstrates before accepting input",
		surface.dance_listening and surface.dance_input_index == 0)
	var dance_pose := _pose_at(surface, 1.25)
	_ck("dance rehint points to the next real floor pad",
		_pose_point(dance_pose).distance_to(surface._dance_pad_rect(
			int(OperaGestureSurface.DANCE_SEQUENCE[0])).get_center()) < 1.0
		and bool(dance_pose.get("pressing", false)))
	var wrong_pad := (int(OperaGestureSurface.DANCE_SEQUENCE[0]) + 1) % 4
	surface._press(surface._dance_pad_rect(wrong_pad).get_center())
	surface._release(surface._dance_pad_rect(wrong_pad).get_center())
	_ck("wrong dance pad pays nothing and gently re-shows",
		not _paid("dance_sequence") and surface.dance_input_index == 0
		and not surface.dance_listening and surface.demo_active)
	for tick in range(28):
		surface._dance_tick(0.15)
	events.clear()
	for step in range(OperaGestureSurface.DANCE_SEQUENCE.size()):
		var pad := int(OperaGestureSurface.DANCE_SEQUENCE[step])
		var pad_center := surface._dance_pad_rect(pad).get_center()
		surface._press(pad_center)
		surface._release(pad_center)
		if step < OperaGestureSurface.DANCE_SEQUENCE.size() - 1:
			_ck("dance prefix %d is state, not scalar payout" % step,
				not _paid("dance_sequence"))
	_ck("exact dance phrase completes once",
		surface.dance_complete and _paid_count("dance_sequence") == 1)

	# Candies move slowly but never expire. Only a matching silhouette changes
	# the deterministic queue; a wrong bin resets the same piece.
	events.clear()
	surface.configure("candy_sort", Color.WHITE)
	_ck("candy sort binds its three-bin authored card",
		surface.visual_context == "lanes_candymaker" and surface.widget_backdrop != null
		and surface.candy_type == int(OperaGestureSurface.CANDY_SEQUENCE[0]))
	var candy_start_type := surface.candy_type
	for tick in range(160):
		surface._candy_tick(0.10)
	_ck("missed candy safely loops without queue progress",
		surface.candy_loops > 0 and surface.candy_piece_index == 0
		and surface.candy_type == candy_start_type and not _paid("candy_sort"))
	var wrong_bin := (surface.candy_type + 1) % 3
	var candy_start := surface.candy_position
	var wrong_target := surface._candy_bin_rect(wrong_bin).get_center()
	surface._press(candy_start)
	surface._drag(wrong_target)
	surface._release(wrong_target)
	_ck("wrong candy bin returns the same piece with no payout",
		surface.candy_sorted == 0 and surface.candy_piece_index == 0
		and surface.candy_type == candy_start_type and not _paid("candy_sort")
		and surface.demo_active)
	var candy_demo_start := _pose_point(_pose_at(surface, 0.0))
	var candy_demo_end := _pose_point(_pose_at(surface, 1.80))
	_ck("candy rehint carries the live piece to its matching bin",
		candy_demo_start.distance_to(surface.candy_position) < 1.0
		and candy_demo_end.distance_to(surface._candy_bin_rect(surface.candy_type).get_center()) < 1.0)
	events.clear()
	for sorted_piece in range(OperaGestureSurface.CANDY_SEQUENCE.size()):
		var expected_type := surface.candy_type
		var piece_center := surface.candy_position
		var matching_bin := surface._candy_bin_rect(expected_type).get_center()
		surface._press(piece_center)
		surface._drag(matching_bin)
		surface._release(matching_bin)
		if sorted_piece == 0:
			_ck("first match advances to the deterministic second piece",
				surface.candy_type == int(OperaGestureSurface.CANDY_SEQUENCE[1]))
	_ck("six valid candy matches complete with six payouts",
		surface.candy_complete and surface.candy_sorted == OperaGestureSurface.CANDY_SEQUENCE.size()
		and _paid_count("candy_sort") == OperaGestureSurface.CANDY_SEQUENCE.size())

	# Paint completion comes from newly covered grid cells. The owner's scalar
	# fill and stationary tap mashing are deliberately irrelevant.
	events.clear()
	surface.configure("paint_reveal", Color.WHITE)
	surface.set_fill(1.0)
	_ck("paint reveal binds the finished sunrise art",
		surface.visual_context == "trace_painter" and surface.paint_reveal_texture != null)
	var paint_canvas := surface._paint_canvas_rect()
	for tap in range(18):
		var tap_point := paint_canvas.position + paint_canvas.size * Vector2(
			(float(tap % 6) + 0.5) / 6.0, (float(tap / 6) + 0.5) / 3.0)
		surface._press(tap_point)
		surface._release(tap_point)
	_ck("stationary paint mashing uncovers no cells",
		surface.paint_covered == 0 and not surface.paint_complete
		and not _paid("paint_reveal"))
	for row in range(OperaGestureSurface.PAINT_GRID_ROWS):
		if surface.paint_complete:
			break
		var y := paint_canvas.position.y + paint_canvas.size.y \
			* (float(row) + 0.5) / float(OperaGestureSurface.PAINT_GRID_ROWS)
		var stroke_start := Vector2(paint_canvas.position.x + 2.0, y)
		var stroke_end := Vector2(paint_canvas.end.x - 2.0, y)
		surface._press(stroke_start)
		surface._drag(stroke_end)
		surface._release(stroke_end)
	_ck("real strokes complete from coarse coverage state",
		surface.paint_complete and surface.paint_covered >= surface._paint_required_cells()
		and surface.paint_coverage() >= OperaGestureSurface.PAINT_REQUIRED_COVERAGE)
	_ck("paint completion emits exactly one whole-picture payout",
		_paid_count("paint_reveal") == 1)
	var paint_demo := _pose_at(surface, 1.1)
	_ck("paint wordless demo stays on the actual canvas",
		paint_canvas.has_point(_pose_point(paint_demo))
		and bool(paint_demo.get("pressing", false)))

	# Farmer feed is a release-driven lob. A tap or weak pull visibly loops the
	# same corn home; only the end of a valid arc pays one landing.
	events.clear()
	surface.configure("farm_lob", Color.WHITE)
	_ck("farm lob binds pig basket and isolated corn art",
		surface.visual_context == "target_farmer" and surface.widget_backdrop != null
		and surface.farm_vegetable_texture != null)
	var farm_anchor := surface._farm_anchor_point()
	var farm_target := surface._farm_target_center()
	var farm_demo_start := _pose_point(_pose_at(surface, 0.0))
	var farm_demo_pull := _pose_point(_pose_at(surface, 1.15))
	_ck("farm demo visibly pulls backward from the basket",
		farm_demo_start.distance_to(farm_anchor) < 1.0
		and (farm_demo_pull - farm_anchor).dot(farm_target - farm_anchor) < 0.0)
	surface._press(farm_anchor)
	surface._release(farm_anchor)
	for tick in range(12):
		surface._farm_tick(0.10)
	_ck("weak farm release loops home without progress",
		surface.farm_loops == 1 and surface.farm_landed == 0
		and surface.farm_piece_position.distance_to(farm_anchor) < 1.0
		and not _paid("farm_lob"))
	var pull_point := surface._farm_demo_pull_point()
	surface._press(farm_anchor)
	surface._drag(pull_point)
	surface._release(pull_point)
	_ck("backward farm release arms a landing but pays only after flight",
		surface.farm_flying and surface.farm_will_land and not _paid("farm_lob"))
	surface._farm_tick(OperaGestureSurface.FARM_FLIGHT_DURATION * 0.5)
	var straight_midpoint := pull_point.lerp(farm_target, 0.5)
	_ck("farm vegetable follows a visible upward arc",
		surface.farm_piece_position.y < straight_midpoint.y - 20.0)
	surface._farm_tick(OperaGestureSurface.FARM_FLIGHT_DURATION * 0.5 + 0.01)
	_ck("first landed vegetable emits exactly one payout",
		surface.farm_landed == 1 and _paid_count("farm_lob") == 1)
	for landing in range(1, OperaGestureSurface.FARM_LOB_GOAL):
		surface._farm_tick(0.50)
		var next_anchor := surface._farm_anchor_point()
		surface._press(next_anchor)
		surface._drag(surface._farm_demo_pull_point())
		surface._release(surface._farm_demo_pull_point())
		for flight_tick in range(10):
			surface._farm_tick(0.10)
	_ck("four deterministic farm landings complete with four payouts",
		surface.farm_complete and surface.farm_landed == OperaGestureSurface.FARM_LOB_GOAL
		and _paid_count("farm_lob") == OperaGestureSurface.FARM_LOB_GOAL)

	# Boxer rhythm has no timing gate: follow the highlighted alternating mitt.
	# The midpoint duck is a demonstrated downward state transition, not a hit.
	events.clear()
	surface.configure("boxer_rhythm", Color.WHITE)
	_ck("boxer rhythm binds approved focus-pad art and starts left",
		surface.visual_context == "lanes_boxer" and surface.widget_backdrop != null
		and surface.widget_mover != null and surface.boxer_expected == 0)
	var boxer_pose := _pose_at(surface, 1.15)
	_ck("boxer hand points at the highlighted real mitt",
		_pose_point(boxer_pose).distance_to(surface._boxer_mitt_rect(0).get_center()) < 1.0
		and bool(boxer_pose.get("pressing", false)))
	var boxer_wrong := surface._boxer_mitt_rect(1).get_center()
	surface._press(boxer_wrong)
	surface._release(boxer_wrong)
	_ck("wrong boxer mitt pays zero and reflashes without advancing",
		surface.boxer_hit_index == 0 and surface.boxer_expected == 0
		and not _paid("boxer_rhythm") and surface.boxer_flash > 1.0
		and surface.demo_active)
	for hit in range(OperaGestureSurface.BOXER_DUCK_AFTER):
		var mitt := surface._boxer_mitt_rect(surface.boxer_expected).get_center()
		surface._press(mitt)
		surface._release(mitt)
	_ck("first three alternating mitts bank exactly three hits",
		surface.boxer_hit_index == OperaGestureSurface.BOXER_DUCK_AFTER
		and _paid_count("boxer_rhythm") == OperaGestureSurface.BOXER_DUCK_AFTER
		and surface.boxer_duck_pending)
	var duck_demo_start := _pose_point(_pose_at(surface, 0.0))
	var duck_demo_end := _pose_point(_pose_at(surface, 1.55))
	_ck("boxer interlude clearly demonstrates a downward duck",
		duck_demo_end.y > duck_demo_start.y + surface.size.y * 0.50
		and absf(duck_demo_end.x - duck_demo_start.x) < 1.0)
	surface._press(center)
	surface._release(center)
	_ck("tapping through the duck cannot bank another hit",
		surface.boxer_duck_pending
		and surface.boxer_hit_index == OperaGestureSurface.BOXER_DUCK_AFTER
		and _paid_count("boxer_rhythm") == OperaGestureSurface.BOXER_DUCK_AFTER)
	var duck_start := Vector2(center.x, surface.size.y * 0.20)
	var duck_finish := Vector2(center.x, surface.size.y * 0.82)
	surface._press(duck_start)
	surface._drag(duck_finish)
	surface._release(duck_finish)
	_ck("real downward duck resumes phrase with zero scalar payout",
		surface.boxer_duck_done and not surface.boxer_duck_pending
		and surface.boxer_hit_index == OperaGestureSurface.BOXER_DUCK_AFTER
		and _paid_count("boxer_rhythm") == OperaGestureSurface.BOXER_DUCK_AFTER)
	while not surface.boxer_complete:
		var next_mitt := surface._boxer_mitt_rect(surface.boxer_expected).get_center()
		surface._press(next_mitt)
		surface._release(next_mitt)
	_ck("six alternating mitts complete with six payouts",
		surface.boxer_hit_index == OperaGestureSurface.BOXER_SEQUENCE.size()
		and _paid_count("boxer_rhythm") == OperaGestureSurface.BOXER_SEQUENCE.size())

	call_deferred("_finish_after_render", surface)
