extends SceneTree
# Shared combat-engine probe: both arenas require input, resolve their bespoke
# enemy states, save completion, and return control without a fail state.
const DADDY_IDLE: Texture2D = preload("res://assets/characters/daddy_25d/daddy_idle.png")
const DADDY_VICTORY: Texture2D = preload("res://assets/characters/daddy_25d/daddy_victory.png")

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

func _check_daddy_prebuilt(label: String, arena: CombatArena) -> void:
	_ck(label + " Daddy victory cameo is prebuilt", arena != null \
		and arena.daddy_victory_sprite != null \
		and is_instance_valid(arena.daddy_victory_sprite) \
		and arena.daddy_victory_animator != null \
		and is_instance_valid(arena.daddy_victory_animator))
	if arena == null or arena.daddy_victory_sprite == null \
			or not is_instance_valid(arena.daddy_victory_sprite) \
			or arena.daddy_victory_animator == null \
			or not is_instance_valid(arena.daddy_victory_animator):
		return
	var sprite: Sprite3D = arena.daddy_victory_sprite
	var animator: DaddySpriteLoop = arena.daddy_victory_animator
	_ck(label + " Daddy victory cameo starts hidden", \
		not sprite.visible and sprite.name == &"DaddyVictoryCameo")
	_ck(label + " Daddy victory cameo starts on idle atlas", \
		sprite.texture == DADDY_IDLE and sprite.hframes == 4 \
		and sprite.vframes == 2 and sprite.frame == 0)
	_ck(label + " Daddy victory cameo starts in idle state", \
		animator.animation_state() == "idle" \
		and String(sprite.get_meta(&"daddy_animation_state", "")) == "idle")
	_ck(label + " hidden Daddy victory cameo does not process", \
		not animator.is_processing() \
		and not bool(sprite.get_meta(&"daddy_animation_processing", true)))
	_ck(label + " Daddy victory cameo has not played", \
		int(sprite.get_meta(&"daddy_victory_play_count", 0)) == 0)

func _check_daddy_victory(label: String, arena: CombatArena) -> void:
	_ck(label + " Daddy victory cameo remains valid", arena != null \
		and arena.daddy_victory_sprite != null \
		and is_instance_valid(arena.daddy_victory_sprite) \
		and arena.daddy_victory_animator != null \
		and is_instance_valid(arena.daddy_victory_animator))
	if arena == null or arena.daddy_victory_sprite == null \
			or not is_instance_valid(arena.daddy_victory_sprite) \
			or arena.daddy_victory_animator == null \
			or not is_instance_valid(arena.daddy_victory_animator):
		return
	var sprite: Sprite3D = arena.daddy_victory_sprite
	var animator: DaddySpriteLoop = arena.daddy_victory_animator
	_ck(label + " Daddy victory atlas and state activate", \
		sprite.visible and sprite.texture == DADDY_VICTORY \
		and sprite.hframes == 4 and sprite.vframes == 2 \
		and animator.animation_state() == "victory" \
		and String(sprite.get_meta(&"daddy_animation_state", "")) == "victory")
	_ck(label + " Daddy victory plays exactly once", \
		int(sprite.get_meta(&"daddy_victory_play_count", 0)) == 1)
	var first_frame: int = animator.current_frame()
	var advanced := false
	for i in range(12):
		await process_frame
		if not is_instance_valid(sprite) or not is_instance_valid(animator):
			break
		if animator.current_frame() != first_frame:
			advanced = true
			break
	_ck(label + " Daddy victory advances before arena exit", \
		advanced and arena.state == "won")
	if is_instance_valid(sprite):
		_ck(label + " Daddy victory remains one-shot while animating", \
			int(sprite.get_meta(&"daddy_victory_play_count", 0)) == 1)

func _ice_case() -> void:
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("ice arena starts with eight surrounding imps", arena != null and arena.enemies.size() == 8)
	_check_daddy_prebuilt("ice", arena)
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
	var hp_before: int = int(arena.boss["hp"])
	arena.boss["phase"] = "shell"
	arena._hit_boss()
	_check_daddy_prebuilt("fire", arena)
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
