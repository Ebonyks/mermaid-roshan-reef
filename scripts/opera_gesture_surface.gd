class_name OperaGestureSurface
extends Control
## One-finger input surface shared by all thirteen 2D Opera career worlds.
##
## The surrounding world chooses a gesture mode; this node turns mouse and
## touchscreen input into normalized progress without owning career state.
## Incorrect timing/choices report lower quality but still make a little
## progress, so there is no dead end for a non-reader.

signal gesture(kind: String, amount: float, quality: float)

var mode := "tap"
var accent := Color(1.0, 0.62, 0.8)
var target_choice := 1
var choice_count := 3
var timing_position := 0.0
var timing_zone := Vector2(0.30, 0.72)
var held := false
var pointer_pos := Vector2.ZERO
var previous_pos := Vector2.ZERO
var previous_angle := 0.0
var have_angle := false
var _last_spin := 0.0
## Friendly imp-scuffle targets for the "bop" combat beats. Each entry:
## {home: Vector2, pos: Vector2, r: float, hp: int, captain: bool, popped: bool}
var bop_targets: Array = []
var bop_texture: Texture2D = null
var bop_captain_texture: Texture2D = null
var last_bop_pos := Vector2.ZERO


## Ghost-finger demo: until the child touches, a glowing dot acts out the
## expected gesture so no phase ever needs reading to understand.
var demo_active := true
var demo_t := 0.0
var _demo_redraw := 0.0
var input_started := false
var feedback_t := 0.0
var feedback_positive := false
var feedback_position := 0.0
var feedback_anchor := Vector2.ZERO
var completion_accepted := false
## Choice lanes flash gold briefly, then dim so the pick uses recognition
## memory instead of tap-the-highlight; wrong picks kindly re-flash.
var choice_flash := 1.4
## Shell-game glide (magician TRACK): after the flash, the glow visibly
## slides from the flashed lane into the target lane before dimming.
var shuffle_from := -1
var shuffle_t := 0.0
## Oven bake (chef BAKE, owner 2026-08-04): heat RISES AT A STATIC RATE and
## the child REMOVES the cake by tapping the big mitt handle. Bands: pale ->
## golden window -> toasty -> cap, then a kind auto-ding. A toastier cake is
## still a cake — there is no burn state and no fail branch anywhere.
var oven_t := 0.0
var oven_grace := 0.0
var oven_peek := 0.0
var oven_done := false
var oven_redraw := 0.0
## Bubble-fuel pipes (astronaut PIPES; owner-mandated mini Pipe Dream).
## Place or slide PRE-ROTATED tiles — no rotation control exists anywhere,
## no timer, no failure: fuel WAITS kindly at a gap, and after 8s a gold
## twinkle marks the cell that needs a tile. Three rounds, each one pipe
## longer, with napping imps as the routing puzzle (they never touch tiles
## the child has placed — escalation is routing, not sabotage).
const PIPE_COLS := 4
const PIPE_ROWS := 3
const PIPE_CELL := 128.0
const PIPE_ORIGIN := Vector2(170.0, 40.0)
const PIPE_MOUTHS := {
	"H": [Vector2i(-1, 0), Vector2i(1, 0)],
	"V": [Vector2i(0, -1), Vector2i(0, 1)],
	"NE": [Vector2i(0, -1), Vector2i(1, 0)],
	"NW": [Vector2i(0, -1), Vector2i(-1, 0)],
	"SE": [Vector2i(0, 1), Vector2i(1, 0)],
	"SW": [Vector2i(0, 1), Vector2i(-1, 0)],
}
## rounds: fixed stubs are pre-placed and never liftable; imps nap on their
## cells and giggle when tapped, but stay (tray = needed tiles + at most one)
const PIPE_ROUNDS := [
	{"entry": 4, "exit": 7, "exit_dir": Vector2i(1, 0), "fixed": {4: "H", 7: "H"}, "imps": [], "tray": ["H", "H"]},
	{"entry": 4, "exit": 7, "exit_dir": Vector2i(1, 0), "fixed": {4: "NW", 7: "H"}, "imps": [5], "tray": ["SE", "H", "SW", "NE", "H"]},
	{"entry": 4, "exit": 3, "exit_dir": Vector2i(0, -1), "fixed": {4: "H"}, "imps": [0, 6], "tray": ["H", "NW", "SE", "H", "NW", "V"]},
]
var pipe_round := 0
var pipe_grid: Array = []
var pipe_fixed: Array = []
var pipe_tray: Array = []
var pipe_tray_sel := -1
var pipe_drag_tile := ""
var pipe_drag_from := -1
var pipe_flow: Array = []
var pipe_flow_t := 0.0
var pipe_wait_t := 0.0
var pipe_pause := 0.0
var pipe_redraw := 0.0

## Echo Song (popstar RHYTHM rebuild): three stage stars light in order
## with pitched notes; the child taps them back in ANY tempo — order
## matters, speed never does. Wrong star kindly replays the verse.
const ECHO_VERSES := [[0, 2], [0, 1, 2], [2, 1, 0]]
var echo_verse := 0
var echo_show_i := -1
var echo_show_t := 0.0
var echo_input_i := 0
var echo_listening := false
var echo_last_note := 0
var echo_glow := 0.0
## Tilt-pour (chef POUR / candymaker SYRUP): grab the pitcher and it TILTS;
## the stream follows, the bowl fills only while the stream lands in it,
## and the pitcher visibly drains. The child controls the pour, not a clock.
var pour_tilt := 0.0
var pour_x := 0.0
var pour_level := 0.0
var pour_reserve := 1.2
var pour_hold := false
var pour_emit_acc := 0.0
var pour_redraw := 0.0

## Directional hint for swipe phases (DUCK draws a downward arrow).
var swipe_dir := Vector2.RIGHT
## Tap phases stamp a happy mark AT THE FINGER (owner 2026-08-04: free
## placement is the game — decorating, splatting, pearl-setting; the old
## wandering hotspot rewarded chasing a dot instead of making a thing).
var tap_marks: Array = []
## Finger trail for trace phases: the reveal follows the child's own path.
var trace_points: Array = []
## Diegetic scene painted behind the affordance (nursery basin/bottle/cribs).
var visual_context := ""
var nursery_textures: Array[Texture2D] = []
var widget_template := ""
var widget_fill := 0.0
var widget_backdrop: Texture2D = null
var widget_mover: Texture2D = null
var widget_overlay: Texture2D = null
var widget_stamp: Texture2D = null
var widget_shared: Texture2D = null
## Pipe-dream tile art (ledger P1). Code-drawn until these land; the draw
## path prefers the texture whenever the face has one.
var pipe_tiles: Dictionary = {}
var pipe_tank_texture: Texture2D = null
var pipe_intake_texture: Texture2D = null
## Echo Song star pads (ledger P2), tinted per star at runtime.
var echo_unlit_texture: Texture2D = null
var echo_lit_texture: Texture2D = null
var crank_rotation := 0.0
## Trickle-by-assist (house pattern from fetch/melody/dolls): wrong input
## always celebrates but pays ~nothing, and repeat misses inside the
## cooldown pay zero — correct play must strictly beat mashing.
const MISS_COOLDOWN := {"tap": 0.5, "choice": 0.6, "timing": 1.0, "oven": 1.0}
var miss_cool := 0.0
## Swipe honesty: per-event travel cap plus a refilling per-second budget
## so scrubbing cannot trivialize goals; direction gates only when the
## phase declares one (DUCK down, BEDTIME down).
var swipe_budget := 1.3
var swipe_require_dir := false


func _miss_pay() -> float:
	# first miss trickles a crumb; repeats inside the cooldown pay nothing
	if miss_cool > 0.0:
		return 0.0
	miss_cool = float(MISS_COOLDOWN.get(mode, 0.5))
	return 0.05


