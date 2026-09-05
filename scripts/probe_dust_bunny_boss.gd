extends SceneTree
# Import/runtime contract for the four-frame dust-bunny first-boss animations.

const BOSS_SHEETS: Array[String] = [
	"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_jump.png",
	"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_laugh_vulnerable.png",
	"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_flinch.png",
	"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_angry.png",
	"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_implode.png",
]

var failures: int = 0
var damage_events: int = 0
var health_events: Array[int] = []
var final_round_speed_events: Array[float] = []


func _init() -> void:
	await _run()


func _ck(label: String, ok: bool, detail: String = "") -> void:
	if ok:
		print("BUNNYBOSS|", label, ": OK ", detail)
	else:
		failures += 1
		print("BUNNYBOSS|", label, ": FAIL ", detail)


func _on_damage_cycle_completed() -> void:
	damage_events += 1


func _on_boss_health_changed(rounds_remaining: int, _total_rounds: int) -> void:
	health_events.append(rounds_remaining)


func _on_final_round_started(speed_multiplier: float) -> void:
	final_round_speed_events.append(speed_multiplier)


func _run() -> void:
	var all_sheets_import: bool = true
	for path: String in BOSS_SHEETS:
		all_sheets_import = all_sheets_import and ResourceLoader.exists(path)
	_ck("five animation atlases import", all_sheets_import)

	var boss: DustBunnyBossSprite = DustBunnyBossSprite.new()
	boss.damage_cycle_completed.connect(_on_damage_cycle_completed)
	boss.boss_health_changed.connect(_on_boss_health_changed)
	boss.final_round_started.connect(_on_final_round_started)
	root.add_child(boss)
	await process_frame
	_ck("boss is one animated 2D card", boss.sprite is AnimatedSprite3D)
	var frames: SpriteFrames = boss.sprite.sprite_frames
	_ck("idle holds one authored frame", frames.get_frame_count(&"idle") == 1)
	for animation: StringName in [
		&"jump", &"laugh_vulnerable", &"angry", &"angry_jump_final", &"implode"
	]:
		_ck(
			"%s has four frames" % animation,
			frames.get_frame_count(animation) == 4
		)
		_ck(
			"%s is a one shot" % animation,
			not frames.get_animation_loop(animation)
		)
	var expected_final_paths: Array[String] = [
		"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_angry.png",
		"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_angry.png",
		"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_jump.png",
		"res://assets/sprites/dust_bunnies/boss/dust_bunny_boss_jump.png",
	]
	var expected_final_regions: Array[Rect2] = [
		Rect2(0.0, 512.0, 512.0, 512.0),
		Rect2(512.0, 512.0, 512.0, 512.0),
		Rect2(512.0, 0.0, 512.0, 512.0),
		Rect2(512.0, 512.0, 512.0, 512.0),
	]
	var final_reuse_ok: bool = true
	for frame_index: int in DustBunnyBossSprite.FRAME_COUNT:
		var frame_texture: Texture2D = frames.get_frame_texture(
			&"angry_jump_final", frame_index
		)
		var atlas: AtlasTexture = frame_texture as AtlasTexture
		final_reuse_ok = final_reuse_ok and atlas != null \
			and atlas.atlas.resource_path == expected_final_paths[frame_index] \
			and atlas.region == expected_final_regions[frame_index]
	_ck("final angry jump reuses approved angry and jump frames", final_reuse_ok)
	for animation: StringName in [&"flinch_1", &"flinch_2", &"flinch_3"]:
		_ck(
			"%s has two distinct reaction frames" % animation,
			frames.get_frame_count(animation) == 2
		)
		_ck(
			"%s is a one shot" % animation,
			not frames.get_animation_loop(animation)
		)
	_ck("idle loops", frames.get_animation_loop(&"idle"))
	_ck("paint stays unshaded", not boss.sprite.shaded)
	_ck("card faces camera", boss.sprite.billboard == BaseMaterial3D.BILLBOARD_ENABLED)
	_ck(
		"card casts no shadow",
		boss.sprite.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	)
	_ck(
		"boss scale is larger than regular bunny",
		boss.sprite.pixel_size * float(DustBunnyBossSprite.FRAME_SIZE.y) > 7.0
	)
	_ck(
		"boss groups registered",
		boss.is_in_group(&"enemy") and boss.is_in_group(&"boss_enemy")
			and boss.is_in_group(&"dust_bunny_boss")
	)
	_ck(
		"health starts as three rounds of three taps",
		boss.boss_health_rounds_remaining == 3
			and boss.damage_rounds_completed == 0
			and DustBunnyBossSprite.REQUIRED_TAPS == 3
			and DustBunnyBossSprite.TOTAL_DAMAGE_ROUNDS == 3
			and not boss.final_round_active
			and is_equal_approx(boss.combat_speed_scale, 1.0)
	)
	var jump_duration: float = boss.play_jump(-1.0)
	_ck("normal-round dust-plume jump starts", jump_duration > 0.6
		and boss.sprite.animation == &"jump" and boss.sprite.flip_h)
	boss._on_animation_finished()
	_ck(
		"three tap sounds use one positional SFX player",
		boss.tap_sfx_player is AudioStreamPlayer3D
			and boss.tap_sfx_player.bus == &"SFX"
			and boss.tap_sfx_player.max_polyphony == 3
	)
	_ck("protected boss rejects taps", not boss.register_vulnerable_tap())

	var laugh_duration: float = boss.play_vulnerable_laugh()
	_ck(
		"laugh begins protected",
		laugh_duration >= 0.7 and boss.action_locked and not boss.vulnerable
			and boss.sprite.animation == &"laugh_vulnerable"
	)
	boss.sprite.frame = 1
	boss._on_frame_changed()
	_ck(
		"head flash opens a short three-tap window",
		boss.vulnerable and boss.vulnerability_time_left >= 0.5
			and boss.vulnerability_time_left <= 1.0
	)

	var tap_one: bool = boss.register_vulnerable_tap()
	_ck(
		"tap one has its own flinch and sound",
		tap_one and boss.accepted_taps == 1 and boss.vulnerable
			and boss.sprite.animation == &"flinch_1"
			and boss.last_tap_sfx_path == "res://assets/audio/ui_tap.ogg"
	)
	boss._on_animation_finished()
	_ck(
		"tap one returns to exposed laugh",
		boss.vulnerable and boss.sprite.animation == &"laugh_vulnerable"
			and not boss.sprite.is_playing()
	)

	var tap_two: bool = boss.register_vulnerable_tap()
	_ck(
		"tap two has its own stronger flinch and sound",
		tap_two and boss.accepted_taps == 2 and boss.vulnerable
			and boss.sprite.animation == &"flinch_2"
			and boss.last_tap_sfx_path == "res://assets/audio/hop_boing.ogg"
	)
	boss._on_animation_finished()
	_ck(
		"tap two returns to exposed laugh",
		boss.vulnerable and boss.sprite.animation == &"laugh_vulnerable"
			and not boss.sprite.is_playing()
	)

	var tap_three: bool = boss.register_vulnerable_tap()
	_ck(
		"tap three has its own final flinch and sound",
		tap_three and boss.accepted_taps == 3 and not boss.vulnerable
			and boss.sprite.animation == &"flinch_3"
			and boss.last_tap_sfx_path == "res://assets/audio/chime.ogg"
	)
	_ck(
		"first three taps remove one of three health rounds",
		damage_events == 1 and boss.damage_rounds_completed == 1
			and boss.boss_health_rounds_remaining == 2
			and health_events == [2] and not boss.final_round_active
	)
	boss._on_animation_finished()
	_ck(
		"first damage round recycles through normal anger",
		boss.sprite.animation == &"angry" and boss.accepted_taps == 0
	)
	boss._on_animation_finished()

	boss.play_vulnerable_laugh()
	boss.sprite.frame = 1
	boss._on_frame_changed()
	for tap_number: int in range(1, DustBunnyBossSprite.REQUIRED_TAPS + 1):
		var accepted: bool = boss.register_vulnerable_tap()
		_ck(
			"second round tap %d accepted" % tap_number,
			accepted and boss.sprite.animation == StringName(
				"flinch_%d" % tap_number
			)
		)
		boss._on_animation_finished()
	_ck(
		"second damage round starts the faster final round",
		damage_events == 2 and boss.damage_rounds_completed == 2
			and boss.boss_health_rounds_remaining == 1
			and health_events == [2, 1] and boss.final_round_active
			and is_equal_approx(
				boss.combat_speed_scale,
				DustBunnyBossSprite.FINAL_ROUND_SPEED_SCALE
			)
			and final_round_speed_events == [
				DustBunnyBossSprite.FINAL_ROUND_SPEED_SCALE
			]
	)
	_ck(
		"last round replaces anger with the powerful angry jump",
		boss.sprite.animation == &"angry_jump_final"
			and is_equal_approx(
				boss.sprite.speed_scale,
				DustBunnyBossSprite.FINAL_ROUND_SPEED_SCALE
			)
			and boss.animation_duration(&"angry_jump_final") < 0.5
	)
	boss._on_animation_finished()

	var final_laugh_duration: float = boss.play_vulnerable_laugh()
	boss.sprite.frame = 1
	boss._on_frame_changed()
	_ck(
		"final-round tell and tap window are faster but fair",
		final_laugh_duration < laugh_duration
			and final_laugh_duration >= 0.5
			and is_equal_approx(
				boss.vulnerability_time_left,
				DustBunnyBossSprite.FINAL_ROUND_VULNERABILITY_WINDOW
			)
	)
	boss.register_vulnerable_tap()
	boss._process(DustBunnyBossSprite.FINAL_ROUND_VULNERABILITY_WINDOW + 0.01)
	_ck(
		"missed final window resets through angry jump without damage",
		not boss.vulnerable and boss.accepted_taps == 0
			and boss.sprite.animation == &"angry_jump_final"
			and damage_events == 2 and boss.boss_health_rounds_remaining == 1
	)
	boss._on_animation_finished()

	boss.play_vulnerable_laugh()
	boss.sprite.frame = 1
	boss._on_frame_changed()
	for tap_number: int in range(1, DustBunnyBossSprite.REQUIRED_TAPS + 1):
		var accepted: bool = boss.register_vulnerable_tap()
		_ck(
			"final round tap %d accepted" % tap_number,
			accepted and boss.sprite.animation == StringName(
				"flinch_%d" % tap_number
			)
		)
		boss._on_animation_finished()
	_ck(
		"three rounds of three end in the full-speed implosion",
		damage_events == 3 and boss.damage_rounds_completed == 3
			and boss.boss_health_rounds_remaining == 0
			and health_events == [2, 1, 0]
			and boss.defeated and boss.action_locked
			and boss.sprite.animation == &"implode"
			and is_equal_approx(boss.sprite.speed_scale, 1.0)
			and boss.animation_duration(&"implode") > 0.6
	)
	boss._on_animation_finished()
	_ck("final wisps remove the card", boss.defeated and not boss.sprite.visible)
	_ck("boss art adds no mesh", boss.find_children("*", "MeshInstance3D", true, false).is_empty())
	_ck("boss art adds no physics body",
		boss.find_children("*", "CollisionObject3D", true, false).is_empty())
	boss.queue_free()
	await _check_counter_mode()

	if failures == 0:
		print("BUNNYBOSS|result: ALL OK")
		quit(0)
	else:
		print("BUNNYBOSS|result: %d FAIL" % failures)
		quit(1)


