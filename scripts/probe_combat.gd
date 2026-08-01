extends SceneTree
# Shared combat-engine probe: both arenas require input, resolve their bespoke
# enemy states, save completion, and return control without a fail state.

const DADDY_IDLE: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_idle.png")
const DADDY_VICTORY: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_victory.png")

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260714)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _ice_case()
	await _fire_case()
	print("COMBAT|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("COMBAT|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _check_daddy_ready(prefix: String, arena: CombatArena) -> void:
	var sprite: Sprite3D = arena.daddy_victory_sprite
	var animator: DaddySpriteLoop = arena.daddy_victory_animator
	_ck(prefix + " Daddy cameo is prebuilt and hidden",
		sprite != null and animator != null and not sprite.visible
		and sprite.texture == DADDY_IDLE
		and animator.animation_state() == "idle")

func _check_daddy_victory(prefix: String, arena: CombatArena) -> void:
	var sprite: Sprite3D = arena.daddy_victory_sprite
	var animator: DaddySpriteLoop = arena.daddy_victory_animator
	_ck(prefix + " Daddy victory action is visible",
		sprite != null and animator != null and sprite.visible
		and sprite.texture == DADDY_VICTORY
		and animator.animation_state() == "victory")
	if sprite == null:
		return
	var first_frame: int = sprite.frame
	var advanced := false
	for i in range(6):
		await process_frame
		if is_instance_valid(sprite) and sprite.frame != first_frame:
			advanced = true
			break
	_ck(prefix + " Daddy victory atlas advances", advanced)

func _ice_case() -> void:
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("ice arena starts with eight surrounding imps", arena != null and arena.enemies.size() == 8)
	_check_daddy_ready("ice", arena)
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	for i in range(30):
		await process_frame
	_ck("ice battle cannot win passively", arena.state == "play" and not main.combat_ice_done)
	for enemy: Dictionary in arena.enemies:
		arena._freeze_imp(enemy)
		enemy["timer"] = 0.0
	await process_frame
	await process_frame
	_ck("frozen imps melt into popcorn", arena.state == "won")
	await _check_daddy_victory("ice", arena)
	arena.win_t = 0.0
	await process_frame
	await process_frame
	_ck("ice completion saves", main.combat_ice_done)

func _fire_case() -> void:
	# Fire combat is entered from the live Pearl Castle hall. Build that source
	# state instead of only labelling an empty probe dictionary as "level2": the
	# main loop resumes the owning arena on the same frame the combat child exits.
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_combat("fire")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("pepper boss arena builds", arena != null and not arena.boss.is_empty())
	_check_daddy_ready("fire", arena)
	var hp_before: int = int(arena.boss["hp"])
	arena.boss["phase"] = "shell"
	arena._hit_boss()
	_ck("spiky shell blocks fire", int(arena.boss["hp"]) == hp_before)
	arena.boss["phase"] = "peek"
	for i in range(hp_before):
		arena._hit_boss()
	_ck("pepper fire tames boss", arena.state == "won")
	await _check_daddy_victory("fire", arena)
	arena.win_t = 0.0
	await process_frame
	await process_frame
	_ck("fire completion saves and returns", main.combat_fire_done and main.game == "level2")