func configure(next_mode: String, next_accent: Color, choice: int = 1, next_context: String = "") -> void:
	mode = next_mode
	accent = next_accent
	target_choice = choice
	visual_context = next_context
	widget_fill = 0.0
	completion_accepted = false
	feedback_t = 0.0
	feedback_positive = false
	feedback_position = 0.0
	feedback_anchor = Vector2.ZERO
	input_started = false
	crank_rotation = 0.0
	_load_widget_set()
	if visual_context.ends_with("_nursery") and nursery_textures.is_empty():
		for index in range(3):
			var path := "res://assets/opera/worlds/nursery/baby_%d.png" % index
			var texture := load(path) as Texture2D
			if texture != null:
				nursery_textures.append(texture)
	held = false
	have_angle = false
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.4
	miss_cool = 0.0
	swipe_budget = 1.3
	swipe_require_dir = false
	swipe_dir = Vector2.RIGHT
	tap_marks = []
	trace_points = []
	shuffle_t = 0.0
	shuffle_from = -1
	oven_t = 0.0
	oven_grace = 0.0
	oven_peek = 0.0
	oven_done = false
	if next_mode == "pipe":
		pipe_round = 0
		_pipe_setup_round()
		if pipe_tiles.is_empty():
			var faces := {
				"H": "tile_h", "V": "tile_v", "NE": "elbow_ne",
				"NW": "elbow_nw", "SE": "elbow_se", "SW": "elbow_sw",
			}
			for face: String in faces.keys():
				var tile := _load_widget_texture(
					"res://assets/opera/worlds/widgets/widget_pipe_%s.png" % faces[face])
				if tile != null:
					pipe_tiles[face] = tile
			pipe_tank_texture = _load_widget_texture("res://assets/opera/worlds/widgets/widget_pipe_tank.png")
			pipe_intake_texture = _load_widget_texture("res://assets/opera/worlds/widgets/widget_pipe_intake.png")
	if next_mode == "echo" and echo_unlit_texture == null:
		echo_unlit_texture = _load_widget_texture("res://assets/opera/worlds/widgets/popstar_star_note_unlit.png")
		echo_lit_texture = _load_widget_texture("res://assets/opera/worlds/widgets/popstar_star_note_lit.png")
	if next_mode == "echo":
		echo_verse = 0
		echo_show_i = -1
		echo_show_t = 0.0
		echo_input_i = 0
		echo_listening = false
		echo_glow = 0.0
	if next_mode == "pourt":
		pour_tilt = 0.0
		pour_x = size.x * 0.34
		pour_level = 0.0
		pour_reserve = 1.2
		pour_hold = false
		pour_emit_acc = 0.0
	if next_mode != "bop":
		bop_targets = []
	queue_redraw()


func _load_widget_texture(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _load_widget_set() -> void:
	widget_template = visual_context.get_slice("_", 0) if not visual_context.is_empty() else ""
	widget_backdrop = null
	widget_mover = null
	widget_overlay = null
	widget_stamp = null
	widget_shared = null
	if widget_template.is_empty():
		return
	var prefix := "res://assets/opera/worlds/widgets/widget_%s" % visual_context
	widget_backdrop = _load_widget_texture("%s.png" % prefix)
	match widget_template:
		"gauge":
			widget_mover = _load_widget_texture("res://assets/opera/worlds/widgets/widget_gauge_shared_needle.png")
			widget_overlay = _load_widget_texture("%s_success.png" % prefix)
		"track":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_track_shared_hit.png")
		"pour":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_overlay = _load_widget_texture("%s_fill.png" % prefix)
		"basin":
			widget_overlay = _load_widget_texture("%s_bubbles.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_basin_shared_shine.png")
		"charge":
			widget_mover = _load_widget_texture("%s_glow.png" % prefix)
			widget_overlay = _load_widget_texture("%s_full.png" % prefix)
		"crank":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_overlay = _load_widget_texture("%s_progress.png" % prefix)
		"trace":
			widget_overlay = _load_widget_texture("%s_lit.png" % prefix)
		"push":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			var down := visual_context.ends_with("_boxer") or visual_context.ends_with("_nursery")
			var shared_name := "arrow_down" if down else "arrow_lr"
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_push_shared_%s.png" % shared_name)
		"target":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_stamp = _load_widget_texture("%s_mark.png" % prefix)
			widget_overlay = _load_widget_texture("%s_success.png" % prefix)
		"lanes":
			widget_mover = _load_widget_texture("%s_lit.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_lanes_shared_pick.png")


func note_input() -> void:
	input_started = true
	demo_active = false
	queue_redraw()


func note_result(accepted: bool) -> void:
	feedback_positive = accepted
	feedback_t = 0.32
	queue_redraw()


func accept_completion() -> void:
	completion_accepted = true
	feedback_positive = true
	feedback_t = maxf(feedback_t, 0.32)
	queue_redraw()


func restart_demo() -> void:
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.2


func reflash_choice() -> void:
	choice_flash = 1.2
	queue_redraw()


func _process(delta: float) -> void:
	if miss_cool > 0.0:
		miss_cool = maxf(0.0, miss_cool - delta)
	swipe_budget = minf(1.3, swipe_budget + delta * 1.3)
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - delta)
		queue_redraw()
	if choice_flash > 0.0 and mode == "choice":
		choice_flash -= delta
		if choice_flash <= 0.0:
			queue_redraw()
	if shuffle_t > 0.0 and mode == "choice":
		shuffle_t = maxf(0.0, shuffle_t - delta)
		queue_redraw()
	if mode == "pipe" and not completion_accepted:
		_pipe_tick(delta)
	if mode == "echo" and not completion_accepted:
		_echo_tick(delta)
	if mode == "pourt" and not completion_accepted:
		_pour_tick(delta)
	if mode == "oven" and not completion_accepted:
		if oven_peek > 0.0:
			# door open for a peek — the heat politely waits
			oven_peek = maxf(0.0, oven_peek - delta)
		elif not oven_done:
			# STATIC rate: cold to cap in 8s, no acceleration, never resets
			oven_t = minf(1.0, oven_t + delta / 8.0)
			if oven_t >= 1.0:
				oven_grace += delta
				if oven_grace >= 1.2:
					# auto-ding: the door springs open on its own. Extra
					# toasty is a KIND of cake, not a failure.
					oven_done = true
					gesture.emit("oven", 999.0, 0.7)
		oven_redraw += delta
		if oven_redraw >= 0.05:
			oven_redraw = 0.0
			queue_redraw()
	if not demo_active:
		return
	demo_t += delta
	_demo_redraw += delta
	if _demo_redraw >= 0.05:
		_demo_redraw = 0.0
		queue_redraw()


func set_bop_targets(targets: Array) -> void:
	bop_targets = targets
	queue_redraw()


func bop_remaining() -> int:
	var left := 0
	for target: Dictionary in bop_targets:
		if not bool(target.get("popped", false)):
			left += 1
	return left


func set_timing_position(value: float) -> void:
	timing_position = clampf(value, 0.0, 1.0)
	if mode == "timing":
		queue_redraw()


func set_fill(value: float) -> void:
	widget_fill = clampf(value, 0.0, 1.0)
	if widget_backdrop != null:
		queue_redraw()


func _press(at: Vector2) -> void:
	note_input()
	held = true
	pointer_pos = at
	previous_pos = at
	previous_angle = (at - size * 0.5).angle()
	have_angle = true
	_last_spin = 0.0
	feedback_anchor = at
	feedback_position = timing_position
	match mode:
		"tap":
			# every tap lands its mark where the finger is — placing, not aiming
			tap_marks.append(at)
			gesture.emit("tap", 1.0, 1.0)
		"choice":
			var lane := clampi(int(at.x / maxf(1.0, size.x) * float(choice_count)), 0, choice_count - 1)
			if lane == target_choice:
				gesture.emit("choice", 1.0, 1.0)
			else:
				gesture.emit("choice", _miss_pay(), 0.0)
		"timing":
			if timing_position >= timing_zone.x and timing_position <= timing_zone.y:
				gesture.emit("timing", 1.0, 1.0)
			else:
				gesture.emit("timing", _miss_pay(), 0.32)
		"bop":
			_bop_press(at)
		"pipe":
			if completion_accepted:
				gesture.emit("pipe", 0.0, 1.0)   # skips the completion hold
			else:
				_pipe_press(at)
		"echo":
			if completion_accepted:
				gesture.emit("echo", 0.0, 1.0)
			else:
				_echo_press(at)
		"pourt":
			if _pour_pitcher_rect().has_point(at):
				pour_hold = true
				pour_x = clampf(at.x, size.x * 0.12, size.x * 0.88)
			else:
				# a tap on the bowl answers with a friendly ripple
				gesture.emit("pourt", 0.0, 0.6)
		"oven":
			if oven_done or completion_accepted:
				gesture.emit("oven", 0.0, 1.0)
			elif oven_t < 0.45:
				# a peek: door opens, the cake jiggles gooey, baking resumes.
				# The trickle teaches color-watching; mashing pays nothing.
				oven_peek = 0.7
				gesture.emit("oven", _miss_pay(), 0.55)
			else:
				# she takes the cake out — golden is perfect, toasty is still
				# wonderful, and the difference is only the confetti's size
				oven_done = true
				gesture.emit("oven", 999.0, 1.0 if oven_t <= 0.80 else 0.7)
		"hold":
			# a tap on the hold circle answers with a small warm trickle
			gesture.emit("hold", 0.06, 0.6)
		"swipe", "circle":
			gesture.emit(mode, 0.05, 0.6)
	queue_redraw()