func _check_counter_mode() -> void:
	var counter: DustBunnyBossSprite = DustBunnyBossSprite.new()
	root.add_child(counter)
	await process_frame
	counter.configure_counter_mode(2.4)
	_ck("counter cannot hit a shielded head", not counter.register_counter_tap())
	for round_index in range(3):
		counter.play_vulnerable_laugh()
		counter.sprite.frame = 1
		counter._on_frame_changed()
		_ck("counter opening remains generous in every phase",
			is_equal_approx(counter.vulnerability_time_left, 2.4))
		_ck("one counter removes exactly one round",
			counter.register_counter_tap()
			and counter.damage_rounds_completed == round_index + 1)
		_ck("counter closes immediately against duplicate input",
			not counter.register_counter_tap() and not counter.register_vulnerable_tap())
		_ck("counter starts approved first flinch", counter.sprite.animation == &"flinch_1")
		counter._on_animation_finished()
		_ck("counter retains approved second flinch", counter.sprite.animation == &"flinch_2")
		counter._on_animation_finished()
		_ck("counter retains approved third flinch", counter.sprite.animation == &"flinch_3")
		counter._on_animation_finished()
		if round_index < 2:
			counter._on_animation_finished()
	_ck("third counter ends in approved implosion",
		counter.defeated and counter.sprite.animation == &"implode")
	counter.queue_free()
