extends SceneTree
# Visual review capture for the Dust Bunny Boss arena — the dimension the
# persona playtest (scripts/probe_dust_boss_balance.gd) is blind to: what the
# encounter actually LOOKS like on the phone, state by state.
#
# It drives the real encounter (main's own tick is parked, this file owns the
# clock) and captures one frame per beat through the game's own camera, at the
# 1280x720 base canvas under the mobile renderer. Display-only: no assertions,
# no gate tokens. Set DUSTBOSS_SHOT_OUT to choose the output folder.
#
# Run: xvfb-run -a godot --rendering-method mobile -s scripts/probe_dust_boss_shots.gd

const DT := 0.05

var main: ReefMain
var boss: DustBossGame
var out_dir := ""
var shot_i := 0

func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("DUSTSHOT|HEADLESS SKIP (needs a real viewport; run under xvfb)")
		quit()
		return
	var requested: String = OS.get_environment("DUSTBOSS_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path("res://tmp/dust_boss_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	# The real encounter is reached after the launch menu has been dismissed.
	# Mirror that seam before capture: a native desktop tooltip can otherwise
	# outlive its covered button and contaminate an otherwise opaque review card.
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
	elif main.intro_active:
		main._skip_intro()
	await _settle(20)
	boss = main._game_obj("dustboss", DustBossGame) as DustBossGame
	main.dust_boss_cool = 0.0
	main.game = ""
	main._start_game_now(main.dust_boss_fr)
	await _settle(4)
	# This file owns the clock, so main must not tick the encounter as well.
	# Stop MAIN's _process — do NOT rename main.game: player.gd yields the
	# camera by game id, so a sentinel id silently hands the lens back to the
	# free-swim chase cam and every capture comes out framed on nothing.
	main.set_process(false)
	# 0. the reusable splash language: signature action, grin, live tell
	await _shot("00a_splash_jump")
	await _wait_for_splash_beat("grin", 300)
	await _shot("00b_splash_grin")
	await _wait_for_splash_beat("flash", 300)
	await _shot("00c_splash_vulnerability_flash")
	# 1. the showing, mid-rise and on its demo flash
	await _pump_until("showing", 0.0, 1.4, 400)
	await _shot("01_showing_rise")
	await _pump_until_flash(400)
	await _shot("02_showing_demo_flash")
	# 2. the shielded prowl — mid-hop, star dim
	await _pump_until("prowl", 1.5, -1.0, 600)
	await _shot("03_prowl_hop_shielded")
	# 3. the wind-up telegraph
	await _pump_until("windup", 0.0, -1.0, 600)
	await _shot("04_windup_glimmer")
	# 4. THE WINDOW — airborne, star strobing, pointer up
	await _pump_until("vuln", 6.0, -1.0, 600)
	await _shot("05_window_open")
	# 5. the bonk and the dizzy phase
	await _strike()
	await _shot("06_struck_dizzy")
	await _pump_until("prowl", 0.0, -1.0, 600)
	await _shot("07_dizzy_prowl")
	# 6. angry
	await _strike()
	await _pump_until("prowl", 0.0, -1.0, 900)
	await _shot("08_angry_prowl")
	await _pump_until("vuln", 6.0, -1.0, 900)
	await _shot("09_angry_window")
	# 7. the befriending
	await _strike()
	await _shot("10_friends")
	await _pump(220)
	await _wait_for_day_two(300)
	await _wait_for_day_two_beat("open", 300)
	await _shot("11_day_two_begins")
	print("DUSTSHOT|DONE|", out_dir)
	quit()

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _pump(n: int) -> void:
	for i in range(n):
		if not main.g.has("db_state"):
			return
		boss.tick(DT, main.dust_boss_fr, main.player.position)
		await process_frame


func _wait_for_splash_beat(want: String, cap: int) -> void:
	var n := 0
	while n < cap and main.g.has("db_state"):
		var splash: BossSplash2D = main.g.get("db_splash") as BossSplash2D
		if splash != null and is_instance_valid(splash) \
				and splash.current_beat() == want:
			return
		n += 1
		await process_frame


func _wait_for_day_two(cap: int) -> void:
	var n := 0
	while n < cap and not main.day_two_transition_active:
		n += 1
		await process_frame
	# A prior visual run may have persisted the one-time Day Two unlock. The
	# production seam correctly stays idempotent on rematch; this display-only
	# probe still needs a repeatable way to review the overlay itself.
	if not main.day_two_transition_active:
		main._show_day_two_transition()
		await process_frame


func _wait_for_day_two_beat(want: String, cap: int) -> void:
	var n := 0
	var transition: DayTwoTransition2D = \
		main.day_two_transition_layer as DayTwoTransition2D
	if transition != null and is_instance_valid(transition):
		# Review the same authored instant on every machine. Production remains
		# delta-driven; only this visual harness takes ownership of its clock.
		transition.set_process(false)
	while n < cap and main.day_two_transition_active:
		if transition != null and is_instance_valid(transition) \
				and transition.current_beat() == want:
			return
		if transition != null and is_instance_valid(transition):
			transition._process(DT)
		n += 1
		await process_frame

func _pump_until(want: String, min_y: float, min_st: float, cap: int) -> void:
	# pump the encounter until it reaches `want` (and optionally is at least
	# min_y off the floor / min_st seconds into the state)
	var n := 0
	while n < cap and main.g.has("db_state"):
		var ok: bool = String(main.g.get("db_state", "")) == want \
			and float(main.g.get("db_y", 0.0)) >= min_y \
			and float(main.g.get("db_st", 0.0)) >= min_st
		if ok:
			return
		boss.tick(DT, main.dust_boss_fr, main.player.position)
		n += 1
		await process_frame

func _pump_until_flash(cap: int) -> void:
	var n := 0
	while n < cap and main.g.has("db_state"):
		if float(main.g.get("db_flash", 0.0)) >= 0.99:
			return
		boss.tick(DT, main.dust_boss_fr, main.player.position)
		n += 1
		await process_frame

func _strike() -> void:
	# Stand under him and wait for the animation kit's real vulnerability bit.
	# A state-name-only driver can arrive before frame two opens the tell and
	# miss the short window on slower renderers, producing a misleading review.
	var wanted_hits: int = int(main.g.get("db_hits", 0)) + 1
	for attempt: int in range(5):
		if not main.g.has("db_state") \
				or int(main.g.get("db_hits", 0)) >= wanted_hits:
			break
		await _pump_until("vuln", 0.0, -1.0, 900)
		var open_wait := 0
		while open_wait < 80 and main.g.has("db_state") \
				and String(main.g.get("db_state", "")) == "vuln":
			var kit: DustBunnyBossSprite = main.g.get("db_kit") as DustBunnyBossSprite
			if kit != null and is_instance_valid(kit) and kit.vulnerable:
				break
			boss.tick(DT, main.dust_boss_fr, main.player.position)
			open_wait += 1
			await process_frame
		var r: Node3D = main.g.get("oc_root") as Node3D
		if r != null:
			main.player.position = r.position + Vector3(
				float(main.g.get("db_x", 0.0)), 3.0,
				float(main.g.get("db_z", 0.0)))
		var n := 0
		while n < 200 and main.g.has("db_state") \
				and int(main.g.get("db_hits", 0)) < wanted_hits \
				and String(main.g.get("db_state", "")) == "vuln":
			main.touch_ui.action_down = (n % 2) == 0
			boss.tick(DT, main.dust_boss_fr, main.player.position)
			n += 1
			await process_frame
	main.touch_ui.action_down = false
	await _pump(6)

func _shot(shot_name: String) -> void:
	await _settle(2)
	if shot_name == "11_day_two_begins" and main.day_two_transition_active:
		var transition: DayTwoTransition2D = \
			main.day_two_transition_layer as DayTwoTransition2D
		if transition != null and is_instance_valid(transition):
			var title: Control = transition.get_node_or_null(
				"DayTwoTransitionRoot/DayTwoTransitionStage/DayTwoTitleCard") as Control
			var castle: Control = transition.get_node_or_null(
				"DayTwoTransitionRoot/DayTwoTransitionStage/DayTwoCastle") as Control
			if title != null and castle != null:
				print("DUSTSHOT|DAY2_XFORM|beat=", transition.current_beat(),
					"|title_pos=", title.position, "|title_scale=", title.scale,
					"|castle_pos=", castle.position, "|castle_size=", castle.size,
					"|castle_scale=", castle.scale)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	shot_i += 1
	var err: Error = image.save_png(out_dir.path_join(shot_name + ".png"))
	print("DUSTSHOT|", shot_name, "|state=", String(main.g.get("db_state", "-")),
		"|hits=", int(main.g.get("db_hits", 0)), "|", "OK" if err == OK else "not saved")