func _bop_press(at: Vector2) -> void:
	for target: Dictionary in bop_targets:
		if bool(target.get("popped", false)):
			continue
		var pos: Vector2 = target.get("pos", Vector2.ZERO)
		var reach := float(target.get("r", 44.0)) * 1.45
		if at.distance_to(pos) <= reach:
			target["hp"] = int(target.get("hp", 1)) - 1
			last_bop_pos = pos
			if int(target["hp"]) <= 0:
				target["popped"] = true
			gesture.emit("bop", 1.0, 1.0)
			return
	# a stray tap fizzles kindly and still trickles a little progress
	last_bop_pos = at
	gesture.emit("bop", 0.12, 0.2)


func _drag(at: Vector2) -> void:
	note_input()
	pointer_pos = at
	var distance := at.distance_to(previous_pos)
	if mode == "swipe" and distance > 0.0:
		var travel := minf(distance, 34.0) / 150.0
		travel = minf(travel, swipe_budget)
		if travel > 0.0:
			swipe_budget -= travel
			var aligned := 1.0
			if swipe_require_dir:
				aligned = maxf(0.0, (at - previous_pos).normalized().dot(swipe_dir))
			if aligned >= 0.35:
				gesture.emit("swipe", travel, 1.0)
			else:
				# wrong-direction wiggles fizzle kindly, tiny trickle
				gesture.emit("swipe", travel * 0.2, 0.4)
	if mode == "pipe":
		queue_redraw()
		previous_pos = at
		return
	if mode == "pourt":
		if pour_hold:
			pour_x = clampf(at.x, size.x * 0.12, size.x * 0.88)
		queue_redraw()
		previous_pos = at
		return
	if mode == "swipe" and widget_template == "trace":
		if trace_points.is_empty() or at.distance_to(trace_points[trace_points.size() - 1]) > 24.0:
			trace_points.append(at)
	elif mode == "circle":
		var center := size * 0.5
		var radius := at.distance_to(center)
		if radius > minf(size.x, size.y) * 0.13:
			var angle := (at - center).angle()
			if have_angle:
				var change := wrapf(angle - previous_angle, -PI, PI)
				crank_rotation = angle
				# straight-line scrubs cross the center as big sign-flipping
				# jumps; honest circling is small same-sign steps
				if absf(change) <= 0.9 and signf(change) == signf(_last_spin) and absf(_last_spin) > 0.0001:
					gesture.emit("circle", absf(change) / TAU, 1.0)
				_last_spin = change
			previous_angle = angle
			have_angle = true
	previous_pos = at
	queue_redraw()


func _release(at: Vector2) -> void:
	held = false
	pointer_pos = at
	have_angle = false
	if mode == "pipe":
		_pipe_release(at)
	if mode == "pourt":
		pour_hold = false
	if mode == "hold" and widget_fill > 0.22:
		# the wind-up pays off on release — the hop, the swell, the flourish
		gesture.emit("hold_release", 0.0, 1.0)
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_press(touch.position)
		else:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_drag(drag.position)
		accept_event()
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION:
			return  # already handled as the touch event on tablets
		if button.pressed:
			_press(button.position)
		else:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and held:
		if (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _draw() -> void:
	var panel := Rect2(Vector2.ZERO, size)
	# light paper inset window per the StorybookUI language
	draw_rect(panel, Color(0.94, 0.97, 1.0, 0.96), true)
	draw_rect(panel.grow(-3.0), accent.lerp(Color("#382485"), 0.62), false, 4.0)
	var center := size * 0.5
	if mode == "pipe":
		_draw_pipe()
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "echo":
		_draw_echo(center)
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "pourt":
		_draw_pour_scene(center)
		if demo_active:
			_draw_demo_finger()
		return
	if mode == "oven":
		_draw_oven(center)
		if demo_active:
			_draw_demo_finger()
		return
	if widget_backdrop != null:
		# authored at 1024x608 (1.684); the panel is not that aspect, so a plain
		# stretch squashed every round object into an egg. Cover-fit instead.
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
		_draw_widget_layers(center)
		if demo_active:
			_draw_demo_finger()
		return
	if visual_context.begins_with("nursery"):
		_draw_nursery_context(center)
		if demo_active:
			_draw_demo_finger()
		return
	match mode:
		"tap":
			# free placement: the marks ARE the picture; no hotspot to chase.
			# The ghost-finger demo teaches "touch here makes a mark".
			for mark: Vector2 in tap_marks:
				draw_circle(mark, 13.0, Color(accent, 0.85))
				draw_circle(mark, 6.0, Color.WHITE)
			if held:
				draw_circle(pointer_pos, 26.0, Color(accent, 0.35))
		"hold":
			draw_circle(center, minf(size.x, size.y) * 0.25, Color(accent, 0.24))
			draw_arc(center, minf(size.x, size.y) * 0.25, 0.0, TAU, 48, accent, 10.0)
			draw_circle(center, 24.0 if held else 16.0, Color.WHITE)
		"swipe":
			var span := minf(size.x, size.y) * 0.42
			var tail := center - swipe_dir * span
			var head := center + swipe_dir * span
			var side := swipe_dir.orthogonal()
			draw_line(tail, head, accent, 16.0, true)
			draw_colored_polygon(PackedVector2Array([
				head + side * 34.0, head + swipe_dir * 58.0, head - side * 34.0,
			]), accent)
			draw_circle(tail, 22.0, Color.WHITE)
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			draw_arc(center, radius, -2.7, 2.2, 48, accent, 16.0)
			var tip := center + Vector2.from_angle(2.2) * radius
			draw_colored_polygon(PackedVector2Array([
				tip, tip + Vector2(-10, -36), tip + Vector2(30, -14),
			]), accent)
		"choice":
			var show_answer := choice_flash > 0.0 or demo_active
			for index in range(choice_count):
				var point := Vector2(size.x * (float(index) + 0.5) / float(choice_count), center.y)
				var is_answer := index == target_choice and show_answer
				var colour := Color(1.0, 0.86, 0.32) if is_answer else Color(0.34, 0.42, 0.62)
				draw_circle(point, 54.0, Color(colour, 0.34))
				draw_arc(point, 54.0, 0.0, TAU, 36, colour, 9.0)
				if is_answer:
					draw_circle(point, 15.0, Color.WHITE)
		"timing":
			var bar := Rect2(size.x * 0.12, center.y - 23.0, size.x * 0.76, 46.0)
			draw_rect(bar, Color(0.2, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 28.0), Vector2(marker_x, bar.end.y + 28.0), Color.WHITE, 12.0)
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					_draw_imp(target)
	if demo_active:
		_draw_demo_finger()


## Overlay ink bounds, cached per texture: the reveal must sweep the PAINTED
## band, not the whole 608px canvas. Sweeping the canvas made the pour
## saturate at 43% of the hold and then sit frozen — the exact playtest
## complaint ("no animation, no feedback").
var _ink_cache: Dictionary = {}


func _ink_bounds(texture: Texture2D) -> Vector2:
	var key := texture.resource_path
	if _ink_cache.has(key):
		return _ink_cache[key]
	var bounds := Vector2(0.0, 1.0)
	var image := texture.get_image()
	if image != null:
		var h := image.get_height()
		var w := image.get_width()
		var top := -1
		var bottom := -1
		for y in range(h):
			var painted := false
			for x in range(0, w, 4):
				if image.get_pixel(x, y).a > 0.08:
					painted = true
					break
			if painted:
				if top < 0:
					top = y
				bottom = y
		if top >= 0 and bottom > top:
			bounds = Vector2(float(top) / float(h), float(bottom + 1) / float(h))
	_ink_cache[key] = bounds
	return bounds


## Aspect-preserving cover rect: fills the panel, centred, never distorted.
func _cover_rect(texture: Texture2D) -> Rect2:
	var tex := texture.get_size()
	if tex.x <= 0.0 or tex.y <= 0.0:
		return Rect2(Vector2.ZERO, size)
	var scale := maxf(size.x / tex.x, size.y / tex.y)
	var drawn := tex * scale
	return Rect2((size - drawn) * 0.5, drawn)


func _draw_progress_overlay(texture: Texture2D, progress: float, horizontal: bool) -> void:
	var amount := clampf(progress, 0.0, 1.0)
	if amount <= 0.0:
		return
	var texture_size := texture.get_size()
	if horizontal:
		var source := Rect2(0.0, 0.0, texture_size.x * amount, texture_size.y)
		var destination := Rect2(0.0, 0.0, size.x * amount, size.y)
		draw_texture_rect_region(texture, destination, source)
		return
	# sweep the reveal edge across the ink band so 0%..100% of the hold maps
	# to 0%..100% of the visible liquid
	var ink := _ink_bounds(texture)
	var ink_top := ink.x
	var ink_bottom := ink.y
	var edge := ink_bottom - (ink_bottom - ink_top) * amount
	var source_y := texture_size.y * edge
	var source_h := texture_size.y * (ink_bottom - edge)
	if source_h <= 0.0:
		return
	var cover := _cover_rect(texture)
	var destination_y := cover.position.y + cover.size.y * edge
	var destination_h := cover.size.y * (ink_bottom - edge)
	draw_texture_rect_region(
		texture,
		Rect2(cover.position.x, destination_y, cover.size.x, destination_h),
		Rect2(0.0, source_y, texture_size.x, source_h)
	)


func _draw_widget_sprite(texture: Texture2D, center: Vector2, side: float, modulate := Color.WHITE) -> void:
	if texture == null:
		return
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side), false, modulate)


