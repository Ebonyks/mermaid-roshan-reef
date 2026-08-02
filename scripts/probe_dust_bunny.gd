extends SceneTree
# Import/runtime contract for the animated dust-bunny enemy project.

var failures: int = 0


func _init() -> void:
	await _run()


func _ck(label: String, ok: bool, detail: String = "") -> void:
	if ok:
		print("OK  ", label, " ", detail)
	else:
		failures += 1
		print("FAIL ", label, " ", detail)


func _run() -> void:
	_ck(
		"animation atlases import",
		ResourceLoader.exists("res://assets/sprites/dust_bunnies/dust_bunny_idle.png")
			and ResourceLoader.exists("res://assets/sprites/dust_bunnies/dust_bunny_hop.png")
			and ResourceLoader.exists("res://assets/sprites/dust_bunnies/dust_bunny_defeat.png")
	)
	var bunny: DustBunnySprite = DustBunnySprite.new()
	root.add_child(bunny)
	await process_frame
	_ck("animated card created", bunny.sprite is AnimatedSprite3D)
	var frames: SpriteFrames = bunny.sprite.sprite_frames
	_ck("idle has six frames", frames.get_frame_count(&"idle") == 6)
	_ck("hop has six frames", frames.get_frame_count(&"hop") == 6)
	_ck("defeat has six frames", frames.get_frame_count(&"defeat") == 6)
	_ck("idle loops", frames.get_animation_loop(&"idle"))
	_ck("hop is one shot", not frames.get_animation_loop(&"hop"))
	_ck("defeat is one shot", not frames.get_animation_loop(&"defeat"))
	_ck("paint stays unshaded", not bunny.sprite.shaded)
	_ck("card faces camera", bunny.sprite.billboard == BaseMaterial3D.BILLBOARD_ENABLED)
	_ck("card casts no shadow",
		bunny.sprite.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
	_ck("enemy groups registered",
		bunny.is_in_group(&"enemy") and bunny.is_in_group(&"dust_bunny_enemy"))
	var duration: float = bunny.play_hop(-1.0)
	_ck("hop action starts", duration > 0.6 and bunny.action_locked
		and bunny.sprite.animation == &"hop" and bunny.sprite.flip_h)
	bunny.action_locked = false
	var defeat_duration: float = bunny.play_defeat(1.0)
	_ck("defeat action starts", defeat_duration >= 0.7 and bunny.action_locked
		and bunny.defeated and bunny.sprite.animation == &"defeat")
	bunny._on_animation_finished()
	_ck("clean sparkle hides card", not bunny.sprite.visible and bunny.defeated)

	var ai_a: DustBunnyAI = DustBunnyAI.new()
	var ai_b: DustBunnyAI = DustBunnyAI.new()
	var start := Vector3.ZERO
	var center := Vector3.ZERO
	var target := Vector3(4.0, 0.0, 0.0)
	ai_a.setup(start, center, 6.0, 4242, 0.0)
	ai_b.setup(start, center, 6.0, 4242, 0.0)
	var actions: int = 0
	var bumps: int = 0
	var landings: int = 0
	var max_height: float = 0.0
	var deterministic: bool = true
	var contained: bool = true
	for _step in range(360):
		var out_a: Dictionary = ai_a.tick(1.0 / 60.0, target)
		var out_b: Dictionary = ai_b.tick(1.0 / 60.0, target)
		if StringName(out_a["action"]) == &"hop":
			actions += 1
		if bool(out_a["bump"]):
			bumps += 1
		if bool(out_a["landed"]):
			landings += 1
		max_height = maxf(max_height, ai_a.pos.y)
		var horizontal := Vector2(ai_a.pos.x, ai_a.pos.z)
		contained = contained and horizontal.length() <= 6.001
		deterministic = deterministic and ai_a.pos.is_equal_approx(ai_b.pos) \
			and out_a == out_b
	_ck("idle-to-hop state machine runs", actions >= 4 and landings >= 3,
		"actions=%d landings=%d" % [actions, landings])
	_ck("hop has readable arc", max_height > 1.2, "height=%.2f" % max_height)
	_ck("enemy reports gentle shield bump", bumps >= 1, "bumps=%d" % bumps)
	_ck("enemy stays inside arena", contained)
	_ck("seeded motion is deterministic", deterministic)
	_ck("no physics body added",
		bunny.find_children("*", "CollisionObject3D", true, false).is_empty())
	bunny.queue_free()
	if failures == 0:
		print("DUST BUNNY PROBE: ALL OK")
		quit(0)
	else:
		print("DUST BUNNY PROBE: %d FAIL" % failures)
		quit(1)
