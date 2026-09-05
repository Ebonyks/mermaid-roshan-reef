extends SceneTree
## Reproducible input personas against the live encounter and animation clocks.
## These are simulation results, not evidence of a child's enjoyment/comprehension.

const PERSONAS: Array[Dictionary] = [
	{"name": "attentive", "reaction": 0.45, "speed": 0.85, "counter": 0.6},
	{"name": "learning", "reaction": 1.15, "speed": 0.65, "counter": 1.2},
	{"name": "slow", "reaction": 2.0, "speed": 0.4, "counter": 2.4},
	{"name": "slow_counter", "reaction": 1.0, "speed": 0.6, "counter": 4.0},
	{"name": "moving_masher", "reaction": 0.9, "speed": 0.7, "counter": 0.0, "mash": true},
]
const CONTROLS: Array[Dictionary] = [
	{"name": "idle", "reaction": 0.0, "speed": 0.0, "counter": 0.0, "never_tap": true},
	{"name": "stationary_masher", "reaction": 0.0, "speed": 0.0, "counter": 0.0, "mash": true},
	{"name": "held_action", "reaction": 0.0, "speed": 0.0, "counter": 0.0, "held": true},
	{"name": "movement_only", "reaction": 0.6, "speed": 0.8, "counter": 0.0, "never_tap": true},
]
const CAP: float = 150.0
var main: ReefMain
var boss: DustBossGame
var failures: int = 0

func _init() -> void:
	Engine.time_scale = 3.0
	Engine.max_fps = 120
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	boss = main._game_obj("dustboss", DustBossGame) as DustBossGame
	var controls: bool = "--controls" in OS.get_cmdline_user_args()
	var roster: Array[Dictionary] = CONTROLS if controls else PERSONAS
	print("DUSTBAL|schema persona,seconds,rounds,damage,avoids,opening_misses,taps,result")
	for persona: Dictionary in roster:
		await _play(persona, controls)
	print("DUSTBAL|result: ", "ALL OK" if failures == 0 else "%d FAILED" % failures)
	quit(1 if failures > 0 else 0)

func _play(persona: Dictionary, negative: bool) -> void:
	if main.game != "":
		main._clear_game()
	main.game = ""
	main.save_data["dustboss_pending_rounds"] = 0
	main.save_data["dustboss_pending_damage"] = 0
	main.save_data["dustboss_pending_misses"] = 0
	main._start_game_now(main.dust_boss_fr)
	var elapsed: float = 0.0
	var open_elapsed: float = 0.0
	var previous_state: String = ""
	var was_open: bool = false
	var tapped_open: bool = false
	var taps: int = 0
	var hits: int = 0
	var damage: int = 0
	var avoids: int = 0
	var misses: int = 0
	var mash_frame: int = 0
	while main.game == "dustboss" and elapsed < (60.0 if negative else CAP):
		var delta: float = maxf(0.001, main.get_process_delta_time())
		var state: String = String(main.g.get("db_state", ""))
		var k: DustBunnyBossSprite = boss.kit()
		var open_now: bool = state == "vuln" and k != null and k.vulnerable
		if open_now:
			open_elapsed = open_elapsed + delta if was_open else 0.0
		else:
			open_elapsed = 0.0
			if state != "vuln":
				tapped_open = false
		was_open = open_now
		main.touch_ui.stick_vec = Vector2.ZERO
		if state in ["tell", "strike"] and float(persona["speed"]) > 0.0:
			var geometry: Dictionary = boss.danger_geometry()
			var tell_elapsed: float = float(geometry.get("tell_elapsed", 0.0))
			if state == "strike":
				tell_elapsed += float(main.g.get("db_st", 0.0))
			if tell_elapsed >= float(persona["reaction"]):
				var safe: Vector2 = geometry.get("safe_point", Vector2.ZERO) as Vector2
				var offset: Vector2 = safe - boss.stage.player_local()
				main.touch_ui.stick_vec = (offset / (24.0 * delta)).limit_length(float(persona["speed"]))
		main.touch_ui.action_down = false
		if bool(persona.get("held", false)):
			main.touch_ui.action_down = true
		elif not bool(persona.get("never_tap", false)):
			if bool(persona.get("mash", false)):
				mash_frame += 1
				main.touch_ui.action_down = mash_frame % 6 == 0
			elif open_now and not tapped_open and open_elapsed >= float(persona["counter"]):
				main.touch_ui.action_down = true
				tapped_open = true
		if main.touch_ui.action_down and not bool(persona.get("held", false)):
			taps += 1
		hits = maxi(hits, int(main.g.get("db_hits", 0)))
		damage = maxi(damage, int(main.g.get("db_damage_taken", 0)))
		avoids = maxi(avoids, int(main.g.get("db_avoids", 0)))
		misses = maxi(misses, int(main.g.get("db_opening_misses", 0)))
		previous_state = state
		await process_frame
		elapsed += delta
	var ok: bool = hits == 0 if negative else hits == 3 and main.game != "dustboss"
	if not ok:
		failures += 1
	print("DUSTBAL|%s,%.2f,%d,%d,%d,%d,%d,%s" % [
		String(persona["name"]), elapsed, hits, damage, avoids, misses, taps,
		"OK" if ok else "FAIL:" + previous_state])
	main.touch_ui.action_down = false
	main.touch_ui.stick_vec = Vector2.ZERO
	if main.game == "dustboss":
		main._clear_game()
	main.game = ""
	await process_frame