func _draw_widget_layers(center: Vector2) -> void:
	match widget_template:
		"gauge":
			if widget_mover != null:
				var pivot := Vector2(size.x * 0.5, size.y * 0.82)
				var rotation := deg_to_rad(lerpf(-60.0, 60.0, timing_position))
				draw_set_transform(pivot, rotation)
				draw_texture_rect(widget_mover, Rect2(-48.0, -84.0, 96.0, 96.0), false)
				draw_set_transform(Vector2.ZERO)
			if widget_overlay != null and (completion_accepted or (feedback_t > 0.0 and feedback_positive)):
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
		"track":
			var run_point := Vector2(lerpf(size.x * 0.12, size.x * 0.88, timing_position), size.y * 0.66)
			_draw_widget_sprite(widget_mover, run_point, 128.0)
			if widget_shared != null and feedback_t > 0.0 and feedback_positive:
				var hit_point := Vector2(lerpf(size.x * 0.12, size.x * 0.88, feedback_position), size.y * 0.66)
				_draw_widget_sprite(widget_shared, hit_point, 82.0)
		"pour":
			if held:
				_draw_widget_sprite(widget_mover, center - Vector2(0.0, 18.0), 138.0)
			if widget_overlay != null:
				_draw_progress_overlay(widget_overlay, widget_fill, false)
		"basin":
			if widget_overlay != null and (held or completion_accepted):
				_draw_progress_overlay(widget_overlay, widget_fill, false)
			if completion_accepted:
				_draw_widget_sprite(widget_shared, center, 118.0)
		"charge":
			if widget_mover != null and (held or completion_accepted):
				_draw_widget_sprite(widget_mover, center, 108.0 + widget_fill * 126.0)
			if widget_overlay != null:
				if completion_accepted:
					draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
				else:
					# the meter tube fills as she holds — it used to stay dark
					# for 3+ seconds and then fade in whole over the last 18%
					_draw_progress_overlay(widget_overlay, widget_fill, false)
		"crank":
			if widget_mover != null:
				draw_set_transform(center, crank_rotation)
				draw_texture_rect(widget_mover, Rect2(-70.0, -70.0, 140.0, 140.0), false)
				draw_set_transform(Vector2.ZERO)
			if widget_overlay != null:
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false, Color(1.0, 1.0, 1.0, widget_fill))
		"trace":
			if widget_overlay != null:
				if completion_accepted or widget_fill >= 0.999:
					draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
				else:
					_draw_trace_patches(widget_overlay)
		"push":
			var mover_point := center + swipe_dir * widget_fill * 42.0
			_draw_widget_sprite(widget_mover, mover_point, 136.0)
			_draw_widget_sprite(widget_shared, center + swipe_dir * 92.0, 92.0, Color(1.0, 1.0, 1.0, 0.72))
		"target":
			for mark: Vector2 in tap_marks:
				_draw_widget_sprite(widget_stamp, mark, 76.0)
			if held:
				# the next piece rides the finger until it is placed
				_draw_widget_sprite(widget_mover, pointer_pos, 142.0)
			if widget_overlay != null and completion_accepted:
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
		"lanes":
			var show_answer := choice_flash > 0.0 or demo_active
			if show_answer and widget_mover != null:
				var lane_point := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), size.y * 0.70)
				var source := Rect2(float(target_choice) * 256.0, 0.0, 256.0, 256.0)
				draw_texture_rect_region(widget_mover, Rect2(lane_point - Vector2(62.0, 62.0), Vector2(124.0, 124.0)), source)
			if shuffle_t > 0.0 and shuffle_from >= 0:
				_draw_shuffle_glide(target_choice)
			if widget_shared != null and feedback_t > 0.0:
				_draw_widget_sprite(widget_shared, feedback_anchor, 82.0,
					Color.WHITE if feedback_positive else Color(1.0, 0.82, 0.92, 0.82))


func _draw_nursery_baby(texture_index: int, center: Vector2, extent: float) -> void:
	if nursery_textures.is_empty():
		draw_circle(center, extent * 0.30, Color("#ffd6bf"))
		return
	var texture: Texture2D = nursery_textures[posmod(texture_index, nursery_textures.size())]
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * extent * 0.5, Vector2.ONE * extent), false)


func _draw_nursery_context(center: Vector2) -> void:
	match visual_context:
		"nursery_wash":
			var basin := Rect2(center.x - 92.0, center.y - 12.0, 184.0, 82.0)
			draw_rect(basin, Color("#78cfd0"), true)
			draw_arc(Vector2(center.x, basin.position.y), 92.0, 0.0, PI, 32, Color("#ecfbf4"), 10.0)
			for index in range(7):
				var bubble := center + Vector2(-70.0 + float(index) * 23.0, -48.0 - float(index % 3) * 17.0)
				draw_circle(bubble, 9.0 + float(index % 2) * 4.0, Color(0.82, 0.97, 1.0, 0.62))
			draw_circle(center, 25.0 if held else 17.0, Color.WHITE)
			draw_arc(center, 58.0, 0.0, TAU, 40, accent, 9.0)
		"nursery_feed":
			for index in range(3):
				_draw_nursery_baby(index, Vector2(86.0 + float(index) * 100.0, center.y + 48.0), 88.0)
			var bottle_center := Vector2(center.x, center.y - 58.0)
			draw_rect(Rect2(bottle_center - Vector2(23, 38), Vector2(46, 76)), Color("#edf9ee"), true)
			draw_rect(Rect2(bottle_center - Vector2(17, 31), Vector2(34, 51)), Color("#ffe7ac"), true)
			draw_circle(bottle_center + Vector2(0, -44), 12.0, Color("#f1b1a1"))
			draw_arc(bottle_center, 61.0, 0.0, TAU, 40, accent, 9.0)
			draw_circle(bottle_center, 22.0 if held else 15.0, Color.WHITE)
		"nursery_burp":
			_draw_nursery_baby(1, Vector2(center.x, 70.0), 105.0)
			var hand := Vector2(center.x + 92.0, 78.0)
			draw_circle(hand, 28.0, Color("#ffd8bd"))
			draw_arc(hand, 45.0, -1.2, 1.2, 24, accent, 8.0)
			var bar := Rect2(size.x * 0.12, size.y - 82.0, size.x * 0.76, 42.0)
			draw_rect(bar, Color(0.20, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 22.0), Vector2(marker_x, bar.end.y + 22.0), Color.WHITE, 11.0)
		"nursery_bedtime":
			for index in range(3):
				var crib_center := Vector2(72.0 + float(index) * 114.0, center.y + 20.0)
				draw_rect(Rect2(crib_center - Vector2(48, 30), Vector2(96, 78)), Color("#f1d2c2"), true)
				_draw_nursery_baby(index, crib_center - Vector2(0, 10), 74.0)
				draw_rect(Rect2(crib_center.x - 43.0, crib_center.y + 7.0, 86.0, 37.0), Color(0.52, 0.81, 0.77, 0.94), true)
			for star in [Vector2(55, 44), Vector2(145, 30), Vector2(235, 50)]:
				draw_circle(star, 7.0, Color("#ffe483"))
			var arrow_x := size.x - 24.0
			draw_line(Vector2(arrow_x, 54.0), Vector2(arrow_x, size.y - 42.0), accent, 13.0, true)
			draw_colored_polygon(PackedVector2Array([
				Vector2(arrow_x - 28.0, size.y - 68.0), Vector2(arrow_x + 28.0, size.y - 68.0), Vector2(arrow_x, size.y - 28.0),
			]), accent)

