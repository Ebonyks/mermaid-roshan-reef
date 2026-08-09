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
	if main.intro_active:
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
	# stand under him during a window and land one real tap
	await _pump_until("vuln", 0.0, -1.0, 900)
	var r: Node3D = main.g.get("oc_root") as Node3D
	if r != null:
		main.player.position = r.position + Vector3(float(main.g.get("db_x", 0.0)), 3.0,
			float(main.g.get("db_z", 0.0)))
	var hits: int = int(main.g.get("db_hits", 0))
	var n := 0
	while n < 200 and main.g.has("db_state") and int(main.g.get("db_hits", 0)) == hits:
		main.touch_ui.action_down = (n % 4) < 2
		boss.tick(DT, main.dust_boss_fr, main.player.position)
		n += 1
		await process_frame
	main.touch_ui.action_down = false
	await _pump(6)

func _shot(shot_name: String) -> void:
	await _settle(2)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	shot_i += 1
	var err: Error = image.save_png(out_dir.path_join(shot_name + ".png"))
	print("DUSTSHOT|", shot_name, "|state=", String(main.g.get("db_state", "-")),
		"|hits=", int(main.g.get("db_hits", 0)), "|", "OK" if err == OK else "not saved")
