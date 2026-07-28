extends SceneTree
# Skin audit: every wardrobe skin keeps the classic controller skeleton live,
# alternate looks use illustrated Sprite3D cards, and the fairy-flight
# force/restore path returns to the skin SHE chose.
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
	for sk in main.SKINS:
		var sid: String = String(sk["id"])
		pl.set_skin(sid, String(sk["sprite"]))
		for i in range(5):
			await process_frame
		if pl.skel == null:
			print("FAIL: skin ", sid, " has no live skeleton")
			continue
		if pl.bone_idx.get("tail4", -1) < 0:
			print("FAIL: skin ", sid, " missing tail bones (not a rigged body)")
		if sid == "fairy":
			if pl.skin_sprite == null or pl.skin_sprite.texture == null or not pl.skin_sprite.visible:
				print("FAIL: fairy skin is not using its Sprite3D card")
			if pl.skin_models.has("fairy"):
				print("FAIL: retired fairy model was instantiated")
	# the fairy-flight force/restore round trip must come back to HER choice
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
	print("skin audit complete")
	quit()