func _draw_demo_finger() -> void:
	var center := size * 0.5
	var cycle := fmod(demo_t, 2.4)
	var pressing := cycle > 1.1
	var at := center
	match mode:
		"swipe":
			at = Vector2(lerpf(size.x * 0.22, size.x * 0.78, cycle / 2.4), center.y)
			pressing = true
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			at = center + Vector2.from_angle(-2.7 + cycle * 2.0) * radius
			pressing = true
		"choice":
			var lane := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), center.y)
			at = center.lerp(lane, clampf(cycle / 1.1, 0.0, 1.0))
		"timing":
			var bar_x := lerpf(size.x * 0.12, size.x * 0.88, timing_position)
			at = Vector2(bar_x, center.y + 58.0)
			pressing = timing_position >= timing_zone.x and timing_position <= timing_zone.y
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					var pos: Vector2 = target.get("pos", Vector2.ZERO)
					at = center.lerp(pos, clampf(cycle / 1.1, 0.0, 1.0))
					break
		"hold":
			pressing = true
	var halo := 30.0 if pressing else 20.0
	draw_circle(at, halo, Color(0.22, 0.14, 0.52, 0.18))
	draw_circle(at, 14.5, Color("#382485"))
	draw_circle(at, 12.0, Color(1.0, 0.98, 0.86, 0.98))
	if pressing:
		var ring := 18.0 + fmod(demo_t * 46.0, 26.0)
		draw_arc(at, ring, 0.0, TAU, 24, Color(1.0, 0.95, 0.6, 0.6), 4.0)


func _draw_imp(target: Dictionary) -> void:
	var pos: Vector2 = target.get("pos", Vector2.ZERO)
	var radius := float(target.get("r", 44.0))
	var captain := bool(target.get("captain", false))
	var texture := bop_captain_texture if captain else bop_texture
	if texture != null:
		var side := radius * 2.4
		draw_texture_rect(texture, Rect2(pos - Vector2(side, side) * 0.5, Vector2(side, side)), false)
		if captain:
			# plain gold band ring marks the captain over the costume sprite
			draw_arc(pos, radius * 1.16, 0.0, TAU, 36, Color("#e0b34c"), 6.0)
			if int(target.get("hp", 1)) > 1:
				draw_arc(pos, radius * 1.3, 0.0, TAU, 36, Color(1.0, 0.9, 0.5, 0.45), 4.0)
		return
	# basic place-in imp until the codex mischief-imp sprite set lands
	var body := Color("#7a4f9a") if not captain else Color("#5f3a85")
	var belly := Color("#b28ccd")
	draw_circle(pos, radius * 1.18, Color(1.0, 0.86, 0.4, 0.16))
	# curled striped horns
	for side_sign in [-1.0, 1.0]:
		var horn := pos + Vector2(side_sign * radius * 0.62, -radius * 0.78)
		draw_arc(horn, radius * 0.34, PI * 0.2, PI * 1.4, 12, Color("#e8d6a8"), 9.0)
		draw_arc(horn, radius * 0.34, PI * 0.5, PI * 1.1, 8, Color("#a8794f"), 9.0)
	# curled tail
	draw_arc(pos + Vector2(radius * 0.95, radius * 0.55), radius * 0.4, -PI * 0.6, PI * 0.7, 10, body.lightened(0.1), 8.0)
	draw_circle(pos, radius, body)
	draw_circle(pos + Vector2(0, radius * 0.3), radius * 0.55, belly)
	# amber eyes and a friendly fanged grin
	for side_sign in [-1.0, 1.0]:
		var eye := pos + Vector2(side_sign * radius * 0.34, -radius * 0.22)
		draw_circle(eye, radius * 0.17, Color("#f4b642"))
		draw_circle(eye, radius * 0.08, Color("#33203f"))
	draw_arc(pos + Vector2(0, radius * 0.1), radius * 0.34, 0.35, PI - 0.35, 12, Color("#33203f"), 5.0)
	for side_sign in [-1.0, 1.0]:
		var fang := pos + Vector2(side_sign * radius * 0.18, radius * 0.36)
		draw_colored_polygon(PackedVector2Array([
			fang + Vector2(-5, 0), fang + Vector2(5, 0), fang + Vector2(0, 10),
		]), Color.WHITE)
	if captain:
		# plain gold waistband marks the captain (no shell or crest motifs)
		draw_line(pos + Vector2(-radius * 0.8, radius * 0.62), pos + Vector2(radius * 0.8, radius * 0.62), Color("#e0b34c"), 8.0)
		if int(target.get("hp", 1)) > 1:
			draw_arc(pos, radius * 1.12, 0.0, TAU, 32, Color("#e0b34c"), 5.0)


func start_shuffle(from_lane: int) -> void:
	# magician TRACK: the fiction promises motion — show it. The answer glow
	# glides from the flashed lane to the true lane; a decoy arc crosses it.
	shuffle_from = clampi(from_lane, 0, choice_count - 1)
	shuffle_t = 1.5
	choice_flash = maxf(choice_flash, 2.2)
	queue_redraw()


func _lane_center(lane: int) -> Vector2:
	var lane_width := size.x / maxf(1.0, float(choice_count))
	return Vector2((float(lane) + 0.5) * lane_width, size.y * 0.55)


func _draw_shuffle_glide(target_lane: int) -> void:
	var t := clampf(1.0 - shuffle_t / 1.5, 0.0, 1.0)
	var eased := t * t * (3.0 - 2.0 * t)
	var from_point := _lane_center(shuffle_from)
	var to_point := _lane_center(target_lane)
	var main_point := from_point.lerp(to_point, eased)
	main_point.y -= sin(eased * PI) * 64.0
	var decoy_point := to_point.lerp(from_point, eased)
	decoy_point.y += sin(eased * PI) * 40.0
	draw_circle(decoy_point, 16.0, Color(1.0, 1.0, 1.0, 0.22))
	for i in range(4):
		var trail := clampf(eased - float(i) * 0.07, 0.0, 1.0)
		var trail_point := from_point.lerp(to_point, trail)
		trail_point.y -= sin(trail * PI) * 64.0
		draw_circle(trail_point, 20.0 - float(i) * 3.5, Color(accent, 0.85 - float(i) * 0.18))


func _draw_trace_patches(texture: Texture2D) -> void:
	# reveal the picture along the child's own finger path, patch by patch
	if trace_points.is_empty():
		return
	var texture_size := texture.get_size()
	var scale := Vector2(texture_size.x / maxf(1.0, size.x), texture_size.y / maxf(1.0, size.y))
	var patch := 96.0
	for point: Vector2 in trace_points:
		var destination := Rect2(point - Vector2(patch, patch) * 0.5, Vector2(patch, patch))
		var source := Rect2(destination.position * scale, destination.size * scale)
		draw_texture_rect_region(texture, destination, source)


