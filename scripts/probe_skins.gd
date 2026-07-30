extends SceneTree
# Sprite-only skin audit: classic Roshan uses the animated atlas, alternative
# looks use their illustrated cutouts, and no retired character skeleton loads.

func _count_skeletons(node: Node) -> int:
	var total := 1 if node is Skeleton3D else 0
	for child in node.get_children():
		total += _count_skeletons(child)
	return total

func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	for i in range(15):
		await process_frame
	var pl: Node = main.player
	if _count_skeletons(pl) != 0:
		print("FAIL: retired character skeleton loaded below Roshan")
	for skin_entry in main.SKINS:
		var skin: Dictionary = skin_entry
		var sid := String(skin["id"])
		var sprite_path := String(skin["sprite"])
		pl.set_skin(sid, sprite_path)
		for i in range(3):
			await process_frame
		if sid == "classic":
			if not pl.classic_sprite.visible or pl.skin_sprite.visible:
				print("FAIL: classic skin is not the primary animated sprite")
			var classic_path := String((pl.classic_sprite.texture as Texture2D).resource_path)
			if not classic_path.begins_with("res://assets/characters/roshan_25d/"):
				print("FAIL: classic skin texture is outside the Roshan atlas: ", classic_path)
		else:
			if pl.classic_sprite.visible or not pl.skin_sprite.visible:
				print("FAIL: skin ", sid, " did not select its 2D cutout")
			var actual_path := String((pl.skin_sprite.texture as Texture2D).resource_path)
			if actual_path != sprite_path:
				print("FAIL: skin ", sid, " loaded ", actual_path,
					" instead of ", sprite_path)
	# Career state must never swap the sprite back to a model or hide Roshan.
	pl.set_skin("classic", "")
	pl.set_costume("ballerina")
	await process_frame
	if not pl.classic_sprite.visible or String(pl.costume_id) != "ballerina":
		print("FAIL: sprite disappeared while opera costume state was active")
	pl.clear_costume()
	# The fairy-flight force/restore round trip must return to her chosen skin.
	main.skin_id = "huluu"
	main._apply_skin()
	for i in range(3):
		await process_frame
	pl.set_skin("fairy", main.FAIRY_SKIN_PATH)
	for i in range(3):
		await process_frame
	main._apply_skin()
	for i in range(3):
		await process_frame
	if String(pl.skin_id) != "huluu":
		print("FAIL: skin reverted after forced-skin game (now: ", pl.skin_id, ")")
	else:
		print("skin round-trip ok (huluu kept through forced fairy)")
	if _count_skeletons(pl) != 0:
		print("FAIL: changing skins or costumes introduced a skeleton")
	print("sprite skin audit complete")
	quit()