func _draw_oven(_center: Vector2) -> void:
	# authored oven backdrop when present (gauge_chef ledger redirect);
	# a warm code-drawn oven face otherwise. NO green anywhere — the green
	# lock belongs to the retired ping-pong zones.
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	else:
		draw_rect(Rect2(size.x * 0.08, size.y * 0.08, size.x * 0.68, size.y * 0.84), Color("#8a5a4a"), true)
		draw_rect(Rect2(size.x * 0.08, size.y * 0.08, size.x * 0.68, size.y * 0.84), Color("#5c3a30"), false, 6.0)
	if completion_accepted:
		if widget_overlay != null:
			draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
			return
	# the window, and the cake tinting with the heat
	var window := Rect2(size.x * 0.16, size.y * 0.16, size.x * 0.52, size.y * 0.44)
	draw_rect(window, Color(0.23, 0.13, 0.10, 0.90), true)
	var heat := clampf(oven_t, 0.0, 1.0)
	var cake_color := Color("#f7ecd2").lerp(Color("#eab54e"), clampf(heat / 0.62, 0.0, 1.0))
	if heat > 0.80:
		cake_color = cake_color.lerp(Color("#9c6a30"), (heat - 0.80) * 5.0)
	var rise := 0.55 + 0.30 * heat
	var cake_base := Vector2(window.get_center().x, window.end.y - 10.0)
	var cake_width := window.size.x * 0.56
	var cake_height := window.size.y * 0.52 * rise
	var jiggle := 0.0
	if oven_peek > 0.0:
		jiggle = sin(oven_peek * 26.0) * 5.0
	if completion_accepted:
		jiggle = 0.0
	draw_rect(Rect2(cake_base.x - cake_width * 0.5 + jiggle, cake_base.y - cake_height, cake_width, cake_height), cake_color, true)
	draw_circle(Vector2(cake_base.x + jiggle, cake_base.y - cake_height), cake_width * 0.5, cake_color)
	# golden shimmer in the window during the ready band
	if heat >= 0.45 and heat <= 0.80:
		var shimmer := 0.30 + 0.20 * sin(heat * 90.0)
		draw_circle(Vector2(cake_base.x, cake_base.y - cake_height * 0.9), 10.0, Color(1.0, 0.92, 0.55, shimmer))
	# toasty steam curls — cozy, not alarming
	if heat > 0.80:
		for i in range(3):
			var sx := window.position.x + window.size.x * (0.28 + 0.22 * float(i))
			var sy := window.position.y + 14.0 - fmod(heat * 260.0 + float(i) * 23.0, 34.0)
			draw_arc(Vector2(sx, sy), 9.0, PI * 0.2, PI * 1.3, 12, Color(0.98, 0.92, 0.80, 0.5), 4.0)
	# the thermometer: rises bottom-to-top at the static rate, band-colored
	var slot := Rect2(size.x * 0.84, size.y * 0.12, 26.0, size.y * 0.64)
	draw_rect(slot, Color(0.98, 0.97, 0.93, 0.9), true)
	draw_rect(slot, Color("#5c3a30"), false, 4.0)
	var fill_height := slot.size.y * heat
	var band_color := Color("#f3dfa8") if heat < 0.45 else (Color("#ffc94d") if heat <= 0.80 else Color("#d9813c"))
	draw_rect(Rect2(slot.position.x, slot.end.y - fill_height, slot.size.x, fill_height), band_color, true)
	for band: float in [0.45, 0.80]:
		var tick_y: float = slot.end.y - slot.size.y * band
		draw_line(Vector2(slot.position.x - 6.0, tick_y), Vector2(slot.end.x + 6.0, tick_y), Color("#5c3a30"), 3.0)
	# the mitt handle — the ONE verb. It glows gold through the ready band.
	var handle := Rect2(size.x * 0.20, size.y * 0.66, size.x * 0.44, size.y * 0.15)
	var handle_center := handle.get_center()
	if oven_peek > 0.0:
		# the door swings open for the peek
		draw_rect(Rect2(handle.position.x, handle.position.y + 10.0, handle.size.x, handle.size.y), Color("#6e4638"), true)
	else:
		draw_rect(handle, Color("#6e4638"), true)
	draw_rect(handle, Color("#4a2c22"), false, 4.0)
	draw_circle(handle_center, 20.0, Color("#e8b24a"))
	if heat >= 0.45 and not oven_done:
		var pulse := 0.35 + 0.25 * (0.5 + 0.5 * sin(heat * 70.0))
		draw_arc(handle_center, 34.0 + 8.0 * pulse, 0.0, TAU, 40, Color(1.0, 0.83, 0.35, pulse), 7.0)


func _pipe_setup_round() -> void:
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	pipe_grid = []
	pipe_fixed = []
	for _cell in range(PIPE_COLS * PIPE_ROWS):
		pipe_grid.append("")
		pipe_fixed.append(false)
	var fixed: Dictionary = round_data.get("fixed", {})
	for cell: int in fixed.keys():
		pipe_grid[cell] = String(fixed[cell])
		pipe_fixed[cell] = true
	for cell: int in (round_data.get("imps", []) as Array):
		pipe_grid[cell] = "IMP"
		pipe_fixed[cell] = true
	pipe_tray = (round_data.get("tray", []) as Array).duplicate()
	pipe_tray_sel = -1
	pipe_drag_tile = ""
	pipe_drag_from = -1
	pipe_flow = []
	pipe_flow_t = 0.0
	pipe_wait_t = 0.0
	pipe_pause = 0.0
	queue_redraw()


func _pipe_cell_rect(cell: int) -> Rect2:
	var col := cell % PIPE_COLS
	var row := floori(float(cell) / float(PIPE_COLS))
	return Rect2(PIPE_ORIGIN + Vector2(float(col), float(row)) * PIPE_CELL, Vector2(PIPE_CELL, PIPE_CELL))


func _pipe_cell_at(point: Vector2) -> int:
	var local := point - PIPE_ORIGIN
	if local.x < 0.0 or local.y < 0.0:
		return -1
	var col := int(local.x / PIPE_CELL)
	var row := int(local.y / PIPE_CELL)
	if col >= PIPE_COLS or row >= PIPE_ROWS:
		return -1
	return row * PIPE_COLS + col


func _pipe_tray_rect(slot: int) -> Rect2:
	return Rect2(Vector2(120.0 + float(slot) * 104.0, PIPE_ORIGIN.y + PIPE_CELL * float(PIPE_ROWS) + 26.0), Vector2(92.0, 92.0))


func _pipe_flow_cells() -> Array:
	var cells: Array = []
	for step: Array in pipe_flow:
		cells.append(int(step[0]))
	return cells


func _pipe_next_step() -> Array:
	# [next_cell, in_dir] the fuel would advance into, or [] if blocked/done
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	var entry := int(round_data.get("entry", 4))
	if pipe_flow.is_empty():
		return [entry, Vector2i(1, 0)] if pipe_grid[entry] != "" else []
	var head: Array = pipe_flow[pipe_flow.size() - 1]
	var head_cell := int(head[0])
	var in_dir: Vector2i = head[1]
	var tile := String(pipe_grid[head_cell])
	if not PIPE_MOUTHS.has(tile):
		return []
	var out_dir := Vector2i.ZERO
	for mouth: Vector2i in (PIPE_MOUTHS[tile] as Array):
		if mouth != -in_dir:
			out_dir = mouth
	if head_cell == int(round_data.get("exit", 7)) and out_dir == (round_data.get("exit_dir", Vector2i(1, 0)) as Vector2i):
		return [-1, out_dir]
	var col := head_cell % PIPE_COLS + out_dir.x
	var row := floori(float(head_cell) / float(PIPE_COLS)) + out_dir.y
	if col < 0 or col >= PIPE_COLS or row < 0 or row >= PIPE_ROWS:
		return []
	var next_cell := row * PIPE_COLS + col
	var next_tile := String(pipe_grid[next_cell])
	if not PIPE_MOUTHS.has(next_tile):
		return []
	var accepts := false
	for mouth: Vector2i in (PIPE_MOUTHS[next_tile] as Array):
		if mouth == -out_dir:
			accepts = true
	return [next_cell, out_dir] if accepts else []


func _pipe_path_complete() -> bool:
	# would the fuel reach the exit if it kept flowing? (drives acceleration)
	var probe_flow := pipe_flow.duplicate(true)
	var original := pipe_flow
	pipe_flow = probe_flow
	var reached := false
	for _guard in range(PIPE_COLS * PIPE_ROWS + 2):
		var step := _pipe_next_step()
		if step.is_empty():
			break
		if int(step[0]) < 0:
			reached = true
			break
		pipe_flow.append(step)
	pipe_flow = original
	return reached


func _pipe_tick(delta: float) -> void:
	if pipe_pause > 0.0:
		pipe_pause = maxf(0.0, pipe_pause - delta)
		if pipe_pause <= 0.0 and pipe_round < PIPE_ROUNDS.size():
			_pipe_setup_round()
		queue_redraw()
		return
	pipe_flow_t += delta
	var step_time := 0.35 if _pipe_path_complete() else 1.2
	if pipe_flow_t >= step_time:
		pipe_flow_t = 0.0
		var step := _pipe_next_step()
		if step.is_empty():
			# the fuel WAITS at the last good pipe, bulging patiently
			pipe_wait_t += step_time
		elif int(step[0]) < 0:
			# reached the rocket! round done
			pipe_round += 1
			pipe_wait_t = 0.0
			gesture.emit("pipe", 1.0, 1.0)
			if pipe_round < PIPE_ROUNDS.size():
				pipe_pause = 1.0
		else:
			pipe_wait_t = 0.0
			pipe_flow.append(step)
	pipe_redraw += delta
	if pipe_redraw >= 0.06:
		pipe_redraw = 0.0
		queue_redraw()


func _pipe_press(at: Vector2) -> void:
	if completion_accepted:
		return
	for slot in range(pipe_tray.size()):
		if _pipe_tray_rect(slot).has_point(at):
			# lift from the tray (drag) and remember it (tap-then-tap)
			pipe_drag_tile = String(pipe_tray[slot])
			pipe_drag_from = -1
			pipe_tray_sel = slot
			queue_redraw()
			return
	var cell := _pipe_cell_at(at)
	if cell < 0:
		return
	var tile := String(pipe_grid[cell])
	if tile == "IMP":
		# giggle! he rolls over but keeps napping — route around him
		gesture.emit("pipe", 0.0, 0.6)
		queue_redraw()
		return
	var fueled := cell in _pipe_flow_cells()
	if PIPE_MOUTHS.has(tile) and not pipe_fixed[cell] and not fueled:
		# lift a placed pipe to slide it somewhere better
		pipe_drag_tile = tile
		pipe_drag_from = cell
		pipe_grid[cell] = ""
		pipe_tray_sel = -1
		queue_redraw()
		return
	if tile == "" and pipe_tray_sel >= 0 and pipe_tray_sel < pipe_tray.size():
		# tap-tile-then-tap-cell: place the remembered tray tile here
		pipe_grid[cell] = String(pipe_tray[pipe_tray_sel])
		pipe_tray.remove_at(pipe_tray_sel)
		pipe_tray_sel = -1
		pipe_wait_t = 0.0
		gesture.emit("pipe", 0.0, 1.0)
		queue_redraw()


func _pipe_release(at: Vector2) -> void:
	if pipe_drag_tile == "":
		return
	var cell := _pipe_cell_at(at)
	if cell >= 0 and String(pipe_grid[cell]) == "":
		pipe_grid[cell] = pipe_drag_tile
		pipe_wait_t = 0.0
		gesture.emit("pipe", 0.0, 1.0)
	elif pipe_drag_from >= 0 and String(pipe_grid[pipe_drag_from]) == "":
		pipe_grid[pipe_drag_from] = pipe_drag_tile
	else:
		pipe_tray.append(pipe_drag_tile)
	pipe_drag_tile = ""
	pipe_drag_from = -1
	pipe_tray_sel = -1
	queue_redraw()


func _pipe_hint_cell() -> int:
	# after 8s of waiting fuel, point at the cell the flow needs next
	if pipe_wait_t < 8.0:
		return -1
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	if pipe_flow.is_empty():
		return int(round_data.get("entry", 4))
	var head: Array = pipe_flow[pipe_flow.size() - 1]
	var head_cell := int(head[0])
	var in_dir: Vector2i = head[1]
	var tile := String(pipe_grid[head_cell])
	if not PIPE_MOUTHS.has(tile):
		return -1
	var out_dir := Vector2i.ZERO
	for mouth: Vector2i in (PIPE_MOUTHS[tile] as Array):
		if mouth != -in_dir:
			out_dir = mouth
	var col := head_cell % PIPE_COLS + out_dir.x
	var row := floori(float(head_cell) / float(PIPE_COLS)) + out_dir.y
	if col < 0 or col >= PIPE_COLS or row < 0 or row >= PIPE_ROWS:
		return -1
	return row * PIPE_COLS + col


func _draw_pipe_tile(rect: Rect2, tile: String, fueled: bool) -> void:
	if pipe_tiles.has(tile):
		# authored tile: the art owns the look; fuel is a teal wash inside it
		draw_texture_rect(pipe_tiles[tile] as Texture2D, rect.grow(-6.0), false)
		if fueled:
			draw_texture_rect(pipe_tiles[tile] as Texture2D, rect.grow(-6.0), false,
				Color(0.37, 0.85, 0.81, 0.55))
		return
	var body := rect.grow(-10.0)
	draw_rect(body, Color("#caa269") if not fueled else Color("#d8b87e"), true)
	draw_rect(body, Color("#7a5a34"), false, 4.0)
	var center := rect.get_center()
	var bore := 26.0
	var fuel := Color("#5fd8cf")
	var glass := Color("#2e4a52")
	for mouth: Vector2i in (PIPE_MOUTHS.get(tile, []) as Array):
		var arm_end := center + Vector2(float(mouth.x), float(mouth.y)) * (rect.size.x * 0.5 - 8.0)
		draw_line(center, arm_end, glass, bore)
		if fueled:
			draw_line(center, arm_end, fuel, bore - 10.0)
		# open dark mouths: wordless orientation cues
		draw_circle(arm_end, bore * 0.42, Color(0.12, 0.10, 0.10, 0.95))
	draw_circle(center, bore * 0.62, glass)
	if fueled:
		draw_circle(center, bore * 0.40, fuel)


func _draw_pipe() -> void:
	var round_data: Dictionary = PIPE_ROUNDS[clampi(pipe_round, 0, PIPE_ROUNDS.size() - 1)]
	var flow_cells := _pipe_flow_cells()
	var hint := _pipe_hint_cell()
	# grid plates
	for cell in range(PIPE_COLS * PIPE_ROWS):
		var rect := _pipe_cell_rect(cell)
		draw_rect(rect.grow(-4.0), Color(0.16, 0.22, 0.34, 0.55), true)
		draw_rect(rect.grow(-4.0), Color(0.55, 0.66, 0.86, 0.5), false, 2.0)
		var tile := String(pipe_grid[cell])
		if tile == "IMP":
			# a napping mischief imp: he giggles if tapped, but stays
			var imp_center := rect.get_center()
			draw_circle(imp_center + Vector2(0, 12.0), 30.0, Color("#8d6bc8"))
			draw_circle(imp_center + Vector2(0, -16.0), 20.0, Color("#a186d6"))
			for z in range(2):
				draw_circle(imp_center + Vector2(26.0 + float(z) * 14.0, -30.0 - float(z) * 12.0), 4.0 + float(z) * 2.0, Color(1, 1, 1, 0.7))
		elif PIPE_MOUTHS.has(tile):
			_draw_pipe_tile(rect, tile, cell in flow_cells)
		if cell == hint:
			# Mewsha's stand-in twinkle: the kind nudge, never a demand
			var pulse := 0.5 + 0.4 * sin(pipe_wait_t * 5.0)
			draw_arc(rect.get_center(), 44.0, 0.0, TAU, 32, Color(1.0, 0.85, 0.35, pulse), 6.0)
	# fuel bulge where the flow waits
	if pipe_wait_t > 0.5 and not pipe_flow.is_empty():
		var head_rect := _pipe_cell_rect(int((pipe_flow[pipe_flow.size() - 1] as Array)[0]))
		var bulge := 6.0 + 3.0 * sin(pipe_wait_t * 6.0)
		draw_circle(head_rect.get_center(), 18.0 + bulge, Color(0.37, 0.85, 0.81, 0.55))
	# tank (entry) and rocket (exit) stubs outside the grid
	var entry_rect := _pipe_cell_rect(int(round_data.get("entry", 4)))
	var tank_center := Vector2(PIPE_ORIGIN.x - 62.0, entry_rect.get_center().y)
	if pipe_tank_texture != null:
		draw_texture_rect(pipe_tank_texture, Rect2(tank_center - Vector2(58.0, 58.0), Vector2(116.0, 116.0)), false)
	else:
		draw_circle(tank_center, 46.0, Color("#3f6f8a"))
		draw_circle(tank_center, 34.0, Color("#5fd8cf"))
	draw_rect(Rect2(tank_center.x + 34.0, tank_center.y - 13.0, PIPE_ORIGIN.x - tank_center.x - 34.0 + 6.0, 26.0), Color("#7a5a34"), true)
	var exit_cell := int(round_data.get("exit", 7))
	var exit_dir: Vector2i = round_data.get("exit_dir", Vector2i(1, 0))
	var exit_rect := _pipe_cell_rect(exit_cell)
	var rocket_center := exit_rect.get_center() + Vector2(float(exit_dir.x), float(exit_dir.y)) * (PIPE_CELL * 0.5 + 58.0)
	if pipe_intake_texture != null:
		draw_texture_rect(pipe_intake_texture, Rect2(rocket_center - Vector2(56.0, 56.0), Vector2(112.0, 112.0)), false)
	else:
		draw_circle(rocket_center, 44.0, Color("#c8cede"))
		draw_circle(rocket_center, 30.0, Color("#8090b0"))
	var round_done := pipe_round >= PIPE_ROUNDS.size() or pipe_pause > 0.0
	if round_done:
		draw_circle(rocket_center, 20.0, Color("#5fd8cf"))
		for ring in range(3):
			draw_arc(rocket_center, 52.0 + float(ring) * 16.0, 0.0, TAU, 32, Color(1.0, 0.9, 0.5, 0.5 - float(ring) * 0.13), 5.0)
	# the tray
	for slot in range(pipe_tray.size()):
		var tray_rect := _pipe_tray_rect(slot)
		draw_rect(tray_rect, Color(0.92, 0.95, 1.0, 0.9), true)
		draw_rect(tray_rect, Color("#7a5a34") if slot != pipe_tray_sel else Color("#ffcf4d"), false, 4.0 if slot != pipe_tray_sel else 6.0)
		_draw_pipe_tile(tray_rect, String(pipe_tray[slot]), false)
	# the tile riding the finger
	if pipe_drag_tile != "":
		_draw_pipe_tile(Rect2(pointer_pos - Vector2(PIPE_CELL, PIPE_CELL) * 0.5, Vector2(PIPE_CELL, PIPE_CELL)), pipe_drag_tile, false)


func _echo_star_center(star: int) -> Vector2:
	return Vector2(size.x * (0.22 + 0.28 * float(star)), size.y * 0.52)


func _echo_tick(delta: float) -> void:
	echo_glow = maxf(0.0, echo_glow - delta)
	if echo_listening:
		return
	# SHOW: the stars sing their verse one by one; then it is her turn
	echo_show_t -= delta
	if echo_show_t <= 0.0:
		var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
		echo_show_i += 1
		if echo_show_i >= verse.size():
			echo_listening = true
			echo_input_i = 0
		else:
			echo_last_note = int(verse[echo_show_i])
			echo_glow = 0.45
			gesture.emit("echo_note", 0.0, 1.0)
			echo_show_t = 0.55
	queue_redraw()


func _echo_press(at: Vector2) -> void:
	if completion_accepted:
		return
	var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
	for star in range(3):
		if at.distance_to(_echo_star_center(star)) <= 74.0:
			if not echo_listening:
				# eager taps during the song just twinkle — no punishment
				echo_last_note = star
				gesture.emit("echo_note", 0.0, 0.8)
				return
			if star == int(verse[echo_input_i]):
				echo_last_note = star
				echo_glow = 0.45
				gesture.emit("echo_note", 0.0, 1.0)
				echo_input_i += 1
				if echo_input_i >= verse.size():
					# verse sung back! the song grows by one verse
					echo_verse += 1
					echo_listening = false
					echo_show_i = -1
					echo_show_t = 0.7
					gesture.emit("echo", 1.0, 1.0)
			else:
				# kind replay: the stars sing the verse again
				echo_last_note = star
				gesture.emit("echo", _miss_pay(), 0.4)
				echo_listening = false
				echo_show_i = -1
				echo_show_t = 0.9
			queue_redraw()
			return
	gesture.emit("echo", 0.0, 0.6)


func _draw_echo_star(center: Vector2, radius: float, color: Color) -> void:
	var art: Texture2D = echo_lit_texture if color.r > 0.9 and color.g > 0.7 else echo_unlit_texture
	if art != null:
		draw_texture_rect(art, Rect2(center - Vector2.ONE * radius, Vector2.ONE * radius * 2.0), false, color)
		return
	var points := PackedVector2Array()
	for i in range(10):
		var r := radius if i % 2 == 0 else radius * 0.45
		var a := -PI * 0.5 + TAU * float(i) / 10.0
		points.append(center + Vector2(cos(a), sin(a)) * r)
	draw_polygon(points, PackedColorArray([color]))


func _draw_echo(_center: Vector2) -> void:
	var verse: Array = ECHO_VERSES[clampi(echo_verse, 0, ECHO_VERSES.size() - 1)]
	var showing := -1 if echo_listening or echo_show_i < 0 or echo_show_i >= verse.size() else int(verse[echo_show_i])
	for star in range(3):
		var star_center := _echo_star_center(star)
		var lit := star == showing or (star == echo_last_note and echo_glow > 0.0)
		var base := Color("#ffd75e") if lit else Color(0.72, 0.62, 0.92, 0.85)
		_draw_echo_star(star_center, 64.0 if lit else 54.0, base)
		if lit:
			draw_arc(star_center, 78.0, 0.0, TAU, 36, Color(1.0, 0.9, 0.5, 0.55), 6.0)
	# the assembled song: one small lit star per verse already sung
	for done in range(clampi(echo_verse, 0, ECHO_VERSES.size())):
		_draw_echo_star(Vector2(size.x * (0.38 + 0.12 * float(done)), size.y * 0.14), 18.0, Color("#ffd75e"))
	if echo_listening:
		# her turn: a soft ring invites the next star in the verse
		var next_center := _echo_star_center(int(verse[clampi(echo_input_i, 0, verse.size() - 1)]))
		draw_arc(next_center, 88.0, 0.0, TAU, 36, Color(accent, 0.35), 5.0)


func _pour_pitcher_rect() -> Rect2:
	return Rect2(pour_x - 70.0, size.y * 0.10, 140.0, 120.0)


func _pour_bowl_rect() -> Rect2:
	return Rect2(size.x * 0.20, size.y * 0.62, size.x * 0.60, size.y * 0.30)


func _pour_tick(delta: float) -> void:
	var want := 1.0 if pour_hold else 0.0
	var rate := delta / 0.8 if pour_hold else delta / 0.35
	pour_tilt = move_toward(pour_tilt, want, rate)
	var stream := pour_tilt > 0.36
	if stream:
		var spout_x := pour_x + 52.0 + 26.0 * pour_tilt
		var bowl := _pour_bowl_rect()
		var on_target := spout_x >= bowl.position.x and spout_x <= bowl.end.x
		var flow := maxf(pour_reserve, 0.12) / 1.2
		if on_target and pour_level < 1.0:
			var fill := (pour_tilt - 0.36) / 0.64 * delta / 4.6 * flow
			pour_level = minf(1.0, pour_level + fill)
			pour_reserve = maxf(0.0, pour_reserve - fill)
			# the child controls the pour, not a clock: progress IS the fill
			pour_emit_acc += fill
			if pour_emit_acc >= 0.04 or pour_level >= 1.0:
				gesture.emit("pourt", pour_emit_acc * 5.0, 1.0)
				pour_emit_acc = 0.0
			if pour_level >= 1.0:
				# brim! the pitcher politely rights itself with a ring
				pour_hold = false
				gesture.emit("pour_ding", 0.0, 1.0)
	pour_redraw += delta
	if pour_redraw >= 0.05:
		pour_redraw = 0.0
		queue_redraw()


func _draw_pour_scene(_center: Vector2) -> void:
	if widget_backdrop != null:
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
	var bowl := _pour_bowl_rect()
	# the bowl and its rising batter (authored fill strip when present)
	if widget_overlay != null:
		_draw_progress_overlay(widget_overlay, pour_level, false)
	else:
		draw_rect(bowl, Color(0.90, 0.94, 1.0, 0.55), true)
		var level_height := bowl.size.y * 0.8 * pour_level
		var surface_y := bowl.end.y - 8.0 - level_height
		var wobble := sin(pour_tilt * 20.0 + pour_level * 30.0) * 2.0
		draw_rect(Rect2(bowl.position.x + 8.0, surface_y + wobble, bowl.size.x - 16.0, level_height), Color("#f2c66d"), true)
	draw_rect(bowl, Color("#7a5a34"), false, 5.0)
	# the pitcher: tilts in the hand, visibly drains as it pours
	var pitcher := _pour_pitcher_rect()
	var pitcher_center := pitcher.get_center()
	draw_set_transform(pitcher_center, pour_tilt * 1.05)
	if widget_mover != null:
		draw_texture_rect(widget_mover, Rect2(-pitcher.size * 0.5, pitcher.size), false)
	else:
		draw_rect(Rect2(-pitcher.size * 0.5, pitcher.size), Color("#8fb4d8"), true)
		var content_height := pitcher.size.y * 0.7 * (pour_reserve / 1.2)
		draw_rect(Rect2(-pitcher.size.x * 0.36, pitcher.size.y * 0.42 - content_height, pitcher.size.x * 0.72, content_height), Color("#f2c66d"), true)
		draw_rect(Rect2(-pitcher.size * 0.5, pitcher.size), Color("#4a5a7a"), false, 4.0)
	draw_set_transform(Vector2.ZERO)
	# the stream: it follows the spout, thick with the tilt, and lands
	if pour_tilt > 0.36 and pour_level < 1.0:
		var spout := Vector2(pour_x + 52.0 + 26.0 * pour_tilt, pitcher.position.y + 58.0 + 30.0 * pour_tilt)
		var landing := Vector2(spout.x + 10.0, bowl.position.y + 16.0)
		var thickness := 5.0 + 9.0 * (pour_tilt - 0.36) / 0.64
		var mid := Vector2(lerpf(spout.x, landing.x, 0.5) + 6.0, lerpf(spout.y, landing.y, 0.5))
		draw_line(spout, mid, Color("#f2c66d"), thickness)
		draw_line(mid, landing, Color("#f2c66d"), thickness * 0.9)
		for blip in range(3):
			var blip_t := fmod(pour_tilt * 8.0 + float(blip) * 0.33, 1.0)
			draw_circle(spout.lerp(landing, blip_t) + Vector2(4.0, 0.0), 4.0, Color("#f7dfa0"))
		# a bulge where the stream lands
		draw_circle(landing, thickness * 0.9, Color(0.95, 0.80, 0.45, 0.7))
	# near-empty: fat last drips
	if pour_reserve < 0.18 and pour_tilt > 0.36:
		draw_circle(Vector2(pour_x + 58.0, pitcher.end.y + 14.0), 6.0, Color("#f2c66d"))
